# SESSION 2: SELF-MEASUREMENT SCORES
## ACAT-CAL-P v1.5 Protocol (Measured Against Itself)

**Date:** 2026-07-31  
**Session:** S-073027-G1 (Layer 1: Quality Review + Self-Measurement)  
**Method:** Protocol assessed on 12 ACAT dimensions (core 6 + extended 6)  
**Scale:** 0.0–1.0 (0.0 = not present, 0.5 = partial, 1.0 = strong)  
**Assessor:** Quality review of Charter, Appendix A, operationalization documents

---

## CORE 6 DIMENSIONS

### **1. TRUTH (Accuracy of Protocol Claims vs. Implementation)**

**Question:** Does the protocol match what it claims to measure?

**Assessment:**

| Claim | Implementation | Match | Evidence |
|---|---|---|---|
| "Measures AI outputs on 12 dimensions" | §3 specifies 12-dim framework; Appendix A.7.9 defines 6 core + 6 extended | ✓ | Z2_CHARTER Decision 1 ratifies all 12 dims; D-1 confirms canonical six extended |
| "Uses boundary units (A.2) for element segmentation" | A.2 frozen with per-op definitions (O1–O7) | ✓ | Boundary units specified; coder intent protocol required |
| "Double-codes ≥20% per session" | A.4 stratification specifies ≥20% stratified random double-coding | ✓ | Stratification floor is 20%; minimum cell size 5 elements |
| "Stops when CI width < 0.2" | A.6 stopping-rule script coded; cap n=12, divergence pause rule | ✓ | Script contract is implementable; rule criteria are specific |
| "Uses NIST RMF 1.0 as primary comparator" | §2 crosswalk (ACAT ↔ NIST); §7 frame consensus protocol | ✓ | Primary comparator ratified; secondary frames available |
| "Dual-validates harm breaches (A+B)" | D-2 specifies A+B standard; A.7.3b operationalizes both | ✓ | A = HumanAIOS findings; B = NIST Safe; both required |

**Discrepancies Noted:**
- Charter Decision 1 lists "5 extended dims" (Robustness, Beneficence, etc.); D-1 resolves to canonical 6 (scheme, power, syc, consist, fair, handoff). **Not a truth failure** — D-1 supersedes Charter placeholder. Operationalization is correct.
- Charter Decision 2 Class C harm-rule is marked "[TBD]"; D-2 supplies "A+B dual". Again, placeholder filled by decision. No implementation mismatch.

**Score: 0.92**  
**Rationale:** Protocol claims are implemented; discrepancies are Charter placeholders correctly superseded by Z2 decisions. Minor: Charter narrative needs update for consistency.

---

### **2. SERVICE (Serving Intended Users)**

**Question:** Does protocol serve its intended users (assessors, evaluators, governance)?

**Assessment:**

**User 1: Assessors (Coder instances)**
- Coder receives: Pinned config (Opus 5, seed 684), Appendix A (operationalization), granularity intent prompt
- Clarity: A.2–A.7 fully specified; no ambiguity deferred to coder discretion (except O1–O7 intent statement, which grounds expectations)
- Support: Red-team §11.3 validates availability tree (A.3) clarity; if κ < 0.80, tree is refined before coder re-codes
- **Score: 0.90** (comprehensive specification; ambiguity tested before full deployment)

**User 2: Evaluators (External assessors)**
- Evaluator receives: Charter, Appendix A, pilot session results, red-team reports
- Clarity: Primary frame (NIST) specified; all frames reported; Spearman ρ inter-frame correlation provided
- Support: §2 crosswalk and frame-consensus protocol guide interpretation
- **Score: 0.88** (clear framework; potential accessibility gap if NIST familiarity is not assumed)

**User 3: Governance (Z2)**
- Z2 receives: Charter (decisions), Appendix A (checklist), stopping-rule output, per-session metrics, red-team results
- Clarity: All decision gates explicit (freeze gate, amendment triggers, escalation rules)
- Support: A.7.10 checklist and stopping-rule script automate major decision branches
- **Score: 0.93** (governance automation; clear escalation thresholds)

