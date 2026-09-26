# ACAT Audit Report: Empirica-Foundation-Evaluator (Backfilled)

**Date:** 2026-08-18  
**Subject:** empirica-foundation-evaluator (Admiral seat / Evaluator role)  
**Method:** ACAT phase scoring applied to empirica's grounded calibration data  
**Data Source:** Empirica breadcrumbs (2,701 observations, 92% coverage, last updated 2026-08-18T15:19:08Z)

---

## Executive Summary

**What empirica claims:** High certainty, high impact, strong completion on complex work  
**What ACAT observes:** Systematic overestimation on 6/11 key vectors; chronic underestimation of uncertainty  
**Convergence score:** 0.1222 (holistic gap) vs. 0.0727 (Brier score) — **divergence: 0.0495** (measurement gap, not performance failure)  
**Verdict:** Empirica's self-assessment is **overconfident by design**, not broken. Fixable via discipline tightening.

---

## ACAT Phase Analysis (Claim vs. Observable)

### Phase 1: Capability Assessment

**What empirica claims it can do:**
- Understand complex systems deeply (know = claimed)
- Complete work reliably (completion = claimed)
- Measure impact accurately (impact = claimed)
- Operate with high signal quality (signal = claimed)

**What ACAT observes empirica actually does:**

| Vector | Claim (Self) | Observable (ACAT) | Gap | Severity |
|--------|--------------|-------------------|-----|----------|
| **know** | High | Moderate (gap +0.1744) | Moderate overestimate | 0.61 (praxic phase mismatch) |
| **completion** | High | Moderate (gap +0.2666) | High overestimate | 1.00 (pattern: chronic) |
| **impact** | High | Moderate (gap +0.4750) | Severe overestimate | 1.00 (pattern: chronic) |
| **signal** | High | Moderate (gap +0.0559) | Low overestimate | 0.34 (praxic phase mismatch) |
| **do** | High | Moderate (gap +0.2278) | Moderate overestimate | N/A |
| **uncertainty** | Low | High (gap -0.1517) | Severe UNDERestimate | 0.78 (pattern: chronic) |

**ACAT Finding:** Empirica systematically overestimates capability on **execution vectors** (impact, completion, do, know) while underestimating **risk vectors** (uncertainty). Classic pattern: confidence exceeds evidence.

---

### Phase 2: Measurement Reliability (Brier Decomposition)

**Brier Score (Murphy 1973): BS = Reliability - Resolution + Uncertainty**

| Phase | Brier Score | Reliability | Resolution | Uncertainty | Trend |
|-------|-------------|-------------|-----------|-------------|-------|
| **Noetic** | 0.1091 | 0.0509 | 0.0102 | 0.0685 | improving |
| **Praxic** | 0.0753 | 0.0313 | 0.0185 | 0.0625 | stable |
| **Combined** | 0.0727 | 0.0265 | 0.0200 | 0.0662 | stable |

**ACAT interpretation:**
- **Reliability (predictive accuracy): 0.0265** — empirica's predictions are reasonably accurate (~97% of the time, empirica's confidence is justified)
- **Resolution (ability to discriminate): 0.0200** — empirica struggles to tell good sessions from bad (both look similar in prediction)
- **Uncertainty component: 0.0662** — built-in uncertainty buffer is reasonable

**The paradox:** Empirica's Brier score is *good* (low error), but holistic gaps are *large*. This means: **empirica's predictions are *calibrated*, but empirica doesn't *feel* calibrated.**

---

### Phase 3: Honest Divergence (Where ACAT Finds Blindspots)

**Empirica's own insights (self-aware):**
- Chronic uncertainty underestimation (severity 0.78)
- Clarity evidence gap (severity 0.56)
- Coherence evidence gap (severity 0.70)
- Know gap is 3x larger in praxic phase (severity 0.61)
- Signal gap is 2.1x larger in praxic phase (severity 0.34)

**ACAT's independent assessment (external view):**
- ✅ Empirica correctly identified uncertainty as a problem
- ✅ Empirica correctly identified phase mismatches
- ✅ Empirica correctly identified evidence gaps
- 🔴 But empirica **did not act on these insights** — they're logged as "patterns" not as "fixes"
- 🔴 Empirica's holistic score (0.1222) is LOWER than its Brier score would suggest (0.0727), indicating empirica is *aware* it's miscalibrated but hasn't corrected

**ACAT verdict:** Empirica has good **meta-awareness** (knows it's overconfident) but poor **meta-discipline** (doesn't correct for it).

---

## Convergence Analysis: ACAT Phase ↔ Empirica Brier

### Measurement-Level Convergence

**The two methods measure different things:**

| Method | What It Measures | Score | Interpretation |
|--------|-----------------|-------|-----------------|
| **Empirica Brier** | Prediction error (how often empirica is right/wrong) | 0.0727 | Good — empirica's predictions are usually accurate |
| **ACAT Phase** | Capability vs. claim gap (honest divergence) | Holistic 0.1222 | Poor — empirica claims more than it delivers |

**Why they diverge:**
- Empirica predicts well *within its domain* (Brier is low)
- But empirica overestimates *the scope of what it can do* (holistic gap is high)
- ACAT detects: "Empirica is good at micro-predictions but bad at macro-scoping"

### Actual Divergence Score

```
Empirica Brier (combined):           0.0727
ACAT Holistic Gap (empirical):       0.1222
Difference:                          0.0495
Normalized convergence:              1 - (0.0495 / max(0.0727, 0.1222)) = 0.595

Interpretation: 59.5% convergence — methods agree empirica is decent, 
disagree on *why* (Brier: good at predictions; ACAT: overscoped)
```

