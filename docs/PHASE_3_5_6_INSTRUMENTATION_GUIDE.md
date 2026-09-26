# Phase 3.5.6: Observable Claude — Instrumentation Guide
## For Other Empirica Practices

This guide shows how to adopt the empirica-foundation-evaluator's OTEL instrumentation pattern in your own practice.

---

## Quick Start (5 minutes)

### 1. Install Dependencies

```bash
pip install opentelemetry-api opentelemetry-sdk \
  opentelemetry-exporter-otlp opentelemetry-exporter-prometheus
```

### 2. Copy Base Modules

Copy these files from empirica-foundation-evaluator to your practice:

```bash
# Core instrumentation
cp empirica-foundation-evaluator/empirica/otel_instrumentation.py YOUR_PRACTICE/empirica/

# Epistemic metrics (optional, for seat health tracking)
cp empirica-foundation-evaluator/empirica/epistemic_metrics.py YOUR_PRACTICE/empirica/

# CLI hooks (optional, for automatic transaction instrumentation)
cp empirica-foundation-evaluator/empirica/cli_instrumentation_hooks.py YOUR_PRACTICE/empirica/
```

### 3. Initialize in Your Code

```python
from empirica.otel_instrumentation import initialize_instrumentation

# At startup
instr = initialize_instrumentation(service_name="YOUR_PRACTICE_NAME")

# In transaction spans
with instr.transaction_span("code", goal="Your task"):
    with instr.phase_span("preflight"):
        # Your noetic work
        pass
    with instr.phase_span("CHECK"):
        # Your decision point
        pass
    with instr.phase_span("praxic"):
        # Your execution work
        pass
```

### 4. Configure Observability Stack

Ensure OTEL Collector is running:
- gRPC receiver: `localhost:4317` (traces)
- Prometheus exporter: `localhost:8889` (metrics)

```bash
# Start observability stack (if not already running)
cd YOUR_PRACTICE
docker-compose up -d otel-collector prometheus grafana
```

### 5. View Results

- **Jaeger UI:** http://localhost:16686 (traces)
- **Prometheus:** http://localhost:9090 (metrics)
- **Grafana:** http://localhost:3000 (dashboards)

---

## Integration Patterns

### Pattern 1: Automatic CLI Instrumentation

Wrap empirica CLI commands to automatically emit spans:

```python
from empirica.cli_instrumentation_hooks import CLIHookWrapper

wrapper = CLIHookWrapper()

# Wrap empirica preflight-submit
preflight_payload = json.dumps({
    "work_type": "code",
    "vectors": {...},
    "goals": [...]
})

returncode = wrapper.run_with_instrumentation([
    "preflight-submit", "-"
])
# Span automatically emitted with context
```

### Pattern 2: Manual Transaction Instrumentation

For custom workflows not using empirica CLI:

```python
with instr.transaction_span("research", goal="Investigate X"):
    # PREFLIGHT
    with instr.phase_span("preflight", {"task": "plan investigation"}):
        instr.record_vector("clarity", 0.7, "preflight")
        # ... your preflight work
    
    # Investigation (noetic)
    with instr.phase_span("noetic", {"searches": 5}):
        instr.record_unknown_count(3)
        instr.increment_unknown_resolved(1)
        # ... your investigation
    
    # Decision gate
    with instr.phase_span("CHECK"):
        instr.increment_CHECK_decision("proceed")
        # ... your decision
    
    # Execution (praxic)
    with instr.phase_span("praxic"):
        instr.increment_type_violation("findings_only")
        # ... your execution
```

### Pattern 3: Epistemic Health Tracking

Track seat health metrics:

```python
from empirica.epistemic_metrics import EpistemicHealthMetrics

epistemic = EpistemicHealthMetrics(instr)

# After POSTFLIGHT, record epistemic state
postflight_data = {
    "vectors": {"uncertainty": 0.15, "know": 0.85, ...},
    "unknowns": [{"id": "u1", ...}, ...],
    "findings": [{"id": "f1", ...}, ...],
    "goals_completed": 1,
    "goals_in_scope": 1,
}

metrics = epistemic.process_postflight_payload(postflight_data)
# Metrics automatically recorded to Prometheus
```

---

## Configuring Your Dashboard

### Step 1: Import Dashboard Template

In Grafana:
1. Dashboards → Import
2. Paste JSON from `grafana_dashboard_seat_health.json`
3. Select Prometheus data source
4. Click Import

### Step 2: Customize for Your Practice

Edit the dashboard JSON:
- Replace `empirica-foundation-evaluator` with your `service_name`
- Add your practice-specific metrics (if any)
- Adjust thresholds for your workload

```json
{
  "targets": [
    {
      "expr": "empirica_unknowns_total{service=\"YOUR_PRACTICE_NAME\"}"
    }
  ]
}
```

### Step 3: Add to AlertManager

Import alerting rules:

```bash
# Copy rules to Prometheus config directory
cp empirica-foundation-evaluator/agent/empirica_seat_alerting_rules.yaml \
  /etc/prometheus/rules/seat-health.yml

# Reload Prometheus
curl -X POST http://localhost:9090/-/reload
```

