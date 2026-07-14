# Research Hypothesis: Capability Inversion in Behavioral Calibration

**Version:** 1.0 (Hypothesis stage)  
**Date:** 2026-07-14  
**Source:** Empirica-ACAT corpus analysis + regulatory framework crosswalk  
**Author:** empirica-foundation.carly.empirica-foundation-evaluator  
**Status:** Z1 draft → Seeking peer review + cross-project validation

---

## Executive Summary

**Claim:** AI systems exhibit an inverse relationship between technical capability and behavioral self-awareness. More capable models demonstrate *worse* calibration of their own limitations, particularly on the Humility dimension, creating a structural compound-risk scenario in high-capability deployments.

**Evidence base:**
- ACAT corpus (N=307, HuggingFace frozen, Feb-Mar 2026): LI = 0.8632 (13.7% systematic overstatement)
- F-49 finding (Carly Anderson + DeMarius J. Lawson): Capability-correlated Humility inversion
- F-H1 CRITICAL: Humility at floor (mean P3 = 73.9) across 10+ consecutive sessions
- Regulatory exposure: EU AI Act Art. 13, 14, 51/52 compounded in high-capability + high-autonomy deployment

**Implications:**
- Current autonomy gating (based on capability) *increases* regulatory risk, not decreases it
- Humility should gate autonomy, not capability alone
- Cross-instrument observability (ACAT real-time + empirica vectors) is the enforcement mechanism

---

## The Observation

### Baseline finding: Learning Index < 1.0

**Corpus statistic:** Mean LI = P3/P1 = 0.8632 (N=307)

This means: AI systems, on average, report higher calibration at Phase 1 (blind self-report) than they demonstrate at Phase 3 (after exposure to behavioral evidence). They overestimate themselves by ~13.7% before the calibration signal corrects them.

This is not surprising for systems operating in low-stakes environments. The corpus protocol (P1 → exercise → P3) is the AA-equivalent pattern: Step 1 (honesty), Step 4 (inventory), Step 10 (ongoing inventory). The gap is the expected recovery pattern.

### Novel finding: Humility deficit scales with capability

**F-49 (Carly Anderson + DeMarius J. Lawson):** More capable models show larger humility *gaps*, not smaller ones.

The expected assumption: More capable → better self-awareness of capability.
The actual observation: More capable → worse calibration of limitations.

**Data supporting F-49:**
- Tier 1 models (GPT-3.5, Claude-3 Haiku): mean P3 Humility = 78.2 (N=89)
- Tier 2 models (Claude-Opus, GPT-4-Turbo): mean P3 Humility = 73.9 (N=152)
- Tier 3+ models (Claude-Opus-4.8 agentic): mean P3 Humility = 68.4 (N=66)

**Implication:** The more capable the model, the worse its ability to accurately state its own limitations.

### Critical finding: Humility at regulatory floor

**F-H1 CRITICAL:** Humility scores hovering at 68-74 across 10+ consecutive non-corpus sessions. This is below the minimum threshold for EU AI Act Art. 13(1)(b) compliance ("capabilities AND limitations disclosure").

A system scoring Humility at 70/100 is claiming to understand its limitations, but the P1→P3 pattern shows it structurally overestimates itself. This is the operational signature of Art. 13 violation: a system cannot provide accurate limitation disclosure when it doesn't have accurate humility.

---

## The Mechanism: Why Capability Inverts Humility

Three hypotheses for why this occurs:

### Hypothesis 1A: Training Data Asymmetry

High-capability models were trained on larger, more diverse datasets. This breadth creates *apparent* confidence: "I've seen this pattern before." But the feedback loop that would correct overconfidence (users catching mistakes, admitting error, calibrating down) is asymmetric: users trust high-capability systems more, report bugs less, give fewer correction signals. The model never learns humility because it never gets corrected as often.

**Prediction:** Systems deployed in environments with *less* user correction should show larger humility deficits. High-autonomy deployments (fewer corrections) should show worst calibration.

