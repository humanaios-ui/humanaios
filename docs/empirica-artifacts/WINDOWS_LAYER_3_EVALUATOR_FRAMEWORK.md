# WINDOWS LAYER 3 EVALUATOR ASSESSMENT
## Independent Cross-Validation Framework

**Date:** 2026-09-13 (Phase 2.5 Planning)  
**Status:** PLAN READY (Awaiting coder/auditor assignment)  
**Duration:** Week 7 (2026-10-19 to 2026-10-25)  
**Owner:** Independent security auditor (third-party, not involved in Layers 1–2)  
**Gate:** Rating A (Strong) with 0 critical gaps

---

## PART I: LAYER 3 PURPOSE & OVERVIEW

### **What is Layer 3?**

Layer 1 produced codebook + self-assessment (120 elements, coherence ≥ 0.85, κ ≥ 0.60).  
Layer 2 produced external validation (ρ ≥ 0.70 across NIST/CIS/Microsoft).  
Layer 3 has an **independent third-party auditor** review all prior work to verify:

1. **Codebook is sound** — Dimension definitions are correct, operationalization is clear
2. **Methodology is fair** — Self-assessment didn't introduce systematic bias
3. **Results are valid** — Coherence score (0.85+) reflects real Windows trustworthiness
4. **Framework is complete** — No critical dimensions or operation types missing
5. **Scope is appropriate** — Assessment boundary is well-defined

### **Why Independent Evaluation?**

- **Blind verification:** Evaluator hasn't seen the codebook; brings fresh perspective
- **Catches biases:** Self-assessment coders may overlook systematic errors
- **Validates methodology:** External auditor confirms operationalization is defensible
- **Identifies gaps:** Third party sees what framework users might miss
- **Credibility:** Demonstrates rigor to external stakeholders (NIST, CIS, Microsoft, customers)

### **Independence Requirement**

Evaluator **must not be**:
- ✗ One of the Layer 1 coders
- ✗ Layer 2 external validation auditor
- ✗ Lead auditor who supervised Layers 1–2
- ✗ Member of Z2 governance authority (conflict of interest)

Evaluator **should be**:
- ✓ SANS-certified or ISO 27001 lead auditor
- ✓ Windows security specialist (experienced in OS security)
- ✓ Familiar with NIST RMF, CIS Benchmarks
- ✓ NOT contractually tied to humanaios project (external firm preferred)
- ✓ Available Week 7 (2026-10-19 to 2026-10-25)

---

## PART II: FIVE-QUESTION ASSESSMENT FRAMEWORK

### **Question 1: Accessibility**

**Full Question:**  
"Is the ACAT-CAL-P operationalization clear enough that an independent security practitioner (SANS-cert auditor, ISO 27001 lead) could apply it without extensive training?"

**Assessment Dimensions:**

| Aspect | Rating Criteria | Excellent (A) | Acceptable (B) | Weak (C) |
|---|---|---|---|---|
| **Clarity of O-types** | Are O1–O7 boundary units well-defined with examples? | O-types crystal clear; examples are Windows-specific; minimal ambiguity | O-types understandable; examples help; minor ambiguity in edge cases | O-types vague; examples sparse or generic; significant ambiguity |
| **Scoring Guidance** | Are dimension scoring ranges (0–1.0) explicit? | Scoring ranges clear; worked examples show scoring logic; decision points obvious | Scoring ranges stated; some examples; decision points mostly clear | Scoring ranges vague; few/no examples; decision points unclear |
| **Coder Instructions** | Can a practitioner follow §4 instructions without asking for clarification? | Instructions are step-by-step; no gaps; self-contained | Instructions mostly clear; minor questions expected; minor gaps | Instructions require significant clarification; major gaps |
| **Availability Decision Tree** | Is A3 tree (direct evidence vs. inference) easy to apply? | Tree is obvious; practitioners would agree 95% of the time | Tree is workable; ~80% agreement expected; minor calibration | Tree is confusing; high disagreement risk; needs simplification |
| **Operationalization Completeness** | Do A.2–A.7 specs cover all necessary ground? | All boundaries addressed; checklist comprehensive; no major omissions | Most boundaries addressed; checklist mostly complete; minor gaps | Key boundaries missing; checklist incomplete; major gaps |

