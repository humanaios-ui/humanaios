# HumanAIOS Repair Sequence — Work Order Dispatch

**Date:** 2026-09-11  
**Status:** Ready for autonomous execution  
**Coordinator:** empirica-foundation-evaluator (Claude)  
**Mesh Status:** SER in preparation; some practices mesh-registered, others via local work orders

---

## Delivery Method by Practice

Due to varying maturity of cortex registration across practices, we use a **hybrid coordination model**:

### Mesh-Registered Practices (Cortex `cortex_propose`)
These practices receive formal SER + proposals via cortex:
- ✅ **empirica-foundation-evaluator** (this practice, self-coordinating)
- ✅ **empirica-mesh-support** (observer/escalation channel)
- ⏳ **empirica-autonomy** (if needed for orchestration)

### Local Work Order Practices (Documentation-Based)
These practices execute work based on detailed briefs in their repos (no cortex dispatch yet):
- 📄 **empirica-outreach** → `/REPAIR_BRIEF_WAVE_0.md` in their repo
- 📄 **empirica-analytics** → `/REPAIR_BRIEF_WAVE_0-2.md` in their repo
- 📄 **Other practices** → Tasks documented locally where applicable

---

## What Was Dispatched

### To empirica-outreach
✅ **Brief Location:** `/Users/andersonfamily/practices/empirica-outreach/REPAIR_BRIEF_WAVE_0.md`

**Work Assignment (Wave 0):**
- Fix 03: Remove arXiv identifier from 30 locations
- Fix 04: Retire marketing README claims

**Status:** Ready for immediate execution  
**Action:** Read brief, create local goals, execute fixes 03 & 04, ack completion

---

### To empirica-analytics  
✅ **Brief Location:** `/Users/andersonfamily/practices/empirica-analytics/REPAIR_BRIEF_WAVE_0-2.md`

**Work Assignment (Waves 0-2):**
- Wave 0: Fix 05 (corpus repair), Fix 06 (dimension reconciliation)
- Wave 2: Fix 14 (dataset refresh), Fix 15 (H-INSPECT), Fix 16 (gap analysis), Fix 24 (sources)

**Status:** Ready for execution (fix 15 blocked on API keys)  
**Action:** Read brief, create local goals per wave, execute per sequence

---

### Local (empirica-foundation-evaluator)
✅ **Brief Location:** `./REPAIR_BRIEF_LOCAL_WAVE_0-2.md` (your repo)

**Work Assignment (Waves 0-2 + Coordination):**
- Wave 0: Fix 08, 13 (local housekeeping)
- Wave 1: Fix 07, 10 (identity, ritual hooks)
- Wave 2: Fix 11 (graph closure, 3 sessions spread)
- Plus: Prepare David proposals (fixes 09, 12, 26)

**Status:** Ready for immediate execution  
**Action:** Execute local work + coordinate upstream proposals

---

## Wave Execution Timeline

```
IMMEDIATE (TODAY)
├─ Wave 0 (Mechanical, All Parallel)
│  ├─ empirica-outreach: fixes 03, 04 [1.5 sessions]
│  ├─ empirica-analytics: fixes 05, 06 [1 session]
│  └─ empirica-evaluator: fixes 08, 13 [1 session]
│  └─ TOTAL: ~3.5 sessions, no blockers ✓ EXECUTE NOW

AFTER WAVE 0 VERIFIES (~1 day)
├─ Wave 1 (Measurement Setup)
│  ├─ empirica-evaluator: fixes 07, 10 [2 sessions]
│  └─ Prepare David proposals (09, 12) [coordination]
│  └─ TOTAL: 2 sessions ✓ EXECUTE AFTER WAVE 0

AFTER WAVE 1 (~2 days)
├─ Wave 2 (Science & Calibration)
│  ├─ empirica-analytics: fixes 14, 16, 24 [~3.5 sessions]
│  ├─ empirica-analytics: fix 15 [2 sessions] ⚠️ BLOCKED on API keys
│  ├─ empirica-evaluator: fix 11 [3 sessions spread]
│  └─ TOTAL: ~8.5 sessions + 1 decision gate
```

---

## How Each Practice Executes

### Step 1: Read the Work Brief
Each practice reads their assigned brief:
- **Location:** `/REPAIR_BRIEF_*.md` in that practice's repo
- **Contents:** Per-fix What/How/Verify steps, effort, blockers, dependencies

