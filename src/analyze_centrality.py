import pandas as pd
import numpy as np
import networkx as nx
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
print("PHASE 2 — CENTRALITY, INFLUENCE & COMMUNITY ANALYSIS")
print("=" * 70)

print("\nLoading datasets...")

users = pd.read_csv(DATA_DIR / "users.csv")
interactions = pd.read_csv(DATA_DIR / "interactions.csv")

print(f"Users:        {len(users):,}")
print(f"Interactions: {len(interactions):,}")


# ============================================================
# BUILD FULL NETWORK
# ============================================================

print("\n" + "=" * 70)
print("BUILDING FULL INTERACTION NETWORK")
print("=" * 70)

G = nx.DiGraph()

G.add_nodes_from(users["user_id"])

for row in interactions.itertuples(index=False):

    source = row.source_user
    target = row.target_user

    if source == target:
        continue

    if G.has_edge(source, target):
        G[source][target]["weight"] += 1
    else:
        G.add_edge(
            source,
            target,
            weight=1
        )

print(f"Nodes: {G.number_of_nodes():,}")
print(f"Edges: {G.number_of_edges():,}")


# ============================================================
# BUILD PROPAGATION NETWORK
# ============================================================

print("\n" + "=" * 70)
print("BUILDING PROPAGATION NETWORK")
print("=" * 70)

propagation_types = [
    "Share",
    "CrossPlatformShare"
]

propagation_df = interactions[
    interactions["interaction_type"].isin(
        propagation_types
    )
].copy()

P = nx.DiGraph()

P.add_nodes_from(users["user_id"])

for row in propagation_df.itertuples(index=False):

    source = row.source_user
    target = row.target_user

    if source == target:
        continue

    if P.has_edge(source, target):
        P[source][target]["weight"] += 1
    else:
        P.add_edge(
            source,
            target,
            weight=1
        )

print(
    f"Propagation interactions: "
    f"{len(propagation_df):,}"
)

print(
    f"Propagation edges: "
    f"{P.number_of_edges():,}"
)


# ============================================================
# CENTRALITY — FULL NETWORK
# ============================================================

print("\n" + "=" * 70)
print("CALCULATING CENTRALITY METRICS")
print("=" * 70)

print("\n[1/5] Degree centrality...")

in_degree = dict(G.in_degree())
out_degree = dict(G.out_degree())

in_degree_centrality = nx.in_degree_centrality(G)
out_degree_centrality = nx.out_degree_centrality(G)


# ============================================================
# PAGERANK
# ============================================================

print("[2/5] PageRank...")

pagerank = nx.pagerank(
    G,
    alpha=0.85,
    weight="weight"
)


# ============================================================
# BETWEENNESS
# ============================================================

print("[3/5] Betweenness centrality...")

betweenness = nx.betweenness_centrality(
    G,
    normalized=True,
    weight=None
)


# ============================================================
# CLOSENESS
# ============================================================

print("[4/5] Closeness centrality...")

closeness = nx.closeness_centrality(G)


# ============================================================
# EIGENVECTOR
# ============================================================

print("[5/5] Eigenvector centrality...")

try:

    eigenvector = nx.eigenvector_centrality(
        G,
        max_iter=1000,
        weight="weight"
    )

except nx.PowerIterationFailedConvergence:

    print(
        "Standard eigenvector calculation "
        "did not converge. Using NumPy method..."
    )

    eigenvector = nx.eigenvector_centrality_numpy(
        G,
        weight="weight"
    )


# ============================================================
# BUILD CENTRALITY DATAFRAME
# ============================================================

print("\nBuilding centrality dataset...")

centrality_df = pd.DataFrame({
    "user_id": list(G.nodes()),

    "in_degree": [
        in_degree[u]
        for u in G.nodes()
    ],

    "out_degree": [
        out_degree[u]
        for u in G.nodes()
    ],

    "in_degree_centrality": [
        in_degree_centrality[u]
        for u in G.nodes()
    ],

    "out_degree_centrality": [
        out_degree_centrality[u]
        for u in G.nodes()
    ],

    "pagerank": [
        pagerank[u]
        for u in G.nodes()
    ],

    "betweenness_centrality": [
        betweenness[u]
        for u in G.nodes()
    ],

    "closeness_centrality": [
        closeness[u]
        for u in G.nodes()
    ],

    "eigenvector_centrality": [
        eigenvector[u]
        for u in G.nodes()
    ]
})


# ============================================================
# ADD USER ATTRIBUTES
# ============================================================

user_attributes = [
    "user_id",
    "user_type",
    "activity_score",
    "influence_score",
    "community_id"
]

available_attributes = [
    column
    for column in user_attributes
    if column in users.columns
]

centrality_df = centrality_df.merge(
    users[available_attributes],
    on="user_id",
    how="left"
)


# ============================================================
# PROPAGATION CENTRALITY
# ============================================================

print("\nCalculating propagation-network centrality...")

prop_in_degree = dict(P.in_degree())
prop_out_degree = dict(P.out_degree())

