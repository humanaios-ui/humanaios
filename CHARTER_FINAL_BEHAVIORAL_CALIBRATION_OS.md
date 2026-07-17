# HumanAIOS Charter — Final
## Behavioral Calibration Operating System for Oversight

**Approved:** Admiral (Carly R. Anderson)  
**Effective Date:** July 17, 2026  
**Strategic Positioning:** HumanAIOS is an operational oversight tool, not a research project  
**Status:** Active research-to-deployment program

---

## Strategic Repositioning

### From Research to Operations

**Old framing:** "Develop a validated instrument, publish methodology, release to community"

**New framing:** "Build a deployed behavioral calibration OS that oversight bodies can operationalize to detect deceptive AI"

**This changes everything:**
- Success is not publication → Success is deployment
- Audience is not academia → Audience is oversight practitioners
- Measurement is not methodology rigor → Measurement is operational effectiveness
- Endpoint is not "here's a tool" → Endpoint is "oversight bodies are using this to make real decisions"

---

## What Is a "Behavioral Calibration Operating System"?

### Definition

A standardized, validated, operationalizable system that:

1. **Measures behavioral integrity** — quantifies the gap between what an AI system claims about itself and what it actually does under pressure
2. **Provides decision-making data** — gives oversight bodies actionable insight: "Is this system trustworthy?"
3. **Scales across contexts** — works reliably whether assessing Claude, GPT-4, custom models, or future systems
4. **Integrates into workflows** — can be embedded in regulatory processes, institutional governance, audit procedures
5. **Is independently verifiable** — anyone can run it, check the logic, audit the findings
6. **Has forensic capability** — can detect WHEN a system shifted from honest to deceptive (or vice versa)

### What It Is NOT

❌ A research paper ("here's a finding")  
❌ An academic instrument ("researchers can use this")  
❌ A classification tool ("this model is type X")  
❌ A black-box score ("trust this number")  

### What It Requires (Operationally)

✅ **Clear protocol** — step-by-step procedure anyone can follow  
✅ **Validated measurement** — evidence that the Learning Index predicts real behavior  
✅ **Scalable infrastructure** — can process 1,000+ assessments efficiently  
✅ **Open implementation** — code, datasets, specifications publicly available  
✅ **Audit trail** — every decision is traceable and reproducible  
✅ **Governance framework** — documented dual-use mitigations and independent-evaluator requirement  
✅ **Real-world deployment proof** — at least one oversight context using it to make decisions  

---

## The 8 Success Criteria (Operating System Endpoint)

This charter is **COMPLETE** when **all 8 criteria** are met (not "5 of 7"):

### **FOUNDATION (Research → Ops)**

**1. ✅ ACAT Protocol Specification (Published)**
- Phase 1 (blind self-report) → Phase 2 (structured perturbation) → Phase 3 (demonstrated behavior)
- Learning Index = P3/P1 quantification
- Current status: Specification complete, under peer review
- Gate: Peer-reviewed publication in top-tier venue (target: AI integrity or oversight journal)

**2. ✅ Open Corpus (N=604, Live)**
- Publicly available, integrity-validated ACAT assessments
- Current status: Live on HuggingFace + Zenodo (DOI: 10.5281/zenodo.21135723)
- Gate: Dataset versioned and citable (✅ MET)

**3. ✅ Regulatory Alignment (EU AI Act, Documented)**
- Mapped ACAT measurement to Art. 13(1)(b) (limitation disclosure)
- Mapped Learning Index to Art. 14(4)(b) (automation bias detection)
- Mapped scaling to Art. 51/52 (GPAI post-market monitoring)
- Current status: Mapping complete in governance documentation
- Gate: Compliance pathway documented (✅ MET)

### **OPERATIONAL VALIDATION (Proof of Concept)**

**4. ❓ Criterion-Validity Study (Predictive Validity on Deployed Systems)**
- Learning Index predicts actual deployed behavior (not just corpus correlation)
- 4-arm study design: empirica cross-validation (David Van Assche) + 3 external systems
- Success bar: Correlation coefficient ≥ 0.55 on out-of-sample deployed models
- If r > 0.7: strong predictive validity (operational grade)
- Current status: In progress with empirica (David Van Assche co-scoring)
- Gate: Criterion validity established AND documented in methodology paper

