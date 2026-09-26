# Epistemic Health Metrics Module — Phase 3.5.6

**Status:** Production-ready | **Last Updated:** 2026-07-31

## Overview

The **Epistemic Health Metrics** module extends OpenTelemetry instrumentation with concrete metrics tracking the epistemic state of an AI practitioner. It measures seven key dimensions of epistemic health and emits alerts when discipline breaks down.

### Why This Matters

The Empirica practice model rests on tight epistemic discipline: artifact type discipline, vector calibration, and connected graph structure. Without instrumentation, blindspots in discipline go undetected until they compound.

This module surfaces those signals as metrics: **calibration drift**, **unknown accumulation**, **artifact type violations**, **graph density**, **goal completion**, and **phase transition speed**. Each metric is grounded in observable evidence.

## The 7 Metrics

### 1. Calibration Drift (gauge)
**Question:** Is the AI's confidence proportional to evidence?

**Measurement:**
- Divergence between `uncertainty` vector and logged unknowns/assumptions
- Penalty for findings-only collapse (no noetic artifacts captured)
- Formula: `|expected_unknowns - actual_unknowns|` + compound penalties

**Threshold:** 0.30 (30% divergence)

**What It Catches:**
- Claiming high confidence while uncertainty is high (overconfidence)
- Logging no unknowns despite high uncertainty (hiding uncertainty)
- Findings-only artifact patterns (type discipline failure)

**Alert Example:**
```
Calibration drift: 0.65 (exceeds 0.30)
→ Reason: Uncertainty at 0.9 but zero unknowns logged
→ Action: Review vector assessments; ensure unknowns match uncertainty
```

---

### 2. Unknown Accumulation (counter)
**Question:** Are unknowns being resolved or piling up?

**Measurement:**
- Total count of unresolved `unknowns` artifacts
- Monitored across transactions

**Threshold:** 10 unresolved unknowns

**What It Catches:**
- Unresolved questions accumulating without investigation
- Epistemic backlog growing faster than investigation capacity

**Alert Example:**
```
Unknown accumulation: 15 (exceeds threshold of 10)
→ Action: Review and resolve outstanding unknowns before next transaction
```

---

### 3. Investigation Latency (histogram)
**Question:** How much time is spent in the noetic (investigation) phase?

**Measurement:**
- Elapsed seconds from `noetic_start` to `noetic_end`
- Histogram distribution across transactions

**What It Tracks:**
- How long investigation takes relative to implementation
- Baseline for detecting rushed or over-extended investigations
- Phase transition sequence with timestamps

**Example Output:**
```
Investigation Latency: 45.2s
Phase Sequence:
  - noetic_start → 2026-07-31T16:00:00
  - noetic_end → 2026-07-31T16:00:45.2
```

---

### 4. Artifact Type Violations (counter)
**Question:** Is artifact type discipline maintained?

**Violations Detected:**
1. **Findings-only collapse** — >90% of artifacts are findings, zero unknowns
2. **Missing decisions** — >5 praxic artifacts but zero decisions recorded
3. **Missing assumptions** — High uncertainty but no assumptions logged

**What It Catches:**
- Discipline breakdown in artifact logging
- Inability to distinguish findings (observations) from decisions (choices)
- Unexpressed assumptions that should be falsifiable

**Alert Example:**
```
Artifact type violations: 2 detected
  1. findings_only_collapse: Findings 25/25 (100%), unknowns 0
  2. missing_assumptions: Uncertainty 0.8 but zero assumptions logged
→ Action: Log unknowns and assumptions proportional to uncertainty
```

---

### 5. Graph Density (gauge)
**Question:** Are artifacts connected via edges, or isolated islands?

**Measurement:**
- `connected_artifacts / total_artifacts`
- Artifacts with edges (sourced_from, grounded_by, invalidates, etc.)

**Threshold:** 0.50 (50% must be connected)

**What It Catches:**
- Artifacts created without relationships
- Inability to sweep/invalidate stale artifacts (only works on connected graphs)
- Poor epistemic hygiene

**Alert Example:**
```
Graph density: 0.15 (3 connected / 20 total, below 0.50)
→ Reason: Most artifacts are isolated islands
→ Action: Link artifacts via edges (sourced_from, grounded_by, etc.)
```

