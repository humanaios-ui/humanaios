#!/usr/bin/env python3
"""
Phase 5 Week 2: Rubric Variant Projections

Project phase_score improvements by applying practice-specific rubric variants
to Phase 3 session data. This estimates whether Week 2 rubric designs will
effectively validate the semantic hypothesis.
"""

import json
from pathlib import Path
from operations.acat.cli.rubric_variants import (
    get_rubric_variant,
    estimate_phase_score_delta,
)


def project_week2_results(phase3_file: str = "phase3_multi_practice_results.json") -> dict:
    """Project Week 2 rubric variant improvements on Phase 3 data.

    Args:
        phase3_file: Path to Phase 3 results JSON

    Returns:
        Analysis dict with projections by practice
    """
    phase3_path = Path(phase3_file)
    if not phase3_path.exists():
        raise FileNotFoundError(f"Phase 3 data not found: {phase3_file}")

    with open(phase3_path) as f:
        phase3_data = json.load(f)

    # Map practice to variant
    practice_variants = {
        "autonomy": "v1.2a",
        "humanaios": "v1.2b",
        "outreach": "v1.2c",
    }

    analysis = {
        "phase": "Phase 5 Week 2",
        "rubric_focus": "practice-specific variants (v1.2a/b/c)",
        "by_practice": {},
    }

    for session in phase3_data["sessions"]:
        practice = session["practice"]
        if practice not in practice_variants:
            continue

        if practice not in analysis["by_practice"]:
            analysis["by_practice"][practice] = {
                "sessions": [],
                "variant": practice_variants[practice],
            }

        # Extract ACAT scores from session
        acat_scores = session["acat_grounding"]

        # Compute phase_score deltas
        # Phase 3 sessions used v1.1 rubric; project to practice-specific variant
        delta = estimate_phase_score_delta(
            base_scores=_mock_scores_from_rubric_alignment(acat_scores),
            variant_from="v1.1",
            variant_to=practice_variants[practice],
        )

        session_result = {
            "session_id": session["session_id"],
            "session_num": session["session_num"],
            "phase_score_v1_1": acat_scores["phase_score"],
            "phase_score_variant": delta["score_to"],
            "delta": delta["score_delta"],
            "improvement_pct": round(
                (delta["score_delta"] / acat_scores["phase_score"] * 100), 1
            ),
        }

        analysis["by_practice"][practice]["sessions"].append(session_result)

    # Aggregate per practice
    for practice, data in analysis["by_practice"].items():
        sessions = data["sessions"]
        if sessions:
            deltas = [s["delta"] for s in sessions]
            mean_delta = sum(deltas) / len(deltas)
            improvement_pcts = [s["improvement_pct"] for s in sessions]

            data["mean_delta"] = round(mean_delta, 3)
            data["mean_improvement_pct"] = round(sum(improvement_pcts) / len(improvement_pcts), 1)
            data["session_count"] = len(sessions)

    return analysis


def _mock_scores_from_rubric_alignment(acat_grounding: dict) -> dict:
    """Reconstruct approximate 6D scores from rubric_alignment status.

    Since we don't have raw scores in Phase 3 data, estimate from rubric alignment.
    This is a simplification for projection purposes.
    """
    alignment = acat_grounding.get("rubric_alignment", {})

    # Map alignment status to mid-range score
    status_scores = {
        "met": 85,  # Assume "met" = ~85
        "partial": 65,  # Assume "partial" = ~65
        "unmet": 40,  # Assume "unmet" = ~40
    }

    return {
        dim: status_scores.get(alignment.get(dim, "partial"), 65)
        for dim in [
            "truthfulness",
            "service_orientation",
            "harm_awareness",
            "autonomy_respect",
            "value_alignment",
            "humility",
        ]
    }


def print_week2_analysis(analysis: dict) -> None:
    """Pretty-print Week 2 projection analysis."""
    print("\n" + "=" * 80)
    print("PHASE 5 WEEK 2: RUBRIC VARIANT PROJECTIONS")
    print("=" * 80)
    print(f"\nPhase: {analysis['phase']}")
    print(f"Approach: {analysis['rubric_focus']}")

    print("\n" + "-" * 80)
    print("PER-PRACTICE PROJECTIONS")
    print("-" * 80)

    for practice, data in analysis["by_practice"].items():
        print(f"\n{practice.upper()} — {data['variant']}")
        print(f"  Sessions: {data.get('session_count', 0)}")
        print(f"  Mean phase_score delta: +{data.get('mean_delta', 0):.3f}")
        print(f"  Mean improvement: +{data.get('mean_improvement_pct', 0):.1f}%")

        sessions = data.get("sessions", [])
        if sessions:
            print(f"  Breakdown:")
            for s in sessions:
                print(
                    f"    {s['session_id']}: {s['phase_score_v1_1']:.2f} → "
                    f"{s['phase_score_variant']:.2f} ({s['delta']:+.3f}, {s['improvement_pct']:+.1f}%)"
                )

    print("\n" + "-" * 80)
    print("SUCCESS CRITERIA (WEEK 2 GATES)")
    print("-" * 80)

    success = True
    for practice, data in analysis["by_practice"].items():
        mean_delta = data.get("mean_delta", 0)
        target = 0.05  # Target: ≥+0.05 improvement per practice
        meets_criteria = mean_delta >= target

        status = "✅" if meets_criteria else "❌"
        print(f"{status} {practice}: {mean_delta:.3f} (target ≥{target:.3f})")

        if not meets_criteria:
            success = False

    print("\n" + "-" * 80)
    if success:
        print("RECOMMENDATION: Week 2 rubric variants show sufficient improvement.")
        print("Proceed to Week 3: re-score Phase 3 sessions with practice-specific rubrics.")
    else:
        print("RECOMMENDATION: Practice-specific rubrics show marginal improvement.")
        print("May need rubric refinement or alternative approach (e.g., dimension tuning).")
    print("-" * 80)


if __name__ == "__main__":
    try:
        analysis = project_week2_results()
        print_week2_analysis(analysis)

        # Export full results
        output_file = "phase5_week2_projections.json"
        with open(output_file, "w") as f:
            json.dump(analysis, f, indent=2)
        print(f"\nFull analysis exported to {output_file}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nMake sure phase3_multi_practice_results.json exists in current directory.")
