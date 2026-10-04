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
print("PHASE 4 — TEMPORAL & CROSS-PLATFORM DIFFUSION ANALYSIS")
print("=" * 70)

print("\nLoading datasets...")

users = pd.read_csv(DATA_DIR / "users.csv")
interactions = pd.read_csv(DATA_DIR / "interactions.csv")

interactions["timestamp"] = pd.to_datetime(
    interactions["timestamp"]
)

print(f"Users:        {len(users):,}")
print(f"Interactions: {len(interactions):,}")


# ============================================================
# TEMPORAL OVERVIEW
# ============================================================

print("\n" + "=" * 70)
print("TEMPORAL OVERVIEW")
print("=" * 70)

print(
    f"\nStart: {interactions['timestamp'].min()}"
)

print(
    f"End:   {interactions['timestamp'].max()}"
)

print(
    f"Duration: "
    f"{interactions['timestamp'].max() - interactions['timestamp'].min()}"
)


# ============================================================
# INTERACTIONS BY MONTH
# ============================================================

print("\n" + "=" * 70)
print("INTERACTIONS BY MONTH")
print("=" * 70)

interactions["month"] = (
    interactions["timestamp"]
    .dt.to_period("M")
    .astype(str)
)

monthly = interactions.groupby(
    "month"
).size().reset_index(
    name="interaction_count"
)

print(monthly.to_string(index=False))

monthly.to_csv(
    RESULTS_DIR / "temporal_monthly_activity.csv",
    index=False
)


# ============================================================
# INTERACTIONS BY DAY
# ============================================================

interactions["date"] = (
    interactions["timestamp"].dt.date
)

daily = interactions.groupby(
    "date"
).size().reset_index(
    name="interaction_count"
)

daily["date"] = pd.to_datetime(
    daily["date"]
)

print("\nDaily statistics:")
print(
    daily["interaction_count"]
    .describe()
    .round(3)
)

daily.to_csv(
    RESULTS_DIR / "temporal_daily_activity.csv",
    index=False
)


# ============================================================
# INTERACTION TYPES OVER TIME
# ============================================================

print("\n" + "=" * 70)
print("INTERACTION TYPES OVER TIME")
print("=" * 70)

monthly_types = pd.crosstab(
    interactions["month"],
    interactions["interaction_type"]
)

print(monthly_types)

monthly_types.to_csv(
    RESULTS_DIR / "temporal_interaction_types.csv"
)


# ============================================================
# PLATFORM ACTIVITY OVER TIME
# ============================================================

print("\n" + "=" * 70)
print("PLATFORM ACTIVITY OVER TIME")
print("=" * 70)

monthly_platforms = pd.crosstab(
    interactions["month"],
    interactions["source_platform"]
)

print(monthly_platforms)

monthly_platforms.to_csv(
    RESULTS_DIR / "temporal_platform_activity.csv"
)


# ============================================================
# HOUR OF DAY
# ============================================================

print("\n" + "=" * 70)
print("ACTIVITY BY HOUR")
print("=" * 70)

interactions["hour"] = (
    interactions["timestamp"].dt.hour
)

hourly = interactions.groupby(
    "hour"
).size().reset_index(
    name="interaction_count"
)

print(hourly.to_string(index=False))

hourly.to_csv(
    RESULTS_DIR / "temporal_hourly_activity.csv",
    index=False
)


# ============================================================
# DAY OF WEEK
# ============================================================

print("\n" + "=" * 70)
print("ACTIVITY BY DAY OF WEEK")
print("=" * 70)

interactions["day_of_week"] = (
    interactions["timestamp"].dt.day_name()
)

weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

weekday = interactions.groupby(
    "day_of_week"
).size().reindex(
    weekday_order
).reset_index(
    name="interaction_count"
)

print(weekday.to_string(index=False))

weekday.to_csv(
    RESULTS_DIR / "temporal_weekday_activity.csv",
    index=False
)


# ============================================================
# CASCADE TEMPORAL ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("CASCADE TEMPORAL ANALYSIS")
print("=" * 70)

cascade_records = []

for cascade_id, group in interactions.groupby(
    "cascade_id",
    sort=False
):

    group = group.sort_values("timestamp")

    start = group["timestamp"].iloc[0]
    end = group["timestamp"].iloc[-1]

    duration_seconds = (
        end - start
    ).total_seconds()

    cascade_records.append({

        "cascade_id": cascade_id,

        "start_time": start,

        "end_time": end,

        "duration_hours":
            duration_seconds / 3600,

        "duration_days":
            duration_seconds / 86400,

        "cascade_size":
            len(group),

        "cascade_depth":
            group["cascade_depth"].max(),

        "unique_platforms":
            pd.concat([
                group["source_platform"],
                group["target_platform"]
            ]).nunique(),

        "unique_communities":
            pd.concat([
                group["source_community"],
                group["target_community"]
            ]).nunique(),

        "cross_platform_events":
            (
                group["interaction_type"]
                == "CrossPlatformShare"
            ).sum(),

        "cross_community_events":
            (
                group["source_community"]
                != group["target_community"]
            ).sum()
    })


cascade_df = pd.DataFrame(
    cascade_records
)


# ============================================================
# CASCADE START TIME
# ============================================================

cascade_df["start_month"] = (
    cascade_df["start_time"]
    .dt.to_period("M")
    .astype(str)
)

cascade_monthly = cascade_df.groupby(
    "start_month"
).agg({

    "cascade_id": "count",

    "cascade_size": "mean",

    "cascade_depth": "mean",

    "duration_hours": "mean",

    "unique_platforms": "mean",

    "unique_communities": "mean"

}).rename(
    columns={
        "cascade_id": "cascade_count"
    }
).round(3)

