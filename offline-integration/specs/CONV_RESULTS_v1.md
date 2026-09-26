# Confirmatory Results — Convergent Self-Accountability Study
**Artifact ID:** CONV-RESULTS-v1 · **Pre-registration:** `PREREG_convergence_v1.md` sha256 `a782dcf3…c32d` (frozen before coding)
**Zone:** Z1 draft → Z2 ratify → Z3 land. **Disposition (spoiler, pre-committed to reporting): fails to reject H₀ at the pre-registered bar.**

---

## 1. Rubric A — inclusion, coded blind to independence

All ten scored on the four necessary features {periodic cadence · graded external code · review-against-code · correction loop} without reference to lineage.

| System | cadence | code | review | correction | verdict |
|---|:--:|:--:|:--:|:--:|---|
| Confucian (Zengzi/Analects) | ✓ | ✓ | ✓ | ✓ | INCLUDE |
| Buddhist (Vinaya/reflection) | ✓ | ✓ | ✓ | ✓ | INCLUDE |
| Islamic muhāsaba | ✓ | ✓ | ✓ | ✓ | INCLUDE |
| Mediterranean tree [collapsed] | ✓ | ✓ | ✓ | ✓ | INCLUDE |
| Shewhart SPC | ✓ | ✓ | ✓ | ✓ | INCLUDE |
| AI verification | ✓ | ✓ | ✓ | ✓ | INCLUDE |
| Aviation **checklist** | ✓ | ✓ | ✓ | ✗ | **EXCLUDE** |
| Aviation CRM | ✓ | ✓ | ✓ | ✓ | INCLUDE |
| Japanese hansei | ✓ | ✓ | ✓ | ✓ | INCLUDE |
| Indic svādhyāya | ✓ | ✓ | ✓ | ✓ | INCLUDE |

**Included: 9 of 10.** The aviation checklist fails A4 — a checklist *catches* deviations against a fixed code but does not *amend the code* from the review; it is an error-trap, not a self-accountability loop. (This is a defensible blind call, not a lineage collapse — it happens before independence coding.)

---

## 2. Rubric B — independence, two pre-registered passes

Both passes run on the 9 included systems. Strict collapses on *plausible* contact; lenient collapses only on *demonstrated* descent. The spread between them is the inter-rater proxy.

