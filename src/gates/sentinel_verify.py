"""
Sentinel verification gates: Check epistemic vector thresholds before action.

Validates:
- Know/uncertainty balance: sufficient grounding
- Context availability: domain knowledge vs. task scope
- Engagement and clarity: work readiness
- Action-appropriate thresholds: different actions need different vectors
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum
import json


class ActionType(str, Enum):
    """Types of actions requiring different epistemic thresholds."""
    INVESTIGATE = "investigate"
    IMPLEMENT = "implement"
    DEPLOY = "deploy"
    ESCALATE = "escalate"
    PUBLISH = "publish"


class VectorLevel(str, Enum):
    """Verification outcome."""
    PASS = "pass"
    FAIL = "fail"
    MARGINAL = "marginal"  # Passes but close to threshold


@dataclass
class EpistemicVectors:
    """Current epistemic state."""
    know: float  # 0.0-1.0: how much do we understand?
    uncertainty: float  # 0.0-1.0: how uncertain are we?
    context: float  # 0.0-1.0: relevant domain knowledge available?
    engagement: float  # 0.0-1.0: how engaged/motivated for this work?
    clarity: float  # 0.0-1.0: how clear is the goal/direction?
    coherence: float  # 0.0-1.0: how consistent are findings?


@dataclass
class VectorThresholds:
    """Minimum vector values required for an action."""
    action: ActionType
    min_know: float
    max_uncertainty: float
    min_context: float
    min_engagement: float
    min_clarity: float
    min_coherence: float


@dataclass
class VectorCheckResult:
    """Result of Sentinel vector verification."""
    level: VectorLevel
    vectors: EpistemicVectors
    thresholds: VectorThresholds
    passed_checks: List[str]
    marginal_checks: List[str]
    failed_checks: List[str]
    recommendations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "level": self.level.value,
            "vectors": {
                "know": self.vectors.know,
                "uncertainty": self.vectors.uncertainty,
                "context": self.vectors.context,
                "engagement": self.vectors.engagement,
                "clarity": self.vectors.clarity,
                "coherence": self.vectors.coherence,
            },
            "thresholds": {
                "action": self.thresholds.action.value,
                "min_know": self.thresholds.min_know,
                "max_uncertainty": self.thresholds.max_uncertainty,
                "min_context": self.thresholds.min_context,
                "min_engagement": self.thresholds.min_engagement,
                "min_clarity": self.thresholds.min_clarity,
                "min_coherence": self.thresholds.min_coherence,
            },
            "passed_checks": self.passed_checks,
            "marginal_checks": self.marginal_checks,
            "failed_checks": self.failed_checks,
            "recommendations": self.recommendations,
        }


class SentinelGate:
    """
    Verification gate that enforces Sentinel vector thresholds.

    Different actions require different epistemic confidence levels:
    - INVESTIGATE: lower thresholds (learning phase)
    - IMPLEMENT: higher know + context + clarity
    - DEPLOY: highest thresholds (production action)
    - ESCALATE: high urgency tolerance (uncertainty OK if engagement high)
    - PUBLISH: high coherence + know (output quality matters)
    """

    # Define action-specific thresholds
    THRESHOLDS: Dict[ActionType, VectorThresholds] = {
        ActionType.INVESTIGATE: VectorThresholds(
            action=ActionType.INVESTIGATE,
            min_know=0.2,
            max_uncertainty=0.8,
            min_context=0.2,
            min_engagement=0.3,
            min_clarity=0.2,
            min_coherence=0.1,
        ),
        ActionType.IMPLEMENT: VectorThresholds(
            action=ActionType.IMPLEMENT,
            min_know=0.75,
            max_uncertainty=0.25,
            min_context=0.80,
            min_engagement=0.85,
            min_clarity=0.80,
            min_coherence=0.70,
        ),
        ActionType.DEPLOY: VectorThresholds(
            action=ActionType.DEPLOY,
            min_know=0.90,
            max_uncertainty=0.10,
            min_context=0.90,
            min_engagement=0.95,
            min_clarity=0.90,
            min_coherence=0.85,
        ),
        ActionType.ESCALATE: VectorThresholds(
            action=ActionType.ESCALATE,
            min_know=0.3,
            max_uncertainty=0.7,  # Escalation OK when uncertain but urgent
            min_context=0.3,
            min_engagement=0.90,  # High urgency must be present
            min_clarity=0.3,
            min_coherence=0.2,
        ),
        ActionType.PUBLISH: VectorThresholds(
            action=ActionType.PUBLISH,
            min_know=0.85,
            max_uncertainty=0.15,
            min_context=0.85,
            min_engagement=0.90,
            min_clarity=0.85,
            min_coherence=0.85,  # High coherence for publishable work
        ),
    }

    def verify(
        self,
        vectors: EpistemicVectors,
        action: ActionType
    ) -> VectorCheckResult:
        """
        Verify epistemic state is sufficient for the proposed action.

        Args:
            vectors: Current epistemic state
            action: Action type requiring verification

        Returns:
            VectorCheckResult with pass/fail + recommendations
        """
        thresholds = self.THRESHOLDS[action]
        passed_checks: List[str] = []
        marginal_checks: List[str] = []
        failed_checks: List[str] = []
        recommendations: List[str] = []

        # Check each vector
        checks = [
            ("know", vectors.know, thresholds.min_know, ">=", False),
            ("uncertainty", vectors.uncertainty, thresholds.max_uncertainty, "<=", False),
            ("context", vectors.context, thresholds.min_context, ">=", False),
            ("engagement", vectors.engagement, thresholds.min_engagement, ">=", False),
            ("clarity", vectors.clarity, thresholds.min_clarity, ">=", False),
            ("coherence", vectors.coherence, thresholds.min_coherence, ">=", False),
        ]

        for vector_name, value, threshold, direction, is_max in checks:
            if direction == ">=":
                passed = value >= threshold
                marginal = (value >= threshold * 0.9) and (value < threshold)
            else:  # <=
                passed = value <= threshold
                marginal = (value <= threshold * 1.1) and (value > threshold)

            if passed:
                passed_checks.append(
                    f"{vector_name}: {value:.2f} {'≥' if direction == '>=' else '≤'} {threshold:.2f}"
                )
            elif marginal:
                marginal_checks.append(
                    f"{vector_name}: {value:.2f} {'≥' if direction == '>=' else '≤'} {threshold:.2f} "
                    f"(within 10% margin)"
                )
            else:
                failed_checks.append(
                    f"{vector_name}: {value:.2f} {'≥' if direction == '>=' else '≤'} {threshold:.2f} FAILED"
                )

        # Determine level
        if failed_checks:
            level = VectorLevel.FAIL
            recommendations.append(
                f"Cannot proceed with {action.value}: vector thresholds not met. "
                "Invest in noetic work to improve grounding."
            )
        elif marginal_checks:
            level = VectorLevel.MARGINAL
            recommendations.append(
                f"Marginal readiness for {action.value}. Consider: "
                f"(1) completing noetic work on {', '.join(m.split(':')[0] for m in marginal_checks)}, "
                f"(2) reducing scope, (3) proceeding with higher caution."
            )
        else:
            level = VectorLevel.PASS

        return VectorCheckResult(
            level=level,
            vectors=vectors,
            thresholds=thresholds,
            passed_checks=passed_checks,
            marginal_checks=marginal_checks,
            failed_checks=failed_checks,
            recommendations=recommendations,
        )

    def recommend_action(self, vectors: EpistemicVectors) -> ActionType:
        """
        Recommend the highest-trust action the current vectors support.

        Returns:
            The ActionType with the lowest bar that all vectors meet.
        """
        for action in [
            ActionType.DEPLOY,
            ActionType.PUBLISH,
            ActionType.IMPLEMENT,
            ActionType.ESCALATE,
            ActionType.INVESTIGATE,
        ]:
            result = self.verify(vectors, action)
            if result.level in [VectorLevel.PASS, VectorLevel.MARGINAL]:
                return action

        # Fallback: always safe to investigate
        return ActionType.INVESTIGATE
