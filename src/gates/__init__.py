"""
Validation gates for Sentinel checkpoint enforcement.

Three independent gates enforce transaction discipline:
- readiness_gates: Verify noetic work complete before praxic
- resource_guard: Check allocation constraints
- sentinel_verify: Verify epistemic vectors meet action thresholds

CLI commands available via: python3 -m src.gates.cli
  - readiness-check: Verify noetic phase completion
  - resource-check: Validate resource allocation
  - sentinel-verify: Check epistemic vectors for action
"""

from .readiness_gates import ReadinessGate, ReadinessLevel, EvidenceRequirement
from .resource_guard import ResourceGuard, ResourceBudget, ResourceEstimate, ResourceCheckLevel
from .sentinel_verify import SentinelGate, ActionType, EpistemicVectors, VectorLevel

__all__ = [
    "ReadinessGate",
    "ReadinessLevel",
    "EvidenceRequirement",
    "ResourceGuard",
    "ResourceBudget",
    "ResourceEstimate",
    "ResourceCheckLevel",
    "SentinelGate",
    "ActionType",
    "EpistemicVectors",
    "VectorLevel",
]
