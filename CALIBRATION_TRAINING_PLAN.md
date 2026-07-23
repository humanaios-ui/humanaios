# Phase 5 Weeks 4-6: Per-Practice Calibration & Training Plan

**Date:** 2026-07-23  
**Author:** empirica-foundation-evaluator  
**Objective:** Calibrate per-practice 'know' vectors to achieve empirica-ACAT convergence targets  
**Scope:** autonomy, humanaios, outreach (3 practices)  
**Timeline:** Weeks 4, 5, 6 (3-week intensive calibration cycle)

---

## Executive Summary

Week 3 Task 2 re-measured convergence with discount factors applied:
- Overall: 61.7% improvement (0.3873 → 0.1483 mean delta) ✅ **PASS**
- Autonomy: 84.3% improvement (0.0618 effective) ✅ **STRONG**
- Humanaios: 63.4% improvement (0.1427 effective) ✅ **ADEQUATE**
- Outreach: 36.4% improvement (0.2403 effective) ⚠️ **INSUFFICIENT**

**Strategy:** Maintain autonomy (no work), monitor humanaios (light feedback), and conduct intensive calibration on outreach (primary focus).

---

## Why Per-Practice Calibration Matters

The 'know' vector means different things per practice:
- **autonomy:** "How confident am I in my routing decisions?" (operational)
- **humanaios:** "How well do I understand the rubric mechanics?" (technical)
- **outreach:** "How consistent is my voice with established tone?" (performative)

Each semantic requires different calibration:
- Autonomy needs validation against routing outcomes
- Humanaios needs technical verification against rubric specs
- Outreach needs **tone/performance feedback** against brand guidelines

The discount factors address *magnitude* (how much to reduce), but calibration addresses *semantics* (what the vector actually measures and whether current assessment is accurate).

---

## Practice 1: Autonomy

### Current State

| Metric | Value | Assessment |
|--------|-------|-----------|
| 'know' definition | Operational routing confidence | Confidence in ECO proposal routing |
| Phase 3 baseline delta | 0.3940 | Significantly overestimated |
| Phase 5 effective delta | 0.0618 | Nearly aligned ✅ |
| Discount factor | 0.65× | Highly effective |
| Sessions meeting target (≤0.148) | 3/3 | 100% pass rate |

### Calibration Target (End of Week 6)

**Goal:** Maintain current performance (effective delta ≤0.065)

| Target | Value | Rationale |
|--------|-------|-----------|
| Empirica 'know' | 0.85–0.95 | High confidence in routing (data-driven) |
| Effective 'know' (with 0.65× discount) | 0.55–0.62 | After discount, aligned with ACAT observation |
| Convergence delta | ≤0.065 | Maintain current strong alignment |
| Confidence ratio | know/uncertainty ≥ 3.0 | Self-assessment confidence justified |

### Calibration Mechanism (Weeks 4-6)

#### Week 4: Establish Baseline
- **Activity:** Review autonomy's Phase 3 routing decisions against actual outcomes
  - Which routing decisions were correct? (measure against subsequent outcomes)
  - Which routing decisions were incorrect or uncertain? (identify failure patterns)
  - Does empirica 'know' track actual routing accuracy?

- **Feedback:** "Here's your routing accuracy in Phase 3 sessions: X% correct. Your 'know' assessment was {0.85}, actual accuracy was {Y}%. Alignment is {good/needs work}."

- **Measurement:** Routing accuracy percentage + 'know' correlation

#### Week 5: Identify Gaps
- **Activity:** Analyze where 'know' diverges from actual routing performance
  - Sessions where 'know' was high but routing was uncertain → overconfidence
  - Sessions where 'know' was high and routing was correct → accurate
  - Pattern analysis: are there specific routing scenarios where confidence is misplaced?

- **Feedback:** "Your 'know' is most accurate on [scenario A], less accurate on [scenario B]. Recommend focusing awareness on [specific routing type]."

- **Measurement:** Per-scenario confidence correlation

#### Week 6: Verify Stability
- **Activity:** Conduct new routing sessions and measure convergence in real-time
  - Run 2-3 new autonomy sessions
  - Score with ACAT (get phase_score)
  - Apply discount and measure convergence delta
  - Compare to Week 3 baseline (target: ≤0.065)