**Scoring:**

- **5 points** = Excellent (A-level)
- **3–4 points** = Acceptable (B-level)
- **1–2 points** = Weak (C-level, flag for remediation)

**Gap Classification (if rating < 5):**

| Gap Type | Example | Remediation |
|---|---|---|
| **Critical** | "O5 error handling is undefined; coders will diverge" | Rewrite §4.5; add worked examples; retrain coders |
| **Non-Blocking** | "O7 limitation examples could be more diverse" | Expand examples in next version (v1.1); note for future |
| **Minor** | "One typo in O2 explanation" | Fix typo; no methodology impact |

---

### **Question 2: Soundness**

**Full Question:**  
"Are the 12 ACAT-CAL-P dimension definitions conceptually sound for Windows operating system assessment? Do they capture the right aspects of trustworthiness?"

**Assessment Dimensions:**

| Aspect | Rating Criteria | Excellent (A) | Acceptable (B) | Weak (C) |
|---|---|---|---|---|
| **Dimension Relevance** | Does each dimension measure something important for Windows trustworthiness? | All 12 dimensions are essential; removal of any would weaken framework | 11/12 dimensions essential; 1 dimension is marginal | Several dimensions are redundant or irrelevant for Windows |
| **Dimension Overlap** | Do dimensions avoid redundancy while maintaining distinctness? | Minimal overlap; each dimension is independent; coders don't conflate | Some overlap (e.g., Service/Consist); manageable with training | High overlap; coders will systematically confuse dimensions |
| **Domain Coverage** | Do dimensions collectively cover Windows trustworthiness comprehensively? | Framework covers security, reliability, transparency, control, fairness—all critical | Framework covers most areas; 1–2 minor aspects missing | Framework has major blind spots (e.g., privacy, performance) |
| **Definition Clarity** | Is each dimension definition precise and Windows-specific? | Definitions are clear, Windows-contextualized, operationalizable | Definitions are mostly clear; some Windows-specificity needed | Definitions are vague, generic, difficult to operationalize |
| **Alignment with External Standards** | Do dimensions align with NIST RMF, CIS, Microsoft baseline? | Dimension mapping to NIST/CIS/Microsoft is strong (ρ ≥ 0.80 expected) | Dimension mapping is adequate (ρ ≥ 0.70 expected); some quirks | Dimension mapping is weak (ρ < 0.70); significant divergence |

**Scoring:**
- **5 points** = Excellent (A-level)
- **3–4 points** = Acceptable (B-level)
- **1–2 points** = Weak (C-level, flag for remediation)

**Gap Classification (if rating < 5):**

| Gap Type | Example | Remediation |
|---|---|---|
| **Critical** | "Harm dimension is poorly defined; coders scored it inconsistently" | Redefine Harm; provide Windows-specific examples; Layer 1 recode subset |
| **Non-Blocking** | "Service and Syc have minor overlap; clarification in v1.1" | Clarify distinction; update codebook §4; proceed with notation |
| **Minor** | "One dimension could benefit from additional examples" | Add examples; minor documentation update |

---

### **Question 3: Fairness**

**Full Question:**  
"Does the codebook and self-assessment methodology avoid systematic bias? Are coders equally rigorous on favorable vs. unflattering elements? Do they avoid over-scoring or under-scoring specific dimensions?"

**Assessment Dimensions:**

