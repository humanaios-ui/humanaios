# Phase 3 Stream B — Message Routing Matrix

**Canonical Decision Table for Cross-Practice Proposals**

---

## ROUTING LOGIC: (source, target, proposal_type) → decision

### Hub Routes (Autonomy as Router)

```
SOURCE          TARGET                  PROPOSAL_TYPE              ROUTE_CLASS   ACK_SLA   ESCALATION_SLA   HANDLER
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
autonomy        flta-app-empirica       resource-audit-request     DIRECT        30m       120m             audit_handler
autonomy        flta-app-empirica       resource-audit-result      DIRECT_REPLY  15m       60m              completion_ack
autonomy        grok-crossref           validation-request         DIRECT        30m       60m              validation_handler
autonomy        grok-crossref           validation-result          DIRECT_REPLY  15m       45m              completion_ack
autonomy        humanaios-internal      cross-project-dispatch     DIRECT        30m       120m             dispatch_handler
autonomy        humanaios-internal      operational-status         DIRECT_REPLY  15m       60m              status_ack
autonomy        opportunity-agg         candidate-screening        DIRECT        60m       240m             screening_handler
autonomy        opportunity-agg         vetting-result             DIRECT_REPLY  30m       120m             vetting_ack
autonomy        humanaios               escalation-decision        PRIORITY      30m       60m              decision_handler
autonomy        humanaios               governance-update          BROADCAST     30m       120m             update_handler
```

### Peer Routes (Direct Practice-to-Practice, Logged to SER 2)

```
SOURCE                  TARGET                  PROPOSAL_TYPE              ROUTE_CLASS   ACK_SLA   ESCALATION_SLA
────────────────────────────────────────────────────────────────────────────────────────────────────
flta-app-empirica       humanaios-internal      sub-project-handoff        PEER          60m       120m
flta-app-empirica       opportunity-agg         resource-discovery         PEER          60m       120m
flta-app-empirica       humanaios               escalation                 ESCALATION    30m       60m
grok-crossref           humanaios               divergence-alert           ESCALATION    30m       45m
humanaios-internal      opportunity-agg         onboarding-candidate       PEER          60m       120m
humanaios-internal      humanaios               resource-allocation        ESCALATION    30m       90m
opportunity-agg         humanaios               collaboration-proposal     ESCALATION    30m       120m
```

### Escalation Routes (Critical Decisions to Admiral)

```
SOURCE                  TARGET          PROPOSAL_TYPE              SLA_MINUTES   HANDLER
──────────────────────────────────────────────────────────────────────────────
[any practice]          humanaios       escalation                 60m [ACK]     escalation_handler
[any practice]          humanaios       governance-change-request  60m [ACK]     governance_handler
humanaios               mesh-support    cross-org-escalation       60m [ACK]     infrastructure_handler
```

---

## MESSAGE TYPE SPECIFICATIONS

### resource-audit-request
**From:** autonomy  
**To:** flta-app-empirica  
**Description:** Request external resource verification  
**Payload Schema:**
```json
{
  "proposal_id": "uuid",
  "resource_ids": ["string"],
  "audit_type": "external_input|ground_truth|compliance",
  "required_by": "ISO8601 timestamp",
  "context": "string (optional context)"
}
```
**Response Type:** resource-audit-result  
**SLA:** 120m escalation if silent  
**Handlers:** flta-app-empirica.audit_handler()

### validation-request
**From:** autonomy  
**To:** grok-crossref  
**Description:** Request independent validation of a claim  
**Payload Schema:**
```json
{
  "proposal_id": "uuid",
  "claim": "string",
  "claim_context": "object",
  "claim_grounding": "read|ran|retrieved|assumed",
  "reference_artifacts": ["artifact_id"]
}
```
**Response Type:** validation-result  
**SLA:** 60m escalation if silent  
**Handlers:** grok-crossref.validation_handler()

### cross-project-dispatch
**From:** autonomy  
**To:** humanaios-internal  
**Description:** Route work to sub-projects (FLTA, etc.)  
**Payload Schema:**
```json
{
  "proposal_id": "uuid",
  "sub_project": "flta|ops|other",
  "work_type": "string",
  "work_description": "string",
  "deadline": "ISO8601 timestamp"
}
```
**Response Type:** operational-status  
**SLA:** 120m escalation if silent  
**Handlers:** humanaios-internal.dispatch_handler()

