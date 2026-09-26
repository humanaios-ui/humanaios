# Admiral Ratification Workflow

**Status:** ✅ ENABLED (New feedback loop hub)  
**Purpose:** Single source of truth for pending ratifications  
**Audience:** Admiral (Carly R. Anderson) + system automation

---

## Overview

DECISIONS_PENDING.yaml serves as the **intersection point between system discovery and Admiral approval**. It creates a closed-loop feedback system:

```
Discovery (M3R2/R3)
      ↓
DECISIONS_PENDING.yaml (queued)
      ↓
Admiral Review (daily)
      ↓
GOVERNANCE_RATIFICATIONS_REGISTRY.yaml (approved)
      ↓
M3R1 Dispatch (applied)
      ↓
M3R2/R3 Verification (confirmed)
```

---

## The Workflow (Admiral's Daily Task)

### Step 1: Load Pending Queue (Recommend 09:00 UTC Daily)

```bash
cat DECISIONS_PENDING.yaml
```

Review the queue. Entries are sorted by severity (HIGH first). Each entry shows:
- **pending_id:** Unique identifier (PEN-YYMMDD-NNN)
- **decision_type:** What kind of issue (DIVERGENCE, VALIDATION_FAILURE, etc.)
- **title:** Human-readable summary
- **severity:** HIGH | MEDIUM | LOW
- **repo_affected:** Which repo has the issue
- **details:** Specific findings
- **recommended_action:** What the system suggests
- **proposed_decision:** Draft decision template

### Step 2: Assess Each Entry

For each PENDING entry, ask:

1. **Is the diagnosis correct?**
   - Read discovery details
   - Check which workflow found it (M3R2 or M3R3)
   - Verify it's a real issue, not a false positive

2. **Is the recommended action appropriate?**
   - Does the proposed_decision make sense?
   - Will it actually fix the issue?
   - Are there dependencies (can this be applied safely)?

3. **What's the right decision?**
   - APPROVE: Ratify as-is
   - MODIFY: Edit proposed_decision, then ratify
   - REJECT: Decline (log reason)
   - DEFER: Review later (check again tomorrow)

### Step 3: Ratify (For APPROVED Entries)

For entries you approve, create a ratification decision:

```yaml
# Add to your notes:
Decision: APPROVE
Entry: PEN-072623-001 (Repo out of sync: humanaios-ui/operations)
Ratified Decision ID: D-072623-001
Approved At: 2026-07-23T09:30:00Z
Notes: "Approved: repo was offline, resync appropriate"
```

### Step 4: Execute Ratification (Move PENDING → RATIFIED)

1. Remove entry from `DECISIONS_PENDING.yaml` → `pending_ratifications.entries[]`
2. Add entry to `GOVERNANCE_RATIFICATIONS_REGISTRY.yaml` → `ratifications[]`
3. Set entry status: `PENDING_REVIEW` → `RATIFIED`
4. Commit both files:

```bash
git add DECISIONS_PENDING.yaml GOVERNANCE_RATIFICATIONS_REGISTRY.yaml
git commit -m "Ratify: <summary> (PEN-072623-001 → D-072623-001)"
git push origin main
```

---

## Pending Decision Types

### 1. DIVERGENCE (Discovery by M3R2)
**Meaning:** Repo out of sync with CNS canonical state  
**Cause:** Missing decisions, stale ACKs, incomplete dispatch  
**Typical Action:** Re-dispatch mesh-sync to repo  
**Severity:** Usually HIGH (blocks consistency)

