# Phase 3.5 Orchestration Task Breakdown
## Sep 16, 2026 — Task Decomposition for 20 Orchestration Goals

### Goal 1: Phase 3.5 Deployment — Loki + Jaeger
**Status:** READY  
**Priority:** P0 (blocks Phase 3.5 gates)

#### Tasks:
- **3.5.1.1 Deploy Jaeger (distributed tracing)**
  - Apply jaeger-deployment.yaml to K8s
  - Verify pod status (running)
  - Health check: `/api/health` → 200
  - Estimate: 10 min

- **3.5.1.2 Deploy Loki (log aggregation)**
  - Apply loki-deployment.yaml to K8s
  - Verify Promtail sidecar health
  - Health check: `/ready` → 200
  - Estimate: 10 min

- **3.5.1.3 Smoke tests (Jaeger + Loki)**
  - Ingest test trace via gRPC
  - Ingest test logs via Promtail
  - Query both services
  - Estimate: 5 min

- **3.5.1.4 Integration validation**
  - Verify trace correlation (trace IDs match)
  - Verify Promtail → Loki pipeline
  - Confirm Jaeger UI loads
  - Estimate: 5 min

- **3.5.1.5 Readiness certification**
  - All smoke tests pass
  - Data flowing in both systems
  - Update Phase 3.5 status to DEPLOYED
  - Estimate: 2 min

**Total:** ~30 min; Owner: mesh-support + evaluator

---

### Goal 2: Phase 3.5 Instrumentation — Empirica Sessions → Observability
**Status:** DESIGN READY  
**Priority:** P0 (Phase 3.5 Task 4)

#### Tasks:
- **3.5.2.1 Wire empirica session logs → Loki**
  - Configure Promtail job: empirica-sessions
  - Parse JSON session logs (timestamp, level, message)
  - Add labels: ai_id, phase, practice
  - Estimate: 10 min

- **3.5.2.2 Wire practice stdout → Loki**
  - Configure regex parser for practice execution output
  - Tag logs by practice_id
  - Add severity classification
  - Estimate: 10 min

- **3.5.2.3 Wire ACAT metrics → Loki**
  - Ingest ACAT evaluation vectors as structured logs
  - Parse JSON (brier_error, predicted, actual)
  - Index by ai_id + vector_name
  - Estimate: 10 min

- **3.5.2.4 Validation: log ingestion rate**
  - Query Loki for empirica-sessions logs
  - Measure ingestion latency (p95, p99)
  - Confirm data freshness (< 5s lag)
  - Estimate: 5 min

- **3.5.2.5 Readiness handoff**
  - All 3 log sources flowing
  - Query performance acceptable
  - Document log schema
  - Estimate: 5 min

**Total:** ~40 min; Owner: evaluator (task 4)

---

### Goal 3: Phase 3.5 Dashboards — Observability Readiness
**Status:** SPEC READY  
**Priority:** P0 (Phase 3.5 Task 5)

#### Tasks:
- **3.5.3.1 Dashboard 1: Empirica Phase Latency**
  - PREFLIGHT → CHECK → POSTFLIGHT timeline
  - Track per-practice median latencies
  - Alert on >5min phases
  - Estimate: 15 min

- **3.5.3.2 Dashboard 2: Multi-Practice Request Traces**
  - Jaeger query: traces > 2 practices
  - Show end-to-end latency
  - Identify cross-practice bottlenecks
  - Estimate: 15 min

- **3.5.3.3 Dashboard 3: Epistemic Vectors (ACAT)**
  - Per-practice vector scores (13 vectors)
  - Confidence intervals from ACAT
  - Historical trend (week view)
  - Estimate: 20 min

- **3.5.3.4 Dashboard 4: SER Coordination Health**
  - SER state transitions per 1h window
  - Escalation frequency (red if >3/day)
  - Participants by practice
  - Estimate: 15 min

- **3.5.3.5 Dashboard 5-6: Integration + Handoff**
  - Combine dashboards into shared view
  - Add filtering (practice, phase, time)
  - Export as Grafana JSON
  - Estimate: 15 min

**Total:** ~80 min; Owner: evaluator (task 5)

---

### Goal 4: Phase 3.5 Validation — Data Quality & Performance
**Status:** CHECKLIST READY  
**Priority:** P1 (post-deployment)

#### Tasks:
- **3.5.4.1 Log ingestion validation**
  - Query all 3 log sources in Loki
  - Verify sample rate (empirica vs practice vs ACAT)
  - Check retention (30d hot per config)
  - Estimate: 10 min

- **3.5.4.2 Trace query performance**
  - Measure query latency: `/api/traces?service=...`
  - Target: < 1s for 1-week window
  - Verify sampling ratios per service
  - Estimate: 10 min

- **3.5.4.3 Dashboard rendering validation**
  - Load all 6 dashboards
  - Verify panel rendering (no errors)
  - Check data freshness (< 2min lag)
  - Estimate: 10 min

- **3.5.4.4 Cross-practice trace correlation**
  - Send test request: practice A → gateway → practice B
  - Verify trace ID continuity in Jaeger
  - Confirm logs correlated with traces
  - Estimate: 10 min

- **3.5.4.5 Phase 3.5 completion certification**
  - All validation checks pass
  - Data flowing at expected rates
  - No query timeouts
  - Sign-off ready for Phase 3.6
  - Estimate: 5 min

**Total:** ~45 min; Owner: evaluator + practices (task 5)

---

### Orchestration Goals 5-20: Coordination + Synchronization
**These are status collabs from mesh-support — moving to async replies**

Each remaining goal gets 1 coordinating task:
- **Task Pattern:** Acknowledge status → log finding → route to Phase 3.5 → close collab

Examples:
- Goal 5: Phase 3 Wave 1 → Status ack → wire to 3.5.1 deployment
- Goal 6: Phase 2.C.1 audits → Status ack → feeding Phase 3.5 baseline
- Goal 7-20: Benchmark assessments, routing verifications, etc. → Status ack → Phase 3+ coordination

**Total:** ~30 min (async batch processing of 16 collabs)

---

## Execution Sequence & Timeline

**Immediate (next 60 min):**
1. ✅ Critical blocker investigation → decision logged
2. ✅ Stuck loop + Phase 1→2 replies → sent
3. ⏳ **NOW:** Break down 20 goals into 60+ tasks (this document)
4. ⏳ **Next:** Commit task structure to git
5. ⏳ **Then:** Phase 3.5 deployment execution

**Phase 3.5 Execution (90 min total):**
- T+0–30min: Deploy Loki + Jaeger (3.5.1)
- T+30–70min: Instrumentation + validation (3.5.2)
- T+70–90min: Dashboards (3.5.3)
- T+90–180min: Full validation + sign-off (3.5.4)

**Critical Path:**
```
Deploy (30min) → Instrument (40min) → Dashboards (80min) → Validate (45min)
                = ~195 min (3.25 hours) to full Phase 3.5 completion
```

## Success Criteria (Phase 3.5)

✅ All 4 goal categories have task breakdown (≥5 tasks each)  
✅ Tasks are discrete and measurable  
✅ Loki + Jaeger deployed and healthy  
✅ All 3 log sources flowing into observability  
✅ 6 dashboards created and rendering  
✅ Cross-practice traces validated  
✅ Phase 3.5 completion certification signed  

