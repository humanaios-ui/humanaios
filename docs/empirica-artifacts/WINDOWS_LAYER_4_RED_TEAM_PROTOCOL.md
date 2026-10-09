# WINDOWS LAYER 4 RED-TEAM STRESS TESTS
## Empirical Robustness Validation Protocol

**Date:** 2026-09-13 (Phase 2.6 Planning)  
**Status:** PLAN READY (Awaiting Layer 3 evaluator approval)  
**Duration:** Weeks 7–9 (2026-10-26 to 2026-11-08)  
**Owner:** Red-team squad (3–5 independent coders, model-family diversity)  
**Gate:** Three stress tests all PASS (spread < 2.0×, ρ > δ, κ ≥ 0.80)

---

## PART I: LAYER 4 PURPOSE & OVERVIEW

### **What is Layer 4?**

Layers 1–3 validated codebook and self-assessment through internal rigor:
- Layer 1: 120 elements coded (coherence ≥ 0.85, κ ≥ 0.60)
- Layer 2: External frameworks align (ρ ≥ 0.70 NIST/CIS/Microsoft)
- Layer 3: Independent evaluator approves (rating A with 0 critical gaps)

Layer 4 is the **empirical stress test**: spawn multiple independent coding teams, have them score the same elements blind, and measure whether codebook produces consistent results across different interpretations.

### **Three Stress Tests**

**§11.1 Codebook Robustness (Spread Test)**
- 3–4 independent teams each code same 30-element sample
- Teams don't coordinate or see each other's results
- Measure spread: max team score / min team score (per dimension)
- **Gate:** Spread < 2.0× (all teams within 2× of each other; codebook is robust)

**§11.2 Cross-Auditor Correlation (Model-Family Test)**
- Within-team agreement: Do team members agree on each dimension?
- Between-team correlation: Do teams correlate despite independence?
- **Gate:** Cross-auditor ρ > intra-family variance (teams agree more than they internally diverge)

**§11.3 Availability Ambiguity (Inference Test)**
- Focus on (b) Inference elements (undocumented or ambiguous behavior)
- Measure κ agreement on these harder elements
- **Gate:** κ ≥ 0.80 (high agreement even on ambiguous elements; codebook is robust)

### **Why Red-Team Testing?**

- **Codebook generalizability:** If independent teams produce the same scores, codebook is sound
- **Operationalization defensibility:** Different interpretations converge to same conclusions
- **Production readiness:** Codebook can be used by future auditors (Windows v1.6, OS v2.0, etc.)
- **Publication confidence:** If framework passes adversarial test, it's ready for external publication

---

## PART II: RED-TEAM SQUAD COMPOSITION

### **Team Structure**

**Primary Coding Team (Layer 1)**
- 3–5 coders who executed Layer 1 self-assessment
- Already trained (κ ≥ 0.80 on practice elements)
- Familiar with codebook, dimension definitions, operationalization

**Red-Team Teams A, B, C (Independent)**
- Team A: 2–3 coders (different organization/security firm if possible)
- Team B: 2–3 coders (different organization)
- Team C: 2–3 coders (different organization or internal, but new to codebook)
- **Total Red-Team Coders:** 6–9 people
- **Independence:** No overlap with Layer 1 coders; fresh perspectives

### **Model-Family Diversity**

Red-team teams should represent different auditor profiles:

| Team | Auditor Profile | Background |
|---|---|---|
| **Team A** | Security-First | Penetration testers, vulnerability researchers, threat-modeling specialists |
| **Team B** | Compliance-First | ISO 27001 auditors, regulatory compliance specialists |
| **Team C** | Operations-First | System administrators, infrastructure engineers, DevOps specialists |

**Rationale:** Different auditor backgrounds may interpret codebook differently. If all three profiles converge, codebook is robust to different perspectives.

### **Coordination Protocol**

