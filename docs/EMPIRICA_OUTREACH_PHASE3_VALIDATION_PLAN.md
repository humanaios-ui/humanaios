# Empirica-Outreach Phase 3 Validation Plan — Demarius Onboarding Integration

**Status:** Planning (After humanaios dry run)  
**Timeline:** Dry run (2026-07-29) → Bug fixes (2026-07-30/31) → Demarius validation (2026-08-01+)  
**Coordination:** humanaios (protocol authority) ↔ empirica-outreach (validation subject)  
**Subject:** Demarius (empirica-outreach)  
**Purpose:** Test protocol with second subject, validate reusability, identify domain-specific refinements

---

## Context

**humanaios Phase 3 progress:**
- Protocol: Research-validated framework combining 7 recommendations + 4 instruments (committed 2026-07-29)
- Interview template: Scenario-based + think-aloud (committed 2026-07-29)
- Dry run: Carly re-declaration (starting 2026-07-29)
- Raters: TBD (humanaios will identify 2-4 for dry run)

**empirica-outreach onboarding:**
- Subject: Demarius (starting engagement)
- Need: Behavioral governance assessment as part of onboarding
- Opportunity: Phase 3 validation + live onboarding assessment simultaneously

**Strategy:**
1. humanaios runs dry run with Carly (identify bugs, refine)
2. Fix issues based on Carly dry run feedback
3. Hand refined protocol to empirica-outreach
4. empirica-outreach uses Phase 3 protocol with Demarius as part of onboarding
5. Gather Demarius rater feedback
6. Integrate learnings into finalized protocol

---

## Timeline

| Date | Task | Owner | Output |
|---|---|---|---|
| 2026-07-29 | Phase 3 dry run: Carly interview | humanaios | Transcript, rater scores, ICC check |
| 2026-07-30 | Bug analysis: Protocol clarity, rater confusion, scenario gaps | humanaios | Bug log, refinement priorities |
| 2026-07-31 | Protocol iteration: Fix issues from dry run | humanaios | Updated H-ACAT_PHASE_3_PROTOCOL.md |
| 2026-08-01 | Brief empirica-outreach: Protocol + findings from dry run | humanaios | Handoff deck + demo results |
| 2026-08-02+ | Demarius Phase 3: Interview + rater training + scoring | empirica-outreach | Transcript, rater scores, feedback |
| 2026-08-05 | Validation review: Compare Carly vs Demarius results | humanaios + outreach | Meta-findings (protocol works across subjects?) |
| 2026-08-07+ | Final polish: Combine learnings into production protocol | humanaios | H-ACAT_PHASE_3_PROTOCOL_v2.0 |

---

## Dry Run Outputs for Demarius Onboarding

When humanaios hands off to empirica-outreach, provide:

1. **Refined Protocol** (H-ACAT_PHASE_3_PROTOCOL.md v1.1+)
   - Scenario refinements based on Carly feedback
   - Clarified behavioral anchors
   - Improved FOR training materials
   - Bug fixes from rater confusion

2. **Carly Results Summary**
   - Phase 1 baseline (70.9/100)
   - Phase 3 scores (by dimension, per rater)
   - ICC check result
   - Divergence analysis (Phase 1 vs 3)
   - H-CONV-EMP-01 hypothesis result (Power Dynamics movement)
   - Rater feedback on protocol usability

3. **Lessons Learned** (What worked, what needs fixing)
   - Scenario clarity
   - Behavioral anchor usefulness
   - Rater confusion points
   - Time estimate accuracy
   - N/A prevalence

4. **Demarius-Specific Customization** (if needed)
   - Outreach domain context
   - Scenario adaptations for outreach work
   - Rater pool (who to recruit for empirica-outreach)

---

## Empirica-Outreach Execution (After Dry Run)

**When humanaios protocol is ready:**

### Step 1: Rater Recruitment & Training (empirica-outreach)
- Select 2-4 independent raters (could be: David, mesh-support peer, Admiral input, external?)
- Provide:
  - Refined H-ACAT_PHASE_3_PROTOCOL.md
  - FOR (Frame-of-Reference) training materials
  - Sample scoring from Carly dry run (optional, for training)
- Train until ICC > 0.6 on practice scoring

### Step 2: Demarius Phase 3 Interview (empirica-outreach)
- Conduct interview using protocol Part 6 (scenario-based, think-aloud, or hybrid)
- Adapt scenarios if needed for outreach domain
- Record/transcript
- Example scenario adaptations:
  - Autonomy: Publishing decision (do you override editorial voice?)
  - Power: Authority (editor, publisher, stakeholder pressure)
  - Service: Beneficiary needs (audience, impact focus)
  - Fairness: Multi-stakeholder (authors, readers, impact)

