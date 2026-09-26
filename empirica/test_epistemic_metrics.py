#!/usr/bin/env python3
"""
Test suite for Phase 3.5.6 Epistemic Health Metrics Module

Tests all 7 metrics:
1. Calibration Drift
2. Unknown Accumulation
3. Investigation Latency
4. Artifact Type Violations
5. Graph Density
6. Goal Completion Ratio
7. Phase Transition Speed
"""

import json
import time
from epistemic_metrics import (
    EpistemicHealthMetrics,
    EpistemicVector,
    ArtifactCounts,
    GoalState,
    ValidationError,
    MetricThreshold,
)


def test_vector_validation():
    """Test epistemic vector validation"""
    print("\n[TEST] Vector Validation")
    print("  ✓ Valid vector (0.5)")
    vec = EpistemicVector("know", 0.5)
    assert vec.value == 0.5

    print("  ✓ Edge cases: 0.0, 1.0")
    vec_min = EpistemicVector("uncertainty", 0.0)
    vec_max = EpistemicVector("clarity", 1.0)
    assert vec_min.value == 0.0
    assert vec_max.value == 1.0

    print("  ✓ Invalid vector raises ValidationError")
    try:
        EpistemicVector("bad", 1.5)
        assert False, "Should have raised ValidationError"
    except ValidationError as e:
        assert "outside [0.0, 1.0]" in str(e)

    print("  ✓ Negative value raises ValidationError")
    try:
        EpistemicVector("bad", -0.1)
        assert False, "Should have raised ValidationError"
    except ValidationError as e:
        assert "outside [0.0, 1.0]" in str(e)


def test_artifact_counts():
    """Test artifact count tracking"""
    print("\n[TEST] Artifact Counts")
    counts = ArtifactCounts(findings=10, unknowns=3, decisions=2, assumptions=1)

    print(f"  ✓ Total: {counts.total()} (expected 16)")
    assert counts.total() == 16

    print(f"  ✓ Total noetic: {counts.total_noetic()} (expected 4)")
    assert counts.total_noetic() == 4

    print(f"  ✓ Total praxic: {counts.total_praxic()} (expected 12)")
    assert counts.total_praxic() == 12


def test_metric_1_calibration_drift():
    """Test Metric 1: Calibration Drift"""
    print("\n[TEST] Metric 1: Calibration Drift")
    metrics = EpistemicHealthMetrics()

    # Scenario 1: Low uncertainty + few unknowns = good calibration
    print("  Scenario 1: Low uncertainty, few unknowns (good calibration)")
    metrics._vectors = {
        "uncertainty": EpistemicVector("uncertainty", 0.1)
    }
    metrics._artifact_counts = ArtifactCounts(unknowns=0)
    drift = metrics.compute_calibration_drift()
    print(f"    Drift: {drift} (should be low)")
    assert drift < 0.3  # Below threshold

    # Scenario 2: High uncertainty + no unknowns = bad calibration (drift)
    print("  Scenario 2: High uncertainty, zero unknowns (bad calibration)")
    metrics._vectors = {
        "uncertainty": EpistemicVector("uncertainty", 0.9)
    }
    metrics._artifact_counts = ArtifactCounts(unknowns=0)
    drift = metrics.compute_calibration_drift()
    print(f"    Drift: {drift} (should be high, > 0.3)")
    assert drift > 0.3  # Above threshold

    # Scenario 3: Findings-only collapse
    print("  Scenario 3: Findings-only collapse")
    metrics._vectors = {
        "uncertainty": EpistemicVector("uncertainty", 0.1)
    }
    metrics._artifact_counts = ArtifactCounts(findings=15, unknowns=0)
    drift = metrics.compute_calibration_drift()
    print(f"    Drift: {drift} (should be high due to type violation)")
    assert drift > 0.3

    result = metrics.record_calibration_drift(drift)
    assert result["metric"] == "calibration_drift"
    assert result["threshold_exceeded"] == (drift > MetricThreshold.CALIBRATION_DRIFT_THRESHOLD.value)
    print(f"    ✓ Metric recorded: {result['value']}")


