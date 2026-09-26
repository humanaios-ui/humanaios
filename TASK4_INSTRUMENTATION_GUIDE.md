# Task 4: Instrumentation Guide

## Overview

Task 4 instruments empirica services to forward logs (→ Loki) and traces (→ Jaeger), enabling real-time observability of distributed transactions across practices.

**Status:** Task 4 designs and integration code complete. Ready for deployment + validation.

---

## Files

| File | Purpose | Task |
|------|---------|------|
| `empirica-loki-logging.py` | Python logging handlers for Loki integration | 3.5.2-4 |
| `empirica-jaeger-tracing.py` | OpenTelemetry instrumentation + Jaeger exporters | 3.5.1-4 |
| `practice-instrumentation-example.py` | Example practice instrumentation (mock) | 3.5-demo |
| `TASK4_INSTRUMENTATION_GUIDE.md` | This file | 3.5-docs |

---

## Task 4.1: Loki Log Forwarding (3.5.2)

### Overview

Wire empirica session logs, practice stdout, and ACAT metrics → Loki.

### Implementation

#### 1. Wire Empirica Session Logs

**Filename:** `empirica-loki-logging.py` → `EmpirikaLokiHandler`

**What it does:**
- Python logging handler that sends empirica logs to Loki via HTTP API
- Batches logs (default 10) before pushing
- Extracts context: session_id, practice, phase
- Formats as JSON with timestamps (nanosecond precision)

**Integration points:**
- `empirica preflight-submit` → PREFLIGHT phase log
- `empirica check-submit` → CHECK phase log
- `empirica postflight-submit` → POSTFLIGHT phase log
- Goal creation/completion logs
- Vector updates

**Usage:**

```python
from empirica_loki_logging import setup_empirica_loki_logging

# Configure at session start
logger = setup_empirica_loki_logging(
    session_id="sess_abc123",
    practice="autonomy",
    phase="PREFLIGHT",
    loki_url="http://loki:3100"  # or k8s service http://loki:3100
)

# Log phase start
logger.info("PREFLIGHT submitted")

# Log vector state
logger.debug(f"Vectors: know=0.75, uncertainty=0.20")

# Logs are buffered (10 entries) then pushed to Loki
```

**Loki labels (visible in queries):**
- `job`: "empirica-sessions"
- `practice`: autonomy | mesh-support | outreach | website | humanaios
- `phase`: PREFLIGHT | CHECK | POSTFLIGHT
- `session_id`: unique session identifier

**Query in Loki UI:**
```
{job="empirica-sessions", practice="autonomy", phase="POSTFLIGHT"}
```

#### 2. Wire Practice Stdout

**Configuration:** `promtail-local-config.yaml` → `practice-stdout` job

**What it does:**
- Promtail scrapes practice process stdout (log files)
- Regex-parses lines into: timestamp, level, practice, message
- Forwards to Loki with labels

**Setup:**

1. Practice logs to file: `/var/log/practice-<name>.log`
   ```bash
   # In practice startup
   exec > /var/log/practice-autonomy.log 2>&1
   ```

2. Promtail config (included in K8s deployment):
   ```yaml
   - job_name: practice-stdout
     static_configs:
       - targets: [localhost]
         labels:
           job: practice-stdout
           __path__: /var/log/practice-*.log
     pipeline_stages:
       - regex:
           expression: '(?P<timestamp>\S+)\s+(?P<level>\w+)\s+(?P<practice>\w+)\s+(?P<message>.*)'
   ```

3. Logs appear in Loki with labels: practice, level, job

**Loki query:**
```
{job="practice-stdout", practice="autonomy", level="error"}
```

#### 3. Wire ACAT Metrics

**Filename:** `empirica-loki-logging.py` → `AcatMetricsLokiHandler`

**What it does:**
- Separate logger for ACAT calibration checks
- Logs predicted vs actual vector values
- Calculates Brier error per vector

**Usage:**

```python
from empirica_loki_logging import setup_acat_metrics_logging

acat_logger = setup_acat_metrics_logging(loki_url="http://loki:3100")

# After POSTFLIGHT, log calibration check
acat_logger.info("ACAT calibration check", extra={
    'ai_id': 'autonomy',
    'vector_name': 'know',
    'predicted': 0.82,
    'actual': 0.78,
    'brier_error': 0.0016,
    'phase': 'POSTFLIGHT',
    'session_id': 'sess_abc123'
})
```

**Loki labels:**
- `job`: "acat-grounding"
- `source`: "empirica"

**Loki query:**
```
{job="acat-grounding", source="empirica"}
| json
| know_predicted > 0.70
```

---

## Task 4.2: Jaeger Trace Instrumentation (3.5.1)

### Overview

Wire gateway + practice services with OpenTelemetry → Jaeger trace collection.

### Implementation

#### 1. Setup Jaeger Tracer

**Filename:** `empirica-jaeger-tracing.py` → `setup_jaeger_tracer()`

