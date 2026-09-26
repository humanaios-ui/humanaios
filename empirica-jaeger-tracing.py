#!/usr/bin/env python3
"""
Empirica → Jaeger Distributed Tracing Integration
Instruments gateway + practice services with OpenTelemetry
"""

from opentelemetry import trace, metrics
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.jaeger import JaegerPropagator
from opentelemetry.propagators.composite import CompositePropagator
from opentelemetry.sdk.resources import Resource
from opentelemetry.api.trace import Status, StatusCode
from opentelemetry.trace.propagation.tracecontext import TraceContextPropagator
import functools
from typing import Optional, Dict, Any, Callable
from contextlib import contextmanager

# Configure Jaeger exporter
def setup_jaeger_tracer(
    service_name: str,
    jaeger_agent_host: str = "localhost",
    jaeger_agent_port: int = 6831,
    sample_rate: float = 0.1
) -> trace.Tracer:
    """
    Initialize Jaeger tracer for a service

    Args:
        service_name: Name of the service (e.g., "gateway", "autonomy", "mesh-support")
        jaeger_agent_host: Jaeger agent hostname
        jaeger_agent_port: Jaeger agent UDP port (6831 for compact thrift)
        sample_rate: Sampling rate (0.0-1.0)

    Returns:
        Configured tracer instance
    """

    # Create Jaeger exporter
    jaeger_exporter = JaegerExporter(
        agent_host_name=jaeger_agent_host,
        agent_port=jaeger_agent_port,
    )

    # Create tracer provider with resource
    resource = Resource(attributes={
        "service.name": service_name,
        "service.version": "1.0.0",
        "service.instance.id": f"{service_name}-instance-001",
    })

    trace_provider = TracerProvider(resource=resource)
    trace_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))

    # Set global tracer provider
    trace.set_tracer_provider(trace_provider)

    # Configure trace propagators (W3C + Jaeger)
    set_global_textmap(CompositePropagator([
        TraceContextPropagator(),
        JaegerPropagator()
    ]))

    # Auto-instrument common libraries
    RequestsInstrumentor().instrument()
    LoggingInstrumentor().instrument()

    return trace.get_tracer(__name__)


def instrument_gateway(app):
    """
    Instrument Flask/HTTP gateway with Jaeger tracing

    Usage:
        app = Flask(__name__)
        tracer = setup_jaeger_tracer("gateway")
        instrument_gateway(app)
    """
    FlaskInstrumentor().instrument_app(app)


def instrument_database(engine):
    """
    Instrument SQLAlchemy database connections

    Usage:
        engine = create_engine("postgresql://...")
        tracer = setup_jaeger_tracer("autonomy")
        instrument_database(engine)
    """
    SQLAlchemyInstrumentor().instrument(
        engine=engine,
        service=trace.get_tracer(__name__).resource.attributes.get('service.name', 'unknown')
    )