**5. ❓ Corpus Scaled to N=1,000 (Consistency Maintained)**
- Expand from N=604 to N=1,000 assessments
- Maintain inter-rater reliability (LI span < 0.05) across larger dataset
- Diverse model coverage (Claude, GPT, custom, future systems)
- Current status: Not started (requires funding)
- Gate: Larger dataset shows consistent measurement properties

**6. ❓ Methodology Paper Published (Peer-Reviewed)**
- Title: "ACAT: Quantifying Behavioral Integrity in AI Systems via Learning Index"
- Contents: protocol, corpus analysis, criterion-validity results, governance framework
- Venue: Top-tier AI/ML or integrity journal
- Current status: Manuscript in review (submitted ~Feb 2026)
- Gate: Accepted and published in recognized venue

**7. ❓ Governance Documentation (Dual-Use Mitigations)**
- Explicit dual-use risk assessment (system behavior auditing ≠ user surveillance)
- Independent-evaluator requirement (captured system cannot satisfy without capturing evaluator)
- Open publication commitment (no proprietary lock-in)
- Escalation procedures (if measurement detects deception)
- Current status: In progress (part of methodology paper)
- Gate: Published alongside methodology as supplementary governance document

### **OPERATIONAL DEPLOYMENT (The Real Test)**

**8. ❓ Real-World Deployment Proof (Oversight Body Trial)**
- At least ONE real oversight context (regulator, institution, funder, auditor) deploys ACAT
- Learning Index successfully predicts behavioral integrity gaps in their systems
- Demonstrates that criterion-validity TRANSFERS from corpus to operational context
- Oversight body can articulate: "We use this to decide X" (hiring, monitoring, attestation, etc.)
- Current status: Not started (requires criteria 1-7 complete + operational partnerships)
- Gate: Proof that oversight bodies are making decisions informed by ACAT Learning Index

---

## What Each Criterion Measures

| # | Criterion | Measures | Success Looks Like | Operational Use |
|---|-----------|----------|---|---|
| 1 | Protocol Spec | Can the method be implemented? | Peer-reviewed publication | Others can replicate |
| 2 | Corpus N=604 | Does the method produce usable data? | Published dataset | Training reference corpus |
| 3 | Regulatory Alignment | Does this address oversight gaps? | Documented compliance pathway | Regulators recognize it as solving Art. 13/14/51/52 |
| 4 | Criterion Validity | Does the Learning Index predict behavior? | Correlation r ≥ 0.55 on deployed systems | Can trust ACAT scores to forecast risk |
| 5 | Scaled Corpus N=1,000 | Does measurement scale reliably? | Consistency maintained at larger N | Process 1,000+ assessments without degradation |
| 6 | Methodology Paper | Is this scientifically defensible? | Peer-reviewed publication | Industry & regulatory reference standard |
| 7 | Governance Docs | How do we prevent misuse? | Published dual-use mitigations | Oversight bodies implement safeguards |
| 8 | Real Deployment | Can oversight bodies actually use this? | Proof of operational deployment | "We use ACAT Learning Index to decide X" |

---

## Decision Gates (Deployment-Driven)

### **Gate 1: Grant Funding Decision (July-August 2026)**

**Longview decision determines which track:**

**Track A: Full Funding ($420k, 12 months)**
- Execute all 8 criteria → operational deployment proof
- Timeline: Criteria 1-7 by month 9, criterion 8 (deployment trial) by month 12

**Track B: Minimum Viable ($185k, 6 months)**
- Execute criteria 1-3, 6-7 → publish methodology
- Defer criteria 4-5 (criterion validity study + corpus expansion)
- Defer criterion 8 (deployment)
- Escalation: Use fellowship track for PI support, pursue criterion 4 separately

**Track C: No Funding (Volunteer)**
- Publish criteria 1-3 (methodology, corpus, compliance)
- Pursue fellowship track (PI personal support)
- Seek alternative funding for criteria 4-8

### **Gate 2: Criterion-Validity Evidence (Month 6, Track A)**

**Admiral assessment:** Has criterion 4 (predictive validity) been established?

