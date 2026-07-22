#!/usr/bin/env python3
"""
Per-Practice 'Know' Vector Discount Factors — Phase 5 Week 1 Implementation

Applies practice-scoped discounts to the empirica 'know' vector before convergence
computation. Root cause analysis (Phase 4) identified that 'know' vector semantics
are task-scoped, not universal:

  autonomy: 'know' = operational routing confidence (discount 0.65×)
  humanaios: 'know' = technical rubric comprehension (discount 0.75×)
  outreach: 'know' = voice consistency confidence (discount 0.85×)
  evaluator: 'know' = calibration understanding (discount 1.0×, no change)

This module is intended to hook into empirica's CHECK gate or POSTFLIGHT phase,
applying the discount before convergence_signal computation.

Usage:
    from per_practice_know_discounts import apply_practice_discount

    # In CHECK or POSTFLIGHT context
    postflight_vectors = {...}
    practice_id = "autonomy"
    effective_know = apply_practice_discount(postflight_vectors["know"], practice_id)
    postflight_vectors["know"] = effective_know  # for convergence computation
"""

from typing import Tuple


# Per-practice discount factors (derived from Phase 4 calibration curves)
PRACTICE_KNOW_DISCOUNTS = {
    "autonomy": 0.65,           # Operational → grounding: 0.65×
    "humanaios": 0.75,          # Technical → grounding: 0.75×
    "outreach": 0.85,           # Voice consistency → grounding: 0.85×
    "empirica-foundation-evaluator": 1.0,  # Already grounding-aligned
    "evaluator": 1.0,           # Short form also supported
}


def apply_practice_discount(know_value: float, practice_id: str) -> float:
    """
    Apply per-practice discount factor to 'know' vector.

    Args:
        know_value: Empirica postflight 'know' vector (0.0-1.0)
        practice_id: Practice/AI ID (e.g., "autonomy", "humanaios", "empirica-foundation-evaluator")

    Returns:
        Effective 'know' value after discount (0.0-1.0)

    Example:
        >>> apply_practice_discount(0.95, "autonomy")
        0.6175  # 0.95 * 0.65
        >>> apply_practice_discount(0.97, "evaluator")
        0.97    # No discount (1.0× factor)
    """
    # Extract practice name from canonical 3-form if provided
    if "." in practice_id:
        # format: "org.tenant.practice" → extract "practice"
        practice_id = practice_id.split(".")[-1]

    # Look up discount factor (default 1.0 if practice not in mapping)
    discount = PRACTICE_KNOW_DISCOUNTS.get(practice_id, 1.0)

    # Apply discount (clamp result to [0, 1])
    effective_know = know_value * discount
    return round(max(0.0, min(1.0, effective_know)), 3)


def compute_effective_vectors(
    postflight_vectors: dict,
    practice_id: str
) -> Tuple[dict, dict]:
    """
    Apply per-practice discounts to postflight vectors.

    Returns both original and effective vectors for comparison/logging.

    Args:
        postflight_vectors: Empirica postflight state (must include 'know' key)
        practice_id: Practice identifier

    Returns:
        Tuple of (original_vectors, effective_vectors)
    """
    original = postflight_vectors.copy()
    effective = postflight_vectors.copy()

    # Apply discount to 'know' vector
    original_know = postflight_vectors.get("know", 0.5)
    effective_know = apply_practice_discount(original_know, practice_id)

    effective["know"] = effective_know

    # Record the adjustment for logging
    adjustment = original_know - effective_know
    effective["_know_adjustment"] = round(adjustment, 3)
    effective["_know_discount_factor"] = PRACTICE_KNOW_DISCOUNTS.get(
        practice_id.split(".")[-1] if "." in practice_id else practice_id,
        1.0
    )

    return original, effective


def compute_convergence_with_discount(
    postflight_vectors: dict,
    acat_grounding: dict,
    practice_id: str
) -> dict:
    """
    Compute convergence signal with practice-specific 'know' discount applied.

    Args:
        postflight_vectors: Empirica postflight vectors
        acat_grounding: ACAT assessment result (must include 'phase_score' key)
        practice_id: Practice identifier

    Returns:
        Convergence signal dict with discounted 'know' and adjustment metadata
    """
    original, effective = compute_effective_vectors(postflight_vectors, practice_id)

    # Compute ACAT as vector (normalize phase_score 1-4 to 0-1 scale)
    acat_phase_score = acat_grounding.get("phase_score", 2.0)
    acat_as_vector = acat_phase_score / 4.0

    # Convergence using EFFECTIVE (discounted) know
    delta = effective["know"] - acat_as_vector

    return {
        "empirica_know_original": round(original["know"], 3),
        "empirica_know_effective": round(effective["know"], 3),
        "know_adjustment": effective.get("_know_adjustment", 0.0),
        "know_discount_factor": effective.get("_know_discount_factor", 1.0),
        "empirica_uncertainty": round(postflight_vectors.get("uncertainty", 0.5), 3),
        "acat_phase": acat_grounding.get("phase", 2),
        "acat_phase_score": acat_phase_score,
        "acat_as_vector": round(acat_as_vector, 3),
        "convergence_delta": round(delta, 3),
        "direction": "optimistic" if delta > 0.05 else ("pessimistic" if delta < -0.05 else "aligned"),
        "confidence": acat_grounding.get("confidence", 0.8),
        "grounding_improved_vs_phase3_baseline": delta < 0.387,  # Phase 3 mean
    }