### candidate-screening
**From:** autonomy  
**To:** opportunity-aggregator  
**Description:** Run candidate through mesh-onboarding pipeline  
**Payload Schema:**
```json
{
  "proposal_id": "uuid",
  "candidate_id": "string",
  "candidate_data": "object",
  "screening_stage": "initial|deep|final",
  "priority": "normal|urgent"
}
```
**Response Type:** vetting-result  
**SLA:** 240m escalation if silent  
**Handlers:** opportunity-aggregator.screening_handler()

### escalation-decision
**From:** autonomy  
**To:** humanaios  
**Description:** Critical decision requiring Admiral oversight  
**Payload Schema:**
```json
{
  "proposal_id": "uuid",
  "escalation_source": "string (source practice ai_id)",
  "escalation_reason": "string",
  "escalation_type": "resource|governance|compliance|other",
  "suggested_actions": ["string"]
}
```
**Response Type:** escalation-decision-result  
**SLA:** 60m escalation if silent  
**Handlers:** humanaios.decision_handler()

### divergence-alert
**From:** grok-crossref  
**To:** humanaios  
**Description:** Alert Admiral to detected misalignment  
**Payload Schema:**
```json
{
  "proposal_id": "uuid",
  "divergence_type": "claim|vector|process|other",
  "expected": "string",
  "observed": "string",
  "impact": 0.0-1.0,
  "evidence_artifacts": ["artifact_id"]
}
```
**Response Type:** divergence-decision  
**SLA:** 45m escalation if silent (PRIORITY)  
**Handlers:** humanaios.divergence_handler()

### collaboration-proposal
**From:** opportunity-aggregator  
**To:** humanaios  
**Description:** Propose new mesh participant for onboarding  
**Payload Schema:**
```json
{
  "proposal_id": "uuid",
  "candidate_name": "string",
  "candidate_expertise": ["string"],
  "readiness_score": 0.0-1.0,
  "vetting_checklist": ["item"],
  "recommended_role": "string"
}
```
**Response Type:** collaboration-decision  
**SLA:** 120m escalation if silent  
**Handlers:** humanaios.collaboration_handler()

---

## HANDLER IMPLEMENTATION CHECKLIST

### flta-app-empirica Handlers

- [ ] `audit_handler(proposal)`: Process resource-audit-request, return audit-result
- [ ] `completion_ack(proposal_id)`: Acknowledge result delivery
- [ ] `escalation_handler(escalation)`: Receive escalation from Admiral, log and respond

### grok-crossref Handlers

- [ ] `validation_handler(proposal)`: Process validation-request, return validation-result
- [ ] `divergence_detector(claim)`: Analyze for misalignment, send divergence-alert if needed
- [ ] `completion_ack(proposal_id)`: Acknowledge result delivery

### humanaios-internal Handlers

- [ ] `dispatch_handler(proposal)`: Process cross-project-dispatch, route to sub-projects
- [ ] `status_reporter()`: Send operational-status to autonomy (daily heartbeat)
- [ ] `resource_request_handler(request)`: Handle resource-allocation-request from sub-projects

### opportunity-aggregator Handlers

- [ ] `screening_handler(proposal)`: Process candidate-screening, return vetting-result
- [ ] `readiness_checker(candidate)`: Evaluate mesh-readiness, trigger escalation to Admiral
- [ ] `completion_ack(proposal_id)`: Acknowledge result delivery

### humanaios (Admiral) Handlers

- [ ] `escalation_handler(proposal)`: Receive escalation, make decision, broadcast
- [ ] `decision_handler(escalation)`: Route decision to all affected practices
- [ ] `governance_handler(update)`: Broadcast governance changes
- [ ] `divergence_handler(alert)`: Receive divergence-alert, investigate, escalate if needed

---

## SLA ENFORCEMENT RULES

### ACK SLA (Acknowledgment)
**Trigger:** Proposal received by target  
**Clock:** Starts when target receives proposal via mailbox  
**Deadline:** Practice must send mailbox reply with `status: in_progress`  
**Failure:** Silent > SLA → autonomy logs warning, continues waiting  
**Recovery:** Practice sends late ack, autonomy logs lateness