def test_metric_2_unknown_accumulation():
    """Test Metric 2: Unknown Accumulation"""
    print("\n[TEST] Metric 2: Unknown Accumulation")
    metrics = EpistemicHealthMetrics()

    # Scenario 1: Few unknowns (below threshold)
    print("  Scenario 1: Few unknowns (below threshold)")
    metrics._artifact_counts = ArtifactCounts(unknowns=5)
    result = metrics.record_unknown_accumulation()
    assert result["count"] == 5
    assert result["threshold_exceeded"] == False
    print(f"    ✓ Count: {result['count']}, threshold_exceeded: {result['threshold_exceeded']}")

    # Scenario 2: Many unknowns (above threshold)
    print("  Scenario 2: Many unknowns (above threshold)")
    metrics._artifact_counts = ArtifactCounts(unknowns=15)
    result = metrics.record_unknown_accumulation()
    assert result["count"] == 15
    assert result["threshold_exceeded"] == True
    assert "alert" in result
    print(f"    ✓ Count: {result['count']}, alert triggered: {result['alert']}")


def test_metric_3_investigation_latency():
    """Test Metric 3: Investigation Latency"""
    print("\n[TEST] Metric 3: Investigation Latency")
    metrics = EpistemicHealthMetrics()

    # Mark noetic phase
    print("  Starting noetic phase...")
    metrics.start_noetic_phase()
    time.sleep(0.2)
    elapsed = metrics.end_noetic_phase()

    print(f"    Elapsed: {elapsed:.3f}s (expected ~0.2s)")
    assert 0.15 < elapsed < 0.3  # Allow some variance

    result = metrics.record_investigation_latency()
    assert result["metric"] == "investigation_latency"
    assert "seconds" in result
    assert "phase_transitions" in result
    print(f"    ✓ Latency recorded: {result['seconds']}s")


def test_metric_4_artifact_type_violations():
    """Test Metric 4: Artifact Type Violations"""
    print("\n[TEST] Metric 4: Artifact Type Violations")
    metrics = EpistemicHealthMetrics()

    # Scenario 1: No violations (balanced artifacts)
    print("  Scenario 1: Balanced artifacts (no violations)")
    metrics._artifact_counts = ArtifactCounts(
        findings=5, unknowns=3, decisions=2, assumptions=2, mistakes=1
    )
    violations = metrics.detect_artifact_type_violations()
    assert len(violations) == 0
    print(f"    ✓ Violations: {len(violations)}")

    # Scenario 2: Findings-only collapse
    print("  Scenario 2: Findings-only collapse")
    metrics._artifact_counts = ArtifactCounts(findings=20, unknowns=0)
    violations = metrics.detect_artifact_type_violations()
    assert len(violations) > 0
    assert any(v["type"] == "findings_only_collapse" for v in violations)
    print(f"    ✓ Violations detected: {len(violations)}")

    # Scenario 3: Missing decisions
    print("  Scenario 3: Missing decisions")
    metrics._artifact_counts = ArtifactCounts(
        findings=10, goals=5, mistakes=3, decisions=0
    )
    violations = metrics.detect_artifact_type_violations()
    assert any(v["type"] == "missing_decisions" for v in violations)
    print(f"    ✓ Violations detected: {len(violations)}")

    # Scenario 4: Missing assumptions
    print("  Scenario 4: High uncertainty, no assumptions")
    metrics._vectors = {
        "uncertainty": EpistemicVector("uncertainty", 0.8)
    }
    metrics._artifact_counts = ArtifactCounts(assumptions=0, unknowns=1)
    violations = metrics.detect_artifact_type_violations()
    assert any(v["type"] == "missing_assumptions" for v in violations)
    print(f"    ✓ Violations detected: {len(violations)}")

    result = metrics.record_artifact_type_violations()
    assert result["metric"] == "artifact_type_violations"
    assert "violations" in result
    print(f"    ✓ Violations recorded: {result['violation_count']}")


