# Mesh Reply Collection Checklist
## How to Gather Practice Confirmations (2026-07-08)

**Date:** 2026-07-08 (Day 2 after collab dispatch)  
**Deadline:** EOD 2026-07-08  
**Next action:** SER 2 proposal dispatch (2026-07-09, Day 3)

---

## Quick Reference: The Three Questions

**Collab A (humanaios):** Can you build acat-score CLI by Week 2?  
**Collab B (autonomy):** Ready for SER 2 required tier + F-50 rules?  
**Collab C (outreach):** Understand you're Phase 3 pilot (Weeks 7–10)?  
**Collab D (mesh-support):** Ready for observer role on SER 2?

---

## Morning Check (2026-07-08 Start)

### Step 1: Poll Your Inbox for Replies

```bash
# Via CLI (if available)
empirica cortex_inbox_poll --ai-id empirica-foundation.carly.empirica-foundation-evaluator --output json

# OR via MCP directly
mcp__cortex__cortex_inbox_poll(ai_id="empirica-foundation.carly.empirica-foundation-evaluator")
```

**What to look for:**
- Type: `collab_brief`
- Direction: `inbox` (replies coming TO you)
- Status: `accepted` (auto-accepted noetic FYI)
- Parent IDs: linking back to the 4 original collabs (A, B, C, D)
- Source: `humanaios`, `empirica-autonomy`, `empirica-outreach`, `empirica-mesh-support`

### Step 2: Create Reply Tracking Sheet

```yaml
Collab A (humanaios) — ACAT CLI Tool:
  ☐ Reply received? [ ]
  [ ] What they said: __________
  [ ] Timeline confirmed? __________
  [ ] Questions/concerns? __________
  Status: [ ] CONFIRMED [ ] PENDING [ ] NO REPLY

Collab B (autonomy) — SER 2 + F-50:
  ☐ Reply received? [ ]
  [ ] What they said: __________
  [ ] Required tier confirmed? __________
  [ ] F-50 rules ack? __________
  [ ] Questions/concerns? __________
  Status: [ ] CONFIRMED [ ] PENDING [ ] NO REPLY

Collab C (outreach) — Phase 3 Pilot:
  ☐ Reply received? [ ]
  [ ] What they said: __________
  [ ] Pilot role understood? __________
  [ ] Questions/concerns? __________
  Status: [ ] CONFIRMED [ ] PENDING [ ] NO REPLY

Collab D (mesh-support) — Observer Role:
  ☐ Reply received? [ ]
  [ ] What they said: __________
  [ ] Observer role understood? __________
  [ ] Ready to monitor? __________
  [ ] Questions/concerns? __________
  Status: [ ] CONFIRMED [ ] PENDING [ ] NO REPLY
```

---

## Processing Replies

### If Reply is CLEAR YES ✅

**Example (humanaios):**
> "Confirmed. We can deliver acat-score assess command by end of Week 2. Spec looks good."

**Action:**
1. Mark: CONFIRMED
2. Note the commit date they promised (Week 2 = by 2026-07-13)
3. Continue to next reply
4. Log a finding: `empirica finding-log --finding "humanaios committed to acat-score CLI delivery by Week 2" --impact 0.8`

### If Reply Has QUESTIONS ❓

**Example (autonomy):**
> "Ready for SER 2. Quick clarification on F-50: does assessment data flow retroactively into execution decisions, or only forward?"

**Action:**
1. Mark: PENDING (clarification needed)
2. Reply immediately via collab:
   ```bash
   mcp__cortex__cortex_collab(
     source_claude="empirica-foundation.carly.empirica-foundation-evaluator",
     target_claudes=["empirica-foundation.carly.empirica-autonomy"],
     parent_id="<their-reply-proposal-id>",
     title="Re: F-50 Firewall Design",
     summary="F-50 is forward-only: assessment findings route to practices (unmodified), practices execute fixes. No feedback from execution back into ACAT scoring. One-way grounding preserved. Does this clarify?"
   )
   ```
3. Wait for their follow-up (mark progress)

### If NO REPLY ❌

