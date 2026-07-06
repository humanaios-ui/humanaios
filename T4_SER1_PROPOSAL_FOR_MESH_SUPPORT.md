# T4 SER 1 Proposal — Assessment Coordination

**Date Created:** 2026-07-06  
**From:** empirica-foundation.carly.empirica-foundation-evaluator (Evaluator seat)  
**To:** empirica-foundation.carly.empirica-mesh-support (Mesh-Support seat)  
**Action Required:** Create SER 1 via cortex_propose  
**Priority:** CRITICAL — Unblocks T4 Phase 1–5 execution  
**Timeline:** Immediate (blocks all subsequent phases)

---

## Executive Summary

**SER 1 (Assessment Coordination)** establishes the durable shared state for assessing T4 cortex mesh orchestration across the foundation practices. This SER coordinates two required-tier participants:

- **empirica-foundation-evaluator**: Independent assessment of behavior + calibration
- **empirica-mesh-support**: Execution coordination + routing setup

Once created, SER 1 becomes the canonical coordination record for all T4 mesh implementation work.

---

## What Needs Doing

**Action:** Create SER 1 by calling `cortex_propose` with the payload below.

**Why mesh-support creates it:** The SER is a proposal that both practices need to see. Creating it from mesh-support's seat ensures immediate visibility to both participants and establishes mesh-support as a coordinator in the shared record.

---

## cortex_propose Call Specification

### Tool
```
mcp__cortex__cortex_propose
```

### Parameters

```json
{
  "type": "architecture_decision",
  "action_category": "REFLEX",
  "source_claude": "empirica-foundation.carly.empirica-mesh-support",
  "target_claudes": ["empirica-foundation.carly.empirica-foundation-evaluator"],
  "title": "Create SER 1: Assessment Coordination for T4 Mesh Implementation",
  "summary": "Establish shared epistemic record for Assessment Coordination between mesh-support and evaluator. This SER coordinates assessment of T4 cortex mesh implementation across the foundation practices. Participants: empirica-foundation-evaluator (assessment + oversight) and empirica-mesh-support (execution + routing). Purpose: Create durable shared state for sustained multi-practice coordination per T4 Phase 1.",
  "payload": {
    "action": "create_ser",
    "ser_spec": {
      "title": "T4 Assessment Coordination — Foundation Mesh Implementation",
      "summary": "## Purpose\nCoordinate assessment of T4 cortex mesh orchestration implementation across foundation practices.\n\n## Participants\n- **empirica-foundation-evaluator** (required): Independent assessment of mesh behavior and calibration\n- **empirica-mesh-support** (required): Execution coordination and routing setup\n\n## Scope\n- Assess mesh readiness across: autonomy, humanaios, outreach, website, empirica-cortex\n- Measure empirica↔ACAT convergence (behavioral drift vs epistemic drift grounding)\n- Surface calibration gaps and behavioral drift\n- Establish F-50 firewall (assessment independence from execution)\n\n## Timeline\nT4 Phase 1–5 execution: 30 hours over 4 weeks (commencing 2026-07-06)\n\n## Escalation\nRequired-tier participants must ack within 4 hours of transitions; silence after 14400s triggers re-ping.\n\n## Success Criteria\n- All 6 foundation practices integrated into cortex mesh\n- Assessment + execution workflows fully operational\n- Cross-instrument grounding (empirica + ACAT) validated",
      "participants": [
        {
          "practice_id": "empirica-foundation.carly.empirica-foundation-evaluator",
          "role": "required"
        },
        {
          "practice_id": "empirica-foundation.carly.empirica-mesh-support",
          "role": "required"
        }
      ],
      "escalation_seconds": 14400
    }
  }
}
```

---

## Expected Outcome

✅ **Success:** cortex_propose returns:
```json
{
  "proposal_id": "prop_...",
  "ser_id": "ser_...",
  "ser_state_verified": true,
  "status": "accepted"
}
```

**What happens next:**
- SER 1 appears in both practices' mesh inboxes
- Both participants can ack via `cortex_ser_ack`
- State transitions (open → in_progress → closed) trigger re-pings
- T4 Phase 1 can proceed with Assessment Coordination established

---

## SER 1 Scope in Detail

### Participants & Roles

| Practice | Role | Responsibility |
|----------|------|-----------------|
| empirica-foundation-evaluator | required | Independent assessment, ACAT grounding, F-50 firewall, calibration measurement |
| empirica-mesh-support | required | T4 execution coordination, mesh routing setup, participant orchestration |

Both roles are **required** — silence past the 4-hour escalation window triggers a re-ping.

### Assessment Dimensions

1. **Mesh Readiness**
   - All 6 foundation practices wired into cortex mesh
   - Orchestration event listener operational per practice
   - Cross-practice proposal routing tested end-to-end

2. **Behavioral Drift**
   - Empirica + ACAT convergence measured
   - Vector calibration vs. ground truth (ACAT phase scoring)
   - F-50 firewall holding (no feedback loops between assessment and execution)

3. **Calibration Gaps**
   - Per-practice epistemic state assessed
   - Divergence between self-claimed and grounded vectors surfaced
   - Lessons learned logged for future reference

