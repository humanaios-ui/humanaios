---
title: "Mesh Observability & Telemetry Infrastructure"
subtitle: "Complete observability across all 13 empirica-foundation practices"
date: "2026-08-15"
version: "1.0-DESIGN"
status: "READY FOR IMPLEMENTATION"
authority: "Admiral (Carly R. Anderson), evaluator practice"
---

# Mesh Observability & Telemetry Infrastructure

**Objective:** Establish complete, real-time observability across all 13 practices in the empirica-foundation ecosystem. Enable proactive monitoring, trend analysis, and mesh health dashboards.

**Current State:** POSTFLIGHT data collected for 1 practice (evaluator), aggregated in `.postflight/INDEX.yaml`. Need to expand to 13 practices.

**Timeline:** Aug 15 - Sep 10 (pre-launch coordination phase)

---

## PART A: Current POSTFLIGHT Infrastructure (Evaluator Only)

### Existing Structure

```
.postflight/
├── INDEX.yaml                  ← Master aggregation (7 sessions, 1 practice)
├── MANIFEST.md                 ← Navigation guide
├── 2026-08-14/
│   └── session.yaml            ← Per-session details
└── [Framework docs]            ← Supporting research
```

### Data Currently Collected

**From Evaluator Transactions:**
- 13 epistemic vectors (know, do, context, clarity, coherence, signal, density, state, change, completion, impact, engagement, uncertainty)
- Goal health (19 total, 8 completed, 9 in progress)
- Mesh response times (6 practices tracked, 1 showing NEEDS_ATTENTION)
- Decision timeline (11 decisions, 4 due within 30 days)
- Calibration metrics (variance 0.10, accuracy 0.94)

### Gap: Missing Data

