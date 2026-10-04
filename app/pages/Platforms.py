import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Platforms | SNA Case Study",
    page_icon="🌐",
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

matrix = pd.read_csv(
    RESULTS_DIR / "platform_diffusion_matrix.csv"
)

transitions = pd.read_csv(
    RESULTS_DIR / "platform_diffusion_transitions.csv"
)

platform_activity = pd.read_csv(
    RESULTS_DIR / "temporal_platform_activity.csv"
)


# ============================================================
# TITLE
# ============================================================

st.title("🌐 Cross-Platform Diffusion")

st.markdown(
    """
    Explore how information propagates between Instagram, Facebook,
    Reddit, YouTube, and X.
    """
)

st.divider()


# ============================================================
# KEY METRICS
# ============================================================

st.subheader("Cross-Platform Overview")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Cross-Platform Interactions",
        "7,869"
    )

with c2:
    st.metric(
        "Cross-Platform Cascades",
        "1,729"
    )

with c3:
    st.metric(
        "Platform Pairs",
        "20"
    )


st.info(
    """
    Cross-platform diffusion occurs in 1,729 of the 1,876 analyzed
    cascades, representing 92.16% of all cascades.
    """
)


# ============================================================
# PLATFORM DIFFUSION MATRIX
# ============================================================

st.divider()

st.subheader("Platform-to-Platform Diffusion")

st.write(
    "The matrix shows the number of cross-platform propagation "
    "events from each source platform to each target platform."
)


# ------------------------------------------------------------
# Detect matrix structure
# ------------------------------------------------------------

matrix_display = matrix.copy()

# Remove accidental index columns if present
matrix_display = matrix_display.loc[
    :,
    [
        c for c in matrix_display.columns
        if not c.lower().startswith("unnamed")
    ]
]


