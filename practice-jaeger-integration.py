#!/usr/bin/env python3
"""
Practice Service Integration: Wire Jaeger tracing
Tasks 6-10: Deploy instrumentation to gateway + practice services

This module shows how to integrate Jaeger tracing into a practice service
(e.g., autonomy, mesh-support) with minimal code changes.

Usage:
    from practice_jaeger_integration import initialize_tracing, trace_transaction

    # In practice service startup
    tracer = initialize_tracing("autonomy")

    # In transaction handler
    with trace_transaction(tracer, session_id, "PREFLIGHT") as tracker:
        tracker.set_vector("know", 0.75)
        # ... do work ...
        tracker.end_phase()
"""

import os
import sys
from typing import Optional, Dict, Any
from contextlib import contextmanager

# Import instrumentation modules
try:
    from empirica_jaeger_tracing import (
        setup_jaeger_tracer,
        trace_multi_practice_request,
        EmpiricaPhaseTracer,
        traced_function
    )
    JAEGER_AVAILABLE = True
except ImportError:
    JAEGER_AVAILABLE = False
    print("⚠ Warning: empirica-jaeger-tracing not found. Tracing disabled.")


class PracticeTracingConfig:
    """Configuration for practice tracing"""

    def __init__(
        self,
        service_name: str,
        jaeger_host: str = "localhost",
        jaeger_port: int = 6831,
        sample_rate: float = 0.1
    ):
        self.service_name = service_name
        self.jaeger_host = jaeger_host
        self.jaeger_port = jaeger_port
        self.sample_rate = sample_rate

    @classmethod
    def from_env(cls) -> 'PracticeTracingConfig':
        """Load config from environment variables"""
        return cls(
            service_name=os.getenv('PRACTICE_NAME', 'unknown'),
            jaeger_host=os.getenv('JAEGER_HOST', 'localhost'),
            jaeger_port=int(os.getenv('JAEGER_PORT', 6831)),
            sample_rate=float(os.getenv('TRACE_SAMPLE_RATE', 0.1))
        )


def initialize_tracing(
    service_name: str,
    jaeger_host: str = "localhost",
    jaeger_port: int = 6831,
    sample_rate: float = 0.1
):
    """
    Initialize Jaeger tracing for a practice service

    Args:
        service_name: Name of the practice (e.g., "autonomy", "mesh-support")
        jaeger_host: Jaeger agent hostname
        jaeger_port: Jaeger agent port
        sample_rate: Sampling rate (0.0-1.0)

    Returns:
        Configured tracer instance

    Example:
        tracer = initialize_tracing("autonomy")
    """

    if not JAEGER_AVAILABLE:
        return None

    print(f"🔍 Initializing Jaeger tracing for {service_name}")
    print(f"   Jaeger: {jaeger_host}:{jaeger_port}")
    print(f"   Sampling: {sample_rate * 100:.0f}%")

    tracer = setup_jaeger_tracer(
        service_name=service_name,
        jaeger_agent_host=jaeger_host,
        jaeger_agent_port=jaeger_port,
        sample_rate=sample_rate
    )

    return tracer


@contextmanager
def trace_transaction(tracer, session_id: str, phase: str, practice: str = "unknown"):
    """
    Context manager for tracing empirica transaction phases

    Args:
        tracer: Jaeger tracer instance
        session_id: Unique session identifier
        phase: "PREFLIGHT" | "CHECK" | "POSTFLIGHT"
        practice: Practice name (for spans)

    Example:
        with trace_transaction(tracer, session_id, "PREFLIGHT") as tracker:
            tracker.set_vector("know", 0.75)
            tracker.add_goal("goal_abc", "Phase 3.5 implementation")
            # ... do work ...
            tracker.end_phase(duration_ms=125, status="submitted")

    Yields:
        TransactionTracker: Phase tracking helper
    """

    if not tracer:
        class NoOpTracker:
            def set_vector(self, name, value): pass
            def add_goal(self, goal_id, objective): pass
            def end_phase(self, **attrs): pass

        yield NoOpTracker()
        return

    tracker = TransactionTracker(tracer, session_id, practice, phase)
    try:
        yield tracker
    finally:
        tracker.cleanup()


class TransactionTracker:
    """Helper for tracking empirica phases in Jaeger"""

    def __init__(self, tracer, session_id: str, practice: str, phase: str):
        self.tracer = tracer
        self.session_id = session_id
        self.practice = practice
        self.phase = phase
        self.phase_tracer = EmpiricaPhaseTracer(tracer, session_id, practice)
        self.span = self.phase_tracer.start_phase(phase)

    def set_vector(self, name: str, value: float):
        """Record an epistemic vector"""
        self.phase_tracer.add_vector(self.phase, name, value)

    def add_goal(self, goal_id: str, objective: str):
        """Record goal reference"""
        self.phase_tracer.add_goal(self.phase, goal_id, objective)

    def end_phase(self, **attributes):
        """End phase with result attributes"""
        self.phase_tracer.end_phase(self.phase, **attributes)

    def cleanup(self):
        """Ensure span is closed"""
        if self.phase in self.phase_tracer.spans:
            self.phase_tracer.end_phase(self.phase)


