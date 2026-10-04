import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Communities | SNA Case Study",
    page_icon="👥",
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

community = pd.read_csv(
    RESULTS_DIR / "community_centrality.csv"
)

platform_community = pd.read_csv(
    RESULTS_DIR / "platform_community_diffusion.csv"
)

cross_community = pd.read_csv(
    RESULTS_DIR / "cross_community_cascade_summary.csv"
)


# ============================================================
# TITLE
# ============================================================

st.title("👥 Community Diffusion")

st.markdown(
    """
    Explore how information propagates within and across the
    25 communities represented in the synthetic social network.
    """
)

st.divider()


# ============================================================
# KEY METRICS
# ============================================================

st.subheader("Community Overview")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Communities",
        "25"
    )

with c2:
    st.metric(
        "Users per Community",
        "400"
    )

with c3:
    st.metric(
        "Cross-Community Cascades",
        "1,822"
    )

st.info(
    """
    Cross-community diffusion occurs in 1,822 of the 1,876 analyzed
    cascades, representing 97.12% of all cascades.
    """
)


# ============================================================
# COMMUNITY CENTRALITY
# ============================================================

st.divider()

st.subheader("Community Centrality")

st.write(
    """
    The table summarizes average network characteristics across
    communities. Because the synthetic dataset assigns 400 users
    to each community, community sizes are balanced by design.
    """
)

if not community.empty:

    st.dataframe(
        community,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# COMMUNITY METRIC SELECTOR
# ============================================================

st.subheader("Community Comparison")

numeric_options = {
    "Average In-Degree": "in_degree",
    "Average Out-Degree": "out_degree",
    "Average PageRank": "pagerank",
    "Average Influence": "influence_score",
    "Average Activity": "activity_score"
}

available_options = {
    name: column
    for name, column in numeric_options.items()
    if column in community.columns
}

if available_options:

    selected_name = st.selectbox(
        "Select community metric",
        list(available_options.keys())
    )

    selected_column = available_options[selected_name]

    chart_data = community.copy()

    # Community ID may be stored as an index-like column.
    if "community_id" not in chart_data.columns:

        first_column = chart_data.columns[0]

        chart_data = chart_data.rename(
            columns={
                first_column: "community_id"
            }
        )

    chart_data = chart_data.sort_values(
        selected_column,
        ascending=True
    )

    fig = px.bar(
        chart_data,
        x=selected_column,
        y="community_id",
        orientation="h",
        title=f"{selected_name} by Community",
        labels={
            selected_column: selected_name,
            "community_id": "Community"
        }
    )

    fig.update_layout(
        height=600,
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CROSS-COMMUNITY DIFFUSION
# ============================================================

st.divider()

st.subheader("Cross-Community Diffusion")

if not cross_community.empty:

    st.dataframe(
        cross_community,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PLATFORM × COMMUNITY DIFFUSION
# ============================================================

st.divider()

st.subheader("Cross-Community Diffusion by Platform")

st.write(
    """
    This view shows cross-community propagation associated with
    each source platform.
    """
)

if not platform_community.empty:

    platform_display = platform_community.copy()

    platform_display = platform_display.loc[
        :,
        [
            c for c in platform_display.columns
            if not c.lower().startswith("unnamed")
        ]
    ]

    st.dataframe(
        platform_display,
        use_container_width=True,
        hide_index=True
    )

    # Detect useful numeric column
    numeric_columns = platform_display.select_dtypes(
        include="number"
    ).columns.tolist()

    # Remove community/platform-count fields when possible
    preferred = [
        c for c in numeric_columns
        if "cross" in c.lower()
        or "interaction" in c.lower()
        or "event" in c.lower()
    ]

    if preferred:

        value_column = preferred[0]

    elif numeric_columns:

        value_column = numeric_columns[0]

    else:

        value_column = None

    # Detect platform column
    platform_column = None

    for column in platform_display.columns:

        if "platform" in column.lower():

            platform_column = column
            break

    if value_column and platform_column:

        fig = px.bar(
            platform_display.sort_values(
                value_column,
                ascending=True
            ),
            x=value_column,
            y=platform_column,
            orientation="h",
            title="Cross-Community Diffusion by Platform",
            labels={
                value_column: "Events",
                platform_column: "Platform"
            }
        )

        fig.update_layout(
            height=450,
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# COMMUNITY EXPLORER
# ============================================================

st.divider()

st.subheader("🔎 Community Explorer")

community_ids = []

if "community_id" in community.columns:

    community_ids = sorted(
        community["community_id"]
        .astype(str)
        .unique()
    )

else:

    community_ids = sorted(
        community.iloc[:, 0]
        .astype(str)
        .unique()
    )


selected_community = st.selectbox(
    "Select Community",
    community_ids
)

if "community_id" in community.columns:

    selected_row = community[
        community["community_id"].astype(str)
        == selected_community
    ]

else:

    selected_row = community[
        community.iloc[:, 0].astype(str)
        == selected_community
    ]


if not selected_row.empty:

    data = selected_row.iloc[0]

    st.markdown(
        f"### {selected_community}"
    )

    # --------------------------------------------------------
    # COMMUNITY METRICS
    # --------------------------------------------------------

    metric_columns = [
        ("Users", "user_count"),
        ("In-Degree", "in_degree"),
        ("Out-Degree", "out_degree"),
        ("PageRank", "pagerank"),
        ("Influence", "influence_score"),
        ("Activity", "activity_score")
    ]

    available_metrics = [
        item for item in metric_columns
        if item[1] in community.columns
    ]

    columns = st.columns(
        min(len(available_metrics), 4)
    )

    for i, (label, column) in enumerate(
        available_metrics
    ):

        with columns[i % len(columns)]:

            value = data[column]

            if isinstance(value, float):

                if value < 0.01:

                    display_value = f"{value:.6f}"

                else:

                    display_value = f"{value:.3f}"

            else:

                display_value = f"{value:,.0f}"

            st.metric(
                label,
                display_value
            )


# ============================================================
# INTERPRETATION
# ============================================================

st.divider()

st.subheader("Interpretation")

st.info(
    """
    Cross-community diffusion is widespread in the simulated network:
    97.12% of cascades involve more than one community.

    Communities are balanced by design, with 400 users assigned to
    each of the 25 communities. Therefore, the community analysis
    should focus on differences in network activity and diffusion
    behavior rather than interpreting community size differences.

    The observed patterns describe the controlled synthetic network
    and should not be treated as direct real-world community behavior.
    """
)


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "Source: Phase 2 Community Centrality and Phase 4 Community Diffusion Analysis."
)