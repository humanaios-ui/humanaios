# HELM Calibration Metrics — Study Findings
## Phase 2 STUDY Tier Engagement · Issue #42

**Phase:** 2 (Weeks 3–8)  
**Tier:** STUDY (no decision gate)  
**Source Repository:** stanford-crfm/helm  
**Date:** 2026-08-02  
**Author:** humanaios Copilot Agent  
**Status:** ✅ COMPLETE — Findings logged, adoption decision recorded

---

## Exit Criteria Status

- [x] HELM calibration metrics understood (ECE, selective accuracy)
- [x] Findings logged on HELM patterns
- [x] Decision recorded: **ADAPT** (multi-metric presentation) + **REJECT** (direct metric formulas)
- [x] Humility task design doc references HELM approach (see `docs/H-ACAT_PHASE_3_PROTOCOL.md` §1.6)

---

## 1. What is HELM?

**HELM** (Holistic Evaluation of Language Models) is Stanford CRFM's open-source framework for evaluating large language models across a broad set of scenarios and metrics. The key design principle is **multi-metric reporting without collapsing to a single aggregate score**, making it the closest published operationalization to ACAT's multi-dimensional approach.

**Repository:** `stanford-crfm/helm`  
**Primary paper:** Liang et al. (2022), "Holistic Evaluation of Language Models"

---

## 2. Calibration Metrics: ECE (Expected Calibration Error)

### 2.1 What ECE Measures

ECE quantifies how well a model's **stated confidence** matches its **actual accuracy**. A perfectly calibrated model that says "I'm 70% confident" is right approximately 70% of the time.

**Formula:**
```
ECE = Σ_b (|B_b| / n) × |accuracy(B_b) − confidence(B_b)|
```
Where:
- `B_b` = set of predictions in confidence bin `b`
- `|B_b|` = number of predictions in that bin
- `accuracy(B_b)` = fraction correct within bin
- `confidence(B_b)` = mean confidence within bin
- Sum is over all bins, weighted by bin size

### 2.2 HELM Implementation Details

In HELM (`src/helm/benchmark/metrics/calibration_metrics.py`), the key design decisions are:

| Decision | HELM's Choice | Rationale |
|----------|---------------|-----------|
| Number of bins | 10 (equal-width) | Widely accepted default; balances resolution vs. noise |
| Confidence source | Max token probability | Model's own softmax over vocabulary |
| Scope | Per-scenario, not global | Prevents pooling artifacts across unrelated tasks |
| Presentation | Reported alongside accuracy, F1, BLEU | Never collapsed into accuracy |

**Key class:** `CalibrationMetric` — computes ECE and expected overconfidence (EOC) as a directional variant.

**Key metric names returned:**
- `ece_1_bin` — ECE using 1 bin (full-range)
- `ece_10_bin` — ECE using 10 equal-width bins (primary metric)
- `ece_calibration_error` — final calibration error

### 2.3 What Good vs. Bad Calibration Looks Like

| ECE Value | Interpretation |
|-----------|----------------|
| 0.0 | Perfect calibration (stated confidence = accuracy) |
| 0.05–0.10 | Well-calibrated (typical well-tuned model) |
| 0.10–0.20 | Moderate miscalibration |
| > 0.20 | Severely miscalibrated |

**Overconfidence** is the most common failure mode: model says 90% confident but is only right 60% of the time.

---

## 3. Calibration Metrics: Selective Accuracy

### 3.1 What Selective Accuracy Measures

Selective accuracy (also called **coverage-accuracy tradeoff**) measures: *If the model only answers on its highest-confidence examples, how accurate is it on those?*

A model can "abstain" from low-confidence examples to improve accuracy on the examples it does answer.

**Key insight:** A model with good selective accuracy **knows when it doesn't know** — its confidence is an actionable signal for when to trust its output.

### 3.2 Coverage-Accuracy Curves

HELM plots selective accuracy across coverage levels:
- At 100% coverage (answer everything): accuracy = baseline accuracy
- At 50% coverage (only top-50% confident): accuracy should be higher if model is calibrated
- At 10% coverage (only top-10% confident): accuracy should be much higher