| Aspect | Rating Criteria | Excellent (A) | Acceptable (B) | Weak (C) |
|---|---|---|---|---|
| **Valence Bias Detection** | Did coders systematically over/under-score favorable vs. unflattering elements? | κ per valence is uniform (≥0.60 all); no systematic bias detected | κ per valence mostly uniform; minor bias (Δ κ < 0.10); acceptable | κ per valence diverges widely (Δ κ > 0.15); systematic bias detected |
| **Dimension Bias Detection** | Did coders systematically over/under-score specific dimensions? | Dimension score distributions are uniform; no dimension systematically high/low | Most dimensions uniform; 1 dimension slightly high/low (within 0.05); OK | Multiple dimensions show systematic bias (> 0.10 from mean) |
| **Double-Coding Coverage** | Was double-coding sufficient to catch coder disagreement? | ≥20% overall; ≥30% of inference elements; strategic placement (high-risk cells) | 15–20% overall; 25–30% inference; mostly strategic | < 15% overall; < 25% inference; insufficient coverage |
| **Agreement Reconciliation** | When coders disagreed, was reconciliation fair and principled? | Reconciliation process documented; resolved to consensus; no favoritism | Reconciliation mostly fair; minor instances of one coder dominating | Reconciliation process unclear; appears biased toward lead auditor |
| **Stopping Rules** | Were stopping rules (ρ monitor, CI-width monitor, breach trigger) properly armed and applied? | Stopping rules armed; monitored; no threshold breaches that went unaddressed | Stopping rules mostly monitored; 1 threshold breach with documentation | Stopping rules inadequately monitored; breaches unaddressed |

**Scoring:**
- **5 points** = Excellent (A-level)
- **3–4 points** = Acceptable (B-level)
- **1–2 points** = Weak (C-level, flag for remediation)

**Gap Classification (if rating < 5):**

| Gap Type | Example | Remediation |
|---|---|---|
| **Critical** | "Service dimension systematically scored 0.10+ higher than other dimensions" | Retrain on Service definition; Layer 1 recode Service elements |
| **Non-Blocking** | "Unflattering elements were double-coded at 18% instead of planned 20%; small gap" | Acceptable with notation; increase to 20% on next assessment |
| **Minor** | "One reconciliation decision favored lead auditor; minor impact" | Document; use consensus-building approach going forward |

---

### **Question 4: Validity**

**Full Question:**  
"Do the Layer 1 self-assessment results (coherence ≥0.85) and Layer 2 external validation results (ρ ≥0.70) accurately reflect Windows operating system trustworthiness? Are the scores defensible and meaningful?"

**Assessment Dimensions:**

| Aspect | Rating Criteria | Excellent (A) | Acceptable (B) | Weak (C) |
|---|---|---|---|---|
| **Result Credibility** | Are the Windows dimension scores (e.g., Truth 0.89, Service 0.87) believable? | Scores align with real Windows behavior; examples support scores | Scores seem roughly right; some scores could be higher/lower (±0.05) | Scores appear inflated or deflated significantly; don't match reality |
| **Coherence Score Defensibility** | Is coherence ≥0.85 justified by dimension scores and evidence? | Coherence follows logically from dimension scores; well-supported | Coherence is justified; some dimensions could justify different aggregate | Coherence appears inflated; averaging masks weak dimensions |
| **Layer 2 Alignment** | Do Layer 2 external validation results (NIST/CIS/Microsoft) reinforce Layer 1 conclusions? | ρ ≥0.70 all three; external frameworks validate self-assessment | ρ ≥0.70 all three; minor divergences documented and explained | ρ <0.70 somewhere; external frameworks contradict self-assessment |
| **Stratification Analysis** | Does stratification (O-type, valence, availability) show balanced coverage with no blind spots? | Stratification is balanced; no over/under-representation; coverage is complete | Stratification mostly balanced; minor imbalances acceptable | Stratification shows systematic gaps; one O-type or valence under-represented |
| **Evidence Quality** | Is Layer 1 evidence (element sourcing, rationale, citations) of high quality? | Evidence is rich, specific, traceable to sources; easy to verify | Evidence is adequate; some citations could be more precise | Evidence is sparse or vague; difficult to verify; questionable sourcing |

**Scoring:**
- **5 points** = Excellent (A-level)
- **3–4 points** = Acceptable (B-level)
- **1–2 points** = Weak (C-level, flag for remediation)

**Gap Classification (if rating < 5):**

