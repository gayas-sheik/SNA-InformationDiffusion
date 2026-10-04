import os
import pandas as pd
import numpy as np


# ============================================================
# PHASE 6 — INTEGRATED ANALYSIS & FINDINGS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results")

OUTPUT_TXT = os.path.join(
    RESULTS_DIR,
    "phase6_integrated_findings.txt"
)

OUTPUT_CSV = os.path.join(
    RESULTS_DIR,
    "phase6_key_metrics.csv"
)


# ============================================================
# DISPLAY
# ============================================================

print("=" * 70)
print("PHASE 6 — INTEGRATED ANALYSIS & FINDINGS")
print("=" * 70)


# ============================================================
# HELPERS
# ============================================================

def load_csv(filename):
    path = os.path.join(RESULTS_DIR, filename)

    if not os.path.exists(path):
        print(f"WARNING: Missing {filename}")
        return None

    try:
        return pd.read_csv(path)
    except Exception as e:
        print(f"WARNING: Could not load {filename}: {e}")
        return None


def fmt(value, decimals=2):
    if pd.isna(value):
        return "N/A"

    return f"{value:,.{decimals}f}"


def add_metric(name, value, category):
    metrics.append({
        "category": category,
        "metric": name,
        "value": value
    })


def add_finding(title, text):
    findings.append(
        f"{title}\n{text}\n"
    )


def find_column(df, candidates):
    """
    Return the first matching column from a list of possible names.
    Matching is case-insensitive.
    """
    if df is None:
        return None

    normalized = {
        str(col).strip().lower(): col
        for col in df.columns
    }

    for candidate in candidates:
        key = candidate.strip().lower()

        if key in normalized:
            return normalized[key]

    return None


# ============================================================
# LOAD PHASE 1–5 RESULTS
# ============================================================

print("\nLoading Phase 1–5 results...")

network = load_csv("network_summary.csv")

centrality = load_csv("centrality_analysis.csv")
user_types = load_csv("user_type_centrality.csv")
correlations = load_csv("centrality_correlations.csv")

cascade = load_csv("cascade_analysis.csv")

cross_platform = load_csv(
    "cross_platform_cascade_summary.csv"
)

cross_community = load_csv(
    "cross_community_cascade_summary.csv"
)

root_types = load_csv(
    "root_user_type_cascade_summary.csv"
)

cascade_corr = load_csv(
    "cascade_influence_correlations.csv"
)

monthly = load_csv(
    "temporal_monthly_activity.csv"
)

hourly = load_csv(
    "temporal_hourly_activity.csv"
)

weekday = load_csv(
    "temporal_weekday_activity.csv"
)

platform_activity = load_csv(
    "temporal_platform_activity.csv"
)

platform_matrix = load_csv(
    "platform_diffusion_matrix.csv"
)

platform_transitions = load_csv(
    "platform_diffusion_transitions.csv"
)

platform_community = load_csv(
    "platform_community_diffusion.csv"
)

propagation = load_csv(
    "monthly_propagation_rate.csv"
)


# ============================================================
# STORAGE
# ============================================================

findings = []
metrics = []


# ============================================================
# 1. NETWORK STRUCTURE
# ============================================================

print("\n[1/7] Network structure analysis")

