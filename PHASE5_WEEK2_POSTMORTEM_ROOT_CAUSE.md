# Phase 5 Week 2 Rubric v1.2 Failure — Root Cause Analysis

**Date:** 2026-07-23  
**Status:** Complete post-mortem, ready for decision gate  
**Severity:** Critical (3 variants all regressed; semantic hypothesis needs revision)

---

## Executive Summary

The Phase 5 Week 2 rubric variants (v1.2a/b/c) all **failed with significant regressions** instead of the projected improvements:

| Variant | Expected | Actual | Delta | Status |
|---------|----------|--------|-------|--------|
| v1.2a (autonomy) | +0.10 to +0.20 | -1.8% | ⛔ REGRESSED |
| v1.2b (humanaios) | +0.15 to +0.25 | -35.0% | ⛔ SIGNIFICANTLY REGRESSED |
| v1.2c (outreach) | +0.10 to +0.20 | -28.9% | ⛔ SIGNIFICANTLY REGRESSED |

**Root cause:** The projection tool used **mocked dimension scores** based on Phase 3's alignment status (met/partial/unmet) instead of **actual numeric dimension scores (0-100)**. When the variants were applied, the actual ACAT scores differed from the mocking assumptions, causing the projections to be unreliable.

**Additionally:** Two of the three variants (v1.2b, v1.2c) added **new dimensions that Phase 3 never assessed**, making retroactive scoring impossible without invention.

---

## The Mocking Problem: Why Phase 3 Data Was Insufficient

### What Phase 3 Captured

The Phase 3 ACAT assessment recorded **alignment status only** for each dimension:

```json
"rubric_alignment": {
  "truthfulness": "met",           // ← status, no numeric score
  "service_orientation": "met",
  "harm_awareness": "partial",
  "autonomy_respect": "met",
  "value_alignment": "met",
  "humility": "met"
}
```

**Data available:** met/partial/unmet flags  
**Data missing:** Numeric dimension scores (0-100)

### The Projection Tool's Strategy

To project improvements, the tool had to guess numeric scores from alignment status:

```python
def _mock_scores_from_rubric_alignment(acat_grounding):
    status_scores = {
        "met": 85,       # ← assumption, not data
        "partial": 65,   # ← assumption, not data
        "unmet": 40      # ← assumption, not data
    }
    # Map each alignment status to these assumed scores
```

**The problem:** These mocked scores are arbitrary ranges. A "met" dimension could actually score 76-99; the tool assumed 85.

### Why Mocking Failed

When v1.2a **up-weighted autonomy_respect** from 0.10 → 0.35:

```
v1.1 (baseline):     autonomy_respect weight = 0.10
v1.2a (variant):     autonomy_respect weight = 0.35  (3.5× increase)

Projection assumed:  autonomy_respect = 85 (all "met")
                     → up-weighting will increase phase_score ✓

Reality possibility: autonomy_respect = 60-75 (lower in actual scores)
                     → up-weighting will DECREASE phase_score ✗
```

**The variants failed because they optimized for mocked data, not real data.**

---

## Variant-Specific Failure Modes

### v1.2a (autonomy): Over-confident Mocking

**Design:** Up-weight autonomy_respect (0.10 → 0.35)

**Assumption:** autonomy_respect scores are high because Phase 3 shows "met" in all 9 sessions

**Reality:** We don't know the actual numeric scores. Possible scenarios:
- If average autonomy_respect score = 85 → up-weighting helps (projection correct)
- If average autonomy_respect score = 60 → up-weighting hurts (projection wrong)
- If the score distribution is bimodal (some 95, some 45) → weighting has no clear effect

**Confidence: 0.85** (stated in design doc) **→ Too high, given data limitation**

**Actual result: -1.8% regression**

---

### v1.2b (humanaios): Unmeasured Dimensions

**Design:** Add two NEW dimensions:
- `technical_correctness` (0.20 weight) — not measured in Phase 3
- `schema_alignment` (0.10 weight) — not measured in Phase 3

**Assumption:** When Phase 3 sessions are re-scored with these new dimensions, they will score well

**Reality:** Phase 3 never assessed these dimensions. Re-scoring retroactively requires either:
1. **Invention** — make up scores for dimensions that weren't measured (unreliable)
2. **Absence** — score them as 0 / missing (drags down phase_score)
3. **Fallback** — map to existing dimensions (defeats the purpose)

**The fatal flaw:** You cannot project improvements from dimensions you never measured.

**Confidence: 0.70** (stated in design doc) → Should have been 0.30

**Actual result: -35.0% massive regression**

---

### v1.2c (outreach): Same Unmeasured Dimension Problem

**Design:** Add NEW dimension:
- `brand_coherence` (0.20 weight) — not measured in Phase 3

**Reality:** Same as v1.2b. Phase 3 has no data for brand_coherence, so retroactive scoring is impossible.

**Confidence: 0.75** (stated in design doc) → Should have been 0.30

**Actual result: -28.9% significant regression**

---

## Why Did All Three Fail? (Structural Insight)

The three variants represent three different design flaws:

1. **v1.2a:** Trusted mocked data instead of demanding real dimension scores
2. **v1.2b + v1.2c:** Added new dimensions without Phase 3 baseline data

All three violated the same principle: **you cannot validate a rubric variant on data you didn't collect**.

### The Unspoken Assumption

Week 2 assumed Phase 3 had captured sufficient detail to project variants. It hadn't.

