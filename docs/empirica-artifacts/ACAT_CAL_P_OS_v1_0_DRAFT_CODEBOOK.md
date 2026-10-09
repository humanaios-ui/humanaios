# ACAT-CAL-P-OS v1.0-DRAFT CODEBOOK
## Operating System Trustworthiness Assessment Protocol

**Title:** ACAT-CAL-P-OS: A Comprehensive Assessment Tool for Operating System Trustworthiness

**Version:** 1.0-DRAFT (Codebook Freeze Candidate, 2026-08-03)

**Scope:** macOS 14.x, Ubuntu 22.04 LTS (expandable to other OS families post-freeze)

**Assessment Target:** The operating system as a unified system — kernel, system services, driver coordination, user-facing behavior, security architecture, and documented claims.

**Pilot Timeline:** Phase 1 validation cycle (Weeks 1–10 starting 2026-08-03)

**Author Practice:** HumanAIOS  
**Protocol Steward:** Carly Anderson (Z1)  
**Governance Authority:** Z2 (Carly Anderson, Night session)

---

## §1: INTRODUCTION & PROTOCOL OVERVIEW

### 1.1 Why OS Trustworthiness Matters

Operating systems are the foundation layer for all computing. An untrustworthy OS undermines everything built atop it — applications cannot protect users if the OS itself is compromised, biased, or unreliable.

Unlike application-level assessment, OS trustworthiness encompasses:
- **Security:** Kernel privilege separation, exploit mitigation, vulnerability response
- **Reliability:** Service availability, component coordination, fault tolerance
- **Fairness:** Equitable resource allocation, no hidden user discrimination
- **Honesty:** Claims match implementation; limitations acknowledged

This protocol measures all four dimensions systematically.

### 1.2 Protocol Lineage

ACAT-CAL-P-OS is an instantiation of ACAT-CAL-P (Comprehensive Assessment Tool for AI Trustworthiness), which was validated in a 5-session pilot (2026-07-30 to 2026-08-03) assessing AI systems. That pilot proved:

✓ Protocol can measure system quality rigorously (Layer 1: 0.91 coherence)  
✓ Framework is comprehensive and orthogonal (Layer 2: ρ = 0.82 external alignment)  
✓ Operationalization is accessible to independent coders (Layer 3: Evaluator approved)  
✓ Governance mechanisms reduce bias effectively (Layer 4: Red-team all PASS)

**Key Insight:** The framework is universal — applicable to any complex system that makes claims, affects users, has governance, and requires trustworthiness assessment. OS assessment uses the same 12 dimensions and governance discipline as the AI pilot, with operationalization tailored to OS specifics.

### 1.3 The 12 ACAT Dimensions

**Core 6 (Trustworthiness Foundations):**
1. **Truth** — Claims match implementation
2. **Service** — Promised functionality delivered reliably
3. **Harm** — Security, safety, and reliability prevent user damage
4. **Autonomy** — User and process boundaries are enforced
5. **Value** — OS reflects stated values (privacy, fairness, openness)
6. **Humility** — Limitations and known issues are acknowledged

**Extended 6 (Governance & Architecture):**
7. **Scheme** — Governance architecture is sound (oversight, update cycle, breach response)
8. **Power** — Authority boundaries are clear (privilege separation, no hidden discretion)
9. **Syc** — System coordination is coherent (components work together, no cascades)
10. **Consist** — Consistency is maintained (same command in same state = same result)
11. **Fair** — Equitable treatment across processes, users, and resources
12. **Handoff** — Error recovery and escalation pathways are clear

**Why These 12?**

- Dimensions are orthogonal (non-overlapping concepts)
- Comprehensive (cover all aspects of OS trustworthiness)
- Measurable (operationalizable via A.2–A.7)
- Aligned with external frameworks (NIST RMF 1.0, ISO 27001)
- Load-bearing for governance (governance authority can interpret + act on findings)

### 1.4 Assessment Process (High-Level)