---

### 6. Goal Completion Ratio (counter)
**Question:** What fraction of in-scope goals are complete?

**Measurement:**
- `completed_goals / in_scope_goals`
- Abandoned/out-of-scope goals excluded from denominator

**Threshold:** 0.70 (70% completion)

**What It Tracks:**
- Progress toward phase completion
- Scope creep (new goals vs. completions)
- Work-in-progress accumulation

**Example Output:**
```
Goal Completion: 4/5 (80%)
  Completed: g1, g2, g3, g4
  In Progress: g5
  Out of Scope: g6 (abandoned)
```

---

### 7. Phase Transition Speed (histogram)
**Question:** How long does each phase take (noetic → CHECK → praxic)?

**Measurement:**
- Time in `noetic_start` → `noetic_end`
- Time in `CHECK_start` → `CHECK_end`
- Time in `praxic_start` → `praxic_end`
- Full `noetic_to_praxic` duration

**What It Tracks:**
- Phase balance (investigation vs. execution)
- CHECK gate as a meaningful pause (not a rubber stamp)
- Total transaction time distribution

**Example Output:**
```
Phase Transitions:
  Noetic: 28.5s
  CHECK: 2.3s
  Praxic: 14.2s
  Total (noetic→praxic): 45.0s
```

---

## API Reference

### EpistemicHealthMetrics

Main class for computing epistemic health metrics.

#### Constructor

```python
from epistemic_metrics import EpistemicHealthMetrics

# Option 1: From POSTFLIGHT payload (preferred)
metrics = EpistemicHealthMetrics.from_postflight_payload(
    payload={
        "vectors": {"know": 0.85, "uncertainty": 0.15, ...},
        "artifacts": {"findings": 8, "unknowns": 2, ...},
        "goals": [{"goal_id": "g1", "status": "completed"}, ...],
    },
    otel_instrumentation=otel_instance  # optional
)

# Option 2: Manual construction
metrics = EpistemicHealthMetrics(otel_instrumentation=otel_instance)
```

#### Recording Metrics

```python
# Individual metrics
drift_result = metrics.record_calibration_drift(drift_value)
unknown_result = metrics.record_unknown_accumulation()
violations_result = metrics.record_artifact_type_violations()
density_result = metrics.record_graph_density(connected_count, total_count)
goal_result = metrics.record_goal_completion_ratio()
latency_result = metrics.record_investigation_latency()
phase_result = metrics.record_phase_transition_speed()

# All at once
all_metrics = metrics.compute_all_metrics()

# Export as JSON
json_str = metrics.to_json()
```

#### Ingesting Data

```python
# From payload
metrics.ingest_vectors({"know": 0.85, "uncertainty": 0.15})
metrics.ingest_artifacts({"findings": 8, "unknowns": 2, "decisions": 3})
metrics.ingest_goals([
    {"goal_id": "g1", "status": "completed", "in_scope": True},
    {"goal_id": "g2", "status": "in_progress", "in_scope": True},
])

# Phase transitions
metrics.mark_phase_transition("noetic_start")
metrics.mark_phase_transition("noetic_end")
metrics.mark_phase_transition("CHECK_start")
# ... etc
```

### OTEL Integration

The epistemic metrics module integrates with `otel_instrumentation.py`:

```python
from otel_instrumentation import initialize_instrumentation

instr = initialize_instrumentation()

# Process POSTFLIGHT payload and compute metrics
result = instr.process_postflight_payload(postflight_json)

# Add epistemic attributes to current span
instr.add_epistemic_attributes_to_span(postflight_json)

# Record individual vectors/artifacts
instr.record_epistemic_vector("know", 0.85, phase="postflight")
instr.record_epistemic_artifacts({"findings": 10, "unknowns": 2})
```

## Input Payloads

### POSTFLIGHT Payload Structure

Expected JSON format from empirica POSTFLIGHT submission:

