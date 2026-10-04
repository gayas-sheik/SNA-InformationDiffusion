import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data" / "synthetic"
RESULTS_DIR = PROJECT_ROOT / "results"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("PHASE 3 — INFORMATION CASCADE & DIFFUSION ANALYSIS")
print("=" * 70)

print("\nLoading datasets...")

users = pd.read_csv(DATA_DIR / "users.csv")
information = pd.read_csv(DATA_DIR / "information_items.csv")
interactions = pd.read_csv(DATA_DIR / "interactions.csv")

print(f"Users:         {len(users):,}")
print(f"Information:   {len(information):,}")
print(f"Interactions:  {len(interactions):,}")


# ============================================================
# DATETIME CONVERSION
# ============================================================

print("\nPreparing timestamps...")

interactions["timestamp"] = pd.to_datetime(
    interactions["timestamp"]
)


# ============================================================
# BASIC CASCADE VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("CASCADE VALIDATION")
print("=" * 70)

required_columns = [
    "cascade_id",
    "information_id",
    "interaction_id",
    "parent_interaction_id",
    "cascade_depth",
    "timestamp",
    "source_user",
    "target_user",
    "source_platform",
    "target_platform",
    "source_community",
    "target_community",
    "interaction_type"
]

missing_columns = [
    column
    for column in required_columns
    if column not in interactions.columns
]

if missing_columns:
    raise ValueError(
        f"Missing interaction columns: {missing_columns}"
    )

print("Required columns: PASS")


# ============================================================
# CASCADE-LEVEL ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("BUILDING CASCADE-LEVEL DATASET")
print("=" * 70)

cascade_records = []


for cascade_id, group in interactions.groupby(
    "cascade_id",
    sort=False
):

    group = group.sort_values("timestamp")

    first_event = group.iloc[0]
    last_event = group.iloc[-1]

    cascade_size = len(group)

    max_depth = group["cascade_depth"].max()

    duration_seconds = (
        last_event["timestamp"]
        - first_event["timestamp"]
    ).total_seconds()

    duration_hours = duration_seconds / 3600

    duration_days = duration_seconds / 86400

    unique_users = pd.unique(
        pd.concat([
            group["source_user"],
            group["target_user"]
        ])
    )

    unique_platforms = pd.unique(
        pd.concat([
            group["source_platform"],
            group["target_platform"]
        ])
    )

    unique_communities = pd.unique(
        pd.concat([
            group["source_community"],
            group["target_community"]
        ])
    )

    propagation_events = group[
        group["interaction_type"].isin(
            ["Share", "CrossPlatformShare"]
        )
    ]

    cross_platform_events = group[
        group["interaction_type"]
        == "CrossPlatformShare"
    ]

    cross_community_events = group[
        group["source_community"]
        != group["target_community"]
    ]

    cascade_records.append({

        "cascade_id": cascade_id,

        "information_id":
            first_event["information_id"],

        "cascade_size":
            cascade_size,

        "cascade_depth":
            max_depth,

        "duration_seconds":
            duration_seconds,

        "duration_hours":
            duration_hours,

        "duration_days":
            duration_days,

        "unique_users":
            len(unique_users),

        "unique_platforms":
            len(unique_platforms),

        "unique_communities":
            len(unique_communities),

        "propagation_events":
            len(propagation_events),

        "cross_platform_events":
            len(cross_platform_events),

        "cross_community_events":
            len(cross_community_events),

        "cross_platform":
            len(cross_platform_events) > 0,

        "cross_community":
            len(cross_community_events) > 0,

        "source_platform":
            first_event["source_platform"],

        "source_community":
            first_event["source_community"],

        "root_user":
            first_event["source_user"],

        "root_user_type":
            users.loc[
                users["user_id"]
                == first_event["source_user"],
                "user_type"
            ].iloc[0]
            if (
                first_event["source_user"]
                in set(users["user_id"])
            )
            else "Unknown",

        "root_user_influence":
            users.loc[
                users["user_id"]
                == first_event["source_user"],
                "influence_score"
            ].iloc[0]
            if (
                first_event["source_user"]
                in set(users["user_id"])
            )
            else np.nan,

        "root_user_activity":
            users.loc[
                users["user_id"]
                == first_event["source_user"],
                "activity_score"
            ].iloc[0]
            if (
                first_event["source_user"]
                in set(users["user_id"])
            )
            else np.nan

    })


