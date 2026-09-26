# Epistemic Health Metrics — Integration Guide

**Phase 3.5.6** | **Status:** Ready for deployment

## Quick Start (5 minutes)

### 1. Verify Installation

```bash
cd empirica/
python3 test_epistemic_metrics.py
```

Expected: All tests pass ✓

### 2. Use in Your Code

**Option A: From POSTFLIGHT payload (recommended)**

```python
from epistemic_metrics import EpistemicHealthMetrics

# After POSTFLIGHT submission, get the payload
postflight_payload = {
    "vectors": {"know": 0.88, "uncertainty": 0.12, ...},
    "artifacts": {"findings": 8, "unknowns": 2, ...},
    "goals": [{"goal_id": "g1", "status": "completed"}, ...],
    "investigation_latency_seconds": 45.2,
}

# Create metrics
metrics = EpistemicHealthMetrics.from_postflight_payload(postflight_payload)

# Get all metrics
all_metrics = metrics.compute_all_metrics()

# Export as JSON (for Prometheus, Loki, observability systems)
json_str = metrics.to_json()
```

**Option B: With OTEL instrumentation**

```python
from otel_instrumentation import initialize_instrumentation

instr = initialize_instrumentation()

# After POSTFLIGHT, process payload
result = instr.process_postflight_payload(postflight_payload)

# Metrics are now recorded to Prometheus + attached to spans
```

## Files Created

| File | Purpose | LOC |
|------|---------|-----|
| `epistemic_metrics.py` | Core metrics module | 739 |
| `test_epistemic_metrics.py` | Comprehensive test suite | 426 |
| `example_epistemic_metrics.py` | 5 usage examples | 335 |
| `EPISTEMIC_METRICS.md` | Full documentation | 541 |
| `otel_instrumentation.py` | Updated with integration hooks | — |

**Total:** 1,500 lines of production-ready code

## The 7 Metrics (At a Glance)

| Metric | Measures | Threshold | Alert |
|--------|----------|-----------|-------|
| **Calibration Drift** | Vector confidence vs. evidence | 0.30 | Over/under-confident |
| **Unknown Accumulation** | Unresolved unknowns | 10 | Epistemic backlog |
| **Investigation Latency** | Time in noetic phase | — | Baseline tracking |
| **Artifact Type Violations** | Findings-only, missing decisions | 0 violations | Type discipline break |
| **Graph Density** | Connected artifacts | 0.50 | Isolated artifacts |
| **Goal Completion** | Completed / in-scope goals | 0.70 | Work-in-progress pile-up |
| **Phase Transition Speed** | Time in noetic → CHECK → praxic | — | Phase balance tracking |

## Integration Points

### 1. POSTFLIGHT Handler

When empirica calls `postflight-submit`, wire up metrics:

```python
# In your postflight handler or hook
from epistemic_metrics import EpistemicHealthMetrics

def handle_postflight(postflight_json):
    # Existing POSTFLIGHT logic...
    
    # NEW: Compute epistemic health metrics
    metrics = EpistemicHealthMetrics.from_postflight_payload(postflight_json)
    health_report = metrics.compute_all_metrics()
    
    # Log any alerts
    for metric_name, metric_result in health_report['metrics'].items():
        if metric_result and metric_result.get('threshold_exceeded'):
            logger.warning(f"Epistemic alert: {metric_name}")
            print(f"  {metric_result.get('alert')}")
            print(f"  Action: {metric_result.get('recommended_action')}")
    
    # Export for observability
    export_to_prometheus(metrics.to_json())
```

### 2. OTEL Instrumentation

Existing `otel_instrumentation.py` now has methods:

```python
from otel_instrumentation import get_instrumentation

instr = get_instrumentation()

# Process POSTFLIGHT payload (one-liner)
metrics = instr.process_postflight_payload(postflight_json)

# Add epistemic attributes to current span
instr.add_epistemic_attributes_to_span(postflight_json)

# Record individual vectors/artifacts
instr.record_epistemic_vector("know", 0.85, phase="postflight")
instr.record_epistemic_artifacts({"findings": 10, "unknowns": 2})
```

### 3. Observability Stack

Route JSON output to:

**Prometheus:**
```python
# Metrics are automatically exported if OTEL is configured
# Check: http://localhost:9090/graph
# Search: empirica_calibration_drift, empirica_unknowns_accumulated_total, etc.
```

**Loki:**
```python
# Send JSON as structured log
loki_client.push([{
    "labels": {"job": "epistemic-metrics", "session": postflight_json["session_id"]},
    "entries": [{"timestamp": time.time(), "line": metrics.to_json()}]
}])
```

**Custom Dashboard:**
```python
# Ingest JSON into your observability platform
send_to_datadog(metrics.to_json())
send_to_cloudwatch(metrics.to_json())
```