def test_metric_5_graph_density():
    """Test Metric 5: Graph Density"""
    print("\n[TEST] Metric 5: Graph Density")
    metrics = EpistemicHealthMetrics()

    # Scenario 1: High density (all connected)
    print("  Scenario 1: High density (all artifacts connected)")
    density = metrics.compute_graph_density(connected_artifacts=10, total_artifacts=10)
    assert density == 1.0
    print(f"    Density: {density:.2%}")

    # Scenario 2: Low density (few connected)
    print("  Scenario 2: Low density (few artifacts connected)")
    density = metrics.compute_graph_density(connected_artifacts=3, total_artifacts=20)
    print(f"    Density: {density:.2%}")
    assert density < 0.3

    # Scenario 3: Medium density (at threshold)
    print("  Scenario 3: Medium density (at threshold)")
    density = metrics.compute_graph_density(connected_artifacts=5, total_artifacts=10)
    print(f"    Density: {density:.2%}")
    assert density == 0.5

    result = metrics.record_graph_density(5, 10)
    assert result["metric"] == "graph_density"
    assert result["density"] == 0.5
    assert result["threshold_exceeded"] == False  # 0.5 < 0.5 is False (threshold is not exceeded at edge)
    print(f"    ✓ Density recorded: {result['density']:.2%}")


def test_metric_6_goal_completion_ratio():
    """Test Metric 6: Goal Completion Ratio"""
    print("\n[TEST] Metric 6: Goal Completion Ratio")
    metrics = EpistemicHealthMetrics()

    # Add goals
    print("  Adding goals...")
    metrics.add_goal("g1", "completed")
    metrics.add_goal("g2", "completed")
    metrics.add_goal("g3", "in_progress")
    metrics.add_goal("g4", "abandoned", in_scope=False)

    ratio, completed, in_scope = metrics.compute_goal_completion_ratio()
    print(f"    Completed: {completed}/{in_scope}, Ratio: {ratio:.2%}")
    assert completed == 2
    assert in_scope == 3
    assert abs(ratio - (2 / 3)) < 0.01  # Allow rounding variance (rounded to 3 decimals)

    result = metrics.record_goal_completion_ratio()
    assert result["metric"] == "goal_completion_ratio"
    assert result["completed_goals"] == 2
    assert result["in_scope_goals"] == 3
    print(f"    ✓ Goal completion recorded: {result['ratio']:.2%}")


def test_metric_7_phase_transition_speed():
    """Test Metric 7: Phase Transition Speed"""
    print("\n[TEST] Metric 7: Phase Transition Speed")
    metrics = EpistemicHealthMetrics()

    # Mark phase transitions
    print("  Marking phase transitions...")
    metrics.mark_phase_transition("noetic_start")
    time.sleep(0.1)
    metrics.mark_phase_transition("noetic_end")
    time.sleep(0.05)
    metrics.mark_phase_transition("CHECK_start")
    time.sleep(0.05)
    metrics.mark_phase_transition("CHECK_end")
    time.sleep(0.1)
    metrics.mark_phase_transition("praxic_start")
    time.sleep(0.1)
    metrics.mark_phase_transition("praxic_end")

    speeds = metrics.compute_phase_transition_speeds()
    print(f"    Speeds computed: {list(speeds.keys())}")
    assert "noetic_seconds" in speeds
    assert "CHECK_seconds" in speeds
    assert "praxic_seconds" in speeds
    assert "noetic_to_praxic_seconds" in speeds

    result = metrics.record_phase_transition_speed()
    assert result["metric"] == "phase_transition_speed"
    assert len(result["phase_sequence"]) > 0
    print(f"    ✓ Phase transitions recorded: {len(result['phase_sequence'])} events")