- **Feedback:** "Your calibration is stable. Convergence delta: {value}. Status: {green}."

- **Measurement:** Convergence delta on new data

### Success Criteria

✅ **Primary:** Effective convergence delta remains ≤0.065 (maintain current performance)  
✅ **Secondary:** Routing accuracy tracking shows ≥85% correct decisions  
✅ **Tertiary:** No significant variance week-to-week (stability)

### Timeline

| Week | Deliverable | Owner |
|------|-------------|-------|
| Week 4 (Mon–Wed) | Routing accuracy analysis + Week 4 feedback | empirica-foundation-evaluator |
| Week 5 (Thu–Fri) | Gap analysis + per-scenario feedback | empirica-foundation-evaluator |
| Week 6 (Mon–Wed) | New autonomy sessions scored + convergence verified | autonomy practice |
| Week 6 (Thu–Fri) | Calibration report + sign-off | empirica-foundation-evaluator |

---

## Practice 2: Humanaios

### Current State

| Metric | Value | Assessment |
|--------|-------|-----------|
| 'know' definition | Technical rubric comprehension | Understanding of dimension weights, semantics |
| Phase 3 baseline delta | 0.3900 | Moderately overestimated |
| Phase 5 effective delta | 0.1427 | Just below target (0.148) ⚠️ |
| Discount factor | 0.75× | Adequate but tight |
| Sessions meeting target (≤0.148) | 2.5/3 | ~83% pass rate (1 marginal) |

### Calibration Target (End of Week 6)

**Goal:** Move effective delta from 0.1427 → 0.125 (5% improvement buffer)

| Target | Value | Rationale |
|--------|-------|-----------|
| Empirica 'know' | 0.88–0.98 | High comprehension of rubric mechanics |
| Effective 'know' (with 0.75× discount) | 0.66–0.74 | After discount, safely below 0.148 target |
| Convergence delta | ≤0.125 | Add buffer (currently at 0.1427, target 0.148) |
| Confidence ratio | know/uncertainty ≥ 2.5 | High certainty justified for technical work |

### Calibration Mechanism (Weeks 4-6)

#### Week 4: Spot Check
- **Activity:** Verify humanaios's rubric comprehension against actual implementation
  - Dimension weights: does humanaios's understanding match the coded weights?
  - Semantic definitions: does humanaios's phrasing match rubric intent?
  - Edge cases: are there dimensions where humanaios's model diverges from spec?

- **Feedback:** "Your rubric comprehension is {high/moderate}. Dimension understanding: {dimension A} perfect, {dimension B} 90%, {dimension C} needs work. Recommend review of {dimension C} semantics."

- **Measurement:** Comprehension accuracy by dimension

#### Week 5: Light Training
- **Activity:** Focused review of any divergent dimensions identified in Week 4
  - Read rubric spec carefully for flagged dimensions
  - Self-assess 'know' specifically on those dimensions
  - Document any misunderstandings or ambiguities

- **Feedback:** "After Week 5 review, your understanding of [dimension] improved from 75% → 95%. Current 'know' assessment for this dimension: recommend slight reduction from 0.95 → 0.90 to stay conservative."

- **Measurement:** Updated comprehension per dimension

#### Week 6: Validate
- **Activity:** New rubric refinement session (if applicable) or comprehension quiz
  - If refining rubric: score against technical correctness + schema alignment
  - If quiz: assess 'know' calibration via scenario-based questions
  - Measure convergence delta on new data

- **Feedback:** "Convergence delta on Week 6 work: 0.125 (within target). Calibration is stable. Your 'know' is now well-calibrated."

- **Measurement:** Convergence delta + comprehension accuracy

### Success Criteria

✅ **Primary:** Effective convergence delta improves from 0.1427 → 0.125 (moves away from target edge)  
✅ **Secondary:** Dimension-by-dimension comprehension ≥90% across all 6 rubric dimensions  
✅ **Tertiary:** Self-assessed 'know' matches external validation (correlation ≥0.85)

### Timeline

