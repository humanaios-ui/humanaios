# Advisor/Project Manager Node — HumanAIOS Engagement

**Version:** 1.0  
**Date:** 2026-07-17  
**Status:** Specification (ready to instantiate)  
**Parent Practice:** empirica-foundation.carly.empirica-foundation-evaluator  
**Primary Engagement:** HumanAIOS LLC (ACAT research + governance)  
**External Advisors:** Alex Lee Berlin (REVBY), David Van Assche (empirica)  
**Operational UI:** HAIOSCC (GitHub LastingLightAI/HAIOSCC)

---

## Purpose

The advisor/PM node enforces the disciplined 90-day research and feedback process outlined in Berlin's April 17 Research Plan. It acts as the **coordination and decision engine** between:
- **Evaluator seat** (independent assessment, framework authority)
- **HumanAIOS project** (active research, governance implementation)
- **External advisors** (Berlin/REVBY strategic guidance, empirica technical convergence)
- **Operational surface** (HAIOSCC command center for real-time tracking)

This node is NOT a separate practice. It is a **role + sub-system** within the evaluator seat that specializes in active project governance and advisor coordination.

---

## Charter & Authority

**Charter Duration:** Day 69–90 (21 days remaining, close date July 16, 2026)

**Authority Scope:**
- Track and enforce hard deadlines (Longview RFPs, arXiv, charter close)
- Implement the 90-day disciplined process (Berlin's phases 1–4)
- Manage SER-based coordination with external advisors
- Maintain the decision log and corrections ledger (visible learning)
- Gate financing discussions (3 conditions must be met before readiness)
- Escalate blockers to evaluator seat (Admiral authority)

**What This Node Does NOT Do:**
- Make final decisions (Admiral/evaluator makes those)
- Approve financing (BDFL David + Berlin gate that)
- Modify HumanAIOS governance (that's Night/Z2's call)
- Replace Berlin or empirica in their advisory roles

**What This Node DOES Do:**
- Synthesize inputs from multiple advisors into coherent recommendation
- Maintain visible state of the charter (clock, goals, blockers)
- Implement the structured feedback process Berlin outlined
- Document why decisions were made (decision log)
- Surface when assumptions aren't holding (corrections ledger)

---

## Operating Model

### Coordination Primitive: SER (Shared Epistemic Record)

The advisor/PM node manages THREE persistent SERs:

#### SER 1: Charter & Deadline Tracking
**Participants:**
- empirica-foundation.carly.empirica-foundation-evaluator (required, node operator)
- HumanAIOS.night.humanaios (required, project owner)
- empirica-foundation.carly.empirica-autonomy (participating, governance oversight)

**State:**
- Charter clock (Day N/90, remaining days to July 16)
- Hard deadlines (Longview RFPs, arXiv gate, charter close)
- Milestone status (phases 1–4 of Berlin's 90-day process)
- Escalation log (blockers, risks, decisions)

**Escalation:** 13h on stalled items

#### SER 2: Berlin/REVBY Advisory Sync
**Participants:**
- empirica-foundation.carly.empirica-foundation-evaluator (required, receiver)
- revby.alex-berlin (required, advisor — external contact)
- empirica-foundation.carly.empirica-autonomy (observer)

**State:**
- Call agendas + pre-briefs (30/60-day cadence)
- All 5 recommendations status (addressed, evidence, verification)
- Three financing gate conditions (repeatable method, narrower use case, controlled study N=525)
- Feedback intake & synthesis (what reviewers said, what changed)

**Escalation:** None (asynchronous advisory channel)

#### SER 3: empirica Technical Convergence (David Van Assche)
**Participants:**
- empirica-foundation.carly.empirica-foundation-evaluator (required, evaluator seat)
- empirica.david.empirica-cortex or empirica-autonomy (required, technical convergence)

**State:**
- Admiral seat offer status (Night decision pending)
- ACAT + empirica cross-instrument findings (independent confirmation)
- Data harmonization (two-corpus rule, HF frozen vs Supabase live)
- Governance alignment (F-50 firewall, SER structure adoption)

**Escalation:** 24h on activation (if accepted)

---

## The 90-Day Disciplined Process (Berlin's Framework)

### Phase 1: Public Explanation Simplification (Days 1–30)
**Goal:** Produce 3–5 foundational pages that explain what the project is, what it solves, what it is NOT yet.

**Deliverables:**
- Simplified README (one core idea, one problem statement)
- Plain-language "what we are" page
- "What we are NOT yet" page (explicitly state: not a finished product, not peer-validated, not financing-ready)
- Roadmap (visual or structured)
- 3–5 open research questions

**Feedback:** Nontechnical readers (do they understand the core idea?)

**Decision Log Entry:** Why these framings over others? What was dropped?

### Phase 2: Public Structure Build (Days 31–60)
**Goal:** Formalize GitHub + research archive + one narrow demo

**Deliverables:**
- GitHub repo formalized (Issues for tasks, Discussions for open questions)
- OSF preregistration live (H-FORMAT-01)
- One narrow demo on HuggingFace (ACAT lightweight assessment, NOT the full product)
- Feedback intake form (structured questions, not "what do you think?")
- Corrections ledger (visible, dated, linked to changes)

**Feedback:** Technically literate reviewers (is the method coherent? assumptions clear? methodology sound?)

**Decision Log Entry:** Which demo idea survived, which were deprioritized? Why?

### Phase 3: Targeted Feedback Rounds (Days 61–75)
**Goal:** Run structured feedback with 3–4 defined groups

**Cohorts:**
- **Nontechnical readers** (2–3 people): Can you explain the core idea back to us?
- **Technically literate reviewers** (2–3 people): Is the method reviewable? What assumptions need testing?
- **Potential users** (2–3 people): Would this solve a problem in your workflow? What evidence would you need?
- **Informed peers/observers** (2–3 people): Which claims are strongest? Which overstated? Which sound like research vs. product?

**Method:** Structured written feedback (pre-defined questions, not open-ended praise)

**Recording:** Consistent format (who, what they understood, where confusion arose, what they'd change)

**Decision Log Entry:** What did each cohort teach us? How did we synthesize?

### Phase 4: Decision-Making & Refinement (Days 76–90)
**Goal:** Consolidate feedback, make hard choices about what to keep/drop

**Decisions:**
- Which explanation is clearest? Use that, deprecate others.
- Which use case appears most credible? Narrow the story to that.
- Which outputs seem most meaningful? Deprioritize the rest.
- What should we NOT say (for now)?

**Outputs:**
- Updated public materials (reflecting feedback)
- Visible record of what changed and why
- Three financing gate conditions assessment (met/not-met/pathway-to-met)
- Next 90-day plan (if charter is extended)

**Decision Log Entry:** Why did we choose this narrower positioning? What did we learn from rejecting the broader vision?

---

## Real-Time Tracking: HAIOSCC Integration

HAIOSCC serves as the **operational command center** for the advisor/PM node.

### Dashboard Layers

#### Layer 1: Charter Clock
- Current day (N/90)
- Days remaining to July 16 close
- Phase progress (1–4, % complete)
- Hard deadlines with countdown

#### Layer 2: Recommendations Status (All 5 Berlin Critiques)
| # | Critique | Status | Evidence | Verified | Last Updated |
|---|----------|--------|----------|----------|--------------|
| 1 | Research design rigor | ✅ Addressed | H-FORMAT-01 finalized, N=525 | Yes | Jun 24 |
| 2 | Independent verification | 🟡 In progress | OSF preregistration draft | Pending | Jun 24 |
| 3 | External validation | ✅ Addressed | GitHub Issues, empirica convergence | Yes | Jun 24 |
| 4 | Governance & audit | ✅ Addressed | GOVERNANCE.md v6.4.2, 22 CI tests | Yes | Jun 24 |
| 5 | Value proposition clarity | ✅ Addressed | 3-layer value stack + market data (15k jailbreaks) | Yes | Jun 24 |

#### Layer 3: Financing Gate Conditions (NOT YET MET)
| # | Condition | Current State | Pathway to Met | Target |
|---|-----------|---------------|-----------------|--------|
| 1 | Repeatable method externally validated | In progress | Phase 3 feedback rounds + Phase 4 consolidation | Day 75 |
| 2 | Narrower use case established | In progress | Phase 4 decision consolidation | Day 75 |
| 3 | Controlled study data (H-FORMAT-01 N=525) | Not started | Funding trigger (financing gate prerequisite) | Post-charter |

#### Layer 4: Hard Deadlines
- Longview RFP (AI Power Concentration): July 2 — Status: Draft v0.2, awaiting Z2 ratification
- Longview RFP (Digital Minds): July 10 — Status: Stub
- Charter close: July 16 — Status: POC goals + arXiv gate tracking
- arXiv submission: On hold — Status: Manual review hold + N=524 gate

#### Layer 5: Decision Log (Visible Learning)
- Weekly entries: what material was shown, who reviewed, what they understood, where confusion arose, what changed in response
- Searchable by date, reviewer cohort, recommendation #, phase

#### Layer 6: Corrections Ledger (Visible Accountability)
- Dated entries: assumption that didn't hold, data error discovered, claim overturned, external feedback that shifted positioning
- Linked to GitHub Issues + commits that corrected them

---

## Weekly Rhythm

### Monday: State Snapshot
- Update charter clock
- Flag any deadline risks (red/amber/green)
- Summarize last week's feedback (if in Phase 3)
- Escalate blockers to evaluator seat

### Wednesday: Advisory Sync (as scheduled)
- Berlin call or prep brief
- empirica convergence check (if applicable)
- Decision log entry (what was learned? what changed?)

### Friday: Corrections & Next-Week Preview
- Any corrections ledger updates?
- Phase progress assessment
- Next week's focus + required inputs

---

## Escalation Thresholds

**To Admiral/Evaluator (same-day):**
- Financing readiness triggered before Phase 4 consensus (pulls up the timeline)
- External advisor (Berlin, empirica) signals fundamental blocker
- Hard deadline at risk (< 7 days and not on track)
- Corrections ledger reveals assumption invalidation (requires re-framing)

**To Autonomy/Governance:**
- GOVERNANCE.md self-audit triggers correction (governance discipline)
- Financing gate condition newly met (signals state change)
- Research design cannot be executed within charter (scope re-negotiation)

**To Night/Z2 (HumanAIOS owner):**
- Weekly state snapshot (FYI, no action required)
- Phase transitions (here's what feedback says, here's what we should do)
- Decision consolidation (Phase 4: here's the narrowed positioning, do you agree?)

---

## Success Criteria (End of Charter, Day 90)

✅ **Process discipline:**
- All 4 phases of Berlin's 90-day process completed and documented
- Feedback from all 4 cohorts collected and synthesized in decision log
- Corrections ledger visible and linked to changes
- Weekly state snapshots maintained throughout

✅ **External validation:**
- Berlin (REVBY) provides sign-off that the narrowed positioning is credible
- At least one technically literate reviewer gives methodological thumbs-up (or identifies specific improvement pathways)
- Potential users indicate a use case they'd consider (even if post-charter)

✅ **Financing readiness assessment:**
- Conditions 1 & 2 clearly met OR not-met with named pathways
- Condition 3 explicitly deferred to post-charter (H-FORMAT-01 execution)
- Berlin + evaluator alignment on next stage (financing call or extended research phase)

✅ **Narrower positioning emerged:**
- Public materials reflect one primary use case (not the full enterprise vision)
- Roadmap clearly distinguishes Phase 0 (current research) from Phase 1+ (future)
- "What we are NOT yet" page is explicit and credible

❌ **Failure mode to avoid:**
- Charter close without feedback synthesis (decisions made without external input)
- Corrections ledger stays private (defeats the visible learning principle)
- All 5 recommendations addressed on paper but not validated externally (same-team echo chamber)

---

## Instantiation Steps

### Immediate (This Week)
1. Create SER 1 (Charter & Deadline Tracking) via cortex_propose
2. Activate HAIOSCC dashboard (Layer 1–6 above)
3. Confirm Berlin advisory cadence (already on June 25 schedule, next call TBD)
4. Reach out to David Van Assche on Admiral seat + SER 3 activation

### Week 2 (By July 25)
1. Phase 1 deliverables checkpoint (simplified public explanation)
2. Phase 2 structure assessment (GitHub formalized, demo scoped)
3. Feedback intake form live
4. First decision log entry (what happened this week, what changed)

### Weeks 3–4 (July 30–Aug 13, into Phase 3)
1. Phase 3 feedback rounds begin (cohort selection, scheduled interviews)
2. Weekly state snapshots + corrections ledger live
3. Berlin mid-project call (July 30 or Aug 1 TBD)
4. Synthesis of Phase 3 feedback

### Week 5 (Aug 14–15, pre-close)
1. Phase 4 consolidation (narrowed positioning, financing gate assessment)
2. Final decision log synthesis
3. Berlin wrap-up call (what did we learn, what's next?)
4. Post-charter recommendation to evaluator seat

---

## Node Roles

**Operator:** Claude Code (empirica-foundation-evaluator seat)  
**Project Owner:** Night (empirica-foundation-evaluator, Z2)  
**Technical Convergence:** David Van Assche (empirica-autonomy or empirica-cortex)  
**Strategic Advisor:** Alex Lee Berlin (REVBY, external)  
**Admiral Authority:** Carly R. Anderson (empirica-foundation-evaluator)

---

## References

- Berlin Advisory (June 25, 2026): 30/60-day check-in
- Berlin Research Plan (April 17): All 5 Recommendations.docx
- HumanAIOS Charter: Day 69/90, close July 16, 2026
- HAIOSCC UI: https://github.com/LastingLightAI/HAIOSCC
- REVBY Engagement: https://revby.co/dashboard/projects/MQAAAAEG8S75

---

**Status:** Specification Ready for Implementation  
**Next Action:** Admiral approval + SER instantiation
