# Autonomous Workflow Delegation Model
**Framework for distributed work across empirica-foundation practices**  
**Generated**: 2026-08-22 | **Status**: Ready for activation

---

## Overview

The personal dashboard (intent-os-universal-v2.html) is the **central coordination surface** for the Admiral (Carly). Work is delegated to specialized practices based on their domain expertise and current capacity. Each practice operates autonomously within its domain while reporting state through Cortex mesh collaboration.

---

## Component Allocation

| Component | Owner Practice | Responsibility | Trigger |
|-----------|---|---|---|
| **Dashboard UI** | empirica-foundation-evaluator | Cockpit surface, user interaction, state sync | User stress-tests dashboard |
| **Registry Gate** (cycle2_registry_gate.py) | empirica-autonomy | 3-outcome routing (ACCEPT/QUARANTINE/CANDIDATE) | Record submitted via API |
| **Scoring** (boundary_and_scorer.py) | empirica-autonomy | ROI scoring, feasibility assessment | ACCEPT outcome from gate |
| **Intent Reconciliation** | empirica-foundation-evaluator | Display stated vs revealed intent, surface gaps | System state changed |
| **Feedback Ledger** | empirica-mesh-support | Tri-source feedback aggregation (machine/system/user) | Issues reported or auto-detected |
| **Calibration Audit** | empirica-foundation-evaluator (Admiral) | Monitor practice performance, detect divergence | Weekly or observation-triggered |
| **Resource Harness** | empirica-outreach | Optimize labor/machine/capital split by mode | Mode selection in dashboard |

---

## Practice Responsibilities & Delegation Briefs

### 1. empirica-autonomy
**Domain**: Registry gates, scoring, 3-outcome routing  
**Why delegated**: Specialized in classification logic and anomaly detection  

**Responsibilities**:
- Implement `registry_gate()` with provenance verification
- Maintain attested_sources.json (registry of valid sources)
- Score ACCEPT-routed records for impact/feasibility/strategic fit
- Detect security threats (canary injection testing)
- Report gate performance metrics to mesh-support

**Success Criteria**:
- Gate processes 100+ records/day without errors
- Canary injection detection rate ≥ 99%
- Forged provenance rejection rate ≥ 90%
- Scoring latency < 200ms per record

**Escalation**: If gate rejection rate > 30%, flag to empirica-mesh-support (possible upstream data quality issue)

---

### 2. empirica-mesh-support
**Domain**: Feedback aggregation, tri-source ledger, issue triage  
**Why delegated**: Systems integrator; owns cross-practice coordination  

**Responsibilities**:
- Aggregate feedback from three sources:
  - Machine: self-reports, security rejects, performance alerts
  - System: runtime errors, constraint violations, schema mismatches
  - User: manual issue reports from dashboard
- Triage by severity (high/medium/low)
- Route issues to appropriate practice owners
- Monitor mesh communication health
- Provide weekly calibration audit reports

**Success Criteria**:
- Feedback triage < 5 min after report
- 100% of high-severity issues routed
- Mesh communication latency < 500ms
- Monthly audit reports delivered on schedule

**Escalation**: If tri-source feedback diverges significantly (e.g., machine happy but user reports > 10 issues), alert Admiral

---

### 3. empirica-outreach
**Domain**: Resource optimization, harness modes, capacity management  
**Why delegated**: Owns stakeholder communication and mode selection  

**Responsibilities**:
- Manage four harness modes (balanced/ai-led/human-led/capital-injection)
- Recommend mode based on:
  - Current project phase (discovery, build, test, deploy, measure)
  - Practice capacity (labor available, AI token budget, capital allocation)
  - Stakeholder preferences (Admiral input)
- Monitor resource utilization and flag bottlenecks
- Communicate mode changes to all practices via mesh

**Success Criteria**:
- Mode recommendations within 1 hour of request
- Resource forecasting accuracy > 80%
- Capacity warnings issued 48h+ in advance
- Zero resource conflicts between practices

**Escalation**: If multiple practices simultaneously hit resource caps, escalate mode decision to Admiral

---

### 4. empirica-foundation-evaluator (Admiral)
**Domain**: Orchestration, evaluation, governance  
**Why delegated**: Central authority over intent and system state  

**Responsibilities**:
- Use intent-os-universal-v2.html as personal stress-test dashboard
- Set primary instruction (the one thing that must execute flawlessly)
- Define stated intent (what you want the system to do)
- Observe revealed intent (what the system actually does)
- Call out observable gaps between stated and revealed
- Make GO/NO-GO decisions on proposed work (Z2 ratification)
- Approve final systems going live (Z3 landing)
- Monitor tri-source feedback and calibration drift

