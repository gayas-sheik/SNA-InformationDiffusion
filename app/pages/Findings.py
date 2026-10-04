import streamlit as st
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Findings | SNA Case Study",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("📊 Key Findings")

st.markdown(
    """
    Integrated findings from the network, centrality, cascade,
    cross-platform, community, and temporal analyses.
    """
)

st.divider()


# ============================================================
# FINDING 1
# ============================================================

st.subheader("1. Network Structure")

st.metric(
    "Network Edges",
    "48,463"
)

st.write(
    """
    The full interaction network contains 10,000 users and 48,463
    unique edges. The network density is 0.000485, while the largest
    weakly connected component contains 9,421 users, representing
    94.21% of the network.
    """
)


# ============================================================
# FINDING 2
# ============================================================

st.divider()

st.subheader("2. User Influence")

c1, c2 = st.columns(2)

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

st.write(
    """
    Influential users have the highest average influence and activity
    among the defined user types.
    """
)


# ============================================================
# FINDING 3
# ============================================================

st.divider()

st.subheader("3. Centrality and Influence")

st.metric(
    "Influence ↔ PageRank",
    "r = 0.7014"
)

st.write(
    """
    PageRank shows the strongest meaningful relationship with user
    influence among the centrality measures examined.
    """
)

st.caption(
    "This is an association and does not establish causation."
)


# ============================================================
# FINDING 4
# ============================================================

st.divider()

st.subheader("4. Information Cascades")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Cascades",
        "1,876"
    )

with c2:
    st.metric(
        "Average Size",
        "26.65"
    )

with c3:
    st.metric(
        "Maximum Size",
        "75"
    )

with c4:
    st.metric(
        "Average Duration",
        "249.55 h"
    )

st.write(
    """
    The analysis identified 1,876 information cascades. The average
    cascade size is 26.65 interactions, with a maximum size of 75.
    """
)


# ============================================================
# FINDING 5
# ============================================================

st.divider()

st.subheader("5. Cross-Platform Diffusion")

c1, c2 = st.columns(2)

with c1:
    st.metric(
        "Cross-Platform Cascades",
        "1,729 / 1,876"
    )

with c2:
    st.metric(
        "Percentage",
        "92.16%"
    )

st.write(
    """
    Cross-platform propagation occurs in the large majority of
    analyzed cascades. Cascades involving cross-platform diffusion
    have a mean size of 27.54 compared with 16.26 for cascades
    without cross-platform events.
    """
)


# ============================================================
# FINDING 6
# ============================================================

st.divider()

st.subheader("6. Cross-Community Diffusion")

c1, c2 = st.columns(2)

with c1:
    st.metric(
        "Cross-Community Cascades",
        "1,822 / 1,876"
    )

with c2:
    st.metric(
        "Percentage",
        "97.12%"
    )

st.write(
    """
    Cross-community propagation occurs in 97.12% of analyzed
    cascades. Cascades involving multiple communities have a mean
    size of 27.13 compared with 10.63 for cascades without
    cross-community diffusion.
    """
)


# ============================================================
# FINDING 7
# ============================================================

st.divider()

st.subheader("7. Temporal Growth")

c1, c2 = st.columns(2)

with c1:
    st.metric(
        "January",
        "6,570 interactions"
    )

with c2:
    st.metric(
        "June",
        "9,463 interactions"
    )

st.write(
    """
    Overall interaction activity increases across the six-month
    simulation period.
    """
)


# ============================================================
# FINDING 8
# ============================================================

st.divider()

st.subheader("8. Daily Activity")

c1, c2 = st.columns(2)

with c1:
    st.metric(
        "Most Active Hour",
        "23:00"
    )

with c2:
    st.metric(
        "Activity at 23:00",
        "2,568"
    )

st.write(
    """
    23:00 is the highest-activity hour in the generated dataset.
    """
)


# ============================================================
# FINDING 9
# ============================================================

st.divider()

st.subheader("9. Weekly Activity")

st.metric(
    "Most Active Weekday",
    "Tuesday — 8,564 interactions"
)

st.write(
    """
    Tuesday records the highest interaction activity among the
    weekdays in the simulated dataset.
    """
)


# ============================================================
# FINDING 10
# ============================================================

st.divider()

st.subheader("10. Propagation Rate")

c1, c2 = st.columns(2)

with c1:
    st.metric(
        "Average Monthly Rate",
        "41.83%"
    )

with c2:
    st.metric(
        "Highest Monthly Rate",
        "43.49% — May"
    )

st.write(
    """
    The monthly propagation rate remains relatively consistent
    throughout the six-month simulation, with May recording the
    highest observed rate.
    """
)


# ============================================================
# OVERALL DIFFUSION PATTERN
# ============================================================

st.divider()

st.subheader("🔎 Overall Diffusion Pattern")

st.success(
    """
    The integrated analysis indicates that information diffusion in
    the simulated network is shaped by network connectivity, user
    influence, temporal activity, cross-platform propagation, and
    cross-community movement.
    """
)


# ============================================================
# LIMITATION
# ============================================================

st.divider()

st.subheader("⚠️ Interpretation Boundary")

st.warning(
    """
    The dataset is controlled and synthetic. Therefore, these findings
    demonstrate patterns produced within the simulated network and
    should not be interpreted as direct real-world behavioral or
    causal conclusions.

    In addition, the generated cascades are predominantly chain-like,
    which limits the interpretation of branching diffusion structures.
    """
)


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "Source: Phase 6 Integrated Analysis and Findings."
)