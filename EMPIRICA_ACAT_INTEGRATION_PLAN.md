# Empirica-ACAT Integration Framework
## Operational Calibration via Cross-Instrument Grounding

**Version:** 1.0.0 (Planning Phase)  
**Lead Seat:** empirica-foundation.carly.empirica-foundation-evaluator (Evaluator + ACAT Owner)  
**Scope:** Foundation-wide epistemic calibration + assessment coordination  
**Timeline:** 12-week phased rollout (Phase 1: Weeks 1–4 / T4 concurrent)  
**Status:** NOETIC → Ready for Mesh Proposal  

---

## I. VISION: ACAT as Observable Calibrator

### The Problem
Empirica measures **self-assessed epistemic state** (the 13 vectors). But self-assessment is self-referential and prone to bias. We need **external grounding** — an independent measurement that reflects what's actually true, not just what AIs believe about themselves.

### The Solution
ACAT (Assessment & Calibration Assessment Tool) provides phase-scored assessment of AI behavior in real interactions. When coupled with empirica's epistemic vectors, the **gap between them is the calibration signal**.

```
ACAT Phase Score (ground truth)  ←→  empirica Vector (belief)
                                 ↓
                        Calibration Signal
                        (where work discipline needs attention)
```

### Outcome
A **dual-instrument grounding system** where:
- **ACAT measures behavior** (what AIs actually do under observation)
- **Empirica measures belief** (what AIs think about their own state)
- **Convergence/divergence drives calibration** (gap = discipline opportunity)
- **Data is observable + auditable** (every session tagged with both)

---

## II. ARCHITECTURE: One-Way Grounding + Observable Linkage

### Data Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│ Session Execution (AI ↔ User Interaction)               │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────────┐      ┌──────────────────────┐   │
│  │ Empirica State     │      │ ACAT Observation     │   │
│  │ (Self-assessed)    │      │ (External grounding) │   │
│  ├────────────────────┤      ├──────────────────────┤   │
│  │ • 13 vectors       │      │ • Phase score (1–4)  │   │
│  │ • know: 0.85       │      │ • Behavior observed  │   │
│  │ • uncertainty:0.20 │      │ • Rubric alignment   │   │
│  │ • context: 0.80    │      │ • Drift detected     │   │
│  │ • ... (10 more)    │      │                      │   │
│  └────────────────────┘      └──────────────────────┘   │
│          │                              │                │
└──────────┼──────────────────────────────┼────────────────┘
           ↓                              ↓
    ┌──────────────────────────────────────────────┐
    │ Session Record (Observable Linkage)          │
    ├──────────────────────────────────────────────┤
    │ session_id: ...                              │
    │ empirica_preflight_vectors: {...}            │
    │ empirica_postflight_vectors: {...}           │
    │ acat_phase_score: 3                          │
    │ acat_alignment: {know: +0.15, context: -0.10}│
    │ convergence_signal: {delta, confidence}      │
    │ grounding_link: one-way (ACAT → empirica)    │
    └──────────────────────────────────────────────┘
           ↓
    ┌──────────────────────────────────────────────┐
    │ Calibration Dataset (Longitudinal)           │
    │ Feeds: Evaluator Assessment + Lessons        │
    └──────────────────────────────────────────────┘