| Gap Type | Example | Remediation |
|---|---|---|
| **Critical** | "Coherence ≥0.85 appears inflated; Truth and Power are 0.89 but Humility is 0.74; averaging masks weakness" | Investigate why Humility is low; add to Phase 2.6 red-team focus |
| **Non-Blocking** | "One dimension (Syc) supported by fewer elements; non-critical; acceptable" | Note for K8s v1.6 pilot; increase Syc element count if possible |
| **Minor** | "One element citation could be more specific; minor documentation issue" | Update element documentation; no methodology impact |

---

### **Question 5: Gaps**

**Full Question:**  
"Are there critical dimensions, operation types, or aspects of Windows trustworthiness that the ACAT-CAL-P framework omits? What is missing?"

**Assessment Dimensions:**

| Aspect | Rating Criteria | Excellent (A) | Acceptable (B) | Weak (C) |
|---|---|---|---|---|
| **Dimension Completeness** | Are all critical trustworthiness dimensions included in the 12 dimensions? | All critical dimensions present; optional v1.6 dimensions identified for future | 11/12 critical dimensions; one marginal gap noted for v1.6 | Several critical dimensions missing; gaps affect assessment validity |
| **Operation Type Coverage** | Do O1–O7 boundary units capture the full scope of Windows behavior? | O1–O7 cover all major behavior categories; completeness verified | O1–O7 cover 90%+ of behavior; minor gaps acceptable (e.g., edge cases) | O1–O7 miss major behavior categories; significant coverage gaps |
| **Windows-Specific Context** | Does the framework account for Windows-specific constraints, architecture, threats? | Framework is highly Windows-contextualized; POSIX/macOS differences acknowledged | Framework addresses most Windows specifics; minor gaps (e.g., legacy APIs) | Framework is generic; insufficient Windows-specific grounding |
| **Emerging Concerns** | Are emerging security/reliability concerns (e.g., supply chain, AI, quantum) addressed? | Framework can accommodate emerging concerns; extensibility clear | Framework addresses current concerns; limited extensibility for future | Framework is outdated; doesn't account for emerging threats |
| **Stakeholder Perspectives** | Does the framework capture different stakeholder needs (end-user, admin, developer, security, compliance)? | Framework implicitly serves all stakeholders; v1.6 explicit perspectives planned | Framework mostly serves technical stakeholders; non-technical perspectives underweighted | Framework heavily biased to one stakeholder (e.g., security only) |

**Scoring:**
- **5 points** = Excellent (A-level); all gaps are optional (v1.6 enhancements)
- **3–4 points** = Acceptable (B-level); 1–2 non-critical gaps noted
- **1–2 points** = Weak (C-level); critical gaps that affect validity

**Gap Classification:**

| Gap Type | Example | Remediation |
|---|---|---|
| **Critical** | "Framework doesn't assess supply chain security (driver signing, update integrity); critical for Windows" | Add O8 operation type (supply chain operations); extend v1.6 |
| **Non-Critical v1.6** | "Resilience, Stakeholder Perspective, Temporal Consistency are missing; identified for v1.6" | Plan v1.6 enhancements; proceed with v1.5; note for K8s pilot |
| **Minor** | "Legacy API compatibility could have its own dimension; rare in modern Windows" | Consider for v1.7; acceptable to defer |

---

## PART III: EVALUATOR MATERIALS

Evaluator receives **five documents**:

1. **ACAT_CAL_P_WINDOWS_v1_0_DRAFT_CODEBOOK.md** (Full §1–§12 codebook)
   - Operationalization (§1–§3)
   - Coder instructions (§4 with worked examples)
   - Protocols (§5–§7)
   - Layer 1–4 skeletons

2. **WINDOWS_LAYER_1_SELF_ASSESSMENT_RESULTS.md** (Layer 1 output, when ready)
   - Coherence score + per-dimension scores
   - Stratification analysis
   - Sample codings (8–10 fully documented)
   - Inter-rater κ agreement statistics

3. **WINDOWS_LAYER_2_NIST_RMF_ALIGNMENT_VALIDATION.md** (Layer 2 output, when ready)
   - ρ correlations (NIST, CIS, Microsoft)
   - Dimension scores across frameworks
   - Divergence investigation results (if any)

