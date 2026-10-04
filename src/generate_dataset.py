"""
Synthetic Information Diffusion Dataset Generator
=================================================

Problem Statement:
To analyze how information spreads through social networks and identify
how user influence, network structure, communities, and time affect
the propagation of information.

Dataset:
- 10,000 users
- 1,000 information items
- 25 communities
- 5 platforms
- 50,000 interaction records
- 10,000 source events per platform
- Realistic diffusion cascades
- Parent-child propagation relationships
- Temporal propagation
- Cross-platform propagation
- Cross-community propagation
"""

from pathlib import Path
from datetime import datetime, timedelta
import random

import numpy as np
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

SEED = 42

NUM_USERS = 10_000
NUM_INFORMATION_ITEMS = 1_000
NUM_COMMUNITIES = 25

TOTAL_EVENTS = 50_000
EVENTS_PER_PLATFORM = 10_000

PLATFORMS = [
    "Instagram",
    "Facebook",
    "Reddit",
    "YouTube",
    "X",
]

TOPICS = [
    "Technology",
    "Artificial Intelligence",
    "Gaming",
    "Sports",
    "Education",
    "Entertainment",
    "Science",
    "News",
    "Health",
    "Politics",
]

CONTENT_TYPES = [
    "Text",
    "Image",
    "Video",
    "Article",
    "Link",
]

INTERACTION_TYPES = [
    "Like",
    "Comment",
    "Share",
    "CrossPlatformShare",
]

START_DATE = datetime(2026, 1, 1)
END_DATE = datetime(2026, 6, 30, 23, 59, 59)


# ============================================================
# RANDOM SEED
# ============================================================

random.seed(SEED)
np.random.seed(SEED)


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data" / "synthetic"

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# USER GENERATION
# ============================================================

def generate_users():

    print("Generating users...")

    users = []

    user_types = [
        "Regular",
        "Active",
        "Influential",
        "Bridge",
    ]

    user_type_weights = [
        0.72,
        0.20,
        0.06,
        0.02,
    ]

    platform_weights = [
        0.24,
        0.20,
        0.16,
        0.16,
        0.24,
    ]

    for i in range(NUM_USERS):

        user_id = f"U{i + 1:05d}"

        community_number = (
            i % NUM_COMMUNITIES
        ) + 1

        user_type = random.choices(
            user_types,
            weights=user_type_weights,
            k=1,
        )[0]

        primary_platform = random.choices(
            PLATFORMS,
            weights=platform_weights,
            k=1,
        )[0]

        if user_type == "Regular":

            activity = np.random.beta(
                2,
                8,
            )

            influence = np.random.beta(
                2,
                10,
            )

        elif user_type == "Active":

            activity = np.random.beta(
                5,
                4,
            )

            influence = np.random.beta(
                4,
                7,
            )

        elif user_type == "Influential":

            activity = np.random.beta(
                7,
                2,
            )

            influence = np.random.beta(
                8,
                2,
            )

        else:

            activity = np.random.beta(
                6,
                3,
            )

            influence = np.random.beta(
                6,
                4,
            )

        users.append({
            "user_id": user_id,
            "community_id": (
                f"C{community_number:02d}"
            ),
            "primary_platform": primary_platform,
            "user_type": user_type,
            "activity_score": round(
                float(activity),
                4,
            ),
            "influence_score": round(
                float(influence),
                4,
            ),
        })

    return pd.DataFrame(users)


# ============================================================
# INFORMATION GENERATION
# ============================================================

