import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Influence | SNA Case Study",
    page_icon="👤",
    layout="wide"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]
RESULTS_DIR = BASE_DIR / "results"


# ============================================================
# LOAD DATA
# ============================================================

centrality = pd.read_csv(
    RESULTS_DIR / "centrality_analysis.csv"
)

user_type = pd.read_csv(
    RESULTS_DIR / "user_type_centrality.csv"
)

correlations = pd.read_csv(
    RESULTS_DIR / "centrality_correlations.csv"
)


# ============================================================
# TITLE
# ============================================================

st.title("👤 User Influence")

st.markdown(
    """
    Explore how user influence relates to network position using
    centrality measures and user-type analysis.
    """
)

st.divider()


# ============================================================
# KEY INFLUENCE FINDING
# ============================================================

st.subheader("Key Influence Finding")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Influential Mean Influence",
        "0.805"
    )

with c2:
    st.metric(
        "Influential Mean Activity",
        "0.778"
    )

with c3:
    st.metric(
        "Influence ↔ PageRank",
        "r = 0.7014"
    )

st.info(
    """
    Influence and PageRank show a positive association in the
    synthetic network. This indicates that users with stronger
    network positions tend to have higher influence scores.
    This is an association, not evidence of causation.
    """
)


# ============================================================
# CENTRALITY RANKING
# ============================================================

st.divider()

st.subheader("Centrality Ranking")

metric_options = {
    "In-Degree": "in_degree",
    "Out-Degree": "out_degree",
    "PageRank": "pagerank",
    "Betweenness": "betweenness_centrality",
    "Closeness": "closeness_centrality",
    "Eigenvector": "eigenvector_centrality",
    "Propagation In-Degree": "propagation_in_degree",
    "Propagation Out-Degree": "propagation_out_degree",
    "Propagation PageRank": "propagation_pagerank"
}

selected_metric_name = st.selectbox(
    "Select centrality measure",
    list(metric_options.keys())
)

selected_metric = metric_options[selected_metric_name]


if selected_metric in centrality.columns:

    ranking_columns = [
        "user_id",
        selected_metric,
        "user_type",
        "influence_score",
        "activity_score"
    ]

    ranking_columns = [
        c for c in ranking_columns
        if c in centrality.columns
    ]

    top_users = (
        centrality[ranking_columns]
        .sort_values(
            selected_metric,
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        top_users.sort_values(selected_metric),
        x=selected_metric,
        y="user_id",
        orientation="h",
        title=f"Top 10 Users by {selected_metric_name}",
        labels={
            selected_metric: selected_metric_name,
            "user_id": "User"
        },
        hover_data=[
            c for c in [
                "user_type",
                "influence_score",
                "activity_score"
            ]
            if c in top_users.columns
        ]
    )

    fig.update_layout(
        height=500,
        template="plotly_white",
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.error(
        f"The column '{selected_metric}' was not found "
        "in centrality_analysis.csv."
    )


# ============================================================
# USER EXPLORER
# ============================================================

st.divider()

st.subheader("🔎 User Explorer")

st.write(
    "Select any user to inspect their complete network profile."
)

user_ids = sorted(
    centrality["user_id"].astype(str).unique()
)

selected_user = st.selectbox(
    "Select User",
    user_ids,
    index=0
)

user_row = centrality[
    centrality["user_id"].astype(str) == selected_user
]

if not user_row.empty:

    user_data = user_row.iloc[0]

    st.markdown(
        f"### {selected_user}"
    )

    # --------------------------------------------------------
    # BASIC USER INFORMATION
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "User Type",
            str(user_data["user_type"])
        )

    with c2:
        st.metric(
            "Influence",
            f"{user_data['influence_score']:.4f}"
        )

    with c3:
        st.metric(
            "Activity",
            f"{user_data['activity_score']:.4f}"
        )

    with c4:
        st.metric(
            "Community",
            str(user_data["community_id"])
        )

    # --------------------------------------------------------
    # CENTRALITY METRICS
    # --------------------------------------------------------

    st.markdown("#### Centrality Metrics")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "In-Degree",
            f"{user_data['in_degree']:.0f}"
        )

        st.metric(
            "Out-Degree",
            f"{user_data['out_degree']:.0f}"
        )

        st.metric(
            "PageRank",
            f"{user_data['pagerank']:.6f}"
        )

    with c2:

        st.metric(
            "Betweenness",
            f"{user_data['betweenness_centrality']:.6f}"
        )

        st.metric(
            "Closeness",
            f"{user_data['closeness_centrality']:.6f}"
        )

        st.metric(
            "Eigenvector",
            f"{user_data['eigenvector_centrality']:.6f}"
        )

    with c3:

        st.metric(
            "Propagation In-Degree",
            f"{user_data['propagation_in_degree']:.0f}"
        )

        st.metric(
            "Propagation Out-Degree",
            f"{user_data['propagation_out_degree']:.0f}"
        )

        st.metric(
            "Propagation PageRank",
            f"{user_data['propagation_pagerank']:.6f}"
        )


# ============================================================
# USER TYPE COMPARISON
# ============================================================

st.divider()

st.subheader("User Type Comparison")

st.caption(
    "Average network position, influence, and activity by user type."
)

if not user_type.empty:

    st.dataframe(
        user_type,
        use_container_width=True,
        hide_index=True
    )

    if (
        "user_type" in user_type.columns
        and "influence_score" in user_type.columns
    ):

        fig = px.bar(
            user_type.sort_values("influence_score"),
            x="user_type",
            y="influence_score",
            title="Mean Influence by User Type",
            labels={
                "user_type": "User Type",
                "influence_score": "Mean Influence"
            }
        )

        fig.update_layout(
            height=420,
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# INFLUENCE VS CENTRALITY
# ============================================================

st.divider()

st.subheader("Influence vs Centrality")

correlation_options = {
    "PageRank": "pagerank",
    "In-Degree": "in_degree",
    "Out-Degree": "out_degree",
    "Betweenness": "betweenness_centrality",
    "Closeness": "closeness_centrality",
    "Eigenvector": "eigenvector_centrality"
}

selected_x_name = st.selectbox(
    "Compare influence with",
    list(correlation_options.keys())
)

selected_x = correlation_options[selected_x_name]

if selected_x in centrality.columns:

    fig = px.scatter(
        centrality,
        x=selected_x,
        y="influence_score",
        color="user_type",
        hover_data=[
            "user_id",
            "activity_score",
            "community_id"
        ],
        title=f"Influence vs {selected_x_name}",
        labels={
            selected_x: selected_x_name,
            "influence_score": "Influence"
        }
    )

    fig.update_layout(
        height=500,
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CORRELATION SUMMARY
# ============================================================

st.divider()

st.subheader("Influence Correlations")

st.write(
    "Correlation values show the strength of association between "
    "user influence and network measures."
)

if not correlations.empty:

    st.dataframe(
        correlations,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# INTERPRETATION
# ============================================================

st.divider()

st.subheader("Interpretation")

st.info(
    """
    Influential users have the highest average influence and activity
    among the defined user types. Influence is positively associated
    with several centrality measures, with PageRank showing the
    strongest meaningful relationship (r = 0.7014).

    These results describe associations within the controlled
    synthetic network and should not be interpreted as causal
    relationships.
    """
)


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "Source: Phase 2 Centrality, User-Type and Correlation Analysis."
)