### Escalation SLA (Timeout)
**Trigger:** No final result received by SLA time  
**Clock:** Starts when proposal sent, pauses when ack received  
**Deadline:** Target must send final result via mailbox reply  
**Failure:** Silent > SLA → autonomy sends escalation to Admiral  
**Recovery:** Practice sends late result, autonomy logs lateness + Admiral's decision

### Critical SLA (Escalations Only)
**Trigger:** Escalation to Admiral sent  
**Clock:** Starts when escalation received  
**Deadline:** Admiral must send decision via mailbox reply  
**Failure:** Silent > 60m → autonomy re-pings Admiral, escalates to mesh-support  
**Recovery:** Admiral sends decision, practices receive and ack

---

## ROUTING DECISION FLOWCHART

```
Proposal arrives at autonomy
    |
    v
Is source = humanaios (Admiral)?
    |
    +--YES--> BROADCAST to all practices in SER 2
    |         (governance-update type)
    |
    +--NO--> Is target = humanaios (Admiral)?
              |
              +--YES--> Is escalation = true?
              |         |
              |         +--YES--> Route as PRIORITY (ack SLA 30m)
              |         |
              |         +--NO--> Route as ESCALATION (ack SLA 60m)
              |
              +--NO--> Forward to target practice
                       (Direct route)
                       Check message type:
                         - If request: expect response within SLA
                         - If result: deliver to waiter + ack
                         - If escalation: forward to Admiral

Target receives proposal via cortex mailbox
    |
    v
Handler function called (based on proposal_type)
    |
    v
Handler processes (internal work)
    |
    v
Handler sends mailbox reply:
    - First: ACK (in_progress)
    - Then: RESULT (completed)
    |
    v
Autonomy receives reply, logs to SER 2 + delivers
```

---

## CONFLICT RESOLUTION

### Simultaneous Proposals to Same Target
**Rule:** Queue by receive time; process serially (first-come, first-served)  
**Handler:** Target responds with ack for each, processes in queue order  
**SLA:** Each proposal gets independent SLA countdown (not cumulative)  
**Escalation:** If queue > 5 proposals, escalate backlog to Admiral

### Divergent Responses from Same Proposal
**Rule:** If target sends conflicting results (e.g., ack first, then negative result)  
**Handler:** Autonomy logs divergence as finding, escalates to Admiral  
**Recovery:** Admiral reviews, communicates correct interpretation to target

### Escalation Timeout on Critical Decision
**Rule:** Admiral silent > 60m on escalation  
**Handler:** autonomy sends re-ping + escalates to mesh-support  
**Resolution:** mesh-support reaches out to Admiral + practices involved

---

## MONITORING & OBSERVABILITY

### SER 2 Logging
Every proposal transition is logged to SER 2:
```
{
  "proposal_id": "uuid",
  "source": "ai_id",
  "target": "ai_id",
  "type": "message_type",
  "route": "DIRECT|PEER|ESCALATION|PRIORITY",
  "state": "sent|acked|in_progress|completed|escalated|failed",
  "timestamp": "ISO8601",
  "sla_ack_seconds": int,
  "sla_escalation_seconds": int,
  "ack_delivered_at": "ISO8601",
  "result_delivered_at": "ISO8601"
}
```

### Heartbeat Tracking
Each practice sends daily heartbeat to autonomy:
```json
{
  "source": "practice ai_id",
  "type": "heartbeat",
  "status": "mesh-active|degraded|offline",
  "listener_armed": true,
  "ntfy_topic": "empirica-foundation-orchestration-events-carly",
  "last_proposal_sent": "ISO8601",
  "last_proposal_received": "ISO8601",
  "pending_proposals": int
}
```

### Escalation Audit Trail
Every escalation is logged with full context:
```
escalation_id: uuid
source_practice: ai_id
escalation_reason: string
admiral_decision: string
decision_timestamp: ISO8601
practices_notified: [ai_ids]
follow_up_actions: [strings]
resolution_status: pending|resolved|escalated_further
```

---

**Next:** Verify this routing matrix in CHECK gate, then implement handlers in praxic phase
