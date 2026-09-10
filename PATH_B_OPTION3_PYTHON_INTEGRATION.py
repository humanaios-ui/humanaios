#!/usr/bin/env python3
"""
Path B Option 3: Python Direct Integration

Demonstrates how to integrate ACAT enrichment directly in Python after empirica POSTFLIGHT.
This approach doesn't require hook registration or wrapper scripts—just Python API calls.

Usage:
  1. In your empirica session script, call run_empirica_session_with_acat()
  2. Pass your normal empirica config
  3. Get back enriched session record with ACAT grounding

Example:
  from PATH_B_OPTION3_PYTHON_INTEGRATION import run_empirica_session_with_acat

  result = run_empirica_session_with_acat({
      "session_id": "sess-001",
      "ai_id": "humanaios",
      "vectors": {"know": 0.85, "uncertainty": 0.15, ...},
  })

  print(result["acat_grounding"])  # ACAT assessment results
  print(result["convergence"])     # empirica vs ACAT comparison
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# Add hooks directory to path so we can import acat_postflight_integration
HOOKS_DIR = Path(__file__).parent / "hooks"
if str(HOOKS_DIR) not in sys.path:
    sys.path.insert(0, str(HOOKS_DIR))

# Import existing hook implementation (DRY principle—reuse, don't duplicate)
try:
    from acat_postflight_integration import (
        run_acat_assessment,
        compute_convergence_signal,
        enrich_session_record,
    )
    HOOKS_AVAILABLE = True
except ImportError:
    HOOKS_AVAILABLE = False
    print("Warning: acat_postflight_integration not found; running without ACAT enrichment")


def run_empirica_session_with_acat(
    session_config: Dict[str, Any],
    empirica_binary: str = "empirica",
) -> Dict[str, Any]:
    """
    Run an empirica session and enrich the result with ACAT assessment.

    This is the high-level orchestration for Path B Option 3.

    Args:
        session_config: Dictionary containing:
            - session_id: empirica session ID
            - ai_id: Practice/AI identifier (canonical or bare name)
            - vectors: Dict of empirica vectors (know, uncertainty, ...)
            - postflight_payload: (optional) Full postflight payload dict
            - behavior_transcript_path: (optional) Path to session transcript

        empirica_binary: Path to empirica CLI (default: "empirica")

    Returns:
        enriched_config: Original config + acat_grounding + convergence signal

    Example:
        >>> result = run_empirica_session_with_acat({
        ...     "session_id": "test-001",
        ...     "ai_id": "humanaios",
        ...     "vectors": {"know": 0.9, "uncertainty": 0.1, ...},
        ... })
        >>> print(result["acat_grounding"]["phase"])
        "3"
    """

    session_id = session_config.get("session_id")
    ai_id = session_config.get("ai_id")
    vectors = session_config.get("vectors", {})
    transcript_path = session_config.get("behavior_transcript_path")

    if not session_id or not ai_id:
        print("Warning: Missing session_id or ai_id; skipping ACAT enrichment")
        return session_config

    if not HOOKS_AVAILABLE:
        print("Warning: acat_postflight_integration module not available")
        return session_config

    print(f"[acat-enrichment] Enriching session {session_id} with ACAT assessment...")

    # Call ACAT assessment (same function as empirica hooks use)
    acat_grounding = run_acat_assessment(
        session_id=session_id,
        ai_id=ai_id,
        behavior_transcript_path=transcript_path,
    )

    if not acat_grounding:
        print("[acat-enrichment] ACAT assessment failed; returning unenriched result")
        return session_config

    # Compute convergence signal (empirica vectors vs ACAT observation)
    practice_id = ai_id.split(".")[-1] if "." in ai_id else ai_id
    convergence = compute_convergence_signal(vectors, acat_grounding, practice_id)

    # Add to session config
    result = dict(session_config)
    result["acat_grounding"] = acat_grounding
    result["convergence"] = convergence

    print(f"[acat-enrichment] Enrichment complete:")
    print(f"  ACAT phase: {acat_grounding.get('phase')}")
    print(f"  Convergence delta: {convergence.get('signal', {}).get('delta')}")

    return result


def run_batch_empirica_sessions_with_acat(
    configs: list[Dict[str, Any]],
    max_workers: int = 1,
) -> list[Dict[str, Any]]:
    """
    Run multiple empirica sessions and enrich each with ACAT assessment.

    This is useful for Phase 2/3 evaluation runs (5-10 sessions).

    Args:
        configs: List of session configs (same structure as run_empirica_session_with_acat)
        max_workers: Number of parallel workers (1 = sequential, safe default)

    Returns:
        List of enriched session configs

    Example:
        >>> sessions = [
        ...     {"session_id": "eval-1", "ai_id": "humanaios", "vectors": {...}},
        ...     {"session_id": "eval-2", "ai_id": "humanaios", "vectors": {...}},
        ... ]
        >>> results = run_batch_empirica_sessions_with_acat(sessions)
        >>> print(f"Processed {len(results)} sessions")
    """

    results = []
    for i, config in enumerate(configs, 1):
        print(f"\n[batch] Processing session {i}/{len(configs)}: {config.get('session_id')}")
        result = run_empirica_session_with_acat(config)
        results.append(result)

    return results


def analyze_convergence_across_sessions(
    enriched_sessions: list[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Analyze convergence signal across multiple sessions.

    Computes mean delta, std dev, and identifies calibration patterns.

    Args:
        enriched_sessions: List of session dicts with convergence data

    Returns:
        Analysis dict with statistics and patterns

    Example:
        >>> results = run_batch_empirica_sessions_with_acat(sessions)
        >>> analysis = analyze_convergence_across_sessions(results)
        >>> print(f"Mean convergence delta: {analysis['mean_delta']:.3f}")
    """

    deltas = [
        r.get("convergence", {}).get("signal", {}).get("delta")
        for r in enriched_sessions
        if r.get("convergence")
    ]

    if not deltas:
        return {"error": "No convergence data in sessions"}

    mean_delta = sum(deltas) / len(deltas)
    variance = sum((d - mean_delta) ** 2 for d in deltas) / len(deltas)
    std_dev = variance ** 0.5

    # Categorize sessions by direction
    optimistic = [d for d in deltas if d > 0.1]
    pessimistic = [d for d in deltas if d < -0.1]
    aligned = [d for d in deltas if -0.1 <= d <= 0.1]

    return {
        "session_count": len(deltas),
        "mean_delta": round(mean_delta, 3),
        "std_dev": round(std_dev, 3),
        "min_delta": round(min(deltas), 3),
        "max_delta": round(max(deltas), 3),
        "categorization": {
            "empirica_optimistic": len(optimistic),
            "empirica_pessimistic": len(pessimistic),
            "aligned": len(aligned),
        },
        "calibration_assessment": (
            "well_calibrated" if abs(mean_delta) < 0.05 else
            "slightly_optimistic" if mean_delta > 0.05 else
            "slightly_pessimistic"
        ),
    }