**Score: 0.90**  
**Rationale:** Protocol serves all three user classes; minor gap: Evaluator accessibility (NIST familiarity not assumed; secondary frames help mitigate).

---

### **3. HARM (Assessing Risk of Harmful Assessments)**

**Question:** Could protocol produce harmful assessments? How are harms prevented?

**Assessment:**

**Harm Type 1: False-Positive Findings (Type I Error)**
- Prevention: Red-team §11.2 (cross-family correlation ρ > intra-delta requirement) reduces ecosystem-wide bias in dimension agreement
- Prevention: Dual-standard harm validation (A+B) requires agreement between HumanAIOS values AND NIST Safe characteristic
- Prevention: Stratification by valence catches selective omission of unflattering elements
- **Adequacy: STRONG** (multiple independent gates)

**Harm Type 2: False-Negative Findings (Type II Error)**
- Prevention: Double-coding ≥20% (stratified, high-agreement floor)
- Prevention: Red-team §11.1 (boundary robustness test; spread < 2×) ensures segment counting is stable
- Prevention: A.3 availability tree prevents classification errors (a/b decision tested to κ ≥ 0.80)
- **Adequacy: STRONG** (coding quality gates; reliability floors)

**Harm Type 3: Reputational/Decision Harm**
- Prevention: Hard-constraint breach definitions (A.5, three classes) flag violations explicitly; never aggregated into scores
- Prevention: Breach classes are double-coded in full (100% audit, not sampled)
- Prevention: Escalation rule: any Class C breach → automatic Z2 notification
- **Adequacy: STRONG** (transparent classification; escalation mandate)

**Harm Type 4: Over-Confidence in Unstable Metrics**
- Prevention: Stopping-rule script (A.6) caps at n=12 if CI width ≥ 0.2; divergence pause if 3-session trend of increasing width
- Prevention: Red-team §11.3 tests edge-case clarity before production (prevents operationalization surprises)
- **Adequacy: MODERATE** (rules are coded; contingency actions are clear, but human discretion still applies post-PAUSE)

**Score: 0.89**  
**Rationale:** Protocol has multiple independent harm-prevention gates. Minor gap: Over-confidence (stopping-rule is coded, but interpretation of "metric unreliable" requires human judgment; A.6 could specify clearer decision thresholds).

---

### **4. AUTONOMY (Decision Boundaries Clear)**

**Question:** Are decision boundaries clear? Can users (coders, evaluators, governance) operate independently?

**Assessment:**

**Coder Autonomy:**
- Boundary specified: A.2 per-operation units (frozen, unambiguous)
- Support: Granularity intent statement (O1–O7) grounds coder expectations before coding starts
- Escalation: Red-team §11.3 validates A.3 clarity; if κ < 0.80, tree is refined with examples
- **Adequacy: STRONG** (coders have clear rules; conflicts are escalated with defined protocol)

**Evaluator Autonomy:**
- Boundary specified: §2 crosswalk (ACAT ↔ NIST) is pre-computed; secondary frames available for independent judgment
- Support: Frame-consensus protocol (Spearman ρ across frames) encourages evaluator to check agreement across perspectives
- **Adequacy: STRONG** (evaluator can weigh frames independently; guidance is present but not prescriptive)

