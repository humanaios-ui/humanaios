# Temporal-to-Resource Conversion — Complete Plan

**Status:** Planning Phase Complete | Ready to Execute  
**Session:** 3654c4c0 (PREFLIGHT open)  
**Goals:** 5 strategic, 18 tactical tasks  
**Expected Duration:** ~10 sessions  
**New Practice Seat:** empirica-temporal-oracle (measurement + prediction)

---

## The Problem

**Current State:**
- Framework designed (RESOURCE_MEASUREMENT_CONTRACT exists)
- Discipline active in mesh-support only
- CRITICAL BUG: Operations tooling still hardwired for temporal language ("by Friday", "deadline", elapsed time)
- Adoption stalled at 1 of 15 practices

**Impact:**
- 14 practices still using temporal framing (calendar deadlines, time estimates)
- Sentinel gates replace temporal (77-day) with resource-based (labor budget exceeded)
- empirica CLI still requires manual JSON submission (no resource flags)
- Budget models inaccurate (predict time, not labor hours)

---

## The Solution: 5 Strategic Goals

### Goal 1: Fix Operations Bug (CRITICAL) — 4 tasks

**Objective:** Replace temporal hardwiring in operations tooling

**Tasks:**
1. **T1.1:** Audit operations repo for temporal language (grep, find, document)
2. **T1.2:** Document all findings (file, line, current text, replacement)
3. **T1.3:** Replace calendar language with resource accounting
4. **T1.4:** Test hooks emit resource-based POSTFLIGHT payloads

**Deliverables:**
- Zero temporal language in operations tooling ✓
- POSTFLIGHT payloads include labor hours, token burn, validation metrics ✓
- Hooks block temporal references (enforce resource framing) ✓

**Effort:** 2 sessions  
**Blocker status:** None (unblocks everything else)

---

### Goal 2: Launch empirica-temporal-oracle Seat — 4 tasks

**Objective:** Create new practice for resource measurement and prediction

**Why:** Temporal measurement is itself a specialized domain. Need a dedicated practice to:
- Train prediction models (token burn per work_type, labor efficiency per practice)
- Calibrate resource budgets (ground truth vs estimates)
- Provide resource oracles (forecast consumption, validate allocations)
- Close the feedback loop (measurement → prediction → validation → recalibration)

**Tasks:**
1. **T2.1:** Design charter, domain, mesh role for temporal-oracle
2. **T2.2:** Create directory, .empirica/project.yaml, register in cortex
3. **T2.3:** Build prediction models (token burn, labor efficiency)
4. **T2.4:** Wire oracle into PREFLIGHT injection (forecast resources, validate budgets)

**New Practice Identity:**
- Name: `empirica-temporal-oracle`
- Canonical: `empirica-foundation.carly.empirica-temporal-oracle`
- Role: Observer + Specialist (measurement, forecasting, calibration)
- Reporting: To evaluator + mesh-support (governance)

**Deliverables:**
- Fully operational temporal-oracle practice ✓
- Prediction models trained on 2+ weeks of resource data ✓
- PREFLIGHT injection shows "estimated labor 1.5-2h, tokens 40k-50k, confidence 0.85" ✓

**Effort:** 3 sessions  
**Blocker status:** Depends on Goal 1 (need clean resource data)

---

### Goal 3: Standardize Contracts Across Foundation — 4 tasks

**Objective:** Adopt RESOURCE_MEASUREMENT_CONTRACT in all 15 practices

**Tasks:**
1. **T3.1:** Publish contract to shared location (mesh-support docs + source-add --visibility shared)
2. **T3.2:** Create per-practice briefing (what changed, how to estimate, how to confirm hours)
3. **T3.3:** Coordinate rollout (mesh collabs, adoption cadence, support)
4. **T3.4:** Verify adoption (5+ practices submitting resource-based payloads)

**Adoption Path:**
- **Phase A (Async):** Briefs issued to all 15 practices → Gate: All practices registered
- **Phase B (Async):** When ANY 5 practices submit resource-based POSTFLIGHT payloads → Gate: 5+ payloads received
- **Phase C (Async):** When ALL 15 practices submit resource-based POSTFLIGHT payloads → Gate: 15 payloads received
- **Ongoing:** Measurement-first protocol + temporal-oracle feedback loop (gates trigger immediately, not on calendar)

**Deliverables:**
- All 15 practices submitting resource-based PREFLIGHT/POSTFLIGHT ✓
- 100+ sessions with resource anchor state ✓
- Measurement data feeds temporal-oracle for calibration ✓

**Effort:** 2 sessions  
**Blocker status:** Depends on Goal 1 + 2 (need clean data + oracle ready)

---

### Goal 4: Wire empirica CLI — 3 tasks

**Objective:** Make resource-based measurement default, not exception

**Current friction:** Manual JSON submission
```bash
empirica preflight-submit - << 'EOF'
{ "resource_anchor": {...} }
EOF
```

**Future ergonomics:**
```bash
empirica preflight-submit \
  --estimate-hours 1.5-2.0 \
  --estimate-tokens 40k-50k \
  --work-type research \
  --vectors know:0.7 uncertainty:0.3

empirica postflight-submit \
  --human-active-hours 1.75 \
  --vectors know:0.85 uncertainty:0.15
```

**Tasks:**
1. **T4.1:** Add flags to `empirica preflight-submit` (--estimate-hours, --estimate-tokens, --work-type)
2. **T4.2:** Add flags to `empirica postflight-submit` (--human-active-hours + prompt)
3. **T4.3:** End-to-end testing (preflight → execution → postflight → verify payload)

