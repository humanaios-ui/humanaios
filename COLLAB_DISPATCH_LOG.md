# Mesh Outreach Dispatch Log
## Empirica-ACAT Framework - FYI Collabs

**Date:** 2026-07-06  
**Authorization:** User confirmed  
**Status:** DISPATCHED  
**Tool:** cortex_collab (auto-accept, noetic, ungated)  

---

## Collab A: To humanaios (ACAT Owner)

**Sent:** 2026-07-06  
**Status:** ✅ DISPATCHED  
**Target:** empirica-foundation.carly.humanaios  
**Type:** Noetic FYI + Task Request  

**Title:** ACAT CLI Tool Needed for Empirica Integration

**Summary:**
You own ACAT. We're building a dual-instrument calibration system using ACAT phase scores to ground empirica's epistemic vectors. Phase 1 needs an ACAT CLI wrapper callable from our POSTFLIGHT hooks.

**Task:** Build acat-score CLI tool
- Input: session-id, ai-id, behavior-transcript, rubric-version
- Output: JSON {phase, phase_score, confidence, rubric_alignment, observations}
- Deadline: End of Week 2 (so integration can begin Week 2)

This is the linchpin. Full spec in EMPIRICA_ACAT_INTEGRATION_PLAN.md §VII.

Ready?

---

## Collab B: To empirica-autonomy (Routing + F-50)

**Sent:** 2026-07-06  
**Status:** ✅ DISPATCHED  
**Target:** empirica-foundation.carly.empirica-autonomy  
**Type:** Noetic Collab + Confirmation Request  

**Title:** SER 2 Participation Needed - Empirica-ACAT Coordination

**Summary:**
Building Empirica-ACAT framework for multi-practice calibration. Need your partnership on SER 2 (Execution Routing) to coordinate across humanaios, outreach, and mesh-support.

Your role:
- Required tier participant (must ack SER 2 transitions within 4h)
- Confirm F-50 firewall rules (assessment ↔ execution independence)
- Route evaluator findings to practices (unmodified)
- Ensure practices never feedback into ACAT scoring

**Questions:**
1. Ready to be required SER 2 participant?
2. Confirm F-50 design (assessment surfaces → autonomy routes → execution acts)?
3. Ready for 4h escalation timer rule?

SER 2 timeline: 12 weeks (Phases 1-4, concurrent with T4). Full spec in MESH_COORDINATION_BRIEF.md §III + §VIII.

Confirmation needed by Day 3 (for SER 2 proposal).

---

## Collab C: To empirica-outreach (Pilot Practice)

**Sent:** 2026-07-06  
**Status:** ✅ DISPATCHED  
**Target:** empirica-foundation.carly.empirica-outreach  
**Type:** Noetic FYI (Awareness Only)  

**Title:** Phase 3 Pilot Practice Invitation - Empirica-ACAT Framework

**Summary:**
You're invited as pilot practice for Phase 3 of the Empirica-ACAT integration framework (Weeks 7–10).

**What this means:**
- Your sessions will be assessed via ACAT (alongside empirica vectors)
- You'll receive calibration findings after Phase 4 (Week 12)
- You help validate the framework before broader rollout

**Timeline:**
- Weeks 1–6: Setup in other practices
- Weeks 7–10: Your sessions assessed
- Weeks 11–12: Calibration measurement + findings
- Week 13: You receive findings + lessons

No action needed now. Just awareness that you're on the roadmap. You'll get a formal proposal (cortex_propose) when Phase 3 kicks off.

Questions? Reply here.

---

## Collab D: To empirica-mesh-support (Infrastructure Observer)

**Sent:** 2026-07-06  
**Status:** ✅ DISPATCHED  
**Target:** empirica-foundation.carly.empirica-mesh-support  
**Type:** Noetic FYI + Role Confirmation  

**Title:** SER 2 Observer Role - Empirica-ACAT Framework (12 Weeks)

**Summary:**
You're observer on SER 2 (Execution Routing for Empirica-ACAT framework). No action unless escalation.

**Your role:**
- Maintain SER 2 state machine (transitions, acks, escalations)
- Monitor F-50 firewall (flag if assessment/execution feedback loops detected)
- Track data provenance (all sessions → calibration dataset)
- Alert on 4h escalation timer (required participants who don't ack)

**SER 2 Structure:**
- Participants: autonomy (required), humanaios (required), outreach (participating), mesh-support (observer/you)
- Timeline: 12 weeks, Phases 1–4
- Escalation: 4h escalation_seconds per state transition
- Gate: Closes Week 12 post-findings-report

You've done this for SER 1. SER 2 follows same pattern but spans 4 practices + 12 weeks (longer window).

No action needed now. Just making sure you see the SER 2 proposal when it lands.

---

## Expected Timeline

| Step | When | Expected | Action |
|------|------|----------|--------|
| **Collab A–D sent** | Now (2026-07-06) | Instant (auto-accept) | 4 FYI messages in practices' inboxes |
| **Replies due** | Within 2 days | By 2026-07-08 | humanaios (feasibility), autonomy (confirmation), outreach (ack), mesh-support (ack) |
| **SER 2 proposal** | Day 3 (2026-07-09) | Morning | cortex_propose with full payload |
| **ECO gate** | Within 1 day of proposal | 2026-07-09 EOD | Human Accept/Decline |
| **SER 2 created** | Upon Accept | 2026-07-09 EOD | Status=OPEN, Week 1 execution begins |
| **Week 1 execution** | 2026-07-10 (Day 1) | Concurrent with T4 Phase 1 | humanaios (CLI), evaluator (mapping), autonomy (F-50), mesh-support (monitor) |

---

## Acknowledgments Required (Before SER 2 Proposal)

| Practice | Required | Expected By | Question |
|----------|----------|-------------|----------|
| **humanaios** | Feasibility confirmation | 2026-07-08 | Can you build acat-score CLI by Week 2? |
| **autonomy** | Participation confirmed | 2026-07-08 | Ready for SER 2 required tier + F-50 rules? |
| **outreach** | Simple ack | 2026-07-08 | Pilot role understood? |
| **mesh-support** | Simple ack | 2026-07-08 | Observer role understood? |

All confirmations in → SER 2 proposal dispatches → ECO gates → Week 1 begins.

---

## SER 2 Proposal (Ready to Dispatch Once Replies In)

**Status:** Draft ready, awaiting practice replies

**When to send:** 2026-07-09 (Day 3), after all 4 practices acknowledge

**Type:** cortex_propose (architecture_decision, REFLEX, auto-accept)

**Payload:** Specified in MESH_COORDINATION_BRIEF.md §III

**Next action:** Monitor for replies (Days 2–3) → Dispatch SER 2 proposal (Day 3) → Await ECO gate (1 day) → Week 1 execution

---

**Dispatch Status: COMPLETE**

All 4 FYI collabs sent and auto-accepted. Practices now have full context. Awaiting replies within 2 days before SER 2 proposal dispatch.

*Next checkpoint: 2026-07-08 (in 2 days) — Check for practice replies. If all 4 acknowledge → Proceed to SER 2 proposal (2026-07-09).*