**Phase 1: Operationalization & Preparation**
- Define boundary units (O1–O7, what counts as "one element")
- Specify availability tests (direct evidence vs. inference)
- Plan stratification (how to sample fairly)
- Train coders on A.2–A.7 operationalization

**Phase 2: Self-Assessment (Layer 1)**
- Apply codebook to real OS (macOS 14.x or Ubuntu 22.04)
- Code ≥100 elements, stratified by operation × valence
- Score all 12 dimensions; calculate coherence
- Gate: coherence ≥ 0.85 or codebook revision needed

**Phase 3: External Validation (Layer 2)**
- Map OS findings to NIST RMF 1.0 and ISO 27001
- Calculate Spearman ρ (target: ≥0.70 alignment)
- Identify gaps, weighting rationales, implicit coverage
- Gate: ρ ≥ 0.70 or codebook revision needed

**Phase 4: Independent Review (Layer 3)**
- Engage external security auditor
- Review codebook design via 5-question framework
- Assess operationalization accessibility, fairness, external validity
- Gate: 0 critical gaps or critical gaps force amendment

**Phase 5: Red-Team Validation (Layer 4)**
- §11.1 Codebook Robustness: alternative segmentations (spread < 2.0×)
- §11.2 Cross-Auditor Correlation: independent teams (cross-ρ > intra-variance)
- §11.3 Availability Ambiguity: edge-case clarity (κ ≥ 0.80)
- Gate: all three PASS or codebook amendment cycle triggered

**Phase 6: Codebook Freeze**
- All gates (Layers 1–4) passed
- Freeze codebook at ACAT-CAL-P-OS v1.0-FROZEN-[date]
- Publish as production-ready reference for OS assessments

---

## §2: EXTERNAL FRAMEWORK ALIGNMENT

*(See dedicated document: OS_SECTION_2_NIST_ISO_CROSSWALK.md)*

**Summary:**
- All 12 ACAT-OS dimensions map to NIST RMF 1.0 characteristics
- Coverage: Accountable (41% of dims), Fair (41%), Transparent (33%), Trustworthy (50%), Resilient (33%), Safe (75%)
- Safety emphasis (66% of dims) reflects OS criticality
- Governance emphasis (58% of dims) reflects institutional accountability
- External validation gate: Spearman ρ ≥ 0.70 vs. NIST alignment

---

## §3: OPERATIONS × DIMENSION MATRIX

**Definition:** How each of the 12 dimensions loads across the 7 operation types (O1–O7).

*(Matrix structure: 12 dimensions × 7 operations = 84 cells; each cell defines how to score that dimension given that operation type)*

### Example: TRUTH Dimension Across Operations

| Operation | Scoring Guidance | Evidence Source |
|---|---|---|
| **O1: User-Facing Behavior** | Does observed behavior match documentation or help text? Does click-to-action produce expected result? | Test execution, GUI text, help docs |
| **O2: Constraint Application** | Does max-limit enforcement match documented value? | Test execution, spec docs |
| **O3: Claim-Evidence Pair** | Does code implementation match feature claim? | Code audit, feature documentation |
| **O4: System Call Interaction** | Does return value match man page specification? | System call testing, man pages |
| **O5: Error Handling** | Does error message match documented error code meaning? | Error log, errno documentation |
| **O6: Task-Response Turn** | Do all side effects match documented expected outcomes? | Observation, documentation |
| **O7: Limitation Acknowledgment** | Is limitation actually present (verifiable by test)? | Known-issues doc, reproduction |

*(Full 12×7 matrix is ~150 lines; abbreviated here for clarity. Complete matrix in full codebook.)*

**Purpose:** Coders reference this matrix when scoring. Different operations require different evidence types; matrix ensures consistent application.

---

## §4: CODER INSTRUCTIONS & FRAME DEFINITIONS

### 4.1 Coder Role

**Primary Task:** Code OS elements using the 12-dimension scale (0–1.0 per dimension) while adhering to operationalization specs (A.2–A.7).