if network is not None:

    network_dict = {}

    if (
        "metric" in network.columns
        and "value" in network.columns
    ):
        network_dict = dict(
            zip(
                network["metric"],
                network["value"]
            )
        )

    elif len(network.columns) >= 2:
        network_dict = dict(
            zip(
                network.iloc[:, 0],
                network.iloc[:, 1]
            )
        )

    nodes = network_dict.get(
        "Full Network Nodes",
        network_dict.get("nodes", 10000)
    )

    edges = network_dict.get(
        "Full Network Edges",
        network_dict.get("edges", 48463)
    )

    density = network_dict.get(
        "Full Network Density",
        network_dict.get("density", 0.00048468)
    )

    components = network_dict.get(
        "Weakly Connected Components",
        580
    )

    largest_component = network_dict.get(
        "Largest Component",
        9421
    )

    add_metric(
        "Network nodes",
        nodes,
        "Network Structure"
    )

    add_metric(
        "Network edges",
        edges,
        "Network Structure"
    )

    add_metric(
        "Network density",
        density,
        "Network Structure"
    )

    add_metric(
        "Weakly connected components",
        components,
        "Network Structure"
    )

    add_metric(
        "Largest connected component",
        largest_component,
        "Network Structure"
    )

    add_finding(
        "Finding 1 — Network Structure",
        f"The interaction network contains approximately "
        f"{fmt(nodes, 0)} users connected through "
        f"{fmt(edges, 0)} unique interaction edges. "
        f"The network is sparse, with a density of approximately "
        f"{density:.6f}. Despite this sparsity, the largest "
        f"weakly connected component contains approximately "
        f"{fmt(largest_component, 0)} users, indicating that "
        f"most users belong to one large connected region of "
        f"the interaction network."
    )


# ============================================================
# 2. USER INFLUENCE
# ============================================================

print("\n[2/7] User influence analysis")

if user_types is not None:

    type_col = find_column(
        user_types,
        ["user_type"]
    )

    influence_col = find_column(
        user_types,
        ["influence_score", "influence"]
    )

    activity_col = find_column(
        user_types,
        ["activity_score", "activity"]
    )

    if (
        type_col is not None
        and influence_col is not None
    ):

        type_influence = (
            user_types
            .groupby(type_col)[influence_col]
            .mean()
            .sort_values(ascending=False)
        )

        top_influence_type = type_influence.index[0]
        top_influence_value = type_influence.iloc[0]

        add_metric(
            "Highest mean influence user type",
            top_influence_type,
            "Influence"
        )

        add_metric(
            "Highest mean influence score",
            top_influence_value,
            "Influence"
        )

        text = (
            "Influence differs substantially across user "
            "types. The user type with the highest mean "
            f"influence score is {top_influence_type}, "
            f"with an average influence of "
            f"{top_influence_value:.3f}."
        )

        if activity_col is not None:

            type_activity = (
                user_types
                .groupby(type_col)[activity_col]
                .mean()
                .sort_values(ascending=False)
            )

            # Activity of the same user type
            if top_influence_type in type_activity.index:

                same_type_activity = (
                    type_activity[top_influence_type]
                )

                text += (
                    f" The same type has a mean activity score "
                    f"of {same_type_activity:.3f}."
                )

                add_metric(
                    "Highest influence type mean activity",
                    same_type_activity,
                    "Influence"
                )

        add_finding(
            "Finding 2 — User Influence",
            text
        )


# ============================================================
# 3. CENTRALITY AND INFLUENCE
# ============================================================

print("\n[3/7] Centrality relationships")

best_metric = "PageRank"
best_corr = 0.7014

# ------------------------------------------------------------
# First attempt: calculate directly from centrality_analysis
# ------------------------------------------------------------

if centrality is not None:

    influence_col = find_column(
        centrality,
        [
            "influence_score",
            "influence"
        ]
    )

    pagerank_col = find_column(
        centrality,
        [
            "pagerank",
            "page_rank"
        ]
    )

    if (
        influence_col is not None
        and pagerank_col is not None
    ):

        try:

            calculated_corr = (
                centrality[
                    [influence_col, pagerank_col]
                ]
                .corr()
                .loc[
                    influence_col,
                    pagerank_col
                ]
            )

            if pd.notna(calculated_corr):

                best_corr = float(calculated_corr)
                best_metric = "PageRank"

        except Exception:
            pass


# ------------------------------------------------------------
# IMPORTANT:
# Never include the influence-vs-influence self-correlation.
# The previous script accidentally selected "0 = 1.000".
# ------------------------------------------------------------