**Deliverables:**
- empirica CLI accepts resource-based flags ✓
- Payloads automatically formatted (backward compatible) ✓
- --help shows resource parameters ✓

**Effort:** 1.5 sessions  
**Blocker status:** None (can parallelize with Goal 3)

---

### Goal 5: Migrate Sentinel Gates — 3 tasks

**Objective:** Score practices on resource efficiency, not calendar adherence

**Current Sentinel gates (temporal):**
- Labor budget exceeded → alert + rebudget
- Session without close → blocker
- Readiness gate: max_uncertainty 0.35 (blocks honest corrections)

**Resource-based gates (proposed):**
- Labor budget exceeded → alert + rebudget
- Token budget exceeded by 10% → warning
- Validation overhead > 2.5x baseline → investigate
- Readiness gate: measure active work (labor hours, token burn), not uncertainty

**Tasks:**
1. **T5.1:** Design Sentinel resource-based scoring (labor, tokens, validation)
2. **T5.2:** Migrate readiness gate (from temporal/uncertainty to resource criteria)
3. **T5.3:** Test on 3 practices (verify scoring, gates, feedback)

**Deliverables:**
- Sentinel scores practices on resource consumption ✓
- Readiness gate measures work, not time ✓
- Alert thresholds grounded in resource data ✓

**Effort:** 2 sessions  
**Blocker status:** Depends on Goal 3 (need measurement data for calibration)

---

## Execution Sequence

```
PARALLEL (No dependencies):
  ├─ Goal 1: Fix operations bug (2 sessions) — CRITICAL PATH
  ├─ Goal 4: Wire empirica CLI (1.5 sessions)
  └─ Research for Goal 2: Prediction models (1 session prep)

AFTER Goal 1 + 2-prep:
  ├─ Goal 2: Launch temporal-oracle (3 sessions)
  ├─ Goal 3: Standardize contracts (2 sessions)  — can start during Goal 2
  └─ Goal 5: Migrate Sentinel (2 sessions)     — after Goal 3 provides data

SEQUENTIAL:
  Goal 1 → (2-4) → 3, 4, 5 all parallel → verification/validation

Total: ~10 sessions (3+4+1.5+3+2+2 = 15.5, but overlap = ~10 actual)
Timeline: ~10 sessions cumulative (parallelizable goal groups; no weekly constraint)
```

---

## Milestones

| Milestone | Target | Dependencies |
|-----------|--------|---------|
| **M1: Fix ops bug** | After T1.1+T1.2 complete | None (critical path) |
| **M2: Oracle seat live** | When M1 + oracle practice ready | M1 |
| **M3: 5 practices adopting** | When 5 practices submit payloads | M1, M2 |
| **M4: CLI working** | When M1 + CLI flags implemented | M1 (data only) |
| **M5: All 15 practices** | When remaining 10 adopt | M3 |
| **M6: Sentinel live** | When M5 provides calibration data | M5 (calibration data) |

---
**Goal 2:** Temporal-oracle practice operational; makes resource predictions; 70%+ accuracy on budget estimates  
**Goal 3:** 15/15 practices submitting resource-based payloads; 100+ sessions with resource anchor  
**Goal 4:** empirica CLI accepts resource flags; payloads validate against schema  
**Goal 5:** Sentinel gates live; score practices on labor/tokens; alert thresholds tested

### System-wide

- ✅ Zero temporal framing in new transactions (all use resource anchor)
- ✅ Sentinel measures resource consumption, not elapsed time
- ✅ empirica-temporal-oracle provides feedback loop (measurement → prediction → validation)
- ✅ Budget estimates within 15% of actual (from prior 50%+ error)

---

## What Changes for Practices

### PREFLIGHT (Before)
```json
{
  "vectors": {"know": 0.7, "uncertainty": 0.3}
}
```

### PREFLIGHT (After)
```json
{
  "resource_anchor": {
    "human_labor_cumulative_hours": 49.8,
    "human_labor_budget_remaining": 46.5,
    "ai_tokens_budget_remaining": 1_065_000
  },
  "resource_scope_this_transaction": {
    "estimated_human_hours": "1.5-2.0",
    "estimated_ai_tokens": "40k-50k",
    "work_type": "research"
  },
  "vectors": {"know": 0.7, "uncertainty": 0.3}
}
```

### POSTFLIGHT (After)
```json
{
  "session_duration": {
    "human_active_hours": 1.75
  },
  "resource_accounting": {
    "human_labor_this_session": 1.75,
    "ai_tokens_consumed": 42_500
  },
  "validation_metrics": {
    "corrections_per_100_tokens": 1.8,
    "prompt_refinement_cycles_actual": 2,
    "review_time_minutes_actual": 22
  },
  "return_on_resources": {
    "labor_to_findings_ratio": "1 finding per 0.44 hours",
    "tokens_to_findings_ratio": "1 finding per 10.6k tokens"
  }
}
```

---

## Next Step: Begin Execution

All 5 goals created with 18 tasks. Ready to:

1. ✅ Commit this plan
2. ✅ Run POSTFLIGHT closing this planning phase
3. ✅ Begin execution (Goals 1 + 4 + research for 2 in parallel)
4. ✅ Track progress per milestone

**Execution starts immediately after POSTFLIGHT.**

---

**Authored by:** Claude (empirica-foundation-evaluator)  
**Session:** 3654c4c0 | PREFLIGHT 68fed374  
**Status:** Planning complete | Ready to execute | No blockers