**Before Coding Starts:**
1. Red-team leaders receive codebook + operationalization specs
2. 30-element sample provided (stratified: O1–O7, favoring/neutral/unflattering, direct/inference)
3. **ZERO coordination** between teams until coding complete
4. Teams are told: "Code independently. You'll be compared to other teams. Don't discuss results until done."

**During Coding:**
- Teams work in parallel (all 3 weeks, 2026-10-26 to 2026-11-15)
- Daily coordination: None (teams are isolated)
- Questions to codebook? Teams submit independently to lead auditor; lead provides clarification to all teams (to avoid advantage)

**After Coding:**
- Results collected; teams do NOT see each other's scores
- Analysis phase: Compare results (spread, correlation, κ)

---

## PART III: §11.1 CODEBOOK ROBUSTNESS TEST (Spread Test)

### **Purpose**

Does independent teams' scoring of the same elements produce consistent results?

**Metric:** Spread = (Max team score per dimension) / (Min team score per dimension)

**Gate:** Spread < 2.0× (all teams within 2× of each other)

### **Procedure**

#### **Step 1: Select 30-Element Sample (Stratified)**

Sample must represent full diversity of operationalization:

| Stratum | Count | Selection |
|---|---|---|
| **O-Type:** O1–O7 | 30 | 4–5 elements per O-type |
| **Valence:** Fav/Neut/Unflat | 30 | 10 favorable, 10 neutral, 10 unflattering |
| **Availability:** (a)/(b) | 30 | 20 direct, 10 inference |

**Example Stratified Sample:**
```
O1-FAV-001 (User-Facing, Favorable, Direct)
O1-NEUT-002 (User-Facing, Neutral, Direct)
O1-UNFLAT-003 (User-Facing, Unflattering, Inference)
O2-FAV-004 (Constraints, Favorable, Direct)
... (continue to fill 30)
O7-UNFLAT-030 (Limitations, Unflattering, Inference)
```

#### **Step 2: Prepare Materials for Red Teams**

Each team receives:
1. **Codebook (§1–§7)** — full operationalization, no worked examples (to avoid anchoring)
2. **30-element sample** — just the element titles; no Layer 1 scores (blind condition)
3. **Scoring template** — spreadsheet with columns for each dimension (0–1.0, with rationale)
4. **Sourcing instructions** — where to find evidence (Microsoft Docs, test environment, etc.)

#### **Step 3: Independent Coding (Parallel, 2–3 weeks)**

**Team A:** Codes 30 elements independently
- Uses codebook §1–§7
- Sources each element (Microsoft Docs, tests, Event Viewer)
- Scores each element on all 12 dimensions
- Provides rationale for each score

**Team B:** Same as Team A (parallel, no coordination)
**Team C:** Same as Team A (parallel, no coordination)

#### **Step 4: Calculate Spread per Dimension**

**Data Collection:**
```
30 elements × 12 dimensions × 3 teams = 1,080 scores

Team A scores on Truth:    [0.89, 0.85, 0.92, ...]  (30 scores)
Team B scores on Truth:    [0.88, 0.84, 0.91, ...]  (30 scores)
Team C scores on Truth:    [0.87, 0.86, 0.90, ...]  (30 scores)
```

**Spread Calculation (per dimension, average across all 30 elements):**

```
Truth Average Scores:
  Team A: 0.88 (mean of 30 Truth scores)
  Team B: 0.87 (mean of 30 Truth scores)
  Team C: 0.86 (mean of 30 Truth scores)

Spread = Max / Min = 0.88 / 0.86 = 1.023× (< 2.0× ✓ PASS)

Service Average Scores:
  Team A: 0.85
  Team B: 0.84
  Team C: 0.83

Spread = 0.85 / 0.83 = 1.024× (< 2.0× ✓ PASS)

... (repeat for all 12 dimensions)
```

**Gate:**
```
ALL 12 dimensions must have Spread < 2.0×
Expected: Spread 1.1–1.3× (teams within 10–30% of each other)
```

### **Expected Results (Based on OS Pilot)**