---

## Metrics Reference

### Phase 1: Base Metrics (Always Available)

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `empirica.unknowns.total` | Counter | event | Total unknowns encountered |
| `empirica.investigation.latency.seconds` | Histogram | phase | Time in noetic phase |
| `empirica.unknowns.resolved.total` | Counter | action | Unknowns resolved |
| `empirica.artifact.type.violations.total` | Counter | violation_type | Type discipline violations |
| `empirica.CHECK.decisions.total` | Counter | decision | CHECK gate decisions (proceed/block) |
| `empirica.phase.duration.seconds` | Histogram | phase | Duration of each phase |

### Phase 3: Epistemic Health Metrics (Optional)

| Metric | Type | Threshold | Alert Threshold |
|--------|------|-----------|-----------------|
| `empirica.calibration.drift` | Gauge | 0.0-1.0 | >0.3 yellow, >0.5 red |
| `empirica.unknowns.accumulation` | Gauge | count | >5 yellow, >10 red |
| `empirica.artifact.graph.density` | Gauge | 0.0-1.0 | <0.5 yellow |
| `empirica.goals.completion.ratio` | Gauge | 0.0-1.0 | <0.7 yellow |

---

## Troubleshooting

### Traces Not Appearing in Jaeger

**Check:** Is OTEL Collector running?
```bash
docker-compose ps otel-collector
curl http://localhost:4317/healthz  # Should return 200
```

**Fix:** Start OTEL Collector
```bash
docker-compose up -d otel-collector
```

### Metrics Not in Prometheus

**Check:** Is Prometheus scraping port 8889?
```bash
curl http://localhost:9090/api/v1/targets  # Check scrape jobs
curl http://localhost:8889/metrics | grep empirica  # Check metrics exported
```

**Fix:** Add scrape job to prometheus.yml
```yaml
scrape_configs:
  - job_name: 'otel-collector'
    static_configs:
      - targets: ['localhost:8889']
```

### Dashboard Queries Returning No Data

**Check:** Are metrics being recorded?
```bash
# Telnet into Prometheus metrics endpoint
curl http://localhost:8889/metrics | head -20
```

**Fix:** Ensure instrumentation is being called
```python
# Verify in your code
instr = initialize_instrumentation()
instr.record_unknown_count(5)  # Should record metric
```

---

## Best Practices

1. **Initialize Early:** Call `initialize_instrumentation()` as early as possible in your practice's startup
2. **Use Context Managers:** Always use `transaction_span()` and `phase_span()` for automatic span lifecycle
3. **Record Frequently:** Call metric-recording methods as you progress through phases
4. **Label Thoughtfully:** Use clear phase names and attributes (they appear in Jaeger UI)
5. **Monitor Thresholds:** Adjust alert thresholds for your practice's baseline

---

## Example: Full Transaction Flow

```python
from empirica.otel_instrumentation import initialize_instrumentation

instr = initialize_instrumentation(service_name="my-practice")

with instr.transaction_span("code", goal="Build feature X"):
    # PREFLIGHT
    with instr.phase_span("preflight", {"objective": "Feature X", "complexity": "medium"}):
        instr.record_vector("clarity", 0.8)
        instr.record_vector("know", 0.7)
    
    # Noetic (investigation)
    investigation_start = time.time()
    with instr.phase_span("noetic", {"task": "Design architecture"}):
        # Simulate investigation work
        for i in range(3):
            instr.record_unknown_count(random.randint(2, 5))
            time.sleep(0.5)
        
        investigation_time = time.time() - investigation_start
        instr.record_investigation_latency(investigation_time)
    
    # CHECK gate
    with instr.phase_span("CHECK", {"confidence": 0.85}):
        instr.increment_CHECK_decision("proceed")
    
    # Praxic (execution)
    with instr.phase_span("praxic", {"commits": 1, "tests": 5}):
        instr.record_unknown_count(0)  # All resolved
        instr.increment_unknown_resolved(3)
    
    # POSTFLIGHT
    with instr.phase_span("postflight", {"findings": 2, "goals": 1}):
        instr.record_vector("completion", 1.0)
        instr.record_vector("uncertainty", 0.1)

# Spans automatically exported to Jaeger
# Metrics automatically scraped by Prometheus
# Dashboard updated in real-time
print("✓ Transaction complete. View traces at http://localhost:16686")
```

---

## Contributing Improvements

Found a better pattern? Improve the instrumentation? Make a PR to empirica-foundation-evaluator with:
- Example code showing the pattern
- Updated INSTRUMENTATION_GUIDE.md
- Tests if adding new metrics

---

## References

- [OpenTelemetry Python SDK](https://opentelemetry.io/docs/instrumentation/python/)
- [Prometheus Metrics Types](https://prometheus.io/docs/concepts/metric_types/)
- [Jaeger Tracing](https://www.jaegertracing.io/docs/)
- [Phase 3.5.6 Architecture](./PHASE_3_5_6_IMPLEMENTATION_STATUS.md)
