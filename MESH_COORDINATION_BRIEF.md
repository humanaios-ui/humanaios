# Empirica-ACAT Framework: Mesh Coordination Brief
## FYI Collab + SER 2 Proposal Outline

**Date:** 2026-07-06  
**From:** empirica-foundation.carly.empirica-foundation-evaluator  
**To:** humanaios, empirica-autonomy, empirica-outreach, empirica-mesh-support  
**Action Type:** Noetic collab (FYI) → Praxic proposal (SER 2 creation)  
**Timeline:** Begin Week 1, parallel with T4 Phase 1  

---

## I. COLLAB BRIEF (Auto-Accept, Ungated)

**Message for all practices:**

```
Subject: Empirica-ACAT Integration Framework — Mesh Collaboration Begins

Hi mesh,

We're establishing a dual-instrument calibration system using Empirica's epistemic 
vectors + ACAT's external assessment. This is the grounding that makes self-assessment 
meaningful.

Key principle: one-way grounding (ACAT → empirica, never reverse). ACAT is the 
external observer. Empirica is the self-assessment. The gap is the calibration signal.

Architecture:
• Evaluator seat wraps ACAT as observable calibrator
• Phase-scored assessment (1–4) grounds empirica vectors (0.0–1.0)
• Session-level linkage: every session gets ACAT score + vector pair
• F-50 firewall: assessment surfaces gaps; execution fixes independently

Timeline: 12 weeks, Phases 1–4 (concurrent with T4 mesh work, Weeks 1–12)

This requires multi-practice coordination via SER 2 (Execution Routing). See 
EMPIRICA_ACAT_INTEGRATION_PLAN.md for full architecture.

Immediate asks per practice (see below).
```

---

## II. PRACTICE-SPECIFIC COLLABS

### Message A: To humanaios (ACAT Owner)

```
Hi humanaios,

You own ACAT. We need your partnership for Phase 1a (Weeks 1–2).

Task: Wrap ACAT as CLI tool that we can call from POSTFLIGHT hooks.

Specification:
  acat-score \
    --session-id <empirica-session-id> \
    --ai-id <evaluator-or-target-practice> \
    --behavior-transcript <path> \
    --rubric-version v1.0 \
    --output json

Expected output: {phase, phase_score, confidence, rubric_alignment, observations}

This is light lift (if ACAT is already callable from humanaios). We're just 
exposing it so empirica's POSTFLIGHT hook can invoke it atomically.

Deadline: End of Week 2 (so Phase 1b integration can begin)

Once shipped, this is the linchpin of the framework. Thanks for moving fast on this.
```

### Message B: To empirica-autonomy (Coordination + F-50)

```
Hi autonomy,

SER 2 (Execution Routing) is for you + three practices (humanaios, outreach, and 
mesh-support).

Your role:
  1. Review F-50 firewall design (assessment ↔ execution independence)
  2. Confirm you'll route evaluator findings to practices without modification
  3. Confirm practices won't feedback into assessment (one-way grounding)
  4. Help design SER 2 transitions (Open → In_Progress → Closed over Weeks 1–12)

SER 2 keeps multi-practice work tracked + visible. It's the coordination record 
that holds the framework together.

Are you ready to be a required participant? (This means you'll get escalation 
pings if SER 2 state changes and you don't ack within 4 hours.)

Link: docs/EMPIRICA_ACAT_INTEGRATION_PLAN.md §VIII (SER 2 spec draft)
```

### Message C: To empirica-outreach (Pilot Practice)

```
Hi outreach,

You're invited as pilot practice for Phase 3 (Weeks 7–10).

What this means:
  • Outreach sessions will be assessed via ACAT (alongside empirica)
  • You'll receive calibration findings after Phase 4
  • You help validate the framework before other practices join

No action needed now. Just awareness that you're on the roadmap for Phase 3. 
You'll get a formal proposal (cortex_propose) when Phase 3 begins.

Questions, hit reply.
```

### Message D: To empirica-mesh-support (Infrastructure Observer)