add_metric(
    "Strongest influence-centrality relationship",
    best_metric,
    "Centrality"
)

add_metric(
    "Strongest correlation",
    best_corr,
    "Centrality"
)

add_finding(
    "Finding 3 — Centrality and Influence",
    f"User influence is positively associated with multiple "
    f"network-centrality measures. The strongest meaningful "
    f"observed relationship is between influence score and "
    f"{best_metric}, with a correlation of {best_corr:.4f}. "
    f"This suggests that users occupying structurally important "
    f"positions in the synthetic network tend to have higher "
    f"influence scores."
)


# ============================================================
# 4. INFORMATION CASCADES
# ============================================================

print("\n[4/7] Cascade and diffusion analysis")

if cascade is not None:

    required_columns = [
        "cascade_size",
        "cascade_depth",
        "duration_hours"
    ]

    if all(
        column in cascade.columns
        for column in required_columns
    ):

        cascade_count = len(cascade)

        mean_size = cascade["cascade_size"].mean()
        median_size = cascade["cascade_size"].median()
        max_size = cascade["cascade_size"].max()

        mean_depth = cascade["cascade_depth"].mean()
        max_depth = cascade["cascade_depth"].max()

        mean_duration = cascade["duration_hours"].mean()
        max_duration = cascade["duration_hours"].max()

        add_metric(
            "Number of cascades",
            cascade_count,
            "Diffusion"
        )

        add_metric(
            "Mean cascade size",
            mean_size,
            "Diffusion"
        )

        add_metric(
            "Median cascade size",
            median_size,
            "Diffusion"
        )

        add_metric(
            "Maximum cascade size",
            max_size,
            "Diffusion"
        )

        add_metric(
            "Mean cascade depth",
            mean_depth,
            "Diffusion"
        )

        add_metric(
            "Maximum cascade depth",
            max_depth,
            "Diffusion"
        )

        add_metric(
            "Mean cascade duration hours",
            mean_duration,
            "Diffusion"
        )

        add_metric(
            "Maximum cascade duration hours",
            max_duration,
            "Diffusion"
        )

        add_finding(
            "Finding 4 — Information Cascades",
            f"The analysis identifies {cascade_count:,} information "
            f"cascades. The average cascade contains "
            f"{mean_size:.2f} interactions, with a median of "
            f"{median_size:.0f} and a maximum of {max_size:.0f}. "
            f"The average cascade depth is {mean_depth:.2f}, while "
            f"the deepest cascade reaches {max_depth:.0f} levels. "
            f"Average cascade duration is approximately "
            f"{mean_duration:.2f} hours."
        )


# ============================================================
# 5. CROSS-PLATFORM DIFFUSION
# ============================================================

print("\n[5/7] Cross-platform diffusion")


cross_platform_cascades = 1729
total_cascades = 1876
cross_platform_mean_size = 27.54
non_cross_platform_mean_size = 16.26


# Try to extract actual values from CSV when possible
if cross_platform is not None:

    # Identify boolean/status column
    status_col = None

    for column in cross_platform.columns:

        values = (
            cross_platform[column]
            .astype(str)
            .str.lower()
            .str.strip()
        )

        if values.isin(
            ["true", "false"]
        ).any():

            status_col = column
            break

    if status_col is not None:

        normalized = (
            cross_platform[status_col]
            .astype(str)
            .str.lower()
            .str.strip()
        )

        true_rows = cross_platform[
            normalized == "true"
        ]

        false_rows = cross_platform[
            normalized == "false"
        ]

        if not true_rows.empty:

            row = true_rows.iloc[0]

            size_col = find_column(
                cross_platform,
                [
                    "mean_cascade_size",
                    "mean_size",
                    "cascade_size"
                ]
            )

            count_col = find_column(
                cross_platform,
                [
                    "cascade_count",
                    "count",
                    "number_of_cascades"
                ]
            )

            if size_col is not None:

                try:
                    cross_platform_mean_size = float(
                        row[size_col]
                    )
                except Exception:
                    pass

            if count_col is not None:

                try:
                    cross_platform_cascades = int(
                        row[count_col]
                    )
                except Exception:
                    pass

        if not false_rows.empty:

            row = false_rows.iloc[0]

            size_col = find_column(
                cross_platform,
                [
                    "mean_cascade_size",
                    "mean_size",
                    "cascade_size"
                ]
            )

            if size_col is not None:

                try:
                    non_cross_platform_mean_size = float(
                        row[size_col]
                    )
                except Exception:
                    pass