def generate_information_items(
    users_df,
):

    print("Generating information items...")

    users = users_df[
        "user_id"
    ].tolist()

    user_platform = dict(
        zip(
            users_df["user_id"],
            users_df["primary_platform"],
        )
    )

    information = []

    virality_levels = [
        "Low",
        "Medium",
        "High",
        "Viral",
    ]

    virality_weights = [
        0.52,
        0.30,
        0.14,
        0.04,
    ]

    creation_range = int(
        (
            END_DATE
            - START_DATE
        ).total_seconds()
    )

    for i in range(
        NUM_INFORMATION_ITEMS
    ):

        information_id = (
            f"INFO{i + 1:04d}"
        )

        origin_user = random.choice(
            users
        )

        virality_level = random.choices(
            virality_levels,
            weights=virality_weights,
            k=1,
        )[0]

        if virality_level == "Low":

            virality_score = np.random.uniform(
                0.05,
                0.25,
            )

        elif virality_level == "Medium":

            virality_score = np.random.uniform(
                0.25,
                0.55,
            )

        elif virality_level == "High":

            virality_score = np.random.uniform(
                0.55,
                0.80,
            )

        else:

            virality_score = np.random.uniform(
                0.80,
                1.00,
            )

        created_at = (
            START_DATE
            + timedelta(
                seconds=random.randint(
                    0,
                    creation_range,
                )
            )
        )

        information.append({
            "information_id": information_id,
            "topic": random.choice(
                TOPICS
            ),
            "content_type": random.choice(
                CONTENT_TYPES
            ),
            "origin_user": origin_user,
            "origin_platform": (
                user_platform[origin_user]
            ),
            "virality_level": (
                virality_level
            ),
            "virality_score": round(
                float(virality_score),
                4,
            ),
            "created_at": created_at,
        })

    return pd.DataFrame(
        information
    )


# ============================================================
# EVENT ALLOCATION
# ============================================================

def allocate_events_to_information(
    information_df,
):

    virality = (
        information_df[
            "virality_score"
        ].to_numpy()
    )

    weights = (
        0.20
        + virality ** 2.2
    )

    probabilities = (
        weights / weights.sum()
    )

    # Every information item gets at least 10 events.
    base = np.full(
        NUM_INFORMATION_ITEMS,
        10,
        dtype=int,
    )

    remaining = (
        TOTAL_EVENTS
        - base.sum()
    )

    extra = np.random.multinomial(
        remaining,
        probabilities,
    )

    return base + extra


# ============================================================
# TARGET USER
# ============================================================

def choose_target_user(
    users_df,
    source_user,
    source_community,
    desired_platform,
    cross_community_probability,
):

    candidates = users_df[
        users_df[
            "primary_platform"
        ]
        == desired_platform
    ]

    if candidates.empty:

        candidates = users_df

    # Prefer same-community propagation.
    if (
        random.random()
        > cross_community_probability
    ):

        community_candidates = (
            candidates[
                candidates[
                    "community_id"
                ]
                == source_community
            ]
        )

        if not community_candidates.empty:

            candidates = (
                community_candidates
            )

    scores = (
        0.55
        * candidates[
            "activity_score"
        ].to_numpy()
        +
        0.45
        * candidates[
            "influence_score"
        ].to_numpy()
    )

    scores = np.maximum(
        scores,
        0.001,
    )

    probabilities = (
        scores / scores.sum()
    )

    target = np.random.choice(
        candidates[
            "user_id"
        ].to_numpy(),
        p=probabilities,
    )

    attempts = 0

    while (
        target == source_user
        and attempts < 20
    ):

        target = np.random.choice(
            candidates[
                "user_id"
            ].to_numpy(),
            p=probabilities,
        )

        attempts += 1

    return target


# ============================================================
# PLATFORM TRANSITION
# ============================================================

def choose_next_platform(
    current_platform,
    remaining_platform_counts,
    virality,
):

    available = [
        platform
        for platform in PLATFORMS
        if remaining_platform_counts[
            platform
        ] > 0
    ]

    if not available:

        return current_platform

    cross_probability = (
        0.05
        + 0.25 * virality
    )

    if len(available) == 1:

        return available[0]

    if (
        random.random()
        < cross_probability
    ):

        other = [
            p
            for p in available
            if p != current_platform
        ]

        if other:

            return random.choice(
                other
            )

    if (
        current_platform
        in available
    ):

        return current_platform

    return random.choice(
        available
    )


# ============================================================
# INTERACTION TYPE
# ============================================================

def choose_interaction_type(
    source_platform,
    target_platform,
    virality,
):

    # Cross-platform movement is always
    # represented as a cross-platform share.
    if (
        source_platform
        != target_platform
    ):

        return "CrossPlatformShare"

    share_probability = (
        0.18
        + 0.30 * virality
    )

    comment_probability = 0.27

    if (
        random.random()
        < share_probability
    ):

        return "Share"

    if (
        random.random()
        < comment_probability
    ):

        return "Comment"

    return "Like"


# ============================================================
# PROPAGATION DELAY
# ============================================================