def estimate_phase5_convergence(
    phase3_session_data: list,
    apply_discounts: bool = True
) -> dict:
    """
    Project Phase 5 convergence improvements by applying discounts to Phase 3 sessions.

    Useful for estimating effectiveness before full deployment.

    Args:
        phase3_session_data: List of Phase 3 session dicts (from phase3_multi_practice_results.json)
        apply_discounts: If True, apply discounts; if False, return original for comparison

    Returns:
        Analysis dict with before/after convergence metrics
    """
    practice_deltas = {}

    for session in phase3_session_data:
        practice = session["practice"]
        if practice not in practice_deltas:
            practice_deltas[practice] = {"original": [], "effective": []}

        postflight = session["empirica_postflight"]
        acat = session["acat_grounding"]

        # Original convergence (Phase 3 baseline)
        original_delta = session["convergence"]["convergence_delta"]
        practice_deltas[practice]["original"].append(original_delta)

        # Effective convergence with discount (Phase 5 projection)
        if apply_discounts:
            convergence = compute_convergence_with_discount(postflight, acat, practice)
            effective_delta = convergence["convergence_delta"]
        else:
            effective_delta = original_delta

        practice_deltas[practice]["effective"].append(effective_delta)

    # Compute statistics
    analysis = {
        "phase": "Phase 5 (Projected)",
        "discount_approach": "per-practice factors" if apply_discounts else "none",
        "by_practice": {},
    }

    for practice, data in practice_deltas.items():
        original_deltas = data["original"]
        effective_deltas = data["effective"]

        original_mean = sum(original_deltas) / len(original_deltas)
        effective_mean = sum(effective_deltas) / len(effective_deltas)
        improvement = original_mean - effective_mean

        analysis["by_practice"][practice] = {
            "session_count": len(original_deltas),
            "original_mean_delta": round(original_mean, 4),
            "effective_mean_delta": round(effective_mean, 4),
            "improvement": round(improvement, 4),
            "improvement_pct": round((improvement / original_mean * 100), 1) if original_mean > 0 else 0,
            "discount_factor": PRACTICE_KNOW_DISCOUNTS.get(practice, 1.0),
        }

    # Overall summary
    all_original = [d for deltas in practice_deltas.values() for d in deltas["original"]]
    all_effective = [d for deltas in practice_deltas.values() for d in deltas["effective"]]
    overall_improvement = sum(all_original) / len(all_original) - sum(all_effective) / len(all_effective)

    analysis["overall"] = {
        "session_count": len(all_original),
        "original_mean_delta": round(sum(all_original) / len(all_original), 4),
        "effective_mean_delta": round(sum(all_effective) / len(all_effective), 4),
        "overall_improvement": round(overall_improvement, 4),
        "overall_improvement_pct": round((overall_improvement / (sum(all_original) / len(all_original)) * 100), 1),
    }

    return analysis


if __name__ == "__main__":
    # Example: project Phase 5 improvements on Phase 3 data
    import json
    from pathlib import Path

    phase3_file = Path("phase3_multi_practice_results.json")
    if phase3_file.exists():
        with open(phase3_file) as f:
            phase3_data = json.load(f)

        analysis = estimate_phase5_convergence(phase3_data["sessions"], apply_discounts=True)
        print("Phase 5 Convergence Projection (with discount factors applied):")
        print(json.dumps(analysis, indent=2))
    else:
        print(f"Phase 3 data file not found: {phase3_file}")
        # Standalone example
        print("\nStandalone example:")
        print(f"  autonomy know=0.99 → effective={apply_practice_discount(0.99, 'autonomy')}")
        print(f"  humanaios know=1.00 → effective={apply_practice_discount(1.0, 'humanaios')}")
        print(f"  outreach know=0.97 → effective={apply_practice_discount(0.97, 'outreach')}")
        print(f"  evaluator know=1.00 → effective={apply_practice_discount(1.0, 'evaluator')}")
