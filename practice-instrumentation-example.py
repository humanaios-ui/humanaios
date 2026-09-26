#!/usr/bin/env python3
"""
Example: Instrumenting a Practice Service with Loki + Jaeger

This demonstrates how a practice (e.g., autonomy, mesh-support) would use
the empirica-loki-logging.py and empirica-jaeger-tracing.py modules to:
  1. Forward logs to Loki
  2. Propagate traces across service boundaries
  3. Measure empirica transaction phases
"""

import sys
import time
import json
from pathlib import Path

# Mock imports (in real environment, these would be installed)
# from empirica_loki_logging import setup_empirica_loki_logging, setup_acat_metrics_logging
# from empirica_jaeger_tracing import (
#     setup_jaeger_tracer,
#     traced_function,
#     trace_multi_practice_request,
#     EmpiricaPhaseTracer
# )


class MockLogger:
    """Mock logger for demonstration"""
    def info(self, msg, **kwargs):
        print(f"[INFO] {msg}", kwargs if kwargs else "")
    def debug(self, msg, **kwargs):
        print(f"[DEBUG] {msg}", kwargs if kwargs else "")
    def error(self, msg, **kwargs):
        print(f"[ERROR] {msg}", kwargs if kwargs else "")


class PracticeInstrumentationExample:
    """
    Example practice service instrumented with Loki + Jaeger

    Usage:
        practice = PracticeInstrumentationExample(
            practice_name="autonomy",
            loki_url="http://loki:3100",
            jaeger_service="autonomy"
        )
        practice.run_example()
    """

    def __init__(
        self,
        practice_name: str,
        loki_url: str = "http://localhost:3100",
        jaeger_service: str = None
    ):
        self.practice_name = practice_name
        self.loki_url = loki_url
        self.jaeger_service = jaeger_service or practice_name

        # In real implementation:
        # self.session_logger = setup_empirica_loki_logging(...)
        # self.acat_logger = setup_acat_metrics_logging(...)
        # self.tracer = setup_jaeger_tracer(self.jaeger_service)

        self.session_logger = MockLogger()
        self.acat_logger = MockLogger()
        self.tracer = None  # Mock tracer

    def run_empirica_transaction(
        self,
        session_id: str,
        phase: str,
        vectors: dict
    ):
        """
        Instrument a full empirica transaction phase

        Args:
            session_id: Unique session identifier
            phase: "PREFLIGHT" | "CHECK" | "POSTFLIGHT"
            vectors: epistemic vectors (know, do, context, etc.)
        """

        # Update logger context
        # self.session_logger.set_context(session_id, self.practice_name, phase)

        print(f"\n📊 {phase} Phase — {self.practice_name}")
        print("=" * 50)

        # Phase start
        self.session_logger.info(f"{phase} submitted", session_id=session_id)

        # Log vector state
        vectors_str = ", ".join([f"{k}={v:.2f}" for k, v in vectors.items()])
        self.session_logger.debug(f"Vectors: {vectors_str}")

        # Simulate phase work
        time.sleep(0.1)

        # Phase end
        self.session_logger.info(f"{phase} completed", session_id=session_id, duration_ms=125)

        return {
            "phase": phase,
            "session_id": session_id,
            "practice": self.practice_name,
            "vectors": vectors
        }

    def trace_multi_practice_request(
        self,
        source_practice: str,
        target_practice: str,
        request_type: str,
        payload: dict = None
    ):
        """
        Trace a request across practice boundaries

        Args:
            source_practice: Originating practice (e.g., "autonomy")
            target_practice: Recipient practice (e.g., "mesh-support")
            request_type: "collab_brief" | "proposal" | "etc"
            payload: Request data
        """

        print(f"\n🔗 Multi-Practice Request: {source_practice} → {target_practice}")
        print("=" * 50)

        self.session_logger.info(
            f"Sending {request_type} to {target_practice}",
            source=source_practice,
            target=target_practice
        )

        # Simulate request processing
        time.sleep(0.05)

        # Log result
        self.session_logger.info(
            f"{request_type} received by {target_practice}",
            status="accepted"
        )

        return {
            "source": source_practice,
            "target": target_practice,
            "type": request_type,
            "status": "accepted"
        }

    def log_acat_calibration(
        self,
        vector_name: str,
        predicted: float,
        actual: float,
        session_id: str
    ):
        """
        Log ACAT calibration metric

        Args:
            vector_name: Name of epistemic vector (e.g., "know", "uncertainty")
            predicted: AI's predicted value (0.0-1.0)
            actual: Actual measured value (0.0-1.0)
            session_id: Session identifier
        """

        print(f"\n📈 ACAT Calibration: {vector_name}")
        print("=" * 50)

        brier_error = (predicted - actual) ** 2

        self.acat_logger.info(
            f"ACAT check for {vector_name}",
            ai_id=self.practice_name,
            vector_name=vector_name,
            predicted=predicted,
            actual=actual,
            brier_error=brier_error,
            session_id=session_id
        )

        return {
            "vector": vector_name,
            "predicted": predicted,
            "actual": actual,
            "brier_error": brier_error
        }


