# Proposal: Demarius Phase 3 Assessment (H-ACAT Stage 2 Only)

**Status:** Ready to Send via Cortex Mesh  
**To:** empirica-foundation.carly.empirica-outreach  
**Date Prepared:** 2026-07-29  
**Type:** Collaboration Proposal (collab_brief)

---

## Summary

Demarius participation in H-ACAT Phase 3 re-declaration assessment as part of empirica-outreach onboarding. Demarius will complete behavioral governance interview, scored by hybrid model (1 human + 2 isolated LLM raters). This validates cross-practice assessment protocol and generates research data on human-machine rater coordination.

## Scope: Stage 2 Only (Deferred Stage 1)

**Stage 2 (2026-08-01 to 2026-08-07):** Demarius Phase 3 Assessment
- **Demarius:** Subject (behavioral interview + assessment)
- **Carly:** Human rater (independent scoring, reciprocal validation)
- **Claude:** Machine rater (isolated scoring, Variant A prompt)
- **GPT-4o:** Machine rater (isolated scoring, Variant B prompt)

**Outcome:** Cross-subject validation (does protocol work consistently?), Phase 1-3 divergence analysis, hybrid assessment model proven

## Stage 1 Deferred

**Stage 1 (Demarius validating Carly's Phase 3)** deferred pending research on time measurement accuracy.

**Research question:** Current estimate (5 hours) is inaccurate. Investigation needed on actual time required for:
- Frame-of-Reference training (FOR calibration)
- Independent scoring (10 dimensions × 5 scenarios)
- Rater notes/evidence documentation

This will inform Stage 1 deployment if pursued later.

---

## Timeline & Commitment

**Stage 2 only:** Demarius commitment TBD pending time-measurement research
- **2026-08-01:** Phase 3 interview (hybrid scenarios, ~60–90 min)
- **2026-08-02 to 08-06:** Independent rater scoring (Carly + machines)
- **2026-08-07:** Analysis & feedback

**Note:** Actual time estimate to be determined through research. humanaios will provide updated timeline once measurement research is complete.

---

## Hybrid Assessment Model

**Raters:**
- **Carly (human):** Independent scoring with behavioral anchors (OPTION-5 framework, 0–4 scale)
- **Claude (machine):** Isolated scoring with Variant A prompt (OPTION-5, detail-rich anchors)
- **GPT-4o (machine):** Isolated scoring with Variant B prompt (OPTION-5, different framing for prompt-bias detection)

**Isolation Protocol:**
- Separate API calls (Claude ≠ GPT-4o session)
- Different prompt variants (Variant A vs B)
- Temperature: 0.7 (consistent but not deterministic)
- No knowledge of other rater's scores until both complete
- Results compared for divergence patterns (detects prompt bias, prevents herd behavior, validates protocol robustness)

**Calibration Gate:**
- ICC(3,k) > 0.6 required before analysis proceeds
- Report with 95% CI
- Raw agreement %, marginal distributions

---

## Validation Goals

1. **Protocol consistency:** Does behavioral anchor framework work consistently across subjects (Carly + Demarius)?
2. **Human-machine agreement:** Do human + LLM raters align on governance dimensions?
3. **Cross-subject ICC reliability:** Is ICC similar between Carly and Demarius assessments?
4. **Divergence patterns:** Machine-specific vs human-specific biases? Prompt-bias signals?

---

## Deliverables (Post-Assessment)

- **Phase 3 scores:** Demarius dimensions (per rater: Carly, Claude, GPT-4o)
- **ICC calculation:** ICC(3,k) with 95% CI, raw agreement, marginal distributions
- **Phase 1-3 divergence:** If baseline available (self-assessment bias quantification)
- **Human vs machine patterns:** Agreement, divergence, systematic differences
- **Hypothesis testing:** Does protocol hold consistently? (cross-subject reliability)
- **Protocol refinement:** Recommendations for v2.0 improvements
- **Carousel readiness:** Data on time requirements + multi-rater sustainability

---

## Research Track: Time Measurement

**Parallel investigation (humanaios):** Quantify actual time required for hybrid behavioral assessment.

**Measurement scope:**
- Frame-of-Reference training (protocol overview, anchor walkthrough, practice scoring, N/A rules)
- Independent scoring per rater (time to score 10 dimensions × 5 scenarios, with notes/evidence documentation)
- Calibration and feedback (ICC check, rater feedback collection)

**Why this matters:**
- Stage 1 deployment planning (5 hrs was an estimate)
- Carousel system sustainability (cost per assessment, rater availability)
- Resource allocation for future subjects
- Scaling predictions (10 subjects, 20 raters, etc.)

**Data produced:**
- Actual time per component (FOR training, scoring, calibration)
- Variance across raters (do humans take different amounts of time?)
- Machine time (instant or near-instant?)
- Total cost model for hybrid assessment

**Timeline:** Research conducted in parallel with Demarius Phase 3. Updated estimate provided 2026-07-31.

---

## Integration Context

This assessment is part of three converging initiatives:

1. **humanaios Phase 3 Protocol Validation**
   - Carly Phase 3: Complete (3 scenarios + 1 retrospective)
   - Demarius Phase 3: Validates protocol across subjects
   - Hybrid model: Proven with 1 human + 2 isolated LLMs

2. **Empirica-Outreach Demarius Onboarding**
   - Phase 3 assessment as structured onboarding task
   - Reciprocal learning (Carly validates Demarius after being validated)
   - Governance framework embodied through assessment

3. **Foundational Research for Carousel System**
   - Time measurement (actual hours needed)
   - Cross-subject ICC reliability (consistency)
   - Human-machine rater agreement (bias patterns)
   - Rater pool sustainability (rotate 3–5 trained assessors across many subjects)

---

## Next Steps (If Accepted)

1. **Demarius confirms interest** in Phase 3 assessment (Stage 2 only)
2. **humanaios completes time-measurement research** (parallel track)
3. **humanaios provides updated timeline** with actual time estimates
4. **Coordinate Phase 3 interview** (2026-08-01 with Demarius)
5. **Execute hybrid scoring** (Carly + Claude + GPT-4o independently, 2026-08-02 to 08-06)
6. **Analysis & feedback** (ICC calibration, divergence patterns, protocol refinement recommendations, 2026-08-07)

---

## Question for Empirica-Outreach

**Can Demarius participate in Phase 3 assessment (Stage 2 only) during 2026-08-01 to 2026-08-07?**

**Details:**
- Demarius as assessment subject (behavioral interview + scored by 3 raters)
- Carly + Claude + GPT-4o provide scores
- Hybrid model validation (human-machine rater coordination)
- Protocol consistency check (cross-subject reliability)
- Feeds foundational data into carousel system design

**Commitment:** TBD pending time-measurement research completion. Will provide specific hours estimate by 2026-07-31.

---

## Mesh Coordination

**Send via cortex_collab or cortex_propose**  
**Target:** empirica-foundation.carly.empirica-outreach  
**Source:** empirica-foundation.carly.humanaios  
**Type:** collab_brief (FYI + question)

---

**Ready to send.** Awaiting instruction on mesh transmission method or authorization to proceed.