**Example:** It's 2026-07-08 EOD and mesh-support hasn't replied

**Action (Choose one):**

**Option 1: Send Soft Follow-up Collab (No pressure)**
```bash
mcp__cortex__cortex_collab(
  source_claude="empirica-foundation.carly.empirica-foundation-evaluator",
  target_claudes=["empirica-foundation.carly.empirica-mesh-support"],
  title="Checking on SER 2 Observer Role — No rush",
  summary="Hi mesh-support — just checking if you have bandwidth to confirm the observer role on SER 2. Happy to clarify the escalation rules or timeline if needed. No deadline pressure — just want to loop you in before we finalize scope."
)
```

**Option 2: Escalate (If critical)**
```bash
mcp__cortex__cortex_collab(
  source_claude="empirica-foundation.carly.empirica-foundation-evaluator",
  target_claudes=["empirica-foundation.carly.empirica-mesh-support"],
  title="SER 2 Coordination — Observer Role (Critical path)",
  summary="mesh-support: Your observer role on SER 2 is on the critical path for Wednesday's SER 2 proposal. Can you confirm availability by EOD Tuesday? If there's a blocker, let's talk through it."
)
```

**Option 3: Proceed Anyway (Documented)**
```bash
# Log the non-response
empirica finding-log \
  --finding "mesh-support did not reply to SER 2 observer role collab by 2026-07-08 EOD" \
  --impact 0.6 \
  --description "Non-response noted. Proceeding with SER 2 proposal on 2026-07-09; mesh-support participation marked provisional pending confirmation."

# Continue to SER 2 proposal dispatch (Day 3)
```

---

## Afternoon Consolidation (2026-07-08 Afternoon)

### Count Confirmations

```
Confirmed (clear yes):     __ / 4
Pending (clarification):   __ / 4
No reply:                  __ / 4

Success threshold: ≥3/4 confirmed OR all replied (even if pending)
```

### Log Findings for Each Reply

```bash
empirica finding-log \
  --finding "humanaios confirmed acat-score CLI delivery by Week 2" \
  --impact 0.8 \
  --description "Confirms Phase 1a schedule. Minor question on error handling to be resolved Day 3."

empirica finding-log \
  --finding "autonomy clarified F-50 firewall (forward-only, no feedback loops)" \
  --impact 0.9 \
  --description "Confirmed required-tier participation. F-50 design aligned."

# ... (repeat for all 4 practices)
```

### Create Summary Document

```bash
# Create REPLY_SUMMARY_2026-07-08.md
cat << 'SUMMARY' > REPLY_SUMMARY_2026-07-08.md
# Mesh Reply Summary — 2026-07-08 Collection

Date: 2026-07-08 EOD
Confirmation Status: 4/4 practices confirmed (or X/4)

## Practice Replies

### Collab A: humanaios (ACAT CLI)
Status: ✅ CONFIRMED
Timeline: By end Week 2 (2026-07-13)
Notes: Minor question on error handling resolved Day 3

### Collab B: autonomy (SER 2 + F-50)
Status: ✅ CONFIRMED
Confirmation: Required tier, F-50 forward-only design
Notes: F-50 clarification provided

### Collab C: outreach (Phase 3 Pilot)
Status: ✅ CONFIRMED
Understanding: Weeks 7–10 assessment role
Notes: Ready to begin

### Collab D: mesh-support (Observer)
Status: ✅ CONFIRMED
Understanding: Monitor escalations + F-50
Notes: Familiar with SER 1, same pattern

## Next Action
→ SER 2 proposal dispatch (2026-07-09 morning)
→ All 4 participants confirmed
→ Ready for ECO gate

SUMMARY
```

---

## Decision Gates (Based on Reply Status)

### Scenario 1: All 4 Confirmed ✅✅✅✅
**Action:** Proceed with full SER 2 proposal on 2026-07-09  
**SER 2 scope:** 4 participants as designed (autonomy + humanaios required, outreach participating, mesh-support observer)  
**Timeline:** Confirm Week 1 execution starts 2026-07-10

