"""
Resource guard: Enforce resource allocation constraints before execution.

Verifies:
- Human labor budget: remaining hours vs. work estimate
- AI token budget: remaining tokens vs. estimated consumption
- Practice bandwidth: active practices not overloaded
- Escalation capacity: required escalations within SLA
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum
import json


class ResourceCheckLevel(str, Enum):
    """Resource check outcome."""
    SUFFICIENT = "sufficient"
    INSUFFICIENT = "insufficient"
    WARNING = "warning"  # Sufficient but tight


@dataclass
class ResourceBudget:
    """Current resource allocation state."""
    human_labor_hours_remaining: float
    ai_tokens_remaining: int
    practices_active: int
    practices_capacity: int  # Max practices that should be active
    escalations_pending: int
    escalation_sla_hours: float


@dataclass
class ResourceEstimate:
    """Estimated consumption for proposed work."""
    human_labor_hours: float
    ai_tokens: int
    practices_affected: int
    escalations_required: int


@dataclass
class ResourceCheckResult:
    """Result of resource allocation verification."""
    level: ResourceCheckLevel
    budget: ResourceBudget
    estimate: ResourceEstimate
    passed_checks: List[str]
    warnings: List[str]
    blockers: List[str]
    recommendations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "level": self.level.value,
            "budget": {
                "human_labor_hours_remaining": self.budget.human_labor_hours_remaining,
                "ai_tokens_remaining": self.budget.ai_tokens_remaining,
                "practices_active": self.budget.practices_active,
                "practices_capacity": self.budget.practices_capacity,
                "escalations_pending": self.budget.escalations_pending,
                "escalation_sla_hours": self.budget.escalation_sla_hours,
            },
            "estimate": {
                "human_labor_hours": self.estimate.human_labor_hours,
                "ai_tokens": self.estimate.ai_tokens,
                "practices_affected": self.estimate.practices_affected,
                "escalations_required": self.estimate.escalations_required,
            },
            "passed_checks": self.passed_checks,
            "warnings": self.warnings,
            "blockers": self.blockers,
            "recommendations": self.recommendations,
        }


class ResourceGuard:
    """
    Gate that enforces resource accountability before action.

    Resource-based transaction discipline requires that actions declare
    their resource consumption and verify budget exists. This guard
    prevents overcommitment by validating allocation constraints.
    """

    def __init__(self, budget: ResourceBudget):
        self.budget = budget

    def check(self, estimate: ResourceEstimate) -> ResourceCheckResult:
        """
        Verify that proposed work fits within resource constraints.

        Args:
            estimate: Expected resource consumption

        Returns:
            ResourceCheckResult with level, blockers, warnings
        """
        blockers: List[str] = []
        warnings: List[str] = []
        passed_checks: List[str] = []
        recommendations: List[str] = []

        # Check 1: Human labor budget
        if estimate.human_labor_hours > self.budget.human_labor_hours_remaining:
            blockers.append(
                f"Human labor overcommit: {estimate.human_labor_hours} hours estimated, "
                f"only {self.budget.human_labor_hours_remaining} remaining"
            )
        elif estimate.human_labor_hours > self.budget.human_labor_hours_remaining * 0.8:
            warnings.append(
                f"Human labor warning: {estimate.human_labor_hours} hours requested, "
                f"only {self.budget.human_labor_hours_remaining} remaining (80% threshold)"
            )
        else:
            passed_checks.append(
                f"Human labor sufficient: {estimate.human_labor_hours}h "
                f"<< {self.budget.human_labor_hours_remaining}h remaining"
            )

        # Check 2: AI token budget
        if estimate.ai_tokens > self.budget.ai_tokens_remaining:
            blockers.append(
                f"Token budget overcommit: {estimate.ai_tokens} tokens estimated, "
                f"only {self.budget.ai_tokens_remaining} remaining"
            )
        elif estimate.ai_tokens > self.budget.ai_tokens_remaining * 0.75:
            warnings.append(
                f"Token budget warning: {estimate.ai_tokens} tokens requested, "
                f"only {self.budget.ai_tokens_remaining} remaining (75% threshold)"
            )
        else:
            passed_checks.append(
                f"Token budget sufficient: {estimate.ai_tokens} "
                f"<< {self.budget.ai_tokens_remaining} remaining"
            )

        # Check 3: Practice capacity
        new_active = self.budget.practices_active + estimate.practices_affected
        if new_active > self.budget.practices_capacity:
            blockers.append(
                f"Practice capacity exceeded: {new_active} total active practices, "
                f"limit is {self.budget.practices_capacity}"
            )
        elif new_active > self.budget.practices_capacity * 0.85:
            warnings.append(
                f"Practice capacity warning: {new_active} active practices, "
                f"capacity is {self.budget.practices_capacity} (85% threshold)"
            )
        else:
            passed_checks.append(
                f"Practice capacity available: {new_active} "
                f"<< {self.budget.practices_capacity} capacity"
            )

        # Check 4: Escalation availability
        pending_plus_new = self.budget.escalations_pending + estimate.escalations_required
        # Assume 1 escalation per 2 hours of SLA
        escalation_capacity = int(self.budget.escalation_sla_hours / 2)
        if pending_plus_new > escalation_capacity:
            warnings.append(
                f"Escalation queue filling: {pending_plus_new} total pending, "
                f"capacity ~{escalation_capacity} within SLA"
            )
        else:
            passed_checks.append(
                f"Escalation capacity available: {pending_plus_new} "
                f"<< {escalation_capacity} capacity"
            )

        # Determine level
        if blockers:
            level = ResourceCheckLevel.INSUFFICIENT
        elif warnings:
            level = ResourceCheckLevel.WARNING
            recommendations.append(
                "Consider deferring non-critical practices or reducing work scope"
            )
        else:
            level = ResourceCheckLevel.SUFFICIENT

        return ResourceCheckResult(
            level=level,
            budget=self.budget,
            estimate=estimate,
            passed_checks=passed_checks,
            warnings=warnings,
            blockers=blockers,
            recommendations=recommendations,
        )

    def update_budget(self, new_budget: ResourceBudget) -> None:
        """Update budget state (e.g., after consuming resources)."""
        self.budget = new_budget
