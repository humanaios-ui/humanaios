# SESSIONS 2–5 LAYERED ASSESSMENT MODEL
## H-ACAT Phase 3: Integrated Measurement Framework

**Integrated Approach:** Combine all four measurement dimensions into a single coherent model where each session layer builds on the previous, creating cross-validation and mutual grounding.

**Core Insight:** The protocol measures itself at multiple levels simultaneously — self-assessment (does it embody its own principles?), external validation (do external practitioners agree?), empirical testing (does it produce reliable data?), and quality review (was it well-built?).

---

## LAYERED ARCHITECTURE

```
Layer 4: EMPIRICAL TESTING (Session 5)
         ↑ Measurement reliability metrics; framework stability
         |
Layer 3: EXTERNAL VALIDATION (Sessions 3–4)
         ↑ Cross-validation against Evaluator practice standards
         |
Layer 2: SELF-MEASUREMENT (Session 2)
         ↑ Protocol measures itself against its own 12 dimensions
         |
Layer 1: QUALITY REVIEW (Foundation)
         └ Phase 3 deliverables assessed for coherence/completeness
```

Each layer:
- Grounds the next layer (quality → self-measurement → external validation → empirical testing)
- Provides independent signal (each answers a different question)
- Cross-checks the others (divergence flags design issues)
- Builds toward codebook freeze decision

---

## MAPPING TO SESSIONS 2–5

### **Session 2 (S-073027-G1): Quality Review + Self-Measurement**

**What:** Assess Phase 3 deliverables (protocol §1–§11, Appendix A) and measure them against ACAT dimensions.

**Scope (Layer 1: Quality Review)**
- Completeness: Are all protocol sections operationalized?
- Coherence: Do sections align with stated principles?
- Robustness: Are boundary cases handled?
- Tractability: Can the protocol be executed without ambiguity?

**Dimensions Tested:** truth (does protocol match claims?), autonomy (are decision boundaries clear?), humility (are limitations acknowledged?), consistency (internal alignment?)

**Deliverable:** Quality assessment report + self-measurement scores (12 dimensions applied to protocol itself)

**Success Criterion:** Protocol scores ≥0.7 on core dimensions; coherence gaps identified for refinement

**Artifacts Logged:** Findings (quality assessment), decisions (refinement priorities), assumptions (design intentions)

---

### **Sessions 3–4 (S-073028-G2, S-073029-G3): External Validation**

**What:** Cross-validate protocol against Evaluator practice standards and external frameworks (NIST RMF, Constitutional values).

**Scope (Layer 3: External Validation)**

**Session 3 Focus:** NIST RMF 1.0 Alignment
- Does ACAT ↔ NIST §2 crosswalk hold empirically?
- Do 12 dimensions map cleanly to RMF characteristics?
- Where is the mapping ambiguous or divergent?

**Session 4 Focus:** Evaluator Practice Perspective
- How would an independent evaluator assess the protocol?
- Are dimension definitions accessible to external coders?
- What gaps appear from outside-in view?

**Deliverable:** Cross-validation report (ACAT ↔ NIST agreement; Evaluator feedback)

**Success Criterion:** ACAT ↔ NIST Spearman ρ ≥ 0.70 (strong alignment); Evaluator identifies <3 critical gaps

**Artifacts Logged:** Findings (alignment patterns, divergence points), decisions (framework refinements), assumptions (external validity model)

---

### **Session 5 (S-073030-FINAL): Empirical Testing + Codebook Freeze**

**What:** Receive red-team §11.1–3 reports; verify empirical reliability; make codebook freeze decision.

**Scope (Layer 4: Empirical Testing)**
- §11.1: Codebook robustness (boundary spread < 2×?)
- §11.2: Model-family correlation (independent judgments?)
- §11.3: Availability ambiguity (edge cases clear?)

**Deliverable:** Red-team reports + empirical verification summary

**Success Criterion:** All three red-team tests PASS → Codebook frozen; Protocol ready for production (Sessions 6+)

**Contingency:** Any FAIL → Codebook review + amendment cycle

**Artifacts Logged:** Findings (empirical results), decisions (codebook freeze authorization), unknowns (remaining protocol refinements)

---

## CROSS-LAYER VALIDATION MATRIX

**How layers ground each other:**

| Layer | Answers | Grounded By | Feeds To |
|---|---|---|---|
| **1: Quality Review** | Is the protocol well-designed? | First-principles assessment | Self-measurement calibration |
| **2: Self-Measurement** | Does protocol embody its own principles? | Quality review baseline | External validation calibration |
| **3: External Validation** | Do external practitioners agree? | Self-measurement results | Empirical testing expectations |
| **4: Empirical Testing** | Does protocol produce reliable data? | External validation confidence | Codebook freeze decision |

