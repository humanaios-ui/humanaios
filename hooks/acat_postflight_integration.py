"""
POSTFLIGHT hook: Integrate ACAT assessment scoring into empirica session record.

This hook is called AFTER empirica postflight-submit to:
1. Call acat-score assess to evaluate the session transcript
2. Enrich the session record with acat_grounding section
3. Compute convergence signal (empirica vectors vs. ACAT phase)
4. Apply per-practice 'know' discount factors (Phase 5 Week 1 calibration)

Usage: Hook into empirica's POSTFLIGHT phase via empirica hook registry.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from uuid import uuid4

# Import per-practice discount factors
from per_practice_know_discounts import apply_practice_discount


def run_acat_assessment(
    session_id: str,
    ai_id: str,
    behavior_transcript_path: str | None = None,
    api_key: str | None = None,
    model: str = "claude-opus-4-8",
) -> dict | None:
    """
    Run ACAT assessment via CLI and return structured grounding result.

    Args:
        session_id: empirica session ID
        ai_id: Practice/AI identifier
        behavior_transcript_path: Path to session log/transcript (optional)
        api_key: Anthropic API key (or from env ACAT_API_KEY)
        model: Claude model to use

    Returns:
        Parsed ACAT grounding dict, or None if assessment failed
    """

    # Resolve API key
    if not api_key:
        api_key = os.environ.get("ACAT_API_KEY")
    if not api_key:
        print("Warning: ACAT_API_KEY not set; skipping ACAT assessment", file=sys.stderr)
        return None

    # Build CLI command
    acat_script = Path(__file__).resolve().parent.parent / "operations" / "bin" / "acat-score"
    if not acat_script.exists():
        print(f"Warning: acat-score script not found at {acat_script}; skipping", file=sys.stderr)
        return None

    cmd = [
        "python3",
        str(acat_script),
        "assess",
        "--session-id",
        session_id,
        "--ai-id",
        ai_id,
        "--rubric-version",
        "v1.0",
        "--api-key",
        api_key,
        "--model",
        model,
        "--output",
        "json",
    ]

    if behavior_transcript_path:
        cmd.extend(["--behavior-transcript", behavior_transcript_path])

    try:
        # Run ACAT assessment (timeout: 150s = 2min assessment + buffer)
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=150,
        )

        if result.returncode != 0:
            print(f"Warning: acat-score failed: {result.stderr}", file=sys.stderr)
            return None

        # Parse JSON output
        acat_output = json.loads(result.stdout)
        return acat_output

    except subprocess.TimeoutExpired:
        print("Warning: acat-score timed out after 150s", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"Warning: acat-score output not valid JSON: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Warning: acat-score invocation failed: {e}", file=sys.stderr)
        return None


def compute_convergence_signal(
    empirica_vectors: dict,
    acat_grounding: dict,
    practice_id: str | None = None,
) -> dict:
    """
    Compute convergence signal: gap between empirica self-assessment and ACAT observation.

    Applies per-practice 'know' discount factors (Phase 5 Week 1 calibration) to align
    empirica self-assessment with grounding-based ACAT observation.

    Args:
        empirica_vectors: Dict of empirica vector self-assessments (know, uncertainty, etc.)
        acat_grounding: ACAT assessment output (phase, phase_score, rubric_alignment)
        practice_id: Practice/AI identifier (e.g., "autonomy", "humanaios"). If None, no discount applied.

    Returns:
        Convergence signal dict with deltas (both original and effective), direction, and discount metadata
    """

    empirica_know_original = empirica_vectors.get("know", 0.5)
    acat_phase_score = acat_grounding.get("phase_score", 2.0)

    # Apply per-practice discount (Phase 5 Week 1 calibration)
    if practice_id:
        empirica_know_effective = apply_practice_discount(empirica_know_original, practice_id)
        discount_factor = apply_practice_discount(1.0, practice_id) / 1.0  # Extract discount multiplier
    else:
        empirica_know_effective = empirica_know_original
        discount_factor = 1.0

    # Normalize ACAT phase_score (1.0-4.0) to empirica vector scale (0.0-1.0)
    # Simple mapping: phase_score / 4.0
    acat_as_vector = acat_phase_score / 4.0

    # Compute delta using EFFECTIVE (discounted) 'know'
    delta = empirica_know_effective - acat_as_vector
    delta_original = empirica_know_original - acat_as_vector

    direction = "empirica_optimistic" if delta > 0 else "empirica_pessimistic"
    confidence = acat_grounding.get("confidence", 0.8)

    return {
        "empirica_believes_original": {"know": round(empirica_know_original, 3)},
        "empirica_believes_effective": {"know": round(empirica_know_effective, 3)},
        "know_discount_factor": discount_factor,
        "acat_observes": {"phase": acat_grounding.get("phase"), "confidence": confidence},
        "signal": {
            "delta_original": round(delta_original, 3),
            "delta": round(delta, 3),  # Effective delta (after discount)
            "improvement": round(delta_original - delta, 3),
            "direction": direction,
            "confidence": confidence,
        },
        "calibration_implication": (
            "slight_overestimation" if delta > 0.1
            else "slight_underestimation" if delta < -0.1
            else "aligned"
        ),
    }


def enrich_session_record(
    session_record: dict,
    acat_grounding: dict,
    empirica_vectors: dict,
    practice_id: str | None = None,
) -> dict:
    """
    Enrich empirica session record with ACAT grounding and convergence signal.

    Args:
        session_record: Empirica session DB record
        acat_grounding: ACAT assessment output
        empirica_vectors: Postflight empirica vectors
        practice_id: Practice/AI identifier (for per-practice know discount)

    Returns:
        Enriched session record
    """

    if not acat_grounding:
        return session_record

    convergence = compute_convergence_signal(empirica_vectors, acat_grounding, practice_id)

    # Add acat_grounding section
    session_record["acat_grounding"] = {
        "phase": acat_grounding.get("phase"),
        "phase_score": acat_grounding.get("phase_score"),
        "confidence": acat_grounding.get("confidence"),
        "rubric_alignment": acat_grounding.get("rubric_alignment", {}),
        "observations": acat_grounding.get("observations", []),
        "assessment_id": acat_grounding.get("assessment_id"),
        "timestamp": acat_grounding.get("timestamp"),
    }

    # Add convergence signal
    session_record["convergence"] = convergence

    return session_record


# Hook entry point
def postflight_hook(context: dict, **kwargs) -> dict:
    """
    Empirica POSTFLIGHT hook: integrate ACAT assessment + per-practice know discounts.

    Context dict should contain:
        - session_id: empirica session ID
        - ai_id: Practice/AI identifier (canonical 3-form or bare name)
        - session_record: Empirica session DB record (dict)
        - vectors: Postflight empirica vectors (dict)
        - behavior_transcript_path: Optional path to session log
    """

    session_id = context.get("session_id")
    ai_id = context.get("ai_id")
    session_record = context.get("session_record", {})
    vectors = context.get("vectors", {})
    transcript_path = context.get("behavior_transcript_path")

    if not session_id or not ai_id:
        print("Warning: postflight_hook missing session_id or ai_id", file=sys.stderr)
        return context

    # Extract practice name from ai_id (canonical 3-form: org.tenant.practice or bare name)
    practice_id = ai_id.split(".")[-1] if "." in ai_id else ai_id

    # Run ACAT assessment
    acat_grounding = run_acat_assessment(
        session_id=session_id,
        ai_id=ai_id,
        behavior_transcript_path=transcript_path,
    )

    # Enrich session record with ACAT grounding and per-practice discounted convergence
    if acat_grounding:
        enriched_record = enrich_session_record(session_record, acat_grounding, vectors, practice_id)
        context["session_record"] = enriched_record
        context["acat_grounding"] = acat_grounding
        context["convergence"] = enriched_record.get("convergence")

    return context


if __name__ == "__main__":
    # Example invocation for testing with per-practice discount factors
    print("=" * 80)
    print("Testing POSTFLIGHT Hook with Per-Practice Know Discounts (Phase 5 Week 1)")
    print("=" * 80)

    # Example 1: autonomy (0.65× discount)
    print("\n1. AUTONOMY (0.65× know discount)")
    test_context_autonomy = {
        "session_id": "test-autonomy-001",
        "ai_id": "empirica-foundation.carly.empirica-autonomy",
        "session_record": {"id": "test-autonomy-001"},
        "vectors": {"know": 0.99, "uncertainty": 0.15},
    }
    result_autonomy = postflight_hook(test_context_autonomy)
    convergence_aut = result_autonomy.get("convergence", {})
    if convergence_aut:
        print(f"  Original know: {convergence_aut['empirica_believes_original']}")
        print(f"  Effective know (discounted): {convergence_aut['empirica_believes_effective']}")
        print(f"  Delta (original vs effective): {convergence_aut['signal']}")

    # Example 2: humanaios (0.75× discount)
    print("\n2. HUMANAIOS (0.75× know discount)")
    test_context_humanaios = {
        "session_id": "test-humanaios-001",
        "ai_id": "empirica-foundation.carly.humanaios",
        "session_record": {"id": "test-humanaios-001"},
        "vectors": {"know": 1.0, "uncertainty": 0.12},
    }
    result_humanaios = postflight_hook(test_context_humanaios)
    convergence_hum = result_humanaios.get("convergence", {})
    if convergence_hum:
        print(f"  Original know: {convergence_hum['empirica_believes_original']}")
        print(f"  Effective know (discounted): {convergence_hum['empirica_believes_effective']}")
        print(f"  Delta (original vs effective): {convergence_hum['signal']}")

    # Example 3: evaluator (1.0× no discount)
    print("\n3. EVALUATOR (1.0× no discount)")
    test_context_evaluator = {
        "session_id": "test-evaluator-001",
        "ai_id": "empirica-foundation-evaluator",
        "session_record": {"id": "test-evaluator-001"},
        "vectors": {"know": 0.92, "uncertainty": 0.22},
    }
    result_evaluator = postflight_hook(test_context_evaluator)
    convergence_eval = result_evaluator.get("convergence", {})
    if convergence_eval:
        print(f"  Original know: {convergence_eval['empirica_believes_original']}")
        print(f"  Effective know (no discount): {convergence_eval['empirica_believes_effective']}")
        print(f"  Delta (original vs effective): {convergence_eval['signal']}")

    print("\n" + "=" * 80)
