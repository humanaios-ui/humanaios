"""
M3 Rank 2: Divergence Detection

Detects out-of-sync state across practices:
- T2-A: State fingerprinting (Merkle tree hashing)
- T2-B: Cross-practice diff algorithm
- T2-C: Divergence reporting & alerting (deferred to T2-D)
- T2-D: Integration tests
"""

from .divergence_detection import (
    StateFingerprinter,
    DiffAlgorithm,
    FingerprintResult,
    DivergenceReport,
)

__all__ = [
    'StateFingerprinter',
    'DiffAlgorithm',
    'FingerprintResult',
    'DivergenceReport',
]