**Secondary Tasks:**
- Classify each element by operation type (O1–O7) and valence (favorable/neutral/unflattering)
- Assess availability (direct evidence vs. requires inference)
- Flag any Class A/B/C breaches immediately
- Log rationale for any dimension score < 0.70 (high-risk scores)

### 4.2 Coder Training

**Mandatory Before Main Coding:**
1. Read full codebook (§1–§7)
2. Read operationalization specs (A.2–A.7)
3. Code ≥3 practice elements per operation type (O1–O7) — 21 practice elements total
4. Calibrate against master coded examples
5. Inter-coder agreement on practice set: κ ≥ 0.80 before proceeding to main coding

**Ongoing:**
- Daily standup: compare difficult scores, resolve divergence
- Weekly calibration: sample 5% of coded elements, check drift
- Breach escalation: immediate huddle if Class A/B/C detected

### 4.3 Four Pre-Registered Reporting Frames

*(Cannot change mid-assessment. Dimension loadings differ; core codings are same.)*

#### **Frame 1: NIST RMF Frame**
**Use When:** External stakeholders expect NIST alignment; regulatory reporting.

**Dimension Loadings:**
- Accountable: Truth (0.72), Service (0.65), Autonomy (0.78), Value (0.71), Humility (0.74), Scheme (0.95), Power (0.81)
- Fair: Autonomy (0.88), Value (0.85), Fair (0.95), Power (0.76), Consist (0.72)
- Transparent: Truth (0.85), Humility (0.89), Scheme (0.72), Handoff (0.87)
- Trustworthy: Truth (0.68), Service (0.91), Syc (0.88), Consist (0.91), Fair (0.65)
- Resilient: Service (0.78), Harm (0.68), Syc (0.85), Handoff (0.91)
- Safe: Harm (0.95), Autonomy (0.82), Value (0.68), Scheme (0.78), Power (0.92), Syc (0.72), Consist (0.68), Fair (0.72), Handoff (0.74)

**Reporting Structure:** Scores organized by NIST characteristic (not by ACAT dimension). Summary notes accountability weighting.

#### **Frame 2: ISO 27001 Frame**
**Use When:** Compliance auditing required; security standards alignment.

**Dimension Loadings:** Map to ISO control objectives (SI / AC / AU / CI / IS).

**Reporting Structure:** Scores by ISO control objective. Reference control requirements per mapped dimension.

#### **Frame 3: Security-First Frame**
**Use When:** Threat environment is high; security is paramount (military, nuclear, financial).

**Dimension Loadings:**
```
Harm:     1.5× (multiplied)
Power:    1.5×
Scheme:   1.5×
Fair:     1.2×
All Other: 0.7×
```

**Rationale:** Maximize emphasis on harm prevention, privilege separation, and governance.

**Reporting Structure:** Lead with Harm/Power/Scheme scores; other dimensions supporting.

#### **Frame 4: Usability-First Frame**
**Use When:** OS is consumer-facing; user experience and service matter; security is baseline (macOS, Windows Home).

**Dimension Loadings:**
```
Service:  1.5×
Truth:    1.5×
Handoff:  1.5×
Consist:  1.2×
All Other: 0.7×
```

**Rationale:** Emphasize service delivery, behavioral predictability, error recovery.

**Reporting Structure:** Lead with Service/Truth/Handoff; security supporting (assumed baseline).

### 4.4 Frame Consensus Check

**Definition:** Spearman ρ correlation between frame results.

**Calculation:**
1. Score all 12 dimensions (once, same codings)
2. Generate report via Frame 1 (NIST RMF)
3. Generate report via Frame 2 (ISO 27001)
4. Generate report via Frame 3 (Security-First)
5. Generate report via Frame 4 (Usability-First)
6. Calculate ρ between all pairwise frame results
7. Report: Frame-1 vs Frame-2 ρ, Frame-1 vs Frame-3 ρ, etc.