print("\nCascade activity by month:")
print(cascade_monthly)

cascade_monthly.to_csv(
    RESULTS_DIR / "temporal_cascade_summary.csv"
)


# ============================================================
# PLATFORM-TO-PLATFORM DIFFUSION MATRIX
# ============================================================

print("\n" + "=" * 70)
print("PLATFORM-TO-PLATFORM DIFFUSION")
print("=" * 70)

cross_platform = interactions[
    interactions["interaction_type"]
    == "CrossPlatformShare"
].copy()

platform_matrix = pd.crosstab(
    cross_platform["source_platform"],
    cross_platform["target_platform"]
)

print("\nCross-platform event matrix:")
print(platform_matrix)

platform_matrix.to_csv(
    RESULTS_DIR / "platform_diffusion_matrix.csv"
)


# ============================================================
# PLATFORM TRANSITION COUNTS
# ============================================================

platform_transitions = (
    cross_platform
    .groupby([
        "source_platform",
        "target_platform"
    ])
    .size()
    .reset_index(
        name="cross_platform_events"
    )
    .sort_values(
        "cross_platform_events",
        ascending=False
    )
)

print("\nTop platform transitions:")
print(
    platform_transitions.head(20)
    .to_string(index=False)
)

platform_transitions.to_csv(
    RESULTS_DIR / "platform_diffusion_transitions.csv",
    index=False
)


# ============================================================
# COMMUNITY-TO-COMMUNITY DIFFUSION
# ============================================================

print("\n" + "=" * 70)
print("COMMUNITY-TO-COMMUNITY DIFFUSION")
print("=" * 70)

cross_community = interactions[
    interactions["source_community"]
    != interactions["target_community"]
].copy()

community_matrix = pd.crosstab(
    cross_community["source_community"],
    cross_community["target_community"]
)

print(
    f"\nCross-community interactions: "
    f"{len(cross_community):,}"
)

community_matrix.to_csv(
    RESULTS_DIR / "community_diffusion_matrix.csv"
)


# ============================================================
# PLATFORM CROSS-COMMUNITY ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("PLATFORM × CROSS-COMMUNITY DIFFUSION")
print("=" * 70)

platform_community = cross_community.groupby(
    "source_platform"
).agg({

    "interaction_id": "count",

    "target_community": "nunique",

    "target_platform": "nunique"

}).rename(
    columns={
        "interaction_id":
            "cross_community_interactions",

        "target_community":
            "communities_reached",

        "target_platform":
            "platforms_reached"
    }
)

print(platform_community)

platform_community.to_csv(
    RESULTS_DIR / "platform_community_diffusion.csv"
)


# ============================================================
# PROPAGATION VS ENGAGEMENT OVER TIME
# ============================================================

print("\n" + "=" * 70)
print("PROPAGATION VS ENGAGEMENT")
print("=" * 70)

interactions["behavior"] = np.where(
    interactions["interaction_type"].isin(
        ["Share", "CrossPlatformShare"]
    ),
    "Propagation",
    "Engagement"
)

behavior_monthly = pd.crosstab(
    interactions["month"],
    interactions["behavior"]
)

print(behavior_monthly)

behavior_monthly.to_csv(
    RESULTS_DIR / "temporal_propagation_vs_engagement.csv"
)


# ============================================================
# PROPAGATION RATE BY MONTH
# ============================================================

behavior_monthly["total"] = (
    behavior_monthly.sum(axis=1)
)

if "Propagation" in behavior_monthly.columns:

    behavior_monthly[
        "propagation_rate"
    ] = (
        behavior_monthly["Propagation"]
        / behavior_monthly["total"]
    )

print("\nMonthly propagation rate:")

print(
    behavior_monthly[
        ["Propagation", "Engagement", "propagation_rate"]
    ].round(4)
)

behavior_monthly.to_csv(
    RESULTS_DIR / "monthly_propagation_rate.csv"
)


# ============================================================
# FINAL STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("KEY TEMPORAL & CROSS-PLATFORM STATISTICS")
print("=" * 70)

print(
    f"\nCross-platform interactions: "
    f"{len(cross_platform):,}"
)

print(
    f"Cross-community interactions: "
    f"{len(cross_community):,}"
)

print(
    f"Unique source→target platform pairs: "
    f"{len(platform_transitions):,}"
)

print(
    f"Most active hour: "
    f"{hourly.loc[hourly['interaction_count'].idxmax(), 'hour']}:00"
)

print(
    f"Most active weekday: "
    f"{weekday.loc[weekday['interaction_count'].idxmax(), 'day_of_week']}"
)


# ============================================================
# COMPLETE OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("PHASE 4 COMPLETE")
print("=" * 70)

print("\nGenerated files:")

output_files = [
    "temporal_monthly_activity.csv",
    "temporal_daily_activity.csv",
    "temporal_interaction_types.csv",
    "temporal_platform_activity.csv",
    "temporal_hourly_activity.csv",
    "temporal_weekday_activity.csv",
    "temporal_cascade_summary.csv",
    "platform_diffusion_matrix.csv",
    "platform_diffusion_transitions.csv",
    "community_diffusion_matrix.csv",
    "platform_community_diffusion.csv",
    "temporal_propagation_vs_engagement.csv",
    "monthly_propagation_rate.csv"
]

for filename in output_files:
    print(
        RESULTS_DIR / filename
    )

print("\nNext phase:")
print("Visualization generation")