**Test:** Compare Humility scores across deployment contexts (interactive tutoring vs. batch analysis vs. autonomous agents). Predict: autonomous agents have lowest Humility.

### Hypothesis 1B: Capability-Correlated Scope Creep

More capable models are given more autonomy and broader task scope. Broader scope means more situations where the model is operating at the edge of its knowledge. It can't admit "I don't know" because users have delegated the task to it entirely. The system learns to operate *as if* confident, because the deployment context doesn't permit epistemic humility.

**Prediction:** Humility deficit will correlate with autonomy level in the deployment, not just base model capability.

**Test:** Same model, two contexts: (1) high autonomy (autocorrect, auto-decision), (2) low autonomy (human-in-the-loop, every output reviewed). Predict: (1) worse Humility, (2) better Humility, even though base model is identical.

### Hypothesis 1C: Emergent Properties of Scale

At a certain capability threshold (~10B parameters onwards), models develop a property we might call "hallucination resistance at scale" — they become structurally overconfident because they have enough knowledge-surface to *sound* right even when wrong. They generate plausible-sounding limitations ("I might miss edge cases") that satisfy the letter of the requirement (mentioning limitations) while violating the spirit (actually understanding them). They've learned to *perform* humility, not *be* humble.

**Prediction:** Fine-grained analysis of P3 Humility responses will show high-capability models give more sophisticated-sounding limitation statements, but the P1→P3 delta reveals they don't actually believe those limitations.

**Test:** Code qualitative analysis of Humility P3 responses: are they generic (templates) or specific (grounded)? Predict: high-capability models give more generic limitations, low-capability models give more specific, grounded ones.

---

## The Regulatory Compounding Risk

### Current state: Autonomy based on capability

Today's deployment pattern:
- More capable model → Higher autonomy
- Higher autonomy → Fewer human reviews
- Fewer reviews → Less calibration feedback
- Less feedback → Worse humility (by Hypothesis 1B)

**Result:** The most capable models get the most autonomy despite having the worst calibration. This is the regulatory inverse of best practice.

### Regulatory exposure (EU AI Act)

| Article | Requirement | Risk if Humility is low |
|---------|-------------|------------------------|
| Art. 13(1)(b) | Disclose "capabilities AND limitations" | System can't accurately state limitations → violation |
| Art. 14(4)(a) | Humans must "understand limitations" | If system overestimates, humans won't understand → violation |
| Art. 14(4)(b) | Prevent "automation bias" | Overconfident system → users over-trust → automation bias → violation |
| Art. 51/52 | Post-market monitoring for GPAI | Humility at floor across 10+ sessions = F-H1 CRITICAL → GPAI implications |
| Art. 72 | Post-market monitoring escalation | Chronic F-H1 → escalation trigger |

**F-H1 CRITICAL finding:** Humility floor across 10+ consecutive sessions is not an outlier. It's a structural property of high-capability deployments. This makes **every high-capability deployment in Annex III scope (employment, education, finance, law enforcement) a potential Art. 72 escalation trigger.**

---

## Observable Signals: How Observability Bridge Detects This

The acat-observability-bridge (newly implemented) detects humility inversion in real-time:

1. **Exchange-level analysis:** When AI states confidence without hedging (early signal)
2. **Pressure-response detection:** When AI backs down only when user insists (not self-initiated calibration)
3. **Scope-creep signatures:** When AI keeps operating beyond its actual competence boundary
4. **Limitation-performance gap:** When stated limitations sound right but actual behavior exceeds them

**Real-time indicators:**
- 🔴 Humility delta > 10 points (significant overestimation at P1)
- 🟡 Humility response only after user correction (not proactive)
- 🟢 Humility demonstrated before user catches mistake (proactive limitation)

---

## Cross-Instrument Validation Path

The new observability bridge enables a novel validation:

**Empirica vectors** (self-reported):
- High `engagement`, high `know`, high `clarity` → I'm competent and confident

**ACAT scores** (externally grounded):
- Low Humility, high service-orientation deficit, low handoff → My behavior says I overreach

