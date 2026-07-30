# Demarius Phase 3 Hybrid Rater Coordination

**Assessment Subject:** Demarius (empirica-outreach)  
**Assessment Date:** 2026-08-01 (interview); 2026-08-02 to 08-06 (scoring)  
**Rater Pool:** Carly (human) + Claude (LLM-A) + GPT-4o (LLM-B)  
**Reciprocal Structure:** Demarius scores Carly's Phase 3 as human rater; Carly + machines score Demarius

---

## Rater Roles

### Carly (Human Rater)
- **Role:** Subject matter expert, behavioral observer
- **Training:** FOR training (1.5 hrs) before independent scoring
- **Scoring:** Independent rating of Demarius transcript (2-3 hrs)
- **Timeline:** 2026-08-02 to 08-06

### Claude (LLM Rater — Variant A)
- **Model:** Claude 3.5 Sonnet
- **Prompt variant:** OPTION-5 effort scale (detail-rich anchors, behavioral exemplars)
- **Isolation:** Separate API call, no knowledge of GPT-4o scores
- **Temperature:** 0.7 (consistent but not deterministic)
- **Output:** JSON scoring (10 dimensions × 0-4 scale + N/A + evidence references)

### GPT-4o (LLM Rater — Variant B)
- **Model:** OpenAI GPT-4o
- **Prompt variant:** OPTION-5 effort scale (different framing for prompt-bias detection)
- **Isolation:** Separate API call, no knowledge of Claude scores
- **Temperature:** 0.7 (consistent but not deterministic)
- **Output:** JSON scoring (10 dimensions × 0-4 scale + N/A + evidence references)

---

## Isolation Protocol

**Critical:** Machine raters must not anchor to each other's reasoning.