def sample_delay_seconds(
    interaction_type,
    virality,
):

    if interaction_type == "Like":

        mean_hours = (
            2.0
            + 5.0 * (1.0 - virality)
        )

    elif interaction_type == "Comment":

        mean_hours = (
            4.0
            + 8.0 * (1.0 - virality)
        )

    else:

        mean_hours = (
            6.0
            + 20.0 * (1.0 - virality)
        )

    delay_hours = np.random.exponential(
        mean_hours
    )

    return max(
        1.0,
        delay_hours * 3600.0,
    )


# ============================================================
# SAFE TIMESTAMP
# ============================================================

def generate_next_timestamp(
    current_time,
    interaction_type,
    virality,
):
    """
    Generate a strictly later timestamp.

    The natural diffusion delay is sampled first.

    If the natural delay would exceed the study window,
    the delay is compressed to a fraction of the remaining
    study period.

    This guarantees:

        current_time < next_time <= END_DATE

    without ever terminating a cascade.
    """

    natural_delay = (
        sample_delay_seconds(
            interaction_type,
            virality,
        )
    )

    remaining_seconds = (
        END_DATE
        - current_time
    ).total_seconds()

    if remaining_seconds <= 1:

        # This situation should be extremely rare.
        # Use a deterministic tiny step backward from END_DATE
        # only if current_time itself is at the boundary.
        return END_DATE

    # Never consume the entire remaining time in one step.
    #
    # This guarantees that even very deep cascades can
    # continue generating events without running outside
    # the study period.
    maximum_allowed_delay = (
        remaining_seconds * 0.20
    )

    actual_delay = min(
        natural_delay,
        maximum_allowed_delay,
    )

    actual_delay = max(
        1.0,
        actual_delay,
    )

    next_time = (
        current_time
        + timedelta(
            seconds=actual_delay
        )
    )

    # Final safety clamp.
    if next_time > END_DATE:

        next_time = END_DATE

    # Ensure strict temporal ordering.
    if next_time <= current_time:

        next_time = (
            current_time
            + timedelta(
                seconds=1
            )
        )

        if next_time > END_DATE:

            next_time = END_DATE

    return next_time


# ============================================================
# CASCADE GENERATION
# ============================================================