def traced_function(tracer: trace.Tracer, operation_name: Optional[str] = None):
    """
    Decorator to trace a function call

    Usage:
        tracer = setup_jaeger_tracer("autonomy")

        @traced_function(tracer, operation_name="process_goal")
        def process_goal(goal_id: str):
            # Function is automatically traced
            pass
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with tracer.start_as_current_span(operation_name or func.__name__) as span:
                # Add function arguments as span attributes
                span.set_attribute("function.name", func.__name__)
                span.set_attribute("function.module", func.__module__)

                # Add kwargs as attributes
                for key, value in kwargs.items():
                    if isinstance(value, (str, int, float, bool)):
                        span.set_attribute(f"param.{key}", value)

                try:
                    result = func(*args, **kwargs)
                    span.set_attribute("result.success", True)
                    return result
                except Exception as e:
                    span.set_attribute("result.success", False)
                    span.set_attribute("error.type", type(e).__name__)
                    span.set_attribute("error.message", str(e))
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    raise

        return wrapper
    return decorator


def trace_multi_practice_request(
    tracer: trace.Tracer,
    source_practice: str,
    target_practice: str,
    request_type: str
):
    """
    Context manager for tracing multi-practice requests

    Usage:
        tracer = setup_jaeger_tracer("gateway")

        with trace_multi_practice_request(
            tracer,
            source_practice="autonomy",
            target_practice="mesh-support",
            request_type="collab_brief"
        ) as span:
            # Make cross-practice request
            result = send_to_mesh_support(...)
    """

    @contextmanager
    def _tracer():
        with tracer.start_as_current_span(f"{source_practice}→{target_practice}") as span:
            # Set multi-practice span attributes
            span.set_attribute("source_practice", source_practice)
            span.set_attribute("target_practice", target_practice)
            span.set_attribute("request_type", request_type)
            span.set_attribute("gateway.entry_point", True)

            try:
                yield span
                span.set_attribute("result", "success")
            except Exception as e:
                span.set_attribute("result", "error")
                span.set_attribute("error.message", str(e))
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise

    return _tracer()


class EmpiricaPhaseTracer:
    """Trace empirica transaction phases (PREFLIGHT → CHECK → POSTFLIGHT)"""

    def __init__(self, tracer: trace.Tracer, session_id: str, practice: str):
        self.tracer = tracer
        self.session_id = session_id
        self.practice = practice
        self.spans = {}

    def start_phase(self, phase_name: str):
        """Start a new phase span"""
        span = self.tracer.start_span(phase_name)
        span.set_attribute("session_id", self.session_id)
        span.set_attribute("practice", self.practice)
        span.set_attribute("phase", phase_name)
        span.set_attribute("timestamp", __import__('time').time_ns())
        self.spans[phase_name] = span
        return span

    def end_phase(self, phase_name: str, **attributes):
        """End phase span with results"""
        if phase_name in self.spans:
            span = self.spans[phase_name]
            for key, value in attributes.items():
                if isinstance(value, (str, int, float, bool)):
                    span.set_attribute(key, value)
            span.end()
            del self.spans[phase_name]

    def add_vector(self, phase_name: str, vector_name: str, value: float):
        """Add epistemic vector as span attribute"""
        if phase_name in self.spans:
            self.spans[phase_name].set_attribute(f"vector.{vector_name}", value)

    def add_goal(self, phase_name: str, goal_id: str, objective: str):
        """Add goal reference to phase span"""
        if phase_name in self.spans:
            self.spans[phase_name].set_attribute("goal_id", goal_id)
            self.spans[phase_name].set_attribute("goal_objective", objective)


# Example usage
if __name__ == "__main__":
    import time

    # Setup tracer for gateway
    tracer = setup_jaeger_tracer(
        service_name="gateway",
        jaeger_agent_host="localhost",
        jaeger_agent_port=6831
    )

    # Example 1: Trace a multi-practice request
    print("Example 1: Multi-practice request tracing")
    with trace_multi_practice_request(
        tracer,
        source_practice="autonomy",
        target_practice="mesh-support",
        request_type="collab_brief"
    ) as span:
        time.sleep(0.1)  # Simulate work
        span.set_attribute("response_time_ms", 125)
        print("  ✓ Multi-practice request traced")

    # Example 2: Trace empirica phases
    print("\nExample 2: Empirica phase tracing")
    phase_tracer = EmpiricaPhaseTracer(
        tracer=tracer,
        session_id="sess_demo_001",
        practice="autonomy"
    )

    # PREFLIGHT phase
    preflight_span = phase_tracer.start_phase("PREFLIGHT")
    phase_tracer.add_vector("PREFLIGHT", "know", 0.75)
    phase_tracer.add_vector("PREFLIGHT", "uncertainty", 0.20)
    time.sleep(0.1)
    phase_tracer.end_phase("PREFLIGHT", duration_ms=125, status="submitted")
    print("  ✓ PREFLIGHT phase traced")

    # CHECK phase
    check_span = phase_tracer.start_phase("CHECK")
    phase_tracer.add_vector("CHECK", "clarity", 0.80)
    time.sleep(0.05)
    phase_tracer.end_phase("CHECK", duration_ms=58, status="proceed")
    print("  ✓ CHECK phase traced")

    # POSTFLIGHT phase
    postflight_span = phase_tracer.start_phase("POSTFLIGHT")
    phase_tracer.add_vector("POSTFLIGHT", "completion", 0.95)
    phase_tracer.add_goal("POSTFLIGHT", "goal_abc123", "Phase 3.5 implementation")
    time.sleep(0.15)
    phase_tracer.end_phase("POSTFLIGHT", duration_ms=158, status="closed")
    print("  ✓ POSTFLIGHT phase traced")

    # Example 3: Decorated function tracing
    print("\nExample 3: Function decorator tracing")

    @traced_function(tracer, operation_name="process_goal")
    def process_goal(goal_id: str, priority: int = 1):
        time.sleep(0.05)
        return {"goal_id": goal_id, "processed": True}

    result = process_goal("goal_123", priority=2)
    print(f"  ✓ Function traced: {result}")

    print("\n✅ All traces sent to Jaeger")
    print("View at: http://localhost:16686/search?service=gateway")