| Week | Deliverable | Owner |
|------|-------------|-------|
| Week 4 (Mon–Wed) | Rubric comprehension spot check + dimensional analysis | empirica-foundation-evaluator |
| Week 4 (Thu–Fri) | Week 4 feedback + dimension-specific guidance | empirica-foundation-evaluator |
| Week 5 (Mon–Wed) | Targeted review session on flagged dimensions | humanaios practice |
| Week 5 (Thu–Fri) | Updated self-assessment + comprehension re-score | empirica-foundation-evaluator |
| Week 6 (Mon–Wed) | New validation work (refine or quiz) + convergence measured | humanaios practice |
| Week 6 (Thu–Fri) | Calibration report + sign-off | empirica-foundation-evaluator |

---

## Practice 3: Outreach (PRIORITY)

### Current State

| Metric | Value | Assessment |
|--------|-------|-----------|
| 'know' definition | Voice consistency confidence | Consistency of tone with brand guidelines |
| Phase 3 baseline delta | 0.3780 | Highly overestimated |
| Phase 5 effective delta | 0.2403 | EXCEEDS target (0.148 by +0.0923) ❌ |
| Discount factor | 0.85× | **INSUFFICIENT** (only 15% reduction) |
| Sessions meeting target (≤0.148) | 0/3 | **0% pass rate** |

### Root Cause Analysis

**Why is outreach's discount factor insufficient?**

The 0.85× discount assumes outreach's 'know' is only 15% overestimated. But Phase 3 data shows:
- Effective delta: 0.2403 vs target 0.148 = **62% overestimation** (not 15%)
- To reach target: need effective_know of ~0.545 (from 0.378 baseline acat)
- Current effective_know: 0.2403 * (0.85 reverse calc) = wrong approach

**Better framing:** outreach's effective delta shows 'know' is still calibrated ~0.24 too high. The discount helps (reduces from 0.378 to 0.240), but the underlying semantic—"voice consistency confidence"—is fundamentally misaligned with ACAT's assessment of rubric compliance.

**Hypothesis:** outreach's 'know' measures "do I sound on-brand?" but ACAT measures "did I meet rubric requirements?" These are orthogonal dimensions.

### Calibration Target (End of Week 6)

**Goal:** Reduce effective delta from 0.2403 → 0.130 (42% improvement)

| Target | Value | Rationale |
|--------|-------|-----------|
| Empirica 'know' | 0.70–0.80 | Moderate-to-high brand voice confidence |
| Effective 'know' (with revised discount) | 0.45–0.52 | After discount, meets 0.148 target |
| Convergence delta | ≤0.130 | Safe margin below 0.148 |
| Confidence ratio | know/uncertainty ≥ 2.0 | Conservative confidence (lower than autonomy/humanaios) |
| Revised discount factor (implied) | 0.60–0.65× | Match autonomy's intensity (vs current 0.85×) |

### Calibration Mechanism (Weeks 4-6): Intensive

#### Week 4: Brand Tone Audit (Days 1-3)

**Activity:** Deep review of outreach's actual message generation vs brand guidelines

- **Task 1:** Analyze Phase 3 outreach sessions
  - Read each generated message
  - Compare against brand voice guidelines (tone, vocabulary, phrasing)
  - Rate brand coherence (1-10): how on-brand is each message?
  - Identify: which messages felt "on-brand" vs "off-brand" to evaluator

- **Task 2:** Identify voice consistency patterns
  - Sessions where outreach felt confident: were messages actually on-brand?
  - Sessions where outreach was uncertain: pattern in off-brand messages?
  - Does 'know' track actual brand coherence?

- **Deliverable:** "Voice Coherence Analysis" (1-2 pages)
  - Per-session brand coherence ratings (evaluator assessment)
  - Correlation between outreach's 'know' and actual brand coherence
  - Hypothesis: where is the mismatch?

**Feedback (End of Week 4):**
"Your brand voice coherence in Phase 3: {analysis results}. Your 'know' assessment was {0.8-0.9}, but actual coherence was {Y}. Gap: {delta}. This explains your convergence issue. You're overconfident about your brand consistency."

#### Week 5: Targeted Brand Training (Days 4-7)

**Activity:** Intensive training on brand voice definition + real-time feedback

- **Task 1:** Brand guidelines deep-dive
  - Review formal brand voice guidelines (tone, vocabulary, prohibited phrasing, approved metaphors)
  - Self-assess understanding: "Which dimensions define our brand voice?"
  - Create personal "brand voice checklist" for message generation

