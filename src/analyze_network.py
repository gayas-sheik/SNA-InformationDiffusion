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

print("=" * 60)
print("SNA INFORMATION DIFFUSION ANALYSIS")
print("=" * 60)

print("\nLoading datasets...")

users = pd.read_csv(DATA_DIR / "users.csv")
information = pd.read_csv(DATA_DIR / "information_items.csv")
interactions = pd.read_csv(DATA_DIR / "interactions.csv")

print(f"Users:         {len(users):,}")
print(f"Information:   {len(information):,}")
print(f"Interactions:  {len(interactions):,}")


# ============================================================
# REQUIRED COLUMN VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("SCHEMA VALIDATION")
print("=" * 60)

required_user_columns = [
    "user_id"
]

required_interaction_columns = [
    "interaction_type",
    "source_platform",
    "source_user",
    "target_user",
    "source_community",
    "target_community"
]

missing_user_columns = [
    col
    for col in required_user_columns
    if col not in users.columns
]

missing_interaction_columns = [
    col
    for col in required_interaction_columns
    if col not in interactions.columns
]

if missing_user_columns:
    raise ValueError(
        f"Missing columns in users.csv: {missing_user_columns}"
    )

if missing_interaction_columns:
    raise ValueError(
        f"Missing columns in interactions.csv: "
        f"{missing_interaction_columns}"
    )

print("Users schema:        PASS")
print("Interactions schema: PASS")


# ============================================================
# BASIC VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("BASIC DATA VALIDATION")
print("=" * 60)

print("\nInteraction types:")
print(interactions["interaction_type"].value_counts())

print("\nPlatforms:")
print(interactions["source_platform"].value_counts())

print("\nCommunities:")

source_communities = interactions[
    "source_community"
].nunique()

target_communities = interactions[
    "target_community"
].nunique()

print(f"Source communities: {source_communities}")
print(f"Target communities: {target_communities}")


# ============================================================
# USER REFERENCE VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("USER REFERENCE VALIDATION")
print("=" * 60)

user_ids = set(users["user_id"])

source_users = set(interactions["source_user"])
target_users = set(interactions["target_user"])

missing_source_users = source_users - user_ids
missing_target_users = target_users - user_ids

print(
    f"Unique source users: {len(source_users):,}"
)

print(
    f"Unique target users: {len(target_users):,}"
)

print(
    f"Missing source users: {len(missing_source_users):,}"
)

print(
    f"Missing target users: {len(missing_target_users):,}"
)

if missing_source_users or missing_target_users:
    raise ValueError(
        "Some interaction users do not exist in users.csv."
    )

print("User references: PASS")


# ============================================================
# BUILD FULL INTERACTION NETWORK
# ============================================================

print("\n" + "=" * 60)
print("BUILDING FULL USER INTERACTION NETWORK")
print("=" * 60)

G = nx.DiGraph()

# Add all users as nodes
G.add_nodes_from(users["user_id"])

# Add directed interaction edges
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


print(f"\nNodes: {G.number_of_nodes():,}")
print(f"Edges: {G.number_of_edges():,}")


# ============================================================
# BUILD PROPAGATION NETWORK
# ============================================================

print("\n" + "=" * 60)
print("BUILDING PROPAGATION NETWORK")
print("=" * 60)

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
    f"\nPropagation interactions: "
    f"{len(propagation_df):,}"
)

print(
    f"Propagation nodes:        "
    f"{P.number_of_nodes():,}"
)

print(
    f"Propagation edges:        "
    f"{P.number_of_edges():,}"
)


# ============================================================
# NETWORK STATISTICS
# ============================================================

print("\n" + "=" * 60)
print("NETWORK STATISTICS")
print("=" * 60)