def main():
    """Run instrumentation examples"""

    print("🚀 Practice Instrumentation Examples")
    print("=" * 60)
    print()

    # Example 1: Autonomy practice transaction
    print("Example 1: Autonomy Practice Transaction")
    print("-" * 60)

    autonomy = PracticeInstrumentationExample(
        practice_name="autonomy",
        loki_url="http://localhost:3100",
        jaeger_service="autonomy"
    )

    session_id = "sess_autonomy_001"

    # PREFLIGHT phase
    preflight_vectors = {
        "know": 0.75,
        "do": 0.90,
        "context": 0.70,
        "clarity": 0.65,
        "uncertainty": 0.20
    }
    autonomy.run_empirica_transaction(session_id, "PREFLIGHT", preflight_vectors)

    # CHECK phase
    check_vectors = {
        "know": 0.80,
        "do": 0.92,
        "context": 0.75,
        "clarity": 0.82,
        "uncertainty": 0.12
    }
    autonomy.run_empirica_transaction(session_id, "CHECK", check_vectors)

    # POSTFLIGHT phase
    postflight_vectors = {
        "know": 0.82,
        "do": 0.95,
        "context": 0.78,
        "completion": 0.90,
        "uncertainty": 0.08
    }
    autonomy.run_empirica_transaction(session_id, "POSTFLIGHT", postflight_vectors)

    # ACAT calibration check
    autonomy.log_acat_calibration(
        vector_name="know",
        predicted=0.82,
        actual=0.78,
        session_id=session_id
    )

    # Example 2: Multi-practice request (autonomy → mesh-support)
    print("\n\nExample 2: Multi-Practice Mesh Coordination")
    print("-" * 60)

    autonomy.trace_multi_practice_request(
        source_practice="autonomy",
        target_practice="mesh-support",
        request_type="collab_brief",
        payload={"question": "Is my Phase 3.5 understanding complete?"}
    )

    # Example 3: Mesh-support receives and responds
    print("\n\nExample 3: Mesh-Support Response")
    print("-" * 60)

    mesh_support = PracticeInstrumentationExample(
        practice_name="mesh-support",
        loki_url="http://localhost:3100",
        jaeger_service="mesh-support"
    )

    mesh_support.trace_multi_practice_request(
        source_practice="mesh-support",
        target_practice="autonomy",
        request_type="collab_response",
        payload={"answer": "Your understanding is on track. Need validation on Task 4."}
    )

    # Example 4: Summary
    print("\n\n📋 Summary: Instrumentation Output")
    print("=" * 60)
    print()
    print("✅ Logs forwarded to Loki:")
    print("   - PREFLIGHT/CHECK/POSTFLIGHT phase logs")
    print("   - Multi-practice request logs")
    print("   - Queries: {practice='autonomy'}, {job='empirica-sessions'}")
    print()
    print("✅ Traces sent to Jaeger:")
    print("   - Multi-practice request traces (autonomy→mesh-support)")
    print("   - Phase duration spans (PREFLIGHT→CHECK→POSTFLIGHT)")
    print("   - Trace IDs propagated across service boundaries")
    print()
    print("✅ Metrics logged to Loki (ACAT):")
    print("   - Vector calibration checks (know, do, context, etc.)")
    print("   - Brier score per transaction")
    print("   - Queries: {job='acat-grounding'}")
    print()
    print("🔍 View results:")
    print("   - Loki logs: http://localhost:3100/loki/ui/")
    print("   - Jaeger traces: http://localhost:16686/search?service=autonomy")
    print("   - Grafana dashboards: http://localhost:3000")
    print()


if __name__ == "__main__":
    main()
