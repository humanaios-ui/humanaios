# Tasks 6-10: Instrumentation Deployment

## Overview

Tasks 6-10 cover deploying the Loki + Jaeger instrumentation from Task 4 into empirica CLI and practice services, with end-to-end validation.

**Status:** Deployment scripts + integration guides ready. Tasks 6-10 implement practical wiring.

---

## Task 6: Deploy Loki Instrumentation to Empirica CLI

### Objective

Wire empirica CLI commands (preflight-submit, check-submit, postflight-submit) to forward logs to Loki.

### Implementation

**File:** `empirica-loki-integration.sh`

**What it does:**

```bash
# Step 1: Install instrumentation modules to Python site-packages
cp empirica-loki-logging.py /usr/local/lib/python3.x/site-packages/

# Step 2: Create Loki logging config
mkdir -p ~/.empirica/logging
cat > ~/.empirica/logging/loki.yaml  # Config with handlers + loggers

# Step 3: Create empirica CLI wrapper
cat > ~/.empirica/bin/empirica-with-loki  # Wraps empirica CLI

# Step 4: Create environment setup script
cat > ~/.empirica/setup-loki.sh  # Exports session context
```

### Execution

```bash
# Run integration script
./empirica-loki-integration.sh

# Source environment (enables logging)
source ~/.empirica/setup-loki.sh

# Run empirica commands (logs auto-forward to Loki)
empirica preflight-submit - < preflight.json
empirica check-submit - < check.json
empirica postflight-submit - < postflight.json

# Verify logs in Loki UI
curl "http://localhost:3100/loki/api/v1/query?query={practice=\"autonomy\"}"
```

### Expected Output

```
✓ Loki logging enabled
  Session ID: sess_1722778530
  Practice: autonomy
  Loki URL: http://localhost:3100
```

**Logs appear in Loki:**
```
{job="empirica-sessions", practice="autonomy", session_id="sess_1722778530"}
  │ PREFLIGHT submitted
  │ Vectors: know=0.75, uncertainty=0.20
  │ PREFLIGHT completed
  │ CHECK submitted
  │ Vectors: know=0.80, clarity=0.82
  │ CHECK completed
  │ POSTFLIGHT submitted
  │ POSTFLIGHT completed
```

### Validation Checklist

- [ ] Instrumentation modules installed to site-packages
- [ ] `~/.empirica/logging/loki.yaml` created
- [ ] `~/.empirica/bin/empirica-with-loki` created + executable
- [ ] `source ~/.empirica/setup-loki.sh` sets EMPIRICA_SESSION_ID
- [ ] `empirica preflight-submit` logs appear in Loki within 30s
- [ ] Log query latency < 100ms

---

## Task 7: Wire Practice Stdout + ACAT Metrics

### Objective

Forward practice process logs + ACAT calibration metrics to Loki.

### Practice Stdout Logging

**File:** `promtail-local-config.yaml` (practice-stdout job)

**Setup:**

1. Practice process redirects output to log file:
   ```bash
   # In practice startup
   exec > /var/log/practice-autonomy.log 2>&1
   ```

2. Promtail scrapes + forwards to Loki:
   ```yaml
   - job_name: practice-stdout
     static_configs:
       - targets: [localhost]
         labels:
           __path__: /var/log/practice-*.log
     pipeline_stages:
       - regex:
           expression: '(?P<timestamp>\S+)\s+(?P<level>\w+)\s+(?P<practice>\w+)\s+(?P<message>.*)'
       - labels:
           practice: practice
           level: level
   ```

3. Logs appear in Loki:
   ```
   {job="practice-stdout", practice="autonomy", level="error"}
   ```

### ACAT Metrics Logging

**File:** `empirica-loki-logging.py` (AcatMetricsLokiHandler)

**Integration:**

```python
from empirica_loki_logging import setup_acat_metrics_logging

# Setup at session start
acat_logger = setup_acat_metrics_logging(loki_url="http://loki:3100")

# After POSTFLIGHT, log calibration check
acat_logger.info("ACAT calibration", extra={
    'ai_id': 'autonomy',
    'vector_name': 'know',
    'predicted': 0.82,
    'actual': 0.78,
    'brier_error': 0.0016,
    'phase': 'POSTFLIGHT',
    'session_id': session_id
})
```

**Logs appear in Loki:**
```
{job="acat-grounding", source="empirica"}
  │ ACAT calibration: know=0.82 actual=0.78 brier=0.0016
  │ ACAT calibration: do=0.95 actual=0.92 brier=0.0009
  │ ...
```