def trace_multi_practice_call(tracer, target_practice: str, request_type: str = "collab"):
    """
    Context manager for tracing calls to other practices

    Args:
        tracer: Jaeger tracer instance
        target_practice: Name of target practice
        request_type: Type of request (e.g., "collab_brief", "proposal")

    Example:
        with trace_multi_practice_call(tracer, "mesh-support", "collab_brief") as span:
            response = send_to_mesh_support(payload)
            span.set_attribute("response_code", response.status_code)

    Yields:
        Active span
    """

    if not tracer:
        class NoOpSpan:
            def set_attribute(self, key, value): pass
            def __enter__(self): return self
            def __exit__(self, *args): pass

        return NoOpSpan()

    # Get source practice from environment
    source_practice = os.getenv('PRACTICE_NAME', 'unknown')

    return trace_multi_practice_request(
        tracer,
        source_practice=source_practice,
        target_practice=target_practice,
        request_type=request_type
    )


# Example Flask integration
def example_flask_integration():
    """
    Example: Integrate Jaeger into a Flask practice service

    Usage:
        from practice_jaeger_integration import example_flask_integration
        app = example_flask_integration()
        app.run(port=5000)
    """

    try:
        from flask import Flask, request, jsonify
    except ImportError:
        print("⚠ Flask not installed. Skipping example.")
        return None

    app = Flask(__name__)

    # Initialize tracing
    tracer = initialize_tracing("autonomy")

    @app.route("/transaction", methods=["POST"])
    def handle_transaction():
        """Handle empirica transaction with tracing"""

        payload = request.json
        session_id = payload.get("session_id", "unknown")
        phase = payload.get("phase", "PREFLIGHT")

        # Trace the transaction
        with trace_transaction(tracer, session_id, phase, "autonomy") as tracker:
            # Simulate work
            tracker.set_vector("know", payload.get("vectors", {}).get("know", 0.75))
            tracker.set_vector("do", payload.get("vectors", {}).get("do", 0.90))

            # Simulate goal processing
            goals = payload.get("goals", [])
            if goals:
                tracker.add_goal(goals[0]["id"], goals[0]["objective"])

            # Return result
            result = {
                "session_id": session_id,
                "phase": phase,
                "status": "completed"
            }

            tracker.end_phase(duration_ms=125, status="completed")

            return jsonify(result)

    @app.route("/collab/<target>", methods=["POST"])
    def send_collab(target):
        """Send collab request to another practice with trace propagation"""

        session_id = request.json.get("session_id", "unknown")

        with trace_multi_practice_call(tracer, target, "collab_brief") as span:
            # In real implementation, would call other practice's API
            # headers = extract_trace_context(tracer)
            # response = requests.post(f"http://{target}:5000/receive", json=payload, headers=headers)

            result = {
                "source": "autonomy",
                "target": target,
                "status": "sent",
                "trace_id": "auto"  # Would be actual trace ID from span
            }

            return jsonify(result)

    return app


# Example: Main integration flow
if __name__ == "__main__":
    import time

    print("🚀 Practice Jaeger Integration Example")
    print("=" * 60)
    print()

    # Initialize tracing
    tracer = initialize_tracing("autonomy")
    print()

    # Simulate PREFLIGHT phase
    print("📊 PREFLIGHT Phase")
    with trace_transaction(tracer, "sess_demo_001", "PREFLIGHT", "autonomy") as tracker:
        tracker.set_vector("know", 0.75)
        tracker.set_vector("uncertainty", 0.20)
        time.sleep(0.05)
        tracker.end_phase(duration_ms=125, status="submitted")

    print("  ✓ PREFLIGHT traced")
    print()

    # Simulate CHECK phase
    print("📊 CHECK Phase")
    with trace_transaction(tracer, "sess_demo_001", "CHECK", "autonomy") as tracker:
        tracker.set_vector("clarity", 0.80)
        time.sleep(0.03)
        tracker.end_phase(duration_ms=58, status="proceed")

    print("  ✓ CHECK traced")
    print()

    # Simulate multi-practice call
    print("🔗 Multi-Practice Call")
    with trace_multi_practice_call(tracer, "mesh-support", "collab_brief") as span:
        time.sleep(0.02)
        span.set_attribute("response_code", 200)

    print("  ✓ Cross-practice call traced")
    print()

    # Simulate POSTFLIGHT phase
    print("📊 POSTFLIGHT Phase")
    with trace_transaction(tracer, "sess_demo_001", "POSTFLIGHT", "autonomy") as tracker:
        tracker.set_vector("completion", 0.95)
        tracker.add_goal("goal_abc123", "Phase 3.5 implementation")
        time.sleep(0.07)
        tracker.end_phase(duration_ms=158, status="closed")

    print("  ✓ POSTFLIGHT traced")
    print()

    print("=" * 60)
    print("✅ All phases traced")
    print("View traces at: http://localhost:16686/search?service=autonomy")
    print()
