# Phase 3.4 Execution Plan: Observability Stack Deployment
## Foundation Orchestration — September 16, 2026

---

## OVERVIEW

**Goal:** Stand up production observability infrastructure enabling end-to-end metrics collection, visualization, and distributed tracing across 15-practice foundation orchestration.

**Scope:** Prometheus, Grafana, OpenTelemetry collector + exporters (Jaeger, Loki)
**Resource Budget:** Tokens for config, testing, integration validation
**Unblocks:** Phase 3.5 (measurement baseline convergence), Phase 3.6 (Observable Claude instrumentation)

---

## ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│ 15 PRACTICES (9 Foundation + 6 Cross-Org)                       │
│ ├─ Emit metrics to :800X/metrics (Prometheus scrape)            │
│ ├─ Emit traces to OTEL collector:4317/4318 (OTLP gRPC/HTTP)    │
│ └─ Push logs to OTEL collector                                   │
└────────────────────┬────────────────────────────────────────────┘
                     │
     ┌───────────────┴───────────────┐
     │                               │
┌────▼────────────────────┐  ┌──────▼──────────────────┐
│ Prometheus :9090        │  │ OTEL Collector :4317    │
│ ├─ Scrape 15 practices  │  │ ├─ Ingest traces/logs   │
│ ├─ Time-series storage  │  │ ├─ Batch processing     │
│ └─ 15-day retention     │  │ └─ Export to backends   │
└────┬────────────────────┘  └──────┬──────────────────┘
     │                              │
     │    ┌────────────────────────┬┴─────────────────┐
     │    │                        │                  │