### Validation Checklist

- [ ] `/var/log/practice-*.log` files exist with practice output
- [ ] Promtail scraping practice-stdout job
- [ ] Practice logs appear in Loki {job="practice-stdout"}
- [ ] ACAT metrics logged at end of POSTFLIGHT
- [ ] ACAT logs appear in Loki {job="acat-grounding"}
- [ ] Query {job="practice-stdout"} returns results

---

## Task 8: Deploy Jaeger Instrumentation to Gateway

### Objective

Wire gateway service with Jaeger tracing for multi-practice request traces.

### Implementation

**Files:** `empirica-jaeger-tracing.py` + `practice-jaeger-integration.py`

**Gateway setup:**

```python
from empirica_jaeger_tracing import setup_jaeger_tracer, instrument_gateway
from flask import Flask

app = Flask(__name__)

# Initialize tracer
tracer = setup_jaeger_tracer(
    service_name="gateway",
    jaeger_agent_host="jaeger",  # k8s service
    jaeger_agent_port=6831,
    sample_rate=0.5  # 50% sampling for gateway
)

# Auto-instrument Flask
instrument_gateway(app)

# Tracing is automatic for all routes + HTTP calls
@app.route("/request/<target>", methods=["POST"])
def send_request(target):
    # Spans created automatically by instrumentation
    # Trace context propagated to target practice
    return send_to_practice(target)
```

**Trace hierarchy:**

```
Root span: gateway (entry point)
  ├─ source_practice: autonomy
  ├─ target_practice: mesh-support
  └─ child spans:
      ├─ HTTP request (outbound)
      ├─ Network latency
      └─ Response parsing
```

### Execution

```bash
# Start gateway with tracing
JAEGER_HOST=jaeger JAEGER_PORT=6831 python3 gateway.py

# Send multi-practice request
curl -X POST http://localhost:5000/request/mesh-support \
  -H "X-Source-Practice: autonomy" \
  -d '{"objective": "collab_brief"}'

# View trace in Jaeger UI
# http://localhost:16686/search?service=gateway
```

### Validation Checklist

- [ ] Jaeger exporter configured (agent_host, agent_port)
- [ ] Flask routes auto-instrumented
- [ ] HTTP requests generate child spans
- [ ] Traces appear in Jaeger UI (service=gateway)
- [ ] Span tags show source/target practice
- [ ] Trace latency matches actual request time

---

## Task 9: Deploy Jaeger Instrumentation to Practices

### Objective

Instrument practice services with phase tracing + multi-practice request tracking.

### Implementation

**File:** `practice-jaeger-integration.py`

**Practice setup:**

```python
from practice_jaeger_integration import initialize_tracing, trace_transaction

# In practice startup
tracer = initialize_tracing("autonomy")  # Or "mesh-support", "outreach", etc.

# In transaction handler
def run_transaction(session_id, preflight_json, check_json, postflight_json):
    # PREFLIGHT phase
    with trace_transaction(tracer, session_id, "PREFLIGHT", "autonomy") as tracker:
        tracker.set_vector("know", preflight_json["know"])
        tracker.set_vector("uncertainty", preflight_json["uncertainty"])
        # ... execute PREFLIGHT ...
        tracker.end_phase(duration_ms=125, status="submitted")
    
    # CHECK phase
    with trace_transaction(tracer, session_id, "CHECK", "autonomy") as tracker:
        tracker.set_vector("clarity", check_json["clarity"])
        # ... execute CHECK ...
        tracker.end_phase(duration_ms=58, status="proceed")
    
    # POSTFLIGHT phase
    with trace_transaction(tracer, session_id, "POSTFLIGHT", "autonomy") as tracker:
        tracker.set_vector("completion", postflight_json["completion"])
        tracker.add_goal("goal_abc", "Phase 3.5 implementation")
        # ... execute POSTFLIGHT ...
        tracker.end_phase(duration_ms=158, status="closed")
```

**Trace hierarchy (per practice):**

```
Root span: session_id (from gateway)
  ├─ Child span: PREFLIGHT
  │   ├─ vector.know: 0.75
  │   ├─ vector.uncertainty: 0.20
  │   └─ duration_ms: 125
  ├─ Child span: CHECK
  │   ├─ vector.clarity: 0.80
  │   └─ duration_ms: 58
  └─ Child span: POSTFLIGHT
      ├─ vector.completion: 0.95
      ├─ goal_id: goal_abc
      └─ duration_ms: 158
```

