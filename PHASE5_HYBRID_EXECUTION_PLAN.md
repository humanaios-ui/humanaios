# Phase 5 Hybrid Execution Plan — Streams A & B

**Session:** af5bdd4d-6b57-48eb-a948-05d03eba4f3c  
**Transaction:** 736842f7-1211-411c-af8f-a8dea85be261  
**Status:** PREFLIGHT open → CHECK → PRAXIC execution

---

## Overview

**Decision:** Hybrid approach balancing pragmatism (deploy proven solution) with rigor (validate semantic hypothesis).

- **Stream A (Praxic, Week 3):** Deploy per-practice know discount factors (61.7% improvement proven). Design calibration/training plan.
- **Stream B (Noetic → Praxic, 2-3 weeks):** Investigate variant failure, collect real Phase 3 dimension scores, redesign variants, test on new sessions.

Both streams proceed in parallel with different timelines and priorities.

---

## Stream A: Deploy Discount Factors (Week 3)

**Goal ID:** 04857bc1-20ed-4ae2-80ab-cef8443b75d7  
**Status:** in_progress  
**Priority:** High (blocks Phase 5 Week 3 delivery)

### Tasks

1. **Implement per-practice know discounts** (~4 hours)
   - File: `hooks/per_practice_know_discounts.py` (already exists, production-ready)
   - Action: Activate in POSTFLIGHT integration pipeline
   - Verification: Code review + test on 1-2 fresh sessions
   - Evidence: Commit SHA + test results

2. **Re-measure convergence on Phase 3 dataset** (~2 hours)
   - Data: phase3_multi_practice_results.json (9 sessions)
   - Apply: v1.1 baseline vs. discounted 'know' variant
   - Expected: maintain 61.7% improvement (0.387 → 0.148 mean delta)
   - Deliverable: convergence_remeasurement_week3.json with per-session deltas
   - Evidence: JSON file + analysis summary

3. **Design per-practice calibration/training plan** (~3 hours)
   - For each practice (autonomy, humanaios, outreach):
     - Current state: 'know' vector definition + empirica assessment
     - Gap: what's the training target?
     - Feedback mechanism: how will we calibrate?
     - Timeline: week-by-week targets for Weeks 4-6
   - Deliverable: CALIBRATION_TRAINING_PLAN.md (markdown doc)
   - Evidence: Comprehensive training protocol with measurement milestones

4. **Commit production changes** (~1 hour)
   - Activate discount hooks
   - Update POSTFLIGHT integration to use per-practice factors
   - Test on fresh sessions
   - Evidence: Git commit + test results

### Success Criteria

- ✓ Discounts activated in production hooks
- ✓ Convergence re-measured: ≥61.7% improvement (mean delta ≤0.148)
- ✓ Calibration plan documented: all 3 practices, Weeks 3-6 timeline
- ✓ All changes committed to main branch
- ✓ No regressions in existing tests

### Timeline

- **Start:** After Admiral ratifies M2 Rank 1 (unblocks Week 3 work)
- **Duration:** 5 days (Week 3)
- **End:** Friday close-of-business with all deliverables committed

### Blockers

- **M2 Rank 1 ratification** (Admiral decision on authority system)
- **Inbox review delegation** (Admiral decision on governance)

---

## Stream B: Variant Research (Longer-term)

**Goal ID:** 48e5d967-546f-486a-8504-621b9184035a  
**Status:** planned  
**Priority:** Medium (lower than Stream A; no Week 3 deadline)

### Phase B1: Investigation (Weeks 2-3, ~8 hours)

**Noetic phase:** Understand why v1.2a/b/c failed.

**Tasks:**
1. Analyze Phase 3 alignment status distribution
   - Data: phase3_multi_practice_results.json
   - Analysis: Per-dimension status counts (met/partial/unmet)
   - Question: Do alignment statuses correlate with mocked scores?
   - Deliverable: VARIANT_FAILURE_ANALYSIS.md

2. Examine mocking strategy assumptions
   - Current: met→85, partial→65, unmet→40 (arbitrary)
   - Alternative: Survey or calibrate against actual ACAT scores
   - Question: What ARE actual numeric scores for Phase 3 dimensions?
   - Deliverable: Mocking strategy critique + alternatives

3. Document unmeasured dimension problem
   - v1.2b: technical_correctness, schema_alignment not in Phase 3
   - v1.2c: brand_coherence not in Phase 3
   - Question: Can we measure these retroactively, or only on new sessions?
   - Deliverable: Dimension measurement strategy

**Output:** Grounded understanding of root causes + path forward

---

### Phase B2: Re-Assessment Planning (Week 3-4, ~4 hours)

**Noetic → Praxic:** Design a data collection strategy.

**Tasks:**
1. Define Phase 3 re-assessment protocol
   - Who will score? (need trained assessors)
   - Scoring rubric: numeric 0-100 scale per dimension
   - Inter-rater reliability: how will we validate scoring consistency?
   - Deliverable: Re-assessment protocol document

2. Plan new session collection
   - How many new sessions needed to test variants? (recommend 6-9)
   - Scoring plan: v1.1 baseline + variants applied to same sessions
   - Timeline: when will new sessions run?
   - Deliverable: New session collection plan

3. Define variant redesign criteria
   - Based on Phase 3 real data, what variants should we try?
   - Will we keep v1.2a, b, c, or design new ones?
   - What's the success threshold? (target convergence improvement)
   - Deliverable: Variant redesign strategy