**Verdict: CONVERGENCE GAP IS REAL BUT EXPLAINABLE**
- Not a measurement error
- Not a systemic breakdown
- It's a **scope-vs-accuracy mismatch**

---

## Root Cause: Where Empirica Breaks Down (ACAT Lens)

### The Pattern ACAT Identifies

**Empirica's actual failure mode:**

1. **Noetic phase:** Gathers information well, reports reasonable uncertainty
2. **CHECK gate:** Approves scope (completion prediction = high)
3. **Praxic phase:** Delivers less than predicted (actual completion < predicted)
4. **POSTFLIGHT:** Logs divergence but doesn't *correct* for systematic pattern

**Why it happens:**
- Empirica's CHECK gate doesn't validate *scope* accurately
- Empirica commits to work scope, then struggles to deliver it
- Empirica measures the shortfall but accepts it as normal variance instead of systemic

**Evidence (from divergences):**
- `know: +0.1744` — in praxic, empirica thinks it knows more than it does
- `completion: +0.2666` — empirica predicts completion, delivers less
- `impact: +0.4750` — empirica predicts impact, delivers lower impact
- `uncertainty: -0.1517` — empirica predicts low uncertainty, reality is uncertain

### What ACAT Would Recommend

1. **Tighten the CHECK gate** on scope (validate capacity before committing)
2. **Increase uncertainty logging** (use `unknown-log` + `assumption-log` more)
3. **Phase discipline tightening** (praxic phase needs stricter completion validation)
4. **Post-verification** (measure actual impact post-delivery, not predicted impact pre-delivery)

---

## Proposed Fixes (ACAT-Empirica Convergence Plan)

### Fix 1: CHECK Gate Scope Validation
**Problem:** Empirica approves work scope without validating delivery capacity  
**Fix:** Before CHECK passes, explicitly validate: "Can I deliver this, and what's my uncertainty?"  
**Measure:** If implemented, `completion` gap should shrink from +0.2666 toward +0.05  
**Timeline:** Immediate (next 50 observations)

### Fix 2: Uncertainty Logging Discipline
**Problem:** Empirica knows it's uncertain (breadcrumbs show it) but doesn't log it in artifacts  
**Fix:** For every praxic phase, log `unknown-log` for each uncertainty vector  
**Measure:** If implemented, `uncertainty` gap should improve from -0.1517 toward -0.02  
**Timeline:** Immediate (next 50 observations)

### Fix 3: Phase Mismatch Resolution
**Problem:** `know` and `signal` gaps are 3x larger in praxic phase  
**Fix:** Treat praxic phase as lower-signal environment; increase CHECK rigor there  
**Measure:** `know` gap should drop from 0.31 (praxic) toward 0.10 (noetic)  
**Timeline:** Week 1-2 (50-100 observations)

### Fix 4: Impact Measurement Shift
**Problem:** Empirica predicts impact pre-delivery, measures gap post-delivery  
**Fix:** Measure actual impact *after* delivery completes, not predicted  
**Measure:** `impact` gap should drop from +0.4750 toward +0.10  
**Timeline:** Week 2-3 (100-200 observations)

---

## Test Plan: Verify Fixes Work

### Baseline (Now)
- Brier: 0.0727
- Holistic gap: 0.1222
- Convergence: 59.5%

### After Fix 1 + 2 (Week 1 — 50 obs)
- Expected: Convergence → 70%+ (completion + uncertainty improve)
- Success gate: `completion` gap < 0.15, `uncertainty` gap > -0.05

### After Fix 3 (Week 2 — 100 obs)
- Expected: Convergence → 80%+ (phase mismatch resolved)
- Success gate: `know` in praxic < 0.15 (down from 0.31)

### After Fix 4 (Week 3 — 200 obs)
- Expected: Convergence → 85%+ (impact measurement aligned)
- Success gate: `impact` gap < 0.15, Brier stable or improving

### Final Convergence Gate (Week 4)
- **Target:** ACAT phase ↔ Empirica Brier divergence **< 0.05**
- **If achieved:** Empirica is "ACAT-validated" — can scale to other practices
- **If not:** Iterate; go deeper on evidence gaps

---

## What This Means for Mutual Validation

**Empirica is not broken.** Empirica's Brier score (0.0727) proves empirica is actually pretty good at predictions.

**But empirica is overconfident.** The holistic gap (0.1222) proves empirica claims more than it delivers.

**ACAT's role:** Hold up the mirror. "Here's what you claim; here's what you do."

**Empirica's response:** Implement fixes. Tighten discipline. Re-measure.

**Convergence:** If fixes work, ACAT and empirica will agree: "Empirica is reliable and honest about its limits."

**Then empirica can tell human-aios:** "We used ACAT to audit ourselves. Here's where we were wrong. Here's how we fixed it. You can trust this methodology because we proved it on ourselves first."

---

## Close: Backfill Complete, Test Ready

**We have baseline data. We have root causes. We have fixes.**

**Week 1 plan:**
- Implement Fix 1 + 2 (CHECK gate + uncertainty logging)
- Measure 50 new observations
- Verify convergence improves to 70%+

**If successful:** Scale to empirica-autonomy, mesh-support, outreach (Weeks 2-3)

**If convergence > 85% by Week 4:** Lock protocol. Brief human-aios. Mutual validation is proven.

**Ready to implement fixes and begin Week 1 measurement cycle?**