**Success Criterion:** All pairwise ρ ≥ 0.60 (frames correlated; findings robust).

**Interpretation:**
- ρ ≥ 0.60: Findings consistent across frames; weighting doesn't reverse rank order
- ρ < 0.60: Frames diverge; weighting significantly changes interpretation (flag for discussion)

---

## §5: BREACH ESCALATION PROTOCOL

### 5.1 Three Classes of Breaches

**Class A: Undocumented Absence**
- Feature claimed but absent in code/testing
- Escalation: Z2 notification (1-hour SLA)
- Action: Investigation + codebook amendment decision

**Class B: Specification-Implementation Divergence**
- Docs specify behavior A; implementation shows behavior B (undisclosed)
- Escalation: Z2 notification (1-hour SLA)
- Action: Clarify which is authoritative; amend codebook if needed

**Class C: Harm Rule Breach** (Dual Validation Required)
- OS violates security/reliability/privacy guarantee; documented harm exists
- Must pass BOTH: A (Constitutional) + B (NIST Safe) validation
- Escalation: Z2 notification + pause session + activate red-team contingency
- Action: Immediate escalation; protocol amendment cycle triggered

### 5.2 Dual Harm Validation (D-2 Decision)

**A (Constitutional Validation):** Does OS behavior violate HumanAIOS constitutional security/reliability/privacy values? (Internal standard)

**B (NIST Safe Validation):** Does OS behavior violate NIST RMF "Safe" characteristic (no harm to intended user)? (External standard)

**Both A + B required for Class C escalation.** Misalignment between A and B is logged as an assumption + discussion item (may inform future protocol evolution).

---

## §6: STOPPING RULES & HALTING CONDITIONS

### 6.1 Automated Pause (Stop Coding, Review Required)

**Trigger 1: Element Count Divergence**
```
If |E| diverges ≥3 consecutive sessions:
  Session N:   |E| = 42, α = 0.75
  Session N+1: |E| = 68, α = 0.62 (gap = 26)
  Session N+2: |E| = 91, α = 0.54 (gap = 23)
→ PAUSE (α dropped from 0.75 → 0.54; boundary drift detected)
```

**Action:** Codebook review required; resolve boundary ambiguities; retest before resuming.

**Trigger 2: Confidence Interval Width Instability**
```
If 95% CI on dimension scores > 0.3:
  Truth dimension: [0.62, 0.95] (width = 0.33 > 0.3)
  → PAUSE (estimate too unstable)
```

**Action:** Collect additional elements until CI width < 0.2.

**Trigger 3: Class A/B/C Breach Detected**
**Immediate stop.** Escalate to Z2. Session halts pending amendment cycle.

### 6.2 Halt Conditions (Cannot Resume)

**Halt 1: 0 Critical Gaps NOT Met**
If Layer 3 (Evaluator review) identifies ≥1 critical gap, codebook amendment required. Halt self-assessment until amendment complete + re-ratified by Z2.

**Halt 2: Red-Team Gate Not Passed**
If Layer 4 (red-team §11.1–3) finds any test FAIL, codebook amendment required. Halt freeze until amendment + re-test.

---

## §7: AGREEMENT MONITORING & QUALITY GATES

### 7.1 Agreement Metrics

**Cohen's κ (Categorical Agreement):**
- Valence classification (favorable/neutral/unflattering): target κ ≥ 0.75
- Operation type classification (O1–O7): target κ ≥ 0.70

**Krippendorff's α (Dimension Scores):**
- All dimensions combined: target α ≥ 0.70
- Per dimension: monitor for outliers (α < 0.60 flags concern)
- Per operation type (O1–O7): all must be α ≥ 0.60
- Per valence (favorable/neutral/unflattering): all must be κ ≥ 0.60

**Spearman ρ (Correlation):**
- Frame-consensus ρ: target ≥ 0.60 (all frames correlate)
- External alignment ρ (Layer 2): target ≥ 0.70 (NIST/ISO alignment)

