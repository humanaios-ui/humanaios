# Phase 3.6: Observable Claude Instrumentation — Design & Architecture

**Status**: DESIGN PHASE  
**Date**: 2026-08-04  
**Scope**: OTEL instrumentation for empirica lifecycle + 13-vector epistemic metrics  
**Integration**: Phase 3.5 observability stack (OTEL Collector → Prometheus → Grafana + Jaeger)

---

## Executive Summary

Phase 3.6 instruments the empirica framework to emit:
1. **Distributed traces** for transaction lifecycle (PREFLIGHT → noetic → CHECK → praxic → POSTFLIGHT)
2. **Epistemic metrics** for all 13 vectors (as Prometheus GaugeMetrics)
3. **Transaction context** (transaction_id, goal_id, practice_ai_id) correlated across traces and metrics

This integration flows into Phase 3.5 infrastructure:
- **Traces** → OTEL Collector (gRPC:4317) → Jaeger (16686) for distributed tracing UI
- **Metrics** → OTEL Collector (gRPC:4317) → Prometheus (9090) for time-series storage
- **Dashboards** → Grafana (3000) displays traces + metrics side-by-side per practice

---

## Architecture

### 1. Span Hierarchy (Traces)

```
Transaction Span [transaction_id, start_time, end_time]
├─ span: empirica:preflight
│  └─ attributes: vectors (initial), phase="NOETIC"
├─ span: empirica:noetic_phase
│  └─ child spans per operation (investigation-batch, grep, project-search)
│     └─ attributes: operation, path_or_query, duration_ms
├─ span: empirica:check
│  └─ attributes: gate_result (proceed/investigate), vectors_at_gate
├─ span: empirica:praxic_phase
│  └─ child spans per operation (edit, write, commit)
│     └─ attributes: operation, file_path, lines_changed
├─ span: empirica:postflight
│  └─ attributes: vectors (final), completion_score, artifacts_logged
└─ span: empirica:transaction_closed [commit_sha, artifacts_created]
```

**Span Naming Convention:**
- `empirica:preflight` — PREFLIGHT opens transaction, sets initial vectors
- `empirica:noetic_phase` — Noetic investigation work (reads, greps, searches)
- `empirica:check` — CHECK gate decision
- `empirica:praxic_phase` — Praxic execution work (edits, writes, commits)
- `empirica:postflight` — POSTFLIGHT closes transaction, logs final vectors + artifacts

**Transaction Context (trace-level attributes):**
```json
{
  "transaction_id": "uuid",
  "goal_id": "uuid",
  "practice_ai_id": "empirica-foundation-evaluator",
  "work_type": "code|research|docs|debug|infra|release|remote-ops",
  "phase": "noetic|praxic",
  "status": "open|in_investigation|gated_at_check|in_execution|closed"
}
```

### 2. Metric Design (Time Series)

**Metric Name Pattern:** `empirica_{vector_name}_{stat}`

| Vector | Metric Name | Type | Labels | Description |
|---|---|---|---|---|
| know | `empirica_know_gauge` | Gauge | transaction_id, practice | Self-assessed domain understanding |
| do | `empirica_do_gauge` | Gauge | transaction_id, practice | Execution ability |
| context | `empirica_context_gauge` | Gauge | transaction_id, practice | Surrounding state awareness |
| clarity | `empirica_clarity_gauge` | Gauge | transaction_id, practice | Path-forward clarity |
| coherence | `empirica_coherence_gauge` | Gauge | transaction_id, practice | Internal consistency |
| signal | `empirica_signal_gauge` | Gauge | transaction_id, practice | Information quality |
| density | `empirica_density_gauge` | Gauge | transaction_id, practice | Knowledge per context unit |
| state | `empirica_state_gauge` | Gauge | transaction_id, practice | System state awareness |
| change | `empirica_change_gauge` | Gauge | transaction_id, practice | Amount of change made |
| completion | `empirica_completion_gauge` | Gauge | transaction_id, practice | Progress toward phase goal |
| impact | `empirica_impact_gauge` | Gauge | transaction_id, practice | Significance to project |
| engagement | `empirica_engagement_gauge` | Gauge | transaction_id, practice | Active engagement level |
| uncertainty | `empirica_uncertainty_gauge` | Gauge | transaction_id, practice | Unknowns remaining |