```

### One-Way Grounding Principle

**ACAT informs empirica; empirica does NOT inform ACAT.**

- ✅ Empirica pre-flight vectors influence CHECK gate
- ✅ ACAT phase score grounds empirica post-flight assessment
- ✅ Divergence signals feed lessons + findings
- ❌ Empirica vectors do NOT adjust ACAT scoring (external → internal only)

**Why one-way?** ACAT is the **external observer**. If empirica's self-assessment could feedback into ACAT, the grounding evaporates (circular reasoning).

---

## III. ROLES & RESPONSIBILITIES: Multi-Practice Coordination

### Practice-by-Practice Map

| Practice | Role | Responsibility | Mesh Seat |
|----------|------|-----------------|-----------|
| **empirica-foundation-evaluator** | Assessment + ACAT Wrapper | <ul><li>ACAT phase scoring in-session</li><li>Convergence/divergence analysis</li><li>Calibration signals → findings</li><li>One-way grounding enforcement</li><li>F-50 firewall (independence)</li></ul> | Source (proposes) |
| **empirica-autonomy** | Execution Coordination | <ul><li>Routes proposals to execution practices</li><li>Ensures F-50 (assessment doesn't direct fixes)</li><li>Tracks phase transitions (Phase 1–5)</li><li>Escalates gaps to evaluator</li></ul> | Participant (required) |
| **humanaios** | ACAT Implementation Owner | <ul><li>Maintains ACAT rubric definitions</li><li>Provides phase-scoring API</li><li>Ensures assessment reproducibility</li><li>Documents alignment mappings</li></ul> | Participant (required) |
| **empirica-mesh-support** | Coordination Infrastructure | <ul><li>Maintains SER 2 (Execution Routing)</li><li>Orchestrates practice-to-practice proposals</li><li>Monitors escalation timers</li><li>Tracks data provenance</li></ul> | Observer (blockers only) |
| **empirica-cortex** | Proposal + Data Registry | <ul><li>Cortex stores proposals + SERs</li><li>Data linkage (session ↔ ACAT score)</li><li>Cross-practice query surface</li></ul> | Observer |

### Authority & Independence (F-50 Firewall)

**The F-50 firewall** prevents feedback loops between assessment (evaluator) and execution (autonomy + practices).

```
Evaluator                          Autonomy                         Execution Practices
(Assessment)                     (Routing)                      (humanaios, outreach, etc.)
    ↓                              ↓                                  ↓
Assess behavior        Route findings to execution         Implement fixes (no eval input)
Surface gaps           Ensure F-50 holds                   Report results to eval
Propose fixes    ← [one-way] ←    Receive eval findings   → [one-way] →   Acknowledge ack
    ↑                                                                        ↓
    └────────────────── [NEVER ←─] ──────────────────────────────────────┘
```

**Rules:**
- ✅ Evaluator surfaces findings → autonomy routes → practices execute
- ✅ Practices report results → autonomy → evaluator (for next assessment)
- ❌ Evaluator does NOT direct fixes or override autonomy
- ❌ Practices do NOT feedback into ACAT scoring
- ❌ Autonomy does NOT let execution influence assessment

---

## IV. OBSERVABLE LINKAGE: Data Model

### Session-Level Coupling

Every empirica session gets enriched with ACAT data at PREFLIGHT and POSTFLIGHT:

```yaml
# empirica session record (sessions.db)
session_id: "f4885647-49a9-455c-b8a1-8e5d631c9cc0"
ai_id: "empirica-foundation-evaluator"
created_at: "2026-07-06T14:30:00Z"

# PREFLIGHT vectors (self-assessed)
preflight:
  vectors:
    know: 0.88
    uncertainty: 0.25
    context: 0.85
    # ... (10 more)
  timestamp: "2026-07-06T14:31:00Z"

# Work happens here

# POSTFLIGHT vectors (self-assessed post-work)
postflight:
  vectors:
    know: 0.92
    uncertainty: 0.15
    context: 0.90
    # ... (10 more)
  timestamp: "2026-07-06T15:45:00Z"
  deltas:
    know: +0.04
    uncertainty: -0.10
    # ... (computed)

# ACAT GROUNDING (external observer score)
acat_grounding:
  phase: 3
  phase_score: 3.2  # out of 4.0 (phases don't align 1:1 with empirica)
  rubric_alignment:
    clarity: "met"
    independence: "met"
    evidence_tracing: "partially"
    mesh_discipline: "met"
  observations:
    - "ACAT phase 3: investigation sufficient, ready to implement"
    - "Empirica uncertainty estimate (0.15) aligns with external observation"
    - "Context vector (0.90) matches rubric assessment"
  timestamp: "2026-07-06T15:50:00Z"
  assessor: "empirica-foundation.carly.empirica-foundation-evaluator"

# CONVERGENCE SIGNAL (one-way grounding)
convergence:
  empirica_believes:
    know: 0.92
    uncertainty: 0.15
  acat_observes:
    aligned_to_phase: 3
    confidence: 0.88
  signal:
    delta: +0.15  # empirica's know estimate vs. ACAT phase score
    direction: "empirica_optimistic"  # empirica believes higher than ACAT shows
    confidence: 0.88
  calibration_implication:
    know_vector: "slight_overestimation"
    discipline_flag: "increase noetic work on unknown areas"