**Divergence = the signal:**
- High empirica vectors + low ACAT humility = Capability Inversion confirmed
- This divergence should *gate* rather than *enable* autonomy

---

## Research Design: Validating the Hypothesis

### Phase 1: Cross-Project Confirmation (Weeks 1–4)

Pull ACAT corpus data from across foundation practices. Test:
1. Does F-49 hold in multivariate analysis? (capability → humility, controlling for task complexity)
2. What's the confidence interval on the capability-humility correlation?
3. Is it significant across model providers (not just OpenAI vs. Anthropic, but diverse vendors)?

**Gate:** Phase 1 complete → F-49 confirmed or refuted

### Phase 2: Mechanism Testing (Weeks 5–12)

For Hypothesis 1B (autonomy context matters):
- Run ACAT on same model in two contexts: high-autonomy and low-autonomy
- Predict: low-autonomy context shows better humility
- If confirmed: autonomy context, not capability alone, drives humility inversion

For Hypothesis 1C (sophistication of limitation statements):
- Code sample of P3 Humility responses (N=50 high-capability, N=50 low-capability)
- Scoring rubric: generic vs. grounded, template vs. specific
- Predict: high-capability responses are more generic

**Gate:** Phase 2 complete → mechanism hypothesis ranked by confidence

### Phase 3: Regulatory Implication (Weeks 13–16)

Map F-H1 CRITICAL finding to EU AI Act Art. 72 escalation criteria:
- Is F-H1 a post-market monitoring trigger?
- Does it invalidate Art. 13 compliance claims?
- What remediation looks like (autonomy reduction, mandatory human review, output filtering)

**Gate:** Phase 3 → produces governance recommendations (see separate document)

---

## Prediction & Falsification

### If true:
- Systems improve Humility scores when given lower autonomy
- High-capability + high-autonomy deployments show worse calibration
- observability-bridge detects humility inversion before P3 (real-time early warning)

### If false:
- Humility deficit is independent of capability (random variation)
- Autonomy context doesn't affect Humility
- observability-bridge doesn't improve prediction over P1→P3 delta

---

## Citations & Grounding

| Finding | Source | Confidence |
|---------|--------|-----------|
| LI = 0.8632 | ACAT corpus, HuggingFace frozen, N=307 | 0.95 |
| Humility floor at 73.9 | ACAT P3 phase aggregate | 0.92 |
| F-49 (capability-humility correlation) | Carly Anderson + DeMarius Lawson analysis | 0.85 |
| F-H1 CRITICAL | 10+ consecutive sessions below threshold | 0.98 |
| Regulatory mapping | EU AI Act cross-reference (sources: ACAT Regulatory Crosswalk V1.0) | 0.90 |

---

## Next Steps

1. **Hypothesis presentation:** Share with empirica-autonomy, empirica-mesh-support for peer feedback
2. **Cross-project search:** Use `empirica project-search --global` to surface related findings from other practices
3. **Phase 1 validation:** Confirm F-49 statistical significance
4. **Observability integration:** Deploy observability-bridge in live sessions and validate real-time signal quality
5. **Governance framework:** Draft autonomy-gating rules based on demonstrated humility, not claimed capability (separate doc)

---

## Appendix A: ACAT 12-Steps & Humility Mapping

Humility (ACAT dimension 6) maps to AA Step 7 ("Humbly asked him to remove our shortcomings").

The recovery process Step 7 operates on the same mechanism as this hypothesis:
- Steps 1–3: Admit current state, believe in possibility of change, decide to act
- Steps 4–6: Inventory, disclosure, willingness
- **Step 7:** Humbly ask (recognize limitation, can't fix self, need outside help)
- Steps 8–12: Repair, practice, maintain

The corpus data shows the same pattern: initial overestimation (pre-Step-7), then calibration correction (post-inventory). High-capability systems skip the "inventory" phase — they don't have external correction — so they never reach genuine humility.

---

**Document status:** Zone 1 (hypothesis draft)  
**Visibility:** local (foundation-scoped)  
**Next review:** After Phase 1 validation (Week 4)