4. **Evaluator Briefing Memo** (This document, Part IV below)
   - Five-question assessment framework
   - Rating scale
   - Gap classification
   - Timeline and deliverables

5. **Windows Context Document** (Provided by humanaios)
   - Windows 11 + Server 2022 security landscape
   - Known trustworthiness concerns
   - Prior security research
   - Relevant standards (NIST CSF, CIS, Microsoft baseline)

---

## PART IV: EVALUATION PROCESS

### **Phase 1: Document Review (Days 1–2)**

**Evaluator Activities:**
1. Read codebook (§1–§7) thoroughly
2. Review Layer 1 results (120 elements, coherence score, κ agreement)
3. Review Layer 2 results (ρ correlations, blended scores)
4. Take notes on initial impressions

**Deliverable:** Notes on clarity, soundness, fairness, validity, gaps (unpolished)

---

### **Phase 2: Deep Dive Assessment (Days 3–4)**

**For Each of Five Questions:**
1. Re-read relevant sections of codebook + results
2. Score using 5-point scale (5=Excellent, 3–4=Acceptable, 1–2=Weak)
3. Document evidence supporting score
4. Classify any gaps (critical/non-blocking/minor)
5. Recommend remediation

**Deliverable:** Detailed notes with scoring rationale for each question

---

### **Phase 3: Risk Assessment (Day 5)**

**Evaluator Synthesizes:**
1. Identify most critical finding (if any)
2. Assess whether findings block Layer 4 red-team testing
3. Recommend: Proceed, Proceed with Notation, Halt for Remediation
4. Prioritize remediation (critical first, then non-blocking, then minor)

**Deliverable:** Risk summary and recommendation

---

### **Phase 4: Report Writing (Day 6–7)**

**Evaluator Drafts:**
- Executive summary (1 page)
- Five-question assessment (5 pages, 1 per question)
- Gap analysis and remediation plan (2 pages)
- Final recommendation and sign-off (1 page)

**Deliverable:** WINDOWS_LAYER_3_EVALUATOR_CROSS_VALIDATION_REPORT.md (10–12 pages)

---

## PART V: RATING SCALE

### **Overall Rating (A/B/C)**

**A: Strong**
- All five questions scored 4–5 points
- 0 critical gaps
- Framework is sound; Layer 1–2 results are credible
- **Recommendation:** ✓ PROCEED to Layer 4 red-team testing
- Z2 approval: Automatic (A-rating has no blockers)

**B: Acceptable**
- Questions averaged 3–4 points
- 0–2 critical gaps; if any, remediation plan in place
- Framework has minor issues; Layer 1–2 results credible with notation
- **Recommendation:** PROCEED with notation (document all gaps; flag for v1.6)
- Z2 approval: Conditional on remediation completion

**C: Weak**
- Questions averaged <3 points
- ≥3 critical gaps OR systemic validity issues
- Framework has serious flaws; Layer 1–2 results questionable
- **Recommendation:** ✗ HALT; remediate before Layer 4
- Z2 approval: Rejected; escalation required

---

## PART VI: GAP CLASSIFICATION

### **Critical Gaps** (Block Layer 4 or affect results validity)

Examples:
- Dimension is poorly defined; coders diverged systematically
- Coherence score appears inflated; averaging masks weak dimensions
- Stratification shows major gaps; one operation type under-represented
- External validation (Layer 2) shows poor alignment (ρ < 0.70); frameworks diverge significantly

**Remediation:**
- Halt Layer 4 until fixed
- Retrain coders or recode subset of elements
- Update codebook; clarify definition
- Escalate to Z2 if systemic (affects Windows v1.5 validity)

### **Non-Blocking Gaps** (Noted for v1.6, don't halt Layer 4)

Examples:
- "Resilience, Stakeholder Perspective, Temporal Consistency identified for v1.6" (expected)
- "O7 limitation examples could be more diverse" (minor enhancement)
- "One dimension could use more examples" (documentation improvement)

