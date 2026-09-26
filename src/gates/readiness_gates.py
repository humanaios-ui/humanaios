"""
Readiness gates: Verify noetic work is complete before praxic execution.

Checks:
- Evidence collection: minimum reads/greps completed
- Ground truth availability: external data sources verified
- Assumption documentation: unverified beliefs recorded
- Uncertainty threshold: acceptable level of remaining unknowns
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum
import json


class ReadinessLevel(str, Enum):
    """Readiness assessment outcome."""
    READY = "ready"
    NOT_READY = "not_ready"
    PARTIALLY_READY = "partially_ready"


@dataclass
class EvidenceRequirement:
    """Specification for evidence that must be gathered."""
    name: str
    kind: str  # "read", "grep", "glob", "query", "external"
    minimum_count: int = 1
    confidence_threshold: float = 0.7
    optional: bool = False


@dataclass
class ReadinessCheckResult:
    """Result of a readiness gate evaluation."""
    level: ReadinessLevel
    evidence_gathered: int
    evidence_required: int
    assumptions_undocumented: int
    uncertainty_level: float  # 0.0-1.0, higher = more uncertain
    blockers: List[str]
    passed_checks: List[str]
    recommendations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "level": self.level.value,
            "evidence_gathered": self.evidence_gathered,
            "evidence_required": self.evidence_required,
            "assumptions_undocumented": self.assumptions_undocumented,
            "uncertainty_level": self.uncertainty_level,
            "blockers": self.blockers,
            "passed_checks": self.passed_checks,
            "recommendations": self.recommendations,
        }


class ReadinessGate:
    """
    Gate that enforces noetic-phase completion before moving to praxic.

    Transaction discipline requires clear evidence gathering. This gate
    certifies that sufficient noetic work was done to ground the next phase.
    """

    def __init__(self):
        self.evidence_log: List[Dict[str, Any]] = []
        self.assumptions: List[str] = []
        self.unknowns: List[str] = []

    def log_evidence(
        self,
        kind: str,
        source: str,
        confidence: float,
        notes: str = ""
    ) -> None:
        """Record one piece of gathered evidence."""
        self.evidence_log.append({
            "kind": kind,
            "source": source,
            "confidence": confidence,
            "notes": notes,
        })

    def add_assumption(self, assumption: str, confidence: float) -> None:
        """Record an unverified belief that was taken for granted."""
        self.assumptions.append(f"{assumption} (confidence: {confidence})")

    def add_unknown(self, unknown: str) -> None:
        """Record something known to be unknown."""
        self.unknowns.append(unknown)

    def evaluate(
        self,
        min_evidence_items: int = 3,
        max_undocumented_assumptions: int = 2,
        max_uncertainty: float = 0.25
    ) -> ReadinessCheckResult:
        """
        Evaluate readiness to move from noetic to praxic.

        Args:
            min_evidence_items: Minimum pieces of evidence required
            max_undocumented_assumptions: Max assumptions allowed before blocking
            max_uncertainty: Maximum acceptable uncertainty (0.0 = certain, 1.0 = fully uncertain)

        Returns:
            ReadinessCheckResult with level, blockers, recommendations
        """
        blockers: List[str] = []
        passed_checks: List[str] = []
        recommendations: List[str] = []

        # Check 1: Evidence sufficiency
        if len(self.evidence_log) < min_evidence_items:
            blockers.append(
                f"Insufficient evidence: {len(self.evidence_log)} items gathered, "
                f"{min_evidence_items} required"
            )
        else:
            passed_checks.append(
                f"Evidence sufficiency: {len(self.evidence_log)}/{min_evidence_items} items"
            )

        # Check 2: Evidence confidence
        avg_confidence = self._avg_confidence()
        if avg_confidence < 0.6:
            blockers.append(
                f"Low evidence confidence: {avg_confidence:.2f} (threshold: 0.6)"
            )
        else:
            passed_checks.append(f"Evidence confidence acceptable: {avg_confidence:.2f}")

        # Check 3: Assumption documentation
        undocumented = len(self.assumptions)
        if undocumented > max_undocumented_assumptions:
            blockers.append(
                f"Too many undocumented assumptions: {undocumented} "
                f"(max: {max_undocumented_assumptions})"
            )
        else:
            passed_checks.append(f"Assumptions documented: {undocumented} total")

        # Check 4: Unknown resolution
        unresolved_unknowns = len(self.unknowns)
        if unresolved_unknowns > 3:
            recommendations.append(
                f"High number of unknowns ({unresolved_unknowns}); "
                "consider resolving before proceeding"
            )

        # Check 5: Overall uncertainty
        uncertainty = self._compute_uncertainty()
        if uncertainty > max_uncertainty:
            blockers.append(
                f"Uncertainty too high: {uncertainty:.2f} (max: {max_uncertainty})"
            )
        else:
            passed_checks.append(f"Uncertainty acceptable: {uncertainty:.2f}")

        # Determine readiness level
        if blockers:
            level = ReadinessLevel.NOT_READY
        elif recommendations:
            level = ReadinessLevel.PARTIALLY_READY
        else:
            level = ReadinessLevel.READY

        return ReadinessCheckResult(
            level=level,
            evidence_gathered=len(self.evidence_log),
            evidence_required=min_evidence_items,
            assumptions_undocumented=undocumented,
            uncertainty_level=uncertainty,
            blockers=blockers,
            passed_checks=passed_checks,
            recommendations=recommendations,
        )

    def _avg_confidence(self) -> float:
        """Compute average confidence across all evidence."""
        if not self.evidence_log:
            return 0.0
        total = sum(e["confidence"] for e in self.evidence_log)
        return total / len(self.evidence_log)

    def _compute_uncertainty(self) -> float:
        """
        Compute overall uncertainty as function of:
        - Inverse average confidence
        - Proportion of unknowns
        - Assumption risk
        """
        base_uncertainty = 1.0 - self._avg_confidence()
        unknown_risk = len(self.unknowns) * 0.05  # Each unknown adds 5%
        assumption_risk = len(self.assumptions) * 0.03  # Each assumption adds 3%

        total = min(1.0, base_uncertainty + unknown_risk + assumption_risk)
        return total

    def to_json(self) -> str:
        """Serialize gate state to JSON."""
        return json.dumps({
            "evidence_log": self.evidence_log,
            "assumptions": self.assumptions,
            "unknowns": self.unknowns,
        }, indent=2)
