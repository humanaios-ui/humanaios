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

## Recursive Learning & Gate POSTFLIGHT Protocol

**Principle:** Each gate produces learnings that inform the NEXT gate's design. No knowledge is left on the table.

### Gate POSTFLIGHT Findings (Self-Correcting Loop)

After each gate decision, Admiral logs a POSTFLIGHT finding that captures:
1. **Predicted:** What was supposed to happen (before the gate)
2. **Measured:** What actually happened
3. **Gap:** Difference between predicted and measured
4. **Learning:** What this reveals about the system
5. **Action:** How does this change the NEXT gate's design?

**Example: Gate 2 POSTFLIGHT (Month 6)**

Predicted: "Empirica cross-validation will show consistent r ≥ 0.55 across Claude, GPT-4, and custom models"

Measured: "Claude r=0.72, GPT-4 r=0.61, Custom r=0.58. Model architecture variance higher than anticipated."

Gap: "Criterion 4 predictive validity holds, but varies significantly by model family. Variance unaccounted for in original criterion 4 design."

Learning: "Oversight partners will deploy ACAT on their specific models. Single threshold Learning Index may not be sufficient; model-specific calibration may be needed."

Action: "Gate 3 (Month 9) partner selection should prioritize oversight bodies willing to trial model-specific Learning Index variants. Gate 4 deployment should measure whether model-specific calibration improves oversight utility."

**Logged via CLI:**

```bash
empirica finding-log \
  --finding "Gate 2 POSTFLIGHT (Month 6): Criterion 4 predictive validity established (r≥0.55 across 3 models), but model architecture variance (Claude>>Custom) higher than predicted. Oversight partners will need model-specific calibration guidance." \
  --impact 0.85 \
  --enabled-by "gate-2-postflight" \
  --informs "gate-3-partner-strategy" \
  --trajectory-type "gate_learning_→_next_gate_design" \
  --causal-strength 0.9 \
  --cross-session \
  --visibility shared
```

**Trajectory type:** `gate_learning_→_next_gate_design`
- Source: Gate N POSTFLIGHT findings
- Target: Gate N+1 design specification
- Causal strength: HIGH (prior gate evidence should shape next gate)
- Escalation: If no POSTFLIGHT finding created within 3 days after gate decision → escalate to Admiral
- Impact: Prevents silent knowledge loss; ensures each gate learns and adapts

### Gate Timeline with POSTFLIGHT Recursion

| Phase | Date | Event | POSTFLIGHT? |
|-------|------|-------|-------------|
| **Gate 1** | Aug 1 | Longview decision → Track A/B/C | ✅ Create Gate 1 POSTFLIGHT |
| **→ Phase 1** | Aug 15 | Track A activated, team hired | (Ongoing monitoring) |
| **Gate 2** | Aug 31 | Criterion 4 evidence → Proceed to Gate 3? | ✅ Create Gate 2 POSTFLIGHT |
| | | Gate 2 findings → inform Gate 3 partner strategy | ← Use POSTFLIGHT learnings |
| **→ Phase 2** | Sep 15 | Criterion 4 study running with model-variant focus | (Per Gate 2 POSTFLIGHT) |
| **Gate 3** | Oct 1 | Partner ready? Trial scope confirmed? | ✅ Create Gate 3 POSTFLIGHT |
| | | Gate 3 findings → inform Gate 4 trial protocol | ← Use POSTFLIGHT learnings |
| **→ Phase 3** | Oct 15 | Deployment trial starts with partner-specific protocol | (Per Gate 3 POSTFLIGHT) |
| **Gate 4** | Jan 1 | Trial success measured, criterion 8 proven? | ✅ Create Gate 4 POSTFLIGHT |
| | | Gate 4 findings → inform next-round strategy | ← Feeds into scaling plan |

### HumanAIOS ↔ Empirica Recursive Coordination

**Two feedback loops, interlocked:**

**Loop 1: HumanAIOS SMAG (organizational learning density)**
- Measure: Does research finding flow to implementation?
- Metric: Learning trajectory density (SMAG ledger)
- Cadence: Weekly (compounding)
- Currently: 26% density → improving via empirica CLI wiring

**Loop 2: Empirica Charter (deployment readiness)**
- Measure: Do charter criteria flow to oversight deployment?
- Metric: Criterion 8 readiness (Gate 4)
- Cadence: Gates every 2-4 months (discrete milestones)
- Connects to: SMAG via trajectory infrastructure

**Coordination point: Gate POSTFLIGHT findings feed back to SMAG**

When a gate reveals model variance (Gate 2 learning), create a finding in HumanAIOS:

```bash
empirica finding-log \
  --project-id humanaios \
  --finding "Charter Gate 2 reveals: ACAT criterion validity varies by model architecture (Claude r=0.72 >> Custom r=0.58). Recommend corpus expansion to increase model diversity coverage." \
  --impact 0.8 \
  --enabled-by "empirica-gate-2-postflight" \
  --informs "humanaios-corpus-expansion-criterion-5" \
  --trajectory-type "charter_learning_→_framework_refinement" \
  --cross-session \
  --visibility shared
```

**Result:** Gate 2 discovery (model variance) → HumanAIOS corpus targeted (more diverse models) → Criterion 5 improved → Gate 3 partner selection informed by better data.

**Loop closes and tightens:** Empirica → HumanAIOS → Empirica (recursive).

### Weekly Rhythm (With Recursive Checks)

**Monday 9am: SER 1 State Snapshot**
- Learning density per criterion (via SMAG)
- Any Gate POSTFLIGHT findings pending? (if gate closed recently)
- Has prior gate's POSTFLIGHT learning been incorporated? (check SER trajectories)

