# Phase 5 Hybrid Execution — KICKOFF (M2 Ratified)

**Date:** 2026-07-23  
**Status:** ✅ M2 Rank 1 RATIFIED | ✅ Resource constraints confirmed | ✅ Both streams ACTIVE  
**Ready for:** Immediate execution

---

## Execution Status

### Blockers Cleared

- ✅ **M2 Rank 1 Authority System:** Admiral ratified (governance system active)
- ✅ **Hybrid Approach Approved:** Fits timeline and resource budget
- ✅ **Both Streams Activated:** Stream A (in_progress), Stream B (in_progress)

### Go Live

Both work streams are now active and operational.

---

## Stream A: Week 3 Execution Plan (High-Priority)

**Goal ID:** 04857bc1-20ed-4ae2-80ab-cef8443b75d7  
**Status:** in_progress  
**Duration:** This week (5 days, Mon–Fri)  
**Timeline:**
- **Mon–Tue:** Implement discount factors in production
- **Wed:** Re-measure convergence on Phase 3 data
- **Thu:** Design calibration/training plan
- **Fri:** Commit, test, document

### Task 1: Implement Per-Practice Know Discounts

**What:** Activate the proven Week 1 discount factors in POSTFLIGHT hooks

```
autonomy:   know × 0.65  (was overestimating by ~35%)
humanaios:  know × 0.75  (was overestimating by ~25%)
outreach:   know × 0.85  (was overestimating by ~15%)
```

**Where:** `hooks/per_practice_know_discounts.py` (already exists, production-ready)

**Actions:**
1. Code review: per_practice_know_discounts.py
2. Integrate into POSTFLIGHT pipeline
3. Test on 1-2 fresh sessions
4. Verify no test regressions

**Evidence:** Commit SHA + test results

**Estimated time:** 4 hours

---

### Task 2: Re-Measure Convergence

**What:** Apply discount factors to Phase 3 dataset and verify 61.7% improvement holds

**Data:** phase3_multi_practice_results.json (9 sessions)

**Process:**
1. Load Phase 3 sessions
2. Compute convergence delta with v1.1 baseline (no discounts)
3. Compute convergence delta with discounted 'know' variant
4. Calculate improvement percentage per practice + aggregate
5. **Target:** Mean delta ≤ 0.148 (maintaining 61.7% improvement from 0.387)

**Deliverable:** `convergence_remeasurement_week3.json`

```json
{
  "baseline_convergence": 0.387,
  "discounted_convergence": 0.148,
  "improvement_pct": 61.7,
  "per_practice": {
    "autonomy": {...},
    "humanaios": {...},
    "outreach": {...}
  }
}
```

**Evidence:** JSON file + written analysis

**Estimated time:** 2 hours

---

### Task 3: Design Calibration/Training Plan

**What:** Document per-practice calibration targets and feedback mechanisms for Weeks 4–6

**For each practice (autonomy, humanaios, outreach):**

1. **Current State**
   - 'know' vector definition (what does it measure?)
   - Current empirica assessment from Phase 3
   - Current ACAT convergence delta

2. **Calibration Target**
   - Where should 'know' be at end of Week 6?
   - What empirica-ACAT convergence delta are we targeting?
   - What does "well-calibrated" look like for this practice?

3. **Feedback Mechanism**
   - How will the practice get feedback on their calibration?
   - Weekly check-ins? Spot assessments? Convergence tracking?
   - Who is responsible for feedback (you or the practice)?

4. **Timeline**
   - Week 4: Initial feedback, identify gaps
   - Week 5: Targeted calibration work
   - Week 6: Final assessment, measure improvement

**Deliverable:** `CALIBRATION_TRAINING_PLAN.md` (markdown document, ~2-3 pages)

**Evidence:** Comprehensive training protocol with measurement milestones

**Estimated time:** 3 hours

---

### Task 4: Commit Production Changes

**What:** Finalize, test, and commit all Stream A work

**Actions:**
1. Final code review of discount factor hooks
2. Run test suite (verify no regressions)
3. Test on 1-2 fresh sessions (spot-check convergence improvement)
4. Commit to main: `feat(phase5-week3): activate per-practice know discounts`
5. Verify commit is on main branch

**Evidence:** Commit SHA + test results summary

**Estimated time:** 1 hour

---

### Success Criteria (All Required)

- ✅ Discounts activated in production hooks
- ✅ Convergence re-measured: mean delta ≤ 0.148 (≥61.7% improvement)
- ✅ Per-practice calibration targets defined (autonomy, humanaios, outreach)
- ✅ Calibration/training plan documented (Weeks 4–6 timeline)
- ✅ All changes committed to main
- ✅ No test regressions
- ✅ Ready for Weeks 4–6 calibration phase

---

## Stream B: Variant Research (Parallel, Lower-Priority)

**Goal ID:** 48e5d967-546f-486a-8504-621b9184035a  
**Status:** in_progress  
**Duration:** 2–3 weeks (Weeks 2–6, in parallel with Stream A)  
**Priority:** Medium (research track, no Week 3 blocker)

### Phase B1: Investigation (Start This Week)

**Objective:** Understand why v1.2a/b/c failed using grounded analysis

**Tasks:**
1. Analyze Phase 3 alignment status distribution
   - Count met/partial/unmet per dimension across 9 sessions
   - Compare to mocking strategy (met→85, partial→65, unmet→40)
   - Question: Do real scores match mocking assumptions?

2. Examine dimension score problem
   - Data: phase3_multi_practice_results.json
   - Analysis: What actual numeric scores were ACAT scoring?
   - Finding: Were scores in the assumed ranges, or different?