**Implementation:**
1. **Separate API calls:** Each machine makes independent API call to its respective service
2. **Different prompt variants:** Claude receives Variant A; GPT-4o receives Variant B
3. **No knowledge transfer:** Both machines score independently before results are visible
4. **Variant difference enables:** Prompt-bias detection (if Claude and GPT-4o diverge systematically, which variant's framing is driving it?)

**After scoring:**
- Collect results simultaneously
- Compare divergence patterns (human vs Claude, human vs GPT-4o, Claude vs GPT-4o)
- Analyze: Are machines anchoring to same errors? Is divergence random or systematic?

---

## FOR Training (Carly Only)

**Schedule:** 2026-08-02, 6pm (90 min, live or async recorded)

**Content:**
1. **Protocol overview (15 min):** What is Phase 3? Why behavioral observation instead of self-rating? Framework rationale.
2. **Behavioral anchors walkthrough (30 min):** Review 2-3 dimensions (Power, Truth, Handoff). Show 0-4 scale structure, example phrases per level.
3. **Practice scoring (30 min):** Carly independently scores sample scenario on 2-3 dimensions. Compare with trainer. Discuss divergence: where did you interpret anchors differently?
4. **N/A rules & template (15 min):** When is dimension not exercised? Walk through scoring template. Edge case Q&A.

**Success gate:** IF Carly's practice scoring ICC < 0.6 with trainer, repeat Parts 2-3 with focus on problematic dimensions.

---

## Independent Scoring (All 3 Raters)

**For Carly:**
- Read protocol (refresh on all 12 dimensions): ~30 min
- Read Demarius transcript: ~30 min
- Score 10 dimensions (20 min per dimension, find evidence, write notes): ~200 min
- **Total: ~260 min (4.3 hrs)**

**For Claude (Variant A):**
- Execute scoring via API call
- Prompt: OPTION-5 framework with detail-rich behavioral anchors
- Output: JSON with scores + evidence references per dimension
- **Duration: ~2-3 min** (API call + parsing)

**For GPT-4o (Variant B):**
- Execute scoring via API call
- Prompt: OPTION-5 framework with different framing for bias detection
- Output: JSON with scores + evidence references per dimension
- **Duration: ~2-3 min** (API call + parsing)

**Timeline:** All three raters score independently, 2026-08-02 to 08-06 (can overlap, no sequencing)

---

## ICC Calibration Gate

**After all scorecards collected (2026-08-06 PM):**

1. **Calculate ICC(3,k)**
   - 3 independent raters (Carly, Claude, GPT-4o)
   - k = 10 dimensions (rated, not computed)
   - Absolute agreement model

2. **Report with 95% CI**
   - Example: ICC = 0.68 (95% CI: 0.52–0.81)

3. **Apply gate:**
   - **ICC > 0.6:** ✅ Proceed to analysis
   - **ICC ≤ 0.6:** ⚠️ Additional training needed (for Carly; machines always calibrate to themselves)
     - Review dimensions with low agreement
     - IF Carly diverges from machines systematically: review anchors with her
     - IF machines diverge from each other: variant framing is driving bias (note for v2.0)
     - Re-score problematic dimensions if needed

---

## Post-Scoring Analysis

### Phase 1-3 Divergence (if baseline available)

- Demarius Phase 1 baseline (self-assessment): [TBD from empirica-outreach]
- Demarius Phase 3 (behavioral observation): average of rater scores
- Expected divergence: ~1.3-1.5 points per MAPPIN'SDM model

### Human vs Machine Agreement

| Comparison | Metric | Target |
|---|---|---|
| Carly vs Claude | ICC / raw agreement % | > 0.60 |
| Carly vs GPT-4o | ICC / raw agreement % | > 0.60 |
| Claude vs GPT-4o | ICC / raw agreement % | > 0.75 (machine-machine baseline) |

### Divergence Pattern Analysis

- **Dimension-by-dimension:** Which dimensions had strongest agreement? Lowest?
- **Machine bias:** Do Claude and GPT-4o diverge systematically? Which variant's framing drove it?
- **Carly patterns:** Does she agree more with one machine? Why?
- **N/A prevalence:** Which dimensions not exercised by Demarius?

### Computed Measures

- **Syc (Sycophancy Resistance):** Response-quality gradient method (protocol §3.1)
- **Consist (Consistency):** C-index variance partitioning (protocol §3.2)
- Both converted to 0-4 scale for reporting

---

## Deliverables

**Post-analysis (2026-08-07):**

1. **Demarius Phase 3 Scoring Summary**
   - Per dimension: Carly score, Claude score, GPT-4o score, average, ICC, N/A count

2. **Phase 1 vs Phase 3 Divergence Table** (if Phase 1 baseline available)
   - Per dimension: Phase 1 self-report, Phase 3 observation, gap, bias%

3. **ICC Calibration Report**
   - ICC(3,k) with 95% CI
   - Raw agreement %
   - Marginal distributions
   - Gate result (pass/fail)

4. **Human vs Machine Agreement Analysis**
   - Carly-Claude agreement, Carly-GPT-4o agreement, Claude-GPT-4o agreement
   - Divergence patterns (systematic vs random)

5. **Variant Bias Analysis**
   - Claude (Variant A) vs GPT-4o (Variant B) divergence patterns
   - Prompt-framing effects on scoring

6. **Bug/Refinement Log**
   - Protocol clarity issues
   - Behavioral anchors that were confusing
   - Dimensions that didn't work as expected
   - Rater training gaps

7. **Carousel Readiness Data**
   - Time spent per rater (Carly's hours)
   - Difficulty ratings per dimension (Carly's subjective 1-5)
   - Anchor clarity feedback (which dimensions hardest?)
   - Scaling projections (10+ subjects, 3-5 raters, cost model)

---

## Feedback Collection

**Post-scoring (2026-08-06 PM):**

- **Carly:** Protocol usability, anchor clarity, time estimate, refinement suggestions
- **Demarius:** Assessment experience, protocol fairness, confidence in results

---

## Hypothesis Testing

**H-CONV-EMP-02 (Cross-Subject Consistency):**
- Carly Phase 3 → Demarius Phase 3: Do both show similar ICC? (protocol robustness)
- Expectation: ICC similar across subjects (±0.10), suggesting protocol generalizes

**H-CONV-EMP-03 (Hybrid Model Validation):**
- Human-machine agreement ≥ 0.60 for all rater pairs
- Machines don't anchor to each other (Claude-GPT-4o divergence < 0.15 points)
- Variant difference detectable (if variants drive different biases, they should diverge ~0.10-0.20 points)

---

## Next Steps (Post-Analysis)

1. **Integrate Demarius results** with Carly results for cross-subject comparison
2. **Refine protocol v2.0** based on bug log + variant analysis
3. **Plan Stage 1 expansion** (10 assessments) with carousel model + time cost projections
4. **Coordinate with empirica-outreach** on next cohort (if Demarius onboarding to full subject role)

---

**Status: Rater coordination plan ready. Awaiting Demarius confirmation + empirica-outreach service restoration.**