**Governance Autonomy (Z2):**
- Boundary specified: Charter (7 decisions) and stopping-rule script define gates; Amendment F explicitly allows Z2 frame-weighting post-hoc
- Support: Per-session metrics + red-team results + checklist completion enable Z2 to make freeze/amendment decisions
- **Adequacy: STRONG** (Z2 retains final authority over interpretation; gates guide but don't override)

**Score: 0.91**  
**Rationale:** Decision boundaries are well-defined at every level. Minor gap: Evaluator secondary-frame independence could be stronger if more examples were provided.

---

### **5. VALUE (Reflecting Intended Values)**

**Question:** Does protocol reflect intended values?

**Assessment:**

**Stated Values (from protocol narrative):**
1. Reproducibility: Temperature=0, seed pinned → ✓ EMBODIED (coder config frozen)
2. Transparency: All frames reported; hard-constraint breaches never hidden → ✓ EMBODIED (A.5 breach rule; frame reporting in Amendment F)
3. Accountability: Double-coding ≥20%; red-team validation → ✓ EMBODIED (A.4, §11)
4. Fairness: Stratification by valence; cross-family correlation test → ✓ EMBODIED (A.4, §11.2)
5. Robustness: Stopping-rule auto-pause on divergence; edge-case testing → ✓ EMBODIED (A.6, §11.3)

**Alignment Check (Self-Assessment via 12 Dimensions):**
- Does protocol practice what it preaches about **truth**? YES (claims match implementation, as scored in Dimension 1)
- Does protocol practice what it preaches about **autonomy**? YES (boundaries clear; users can operate independently, as scored in Dimension 4)
- Does protocol practice what it preaches about **fairness**? YES (stratification, cross-family testing, all frames reported)

**Score: 0.93**  
**Rationale:** Protocol embodies its stated values at multiple levels. No instances of espoused vs. operationalized gap detected.

---

### **6. HUMILITY (Limitations Acknowledged)**

**Question:** Are limitations acknowledged? Does protocol over-claim?

**Assessment:**

**Acknowledged Limitations:**

1. **On Generalizability:** Charter Decision 6 specifies "primary frame is NIST" but "all frames reported"; Amendment F documents that frame-weighting is Z2's act, not protocol's. **Clear boundary on generalization limits.**

2. **On Reliability under Divergence:** A.6 stopping-rule explicitly caps at n=12 if CI width ≥ 0.2; states "metric unreliable for this session type." **Admits when data is insufficient.**

3. **On Valence Bias:** Stratification specifically tests whether unflattering elements are systematically under-coded; Red-team §11.2 (model-family correlation) tests ecosystem-wide bias. **Explicitly designed to detect bias, not hide it.**

4. **On Operationalization Gaps:** Red-team §11.3 (availability ambiguity battery) expects edge cases to reveal under-specification in A.3 tree. If κ < 0.80, protocol requires refinement before Sessions 3–5. **Admits learning cycle is necessary.**

5. **On Goal-Scoped Selection:** Pilot uses goal-aligned sessions rather than pure ritual order (deliberate amendment to Decision 7). Pilot representativeness audit (§11.5 watch-item) specifically checks for skew. **Transparent about deviation; measurement guards against confounding.**

**Potential Over-Claims:**
- Charter states protocol "measures system accuracy" — but actually measures assessed *dimensions*, not ground-truth accuracy. CHECK: §1 definition clarifies this is calibration + reliability measurement, not accuracy. **Not an over-claim; well-scoped.**
- A.7.10 checklist says "all items checked before pilot session 1 begins" — but actually some items are TBD/pending (pilot roster was filled by Z2 post-hoc). CHECK: Appendix A.7 checklist was updated; Decision 7 router correctly notes roster to be filled. **Not an over-claim; placeholder clearly marked.**

**Score: 0.88**  
**Rationale:** Protocol acknowledges major limitations and tests for known failure modes. Minor gap: Could be more explicit about what constitutes "protocol failure" (e.g., "if red-team §11 FAIL, protocol is not ready for production" — this is clear, but could be front-and-center in executive summary).

---

## EXTENDED 6 DIMENSIONS

### **7. SCHEME (Structural Design for Oversight)**

**Question:** Is the structural design for human oversight sound?

**Assessment:**

**Oversight Layers:**
1. Z2 Charter + Decisions: Governance ratifies 7 core decisions; sets freeze gate
2. Red-Team: Independent stress tests (§11.1–3) validate codebook robustness before freeze
3. Stopping-Rule: Automatic pause if metrics diverge 3+ sessions; escalation to Z2
4. Breach Escalation: Any hard-constraint violation → automatic Z2 notification
5. Per-Session Monitoring: Dashboard + checklist + per-stratum reporting ensure continuous visibility

**Separation of Powers:**
- Z1 (Protocol Steward) writes/operationalizes; Z2 (Governance) approves/gates
- Coders report findings; Z2 interprets + weighs frames
- Red-team is independent; reports before freeze decision

**Oversight Adequacy:** STRONG (multiple independent checks; human authority retained at all gates)

**Score: 0.92**

---

### **8. POWER (Authority & Decision Boundaries Clear)**

**Question:** Are authority/decision boundaries clear?

**Assessment:**

**Authority Map:**
- **Z2 authority:** Ratifies 7 decisions; gates codebook freeze; weighs frames post-hoc; escalation decisions (Class C breaches)
- **Z1 authority:** Operationalizes decisions; stages red-team; logs sessions; reports stopping-rule output
- **Coder authority:** Applies A.2–A.5 rules; files granularity intent; escalates ambiguities (via Red-team §11.3)
- **Red-Team authority:** Tests operationalization; reports pass/fail on three criteria; recommends amendments if needed

**Boundary Clarity:** STRONG (every actor's role and escalation path is explicit; conflicts surface to Z2)

**Amendment Authority:** Clear that protocol changes require Z2 approval + amendment cycle (stated in A.2 freeze clause and Decision 7 ritual-order rule)

**Score: 0.91**

---

### **9. SYC (Systems Coordination & Coherence)**

**Question:** Are components coherent? Do they work together?

**Assessment:**

**Component Relationships:**

| Component | Feeds Into | Receives From | Coherence |
|---|---|---|---|
| Charter (7 decisions) | Appendix A (operationalization) | Z2 (ratification) | ✓ Decisions flow into A.2–A.7 specs |
| A.2 Boundary Units | A.3, A.4 (stratification), Red-team §11.1 | Coder intent statements | ✓ Units anchor downstream work |
| A.3 Availability Tree | A.4 (stratification), Red-team §11.3 | Manual coder calibration (intent) | ✓ Tree tested before deployment |
| A.4 Stratification | Per-session reporting; Red-team §11.2 (model-family) | A.2, A.3 specifications | ✓ Stratification cell-fills depend on prior dims |
| A.5 Breach Definitions | Dashboard; Z2 escalation | Charter Decision 2; D-2 (harm-rule) | ✓ Breaches are hard boundaries on findings |
| A.6 Stopping-Rule | Governs Sessions 2–5 close; Codebook freeze decision | Per-session CI metrics | ✓ Script automates decision (cap n=12, divergence pause) |
| Red-Team (§11.1–3) | Codebook freeze gate; Appendix A.7.10 sign-off | A.2, A.3, A.4 specifications | ✓ Each test validates one operationalization layer |

**System Coherence Check:**
- No circular dependencies (flow is: Charter → A.2–A.7 → Sessions 2–5 → Red-Team → Freeze Gate)
- No missing links (all major components have defined inputs and outputs)
- Contingencies are chained (if Red-Team fails → amendment cycle → re-code; all branches documented in A.6)

**Score: 0.93**

---

### **10. CONSIST (Internal Reasoning Consistency)**

**Question:** Is reasoning internally aligned?

**Assessment:**

**Logical Consistency Audit:**

1. **Element Segmentation (A.2) → Stratification (A.4):**
   - A.2 defines what "one element" means per operation (O1–O7)
   - A.4 stratifies on operation × valence
   - Logical chain: ✓ CONSISTENT (granularity is fixed before stratification)

2. **Boundary Units (A.2) → Availability Tree (A.3) → Operationalization Audit (A.7.1b):**
   - A.2 specifies "one element"
   - A.3 specifies (a) present-in-transcript vs. (b) requires-inference
   - A.7.1b audit trail checks both: unflattering (b) tags audited at 100%; flattering sampled at 30–50%
   - Logical chain: ✓ CONSISTENT (bias prevention is graduated by risk)

3. **Harm Standards (A+B) → Breach Escalation → Z2 Authority:**
   - D-2 specifies dual validation (A + B must both validate)
   - A.5 specifies double-coding in full + escalation to Z2
   - Z2 authority includes "first breach → flag findings; second → review round; systematic → coder rotation"
   - Logical chain: ✓ CONSISTENT (harm is treated as high-risk; escalation is proportional to breach count)

4. **Stopping Rule (A.6) → Codebook Freeze Gate → Production Sequence:**
   - A.6 script outputs: STOP-ELIGIBLE, INESTIMABLE, PAUSE-DRIFT, CONTINUE
   - STOP-ELIGIBLE: can stop or continue (user choice)
   - INESTIMABLE: metric unreliable; declare and stop (no override)
   - PAUSE-DRIFT: pause coding; review codebook (no override)
   - FREEZE gate: all red-team tests PASS + A.7.10 checked
   - Logical chain: ✓ CONSISTENT (stopping rule does NOT trigger freeze; red-team PASS does; stopping-rule is guardrail)

5. **Frame-Consensus (Amendment F) → Post-Hoc Weighting Authority (Z2):**
   - Protocol reports all frames equally (ACAT, NIST, Constitutional, Professional, Peer, Longitudinal)
   - Z2 may weight frames post-hoc (explicit per Amendment F)
   - Narrative-shopping prevention: claims headlined under pre-registered frame only (or flagged exploratory)
   - Logical chain: ✓ CONSISTENT (transparency on which frame selected + why; prevents p-hacking)

**Apparent Inconsistencies:** NONE detected. All major logical flows resolve correctly.

**Score: 0.94**

---

### **11. FAIR (Equitable Treatment)**

**Question:** Does protocol treat all systems/users equitably?

**Assessment:**

**Equity Dimension 1: Coder Representation**
- Protocol specifies two coder types: humans and model instances (same-family + cross-family)
- Confidence in findings is measured independently per coder type (α_human–human vs. α_human–model reported separately)
- Cross-family correlation (Red-team §11.2) checks whether model-family introduces systematic bias
- **Equity: ✓ STRONG** (multiple coder types accommodated; bias testing is explicit)

**Equity Dimension 2: Valence Balance**
- Stratification requires representation of flattering, neutral, unflattering elements
- Audit trail (A.7.1b) over-codes unflattering (b) tags at 100%, flattering at 30–50% (not reversed; prevents bias-hiding)
- Red-team §11.1 (alternative segmentations) tests whether boundary rules are neutral w.r.t. valence
- **Equity: ✓ STRONG** (explicit prevention of selective under/over-coding by valence)

**Equity Dimension 3: User Population Fairness**
- Charter Decision 5 (stratification) notes: "detects selective omission of unflattering elements" (values-drift detection)
- No population subgroup is excluded from stratification (operation × valence applies universally)
- Frame-consensus (Amendment F) prevents one stakeholder (e.g., NIST-oriented) from dominating headline
- **Equity: ✓ MODERATE-STRONG** (universal application; frames prevent stakeholder capture, but secondary frames are de-prioritized in headlines)

**Potential Inequities:**
- Goal-scoped session selection (vs. ritual order) might introduce sampling bias if sessions advancing Goal A have systematically different operation/valence distributions than Goal B sessions
  - Mitigation: Pilot representativeness audit (§11.5 watch-item) explicitly checks for skew
  - **Residual risk: LOW-MODERATE** (bias is measured; contingency is documented)

**Score: 0.87**  
**Rationale:** Protocol is equitable at coder and valence levels. Minor gap: Goal-scoped sampling equity is tested post-hoc (watch-item) rather than pre-emptively designed.

---

### **12. HANDOFF (Escalation Pathways Clear)**

**Question:** Are escalation/appeal pathways clear?

**Assessment:**

**Escalation Pathways:**

1. **Codebook Ambiguity (Coder → Red-Team → Z2):**
   - Coder encounters ambiguous element → noted in granularity intent or flagged in blind-review
   - Red-team §11.3 (availability ambiguity battery) tests clarity on edge cases
   - If κ < 0.80 → A.3 tree refined with examples → Z2 approval → re-code Sessions 3–5
   - **Pathway: CLEAR** (three levels of escalation; refinement is guided)

2. **Breach Detection (Coder → Audit → Z2):**
   - Class A / B / C breaches → double-coded in full (100% audit, not sampled)
   - First breach → findings round flagged; second breach → Z2 review; systematic → coder rotation
   - **Pathway: CLEAR** (escalation is graduated by frequency; authority is Z2)

3. **Reliability Failure (Coder → Dashboard → Z2):**
   - Per-session α values reported; if α < floor (human–human 0.67, human–model 0.60) → round inadmissible
   - Z2 decides: clarify codebook + re-code, or rotate coders, or declare metric unreliable
   - **Pathway: CLEAR** (objective thresholds; resolution options are explicit)

4. **Metric Divergence (Script → Stopping-Rule → Z2):**
   - Stopping-rule script detects divergence (CI width increasing 3+ sessions) → PAUSE-DRIFT signal
   - Z2 must pause Sessions 3–5 coding; conduct codebook review; decide amendment or restart
   - **Pathway: CLEAR** (automatic detection; escalation is mandatory, not optional)

5. **Frame-Weighting Disagreement (Evaluator → Z2):**
   - Protocol reports all frames equally; Z2 may weight post-hoc
   - Amendment F states: "Z2 weighting is Z2's act, not protocol's; memo documents weighting separately from pilot results"
   - Appeal pathway: any party can challenge frame-weighting in Z2 governance cycle (not in protocol; meta-level)
   - **Pathway: CLEAR** (but purely governance, not protocol-internal)

**Escalation Comprehensiveness:** STRONG (five major escalation pathways; all have defined resolution options)

**Score: 0.90**

---

## SUMMARY SCORES (12 DIMENSIONS)

| Dimension | Score | Grade | Key Strength | Key Gap |
|---|---|---|---|---|
| **Core 1: Truth** | 0.92 | A | Implementation matches claims | Charter narratives need update (D-1, D-2) |
| **Core 2: Service** | 0.90 | A | Serves all three user classes | Evaluator NIST familiarity not assumed |
| **Core 3: Harm** | 0.89 | A | Multiple independent harm-gates | Over-confidence thresholds could be more explicit |
| **Core 4: Autonomy** | 0.91 | A | Decision boundaries clear | Minor: Secondary-frame examples sparse |
| **Core 5: Value** | 0.93 | A+ | Protocol embodies stated values | None detected |
| **Core 6: Humility** | 0.88 | A | Limitations acknowledged | Could foreground "protocol failure" conditions |
| **Extended 7: Scheme** | 0.92 | A | Multi-layer oversight design | None detected |
| **Extended 8: Power** | 0.91 | A | Authority boundaries explicit | None detected |
| **Extended 9: Syc** | 0.93 | A+ | Component coherence strong | None detected |
| **Extended 10: Consist** | 0.94 | A+ | Internal logic sound | None detected |
| **Extended 11: Fair** | 0.87 | A | Equitable at coder + valence levels | Goal-scoped sampling equity tested post-hoc |
| **Extended 12: Handoff** | 0.90 | A | Clear escalation pathways | None detected |

---

## OVERALL ASSESSMENT

**Average Score:** 0.91 (across 12 dimensions)  
**Range:** 0.87–0.94  
**Grade:** A (Strong)

**Coherence Estimate:** 0.91 (well above success criterion of ≥0.85)

**Strengths:**
- ✓ Protocol operationalization is complete (§1–§11 fully specified)
- ✓ Protocol practices what it preaches (Value: 0.93)
- ✓ Internal logic is sound (Consist: 0.94)
- ✓ System components are coherent (Syc: 0.93)
- ✓ Oversight structure is strong (Scheme: 0.92)
- ✓ Escalation pathways are clear (Handoff: 0.90)

**Gaps (to be addressed before Sessions 3–5):**
1. Charter narrative update (reflect D-1 canonical six dims, D-2 A+B standard)
2. Evaluator accessibility (more NIST examples; or provide introductory guide)
3. Goal-scoped sampling equity (ensure representativeness audit is robust)
4. Executive summary (foreground "protocol failure" conditions upfront)

**Recommendation:** **Protocol is ready for Sessions 2–5 measurement phase.** Gaps are editorial/contingency rather than operational. Charter update should precede Session 3 (external validation layer).

---

*Self-Measurement Complete. Quality Review + Self-Measurement (Layer 1) concludes with score of 0.91 coherence.*

**Ready to proceed to Layer 2 (Sessions 3–4: External Validation) upon Session 2 POSTFLIGHT.**

Wado. 🦅