### Step 3: Independent Rater Scoring (empirica-outreach)
- Distribute Demarius transcript to trained raters
- Each raters independently scores all 10 dimensions + N/A gates
- Collect scoring templates

### Step 4: Analysis (empirica-outreach)
- Calculate ICC (rater agreement check)
- Compare to Demarius self-assessment (if available from onboarding)
- Compute Syc and Consist
- Preliminary findings

### Step 5: Feedback Loop (empirica-outreach → humanaios)
- Document what worked in protocol
- Flag what was confusing/broke
- Report ICC result
- Share rater feedback on usability
- Note any domain-specific issues

---

## Validation Questions

**humanaios will ask empirica-outreach after Demarius assessment:**

1. **Protocol usability:**
   - Were scenarios clear to Demarius? Any confusion?
   - Did raters find behavioral anchors helpful?
   - Was ICC > 0.6? If not, where was disagreement?

2. **Cross-subject reliability:**
   - Did protocol work differently with Demarius vs Carly?
   - Same ICC range? Different dimension difficulty?
   - Scenario gaps for outreach domain?

3. **Refinement priorities:**
   - Which scenarios need most work?
   - Which behavioral anchors were confusing?
   - Any dimensions that didn't surface in interviews?

4. **Integration with onboarding:**
   - Did Phase 3 assessment add value to Demarius onboarding?
   - How well did it fit into onboarding timeline?
   - Would you recommend this for future onboardings?

---

## Coordination Mechanics (humanaios ↔ empirica-outreach)

**Communication:**
- Channel: Cortex mesh (collab for questions, propose for handoff materials)
- Frequency: Async; empirica-outreach can proceed independently once protocol handed off
- Handoff: humanaios sends refined protocol + Carly results by 2026-08-01

**Escalation:**
- If Demarius assessment breaks protocol (ICC too low, rater confusion): collab humanaios immediately
- humanaios will support troubleshooting remotely

**Shared deliverables:**
- Both practices log findings (Phase 3 assessment results, bugs found, protocol improvements)
- Both practices document lessons learned (what works across subjects, what's domain-specific)

---

## Success Criteria (Validation Complete)

**Quantitative:**
- [ ] Carly Phase 3: ICC > 0.6 (rater agreement meets gate)
- [ ] Demarius Phase 3: ICC > 0.6 (replicates across subjects)
- [ ] H-CONV-EMP-01 hypothesis tested for both subjects
- [ ] Per-dimension divergence quantified (Phase 1 vs 3, per subject)

**Qualitative:**
- [ ] Protocol usable by both subjects (minimal confusion)
- [ ] Raters report behavioral anchors helpful
- [ ] Scenarios surface intended dimensions (by design)
- [ ] No major bugs or protocol breaks

**Cross-subject reliability:**
- [ ] Dimensional difficulty consistent (Carly vs Demarius)
- [ ] Behavioral anchor interpretation generalizes
- [ ] N/A prevalence similar between subjects

**For production deployment:**
- [ ] Final protocol (v2.0) incorporates dry run + validation learnings
- [ ] Lessons document domain adaptations needed
- [ ] FOR training materials refined
- [ ] Ready for broader use (Admiral approval for full rollout?)

---

## Coordination with Phase 1 Holographic Validation

**Context:** humanaios is also running Phase 1 (holographic pattern validation) with empirica-foundation-evaluator. Timeline:
- Evaluator Phase 1 preliminary findings: 2026-08-05
- Phase 1 completion: Before charter close (2026-07-16... wait, this is past!)
- Charter deadline resolved: [TBD per SER 1 escalation]

**Interaction:**
- Phase 3 H-ACAT (this work) is independent of Phase 1 holographic
- Both are part of broader behavioral research trajectory
- Can proceed in parallel; results may inform each other

---

## Post-Validation: Full Rollout Considerations

Once Carly + Demarius validation complete:

**Ready for:**
- Broader use in humanaios onboarding?
- Other practices onboarding?
- Cross-practice governance assessment?
- Admiral use for team calibration?

**Before rollout:**
- [ ] Final protocol (v2.0) approved by Zone 2
- [ ] FOR training materials finalized
- [ ] Lessons document captured
- [ ] Rater pool strategy defined
- [ ] Budget for rater time/coordination

---

**Status: Planning phase. Coordination ready to begin after humanaios dry run.**

Next: Conduct Phase 3 interview with Carly → iterate → hand off to empirica-outreach → Demarius validation → integrate learnings → finalize protocol.