**What it does:**
- Initializes OpenTelemetry SDK with Jaeger exporter
- Configures span processor + resource attributes
- Auto-instruments HTTP libraries (requests, Flask)
- Sets up trace propagators (W3C Trace Context + Jaeger)

**Usage (gateway service):**

```python
from empirica_jaeger_tracing import (
    setup_jaeger_tracer,
    instrument_gateway,
    trace_multi_practice_request
)
from flask import Flask

# Initialize tracer for gateway
app = Flask(__name__)
tracer = setup_jaeger_tracer(
    service_name="gateway",
    jaeger_agent_host="jaeger",  # k8s service name
    jaeger_agent_port=6831,
    sample_rate=0.5  # 50% sampling for gateway
)

# Auto-instrument Flask routes
instrument_gateway(app)

# Trace multi-practice requests
@app.route("/request/<target_practice>", methods=["POST"])
def send_request(target_practice):
    source = request.headers.get("X-Source-Practice", "unknown")
    
    with trace_multi_practice_request(
        tracer,
        source_practice=source,
        target_practice=target_practice,
        request_type="collab_brief"
    ) as span:
        # Span automatically logs:
        # - source_practice, target_practice, request_type
        # - Success/error status
        # - Timing
        
        result = send_to_practice(target_practice)
        span.set_attribute("response_time_ms", result.elapsed.total_seconds() * 1000)
        return result
```

#### 2. Instrument Practice Services

**Usage (autonomy practice):**

```python
from empirica_jaeger_tracing import (
    setup_jaeger_tracer,
    EmpiricaPhaseTracer,
    traced_function,
    instrument_database
)

# Initialize tracer for practice
tracer = setup_jaeger_tracer(
    service_name="autonomy",
    jaeger_agent_host="jaeger",
    jaeger_agent_port=6831,
    sample_rate=0.1  # 10% baseline sampling
)

# Instrument database
from sqlalchemy import create_engine
engine = create_engine("postgresql://...")
instrument_database(engine)

# Trace empirica phases
def run_transaction(session_id: str):
    phase_tracer = EmpiricaPhaseTracer(tracer, session_id, "autonomy")
    
    # PREFLIGHT phase
    preflight = phase_tracer.start_phase("PREFLIGHT")
    # ... do work ...
    phase_tracer.add_vector("PREFLIGHT", "know", 0.75)
    phase_tracer.add_vector("PREFLIGHT", "uncertainty", 0.20)
    phase_tracer.end_phase("PREFLIGHT", duration_ms=125, status="submitted")
    
    # CHECK phase
    check = phase_tracer.start_phase("CHECK")
    # ... do work ...
    phase_tracer.add_vector("CHECK", "clarity", 0.80)
    phase_tracer.end_phase("CHECK", duration_ms=58, status="proceed")
    
    # POSTFLIGHT phase
    postflight = phase_tracer.start_phase("POSTFLIGHT")
    # ... do work ...
    phase_tracer.add_vector("POSTFLIGHT", "completion", 0.95)
    phase_tracer.add_goal("POSTFLIGHT", goal_id, objective)
    phase_tracer.end_phase("POSTFLIGHT", duration_ms=158, status="closed")

# Trace individual functions
@traced_function(tracer, operation_name="process_goal")
def process_goal(goal_id: str, priority: int = 1):
    # Automatically traced with:
    # - function name + module
    # - parameters as span attributes
    # - exception handling + error status
    return {"goal_id": goal_id, "processed": True}
```

#### 3. Trace Cross-Practice Flows

**Multi-practice trace hierarchy:**

```
Root span: gateway (entry point)
  ├─ source_practice: autonomy
  ├─ target_practice: mesh-support
  └─ request_type: collab_brief
      ├─ Child: PREFLIGHT (autonomy)
      ├─ Child: CHECK (autonomy)
      ├─ Child: HTTP request to mesh-support
      │   ├─ Child: PREFLIGHT (mesh-support)
      │   ├─ Child: CHECK (mesh-support)
      │   └─ Child: POSTFLIGHT (mesh-support)
      └─ Child: POSTFLIGHT (autonomy)
```

**Implementation (gateway):**

```python
# When forwarding request to practice, propagate trace context
@app.route("/request/<target_practice>", methods=["POST"])
def send_request(target_practice):
    with trace_multi_practice_request(
        tracer,
        source_practice="autonomy",
        target_practice=target_practice,
        request_type="collab_brief"
    ) as span:
        # Get current trace context
        headers = {}
        trace.get_current_span().is_recording()
        propagator = trace.propagate()
        
        # Forward to target practice with trace headers
        response = requests.post(
            f"http://{target_practice}:5000/process",
            json=payload,
            headers={**headers, **propagator}
        )
        
        return response.json()
```

**Implementation (practice receiving request):**

```python
# Extract trace context from incoming request
from opentelemetry.propagate import extract

@app.route("/process", methods=["POST"])
def receive_request():
    # Extract trace context from headers
    ctx = extract(request.headers)
    
    with tracer.start_as_current_span("receive_request", context=ctx) as span:
        # This span becomes a child of the gateway's span
        payload = request.json
        
        # Run empirica transaction with tracing
        run_transaction("sess_incoming")
        
        return {"status": "processed"}
```