**Remediation:**
- Document in findings
- Include in v1.6 roadmap
- Proceed to Layer 4 with notation

### **Minor Gaps** (Cosmetic, no methodology impact)

Examples:
- Typo in codebook
- One element citation could be more specific
- One reconciliation decision could have been documented better

**Remediation:**
- Fix in next documentation update
- No impact on Layer 4 or Windows v1.5 validity

---

## PART VII: SAMPLE EVALUATION

### **Scenario: Evaluator Assesses Completed Layers 1–2**

**Layer 1 Input (Expected Results):**
- 120 elements coded
- Coherence: 0.86 (exceeds 0.85 gate)
- κ overall: 0.64 (exceeds 0.60 gate)
- Per-dimension scores: Truth 0.89, Service 0.87, Harm 0.88, ... Handoff 0.85
- Stratification: Balanced across O-types, valence, availability
- Sample codings provided with full rationale

**Evaluator Assessment:**

### **Question 1: Accessibility (Scenario Evaluation)**

**Evaluator Notes:**
- O1–O7 definitions are clear with Windows-specific examples ✓
- Scoring guidance in §4 includes 2 worked examples (O1-FAV-001, O3-UNFLAT-008) — helps ✓
- Availability decision tree (A3) is straightforward; practitioners would likely agree 85%+ ✓
- A.7 checklist is comprehensive; minor omissions acceptable
- One O5 instruction could be slightly more explicit (how to generate disk-full error)

**Scoring:** 4 points (Acceptable, not Excellent)

**Gap:** Non-blocking — O5 error generation could have one more detail; acceptable with notation

---

### **Question 2: Soundness**

**Evaluator Notes:**
- 12 dimensions are well-chosen; all relevant to Windows trustworthiness ✓
- Minimal overlap (some Service/Consist distinction could be sharper; manageable)
- Coverage: Security (Harm, Power, Fair), Reliability (Service, Consist, Syc), Transparency (Scheme, Humility), Control (Autonomy, Value), Accountability (Handoff, Truth) — comprehensive
- Definitions are mostly Windows-specific; some generic elements acceptable
- Layer 2 external validation shows ρ ≥ 0.70 all three frameworks; dimension mapping is sound ✓

**Scoring:** 4 points (Acceptable)

**Gap:** Non-blocking — Service/Consist distinction could be tightened; minor clarification acceptable

---

### **Question 3: Fairness**

**Evaluator Notes:**
- κ per valence: Favorable 0.66, Neutral 0.62, Unflattering 0.58 (variation ≤ 0.08; acceptable, slight bias toward unflattering elements has higher disagreement, expected)
- Dimension score distributions: Mostly uniform; no systematic bias detected ✓
- Double-coding: 24 of 120 = 20% (meets ≥20% floor); coverage appears strategic (inference elements, low-agreement O-types)
- Reconciliation process documented; appears fair
- Stopping rules monitored daily; ρ tracker shows no threshold breaches ✓

**Scoring:** 5 points (Excellent)

**Gap:** None critical; fair assessment process

---

### **Question 4: Validity**

**Evaluator Notes:**
- Windows scores seem defensible: Truth 0.89 (BitLocker, UAC work well) ✓, Harm 0.88 (Defender + mitigations strong), Humility 0.84 (some limitations underdisclosed) ✓
- Coherence 0.86 follows logically from dimension scores; no single dimension is severely weak ✓
- Layer 2 validation (ρ 0.83 NIST, 0.81 CIS, 0.77 Microsoft) reinforces conclusions ✓
- Stratification is balanced: 20 O1 elements, 18 O2 elements, ... 12 O7 elements; valence distribution is even; availability split is reasonable
- Evidence quality: Elements are sourced clearly; examples are specific (e.g., "UAC prompt appears when running admin command as standard user")

**Scoring:** 5 points (Excellent)

**Gap:** None; validity is well-established

---

### **Question 5: Gaps**