**Wednesday 2pm: Advisory Sync**
- Review POSTFLIGHT findings from most recent gate
- Adjust upcoming gate's design if learnings suggest it
- Check HumanAIOS SMAG improvements (is organizational learning accelerating?)

**Friday 4pm: Escalation & Loop Tightness Check**
- Any Gate POSTFLIGHT findings created yet? (if gate closed Mon-Fri)
- Any stalled SER 2 trajectories due to gate learnings not incorporated?
- Is HumanAIOS ↔ Empirica coordination tight? (are learnings flowing both directions?)

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

## SER Structure (Deployment-Aligned, Recursive)

### **SER 1: Research Execution & Grant Management**
- **State:** Criteria 1-7 progress tracking + Gate POSTFLIGHT learnings
- **Measure:** Which criteria are "ready for deployment"? Are prior gate learnings shaping current work?
- **Trajectory types:** 
  - `research_finding_→_criterion` (criteria 1-7 readiness)
  - `gate_learning_→_next_gate_design` (recursive loop closure)
- **Escalation:** 7 days if criterion blocking deployment work; 3 days if Gate POSTFLIGHT finding not created after gate decision
- **Loop closure:** After each gate, SER 1 verifies prior gate's POSTFLIGHT finding exists and is informing current phase

### **SER 2: Collaborator Coordination**
- **State:** David Van Assche (criterion 4), DeMarius Lawson (governance) + Gate POSTFLIGHT impacts
- **Measure:** Criterion-validity study progress, governance framework robustness; are gate learnings adjusting David/DeMarius' scope?
- **Trajectory types:**
  - `empirica_cross_validation_→_criterion_4` (David's work)
  - `governance_finding_→_dual_use_mitigation` (DeMarius' work)
  - `gate_learning_→_collaborator_adjustment` (how prior gates reshape David/DeMarius' work)
- **Escalation:** 14 days on stalled co-development; 7 days if prior gate's POSTFLIGHT learning not incorporated into David/DeMarius' plans

### **SER 3: Deployment Partnerships**
- **State:** Potential oversight partners interested in criterion 8 trial + Gate 2/3 POSTFLIGHT learnings embedded in trial design
- **Participants:** Regulator/institution, HumanAIOS, evaluator oversight
- **Measure:** Is a real-world deployment trial viable? Is trial protocol shaped by prior gates' learnings?
- **Trajectory types:**
  - `oversight_partner_feedback_→_protocol_update` (criterion 8 trial learning)
  - `gate_learning_→_trial_protocol_refinement` (recursive incorporation of Gate 2/3 discoveries)
- **Escalation:** 10 days on partnership conversations; 14 days if trial protocol not updated based on Gate 2/3 POSTFLIGHT learnings

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
   - **NEW:** Incorporate model-variance testing (per recursive learning protocol)

4. **Activate SER 3 (Deployment Partnerships)**
   - Formalize conversations with potential oversight partners
   - Outline deployment trial scope, timeline, success criteria
   - **NEW:** Prepare for Gate 2/3 POSTFLIGHT learnings to inform trial protocol

5. **Wire Gate POSTFLIGHT & Recursive Learning**
   - Define Gate 1 POSTFLIGHT template (Longview decision → Track selection)
   - Brief Admiral on Gate POSTFLIGHT protocol (create finding 3 days after gate decision)
   - Set up trajectory type `gate_learning_→_next_gate_design` in SMAG (Week 1, Day 3)
   - **NEW:** Add weekly rhythm check for POSTFLIGHT learnings incorporation

6. **Wire HumanAIOS ↔ Empirica Coordination**
   - When Gate 2 reveals model variance → log finding in humanaios project
   - When HumanAIOS SMAG learning density improves → log finding in empirica-foundation-evaluator project
   - Set `--visibility shared` on cross-project findings (so both practices see learnings)
   - **NEW:** Quarterly cross-project review: "Are both loops tightening?"

7. **Update Charter Documentation**
   - **DONE:** Replace old 90-day charter with CHARTER_FINAL_BEHAVIORAL_CALIBRATION_OS
   - **DONE:** Link all 8 criteria to grant deliverables
   - **DONE:** Make deployment readiness the primary success measure
   - **NEW:** Add Recursive Learning & Gate POSTFLIGHT section
   - **NEW:** Update SER structure to include Gate learning trajectories

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
**RECURSIVE LEARNING:** Gate POSTFLIGHT protocol active (self-correcting across gates)  
**COORDINATION:** HumanAIOS SMAG ↔ Empirica charter loops interlocked (organizational + deployment learning)

**Next:** Confirm Longview grant decision, identify deployment partners, activate SER 3, wire Gate POSTFLIGHT.

---

**This is the final charter.** It positions HumanAIOS as an operational tool that changes oversight practice, not a research project that publishes findings.

**Key innovations in this charter:**

1. **Operational positioning** — Success = oversight bodies deploying ACAT to make real decisions (not publication)
2. **8 criteria, all required** — Criterion 8 (deployment proof) is the defining gate; nothing is optional
3. **Deployment-driven decision gates** — Gate 2/3/4 measure readiness to deploy, not research completion
4. **Recursive learning protocol** — Each gate produces POSTFLIGHT findings that inform the next gate's design
5. **Dual-loop coordination** — HumanAIOS SMAG (organizational learning) ↔ Empirica charter (deployment readiness) interlocked
6. **Self-correcting system** — No silent knowledge loss; every gate's learning flows forward; no loop ever starts blind

**Commit Messages:**
- b40b432: "Final Charter: Behavioral Calibration Operating System — 8 criteria, deployment-driven success measure"
- [NEXT]: "Charter Enhancement: Add recursive learning & Gate POSTFLIGHT protocol + HumanAIOS ↔ Empirica coordination"