def generate_events(
    users_df,
    information_df,
):

    print(
        "Generating genuine diffusion events..."
    )

    user_community = dict(
        zip(
            users_df["user_id"],
            users_df["community_id"],
        )
    )

    user_platform = dict(
        zip(
            users_df["user_id"],
            users_df["primary_platform"],
        )
    )

    information_records = (
        information_df
        .to_dict("records")
    )

    event_counts = (
        allocate_events_to_information(
            information_df
        )
    )

    # Exactly 10,000 source events per platform.
    remaining_platform_counts = {
        platform: EVENTS_PER_PLATFORM
        for platform in PLATFORMS
    }

    events = []

    global_event_number = 0

    for info_index, info in enumerate(
        information_records
    ):

        required_events = int(
            event_counts[info_index]
        )

        information_id = (
            info["information_id"]
        )

        virality = float(
            info["virality_score"]
        )

        origin_user = (
            info["origin_user"]
        )

        origin_platform = (
            info["origin_platform"]
        )

        # Number of independent cascades.
        if virality < 0.25:

            cascade_count = 1

        elif virality < 0.55:

            cascade_count = random.randint(
                1,
                3,
            )

        elif virality < 0.80:

            cascade_count = random.randint(
                2,
                5,
            )

        else:

            cascade_count = random.randint(
                3,
                8,
            )

        remaining_info_events = (
            required_events
        )

        for cascade_number in range(
            cascade_count
        ):

            if remaining_info_events <= 0:

                break

            cascade_id = (
                f"CASCADE_"
                f"{information_id}_"
                f"{cascade_number + 1:02d}"
            )

            remaining_cascades = (
                cascade_count
                - cascade_number
            )

            if remaining_cascades == 1:

                cascade_target = (
                    remaining_info_events
                )

            else:

                minimum_remaining = (
                    remaining_cascades - 1
                )

                maximum_for_this = (
                    remaining_info_events
                    - minimum_remaining
                )

                average_fraction = (
                    0.35
                    + 0.45 * virality
                )

                suggested = int(
                    remaining_info_events
                    * average_fraction
                    / remaining_cascades
                )

                cascade_target = max(
                    1,
                    min(
                        suggested,
                        maximum_for_this,
                    ),
                )

            # ------------------------------------------------
            # Cascade state
            # ------------------------------------------------

            current_user = origin_user

            current_platform = (
                origin_platform
            )

            current_time = (
                info["created_at"]
            )

            parent_interaction_id = None

            depth = 0

            # ------------------------------------------------
            # Generate events
            # ------------------------------------------------

            for _ in range(
                cascade_target
            ):

                # If current source platform has exhausted
                # its quota, move the current source to a
                # platform that still has quota.
                if (
                    remaining_platform_counts[
                        current_platform
                    ] <= 0
                ):

                    available = [
                        p
                        for p in PLATFORMS
                        if remaining_platform_counts[
                            p
                        ] > 0
                    ]

                    if not available:

                        raise RuntimeError(
                            "No platform quota remaining "
                            "while events are still required."
                        )

                    current_platform = min(
                        available,
                        key=lambda p:
                            remaining_platform_counts[
                                p
                            ],
                    )

                    platform_users = (
                        users_df[
                            users_df[
                                "primary_platform"
                            ]
                            == current_platform
                        ]["user_id"]
                        .to_numpy()
                    )

                    current_user = (
                        random.choice(
                            platform_users
                        )
                    )

                # ------------------------------------------------
                # Choose target platform
                # ------------------------------------------------

                target_platform = (
                    choose_next_platform(
                        current_platform,
                        remaining_platform_counts,
                        virality,
                    )
                )

                # Safety if chosen platform is exhausted.
                if (
                    remaining_platform_counts[
                        target_platform
                    ] <= 0
                ):

                    available = [
                        p
                        for p in PLATFORMS
                        if remaining_platform_counts[
                            p
                        ] > 0
                    ]

                    if not available:

                        raise RuntimeError(
                            "No target platform quota remaining."
                        )

                    target_platform = (
                        random.choice(
                            available
                        )
                    )

                # ------------------------------------------------
                # Community selection
                # ------------------------------------------------

                source_community = (
                    user_community[
                        current_user
                    ]
                )

                cross_community_probability = (
                    0.10
                    + 0.30 * virality
                )

                target_user = (
                    choose_target_user(
                        users_df,
                        current_user,
                        source_community,
                        target_platform,
                        cross_community_probability,
                    )
                )

                # ------------------------------------------------
                # Interaction type
                # ------------------------------------------------

                interaction_type = (
                    choose_interaction_type(
                        current_platform,
                        target_platform,
                        virality,
                    )
                )

                # ------------------------------------------------
                # Timestamp
                # ------------------------------------------------

                timestamp = (
                    generate_next_timestamp(
                        current_time,
                        interaction_type,
                        virality,
                    )
                )

                # ------------------------------------------------
                # Event ID
                # ------------------------------------------------

                depth += 1

                global_event_number += 1

                event_id = (
                    f"INT"
                    f"{global_event_number:06d}"
                )

                target_community = (
                    user_community[
                        target_user
                    ]
                )

                # ------------------------------------------------
                # Store event
                # ------------------------------------------------

                events.append({

                    "interaction_id":
                        event_id,

                    "information_id":
                        information_id,

                    "cascade_id":
                        cascade_id,

                    "parent_interaction_id":
                        parent_interaction_id,

                    "source_user":
                        current_user,

                    "target_user":
                        target_user,

                    "source_platform":
                        current_platform,

                    "target_platform":
                        target_platform,

                    "timestamp":
                        timestamp,

                    "interaction_type":
                        interaction_type,

                    "topic":
                        info["topic"],

                    "content_type":
                        info["content_type"],

                    "virality_level":
                        info["virality_level"],

                    "virality_score":
                        info["virality_score"],

                    "source_community":
                        source_community,

                    "target_community":
                        target_community,

                    "cascade_depth":
                        depth,

                    "is_cross_platform":
                        (
                            current_platform
                            != target_platform
                        ),

                    "is_cross_community":
                        (
                            source_community
                            != target_community
                        ),

                    "weight":
                        1,
                })

                # ------------------------------------------------
                # Update state
                # ------------------------------------------------

                remaining_platform_counts[
                    current_platform
                ] -= 1

                current_user = target_user

                current_platform = (
                    target_platform
                )

                current_time = timestamp

                parent_interaction_id = (
                    event_id
                )

                remaining_info_events -= 1

            # End cascade

            if remaining_info_events <= 0:

                break

        # End information item

    interactions_df = pd.DataFrame(
        events
    )

    return interactions_df


