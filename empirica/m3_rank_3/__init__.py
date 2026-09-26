"""
M3 Rank 3: State Sync Validation

Validates divergence reports and recovers from mismatches:
- T3-A: Validation protocol (hash verification)
- T3-B: Recovery procedures (correction dispatch)
- T3-C: Chaos testing (resilience verification)
- T3-D: Integration tests (end-to-end scenarios)
"""

from .validation_recovery import (
    ValidationOrchestrator,
    RecoveryOrchestrator,
    ValidationVerdict,
    RecoveryResult,
    AuthorityStrategy,
)

__all__ = [
    'ValidationOrchestrator',
    'RecoveryOrchestrator',
    'ValidationVerdict',
    'RecoveryResult',
    'AuthorityStrategy',
]
