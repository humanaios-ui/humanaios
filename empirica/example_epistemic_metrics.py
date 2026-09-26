#!/usr/bin/env python3
"""
Example: Using Epistemic Health Metrics with POSTFLIGHT Payloads

This example demonstrates how to:
1. Create epistemic metrics from POSTFLIGHT JSON payloads
2. Record individual metrics
3. Compute comprehensive health snapshots
4. Integrate with OTEL instrumentation
5. Export metrics to JSON for observability systems
"""

import json
from datetime import datetime
from epistemic_metrics import EpistemicHealthMetrics


# ===== Example 1: Basic POSTFLIGHT Payload Processing =====

def example_basic_postflight_processing():
    """Process a real-looking POSTFLIGHT payload and extract metrics"""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic POSTFLIGHT Payload Processing")
    print("=" * 70)

    # Realistic POSTFLIGHT payload structure
    postflight_payload = {
        "session_id": "abc123def456",
        "timestamp": datetime.utcnow().isoformat(),
        "work_type": "code",
        "vectors": {
            "know": 0.88,
            "do": 0.92,
            "context": 0.85,
            "clarity": 0.90,
            "coherence": 0.88,
            "signal": 0.85,
            "density": 0.82,
            "state": 0.80,
            "change": 0.45,  # Significant changes made
            "completion": 0.95,
            "impact": 0.80,
            "engagement": 0.98,
            "uncertainty": 0.12,  # Low uncertainty = high confidence
        },
        "artifacts": {
            "findings": 8,
            "unknowns": 2,  # Few unknowns - good epistemic discipline
            "decisions": 3,
            "assumptions": 1,
            "mistakes": 0,
            "dead_ends": 1,
            "goals": 4,
        },
        "goals": [
            {"goal_id": "g1", "status": "completed", "in_scope": True},
            {"goal_id": "g2", "status": "completed", "in_scope": True},
            {"goal_id": "g3", "status": "completed", "in_scope": True},
            {"goal_id": "g4", "status": "completed", "in_scope": True},
        ],
        "investigation_latency_seconds": 28.5,
    }

    # Create metrics from payload
    metrics = EpistemicHealthMetrics.from_postflight_payload(postflight_payload)

    print("\n1. Compute Calibration Drift")
    drift_result = metrics.record_calibration_drift(metrics.compute_calibration_drift())
    print(f"   Drift: {drift_result['value']}")
    print(f"   Threshold exceeded: {drift_result['threshold_exceeded']}")
    if drift_result.get('alert'):
        print(f"   ⚠ {drift_result['alert']}")

    print("\n2. Unknown Accumulation")
    unknown_result = metrics.record_unknown_accumulation()
    print(f"   Count: {unknown_result['count']}")
    print(f"   Threshold exceeded: {unknown_result['threshold_exceeded']}")

    print("\n3. Investigation Latency")
    latency_result = metrics.record_investigation_latency()
    print(f"   Time: {latency_result['seconds']}s")

    print("\n4. Artifact Type Violations")
    violations_result = metrics.record_artifact_type_violations()
    print(f"   Violations: {violations_result['violation_count']}")
    for v in violations_result['violations']:
        print(f"     - {v['type']}: {v['description']}")

    print("\n5. Goal Completion Ratio")
    goal_result = metrics.record_goal_completion_ratio()
    print(f"   Completion: {goal_result['ratio']:.1%} ({goal_result['completed_goals']}/{goal_result['in_scope_goals']})")

    print("\nAll metrics computed successfully!")


# ===== Example 2: Detecting Epistemic Health Issues =====