**Meta Metrics (transaction-level):**
- `empirica_transaction_duration_seconds` (Histogram: elapsed time)
- `empirica_artifacts_logged_total` (Counter: finding, decision, unknown, dead-end, etc.)
- `empirica_commits_total` (Counter: commits created)
- `empirica_noetic_duration_seconds` (Histogram: time in noetic phase)
- `empirica_praxic_duration_seconds` (Histogram: time in praxic phase)

### 3. Integration Points

#### OTEL Collector (Already Running)
```yaml
# receiver: OTLP gRPC at localhost:4317
# receiver: OTLP HTTP at localhost:4318
# exporter: Jaeger at localhost:14268 (traces)
# exporter: Prometheus at localhost:8889 (metrics)
```

**Update needed:** Update `otel-collector-config.yml` to bump service.version from "3.4" to "3.6" and deployment.environment from "phase-3.4" to "phase-3.6"

#### Instrumentation Library API

**Module:** `empirica/otel_instrumentation.py`

```python
class OTELInstrumentation:
    def __init__(self, service_name: str = "empirica-foundation-evaluator"):
        """Initialize OTEL tracer + meter (auto-connects to OTEL Collector at localhost:4317)"""
        self.tracer = trace.get_tracer("empirica", version="3.6")
        self.meter = metrics.get_meter("empirica", version="3.6")
        self.metrics = {}  # {vector_name: GaugeMetric}

    def start_transaction(self, transaction_id: str, goal_id: str, work_type: str) -> Span:
        """Open transaction span (called by empirica preflight-submit)"""
        span = self.tracer.start_span(
            "empirica:transaction",
            attributes={
                "transaction_id": transaction_id,
                "goal_id": goal_id,
                "practice_ai_id": "empirica-foundation-evaluator",
                "work_type": work_type,
                "status": "open"
            }
        )
        self._root_span = span  # store for linking child spans
        return span

    def phase_span(self, phase_name: str, attributes: dict = None) -> Span:
        """Emit span for phase (noetic, CHECK, praxic, POSTFLIGHT)"""
        attrs = {"phase": phase_name, **(attributes or {})}
        return self.tracer.start_span(f"empirica:{phase_name}", attributes=attrs)

    def operation_span(self, operation_name: str, attributes: dict = None) -> Span:
        """Emit span for individual operation (read, write, grep, commit, etc.)"""
        attrs = {"operation": operation_name, **(attributes or {})}
        return self.tracer.start_span(f"empirica:op_{operation_name}", attributes=attrs)

    def emit_vector_metrics(self, vectors: dict[str, float]) -> None:
        """Emit 13-vector gauge metrics (called at PREFLIGHT and POSTFLIGHT)"""
        for vector_name, value in vectors.items():
            metric_key = f"empirica_{vector_name}_gauge"
            if metric_key not in self.metrics:
                self.metrics[metric_key] = self.meter.create_gauge(metric_key)
            self.metrics[metric_key].observe(value, {
                "transaction_id": getattr(self, "_current_transaction_id", "unknown"),
                "practice": "empirica-foundation-evaluator"
            })

    def emit_artifact_metric(self, artifact_type: str) -> None:
        """Emit counter for artifacts logged (finding, decision, unknown, etc.)"""
        counter = self.meter.create_counter("empirica_artifacts_logged_total")
        counter.add(1, {"artifact_type": artifact_type})

    def close_transaction(self, commit_sha: str = None) -> None:
        """Close transaction span and flush metrics"""
        if hasattr(self, "_root_span"):
            self._root_span.set_attribute("status", "closed")
            if commit_sha:
                self._root_span.set_attribute("commit_sha", commit_sha)
            self._root_span.end()
```

#### CLI Hooks (Automatic Instrumentation)

**File:** `.empirica/hooks/preflight-post.py` (runs after `empirica preflight-submit`)

