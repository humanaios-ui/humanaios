#!/usr/bin/env python3
"""
OTEL Instrumentation for Empirica Framework
Phase 3.6: Observable Claude Instrumentation

Emits distributed traces and metrics for:
- Transaction lifecycle (PREFLIGHT -> noetic -> CHECK -> praxic -> POSTFLIGHT)
- 13-vector epistemic state (gauges per vector)
- Artifact production (counters per artifact type)
- Phase durations (histograms for noetic/praxic time)

Connects to OTEL Collector at localhost:4317 (gRPC)
Traces exported to Jaeger, metrics exported to Prometheus
"""

from typing import Dict, Optional, Any, ContextManager
from contextlib import contextmanager
import os
from time import time

try:
    from opentelemetry import trace, metrics
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
    from opentelemetry.sdk.resources import Resource
    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False


class OTELInstrumentation:
    """OTEL instrumentation for empirica lifecycle with graceful degradation"""

    def __init__(self, service_name: str = "empirica-foundation-evaluator",
                 otel_endpoint: str = "localhost:4317", enabled: bool = True):
        """Initialize OTEL tracer and meter (gracefully degrades if OTEL unavailable)"""

        self.enabled = enabled and OTEL_AVAILABLE
        self.otel_endpoint = otel_endpoint
        self.service_name = service_name
        self.tracer = None
        self.meter = None
        self.vector_gauges: Dict[str, Any] = {}
        self.phase_histograms: Dict[str, Any] = {}
        self._current_transaction_id = None
        self._root_span = None
        self._transaction_start_time = None

        if not self.enabled:
            return

        try:
            resource = Resource.create({
                "service.name": service_name,
                "service.version": "3.6",
                "deployment.environment": "phase-3.6"
            })

            # Tracer setup
            trace_exporter = OTLPSpanExporter(endpoint=otel_endpoint, insecure=True)
            trace_provider = TracerProvider(resource=resource)
            trace_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
            trace.set_tracer_provider(trace_provider)
            self.tracer = trace.get_tracer(__name__, version="3.6")

            # Meter setup
            metric_exporter = OTLPMetricExporter(endpoint=otel_endpoint, insecure=True)
            metric_reader = PeriodicExportingMetricReader(metric_exporter, interval_millis=5000)
            meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
            metrics.set_meter_provider(meter_provider)
            self.meter = metrics.get_meter(__name__, version="3.6")

            # Pre-create gauge instruments for 13 vectors
            self.vector_gauges = {
                "know": self.meter.create_gauge("empirica_know_gauge", unit="1", description="Domain understanding"),
                "do": self.meter.create_gauge("empirica_do_gauge", unit="1", description="Execution ability"),
                "context": self.meter.create_gauge("empirica_context_gauge", unit="1", description="State awareness"),
                "clarity": self.meter.create_gauge("empirica_clarity_gauge", unit="1", description="Path clarity"),
                "coherence": self.meter.create_gauge("empirica_coherence_gauge", unit="1", description="Internal consistency"),
                "signal": self.meter.create_gauge("empirica_signal_gauge", unit="1", description="Information quality"),
                "density": self.meter.create_gauge("empirica_density_gauge", unit="1", description="Knowledge density"),
                "state": self.meter.create_gauge("empirica_state_gauge", unit="1", description="System state awareness"),
                "change": self.meter.create_gauge("empirica_change_gauge", unit="1", description="Amount of change"),
                "completion": self.meter.create_gauge("empirica_completion_gauge", unit="1", description="Phase progress"),
                "impact": self.meter.create_gauge("empirica_impact_gauge", unit="1", description="Work significance"),
                "engagement": self.meter.create_gauge("empirica_engagement_gauge", unit="1", description="Engagement level"),
                "uncertainty": self.meter.create_gauge("empirica_uncertainty_gauge", unit="1", description="Uncertainty"),
            }

            # Pre-create counter instruments
            self.artifact_counter = self.meter.create_counter(
                "empirica_artifacts_logged_total",
                unit="1",
                description="Total artifacts logged"
            )
            self.commit_counter = self.meter.create_counter(
                "empirica_commits_total",
                unit="1",
                description="Total commits created"
            )

            # Pre-create histogram instruments
            self.transaction_duration = self.meter.create_histogram(
                "empirica_transaction_duration_seconds",
                unit="s",
                description="Transaction duration in seconds"
            )
            self.phase_histograms["noetic"] = self.meter.create_histogram(
                "empirica_noetic_duration_seconds",
                unit="s",
                description="Noetic phase duration"
            )
            self.phase_histograms["praxic"] = self.meter.create_histogram(
                "empirica_praxic_duration_seconds",
                unit="s",
                description="Praxic phase duration"
            )

        except Exception as e:
            self.enabled = False

    def start_transaction(self, transaction_id: str, goal_id: str, work_type: str):
        """Open transaction span"""
        if not self.enabled:
            return None

        self._current_transaction_id = transaction_id
        self._transaction_start_time = time()
        self._root_span = self.tracer.start_span(
            "empirica:transaction",
            attributes={
                "transaction_id": transaction_id,
                "goal_id": goal_id,
                "practice_ai_id": self.service_name,
                "work_type": work_type,
                "status": "open"
            }
        )
        return self._root_span

    @contextmanager
    def phase_span(self, phase_name: str, attributes: Optional[Dict[str, Any]] = None):
        """Context manager for phase spans (noetic, praxic, check, postflight)"""
        if not self.enabled:
            yield None
            return

        phase_start = time()
        attrs = {"phase": phase_name, **(attributes or {})}
        span = self.tracer.start_span(f"empirica:{phase_name}", attributes=attrs)
        try:
            yield span
        finally:
            span.end()
            phase_duration = time() - phase_start
            if phase_name in self.phase_histograms:
                labels = {"transaction_id": self._current_transaction_id or "unknown", "practice": self.service_name}
                self.phase_histograms[phase_name].record(phase_duration, labels)

    @contextmanager
    def operation_span(self, operation_name: str, attributes: Optional[Dict[str, Any]] = None):
        """Context manager for operation spans (read, write, grep, commit, etc.)"""
        if not self.enabled:
            yield None
            return

        attrs = {"operation": operation_name, **(attributes or {})}
        span = self.tracer.start_span(f"empirica:op_{operation_name}", attributes=attrs)
        try:
            yield span
        finally:
            span.end()

    def emit_vector_metrics(self, vectors: Dict[str, float]) -> None:
        """Emit 13-vector gauge metrics"""
        if not self.enabled or not self.meter:
            return

        labels = {"transaction_id": self._current_transaction_id or "unknown", "practice": self.service_name}
        for vector_name, value in vectors.items():
            if vector_name in self.vector_gauges:
                try:
                    self.vector_gauges[vector_name].observe(value, labels)
                except Exception:
                    pass

    def emit_artifact_metric(self, artifact_type: str, count: int = 1) -> None:
        """Emit counter for artifacts logged"""
        if not self.enabled or not self.artifact_counter:
            return

        try:
            self.artifact_counter.add(count, {"artifact_type": artifact_type, "practice": self.service_name})
        except Exception:
            pass

    def emit_commit_metric(self, count: int = 1) -> None:
        """Emit counter for commits"""
        if not self.enabled or not self.commit_counter:
            return

        try:
            self.commit_counter.add(count, {"practice": self.service_name})
        except Exception:
            pass

    def close_transaction(self, commit_sha: Optional[str] = None, artifacts_count: int = 0) -> None:
        """Close transaction span and emit final metrics"""
        if not self.enabled:
            return

        if self._root_span:
            self._root_span.set_attribute("status", "closed")
            if commit_sha:
                self._root_span.set_attribute("commit_sha", commit_sha)
            self._root_span.set_attribute("artifacts_logged", artifacts_count)
            self._root_span.end()
            self._root_span = None

        # Emit transaction duration histogram
        if self._transaction_start_time and self.transaction_duration:
            duration = time() - self._transaction_start_time
            try:
                labels = {"transaction_id": self._current_transaction_id or "unknown", "practice": self.service_name}
                self.transaction_duration.record(duration, labels)
            except Exception:
                pass

        self._current_transaction_id = None
        self._transaction_start_time = None


# Global singleton
_instrumentation = None


def initialize_instrumentation(service_name: str = "empirica-foundation-evaluator",
                               otel_endpoint: str = "localhost:4317",
                               enabled: bool = True) -> OTELInstrumentation:
    """Initialize global instrumentation singleton"""
    global _instrumentation
    if _instrumentation is None:
        _instrumentation = OTELInstrumentation(service_name, otel_endpoint, enabled)
    return _instrumentation


def get_instrumentation() -> OTELInstrumentation:
    """Get global instrumentation singleton"""
    global _instrumentation
    if _instrumentation is None:
        _instrumentation = OTELInstrumentation()
    return _instrumentation
