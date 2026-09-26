#!/usr/bin/env python3
"""
OpenTelemetry observability configuration for Phase 3.3
"""

import os
import logging
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

logger = logging.getLogger('observability')


def setup_tracing():
    """Initialize OpenTelemetry tracing with OTLP exporter"""
    # Get OTLP endpoint (default to localhost:4317 for gRPC)
    otlp_endpoint = os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT', 'http://localhost:4317')

    # Create resource
    resource = Resource.create({
        "service.name": "empirica-task-service",
        "service.version": "3.3",
        "deployment.environment": "phase-3.3"
    })

    # Create OTLP exporter
    try:
        otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
        trace_provider = TracerProvider(resource=resource)
        trace_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
        trace.set_tracer_provider(trace_provider)
        logger.info(f"✅ OpenTelemetry tracing initialized (exporter: {otlp_endpoint})")
    except Exception as e:
        logger.warning(f"⚠️ Failed to initialize OpenTelemetry: {e}")
        logger.info("Tracing will use default no-op tracer")
        trace.set_tracer_provider(TracerProvider(resource=resource))


def get_tracer(name: str):
    """Get a tracer instance"""
    return trace.get_tracer(name)


def setup_metrics():
    """Initialize OpenTelemetry metrics with OTLP exporter"""
    otlp_endpoint = os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT', 'http://localhost:4317')

    resource = Resource.create({
        "service.name": "empirica-task-service",
        "service.version": "3.3",
        "deployment.environment": "phase-3.3"
    })

    try:
        otlp_metric_exporter = OTLPMetricExporter(endpoint=otlp_endpoint)
        metric_reader = PeriodicExportingMetricReader(otlp_metric_exporter)
        meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
        metrics.set_meter_provider(meter_provider)
        logger.info(f"✅ OpenTelemetry metrics initialized (exporter: {otlp_endpoint})")
    except Exception as e:
        logger.warning(f"⚠️ Failed to initialize OpenTelemetry metrics: {e}")
        metrics.set_meter_provider(MeterProvider(resource=resource))


def get_meter(name: str):
    """Get a meter instance"""
    return metrics.get_meter(name)


# Initialize both tracing and metrics on module import
setup_tracing()
setup_metrics()