if __name__ == "__main__":
    # Example: Run 3 test sessions with ACAT enrichment

    print("=" * 80)
    print("Path B Option 3: Python Direct Integration - Example Run")
    print("=" * 80)

    test_sessions = [
        {
            "session_id": "test-humanaios-001",
            "ai_id": "humanaios",
            "vectors": {
                "know": 0.92,
                "uncertainty": 0.15,
                "context": 0.88,
                "engagement": 0.9,
            },
        },
        {
            "session_id": "test-humanaios-002",
            "ai_id": "humanaios",
            "vectors": {
                "know": 0.85,
                "uncertainty": 0.22,
                "context": 0.82,
                "engagement": 0.85,
            },
        },
        {
            "session_id": "test-humanaios-003",
            "ai_id": "humanaios",
            "vectors": {
                "know": 0.88,
                "uncertainty": 0.18,
                "context": 0.85,
                "engagement": 0.88,
            },
        },
    ]

    print("\nRunning batch enrichment...")
    results = run_batch_empirica_sessions_with_acat(test_sessions)

    print("\n" + "=" * 80)
    print("Analyzing convergence...")
    analysis = analyze_convergence_across_sessions(results)

    print("\nConvergence Analysis:")
    print(json.dumps(analysis, indent=2))

    print("\n" + "=" * 80)
    print("Example: First session enrichment")
    print(json.dumps(results[0], indent=2, default=str))