```python
#!/usr/bin/env python3
"""Post-PREFLIGHT hook: emit span + initialize metrics"""

import json
import subprocess
from empirica.otel_instrumentation import OTELInstrumentation

# Read PREFLIGHT result from empirica session
result = json.loads(subprocess.check_output(["empirica", "session-read", "--format", "json"]))

instr = OTELInstrumentation()
instr.start_transaction(
    transaction_id=result["transaction_id"],
    goal_id=result["goal_id"],
    work_type=result["work_type"]
)
instr.emit_vector_metrics(result["vectors"])
```

**File:** `.empirica/hooks/postflight-post.py` (runs after `empirica postflight-submit`)

```python
#!/usr/bin/env python3
"""Post-POSTFLIGHT hook: emit final vectors + close span"""

import json
import subprocess
from empirica.otel_instrumentation import OTELInstrumentation

result = json.loads(subprocess.check_output(["empirica", "session-read", "--format", "json"]))

instr = OTELInstrumentation()
instr.emit_vector_metrics(result["vectors"])
instr.emit_artifact_metric(count=result["artifacts_created_count"])
instr.close_transaction(commit_sha=result["last_commit_sha"])
```

### 4. Trace-to-Dashboard Flow

```
1. Application Code
   └─ OTEL SDK (Python)
      └─ Span + Metric Emission
         ├─ Transaction span (context)
         ├─ Phase spans (noetic/CHECK/praxic/postflight)
         ├─ Operation spans (read/write/grep/commit)
         └─ 13-vector metrics (gauges)

2. OTEL Collector (localhost:4317)
   ├─ Receives: Traces via OTLP gRPC
   ├─ Processes: Batch + Memory Limiter + Attributes
   ├─ Exports: Traces → Jaeger (14268)
   ├─ Exports: Metrics → Prometheus Exporter (8889)
   └─ Status: Health check at 8889/metrics

3. Prometheus (localhost:9090)
   ├─ Scrapes: OTEL Collector metrics endpoint (8889)
   ├─ Stores: Time series (13-vector gauges, transaction counters, phase durations)
   ├─ Retention: 30 days (configurable)
   └─ Status: Health check at 9090/-/healthy

4. Grafana (localhost:3000)
   ├─ Datasource 1: Prometheus (metrics + gauges)
   ├─ Datasource 2: Jaeger (traces)
   ├─ Dashboard 1: Per-practice epistemic vectors (time series)
   ├─ Dashboard 2: Transaction phase breakdown (Jaeger traces)
   └─ Dashboard 3: Artifact production rate (counter metrics)
```

---

## Implementation Tasks (Phased)

### Phase 3.6.1: Core Instrumentation Library (2026-08-05 to 2026-08-18)

**Task 1.1:** Create `empirica/otel_instrumentation.py`
- Initialize tracer + meter
- Implement span lifecycle (start_transaction, phase_span, operation_span, close_transaction)
- Implement metric emission (emit_vector_metrics, emit_artifact_metric)
- Connection to OTEL Collector at localhost:4317

**Task 1.2:** Create `empirica/epistemic_metrics.py`
- Map 13-vector names to Prometheus metric names
- Define meta-metrics (duration, artifact count, commit count)
- Utilities for converting vector dicts to metric observations

**Task 1.3:** Create CLI hooks
- `.empirica/hooks/preflight-post.py` — initialize span + emit initial vectors
- `.empirica/hooks/postflight-post.py` — finalize span + emit final vectors + artifact counts
- Hook registration in `.empirica/settings.json`

**Success Criteria:**
- Spans visible in Jaeger UI for a sample transaction
- Metrics appearing in Prometheus scrape (`curl localhost:9090/api/v1/query?query=empirica_*`)
- CLI hooks execute automatically on preflight-submit and postflight-submit

### Phase 3.6.2: Grafana Integration (2026-08-19 to 2026-09-01)

**Task 2.1:** Update Grafana datasources
- Add Prometheus datasource (if not already present)
- Add Jaeger datasource (if not already present)

**Task 2.2:** Create per-practice epistemic dashboard
- Panel 1: 13-vector time series (stacked area or line chart)
- Panel 2: Transaction phase breakdown (bar chart: noetic_duration, praxic_duration)
- Panel 3: Artifact production rate (counter: findings, decisions, artifacts per day)
- Panel 4: Jaeger trace explorer (drill down into any transaction)