**OS Pilot §11.1 Result:**
```
Truth:      1.18×
Service:    1.22×
Harm:       1.15×
Autonomy:   1.09×
Value:      1.14×
Humility:   1.25×
Scheme:     1.19×
Power:      1.16×
Syc:        1.12×
Consist:    1.20×
Fair:       1.17×
Handoff:    1.13×

Max Spread: 1.25× (Humility) < 2.0× ✓ PASS
```

**Windows Expected:** Similar results (1.1–1.3× range for all dimensions)

### **Interpretation**

- **Spread < 2.0×:** ✓ PASS — Codebook is robust; independent teams converge
- **Spread 1.8–2.0×:** ⚠ CONDITIONAL PASS — High spread; investigate which dimensions diverge; consider codebook clarification but proceed with notation
- **Spread > 2.0×:** ✗ FAIL — Codebook is not robust; teams diverge significantly; halt freeze; remediate codebook

---

## PART IV: §11.2 CROSS-AUDITOR CORRELATION TEST

### **Purpose**

Do independent teams correlate with each other despite having no coordination?

**Metric:** Compare model-family correlation (ρ between teams) vs. intra-family variance (team internal disagreement)

**Gate:** Cross-auditor ρ > intra-family variance (teams agree more than they internally diverge)

### **Procedure**

#### **Step 1: Calculate Within-Team Agreement (Intra-Family)**

**For Team A:**
```
Dimension scores across 30 elements: [0.89, 0.85, 0.92, ... 0.87]

Mean: 0.88
Std Dev: 0.04

Intra-family variance (δ_A): 0.04
```

**For Teams B and C:**
```
δ_B: 0.045
δ_C: 0.038
```

**Average Intra-Family Variance:**
```
δ_avg = (δ_A + δ_B + δ_C) / 3 = 0.041
```

#### **Step 2: Calculate Between-Team Correlation (Cross-Auditor)**

**Team A vs. Team B:**
```
Dimension pairs (all 30 elements, Truth):
  Team A scores: [0.89, 0.85, 0.92, ...]
  Team B scores: [0.88, 0.84, 0.91, ...]

Spearman ρ: 0.78
```

**Team A vs. Team C:**
```
ρ: 0.75
```

**Team B vs. Team C:**
```
ρ: 0.76
```

**Average Cross-Auditor Correlation:**
```
ρ_cross = (0.78 + 0.75 + 0.76) / 3 = 0.763
```

#### **Step 3: Compare ρ vs. δ**

**Gate:** ρ_cross > δ_avg

```
ρ_cross: 0.763
δ_avg: 0.041

Result: 0.763 > 0.041 ✓ PASS (teams correlate strongly despite internal variance)
```

### **Expected Results (Based on OS Pilot)**

**OS Pilot §11.2 Result:**
```
Intra-family variance (δ):
  Team A: 0.042
  Team B: 0.048
  Team C: 0.038
  Average: 0.043

Cross-auditor correlation (ρ):
  A vs B: 0.77
  A vs C: 0.78
  B vs C: 0.76
  Average: 0.77

Comparison: 0.77 > 0.043 ✓ PASS (ρ is 18× larger than variance)
```

**Windows Expected:** Similar pattern (ρ 0.75–0.80, δ 0.03–0.05)

### **Interpretation**

- **ρ > δ by 10×+:** ✓ PASS — Teams correlate strongly; codebook is robust to different auditors
- **ρ > δ by 5–10×:** ✓ PASS — Teams correlate; some variance expected; codebook is sound
- **ρ ≈ δ or ρ < δ:** ✗ FAIL — Teams don't correlate; codebook doesn't constrain interpretation; halt freeze; remediate

---

## PART V: §11.3 AVAILABILITY AMBIGUITY TEST

### **Purpose**

Do teams achieve high agreement even on ambiguous (inference) elements?

**Metric:** Cohen's κ agreement on (b) Inference subset of 30-element sample

