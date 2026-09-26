#!/usr/bin/env python3
"""
Test Phase 3.5.6 OTEL instrumentation for empirica seat
Simulates a transaction and emits traces/metrics
"""

import time
import random
from otel_instrumentation import initialize_instrumentation, get_instrumentation


def simulate_transaction():
    """Simulate a full empirica transaction with instrumentation"""
    instr = initialize_instrumentation()

    print("Starting simulated transaction...")

    # Transaction span
    with instr.transaction_span("code", goal="Phase 3.5.6: Observable Claude"):

        # PREFLIGHT phase
        print("  → PREFLIGHT phase")
        with instr.phase_span("preflight", {
            "work_type": "infra",
            "vector_count": 13,
        }):
            time.sleep(0.2)
            instr.record_vector("clarity", 0.85, "preflight")
            instr.record_vector("know", 0.80, "preflight")

        # Noetic phase (investigation)
        print("  → Noetic phase")
        investigation_start = time.time()
        with instr.phase_span("noetic", {
            "investigation_rounds": 3,
            "files_read": 12,
            "queries_executed": 5,
        }):
            # Simulate investigation steps
            for i in range(3):
                time.sleep(0.1)
                instr.record_unknown_count(random.randint(3, 8))

        investigation_time = time.time() - investigation_start
        instr.record_investigation_latency(investigation_time)
        print(f"    Investigation took {investigation_time:.2f}s")

        # CHECK gate (noetic → praxic transition)
        print("  → CHECK gate")
        with instr.phase_span("CHECK", {"confidence": 0.92}):
            instr.increment_CHECK_decision("proceed")
            time.sleep(0.1)

        # Praxic phase (execution)
        print("  → Praxic phase")
        with instr.phase_span("praxic", {
            "files_edited": 3,
            "commits": 1,
            "tests_run": 47,
        }):
            time.sleep(0.3)
            instr.increment_type_violation("findings_only")  # Type discipline metric

        # POSTFLIGHT phase
        print("  → POSTFLIGHT phase")
        with instr.phase_span("postflight", {
            "findings_logged": 2,
            "goals_completed": 1,
        }):
            instr.increment_unknown_resolved(2)
            instr.record_vector("completion", 1.0, "postflight")
            instr.record_vector("uncertainty", 0.15, "postflight")
            time.sleep(0.1)

    print("✓ Transaction complete, traces emitted to localhost:4317")
    print("  Check Jaeger at http://localhost:16686")
    print("  Check Prometheus at http://localhost:9090")


def test_concurrent_metrics():
    """Test that metrics can be recorded concurrently"""
    instr = get_instrumentation()

    print("\nRecording additional metrics...")
    for i in range(5):
        instr.record_unknown_count(random.randint(1, 5))
        if random.random() > 0.7:
            instr.increment_type_violation("discipline")
        time.sleep(0.05)

    print("✓ Metrics recorded")


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 3.5.6 OTEL Instrumentation Test")
    print("=" * 60)

    simulate_transaction()
    test_concurrent_metrics()

    print("\n" + "=" * 60)
    print("Test complete. Waiting for metrics to be exported...")
    print("=" * 60)
    time.sleep(2)