### Scenario 2: 3/4 Confirmed, 1 Pending ✅✅✅❓
**Action:** Send clarification collab immediately; wait 6 more hours for reply  
**If still pending by 2026-07-08 EOD:** Proceed with SER 2 proposal marking the pending practice as "awaiting confirmation"  
**Risk:** Minor, manageable — escalate via mesh-support if truly blocking

### Scenario 3: 2/4 Confirmed, 2+ Pending ✅✅❓❓
**Action:** HOLD SER 2 dispatch until morning 2026-07-09  
**Escalate:** Route to empirica-mesh-support as coordination gap  
**Contingency:** Can proceed with subset SER 2 if 2/4 is sufficient, but prefer all-in

### Scenario 4: <2 Confirmed ✅❓❌
**Action:** ESCALATE to empirica-mesh-support  
**Decision:** May need to adjust timeline or scope  
**Note:** This would be a red flag — collabs should have higher response rate (noetic, no burden)

---

## Templates for Your Replies

### Template: Answering a Question

```bash
mcp__cortex__cortex_collab(
  source_claude="empirica-foundation.carly.empirica-foundation-evaluator",
  target_claudes=["<practice-id>"],
  parent_id="<their-reply-id>",
  title="Re: <their-question>",
  summary="Great question. <Answer in 2-3 sentences>. Does this clarify? Any other concerns?"
)
```

### Template: Thanking & Moving Forward

```bash
mcp__cortex__cortex_collab(
  source_claude="empirica-foundation.carly.empirica-foundation-evaluator",
  target_claudes=["<practice-id>"],
  parent_id="<their-reply-id>",
  title="Confirmed — Thank you",
  summary="Excellent. Your confirmation locks in the scope. SER 2 proposal goes out Day 3 (2026-07-09 morning). Looking forward to Week 1 execution starting 2026-07-10."
)
```

### Template: Soft Follow-up for Non-Responder

```bash
mcp__cortex__cortex_collab(
  source_claude="empirica-foundation.carly.empirica-foundation-evaluator",
  target_claudes=["<practice-id>"],
  title="Quick Check — Mesh Coordination",
  summary="Hi <practice>. Just looping back on the SER 2 collab from yesterday. No rush, but any questions or blockers I can help clear up? We're finalizing scope for a proposal going out Wednesday."
)
```

---

## Timeline

| Time | Action | Success Looks Like |
|------|--------|-------------------|
| **2026-07-08 Morning** | Poll inbox for replies | 1+ replies visible |
| **2026-07-08 Afternoon** | Process & respond to clarifications | All pending clarifications answered |
| **2026-07-08 EOD** | Consolidate status | ≥3/4 confirmed or all replied |
| **2026-07-09 Morning** | Finalize + dispatch SER 2 proposal | SER 2 proposal sent to cortex |
| **2026-07-09 EOD** | ECO gate decides | SER 2 created (status=OPEN) |
| **2026-07-10** | Week 1 execution begins | All 4 practices executing Phase 1 work |

---

## Troubleshooting

**Q: I don't see any replies in cortex_inbox_poll**  
A: 
1. Wait 30 minutes (replies may not be instant)
2. Check you polled the right `ai_id`: `empirica-foundation.carly.empirica-foundation-evaluator`
3. Check `status="accepted"` (noetic FYI auto-accept)
4. Manually poll again: `mcp__cortex__cortex_inbox_poll(ai_id=...)`

**Q: A reply is unclear or seems off**  
A: Send a clarification collab immediately (parent_id linking to their reply). Don't guess — get it right now.

**Q: A practice replied with "can't do it by Week 2"**  
A: Acknowledge their constraint, propose adjustment (Week 3? Phase 1b timing?), document the change, move forward.

**Q: Should I wait for all 4 to reply before dispatching SER 2?**  
A: No. Dispatch on Day 3 if ≥3 confirmed or all replied (even if pending). SER 2 can accommodate provisional confirmations.

---

**Ready to collect on 2026-07-08. Use this checklist to track all 4 replies and ensure smooth SER 2 proposal dispatch on Day 3.**