prop_pagerank = nx.pagerank(
    P,
    alpha=0.85,
    weight="weight"
)

centrality_df["propagation_in_degree"] = [
    prop_in_degree[u]
    for u in centrality_df["user_id"]
]

centrality_df["propagation_out_degree"] = [
    prop_out_degree[u]
    for u in centrality_df["user_id"]
]

centrality_df["propagation_pagerank"] = [
    prop_pagerank[u]
    for u in centrality_df["user_id"]
]


# ============================================================
# SAVE COMPLETE CENTRALITY DATA
# ============================================================

centrality_df.to_csv(
    RESULTS_DIR / "centrality_analysis.csv",
    index=False
)

print(
    "\nSaved:"
    "\n"
    + str(RESULTS_DIR / "centrality_analysis.csv")
)


# ============================================================
# TOP USERS
# ============================================================

def show_top_users(
    dataframe,
    metric,
    title,
    n=10
):

    print("\n" + "-" * 70)
    print(title)
    print("-" * 70)

    columns = [
        "user_id",
        metric
    ]

    optional = [
        "user_type",
        "influence_score",
        "activity_score",
        "community_id"
    ]

    columns.extend(
        [
            c
            for c in optional
            if c in dataframe.columns
        ]
    )

    print(
        dataframe
        .sort_values(metric, ascending=False)
        [columns]
        .head(n)
        .to_string(index=False)
    )


show_top_users(
    centrality_df,
    "pagerank",
    "TOP 10 USERS — PAGERANK"
)

show_top_users(
    centrality_df,
    "betweenness_centrality",
    "TOP 10 USERS — BETWEENNESS"
)

show_top_users(
    centrality_df,
    "closeness_centrality",
    "TOP 10 USERS — CLOSENESS"
)

show_top_users(
    centrality_df,
    "eigenvector_centrality",
    "TOP 10 USERS — EIGENVECTOR"
)

show_top_users(
    centrality_df,
    "propagation_pagerank",
    "TOP 10 USERS — PROPAGATION PAGERANK"
)


# ============================================================
# USER TYPE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("USER TYPE ANALYSIS")
print("=" * 70)

if "user_type" in centrality_df.columns:

    type_metrics = centrality_df.groupby(
        "user_type"
    ).agg({

        "in_degree": "mean",

        "out_degree": "mean",

        "pagerank": "mean",

        "betweenness_centrality": "mean",

        "closeness_centrality": "mean",

        "eigenvector_centrality": "mean",

        "propagation_in_degree": "mean",

        "propagation_out_degree": "mean",

        "propagation_pagerank": "mean",

        "influence_score": "mean",

        "activity_score": "mean"

    }).round(6)

    print("\n")
    print(type_metrics)

    type_metrics.to_csv(
        RESULTS_DIR / "user_type_centrality.csv"
    )


# ============================================================
# INFLUENCE CORRELATION ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("INFLUENCE vs CENTRALITY")
print("=" * 70)

correlation_columns = [
    "influence_score",
    "activity_score",
    "in_degree",
    "out_degree",
    "pagerank",
    "betweenness_centrality",
    "closeness_centrality",
    "eigenvector_centrality",
    "propagation_in_degree",
    "propagation_out_degree",
    "propagation_pagerank"
]

available_correlation_columns = [
    column
    for column in correlation_columns
    if column in centrality_df.columns
]

correlation_matrix = centrality_df[
    available_correlation_columns
].corr(method="pearson")

print("\n")
print(
    correlation_matrix[
        ["influence_score", "activity_score"]
    ].round(4)
)

correlation_matrix.to_csv(
    RESULTS_DIR / "centrality_correlations.csv"
)


# ============================================================
# COMMUNITY ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("COMMUNITY ANALYSIS")
print("=" * 70)

if "community_id" in centrality_df.columns:

    community_metrics = centrality_df.groupby(
        "community_id"
    ).agg({

        "user_id": "count",

        "in_degree": "mean",

        "out_degree": "mean",

        "pagerank": "mean",

        "betweenness_centrality": "mean",

        "closeness_centrality": "mean",

        "eigenvector_centrality": "mean",

        "propagation_in_degree": "mean",

        "propagation_out_degree": "mean",

        "propagation_pagerank": "mean",

        "influence_score": "mean",

        "activity_score": "mean"

    }).rename(
        columns={
            "user_id": "user_count"
        }
    ).round(6)

    print("\nCommunity summary:")
    print(
        community_metrics
        .sort_values(
            "propagation_pagerank",
            ascending=False
        )
        .head(10)
    )

    community_metrics.to_csv(
        RESULTS_DIR / "community_centrality.csv"
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("PHASE 2 COMPLETE")
print("=" * 70)

print("\nGenerated files:")

print(
    RESULTS_DIR / "centrality_analysis.csv"
)

print(
    RESULTS_DIR / "user_type_centrality.csv"
)

print(
    RESULTS_DIR / "centrality_correlations.csv"
)

print(
    RESULTS_DIR / "community_centrality.csv"
)

print("\nNext phase:")
print("Information cascade and diffusion analysis")