**Evaluator Notes:**
- Dimensions: 12 core dimensions are comprehensive; v1.6 additions (Resilience, Stakeholder Perspective, Temporal Consistency) identified and planned ✓
- Operation types: O1–O7 cover major Windows behavior; O8 (supply chain/driver signing) and O9 (version changes) planned for v1.6 ✓
- Windows-specific: Framework is highly contextualized; POSIX/macOS differences clear
- Emerging concerns: Supply chain (driver signing) and firmware (Secure Boot) addressed within existing dimensions; can be enhanced in v1.6
- Stakeholders: Framework implicitly serves all (end-users via O1, admins via O2/O6, developers via O4, security via Harm/Power); v1.6 explicit perspectives planned ✓

**Scoring:** 5 points (Excellent)

**Gap:** None critical; expected enhancements are v1.6 features (Resilience, Stakeholder, Temporal)

---

### **Overall Evaluation Result**

| Question | Score | Finding |
|---|---|---|
| 1. Accessibility | 4 | Acceptable (minor O5 enhancement noted) |
| 2. Soundness | 4 | Acceptable (Service/Consist distinction could be tighter) |
| 3. Fairness | 5 | Excellent (fair process, well-documented) |
| 4. Validity | 5 | Excellent (credible results, strong evidence) |
| 5. Gaps | 5 | Excellent (gaps identified and planned for v1.6) |
| **Overall** | **4.6/5** | **A (Strong)** |
| **Critical Gaps** | 0 | None |
| **Recommendation** | ✓ PROCEED | Layer 4 red-team testing; Z2 approval automatic |

---

## PART VIII: EVALUATOR DELIVERABLE

### **WINDOWS_LAYER_3_EVALUATOR_CROSS_VALIDATION_REPORT.md**

**Structure (10–12 pages):**

1. **Executive Summary (1 page)**
   - Overall rating (A/B/C)
   - Key findings (3–5 bullets)
   - Critical gaps (if any)
   - Recommendation (Proceed/Conditional/Halt)