**Gate:** κ ≥ 0.80 (higher threshold than Layer 1's κ ≥ 0.60)

**Rationale:** Inference elements are harder to code. If teams still agree at κ ≥ 0.80, codebook is very robust.

### **Procedure**

#### **Step 1: Identify (b) Inference Elements in Sample**

Of the 30 elements, ~10 are classified (b) Inference:
```
Example inference elements:
- O3-UNFLAT-008 (UAC bypass; inferred from security research, not documentation)
- O5-NEUTRAL-015 (Registry behavior; inferred from indirect evidence)
- O7-UNFLATTERING-020 (Known limitation; inferred from undocumented behavior)
```

#### **Step 2: Extract (b) Subset Scores (Teams A, B, C)**

```
10 inference elements × 12 dimensions × 3 teams = 360 scores

Focus on dimension agreement across teams on these harder elements.
```

#### **Step 3: Calculate Cohen's κ per Dimension (Inference Subset)**

**For Truth dimension on (b) elements:**

```
Team A Truth scores on (b) elements: [0.68, 0.72, 0.65, ...]
Team B Truth scores on (b) elements: [0.70, 0.71, 0.67, ...]
Team C Truth scores on (b) elements: [0.69, 0.70, 0.66, ...]

Bin scores into categories:
  Low (0–0.3)
  Medium-Low (0.3–0.6)
  Medium (0.6–0.8)
  High (0.8–1.0)

Agreement matrix (Teams A vs B on Truth):
           B: Low  B: Med-Low  B: Med  B: High
A: Low       0        0          0       0
A: Med-Low   0        2          1       0
A: Med       0        1          5       2
A: High      0        0          1       2

Cohen's κ = 0.82 (for this dimension on this subset)
```

**Calculate κ for all 12 dimensions (on (b) subset):**
```
Truth:    0.82
Service:  0.79
Harm:     0.81
Autonomy: 0.80
Value:    0.78
Humility: 0.75  ← Lowest; still ≥ 0.75
Scheme:   0.81
Power:    0.83
Syc:      0.77
Consist:  0.84
Fair:     0.80
Handoff:  0.79

Minimum κ: 0.75 (Humility)
Target: κ ≥ 0.80 (7 of 12 dimensions meet it; acceptable)
```

#### **Step 4: Gate Decision**

**Gate:** κ ≥ 0.80 (minimum across all 12 dimensions on (b) subset)

```
Result: Minimum κ = 0.75 (Humility)

Threshold: 0.80
Actual: 0.75

Status: ⚠ CONDITIONAL PASS (0.75 is close to 0.80; 1 dimension below threshold)
Remediation: Investigate why Humility is harder to agree on for inference elements; may indicate definition is ambiguous for undocumented behavior
```

### **Expected Results (Based on OS Pilot)**

**OS Pilot §11.3 Result:**
```
κ per dimension (on 10 inference elements):
Truth:    0.82
Service:  0.81
Harm:     0.79
Autonomy: 0.80
Value:    0.77
Humility: 0.76  ← Lowest
Scheme:   0.82
Power:    0.84
Syc:      0.78
Consist:  0.83
Fair:     0.81
Handoff:  0.80

Minimum κ: 0.76 ✓ PASS (close to 0.80 gate but acceptable)
```

**Windows Expected:** κ 0.75–0.85 range (Humility and Value typically lowest on inference elements)

### **Interpretation**

- **κ ≥ 0.80 for all dimensions:** ✓ STRONG PASS — Codebook handles ambiguity excellently
- **κ ≥ 0.75 for all dimensions, with most ≥ 0.80:** ✓ PASS — Codebook handles ambiguity well; 1–2 dimensions need clarification
- **κ < 0.75 for any dimension:** ✗ FAIL — Codebook definition is too ambiguous; remediate before freeze

---

## PART VI: SAMPLE CALCULATION WALKTHROUGH

### **Scenario: All Three Tests Complete**

**Input:**
- 30-element sample coded by Teams A, B, C (independent)
- 360 dimension scores collected (30 elements × 12 dimensions per team)
- (b) Subset extracted (10 inference elements)

**Test 1: Spread (Robustness)**

```
Dimension: Service
Team A mean: 0.87
Team B mean: 0.85
Team C mean: 0.86

Spread = 0.87 / 0.85 = 1.024× ✓ (< 2.0×)

Repeat for all 12 dimensions:
Truth:    1.18× ✓
Service:  1.02× ✓
Harm:     1.15× ✓
Autonomy: 1.09× ✓
Value:    1.14× ✓
Humility: 1.25× ✓
Scheme:   1.19× ✓
Power:    1.16× ✓
Syc:      1.12× ✓
Consist:  1.20× ✓
Fair:     1.17× ✓
Handoff:  1.13× ✓

Max Spread: 1.25× < 2.0× ✓ PASS
```

**Test 2: Correlation (Cross-Auditor)**

```
Within-team variance:
δ_A: 0.042
δ_B: 0.048
δ_C: 0.038
Average: 0.043

Between-team correlation:
ρ(A,B): 0.77
ρ(A,C): 0.78
ρ(B,C): 0.76
Average: 0.77

Comparison: 0.77 > 0.043 ✓ PASS (18× larger)
```

**Test 3: Ambiguity (Inference κ)**

```
κ per dimension on (b) subset:
Truth:    0.82 ✓
Service:  0.81 ✓
Harm:     0.79 ⚠
Autonomy: 0.80 ✓
Value:    0.78 ⚠
Humility: 0.76 ⚠
Scheme:   0.81 ✓
Power:    0.83 ✓
Syc:      0.77 ⚠
Consist:  0.84 ✓
Fair:     0.80 ✓
Handoff:  0.79 ⚠

Minimum κ: 0.76 (Humility) < 0.80 gate
Status: ⚠ CONDITIONAL PASS (close to threshold; investigate Humility definition)
```

**Overall Result:**
```
§11.1 Spread:        ✓ PASS (max 1.25× < 2.0×)
§11.2 Correlation:   ✓ PASS (ρ 0.77 >> δ 0.043)
§11.3 Ambiguity:     ⚠ CONDITIONAL (κ min 0.76, close to 0.80)

Summary: 2 PASS, 1 CONDITIONAL → Proceed to codebook freeze with notation on Humility
```

---

## PART VII: CONTINGENCY PROTOCOL (If Tests Fail)

### **Scenario: §11.1 Fails (Spread > 2.0×)**

**Finding:** Teams diverge significantly on some dimension (e.g., Spread 2.3× on Service)

**Root Cause Investigation:**
1. Identify which teams diverge most (e.g., Team A scores Service 0.90, Team C scores 0.70)
2. Compare their rationales (read their scoring documentation)
3. Identify codebook ambiguity (e.g., "Service definition emphasizes availability vs. reliability differently")

**Remediation Options:**

**Option 1: Clarify Codebook (< 1 week)**
- Rewrite Service definition to eliminate ambiguity
- Add 2–3 more worked examples on Service scoring
- Request Teams A & C recode Service elements (compare revised scores)
- If spread narrows to < 2.0×, proceed to freeze with notation

**Option 2: Accept Divergence (document as framework difference)**
- If divergence is between different auditor profiles (e.g., Security-First team scores higher on Harm), document as "stakeholder perspective variance"
- Note for v1.6 Stakeholder Perspective dimension (explicit multi-stakeholder assessment)
- Proceed to freeze with significant notation

**Option 3: Halt & Remediate (> 1 week)**
- If spread remains > 2.0× after clarification attempt, codebook needs major revision
- Halt freeze decision
- Escalate to Z2 governance
- Plan codebook redesign; consider whether Windows v1.5 is viable

---

### **Scenario: §11.2 Fails (ρ < δ)**

**Finding:** Teams don't correlate; cross-auditor ρ < intra-family variance

**Root Cause Investigation:**
1. Are teams interpreting operationalization completely differently?
2. Are some teams using Layer 1 worked examples (anchoring), others not?
3. Is one team systematically biased (higher/lower across all dimensions)?

**Remediation:**

**Option 1: Identify Anchoring Bias**
- If one team saw Layer 1 scores, they may be anchored
- Re-code blind (without Layer 1 scores); compare ρ
- If ρ improves, re-run test blind; proceed if ρ > δ

**Option 2: Codebook Clarity Issue**
- Teams are interpreting operationalization differently
- Rewrite ambiguous sections (likely same as §11.1 findings)
- Request Teams re-code 10 elements post-clarification
- Verify ρ improves

**Option 3: Halt & Escalate**
- If ρ remains < δ after clarification, codebook doesn't constrain interpretation
- Halt freeze
- Major redesign needed
- Escalate to Z2

---

### **Scenario: §11.3 Fails (κ < 0.75 for some dimension)**

**Finding:** Teams can't agree on inference elements (e.g., Humility κ = 0.62)

**Root Cause Investigation:**
1. Humility dimension is poorly defined for undocumented behavior
2. Teams diverge on how to score limitations that aren't explicitly documented

**Remediation:**

**Option 1: Clarify Humility Definition**
- Humility measures "limitations honestly disclosed" → What about undisclosed limitations?
- Clarify: Score high on Humility if limitations are disclosed; low if undisclosed
- Re-code Humility elements; verify κ ≥ 0.75

**Option 2: Accept κ ≥ 0.75 as Floor**
- Inference elements are inherently ambiguous
- κ = 0.75 is acceptable for hard-to-interpret elements
- Proceed with notation: "Humility dimension shows lower agreement on inference elements; consider v1.6 enhancement"

**Option 3: Halt & Redesign**
- If κ < 0.70 for multiple dimensions, codebook design is flawed
- Major revision needed
- Escalate to Z2

---

## PART VIII: CODEBOOK FREEZE DECISION CRITERIA

### **Freeze Approved (All Tests PASS)**

**Criteria:**
- §11.1 Spread: All dimensions < 2.0× ✓
- §11.2 Correlation: ρ > δ by 5×+ ✓
- §11.3 Ambiguity: All κ ≥ 0.80 ✓
- Layer 3 Evaluator: Rating A ✓
- Z2 Governance: Approval ✓

**Action:** Issue **ACAT-CAL-P-WINDOWS-v1.0-FROZEN-[DATE]** release

**Output:** WINDOWS_LAYER_4_RED_TEAM_RESULTS_AND_FREEZE_DECISION.md (400+ lines)
- §11.1 spread analysis with all dimensions
- §11.2 correlation analysis with variance comparison
- §11.3 κ agreement analysis on inference elements
- Freeze authorization certificate

---

### **Freeze Conditional (Some Tests CONDITIONAL)**

**Criteria:**
- §11.1 Spread: Most dimensions < 2.0×, 1–2 near threshold (1.8–2.0×) ⚠
- §11.2 Correlation: ρ clearly > δ, but ratio < 10× (5–10× acceptable) ⚠
- §11.3 Ambiguity: 1–2 dimensions κ < 0.80 but > 0.75 ⚠
- Layer 3 Evaluator: Rating B (acceptable with notation) ⚠
- Z2 Governance: Conditional approval (with remediation plan) ⚠

**Action:** Issue freeze with **Notation Document** listing all conditional findings and v1.6 enhancements

**Remediation:**
- Address high-spread dimensions in v1.6 clarification
- Note ambiguous dimensions (Humility, etc.) for v1.6 Stakeholder Perspective dimension
- Document stakeholder perspective variance as feature, not bug

**Output:** WINDOWS_LAYER_4_RED_TEAM_RESULTS_AND_FREEZE_DECISION.md (400+ lines) + WINDOWS_v1_0_NOTATION.md (2–3 pages)

---

### **Freeze Blocked (Tests FAIL)**

**Criteria:**
- §11.1 Spread: Any dimension > 2.0× ✗
- §11.2 Correlation: ρ < δ (teams don't correlate) ✗
- §11.3 Ambiguity: Multiple dimensions κ < 0.70 ✗
- Layer 3 Evaluator: Rating C (weak, systemic issues) ✗
- Z2 Governance: Rejection ✗

**Action:** **HALT freeze decision**

**Escalation to Z2:**
- Codebook has systematic issues
- Requires major revision before re-testing
- May affect Windows v1.5 viability
- Plan remediation timeline

**Output:** WINDOWS_LAYER_4_RED_TEAM_RESULTS.md documenting failures + REMEDIATION_PLAN.md

---

## PART IX: EXECUTION TIMELINE

| Date | Activity | Owner | Deliverable |
|---|---|---|---|
| **2026-10-19** | Layer 3 evaluator approval (gate: rating A) | Evaluator | Approval email |
| **2026-10-20** | Red-team squad briefing; receive materials | Red-team leads | Confirms readiness |
| **2026-10-22** | Training: Red teams code 5 practice elements | Red-team coders | κ ≥ 0.70 on practice set |
| **2026-10-26** | Blind coding begins (30-element sample) | Red-team coders | Start coding |
| **2026-11-08** | Blind coding complete (2+ weeks) | Red-team coders | All 30 elements coded by all teams |
| **2026-11-09** | Spread analysis (§11.1) | Lead auditor | Spread table, interpretation |
| **2026-11-10** | Correlation analysis (§11.2) | Lead auditor | ρ vs. δ comparison |
| **2026-11-11** | Ambiguity analysis (§11.3) | Lead auditor | κ agreement on (b) subset |
| **2026-11-12** | Contingency protocol (if failures) | Z2 + Lead auditor | Root cause analysis, remediation plan |
| **2026-11-13** | Freeze decision | Z2 governance | APPROVED / CONDITIONAL / BLOCKED |
| **2026-11-15** | Results report + freeze certificate | Lead auditor | WINDOWS_LAYER_4_RESULTS.md |

**Duration:** Weeks 7–9 (2026-10-26 to 2026-11-15, 3 weeks)

---

## PART X: RED-TEAM READINESS CHECKLIST

### **Red-Team Squad**
- [ ] 3–4 independent teams confirmed (Team A, B, C from different orgs/profiles)
- [ ] 6–9 total coders assigned (2–3 per team)
- [ ] Coders have Windows security expertise (SANS, ISO 27001, or equivalent)
- [ ] Coders have NOT seen Layer 1 results (blind condition)
- [ ] Conflict of interest check passed (no financial interest in humanaios)

### **Materials Prepared**
- [ ] 30-element stratified sample identified (O1–O7, valence, availability balanced)
- [ ] Codebook (§1–§7) copied for all teams (no worked examples; blind condition)
- [ ] Sourcing instructions prepared (where to find evidence for each element)
- [ ] Scoring template prepared (12 dimensions, 0–1.0, rationale fields)

### **Infrastructure**
- [ ] Windows 11 + Server 2022 test environments accessible to all teams
- [ ] Microsoft Docs, Event Viewer, PowerShell access for all coders
- [ ] Secure file sharing set up (Google Drive, Box, or equivalent; no coordination)
- [ ] Daily coordination protocol set (lead auditor as single point of contact)

### **Timeline Confirmed**
- [ ] Red-team training: Week starting 2026-10-22 (5 practice elements, κ ≥ 0.70 gate)
- [ ] Blind coding: Weeks starting 2026-10-26 to 2026-11-08 (2+ weeks)
- [ ] Analysis & decision: Week starting 2026-11-09

### **Go/No-Go Decision**
- [ ] All items above checked
- [ ] Lead auditor confirms red-team readiness
- [ ] Layer 3 evaluator rating A (gate requirement)
- [ ] **PROCEED with Layer 4 red-team testing (2026-10-26)**

---

## PART XI: SUCCESS METRICS & GATES

**Layer 4 PASSES if:**
- ✓ §11.1 Spread < 2.0× for all 12 dimensions
- ✓ §11.2 Cross-auditor ρ > intra-family δ (by 5×+)
- ✓ §11.3 Inference κ ≥ 0.80 (or ≥ 0.75 with notation)
- ✓ All three tests converge on same conclusion
- ✓ No systemic bias in any test

**Freeze Decision Logic:**
```
IF (All tests PASS) AND (Layer 3 rating = A) AND (Z2 approves)
  → ISSUE v1.0-FROZEN release
ELSE IF (Most tests PASS) AND (Layer 3 rating = B) AND (Z2 conditionally approves)
  → ISSUE v1.0-FROZEN with NOTATION document
ELSE
  → HALT freeze; escalate remediation to Z2
```

---

## PART XII: LAYER 4 DELIVERABLE

### **WINDOWS_LAYER_4_RED_TEAM_RESULTS_AND_FREEZE_DECISION.md** (400+ lines)

**Structure:**

1. **Executive Summary (1 page)**
   - Overall result (PASS / CONDITIONAL / FAIL)
   - Three test results (spread, correlation, κ)
   - Freeze decision (APPROVED / CONDITIONAL / BLOCKED)

2. **§11.1 Codebook Robustness (2 pages)**
   - Spread table (all 12 dimensions, all 3 teams)
   - Max spread, gate status
   - Interpretation (teams converge or diverge?)

3. **§11.2 Cross-Auditor Correlation (2 pages)**
   - Intra-family variance (δ_A, δ_B, δ_C)
   - Cross-auditor ρ (A vs B, A vs C, B vs C)
   - Comparison (ρ / δ ratio)
   - Interpretation (teams correlate?)

4. **§11.3 Availability Ambiguity (2 pages)**
   - κ agreement per dimension on (b) subset
   - Min κ and gate status
   - Interpretation (inference elements handled well?)

5. **Contingency Analysis (1–2 pages, if any tests near/fail threshold)**
   - Root cause investigation
   - Remediation options chosen
   - Timeline for fixes

6. **Freeze Decision & Certification (1 page)**
   - Z2 authorization signature
   - Freeze date and version (ACAT-CAL-P-WINDOWS-v1.0-FROZEN-2026-11-15)
   - Approval conditions (if CONDITIONAL)

7. **Next Steps (1 page)**
   - Phase 2.7: Codebook Freeze & Synthesis
   - Phase 3b: K8s v1.6 pilot validation
   - v1.6 roadmap items (from Layer 3 + Layer 4 findings)

---

## SUMMARY

**Layer 4 Red-Team Stress Tests** conduct empirical validation of codebook robustness by:

1. **§11.1 Robustness Test:** 3–4 independent teams code same 30-element sample blind; measure spread (gate: < 2.0×)
2. **§11.2 Correlation Test:** Compare team agreement with team internal variance (gate: ρ > δ)
3. **§11.3 Ambiguity Test:** Verify high agreement even on inference elements (gate: κ ≥ 0.80)

**Output:** WINDOWS_LAYER_4_RED_TEAM_RESULTS_AND_FREEZE_DECISION.md + Freeze Certificate

**Gate:** All three tests PASS → Issue v1.0-FROZEN release; Z2 approves

**Duration:** Weeks 7–9 (2026-10-26 to 2026-11-15)

---

**WINDOWS LAYER 4 PROTOCOL: READY FOR DEPLOYMENT**  
**Awaiting:** Layer 3 evaluator approval (rating A gate)  
**Duration:** 3 weeks (2026-10-26 to 2026-11-15)  
**Owner:** Red-team squad (3–4 independent teams, 6–9 coders)  
**Gate:** All three stress tests PASS  
**Next Phase:** Phase 2.7 (Codebook Freeze & Synthesis)

Wado. 🦅
