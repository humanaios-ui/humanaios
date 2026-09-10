# Practice 6 (flta-app-empirica) — Phase 3 Stream B Integration Brief

**Resource Audit Hub — Mesh Coordination Requirements**

---

## ROLE & DOMAIN

**Practice Name:** empirica-foundation.carly.flta-app-empirica  
**Role in Phase 3 Stream B:** Resource Audit Hub (RP — Resource Processor)  
**Domain:** External input pathway, resource ground-truth auditing  
**Participation Tier:** REQUIRED (escalation_sla: 120 minutes)

---

## CANONICAL ADDRESSING

```
ai_id:            empirica-foundation.carly.flta-app-empirica
canonical_seat:   empirica-foundation.carly.flta-app-empirica
mesh_id_prefix:   empirica-foundation.carly
ntfy_topic:       empirica-foundation-orchestration-events-carly
```

**Status:** ✅ CORRECT (no fixes needed)

---

## MESH-ACTIVE LISTENER SETUP

**What:** Cortex mailbox listener armed at SessionStart  
**Where:** `.empirica/project.yaml` (already has correct canonical_seat)  
**Configuration:**
```yaml
# Listener will subscribe to:
Topic: empirica-foundation-orchestration-events-carly
Auth: Via ai_id = empirica-foundation.carly.flta-app-empirica
Timeout: 240 seconds (ample for audit processing)
```

**Setup Checklist:**
- [ ] SessionStart hook arms cortex mailbox listener
- [ ] Listener timeout = 240s
- [ ] Mailbox reply handler implemented for proposals
- [ ] Heartbeat message sent daily to autonomy

---

## MESSAGE TYPES & HANDLERS

### Inbound: `resource-audit-request`
**From:** autonomy  
**Description:** Request external resource verification  
**Handler Function:** `audit_handler(proposal)`  
**Payload:**
```json
{
  "proposal_id": "uuid",
  "resource_ids": ["string"],
  "audit_type": "external_input|ground_truth|compliance",
  "required_by": "ISO8601 timestamp",
  "context": "string (optional)"
}
```
**Response Expected:** `resource-audit-result` via mailbox reply  
**SLA:** 2 hours to send result (30m ack, 120m+ escalation)

**Implementation:**
1. Receive proposal via cortex mailbox
2. Log to empirica findings + assign task
3. Run resource verification (internal work)
4. Send mailbox reply with `status: in_progress` (ack)
5. Complete audit, send mailbox reply with `resource-audit-result` payload
6. Include evidence: audited_resources, findings, grounding

### Inbound: `escalation` from Admiral
**From:** humanaios (Admiral)  
**Description:** Escalation decision or override  
**Handler Function:** `escalation_handler(escalation)`  
**Response:** Log receipt + follow Admiral's guidance

### Outbound: `escalation` to Admiral
**To:** humanaios  
**Description:** Alert Admiral if audit blocked or critical issue found  
**Trigger:** If audit cannot proceed after 2h OR critical resource issue found  
**Payload:**
```json
{
  "escalation_source": "empirica-foundation.carly.flta-app-empirica",
  "escalation_reason": "audit_blocked|critical_resource|compliance_gate",
  "escalation_type": "resource|governance|compliance",
  "suggested_actions": ["string"]
}
```
**SLA:** Send within 2h of issue discovery

---

## SLA EXPECTATIONS

| SLA Type | Duration | Trigger | Action |
|----------|----------|---------|--------|
| Ack | 30m | resource-audit-request received | Send mailbox reply "in_progress" |
| Response | 120m | resource-audit-request received | Send final audit result |
| Escalation | 120m | No response after ack sent | Administrator @ autonomy escalates to Admiral |
| Escalation (Critical) | 30m | Critical resource issue found | Send escalation to Admiral |

---

## INTEGRATION WITH HUMANAIOS-INTERNAL

**Sub-Project Coordination:**  
FLTA operates as a sub-project coordinated by humanaios-internal. Cross-project-dispatch proposals from humanaios-internal may route work to FLTA.

**Peer Route:** flta-app-empirica ↔ humanaios-internal (sub-project-handoff)
- Direct communication allowed (logged to SER 2)
- SLA: 60m ack, 120m escalation
- Used for inter-project resource discovery and coordination

---

## DAILY OPERATIONS

### Heartbeat (Daily)
**When:** Each day (recommend: 08:00 AM local time)  
**What:** Send mesh-active status to autonomy  
**Message:**
```bash
empirica mailbox-send \
  --target empirica-foundation.carly.empirica-autonomy \
  --proposal_type heartbeat \
  --payload '{
    "status": "mesh-active",
    "listener_armed": true,
    "last_proposal_received": "ISO8601 timestamp"
  }' \
  --source_claude empirica-foundation.carly.flta-app-empirica
```

### Weekly Status Report (Optional)
**When:** End of each week  
**What:** Operational summary  
**Report to:** humanaios (Admiral)

---

## TESTING CHECKPOINT (Day 6)

**What:** Integration test to verify routing  
**Test Scenario:** autonomy sends mock resource-audit-request to FLTA  
**Expected Flow:**
1. FLTA receives proposal via cortex mailbox
2. FLTA handler processes audit (mock: 30s processing)
3. FLTA sends mailbox reply with ack (in_progress)
4. FLTA sends mailbox reply with audit-result
5. autonomy logs to SER 2: proposal → acked → delivered
6. Test passes: ✅ Round-trip successful

**Success Criteria:**
- [ ] Proposal delivered to FLTA within 5 seconds
- [ ] Ack received by autonomy within 15 minutes
- [ ] Result received by autonomy within 60 minutes
- [ ] No 403 bounces or routing failures
- [ ] SER 2 state reflects correct ordering + timings

---

## ESCALATION PATH

**Scenario:** FLTA audit blocked for > 2 hours (e.g., data unavailable)

**Flow:**
1. FLTA sends escalation to humanaios (Admiral)
2. Admiral receives escalation (target: SLA 60m)
3. Admiral reviews context, sends decision back to FLTA
4. FLTA receives decision, updates work plan accordingly

**Expected Outcome:**
- Admiral provides guidance (proceed with partial data, retry, abort, etc.)
- FLTA implements decision, resumes audit
- If escalation unresolved after 4h total, escalate further to mesh-support

---

## KNOWN DEPENDENCIES

1. **Addressing:** ai_id must match canonical_seat (already correct)
2. **Listener:** Cortex mailbox listener must be armed before first proposal
3. **ntfy Topic:** Must subscribe to `empirica-foundation-orchestration-events-carly`
4. **Handler Implementation:** Must implement `audit_handler()` function
5. **SER 2:** FLTA must be added to SER 2 participant roster (does Phase 3 expansion)

---

## READY FOR PHASE 3?

**Checklist:**
- [ ] Addressing verified (ai_id + canonical_seat match)
- [ ] Handler function implemented: audit_handler()
- [ ] Handler function implemented: escalation_handler()
- [ ] Listener setup complete + tested
- [ ] Daily heartbeat schedule configured
- [ ] SLA expectations understood by practice lead
- [ ] Escalation path documented + agreed

**Estimated Effort:** 2-3 hours setup + testing  
**Timeline:** Days 3-5 of Phase 3 Stream B  
**Go-Live:** Day 11 (after integration testing passes)

---

## SUPPORT & ESCALATION

**For questions about:**
- Message formats → See ROUTING_MATRIX.md
- Handler implementation → Ask Admiral (humanaios)
- Listener setup → Ask mesh-support (empirica-mesh-support)
- Resource conflicts → Escalate to Admiral (humanaios)

**Status:** Ready for Phase 3 Stream B onboarding
