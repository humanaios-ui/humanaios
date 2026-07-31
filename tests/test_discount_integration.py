#!/usr/bin/env python3
"""
Unit tests for per-practice know discount integration in POSTFLIGHT hook.

Tests verify:
1. Discount factors are correctly applied per practice
2. Convergence delta computation uses effective (discounted) know
3. Canonical 3-form practice IDs are correctly parsed
4. Original delta is preserved for comparison
"""

import sys
from pathlib import Path

# Add parent dir to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from hooks.acat_postflight_integration import compute_convergence_signal
from per_practice_know_discounts import apply_practice_discount


def test_discount_application():
    """Test that discount factors are correctly applied per practice."""
    test_cases = [
        ("autonomy", 0.99, 0.65, "autonomy should reduce know by 35%"),
        ("humanaios", 1.0, 0.75, "humanaios should reduce know by 25%"),
        ("outreach", 0.97, 0.85, "outreach should reduce know by 15%"),
        ("empirica-foundation-evaluator", 1.0, 1.0, "evaluator should have no reduction"),
    ]

    for practice_id, original_know, expected_discount, description in test_cases:
        effective_know = apply_practice_discount(original_know, practice_id)
        expected_effective = round(original_know * expected_discount, 3)
        assert effective_know == expected_effective, (
            f"{description}: expected {expected_effective}, got {effective_know}"
        )
    print("✓ Discount application test passed")


def test_canonical_form_parsing():
    """Test that canonical 3-form practice IDs are correctly parsed."""
    test_cases = [
        ("empirica-foundation.carly.autonomy", 0.99, 0.65),
        ("empirica-foundation.carly.humanaios", 1.0, 0.75),
        ("org.tenant.outreach", 0.97, 0.85),
    ]

    for canonical_id, original_know, expected_discount in test_cases:
        effective_know = apply_practice_discount(original_know, canonical_id)
        expected_effective = round(original_know * expected_discount, 3)
        assert effective_know == expected_effective, (
            f"Failed to parse {canonical_id}: expected {expected_effective}, got {effective_know}"
        )
    print("✓ Canonical form parsing test passed")


def test_convergence_with_discount():
    """Test that convergence delta correctly uses discounted know."""
    empirica_vectors = {"know": 0.99, "uncertainty": 0.15}
    acat_grounding = {"phase_score": 2.18, "phase": 4, "confidence": 0.83}

    # Test with discount (autonomy)
    result_with_discount = compute_convergence_signal(
        empirica_vectors, acat_grounding, practice_id="autonomy"
    )

    # Test without discount (evaluator)
    result_no_discount = compute_convergence_signal(
        empirica_vectors, acat_grounding, practice_id="empirica-foundation-evaluator"
    )

    # With discount:
    # original_know = 0.99, effective_know = 0.643, acat = 2.18/4 = 0.545
    # delta_original = 0.99 - 0.545 = 0.445
    # delta_effective = 0.643 - 0.545 = 0.098
    assert result_with_discount["signal"]["delta_original"] == 0.445
    assert result_with_discount["signal"]["delta"] == 0.098
    assert result_with_discount["signal"]["improvement"] == 0.347

    # Without discount:
    # original_know = 0.99, effective_know = 0.99 (no discount), acat = 0.545
    # delta = 0.99 - 0.545 = 0.445
    assert result_no_discount["signal"]["delta"] == 0.445
    assert result_no_discount["signal"]["improvement"] == 0.0

    print("✓ Convergence with discount test passed")


def test_convergence_direction():
    """Test that convergence direction is correctly determined."""
    empirica_vectors = {"know": 0.80, "uncertainty": 0.20}
    acat_high = {"phase_score": 2.0, "phase": 3, "confidence": 0.85}  # acat = 0.5

    # With autonomy discount: know = 0.80 * 0.65 = 0.52
    # delta = 0.52 - 0.5 = 0.02 → aligned
    result = compute_convergence_signal(empirica_vectors, acat_high, practice_id="autonomy")
    assert result["signal"]["direction"] == "empirica_optimistic"
    assert result["calibration_implication"] == "aligned"

    print("✓ Convergence direction test passed")


if __name__ == "__main__":
    print("Running discount integration tests...\n")
    test_discount_application()
    test_canonical_form_parsing()
    test_convergence_with_discount()
    test_convergence_direction()
    print("\n✅ All tests passed!")