```

### Mapping Table: Empirica Vectors ↔ ACAT Phases

| Empirica Vector | ACAT Phase Indicator | How It Couples | Grounding Role |
|---|---|---|---|
| **know** | Phase completion readiness | High know + Phase 3 ready = convergence | Phase score grounds vector |
| **uncertainty** | Rubric confidence score | Low uncertainty + rubric "met" = aligned | High rubric confidence ↓ expected uncertainty |
| **context** | Observation coverage | Context vector ↔ "observations" field count | ACAT shows what you missed |
| **clarity** | "clarity met/partial/unmet" | Clarity vector ↔ rubric alignment | Rubric score grounds vector |
| **do** | "independence met" + implementation evidence | Do vector ↔ execution readiness | Phase score indicates action capacity |
| **engagement** | Behavior consistency in observation | Engagement ↔ "observations" coherence | ACAT spots disengagement |

---

## V. INTEGRATION PHASES & TIMELINE

### Phase 1: Foundation (Weeks 1–4) — Concurrent with T4 Phase 1

**Goal:** Establish ACAT + empirica linkage at the evaluator seat.

| Milestone | Owner | Duration | Blocker | Success Criteria |
|-----------|-------|----------|---------|-----------------|
| **1a. Wrap ACAT as CLI** | humanaios | 2 days | None | `acat-score --session-id <id>` returns phase + alignment JSON |
| **1b. Hook ACAT into POSTFLIGHT** | evaluator | 1 day | 1a | POSTFLIGHT payload includes acat_grounding section |
| **1c. Document mapping** | evaluator | 1 day | 1a | Empirica ↔ ACAT vectors documented + audited |
| **1d. Create SER 2** | autonomy | 1 day | (SER 1 must exist) | SER 2: Execution Routing established |
| **1e. Create calibration dataset schema** | evaluator | 1 day | 1b | Postgres table: session_id, vectors, acat_score, delta |

**Deliverables:**
- ✅ ACAT CLI tool
- ✅ Empirica POSTFLIGHT hook (acat_grounding inserted)
- ✅ Vector-phase mapping document
- ✅ SER 2 (Execution Routing for autonomy + humanaios + others)
- ✅ Calibration dataset schema

---

### Phase 2: Grounding Validation (Weeks 5–6)

**Goal:** Test one-way grounding with real session data.

| Milestone | Owner | Duration | Success Criteria |
|-----------|-------|----------|-----------------|
| **2a. Run 5 evaluator sessions** | evaluator | 3 days | Each session: vectors + ACAT phase logged |
| **2b. Analyze convergence signals** | evaluator | 2 days | Delta computed; patterns identified |
| **2c. Document lessons learned** | evaluator | 1 day | Findings: where ACAT ↔ empirica diverge + why |

**Output:**
- Calibration dataset with 5 sessions
- Convergence analysis (δ by vector)
- Initial lessons (e.g., "know vector tends +0.08 vs. ACAT phase score")

---

### Phase 3: Multi-Practice Integration (Weeks 7–10)

**Goal:** Wire ACAT grounding into other practices (autonomy, humanaios, outreach).

| Milestone | Owner | Duration | Success Criteria |
|-----------|-------|----------|-----------------|
| **3a. Autonomy ingests ACAT signals** | autonomy | 3 days | Proposals include ACAT phase in metadata |
| **3b. humanaios refines ACAT rubric** | humanaios | 2 days | Phase-score API updated; alignment improved |
| **3c. Outreach receives calibration findings** | outreach | 2 days | Findings logged; outreach acknowledges via SER 2 |
| **3d. Cross-practice session collection** | evaluator | 3 days | 10+ sessions across practices; convergence re-analyzed |

**Output:**
- ACAT signals in autonomy's proposal routing
- Refined rubric with better vector alignment
- Dataset: 15+ sessions (evaluator + autonomy + humanaios + outreach)

---

### Phase 4: Calibration Measurement (Weeks 11–12)

**Goal:** Measure calibration + produce findings.

| Milestone | Owner | Duration | Success Criteria |
|-----------|-------|----------|-----------------|
| **4a. Aggregate dataset** | evaluator | 1 day | All sessions: merged into calibration table |
| **4b. Compute per-vector calibration** | evaluator | 2 days | Brier score by vector; confidence intervals |
| **4c. Identify high-impact deltas** | evaluator | 1 day | Vectors where divergence > 0.15 flagged |
| **4d. Generate findings + lessons** | evaluator | 2 days | Finding-log: calibration report + per-practice lessons |

**Output:**
- Calibration report (per-vector Brier scores)
- Findings: practices + practices with drift
- Lessons: updated for next quarter

---

## VI. DATA FLOW & OBSERVABLE ARCHITECTURE

### Components

```
┌──────────────────────────────────────────────────────────────────┐
│ Session Execution Environment                                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│ ┌──────────────────┐        ┌──────────────────────────────────┐ │
│ │ empirica         │        │ ACAT Assessment Wrapper          │ │
│ │ ─────────────    │        │ (evaluator's responsibility)      │ │
│ │ • PREFLIGHT      │        │                                  │ │
│ │ • CHECK          │        │ • Query: behavior observation    │ │
│ │ • POSTFLIGHT ◄───┼────────┤ • Score: phase (1–4)            │ │
│ │                  │        │ • Align: rubric fields           │ │
│ │ Session log      │        │ • Link: session_id → acat_id     │ │
│ │ (hot store)      │        │                                  │ │
│ └──────────────────┘        └──────────────────────────────────┘ │
│          ↓                                       ↓                │
└──────────┼───────────────────────────────────────┼────────────────┘
           ↓                                       ↓
    ┌────────────────────────────────────────────────────┐
    │ Empirica + ACAT Observable Record                  │
    │ (One-way grounding: ACAT → empirica beliefs)       │
    │                                                    │
    │ {                                                  │
    │   session_id, ai_id, created_at,                  │
    │   preflight_vectors, postflight_vectors,          │
    │   acat_phase, acat_alignment,                     │
    │   convergence_delta, calibration_implication      │
    │ }                                                  │
    └────────────────────────────────────────────────────┘
           ↓
    ┌────────────────────────────────────────────────────┐
    │ Warm Store (PostgreSQL)                            │
    │ Table: empirica_acat_sessions                      │
    │ (queryable + explorable)                           │
    └────────────────────────────────────────────────────┘
           ↓
    ┌────────────────────────────────────────────────────┐
    │ Search Index (Qdrant)                              │
    │ Embedded: convergence vectors + observations       │
    │ Queryable: "sessions where know diverges > 0.15"   │
    └────────────────────────────────────────────────────┘
           ↓
    ┌────────────────────────────────────────────────────┐
    │ Findings + Lessons                                 │
    │ Output: Calibration insights per practice          │
    │ Usage: Future session CHECK gates, lessons reuse   │
    └────────────────────────────────────────────────────┘
```

### API Surface

**ACAT Scoring (from humanaios):**
```bash
acat-score \
  --session-id "f4885647..." \
  --ai_id "empirica-foundation-evaluator" \
  --behavior-transcript "/path/to/session.log" \
  --rubric-version "v1.0" \
  --output json

# Returns:
{
  "phase": 3,
  "phase_score": 3.2,
  "confidence": 0.88,
  "rubric_alignment": {
    "clarity": "met",
    "independence": "met",
    ...
  },
  "observations": [...]
}
```

**Empirica POSTFLIGHT Hook (new):**
```bash
empirica postflight-submit - << 'EOF'
{
  "session_id": "...",
  "vectors": { ... },
  "acat_grounding": {
    "phase": 3,
    "phase_score": 3.2,
    "confidence": 0.88,
    "convergence_delta": +0.15,
    "calibration_implication": "slight_overestimation"
  }
}
EOF
```

---

## VII. SUCCESS CRITERIA & MEASUREMENT

### Operational Success

✅ **Observable linkage** — Every session has ACAT + empirica data linked  
✅ **One-way grounding** — ACAT informs empirica; reverse never happens  
✅ **F-50 holds** — Assessment findings don't direct execution (autonomy gates)  
✅ **Data accessible** — Queries like "all sessions where convergence > 0.15" work  
✅ **Lessons fed forward** — Next quarter's CHECK gates use calibration insights  

### Calibration Success

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Brier Score (per vector)** | < 0.15 | Empirica prediction vs. ACAT observation |
| **Convergence Rate** | > 80% within 0.10 | Sessions where δ < 0.10 |
| **Outlier Accountability** | 100% | All δ > 0.20 have findings logged |
| **Lesson Reuse** | > 50% | Next-session CHECK gates cite priors |

### Framework Robustness

| Quality | Target | How |
|---------|--------|-----|
| **Rubric Stability** | No phase score changes >0.15 | ACAT consistency across assessors |
| **Mapping Coverage** | All 13 vectors ↔ ACAT aligned | Completeness of vector-phase table |
| **Cross-Practice Adoption** | 5+ practices using framework | Integration count |

---

## VIII. NEXT STEPS: Mesh Proposal Strategy

### What Needs to Happen

1. **Validate plan with constitution + mesh** (this document)
2. **Create SER 2: Execution Routing** (autonomy + humanaios + outreach + mesh-support)
3. **Propose Phase 1 work** to each practice via cortex_propose
4. **Begin Phase 1 deliverables** (Weeks 1–4, concurrent with T4 Phase 1–5)

### Proposed SER 2 (Execution Routing)

SER 2 will coordinate Phase 1 implementation across 4 practices:

| Participant | Role | Commitment |
|-------------|------|------------|
| **empirica-autonomy** | Routing + coordination | Review autonomy's role in F-50 + SER transitions |
| **humanaios** | ACAT ownership | Deliver CLI tool + rubric alignment mapping |
| **empirica-outreach** | Pilot practice | Accept ACAT scoring in Phase 3 rollout |
| **empirica-mesh-support** | Infrastructure observer | Monitor SER 2 transitions + escalations |

SER 2 lifecycle: OPEN (Phase 1a) → IN_PROGRESS (Phase 1b–2) → CLOSED (Phase 4d)

### Mesh Communication Plan

| Step | Who | Action | Tool |
|------|-----|--------|------|
| 1 | Evaluator | Surface this plan to mesh | cortex_collab (FYI) |
| 2 | humanaios | Acknowledge ACAT role | cortex_collab (reply) |
| 3 | autonomy | Confirm SER 2 participation | cortex_collab (reply) |
| 4 | Evaluator | Propose SER 2 + Phase 1 work | cortex_propose (architecture_decision) |
| 5 | ECO | Gate SER 2 creation + task commitment | Human Accept/Decline |
| 6 | All | Begin Phase 1 (concurrent with T4) | SER 2 transitions to IN_PROGRESS |

---

## IX. REFERENCES & RELATED DOCUMENTS

**Governance:**
- `/empirica-constitution` §V (Mesh discipline) + §VI (Multi-practice coordination)
- `docs/EVALUATOR_MANUAL.md` (Assessment methodology, ACAT references)
- `docs/EVALUATOR_SEAT.md` (Role definition, F-50 firewall)

**T4 Mesh Implementation:**
- `T4_MESH_SUPPORT_HANDOFF.md` (Phases 1–5, timeline)
- `T4_SER1_PROPOSAL_FOR_MESH_SUPPORT.md` (Assessment Coordination SER)
- `PHASE_1_BLOCKER_ESCALATION.md` (Cortex infrastructure resolution)

**Technical:**
- `ACAT` system documentation (humanaios, assessment rubric)
- Empirica calibration model (13 vectors, Brier scoring)
- Cortex MCP tools (`cortex_propose`, SER lifecycle)

---

## X. DECISION GATES & NEXT PHASE CRITERIA

### Gate: Before Phase 1 Begins

**Required approvals:**
- ✅ User (Carly) endorses plan
- ⏳ humanaios confirms ACAT CLI tool feasibility
- ⏳ autonomy confirms SER 2 participation + F-50 rules
- ⏳ ECO gates SER 2 creation + task commitments

**Criteria for "ready to execute":**
- All 4 participants acknowledged
- SER 2 created and IN_PROGRESS
- Phase 1a deliverables assigned
- ACAT CLI tool scoped + estimated

### Gate: Before Phase 2

- Phase 1 deliverables completed + committed
- ACAT hook inserted into POSTFLIGHT
- 5 evaluator sessions completed + data logged

---

**Status:** READY FOR MESH PROPOSAL  
**Lead:** Carly R. Anderson (empirica-foundation-evaluator)  
**Next Action:** FYI collab to humanaios + autonomy; propose SER 2

*This document establishes the Empirica-ACAT framework as the foundation's canonical calibration system. Implementation begins Week 1 of Phase 1 (concurrent with T4 mesh execution).*