def example_detect_issues():
    """Demonstrate detection of common epistemic health problems"""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Detecting Epistemic Health Issues")
    print("=" * 70)

    # Payload with issues
    problematic_payload = {
        "vectors": {
            "uncertainty": 0.80,  # HIGH uncertainty
            "know": 0.5,
            "completion": 0.4,
        },
        "artifacts": {
            "findings": 25,  # Many findings
            "unknowns": 0,   # NO unknowns logged (drift signal!)
            "decisions": 0,
            "assumptions": 0,
            "mistakes": 0,
            "dead_ends": 0,
            "goals": 5,
        },
        "goals": [
            {"goal_id": "g1", "status": "in_progress", "in_scope": True},
            {"goal_id": "g2", "status": "in_progress", "in_scope": True},
            {"goal_id": "g3", "status": "planned", "in_scope": True},
        ],
    }

    metrics = EpistemicHealthMetrics.from_postflight_payload(problematic_payload)

    print("\n[Issue Detection Results]\n")

    # 1. Calibration drift
    drift = metrics.compute_calibration_drift()
    drift_result = metrics.record_calibration_drift(drift)
    if drift_result["threshold_exceeded"]:
        print(f"🚨 CALIBRATION DRIFT: {drift_result['alert']}")
        print(f"   Reason: High uncertainty ({problematic_payload['vectors']['uncertainty']}) but no unknowns logged")
        print(f"   Action: {drift_result['recommended_action']}")

    # 2. Unknown accumulation
    print()
    unknown_result = metrics.record_unknown_accumulation()
    if unknown_result["threshold_exceeded"]:
        print(f"🚨 UNKNOWN ACCUMULATION: {unknown_result['alert']}")
    else:
        print(f"✓ Unknown count OK: {unknown_result['count']}")

    # 3. Artifact type violations
    print()
    violations = metrics.detect_artifact_type_violations()
    if violations:
        print(f"🚨 ARTIFACT TYPE VIOLATIONS: {len(violations)} detected")
        for v in violations:
            print(f"   - {v['type'].upper()}")
            print(f"     {v['description']}")
    else:
        print(f"✓ Artifact discipline OK")

    # 4. Goal completion
    print()
    goal_result = metrics.record_goal_completion_ratio()
    if goal_result["threshold_exceeded"]:
        print(f"🚨 GOAL COMPLETION: {goal_result['alert']}")
        print(f"   Action: {goal_result['recommended_action']}")
    else:
        print(f"✓ Goal completion OK: {goal_result['ratio']:.1%}")


# ===== Example 3: JSON Export for External Systems =====

def example_json_export():
    """Export epistemic metrics as JSON for monitoring systems"""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: JSON Export for Observability Systems")
    print("=" * 70)

    payload = {
        "vectors": {
            "know": 0.85,
            "uncertainty": 0.15,
            "completion": 0.92,
        },
        "artifacts": {
            "findings": 6,
            "unknowns": 2,
            "decisions": 2,
            "assumptions": 1,
            "mistakes": 0,
            "dead_ends": 0,
            "goals": 3,
        },
        "goals": [
            {"goal_id": "g1", "status": "completed", "in_scope": True},
            {"goal_id": "g2", "status": "completed", "in_scope": True},
            {"goal_id": "g3", "status": "in_progress", "in_scope": True},
        ],
    }

    metrics = EpistemicHealthMetrics.from_postflight_payload(payload)
    json_output = metrics.to_json()

    print("\nJSON Metrics Output:")
    print("-" * 70)
    # Parse and pretty-print
    parsed = json.loads(json_output)
    print(json.dumps(parsed, indent=2))

    print("\n" + "-" * 70)
    print("This JSON can be sent to:")
    print("  - Prometheus (via Node Exporter or Pushgateway)")
    print("  - Loki (via labels and message)")
    print("  - CloudWatch / Datadog (via structured logs)")
    print("  - Custom observability dashboards")


# ===== Example 4: Manual Metric Recording =====