## API Cheat Sheet

### Creation

```python
# From POSTFLIGHT payload
metrics = EpistemicHealthMetrics.from_postflight_payload(payload)

# Manual
metrics = EpistemicHealthMetrics()
metrics.ingest_vectors({"know": 0.85})
metrics.ingest_artifacts({"findings": 8})
metrics.add_goal("g1", "completed")
```

### Recording

```python
# Individual metrics
drift = metrics.record_calibration_drift(0.15)
unknown = metrics.record_unknown_accumulation()
violations = metrics.record_artifact_type_violations()
density = metrics.record_graph_density(10, 20)
goals = metrics.record_goal_completion_ratio()
latency = metrics.record_investigation_latency()
phases = metrics.record_phase_transition_speed()

# All at once
all_metrics = metrics.compute_all_metrics()
```

### Export

```python
# JSON
json_str = metrics.to_json()

# Direct dict
dict_result = metrics.compute_all_metrics()
```

### Phase Tracking

```python
metrics.mark_phase_transition("noetic_start")
# ... work happens ...
metrics.mark_phase_transition("noetic_end")
metrics.mark_phase_transition("CHECK_start")
# ... etc
```

## Testing

All 7 metrics have full test coverage:

```bash
python3 test_epistemic_metrics.py

# Output:
# ✓ Vector Validation
# ✓ Artifact Counts
# ✓ Metric 1: Calibration Drift
# ✓ Metric 2: Unknown Accumulation
# ✓ Metric 3: Investigation Latency
# ✓ Metric 4: Artifact Type Violations
# ✓ Metric 5: Graph Density
# ✓ Metric 6: Goal Completion Ratio
# ✓ Metric 7: Phase Transition Speed
# ✓ POSTFLIGHT Payload Integration
# ✓ OTEL Integration
# ✓ ALL TESTS PASSED
```

## Examples

5 runnable examples included:

```bash
python3 example_epistemic_metrics.py

# Demonstrates:
# 1. Basic POSTFLIGHT processing
# 2. Issue detection & alerts
# 3. JSON export
# 4. Manual metric recording
# 5. Batch processing multiple sessions
```

## Error Handling

All inputs are validated:

```python
# These will raise ValidationError with descriptive messages:
EpistemicVector("know", 1.5)  # outside [0.0-1.0]
metrics.ingest_artifacts({"findings": -1})  # negative count
metrics.add_goal("g1", "bad_status")  # invalid status

# Errors are caught gracefully in process_postflight_payload():
try:
    result = instr.process_postflight_payload(bad_json)
except Exception as e:
    logger.error(f"Metrics processing failed: {e}")
    # Metrics computation failure never blocks POSTFLIGHT
```

## Production Checklist

- [ ] Tests passing: `python3 test_epistemic_metrics.py`
- [ ] Examples run: `python3 example_epistemic_metrics.py`
- [ ] OTEL instrumentation integrated (if using Prometheus/Jaeger)
- [ ] POSTFLIGHT handler wired up
- [ ] Observability system receiving metrics JSON
- [ ] Alerting configured for threshold_exceeded cases
- [ ] Documentation shared with team
- [ ] Thresholds calibrated for your practice (see EPISTEMIC_METRICS.md)

## Troubleshooting

### ImportError: No module named 'opentelemetry'

OTEL is optional. Metrics work without it, just won't be exported to Prometheus.

Install for full functionality:
```bash
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-prometheus
```

### Calibration Drift Always High

Check for findings-only collapse:
```python
# Good: balanced artifacts
{"findings": 8, "unknowns": 2, "decisions": 2, "assumptions": 1}

# Bad: findings-only
{"findings": 20, "unknowns": 0, "decisions": 0, "assumptions": 0}
```

If uncertainty > 0.3, must log unknowns/assumptions.

### Graph Density Low

Ensure artifacts have edges:
```bash
empirica log-artifacts -
# Include "edges" field:
# [{"from": "f1", "to": "u1", "relation": "grounded_by"}]
```

## Support

- **Documentation:** `EPISTEMIC_METRICS.md` (complete reference)
- **Tests:** `test_epistemic_metrics.py` (all 7 metrics covered)
- **Examples:** `example_epistemic_metrics.py` (5 scenarios)
- **Integration:** This file (quick reference)

## Next Steps

1. **Immediate:** Run tests, verify module works
2. **Short-term:** Wire into POSTFLIGHT handler
3. **Medium-term:** Add observability dashboard
4. **Long-term:** Trend analysis, per-practice calibration

---

**Phase 3.5.6 Status: ✓ Production-Ready**

Epistemic health metrics are now observable, measurable, and actionable.
