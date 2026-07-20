#!/usr/bin/env python3
"""
Teacher/Tradition Matcher v1.0

Given: consciousness level + challenge + learning style
Returns: Ranked teacher/tradition matches with reasoning

Architecture:
- ScoreMatrix: Define how each tradition addresses each dimension
- TeacherMatcher: Load profiles, score, rank, return results
"""

import json
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
from enum import Enum


class LearningStyle(Enum):
    """How people learn best"""
    INTELLECTUAL = "intellectual"  # Study, analysis, philosophy
    DEVOTIONAL = "devotional"      # Relationship, surrender, love
    PRACTICAL = "practical"         # Action, discipline, doing
    MYSTICAL = "mystical"          # Experience, meditation, transcendence


class CommunityType(Enum):
    """How communities operate"""
    ONLINE = "online"
    IN_PERSON = "in_person"
    HYBRID = "hybrid"


@dataclass
class TeacherProfile:
    """A specific teacher or guide"""
    name: str
    tradition: str
    consciousness_level_range: Tuple[int, int]
    learning_styles: List[LearningStyle]
    location: str
    community_type: CommunityType
    challenge_focus: List[str]  # e.g., ["addiction", "grief", "meaning"]
    daily_practice: str
    contact_info: str


@dataclass
class TraditionProfile:
    """A wisdom tradition with its characteristics"""
    name: str
    system_id: str
    consciousness_range: Tuple[int, int]
    primary_learning_style: LearningStyle
    challenge_expertise: List[str]
    core_practice: str
    teachers: List[TeacherProfile]
    community_examples: List[str]


@dataclass
class MatchResult:
    """A tradition/teacher match with score and reasoning"""
    rank: int
    tradition_name: str
    match_score: float  # 0-100
    score_breakdown: Dict[str, float]

    matched_teacher: Optional[TeacherProfile]
    daily_practice: str
    expected_timeline: str
    success_metrics: List[str]
    reasoning: str

    def formatted(self) -> str:
        """Human-readable match explanation"""
        output = []
        output.append(f"\n{'='*70}")
        output.append(f"MATCH #{self.rank}: {self.tradition_name}")
        output.append(f"Score: {self.match_score:.1f}/100")
        output.append(f"{'='*70}\n")

        output.append("SCORE BREAKDOWN:")
        for dimension, score in self.score_breakdown.items():
            output.append(f"  • {dimension:<25} {score:5.1f}/100")
        output.append("")

        if self.matched_teacher:
            output.append("RECOMMENDED TEACHER:")
            output.append(f"  Name: {self.matched_teacher.name}")
            output.append(f"  Specializes in: {', '.join(self.matched_teacher.challenge_focus)}")
            output.append(f"  Location: {self.matched_teacher.location}")
            output.append(f"  Contact: {self.matched_teacher.contact_info}")
            output.append("")

        output.append("YOUR DAILY PRACTICE:")
        output.append(f"  {self.daily_practice}")
        output.append("")

        output.append("EXPECTED TIMELINE:")
        output.append(f"  {self.expected_timeline}")
        output.append("")

        output.append("SUCCESS METRICS:")
        for metric in self.success_metrics:
            output.append(f"  ✓ {metric}")
        output.append("")

        output.append("WHY THIS MATCH:")
        output.append(f"  {self.reasoning}")
        output.append("")

        return "\n".join(output)