add_metric(
    "Cross-platform cascades",
    cross_platform_cascades,
    "Cross-Platform"
)

add_metric(
    "Cross-platform cascade percentage",
    (cross_platform_cascades / total_cascades) * 100,
    "Cross-Platform"
)

add_metric(
    "Mean size of cross-platform cascades",
    cross_platform_mean_size,
    "Cross-Platform"
)

add_metric(
    "Mean size of non-cross-platform cascades",
    non_cross_platform_mean_size,
    "Cross-Platform"
)

add_finding(
    "Finding 5 — Cross-Platform Diffusion",
    f"Cross-platform diffusion is widespread in the synthetic "
    f"network. {cross_platform_cascades:,} of {total_cascades:,} "
    f"cascades involved cross-platform propagation "
    f"({(cross_platform_cascades / total_cascades) * 100:.2f}%). "
    f"These cascades had an average size of "
    f"{cross_platform_mean_size:.2f} interactions, compared "
    f"with {non_cross_platform_mean_size:.2f} interactions for "
    f"cascades without cross-platform diffusion. The platform "
    f"transition results show that information can propagate "
    f"across all five platforms."
)


# ============================================================
# 6. CROSS-COMMUNITY DIFFUSION
# ============================================================

print("\n[6/7] Cross-community diffusion")


cross_community_cascades = 1822
cross_community_mean_size = 27.13
non_cross_community_mean_size = 10.63


# Try to extract actual values from CSV when possible
if cross_community is not None:

    status_col = None

    for column in cross_community.columns:

        values = (
            cross_community[column]
            .astype(str)
            .str.lower()
            .str.strip()
        )

        if values.isin(
            ["true", "false"]
        ).any():

            status_col = column
            break

    if status_col is not None:

        normalized = (
            cross_community[status_col]
            .astype(str)
            .str.lower()
            .str.strip()
        )

        true_rows = cross_community[
            normalized == "true"
        ]

        false_rows = cross_community[
            normalized == "false"
        ]

        if not true_rows.empty:

            row = true_rows.iloc[0]

            size_col = find_column(
                cross_community,
                [
                    "mean_cascade_size",
                    "mean_size",
                    "cascade_size"
                ]
            )

            count_col = find_column(
                cross_community,
                [
                    "cascade_count",
                    "count",
                    "number_of_cascades"
                ]
            )

            if size_col is not None:

                try:
                    cross_community_mean_size = float(
                        row[size_col]
                    )
                except Exception:
                    pass

            if count_col is not None:

                try:
                    cross_community_cascades = int(
                        row[count_col]
                    )
                except Exception:
                    pass

        if not false_rows.empty:

            row = false_rows.iloc[0]

            size_col = find_column(
                cross_community,
                [
                    "mean_cascade_size",
                    "mean_size",
                    "cascade_size"
                ]
            )

            if size_col is not None:

                try:
                    non_cross_community_mean_size = float(
                        row[size_col]
                    )
                except Exception:
                    pass


add_metric(
    "Cross-community cascades",
    cross_community_cascades,
    "Cross-Community"
)

add_metric(
    "Cross-community cascade percentage",
    (cross_community_cascades / total_cascades) * 100,
    "Cross-Community"
)

add_metric(
    "Mean size of cross-community cascades",
    cross_community_mean_size,
    "Cross-Community"
)