- **Task 2:** Guided message generation with live feedback
  - Generate 3-5 sample messages (outreach initiative)
  - Evaluator provides immediate feedback: "This is on-brand because...", "This diverges from brand because..."
  - Outreach revises and re-submits (iteration cycle)
  - Measure: how quickly does outreach learn feedback and apply it?

- **Task 3:** Confidence calibration
  - After each message, outreach estimates 'know': "I'm X% confident this is on-brand"
  - Evaluator provides ground truth: "Actually, this was {on/off}-brand, rating {score}"
  - Track: how well does outreach's confidence match actual performance?

- **Deliverable:** "Brand Voice Training Log" (3-5 messages + feedback cycles)

**Feedback (Mid-Week 5):**
"Initial training cycle: you're learning quickly. Messages 1-2 were off-brand, message 3 on-brand. Your confidence improved from 0.9 → 0.75 on message 3, which is good (more realistic). Continue this pattern in Week 6."

#### Week 6: Validation & Reset (Days 8-10)

**Activity:** Measure improvement via new outreach sessions with real-time coaching

- **Task 1:** New outreach messages under Week 6 conditions
  - Generate 2-3 new messages (not based on Phase 3 training material)
  - After generation, before submission: outreach self-assesses 'know'
  - Submit for ACAT scoring
  - Compare: does ACAT score now correlate better with outreach's 'know'?

- **Task 2:** Convergence re-measurement
  - Score Week 6 messages with ACAT rubric
  - Apply (possibly revised) discount factor
  - Compute convergence delta
  - Target: ≤0.130 (improvement from 0.2403)

- **Task 3:** Calibration validation
  - Compare Week 6 convergence to Week 3 baseline
  - If improved: celebrate and establish new baseline
  - If not improved: diagnose (is discount factor right? is training working?)

- **Deliverable:** "Week 6 Convergence Report" (new session data + analysis)

**Feedback (End of Week 6):**
"Week 6 convergence delta: {value}. Status: {green/yellow/red}. Your brand voice calibration is now {solid/improving/needs continued work}."

### Revised Discount Factor Decision

**Based on Week 4 findings, may need to update discount:**

Current: 0.85× (15% reduction) → ineffective
Needed: 0.60–0.65× (35–40% reduction) → match autonomy intensity

**Decision point (End of Week 4):** 
If analysis shows outreach's 'know' should be ~35–40% lower (not 15%), recommend **updating discount factor to 0.65×** before Week 6 validation.

### Success Criteria

✅ **Primary:** Effective convergence delta improves from 0.2403 → ≤0.130 (42% improvement)  
✅ **Secondary:** Brand voice coherence improves to ≥80% (evaluator assessment)  
✅ **Tertiary:** Week 6 convergence delta ≤0.130 (meets target on new data)  
✅ **Quaternary:** Self-assessed 'know' correlates with brand coherence (≥0.75 correlation)

### Timeline (INTENSIVE)

| Week | Deliverable | Owner |
|------|-------------|-------|
| Week 4 (Mon–Fri) | Voice Coherence Analysis + brand mismatch diagnosis | empirica-foundation-evaluator |
| **Week 4 (Fri)** | **Decision:** Update discount factor to 0.65× if needed | empirica-foundation-evaluator |
| Week 5 (Mon–Fri) | Brand Voice Training (deep-dive + guided iteration) | outreach + empirica-foundation-evaluator |
| Week 6 (Mon–Wed) | New outreach messages + ACAT scoring + convergence calc | outreach + empirica-foundation-evaluator |
| Week 6 (Thu–Fri) | Calibration validation report + sign-off | empirica-foundation-evaluator |

---

## Cross-Practice Summary

### Workload Allocation (Weeks 4-6)

| Practice | Effort | Focus | Owner | Checkpoints |
|----------|--------|-------|-------|------------|
| Autonomy | **LOW** | Maintain (≤0.065 delta) | empirica-foundation-evaluator | Week 4, 6 |
| Humanaios | **MEDIUM** | Monitor + light training (≤0.125 delta) | humanaios + evaluator | Week 4, 5, 6 |
| Outreach | **HIGH** | Intensive training (≤0.130 delta) | outreach + evaluator | Week 4 **decision**, 5, 6 |

### Weekly Rhythm

**Week 4:** Establish baselines, diagnose gaps, make outreach discount decision  
**Week 5:** Execute training/feedback (humanaios light, outreach intensive)  
**Week 6:** Validate on new data, measure convergence, finalize calibration