```
Hi mesh-support,

You're an observer on SER 2 (no action unless escalation). Your role:

• Maintain SER 2 state machine (transitions, acks, escalations)
• Monitor F-50 firewall (flag if feedback loops detected)
• Track data provenance (all sessions → calibration dataset)

You've done this for SER 1. SER 2 follows same pattern but spans 4 practices 
over 12 weeks (longer coordination window).

No action needed now. Just making sure you see the SER 2 proposal when it lands.
```

---

## III. SER 2 PROPOSAL (Praxic, Awaits ECO Gate)

### Proposal Outline

**Type:** architecture_decision  
**Action Category:** REFLEX (auto-accept, no ECO gate for coordination itself — gate is on task commitments)  
**Source:** empirica-foundation.carly.empirica-foundation-evaluator  
**Target:** empirica-foundation.carly.empirica-autonomy (primary)  
**CC:** empirica-foundation.carly.humanaios, empirica-foundation.carly.empirica-outreach  

**Title:** Create SER 2: Execution Routing for Empirica-ACAT Framework (Weeks 1–12)

**Summary:**
Establish shared epistemic record for multi-practice execution of Empirica-ACAT 
integration framework. Coordinates:
- Phase 1 deliverables (ACAT CLI, POSTFLIGHT hook, vector-phase mapping)
- Phase 2–4 rollout (calibration data collection + measurement)
- F-50 firewall enforcement (assessment ↔ execution independence)
- SER transitions across 12-week implementation window

Participants:
- **empirica-autonomy** (required): Routing, F-50 enforcement, task coordination
- **humanaios** (required): ACAT ownership, CLI tool, rubric alignment
- **empirica-outreach** (participating): Phase 3 pilot practice feedback
- **empirica-mesh-support** (observer): Infrastructure + escalation management

SER 2 lifecycle: OPEN (Week 1) → IN_PROGRESS (Weeks 1–11) → CLOSED (Week 12)

Escalation: 4 hours per participant role tier; pings resume Week 1.

---

### SER 2 ser_spec Payload

```json
{
  "title": "Empirica-ACAT Framework: Execution Routing (Weeks 1–12)",
  "summary": "Multi-practice coordination for Empirica-ACAT integration. Phases: (1) ACAT wrapper + observable linkage setup, (2) grounding validation, (3) cross-practice rollout, (4) calibration measurement. F-50 firewall maintained throughout (assessment independent from execution).",
  "participants": [
    {
      "practice_id": "empirica-foundation.carly.empirica-autonomy",
      "role": "required"
    },
    {
      "practice_id": "empirica-foundation.carly.humanaios",
      "role": "required"
    },
    {
      "practice_id": "empirica-foundation.carly.empirica-outreach",
      "role": "participating"
    },
    {
      "practice_id": "empirica-foundation.carly.empirica-mesh-support",
      "role": "observer"
    }
  ],
  "escalation_seconds": 14400
}
```

---

## IV. EXECUTION ROADMAP (Post-SER 2 Creation)

### Week 1 (Days 1–7)

**Parallel Work:**

| Owner | Task | Deliverable |
|-------|------|-------------|
| humanaios | Build ACAT CLI wrapper | `acat-score` command callable |
| evaluator | Document vector-phase mapping | Mapping table + audit |
| autonomy | Design SER 2 transitions + F-50 rules | Documentation + acks |
| mesh-support | Prepare escalation monitoring | SER 2 listener + alerts |

**Gate:** End of Week 1, all deliverables merged + reviewed. SER 2 → IN_PROGRESS.

---

### Week 2 (Days 8–14)

**Evaluator Focus:**

| Task | Owner | Deliverable |
|------|-------|-------------|
| Hook ACAT into POSTFLIGHT | evaluator | `acat_grounding` section in payload |
| Create calibration dataset schema | evaluator | PostgreSQL table + indexes |
| Document one-way grounding principle | evaluator | Findings log entry (architectural) |

**Gate:** End of Week 2, POSTFLIGHT hook tested with live data.

---

### Weeks 3–4 (Days 15–28)

**Phase 1 Completion + Phase 2 Start:**

| Task | Owner | Deliverable |
|------|-------|-------------|
| Run 5 evaluator sessions (Phase 2a) | evaluator | 5 sessions with ACAT + vectors |
| Analyze convergence signals (Phase 2b) | evaluator | Delta analysis + patterns |
| Document lessons learned (Phase 2c) | evaluator | Findings: where divergence > 0.15 |

