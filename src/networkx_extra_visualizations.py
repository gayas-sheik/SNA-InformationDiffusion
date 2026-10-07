import os
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# EXTRA SNA VISUALIZATIONS
# ============================================================

BASE_DIR = r"C:\Users\gayas\Documents\SNA\SNA-CaseStudy"

RESULTS_DIR = os.path.join(
    BASE_DIR,
    "results"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "visualizations"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# DIAGRAM 5
# INFLUENCE VS PAGERANK
# ============================================================

print()
print("==============================================")
print("DIAGRAM 5 — INFLUENCE VS PAGERANK")
print("==============================================")


centrality_file = os.path.join(
    RESULTS_DIR,
    "centrality_analysis.csv"
)

df = pd.read_csv(
    centrality_file
)

print(
    "Loaded users:",
    len(df)
)

print(
    "Columns:",
    df.columns.tolist()
)


# ------------------------------------------------------------
# Calculate correlation
# ------------------------------------------------------------

correlation = df[
    "influence_score"
].corr(
    df["pagerank"]
)

print(
    f"Influence ↔ PageRank correlation: "
    f"{correlation:.4f}"
)


# ------------------------------------------------------------
# Create scatter plot
# ------------------------------------------------------------

plt.figure(
    figsize=(13, 9)
)


# Plot each user type separately so the legend is meaningful.

user_types = sorted(
    df["user_type"].dropna().unique()
)

for user_type in user_types:

    subset = df[
        df["user_type"] == user_type
    ]

    plt.scatter(
        subset["pagerank"],
        subset["influence_score"],
        s=35,
        alpha=0.55,
        label=user_type
    )


# ------------------------------------------------------------
# Add trend line
# ------------------------------------------------------------

x = df["pagerank"]
y = df["influence_score"]

slope, intercept = __import__(
    "numpy"
).polyfit(
    x,
    y,
    1
)

x_line = __import__(
    "numpy"
).linspace(
    x.min(),
    x.max(),
    100
)

y_line = (
    slope * x_line
    + intercept
)

plt.plot(
    x_line,
    y_line,
    linewidth=2,
    linestyle="--",
    label="Linear trend"
)


# ------------------------------------------------------------
# Correlation annotation
# ------------------------------------------------------------

plt.text(
    0.97,
    0.05,
    f"Pearson r = {correlation:.4f}",
    transform=plt.gca().transAxes,
    ha="right",
    va="bottom",
    fontsize=12,
    fontweight="bold",
    bbox=dict(
        facecolor="white",
        edgecolor="gray",
        alpha=0.85
    )
)


# ------------------------------------------------------------
# Labels and title
# ------------------------------------------------------------

plt.title(
    "User Influence vs PageRank\n"
    "Relationship Between Influence and Network Position",
    fontsize=18,
    fontweight="bold",
    pad=20
)

plt.xlabel(
    "PageRank",
    fontsize=12,
    fontweight="bold"
)

plt.ylabel(
    "Influence Score",
    fontsize=12,
    fontweight="bold"
)

plt.legend(
    title="User Type"
)

plt.grid(
    alpha=0.25
)

plt.tight_layout()


# ------------------------------------------------------------
# Save
# ------------------------------------------------------------

output_5 = os.path.join(
    OUTPUT_DIR,
    "networkx_influence_vs_pagerank.png"
)

plt.savefig(
    output_5,
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

plt.close()

print()
print("Diagram 5 created:")
print(output_5)


# ============================================================
# DIAGRAM 6
# PROPAGATION VS ENGAGEMENT OVER TIME
# ============================================================

print()
print("==============================================")
print("DIAGRAM 6 — PROPAGATION VS ENGAGEMENT")
print("==============================================")


temporal_file = os.path.join(
    RESULTS_DIR,
    "temporal_propagation_vs_engagement.csv"
)

temporal = pd.read_csv(
    temporal_file
)

print(
    "Loaded temporal records:",
    len(temporal)
)

print(
    "Columns:",
    temporal.columns.tolist()
)


# ------------------------------------------------------------
# Prepare data
# ------------------------------------------------------------

temporal["month"] = (
    temporal["month"]
    .astype(str)
)

pivot = temporal.pivot(
    index="month",
    columns="behavior",
    values="count"
)

pivot = pivot.sort_index()


# ------------------------------------------------------------
# Create temporal plot
# ------------------------------------------------------------

plt.figure(
    figsize=(13, 8)
)


# Plot every available behavior.

for behavior in pivot.columns:

    plt.plot(
        pivot.index,
        pivot[behavior],
        marker="o",
        linewidth=2.5,
        markersize=6,
        label=behavior
    )


# ------------------------------------------------------------
# Labels and title
# ------------------------------------------------------------

plt.title(
    "Propagation vs Engagement Over Time\n"
    "Monthly Information-Diffusion Activity",
    fontsize=18,
    fontweight="bold",
    pad=20
)

plt.xlabel(
    "Month",
    fontsize=12,
    fontweight="bold"
)

plt.ylabel(
    "Number of Interactions",
    fontsize=12,
    fontweight="bold"
)

plt.xticks(
    rotation=45
)

plt.legend(
    title="Behavior"
)

plt.grid(
    alpha=0.25
)

plt.tight_layout()


# ------------------------------------------------------------
# Save
# ------------------------------------------------------------

output_6 = os.path.join(
    OUTPUT_DIR,
    "networkx_propagation_vs_engagement.png"
)

plt.savefig(
    output_6,
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

plt.close()

print()
print("Diagram 6 created:")
print(output_6)


# ============================================================
# FINAL SUMMARY
# ============================================================

print()
print("==============================================")
print("EXTRA VISUALIZATIONS COMPLETE")
print("==============================================")

print()
print("Created:")

print(
    "1.",
    output_5
)

print(
    "2.",
    output_6
)

print()
print("Both diagrams were saved successfully.")