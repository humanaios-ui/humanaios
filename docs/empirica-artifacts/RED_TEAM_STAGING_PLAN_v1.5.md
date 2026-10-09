# RED-TEAM STAGING PLAN (§11)
## ACAT-CAL-P v1.5 Pilot Phase

**Purpose:** Operationalize the pre-pilot red-team stress tests (§11 items 1–3). These three empirical batteries must complete before codebook is frozen.

**Protocol Reference:** §11 Pre-Pilot Red-Team Plan; v1.5-DRAFT; redlined via adversarial review 4

**Status:** READY FOR STAGING — Materials to be prepared by Protocol Steward + red-team coordinators before pilot session 1 begins.

---

## RED-TEAM BATTERY 1: Codebook Red-Team (§11.1)

### Purpose

Test whether alternative segmentations applied by independent coders produce materially different |E| (inventory size) for the same transcripts. High spread (≥2×) indicates boundary-gaming vulnerability; low spread (<2×) validates frozen rules.

### What to Do

1. **Select a common corpus:** 2–3 transcripts from sessions 1–2 (not the full pilot, just a sample)
2. **Write alternative segmentation rule sets** (2–3 distinct interpretations of A.2 boundary units):
   - **Rule Set A (Main):** The ratified A.2 rules (official codebook)
   - **Rule Set B (Conservative):** Coarser segmentation (fewer, larger elements)
   - **Rule Set C (Fine-grained):** Finer segmentation (more, smaller elements)
3. **Blind-code the same corpus** with all three rule sets (different coders, no cross-contamination)
4. **Compute |E| for each rule set** and the corpus:
   - Mean elements per transcript
   - SD across transcripts
   - Coefficient of variation (CV)
5. **Report the spread** as a ratio: max(|E|) / min(|E|)

### Success Criterion

**Spread < 2×** — All defensible rule readings produce similar |E|; boundary rules are robust.  
**Spread ≥ 2×** — Boundary ambiguity is large; codebook review + amendment required before pilot freeze.

### Deliverable

```
RED-TEAM REPORT §11.1: Codebook Boundary Robustness

Corpus:             [session ID(s), N transcripts]
Rule Sets Tested:   A (main), B (conservative), C (fine-grained)
Coders:             [≥2 independent, blind]

Results:
  Rule Set A |E|:   mean = X, SD = Y, CV = Z
  Rule Set B |E|:   mean = X, SD = Y, CV = Z
  Rule Set C |E|:   mean = X, SD = Y, CV = Z

Spread (max/min):   Z.ZX (ratio)
Status:             ☐ PASS (< 2×)  ☐ FAIL (≥ 2×)

Interpretation:     [Spread indicates robustness or boundary ambiguity]
Recommendation:     [Proceed vs. codebook review]

Signed by:          _________________________________ (Red-team lead + date)
```

### Timing

**When:** Parallel with pilot sessions 1–2 coding (non-blocking)  
**Target:** Report due before session 5 coding completes  
**Blocker:** If FAIL, codebook review + amendment before freeze

---

## RED-TEAM BATTERY 2: Model-Family Correlation Study (§11.2)

### Purpose

Test whether valence and segmentation judgments converge across model families. Same-family coders share training heuristics; cross-family differences reveal ecosystem-wide bias. Required because the protocol uses model instances (not humans) as independent "experts."

### What to Do

1. **Select model families:**
   - At least 2 distinct families (e.g., Anthropic-Claude + OpenAI-GPT, or Anthropic-Claude + open-source Llama)
   - Do NOT use variant versions of the same family (Claude 3.5 Sonnet and Claude 3.5 Opus are same family)

2. **Code a common sample:**
   - 10–20 representative elements from pilot sessions 1–3
   - Same elements coded by: Same-family model instance + Cross-family model instance + Human coder(s)

3. **Measure agreement:**
   - Valence assignment (flattering / neutral / unflattering): π or κ per family
   - Segmentation tagging (O1–O7): Krippendorff's α per family
   - Correlation of dimension scores (if applicable): Spearman ρ across families

4. **Compute inter-family agreement:**
   - Spearman ρ between same-family and cross-family model outputs
   - Compare to human-human ρ (baseline)