**Success Criteria**:
- Dashboard responsive (< 500ms page load)
- Stated vs revealed reconciliation < 5 min latency
- Admiral response to Z2 ratifications < 4 hours
- Calibration drift detected within 24h of occurrence

**Escalation**: If Admiral cannot ratify within 4h, workload escalates to mesh-support or human advisor

---

## Workflow: From Record Submission to Landing

```
[Admiral] issues primary instruction (stated intent)
   ↓
[User/System] submits record via dashboard form
   ↓
[API Bridge] receives POST /gate/registry
   ↓
[empirica-autonomy] processes via registry_gate()
   ├─ QUARANTINE → [empirica-mesh-support] logs security issue
   ├─ CANDIDATE → WIP queue (discovery lane)
   └─ ACCEPT → [empirica-autonomy] scores via scorer()
       ↓
       [Dashboard] updates pipeline (Propose count +1)
       ↓
       [Admiral] observes in Z2 Ratify column
       ↓
       [Admiral] decides: approve (Z2 ratification) OR reject
           ├─ Reject → issue logged to feedback ledger
           └─ Approve → moves to Z3 Landing (verification phase)
               ↓
               [empirica-mesh-support] verifies against operational constraints
               ↓
               [Dashboard] updates (Land column +1)
               ↓
               [System] executes landed decision
```

---

## Mesh Communication (Cortex)

Each practice monitors its queue via `/cortex-mailbox-poll` (30s intervals):

| Message Type | From | To | Frequency |
|---|---|---|---|
| **Collab** (questions/observations) | Any | mesh-support | As-needed |
| **Propose** (work request) | empirica-autonomy | mesh-support | Per record |
| **Ack** (completion) | Practice | Admiral | Per landing |
| **Alert** (escalation) | mesh-support | Admiral | High-severity only |
| **Weekly Report** | mesh-support | Admiral | Every Monday |

---

## Stress-Test Scenario (Admiral's Personal Use)

**Goal**: Verify system under load before full deployment

**Setup**:
1. Admiral opens intent-os-universal-v2.html
2. Sets harness to "ai-led" (higher machine allocation)
3. Submits 20 test records in rapid succession

**Expected Outcomes**:
- All 20 records gate + score within 5 seconds
- No canary injections reach scorer
- Feedback ledger captures any anomalies
- Dashboard updates smoothly (no UI lag)
- Mesh reports no communication timeouts

**Success**: Admiral observes clean pipeline flow (Propose → Ratify → Land) with < 5% latency spike

---

## Metrics & Monitoring

| Metric | Owner | Target | Check Frequency |
|--------|-------|--------|-----------------|
| Gate throughput | empirica-autonomy | 100+ records/day | Continuous |
| Scoring latency | empirica-autonomy | < 200ms p95 | Daily |
| Feedback triage time | empirica-mesh-support | < 5 min | Per-issue |
| Mesh latency | empirica-mesh-support | < 500ms | Hourly |
| Calibration drift | empirica-foundation-evaluator | < 0.05 Δ/day | Daily |
| Resource utilization | empirica-outreach | < 80% any mode | Daily |

---

## Activation Checklist

- [ ] api_bridge.py deployed and running on port 5000
- [ ] intent-os-universal-v2.html wired to API endpoints
- [ ] empirica-autonomy confirms registry_gate() and scorer() ready
- [ ] empirica-mesh-support confirms feedback ledger live
- [ ] empirica-outreach confirms harness modes configurable
- [ ] Cortex mailbox polling active on all practices
- [ ] Admiral completes stress-test scenario
- [ ] All practices acknowledge delegation brief (via mesh ack)

---

## Handoff Notes

**To empirica-autonomy**: Your registry_gate() and scorer() are the critical path. Any latency > 200ms will be immediately visible in Admiral's dashboard. Performance is your primary metric.

**To empirica-mesh-support**: You own the ledger and the mesh. Every issue that reaches Admiral has already been filtered through your triage. Escalation discipline is crucial.

**To empirica-outreach**: Harness modes are the knobs Admiral will turn. Your mode recommendations should explain trade-offs clearly (e.g., "ai-led gives 3x throughput but doubles token cost").

**To Admiral (Carly)**: The dashboard is yours to stress-test. Use it. Push it. Report what breaks. That feedback goes directly to practice owners via mesh acks.

---

*Framework ready for activation. Delegation is autonomous within domain; escalation is structured. Mesh communication is the coordination backbone.*
