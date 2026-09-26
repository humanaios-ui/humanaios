# OpenTelemetry Instrumentation Guide
## Phase 3.4 — Empirica Foundation Observability

---

## SDK Setup

### Python OTEL SDK Installation
```bash
pip install opentelemetry-api opentelemetry-sdk
pip install opentelemetry-exporter-otlp
pip install opentelemetry-instrumentation-requests
pip install opentelemetry-instrumentation-urllib3
```

### Initialize Tracer & Exporter
```python
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

# Create OTLP exporter (points to collector at localhost:4317)
otlp_exporter = OTLPSpanExporter(
    endpoint="localhost:4317",
)

# Create tracer provider
resource = Resource(attributes={
    SERVICE_NAME: "empirica-foundation-evaluator",
    "environment": "production",
    "cluster": "foundation"
})
tracer_provider = TracerProvider(resource=resource)
tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

# Set global tracer provider
trace.set_tracer_provider(tracer_provider)
tracer = trace.get_tracer("empirica.foundation")
```

---

## Span Definitions

### Span 1: PREFLIGHT Transaction
```python
with tracer.start_as_current_span("preflight") as span:
    span.set_attribute("transaction_id", transaction_id)
    span.set_attribute("session_id", session_id)
    span.set_attribute("work_type", "code")
    span.set_attribute("vector_count", 13)
    # PREFLIGHT logic
```

### Span 2: Noetic Work (Investigation)
```python
with tracer.start_as_current_span("noetic_investigation") as span:
    span.set_attribute("query_type", "mailbox_poll")
    span.set_attribute("item_count", 20)
    span.set_attribute("grounding_type", "search")
    # Investigation logic
```

### Span 3: Praxic Work (Execution)
```python
with tracer.start_as_current_span("praxic_execution") as span:
    span.set_attribute("action_type", "mailbox_reply")
    span.set_attribute("target_count", 7)
    span.set_attribute("reply_count", 20)
    # Execution logic
```

### Span 4: Artifact Logging
```python
with tracer.start_as_current_span("log_artifact") as span:
    span.set_attribute("artifact_type", "finding")
    span.set_attribute("confidence", 0.85)
    span.set_attribute("impact", 0.88)
    span.set_attribute("epistemic_source", "search")
    # Log artifact
```

### Span 5: CHECK Gate (Noetic→Praxic)
```python
with tracer.start_as_current_span("check_gate") as span:
    span.set_attribute("claims_declared", claim_count)
    span.set_attribute("claims_grounded", grounded_count)
    span.set_attribute("verdict", "proceed")
    # CHECK logic
```

### Span 6: POSTFLIGHT Closure
```python
with tracer.start_as_current_span("postflight") as span:
    span.set_attribute("transaction_id", transaction_id)
    span.set_attribute("confidence", 0.88)
    span.set_attribute("vector_delta_count", 13)
    span.set_attribute("artifacts_logged", 5)
    # POSTFLIGHT logic
```

---

## Span Attributes (Standard Set)

Every span MUST include:
```
transaction_id     # UUID from PREFLIGHT
session_id         # Session identifier
practice_id        # Emitting practice (evaluator, mesh-support, etc.)
phase              # "noetic" or "praxic"
timestamp          # ISO8601
```

Span-specific attributes:
- **PREFLIGHT**: work_type, vector_count, session_id
- **Noetic**: query_type, item_count, grounding_type
- **Praxic**: action_type, target_count, result
- **Artifacts**: type, confidence, impact, epistemic_source
- **CHECK**: claims_declared, claims_grounded, verdict
- **POSTFLIGHT**: transaction_id, confidence, artifacts_logged

---

## Pilot Practices Instrumentation

### Evaluator (empirica-foundation-evaluator)
✅ Full instrumentation: all span types above

### Mesh-Support (empirica-mesh-support)
- PREFLIGHT/POSTFLIGHT spans
- Noetic: mailbox-poll investigation spans
- Praxic: proposal-reply execution spans
- Artifacts: finding-log, decision-log

### Autonomy (empirica-autonomy)
- PREFLIGHT/POSTFLIGHT spans
- Praxic: phase-execution action spans
- Artifacts: blocker-log spans

### Resource-Miner (empirica-resource-miner)
- PREFLIGHT/POSTFLIGHT spans
- Noetic: resource-discovery investigation
- Artifact: finding-log (resource opportunities)

---

## Baseline Measurement Collection

### Cold-Start Profile
Run this trace 10+ times:
1. Initialize evaluator (PREFLIGHT)
2. Poll mailbox (noetic span)
3. Log findings (artifact spans)
4. Send reply (praxic span)
5. Close transaction (POSTFLIGHT)

**Measure:** Latency from span 1→5, span count, error count

### Warm-Start Profile
Run this trace 20+ times (post-initialization):
1. PREFLIGHT (2nd+ transaction)
2. Noetic work (faster, cache warm)
3. Praxic work
4. POSTFLIGHT

**Measure:** Latency stability, vector delta distributions

---

## Validation Checklist

- [ ] OTEL collector receiving spans (check collector logs)
- [ ] Spans appearing in Jaeger UI within 5 seconds
- [ ] All required attributes present on every span
- [ ] Trace latency < 100ms for evaluator full cycle
- [ ] Sampling at 100% in Phase 3.4
- [ ] Cold-start baseline: 10+ samples collected
- [ ] Warm-start baseline: 20+ samples collected
- [ ] Latency distribution: normal (not bimodal)