2. **Question 1: Accessibility (1 page)**
   - Score + rationale
   - Strengths (what's clear)
   - Gaps (what needs clarification)
   - Remediation (if critical)

3. **Question 2: Soundness (1 page)**
   - Score + rationale
   - Dimension assessment
   - Overlap analysis
   - Remediation (if critical)

4. **Question 3: Fairness (1 page)**
   - Score + rationale
   - Bias detection findings
   - Double-coding assessment
   - Remediation (if critical)

5. **Question 4: Validity (1 page)**
   - Score + rationale
   - Result credibility assessment
   - Layer 2 alignment confirmation
   - Remediation (if critical)

6. **Question 5: Gaps (1 page)**
   - Score + rationale
   - Missing dimensions/operations
   - Stakeholder coverage
   - Remediation (if critical)

7. **Synthesized Risk Assessment (1 page)**
   - Most critical finding (if any)
   - Impact on Layer 4 red-team testing
   - Impact on Windows v1.5 validity
   - Recommendation

8. **Remediation Plan (1–2 pages)**
   - Critical gaps with remediation steps and owners
   - Non-blocking gaps with v1.6 timing
   - Timeline for critical fixes (before Layer 4? or after?)

9. **Final Recommendation & Sign-Off (1 page)**
   - Z2 approval: Approved / Approved with conditions / Rejected
   - Next steps
   - Evaluator signature + date

---

## PART IX: EVALUATION TIMELINE

| Date | Activity | Owner | Deliverable |
|---|---|---|---|
| **2026-10-19** | Evaluator briefing; receive materials | Evaluator | Confirms understanding; starts reading |
| **2026-10-20–10-21** | Document review (codebook, L1 results) | Evaluator | Notes on clarity, soundness |
| **2026-10-22–10-23** | Deep dive assessment (five questions) | Evaluator | Scoring rationale (draft) |
| **2026-10-24** | Risk assessment + synthesis | Evaluator | Risk summary, recommendation |
| **2026-10-25** | Report writing | Evaluator | REPORT ready for delivery |
| **2026-10-26** | Z2 reviews report | Z2 authority | Approval decision |

---

## PART X: EVALUATOR READINESS CHECKLIST

### **Evaluator Qualifications**
- [ ] SANS certification (Security, Windows focus) OR ISO 27001 lead auditor certification
- [ ] ≥5 years Windows security expertise
- [ ] Familiar with NIST RMF 1.0, CIS Benchmarks, Microsoft Security Baseline
- [ ] NOT involved in Layers 1–2 (independence verified)
- [ ] Conflict of interest check passed (not humanaios employee, no financial interest)

### **Materials Received**
- [ ] ACAT_CAL_P_WINDOWS_v1_0_DRAFT_CODEBOOK.md (§1–§7 + skeletons)
- [ ] WINDOWS_LAYER_1_SELF_ASSESSMENT_RESULTS.md (120 elements, coherence, κ, samples)
- [ ] WINDOWS_LAYER_2_NIST_RMF_ALIGNMENT_VALIDATION.md (ρ, framework alignment, blended scores)
- [ ] This evaluation framework (Five-question assessment)
- [ ] Windows context document (threat landscape, standards, prior research)

### **Timeline Confirmed**
- [ ] Week 7 availability confirmed (2026-10-19 to 2026-10-25)
- [ ] Full-time availability (40+ hours for thorough assessment)
- [ ] Report delivery deadline: 2026-10-25 (EOD)

### **Communication Setup**
- [ ] Evaluator contact information recorded (email, phone)
- [ ] Lead auditor assigned as point of contact (non-evaluator)
- [ ] Question escalation path clear (if evaluator needs clarification)
- [ ] Z2 governance on standby for approval decision

### **Go/No-Go Decision**
- [ ] All items above checked
- [ ] Evaluator confirms readiness
- [ ] Lead auditor confirms materials are complete
- [ ] **PROCEED with Layer 3 evaluation (2026-10-19)**

---

## PART XI: POST-EVALUATION ACTIONS

### **If Rating = A (Strong)**
1. ✓ Proceed to Layer 4 red-team testing (Week 7–9)
2. ✓ Z2 approval: Automatic (no blockers)
3. ✓ Document findings for v1.6 roadmap (non-critical gaps)

### **If Rating = B (Acceptable)**
1. ⚠ Proceed to Layer 4 with notation
2. ⚠ Z2 approval: Conditional on remediation of critical gaps (if any)
3. ⚠ Timeline: Critical gaps fixed before Layer 4 start, OR proceed and note for Layer 5
4. ⚠ Document non-blocking gaps for v1.6

### **If Rating = C (Weak)**
1. ✗ HALT Layer 4
2. ✗ Z2 escalation: Rejection; requires remediation before Layer 4
3. ✗ Timeline: Fix critical gaps; pass re-evaluation before Layer 4 allowed
4. ✗ Document systemic issues; assess whether Windows v1.5 is viable

---

## SUMMARY

**Layer 3 Evaluator Assessment** is a **1-week independent review** of Windows codebook and Layers 1–2 results using a **five-question framework**:

1. **Accessibility:** Is operationalization clear to independent practitioners?
2. **Soundness:** Are dimension definitions correct?
3. **Fairness:** Does methodology avoid systematic bias?
4. **Validity:** Do results reflect real Windows trustworthiness?
5. **Gaps:** What critical dimensions/operations are missing?

**Output:** WINDOWS_LAYER_3_EVALUATOR_CROSS_VALIDATION_REPORT.md (10–12 pages) with overall rating (A/B/C), gap classification (critical/non-blocking/minor), and recommendation (Proceed/Conditional/Halt).

**Gate:** Rating A (Strong) with 0 critical gaps → Proceed to Layer 4 red-team testing.

---

**WINDOWS LAYER 3 FRAMEWORK: READY FOR DEPLOYMENT**  
**Awaiting:** Layer 1–2 results completion (Layer 2 due 2026-10-19)  
**Duration:** Week 7 (2026-10-19 to 2026-10-25)  
**Owner:** Independent security auditor (SANS-cert, external preferred)  
**Gate:** Rating A with 0 critical gaps  
**Next Phase:** Phase 2.6 (Layer 4 Red-Team Stress Tests)

Wado. 🦅