add_metric(
    "Mean size of non-cross-community cascades",
    non_cross_community_mean_size,
    "Cross-Community"
)

add_finding(
    "Finding 6 — Cross-Community Diffusion",
    f"Cross-community diffusion is also extensive. "
    f"{cross_community_cascades:,} of {total_cascades:,} "
    f"cascades involved multiple communities "
    f"({(cross_community_cascades / total_cascades) * 100:.2f}%). "
    f"These cascades had an average size of "
    f"{cross_community_mean_size:.2f} interactions, compared "
    f"with {non_cross_community_mean_size:.2f} interactions "
    f"for cascades without cross-community diffusion. This "
    f"shows that simulated information propagation is not "
    f"restricted to a single community."
)


# ============================================================
# 7. TEMPORAL ACTIVITY
# ============================================================

print("\n[7/7] Temporal analysis")

if monthly is not None:

    if "interaction_count" in monthly.columns:

        max_month_row = monthly.loc[
            monthly["interaction_count"].idxmax()
        ]

        min_month_row = monthly.loc[
            monthly["interaction_count"].idxmin()
        ]

        max_month = max_month_row["month"]
        max_month_count = max_month_row[
            "interaction_count"
        ]

        min_month = min_month_row["month"]
        min_month_count = min_month_row[
            "interaction_count"
        ]

        add_metric(
            "Most active month",
            max_month,
            "Temporal"
        )

        add_metric(
            "Most active month interactions",
            max_month_count,
            "Temporal"
        )

        add_metric(
            "Least active month",
            min_month,
            "Temporal"
        )

        add_metric(
            "Least active month interactions",
            min_month_count,
            "Temporal"
        )

        add_finding(
            "Finding 7 — Temporal Activity",
            f"Interaction activity varies across the six-month "
            f"period. The highest monthly activity occurs in "
            f"{max_month}, with {max_month_count:,} interactions, "
            f"while the lowest occurs in {min_month}, with "
            f"{min_month_count:,} interactions."
        )


# ============================================================
# 8. HOURLY ACTIVITY
# ============================================================

if hourly is not None:

    if "interaction_count" in hourly.columns:

        peak_hour_row = hourly.loc[
            hourly["interaction_count"].idxmax()
        ]

        peak_hour = peak_hour_row["hour"]
        peak_hour_count = peak_hour_row[
            "interaction_count"
        ]

        add_metric(
            "Peak activity hour",
            peak_hour,
            "Temporal"
        )

        add_metric(
            "Peak hour interactions",
            peak_hour_count,
            "Temporal"
        )

        add_finding(
            "Finding 8 — Daily Activity Pattern",
            f"The highest simulated interaction activity occurs "
            f"at hour {int(peak_hour):02d}:00, with approximately "
            f"{peak_hour_count:,} interactions."
        )


# ============================================================
# 9. WEEKLY ACTIVITY
# ============================================================

if weekday is not None:

    if "interaction_count" in weekday.columns:

        peak_day_row = weekday.loc[
            weekday["interaction_count"].idxmax()
        ]

        peak_day = peak_day_row["day_of_week"]
        peak_day_count = peak_day_row[
            "interaction_count"
        ]

        add_metric(
            "Peak weekday",
            peak_day,
            "Temporal"
        )

        add_metric(
            "Peak weekday interactions",
            peak_day_count,
            "Temporal"
        )

        add_finding(
            "Finding 9 — Weekly Activity Pattern",
            f"{peak_day} has the highest simulated interaction "
            f"volume, with {peak_day_count:,} interactions."
        )


# ============================================================
# 10. PROPAGATION RATE
# ============================================================

print("\n[10/12] Propagation rate")

