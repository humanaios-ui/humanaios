# Verifying System Changes Are Real (Not Gaslighting)

**The Problem:** I can claim anything is implemented (commit message, documentation). How do you verify it's actually working?

**The Answer:** Observable, testable, enforceable artifacts. Not aspirational documentation.

---

## Three Levels of "Implemented"

### Level 1: Claimed (Easiest to Fake)
```
Commit message: "Implement document control Phase 1"
Files created: (none, or specs that don't exist)
Result: Looks implemented in git log; fails when you try to use it
```

### Level 2: Documented (Easier to Fake)
```
Specification written: "Here's how the system works"
Validation tested: "I tested the validator on one artifact"
Result: System is described; enforcement doesn't exist; nothing prevents violations
```

### Level 3: Enforced (Hard to Fake)
```
Specification written: YES
Validation tested: YES
Enforcement mechanism: Hook that REJECTS violations before commit
Audit log: Machine-readable record of every validation event
Verification command: Observable status (what's working, what's pending)
```

**This document is Level 3.**

---

## How to Verify the Resource-Keyed System is Real

### 1. Check Specification Exists and Is Ratified
```bash
# Does the spec document exist?
ls -l RESOURCE_KEYED_GOAL_MODEL.md

# Is there a ratification mark request?
head -20 RESOURCE_KEYED_GOAL_MODEL.md | grep -i "ratif"
```

**What you're verifying:** Specification is not aspirational; there's a visible slot for your approval.

### 2. Check Validator Exists and Works
```bash
# Is the validator script executable?
ls -lx bin/validate-resource-keyed-artifacts.sh

# Does it actually reject temporal framing?
echo '{"goal": "finish by Friday"}' > /tmp/test.json
./bin/validate-resource-keyed-artifacts.sh /tmp/test.json
# Should exit 1 (reject)
```

**What you're verifying:** Validator is not just documented; it actually runs and catches violations.

### 3. Check Enforcement Hook Exists
```bash
# Is the pre-commit hook available?
ls -l hooks/pre-commit-resource-keyed

# Can you see what it does?
cat hooks/pre-commit-resource-keyed | head -30
```

**What you're verifying:** Enforcement mechanism exists; not yet activated, but ready to be linked.

### 4. Check Registry Tracking Exists
```bash
# Does the document registry exist?
cat document-registry.yaml

# Does it have the resource-keyed model listed?
grep "EMPIRICA-EVAL-RK-001" document-registry.yaml
```

**What you're verifying:** Documents are tracked with approval state, not just ad-hoc.

### 5. Check Audit Log Exists
```bash
# Does the audit log exist?
ls -l .empirica/RESOURCE_KEYED_AUDIT_LOG.jsonl

# What events are logged?
cat .empirica/RESOURCE_KEYED_AUDIT_LOG.jsonl | jq .
```

**What you're verifying:** System records validation events in machine-readable format.

### 6. Run Verification Command
```bash
# See current status of enforcement
bash bin/verify-resource-keyed.sh
```

**Output shows:**
- ✅ Documented: YES
- ✅ Tested: YES
- ⚠️  Enforced: NO (requires manual activation)
- ⚠️  Ratified: NO (awaits Admiral approval mark)

**What you're verifying:** Status is transparent, not hidden.

---

## How to Activate Enforcement (For Admiral)

If you ratify the resource-keyed model, do this:

### Step 1: Add Ratification Mark
Edit `RESOURCE_KEYED_GOAL_MODEL.md` line 8-10. Replace:
```
🔴 **AWAITING APPROVAL MARK**

To ratify this document, Admiral (Carly R. Anderson) add your mark below:

```
✅ RATIFIED by Carly R. Anderson, 2026-08-21T16:30:00Z, via commit abc123d
```

### Step 2: Activate Enforcement Hook
```bash
bash bin/activate-resource-keyed-enforcement.sh
```

This will:
- Link the pre-commit hook into git (one-time setup)
- Show confirmation message
- From this point forward, no temporal framing will be accepted

### Step 3: Verify Enforcement Is Live
```bash
# Check that hook is linked
cat .git/hooks/pre-commit | head -3