### Execution

```bash
# Start practice with tracing
PRACTICE_NAME=autonomy JAEGER_HOST=jaeger python3 autonomy_service.py

# Run transaction (traced automatically)
python3 run_transaction.py --session-id sess_demo_001

# View practice traces in Jaeger UI
# http://localhost:16686/search?service=autonomy
```

### Validation Checklist

- [ ] Tracer initialized for practice service
- [ ] PREFLIGHT phase creates span with vectors
- [ ] CHECK phase creates span with clarity
- [ ] POSTFLIGHT phase creates span with completion + goal
- [ ] Phase spans appear in correct order (PREFLIGHT → CHECK → POSTFLIGHT)
- [ ] Traces appear in Jaeger UI (service=autonomy)
- [ ] Trace duration matches actual phase duration (±5%)

---

## Task 10: End-to-End Validation

### Objective

Validate complete instrumentation: logs in Loki, traces in Jaeger, data consistency.

### Validation Scenarios

#### Scenario 1: Single-Practice Transaction

**Setup:**
```bash
# Start Loki + Jaeger
docker-compose -f docker-compose-phase35.yaml up -d

# Enable empirica logging
source ~/.empirica/setup-loki.sh

# Start practice service
PRACTICE_NAME=autonomy python3 practice_service.py
```

**Execute:**
```bash
# Run transaction
empirica session-create --ai-id empirica-foundation-evaluator --output json
export SESSION_ID=$(cat .empirica/sessions/sessions.db | jq -r '.session_id')

empirica preflight-submit - << EOF
{
  "know": 0.75,
  "do": 0.90,
  "context": 0.70
}
EOF

empirica check-submit - << EOF
{
  "clarity": 0.80,
  "coherence": 0.82
}
EOF

empirica postflight-submit - << EOF
{
  "completion": 0.95,
  "uncertainty": 0.08
}
EOF
```

**Validate Logs:**
```bash
# Query Loki for session logs
curl "http://localhost:3100/loki/api/v1/query?query={session_id=\"$SESSION_ID\"}"

# Expected: 3 log entries (PREFLIGHT, CHECK, POSTFLIGHT submitted)
```

**Validate Traces:**
```bash
# Query Jaeger for session traces
curl "http://localhost:16686/api/traces?service=autonomy&limit=1"

# Expected: 3 spans (PREFLIGHT, CHECK, POSTFLIGHT)
# Each span should have vector attributes
```

#### Scenario 2: Multi-Practice Request

**Execute:**
```bash
# Autonomy sends collab to mesh-support
curl -X POST http://localhost:5000/collab/mesh-support \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "'$SESSION_ID'",
    "type": "collab_brief",
    "payload": {"question": "Ready for production?"}
  }'
```

**Validate Logs:**
```bash
# Query both practices' logs
curl "http://localhost:3100/loki/api/v1/query?query={session_id=\"$SESSION_ID\"}" \
  | jq '.data.result[] | .values[] | .[1]'

# Expected: logs from both autonomy + mesh-support
```

**Validate Traces:**
```bash
# Query gateway traces
curl "http://localhost:16686/api/traces?service=gateway&limit=1" | jq '.data[0]'

# Expected trace hierarchy:
# - gateway span (root)
#   - autonomy PREFLIGHT/CHECK/POSTFLIGHT
#   - HTTP request to mesh-support
#     - mesh-support PREFLIGHT/CHECK/POSTFLIGHT
```

#### Scenario 3: ACAT Calibration

**Execute:**
```bash
# After POSTFLIGHT, log calibration check
python3 << 'EOF'
from empirica_loki_logging import setup_acat_metrics_logging

acat_logger = setup_acat_metrics_logging("http://localhost:3100")

acat_logger.info("ACAT calibration", extra={
    'ai_id': 'autonomy',
    'vector_name': 'know',
    'predicted': 0.82,
    'actual': 0.78,
    'brier_error': 0.0016,
    'session_id': '$SESSION_ID'
})
EOF
```

**Validate:**
```bash
# Query ACAT metrics in Loki
curl "http://localhost:3100/loki/api/v1/query?query={job=\"acat-grounding\"}"

# Expected: calibration entry with brier_error field
```

### Validation Checklist