class TraditionScoreMatrix:
    """Scores for how each tradition addresses different dimensions"""

    # Level calibration: tradition score at different consciousness levels
    LEVEL_SCORES = {
        "aa_12_steps": {
            "low": (0, 50, 0.95),      # (min, max, strength) - AA is BEST for powerlessness
            "lower": (50, 200, 0.90),   # Still excellent for fear/desire
            "middle": (200, 350, 0.70), # Good for courage phase
            "high": (350, 600, 0.85),   # Strong for service/love phases
            "transcendent": (600, 1000, 0.60)  # Less specialized here
        },
        "buddhist": {
            "low": (0, 50, 0.85),
            "lower": (50, 200, 0.90),
            "middle": (200, 350, 0.85),
            "high": (350, 600, 0.95),   # Buddhist excels at compassion/enlightenment
            "transcendent": (600, 1000, 0.95)
        },
        "jesus_teachings": {
            "low": (0, 50, 0.70),
            "lower": (50, 200, 0.80),
            "middle": (200, 350, 0.95),  # Jesus teachings brilliant for ethics/love
            "high": (350, 600, 0.90),
            "transcendent": (600, 1000, 0.75)
        },
        "freemasonry": {
            "low": (0, 50, 0.60),
            "lower": (50, 200, 0.75),
            "middle": (200, 350, 0.95),  # Freemasonry is initiation path
            "high": (350, 600, 0.80),
            "transcendent": (600, 1000, 0.65)
        },
        "hawkins": {
            "low": (0, 50, 0.80),
            "lower": (50, 200, 0.85),
            "middle": (200, 350, 0.90),
            "high": (350, 600, 0.85),
            "transcendent": (600, 1000, 0.90)   # Hawkins covers full spectrum
        },
        "stoic": {
            "low": (0, 50, 0.50),
            "lower": (50, 200, 0.75),
            "middle": (200, 350, 0.95),  # Stoic excels at practical wisdom/courage
            "high": (350, 600, 0.70),
            "transcendent": (600, 1000, 0.60)
        }
    }

    # Challenge expertise: how well each tradition addresses common obstacles
    CHALLENGE_SCORES = {
        "addiction": {
            "aa_12_steps": 0.99,      # AA is THE gold standard
            "hawkins": 0.75,          # Hawkins maps addiction consciousness
            "buddhist": 0.70,         # Addresses craving/attachment
            "jesus_teachings": 0.65,
            "freemasonry": 0.50,
            "stoic": 0.60
        },
        "grief": {
            "buddhist": 0.90,         # Impermanence teaching
            "jesus_teachings": 0.85,  # Resurrection/acceptance
            "hawkins": 0.75,
            "aa_12_steps": 0.65,
            "stoic": 0.80,            # Stoic acceptance
            "freemasonry": 0.50
        },
        "meaning": {
            "jesus_teachings": 0.90,  # Deep existential teaching
            "freemasonry": 0.85,      # Initiation as meaning-making
            "buddhist": 0.90,         # Four Noble Truths
            "hawkins": 0.80,
            "aa_12_steps": 0.70,
            "stoic": 0.75
        },
        "relationship": {
            "jesus_teachings": 0.95,  # Love, forgiveness
            "aa_12_steps": 0.80,      # Making amends
            "buddhist": 0.85,         # Compassion, right speech
            "stoic": 0.70,
            "hawkins": 0.65,
            "freemasonry": 0.60
        },
        "self_mastery": {
            "freemasonry": 0.95,      # Core practice
            "stoic": 0.90,            # Virtue/discipline
            "buddhist": 0.85,         # Eightfold Path
            "hawkins": 0.75,
            "aa_12_steps": 0.70,
            "jesus_teachings": 0.65
        },
        "fear": {
            "aa_12_steps": 0.85,      # Steps 2-3 address fear
            "hawkins": 0.90,          # Maps fear exactly
            "jesus_teachings": 0.80,  # "Fear not" teachings
            "buddhist": 0.75,
            "stoic": 0.85,
            "freemasonry": 0.70
        }
    }

    # Learning style fit
    STYLE_SCORES = {
        "intellectual": {
            "hawkins": 0.95,          # Hawk's system is analytical
            "stoic": 0.90,            # Philosophy/logic
            "buddhist": 0.85,         # Philosophical depth
            "jesus_teachings": 0.70,  # Parables need interpretation
            "aa_12_steps": 0.65,
            "freemasonry": 0.60
        },
        "devotional": {
            "jesus_teachings": 0.95,  # Love, surrender, faith
            "aa_12_steps": 0.90,      # "Turn will over to God"
            "buddhist": 0.80,         # Devotional Buddhism exists
            "stoic": 0.50,
            "hawkins": 0.40,
            "freemasonry": 0.55
        },
        "practical": {
            "aa_12_steps": 0.95,      # 12 steps are concrete actions
            "stoic": 0.90,            # Virtue in action
            "freemasonry": 0.85,      # Ritual and practice
            "buddhist": 0.80,         # Eightfold Path is practice
            "hawkins": 0.60,
            "jesus_teachings": 0.70   # Sermon on Mount
        },
        "mystical": {
            "buddhist": 0.95,         # Meditation, direct experience
            "freemasonry": 0.90,      # Mystical degrees
            "jesus_teachings": 0.85,  # Mystical union teachings
            "hawkins": 0.75,          # Enlightenment states
            "aa_12_steps": 0.70,      # Spiritual awakening
            "stoic": 0.40
        }
    }

    @staticmethod
    def get_level_score(tradition: str, consciousness_level: int) -> float:
        """Get how well tradition addresses this consciousness level"""
        if tradition not in TraditionScoreMatrix.LEVEL_SCORES:
            return 0.5

        scores = TraditionScoreMatrix.LEVEL_SCORES[tradition]

        # Determine which band the level falls into
        if consciousness_level < 50:
            band = scores["low"]
        elif consciousness_level < 200:
            band = scores["lower"]
        elif consciousness_level < 350:
            band = scores["middle"]
        elif consciousness_level < 600:
            band = scores["high"]
        else:
            band = scores["transcendent"]

        # band = (min, max, strength)
        # Return strength * 100 as percentage
        return band[2] * 100

    @staticmethod
    def get_challenge_score(tradition: str, challenge: str) -> float:
        """Get how well tradition addresses this challenge"""
        challenge_lower = challenge.lower().replace(" ", "_")

        if challenge_lower not in TraditionScoreMatrix.CHALLENGE_SCORES:
            return 50.0  # Default middle score for unknown challenges

        challenge_scores = TraditionScoreMatrix.CHALLENGE_SCORES[challenge_lower]

        if tradition not in challenge_scores:
            return 50.0

        return challenge_scores[tradition] * 100

    @staticmethod
    def get_style_score(tradition: str, style: LearningStyle) -> float:
        """Get how well tradition matches this learning style"""
        if style.value not in TraditionScoreMatrix.STYLE_SCORES:
            return 50.0

        style_scores = TraditionScoreMatrix.STYLE_SCORES[style.value]

        if tradition not in style_scores:
            return 50.0

        return style_scores[tradition] * 100


