# Admiral/Evaluator (humanaios) — Phase 3 Stream B Integration Brief

**Governance Gate — Critical Decision & Escalation Hub**

---

## ROLE & DOMAIN

**Practice Name:** empirica-foundation.carly.humanaios  
**Role:** Admiral/Evaluator (GTE — Governance Gate)  
**Domain:** Oversight, calibration assessment, critical decision gating  
**Participation Tier:** REQUIRED (escalation_sla: 60 minutes for critical)

---

## CANONICAL ADDRESSING

**Current State:**
```yaml
ai_id:            humanaios                               ❌ INCORRECT
canonical_seat:   empirica-foundation.carly.humanaios    ✅ CORRECT
```

**Fix Required (CRITICAL — Day 2 of Phase 3):**
```yaml
# File: /Users/andersonfamily/practices/humanaios/.empirica/project.yaml
ai_id: empirica-foundation.carly.humanaios  # Change from humanaios
canonical_seat: empirica-foundation.carly.humanaios  # Keep as is
```

**Impact of Not Fixing:** Admiral listener will fail authentication; escalations cannot be routed; entire Phase 3 governance framework fails

**Wire Format After Fix:**
```
ai_id:       empirica-foundation.carly.humanaios
ntfy_topic:  empirica-foundation-orchestration-events-carly
```

---

## MESH-ACTIVE LISTENER

**Prerequisite:** ai_id fix must be applied before listener deployment  
**Timeout:** 180 seconds (high-priority gate)  
**Subscription:** empirica-foundation-orchestration-events-carly  
**Auth:** Via corrected ai_id  
**Priority:** CRITICAL — Admiral's listener is highest priority in mesh

---

## MESSAGE TYPES

### Inbound: `escalation-decision` (PRIORITY)
**From:** autonomy  
**Description:** Critical decision requiring Admiral oversight  
**Payload:**
```json
{
  "proposal_id": "uuid",
  "escalation_source": "ai_id of escalating practice",
  "escalation_reason": "resource|governance|compliance|other",
  "context": "string",
  "suggested_actions": ["string"]
}
```
**Response:** `escalation-decision-result` via mailbox reply  
**SLA:** 60m to respond (30m ack, 60m escalation = critical timeout)

### Inbound: `divergence-alert` (PRIORITY)
**From:** grok-crossref  
**Description:** Independent validation flagged misalignment  
**SLA:** 45m response (15m ack, 45m escalation)

### Inbound: `governance-update` (Broadcast)
**From:** autonomy  
**Description:** Governance change broadcast to all practices  
**Action:** Receive + log to findings

### Outbound: `escalation-decision-result`
**To:** autonomy (for delivery to escalation source)  
**When:** Admiral makes decision  
**SLA:** Send within 60m of receiving escalation

### Outbound: `governance-update` (Broadcast)
**To:** all practices via autonomy  
**When:** Policy/procedure change needs distribution  
**Frequency:** As needed (non-recurring unless policy changes)

---

## SLA EXPECTATIONS

| SLA Type | Duration | Trigger | Severity |
|----------|----------|---------|----------|
| Ack (Escalation) | 30m | escalation-decision received | CRITICAL |
| Response (Escalation) | 60m | decision made | CRITICAL |
| Ack (Divergence) | 15m | divergence-alert received | PRIORITY |
| Response (Divergence) | 45m | investigation complete | PRIORITY |
| Ack (Routine) | 30m | governance-update received | NORMAL |

---

## ADDRESSING FIX PROCEDURE

**Step 1:** Edit project.yaml
```bash
cd /Users/andersonfamily/practices/humanaios
# Edit .empirica/project.yaml
# Change line: ai_id: humanaios
# To:         ai_id: empirica-foundation.carly.humanaios
```

**Step 2:** Verify fix
```bash
empirica practice-context --ai-id empirica-foundation.carly.humanaios --output json
# Should show: ai_id_mesh = empirica-foundation.carly.humanaios
```

**Step 3:** Commit fix
```bash
git add .empirica/project.yaml
git commit -m "fix: correct canonical 3-form ai_id for Admiral governance gate (Phase 3 Stream B)"
git push origin main
```

**Critical Note:** This fix enables Admiral to participate in Phase 3 orchestration. Without it, all escalations bounce (403).

---

## DECISION HANDLER PATTERNS

### Pattern 1: Resource Escalation
**Escalation From:** flta-app-empirica (audit blocked)  
**Admiral Action:**
1. Review resource status + availability
2. Decide: proceed_with_partial | retry_later | abort | escalate_further
3. Send decision back to escalation source via autonomy
4. Log decision to findings + SER 2

### Pattern 2: Divergence Alert
**Alert From:** grok-crossref (misalignment detected)  
**Admiral Action:**
1. Review divergence context + evidence
2. Decide: investigate_further | escalate_to_meshsupport | accept_divergence | retract_claim
3. Broadcast decision to involved practices
4. Log to findings as decision artifact

### Pattern 3: Governance Change
**Change From:** Admiral (self-initiated)  
**Admiral Action:**
1. Draft governance update
2. Send via cortex_publish (autonomy broadcasts)
3. All practices receive via heartbeat subscription
4. Document change in CLAUDE.md across practices

---

## DAILY HEARTBEAT

```bash
empirica mailbox-send \
  --target empirica-foundation.carly.empirica-autonomy \
  --proposal_type heartbeat \
  --payload '{
    "status":"mesh-active",
    "listener_armed":true,
    "escalations_pending":N,
    "escalations_resolved_this_week":N
  }' \
  --source_claude empirica-foundation.carly.humanaios
```

---

## TESTING CHECKPOINT (Day 6)

**Prerequisite:** ai_id fix must be applied first  
**Test Scenario:** autonomy sends mock escalation-decision  
**Expected:**
- Proposal delivered within 5s (after fix)
- Ack within 15m (Admiral priority)
- Decision response within 60m
- No 403 bounces
- SER 2 updated with escalation state

**If 403 Bounce:** Addressing fix was not applied; verify project.yaml

---

## READY CHECKLIST

- [ ] ai_id fix applied to project.yaml
- [ ] Fix committed to git
- [ ] practice-context confirms canonical 3-form
- [ ] Handler: escalation_handler()
- [ ] Handler: divergence_handler()
- [ ] Handler: governance_handler()
- [ ] Listener armed (after fix, timeout = 180s)
- [ ] Daily heartbeat scheduled
- [ ] Decision patterns documented + agreed
- [ ] SLA expectations (60m critical) understood

**Critical Blocker:** If ai_id not fixed by Day 2, Admiral cannot receive escalations and entire orchestration framework fails

---

## TIMELINE

**Day 1-2:** Apply addressing fix (CRITICAL PATH)  
**Day 3-4:** Deploy listener (after fix confirmed)  
**Day 5-6:** Integration testing with escalations  
**Day 7-8:** Escalation drill (test 4h timeout re-ping)  
**Day 9-10:** Live decision-making during cross-practice proposals  
**Day 11:** Go-live (after 0 escalation routing failures verified)

---

## ESCALATION OVERFLOW PROTOCOL

**If Admiral receives > 5 escalations simultaneously:**
1. Triage by severity (critical > priority > normal)
2. Process critical first (60m SLA)
3. Log others to queue
4. If queue > 10, escalate to empirica-mesh-support for triage support
5. Document overflow in findings

---

**Status:** Ready for Phase 3 Stream B (after addressing fix)