┌────▼────▼──────┐    ┌───────────▼────┐    ┌────────▼─────────┐
│ Grafana :3000  │    │ Jaeger :16686  │    │ Loki :3100       │
│ ├─ Dashboards  │    │ ├─ Traces view │    │ ├─ Log retention │
│ ├─ Alerting    │    │ └─ Latency     │    │ └─ Correlate     │
│ └─ Multi-user  │    │    analysis    │    │    logs + traces │
└────────────────┘    └────────────────┘    └──────────────────┘
```

---

## TASK BREAKDOWN

### Task 1: Prometheus Setup & Configuration ✓ (In Progress)
**Deliverables:**
- prometheus.yml: Scrape configs for 15 practices (9 foundation + 6 cross-org)
- Practice endpoints defined: :8001-:8015 (unique port per practice)
- Recording rules: PromQL rules for computed metrics
- Retention: 15 days, 500GB storage
- Self-monitoring: Prometheus metrics on :9090/metrics

**Validation:** Scrape success rate > 99%, zero missing targets

**Handoff to Task 2:** Once metrics flowing, Grafana dashboards consume them

---

### Task 2: Grafana Dashboards & Visualization (Queued)
**Deliverables:**
1. **Orchestration Health Dashboard**
   - Phase progress gauge, goal timeline, blocker count
   - Practice participation heatmap, SER state summary
   - Alerting thresholds: critical blocker count > 2, phase velocity < 5%

2. **Resource Consumption Dashboard**
   - Cumulative labor hours, token consumption, burn rate
   - Practice bandwidth allocation (radar), efficiency ratio
   - Alerting: token spend > 80%, burn > 200k/txn

3. **Per-Practice Metrics Dashboard**
   - Template dashboard repeated for each of 15 practices
   - Transactions, uncertainty trend, artifact production
   - Drop-down filtering by practice

4. **Measurement Baseline Dashboard**
   - P0/P50/P99 latencies (cold+warm baselines)
   - Vector delta distributions, artifact count stats
   - Success criteria display (baseline sample count, latency gates)

5. **Trace View Dashboard**
   - Distributed trace latency heatmap
   - Span count by practice, error rate by span type
   - Critical path identification

**Validation:** All dashboards queryable, alerts firing correctly

---

### Task 3: OpenTelemetry Collector & Tracing (Queued)
**Deliverables:**
- otel-collector-config.yaml: OTLP receivers, processors, exporters
- Receiver: gRPC (:4317) + HTTP (:4318) OTLP ingestion
- Processors: attributes (add cluster/environment), span naming, 100% sampling
- Exporters: Jaeger (traces), Loki (logs), Prometheus (metrics)
- Instrumentation guide: How to emit spans from evaluator + pilot practices

**Validation:** End-to-end trace from emit → Jaeger query view

**Pilot practices:** Evaluator + 3 volunteers (mesh-support, autonomy, resource-miner)

---

### Task 4: Measurement Baseline Establishment (Queued)
**Deliverables:**
- Cold-start baseline: Evaluator init → first goal completion
  - Sample count: > 30 runs
  - Captures: P0, P50, P99 latencies, vector deltas, artifact counts
  
- Warm-start baseline: 2nd–Nth transactions
  - Shows steady-state performance
  - Identifies any degradation patterns

- Baseline metrics document: JSON + Markdown summary
  - Mean, median, IQR for latencies
  - Artifact distributions (findings, unknowns, decisions per txn)
  - Calibration confidence trends

**Validation:** Baseline sample size > 30, latency distribution normal

**Used by Phase 3.5:** Convergence analysis compares later runs against baseline

---

### Task 5: Integration Testing & Validation (Queued)
**Test 1: Metric Flow**
- Emit metric from practice → Prometheus scrape → Grafana query → verify value
- Repeat for 5+ practices
- Verify label consistency (practice, org, tier)

**Test 2: Trace Flow**
- Emit span from evaluator → OTEL collector → Jaeger → query latency
- Verify span attributes (transaction_id, goal_id, practice_id)
- Measure end-to-end trace latency (should be < 100ms)

**Test 3: Cross-Practice Correlation**
- Practice A emits metric change → verify visible in Grafana across B,C,D
- Tests that shared context (resource pool, SER state) is observable

**Test 4: Measurement Gate Readiness**
- SLO checks: data freshness, cardinality, completeness
- Sample size checks: > 30 baseline samples collected
- Quality gates: > 95% non-null data points

**Validation:** All 4 tests green before Phase 3.5 kickoff

---

### Task 6: Phase 3 Gate Readiness Verification (Queued)
**Checklist:**
- [ ] Prometheus: all 15 practices reporting metrics, scrape rate > 99%
- [ ] Grafana: all 5 dashboards live, queries responsive < 200ms
- [ ] OTEL Collector: ingesting traces, exporting to Jaeger/Loki
- [ ] Baseline: > 30 samples collected, distribution analysis complete
- [ ] Integration tests: 4/4 passing
- [ ] No critical bugs: logging, metric cardinality, trace sampling
- [ ] Phase 3.5 ready: baseline data structured for convergence analysis
- [ ] Phase 3.6 ready: Observable Claude instrumentation can begin

**Sign-off:** Phase 3.4 complete, Phase 3.5 green to proceed

---

## SUCCESS CRITERIA

| Criterion | Target | Evidence |
|-----------|--------|----------|
| Metric collection | 99%+ scrape success | Prometheus target state page |
| Dashboard responsiveness | < 200ms query latency | Grafana browser inspect |
| Trace sampling | 100% in Phase 3.4 | OTEL sampling_percentage=100 |
| Baseline samples | > 30 | Baseline JSON: `sample_count` field |
| Integration tests | 4/4 passing | Test results document |
| Alert thresholds | Calibrated + firing | Example alert log |
| Cross-practice visibility | Observable correlations | Grafana dashboard screenshot |

---

## TIMELINE (Resource-Accounting)

Estimated resource consumption:
- **Human labor:** 2–4 hours (evaluator, mesh-support pair-programming)
- **AI tokens:** 150k–250k (config generation, testing, validation)
- **Evaluator bandwidth:** ~40% of Phase 3.4 execution
- **Mesh-support bandwidth:** ~30% (OTEL troubleshooting, pilot instrumentation)
- **Foundation practices:** ~20% (sending metrics + traces)

**Execution order:** Tasks 1→2→3 in parallel, 4 concurrent with 2+3, then 5+6