3. Document unmeasured dimensions
   - v1.2b: technical_correctness, schema_alignment not measured in Phase 3
   - v1.2c: brand_coherence not measured in Phase 3
   - Decision: Can these be retroactively scored, or only forward?

**Deliverable:** `VARIANT_FAILURE_ANALYSIS.md` (analysis + findings)

**Estimated time:** 8 hours (spread across this week and next)

---

### Phase B2: Re-Assessment Planning (Weeks 3–4)

**Objective:** Design data collection strategy for real variant validation

**Tasks:**
1. Define Phase 3 re-assessment protocol
   - Scoring rubric: 0-100 numeric scale per dimension
   - Who scores? (trained assessors needed)
   - Inter-rater reliability: how to validate consistency?

2. Plan new session collection
   - How many new sessions? (recommend 6-9)
   - When will they run? (Week 5?)
   - How will they be scored? (v1.1 baseline + variants)

3. Variant redesign criteria
   - Based on Phase 3 real data, what variants should we try?
   - Keep v1.2a/b/c, or design new ones?
   - Success threshold? (target convergence improvement)

**Deliverable:** Re-assessment protocol + new session plan + variant strategy

**Estimated time:** 4 hours (Weeks 3–4)

---

### Phase B3: Execution (Weeks 4–5)

**Objective:** Collect real data and redesign variants

**Tasks:**
1. Re-score Phase 3 with revised numeric rubric
2. Analyze per-practice dimension patterns
3. Redesign variants based on actual data

**Deliverable:** Revised `rubric_variants.py` with grounded design

**Estimated time:** 12 hours (Weeks 4–5)

---

### Phase B4: Validation (Weeks 5–6)

**Objective:** Test variants on new data

**Tasks:**
1. Score new sessions with v1.1 + redesigned variants
2. Analyze convergence improvement
3. Decision memo: deploy variants, refute hypothesis, or continue research?

**Deliverable:** `VARIANT_VALIDATION_REPORT.md` + `VARIANT_DECISION_MEMO.md`

**Estimated time:** 8 hours (Weeks 5–6)

---

## Weekly Allocation

```
Week 3:
  Stream A: 90% (primary focus, Week 3 deliverables)
  Stream B: 10% (start Phase B1 investigation)

Week 4:
  Stream A: 50% (monitor calibration, support practices)
  Stream B: 50% (continue Phase B1-B2, start Phase B3)

Week 5:
  Stream A: 40% (calibration feedback, monitoring)
  Stream B: 60% (Phase B3-B4, new session collection)

Week 6:
  Stream A: 30% (final verification)
  Stream B: 70% (Phase B4 validation, decision memo)
```

---

## Immediate Next Steps (This Week)

### Monday
- ✅ Review PHASE5_HYBRID_EXECUTION_PLAN.md (this file)
- ✅ Confirm resource allocation with team
- **Task:** Code review: per_practice_know_discounts.py

### Tuesday
- **Task:** Implement discounts, integrate into POSTFLIGHT
- **Task:** Test on 1-2 fresh sessions

### Wednesday
- **Task:** Re-measure convergence on Phase 3 data
- **Deliverable:** convergence_remeasurement_week3.json

### Thursday
- **Task:** Design calibration/training plan (3 practices)
- **Deliverable:** CALIBRATION_TRAINING_PLAN.md

### Friday
- **Task:** Test, commit, verify everything on main
- **Task:** Start Phase B1 investigation (alignment distribution analysis)

---

## Success Definition (End of Week 3)

✅ **Stream A Complete:**
- Discounts deployed and verified
- Convergence ≥61.7% improvement
- Calibration plan for all 3 practices
- All changes committed to main

✅ **Stream B Started:**
- Phase B1 investigation underway
- Findings logged to artifact graph
- Path forward clear (Phase B2 planning)

---

## Risk Management

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|-----------|
| Discounts don't hold in production | Low | High | Already proven on Phase 3; production hooks straightforward |
| Phase 3 convergence remeasurement takes longer | Medium | Medium | Start early; can parallelize with other tasks |
| Calibration plan needs Admiral input | Medium | Low | Can draft independently, iterate with feedback |
| Stream B interferes with Stream A | Low | Medium | Strict 90/10 allocation Week 3; review Wed if needed |

---

## Artifacts This Transaction

**Noetic (Investigation):**
- PHASE5_WEEK2_POSTMORTEM_ROOT_CAUSE.md ✓
- PHASE5_WEEK2_DECISION_SUMMARY.txt ✓
- Findings/decisions/unknowns artifact graph (13 nodes) ✓

**Praxic (Execution):**
- PHASE5_HYBRID_EXECUTION_PLAN.md ✓
- HYBRID_EXECUTION_KICKOFF.md ✓
- convergence_remeasurement_week3.json (due Wed)
- CALIBRATION_TRAINING_PLAN.md (due Thu)

**To be logged:**
- Phase B1 findings (mid-week)
- Production deployment evidence (Fri)

---

## Decision Points Remaining

**None blocking execution.** M2 Rank 1 ratified. Both streams active. Proceeding with hybrid plan.

Optional future decisions:
- **Week 4:** If Stream B Phase B1 findings suggest scope change, discuss with Admiral
- **Week 5:** If Phase B3 redesign reveals major changes needed, may need to extend timeline

---

**Prepared by:** empirica-foundation-evaluator  
**Authority:** M2 Rank 1 ratified, hybrid approach approved  
**Status:** READY FOR EXECUTION  
**Next:** Begin Stream A Task 1 immediately; Stream B Phase B1 parallel

---

*Execution timing clock starts now. Stream A delivers end of Week 3. Stream B runs in parallel, reports Weeks 5–6.*
