# Empirica-ACAT Framework — Finalized Commitment
## All Decisions Locked | Goals Closed

**Date:** 2026-07-06  
**User Authorization:** Carly R. Anderson (Admiral + Evaluator)  
**Status:** ✅ **CLOSED — READY FOR EXECUTION**

---

## Decision Locks — Option A Confirmed

### Decision 1: ACAT CLI Specification
**Selected:** Option A (ACAT_CLI_ASSESSMENT.md exact spec)

```bash
acat-score assess \
  --session-id <uuid> \
  --ai-id <practice> \
  --behavior-transcript <path> \
  --rubric-version v1.0 \
  --output json
```

**Returns:** `{phase, phase_score, confidence, rubric_alignment, observations}`

**Owner:** humanaios (required)  
**Deadline:** End of Week 2 (by 2026-07-13)  
**Deliverable:** Command callable from shell, JSON output matching HTTP API response, exit codes 0 on success / non-zero on failure

---

### Decision 2: Observable Linkage Timeline
**Selected:** Option A (Full integration Phase 1a)

**Phase 1a Milestones:**
- **Week 1 (2026-07-10):** ACAT CLI development starts + evaluator documents vector-phase mapping
- **Week 2 (2026-07-13):** ACAT CLI delivered (deadline) + POSTFLIGHT hook integration begins
- **Week 3 (2026-07-20):** POSTFLIGHT hook live + first 5 sessions assessed + observable linkage validated

**Integration Path:**
```
Session POSTFLIGHT
    ↓
acat-score assess CLI invocation (subprocess.run)
    ↓
Session record enriched with {phase, phase_score, confidence, rubric_alignment, convergence_delta}
    ↓
Observable dataset ready for calibration measurement (Phase 2)
```

---

### Decision 3: SER 2 vs. T4 Sequencing
**Selected:** Option A (Keep concurrent)

**Execution Timeline:**
- **SER 1 (T4):** Assessment Coordination — empirica-foundation-evaluator + empirica-mesh-support
  - Phase 1: Days 1–2 (listener setup, coordination established)
  - Timeline: 30 hours over 4 weeks (2026-07-06 through 2026-08-03)
  
- **SER 2 (Empirica-ACAT):** Execution Routing — autonomy + humanaios + outreach + mesh-support
  - Phase 1: Weeks 1–4 (CLI, mapping, F-50, schema)
  - Timeline: 12 weeks (2026-07-10 through 2026-10-01)

**Concurrency Benefit:** Parallel work reduces critical path, mesh-support can hold both SERs simultaneously

**Coordination Rule:** mesh-support observer role on SER 2 monitors F-50 firewall adherence — assessment (T4) and execution (SER 2) stay independent

---

## Goals Closed

### Goal 1: T3 ACAT-Empirica Integration
**Objective:** Wire behavioral drift into grounded calibration  
**Status:** ✅ **CLOSED — PLANNING COMPLETE**

**Evidence:**
- Commits: 686a3f8, fdf4024, a135952, 9e80b92, 69bf515, e3cf6ac
- Files: EMPIRICA_ACAT_INTEGRATION_PLAN.md (491 lines), MESH_COORDINATION_BRIEF.md (346 lines), PLANNING_SUMMARY_*.md (289 lines), ACAT_CLI_ASSESSMENT.md (284 lines)
- Artifacts: 4 mesh collabs dispatched, SER 2 proposal ready, observable linkage spec complete, F-50 firewall rules defined
- Decision locks: 3/3 options finalized (CLI spec, timeline, sequencing)

**Handoff:** Ready for Phase 1 execution (Week 1 start: 2026-07-10)

---

### Goal 2: T4 12-Month Roadmap
**Objective:** Phased execution with publication path  
**Status:** ✅ **CLOSED — T4 PHASE 1 UNBLOCKED**

**Evidence:**
- SER 1 proposal created and ready for mesh-support action: T4_SER1_PROPOSAL_FOR_MESH_SUPPORT.md
- T4 Phase dependencies mapped: Phase 1 (SER creation) → Phase 2 (autonomy integration) → Phase 3 (assessment) → Phase 4 (calibration) → Phase 5 (findings)
- Timeline: 30 hours over 4 weeks (concurrent with SER 2)
- Mesh routing ready: T4 mesh implementation gates Phases 2–5

**Handoff:** Awaiting mesh-support cortex_propose execution for SER 1 creation (then T4 Phase 1 proceeds)

---

## Concurrent Execution Plan (Week 1 Start: 2026-07-10)

### SER 1 (T4) — Parallel Track
**Owner:** empirica-mesh-support (required)  
**Evaluator:** empirica-foundation-evaluator (required)

| Day | Activity | Owner | Deliverable |
|-----|----------|-------|-------------|
| 1–2 | SER 1 creation, listener setup | mesh-support | SER 1 status=OPEN |
| 3–5 | Autonomy + integration planning | autonomy | Integration roadmap |
| 6–10 | Assessment methodology + ACAT grounding design | evaluator | Methodology doc |

---

### SER 2 (Empirica-ACAT) — Parallel Track
**Owner:** autonomy (required) + humanaios (required) + outreach (participating) + mesh-support (observer)

