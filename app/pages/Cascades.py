import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Cascades | SNA Case Study",
    page_icon="🌊",
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

cascade = pd.read_csv(
    RESULTS_DIR / "cascade_analysis.csv"
)

cross_platform = pd.read_csv(
    RESULTS_DIR / "cross_platform_cascade_summary.csv"
)

cross_community = pd.read_csv(
    RESULTS_DIR / "cross_community_cascade_summary.csv"
)

root_types = pd.read_csv(
    RESULTS_DIR / "root_user_type_cascade_summary.csv"
)


# ============================================================
# TITLE
# ============================================================

st.title("🌊 Information Cascades")

st.markdown(
    """
    Explore how information propagates through users, platforms,
    and communities using the analyzed information cascades.
    """
)

st.divider()


# ============================================================
# KEY CASCADE METRICS
# ============================================================

st.subheader("Cascade Overview")

total_cascades = len(cascade)
average_size = cascade["cascade_size"].mean()
median_size = cascade["cascade_size"].median()
maximum_size = cascade["cascade_size"].max()

average_depth = cascade["cascade_depth"].mean()
maximum_depth = cascade["cascade_depth"].max()

average_duration = cascade["duration_hours"].mean()
maximum_duration = cascade["duration_hours"].max()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Total Cascades",
        f"{total_cascades:,}"
    )

with c2:
    st.metric(
        "Average Size",
        f"{average_size:.2f}"
    )

with c3:
    st.metric(
        "Median Size",
        f"{median_size:.0f}"
    )

with c4:
    st.metric(
        "Maximum Size",
        f"{maximum_size:.0f}"
    )


c5, c6, c7, c8 = st.columns(4)

with c5:
    st.metric(
        "Average Depth",
        f"{average_depth:.2f}"
    )

with c6:
    st.metric(
        "Maximum Depth",
        f"{maximum_depth:.0f}"
    )

with c7:
    st.metric(
        "Average Duration",
        f"{average_duration:.2f} h"
    )

with c8:
    st.metric(
        "Maximum Duration",
        f"{maximum_duration:.2f} h"
    )


# ============================================================
# CASCADE DISTRIBUTION
# ============================================================

st.divider()

st.subheader("Cascade Size Distribution")

fig = px.histogram(
    cascade,
    x="cascade_size",
    nbins=30,
    title="Distribution of Information Cascade Sizes",
    labels={
        "cascade_size": "Cascade Size",
        "count": "Number of Cascades"
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
# CASCADE EXPLORER
# ============================================================

st.divider()

st.subheader("🔎 Cascade Explorer")

st.write(
    "Select an individual cascade to inspect its diffusion characteristics."
)

cascade_ids = sorted(
    cascade["cascade_id"].astype(str).unique()
)

selected_cascade = st.selectbox(
    "Select Cascade",
    cascade_ids
)

selected_row = cascade[
    cascade["cascade_id"].astype(str) == selected_cascade
]

if not selected_row.empty:

    data = selected_row.iloc[0]

    st.markdown(
        f"### {selected_cascade}"
    )

    # --------------------------------------------------------
    # BASIC CASCADE METRICS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Cascade Size",
            f"{data['cascade_size']:.0f}"
        )

    with c2:
        st.metric(
            "Cascade Depth",
            f"{data['cascade_depth']:.0f}"
        )

    with c3:
        st.metric(
            "Duration",
            f"{data['duration_hours']:.2f} h"
        )

    with c4:
        st.metric(
            "Unique Users",
            f"{data['unique_users']:.0f}"
        )

    c5, c6, c7, c8 = st.columns(4)

    with c5:
        st.metric(
            "Unique Platforms",
            f"{data['unique_platforms']:.0f}"
        )

    with c6:
        st.metric(
            "Unique Communities",
            f"{data['unique_communities']:.0f}"
        )

    with c7:
        st.metric(
            "Cross-Platform Events",
            f"{data['cross_platform_events']:.0f}"
        )

    with c8:
        st.metric(
            "Cross-Community Events",
            f"{data['cross_community_events']:.0f}"
        )

    # --------------------------------------------------------
    # ROOT INFORMATION
    # --------------------------------------------------------

    st.markdown("#### Root Information")

    root_columns = [
        "root_user",
        "root_user_type",
        "root_user_influence",
        "source_platform",
        "information_id"
    ]

    available_root_columns = [
        c for c in root_columns
        if c in cascade.columns
    ]

    if available_root_columns:

        root_display = pd.DataFrame(
            [data[available_root_columns].to_dict()]
        )

        st.dataframe(
            root_display,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# CROSS-PLATFORM CASCADE ANALYSIS
# ============================================================

st.divider()

st.subheader("🌐 Cross-Platform Diffusion")

if not cross_platform.empty:

    st.dataframe(
        cross_platform,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# CROSS-COMMUNITY CASCADE ANALYSIS
# ============================================================

st.divider()

st.subheader("👥 Cross-Community Diffusion")

if not cross_community.empty:

    st.dataframe(
        cross_community,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# ROOT USER TYPE ANALYSIS
# ============================================================

st.divider()

st.subheader("Root User Type and Cascade Size")

if not root_types.empty:

    st.dataframe(
        root_types,
        use_container_width=True,
        hide_index=True
    )

    if (
        "user_type" in root_types.columns
        and "mean_cascade_size" in root_types.columns
    ):

        fig = px.bar(
            root_types.sort_values("mean_cascade_size"),
            x="user_type",
            y="mean_cascade_size",
            title="Average Cascade Size by Root User Type",
            labels={
                "user_type": "Root User Type",
                "mean_cascade_size": "Average Cascade Size"
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
# INTERPRETATION
# ============================================================

st.divider()

st.subheader("Interpretation")

st.info(
    """
    The analysis identifies 1,876 information cascades with an
    average size of 26.65 interactions and a maximum size of 75.
    Cross-platform and cross-community propagation occur frequently
    within the simulated network.

    Because the dataset is synthetic and the generated cascades are
    predominantly chain-like, these results should be interpreted
    as characteristics of the controlled simulation rather than
    direct real-world diffusion behavior.
    """
)


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "Source: Phase 3 Information Cascade and Diffusion Analysis."
)