def network_statistics(graph, name):

    n = graph.number_of_nodes()
    m = graph.number_of_edges()

    density = nx.density(graph)

    in_degrees = dict(graph.in_degree())
    out_degrees = dict(graph.out_degree())

    print(f"\n{name}")
    print("-" * 40)

    print(f"Nodes:              {n:,}")
    print(f"Edges:              {m:,}")
    print(f"Density:            {density:.8f}")

    print(
        f"Average in-degree:  "
        f"{np.mean(list(in_degrees.values())):.4f}"
    )

    print(
        f"Average out-degree: "
        f"{np.mean(list(out_degrees.values())):.4f}"
    )

    print(
        f"Maximum in-degree:  "
        f"{max(in_degrees.values()):,}"
    )

    print(
        f"Maximum out-degree: "
        f"{max(out_degrees.values()):,}"
    )

    return {
        "network": name,
        "nodes": n,
        "edges": m,
        "density": density,
        "average_in_degree": np.mean(
            list(in_degrees.values())
        ),
        "average_out_degree": np.mean(
            list(out_degrees.values())
        ),
        "max_in_degree": max(
            in_degrees.values()
        ),
        "max_out_degree": max(
            out_degrees.values()
        )
    }


full_stats = network_statistics(
    G,
    "Full Interaction Network"
)

propagation_stats = network_statistics(
    P,
    "Propagation Network"
)


# ============================================================
# CONNECTIVITY
# ============================================================

print("\n" + "=" * 60)
print("CONNECTIVITY")
print("=" * 60)

weak_components = list(
    nx.weakly_connected_components(G)
)

print(
    f"\nWeakly connected components: "
    f"{len(weak_components):,}"
)

largest_component = max(
    weak_components,
    key=len
)

print(
    f"Largest component size: "
    f"{len(largest_component):,}"
)

print(
    f"Largest component percentage: "
    f"{len(largest_component) / G.number_of_nodes() * 100:.2f}%"
)


# ============================================================
# DEGREE CENTRALITY
# ============================================================

print("\n" + "=" * 60)
print("DEGREE CENTRALITY")
print("=" * 60)

in_degree_centrality = nx.in_degree_centrality(G)
out_degree_centrality = nx.out_degree_centrality(G)

centrality_df = pd.DataFrame({
    "user_id": list(G.nodes()),

    "in_degree": [
        G.in_degree(u)
        for u in G.nodes()
    ],

    "out_degree": [
        G.out_degree(u)
        for u in G.nodes()
    ],

    "in_degree_centrality": [
        in_degree_centrality[u]
        for u in G.nodes()
    ],

    "out_degree_centrality": [
        out_degree_centrality[u]
        for u in G.nodes()
    ]
})


# ============================================================
# ADD USER INFORMATION
# ============================================================

user_columns = [
    "user_id",
    "user_type",
    "activity_score",
    "influence_score",
    "community_id"
]

available_columns = [
    column
    for column in user_columns
    if column in users.columns
]

centrality_df = centrality_df.merge(
    users[available_columns],
    on="user_id",
    how="left"
)


# ============================================================
# SAVE RESULTS
# ============================================================

centrality_df = centrality_df.sort_values(
    "in_degree",
    ascending=False
)

centrality_df.to_csv(
    RESULTS_DIR / "user_degree_centrality.csv",
    index=False
)

network_summary = pd.DataFrame([
    full_stats,
    propagation_stats
])

network_summary.to_csv(
    RESULTS_DIR / "network_summary.csv",
    index=False
)


# ============================================================
# TOP USERS
# ============================================================

print("\n" + "=" * 60)
print("TOP USERS BY IN-DEGREE")
print("=" * 60)

display_columns = [
    "user_id",
    "in_degree",
    "out_degree",
    "in_degree_centrality",
    "out_degree_centrality"
]

optional_columns = [
    "user_type",
    "influence_score"
]

for column in optional_columns:

    if column in centrality_df.columns:
        display_columns.append(column)

print(
    centrality_df[
        display_columns
    ].head(10).to_string(index=False)
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n" + "=" * 60)
print("PHASE 1 COMPLETE")
print("=" * 60)

print("\nGenerated files:")

print(
    RESULTS_DIR / "network_summary.csv"
)

print(
    RESULTS_DIR / "user_degree_centrality.csv"
)

print("\nNext phase:")
print("Centrality + influence + community analysis")