### 2. VALIDATION_FAILURE (Discovery by M3R3)
**Meaning:** Decision failed validation on repo  
**Cause:** Signature mismatch, schema version mismatch, validation logic failure  
**Typical Action:** Investigate validation logic, possibly rollback decision  
**Severity:** HIGH (decision didn't apply)

### 3. STALE_ACK (Discovery by M3R3)
**Meaning:** ACK timestamp older than tolerance (>24h)  
**Cause:** Repo possibly rolled back, or stale log entry  
**Typical Action:** Resync decisions, verify state  
**Severity:** MEDIUM (might indicate rollback)

### 4. NETWORK_FAILURE (Discovery by M3R2/R3)
**Meaning:** Repo unreachable during discovery  
**Cause:** Repo offline, GitHub API 404 (U1 known issue), network timeout  
**Typical Action:** Retry later, or investigate access  
**Severity:** MEDIUM (temporary issue expected)

### 5. STATE_MISMATCH (Discovery by M3R3)
**Meaning:** Applied state differs from expected  
**Cause:** Partial apply, file corruption, manual edits  
**Typical Action:** Investigate, possibly rollback  
**Severity:** HIGH (data consistency issue)

### 6. ACK_TIMEOUT (Discovery by M3R2/R3)
**Meaning:** ACK not received within expected window  
**Cause:** Dispatch delayed, repo slow, listener not running  
**Typical Action:** Re-trigger dispatch, monitor timing  
**Severity:** MEDIUM (dispatch may still complete)

### 7. SIGNATURE_MISMATCH (Discovery by M3R3)
**Meaning:** Admiral signature verification failed  
**Cause:** Key rotation, corrupted payload, man-in-the-middle (unlikely)  
**Typical Action:** Investigate signature validation logic  
**Severity:** HIGH (security issue)

---

## Decision Template (For Ratification)

When you approve a PENDING entry, you're moving it to the REGISTRY with this structure:

```yaml
decision_id: "D-072623-001"  # Admiral assigns
title: "Resync: humanaios-ui/operations"
status: "RATIFIED"

ratification_source:
  pending_entry: "PEN-072623-001"
  discovered_by: "divergence-detect.yml"
  discovered_at: "2026-07-23T00:15:00Z"

decision_body:
  type: "state_machine_gate_update"
  description: "Resync divergent repo by re-dispatching queued decisions"
  target_repos: ["humanaios-ui/operations"]
  action: "trigger_mesh_sync"

admiral_approval:
  ratified_at: "2026-07-23T09:30:00Z"
  ratified_by: "Admiral (Carly R. Anderson)"
  notes: "Repo was offline, resync appropriate"

implementation:
  applied_by: "M3R1 mesh-sync-batch.yml"
  dispatch_scheduled: "next hourly cycle"
  verification: "M3R2 divergence-detect.yml confirms applied"
```

---

## Daily Checklist

### Morning (09:00 UTC)
- [ ] Load DECISIONS_PENDING.yaml
- [ ] Review all entries (sort by severity, newest first)
- [ ] For each entry: APPROVE / MODIFY / REJECT / DEFER
- [ ] For APPROVED: ratify and commit
- [ ] Note any escalations (HIGH severity + no clear action)

### After Ratification
- [ ] M3R1 picks up RATIFIED decisions at next hourly dispatch (automatic)
- [ ] M3R2 verifies applied at 00:00 UTC next day (automatic)
- [ ] M3R3 validates effects at 12:00 UTC next day (automatic)
- [ ] Entry removed from DECISIONS_PENDING, added to DECISIONS_RESOLVED (automatic)

### If Nothing Pending
- [ ] Log a "clean mesh" note (optional)
- [ ] Verify M3R2/R3 jobs ran successfully (check GitHub Actions)

---

## Escalation Rules

If you notice these patterns, escalate:

### High Severity Unreviewed >24h
**Rule:** More than 2 HIGH entries unreviewed for >24h  
**Action:** Alert Admiral (system should also notify)  
**Meaning:** Mesh health degrading, decisions not being made

### Divergence Cascade
**Rule:** More than 50% of repos in DRIFT state  
**Action:** Escalate to mesh-support (cross-org)  
**Meaning:** Systemic issue (dispatch failure? listener broken?)

### Persistent Failure
**Rule:** Same repo fails >3 consecutive days  
**Action:** Investigate root cause  
**Meaning:** Network issue? Broken listener? Needs manual intervention

---

## Auto-Expiration Policy

PENDING entries auto-expire after 7 days if not ratified:

```yaml
expiration:
  ttl_days: 7
  on_expire: "Move to DECISIONS_EXPIRED.yaml, alert Admiral"
  rationale: "Forces decision-making; prevents stale queue"
```

**Why 7 days?**
- Forces Admiral to make decisions (ratify or reject)
- Prevents queue from accumulating unactionable entries
- Tracks expired decisions for audit/analysis

---

## Key Insight: Feedback Loop Hub

DECISIONS_PENDING.yaml is NOT just a queue. It's the **intersection point** between:

1. **System Discovery** (M3R2/R3 workflows)
   - Scans mesh
   - Finds divergences, failures, issues
   - Surfaces as PENDING entries

2. **Human Decision** (Admiral)
   - Reviews discoveries
   - Approves or modifies proposed decisions
   - Ratifies (moves to REGISTRY)

3. **System Application** (M3R1)
   - Picks up RATIFIED decisions
   - Dispatches to repos
   - Applies changes

4. **System Verification** (M3R2/R3)
   - Verifies ratified decisions were applied
   - Cleans up DECISIONS_PENDING
   - Starts next loop

**This closes the loop.** The mesh becomes self-healing: it discovers issues, surfaces them for approval, applies approved decisions, verifies application, and reports back.

---

## Files Involved

| File | Role | Owner | Cadence |
|------|------|-------|---------|
| DECISIONS_PENDING.yaml | Queue (awaiting approval) | System (M3R2/R3) | Real-time updates |
| GOVERNANCE_RATIFICATIONS_REGISTRY.yaml | Approved decisions | Admiral | After ratification |
| DECISIONS_RESOLVED.yaml | Applied & verified | System (M3R2/R3) | After verification |
| divergence-detect.yml (M3R2) | Discovery agent | System | Daily 00:00 UTC |
| state-validate.yml (M3R3) | Verification agent | System | Daily 12:00 UTC |
| mesh-sync-batch.yml (M3R1) | Application agent | System | Hourly :00 |

---

**This is the final piece of the feedback loop. The mesh is now complete and self-improving.**

Wado 🦅