| Week | Phase | humanaios | evaluator | autonomy | mesh-support |
|------|-------|-----------|-----------|----------|--------------|
| **1–2** | Phase 1a: Setup | CLI design + build start | Vector-phase mapping | F-50 rules design | Prep monitoring |
| **2–3** | Phase 1b: Integration | CLI delivery (Week 2) | Hook integration | F-50 implementation | Escalation setup |
| **3–4** | Phase 1c: Validation | CLI testing | First 5 sessions | Integration test | Observe F-50 |

---

## Data Flow — Observable Linkage

```
Session execution (any practice)
    ↓
Empirica PREFLIGHT (baseline vectors)
    ↓
Session work (the practice operates)
    ↓
Empirica POSTFLIGHT hook
    ↓
acat-score CLI invocation
    ↓
ACAT returns: {phase, phase_score, confidence, rubric_alignment}
    ↓
Session record enriched:
  {
    empirica_vectors: {know: 0.85, uncertainty: 0.2, ...},
    acat_grounding: {phase: 3, phase_score: 3.2, confidence: 0.88},
    convergence: {delta: +0.05, direction: "aligned"},
    calibration_implication: "know_vector accurate"
  }
    ↓
Observable dataset (hot: session logs, warm: PostgreSQL, search: Qdrant, cold: git notes)
    ↓
Phase 2 Analysis: Brier scores, convergence rates, outlier accountability
    ↓
Phase 4 Report: Calibration findings + lessons + implications
```

---

## Success Criteria (All Phases)

### Phase 1a (Weeks 1–2): Setup
- ✅ ACAT CLI delivered by end Week 2
- ✅ evaluator vector-phase mapping documented
- ✅ autonomy F-50 rules drafted
- ✅ mesh-support escalation monitoring ready

### Phase 1b (Week 3): Integration
- ✅ POSTFLIGHT hook live
- ✅ First 5 sessions assessed via acat-score
- ✅ Observable linkage validated (session record contains both empirica + ACAT data)

### Phase 1c (Week 4): Validation
- ✅ All Phase 1 deliverables complete
- ✅ SER 2 transitions to IN_PROGRESS
- ✅ Week 1 execution retrospective logged

### Phase 2 (Weeks 5–6): Grounding
- ✅ Convergence validation: δ < ±0.15 for ≥80% of sessions
- ✅ No F-50 firewall violations (assessment findings don't direct execution)

### Phase 3 (Weeks 7–10): Multi-Practice
- ✅ outreach pilot: 50+ sessions assessed
- ✅ Cross-practice calibration measured

### Phase 4 (Weeks 11–12): Findings
- ✅ Brier score < 0.15 per vector
- ✅ Calibration report + lessons delivered
- ✅ SER 2 transitions to CLOSED

---

## Mesh Coordination Status

### Collabs (Dispatched 2026-07-06)
- ✅ Collab A (humanaios): ACAT CLI task
- ✅ Collab B (autonomy): SER 2 + F-50 confirmation
- ✅ Collab C (outreach): Phase 3 pilot notification
- ✅ Collab D (mesh-support): Observer role briefing

**Awaiting:** Practice replies by 2026-07-08

### SER 2 Proposal (Ready to dispatch)
**When:** 2026-07-09 (Day 3, after all 4 replies received)  
**Type:** architecture_decision, REFLEX (auto-accept)  
**ECO gate:** Day 4 EOD (2026-07-09)  
**SER 2 created:** Upon Accept → status=OPEN

### SER 1 (T4)
**Status:** Proposal ready in T4_SER1_PROPOSAL_FOR_MESH_SUPPORT.md  
**Action:** mesh-support to execute cortex_propose  
**Timeline:** Immediate (unblocks T4 Phases 2–5)

---

## Repository State

**All commits + files:**
- e3cf6ac — assessment: ACAT CLI interface beneficial for Empirica integration
- 686a3f8 — log: Mesh outreach collabs dispatched - live coordination begins
- fc19aa4 — docs: Mesh outreach dispatch confirmation - authorization complete
- 85a7d9a — log: Mesh outreach dispatch - 4 FYI collabs for Empirica-ACAT framework
- fdf4024 — docs: Planning summary for Empirica-ACAT framework integration
- a135952 — docs: Mesh coordination brief for Empirica-ACAT framework
- 9e80b92 — plan: Empirica-ACAT integration framework for operational calibration
- 69bf515 — docs: T4 SER 1 proposal for mesh-support action

**Branch:** main (clean, all changes committed)

---

## Next Checkpoints

| Date | Event | Status |
|------|-------|--------|
| 2026-07-08 (Day 2) | Practice replies due | ⏳ Awaiting |
| 2026-07-09 (Day 3) | SER 2 proposal dispatch | 📤 Queued |
| 2026-07-09 EOD (Day 4) | ECO gate decision | 🔐 Gates |
| 2026-07-10 (Day 5) | Week 1 execution begins | 🚀 Launch |

---

## Authorization & Closure

**User:** Carly R. Anderson (empirica-foundation Admiral + Evaluator)  
**Authorization:** All three options (A, A, A) confirmed 2026-07-06  
**Goals closed:** T3 (ACAT-Empirica Integration), T4 (12-Month Roadmap)  
**Status:** ✅ **FINALIZED — READY FOR EXECUTION**

**The Empirica-ACAT framework is now a constitutional, multi-practice, measurable calibration system with locked execution plans, mesh coordination in motion, and SER 2 staged to launch Week 1. Your dual-instrument grounding begins with SER 2 creation pending Week 1 start.**

---

*This document closes all planning. Execution begins 2026-07-10.*
