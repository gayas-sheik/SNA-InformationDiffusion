import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Methodology | SNA Case Study",
    page_icon="ℹ️",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("ℹ️ Methodology")

st.markdown(
    """
    Overview of the data, network model, analytical techniques,
    validation process, and interpretation boundaries used in
    the Information Diffusion SNA case study.
    """
)

st.divider()


# ============================================================
# RESEARCH PROBLEM
# ============================================================

st.subheader("Research Problem")

st.write(
    """
    To analyze how information spreads through social networks and
    identify how user influence, network structure, communities,
    and time affect the propagation of information.
    """
)

st.subheader("Research Question")

st.write(
    """
    How does information spread across social networks, and what
    factors determine how far, how fast, and through whom it spreads?
    """
)


# ============================================================
# DATASET
# ============================================================

st.divider()

st.subheader("Dataset")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Interactions", "50,000")

with c2:
    st.metric("Users", "10,000")

with c3:
    st.metric("Information Items", "1,000")

with c4:
    st.metric("Communities", "25")

c5, c6 = st.columns(2)

with c5:
    st.metric("Platforms", "5")

with c6:
    st.metric("Cascades", "1,876")


st.write(
    """
    The study uses a controlled synthetic social-network dataset.
    The dataset was generated to provide a consistent environment
    containing users, information items, communities, interactions,
    timestamps, and diffusion relationships across five platforms.
    """
)


# ============================================================
# PLATFORMS
# ============================================================

st.subheader("Simulated Platforms")

platforms = [
    "Instagram",
    "Facebook",
    "Reddit",
    "YouTube",
    "X"
]

st.write("The simulated network contains:")

for platform in platforms:
    st.write(f"• {platform}")


# ============================================================
# INTERACTION TYPES
# ============================================================

st.subheader("Interaction Types")

interaction_types = {
    "Like / Reaction": "Engagement",
    "Comment / Reply": "Engagement",
    "Share / Repost / Retweet": "Propagation",
    "Cross-Platform Share": "Propagation"
}

for interaction, purpose in interaction_types.items():
    st.write(
        f"• **{interaction}** — {purpose}"
    )


# ============================================================
# NETWORK MODEL
# ============================================================

st.divider()

st.subheader("Network Model")

st.write(
    """
    Users are represented as nodes, while interactions between users
    are represented as directed edges. Two analytical views were used:
    the full interaction network and the propagation network.
    """
)

c1, c2 = st.columns(2)

with c1:

    st.markdown("### Full Interaction Network")

    st.write(
        """
        Includes all modeled user interactions, including likes,
        comments, shares, and cross-platform shares.
        """
    )

with c2:

    st.markdown("### Propagation Network")

    st.write(
        """
        Focuses on interactions that represent information propagation,
        particularly shares and cross-platform shares.
        """
    )


# ============================================================
# SNA TECHNIQUES
# ============================================================

st.divider()

st.subheader("SNA Techniques")

techniques = {
    "Degree Centrality":
        "Measures direct connectivity through incoming and outgoing interactions.",

    "PageRank":
        "Identifies users receiving importance from connected users.",

    "Betweenness Centrality":
        "Identifies users positioned on paths connecting other users.",

    "Closeness Centrality":
        "Measures how close a user is to other users in the network.",

    "Eigenvector Centrality":
        "Measures connectivity to other highly connected users.",

    "Community Analysis":
        "Examines network structure and diffusion across user communities.",

    "Cascade Analysis":
        "Measures the size, depth, duration, and reach of information cascades.",

    "Temporal Analysis":
        "Examines how interaction and propagation activity changes over time.",

    "Cross-Platform Analysis":
        "Examines movement of information between the five simulated platforms."
}

for technique, explanation in techniques.items():

    with st.container(border=True):

        st.markdown(
            f"**{technique}**"
        )

        st.write(explanation)


# ============================================================
# ANALYSIS PIPELINE
# ============================================================

st.divider()

st.subheader("Analysis Pipeline")

st.markdown(
    """
    **Phase 1 — Network Construction**

    Build the full interaction and propagation networks.

    ↓

    **Phase 2 — Centrality, Influence & Community Analysis**

    Measure user importance and network position.

    ↓

    **Phase 3 — Information Cascade & Diffusion Analysis**

    Analyze cascade size, depth, duration, and propagation.

    ↓

    **Phase 4 — Temporal & Cross-Platform Analysis**

    Analyze time patterns and movement between platforms and communities.

    ↓

    **Phase 5 — Visualization**

    Generate analytical visualizations.

    ↓

    **Phase 6 — Integrated Findings**

    Combine the results into the major findings of the study.
    """
)


# ============================================================
# VALIDATION
# ============================================================

st.divider()

st.subheader("Dataset Validation")

st.write(
    """
    The generated dataset was validated before analysis to verify
    structural consistency and diffusion relationships.
    """
)

validation_items = [
    "50,000 total interactions",
    "10,000 users",
    "1,000 information items",
    "1,876 cascades",
    "No duplicate interaction IDs",
    "No broken parent references",
    "No incorrect cascade depths",
    "No parent timestamp violations",
    "No cross-platform consistency errors",
    "No cross-community consistency errors",
    "No self-interactions"
]

for item in validation_items:
    st.write(f"✅ {item}")


# ============================================================
# INTERPRETATION BOUNDARY
# ============================================================

st.divider()

st.subheader("Interpretation Boundary")

st.warning(
    """
    The dataset is synthetic and controlled. Therefore, the results
    describe patterns produced within the simulated social network
    and should not be interpreted as direct real-world behavioral
    or causal conclusions.
    """
)


# ============================================================
# LIMITATIONS
# ============================================================

st.subheader("Limitations")

st.write(
    """
    • The dataset is synthetic rather than collected from real
      social-media platforms.

    • Platform activity is controlled and relatively balanced by design.

    • The generated cascades are predominantly chain-like, limiting
      analysis of complex branching diffusion structures.

    • Correlations identify associations and do not establish causality.
    """
)


# ============================================================
# REAL-WORLD APPLICATIONS
# ============================================================

st.divider()

st.subheader("Potential Real-World Applications")

applications = [
    "Misinformation and rumor propagation analysis",
    "Identification of influential users",
    "Viral-content monitoring",
    "Cross-platform information tracking",
    "Community-level information diffusion analysis",
    "Emergency and public-information propagation studies",
    "Marketing and campaign diffusion analysis"
]

for application in applications:
    st.write(f"• {application}")


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SNA Case Study • Information Diffusion in Social Networks"
)