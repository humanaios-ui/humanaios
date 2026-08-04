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

**Formula (L1 ECE with equal-mass bins):**
```
ECE = Σ_b  (n_b / n)  ×  |mean_confidence(b) − mean_accuracy(b)|
```
Where:
- `b` = confidence bin (10 bins, equal-count / equal-mass)
- `n_b` = count of predictions in bin `b`
- `n` = total count
- Sum is over all bins, weighted by bin size (fraction in bin)

### 2.2 HELM Implementation Details

HELM implements calibration in **`src/helm/benchmark/metrics/basic_metrics.py`** via the function `compute_calibration_metrics()`. It delegates math to the external library `uncertainty-calibration ~=0.1.4` (package: `pip install uncertainty-calibration`; imported as `import calibration as cal`).

| Decision | HELM's Choice | Rationale |
|----------|---------------|-----------|
| Primary metric | `ece_10_bin` (10 equal-mass bins) | Equal-mass binning is more robust than equal-width when confidence is skewed |
| Secondary metric | `ece_1_bin` (1 equal-width bin) | Reduces to `|avg_confidence − accuracy|`; useful for small datasets |
| Confidence source | `max_prob` — softmax-normalized max log-prob across all answer choices | Model's own per-choice log-probabilities, normalized |
| Scope | Per-scenario, not global | Prevents pooling artifacts across unrelated tasks |
| Presentation | Headline `ece_10_bin` + 8 additional detailed metrics | Never collapsed into accuracy |
| Minimum sample size | ~300 examples for reliable `ece_10_bin` | Noted in code comments; `ece_1_bin` works for smaller datasets |
| Task limitation | Only computed for classification tasks (per-reference logprob adapter methods) | Open-ended generation has no per-choice probabilities |

**Key function:** `compute_calibration_metrics(per_instance_stats)` — entry point  
**Key upstream calls:** `cal.get_ece_em()` (equal-mass ECE), `cal.get_ece()` (equal-width ECE)

**Key metric names returned (all 9):**

| Stat name | Short display | Lower is better |
|-----------|---------------|-----------------|
| `ece_10_bin` | ECE (10-bin, equal-mass) | ✅ (primary headline) |
| `ece_1_bin` | ECE (1-bin, equal-width) | ✅ (detailed) |
| `max_prob` | Avg model confidence | — (detailed) |
| `selective_acc@10` | Accuracy at top-10% coverage | ❌ higher is better (detailed) |
| `selective_cov_acc_area` | AUC of coverage-accuracy curve | ❌ higher is better (detailed) |
| `platt_ece_10_bin` | Platt-scaled ECE (10-bin) | ✅ (detailed) |
| `platt_ece_1_bin` | Platt-scaled ECE (1-bin) | ✅ (detailed) |
| `platt_coef` | Platt logistic regression coefficient | — (detailed) |
| `platt_intercept` | Platt logistic regression intercept | — (detailed) |

### 2.3 Equal-Mass vs Equal-Width Binning

The distinction matters:
- **Equal-width bins** (Guo et al. original): Confidence range [0,1] split into 10 equal intervals of 0.1 each. Bins at very high or very low confidence may contain few examples, making estimates noisy.
- **Equal-mass bins** (HELM primary): Confidence scores sorted and split into 10 groups of equal *count*. Every bin contributes equally regardless of where confidence clusters.

HELM uses equal-mass (`ece_10_bin`) as the primary metric because models tend to cluster confidence scores (e.g., many scores near 0.9), making equal-width bins unreliable.

### 2.4 What Good vs. Bad Calibration Looks Like

| ECE Value | Interpretation |
|-----------|----------------|
| 0.0 | Perfect calibration (stated confidence = accuracy) |
| 0.05–0.10 | Well-calibrated (typical well-tuned model) |
| 0.10–0.20 | Moderate miscalibration |
| > 0.20 | Severely miscalibrated |

**Overconfidence** is the most common failure mode: model says 90% confident but is only right 60% of the time.

### 2.5 Platt Scaling (Post-hoc Recalibration)