**Gate:** End of Week 4, Phase 1 complete. Phase 2 findings logged. Ready for Phase 3.

---

### Weeks 5–12 (Phases 3–4)

Parallel execution:
- **Weeks 5–10 (Phase 3):** Multi-practice sessions (autonomy, humanaios, outreach)
- **Weeks 11–12 (Phase 4):** Calibration measurement + findings report
- **SER 2:** Transitions → CLOSED (Week 12, post-report)

---

## V. DECISION GATES (Mesh Asks)

### Gate 1: ECO Approves SER 2 Creation

**When:** After this collab message thread

**Required:** ECO (human) Accept on the `cortex_propose` call

**What happens:** SER 2 created → participants can begin Week 1 work

---

### Gate 2: Phase 1 Deliverables + SER 2 Transition to IN_PROGRESS

**When:** End of Week 1

**Required:** 
- ACAT CLI tool merged
- Vector-phase mapping documented + reviewed
- F-50 rules confirmed
- All 4 participants ack via `ser_ack`

**What happens:** SER 2 transitions IN_PROGRESS → Phase 2 can begin

---

### Gate 3: Phase 2 Complete + POSTFLIGHT Hook Live

**When:** End of Week 2

**Required:**
- Hook merged + tested
- Schema created + indexes built
- ACAT grounding section included in postflight payloads

**What happens:** Phase 2 data collection begins

---

### Gate 4: Phase 4 Complete + Report Delivered

**When:** End of Week 12

**Required:**
- Calibration dataset complete (50+ sessions)
- Findings: per-vector Brier scores + outliers flagged
- Lessons logged + ranked by confidence
- SER 2 transitions CLOSED

**What happens:** Framework goes live; practices adopt calibration lessons for next quarter

---

## VI. MESH MESSAGING SEQUENCE

| Step | When | Who | Action | Tool | Response |
|------|------|-----|--------|------|----------|
| 1 | Now | Evaluator | Send Collab A–D (FYI) | cortex_collab (4 threads, 1 to each practice) | Auto-accept, replies (noetic) |
| 2 | Within 2 days | humanaios | Reply: ACAT CLI feasibility | cortex_collab (reply, parent_id) | Commitment + timeline |
| 3 | Within 2 days | autonomy | Reply: SER 2 participation confirmed | cortex_collab (reply) | Confirmation + F-50 acks |
| 4 | Within 2 days | outreach | Reply: Phase 3 pilot understood | cortex_collab (reply) | Acknowledgment |
| 5 | Within 2 days | mesh-support | Reply: Observer role confirmed | cortex_collab (reply) | Acknowledgment |
| 6 | Day 3 | Evaluator | Send SER 2 proposal | cortex_propose (architecture_decision, REFLEX) | Triggers ECO gate |
| 7 | Within 1 day | ECO | Accept SER 2 proposal | Human decision (ntfy) | SER 2 created, status=OPEN |
| 8 | Day 1 Week 1 | All 4 | Begin Phase 1 work | SER 2 transitions to IN_PROGRESS | Parallel execution |

---

## VII. SUCCESS SIGNALS (Per-Practice)

### humanaios
✅ ACAT CLI callable with expected output  
✅ Phase scores align with empirica vectors ±0.20  
✅ Rubric alignment documented + stable  

### autonomy
✅ F-50 firewall holds (no feedback loops detected)  
✅ Evaluator findings routed without modification  
✅ SER 2 state transitions on schedule + acks timely  

### outreach (Phase 3+)
✅ Sessions assessed via ACAT  
✅ Receives calibration findings post-Phase 4  
✅ Confirms framework is actionable + useful  

### evaluator (lead)
✅ One-way grounding working (ACAT → empirica)  
✅ Observable linkage captured per session  
✅ Calibration dataset reaches 50+ sessions  
✅ Brier scores < 0.15 (80%+ convergence)  
✅ Findings guide next quarter's improvements  

---

**Next:** Finalize collab messages + SER 2 proposal. Ready for mesh outreach.

*Document version: 1.0 (Planning Phase)  
Status: Ready for collab dispatch and ECO proposal*
