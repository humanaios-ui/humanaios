# Escalation Protocol — Zone Transitions & Decision Gates

**Version:** 1.0  
**Status:** M2 Rank 1 Task 3 (DRAFT — awaiting Admiral ratification)  
**Authority:** empirica-foundation Admiral (Carly R. Anderson)  
**Date:** 2026-07-18

---

## Executive Summary

This protocol defines when and how decisions escalate between governance zones, what communication is required, and who makes the final call at each gate. It is the operational complement to AUTHORITY_MATRIX.yaml.

**Key principle:** Escalation is triggered by **objective conditions** (found objections, failed CHECK gate, P3 verification failure), not subjective judgment. A practitioner facing an escalation trigger does not decide whether to escalate — they **must** escalate and document it.

---

## Table of Contents

1. [Escalation Triggers (6 patterns)](#escalation-triggers)
2. [Zone Transition Paths](#zone-transition-paths)
3. [Communication Protocol](#communication-protocol)
4. [Approval Workflow](#approval-workflow-per-zone)
5. [Decision Gates](#decision-gates)
6. [Special Cases](#special-cases)
7. [Enforcement & Audit](#enforcement--audit)

---

## Escalation Triggers

### Trigger 1: Objection in Zone 1 (Chat/Collab)

**Condition:** Any participant in a Zone 1 deliberation (Slack thread, collab mesh, proposal discussion) expresses a concern, objection, or "needs more info" response.

**Who detects:** The proposal originator or Admiral.

**What to do:**
1. **Do NOT auto-approve.** Zone 1 auto-approval rules say "zero objections after 24h" — one objection breaks the 24h window.
2. **Log the objection:** Reply with `empirica finding-log --finding "Zone 1 objection: <concern>" --impact 0.6` (or include in Slack thread).
3. **Attempt resolution:** Can you answer the objection in chat? If yes → reply + reset the 24h window. If no → escalate.
4. **Escalate to Zone 2:** Message: "Zone 1 objection unresolved. Escalating to Admiral for Zone 2 authority decision."

**Latency:** Same business day.

**Escalation target:** Zone 2 (Admiral authority decision).

**Example:**

```
Zone 1 (Slack #wgs-sync):
  Practitioner A: "Let's add calibration_weights to project.yaml for all 9 practices"
  Practitioner B: "Concerned about backward compat — do we support the old schema?"
  
  → Trigger detected: objection raised
  
  Practitioner A: "Good point. Looking into schema versioning..."
  [5 minutes later]
  
  Practitioner A: "empirica finding-log: Schema v1 doesn't have calibration_weights, v1.1 does.
                   We can support both. Auto-default for old schemas."
  Practitioner B: "✓ OK with that approach"
  
  → Objection resolved in Zone 1. 24h window resets.
  
  [24h later, still no objections]
  
  → Zone 1 auto-approval → escalate to Zone 2
```

---

### Trigger 2: Veto / Block in Zone 2 (Authority Decision)

**Condition:** The Zone 2 decision-maker (Admiral or delegated authority) reviews the proposal + findings and decides "BLOCKED" or "CONDITIONAL — needs major revision."

**Who detects:** The Admiral (authority decision-maker).

**What to do:**
1. **Document the veto:** Write a decision-log with rationale. Example: "Blocked: dependency update breaks schema compatibility. Requires migration plan (missing)."
2. **Return to Zone 1:** Reply to the originator: "Your proposal is blocked per [decision-log ID]. Revised proposal needed by [date]."
3. **Set revision deadline:** Typically 3–5 business days for major revisions.

**Latency:** Veto same-day or next-day. Revision window: 3–5 days.

**Escalation target:** Return to Zone 1 (proposer revises; Admiral re-reviews).

**Example:**

```
Zone 2 (Admiral review):
  Proposal: "Update mcp version from 1.5 to 2.0 across all 9 practices"
  Findings: Version 2.0 has breaking API changes. No migration plan documented.
  
  Admiral decision: "BLOCKED"
  
  decision-log: "Blocked: breaking API change (mcp v1.5 → v2.0) requires
                migration plan for each practice. Version compatibility matrix
                missing. Revise by 2026-07-25."
  
  → Return to Zone 1 (proposer authors migration guide)
  → Re-submit to Zone 2 (Admiral re-reviews)
```

---

### Trigger 3: CHECK Gate Failure (empirica vectors below threshold)

**Condition:** Practitioner runs `empirica check-submit` and Sentinel returns `investigate` (vectors below threshold) or flags intent gaps.

**Who detects:** The Sentinel (empirica infrastructure).

**What to do:**
1. **Log the CHECK failure:** Empirica automatically creates a session snapshot.
2. **Investigate the gaps:** Go back to NOETIC phase (read more code, log more findings, resolve unknowns).
3. **Re-run CHECK:** Once vectors improve, re-submit CHECK.
4. **If vectors won't improve:** This signals the proposal is not ready. Escalate to Admiral via decision-log: "Unable to reach CHECK threshold. Vectors plateau at know=0.6, uncertainty=0.5. Needs architectural guidance."

**Latency:** Immediate (CHECK failure halts praxic progression).

**Escalation target:** Zone 2 (Admiral guidance or proposal rejection).

**Example:**

```
Practitioner work (NOETIC → CHECK):
  Vector estimates: know=0.75, uncertainty=0.35, context=0.7, clarity=0.8
  
  $ empirica check-submit - << EOF
  { "vectors": { "know": 0.75, "uncertainty": 0.35, ... } }
  EOF
  
  Response: "investigate" (vectors below threshold)
  Intent gaps: "Unknown: How does this interact with existing schema?"
  
  → HALT PRAXIC. Return to NOETIC.
  → Read schema docs, log finding.
  
  Re-estimated vectors: know=0.8, uncertainty=0.25
  
  $ empirica check-submit - << EOF
  { "vectors": { "know": 0.8, "uncertainty": 0.25, ... } }
  EOF
  
  Response: "proceed" → Zone 3 (PRAXIC authorized)
```

---

### Trigger 4: P3 Verification Failure (Zone 3)

**Condition:** After `git push` in Zone 3, the practitioner runs P3 verification (curl raw.githubusercontent.com) and the change is NOT visible, OR CI/CD checks fail.

**Who detects:** The Zone 3 executor (practitioner).

**What to do:**
1. **HALT immediately.** Do NOT proceed to the next file.
2. **Investigate:** Check git status, verify commit was pushed, check GitHub Actions logs.
3. **Common causes:**
   - Push failed (auth issue, network timeout)
   - Wrong branch (committed to feature branch, not main)
   - CI/CD caught an error (linting, type check, test failure)
4. **Resolve the issue:**
   - If push issue: re-authenticate, retry push.
   - If CI/CD failure: fix the code, re-commit, re-push.
5. **Log the failure:** `empirica dead-end-log --approach "Direct push to main" --why-failed "CI/CD failed: linting error"` (if applicable).
6. **Escalate if unresolvable:** "P3 verification failed after 3 retries. CI/CD error unresolved. Escalating to Admiral."

**Latency:** Immediate (don't move to next file).

**Escalation target:** Zone 2 (Admiral review) → potentially Zone 1 (proposal abandoned or revised).

**Example:**

```
Zone 3 (Terminal execution):
  Practitioner: Edited project.yaml, committed (commit abc123)
  
  $ git push origin main
  > Pushing... OK
  
  P3 Verification:
  $ curl -sS https://raw.githubusercontent.com/.../project.yaml | grep "calibration_weights"
  > (no output — change NOT visible)
  
  → TRIGGER: P3 verification failure
  
  Investigation:
  $ git status
  > On branch main, everything up to date
  
  $ git log --oneline | head -3
  > abc123 Commit message
  
  $ git branch --show-current
  > main ✓
  
  GitHub Actions log: "Lint error: YAML syntax invalid"
  
  → Root cause: YAML syntax error (linter blocked merge)
  
  Fix: Correct YAML syntax, re-commit (commit def456)
  
  $ git push origin main
  $ curl -sS ... | grep "calibration_weights"
  > (now visible) ✓
  
  → P3 verification PASSES → continue
```

---

### Trigger 5: Cross-Practice Impact Detected (During any zone)

**Condition:** A change is discovered that affects multiple practices or shared systems, but was proposed as single-practice work.

**Who detects:** A peer practice or Admiral reviewing the findings.

**What to do:**
1. **PAUSE the proposal.** Don't let it proceed to Zone 3.
2. **Log the discovery:** `empirica finding-log --finding "Cross-practice impact detected: change affects empirica-mesh-support schema" --impact 0.8`
3. **Escalate to Admiral:** "Cross-practice impact identified. Needs empirica-mesh-support coordination."
4. **Restart at Zone 1:** Treat as a new cross-practice proposal (coordinated collab mesh).

**Latency:** Same-day escalation.

**Escalation target:** Zone 1 (restart as cross-practice collab).

**Example:**

```
Practitioner X (Zone 2 review, empirica-autonomy change):
  Proposal: "Update empirica-cli version to 1.13.0 in autonomy"
  Findings: CLI change includes new mesh-send API.
  
  Peer review comment: "This new API affects empirica-mesh-support.
                       Need to coordinate their implementation too."
  
  → TRIGGER: Cross-practice impact detected
  
  Decision: Escalate to cross-practice collab.
  
  New proposal (Zone 1): "Coordinate empirica-cli 1.13.0 rollout with
                         empirica-autonomy + empirica-mesh-support.
                         Both must implement new mesh-send API."
  
  Collab mesh: autonomy + mesh-support team members join.
  
  → Proceed as multi-practice Zone 1 deliberation
```

---

### Trigger 6: Unknown Discovered During Zone 3 Execution (C-6 Violation)

**Condition:** During Zone 3 execution, the practitioner discovers a file or system that needs editing but is NOT in the Zone 2 authority document's "files affected" matrix. Per Z3_PROTOCOL.md Section C-6, this is a violation.

**Who detects:** The Zone 3 executor.

**What to do:**
1. **STOP immediately.** Do NOT edit the file.
2. **Log the discovery:** `empirica unknown-log --unknown "Discovered X during execution, but not in authority doc matrix"`
3. **Surface as Z2 question:** Reply to Admiral: "Discovered [file] needs editing for this change to work, but it's not in the authority matrix. Is this in scope?"
4. **Halt execution:** Don't proceed until Admiral clarifies.

**Latency:** Immediate.

**Escalation target:** Zone 2 (Admiral clarification).

**Example:**

```
Zone 3 (Terminal execution, empirica-outreach project):
  Authority doc: "Update project.yaml calibration_weights field"
  Practitioner: Edits project.yaml, commits (per C-1 to C-5).
  
  During P3 verification, notices: "But the CLI tool won't read
  the new field unless we also update CLAUDE.md default-vectors section."
  
  → TRIGGER: Unauthorized file discovered (C-6 violation)
  
  Escalation: "Discovered CLAUDE.md default-vectors needs update.
              Not in authority matrix. Awaiting Admiral clarification."
  
  Admiral reply: "CLAUDE.md updates are separate Zone 2 decision.
                 Halt the current session. Regroup for multi-file change."
  
  → Authority doc REVISED to include CLAUDE.md
  → Restart at Zone 1 (new proposal: "Update project.yaml + CLAUDE.md together")
```

---

## Zone Transition Paths

```
┌──────────────────────────────────────────────────────────────────────┐
│ ZONE 1: Deliberation (PREFLIGHT + NOETIC)                          │
│ - Collab, proposals, findings, unknowns                             │
│ - Auto-approval if zero objections after 24h–72h                    │
└──────────┬───────────────────────────────────────────────────────────┘
           │
     [Objection found?]
           ├─ YES → Trigger 1 (stay in Zone 1, resolve)
           └─ NO → (no objections) proceed to Zone 2
                  
           │
           ▼
┌──────────────────────────────────────────────────────────────────────┐
│ ZONE 2: Authority Decision (CHECK gate, empirica)                  │
│ - Authority doc review + Sentinel CHECK                             │
│ - Admiral decides: APPROVE / CONDITIONAL / BLOCKED                  │
└──────────┬───────────────────────────────────────────────────────────┘
           │
     [Admiral decision]
           ├─ BLOCKED → Trigger 2 (return to Zone 1, revise)
           ├─ CONDITIONAL → Trigger 2 (return to Zone 1, address conditions)
           ├─ APPROVED & CHECK=proceed → proceed to Zone 3
           └─ APPROVED & CHECK=investigate → Trigger 3 (NOETIC more)
                  
           │
           ▼
┌──────────────────────────────────────────────────────────────────────┐
│ ZONE 3: Execution (PRAXIC + POSTFLIGHT)                             │
│ - Z3 pre-flight checklist + discipline                              │
│ - P3 verification + POSTFLIGHT                                      │
└──────────┬───────────────────────────────────────────────────────────┘
           │
     [Per-file execution]
           ├─ HALT? Unknown discovered → Trigger 6 (return to Z2)
           ├─ HALT? P3 verification fails → Trigger 4 (resolve or Z2)
           ├─ HALT? Cross-practice impact → Trigger 5 (restart Z1)
           └─ SUCCESS → Commit + verify + POSTFLIGHT close
                  
           │
           ▼
┌──────────────────────────────────────────────────────────────────────┐
│ Grounded Calibration (POSTFLIGHT measurement)                       │
│ - Vectors: predicted vs actual                                      │
│ - Divergence > 0.3? → Trigger 5 (decision-log, procedure update)   │
│ - All verified → Transaction closed                                 │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Communication Protocol

Every escalation must include:

### Required Fields (All Escalations)

1. **What triggered the escalation?** (cite the trigger #)
2. **What is the current state?** (findings, decision, error message)
3. **Who is the target?** (who decides next?)
4. **What is being requested?** (approval, clarification, reversal?)
5. **Deadline:** (when is a decision needed?)

### Communication Channels (By Zone)

| Zone | Channel | Format | Audience |
|------|---------|--------|----------|
| Z1 ↔ Z2 | Slack #wgs-sync or collab mesh | Threaded message + finding-log refs | Zone 1 team + Admiral |
| Z2 → Z1 | Reply to original proposal thread | Decision-log formatted (written) | Original proposer + team |
| Z2 ↔ Z3 | Empirica findings / decision-log + Slack | Brief message (decision) + detailed log | Zone 3 executor + Admiral |
| Z3 ↔ Z2 | Empirica dead-end-log + Slack | Urgent (P3 verification failure) | Zone 3 executor + Admiral |

### Template Messages

**Zone 1 → Zone 2 (Escalation):**
```
Escalating [issue] to Zone 2 per Trigger [#].

[Current State]
- Objection: [specific concern]
- Finding ID: [link to finding-log]
- Team consensus: [yes/no]

[Request]
Admiral decision needed on [specific question].

[Deadline]
Needed by [date] to maintain project timeline.
```

**Zone 2 → Zone 1 (Veto):**
```
Your proposal is BLOCKED per Zone 2 decision.

[Rationale]
Decision-log ID: [link]
Core issue: [specific reason]

[Path Forward]
Revise your proposal by [date] addressing:
- [specific requirement 1]
- [specific requirement 2]

Resubmit for re-review.
```

**Zone 3 ↔ Zone 2 (P3 Failure):**
```
🚨 URGENT: P3 Verification Failure

[What failed]
File: [path]
Commit: [SHA]
Verification: [curl result / CI/CD error]

[Root cause]
[diagnosis]

[Action taken]
- [attempted fix]

[Status]
[ ] Resolved (ready to retry)
[ ] Unresolved (awaiting Admiral guidance)

[Decision needed]
Halt other files? Revert? Proceed with workaround?
```

---

## Approval Workflow Per Zone

### Zone 1 Approval (Auto-Approval + Objection Period)

```
Day 0: Proposal posted
  ↓
Day 1–N: Objection period (24h–72h depending on issue type)
  - Participants comment / object / clarify
  ↓
END of objection period:
  - If objections remain → Escalate to Zone 2
  - If zero objections → AUTO-APPROVED → proceed to Zone 2
  ↓
Zone 2: Formal authority review + approval
```

**Authority decision-maker:** Practice owner or Admiral (depending on issue type).

### Zone 2 Approval (Explicit Authority Gate)

```
Proposal + Findings received (from Zone 1)
  ↓
Authority decision-maker reviews:
  - Completeness of findings
  - empirica CHECK gate status (if applicable)
  - Cross-practice impact assessment
  ↓
Decision: APPROVE / CONDITIONAL / BLOCKED
  ↓
If APPROVE:
  - Write decision-log (rationale + timestamp)
  - Communicate to Zone 1: "Approved. Proceed to Zone 3."
  - Copy decision-log link to commit message (Zone 3 trace)
  ↓
If CONDITIONAL:
  - Write decision-log (conditions + revision deadline)
  - Communicate: "Conditional approval. Revise by [date]."
  - Return to Zone 1 for revision
  ↓
If BLOCKED:
  - Write decision-log (rationale)
  - Communicate: "Blocked per [reason]. Revise or abandon."
  - Return to Zone 1 (if revision possible)
```

**Authority decision-maker:** Admiral (or delegated per AUTHORITY_MATRIX.yaml).

### Zone 3 Approval (Pre-flight Checklist + Execution Discipline)

```
Zone 2 authority document + approval received
  ↓
Run pre-flight checklist (Z3_PROTOCOL.md Sections B-1 through B-10)
  - Authority doc loaded ✓
  - Files affected confirmed ✓
  - Git branch clean ✓
  - (etc. — all 10 items)
  ↓
If all checks PASS:
  - Proceed to execution
  - One file at a time (C-1)
  - Diff before staging (C-2)
  - Commit per Z3 standard (C-3)
  ↓
For each file:
  - Edit → save → diff → stage → commit → push
  - P3 verification (curl raw, grep result)
  - Log verification ledger
  - Move to next file
  ↓
When all files done:
  - Run POSTFLIGHT (empirica postflight-submit)
  - Close goals (goals-complete-task with commit evidence)
  - Transaction closed
  ↓
If any check FAILS:
  - HALT. Do not proceed.
  - Log findings (root cause)
  - Escalate to Admiral (fix issue or revise proposal)
```

**Authority decision-maker:** Zone 3 executor (with pre-flight checklist approval).

---

## Decision Gates

### Gate 1: Zone 1 → Zone 2 (Auto-Approval Gate)

**Condition:** Objection period elapsed with zero objections.

**Who decides:** Automatic (no explicit decision-maker).

**Evidence:** Thread timestamp + final comment timestamp >= 24h–72h apart + no objection logged.

**Action:** Escalate to Zone 2 authority review (implicit).

---

### Gate 2: Zone 2 → Zone 3 (Admiral Approval Gate)

**Condition:** Admiral reviews Zone 2 authority document + findings and approves.

**Who decides:** Admiral.

**Evidence:** Decision-log written + linked in approval message + commit message references decision-log.

**Action:** Grant authority to Zone 3 execution. Pre-flight checklist may begin.

---

### Gate 3: Zone 3 Pre-flight (Readiness Gate)

**Condition:** All 10 items in Z3_PROTOCOL.md Sections B-1 through B-10 checked off.

**Who decides:** Zone 3 executor.

**Evidence:** Pre-flight checklist signed off (can be a comment in a Slack thread or a code comment).

**Action:** Proceed to file-by-file execution.

---

### Gate 4: Zone 3 Per-File (Verification Gate)

**Condition:** P3 verification confirms the change landed (curl raw URL, grep passes).

**Who decides:** P3 verification ledger (automated check).

**Evidence:** curl output + grep result + timestamp.

**Action:** Log verification + proceed to next file (or POSTFLIGHT if last file).

---

### Gate 5: POSTFLIGHT (Grounded Calibration Gate)

**Condition:** empirica postflight-submit completes with vectors measured.

**Who decides:** Sentinel (empirica infrastructure).

**Evidence:** Calibration report + divergence score (predicted vs actual).

**Action:** Close transaction. If divergence > 0.3, flag for Admiral review (mistake-log or decision-log).

---

## Special Cases

### Special Case 1: Emergency / Security Escalation

**Trigger:** A security incident or production outage requires immediate Zone 3 action without full Zone 1–2 deliberation.

**Protocol:**
1. Admiral is directly notified (phone / urgent Slack).
2. Verbal approval to proceed (no written authority doc needed initially).
3. Zone 3 execution begins immediately (pre-flight checklist still required).
4. Authority doc written retroactively (within 24h after fix lands).
5. POSTFLIGHT closes transaction.

**Timeline:** Minutes (vs. typical 24–72h).

**Example:** "Critical: database connection string leaked in GitHub. Admiral approves immediate secret rotation. Execute Zone 3 now. Docs follow."

---

### Special Case 2: Cross-Org Escalation (Mesh-Support Coordination)

**Trigger:** Change affects both empirica-foundation and empirica (company org).

**Protocol:**
1. empirica-foundation team files proposal (Zone 1, local).
2. Zone 2 (Admiral) reviews + flags cross-org impact.
3. Escalate to mesh-support via collab (mesh-send to empirica.david.empirica-mesh-support).
4. Mesh-support coordinates company-side decision (ECO/autonomy gated).
5. Once company approves, empirica-foundation proceeds to Zone 3.

**Timeline:** 48–72h (slower due to cross-org).

**Ownership:** empirica-foundation Admiral (leads collab) + mesh-support (executes company side).

---

### Special Case 3: Proposal Abandoned (Withdrawal)

**Trigger:** Originator or Admiral decides the proposal is no longer worth pursuing.

**Protocol:**
1. Log decision-log: "Abandoned: [reason]"
2. Post in original thread: "Proposal withdrawn per [decision-log ID]."
3. No escalation needed; transaction closed.

**Timeline:** Same-day.

---

## Enforcement & Audit

### Enforcement (Who ensures triggers are followed?)

| Responsibility | Who | How |
|---|---|---|
| **Zone 1 monitoring** | Practice owner + Admiral | Read Slack threads, look for objections. Auto-escalate if found. |
| **Zone 2 gating** | Admiral | Review all Zone 2 authority docs before proceeding. If incomplete findings, escalate back to Zone 1. |
| **Zone 3 pre-flight** | Zone 3 executor | Self-enforcing (checklist must be signed off). |
| **P3 verification** | Zone 3 executor + Admiral (spot-check) | Verification ledger is the record. Admiral audits periodically. |
| **POSTFLIGHT calibration** | Sentinel + Admiral | Sentinel scores divergence. Admiral reviews if > 0.3. |

### Audit (Quarterly Review)

**Every quarter, Admiral reviews:**

1. **Escalation log:** How many escalations per trigger type?
2. **Reversal rate:** How many Zone 1 → Zone 2 → Zone 1 cycles (indicates unclear proposals)?
3. **P3 failure rate:** How many P3 verification failures? (Indicates CI/CD issues or discipline gaps).
4. **Calibration divergence:** POSTFLIGHT vectors — any systematic bias?
5. **Procedure updates:** Do escalation rules need refinement?

**Output:** Quarterly decision-log summarizing findings + procedure updates (if any).

---

## Summary Table (Quick Reference)

| Trigger | Condition | Escalates To | Latency | Example |
|---------|-----------|---|---|---|
| **1** | Objection in Z1 | Z2 (return if unresolved) | same day | Peer raises concern about backward compat |
| **2** | Veto in Z2 | Z1 (revise) | same-day reply | Admiral blocks due to missing migration plan |
| **3** | CHECK fail | NOETIC (more investigation) | immediate | Vectors know=0.6, need 0.75 |
| **4** | P3 fail | Z2 (Admiral) or Z1 (restart) | immediate | curl doesn't show change; CI error |
| **5** | Cross-practice impact | Z1 (restart multi-practice collab) | same day | Change affects mesh-support; need coordination |
| **6** | Unknown in Z3 | Z2 (clarification) | immediate | Discovered file needs edit; not in authority doc |

---

**Status:** DRAFT — awaiting Admiral ratification  
**Next Steps:** Task 4 (Align CLAUDE.md across 9 practices) + Task 5 (Governance ratification)

