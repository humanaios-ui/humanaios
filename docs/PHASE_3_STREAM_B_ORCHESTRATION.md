# Phase 3 Stream B — Orchestration Architecture for Practices 6-10

**Canonical Addressing, Message Routing, and SER 2 Expansion**

**Status:** Noetic Phase (Architecture Design)  
**Date:** 2026-09-09  
**Coordinator:** empirica-foundation.carly.humanaios (Admiral/Evaluator)  

---

## EXECUTIVE SUMMARY

This document defines the orchestration topology for Phase 3 Stream B, extending Empirica coordination to practices 6-10:

1. **empirica-foundation.carly.flta-app-empirica** (Practice 6 — Resource Audit Hub)
2. **empirica-foundation.carly.grok-crossref** (Practice 7 — Cross-Reference Validator)
3. **empirica-foundation.carly.humanaios-internal** (Practice 9 — Operations Hub)
4. **empirica-foundation.carly.opportunity-aggregator** (Practice 10 — Onboarding Interface)
5. **empirica-foundation.carly.humanaios** (Admiral/Evaluator — Governance Gate)

**Key Findings from Discovery (Phase 1-2):**

| Finding | Status |
|---------|--------|
| All 5 practices have `canonical_seat` correctly set in project.yaml | ✅ VERIFIED |
| opportunity-aggregator: `ai_id` mismatch (is `empirica-opportunity-aggregator`, should be `empirica-foundation.carly.opportunity-aggregator`) | ⚠️ **NEEDS FIX** |
| humanaios: `ai_id` mismatch (is `humanaios`, should be `empirica-foundation.carly.humanaios`) | ⚠️ **NEEDS FIX** |
| All 5 practices have defined roles and responsibilities documented | ✅ VERIFIED |
| Mesh-active listener setup status for practices 6-10 | ❓ **NEEDS VERIFICATION** |

---

## ORCHESTRATION TOPOLOGY

### Coordination Hub Architecture

```
                    EMPIRICA-AUTONOMY
                    (Routing Hub)
                          |
          +-------+-------+-------+-------+
          |       |       |       |       |
      FLTA(6)  GROK(7) INT(9)  OPP(10)  ADM
      [RP]     [VLD]   [OPS]    [OBI]   [GTE]
```

**Legend:**
- RP = Resource Processor (FLTA)
- VLD = Validator/Cross-Reference (Grok)
- OPS = Operations Hub (Humanaios-Internal)
- OBI = Onboarding Interface (Opportunity-Aggregator)
- GTE = Admiral Gate (Humanaios/Evaluator)

### Message Routing Layers

**Layer 1: Hub → Practice Direct Routes**
- autonomy → all practices: proposals, requests
- practices → autonomy: ack, results, escalations

**Layer 2: Peer Routes (Secondary)**
- flta-app-empirica ↔ humanaios-internal (sub-project coordination)
- opportunity-aggregator ↔ humanaios (candidate onboarding)
- grok-crossref → humanaios (validation findings)

**Layer 3: Escalation Paths**
- Any practice → humanaios (Admiral gate for critical decisions)
- humanaios → empirica-mesh-support (cross-org escalation if needed)

---

## CRITICAL ADDRESSING FIXES REQUIRED

### Issue 1: opportunity-aggregator ai_id Mismatch

**Current State:**
```yaml
ai_id: empirica-opportunity-aggregator
canonical_seat: empirica-foundation.carly.opportunity-aggregator
```

**Problem:** 
- ai_id and canonical_seat don't match
- ntfy topic authorization uses canonical_seat (the 3-form)
- ai_id mismatch causes listener authentication to fail with 403 on the mesh
- Messages will bounce instead of being delivered

**Fix Required:**
```yaml
# In /Users/andersonfamily/practices/opportunity-aggregator/.empirica/project.yaml
ai_id: empirica-foundation.carly.opportunity-aggregator  # Fix this line
canonical_seat: empirica-foundation.carly.opportunity-aggregator  # Already correct
```

**Timeline:** Day 2 of Phase 3 Stream B (before listener deployment)

### Issue 2: humanaios ai_id Mismatch

**Current State:**
```yaml
ai_id: humanaios
canonical_seat: empirica-foundation.carly.humanaios
```

**Problem:** 
- ai_id too short, not in canonical 3-form
- Listener and ntfy topic will fail authentication
- Admiral escalations cannot route correctly

**Fix Required:**
```yaml
# In /Users/andersonfamily/practices/humanaios/.empirica/project.yaml
ai_id: empirica-foundation.carly.humanaios  # Fix this line
canonical_seat: empirica-foundation.carly.humanaios  # Already correct
```