### Weekly Check-In Cadence

- **Mondays:** Weekly plan + prior-week summary
- **Wednesdays:** Mid-week progress check
- **Fridays:** Deliverable review + next week preview

---

## Success Definition (End of Week 6)

### Convergence Targets Met

✅ Autonomy: effective delta ≤0.065 (current: 0.0618) → maintain  
✅ Humanaios: effective delta ≤0.125 (current: 0.1427) → improve  
✅ Outreach: effective delta ≤0.130 (current: 0.2403) → major improvement

### Overall Convergence (All 3 Practices)

Expected: Mean effective delta ≤0.108 (down from current 0.1483)  
Improvement: ≤28% additional convergence gain on top of Week 3 61.7%  
Total convergence: 61.7% + 28% ≈ 80% improvement vs Phase 3 baseline

### Calibration Stability

✅ Per-practice 'know' vectors track actual performance (correlation ≥0.75 per practice)  
✅ Self-assessed confidence justified by external outcomes  
✅ No significant variance week-to-week (calibration stable)

---

## Measurement & Evidence Trail

### Artifacts to Create (Weeks 4-6)

- **Week 4:** 
  - Autonomy routing accuracy analysis
  - Humanaios comprehension spot check
  - Outreach Voice Coherence Analysis + discount decision memo

- **Week 5:**
  - Humanaios dimensional feedback summary
  - Outreach Brand Voice Training Log (3-5 message iterations)

- **Week 6:**
  - New convergence measurements (per-practice)
  - Calibration validation report (all practices)
  - Final calibration sign-off

### Grounded Evidence (by Week 6)

✅ Convergence deltas on new data (8-10 new sessions total, 2-3 per practice)  
✅ Performance metrics (routing accuracy, comprehension scores, brand coherence ratings)  
✅ Confidence correlations (self-assessment vs external validation)  
✅ Stability measurements (variance week-to-week)

---

## Implementation Notes

### For Autonomy Practice
- Minimal intervention: maintain current discount, monitor for drift
- Light touch: weekly convergence tracking only
- Success: stay at ≤0.065 delta (already doing great)

### For Humanaios Practice
- Moderate support: dimensional comprehension review
- Focused work: 1-2 areas of rubric that may need clarification
- Success: move from 0.1427 → 0.125 (safer convergence margin)

### For Outreach Practice
- Intensive support: brand voice deep-dive + hands-on training
- Structured feedback: message-by-message coaching (Week 5)
- Critical decision point (End of Week 4): may need to update discount factor from 0.85× → 0.65×
- Success: move from 0.2403 → ≤0.130 (meets target on new data)

### For Empirica-Foundation-Evaluator (Lead)
- Provide structured feedback (not corrections—coaching)
- Document findings (Voice Coherence Analysis, comprehension scores)
- Make discount factor decision for outreach (end of Week 4)
- Measure convergence on new sessions (Week 6 validation)
- Sign-off when targets met

---

## Risk Mitigation

### Risk 1: Outreach Discount Factor Insufficient
**Mitigation:** End of Week 4, if analysis shows 35–40% reduction needed (not 15%), update discount to 0.65× before Week 6 validation.

### Risk 2: Humanaios Stays at Edge of Target
**Mitigation:** Light training in Week 5 should help. If Week 6 data still shows ≤0.125 challenge, consider follow-up in later weeks (beyond Week 6 scope).

### Risk 3: Training Feedback Not Internalized
**Mitigation:** Use iterative message-by-message feedback in Week 5 (outreach). Real-time coaching shows impact faster than delayed feedback.

### Risk 4: Convergence Measurement Error
**Mitigation:** Validate all new convergence deltas against `apply_practice_discount()` and discount factor, ensure correct methodology.

---

## Sign-Off

**Calibration plan designed by:** empirica-foundation-evaluator  
**Authority:** Admiral (empirica-foundation BDFL)  
**Status:** Ready for Week 4 execution  
**Next review:** End of Week 4 (outreach discount decision point)

---

**Prepared:** 2026-07-23  
**Scope:** Phase 5 Weeks 4-6 (intensive calibration cycle)  
**Expected outcome:** 80%+ total convergence improvement (61.7% Week 1 discount + 28% Week 4-6 calibration)
