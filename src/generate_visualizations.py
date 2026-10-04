import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# ============================================================
# PHASE 5 — VISUALIZATION GENERATION
# Robust visualization generator for SNA Diffusion Case Study
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
VIS_DIR = os.path.join(BASE_DIR, "visualizations")

os.makedirs(VIS_DIR, exist_ok=True)


# ============================================================
# CONFIGURATION
# ============================================================

plt.rcParams["figure.dpi"] = 120
plt.rcParams["savefig.dpi"] = 300
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.25


print("=" * 70)
print("PHASE 5 — VISUALIZATION GENERATION")
print("=" * 70)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_result(filename):
    """
    Load a result CSV safely.
    """
    path = os.path.join(RESULTS_DIR, filename)

    if not os.path.exists(path):
        print(f"WARNING: Missing file: {filename}")
        return None

    try:
        df = pd.read_csv(path)
        print(f"Loaded: {filename}")
        return df
    except Exception as e:
        print(f"ERROR loading {filename}: {e}")
        return None


def save_plot(filename):
    """
    Save current matplotlib figure.
    """
    path = os.path.join(VIS_DIR, filename)

    plt.tight_layout()
    plt.savefig(
        path,
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()

    print(f"Created: {filename}")


def require_columns(df, columns, filename):
    """
    Check whether required columns exist.
    """
    missing = [col for col in columns if col not in df.columns]

    if missing:
        print(
            f"WARNING: {filename} is missing columns: {missing}"
        )
        print(f"Available columns: {list(df.columns)}")
        return False

    return True


def clean_month_column(df, column="month"):
    """
    Convert month column to string safely.
    """
    if column in df.columns:
        df[column] = df[column].astype(str)

    return df


def numeric_columns(df, excluded=None):
    """
    Return numeric columns excluding specified columns.
    """
    if excluded is None:
        excluded = []

    return [
        col
        for col in df.columns
        if col not in excluded
        and pd.api.types.is_numeric_dtype(df[col])
    ]


# ============================================================
# 1. MONTHLY INTERACTION ACTIVITY
# ============================================================

print("\n[1/14] Monthly interaction activity")

df = load_result("temporal_monthly_activity.csv")

if df is not None and require_columns(
    df,
    ["month", "interaction_count"],
    "temporal_monthly_activity.csv"
):

    df = clean_month_column(df)

    plt.figure(figsize=(10, 6))

    plt.plot(
        df["month"],
        df["interaction_count"],
        marker="o",
        linewidth=2
    )

    plt.title("Monthly Interaction Activity")
    plt.xlabel("Month")
    plt.ylabel("Number of Interactions")
    plt.xticks(rotation=45)
    plt.grid(alpha=0.25)

    save_plot("01_monthly_interaction_activity.png")


# ============================================================
# 2. INTERACTION TYPES OVER TIME
# ============================================================

print("\n[2/14] Interaction types over time")

df = load_result("temporal_interaction_types.csv")

if df is not None and "month" in df.columns:

    df = clean_month_column(df)

    # Phase 4 produces this file in WIDE format:
    #
    # month | Comment | CrossPlatformShare | Like | Share
    #
    # We therefore directly plot the interaction columns.

    interaction_columns = [
        "Comment",
        "CrossPlatformShare",
        "Like",
        "Share"
    ]

    available = [
        col for col in interaction_columns
        if col in df.columns
    ]

    if available:

        plt.figure(figsize=(11, 6))

        for column in available:

            plt.plot(
                df["month"],
                df[column],
                marker="o",
                linewidth=2,
                label=column
            )

        plt.title("Interaction Types Over Time")
        plt.xlabel("Month")
        plt.ylabel("Number of Interactions")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(alpha=0.25)

        save_plot("02_interaction_types_over_time.png")

    else:
        print(
            "WARNING: No recognized interaction-type columns found."
        )


# ============================================================
# 3. PLATFORM ACTIVITY OVER TIME
# ============================================================

print("\n[3/14] Platform activity over time")

df = load_result("temporal_platform_activity.csv")

if df is not None and "month" in df.columns:

    df = clean_month_column(df)

    # Phase 4 produces this in WIDE format:
    #
    # month | Facebook | Instagram | Reddit | X | YouTube

    platform_columns = [
        "Facebook",
        "Instagram",
        "Reddit",
        "X",
        "YouTube"
    ]

    available = [
        col for col in platform_columns
        if col in df.columns
    ]

    if available:

        plt.figure(figsize=(11, 6))

        for platform in available:

            plt.plot(
                df["month"],
                df[platform],
                marker="o",
                linewidth=2,
                label=platform
            )

        plt.title("Platform Activity Over Time")
        plt.xlabel("Month")
        plt.ylabel("Number of Interactions")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(alpha=0.25)

        save_plot("03_platform_activity_over_time.png")

    else:
        print(
            "WARNING: No recognized platform columns found."
        )


# ============================================================
# 4. ACTIVITY BY HOUR
# ============================================================

print("\n[4/14] Activity by hour")

df = load_result("temporal_hourly_activity.csv")

if df is not None and require_columns(
    df,
    ["hour", "interaction_count"],
    "temporal_hourly_activity.csv"
):

    df = df.sort_values("hour")

    plt.figure(figsize=(11, 6))

    plt.bar(
        df["hour"],
        df["interaction_count"]
    )

    plt.title("Interaction Activity by Hour")
    plt.xlabel("Hour of Day")
    plt.ylabel("Number of Interactions")
    plt.xticks(range(24))
    plt.grid(axis="y", alpha=0.25)

    save_plot("04_activity_by_hour.png")


# ============================================================
# 5. ACTIVITY BY DAY OF WEEK
# ============================================================

print("\n[5/14] Activity by day of week")

df = load_result("temporal_weekday_activity.csv")

if df is not None and require_columns(
    df,
    ["day_of_week", "interaction_count"],
    "temporal_weekday_activity.csv"
):

    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    df["day_of_week"] = pd.Categorical(
        df["day_of_week"],
        categories=weekday_order,
        ordered=True
    )

    df = df.sort_values("day_of_week")

    plt.figure(figsize=(10, 6))

    plt.bar(
        df["day_of_week"],
        df["interaction_count"]
    )

    plt.title("Interaction Activity by Day of Week")
    plt.xlabel("Day of Week")
    plt.ylabel("Number of Interactions")
    plt.xticks(rotation=30)
    plt.grid(axis="y", alpha=0.25)

    save_plot("05_activity_by_day_of_week.png")


# ============================================================
# 6. CASCADE SIZE DISTRIBUTION
# ============================================================

print("\n[6/14] Cascade size distribution")

df = load_result("cascade_analysis.csv")

if df is not None and require_columns(
    df,
    ["cascade_size"],
    "cascade_analysis.csv"
):

    plt.figure(figsize=(10, 6))

    plt.hist(
        df["cascade_size"].dropna(),
        bins=20,
        edgecolor="black"
    )

    plt.title("Distribution of Information Cascade Sizes")
    plt.xlabel("Cascade Size")
    plt.ylabel("Number of Cascades")
    plt.grid(axis="y", alpha=0.25)

    save_plot("06_cascade_size_distribution.png")


# ============================================================
# 7. CASCADE DURATION DISTRIBUTION
# ============================================================

print("\n[7/14] Cascade duration distribution")

if df is not None and require_columns(
    df,
    ["duration_hours"],
    "cascade_analysis.csv"
):

    plt.figure(figsize=(10, 6))

    plt.hist(
        df["duration_hours"].dropna(),
        bins=20,
        edgecolor="black"
    )

    plt.title("Distribution of Information Cascade Duration")
    plt.xlabel("Duration (Hours)")
    plt.ylabel("Number of Cascades")
    plt.grid(axis="y", alpha=0.25)

    save_plot("07_cascade_duration_distribution.png")


# ============================================================
# 8. CROSS-PLATFORM DIFFUSION MATRIX
# ============================================================

print("\n[8/14] Cross-platform diffusion matrix")

df = load_result("platform_diffusion_matrix.csv")

if df is not None:

    # The matrix may contain:
    #
    # source_platform, Facebook, Instagram, Reddit, X, YouTube
    #
    # or an unnamed first column after CSV export.

    first_column = df.columns[0]

    matrix = df.set_index(first_column)

    # Remove accidental unnamed columns.
    matrix = matrix.loc[
        :,
        ~matrix.columns.astype(str).str.startswith("Unnamed")
    ]

    # Convert matrix values to numeric.
    matrix = matrix.apply(
        pd.to_numeric,
        errors="coerce"
    )

    matrix = matrix.dropna(
        axis=0,
        how="all"
    ).dropna(
        axis=1,
        how="all"
    )

    if matrix.shape[0] > 0 and matrix.shape[1] > 0:

        plt.figure(figsize=(9, 7))

        plt.imshow(
            matrix.values,
            aspect="auto"
        )

        plt.colorbar(
            label="Cross-platform interactions"
        )

        plt.xticks(
            range(len(matrix.columns)),
            matrix.columns,
            rotation=45
        )

        plt.yticks(
            range(len(matrix.index)),
            matrix.index
        )

        plt.xlabel("Target Platform")
        plt.ylabel("Source Platform")

        plt.title(
            "Cross-Platform Information Diffusion"
        )

        # Add values to heatmap.
        for i in range(matrix.shape[0]):

            for j in range(matrix.shape[1]):

                value = matrix.iloc[i, j]

                if pd.notna(value):

                    plt.text(
                        j,
                        i,
                        f"{int(value)}",
                        ha="center",
                        va="center",
                        fontsize=8
                    )

        save_plot(
            "08_cross_platform_diffusion_matrix.png"
        )


# ============================================================
# 9. TOP PLATFORM TRANSITIONS
# ============================================================

print("\n[9/14] Top platform transitions")

df = load_result(
    "platform_diffusion_transitions.csv"
)

if df is not None and require_columns(
    df,
    [
        "source_platform",
        "target_platform",
        "cross_platform_events"
    ],
    "platform_diffusion_transitions.csv"
):

    df = df.copy()

    df["cross_platform_events"] = pd.to_numeric(
        df["cross_platform_events"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["cross_platform_events"]
    )

    df = df.sort_values(
        "cross_platform_events",
        ascending=False
    ).head(10)

    labels = (
        df["source_platform"].astype(str)
        + " → "
        + df["target_platform"].astype(str)
    )

    plt.figure(figsize=(10, 6))

    plt.barh(
        labels.iloc[::-1],
        df["cross_platform_events"].iloc[::-1]
    )

    plt.title(
        "Top Cross-Platform Diffusion Pathways"
    )

    plt.xlabel(
        "Cross-Platform Interactions"
    )

    plt.ylabel(
        "Platform Transition"
    )

    plt.grid(axis="x", alpha=0.25)

    save_plot(
        "09_top_platform_transitions.png"
    )


# ============================================================
# 10. PROPAGATION VS ENGAGEMENT
# ============================================================

print("\n[10/14] Propagation vs engagement")

df = load_result(
    "temporal_propagation_vs_engagement.csv"
)

if df is not None and "month" in df.columns:

    df = clean_month_column(df)

    # The Phase 4 file is expected to be WIDE:
    #
    # month | Engagement | Propagation

    if (
        "Engagement" in df.columns
        and "Propagation" in df.columns
    ):

        plt.figure(figsize=(11, 6))

        plt.plot(
            df["month"],
            df["Engagement"],
            marker="o",
            linewidth=2,
            label="Engagement"
        )

        plt.plot(
            df["month"],
            df["Propagation"],
            marker="o",
            linewidth=2,
            label="Propagation"
        )

        plt.title(
            "Propagation vs Engagement Over Time"
        )

        plt.xlabel("Month")
        plt.ylabel("Number of Interactions")

        plt.xticks(rotation=45)

        plt.legend()

        plt.grid(alpha=0.25)

        save_plot(
            "10_propagation_vs_engagement.png"
        )

    # Fallback for long-format data.
    elif (
        "behavior" in df.columns
        and "count" in df.columns
    ):

        pivot = df.pivot(
            index="month",
            columns="behavior",
            values="count"
        )

        plt.figure(figsize=(11, 6))

        for column in pivot.columns:

            plt.plot(
                pivot.index,
                pivot[column],
                marker="o",
                linewidth=2,
                label=column
            )

        plt.title(
            "Propagation vs Engagement Over Time"
        )

        plt.xlabel("Month")
        plt.ylabel("Number of Interactions")

        plt.xticks(rotation=45)

        plt.legend()

        plt.grid(alpha=0.25)

        save_plot(
            "10_propagation_vs_engagement.png"
        )

    else:

        print(
            "WARNING: Could not identify "
            "Propagation/Engagement columns."
        )


# ============================================================
# 11. MONTHLY PROPAGATION RATE
# ============================================================

print("\n[11/14] Monthly propagation rate")

df = load_result(
    "monthly_propagation_rate.csv"
)

if df is not None and "month" in df.columns:

    df = clean_month_column(df)

    if "propagation_rate" in df.columns:

        rate = pd.to_numeric(
            df["propagation_rate"],
            errors="coerce"
        )

        # Phase 4 stores the rate as a fraction,
        # e.g. 0.4017 = 40.17%.

        plt.figure(figsize=(10, 6))

        plt.plot(
            df["month"],
            rate * 100,
            marker="o",
            linewidth=2
        )

        plt.title(
            "Monthly Information Propagation Rate"
        )

        plt.xlabel("Month")
        plt.ylabel("Propagation Rate (%)")

        plt.xticks(rotation=45)

        plt.grid(alpha=0.25)

        save_plot(
            "11_monthly_propagation_rate.png"
        )

    else:

        print(
            "WARNING: propagation_rate column not found."
        )


# ============================================================
# 12. CROSS-COMMUNITY DIFFUSION BY PLATFORM
# ============================================================

print(
    "\n[12/14] Platform × cross-community diffusion"
)

df = load_result(
    "platform_community_diffusion.csv"
)

if df is not None and require_columns(
    df,
    [
        "source_platform",
        "cross_community_interactions"
    ],
    "platform_community_diffusion.csv"
):

    df["cross_community_interactions"] = pd.to_numeric(
        df["cross_community_interactions"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["cross_community_interactions"]
    )

    plt.figure(figsize=(10, 6))

    plt.bar(
        df["source_platform"],
        df["cross_community_interactions"]
    )

    plt.title(
        "Cross-Community Diffusion by Platform"
    )

    plt.xlabel("Source Platform")

    plt.ylabel(
        "Cross-Community Interactions"
    )

    plt.grid(axis="y", alpha=0.25)

    save_plot(
        "12_cross_community_diffusion_by_platform.png"
    )


# ============================================================
# 13. CASCADE ACTIVITY BY START MONTH
# ============================================================

print(
    "\n[13/14] Cascade activity by start month"
)

df = load_result(
    "temporal_cascade_summary.csv"
)

if df is not None and require_columns(
    df,
    ["start_month", "cascade_count"],
    "temporal_cascade_summary.csv"
):

    df["start_month"] = df[
        "start_month"
    ].astype(str)

    df = df.sort_values("start_month")

    plt.figure(figsize=(10, 6))

    plt.plot(
        df["start_month"],
        df["cascade_count"],
        marker="o",
        linewidth=2
    )

    plt.title(
        "Number of Information Cascades by Start Month"
    )

    plt.xlabel("Cascade Start Month")

    plt.ylabel("Number of Cascades")

    plt.xticks(rotation=45)

    plt.grid(alpha=0.25)

    save_plot(
        "13_cascades_by_start_month.png"
    )


# ============================================================
# 14. COMMUNITY-TO-COMMUNITY DIFFUSION
# ============================================================

print(
    "\n[14/14] Community diffusion heatmap"
)

df = load_result(
    "community_diffusion_matrix.csv"
)

if df is not None:

    first_column = df.columns[0]

    matrix = df.set_index(first_column)

    # Remove accidental unnamed columns.
    matrix = matrix.loc[
        :,
        ~matrix.columns.astype(str).str.startswith("Unnamed")
    ]

    # Convert values to numeric.
    matrix = matrix.apply(
        pd.to_numeric,
        errors="coerce"
    )

    matrix = matrix.dropna(
        axis=0,
        how="all"
    ).dropna(
        axis=1,
        how="all"
    )

    if matrix.shape[0] > 0 and matrix.shape[1] > 0:

        plt.figure(figsize=(12, 10))

        plt.imshow(
            matrix.values,
            aspect="auto"
        )

        plt.colorbar(
            label="Cross-community interactions"
        )

        plt.xticks(
            range(len(matrix.columns)),
            matrix.columns,
            rotation=90,
            fontsize=7
        )

        plt.yticks(
            range(len(matrix.index)),
            matrix.index,
            fontsize=7
        )

        plt.xlabel("Target Community")
        plt.ylabel("Source Community")

        plt.title(
            "Community-to-Community Information Diffusion"
        )

        save_plot(
            "14_community_diffusion_heatmap.png"
        )


# ============================================================
# COMPLETION SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("PHASE 5 COMPLETE")
print("=" * 70)

print("\nVisualizations saved to:")
print(VIS_DIR)


generated_files = sorted(
    [
        filename
        for filename in os.listdir(VIS_DIR)
        if filename.lower().endswith(".png")
    ]
)

print(
    f"\nTotal PNG visualizations currently in folder: "
    f"{len(generated_files)}"
)

for filename in generated_files:
    print(f"  - {filename}")

print("\nAll visualization generation completed.")
print("=" * 70)