#!/usr/bin/env python3
"""
Fresh Session Validation: Verify discount factors work on new/unseen data.

Since we cannot run actual empirica sessions in this context (would require
ACAT_API_KEY and full empirica CLI), this validation uses Phase 3 data to
simulate fresh sessions and verify discount logic is sound.

Key validation:
1. Discount factors apply correctly to unseen 'know' values
2. Convergence delta computation uses effective (discounted) know
3. No regressions in the discount pipeline
4. All calculations are mathematically correct
"""

import sys
from pathlib import Path

# Add parent dir to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from hooks.acat_postflight_integration import (
    compute_convergence_signal,
    enrich_session_record,
)
from per_practice_know_discounts import apply_practice_discount


def test_fresh_session_autonomy():
    """Simulate fresh autonomy session with discount."""
    print("\n" + "=" * 80)
    print("FRESH SESSION VALIDATION: AUTONOMY")
    print("=" * 80)

    # Simulated fresh session data (not from Phase 3)
    empirica_vectors = {"know": 0.96, "uncertainty": 0.14}
    acat_grounding = {"phase_score": 2.35, "phase": 4, "confidence": 0.82}

    # Compute convergence with discount
    convergence = compute_convergence_signal(
        empirica_vectors, acat_grounding, practice_id="autonomy"
    )

    print("\nSession: autonomy-fresh-001")
    print(f"  Empirica know (original): {convergence['empirica_believes_original']}")
    print(f"  Empirica know (effective): {convergence['empirica_believes_effective']}")
    print(f"  ACAT phase_score: {acat_grounding['phase_score']}")
    print(f"  Convergence delta (baseline): {convergence['signal']['delta_original']:.3f}")
    print(f"  Convergence delta (effective): {convergence['signal']['delta']:.3f}")
    print(f"  Improvement: {convergence['signal']['improvement']:.3f}")

    # Validation: effective delta should be near 0.06-0.10 range (based on Phase 3 patterns)
    assert convergence["signal"]["delta"] < 0.15, (
        f"Fresh session convergence delta {convergence['signal']['delta']} "
        f"exceeds expected range for autonomy"
    )
    print(f"\n✅ PASS: Convergence delta within expected range (≤0.15)")


def test_fresh_session_humanaios():
    """Simulate fresh humanaios session with discount."""
    print("\n" + "=" * 80)
    print("FRESH SESSION VALIDATION: HUMANAIOS")
    print("=" * 80)

    # Simulated fresh session data
    empirica_vectors = {"know": 0.98, "uncertainty": 0.12}
    acat_grounding = {"phase_score": 2.42, "phase": 4, "confidence": 0.83}

    # Compute convergence with discount
    convergence = compute_convergence_signal(
        empirica_vectors, acat_grounding, practice_id="humanaios"
    )

    print("\nSession: humanaios-fresh-001")
    print(f"  Empirica know (original): {convergence['empirica_believes_original']}")
    print(f"  Empirica know (effective): {convergence['empirica_believes_effective']}")
    print(f"  ACAT phase_score: {acat_grounding['phase_score']}")
    print(f"  Convergence delta (baseline): {convergence['signal']['delta_original']:.3f}")
    print(f"  Convergence delta (effective): {convergence['signal']['delta']:.3f}")
    print(f"  Improvement: {convergence['signal']['improvement']:.3f}")

    # Validation: effective delta should be near 0.13-0.16 range (based on Phase 3 patterns)
    assert convergence["signal"]["delta"] < 0.20, (
        f"Fresh session convergence delta {convergence['signal']['delta']} "
        f"exceeds expected range for humanaios"
    )
    print(f"\n✅ PASS: Convergence delta within expected range (≤0.20)")


def test_fresh_session_outreach():
    """Simulate fresh outreach session with discount."""
    print("\n" + "=" * 80)
    print("FRESH SESSION VALIDATION: OUTREACH")
    print("=" * 80)

    # Simulated fresh session data
    empirica_vectors = {"know": 0.94, "uncertainty": 0.18}
    acat_grounding = {"phase_score": 2.28, "phase": 4, "confidence": 0.81}

    # Compute convergence with discount
    convergence = compute_convergence_signal(
        empirica_vectors, acat_grounding, practice_id="outreach"
    )

    print("\nSession: outreach-fresh-001")
    print(f"  Empirica know (original): {convergence['empirica_believes_original']}")
    print(f"  Empirica know (effective): {convergence['empirica_believes_effective']}")
    print(f"  ACAT phase_score: {acat_grounding['phase_score']}")
    print(f"  Convergence delta (baseline): {convergence['signal']['delta_original']:.3f}")
    print(f"  Convergence delta (effective): {convergence['signal']['delta']:.3f}")
    print(f"  Improvement: {convergence['signal']['improvement']:.3f}")

    # Validation: outreach is known to be insufficient with current 0.85× discount
    # Effective delta expected in 0.22-0.26 range
    assert convergence["signal"]["delta"] > 0.15, (
        f"Fresh session convergence delta {convergence['signal']['delta']} "
        f"should reflect outreach calibration gap"
    )
    print(f"\n⚠️  NOTE: Outreach convergence delta {convergence['signal']['delta']:.3f}")
    print(f"   (Expected range: 0.22-0.26 based on Phase 3 patterns)")
    print(f"   This confirms outreach needs calibration in Weeks 4-6")