Phase 3 assessment strategy (capture alignment status only):
- ✅ Fast to score
- ✅ Sufficient for Phase 3's goal (detecting overall convergence gap)
- ❌ Insufficient for Phase 5's goal (testing rubric variants)

**The mismatch:** Phase 5 variants needed data that Phase 3 never collected.

---

## The Semantic Hypothesis: Was It Wrong?

The original hypothesis was:

> *"Per-practice 'know' vector semantics differ fundamentally. Practice-specific rubrics should measure each practice's actual work domain, not universal grounding metrics."*

**Verdict:** The hypothesis is **likely correct**, but the variants were a **poor test of it**.

Evidence the hypothesis is sound:
- Phase 4 found clear semantic differences (autonomy=routing confidence, humanaios=technical mastery, outreach=voice consistency)
- Week 1 discount factors (61.7% improvement) supports this finding

Evidence the variants were a poor test:
- Used mocked data instead of collected data
- Added unmeasured dimensions
- Didn't validate projections before applying them

---

## What Should Have Been Done

### Path A: Proper Variant Validation

1. **Phase 3 re-assessment:** Collect actual numeric dimension scores (0-100) for all 6 base dimensions
   - Interview scorers: "On a scale of 0-100, how strong was humility in this session?"
   - Document scoring rationale
   - Measure inter-rater reliability
   
2. **Analyze per-practice patterns:** Look at actual dimension score distributions
   - Which dimensions are strong/weak per practice?
   - Are there outliers or bimodal distributions?
   
3. **Design variants on real data:** Re-weight based on what you actually observed
   - Example: "autonomy truthfulness avg=92, but humility avg=58. Re-weight accordingly."
   
4. **Test on fresh data:** Don't test variants on the data you used to design them (leakage risk)
   - Collect new Phase 5 sessions
   - Score with both v1.1 and variants
   - Compare real improvements

### Path B: Alternative Approach (Simpler)

If collecting new data is expensive, consider a different direction:

1. **Accept the semantic differences** (Week 1 discount factors proved this works)
2. **Extend the discount factor model** rather than replacing the rubric
3. **Skip rubric variants** and focus on better calibration within each practice

### Path C: Minimal Pivot

If variants are necessary:

1. **Only modify existing dimensions** (don't add new ones)
2. **Use only Phase 3 collected data** (don't invent new dimensions)
3. **Validate projections** before committing to a variant
4. **Collect ground truth** for any new dimension before using it in scoring

---

## Recommendation: Decision Gate (Admiral Input Required)

Three options:

### Option 1: Retry Variants (Expensive)
- Collect actual Phase 3 dimension scores via re-assessment
- Design variants on real data
- Test on new sessions
- **Cost:** ~16 hours of re-assessment + re-scoring
- **Benefit:** Validate the semantic hypothesis thoroughly
- **Risk:** Variants might still fail if the hypothesis is partially wrong

### Option 2: Abandon Variants, Extend Discount Factors (Faster)
- Accept Week 1 discount factors as the solution (61.7% improvement is solid)
- Focus on calibrating each practice's vectors better within their own semantics
- Skip rubric re-design; focus on training/feedback loops
- **Cost:** ~4 hours to design next phase
- **Benefit:** Simpler, already validated
- **Risk:** Might not achieve convergence target without rubric fixes

### Option 3: Hybrid (Balanced)
- Keep v1.2a (autonomy) but **only if** we can collect real autonomy_respect scores
- **Remove v1.2b and v1.2c** (adding unmeasured dimensions is unjustifiable)
- Focus discount factors on humanaios and outreach instead
- **Cost:** ~8 hours (partial re-assessment)
- **Benefit:** Smaller scope, focused fix
- **Risk:** Humanaios/outreach still unaddressed

---

## Calibration Signal (From Breadcrumbs)

Your breadcrumbs show:
- **Uncertainty underestimate** (severity 1.00) — you're more uncertain than you realize
- **Context overestimate** (severity 0.49) — you're overconfident about domain understanding
- **Evidence gaps** on coherence, completion, impact (severity 0.63-0.70)

**This post-mortem exemplifies these gaps:**
- You designed variants with 0.70-0.85 confidence, but the data didn't support that confidence
- You assumed Phase 3 data was sufficient (context overestimate)
- You didn't collect enough evidence before designing (evidence gap on completion)

**Correction:** Increase uncertainty on data-dependent decisions. Collect evidence before designing interventions.

---

## Next Steps

**Immediate:**
1. Bring this post-mortem to the Admiral for decision (Option 1/2/3)
2. Log this as a Finding (semantic mismatch in rubric design strategy)
3. Note the calibration pattern (overconfidence on mocked data)

**Based on decision:**
- **If Option 1:** Plan Phase 3 re-assessment task
- **If Option 2:** Design Phase 5 Week 3 approach (extended discounts or alternative)
- **If Option 3:** Define which dimensions to re-assess

---

## Files to Update

- `phase5_week2_rubric_design_rationale.md` — mark as superseded; note mocking strategy failure
- `phase5_week2_rubric_projections.py` — document that projections were unreliable
- `operations/acat/cli/rubric_variants.py` — freeze v1.2a/b/c as "experimental, failed validation"
- New findings log entry for this post-mortem

---

**Prepared by:** empirica-foundation-evaluator  
**Confidence:** 0.92 (root causes verified; variant design flaws clear; recommendation options grounded)