# ============================================================
# PLATFORM QUOTA
# ============================================================

def verify_platform_quota(
    interactions_df,
):

    counts = (
        interactions_df[
            "source_platform"
        ]
        .value_counts()
        .to_dict()
    )

    print(
        "\nSource-platform distribution:"
    )

    for platform in PLATFORMS:

        count = counts.get(
            platform,
            0,
        )

        print(
            f"{platform:<12}"
            f"{count:>8,}"
        )

        if count != EVENTS_PER_PLATFORM:

            raise RuntimeError(
                f"Platform quota failed for "
                f"{platform}: {count}"
            )


# ============================================================
# CASCADE VALIDATION
# ============================================================

def validate_cascades(
    interactions_df,
):

    print(
        "\nCascade integrity validation:"
    )

    event_lookup = (
        interactions_df
        .set_index(
            "interaction_id"
        )
        .to_dict("index")
    )

    parent_errors = 0
    cascade_errors = 0
    information_errors = 0
    timestamp_errors = 0
    depth_errors = 0
    root_errors = 0

    for _, row in (
        interactions_df.iterrows()
    ):

        depth = int(
            row["cascade_depth"]
        )

        parent_id = (
            row["parent_interaction_id"]
        )

        # ------------------------------------------------
        # Root
        # ------------------------------------------------

        if depth == 1:

            if pd.notna(parent_id):

                root_errors += 1

            continue

        # ------------------------------------------------
        # Non-root must have parent
        # ------------------------------------------------

        if pd.isna(parent_id):

            parent_errors += 1

            continue

        parent_id = str(
            parent_id
        )

        if parent_id not in event_lookup:

            parent_errors += 1

            continue

        parent = event_lookup[
            parent_id
        ]

        # ------------------------------------------------
        # Same cascade
        # ------------------------------------------------

        if (
            parent["cascade_id"]
            != row["cascade_id"]
        ):

            cascade_errors += 1

        # ------------------------------------------------
        # Same information
        # ------------------------------------------------

        if (
            parent["information_id"]
            != row["information_id"]
        ):

            information_errors += 1

        # ------------------------------------------------
        # Timestamp
        # ------------------------------------------------

        parent_time = pd.Timestamp(
            parent["timestamp"]
        )

        child_time = pd.Timestamp(
            row["timestamp"]
        )

        if parent_time >= child_time:

            timestamp_errors += 1

        # ------------------------------------------------
        # Depth
        # ------------------------------------------------

        expected_depth = (
            int(
                parent[
                    "cascade_depth"
                ]
            )
            + 1
        )

        if depth != expected_depth:

            depth_errors += 1

    print(
        f"Parent errors:       "
        f"{parent_errors:,}"
    )

    print(
        f"Cascade errors:      "
        f"{cascade_errors:,}"
    )

    print(
        f"Information errors:  "
        f"{information_errors:,}"
    )

    print(
        f"Timestamp errors:    "
        f"{timestamp_errors:,}"
    )

    print(
        f"Depth errors:        "
        f"{depth_errors:,}"
    )

    print(
        f"Root errors:         "
        f"{root_errors:,}"
    )

    total_errors = (
        parent_errors
        + cascade_errors
        + information_errors
        + timestamp_errors
        + depth_errors
        + root_errors
    )

    if total_errors != 0:

        raise RuntimeError(
            "Cascade integrity validation failed."
        )

    print(
        "Cascade integrity: PASS"
    )


# ============================================================
# FULL VALIDATION
# ============================================================

