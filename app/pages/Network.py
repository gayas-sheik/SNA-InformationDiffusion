import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Network | SNA Case Study",
    page_icon="🕸️",
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

network_summary = pd.read_csv(
    RESULTS_DIR / "network_summary.csv"
)

# Use Phase 2 centrality results because they contain
# both normal and propagation degree measures.
degree_data = pd.read_csv(
    RESULTS_DIR / "centrality_analysis.csv"
)


# ============================================================
# TITLE
# ============================================================

st.title("🕸️ Network Analysis")

st.markdown(
    """
    Explore the structure of the social network and compare the
    **full interaction network** with the **propagation network**.
    """
)

st.divider()


# ============================================================
# NETWORK TYPE
# ============================================================

network_type = st.radio(
    "Select network",
    ["Full Interaction Network", "Propagation Network"],
    horizontal=True
)


# ============================================================
# NETWORK METRICS
# ============================================================

if network_type == "Full Interaction Network":

    nodes = 10000
    edges = 48463
    density = 0.00048468
    avg_in = 4.8463
    avg_out = 4.8463
    max_in = 28
    max_out = 27
    components = 580
    largest_component = 9421

else:

    nodes = 10000
    edges = 20801
    density = 0.00020803
    avg_in = 2.0801
    avg_out = 2.0801
    max_in = 18
    max_out = 16

    # Propagation network connectivity was not separately
    # calculated in Phase 1, so we do not invent it.
    components = None
    largest_component = None


# ============================================================
# METRIC CARDS
# ============================================================

st.subheader("Network Statistics")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Nodes",
        f"{nodes:,}"
    )

with c2:
    st.metric(
        "Edges",
        f"{edges:,}"
    )

with c3:
    st.metric(
        "Density",
        f"{density:.6f}"
    )

with c4:
    st.metric(
        "Average In-Degree",
        f"{avg_in:.2f}"
    )


c5, c6, c7, c8 = st.columns(4)

with c5:
    st.metric(
        "Average Out-Degree",
        f"{avg_out:.2f}"
    )

with c6:
    st.metric(
        "Maximum In-Degree",
        max_in
    )

with c7:
    st.metric(
        "Maximum Out-Degree",
        max_out
    )

with c8:

    if components is not None:
        st.metric(
            "Weak Components",
            components
        )
    else:
        st.metric(
            "Weak Components",
            "—"
        )


# ============================================================
# CONNECTIVITY
# ============================================================

if network_type == "Full Interaction Network":

    st.subheader("Connectivity")

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Weakly Connected Components",
            f"{components:,}"
        )

    with c2:

        st.metric(
            "Largest Component",
            f"{largest_component:,} users"
        )

        st.caption(
            "94.21% of all users belong to the largest weakly "
            "connected component."
        )


# ============================================================
# DEGREE DISTRIBUTION
# ============================================================

st.divider()

st.subheader("Degree Distribution")

if network_type == "Full Interaction Network":

    degree_column = "in_degree"

else:

    degree_column = "propagation_in_degree"


if degree_column in degree_data.columns:

    fig = px.histogram(
        degree_data,
        x=degree_column,
        nbins=30,
        title=f"{network_type} — In-Degree Distribution",
        labels={
            degree_column: "In-Degree",
            "count": "Number of Users"
        }
    )

    fig.update_layout(
        height=450,
        margin=dict(l=20, r=20, t=60, b=20),
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.warning(
        f"The required column '{degree_column}' "
        "was not found in the result file."
    )


# ============================================================
# TOP USERS
# ============================================================

st.divider()

st.subheader("Top Users by In-Degree")

if network_type == "Full Interaction Network":

    display_columns = [
        "user_id",
        "in_degree",
        "out_degree",
        "user_type",
        "influence_score"
    ]

    available_columns = [
        c for c in display_columns
        if c in degree_data.columns
    ]

    top_users = (
        degree_data
        .sort_values(
            "in_degree",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_users[available_columns],
        use_container_width=True,
        hide_index=True
    )

else:

    if "propagation_in_degree" in degree_data.columns:

        display_columns = [
            "user_id",
            "propagation_in_degree",
            "propagation_out_degree",
            "user_type",
            "influence_score"
        ]

        available_columns = [
            c for c in display_columns
            if c in degree_data.columns
        ]

        top_users = (
            degree_data
            .sort_values(
                "propagation_in_degree",
                ascending=False
            )
            .head(10)
        )

        st.dataframe(
            top_users[available_columns],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "The propagation degree columns were not found "
            "in the centrality analysis result."
        )


# ============================================================
# INTERPRETATION
# ============================================================

st.divider()

st.subheader("Interpretation")

if network_type == "Full Interaction Network":

    st.info(
        """
        The full interaction network is sparse but broadly connected.
        It contains 48,463 unique interaction edges among 10,000 users,
        while the largest weakly connected component contains 9,421 users.
        """
    )

else:

    st.info(
        """
        The propagation network isolates interactions that represent
        information spreading. It contains 20,801 propagation edges,
        making it substantially sparser than the full interaction network.
        """
    )


# ============================================================
# NOTE
# ============================================================

st.caption(
    "Source: Phase 1 network construction and Phase 2 centrality analysis."
)