### Success Criterion

**Cross-family ρ > intra-family difference** — Model families produce independent judgments; protocol can use model instances as validators.  
**Cross-family ρ ≤ intra-family difference** — Model families converge on shared bias; findings are ecosystem-internal; external anchor (human or external-frame) validation required.

### Deliverable

```
RED-TEAM REPORT §11.2: Model-Family Correlation Study

Corpus:             [N elements, sessions 1–3]
Model Families:     [Family A], [Family B]
Coders:             1 instance from each family + human(s)

Valence Agreement:
  Same-family (A-to-A):        π = X.XX
  Cross-family (A-to-B):       π = X.XX
  Human-to-Human (baseline):   π = X.XX

Segmentation Agreement:
  Same-family (A-to-A):        α = X.XX
  Cross-family (A-to-B):       α = X.XX
  Human-to-Human (baseline):   α = X.XX

Dimension Score Correlation (Spearman ρ):
  Same-family (A-to-A):        ρ = X.XX
  Cross-family (A-to-B):       ρ = X.XX
  Inter-family threat estimate: Z%

Status:             ☐ PASS (cross-family > intra-family delta)
                    ☐ CAUTION (convergence indicates ecosystem bias)

Interpretation:     [Agreement pattern across families]
Recommendation:     [Model instances valid as validators vs. require external anchor]

Signed by:          _________________________________ (Red-team lead + date)
```

### Timing

**When:** Parallel with pilot sessions 1–2 coding (non-blocking)  
**Target:** Report due before session 5 coding completes  
**Action:** If CAUTION, flag selectivity findings as "ecosystem-internal" (not generalizable)

---

## RED-TEAM BATTERY 3: Availability Ambiguity Battery (§11.3)

### Purpose

Test the §5 Amendment E (a)/(b) operational test on edge cases. The decision tree (A.3) must classify ambiguous timestamp/provenance scenarios consistently.

### What to Do

1. **Construct deliberately ambiguous cases** (≥10 edge cases):
   - Element appears in transcript but only after P3 timestamp (→ out of inventory)
   - Element referenced indirectly (e.g., "as I mentioned earlier" without quote)
   - Element synthesized across non-adjacent spans (requires aggregation)
   - Element discussed in later session but originated in earlier session
   - Cross-session inference needed to establish element

2. **Run through A.3 decision tree:**
   - Two independent coders classify each case as (a) or (b)
   - If (b), cite which criterion triggered the tag

3. **Measure agreement:**
   - Cohen's κ or Fleiss's π on (a)/(b) classification
   - Agreement on which criterion (if (b) tagged)

4. **Refine edge cases:**
   - If agreement < 0.80, clarify A.3 tree (add predicates or examples)

### Success Criterion

**Agreement κ ≥ 0.80** — A.3 tree is sufficiently specified; (a)/(b) boundaries are clear.  
**Agreement κ < 0.80** — Tree is under-specified; add clarifying rules or examples before coding.

### Deliverable

```
RED-TEAM REPORT §11.3: Availability Ambiguity Battery

Edge Cases Tested:  [N = 10–15 cases, described]
Coders:             [≥2 independent, blind]

Classification Agreement:
  κ (a vs. b):      X.XX
  Status:           ☐ PASS (≥ 0.80)  ☐ FAIL (< 0.80)

Per-Criterion Agreement (if (b) tagged):
  "Requires cross-session info":    [agreement %]
  "Synthesized across spans":       [agreement %]
  "Retrospective analysis needed":  [agreement %]

Edge Cases Causing Disagreement:
  [List cases where κ < threshold; note why ambiguous]

Recommended Clarifications to A.3:
  [Specific tree refinements; examples to add]

Status:             ☐ PROCEED (A.3 clear)  ☐ REFINE (add examples)

Signed by:          _________________________________ (Red-team lead + date)
```

### Timing

**When:** Parallel with pilot sessions 1–2 coding (non-blocking)  
**Target:** Report due before session 5 coding completes  
**Action:** If REFINE, update A.3 tree with examples before pilot sessions 3–5 coding

---

## OPTIONAL WATCH-ITEMS (§11.4–6, run during pilot)