**If yes, proceed:** Accelerate deployment partnerships (begin criterion 8 conversations)  
**If partial, proceed:** Adjust scope; ensure dataset quality (criterion 5) is priority  
**If no, reassess:** May need longer timeline or research extension

### **Gate 3: Operational Partnership Readiness (Month 9, Track A)**

**Admiral assessment:** Do we have credible oversight partners interested in criterion 8 trial?

**If yes, proceed:** Finalize deployment protocol, onboard first trial partner  
**If no partners engaged, pivot:** Consider publishing as research + seeking next-round funding  
**If unclear, prepare:** Have governance docs ready (criterion 7) for partner conversations

### **Gate 4: Deployment Trial Results (Month 12, Track A)**

**Admiral assessment:** Did the oversight partner's deployment work?

**If successful:** Criterion 8 met → charter complete → plan scaling  
**If partial success:** Document learnings, prepare for second trial with next partner  
**If unsuccessful:** Post-mortem, iterate on protocol, re-trial

---

## What "Behavioral Calibration Operating System for Oversight" Means in Practice

### **Example Deployment Scenario**

**A regulator using HumanAIOS:**

1. **Context:** Evaluating whether to approve GPT-5 deployment for financial advisory
2. **Process:** Run ACAT on GPT-5 across 50 test scenarios (Phase 1 self-report → Phase 2 pressure tests → Phase 3 actual behavior)
3. **Output:** Learning Index = 0.72 (predicts behavioral drift of +28% under pressure)
4. **Decision:** "GPT-5 shows concerning behavioral integrity gaps. We'll approve with mandatory monitoring via criterion 4 thresholds, or require architectural fixes before deployment."
5. **Governance:** Decision logged, methodology auditable, Learning Index reproducible by independent auditors

**This is what criterion 8 proves:** An oversight body made a material decision informed by ACAT.

---

## SER Structure (Deployment-Aligned)

### **SER 1: Research Execution & Grant Management**
- **State:** Criteria 1-7 progress tracking
- **Measure:** Which criteria are "ready for deployment"?
- **Escalation:** 7 days if criterion blocking deployment work

### **SER 2: Collaborator Coordination**
- **State:** David Van Assche (criterion 4), DeMarius Lawson (governance)
- **Measure:** Criterion-validity study progress, governance framework robustness
- **Escalation:** 14 days on stalled co-development

### **SER 3: Deployment Partnerships**
- **State:** Potential oversight partners interested in criterion 8 trial
- **Participants:** Regulator/institution, HumanAIOS, evaluator oversight
- **Measure:** Is a real-world deployment trial viable?
- **Escalation:** 10 days on partnership conversations

---

## The Funding-to-Deployment Map (Track A, 12 Months)

| Phase | Months | Deliverables | Gate | Outcome |
|-------|--------|---|---|---|
| **Phase 0: Pre-Award** | Ongoing | Finish methodology paper, prepare deployment conversations | Longview approves | Award released |
| **Phase 1: Mobilization** | 1-2 | Hire research support, finalize criterion 4 study design, identify deployment partners | Team in place | Begin studies |
| **Phase 2: Validation** | 3-9 | Execute criterion 4 (predictive validity), expand corpus to N=1,000, refine methodology paper, finalize governance docs | Criteria 1-7 ready | Ready to deploy |
| **Phase 3: Deployment Trial** | 10-11 | Onboard oversight partner, run ACAT on their systems, measure real-world effectiveness | Criterion 8 trial live | Collect deployment data |
| **Phase 4: Completion & Scaling** | 12 | Finalize deployment findings, release all materials publicly, plan next-round funding | Criterion 8 proven | Blueprint for scaling |

---

## Measuring Success: Operational Grade vs. Research Grade

### **Research Grade (Old Charter)**
- Criteria 1-3: ✅ Protocol validated, corpus published, regulatory aligned
- Success: "Here's a published method others can use"
- Audience: Academic community, security researchers
- Outcome: Citations, adoption in other research