def validate(
    users_df,
    information_df,
    interactions_df,
):

    print(
        "\n"
        + "=" * 70
    )

    print(
        "FINAL DATASET VALIDATION"
    )

    print(
        "=" * 70
    )

    # --------------------------------------------------------
    # Sizes
    # --------------------------------------------------------

    assert (
        len(users_df)
        == NUM_USERS
    )

    assert (
        len(information_df)
        == NUM_INFORMATION_ITEMS
    )

    assert (
        len(interactions_df)
        == TOTAL_EVENTS
    )

    # --------------------------------------------------------
    # IDs
    # --------------------------------------------------------

    assert (
        interactions_df[
            "interaction_id"
        ].is_unique
    )

    # --------------------------------------------------------
    # No self-interactions
    # --------------------------------------------------------

    assert (
        interactions_df[
            "source_user"
        ]
        !=
        interactions_df[
            "target_user"
        ]
    ).all()

    # --------------------------------------------------------
    # User references
    # --------------------------------------------------------

    assert (
        interactions_df[
            "source_user"
        ].isin(
            users_df[
                "user_id"
            ]
        )
    ).all()

    assert (
        interactions_df[
            "target_user"
        ].isin(
            users_df[
                "user_id"
            ]
        )
    ).all()

    # --------------------------------------------------------
    # Information references
    # --------------------------------------------------------

    assert (
        interactions_df[
            "information_id"
        ].isin(
            information_df[
                "information_id"
            ]
        )
    ).all()

    # --------------------------------------------------------
    # Timestamp range
    # --------------------------------------------------------

    assert (
        interactions_df[
            "timestamp"
        ]
        >= START_DATE
    ).all()

    assert (
        interactions_df[
            "timestamp"
        ]
        <= END_DATE
    ).all()

    # --------------------------------------------------------
    # Platform quota
    # --------------------------------------------------------

    verify_platform_quota(
        interactions_df
    )

    # --------------------------------------------------------
    # Basic statistics
    # --------------------------------------------------------

    print(
        f"\nTotal interactions: "
        f"{len(interactions_df):,}"
    )

    print(
        "\nInteraction types:"
    )

    print(
        interactions_df[
            "interaction_type"
        ].value_counts()
    )

    print(
        "\nCross-platform events:"
    )

    print(
        interactions_df[
            "is_cross_platform"
        ].value_counts()
    )

    print(
        "\nCross-community events:"
    )

    print(
        interactions_df[
            "is_cross_community"
        ].value_counts()
    )

    print(
        "\nCascade depth:"
    )

    print(
        interactions_df[
            "cascade_depth"
        ].describe()
    )

    print(
        "\nCascade count:"
    )

    print(
        interactions_df[
            "cascade_id"
        ].nunique()
    )

    print(
        "\nInformation items with events:"
    )

    print(
        interactions_df[
            "information_id"
        ].nunique()
    )

    # --------------------------------------------------------
    # Duplicate IDs
    # --------------------------------------------------------

    duplicate_ids = (
        interactions_df[
            "interaction_id"
        ]
        .duplicated()
        .sum()
    )

    print(
        "\nDuplicate interaction IDs: "
        f"{duplicate_ids:,}"
    )

    if duplicate_ids != 0:

        raise RuntimeError(
            "Duplicate interaction IDs detected."
        )

    # --------------------------------------------------------
    # Duplicate event records
    # --------------------------------------------------------

    duplicate_columns = [
        "information_id",
        "cascade_id",
        "parent_interaction_id",
        "source_user",
        "target_user",
        "source_platform",
        "target_platform",
        "timestamp",
        "interaction_type",
    ]

    duplicate_events = (
        interactions_df[
            duplicate_columns
        ]
        .duplicated()
        .sum()
    )

    print(
        "\nDuplicate event records: "
        f"{duplicate_events:,}"
    )

    if duplicate_events != 0:

        raise RuntimeError(
            "Duplicate diffusion events detected."
        )

    # --------------------------------------------------------
    # Cross-platform consistency
    # --------------------------------------------------------

    expected_cross_platform = (
        interactions_df[
            "source_platform"
        ]
        !=
        interactions_df[
            "target_platform"
        ]
    )

    actual_cross_platform = (
        interactions_df[
            "is_cross_platform"
        ].astype(bool)
    )

    errors = (
        expected_cross_platform
        != actual_cross_platform
    ).sum()

    print(
        "\nCross-platform consistency errors: "
        f"{errors:,}"
    )

    if errors != 0:

        raise RuntimeError(
            "Cross-platform consistency failed."
        )

    # --------------------------------------------------------
    # Cross-community consistency
    # --------------------------------------------------------

    expected_cross_community = (
        interactions_df[
            "source_community"
        ]
        !=
        interactions_df[
            "target_community"
        ]
    )

    actual_cross_community = (
        interactions_df[
            "is_cross_community"
        ].astype(bool)
    )

    errors = (
        expected_cross_community
        != actual_cross_community
    ).sum()

    print(
        "Cross-community consistency errors: "
        f"{errors:,}"
    )

    if errors != 0:

        raise RuntimeError(
            "Cross-community consistency failed."
        )

    # --------------------------------------------------------
    # Cross-platform interaction type
    # --------------------------------------------------------

    cross_platform_rows = (
        interactions_df[
            "source_platform"
        ]
        !=
        interactions_df[
            "target_platform"
        ]
    )

    type_errors = (
        interactions_df.loc[
            cross_platform_rows,
            "interaction_type",
        ]
        !=
        "CrossPlatformShare"
    ).sum()

    print(
        "Cross-platform interaction-type errors: "
        f"{type_errors:,}"
    )

    if type_errors != 0:

        raise RuntimeError(
            "Cross-platform interaction type validation failed."
        )

    # --------------------------------------------------------
    # Strong cascade validation
    # --------------------------------------------------------

    validate_cascades(
        interactions_df
    )

    # --------------------------------------------------------
    # FINAL
    # --------------------------------------------------------

    print(
        "\n"
        + "=" * 70
    )

    print(
        "ALL VALIDATION CHECKS PASSED"
    )

    print(
        "=" * 70
    )