**NOT currently collected:**
- Individual practice POSTFLIGHT results (only evaluator)
- Mesh-wide goal health (only evaluator's view)
- Per-practice calibration (only evaluator)
- Cross-practice dependencies + blocker cascade
- Real-time mesh event stream (collabs, proposals, completions)
- Performance metrics per practice (latency, throughput, reliability)
- Practice-specific burnout signals
- Autonomous watch-sweep status (missed items, stalled proposals)

---

## PART B: Extended Observability Architecture (13 Practices)

### Target: Unified Telemetry Layer

```
┌─────────────────────────────────────────────────────────────┐
│  UNIFIED MESH OBSERVABILITY LAYER                           │
│  (Evaluator as the collection + aggregation point)          │
└─────────────────────────────────────────────────────────────┘
              ↓
    ┌─────────────────────────────────────────┐
    │  DATA INGESTION (from 13 practices)      │
    │  - POSTFLIGHT vectors (13 × 13 vectors) │
    │  - Goal health snapshots                 │
    │  - Mesh event logs (collabs, proposals)  │
    │  - Calibration reports                   │
    └─────────────────────────────────────────┘
              ↓
    ┌─────────────────────────────────────────┐
    │  AGGREGATION & ANALYSIS                  │
    │  - Mesh-wide trends (by dimension)       │
    │  - Practice responsiveness + health      │
    │  - Blocker cascade analysis              │
    │  - Burnout + sustainability signals      │
    │  - Autonomy watch-sweep status           │
    └─────────────────────────────────────────┘
              ↓
    ┌─────────────────────────────────────────┐
    │  DASHBOARDS & ALERTS                     │
    │  - Mesh health dashboard (real-time)     │
    │  - Practice profiles (weekly)            │
    │  - Trend reports (bi-weekly)             │
    │  - Incident alerts (on anomaly)          │
    └─────────────────────────────────────────┘
```

### Data Collection Sources

| Source | Data | Frequency | Owner |
|--------|------|-----------|-------|
| **POSTFLIGHT** | 13 vectors, goal health, calibration | Per transaction (per practice) | Each practice |
| **Cortex mailbox** | Collab/proposal events, response times, SLA compliance | Real-time (via listener) | mesh-support (polling) |
| **Empirica goals** | Goal creation, updates, completion, task progress | Per operation | Each practice |
| **Artifact logs** | Finding/decision/assumption/unknown breadth, epistemic sources | Per transaction | Each practice |
| **Autonomy watch** | Stalled proposals, dropped items, retry events | Hourly sweep | autonomy |

---

## PART C: Implementation Plan (Phase 1: Aug 15-Sep 10)

### Stage 1: Data Collection Infrastructure (Week 1-2: Aug 15-24)

**Goal:** Build the data ingestion layer to collect POSTFLIGHT + telemetry from all 13 practices.

#### Task 1.1: Standardize POSTFLIGHT Output Across Practices

**What:** Each practice must emit a consistent POSTFLIGHT JSON with:
- Session metadata (date, practice_id, transaction_id)
- All 13 vectors
- Goal health (completed/in-progress/planned counts)
- Mesh events (inbox items, outgoing collabs, response times)
- Calibration metrics (variance, accuracy on predictions)

**Action:** Create a `POSTFLIGHT_SCHEMA.json` template. Each practice's empirica CLI already emits POSTFLIGHT JSON—just need to normalize field names + add mesh metrics.

**Owner:** evaluator (schema) + each practice (adoption)  
**Effort:** 3h per practice to integrate schema into their POSTFLIGHT emission  
**Timeline:** Aug 15-20

#### Task 1.2: Set Up Telemetry Ingestion (Evaluator → Cortex)

**What:** Evaluator polls Cortex for mesh events (collabs, proposals, completions) and correlates with practice POSTFLIGHT data.

**Mechanism:**
```bash
# Hourly: Cortex event log ingestion
empirica loop register --name mesh-telemetry-ingest --kind interval \
  --interval 1h \
  --description "Poll Cortex for mesh events (collabs, proposals, completions) + correlate with practice POSTFLIGHT"

# Body: 
# 1. cortex_inbox_poll(ai_id=<each-practice>) → event times, response times
# 2. cortex_outbox_poll(ai_id=<each-practice>) → sent proposals, completion times
# 3. correlate with practice's last POSTFLIGHT transaction timestamp
# 4. store in telemetry database (Supabase table: mesh_events)
```

**Owner:** evaluator (infrastructure) + mesh-support (validation)  
**Effort:** 4h (loop setup + correlation logic)  
**Timeline:** Aug 18-22

#### Task 1.3: POSTFLIGHT Data Aggregation (All Practices → Master Index)

**What:** Evaluator collects POSTFLIGHT outputs from all 13 practices and maintains a unified `.postflight/INDEX.yaml` that shows mesh-wide trends.

**Mechanism:**
```yaml
# .postflight/INDEX.yaml (extended)
version: "1.0-mesh"
aggregation_mode: "mesh-wide (13 practices)"
last_updated: "2026-08-15T..."

summary:
  total_practices: 13
  total_sessions_aggregated: 84  # 12 sessions per practice × 7 days
  
practices:
  "empirica-autonomy":
    sessions: 12
    latest_postflight: "2026-08-14T..."
    vectors:
      know: [0.82, 0.85, ..., 0.92]  # trend per vector
      uncertainty: [...]
    goals: {completed: 4, in_progress: 3}
    mesh_health: {response_time_hours: 6, reliability: 1.0, status: "EXCELLENT"}
  
  "empirica-outreach":
    sessions: 8
    latest_postflight: "2026-08-14T..."
    vectors: {...}
    goals: {completed: 2, in_progress: 5}
    mesh_health: {response_time_hours: 42, reliability: 0.70, status: "NEEDS_ATTENTION"}
  
  # ... 11 more practices

vector_trends_mesh_wide:
  know: {trend: "↗ +0.15", interpretation: "..."}
  uncertainty: {trend: "↘ -0.12", interpretation: "..."}
  # ...

mesh_health_summary:
  average_response_time: 18h
  practices_by_responsiveness:
    - {practice: "autonomy", hours: 6, reliability: 1.0, status: "EXCELLENT"}
    - {practice: "evaluator", hours: 12, reliability: 0.95, status: "EXCELLENT"}
    - {practice: "outreach", hours: 42, reliability: 0.70, status: "NEEDS_ATTENTION"}
  
blockers_and_dependencies:
  cross_practice_blockers:
    - {blocker: "interview_scheduling", affects_practices: 3, impact_score: 0.8}
    - {blocker: "wisdom_engine_spec", affects_practices: 2, impact_score: 0.7}
  
  cascade_risk: "outreach 42h response time → affects interview scheduling (3 goals affected)"
```

**Owner:** evaluator  
**Effort:** 6h (set up aggregation scripts, test with 3 practices first, then roll to all 13)  
**Timeline:** Aug 20-24

---

### Stage 2: Dashboard & Alerting (Week 3: Aug 25-31)

**Goal:** Make mesh health visible in real-time. Build dashboards + set up anomaly alerts.

#### Task 2.1: Mesh Health Dashboard (Real-Time)

**What:** Web dashboard showing:
- 13-practice mesh status (grid: practice × vector, heatmap colors for health)
- Practice responsiveness scores (table: practice, response time, reliability %, status)
- Top blockers + cascade impact
- Vector trends (sparklines per vector, mesh-wide)
- Burnout risk signals (engagement + artifact logging breadth trends)

**Tech:** Supabase + simple HTML/Recharts dashboard (can be hosted on evaluator's Artifact system or as a static Supabase view).

**Owner:** evaluator  
**Effort:** 8h (dashboard setup + Supabase telemetry tables)  
**Timeline:** Aug 25-28

#### Task 2.2: Anomaly Alerting

**What:** Automated alerts on:
- Practice responsiveness drop > 20h / day (e.g., outreach 42h → triggers if it hits 50h+)
- Burnout signals (engagement < 0.65 for 2+ consecutive transactions)
- Blocker cascade (if top blocker now affects 4+ practices)
- Stalled proposals (collab or typed proposal with no reply > 24h, should be 4-6h median)

**Mechanism:**
```bash
# Hourly alert check
empirica loop register --name mesh-anomaly-alerts --kind interval \
  --interval 1h
  
# Body:
# 1. Read latest .postflight/INDEX.yaml mesh_health section
# 2. Compare to prior hour snapshot
# 3. If anomaly detected: log finding + send cortex_collab to Admiral
```

**Owner:** evaluator  
**Effort:** 4h  
**Timeline:** Aug 28-30

---

### Stage 3: Per-Practice Profiles & Weekly Reports (Week 4: Sep 1-10)

**Goal:** Enable deeper observability at practice level. Weekly trend reports.

#### Task 3.1: Per-Practice Profile Pages

**What:** One page per practice showing:
- Last 12 sessions' vectors (trend + current)
- Goal health (burndown chart)
- Mesh responsiveness (response time trend, SLA compliance %)
- Recent escalations + resolutions
- Calibration vs. reality (belief variance over time)

**Owner:** evaluator  
**Effort:** 6h (template + automation to generate 13 profiles weekly)  
**Timeline:** Sep 1-5

#### Task 3.2: Weekly Mesh Trend Report

**What:** Automated report (email + artifact) showing:
- Vector movements (which dimensions improving/declining across mesh)
- Practice health ratings (EXCELLENT/GOOD/NEEDS_ATTENTION per practice)
- Blockers + progress (which blockers got resolved, which are new)
- Burnout risk scorecard (list practices by burnout risk: 0-1 scale)
- Mesh efficiency (SLA compliance %, response time distribution)

**Cadence:** Sunday 6 AM UTC, delivered to Admiral inbox  
**Owner:** evaluator  
**Effort:** 5h (automation setup)  
**Timeline:** Sep 5-10

---

## PART D: Success Criteria

### By Aug 24 (End of Stage 1)

- [ ] POSTFLIGHT schema standardized + adopted by 13 practices
- [ ] Telemetry ingestion loop running (hourly Cortex event collection)
- [ ] Master INDEX.yaml aggregating all 13 practices
- [ ] Mesh-wide vector trends visible (know, uncertainty, engagement, etc.)
- [ ] Practice responsiveness scores calculated + ranked

### By Aug 31 (End of Stage 2)

- [ ] Mesh health dashboard live (13-practice grid, responsiveness table, blocker list)
- [ ] Anomaly alerts configured + tested on 3 practices
- [ ] Admiral can see at-a-glance "which practices need attention"
- [ ] Burnout signals + stalled proposals are flagged

### By Sep 10 (End of Stage 3)

- [ ] 13 per-practice profile pages generated + updated weekly
- [ ] Weekly trend reports automated + delivered
- [ ] Complete observability established: Admiral has visibility into:
  - Each practice's epistemic state (13 vectors)
  - Mesh coordination health (response times, SLA compliance)
  - Cross-practice dependencies + blocker cascades
  - Burnout + sustainability risks
  - Calibration tracking (beliefs vs. reality per practice)

---

## PART E: Technical Integration Points

### Supabase Schema (New Tables)

```sql
-- Telemetry data storage
CREATE TABLE mesh_telemetry (
  id UUID PRIMARY KEY,
  collected_at TIMESTAMP,
  practice_id TEXT,  -- e.g. "empirica-foundation.carly.empirica-autonomy"
  session_id TEXT,
  
  -- Vectors (one row per transaction per practice)
  vector_know FLOAT,
  vector_uncertainty FLOAT,
  vector_engagement FLOAT,
  -- ... all 13 vectors
  
  -- Goal health
  goals_completed INT,
  goals_in_progress INT,
  goals_planned INT,
  
  -- Mesh events
  inbox_items INT,
  collabs_responded INT,
  avg_response_time_hours INT,
  sla_compliance FLOAT,  -- % of collabs replied within 4-6h
  
  -- Calibration
  calibration_variance FLOAT,
  accuracy_on_predictions FLOAT
);

CREATE TABLE mesh_events (
  id UUID PRIMARY KEY,
  ts TIMESTAMP,
  event_type TEXT,  -- "collab" | "proposal" | "completion" | "escalation"
  source_practice TEXT,
  target_practice TEXT,
  proposal_id TEXT,
  response_time_hours FLOAT
);

CREATE TABLE anomalies (
  id UUID PRIMARY KEY,
  detected_at TIMESTAMP,
  practice_id TEXT,
  anomaly_type TEXT,  -- "high_response_time" | "burnout_signal" | "stalled_proposal"
  severity TEXT,      -- "warning" | "critical"
  message TEXT,
  auto_alert_sent BOOLEAN
);
```

### Cortex Integration

- Evaluator polls `cortex_inbox_poll()` for all 13 practices hourly
- Correlates proposal response times with practice POSTFLIGHT data
- Feeds into mesh_events table for trend analysis

### Empirica Integration

- Each practice's POSTFLIGHT CLI already emits JSON
- Standardize JSON schema across practices (name-space consistency)
- Evaluator fetches via empirica CLI: `empirica project-search --project-id <practice> --output json`
- Aggregates into INDEX.yaml

---

## PART F: Admiral Interface

### Quick Access Points

**Dashboard (real-time):**
- URL: (Supabase view or Artifact page)
- Refresh: Every 5 minutes
- Use case: "Is the mesh healthy right now?"

**Weekly Report (Sunday 6 AM UTC):**
- Delivery: Cortex collab_brief to Admiral
- Content: Trend analysis + alerts + blockers
- Use case: "What changed this week?"

**Per-Practice Profiles (updated weekly):**
- Location: `.postflight/<practice>/profile.yaml`
- Content: 12-session history per practice
- Use case: "How is autonomy doing? Is outreach burnout risk rising?"

**Anomaly Alerts (real-time):**
- Delivery: Cortex collab_brief + finding-log
- Trigger: Response time > 50h, burnout signal, stalled proposal
- Use case: "Alert me if something breaks"

---

## PART G: Rollout Schedule

| Week | Task | Owner | Status |
|------|------|-------|--------|
| Aug 15-20 | POSTFLIGHT schema + adoption (13 practices) | evaluator | Design |
| Aug 18-22 | Telemetry ingestion loop | evaluator | Design |
| Aug 20-24 | Master INDEX.yaml aggregation | evaluator | Design |
| Aug 25-28 | Mesh health dashboard | evaluator | Design |
| Aug 28-30 | Anomaly alerting | evaluator | Design |
| Sep 1-5 | Per-practice profiles | evaluator | Planned |
| Sep 5-10 | Weekly trend reports | evaluator | Planned |

**Go-Live:** Sep 11 (aligned with Phase 1b launch) — Admiral has complete mesh observability before operational launch.

---

## PART H: Success Metrics

**By Sep 11:**

- ✅ All 13 practices' POSTFLIGHT data flowing into master INDEX.yaml
- ✅ Mesh health dashboard showing 13-practice status in real-time
- ✅ Admiral can identify which practices need attention (responsiveness, burnout, blockers) in <30 seconds
- ✅ Weekly trend reports automated + delivered
- ✅ Anomaly alerts configured + tested
- ✅ Evaluator can answer "Is the mesh healthy?" with data (not guessing)

**Beyond Sep 11:**

- Continuous mesh health monitoring through Phase 1b + Phase 2
- Proactive intervention on burnout + blocker cascade
- Evidence-based decisions on resource allocation + practice support
- Complete audit trail of mesh performance + health trends

---

**Status:** Design complete, ready for implementation Aug 15.  
**Next:** Confirm scope with Admiral, begin Stage 1 infrastructure setup.