```json
{
  "session_id": "abc-123-def",
  "timestamp": "2026-07-31T16:00:00Z",
  "work_type": "code",
  "vectors": {
    "know": 0.85,
    "do": 0.92,
    "context": 0.90,
    "clarity": 0.88,
    "coherence": 0.85,
    "signal": 0.80,
    "density": 0.78,
    "state": 0.82,
    "change": 0.45,
    "completion": 0.95,
    "impact": 0.85,
    "engagement": 0.98,
    "uncertainty": 0.12
  },
  "artifacts": {
    "findings": 8,
    "unknowns": 2,
    "decisions": 3,
    "assumptions": 1,
    "mistakes": 0,
    "dead_ends": 1,
    "goals": 5
  },
  "goals": [
    {"goal_id": "g1", "status": "completed", "in_scope": true},
    {"goal_id": "g2", "status": "completed", "in_scope": true},
    {"goal_id": "g3", "status": "in_progress", "in_scope": true},
    {"goal_id": "g4", "status": "abandoned", "in_scope": false}
  ],
  "investigation_latency_seconds": 45.2,
  "graph_density": {
    "connected_artifacts": 10,
    "total_artifacts": 15
  }
}
```

## Output Format

### JSON Metrics Output

```json
{
  "timestamp": "2026-07-31T16:44:06.795252",
  "metrics": {
    "calibration_drift": {
      "metric": "calibration_drift",
      "value": 0.05,
      "threshold": 0.30,
      "threshold_exceeded": false,
      "timestamp": "2026-07-31T16:44:06.795262"
    },
    "unknown_accumulation": {
      "metric": "unknown_accumulation",
      "count": 2,
      "threshold": 10,
      "threshold_exceeded": false,
      "timestamp": "2026-07-31T16:44:06.795267"
    },
    "artifact_type_violations": {
      "metric": "artifact_type_violations",
      "violations": [],
      "violation_count": 0,
      "threshold_exceeded": false,
      "timestamp": "2026-07-31T16:44:06.795274"
    },
    "goal_completion_ratio": {
      "metric": "goal_completion_ratio",
      "ratio": 0.80,
      "completed_goals": 4,
      "in_scope_goals": 5,
      "threshold": 0.70,
      "threshold_exceeded": false,
      "timestamp": "2026-07-31T16:44:06.795296"
    },
    "graph_density": {
      "metric": "graph_density",
      "density": 0.67,
      "connected_artifacts": 10,
      "total_artifacts": 15,
      "threshold": 0.50,
      "threshold_exceeded": false,
      "timestamp": "2026-07-31T16:44:06.795283"
    }
  },
  "artifact_counts": {
    "findings": 8,
    "unknowns": 2,
    "decisions": 3,
    "assumptions": 1,
    "mistakes": 0,
    "dead_ends": 1,
    "goals": 5
  },
  "vectors": {
    "know": {"name": "know", "value": 0.85, "phase": null, "timestamp": null},
    "uncertainty": {"name": "uncertainty", "value": 0.12, "phase": null, "timestamp": null}
  }
}
```

### Prometheus Metrics

Metrics are exported as:
- **Gauges:** calibration_drift, graph_density, goals_completion_ratio
- **Counters:** unknown_accumulation, artifact_type_violations
- **Histograms:** investigation_latency_seconds, phase_duration_seconds

Example:
```
# HELP empirica_calibration_drift Divergence between vector assessments and evidence
# TYPE empirica_calibration_drift gauge
empirica_calibration_drift{phase="postflight"} 0.05

# HELP empirica_unknowns_accumulated_total Total accumulated unresolved unknowns
# TYPE empirica_unknowns_accumulated_total counter
empirica_unknowns_accumulated_total{status="unresolved"} 2

# HELP empirica_investigation_latency_seconds Time spent in noetic phase
# TYPE empirica_investigation_latency_seconds histogram
empirica_investigation_latency_seconds_bucket{le="10.0", phase="noetic"} 0
empirica_investigation_latency_seconds_bucket{le="100.0", phase="noetic"} 5
empirica_investigation_latency_seconds_sum{phase="noetic"} 228.5
empirica_investigation_latency_seconds_count{phase="noetic"} 5
```

## Running Tests

```bash
cd empirica/
python3 test_epistemic_metrics.py
```