# ============================================================
# SAVE
# ============================================================

def save_files(
    users_df,
    information_df,
    interactions_df,
):

    users_path = (
        DATA_DIR / "users.csv"
    )

    information_path = (
        DATA_DIR / "information_items.csv"
    )

    interactions_path = (
        DATA_DIR / "interactions.csv"
    )

    users_df.to_csv(
        users_path,
        index=False,
    )

    information_df.to_csv(
        information_path,
        index=False,
    )

    interactions_df.to_csv(
        interactions_path,
        index=False,
    )

    print(
        "\nFiles saved:"
    )

    print(users_path)
    print(information_path)
    print(interactions_path)


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "=" * 70
    )

    print(
        "SYNTHETIC INFORMATION DIFFUSION DATASET"
    )

    print(
        "DIRECT DIFFUSION GENERATION"
    )

    print(
        "=" * 70
    )

    print(
        f"\nTarget events: "
        f"{TOTAL_EVENTS:,}"
    )

    print(
        f"Events per platform: "
        f"{EVENTS_PER_PLATFORM:,}"
    )

    print(
        f"Users: "
        f"{NUM_USERS:,}"
    )

    print(
        f"Information items: "
        f"{NUM_INFORMATION_ITEMS:,}"
    )

    print(
        f"Communities: "
        f"{NUM_COMMUNITIES}"
    )

    users_df = (
        generate_users()
    )

    information_df = (
        generate_information_items(
            users_df
        )
    )

    interactions_df = (
        generate_events(
            users_df,
            information_df,
        )
    )

    print(
        f"\nGenerated events: "
        f"{len(interactions_df):,}"
    )

    # --------------------------------------------------------
    # Exact event count
    # --------------------------------------------------------

    if (
        len(interactions_df)
        != TOTAL_EVENTS
    ):

        raise RuntimeError(
            "Generator failed to create exactly "
            f"{TOTAL_EVENTS:,} events. "
            f"Generated: "
            f"{len(interactions_df):,}"
        )

    # --------------------------------------------------------
    # Convert timestamp
    # --------------------------------------------------------

    interactions_df[
        "timestamp"
    ] = pd.to_datetime(
        interactions_df[
            "timestamp"
        ]
    )

    # --------------------------------------------------------
    # Sort chronologically
    #
    # IMPORTANT:
    # Never renumber interaction IDs here.
    # parent_interaction_id depends on them.
    # --------------------------------------------------------

    interactions_df = (
        interactions_df
        .sort_values(
            "timestamp"
        )
        .reset_index(
            drop=True
        )
    )

    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    validate(
        users_df,
        information_df,
        interactions_df,
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    save_files(
        users_df,
        information_df,
        interactions_df,
    )

    print(
        "\n"
        + "=" * 70
    )

    print(
        "DATASET GENERATION COMPLETE"
    )

    print(
        "=" * 70
    )


if __name__ == "__main__":

    main()