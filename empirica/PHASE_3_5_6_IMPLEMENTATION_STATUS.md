# Phase 3.5.6: Observable Claude - Empirica Instrumentation
## Implementation Status & Architecture

### Current Status (Live)

| Phase | Status | Files | Notes |
|-------|--------|-------|-------|
| **Phase 1: OTEL Integration** | ✅ COMPLETE | `otel_instrumentation.py`, `test_otel_instrumentation.py` | Tracer + meter providers active, OTEL Collector running (port 4317 gRPC, 8889 Prometheus) |
| **Phase 2: CLI Instrumentation** | ✅ COMPLETE | `cli_instrumentation_hooks.py`, `example_cli_instrumentation.py` | Command classification, span lifecycle, context extraction working |
| **Phase 3: Epistemic Metrics** | 🔄 IN PROGRESS | `epistemic_metrics.py` (agent building) | Unknown accumulation, calibration drift, graph density, type violations |
| **Phase 4: Dashboard** | 🔄 IN PROGRESS | `grafana_dashboard_seat_health.json` (agent building) | 4-panel grid: seat epistemic health, phase breakdown, task service, correlation |
| **Phase 5: Alerting Rules** | ✅ PREPARED | `empirica_seat_alerting_rules.yaml` | 10 alert rules covering stalls, accumulation, calibration drift, gate imbalance |
| **Phase 6: Documentation** | 📋 PENDING | `INSTRUMENTATION_GUIDE.md` (TODO) | Usage patterns, deployment instructions, troubleshooting |

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Empirica CLI                                 │
│  (preflight-submit, check-submit, postflight-submit, etc.)      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│           CLI Instrumentation Hooks (Phase 2)                   │
│  - Command classification (PREFLIGHT/noetic/CHECK/praxic/       │
│    POSTFLIGHT)                                                   │
│  - Context extraction from JSON payloads                        │
│  - Span lifecycle (open/close at phase boundaries)              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│         OTEL Instrumentation (Phase 1)                          │
│  - TracerProvider (gRPC export to localhost:4317)               │
│  - MeterProvider (Prometheus export to :8889)                   │
│  - Span attributes, metric recording                            │
│  - Epistemic Metrics Integration (Phase 3)                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
    ┌────────┐      ┌──────────┐   ┌────────┐
    │ Jaeger │      │Prometheus│   │  Task  │
    │  UI    │      │  Server  │   │Service │
    │:16686  │      │  :9090   │   │Metrics │
    └────────┘      └──────────┘   └────────┘
                         │
                         ▼
    ┌─────────────────────────────────┐
    │  Grafana Dashboard (Phase 4)    │
    │  - Empirica Seat Health Panel   │
    │  - Phase Duration Breakdown     │
    │  - Task Service Correlation     │
    │  - Infrastructure + Epistemic   │
    └─────────────────────────────────┘
                         │
                         ▼
    ┌─────────────────────────────────┐
    │  AlertManager (Phase 5)         │
    │  - Investigation Stalls         │
    │  - Unknown Accumulation         │
    │  - Calibration Drift            │
    │  - Type Discipline Violations   │
    └─────────────────────────────────┘