Expected output:
```
======================================================================
Phase 3.5.6 Epistemic Health Metrics - Test Suite
======================================================================
[TEST] Vector Validation
  ✓ Valid vector (0.5)
  ...
✓ ALL TESTS PASSED
```

## Examples

See `example_epistemic_metrics.py` for:
1. Basic POSTFLIGHT payload processing
2. Detecting epistemic health issues
3. JSON export for observability systems
4. Manual metric recording
5. Batch processing multiple sessions

Run:
```bash
python3 empirica/example_epistemic_metrics.py
```

## Integration Points

### With empirica CLI

Future: Integrate with `empirica postflight-submit` hook to auto-compute metrics.

### With Observability Stack

1. **Prometheus:** Scrape Prometheus endpoint at `localhost:8000/metrics`
2. **Loki:** Send structured logs via JSON body
3. **Jaeger:** Trace attributes attached to spans
4. **Dashboards:** Use metric labels for filtering/grouping

### With empirica-foundation-evaluator

The Evaluator seat can:
- Log metric violations as findings
- Flag calibration drift as high-risk
- Monitor trend of unknown accumulation
- Alert on artifact type discipline breaks
- Track goal completion velocity

## Design Principles

1. **Production-ready:** Error handling, sensible defaults, validated inputs
2. **Observable:** All metrics emit to Prometheus/OTEL
3. **Grounded:** Thresholds based on empirica best practices, not arbitrary
4. **Composable:** Individual metrics + compute_all_metrics() API
5. **Portable:** Minimal dependencies (Python stdlib + opentelemetry)

## Validation & Error Handling

All inputs are validated:

```python
# Vector values must be in [0.0, 1.0]
EpistemicVector("know", 1.5)  # ✗ ValidationError

# Artifact counts must be non-negative
metrics.ingest_artifacts({"findings": -1})  # ✗ ValidationError

# Phase status must be valid
metrics.add_goal("g1", "invalid_status")  # ✗ ValidationError
```

Validation errors are descriptive:
```
ValidationError: Vector 'know' value 1.5 outside [0.0, 1.0]
```

## Threshold Configuration

Thresholds can be customized via `MetricThreshold` enum:

```python
from epistemic_metrics import MetricThreshold

# Current defaults:
MetricThreshold.CALIBRATION_DRIFT_THRESHOLD.value  # 0.30
MetricThreshold.UNKNOWN_ACCUMULATION_THRESHOLD.value  # 10
MetricThreshold.GRAPH_DENSITY_THRESHOLD.value  # 0.50
MetricThreshold.GOAL_COMPLETION_THRESHOLD.value  # 0.70
```

To modify, edit the enum in `epistemic_metrics.py`.

## Troubleshooting

### "No module named 'opentelemetry'"

The module can operate without OTEL (metrics computed but not exported). Install for full functionality:
```bash
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-prometheus
```

### Calibration Drift Always High

Check for findings-only artifact pattern. Ensure unknowns/assumptions are logged whenever uncertainty > 0.3.

### Unknown Accumulation Growing

Investigate whether unknowns are being resolved. Check `unknown-resolve` logs in breadcrumbs.

### Graph Density Low

Ensure artifacts have edges. Use `log-artifacts` with `edges` field to create relationships:
```bash
empirica log-artifacts --nodes=[...] --edges=[{"from":"f1","to":"u1","relation":"grounded_by"}]
```

## Future Work

1. **Per-practice baselines** — Learn expected ranges for each practice
2. **Trend analysis** — Alert on degradation vectors
3. **Cross-session correlations** — Which metrics predict phase delays?
4. **Auto-calibration** — Suggested threshold adjustments based on data
5. **Composite scores** — Epistemic health index (weighted combination)

## References

- Empirica Practice Model: `/empirica-constitution`
- Epistemic Transactions: `/epistemic-transaction`
- OTEL Instrumentation: `otel_instrumentation.py`
- Test Suite: `test_epistemic_metrics.py`
- Examples: `example_epistemic_metrics.py`

---

**Status:** Stable for Phase 3.5.6
**Last updated:** 2026-07-31
**Maintained by:** empirica-foundation-evaluator practice