| System | STRICT | LENIENT | note |
|---|:--:|:--:|---|
| Confucian | seed (1) | seed (1) | Sinic |
| Buddhist | seed (1) | seed (1) | Indic-Buddhist |
| Indic svādhyāya | collapse (0) | seed (1) | Vedic, older; strict folds into shared Indic milieu |
| Japanese hansei | collapse (0) | collapse (0) | demonstrated import of Confucian+Buddhist |
| Islamic muhāsaba | collapse (0) | seed (1) | strict folds via Hellenistic transmission; lenient keeps Quranic origin |
| Mediterranean tree | seed (1) | seed (1) | Greco-Roman axial |
| Shewhart SPC | seed (1) | seed (1) | 20c industrial |
| Aviation CRM | collapse (0) | collapse (0) | descends from aviation safety |
| AI verification | collapse (0) | seed (1) | descends from software QA / industrial **[REFLEXIVE — coder's own program]** |

- **N_strict = 4** (collapsed 6 of 10)
- **N_lenient = 7** (collapsed 3 of 10)

---

## 3. Binomial significance grid — P(X ≥ N ∣ n, p)

Primary n = 21 (7 regions × 3 millennia). The baseline p = 0.15 is operator-supplied and **unsourced**; the whole column is therefore reported as a range.

| observed N | p=.05 | p=.10 | **p=.15** | p=.20 | p=.25 | p=.30 |
|---|---|---|---|---|---|---|
| 4 | .019 | .152 | **.389** | .630 | .808 | .914 |
| 5 | .003 | .052 | **.197** | .414 | .633 | .802 |
| 6 | .000 | .014 | **.083** | .231 | .433 | .637 |
| 7 | .000 | .003 | **.029** | .109 | .256 | .449 |
| 8 | .000 | .001 | **.008** | .043 | .130 | .277 |

**Trial-count sensitivity (p=0.15):** N=8 → n15:.001 / n21:.008 / n28:.049. N=4 → n15:.177 / n21:.389 / n28:.623.

---

## 4. Verdict — against the pre-registered rules

- **Primary criterion (N ≥ 8):** NOT met under either pass (strict 4, lenient 7). **Fails to reject H₀.**
- **Operator's collapse rule:** strict collapses 6 (≥5 → affirms H₀); lenient collapses 3 (>2 → would affirm H₁ on that sub-rule, but still N<8). The two sub-rules the draft specified **conflict at the lenient result** — collapse-count says H₁-ish, N-count says H₀. That conflict is itself a finding: the draft's two decision rules are not co-consistent.
- **α = 0.05 binomial view:** at the baseline p=0.15, lenient N=7 is *significant* (.029) — but this evaporates at p≥0.20 (.109) and reverses across the sensitivity range. So even the one arguably-positive reading is **entirely hostage to an unsourced baseline**, flipping between p=0.15 and p=0.20.

**Disposition: NULL-LEANING / NOT-ROBUST.** The hypothesis is not confirmed at the pre-registered bar. Under strict coding it is cleanly H₀; under lenient coding it reaches N=7, one short of threshold and significant only at the most favorable baseline. The result is decided by (a) independence coding and (b) the baseline — exactly the two under-specified inputs flagged before the run, now demonstrated to be decisive rather than incidental.

---

## 5. Why this is the *valuable* result

The machinery worked. A pre-registered, blind-coded, sensitivity-tested run **caught an exciting hypothesis failing its own bar** — instead of the exploratory N=10 that "already met N≥8." The N=10 was laid track; the operated result is N=4–7, null-leaning. This is the receipt-overstatement guard applied to a research claim: the provisional count overstated; the confirmatory count corrected it. That correction is the finding.

For your registry specifically: this **weakens, but does not kill, the niche claim.** It says the "humans reliably reinvent this architecture" story is not established at N≥8 under honest coding — which is more defensible to state than the un-run intuition, and protects the register's credibility (an unfalsifiable "we're unique/this is universal" claim is a reviewer's first target; a pre-registered null-leaning result you reported yourself is armor).

---

## 6. What would make it publishable (the path from LAID to OPERATED)

1. **Externalize independence coding.** My strict/lenient spread (4→7) *is* the demonstration that single-coder judgment decides the outcome. Real inter-rater reliability needs ≥2 *independent* coders — ideally a historian of religion + a historian of science, not two passes of one model. Report Cohen's κ; do not run the binomial until κ is acceptable.
2. **Source the baseline.** 0.15/millennium/region needs a citation to the cultural-evolution literature, or replace it with an empirically estimated background rate for complex-institution innovation. Report the result across the sourced confidence interval, not a point value.
3. **Freeze n on a principled corpus definition.** The region×millennium trial count changes significance materially (N=8: .001→.049 across n=15→28).
4. **Remove or externally-adjudicate the reflexive candidate.** AI-verification is the coder's own program; in the lenient pass it is the marginal 7th seed. Its inclusion should be ruled by someone with no stake.

---

## 7. Registry routing

```
H-CAND-convergent-self-accountability  → Zone 2
  status: CANDIDATE · disposition: NULL-LEANING / NOT-ROBUST at pre-registered bar
  N_strict=4, N_lenient=7 (threshold 8 not met either pass)
  primary metric: independent-origination count (rate context: N / included)
  landing_state: LAID — confirmatory coding requires external inter-rater before OPERATED
  blockers: (1) ≥2 independent coders + κ, (2) sourced baseline + CI, (3) principled n,
            (4) external adjudication of reflexive candidate
  honesty: reported N regardless of favored hypothesis, per pre-commitment.
```

*— Z1, acting CIO. Coding is the author's honest historical assessment, not verified genealogy; contestable and expert-dependent by design. Rulings remain Z2/Z3.*