class TeacherMatcher:
    """Match people to traditions and teachers"""

    # Scoring weights
    WEIGHTS = {
        "consciousness_level": 0.40,  # Biggest factor: is tradition right for this level?
        "challenge_fit": 0.30,        # How well does tradition address their obstacle?
        "learning_style": 0.20,       # Does their learning style match?
        "practical": 0.10             # Can they actually access it?
    }

    TRADITIONS = ["aa_12_steps", "buddhist", "jesus_teachings", "freemasonry", "hawkins", "stoic"]

    def __init__(self, tradition_profiles_file: Optional[str] = None):
        """Initialize matcher with tradition profiles"""
        self.matrix = TraditionScoreMatrix()
        self.tradition_profiles = self._load_or_create_profiles(tradition_profiles_file)

    def _load_or_create_profiles(self, filepath: Optional[str]) -> Dict:
        """Load tradition profiles or create seed profiles"""
        if filepath:
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except FileNotFoundError:
                pass

        # Seed profiles (to be expanded with real teachers)
        return {
            "aa_12_steps": {
                "name": "Alcoholics Anonymous / 12-Step Programs",
                "description": "Recovery through admission, faith, and service",
                "strength_range": [0, 600],
                "primary_style": "practical",
                "teachers": [
                    {"name": "Local AA Group", "location": "Worldwide", "contact": "aa.org"}
                ]
            },
            "buddhist": {
                "name": "Buddhism (Multiple Traditions)",
                "description": "Path through mindfulness, compassion, and enlightenment",
                "strength_range": [50, 1000],
                "primary_style": "mystical",
                "teachers": [
                    {"name": "Local Sangha", "location": "Worldwide", "contact": "buddhanet.net"}
                ]
            },
            "jesus_teachings": {
                "name": "Christian / Jesus Teachings",
                "description": "Love, forgiveness, resurrection consciousness",
                "strength_range": [200, 700],
                "primary_style": "devotional",
                "teachers": [
                    {"name": "Local Church/Spiritual Director", "location": "Worldwide", "contact": "various"}
                ]
            },
            "freemasonry": {
                "name": "Freemasonry (Degrees)",
                "description": "Initiation through ritual and mastery",
                "strength_range": [200, 500],
                "primary_style": "practical",
                "teachers": [
                    {"name": "Local Lodge", "location": "Worldwide", "contact": "freemasons.org"}
                ]
            },
            "hawkins": {
                "name": "Hawkins Consciousness Map",
                "description": "Scientific calibration of consciousness levels",
                "strength_range": [0, 1000],
                "primary_style": "intellectual",
                "teachers": [
                    {"name": "Hawkins' Writings", "location": "Self-study", "contact": "davidhawkins.com"}
                ]
            },
            "stoic": {
                "name": "Stoicism (Modern Practice)",
                "description": "Virtue, discipline, acceptance through philosophy",
                "strength_range": [200, 500],
                "primary_style": "intellectual",
                "teachers": [
                    {"name": "Philosophy Groups", "location": "Worldwide", "contact": "various"}
                ]
            }
        }

    def match(
        self,
        consciousness_level: int,
        challenge: str,
        learning_style: LearningStyle
    ) -> List[MatchResult]:
        """
        Match person to traditions and teachers

        Args:
            consciousness_level: Hawkins 0-1000
            challenge: e.g., "addiction", "grief", "meaning"
            learning_style: LearningStyle enum

        Returns:
            Ranked list of MatchResult
        """
        results = []

        for tradition in self.TRADITIONS:
            # Calculate scores for each dimension
            level_score = self.matrix.get_level_score(tradition, consciousness_level)
            challenge_score = self.matrix.get_challenge_score(tradition, challenge)
            style_score = self.matrix.get_style_score(tradition, learning_style)
            practical_score = 75.0  # Assume all are reasonably accessible for now

            # Aggregate score
            total_score = (
                level_score * self.WEIGHTS["consciousness_level"] +
                challenge_score * self.WEIGHTS["challenge_fit"] +
                style_score * self.WEIGHTS["learning_style"] +
                practical_score * self.WEIGHTS["practical"]
            )

            result = MatchResult(
                rank=0,  # Will be set after sorting
                tradition_name=tradition.upper(),
                match_score=total_score,
                score_breakdown={
                    "Consciousness Level Fit": level_score,
                    "Challenge Expertise": challenge_score,
                    "Learning Style Match": style_score,
                    "Practical Access": practical_score
                },
                matched_teacher=None,  # Will be set from profiles
                daily_practice=self._get_practice_blueprint(tradition),
                expected_timeline=self._get_timeline(consciousness_level, tradition),
                success_metrics=self._get_metrics(challenge),
                reasoning=self._generate_reasoning(tradition, consciousness_level, challenge, learning_style)
            )

            results.append(result)

        # Sort by score (descending) and assign ranks
        results.sort(key=lambda r: r.match_score, reverse=True)
        for i, result in enumerate(results, 1):
            result.rank = i

        return results

    def _get_practice_blueprint(self, tradition: str) -> str:
        """Get daily practice for this tradition"""
        practices = {
            "aa_12_steps": "Attend weekly meeting (1hr), work one step per week, call sponsor daily (5min), 10min morning reflection",
            "buddhist": "Daily meditation (20-60min), study sutras (15min), practice mindful living throughout day",
            "jesus_teachings": "Prayer (morning/evening, 15min each), scripture study (20min), service to others (2hrs/week)",
            "freemasonry": "Monthly lodge meeting (2-3hrs), degree study as needed, fellowship with brothers",
            "hawkins": "Self-study of Hawkins maps (1hr/week), calibration exercises (20min), consciousness journaling",
            "stoic": "Marcus Aurelius reading (20min), virtue practice check-in (10min), philosophical contemplation"
        }
        return practices.get(tradition, "Consult with tradition teachers for personalized practice")

    def _get_timeline(self, level: int, tradition: str) -> str:
        """Get expected transformation timeline"""
        if level < 100:
            return "3-6 months for initial stabilization; 1-2 years for deep transformation"
        elif level < 300:
            return "6-12 months to see significant progress; 2-3 years for integration"
        else:
            return "Refinement phase: ongoing deepening; 6-12 month cycles of insight and integration"

    def _get_metrics(self, challenge: str) -> List[str]:
        """Success metrics for this challenge"""
        metrics = {
            "addiction": [
                "Days/weeks/months of sobriety",
                "Reduced cravings and obsession",
                "Improved relationships",
                "Emotional stability",
                "Sense of purpose emerging"
            ],
            "grief": [
                "Integration of loss",
                "Periods of peace increasing",
                "Ability to honor memory without pain",
                "Energy returning for life",
                "Meaning-making from loss"
            ],
            "meaning": [
                "Clarity on life purpose",
                "Actions aligned with values",
                "Sense of contribution",
                "Reduced existential anxiety",
                "Joy in daily practice"
            ]
        }
        return metrics.get(challenge.lower(), [
            "Increasing clarity",
            "Greater peace",
            "Aligned action",
            "Community connection",
            "Personal growth"
        ])

    def _generate_reasoning(self, tradition: str, level: int, challenge: str, style: LearningStyle) -> str:
        """Explain why this is a good match"""
        reasons = {
            "aa_12_steps": f"AA specializes in powerlessness/transformation at your level. Unmatched expertise in addiction recovery. Practical, community-based approach.",
            "buddhist": f"Buddhism offers comprehensive path from suffering to enlightenment, addressing your challenge through mindfulness and compassion.",
            "jesus_teachings": f"Jesus teachings emphasize love, forgiveness, and transformation. Strong resonance with your learning style and challenge.",
            "freemasonry": f"Initiation-based mastery through ritual and brotherhood. Excellent for self-directed growth at your consciousness level.",
            "hawkins": f"Hawkins map provides scientific understanding of your consciousness level. Intellectual framework for self-assessment.",
            "stoic": f"Stoicism offers practical philosophy for developing virtue and mastering challenge through discipline and wisdom."
        }
        return reasons.get(tradition, f"{tradition} offers a strong match for your current level and challenge.")


# ============================================================================
# TEST CASES
# ============================================================================

def run_test_matches():
    """Test the matcher"""
    print("\n" + "=" * 80)
    print("TEACHER/TRADITION MATCHER - TEST SUITE")
    print("=" * 80 + "\n")

    matcher = TeacherMatcher()

    # Test case 1: Addiction at level 50
    print("TEST 1: Addiction Recovery (Level 50)")
    print("─" * 80)
    matches = matcher.match(
        consciousness_level=50,
        challenge="addiction",
        learning_style=LearningStyle.PRACTICAL
    )

    for match in matches[:3]:  # Show top 3
        print(match.formatted())

    # Test case 2: Meaning-seeking at level 350
    print("\nTEST 2: Meaning-Seeking (Level 350)")
    print("─" * 80)
    matches = matcher.match(
        consciousness_level=350,
        challenge="meaning",
        learning_style=LearningStyle.INTELLECTUAL
    )

    for match in matches[:3]:
        print(match.formatted())


if __name__ == "__main__":
    run_test_matches()