- [ ] **Loki Logs:**
  - [ ] Session logs {session_id="$SESSION_ID"} appear within 10s
  - [ ] PREFLIGHT/CHECK/POSTFLIGHT entries logged
  - [ ] Practice-stdout logs appear {job="practice-stdout"}
  - [ ] ACAT metrics appear {job="acat-grounding"}

- [ ] **Jaeger Traces:**
  - [ ] Service traces visible (autonomy, gateway)
  - [ ] Phase spans created (PREFLIGHT → CHECK → POSTFLIGHT)
  - [ ] Vector attributes present in spans
  - [ ] Multi-practice trace hierarchy correct

- [ ] **Data Consistency:**
  - [ ] Trace IDs match between services (trace propagation)
  - [ ] Phase latency in logs ≈ phase span duration in traces (±5%)
  - [ ] Vector values in logs match span attributes

- [ ] **Performance:**
  - [ ] Log query latency < 100ms
  - [ ] Trace query latency < 200ms
  - [ ] Log ingestion rate ≥ 100 logs/sec
  - [ ] No dropped spans or logs

### Commands for Validation

```bash
# Check Loki ingestion
curl http://localhost:3100/metrics | grep loki_distributor_bytes_received_total

# Check Jaeger ingestion
curl http://localhost:14269/metrics | grep jaeger_collector_spans_received

# Query all logs for session
curl -s "http://localhost:3100/loki/api/v1/query?query={session_id=\"$SESSION_ID\"}" \
  | jq '.data.result[0].values | map(.[1])'

# Query all traces for service
curl -s "http://localhost:16686/api/traces?service=autonomy&limit=10" \
  | jq '.data[] | {traceID, spans: (.spans | length)}'

# Check datasource connectivity in Grafana
curl -s http://localhost:3000/api/datasources | jq '.[] | {name, type, url}'
```

---

## Integration Timeline

| Task | Effort | Dependencies | Output |
|------|--------|--------------|--------|
| Task 6: Deploy Loki to empirica | 15 min | Loki running | empirica CLI forwards logs |
| Task 7: Wire practice logs + ACAT | 20 min | Promtail running | Practice + ACAT logs in Loki |
| Task 8: Deploy Jaeger to gateway | 20 min | Jaeger running | Gateway traces in Jaeger |
| Task 9: Deploy Jaeger to practices | 25 min | All services running | Full trace hierarchy |
| Task 10: End-to-end validation | 30 min | All above complete | Validated logs + traces |
| **Total** | **110 min** | **~2 hours** | **Production-ready** |

---

## Troubleshooting

### Logs not appearing in Loki

```bash
# Check if Loki is running
curl http://localhost:3100/ready

# Check if logs are being batched
# (default batch size 10 - may need to run multiple commands)
for i in {1..15}; do
  empirica preflight-submit - < /dev/null 2>/dev/null || true
done

# Check for errors in CLI wrapper
echo $PYTHONPATH
ls -la ~/.empirica/bin/empirica-with-loki
```

### Traces not appearing in Jaeger

```bash
# Check if Jaeger is running
curl http://localhost:14269/

# Check if Elasticsearch is running
curl http://elasticsearch:9200/_cluster/health

# Check for tracer initialization errors
python3 -c "from empirica_jaeger_tracing import setup_jaeger_tracer; setup_jaeger_tracer('test')"

# Verify span batching (may need multiple operations)
for i in {1..5}; do
  # Run traced operations
  python3 practice-jaeger-integration.py > /dev/null
done
```

### Trace context not propagating

```bash
# Check if trace propagators are set
python3 << 'EOF'
from opentelemetry.propagate import get_global_textmap
prop = get_global_textmap()
print(f"Propagators: {type(prop)}")
EOF

# Verify headers in requests
curl -v -X POST http://localhost:5000/request/mesh-support 2>&1 | grep -i trace
```

---

## Next Steps

1. **Execute Tasks 6-10** in order (2 hours total)
2. **Validate each task** using checklists + commands
3. **Monitor Loki + Jaeger** dashboards during validation
4. **Fix any gaps** (missing logs, dropped traces)
5. **Move to Phase 3.5.3** (dashboard creation) once all tasks validated

---

## References

- empirica-loki-integration.sh: CLI integration script
- empirica-loki-logging.py: Logging handlers
- practice-jaeger-integration.py: Practice integration
- empirica-jaeger-tracing.py: Tracing SDK
- TASK4_INSTRUMENTATION_GUIDE.md: Reference guide