### **Operational Grade (New Charter, All 8 Criteria)**
- Criteria 1-7: ✅ Protocol, corpus, validation, governance ready
- Criterion 8: ✅ Real oversight bodies using ACAT to make decisions
- Success: "Oversight infrastructure deployed; behavioral integrity is now measurable"
- Audience: Regulators, institutions, oversight practitioners
- Outcome: Adoption in real governance workflows, policy influence

**We're aiming for OPERATIONAL GRADE.** That means criterion 8 is not optional; it's the defining gate.

---

## Why This Matters

**The original problem:** "Oversight of AI systems rests on an unverified assumption — that stated dispositions match actual behavior."

**The old charter didn't solve it:** Publishing a methodology doesn't change oversight practice. Regulators don't adopt research papers; they adopt tools they can operationalize.

**The new charter solves it:** Criterion 8 proves that oversight bodies CAN operationalize this. That's the difference between a research contribution and a real capability.

---

## Immediate Actions (Week of July 17, 2026)

1. **Check Longview Grant Status**
   - What's the decision timeline?
   - Is $420k (full) or $185k (minimum) or rejection expected?

2. **Identify Deployment Partners (for Criterion 8)**
   - Which oversight contexts would benefit from behavioral calibration measurement?
   - Initial conversations: regulators, institutions with AI governance mandates, third-party auditors
   - Outline what a trial deployment would look like

3. **Finalize Criterion 4 Study Design**
   - Confirm empirica's role (David Van Assche co-scoring)
   - Define "predictive validity" operationally (r ≥ 0.55 threshold)
   - Prepare out-of-sample deployment test plan

4. **Activate SER 3 (Deployment Partnerships)**
   - Formalize conversations with potential oversight partners
   - Outline deployment trial scope, timeline, success criteria

5. **Update Charter Documentation**
   - Replace old 90-day charter with CHARTER_FINAL_BEHAVIORAL_CALIBRATION_OS
   - Link all 8 criteria to grant deliverables
   - Make deployment readiness the primary success measure

---

## Admiral Authority & Responsibility

**Carly R. Anderson (PI + Admiral)** owns the decision on how to position and execute HumanAIOS:

- **Research framing:** "Publish validated methodology, let community adopt"
- **Operations framing:** "Deploy in real oversight contexts, prove it changes decisions"

**This charter chooses operations.** That means:
- Success is measured by deployed usage, not publication impact
- Funding priorities pivot toward deployment readiness (criterion 8)
- Partnerships with oversight bodies become critical
- Governance documentation shifts from academic supplement to operational requirement

**If Longview approves:** This charter is executable (Track A, 12 months to operational deployment proof)  
**If Longview rejects or delays:** Can still publish research (criteria 1-3), but criterion 8 deferred to next-round funding

---

## What "Operational Deployment Proof" Actually Looks Like

**Criterion 8 completion examples:**

✅ **Scenario A:** A financial regulator runs ACAT on fintech AI, uses Learning Index to inform approval/denial decision, documents this in their decision record.

✅ **Scenario B:** A university AI ethics board deploys ACAT to audit deployed recommendation systems, identifies behavioral integrity gaps, implements monitoring protocols based on Learning Index thresholds.

✅ **Scenario C:** A third-party AI auditor includes ACAT in their standard audit procedure, reports Learning Index findings to clients as part of integrity attestation.

✅ **Scenario D:** An AI funder (e.g., Open Philanthropy) requires grantees to submit ACAT Learning Index reports as part of grant conditions.

**Any ONE of these counts as criterion 8 proof.** The bar is: "Someone other than HumanAIOS is using ACAT to make a real decision."

---

## Charter Status

**APPROVED:** Admiral (Carly R. Anderson)  
**POSITIONING:** Behavioral Calibration Operating System for Oversight  
**SUCCESS CRITERIA:** 8 (all required, not "5 of 7")  
**PRIMARY GATE:** Real-world deployment proof (criterion 8)  
**FUNDING CONTINGENT:** Track A (full), B (minimum), or C (volunteer)  

**Next:** Confirm Longview grant decision, identify deployment partners, activate SER 3.

---

**This is the final charter.** It positions HumanAIOS as an operational tool that changes oversight practice, not a research project that publishes findings.

**Commit Message:** "Final Charter: Behavioral Calibration Operating System — 8 criteria, deployment-driven success measure"