cascade_df = pd.DataFrame(cascade_records)

print(
    f"\nCascades analyzed: "
    f"{len(cascade_df):,}"
)


# ============================================================
# CASCADE SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("CASCADE SIZE & DEPTH")
print("=" * 70)

summary_columns = [
    "cascade_size",
    "cascade_depth",
    "duration_hours",
    "unique_users",
    "unique_platforms",
    "unique_communities",
    "propagation_events",
    "cross_platform_events",
    "cross_community_events"
]

print(
    cascade_df[
        summary_columns
    ].describe().round(3)
)


# ============================================================
# LARGE CASCADES
# ============================================================

print("\n" + "=" * 70)
print("TOP 20 LARGEST CASCADES")
print("=" * 70)

top_cascades = cascade_df.sort_values(
    "cascade_size",
    ascending=False
).head(20)

print(
    top_cascades[
        [
            "cascade_id",
            "information_id",
            "cascade_size",
            "cascade_depth",
            "duration_hours",
            "unique_users",
            "unique_platforms",
            "unique_communities",
            "cross_platform_events",
            "cross_community_events",
            "root_user_type",
            "root_user_influence"
        ]
    ].to_string(index=False)
)


# ============================================================
# PROPAGATION RATE
# ============================================================

print("\n" + "=" * 70)
print("PROPAGATION RATE")
print("=" * 70)

cascade_df["events_per_hour"] = np.where(
    cascade_df["duration_hours"] > 0,
    cascade_df["cascade_size"]
    / cascade_df["duration_hours"],
    np.nan
)

cascade_df["users_per_hour"] = np.where(
    cascade_df["duration_hours"] > 0,
    cascade_df["unique_users"]
    / cascade_df["duration_hours"],
    np.nan
)

print(
    cascade_df[
        [
            "events_per_hour",
            "users_per_hour"
        ]
    ].describe().round(3)
)


# ============================================================
# CROSS-PLATFORM ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("CROSS-PLATFORM DIFFUSION")
print("=" * 70)

cross_platform_summary = cascade_df.groupby(
    "cross_platform"
).agg({

    "cascade_id": "count",

    "cascade_size": "mean",

    "cascade_depth": "mean",

    "duration_hours": "mean",

    "unique_users": "mean",

    "unique_platforms": "mean",

    "unique_communities": "mean",

    "cross_platform_events": "mean"

}).rename(
    columns={
        "cascade_id": "cascade_count"
    }
).round(3)

print(
    cross_platform_summary
)

cross_platform_summary.to_csv(
    RESULTS_DIR / "cross_platform_cascade_summary.csv"
)


# ============================================================
# CROSS-COMMUNITY ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("CROSS-COMMUNITY DIFFUSION")
print("=" * 70)

cross_community_summary = cascade_df.groupby(
    "cross_community"
).agg({

    "cascade_id": "count",

    "cascade_size": "mean",

    "cascade_depth": "mean",

    "duration_hours": "mean",

    "unique_users": "mean",

    "unique_platforms": "mean",

    "unique_communities": "mean",

    "cross_community_events": "mean"

}).rename(
    columns={
        "cascade_id": "cascade_count"
    }
).round(3)

print(
    cross_community_summary
)

cross_community_summary.to_csv(
    RESULTS_DIR / "cross_community_cascade_summary.csv"
)


# ============================================================
# ROOT USER TYPE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("ROOT USER TYPE vs CASCADE PERFORMANCE")
print("=" * 70)

root_type_summary = cascade_df.groupby(
    "root_user_type"
).agg({

    "cascade_id": "count",

    "cascade_size": "mean",

    "cascade_depth": "mean",

    "duration_hours": "mean",

    "unique_users": "mean",

    "unique_platforms": "mean",

    "unique_communities": "mean",

    "propagation_events": "mean",

    "cross_platform_events": "mean",

    "cross_community_events": "mean"

}).rename(
    columns={
        "cascade_id": "cascade_count"
    }
).round(3)

print(
    root_type_summary
)

root_type_summary.to_csv(
    RESULTS_DIR / "root_user_type_cascade_summary.csv"
)


# ============================================================
# ROOT USER INFLUENCE vs CASCADE SIZE
# ============================================================