st.dataframe(
    matrix_display,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# HEATMAP
# ============================================================

st.subheader("Diffusion Heatmap")

# Try to identify source column
possible_source_columns = [
    c for c in matrix_display.columns
    if c.lower() in [
        "source_platform",
        "platform",
        "from",
        "source"
    ]
]

if possible_source_columns:

    source_column = possible_source_columns[0]

    heatmap_data = matrix_display.set_index(
        source_column
    )

else:

    # If the CSV already has platforms as the index,
    # use the first column as the source label.
    first_column = matrix_display.columns[0]

    heatmap_data = matrix_display.set_index(
        first_column
    )


# Convert values to numeric where possible
heatmap_data = heatmap_data.apply(
    pd.to_numeric,
    errors="coerce"
)

fig = px.imshow(
    heatmap_data,
    text_auto=True,
    aspect="auto",
    title="Cross-Platform Diffusion Matrix",
    labels={
        "x": "Target Platform",
        "y": "Source Platform",
        "color": "Propagation Events"
    }
)

fig.update_layout(
    height=550,
    template="plotly_white"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# TOP TRANSITIONS
# ============================================================

st.divider()

st.subheader("Top Cross-Platform Transitions")

if not transitions.empty:

    transition_display = transitions.copy()

    transition_display = transition_display.loc[
        :,
        [
            c for c in transition_display.columns
            if not c.lower().startswith("unnamed")
        ]
    ]

    # If the expected columns exist, sort by event count.
    if "cross_platform_events" in transition_display.columns:

        transition_display = transition_display.sort_values(
            "cross_platform_events",
            ascending=False
        )

    st.dataframe(
        transition_display.head(20),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TOP TRANSITION CHART
# ============================================================

if not transitions.empty:

    # Use the actual Phase 4 schema when available.
    if all(
        column in transitions.columns
        for column in [
            "source_platform",
            "target_platform",
            "cross_platform_events"
        ]
    ):

        chart_data = (
            transitions[
                [
                    "source_platform",
                    "target_platform",
                    "cross_platform_events"
                ]
            ]
            .copy()
        )

        chart_data["transition"] = (
            chart_data["source_platform"]
            + " → "
            + chart_data["target_platform"]
        )

        chart_data = (
            chart_data
            .sort_values(
                "cross_platform_events",
                ascending=False
            )
            .head(10)
            .sort_values(
                "cross_platform_events"
            )
        )

        fig = px.bar(
            chart_data,
            x="cross_platform_events",
            y="transition",
            orientation="h",
            text="cross_platform_events",
            title="Top 10 Cross-Platform Diffusion Pathways",
            labels={
                "transition": "Platform Transition",
                "cross_platform_events": "Propagation Events"
            }
        )

        fig.update_traces(
            textposition="outside"
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
# PLATFORM ACTIVITY
# ============================================================

st.divider()

st.subheader("Platform Activity Over Time")

activity = platform_activity.copy()

activity = activity.loc[
    :,
    [
        c for c in activity.columns
        if not c.lower().startswith("unnamed")
    ]
]


# Detect month/date column
date_column = None

for column in activity.columns:

    lower = column.lower()

    if (
        "month" in lower
        or "date" in lower
        or "time" in lower
    ):

        date_column = column
        break


if date_column:

    activity_long = activity.melt(
        id_vars=[date_column],
        var_name="Platform",
        value_name="Interactions"
    )

    fig = px.line(
        activity_long,
        x=date_column,
        y="Interactions",
        color="Platform",
        markers=True,
        title="Platform Activity Over Time",
        labels={
            date_column: "Month",
            "Interactions": "Interactions"
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
# PLATFORM SELECTOR
# ============================================================

st.divider()

st.subheader("🔎 Platform Explorer")

platforms = [
    "Facebook",
    "Instagram",
    "Reddit",
    "X",
    "YouTube"
]

selected_platform = st.selectbox(
    "Select a platform",
    platforms
)

st.markdown(
    f"### {selected_platform}"
)


# ============================================================
# OUTGOING TRANSITIONS
# ============================================================

st.markdown("#### Outgoing Diffusion")

if not transitions.empty:

    required_columns = [
        "source_platform",
        "target_platform",
        "cross_platform_events"
    ]

    if all(
        column in transitions.columns
        for column in required_columns
    ):

        outgoing = transitions[
            transitions["source_platform"]
            == selected_platform
        ].copy()

        # Remove self-transitions if any exist.
        outgoing = outgoing[
            outgoing["target_platform"]
            != selected_platform
        ]

        outgoing = outgoing.sort_values(
            "cross_platform_events",
            ascending=False
        )

        if not outgoing.empty:

            total_outgoing = int(
                outgoing["cross_platform_events"].sum()
            )

            top_destination = (
                outgoing.iloc[0]["target_platform"]
            )

            top_count = int(
                outgoing.iloc[0]["cross_platform_events"]
            )

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "Outgoing Cross-Platform Events",
                    f"{total_outgoing:,}"
                )

            with c2:

                st.metric(
                    "Top Destination",
                    top_destination
                )

            with c3:

                st.metric(
                    "Top Destination Events",
                    f"{top_count:,}"
                )


            # --------------------------------------------
            # Outgoing diffusion chart
            # --------------------------------------------

            fig = px.bar(
                outgoing,
                x="target_platform",
                y="cross_platform_events",
                text="cross_platform_events",
                title=f"{selected_platform} → Other Platforms",
                labels={
                    "target_platform": "Target Platform",
                    "cross_platform_events":
                        "Propagation Events"
                }
            )

            fig.update_traces(
                textposition="outside"
            )

            fig.update_layout(
                height=450,
                template="plotly_white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


            # --------------------------------------------
            # Detailed outgoing table
            # --------------------------------------------

            st.dataframe(
                outgoing[
                    [
                        "source_platform",
                        "target_platform",
                        "cross_platform_events"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                f"No outgoing cross-platform diffusion was found "
                f"for {selected_platform}."
            )

    else:

        st.error(
            "The platform transition result file does not contain "
            "the expected columns: source_platform, "
            "target_platform, cross_platform_events."
        )


# ============================================================
# INTERPRETATION
# ============================================================

st.divider()

st.subheader("Interpretation")

st.info(
    """
    Cross-platform diffusion is widespread in the simulated network.
    Facebook → YouTube is the highest observed directed transition
    with 421 events, followed by Facebook → Reddit with 419 events
    and YouTube → Reddit with 414 events.

    These transition frequencies describe the controlled synthetic
    network and should not be interpreted as evidence that one
    real-world platform inherently drives information toward another.
    """
)


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "Source: Phase 4 Temporal and Cross-Platform Diffusion Analysis."
)