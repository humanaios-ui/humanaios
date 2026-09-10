# Practice 7 (grok-crossref) — Phase 3 Stream B Integration Brief

**Cross-Reference Validator — Independent Validation Seat**

---

## ROLE & DOMAIN

**Practice Name:** empirica-foundation.carly.grok-crossref  
**Role:** Cross-Reference Validator (VLD — Validator/Cross-Reference)  
**Domain:** Independent validation, convergent-validity checking  
**Participation Tier:** PARTICIPATING (escalation_sla: 60 minutes)  
**Access:** Read-only to humanaios operations (F-50 boundary)

---

## CANONICAL ADDRESSING

```
ai_id:            empirica-foundation.carly.grok-crossref
canonical_seat:   empirica-foundation.carly.grok-crossref
ntfy_topic:       empirica-foundation-orchestration-events-carly
```

**Status:** ✅ CORRECT

---

## MESH-ACTIVE LISTENER

**Timeout:** 180 seconds  
**Subscription:** empirica-foundation-orchestration-events-carly  
**Handler:** Mailbox reply handler for validation-request

---

## MESSAGE TYPES

### Inbound: `validation-request`
**From:** autonomy  
**Payload:**
```json
{
  "proposal_id": "uuid",
  "claim": "string to validate",
  "claim_context": "object",
  "grounding": "read|ran|retrieved|assumed",
  "reference_artifacts": ["artifact_id"]
}
```
**Response:** `validation-result` via mailbox reply  
**SLA:** 1 hour to respond (30m ack, 60m escalation)

### Outbound: `divergence-alert` (if misalignment found)
**To:** humanaios (Admiral) — PRIORITY escalation  
**Payload:**
```json
{
  "divergence_type": "claim|vector|process|other",
  "expected": "string",
  "observed": "string",
  "impact": 0.0-1.0,
  "evidence": ["artifact_id"]
}
```
**SLA:** Send within 15 minutes of discovering divergence

---

## SLA EXPECTATIONS

| SLA Type | Duration | Action |
|----------|----------|--------|
| Ack | 30m | Send "in_progress" mailbox reply |
| Response | 60m | Send validation-result |
| Divergence Alert | 15m | If misalignment found (PRIORITY) |

---

## CRITICAL CONSTRAINTS

**F-50 Boundary:** Grok has **read-only** access to humanaios operations
- ✅ Can read: operations/CURRENT.md, REGISTERED.md, open PRs
- ❌ Cannot write: No commits to humanaios-ui/operations
- ❌ Cannot co-write: Results logged in grok-crossref project only

**Epistemic Independence:** Grok's findings feed humanaios as external validation evidence (convergent-validity)

---

## DAILY HEARTBEAT

```bash
empirica mailbox-send \
  --target empirica-foundation.carly.empirica-autonomy \
  --proposal_type heartbeat \
  --payload '{"status":"mesh-active","listener_armed":true}' \
  --source_claude empirica-foundation.carly.grok-crossref
```

---

## TESTING (Day 6-8)

**Test:** autonomy sends mock validation-request  
**Expected:**
- Receive proposal within 5s
- Ack within 15m
- Validation result within 60m
- No routing failures

---

## READY CHECKLIST

- [ ] Addressing verified
- [ ] Handler: validation_handler()
- [ ] Handler: divergence_detector()
- [ ] Listener armed
- [ ] Read-only access to humanaios confirmed
- [ ] F-50 boundary understood (write scope = grok-crossref only)

**Timeline:** Days 3-5 setup, Days 6-10 testing, Day 11 go-live

---

**Status:** Ready for Phase 3 Stream B