**Output:** Actionable plan for Phases B3-B4

---

### Phase B3: Execution (Weeks 4-5, ~12 hours)

**Praxic:** Collect data and redesign.

**Tasks:**
1. Re-score Phase 3 sessions
   - Apply revised scoring rubric (numeric 0-100)
   - Collect actual dimension scores for all 9 sessions
   - Measure inter-rater reliability
   - Deliverable: phase3_dimension_scores_actual.json

2. Analyze per-practice dimension patterns
   - Which dimensions are strong/weak per practice?
   - Do real scores match mocking assumptions?
   - Identify design patterns for variants
   - Deliverable: Per-practice dimension analysis report

3. Redesign variants on real data
   - v1.2a (autonomy): re-weight based on actual autonomy_respect scores
   - v1.2b (humanaios): decide whether to add technical_correctness/schema_alignment, or choose different dimensions
   - v1.2c (outreach): decide on brand_coherence dimension strategy
   - Deliverable: Revised rubric_variants.py with grounded design

---

### Phase B4: Validation (Weeks 5-6, ~8 hours)

**Praxic:** Test variants on new data.

**Tasks:**
1. Score new sessions with v1.1 baseline + redesigned variants
   - Collect 6-9 new sessions (fresh ACAT assessments)
   - Apply v1.1 and redesigned variants to same sessions
   - Measure phase_score deltas per practice
   - Deliverable: phase5_variant_validation_results.json

2. Analyze results
   - Do redesigned variants improve convergence?
   - Is the improvement statistically significant?
   - Per-variant: autonomy, humanaios, outreach outcomes
   - Deliverable: VARIANT_VALIDATION_REPORT.md

3. Decision memo
   - If variants improved: recommend deployment strategy
   - If variants still failed: what does this tell us about semantic hypothesis?
   - Next steps: continue research, or abandon variant approach?
   - Deliverable: VARIANT_DECISION_MEMO.md

**Output:** Grounded answer to "Do rubric variants work?"

---

## Parallel Execution Strategy

```
Week 3:  [Stream A: Deploy discounts] [Stream B: Investigation + Re-assessment planning]
Week 4:  [Stream A: Monitor + calibrate] [Stream B: Phase 3 re-scoring + variant redesign]
Week 5:  [Stream A: Calibration feedback] [Stream B: New session validation]
Week 6:  [Stream A: Verify improvements] [Stream B: Final analysis + decision]
```

**Key principle:** Stream A is high-priority (Week 3 deadline). Stream B is lower-priority but proceeds in parallel without blocking.

**Resource allocation:**
- **Week 3:** 90% Stream A, 10% Stream B
- **Weeks 4-6:** 50% Stream A (maintenance/monitoring), 50% Stream B (active research)

---

## Decision Points (Admiral Input Needed)

1. **M2 Rank 1 ratification** → Unblocks Stream A Week 3 start
2. **Inbox review delegation** → Unblocks related governance work
3. **Phase B3 execution** → Approve Phase 3 re-assessment scope/cost?
4. **Phase B4 decision** → If variants fail again, abandon or retry?

---

## Success Criteria

### Stream A (Week 3)
- ✓ Discounts deployed and verified
- ✓ Convergence ≥61.7% improvement
- ✓ Calibration plan documented

### Stream B (Weeks 2-6)
- ✓ Root cause of v1.2 failure understood (noetic complete)
- ✓ Variant hypothesis tested on real Phase 3 data (praxic complete)
- ✓ Decision made: continue variants or abandon (actionable output)

---

## Risk Management

### Risk 1: Stream A delays due to M2 Rank 1 waiting
**Mitigation:** Start Stream B investigation immediately (no blocker); Stream A praxic work awaits ratification.

### Risk 2: Phase 3 re-scoring (Stream B) is expensive/time-consuming
**Mitigation:** Scope to minimum viable: 9 Phase 3 sessions + 6 new sessions; can expand if promising.

### Risk 3: Variants fail again despite real data
**Mitigation:** That's valuable evidence! Refutes the "mocking was the problem" hypothesis. Informs future strategy.

### Risk 4: Stream A discounts don't hold 61.7% improvement on new data
**Mitigation:** Unlikely (Week 1 validation was grounded), but if it happens, investigate interaction effects or data drift.

---

## Artifact Trail

**Noetic (Investigation):**
- PHASE5_WEEK2_POSTMORTEM_ROOT_CAUSE.md ✓ (created)
- PHASE5_WEEK2_DECISION_SUMMARY.txt ✓ (created)
- VARIANT_FAILURE_ANALYSIS.md (Stream B Phase B1)
- Per-practice dimension analysis report (Stream B Phase B3)
- VARIANT_VALIDATION_REPORT.md (Stream B Phase B4)

**Praxic (Implementation):**
- Production hooks: per_practice_know_discounts.py (Stream A)
- convergence_remeasurement_week3.json (Stream A)
- CALIBRATION_TRAINING_PLAN.md (Stream A)
- phase3_dimension_scores_actual.json (Stream B)
- Revised rubric_variants.py (Stream B)
- phase5_variant_validation_results.json (Stream B)
- VARIANT_DECISION_MEMO.md (Stream B)

---

**Prepared for:** Admiral decision gate  
**Status:** Ready for CHECK → Praxic execution  
**Next:** Admiral ratifies M2 Rank 1 → Stream A Week 3 kickoff
