# Information Diffusion in Social Networks

## 🚀 Live Interactive Dashboard

👉 **[Open the Live SNA Information Diffusion Dashboard](https://sna-informationdiffusion-118.streamlit.app/)**

Explore the interactive dashboard for network structure, user influence, information cascades, cross-platform diffusion, community diffusion, temporal patterns, and integrated findings.

---

## 📌 Project Overview

This Social Network Analysis case study focuses on **Information Diffusion in Social Networks**.

The project analyzes how information spreads through social networks and identifies how **user influence, network structure, communities, and time** affect the propagation of information.

### Problem Statement

> **To analyze how information spreads through social networks and identify how user influence, network structure, communities, and time affect the propagation of information.**

### Research Question

> **How does information spread across social networks, and what factors determine how far, how fast, and through whom it spreads?**

---

## 🎯 Objectives

The main objectives of this study are to:

- Analyze the structure of a social interaction network.
- Identify influential and highly connected users.
- Study how information propagates through information cascades.
- Analyze cross-platform information diffusion.
- Examine cross-community propagation.
- Investigate temporal patterns in information activity.
- Compare engagement with actual information propagation.
- Identify factors associated with wider information diffusion.
- Interpret the findings in the context of real-world social networks.

---

# 🌐 Platforms

The synthetic dataset models interactions across five social platforms:

- Instagram
- Facebook
- Reddit
- YouTube
- X

---

# 📊 Dataset

This project uses a **controlled synthetic social-network dataset** designed specifically for studying information diffusion.

The dataset contains:

| Feature | Value |
|---|---:|
| Users | 10,000 |
| Interactions | 50,000 |
| Information Items | 1,000 |
| Communities | 25 |
| Platforms | 5 |
| Cascades | 1,876 |
| Topics | 10 |
| Content Types | 5 |

### Interaction Types

The dataset contains four major interaction categories:

- **Likes / Reactions**
- **Comments / Replies**
- **Shares / Reposts / Retweets**
- **Cross-platform transfers**

Likes and comments are primarily treated as **engagement**, while shares, reposts, retweets, and cross-platform transfers represent **information propagation**.

---

# 🧠 Social Network Analysis

The project models users and their interactions as a **directed social network**.

In the network:

- **Nodes** represent users.
- **Directed edges** represent interactions between users.
- Edge direction represents the direction of the interaction or information movement.

Two major network views are analyzed:

### Full Interaction Network

Includes all interaction types such as likes, comments, shares, and cross-platform transfers.

### Propagation Network

Focuses specifically on interactions that represent information propagation.

---

# 🔍 Network Structure

The full interaction network contains:

- **10,000 users**
- **48,463 directed edges**
- Network density of approximately **0.000485**
- Largest weakly connected component containing **9,421 users**
- **580 weakly connected components**

The network is therefore highly sparse, while still containing a very large connected component.

---

# 👤 User Influence

Users are categorized into four user types:

- **Regular**
- **Active**
- **Bridge**
- **Influential**

The project uses several network centrality measures to understand user importance.

### Centrality Measures

- Degree Centrality
- PageRank
- Betweenness Centrality
- Closeness Centrality
- Eigenvector Centrality
- Propagation-specific centrality measures

### Influence and Centrality

The strongest observed relationship among the main influence measures was:

**Influence Score ↔ PageRank: r = 0.7014**

This indicates a strong positive association between the influence score and PageRank within the synthetic network.

Influential users also showed higher average connectivity and centrality values than Regular users.

---

# 🌊 Information Cascades

Information cascades are used to study how individual pieces of information propagate through the network.

The dataset contains:

**1,876 information cascades**

### Cascade Statistics

| Metric | Value |
|---|---:|
| Average cascade size | 26.65 |
| Median cascade size | 28 |
| Maximum cascade size | 75 |
| Average cascade depth | 26.65 |
| Maximum cascade depth | 75 |
| Average cascade duration | 249.55 hours |
| Maximum cascade duration | 871.26 hours |

The analysis examines:

- Cascade size
- Cascade depth
- Cascade duration
- Number of users involved
- Number of platforms involved
- Number of communities involved
- Cross-platform propagation
- Cross-community propagation
- Propagation rate

### Important Dataset Limitation

The synthetic cascades are predominantly **chain-like** rather than highly branching diffusion trees.

As a result, cascade size and cascade depth are closely aligned.

This is treated as a limitation of the controlled synthetic dataset and **not as evidence that real-world information diffusion is always chain-like**.

---

# 🔄 Cross-Platform Diffusion

The project studies how information moves between different social platforms.

### Key Finding

**1,729 out of 1,876 cascades (92.16%)** involved cross-platform diffusion.

Average cascade size:

| Cascade Type | Average Size |
|---|---:|
| With cross-platform diffusion | 27.54 |
| Without cross-platform diffusion | 16.26 |

This shows that, within the synthetic network, cascades involving multiple platforms were associated with larger cascade sizes.

The project also analyzes individual platform-to-platform transition pathways.

---

# 🏘️ Cross-Community Diffusion

Information diffusion is also analyzed across community boundaries.

### Key Finding

**1,822 out of 1,876 cascades (97.12%)** involved cross-community diffusion.

Average cascade size:

| Cascade Type | Average Size |
|---|---:|
| With cross-community diffusion | 27.13 |
| Without cross-community diffusion | 10.63 |

This indicates that cascades crossing community boundaries were associated with substantially larger cascade sizes in the synthetic dataset.

---

# ⏱️ Temporal Analysis

The dataset covers approximately six months:

**January 2026 – June 2026**

Monthly interaction activity:

| Month | Interactions |
|---|---:|
| January | 6,570 |
| February | 7,444 |
| March | 8,731 |
| April | 8,519 |
| May | 9,273 |
| June | 9,463 |

The project also analyzes:

- Activity by hour
- Activity by day of week
- Monthly cascade activity
- Platform activity over time
- Monthly propagation rates

The highest observed hourly activity occurred at **23:00**.

Tuesday recorded the highest total activity among the weekdays.

Because the dataset is synthetic and controlled, these temporal patterns should **not** be interpreted as real-world behavioral patterns.

---

# 📈 Propagation vs Engagement

An important part of the analysis is distinguishing between **interaction** and **actual information propagation**.

### Engagement

Includes:

- Likes / Reactions
- Comments / Replies

### Propagation

Includes:

- Shares / Reposts / Retweets
- Cross-platform transfers

Monthly propagation rates were also calculated.

The average monthly propagation rate was approximately:

**41.83%**

The highest observed monthly propagation rate was:

**43.49% in May**

This distinction allows the study to examine whether information is simply receiving engagement or actually moving through the network.

---

# 📊 Visualizations

The project contains visualizations covering:

- Monthly interaction activity
- Interaction types over time
- Platform activity over time
- Activity by hour
- Activity by day of week
- Cascade size distribution
- Cascade duration distribution
- Cross-platform diffusion matrix
- Top platform transition pathways
- Propagation vs engagement
- Monthly propagation rate
- Cross-community diffusion by platform
- Cascades by starting month
- Community diffusion heatmap

---

# 🖥️ Interactive Streamlit Dashboard

The project includes an interactive **Streamlit dashboard**.

### Dashboard Sections

1. **Network**
2. **Influence**
3. **Cascades**
4. **Platforms**
5. **Communities**
6. **Temporal**
7. **Findings**
8. **Methodology**

### 🚀 Open the Live Dashboard

👉 **[Open SNA Information Diffusion Dashboard](https://sna-informationdiffusion-118.streamlit.app/)**

The dashboard provides an interactive way to explore the results without running the analysis scripts manually.

---

# ⚙️ Running the Dashboard Locally

Clone the repository:

```bash
git clone https://github.com/gayas-sheik/SNA-InformationDiffusion.git