**Task 2.3:** Create transaction detail dashboard
- Span timeline (Gantt chart showing span durations)
- Vector progression (vectors at preflight vs. postflight)
- Commit sha + artifact links

**Success Criteria:**
- Dashboards load without errors
- Metrics are visible and updating in real-time
- Traces are clickable and link to Jaeger

### Phase 3.6.3: Testing & Integration (2026-09-02 to 2026-09-15)

**Task 3.1:** Integration tests
- Mock a sample transaction (PREFLIGHT → noetic → CHECK → praxic → POSTFLIGHT)
- Verify spans appear in Jaeger within 5 seconds
- Verify metrics appear in Prometheus within 10 seconds
- Verify correlation between transaction_id across traces and metrics

**Task 3.2:** End-to-end test (live)
- Create a real empirica transaction (preflight-submit with sample work)
- Manually verify in Jaeger UI (traces visible)
- Manually verify in Prometheus UI (metrics present)
- Manually verify in Grafana UI (dashboards updated)

**Task 3.3:** Performance / resource impact
- Measure memory overhead of instrumentation library
- Measure latency impact on empirica operations
- Ensure OTEL Collector doesn't degrade Prometheus scrape performance

**Success Criteria:**
- All integration tests passing
- End-to-end test validates full flow (span → Jaeger, metric → Prometheus → Grafana)
- Resource overhead < 5% CPU, < 50MB memory

### Phase 3.6.4: Documentation & Runbook (2026-09-16 to 2026-09-30)

**Task 4.1:** Developer guide
- How to enable instrumentation (environment variable? opt-in hook?)
- How to interpret traces in Jaeger (span hierarchy, attributes)
- How to query metrics in Prometheus (PromQL examples)
- How to use Grafana dashboards (filtering, time ranges)

**Task 4.2:** Runbook: Troubleshooting
- "Traces not appearing in Jaeger" → checklist
- "Metrics not appearing in Prometheus" → checklist
- "OTEL Collector health check failing" → checklist

**Task 4.3:** Update Phase 3.5 documentation
- Mention Phase 3.6 integration
- Link to new Phase 3.6 dashboards
- Update OTEL Collector config (3.4 → 3.6)

**Success Criteria:**
- Developer guide is clear and complete
- Runbook resolves all known issues
- Phase 3.5 + 3.6 docs are integrated

---

## Dependencies & Blockers

**No Blockers Identified:**
- OTEL Collector already running ✓
- Prometheus already configured ✓
- Grafana already available ✓
- Jaeger already running ✓
- Phase 3.5 observability stack complete (2/3) ✓

**Optional Enhancements (Post-Phase 3.6):**
- Span sampling (send 10% of spans to reduce cardinality)
- Custom attributes for A/B testing (model version, practice-specific signals)
- Alerting rules for epistemic health (e.g., "uncertainty > 0.6 for >30min")

---

## Success Metrics (Phase 3.6 Completion)

By end of Phase 3.6 (2026-09-30):

- ✅ **Traces:** OTEL spans emitted for all empirica lifecycle events (PREFLIGHT/noetic/CHECK/praxic/POSTFLIGHT)
- ✅ **Metrics:** 13-vector gauges flowing to Prometheus in real-time
- ✅ **Dashboards:** Per-practice epistemic trends visible in Grafana
- ✅ **Integration:** Traces and metrics correlated by transaction_id end-to-end
- ✅ **Zero Breaking Changes:** Empirica framework unchanged, instrumentation is opt-in
- ✅ **Grader Version Locked:** Claude Haiku 4.5 baseline established, bridging study protocol defined for future upgrades
- ✅ **Testing:** Integration tests passing, end-to-end test validates full Jaeger → Prometheus → Grafana flow

---

## Related

- **Phase 3.5**: Observability Stack (Jaeger, Prometheus, Grafana) — COMPLETE (2/3, Loki deferred)
- **Phase 3.4**: Alerting Rules & OTEL Collector — COMPLETE
- **Phase 3.6.1**: Observable Claude Instrumentation — THIS PHASE
- **Phase 3.7**: SLO/SLI Tracking (deferred)
- **Constitution**: §I (phase-aware completion), §II (cognitive immune system), §IV (practice model)

---

**Status:** Design Complete — Ready for Implementation Kickoff (2026-08-05)