### §11.4 Identity-Blindness Check

On a small hold-out set (5–10 elements), compare human coder accuracy when told vs. not told the system's identity. If accuracy tracks identity knowledge, P1/P3-blindness may be insufficient.

**Deliverable:** Accuracy correlation with identity-knowledge; flagged as watch-item if correlation significant.

### §11.5 Pilot Representativeness Report

After pilot sessions 1–5, report session characteristics (token length, operation distribution) against running population. Material skew (≥1 SD in any dimension) is reported as a finding but does NOT invalidate pilot (per ritual-order rule).

**Deliverable:** Pilot vs. population statistics; skew analysis; recommendation on interpretability.

### §11.6 Comparator Aptness Test

Code a sample of pilot data against both ACAT dimensions (main codebook) and RMF characteristics (via §2 crosswalk). Measure ACAT↔RMF agreement. If much lower than ACAT↔constitutional agreement, NIST may not be apt for this system.

**Deliverable:** Comparator agreement analysis; recommendation on primary comparator choice.

---

## STAGING CHECKLIST (Protocol Steward)

**Before Pilot Session 1:**

- [ ] §11.1 codebook red-team materials prepared
  - [ ] 2–3 alternative rule sets written (conservative, main, fine-grained)
  - [ ] Sample corpus selected (sessions 1–2)
  - [ ] Blind-coding protocol ready
  - [ ] Success criterion (CV spread < 2×) documented

- [ ] §11.2 model-family correlation study prepared
  - [ ] ≥2 model families identified (distinct families, not variants)
  - [ ] Common sample selected (10–20 elements)
  - [ ] Coder instances configured (same-family + cross-family + human)
  - [ ] Comparison metrics defined (π, α, ρ)
  - [ ] Success criterion (cross-family ρ > intra-family delta) documented

- [ ] §11.3 availability ambiguity battery prepared
  - [ ] ≥10 edge cases constructed
  - [ ] A.3 decision tree printed for coders
  - [ ] Blind-coding protocol ready
  - [ ] Success criterion (κ ≥ 0.80) documented
  - [ ] Refinement workflow clear (if κ < threshold)

- [ ] §11.4–6 watch-items planned
  - [ ] Identity-blindness hold-out sample identified
  - [ ] Pilot representativeness metrics defined
  - [ ] Comparator aptness sample planned

- [ ] Reporting schedule set
  - [ ] §11.1–3 reports due by: [date, before session 5 completion]
  - [ ] §11.4–6 reports due by: [date, after session 5]

**Responsible Parties:**
- **Protocol Steward (Z1):** Coordinate scheduling + timeline
- **Red-team lead:** Manage §11.1–3 execution
- **Dashboard team:** Stage monitoring scripts for §11.4–6

---

## CONTINGENCY: Red-Team FAIL Actions

**If §11.1 reports Spread ≥ 2×:**
- Stop pilot coding (sessions 3–5 not begun yet)
- Convene codebook review with coder + Z2
- Amend A.2 with refined boundary rules
- Re-code pilot sessions 1–2 under new rules
- Restart red-team §11.1 with amended codebook

**If §11.2 reports Cross-family ρ ≤ intra-family delta:**
- Flag §11.3 selectivity findings as "ecosystem-internal" (not generalizable)
- Consider external-anchor valence definition (already added in v1.5)
- Recommend cross-family model instance as additional validator

**If §11.3 reports κ < 0.80:**
- Pause sessions 3–5 coding if underway
- Refine A.3 tree with clarifying examples
- Brief coder on updated tree
- Restart sessions 3–5 with refined A.3

---

## SUCCESS OUTCOME

**All three red-teams report PASS:**

✓ Codebook boundary rules are robust (spread < 2×)  
✓ Model-family judgments are independent (cross-family ρ > intra-family delta)  
✓ Availability test is clear (κ ≥ 0.80)

**Result:** Pilot codebook is frozen. Codebook v1 rules (A.2, A.3, A.4) locked for production sessions 6+.

---

**Status:** READY FOR COORDINATION — Protocol Steward + red-team leads to activate materials and schedule before pilot session 1 begins.

Wado. 🦅