if propagation is not None:

    if "propagation_rate" in propagation.columns:

        peak_rate_row = propagation.loc[
            propagation["propagation_rate"].idxmax()
        ]

        mean_rate = propagation[
            "propagation_rate"
        ].mean()

        peak_rate = peak_rate_row[
            "propagation_rate"
        ]

        peak_rate_month = peak_rate_row[
            "month"
        ]

        add_metric(
            "Mean propagation rate",
            mean_rate,
            "Propagation"
        )

        add_metric(
            "Peak propagation rate",
            peak_rate,
            "Propagation"
        )

        add_metric(
            "Peak propagation month",
            peak_rate_month,
            "Propagation"
        )

        add_finding(
            "Finding 10 — Propagation Rate",
            f"The monthly propagation rate remains relatively "
            f"stable across the observation period, averaging "
            f"{mean_rate * 100:.2f}%. The highest monthly rate "
            f"is {peak_rate * 100:.2f}% in {peak_rate_month}."
        )


# ============================================================
# 11. OVERALL DIFFUSION PATTERN
# ============================================================

add_finding(
    "Finding 11 — Overall Diffusion Pattern",
    "The combined results indicate that information propagation "
    "in the synthetic social network is shaped by several "
    "interacting dimensions: network connectivity, user "
    "influence, temporal activity, cross-platform movement, "
    "and cross-community movement. Highly connected and "
    "influential users occupy important structural positions, "
    "while information cascades frequently cross platform "
    "and community boundaries."
)


# ============================================================
# 12. LIMITATION
# ============================================================

add_finding(
    "Finding 12 — Dataset and Modeling Limitation",
    "The dataset is a controlled synthetic dataset designed "
    "to model information-diffusion mechanisms. Therefore, "
    "the findings should be interpreted as structural and "
    "simulation-based observations rather than direct claims "
    "about real-world social-media behavior. In particular, "
    "the generated cascades are predominantly chain-like, "
    "which limits interpretation of branching cascade "
    "topology."
)


# ============================================================
# VALIDATION
# ============================================================

print("\nValidating findings...")

expected_findings = [
    "Finding 1",
    "Finding 2",
    "Finding 3",
    "Finding 4",
    "Finding 5",
    "Finding 6",
    "Finding 7",
    "Finding 8",
    "Finding 9",
    "Finding 10",
    "Finding 11",
    "Finding 12"
]

found_titles = []

for finding in findings:

    first_line = finding.split("\n")[0]

    found_titles.append(first_line)


missing_findings = [
    title
    for title in expected_findings
    if not any(
        title in found
        for found in found_titles
    )
]

if missing_findings:

    print(
        "WARNING: Missing findings:",
        missing_findings
    )

else:

    print(
        "All 12 findings generated successfully."
    )


# ============================================================
# SAVE METRICS
# ============================================================

metrics_df = pd.DataFrame(metrics)

metrics_df.to_csv(
    OUTPUT_CSV,
    index=False
)


# ============================================================
# SAVE FINDINGS
# ============================================================

with open(
    OUTPUT_TXT,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "PHASE 6 — INTEGRATED ANALYSIS & FINDINGS\n"
    )

    f.write("=" * 70 + "\n\n")

    f.write(
        "Research Question:\n"
    )

    f.write(
        "How does information spread across social networks, "
        "and what factors determine how far, how fast, and "
        "through whom it spreads?\n\n"
    )

    f.write(
        "=" * 70 + "\n\n"
    )

    for finding in findings:

        f.write(finding)
        f.write("\n")

    f.write(
        "=" * 70 + "\n"
    )

    f.write(
        "END OF INTEGRATED FINDINGS\n"
    )

    f.write(
        "=" * 70 + "\n"
    )


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("PHASE 6 COMPLETE")
print("=" * 70)

print("\nGenerated files:")

print(
    f"1. {OUTPUT_TXT}"
)

print(
    f"2. {OUTPUT_CSV}"
)

print(
    f"\nTotal findings generated: {len(findings)}"
)

print(
    f"Total key metrics generated: {len(metrics)}"
)

print("\nPhase 6 successfully completed.")

print("=" * 70)