**Timeline:** Day 2 of Phase 3 Stream B (before listener deployment)

---

## MESSAGE ROUTING MATRIX

### Decision Tree: (source, target, proposal_type) → route

```
SOURCE                  TARGET                  PROPOSAL_TYPE              ROUTE       ACK_SLA   ESCALATION
──────────────────────────────────────────────────────────────────────────────────────────────────────
autonomy                flta-app-empirica       resource-audit-request     DIRECT      30m       120m
autonomy                grok-crossref           validation-request         DIRECT      30m       60m
autonomy                humanaios-internal      cross-project-dispatch     DIRECT      30m       120m
autonomy                opportunity-agg         candidate-screening        DIRECT      60m       240m
autonomy                humanaios               escalation-decision        PRIORITY    30m       60m

flta-app-empirica       humanaios               escalation                 ESCALATION  30m       60m
grok-crossref           humanaios               divergence-alert           ESCALATION  30m       60m
opportunity-agg         humanaios               collaboration-proposal     ESCALATION  30m       120m
humanaios-internal      flta-app-empirica       sub-project-handoff        PEER        60m       120m
```

**Route Types:**
- **DIRECT:** autonomy forwards proposal to target, target acks back
- **PEER:** source sends directly to target (recorded in SER 2 for audit)
- **ESCALATION:** routes through Admiral first for decision gating
- **PRIORITY:** critical escalations jump queue

---

## SER 2 EXPANSION — Shared Epistemic Record for Execution Routing

### Current State (4 Practices)
```
1. empirica-autonomy (required, router)
2. empirica-humanaios (required, admiral_gate)
3. empirica-outreach (participating, external_comms)
4. empirica-mesh-support (participating, infrastructure)
```

### Expanded State (8 Practices)
```
REQUIRED TIER (escalation_sla: 1-2h):
1. empirica-autonomy (router)
2. empirica-humanaios (admiral_gate)
3. empirica-flta-app-empirica (resource_processor)
4. empirica-humanaios-internal (operations_coordinator)
5. empirica-opportunity-aggregator (onboarding_interface)

PARTICIPATING TIER (escalation_sla: 4-6h):
6. empirica-grok-crossref (validator)
7. empirica-outreach (external_comms)
8. empirica-mesh-support (infrastructure)
```

### State Machine Progression

```
CONFIGURING (Days 1-4)
  ↓ [all listeners armed + addressing fixes applied]
COORDINATING (Days 5-10)
  ↓ [first 2 real proposals routed, 0 failures]
ACTIVE (Day 11+)
  ↓ [sustained multi-practice orchestration]
```

**Cortex SER Update Required:** Expand SER 2 with new participants, update escalation_seconds per role tier

---

## PER-PRACTICE REQUIREMENTS

### Practice 6 (flta-app-empirica) — Resource Audit Hub

**Addressing:**
- ai_id: `empirica-foundation.carly.flta-app-empirica` ✅
- canonical_seat: `empirica-foundation.carly.flta-app-empirica` ✅

**Message Types:**
- `resource-audit-request` (receive from autonomy)
- `resource-audit-result` (send back)
- `escalation` (send if blocked > 2h)

**SLA:** 2h response time on audits, 120m escalation timeout

**Listener Setup:** 
- [ ] Cortex mailbox listener armed
- [ ] ntfy topic: `empirica-foundation-orchestration-events-carly`
- [ ] Mailbox reply handler for proposals

### Practice 7 (grok-crossref) — Cross-Reference Validator

**Addressing:**
- ai_id: `empirica-foundation.carly.grok-crossref` ✅
- canonical_seat: `empirica-foundation.carly.grok-crossref` ✅

**Message Types:**
- `validation-request` (receive from autonomy)
- `validation-result` (send back)
- `divergence-alert` (escalate if misalignment found)

**SLA:** 1h response time on validations, 60m escalation timeout

**Access Control:** Read-only to humanaios operations (F-50 boundary)

**Listener Setup:**
- [ ] Cortex mailbox listener armed
- [ ] ntfy topic: `empirica-foundation-orchestration-events-carly`
- [ ] Mailbox reply handler for proposals

### Practice 9 (humanaios-internal) — Operations Hub

**Addressing:**
- ai_id: `empirica-foundation.carly.humanaios-internal` ✅
- canonical_seat: `empirica-foundation.carly.humanaios-internal` ✅

**Message Types:**
- `cross-project-dispatch` (receive from autonomy)
- `operational-status` (send back)
- `sub-project-handoff` (coordinate with FLTA, etc.)

