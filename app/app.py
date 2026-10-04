import streamlit as st
import pandas as pd
from pathlib import Path

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Information Diffusion | SNA Case Study",
    page_icon="🌐",
    layout="wide"
)

# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e3e8ef;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.metric-title {
    font-size: 14px;
    color: #667085;
}

.metric-value {
    font-size: 28px;
    font-weight: 700;
    color: #182230;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #182230;
    margin-top: 25px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# TITLE
# ============================================================

st.title("🌐 Information Diffusion in Social Networks")

st.markdown(
    """
    ### Interactive Social Network Analysis Dashboard

    **SNA Case Study**

    Explore network structure, user influence, information cascades,
    cross-platform diffusion, community diffusion, and temporal patterns.
    """
)

st.divider()

# ============================================================
# LOAD RESULTS
# ============================================================

network_summary_file = RESULTS_DIR / "network_summary.csv"
cascade_file = RESULTS_DIR / "cascade_analysis.csv"
centrality_file = RESULTS_DIR / "centrality_analysis.csv"

try:
    network_summary = pd.read_csv(network_summary_file)
    cascade_analysis = pd.read_csv(cascade_file)
    centrality_analysis = pd.read_csv(centrality_file)

except FileNotFoundError as e:
    st.error(
        f"Required result file was not found:\n\n{e}\n\n"
        "Make sure the Streamlit app is inside the app folder "
        "of your SNA-CaseStudy project."
    )
    st.stop()

# ============================================================
# KEY METRICS
# ============================================================

st.markdown(
    '<div class="section-title">📊 Study Overview</div>',
    unsafe_allow_html=True
)

# Known project-level metrics
total_interactions = 50000
total_users = 10000
total_information = 1000
total_communities = 25
total_platforms = 5
total_cascades = len(cascade_analysis)

# ------------------------------------------------------------
# Metric cards
# ------------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Interactions",
        f"{total_interactions:,}"
    )

with col2:
    st.metric(
        "Users",
        f"{total_users:,}"
    )

with col3:
    st.metric(
        "Information Items",
        f"{total_information:,}"
    )

with col4:
    st.metric(
        "Cascades",
        f"{total_cascades:,}"
    )

col5, col6, col7 = st.columns(3)

with col5:
    st.metric(
        "Communities",
        f"{total_communities:,}"
    )

with col6:
    st.metric(
        "Platforms",
        f"{total_platforms:,}"
    )

with col7:
    st.metric(
        "Network Edges",
        "48,463"
    )

# ============================================================
# NETWORK OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">🕸️ Network Overview</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    st.subheader("Full Interaction Network")

    st.write(
        "The full interaction network represents users connected "
        "through interactions such as likes, comments, shares, "
        "and cross-platform shares."
    )

    st.metric(
        "Unique Edges",
        "48,463"
    )

    st.metric(
        "Network Density",
        "0.000485"
    )

with col2:

    st.subheader("Propagation Network")

    st.write(
        "The propagation network isolates interactions representing "
        "information propagation, including shares and cross-platform "
        "shares."
    )

    st.metric(
        "Propagation Edges",
        "20,801"
    )

    st.metric(
        "Propagation Density",
        "0.000208"
    )

# ============================================================
# CASCADE OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">🌊 Information Diffusion</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average Cascade Size",
        "26.65"
    )

with col2:
    st.metric(
        "Maximum Cascade Size",
        "75"
    )

with col3:
    st.metric(
        "Average Cascade Depth",
        "26.65"
    )

# ============================================================
# IMPORTANT FINDINGS
# ============================================================

st.markdown(
    '<div class="section-title">🔎 Key Findings</div>',
    unsafe_allow_html=True
)

findings = [
    ("Network Structure",
     "The network contains 48,463 unique interaction edges "
     "across 10,000 users."),

    ("User Influence",
     "Influence and PageRank show a meaningful positive relationship "
     "(r = 0.7014)."),

    ("Cross-Platform Diffusion",
     "92.16% of information cascades involve cross-platform propagation."),

    ("Cross-Community Diffusion",
     "97.12% of information cascades involve multiple communities."),

    ("Propagation Rate",
     "The average monthly propagation rate is 41.83%, "
     "with the highest value of 43.49% in May 2026."),

    ("Synthetic Dataset",
     "The findings represent patterns observed in a controlled "
     "synthetic social-network environment.")
]

for title, description in findings:

    with st.container(border=True):

        st.markdown(
            f"**{title}**"
        )

        st.write(description)

# ============================================================
# STUDY SCOPE
# ============================================================

st.divider()

st.info(
    """
    **Study Scope**

    This study uses a controlled synthetic dataset. Therefore,
    the observed patterns demonstrate the behavior of the simulated
    network and should not be interpreted as direct real-world
    behavioral or causal findings.
    """
)

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SNA Case Study • Information Diffusion in Social Networks"
)