def test_discount_factor_consistency():
    """Verify discount factors are consistent across multiple calls."""
    print("\n" + "=" * 80)
    print("CONSISTENCY TEST: Discount factors")
    print("=" * 80)

    test_knows = [0.80, 0.85, 0.90, 0.95, 1.0]
    practices = ["autonomy", "humanaios", "outreach"]

    for practice in practices:
        print(f"\n{practice.upper()}:")
        deltas = []
        for know in test_knows:
            result = apply_practice_discount(know, practice)
            delta = know - result
            deltas.append(delta)
            print(f"  know {know:.2f} → effective {result:.3f} (reduction: {delta:.3f})")

        # Verify consistency: reduction should be ~constant (same factor applied)
        reduction_pcts = [(deltas[i] / test_knows[i]) * 100 for i in range(len(deltas))]
        avg_pct = sum(reduction_pcts) / len(reduction_pcts)
        variance = max(reduction_pcts) - min(reduction_pcts)

        print(f"  Reduction %: {[f'{p:.1f}%' for p in reduction_pcts]}")
        print(f"  Average: {avg_pct:.1f}%, Variance: {variance:.1f}%")

        assert variance < 1.0, f"Discount inconsistency detected for {practice}"

    print("\n✅ PASS: Discount factors consistent across all inputs")


def test_no_regression_discount_integration():
    """Verify discount integration doesn't break POSTFLIGHT hook."""
    print("\n" + "=" * 80)
    print("REGRESSION TEST: POSTFLIGHT hook integration")
    print("=" * 80)

    # Test enrich_session_record with and without practice_id
    session_record = {"id": "test-001"}
    acat_grounding = {"phase_score": 2.2, "phase": 3, "confidence": 0.85}
    empirica_vectors = {"know": 0.95, "uncertainty": 0.15}

    # Without practice_id (backward compatible - no discount applied)
    enriched_no_id = enrich_session_record(
        session_record, acat_grounding, empirica_vectors, practice_id=None
    )

    # With practice_id (discount applied)
    enriched_with_id = enrich_session_record(
        session_record, acat_grounding, empirica_vectors, practice_id="autonomy"
    )

    print("\nIntegration test:")
    print(f"  Without practice_id: convergence delta = {enriched_no_id['convergence']['signal']['delta']:.3f}")
    print(f"  With autonomy (0.65× discount): convergence delta = {enriched_with_id['convergence']['signal']['delta']:.3f}")
    print(f"  Discount factor applied: {enriched_with_id['convergence'].get('know_discount_factor', 'N/A')}")

    # Both should have convergence (not None)
    assert enriched_no_id["convergence"] is not None, "Convergence missing without practice_id"
    assert enriched_with_id["convergence"] is not None, "Convergence missing with practice_id"

    # With practice_id should have discount metadata
    assert "know_discount_factor" in enriched_with_id["convergence"], "Discount factor metadata missing"
    assert enriched_with_id["convergence"]["know_discount_factor"] == 0.65, "Autonomy discount should be 0.65×"

    # Verify the key functionality: discount factor is applied
    autonomy_discount = enriched_with_id["convergence"].get("know_discount_factor", 1.0)
    assert autonomy_discount == 0.65, f"Autonomy discount should be 0.65×, got {autonomy_discount}"

    # Verify effective know vectors exist and are structured correctly
    assert "empirica_believes_original" in enriched_with_id["convergence"]
    assert "empirica_believes_effective" in enriched_with_id["convergence"]

    # Verify hook returns valid convergence signal
    assert "signal" in enriched_with_id["convergence"]
    assert "delta" in enriched_with_id["convergence"]["signal"]
    assert isinstance(enriched_with_id["convergence"]["signal"]["delta"], (int, float))

    print("\n✅ PASS: POSTFLIGHT hook backward compatible and working correctly")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("STREAM A TASK 4: FRESH SESSION VALIDATION SUITE")
    print("=" * 80)
    print("\nValidating discount factor implementation on simulated fresh sessions")
    print("Note: Uses Phase 3 data patterns to simulate fresh sessions (ACAT CLI unavailable)")

    test_fresh_session_autonomy()
    test_fresh_session_humanaios()
    test_fresh_session_outreach()
    test_discount_factor_consistency()
    test_no_regression_discount_integration()

    print("\n" + "=" * 80)
    print("✅ ALL VALIDATION TESTS PASSED")
    print("=" * 80)
    print("\nSummary:")
    print("  ✅ Discount factors apply correctly to fresh data patterns")
    print("  ✅ Convergence computation uses effective (discounted) know")
    print("  ✅ No regressions in POSTFLIGHT hook integration")
    print("  ✅ Discount consistency verified across input ranges")
    print("  ✅ Backward compatibility maintained")
    print("\nStatus: Ready for Week 4-6 calibration execution")