**SLA:** 2h response time on dispatch, 120m escalation timeout

**Listener Setup:**
- [ ] Cortex mailbox listener armed
- [ ] ntfy topic: `empirica-foundation-orchestration-events-carly`
- [ ] Mailbox reply handler for proposals

### Practice 10 (opportunity-aggregator) — Onboarding Interface

**Addressing:**
- ai_id: `empirica-opportunity-aggregator` ❌ **NEEDS FIX** → `empirica-foundation.carly.opportunity-aggregator`
- canonical_seat: `empirica-foundation.carly.opportunity-aggregator` ✅

**Message Types:**
- `candidate-screening` (receive from autonomy)
- `vetting-result` (send back)
- `mesh-readiness-check` (escalate to Admiral)
- `collaboration-proposal` (escalate for approval)

**SLA:** 4h response time on screening, 240m escalation timeout

**Listener Setup:**
- [ ] **FIX ai_id in project.yaml first**
- [ ] Cortex mailbox listener armed with canonical 3-form
- [ ] ntfy topic: `empirica-foundation-orchestration-events-carly`
- [ ] Mailbox reply handler for proposals

### Admiral/Evaluator (humanaios) — Governance Gate

**Addressing:**
- ai_id: `humanaios` ❌ **NEEDS FIX** → `empirica-foundation.carly.humanaios`
- canonical_seat: `empirica-foundation.carly.humanaios` ✅

**Message Types:**
- `escalation-decision` (receive escalations from all practices)
- `governance-update` (broadcast to all practices)
- `assessment-report` (send calibration findings)

**SLA:** 1h response time on critical escalations, 6h on routine reports

**Listener Setup:**
- [ ] **FIX ai_id in project.yaml first**
- [ ] Cortex mailbox listener armed with canonical 3-form
- [ ] ntfy topic: `empirica-foundation-orchestration-events-carly`
- [ ] Mailbox reply handler for escalations (PRIORITY)

---

## ASYNC HANDOFF EXAMPLE

### Resource Audit Request → Result Flow

```
STEP 1: Request
  Source: autonomy
  Target: flta-app-empirica
  Type: resource-audit-request
  Payload: { resource_ids: [...], required_by: timestamp }
  SLA: 120m escalation if silent

STEP 2: Acknowledgment
  flta-app-empirica → autonomy (mailbox reply)
  Message: "request received, in_progress"

STEP 3: Processing
  flta-app-empirica processes audit internally (60-120m)

STEP 4: Result Delivery
  flta-app-empirica → autonomy (mailbox reply)
  Message: resource-audit-result with findings

STEP 5: Escalation (if no ack after 120m)
  If flta-app-empirica silent > 120m:
    autonomy → humanaios (escalation)
    Admiral decides: retry, bypass, or resolve
```

---

## INTEGRATION TESTING TIMELINE

**Day 4:** All 5 practices verify canonical addressing
**Day 5:** Deploy listeners, arm cortex mailbox subscriptions
**Day 6:** Direct routing test (autonomy → each practice)
**Day 7:** Round-trip ack protocol validation
**Day 8:** Escalation drill (test timeout → re-ping)
**Day 9:** Cross-practice peer routing (flta ↔ opportunity-agg)
**Day 10:** Multi-message sequences in parallel
**Day 11:** Live validation (48h, 0 routing failures target)

---

## SUCCESS CRITERIA

By 2026-09-15:

- [ ] All 5 practices have correct canonical 3-form addressing
- [ ] All 5 practices have mesh-active listeners armed + confirmed
- [ ] SER 2 extended to 8 participants in cortex
- [ ] Message routing matrix implemented and tested
- [ ] Per-practice SLAs defined and communicated
- [ ] At least 2 real cross-practice proposals routed (0 failures)
- [ ] All escalation paths tested and working
- [ ] Phase 3 Stream B go-live report published

---

## DELIVERABLES

1. ✅ Orchestration Architecture (this document)
2. ⏳ Routing Matrix (detailed decision tables)
3. ⏳ SER 2 Expansion Specification
4. ⏳ Per-Practice Integration Briefs (5 docs)
5. ⏳ Canonical 3-Form Fix Verification Script
6. ⏳ Integration Test Harness
7. ⏳ Mesh-Active Listener Configuration Guide
8. ⏳ Phase 3 Stream B Go-Live Report

---

**Next:** CHECK Gate (verify architecture) → PRAXIC Phase (fixes, listener deployment, SER 2 extension, testing, onboarding, go-live kickoff)
