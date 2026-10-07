import os
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# DIAGRAM 6 — PROPAGATION VS ENGAGEMENT OVER TIME
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
# 1. LOAD TEMPORAL DATA
# ============================================================

file_path = os.path.join(
    RESULTS_DIR,
    "temporal_propagation_vs_engagement.csv"
)

df = pd.read_csv(file_path)

print("Loaded temporal records:", len(df))

print(
    "Columns:",
    df.columns.tolist()
)


# ============================================================
# 2. PREPARE MONTH ORDER
# ============================================================

df["month"] = df["month"].astype(str)

month_order = [
    "2026-01",
    "2026-02",
    "2026-03",
    "2026-04",
    "2026-05",
    "2026-06"
]

df["month"] = pd.Categorical(
    df["month"],
    categories=month_order,
    ordered=True
)

df = df.sort_values("month")


# ============================================================
# 3. CREATE FIGURE
# ============================================================

plt.figure(
    figsize=(14, 8)
)


# ============================================================
# 4. PLOT ENGAGEMENT
# ============================================================

plt.plot(
    df["month"],
    df["Engagement"],
    marker="o",
    linewidth=2.5,
    markersize=8,
    label="Engagement"
)


# ============================================================
# 5. PLOT PROPAGATION
# ============================================================

plt.plot(
    df["month"],
    df["Propagation"],
    marker="o",
    linewidth=2.5,
    markersize=8,
    label="Propagation"
)


# ============================================================
# 6. ADD ENGAGEMENT VALUES
# ============================================================

for i in range(len(df)):

    value = df.iloc[i]["Engagement"]

    plt.annotate(
        f"{int(value):,}",
        (
            df.iloc[i]["month"],
            value
        ),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center",
        fontsize=9
    )


# ============================================================
# 7. ADD PROPAGATION VALUES
# ============================================================

for i in range(len(df)):

    value = df.iloc[i]["Propagation"]

    plt.annotate(
        f"{int(value):,}",
        (
            df.iloc[i]["month"],
            value
        ),
        xytext=(0, -18),
        textcoords="offset points",
        ha="center",
        fontsize=9
    )


# ============================================================
# 8. TITLE
# ============================================================

plt.title(
    "Propagation vs Engagement Over Time\n"
    "Monthly Information-Diffusion Activity",
    fontsize=18,
    fontweight="bold",
    pad=20
)


# ============================================================
# 9. AXIS LABELS
# ============================================================

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


# ============================================================
# 10. LEGEND
# ============================================================

plt.legend(
    title="Interaction Category",
    loc="upper left"
)


# ============================================================
# 11. GRID
# ============================================================

plt.grid(
    alpha=0.25
)


# ============================================================
# 12. SAVE
# ============================================================

output_file = os.path.join(
    OUTPUT_DIR,
    "networkx_propagation_vs_engagement.png"
)

plt.tight_layout()

plt.savefig(
    output_file,
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

plt.close()


# ============================================================
# 13. SUMMARY
# ============================================================

print()
print("==============================================")
print("Propagation vs Engagement diagram created!")
print("==============================================")

print(
    "Months plotted:",
    len(df)
)

print(
    "Engagement total:",
    f"{df['Engagement'].sum():,}"
)

print(
    "Propagation total:",
    f"{df['Propagation'].sum():,}"
)

print()
print("Saved to:")
print(output_file)