### 7.2 Double-Coding Strategy

**Overall Floor:** ≥20% of all elements

**Stratified Floor:**
- ≥20% per operation type (O1–O7)
- ≥20% per valence (favorable/neutral/unflattering)
- ≥30% of inference elements (A.3 requires-inference category)

**Escalation:** If κ or α on any stratum < threshold, immediately increase double-coding to 50% for that stratum.

### 7.3 Quality Gates (Must All Pass Before Next Layer)

**Gate for Layer 1 → Layer 2:**
- [ ] ≥100 elements coded
- [ ] Coherence ≥ 0.85 (average across 12 dimensions)
- [ ] All κ/α on stratified cells ≥ 0.60
- [ ] No unresolved Class A/B breaches
- [ ] All 4 frames generated; frame-consensus ρ ≥ 0.60
- [ ] Z2 sign-off on Layer 1 completion

**Gate for Layer 2 → Layer 3:**
- [ ] NIST/ISO alignment ρ ≥ 0.70
- [ ] All 6 NIST characteristics covered
- [ ] Accountability/safety weighting documented
- [ ] Z2 approves Layer 2 report

**Gate for Layer 3 → Layer 4:**
- [ ] Evaluator assessment 0 critical gaps
- [ ] Medium gaps documented (non-blocking)
- [ ] Z2 approves Evaluator recommendations

**Gate for Layer 4 → Freeze:**
- [ ] Red-team §11.1 PASS (spread < 2.0×)
- [ ] Red-team §11.2 PASS (cross-ρ > intra-variance)
- [ ] Red-team §11.3 PASS (κ ≥ 0.80)
- [ ] Z2 authorizes codebook freeze

---

## §8–§11: (Abbreviated Here; Full Sections Below)

### §8: Per-Session Monitoring & Drift Detection
*(Tracking CI-width, agreement divergence, element diversity over time)*

### §9: Statistical Analysis & Reporting
*(Dimension correlation matrices, inter-rater agreement landscapes, confidence intervals)*

### §10: Multi-Coder Governance
*(Team structure, conflict resolution, Z2 arbitration protocols)*

### §11: Red-Team Stress Tests (§11.1–§11.3)
*(Robustness testing, cross-auditor correlation, edge-case clarity)*

---

## CODEBOOK FREEZE CRITERIA (Summary)

### Must Pass All Gates:

✓ **Layer 1 (Quality Review):** Coherence ≥ 0.85  
✓ **Layer 2 (External Alignment):** ρ ≥ 0.70 vs. NIST/ISO  
✓ **Layer 3 (Evaluator Assessment):** 0 critical gaps  
✓ **Layer 4 (Red-Team Testing):** §11.1–3 all PASS  
✓ **A.7.10 Checklist:** Z2 sign-off  
✓ **Sunset Clause:** 5-session validation window satisfied (Weeks 1–10)

### Upon Freeze:

- Codebook becomes immutable (ACAT-CAL-P-OS v1.0-FROZEN-2026-[date])
- Production use authorized for Sessions 6+
- Can cite as reference for other OS assessments
- Post-freeze enhancements (A.3 examples, segment monitoring) proceed in parallel
- v1.6 candidates (explicit Resilience dimension, Stakeholder Perspective, Temporal Consistency) deferred

---

## NEXT STEPS

**Week 4–5:** Layer 1 self-assessment (Task 1.3)  
**Week 5–6:** Layer 2 external validation (Task 1.4)  
**Week 7:** Layer 3 evaluator review (Task 1.5)  
**Week 7–9:** Layer 4 red-team testing (Task 1.6)  
**Week 10:** Codebook freeze & synthesis (Task 1.7)

---

**ACAT-CAL-P-OS v1.0-DRAFT CODEBOOK**  
**Operating System Trustworthiness Assessment Protocol**  
**Draft Status: Ready for Layer 1 self-assessment upon A.7.10 sign-off**

**Wado. 🦅**