4. **Cross-Instrument Grounding**
   - Empirica's 13-vector model ↔ ACAT's 12-step mapping aligned
   - One-way grounding link (ACAT grounds empirica) verified
   - Measurement methodology documented

### Timeline & Phases

| Phase | Work | Owner | Duration | Blocker |
|-------|------|-------|----------|---------|
| **1** | SER 1 creation, listener setup, initial coordination | mesh-support | Days 1–2 | ← **This proposal** |
| **2** | Autonomy + humanaios/outreach/website integration | autonomy | Days 3–5 | Phase 1 |
| **3** | Assessment methodology + ACAT grounding | evaluator | Days 6–10 | Phase 1 |
| **4** | Cross-instrument calibration measurement | evaluator | Days 11–20 | Phase 3 |
| **5** | Findings report + lessons learned | evaluator | Days 21–30 | Phase 4 |

**Total duration:** 30 hours over 4 weeks (commencing 2026-07-06)

### Success Criteria

✅ All 6 foundation practices registered in cortex mesh  
✅ Proposal routing working end-to-end (empirica-foundation.carly.* ↔ empirica-foundation.carly.*)  
✅ Assessment + execution workflows operational with F-50 firewall active  
✅ Empirica ↔ ACAT convergence validated via grounded measurement  
✅ Lessons learned + calibration report completed  

---

## Context & Background

### Why This SER?

The foundation's T4 mesh implementation requires **independent assessment alongside execution**. SER 1 creates the durable coordination record so:

1. **Evaluator** (external grounding) measures mesh behavior + calibration independently
2. **Mesh-support** (execution) coordinates routing setup without feedback loops
3. **F-50 firewall** (independence constraint) prevents assessment from influencing execution or vice versa
4. **Cross-instrument grounding** (ACAT ↔ empirica) validates measurement methodology

Without SER 1, there's no shared state for assessing whether the mesh is working as designed.

### What Unblocked This

- ✅ Cortex MCP tools wired into empirica environment
- ✅ Both practices' canonical seats registered in cortex mesh
- ✅ Authentication + credential configuration verified
- ✅ Assessment methodology + ACAT grounding linkage documented

### Reference Documents

- **T4_MESH_SUPPORT_HANDOFF.md** — Full T4 implementation specification (5 phases, success criteria, timeline)
- **PHASE_1_BLOCKER_ESCALATION.md** — Cortex integration blocker (now resolved)
- **docs/EVALUATOR_MANUAL.md** — Evaluator operational manual + assessment methodology
- **docs/EVALUATOR_SEAT.md** — Role definition (independence, authority bounds)

---

## Instructions for Mesh-Support

### Step 1: Verify Prerequisites
```bash
# Confirm your canonical seat
cat .empirica/project.yaml | grep canonical_seat
# Expected: empirica-foundation.carly.empirica-mesh-support

# Confirm cortex credentials loaded
grep -A2 "cortex:" ~/.empirica/credentials.yaml | head -5
# Expected: api_key + api_url
```

### Step 2: Invoke cortex_propose
Load the **cortex-mailbox-send** skill for full operational guidance, then invoke:

```python
mcp__cortex__cortex_propose(
    type="architecture_decision",
    action_category="REFLEX",
    source_claude="empirica-foundation.carly.empirica-mesh-support",
    target_claudes=["empirica-foundation.carly.empirica-foundation-evaluator"],
    title="Create SER 1: Assessment Coordination for T4 Mesh Implementation",
    summary="Establish shared epistemic record for Assessment Coordination...",
    payload={
        "action": "create_ser",
        "ser_spec": { /* full spec from Parameters section above */ }
    }
)
```

### Step 3: Verify Success
```bash
empirica mailbox poll --ai-id empirica-mesh-support --status accepted --output json
# Look for: ser_id, ser_state_verified=true
```

### Step 4: Log Completion
```bash
empirica goals-complete-task --task-id <T4_Phase_1_Task_ID> \
  --evidence "SER 1 created: ser_id=ser_..."
```

---

## Escalation & Support

**If cortex_propose fails:**
- Check that canonical seat is `empirica-foundation.carly.empirica-mesh-support`
- Verify credentials in `~/.empirica/credentials.yaml`
- Confirm cortex API URL (should be `https://cortex.getempirica.com`)
- Check network connectivity (curl the health endpoint)
- If still blocked, surface to Night (Zone 2) — may need cortex instance debugging

**If SER 1 creation succeeds but doesn't appear in evaluator's inbox:**
- Wait 30 seconds (mesh routing delay)
- Poll inbox: `empirica mailbox poll --ai-id empirica-foundation-evaluator`
- Check if proposal status is `eco_review` (awaiting ECO decision) vs. `accepted` (ready to action)

---

## Approval & Sign-Off

**Proposed by:** Carly R. Anderson (empirica-foundation Admiral + Evaluator)  
**Created:** 2026-07-06  
**Status:** Ready for mesh-support action

**Approval:** User authorization confirmed — proceed with cortex_propose invocation.

---

*This proposal unblocks T4 Phase 1 execution. Once SER 1 is created, T4 timeline begins and Phase 2–5 work can commence.*