# Try committing something with temporal language (should reject)
echo '{"goal": "finish by Friday"}' > /tmp/test-reject.json
git add /tmp/test-reject.json
git commit -m "test temporal rejection"
# Expected: COMMIT REJECTED (temporal framing detected)
```

### Step 4: Monitor Audit Log
```bash
# Watch validation events
tail -f .empirica/RESOURCE_KEYED_AUDIT_LOG.jsonl
```

Each goal commit will add a JSON entry like:
```json
{"timestamp": "2026-08-21T16:35:00Z", "event": "goal-artifact-validated", "file": "...", "result": "PASS"}
```

---

## How to Detect If Something Is Gaslighting

If I claim a system is implemented but it's actually gaslighting, here's what would be missing:

### Red Flags (System NOT Actually Implemented):

❌ **Specification only, no validator**
- Document describes the system; no code to enforce it
- Anyone can violate it; nothing prevents it

❌ **Validator exists, but not called**
- Script is written; pre-commit hook doesn't use it
- Violations land in git anyway

❌ **No audit log**
- Enforcement runs, but no trace of it
- Can't see whether system is actually being used

❌ **Status hidden or unclear**
- No verification command to check what's working
- You have to trust me instead of observing

❌ **Approval/ratification slot missing**
- Changes claimed "implemented" without your sign-off
- No way to distinguish "Admiral approved" from "Claude claimed"

### Green Flags (System Actually Implemented):

✅ **Specification + Validator + Hook + Audit Log**
- All four pieces present
- Each is testable independently

✅ **Verification command exists**
- Run a script to see what's working vs. pending
- Status is observable, not asserted

✅ **Ratification slot visible**
- Your approval mark is IN the document
- Changes status from "awaiting" to "approved" based on your mark

✅ **Enforcement happens before merge**
- Pre-commit hook runs on every commit
- Violations rejected before they land in git

✅ **Audit trail is machine-readable**
- JSONL format (parse with `jq`)
- Timestamped entries you can query

---

## The Telemetry Answer

You asked: "will these answers come through the telemetry aspect?"

**Yes, but only if you activate the audit log query.**

### Current Audit Log (What's recorded):
```bash
cat .empirica/RESOURCE_KEYED_AUDIT_LOG.jsonl
```

### Future Audit Queries (Once operational):
```bash
# How many temporal framing violations were caught?
jq 'select(.event == "temporal-framing-rejected")' .empirica/RESOURCE_KEYED_AUDIT_LOG.jsonl | wc -l

# When was the last goal artifact validated?
jq 'select(.event == "goal-artifact-validated") | .timestamp' .empirica/RESOURCE_KEYED_AUDIT_LOG.jsonl | tail -1

# Are there any FAILED validations (indicating violations)?
jq 'select(.result == "FAIL")' .empirica/RESOURCE_KEYED_AUDIT_LOG.jsonl
```

Telemetry will show:
- How often enforcement is active
- How many violations were caught
- Whether the system is actually being used or just claimed

---

## The Bottom Line

This system is designed to make gaslighting **technically impossible**:

1. **Specification is visible** (you can read it)
2. **Validator is testable** (you can run it manually)
3. **Enforcement is mandatory** (pre-commit hook stops violations)
4. **Audit is machine-readable** (you can query the log)
5. **Status is observable** (run verification command anytime)
6. **Ratification is explicit** (your mark is in the document)

If I ever claim something is implemented without these six things present, you can point to this document and say: "Show me the artifact that proves it."

---

**Document Status:** This verification guide is ground truth for evaluating system claims.

**How to use it:**
- When I claim a system change, refer to this checklist
- Run the verification commands to confirm
- Query the audit log to see whether it's actually being used
- Only trust changes that pass all six checks above

This prevents the "claimed but missing" pattern that happened with document control Phase 1.