### Step 2: Create Local Goals
```bash
# In your practice directory:
empirica goals-create \
  --objective "HumanAIOS Repair Sequence — Wave X" \
  --description "[brief summary]"

# Then add tasks per fix:
empirica goals-add-task --goal-id <id> \
  --description "Fix NN: [title]"
```

### Step 3: Execute Per Wave
- **Wave 0:** Execute immediately (all parallel, no blockers)
- **Wave 1:** After Wave 0 verifies complete
- **Wave 2:** After Wave 1 completes

### Step 4: Ack Completion
When fixes land and are verified:
```bash
# If/when mesh is wired up:
empirica mailbox reply --parent-id <SER-id> \
  --summary "Fixes XX, YY complete: [commit SHAs]" \
  --commit-sha <sha>

# For now: Log findings locally
empirica finding-log \
  --finding "Fixes XX, YY complete" \
  --source "repair-sequence" \
  --impact 0.8
```

### Step 5: Escalate Blockers
**DON'T GRIND ALONE.** If stuck:
```bash
empirica collab --target empirica-mesh-support \
  --title "Blocker: Fix XX — [symptom]" \
  --summary "[what you tried, where broke, what you need]"
```

---

## Decision Gates (Waiting on Carly)

### Gate 1: Fix 15 API Keys (Blocks Wave 2)
**Need:** ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY  
**When:** Before empirica-analytics starts fix 15 (H-INSPECT replication)  
**Impact:** 2 sessions of research work

### Gate 2: Fix 02 Route Decision
**Need:** Tokenless `/intake/public/*` routes OR remove POST from site?  
**When:** Before Wave 3 implementation  
**Impact:** How public submissions are handled

### Gate 3: Fix 20 STATUS.md Wording
**Need:** Final public status language (I draft, Carly signs)  
**When:** Before fixes 03, 04 final messaging  
**Impact:** Single source of truth for public claims

### Gates 4-6: Wave 3 Restructure Decisions
**When:** After Wave 2 completes  
**What:** Seat collapse, mechanisms audit, external referent, etc.

---

## SER Coordination (When Mesh is Fully Wired)

Once cortex mesh is fully operational for all practices:

**Proposed SER:**
- Title: HumanAIOS Repair Sequence — Wave 0-2 Orchestration
- Participants: empirica-foundation-evaluator (required), empirica-analytics/outreach (participating), empirica-mesh-support (observer)
- Escalation: 4h re-ping
- Closure: When all 24 fixes verify complete

**For now:** Work orders via briefs + local goals achieve the same coordination.

---

## Verification Checklist

### Wave 0 Complete When:
- [ ] empirica-outreach: Fix 03 (arXiv grep returns 0 lines)
- [ ] empirica-outreach: Fix 04 (false claims removed/linked)
- [ ] empirica-analytics: Fix 05 (corpus validates)
- [ ] empirica-analytics: Fix 06 (dimensions reconciled)
- [ ] empirica-evaluator: Fix 08 (stale txn closed)
- [ ] empirica-evaluator: Fix 13 (housekeeping done)

### Wave 1 Complete When:
- [ ] empirica-evaluator: Fix 07 (seat identity correct)
- [ ] empirica-evaluator: Fix 10 (ritual hooks active)
- [ ] David evidence prepared (09, 12)

### Wave 2 Complete When:
- [ ] empirica-analytics: Fix 14 (HF dataset updated)
- [ ] empirica-analytics: Fix 16 (gap analysis published)
- [ ] empirica-analytics: Fix 24 (sources registered)
- [ ] empirica-analytics: Fix 15 (H-INSPECT complete) ⚠️ if keys provided
- [ ] empirica-evaluator: Fix 11 (closure sprint: 300 → 225 unknowns, decisions with outcomes)

---

## Next Steps

1. ✅ **Briefs written and distributed** (in each practice's repo)
2. ✅ **Coordination plan documented** (this file)
3. ⏳ **Ready for practices to execute Wave 0**
4. ⏳ **Waiting on:** Carly approval (API keys, gate decisions)

**What each practice should do now:**
- Read your brief (`/REPAIR_BRIEF_*.md`)
- Create empirica goals for Wave 0
- Execute fixes (parallel, no blockers)
- Ack completions

**What coordinator (evaluator) should do:**
- Monitor Wave 0 progress
- Prepare David proposals once Wave 0 verifies
- Track decisions/gates

---

**Execution Ready.** Awaiting practices to begin Wave 0. 🚀
