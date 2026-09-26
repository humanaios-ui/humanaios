#!/usr/bin/env python3
"""
Epistemic Metrics Mapping for Phase 3.6
Maps 13-vector empirica framework to Prometheus metric names and labels
"""

from typing import Dict, List, Tuple

# 13-vector epistemic framework
EPISTEMIC_VECTORS = [
    "know",
    "do",
    "context",
    "clarity",
    "coherence",
    "signal",
    "density",
    "state",
    "change",
    "completion",
    "impact",
    "engagement",
    "uncertainty",
]

# Vector to Prometheus metric name mapping
VECTOR_METRIC_MAPPING = {
    "know": "empirica_know_gauge",
    "do": "empirica_do_gauge",
    "context": "empirica_context_gauge",
    "clarity": "empirica_clarity_gauge",
    "coherence": "empirica_coherence_gauge",
    "signal": "empirica_signal_gauge",
    "density": "empirica_density_gauge",
    "state": "empirica_state_gauge",
    "change": "empirica_change_gauge",
    "completion": "empirica_completion_gauge",
    "impact": "empirica_impact_gauge",
    "engagement": "empirica_engagement_gauge",
    "uncertainty": "empirica_uncertainty_gauge",
}

# Vector descriptions for Prometheus help text
VECTOR_DESCRIPTIONS = {
    "know": "Self-assessed domain understanding (0.0-1.0)",
    "do": "Execution ability (0.0-1.0)",
    "context": "Surrounding state awareness (0.0-1.0)",
    "clarity": "Path-forward clarity (0.0-1.0)",
    "coherence": "Internal consistency of understanding (0.0-1.0)",
    "signal": "Information quality (0.0-1.0)",
    "density": "Knowledge density per context unit (0.0-1.0)",
    "state": "System state awareness (0.0-1.0)",
    "change": "Amount of change made (0.0-1.0)",
    "completion": "Progress toward current phase goal (0.0-1.0)",
    "impact": "Significance of work to project (0.0-1.0)",
    "engagement": "Active engagement level (0.0-1.0)",
    "uncertainty": "Unknowns remaining (0.0-1.0)",
}

# Meta-metrics
META_METRICS = {
    "empirica_transaction_duration_seconds": "Transaction total duration (histogram)",
    "empirica_artifacts_logged_total": "Total artifacts logged (counter)",
    "empirica_commits_total": "Total commits created (counter)",
    "empirica_noetic_duration_seconds": "Noetic phase duration (histogram)",
    "empirica_praxic_duration_seconds": "Praxic phase duration (histogram)",
}

# Standard labels
STANDARD_LABELS = ["transaction_id", "practice"]
ARTIFACT_LABELS = ["artifact_type", "practice"]
PHASE_LABELS = ["phase", "transaction_id", "practice"]


def validate_vector_dict(vectors: Dict[str, float]) -> bool:
    """Validate that vector dict has all 13 vectors in 0.0-1.0 range"""
    if not isinstance(vectors, dict):
        return False
    if len(vectors) != len(EPISTEMIC_VECTORS):
        return False
    for vector_name in EPISTEMIC_VECTORS:
        if vector_name not in vectors:
            return False
        value = vectors[vector_name]
        if not isinstance(value, (int, float)) or value < 0.0 or value > 1.0:
            return False
    return True


def get_metric_name(vector_name: str) -> str:
    """Get Prometheus metric name for a vector"""
    if vector_name not in VECTOR_METRIC_MAPPING:
        raise ValueError(f"Unknown vector: {vector_name}")
    return VECTOR_METRIC_MAPPING[vector_name]


def get_vector_description(vector_name: str) -> str:
    """Get description for a vector"""
    if vector_name not in VECTOR_DESCRIPTIONS:
        raise ValueError(f"Unknown vector: {vector_name}")
    return VECTOR_DESCRIPTIONS[vector_name]


def vector_dict_to_observations(vectors: Dict[str, float],
                               transaction_id: str,
                               practice: str) -> List[Tuple[str, float, Dict[str, str]]]:
    """Convert vector dict to (metric_name, value, labels) tuples for emission"""
    if not validate_vector_dict(vectors):
        return []

    observations = []
    labels = {"transaction_id": transaction_id, "practice": practice}
    for vector_name, value in vectors.items():
        metric_name = get_metric_name(vector_name)
        observations.append((metric_name, value, labels))
    return observations


def get_vector_by_index(index: int) -> str:
    """Get vector name by index (0-12)"""
    if index < 0 or index >= len(EPISTEMIC_VECTORS):
        raise IndexError(f"Vector index {index} out of range")
    return EPISTEMIC_VECTORS[index]


def get_vector_index(vector_name: str) -> int:
    """Get index of vector in the 13-vector array"""
    try:
        return EPISTEMIC_VECTORS.index(vector_name)
    except ValueError:
        raise ValueError(f"Unknown vector: {vector_name}")


def create_vector_timeseries_label_set(vectors: Dict[str, float]) -> Dict[str, float]:
    """Create a time-series-ready dict mapping metric names to values"""
    result = {}
    for vector_name in EPISTEMIC_VECTORS:
        metric_name = get_metric_name(vector_name)
        result[metric_name] = vectors.get(vector_name, 0.0)
    return result


# Calibration vector weights (per work_type)
VECTOR_WEIGHTS_BY_WORK_TYPE = {
    "code": {
        "know": 0.07,
        "do": 0.12,
        "context": 0.07,
        "clarity": 0.08,
        "coherence": 0.07,
        "signal": 0.06,
        "density": 0.06,
        "state": 0.07,
        "change": 0.08,
        "completion": 0.09,
        "impact": 0.08,
        "engagement": 0.06,
    },
    "research": {
        "know": 0.12,
        "do": 0.06,
        "context": 0.08,
        "clarity": 0.08,
        "coherence": 0.09,
        "signal": 0.08,
        "density": 0.10,
        "state": 0.06,
        "change": 0.04,
        "completion": 0.07,
        "impact": 0.06,
        "engagement": 0.06,
    },
    "docs": {
        "know": 0.08,
        "do": 0.05,
        "context": 0.06,
        "clarity": 0.12,
        "coherence": 0.09,
        "signal": 0.08,
        "density": 0.10,
        "state": 0.05,
        "change": 0.04,
        "completion": 0.10,
        "impact": 0.07,
        "engagement": 0.06,
    },
}


def get_vector_weights(work_type: str) -> Dict[str, float]:
    """Get vector weights for calibration by work type"""
    return VECTOR_WEIGHTS_BY_WORK_TYPE.get(work_type, {})
