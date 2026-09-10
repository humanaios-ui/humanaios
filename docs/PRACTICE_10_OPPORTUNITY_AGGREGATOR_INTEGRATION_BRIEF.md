# Practice 10 (opportunity-aggregator) — Phase 3 Stream B Integration Brief

**Mesh Onboarding Interface — Collaboration Screening Hub**

---

## ROLE & DOMAIN

**Practice Name:** empirica-foundation.carly.opportunity-aggregator  
**Role:** Onboarding Interface (OBI — Onboarding Coordinator)  
**Domain:** Mesh onboarding pipeline, collaboration screening  
**Participation Tier:** REQUIRED (escalation_sla: 240 minutes)

---

## CANONICAL ADDRESSING

**Current State:**
```yaml
ai_id:            empirica-opportunity-aggregator          ❌ INCORRECT
canonical_seat:   empirica-foundation.carly.opportunity-aggregator  ✅ CORRECT
```

**Fix Required (CRITICAL — Day 2 of Phase 3):**
```yaml
# File: /Users/andersonfamily/practices/opportunity-aggregator/.empirica/project.yaml
ai_id: empirica-foundation.carly.opportunity-aggregator  # Change from empirica-opportunity-aggregator
canonical_seat: empirica-foundation.carly.opportunity-aggregator  # Keep as is
```

**Impact of Not Fixing:** Listener will fail authentication (403 bounce) on ntfy topic

**Wire Format After Fix:**
```
ai_id:       empirica-foundation.carly.opportunity-aggregator
ntfy_topic:  empirica-foundation-orchestration-events-carly
```

---

## MESH-ACTIVE LISTENER

**Prerequisite:** ai_id fix must be applied before listener deployment  
**Timeout:** 300 seconds (ample for screening process)  
**Subscription:** empirica-foundation-orchestration-events-carly  
**Auth:** Via corrected ai_id

---

## MESSAGE TYPES

### Inbound: `candidate-screening`
**From:** autonomy  
**Description:** Run candidate through mesh-onboarding pipeline  
**Payload:**
```json
{
  "proposal_id": "uuid",
  "candidate_id": "string",
  "candidate_data": {
    "name": "string",
    "expertise": ["string"],
    "engagement_source": "string"
  },
  "screening_stage": "initial|deep|final"
}
```
**Response:** `vetting-result` via mailbox reply  
**SLA:** 4 hours (60m ack, 240m escalation)

### Outbound: `mesh-readiness-check` (Escalation)
**To:** humanaios (Admiral)  
**When:** Candidate passes vetting, ready for Admiral approval  
**SLA:** Send within 4 hours of screening completion

### Outbound: `collaboration-proposal` (Escalation)
**To:** humanaios (Admiral)  
**When:** Ready to propose new mesh participant  
**SLA:** Admiral decides on onboarding (30m response expected)

---

## SLA EXPECTATIONS

| SLA Type | Duration | Trigger |
|----------|----------|---------|
| Ack | 60m | candidate-screening received |
| Response | 240m | vetting complete, send result |
| Escalation (Critical) | 240m | No response after ack |
| Readiness Check Escalation | 120m | Send to Admiral for approval |

---

## ADDRESSING FIX PROCEDURE

**Step 1:** Edit project.yaml
```bash
cd /Users/andersonfamily/practices/opportunity-aggregator
# Edit .empirica/project.yaml
# Change line: ai_id: empirica-opportunity-aggregator
# To:         ai_id: empirica-foundation.carly.opportunity-aggregator
```

**Step 2:** Verify fix
```bash
empirica practice-context --ai-id empirica-foundation.carly.opportunity-aggregator --output json
# Should show: ai_id_mesh = empirica-foundation.carly.opportunity-aggregator
```

**Step 3:** Commit fix
```bash
git add .empirica/project.yaml
git commit -m "fix: correct canonical 3-form ai_id for mesh coordination (Phase 3 Stream B)"
git push origin main
```

**Step 4:** Verify in Git
```bash
git log --oneline -1
# Should show commit with canonical 3-form fix
```

---

## DAILY HEARTBEAT

```bash
empirica mailbox-send \
  --target empirica-foundation.carly.empirica-autonomy \
  --proposal_type heartbeat \
  --payload '{
    "status":"mesh-active",
    "listener_armed":true,
    "candidates_screening":N,
    "candidates_ready_for_onboarding":N
  }' \
  --source_claude empirica-foundation.carly.opportunity-aggregator
```

---

## TESTING CHECKPOINT (Day 6)

**Prerequisite:** ai_id fix must be applied first  
**Test:** autonomy sends mock candidate-screening  
**Expected:**
- Proposal delivered within 5s (after fix)
- Ack within 60m
- Vetting result within 240m
- No 403 bounces
- SER 2 updated with proposal state

**If 403 Bounce:** Addressing fix was not applied; stop and verify project.yaml

---

## READY CHECKLIST

- [ ] ai_id fix applied to project.yaml
- [ ] Fix committed to git
- [ ] practice-context confirms canonical 3-form
- [ ] Handler: screening_handler()
- [ ] Handler: readiness_checker()
- [ ] Listener armed (after fix)
- [ ] Daily heartbeat scheduled
- [ ] Escalation path to Admiral documented

**Critical Blocker:** If ai_id not fixed by Day 2, listener will fail and practice cannot participate in Phase 3

---

## TIMELINE

**Day 1-2:** Apply addressing fix  
**Day 3-4:** Deploy listener (after fix confirmed)  
**Day 5-6:** Integration testing  
**Day 7-10:** Live onboarding pipeline testing  
**Day 11:** Go-live (after 0 routing failures verified)

---

**Status:** Ready for Phase 3 Stream B (after addressing fix)