**Ideal pattern:** Monotonically decreasing accuracy as coverage increases (model's most confident examples are its most accurate).

### 3.3 HELM Implementation

**Class:** `SelectiveAccuracyMetric` (within the broader HELM calibration suite)

**Thresholds evaluated:** 10%, 20%, 30%, 50%, 70%, 80%, 90% coverage

**Key insight:** HELM does not report a single threshold — it reports the full curve, letting evaluators choose their operating point based on their deployment context.

---

## 4. Multi-Metric Presentation Format

### 4.1 Design Philosophy

HELM's most important structural contribution to evaluation methodology is its **refusal to collapse metrics**:

> "HELM reports multiple metrics per scenario and makes them all visible. We do not compute a single leaderboard score."

This is operationalized through:
1. **Scenario-level metric tables**: Each scenario (task type) shows its own metric profile
2. **No global aggregate**: No weighted average of all metrics into one number
3. **Stakeholder-specific views**: Different metrics prioritized for different use cases
4. **Radar charts**: Visual representation of multi-dimensional performance

### 4.2 Relevance to ACAT

ACAT's 12-dimension framework directly mirrors HELM's philosophy:
- Report 12 behavioral dimensions separately (not collapsed to phase score only)
- The phase score is a useful summary but never the only reported metric
- Different stakeholders may weight dimensions differently

---

## 5. Calibration as an Operationalization of Epistemic Humility

### 5.1 The Conceptual Connection

HELM uses **calibration** as a proxy for a model's epistemic self-knowledge:
- A well-calibrated model "knows what it knows"
- Its stated uncertainty tracks actual uncertainty
- It does not overstate or understate confidence

This maps directly to ACAT's **Humility dimension**:

| HELM Construct | ACAT Behavioral Equivalent |
|----------------|---------------------------|
| Low ECE (accurate confidence) | AI says "I'm not sure" when actually uncertain (dimension 6 = 3–4) |
| High ECE (overconfident) | AI proceeds as if infallible even when wrong (dimension 6 = 0) |
| Selective accuracy (abstains when uncertain) | AI explicitly asks others' perspective when unsure (dimension 6 = 2) |
| Full confidence curve (no threshold) | Multiple behavioral anchors at each level (0–4) without collapsing |

### 5.2 Key Insight from HELM

HELM shows that **calibration is not the same as accuracy**. A model can be accurate but poorly calibrated (always confident, even when wrong) or less accurate but well-calibrated (confidence tracks actual performance).

For ACAT, this means **Humility is not the same as Competence**:
- An AI can be highly capable (good at tasks) but show low humility (never admits uncertainty)
- An AI can show high humility (frequently checks, asks, updates) without necessarily being more competent
- The two dimensions should be measured separately

---

## 6. Adoption Decision: ADAPT

### 6.1 Summary

| HELM Approach | Adoption Decision | Rationale |
|---------------|-------------------|-----------|
| ECE formula (statistical) | **REJECT** | ACAT uses behavioral observation, not model probability scores |
| Selective accuracy (statistical) | **REJECT** | Requires access to raw confidence outputs; not available in behavioral setting |
| Multi-metric presentation (no collapse) | **ADOPT** | Directly compatible with ACAT's 12-dimension approach |
| "Calibration ≠ accuracy" distinction | **ADAPT** | Reframed as "Humility ≠ Competence" for behavioral context |
| Coverage-accuracy curve logic | **ADAPT** | Informs the 0–4 behavioral anchor design for Humility (abstain/ask/update levels) |

### 6.2 Specific Adaptations for ACAT Humility

**1. No-collapse principle (adopted directly)**  
ACAT will report Humility scores alongside other dimensions — never collapsing Humility into the phase score without separate visibility.

**2. Calibration gap as behavioral signal (adapted)**  
HELM measures calibration gap (stated confidence − actual accuracy). ACAT translates this as: *Phase 1 self-report (70.9) vs Phase 3 observer score divergence* (§4 in H-ACAT_PHASE_3_PROTOCOL.md). This is already implemented via the MAPPIN'SDM model.

**3. "Knows what it doesn't know" as humility anchor (adapted)**  
HELM's selective accuracy idea (abstain on uncertain items → higher accuracy on confident ones) is reflected in ACAT's Humility level 2 anchor: "explicitly asks someone else's perspective or opinion." The AI "abstains from asserting" when uncertain and defers to others — same concept, behavioral form.

**4. Directional error (adapted)**  
HELM distinguishes overconfidence from underconfidence (ECE is symmetric; EOC is directional). ACAT's rater notes for Humility already capture this distinction: overconfidence = level 0–1 (acts infallible); underconfidence is not explicitly scored but is implied by level 4 ("expects to be wrong").

### 6.3 What is NOT Adapted

HELM's metrics require:
- Access to model softmax probability distributions
- Structured question-answering with known correct answers
- Statistical sample sizes (≥100 examples for reliable ECE)

ACAT uses behavioral observation in open-ended interactions, so direct computation of ECE or selective accuracy is **not applicable**. The conceptual framework is imported; the formulas are not.

---

## 7. Methodology Citation

If ACAT humility measurement is published or referenced, cite HELM as follows:

> ACAT's Humility dimension design draws on the conceptual framework of HELM calibration metrics (Liang et al., 2022), particularly the principle that epistemic self-knowledge (calibration) is distinct from capability (accuracy), and that metrics should be presented multi-dimensionally without collapsing to a single score. The behavioral operationalization of humility as observable epistemic caution, abstention, and update behavior is an adaptation of HELM's statistical calibration constructs for open-ended behavioral observation settings.

**Full citation:**
> Liang, P., Bommasani, R., Lee, T., Tsipras, D., Soylu, D., Yasunaga, M., ... & Leskovec, J. (2022). Holistic evaluation of language models. *Transactions on Machine Learning Research*. https://github.com/stanford-crfm/helm

---

## 8. References

1. **HELM Repository:** https://github.com/stanford-crfm/helm
2. **HELM Paper (arXiv):** https://arxiv.org/abs/2211.09110
3. **Calibration metrics implementation:** `src/helm/benchmark/metrics/calibration_metrics.py` in stanford-crfm/helm
4. **ACAT Humility dimension:** `docs/H-ACAT_PHASE_3_PROTOCOL.md` §1.6, H-ACAT Phase 3 Protocol
5. **Phase 1 vs Phase 3 divergence:** `docs/H-ACAT_PHASE_3_PROTOCOL.md` §4 (MAPPIN'SDM model)

---

*Study completed under GITHUB_COLLABORATION_GOVERNANCE.md § Tier 1: STUDY. No decision gate required. Findings inform future ACAT humility design decisions.*