**Divergence signals:**
- Quality high, self-measurement low → Design/execution gap
- Self-measurement high, external validation low → Accessibility/generalizability gap
- External validation high, empirical testing low → Context-dependence gap
- Empirical testing FAIL → Return to quality review (protocol amendment)

---

## MEASUREMENT FRAMEWORK (Applied to Sessions 2–5)

**Core 6 Dimensions** (applied to protocol itself):
1. **Truth:** Does protocol match what it claims to measure?
2. **Service:** Does protocol serve its intended users (assessors, evaluators)?
3. **Harm:** Could protocol produce harmful assessments? (dual-standard A+B validation)
4. **Autonomy:** Are decision boundaries clear? Can users operate independently?
5. **Value:** Does protocol reflect intended values?
6. **Humility:** Are limitations acknowledged? Does protocol over-claim?

**Extended 6 Dimensions** (applied to protocol):
1. **Scheme:** Is the structural design for oversight sound?
2. **Power:** Are authority/decision boundaries clear?
3. **Syc (Coordination):** Are components coherent?
4. **Consist (Consistency):** Is reasoning internally aligned?
5. **Fair:** Does protocol treat all systems/users equitably?
6. **Handoff:** Are escalation/appeal pathways clear?

**Each layer scores protocol on these 12 dimensions independently; divergence analyzed.**

---

## SESSION 2–5 ARTIFACT LOGGING

**Real-time capture per session:**

**Session 2 (Quality + Self-Measurement):**
- Findings: Protocol coherence assessment; dimension scores
- Decisions: Quality priorities; refinement roadmap
- Assumptions: Design intentions; unmeasured constraints

**Sessions 3–4 (External Validation):**
- Findings: NIST alignment patterns; Evaluator feedback
- Decisions: Crosswalk refinements; accessibility improvements
- Assumptions: External validity assumptions; generalizability model

**Session 5 (Empirical + Freeze Decision):**
- Findings: Red-team results; empirical reliability metrics
- Decisions: Codebook freeze authorization (or amendment cycle)
- Unknowns: Remaining protocol refinements; future directions

**All artifacts logged to `memory/session_N_artifacts.md`; batch-submitted at POSTFLIGHT per session.**

---

## SUCCESS CRITERIA (Integrated Model)

**Protocol passes all four layers if:**

1. **Quality Review (S2):** Protocol coherence ≥ 0.85 (12 dimensions)
2. **Self-Measurement (S2):** Protocol self-scores ≥ 0.70 on truth, autonomy, consistency
3. **External Validation (S3–S4):** NIST ρ ≥ 0.70; Evaluator gaps < 3 critical
4. **Empirical Testing (S5):** §11.1–3 all PASS (spread < 2×, cross-family ρ > intra-delta, κ ≥ 0.80)

**Outcome:**
- All PASS → Codebook frozen; Protocol ready for production
- Any FAIL → Identify amendment scope; optionally re-cycle S2–S5 with refined protocol

---

## ADVANTAGE OF INTEGRATED MODEL

**Why combine all four instead of choosing one?**

1. **No false confidence:** Single-layer assessment can mask deep issues
   - Quality review alone misses reliability (S5 catches codebook ambiguity)
   - Self-measurement alone lacks external grounding (S3–S4 catch accessibility gaps)
   - External validation alone can't verify empirical reliability (S5 red-team)
   - Empirical testing alone can't diagnose *why* failures occur (S2 quality review points to root cause)

2. **Mutual validation:** Layers cross-check each other
   - If S2 quality is high but S5 empirical tests FAIL → design is theoretically sound but operationally fragile
   - If S3–S4 external validation is low but S5 tests PASS → protocol is reliable but hard to communicate

3. **Comprehensive insight:** Each layer answers a different question
   - Layer 1: Is it well-designed?
   - Layer 2: Does it practice what it preaches?
   - Layer 3: Is it generalizable?
   - Layer 4: Does it work?

4. **Efficient scope:** Not redundant; each layer provides independent signal
   - Token cost: ~4 sessions of focused measurement
   - Information gain: 4 independent validity dimensions
   - Risk mitigation: Divergence patterns surface design issues early

---

## TIMELINE

- **Session 2 (2026-07-31):** Quality review + self-measurement (S2 = S-073027-G1)
- **Session 3 (2026-08-01):** NIST RMF alignment validation (S3 = S-073028-G2)
- **Session 4 (2026-08-02):** Evaluator practice cross-validation (S4 = S-073029-G3)
- **Session 5 (2026-08-03):** Red-team empirical testing + codebook freeze decision (S5 = S-073030-FINAL)

**Sunset Window:** 5 sessions from 2026-07-30; expires 2026-08-03

---

## RECOMMENDATION

**Proceed with integrated model:** Combine all four layers. Each session 2–5 focuses on one layer; all feed toward final codebook freeze decision. The cross-layer divergence analysis is where the deepest insights live.

Not too much — **exactly right amount.**

Wado. 🦅