def test_postflight_payload_integration():
    """Test integration with POSTFLIGHT JSON payload"""
    print("\n[TEST] POSTFLIGHT Payload Integration")

    payload = {
        "vectors": {
            "know": 0.85,
            "do": 0.75,
            "context": 0.90,
            "clarity": 0.88,
            "coherence": 0.82,
            "signal": 0.80,
            "density": 0.75,
            "state": 0.85,
            "change": 0.20,
            "completion": 0.90,
            "impact": 0.85,
            "engagement": 0.95,
            "uncertainty": 0.15,
        },
        "artifacts": {
            "findings": 8,
            "unknowns": 2,
            "decisions": 3,
            "assumptions": 1,
            "mistakes": 1,
            "dead_ends": 0,
            "goals": 5,
        },
        "goals": [
            {"goal_id": "g1", "status": "completed", "in_scope": True},
            {"goal_id": "g2", "status": "completed", "in_scope": True},
            {"goal_id": "g3", "status": "in_progress", "in_scope": True},
            {"goal_id": "g4", "status": "abandoned", "in_scope": False},
        ],
        "investigation_latency_seconds": 45.2,
    }

    print("  Creating metrics from payload...")
    metrics = EpistemicHealthMetrics.from_postflight_payload(payload)

    print("  Computing all metrics...")
    all_metrics = metrics.compute_all_metrics()

    print("    ✓ Metrics computed")
    assert "metrics" in all_metrics
    assert "artifact_counts" in all_metrics
    assert "vectors" in all_metrics
    assert all_metrics["metrics"]["calibration_drift"] is not None
    assert all_metrics["metrics"]["unknown_accumulation"] is not None
    assert all_metrics["metrics"]["artifact_type_violations"] is not None
    assert all_metrics["metrics"]["goal_completion_ratio"] is not None

    # Check JSON serialization
    json_str = metrics.to_json()
    parsed = json.loads(json_str)
    assert "metrics" in parsed
    print("    ✓ JSON serialization successful")


def test_otel_integration():
    """Test integration with OTEL instrumentation"""
    print("\n[TEST] OTEL Integration")

    try:
        from otel_instrumentation import initialize_instrumentation
        instr = initialize_instrumentation()

        # Process a sample payload
        payload = {
            "vectors": {"know": 0.8, "uncertainty": 0.2},
            "artifacts": {"findings": 5, "unknowns": 1, "decisions": 2, "goals": 3},
        }

        print("  Processing payload through OTEL instrumentation...")
        result = instr.process_postflight_payload(payload)
        assert "metrics" in result
        print("    ✓ Payload processed successfully")

        # Test epistemic attributes on span
        print("  Adding epistemic attributes to span...")
        instr.add_epistemic_attributes_to_span(payload)
        print("    ✓ Attributes added")

        # Test vector recording
        print("  Recording epistemic vector...")
        instr.record_epistemic_vector("know", 0.85, phase="postflight")
        print("    ✓ Vector recorded")

        # Test artifact recording
        print("  Recording epistemic artifacts...")
        instr.record_epistemic_artifacts({"findings": 10, "unknowns": 2})
        print("    ✓ Artifacts recorded")

    except ImportError as e:
        print(f"  ⚠ OTEL instrumentation not available: {e}")
        print("    (This is okay if running in isolation)")


def run_all_tests():
    """Run all test suites"""
    print("=" * 70)
    print("Phase 3.5.6 Epistemic Health Metrics - Test Suite")
    print("=" * 70)

    try:
        test_vector_validation()
        test_artifact_counts()
        test_metric_1_calibration_drift()
        test_metric_2_unknown_accumulation()
        test_metric_3_investigation_latency()
        test_metric_4_artifact_type_violations()
        test_metric_5_graph_density()
        test_metric_6_goal_completion_ratio()
        test_metric_7_phase_transition_speed()
        test_postflight_payload_integration()
        test_otel_integration()

        print("\n" + "=" * 70)
        print("✓ ALL TESTS PASSED")
        print("=" * 70)
        return True

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
