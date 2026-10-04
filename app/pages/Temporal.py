import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Temporal | SNA Case Study",
    page_icon="⏱️",
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

monthly = pd.read_csv(
    RESULTS_DIR / "temporal_monthly_activity.csv"
)

daily = pd.read_csv(
    RESULTS_DIR / "temporal_daily_activity.csv"
)

interaction_types = pd.read_csv(
    RESULTS_DIR / "temporal_interaction_types.csv"
)

platform_activity = pd.read_csv(
    RESULTS_DIR / "temporal_platform_activity.csv"
)

hourly = pd.read_csv(
    RESULTS_DIR / "temporal_hourly_activity.csv"
)

weekday = pd.read_csv(
    RESULTS_DIR / "temporal_weekday_activity.csv"
)

cascade_monthly = pd.read_csv(
    RESULTS_DIR / "temporal_cascade_summary.csv"
)

propagation_rate = pd.read_csv(
    RESULTS_DIR / "monthly_propagation_rate.csv"
)


# ============================================================
# TITLE
# ============================================================

st.title("⏱️ Temporal Diffusion")

st.markdown(
    """
    Explore when information activity and propagation occur
    throughout the six-month study period.
    """
)

st.divider()


# ============================================================
# KEY METRICS
# ============================================================

st.subheader("Temporal Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Study Period",
        "Jan – Jun 2026"
    )

with c2:
    st.metric(
        "Total Interactions",
        "50,000"
    )

with c3:
    st.metric(
        "Most Active Hour",
        "23:00"
    )

with c4:
    st.metric(
        "Most Active Weekday",
        "Tuesday"
    )

st.info(
    """
    The temporal patterns describe activity within the controlled
    synthetic dataset. They should not be interpreted as real-world
    user-behavior patterns.
    """
)


# ============================================================
# MONTHLY ACTIVITY
# ============================================================

st.divider()

st.subheader("📅 Monthly Interaction Activity")

monthly_display = monthly.copy()

monthly_display = monthly_display.loc[
    :,
    [
        c for c in monthly_display.columns
        if not c.lower().startswith("unnamed")
    ]
]

# Identify month and interaction-count column

month_column = None

for column in monthly_display.columns:

    if "month" in column.lower():

        month_column = column
        break

if month_column is None:

    month_column = monthly_display.columns[0]


numeric_columns = monthly_display.select_dtypes(
    include="number"
).columns.tolist()