---

## Task 4.3: Validation

### Checklist

- [ ] **Loki Logs:**
  - [ ] Empirica session logs appear in Loki (query: {job="empirica-sessions"})
  - [ ] Practice stdout logs appear (query: {job="practice-stdout"})
  - [ ] ACAT metrics appear (query: {job="acat-grounding"})
  - [ ] Log query latency < 100ms (Loki UI)
  - [ ] Ingestion rate ≥ 100 logs/sec

- [ ] **Jaeger Traces:**
  - [ ] Multi-practice request traces visible (query: service=gateway)
  - [ ] Trace hierarchy correct (root span → child spans per phase)
  - [ ] Vectors logged as span attributes
  - [ ] Trace latency accurate (within 5% of actual)
  - [ ] Sampling strategy applied (50% gateway, 10% baseline)

- [ ] **Integration:**
  - [ ] Trace IDs match between Loki + Jaeger (if both log same event)
  - [ ] Cross-practice traces show correct flow
  - [ ] Error traces captured (100% sampling for errors)
  - [ ] Phase transitions visible in traces

### Validation Commands

#### Loki

```bash
# Test log ingestion via curl
curl -X POST http://localhost:3100/loki/api/v1/push \
  -H "Content-Type: application/json" \
  -d '{
    "streams": [{
      "stream": {
        "job": "empirica-sessions",
        "practice": "autonomy",
        "phase": "POSTFLIGHT"
      },
      "values": [["1722778530000000000", "Test log entry"]]
    }]
  }'

# Query logs
curl "http://localhost:3100/loki/api/v1/query?query={practice=\"autonomy\"}"

# Check ingestion metrics
curl http://localhost:3100/metrics | grep loki_distributor_bytes_received_total
```

#### Jaeger

```bash
# Test trace ingestion via curl
curl -X POST http://localhost:14268/api/traces \
  -H "Content-Type: application/json" \
  -d '{
    "batches": [{
      "process": {
        "serviceName": "gateway"
      },
      "spans": [{
        "traceID": "1234567890abcdef",
        "spanID": "abcdef1234567890",
        "operationName": "test-span",
        "startTime": 1722778530000000,
        "duration": 1000000
      }]
    }]
  }'

# Query traces
curl "http://localhost:16686/api/traces?service=gateway&limit=10"

# Check collector metrics
curl http://localhost:14269/metrics | grep jaeger_collector_spans_received
```

---

## Integration Timeline

### Deployment + Smoke Tests (Already Done in Task 3)
- Loki healthy + HTTP API responding
- Jaeger healthy + trace ingestion working
- Elasticsearch backend operational

### Task 4: Instrumentation (Current)
- Loki logging handlers integrated
- Jaeger tracing configured
- Practice services instrumented
- Empirica CLI wrapped with logging

### Task 5: Validation
- Log ingestion rate measured
- Trace completeness verified
- Query latency benchmarked
- Error tracing validated

### Phase 3.5.3: Dashboards
- Per-practice latency dashboards
- Multi-practice trace visualizations
- Log completeness metrics
- ACAT calibration dashboards

---

## Troubleshooting

### Logs not appearing in Loki

```bash
# Check Promtail status
docker logs promtail-phase35

# Verify Promtail can reach Loki
docker exec promtail-phase35 curl http://loki:3100/ready

# Check scrape configs
docker inspect promtail-phase35 | grep -A 10 "promtail-config"
```

### Traces not appearing in Jaeger

```bash
# Check Jaeger logs
docker logs jaeger-phase35

# Verify Elasticsearch is reachable
docker exec jaeger-phase35 curl http://elasticsearch:9200/_cluster/health

# Check trace ingestion metrics
curl http://localhost:14269/metrics | grep jaeger_collector_spans
```

### High latency in queries

```bash
# Check Loki cache settings
curl http://localhost:3100/loki/config | jq '.frontend'

# Check Jaeger query performance
curl "http://localhost:16686/api/traces?service=gateway&limit=1" -w "Query time: %{time_total}s"

# Check resource usage
docker stats loki-phase35 jaeger-phase35 elasticsearch
```

---

## Next Steps

1. **Deploy instrumentation code** to empirica + practices
2. **Start collecting logs + traces** from running services
3. **Validate data flow** (Task 5 validation checklist)
4. **Create dashboards** (Phase 3.5.3) to visualize traces + logs
5. **Measure baseline metrics** (latency, ingestion rate, sampling)

---

## References

- OpenTelemetry Python: https://opentelemetry.io/docs/instrumentation/python/
- Jaeger Client Python: https://github.com/jaegertracing/jaeger-client-python
- Loki API: https://grafana.com/docs/loki/latest/api/
- Promtail Config: https://grafana.com/docs/loki/latest/clients/promtail/