def example_manual_recording():
    """Manually record metrics step-by-step (lower-level API)"""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Manual Metric Recording")
    print("=" * 70)

    metrics = EpistemicHealthMetrics()

    print("\n1. Record vectors")
    from epistemic_metrics import EpistemicVector
    metrics._vectors = {
        "know": EpistemicVector("know", 0.88),
        "uncertainty": EpistemicVector("uncertainty", 0.12),
        "completion": EpistemicVector("completion", 0.95),
    }
    print(f"   Recorded {len(metrics._vectors)} vectors")

    print("\n2. Record artifacts")
    metrics.ingest_artifacts({
        "findings": 8,
        "unknowns": 2,
        "decisions": 2,
    })
    print(f"   Total artifacts: {metrics._artifact_counts.total()}")

    print("\n3. Add goals")
    metrics.add_goal("g1", "completed")
    metrics.add_goal("g2", "completed")
    metrics.add_goal("g3", "in_progress")
    print(f"   Added {len(metrics._goals)} goals")

    print("\n4. Mark phase transitions")
    import time
    metrics.mark_phase_transition("noetic_start")
    time.sleep(0.05)
    metrics.mark_phase_transition("noetic_end")
    metrics.mark_phase_transition("CHECK_start")
    time.sleep(0.05)
    metrics.mark_phase_transition("CHECK_end")
    print(f"   Recorded {len(metrics._phase_transitions)} phase events")

    print("\n5. Compute all metrics")
    all_metrics = metrics.compute_all_metrics()
    print(f"   Calibration drift: {all_metrics['metrics']['calibration_drift']['value']:.3f}")
    print(f"   Goal completion: {all_metrics['metrics']['goal_completion_ratio']['ratio']:.1%}")
    print(f"   Phase speeds: {list(all_metrics['metrics']['phase_transition_speed']['speeds'].keys())}")


# ===== Example 5: Batch Processing Multiple Sessions =====

def example_batch_processing():
    """Process metrics from multiple POSTFLIGHT payloads"""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Batch Processing Multiple Sessions")
    print("=" * 70)

    sessions = [
        {
            "session_id": "session_1",
            "vectors": {"know": 0.85, "uncertainty": 0.15, "completion": 0.90},
            "artifacts": {"findings": 8, "unknowns": 2, "decisions": 2, "goals": 3},
            "goals": [
                {"goal_id": "g1", "status": "completed", "in_scope": True},
                {"goal_id": "g2", "status": "completed", "in_scope": True},
                {"goal_id": "g3", "status": "completed", "in_scope": True},
            ],
        },
        {
            "session_id": "session_2",
            "vectors": {"know": 0.72, "uncertainty": 0.38, "completion": 0.65},
            "artifacts": {"findings": 12, "unknowns": 5, "decisions": 1, "goals": 4},
            "goals": [
                {"goal_id": "g1", "status": "in_progress", "in_scope": True},
                {"goal_id": "g2", "status": "completed", "in_scope": True},
                {"goal_id": "g3", "status": "in_progress", "in_scope": True},
                {"goal_id": "g4", "status": "planned", "in_scope": True},
            ],
        },
    ]

    print(f"\nProcessing {len(sessions)} sessions...\n")

    for session_data in sessions:
        session_id = session_data["session_id"]
        metrics = EpistemicHealthMetrics.from_postflight_payload(session_data)

        drift = metrics.compute_calibration_drift()
        goal_ratio, completed, in_scope = metrics.compute_goal_completion_ratio()

        print(f"Session: {session_id}")
        print(f"  Calibration Drift: {drift:.3f}")
        print(f"  Goal Completion: {goal_ratio:.1%} ({completed}/{in_scope})")
        print(f"  Total Artifacts: {metrics._artifact_counts.total()}")
        print()


# ===== Main =====

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("Epistemic Health Metrics - Usage Examples")
    print("Phase 3.5.6 Integration Guide")
    print("=" * 70)

    example_basic_postflight_processing()
    example_detect_issues()
    example_json_export()
    example_manual_recording()
    example_batch_processing()

    print("\n" + "=" * 70)
    print("✓ All examples completed successfully!")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Integrate EpistemicHealthMetrics.from_postflight_payload() into your POSTFLIGHT handler")
    print("  2. Route JSON output to Prometheus/Loki for visualization")
    print("  3. Set up alerts based on threshold_exceeded flags")
    print("  4. Monitor trend of key metrics across sessions")
    print("\n" + "=" * 70 + "\n")