```

### Phase 3: Epistemic Metrics (In Progress)

**Expected deliverables:**
- `epistemic_metrics.py` module with `EpistemicHealthMetrics` class
- Metrics:
  - `empirica_unknowns_total` (counter)
  - `empirica_calibration_drift` (gauge-via-histogram)
  - `empirica_investigation_latency_seconds` (histogram)
  - `empirica_artifact_type_violations_total` (counter)
  - `empirica_graph_density` (gauge-via-histogram)
  - `empirica_goals_completion_ratio` (counter)
  - `empirica_phase_transition_speed` (histogram)
- Integration with OTEL instrumentation (Phase 1)
- POSTFLIGHT payload parsing

### Phase 4: Grafana Dashboard (In Progress)

**Expected deliverables:**
- `grafana_dashboard_seat_health.json` (Grafana 8.0+ compatible)
- 4-panel layout:
  1. **Epistemic Health**: unknown count, calibration drift, investigation latency
  2. **Phase Breakdown**: bar chart of average phase durations
  3. **Task Service Health**: queue depth, active workers, latency
  4. **Correlation Graph**: seat activity vs infrastructure load

### Phase 5: Alerting Rules (Ready)

**10 Alert Rules Configured:**
1. Investigation Stall (60+ min no noetic activity)
2. Unknown Accumulation (> 5 unresolved)
3. Critical Unknown Accumulation (> 10)
4. Type Discipline Violation
5. Calibration Drift (> 0.3)
6. Critical Calibration Drift (> 0.5)
7. Goal Completion Stall (no progress in 30 min)
8. CHECK Gate Imbalance (blocks > 50%)
9. Long Noetic Phase (> 1 hour)
10. Correlation: Latency during investigation + high queue

**Location:** `agent/empirica_seat_alerting_rules.yaml`
**Deployment:** Import into AlertManager Prometheus config

### Metrics Data Flow

```
POSTFLIGHT JSON Payload
    │
    ├─ work_type, vectors, findings, unknowns, goals
    │
    ▼
Epistemic Metrics Module (Phase 3)
    │
    ├─ Calculate calibration_drift (vector vs evidence)
    ├─ Count unknown_accumulation
    ├─ Measure graph_density (connected/total artifacts)
    ├─ Track type_violations (if findings-only collapse)
    ├─ Record phase_durations
    │
    ▼
OTEL Meter
    │
    ├─ Histogram.record() for latency metrics
    ├─ Counter.add() for accumulation metrics
    │
    ▼
Prometheus Exporter (port 8889)
    │
    ▼
Prometheus Server (port 9090)
    │
    ├─ Metric scrape every 30s
    │
    ▼
Grafana Dashboard (queries Prometheus)
    │
    ├─ Display real-time seat health
    ├─ Correlate with task service metrics
    │
    ▼
AlertManager (evaluates alerting rules)
    │
    ├─ Fire alerts when thresholds exceeded
    ├─ Route to Slack #alerts-epistemic
```

### Integration Checklist

- [ ] Phase 3 (`epistemic_metrics.py`) complete
- [ ] Phase 4 (`grafana_dashboard_seat_health.json`) complete
- [ ] Integrate Phase 3 metrics into `otel_instrumentation.py`
- [ ] Add alerting rules to AlertManager config
- [ ] Test full flow: POSTFLIGHT → metrics → Prometheus → Grafana
- [ ] Document patterns in `INSTRUMENTATION_GUIDE.md`
- [ ] Commit Phases 3-5 work
- [ ] Create example: full transaction with all metrics visible in Grafana

### Testing Plan

1. **Unit Tests:** epistemic_metrics.py validation
2. **Integration Test:** CLI → OTEL → Prometheus → Grafana
3. **Alert Test:** Trigger each alert rule manually
4. **Correlation Test:** Run task service + seat concurrently, verify dashboard correlation
5. **Production Readiness:** 24-hour stability run with real empirica workloads

### Known Dependencies

- OTEL Collector must be running (port 4317 gRPC)
- Prometheus must scrape port 8889 (OTEL Collector's Prometheus endpoint)
- Grafana must have Prometheus data source configured
- AlertManager must have alerting rules loaded

### Next Steps

1. ✅ Phase 3 agent completes: `epistemic_metrics.py`
2. ✅ Phase 4 agent completes: Grafana dashboard JSON
3. Integrate Phase 3 → Phase 1 (wire epistemic metrics into OTEL)
4. Test full pipeline (POSTFLIGHT → metrics → Prometheus → Grafana → alerts)
5. Commit Phase 3, 4, 5 work
6. Create Phase 6: `INSTRUMENTATION_GUIDE.md` for other practices
7. Final POSTFLIGHT for Phase 3.5.6

---

**Status:** Parallel agents working on Phase 3 & 4 | Ready for Phase 5 & 6 integration
