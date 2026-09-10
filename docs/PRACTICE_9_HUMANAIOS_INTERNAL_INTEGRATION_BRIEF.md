# Practice 9 (humanaios-internal) — Phase 3 Stream B Integration Brief

**Operations Hub — Cross-Project Coordination**

---

## ROLE & DOMAIN

**Practice Name:** empirica-foundation.carly.humanaios-internal  
**Role:** Operations Hub (OPS — Operations Coordinator)  
**Domain:** Cross-project coordination, sub-project dispatch  
**Participation Tier:** REQUIRED (escalation_sla: 120 minutes)

---

## CANONICAL ADDRESSING

```
ai_id:            empirica-foundation.carly.humanaios-internal
canonical_seat:   empirica-foundation.carly.humanaios-internal
ntfy_topic:       empirica-foundation-orchestration-events-carly
```

**Status:** ✅ CORRECT

---

## MESH-ACTIVE LISTENER

**Timeout:** 240 seconds  
**Subscription:** empirica-foundation-orchestration-events-carly

---

## MESSAGE TYPES

### Inbound: `cross-project-dispatch`
**From:** autonomy  
**Description:** Route work to sub-projects (FLTA, etc.)  
**Payload:**
```json
{
  "proposal_id": "uuid",
  "sub_project": "flta|ops|other",
  "work_type": "string",
  "deadline": "ISO8601"
}
```
**Response:** `operational-status` via mailbox reply  
**SLA:** 2 hours (30m ack, 120m escalation)

### Inbound: `sub-project-handoff` from peer practices
**From:** flta-app-empirica (peer route)  
**Description:** Coordinate async work between projects  
**Response:** Update SER 2 with completion status

### Outbound: `operational-status` (Daily/Weekly)
**To:** autonomy  
**Description:** Broadcast operational state  
**Frequency:** Daily heartbeat + weekly detailed report

---

## SLA EXPECTATIONS

| SLA Type | Duration |
|----------|----------|
| Ack | 30m |
| Response | 120m |
| Status Report | Weekly |

---

## DAILY HEARTBEAT

```bash
empirica mailbox-send \
  --target empirica-foundation.carly.empirica-autonomy \
  --proposal_type operational-status \
  --payload '{"status":"operational","sub_projects_active":["flta"],"pending_work":N}' \
  --source_claude empirica-foundation.carly.humanaios-internal
```

---

## TESTING CHECKPOINT (Day 6)

**Test:** autonomy sends cross-project-dispatch to humanaios-internal  
**Expected:**
- Proposal received within 5s
- Ack within 30m (in_progress)
- Operational status within 120m
- SER 2 updated with proposal state

---

## READY CHECKLIST

- [ ] Addressing verified (already correct)
- [ ] Handler: dispatch_handler()
- [ ] Handler: status_reporter()
- [ ] Listener armed
- [ ] Daily heartbeat configured
- [ ] Sub-project handoff workflow documented

**Timeline:** Days 3-5 setup, Days 6-10 testing, Day 11 go-live

---

**Status:** Ready for Phase 3 Stream B