if numeric_columns:

    value_column = numeric_columns[0]

    fig = px.line(
        monthly_display,
        x=month_column,
        y=value_column,
        markers=True,
        title="Total Interactions by Month",
        labels={
            month_column: "Month",
            value_column: "Interactions"
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
# INTERACTION TYPES
# ============================================================

st.divider()

st.subheader("Interaction Types Over Time")

interaction_display = interaction_types.copy()

interaction_display = interaction_display.loc[
    :,
    [
        c for c in interaction_display.columns
        if not c.lower().startswith("unnamed")
    ]
]

month_column = None

for column in interaction_display.columns:

    if "month" in column.lower():

        month_column = column
        break

if month_column is None:

    month_column = interaction_display.columns[0]


interaction_long = interaction_display.melt(
    id_vars=[month_column],
    var_name="Interaction Type",
    value_name="Interactions"
)

fig = px.line(
    interaction_long,
    x=month_column,
    y="Interactions",
    color="Interaction Type",
    markers=True,
    title="Interaction Types Over Time",
    labels={
        month_column: "Month",
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
# PLATFORM ACTIVITY
# ============================================================

st.divider()

st.subheader("Platform Activity Over Time")

platform_display = platform_activity.copy()

platform_display = platform_display.loc[
    :,
    [
        c for c in platform_display.columns
        if not c.lower().startswith("unnamed")
    ]
]

month_column = None

for column in platform_display.columns:

    if "month" in column.lower():

        month_column = column
        break

if month_column is None:

    month_column = platform_display.columns[0]


platform_long = platform_display.melt(
    id_vars=[month_column],
    var_name="Platform",
    value_name="Interactions"
)

fig = px.line(
    platform_long,
    x=month_column,
    y="Interactions",
    color="Platform",
    markers=True,
    title="Platform Activity Over Time",
    labels={
        month_column: "Month",
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
# HOURLY ACTIVITY
# ============================================================

st.divider()

st.subheader("🕐 Activity by Hour")

hourly_display = hourly.copy()

hourly_display = hourly_display.loc[
    :,
    [
        c for c in hourly_display.columns
        if not c.lower().startswith("unnamed")
    ]
]

hour_column = None

for column in hourly_display.columns:

    if (
        "hour" in column.lower()
        or "time" in column.lower()
    ):

        hour_column = column
        break

if hour_column is None:

    hour_column = hourly_display.columns[0]


numeric_columns = hourly_display.select_dtypes(
    include="number"
).columns.tolist()


if numeric_columns:

    value_column = numeric_columns[0]

    fig = px.bar(
        hourly_display,
        x=hour_column,
        y=value_column,
        title="Interaction Activity by Hour",
        labels={
            hour_column: "Hour",
            value_column: "Interactions"
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
# WEEKDAY ACTIVITY
# ============================================================

st.divider()

st.subheader("📆 Activity by Day of Week")

weekday_display = weekday.copy()

weekday_display = weekday_display.loc[
    :,
    [
        c for c in weekday_display.columns
        if not c.lower().startswith("unnamed")
    ]
]

weekday_column = None

for column in weekday_display.columns:

    if "day" in column.lower():

        weekday_column = column
        break

if weekday_column is None:

    weekday_column = weekday_display.columns[0]


numeric_columns = weekday_display.select_dtypes(
    include="number"
).columns.tolist()


if numeric_columns:

    value_column = numeric_columns[0]

    fig = px.bar(
        weekday_display,
        x=weekday_column,
        y=value_column,
        title="Interaction Activity by Weekday",
        labels={
            weekday_column: "Weekday",
            value_column: "Interactions"
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
# PROPAGATION RATE
# ============================================================

st.divider()

st.subheader("📈 Monthly Propagation Rate")

rate_display = propagation_rate.copy()

rate_display = rate_display.loc[
    :,
    [
        c for c in rate_display.columns
        if not c.lower().startswith("unnamed")
    ]
]

month_column = None

for column in rate_display.columns:

    if "month" in column.lower():

        month_column = column
        break

if month_column is None:

    month_column = rate_display.columns[0]


numeric_columns = rate_display.select_dtypes(
    include="number"
).columns.tolist()


if numeric_columns:

    rate_column = numeric_columns[0]

    fig = px.line(
        rate_display,
        x=month_column,
        y=rate_column,
        markers=True,
        title="Monthly Propagation Rate",
        labels={
            month_column: "Month",
            rate_column: "Propagation Rate"
        }
    )

    fig.update_layout(
        height=450,
        template="plotly_white",
        yaxis_tickformat=".1%"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CASCADE ACTIVITY BY MONTH
# ============================================================

st.divider()

st.subheader("🌊 Cascade Activity by Month")

cascade_display = cascade_monthly.copy()

cascade_display = cascade_display.loc[
    :,
    [
        c for c in cascade_display.columns
        if not c.lower().startswith("unnamed")
    ]
]

st.dataframe(
    cascade_display,
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
    Interaction activity increases overall across the six-month
    simulation period, with June recording 9,463 interactions
    compared with 6,570 in January.

    The highest observed activity occurs at 23:00, while Tuesday
    is the most active weekday in the generated dataset.

    The average monthly propagation rate is approximately 41.83%,
    with May showing the highest observed monthly rate at 43.49%.

    These temporal patterns are characteristics of the controlled
    synthetic dataset and should not be generalized to real-world
    social-media behavior.
    """
)


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "Source: Phase 4 Temporal and Cross-Platform Diffusion Analysis."
)