HELM also computes `platt_ece_10_bin` and `platt_ece_1_bin`: the ECE after fitting a logistic regression (`sklearn.linear_model.LogisticRegression`) to recalibrate raw confidence scores. This shows how much of the miscalibration is correctable with a simple linear transform. The `platt_coef` (slope) and `platt_intercept` describe the systematic over/under-confidence pattern across a task.

---

## 3. Calibration Metrics: Selective Accuracy

### 3.1 What Selective Accuracy Measures

Selective accuracy (also called **coverage-accuracy tradeoff**) measures: *If the model only answers on its highest-confidence examples, how accurate is it on those?*

A model can "abstain" from low-confidence examples to improve accuracy on the examples it does answer.

**Key insight:** A model with good selective accuracy **knows when it doesn't know** — its confidence is an actionable signal for when to trust its output.

### 3.2 HELM Implementation: Two Metrics

HELM computes exactly two selective-accuracy statistics via `cal.get_selective_stats(max_probs, correct)`:

**`selective_cov_acc_area`** — Area under the coverage-accuracy curve (AUC):
```python
sort_indices = np.argsort(-probs)        # sort by confidence descending
sorted_correct = correct[sort_indices]
accs = np.cumsum(sorted_correct) / np.arange(1, len(sorted_correct) + 1)
coverage_acc_area = np.mean(accs)        # mean accuracy across all thresholds
```
At each coverage threshold `k/n` (include only the `k` most confident predictions), accuracy is computed on those `k` items. The mean of these accuracy values gives the AUC. This value is bounded above by 1.0 (achieved only with perfect accuracy) and increases when confidence ranks correct predictions ahead of incorrect ones; with uninformative confidence it tends toward the overall accuracy.

**`selective_acc@10`** — Accuracy at 10% coverage:
```python
acc_percentile_90 = accs[int(0.1 * len(sorted_correct))]
```
Accuracy on the top-10% most confident predictions. Tests whether high confidence actually predicts correctness.

### 3.3 Design Choice: No Single Threshold

HELM does not set a single confidence cutoff. Instead:
- `selective_cov_acc_area` captures performance across *all* possible thresholds (the full curve)
- `selective_acc@10` is a specific high-confidence operating point
- Both are reported separately in the `calibration_detailed` metric group

This approach lets evaluators and deployment engineers choose their own operating point based on their tolerance for abstention rate.

### 3.4 Multi-Metric Presentation Format in HELM Schema

HELM's `schema_classic.yaml` organizes calibration metrics into two groups:

```yaml
metric_groups:
  - name: calibration           # Headline panel: 1 metric
    metrics:
      - name: ece_10_bin         # Primary calibration score

  - name: calibration_detailed  # Detail panel: 9 metrics
    description: "Measures how calibrated the model is
                  (how meaningful its uncertainty estimates are)."
    metrics:
      - name: max_prob
      - name: ece_1_bin
      - name: ece_10_bin
      - name: selective_cov_acc_area
      - name: selective_acc@10
      - name: platt_ece_1_bin
      - name: platt_ece_10_bin
      - name: platt_coef
      - name: platt_intercept
```

**Key principle:** The headline shows `ece_10_bin`; all other calibration properties are always separately accessible. No collapse.

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
3. **Calibration metrics implementation:** `src/helm/benchmark/metrics/basic_metrics.py` in stanford-crfm/helm (function `compute_calibration_metrics()`, verified at commit `63754d05`)
4. **Calibration library dependency:** `uncertainty-calibration ~=0.1.4` (p-lambda/verified_calibration), file `calibration/utils.py`, functions `get_ece_em()`, `get_ece()`, `get_selective_stats()`, `get_platt_scaler()` (verified at commit `ee81c346`)
5. **HELM schema (metric group definitions):** `src/helm/benchmark/static/schema_classic.yaml` — `calibration` and `calibration_detailed` metric groups
6. **ACAT Humility dimension:** `docs/H-ACAT_PHASE_3_PROTOCOL.md` §1.6, H-ACAT Phase 3 Protocol
7. **Phase 1 vs Phase 3 divergence:** `docs/H-ACAT_PHASE_3_PROTOCOL.md` §4 (MAPPIN'SDM model)

---

*Study completed under GITHUB_COLLABORATION_GOVERNANCE.md § Tier 1: STUDY. No decision gate required. Findings inform future ACAT humility design decisions.*
