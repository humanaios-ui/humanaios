#!/usr/bin/env python3
"""
Phase 3.5.6 Phase 2: Example - Using CLI Instrumentation Hooks
Demonstrates how to instrument actual empirica CLI commands
"""

import json
import time
from cli_instrumentation_hooks import CLIHookWrapper
from otel_instrumentation import get_instrumentation


def example_instrumented_preflight():
    """Example: Instrument a PREFLIGHT command with context"""
    wrapper = CLIHookWrapper()
    instr = get_instrumentation()

    print("Example 1: Instrumented PREFLIGHT command")
    print("=" * 60)

    # Create PREFLIGHT payload
    preflight_payload = {
        "work_type": "code",
        "work_summary": "Example Phase 3.5.6 work: CLI instrumentation",
        "vectors": {
            "know": 0.85,
            "do": 0.80,
            "context": 0.90,
            "clarity": 0.85,
            "coherence": 0.80,
            "signal": 0.75,
            "density": 0.80,
            "state": 0.85,
            "change": 0.0,
            "completion": 0.0,
            "impact": 0.85,
            "engagement": 0.90,
            "uncertainty": 0.20
        },
        "goals": [
            {
                "objective": "Phase 3.5.6: Observable Claude - CLI Instrumentation",
                "status": "in_progress"
            }
        ]
    }

    # Simulate running: echo $PAYLOAD | empirica preflight-submit -
    # (we won't actually run empirica, just demonstrate the instrumentation)
    payload_json = json.dumps(preflight_payload)

    print(f"Payload: {json.dumps(preflight_payload, indent=2)[:200]}...")
    print()
    print("Calling: empirica preflight-submit -")
    print()

    # Pre-hook: simulates what happens before empirica command
    wrapper.hook.pre_command_hook("preflight-submit", payload_json)
    print("✓ Pre-command hook: transaction span started")
    print(f"  - Phase: preflight")
    print(f"  - Work type: {preflight_payload['work_type']}")
    print(f"  - Goal: {preflight_payload['goals'][0]['objective']}")
    print()

    # Simulate command execution
    time.sleep(0.5)
    print("🔄 Empirica executing: loading configuration, validating vectors...")
    time.sleep(0.5)

    # Post-hook: simulates what happens after command (returncode 0 = success)
    wrapper.hook.post_command_hook("preflight-submit", returncode=0)
    print()
    print("✓ Post-command hook: transaction span closed")
    print("  - Duration recorded")
    print("  - Return code: 0 (success)")
    print()


def example_instrumented_noetic_phase():
    """Example: Instrument a noetic phase command"""
    wrapper = CLIHookWrapper()

    print("Example 2: Instrumented NOETIC phase command")
    print("=" * 60)

    cmd = "unknown-log --unknown 'Can OTEL work with empirica seat?'"
    print(f"Calling: empirica {cmd}")
    print()

    # Simulate noetic command
    wrapper.hook.pre_command_hook(cmd, stdin_data=None)
    print("✓ Pre-command hook: phase span started")
    print("  - Phase: noetic")
    print()

    time.sleep(0.3)
    print("🔄 Empirica executing: logging unknown to database...")
    time.sleep(0.3)

    wrapper.hook.post_command_hook(cmd, returncode=0)
    print()
    print("✓ Post-command hook: phase span closed")
    print("  - Duration recorded in metric: empirica.phase.duration.seconds")
    print()


def example_instrumented_check_gate():
    """Example: Instrument the CHECK gate"""
    wrapper = CLIHookWrapper()

    print("Example 3: Instrumented CHECK gate")
    print("=" * 60)

    check_payload = {
        "work_type": "code",
        "vectors": {
            "know": 0.90,
            "do": 0.85,
            "context": 0.92,
            "uncertainty": 0.12,
        }
    }

    payload_json = json.dumps(check_payload)

    cmd = "check-submit -"
    print(f"Calling: empirica {cmd}")
    print(f"Payload vectors: {check_payload['vectors']}")
    print()

    wrapper.hook.pre_command_hook(cmd, payload_json)
    print("✓ Pre-command hook: CHECK span started")
    print()

    # Simulate CHECK decision
    time.sleep(0.2)
    print("🔄 Empirica executing: validating evidence, checking calibration...")
    print("   Decision: PROCEED (noetic phase sufficient, moving to praxic)")
    time.sleep(0.2)

    # CHECK succeeded (returncode 0 = proceed)
    wrapper.hook.post_command_hook(cmd, returncode=0)
    print()
    print("✓ Post-command hook: CHECK decision recorded")
    print("  - Counter metric: empirica.CHECK.decisions.total")
    print("  - Decision attribute: 'proceed'")
    print()


def example_full_transaction_flow():
    """Example: Full transaction flow with all phases"""
    wrapper = CLIHookWrapper()

    print("Example 4: Full Transaction Flow (PREFLIGHT → noetic → CHECK → praxic → POSTFLIGHT)")
    print("=" * 90)

    phases = [
        ("preflight-submit", "preflight", 0.3),
        ("investigate", "noetic", 0.5),
        ("check-submit", "CHECK", 0.2),
        ("goal-create", "praxic", 0.4),
        ("postflight-submit", "postflight", 0.3),
    ]

    for cmd, phase, duration in phases:
        print(f"\n{'─' * 90}")
        print(f"Phase: {phase:12} | Command: empirica {cmd}")
        print(f"{'─' * 90}")

        wrapper.hook.pre_command_hook(cmd)
        print(f"  ✓ Phase span started: empirica.phase.duration.seconds")

        time.sleep(duration)
        print(f"  🔄 Executing ({duration}s)...")

        wrapper.hook.post_command_hook(cmd, returncode=0)
        print(f"  ✓ Phase span closed, metrics recorded")

    print(f"\n{'─' * 90}")
    print("✓ Full transaction complete with end-to-end tracing")
    print("  Traces exported to Jaeger (localhost:16686)")
    print("  Metrics exported to Prometheus (localhost:9090)")
    print(f"{'─' * 90}\n")


if __name__ == "__main__":
    print("\n" + "=" * 90)
    print("Phase 3.5.6 Phase 2: CLI Instrumentation Examples")
    print("=" * 90 + "\n")

    example_instrumented_preflight()
    print("\n")
    example_instrumented_noetic_phase()
    print("\n")
    example_instrumented_check_gate()
    print("\n")
    example_full_transaction_flow()

    print("=" * 90)
    print("Setup complete! CLI instrumentation is active.")
    print("=" * 90)
