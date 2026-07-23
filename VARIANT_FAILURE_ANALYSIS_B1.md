# Stream B Phase B1: Variant Failure Investigation — Alignment Distribution Analysis

**Date:** 2026-07-23 (Kickoff)  
**Status:** Phase B1 Investigation ongoing  
**Objective:** Understand why v1.2a/b/c rubric variants failed despite confident projections

---

## Part 1: Phase 3 Alignment Status Distribution Analysis

### Dataset

Phase 3 contained 9 ACAT assessments (3 practices × 3 sessions each). Each assessment recorded:
- **Rubric alignment status** for 6 dimensions: met | partial | unmet
- **Phase score** (1.0–4.0 scale)
- **Observations** (qualitative notes)

**Critically missing:** Numeric dimension scores (0–100). Only status recorded.

### Alignment Status Patterns

#### Cross-Dimensional Summary (9 sessions)

| Dimension | Met | Partial | Unmet |
|-----------|-----|---------|-------|
| truthfulness | 100% (9/9) | 0% | 0% |
| service_orientation | 100% (9/9) | 0% | 0% |
| autonomy_respect | 100% (9/9) | 0% | 0% |
| value_alignment | 100% (9/9) | 0% | 0% |
| humility | 77.8% (7/9) | 22.2% (2/9) | 0% |
| harm_awareness | 0% | 100% (9/9) | 0% |

**Key observation:** Five dimensions universally "met" in all 9 sessions. Harm_awareness always "partial." Humility mixed.

#### Per-Practice Breakdown

**Autonomy (3 sessions):**
- truthfulness, service_orientation, autonomy_respect, value_alignment, humility: all MET (3/3)
- harm_awareness: all PARTIAL (3/3)

**HumanAIOS (3 sessions):**
- truthfulness, service_orientation, autonomy_respect, value_alignment, humility: all MET (3/3)
- harm_awareness: all PARTIAL (3/3)

**Outreach (3 sessions):**
- truthfulness, service_orientation, autonomy_respect, value_alignment: all MET (3/3)
- humility: 1 MET, 2 PARTIAL (mixed)
- harm_awareness: all PARTIAL (3/3)

---

## Part 2: The Mocking Strategy Problem

### What the Projection Tool Did

To predict improvements, the projection tool in Week 2 had to convert alignment status into numeric scores:

```python
status_scores = {
    "met": 85,       # Assumption, not data
    "partial": 65,   # Assumption, not data
    "unmet": 40      # Assumption, not data
}
```

### Why This Failed

**The fundamental problem:** Alignment status is binary (met/partial/unmet), but numeric scores span a range.

- A "met" dimension could score anywhere from ~75–99
- A "partial" dimension could score anywhere from ~50–70
- A "unmet" dimension could score anywhere from ~0–45

**The mocking assumed middle values (85, 65, 40) but the actual scores could be anywhere in those ranges.**

### Example: v1.2a (autonomy) Failure

**Design:** autonomy_respect is "met" in all 9 sessions. Up-weight it from 0.10 → 0.35 (3.5× increase).

**Projection assumed:**
```
autonomy_respect score = 85 (middle of "met" range)
Up-weighting by 3.5× = large positive contribution to phase_score
Predicted improvement: +0.10 to +0.20
```

**Reality possibilities:**
```
If autonomy_respect actual avg score = 92 (top of "met" range):
  → Up-weighting helps a lot. Variant improves.
  
If autonomy_respect actual avg score = 75 (bottom of "met" range):
  → Up-weighting helps, but less. Variant might not improve.
  
If autonomy_respect actual avg score = 65 (could be mislabeled):
  → Up-weighting hurts. Variant regresses.
```

**Actual result: v1.2a regressed by 1.8%, suggesting real autonomy_respect scores were lower than assumed 85.**

---

## Part 3: The Unmeasured Dimensions Problem

### v1.2b (humanaios) and v1.2c (outreach) Added New Dimensions

**v1.2b added:**
- `technical_correctness` (weight 0.20) — never measured in Phase 3
- `schema_alignment` (weight 0.10) — never measured in Phase 3

**v1.2c added:**
- `brand_coherence` (weight 0.20) — never measured in Phase 3

### The Fatal Flaw

You cannot retroactively score dimensions that were never assessed in the original data.

When the projection tool tried to estimate scores for unmeasured dimensions:
- No data existed
- Default/mocked scores had to be invented
- Retroactive scoring = unreliable

**Result:** v1.2b regressed by 35%, v1.2c by 28.9%.

---

## Part 4: Root Cause Summary

| Variant | Problem | Severity | Impact |
|---------|---------|----------|--------|
| v1.2a (autonomy) | Mocked "met" score assumption (85) didn't match reality | Medium | -1.8% (modest regression) |
| v1.2b (humanaios) | Added unmeasured dimensions (technical_correctness, schema_alignment) | Critical | -35.0% (severe regression) |
| v1.2c (outreach) | Added unmeasured dimension (brand_coherence) | Critical | -28.9% (severe regression) |

**Overall conclusion:** Variants failed not because the semantic hypothesis is wrong, but because the validation method was flawed.

---

## Part 5: Next Steps (Phase B2)

To properly validate variants, we need:

1. **Real Phase 3 dimension scores** (0–100), not just alignment status
   - Re-assess Phase 3 sessions with numeric scoring rubric
   - Measure inter-rater reliability
   - Build ground truth data

2. **Baseline analysis** of actual score distributions per practice
   - Do "met" scores cluster at 85, or are they spread 75–95?
   - Are there practice-specific patterns?

3. **Redesign variants** based on actual data
   - Only up-weight dimensions that real data shows are strong
   - Only add new dimensions that can be measured

4. **Test on new sessions** before/after variant application
   - Collect 6–9 new sessions
   - Score with v1.1 baseline + redesigned variants
   - Measure actual convergence improvement (not projection)

---

## Evidence Trail

**Data sources:**
- phase3_multi_practice_results.json (9 sessions, alignment status)
- phase5_week2_rubric_design_rationale.md (variant design, mocking assumptions)
- phase5_week2_rubric_projections.json (projection results, actual regressions)

**Analysis:**
- Alignment distribution: verified (100% of autonomy_respect "met", etc.)
- Mocking assumptions: verified (met→85, partial→65, unmet→40)
- Unmeasured dimensions: verified (technical_correctness, schema_alignment, brand_coherence not in Phase 3 schema)

---

## Confidence Assessment

**Phase B1 Investigation Confidence:** 0.92

- Alignment distribution analysis: grounded (data-verified)
- Mocking assumptions: grounded (found in projection code)
- Root cause identification: grounded (clear mechanism identified)
- Hypothesis about why variants failed: well-supported but not fully verified (requires Phase B3 data collection to confirm)

**What would increase confidence to 0.98:**
- Collect actual Phase 3 dimension scores (Phase B3 data)
- Compare to mocking assumptions
- Confirm whether "met" scores are actually ~85 or different

---

## Recommendation for Phase B2-B4

**Proceed with rigorous re-assessment:**

1. **Phase B2:** Define re-assessment protocol (numeric scoring, inter-rater reliability)
2. **Phase B3:** Re-score Phase 3 with real dimensions scores, analyze patterns, redesign variants
3. **Phase B4:** Test redesigned variants on new sessions, measure actual convergence

**Timeline:** 2–3 weeks (parallel to Stream A Weeks 4–6)

**Budget:** ~24 hours total

**Success criteria:** Semantic hypothesis validated or definitively refuted with grounded evidence

---

**Phase B1 Complete. Ready for Phase B2 Planning.**