print("\n" + "=" * 70)
print("ROOT USER INFLUENCE vs CASCADE SIZE")
print("=" * 70)

influence_columns = [
    "root_user_influence",
    "root_user_activity",
    "cascade_size",
    "cascade_depth",
    "unique_users",
    "unique_platforms",
    "unique_communities",
    "duration_hours",
    "propagation_events",
    "cross_platform_events",
    "cross_community_events"
]

influence_correlation = cascade_df[
    influence_columns
].corr(method="pearson").round(4)

print(
    influence_correlation[
        [
            "root_user_influence",
            "root_user_activity"
        ]
    ]
)

influence_correlation.to_csv(
    RESULTS_DIR / "cascade_influence_correlations.csv"
)


# ============================================================
# PLATFORM ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("SOURCE PLATFORM vs CASCADE PERFORMANCE")
print("=" * 70)

platform_summary = cascade_df.groupby(
    "source_platform"
).agg({

    "cascade_id": "count",

    "cascade_size": "mean",

    "cascade_depth": "mean",

    "duration_hours": "mean",

    "unique_users": "mean",

    "unique_platforms": "mean",

    "unique_communities": "mean",

    "cross_platform_events": "mean",

    "cross_community_events": "mean"

}).rename(
    columns={
        "cascade_id": "cascade_count"
    }
).round(3)

print(
    platform_summary
)

platform_summary.to_csv(
    RESULTS_DIR / "platform_cascade_summary.csv"
)


# ============================================================
# INFORMATION ITEM ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("INFORMATION ITEM PROPAGATION")
print("=" * 70)

information_summary = cascade_df.groupby(
    "information_id"
).agg({

    "cascade_id": "count",

    "cascade_size": "mean",

    "cascade_depth": "mean",

    "unique_users": "mean",

    "unique_platforms": "mean",

    "unique_communities": "mean"

}).rename(
    columns={
        "cascade_id": "cascade_count"
    }
).sort_values(
    "cascade_size",
    ascending=False
)

print("\nTop 10 information items by average cascade size:")

print(
    information_summary.head(10)
)

information_summary.to_csv(
    RESULTS_DIR / "information_diffusion_summary.csv"
)


# ============================================================
# SAVE COMPLETE CASCADE DATA
# ============================================================

cascade_df.to_csv(
    RESULTS_DIR / "cascade_analysis.csv",
    index=False
)


# ============================================================
# OVERALL KEY STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("KEY DIFFUSION STATISTICS")
print("=" * 70)

print(
    f"\nTotal cascades: "
    f"{len(cascade_df):,}"
)

print(
    f"Average cascade size: "
    f"{cascade_df['cascade_size'].mean():.2f}"
)

print(
    f"Median cascade size: "
    f"{cascade_df['cascade_size'].median():.2f}"
)

print(
    f"Maximum cascade size: "
    f"{cascade_df['cascade_size'].max():,}"
)

print(
    f"Average cascade depth: "
    f"{cascade_df['cascade_depth'].mean():.2f}"
)

print(
    f"Maximum cascade depth: "
    f"{cascade_df['cascade_depth'].max():,}"
)

print(
    f"Average cascade duration: "
    f"{cascade_df['duration_hours'].mean():.2f} hours"
)

print(
    f"Maximum cascade duration: "
    f"{cascade_df['duration_hours'].max():.2f} hours"
)

print(
    f"Cross-platform cascades: "
    f"{cascade_df['cross_platform'].sum():,}"
)

print(
    f"Cross-community cascades: "
    f"{cascade_df['cross_community'].sum():,}"
)


# ============================================================
# OUTPUT FILES
# ============================================================

print("\n" + "=" * 70)
print("PHASE 3 COMPLETE")
print("=" * 70)

print("\nGenerated files:")

output_files = [
    "cascade_analysis.csv",
    "cross_platform_cascade_summary.csv",
    "cross_community_cascade_summary.csv",
    "root_user_type_cascade_summary.csv",
    "cascade_influence_correlations.csv",
    "platform_cascade_summary.csv",
    "information_diffusion_summary.csv"
]

for filename in output_files:
    print(RESULTS_DIR / filename)

print("\nNext phase:")
print("Temporal diffusion + platform-to-platform propagation analysis")