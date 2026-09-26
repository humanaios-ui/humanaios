# HumanAIOS Repair Sequence — Mesh Orchestration Master Plan

**Date:** 2026-09-11  
**Coordinator:** Claude (empirica-foundation-evaluator seat)  
**Status:** Ready to dispatch to practices  
**Next Action:** Issue SER proposal to practices via mesh

---

## What We're Doing

Automating 24 remaining fixes across the foundation practices. Instead of one AI doing all the work, we're **delegating by domain** to the practices that own those domains.

- **empirica-analytics:** 6 fixes (data pipeline, research)
- **empirica-outreach:** 3 fixes (API, documentation)
- **empirica-foundation-evaluator:** 5 local fixes + coordination role
- **David (upstream):** 3 fixes (listener, readiness gate, defects report) — prepared but not executed

---

## Practice Briefs (Detailed Work Assignments)

Each practice has received a **detailed work brief** with everything they need to execute autonomously:

### empirica-analytics
📄 **File:** `/Users/andersonfamily/practices/empirica-analytics/REPAIR_BRIEF_WAVE_0-2.md`

**Fixes assigned:**
- Fix 05: Repair frozen corpus file (0.5 session)
- Fix 06: Reconcile dimension list (0.5 session)
- Fix 14: Refresh HuggingFace dataset (1 session)
- Fix 15: Run H-INSPECT replication (2 sessions + **blocked on Carly API keys**)
- Fix 16: Fractal-gap analysis (2 sessions)
- Fix 24: Register canonical sources (15 min)

**Total:** ~6 sessions + 1 decision gate

**Key blockers:**
- Fix 01 (API up) — already done ✅
- Fix 05 (corpus valid) — they do
- Carly API keys for fix 15 — **decision gate**

### empirica-outreach
📄 **File:** `/Users/andersonfamily/practices/empirica-outreach/REPAIR_BRIEF_WAVE_0.md`

**Fixes assigned:**
- Fix 01: Bring API back [**ALREADY COMPLETE**] ✅
- Fix 03: Remove arXiv from 30 locations (1 session)
- Fix 04: Retire false README claims (0.5 session)

**Total:** ~1.5 sessions, all mechanical

**Dependencies:** None. Execute immediately in parallel.

### empirica-foundation-evaluator (Local)
📄 **File:** `/Users/andersonfamily/practices/empirica-foundation-evaluator/REPAIR_BRIEF_LOCAL_WAVE_0-2.md`

**Fixes assigned:**
- Fix 08: Close stale transaction (10 min)
- Fix 13: Housekeeping (1 session)
- Fix 07: Fix seat identity (1 session)
- Fix 10: Session ritual hooks (1 session)
- Fix 11: Graph closure sprint (3 sessions spread)

**Total:** ~6 sessions local + coordination overhead

**Plus coordination role:**
- Prepare evidence for David fixes (09, 12)
- Send final upstream defects report (26)

---

## Execution Sequence (No Decisions Required)

```
┌─────────────────────────────────────────────────────┐
│ Wave 0: Mechanical (Execute Immediately)            │
├─────────────────────────────────────────────────────┤
│                                                     │
│ empirica-outreach (parallel):                       │
│   - Fix 03: Remove arXiv (1 session)                │
│   - Fix 04: Retire README claims (0.5 session)     │
│                                                     │
│ empirica-analytics (parallel):                      │
│   - Fix 05: Repair corpus file (0.5 session)       │
│   - Fix 06: Reconcile dimensions (0.5 session)     │
│                                                     │
│ empirica-evaluator (local):                         │
│   - Fix 08: Close stale txn (10 min)               │
│   - Fix 13: Housekeeping (1 session)               │
│                                                     │
│ ✓ Total: ~4 sessions, all parallel, no blockers    │
│                                                     │
└─────────────────────────────────────────────────────┘
         ↓ After Wave 0 verifies complete
┌─────────────────────────────────────────────────────┐
│ Wave 1: Measurement Setup                           │
├─────────────────────────────────────────────────────┤
│                                                     │
│ empirica-evaluator (local):                         │
│   - Fix 07: Fix seat identity (1 session)          │
│   - Fix 10: Session ritual hooks (1 session)       │
│                                                     │
│ Plus: Prepare David proposals (fix 09, 12)         │
│   - Gather listener logs, document issue           │
│   - Send evidence via mesh-support                 │
│                                                     │
│ ✓ Total: 2 sessions + coordination overhead        │
│                                                     │
└─────────────────────────────────────────────────────┘
         ↓ After Wave 1 completes
┌─────────────────────────────────────────────────────┐
│ Wave 2: Science & Calibration                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│ empirica-analytics (parallel):                      │
│   - Fix 14: Refresh dataset (1 session)            │
│   - Fix 16: Fractal-gap analysis (2 sessions)      │
│   - Fix 24: Register sources (15 min)              │
│                                                     │
│ empirica-analytics (BLOCKED on gate):               │
│   - Fix 15: H-INSPECT replication (2 sessions)     │
│     → Waiting for: Carly API keys                  │
│                                                     │
│ empirica-evaluator (local):                         │
│   - Fix 11: Graph closure sprint (3 sessions)      │
│                                                     │
│ ✓ Total: ~8 sessions (analytics) + 3 sessions (eval)  │
│ ⚠ Blocker: Carly API keys for fix 15               │
│                                                     │
└─────────────────────────────────────────────────────┘
         ↓ When Wave 2 completes
┌─────────────────────────────────────────────────────┐
│ Wave 3: Decisions (Stays with Admiral/Carly)       │
├─────────────────────────────────────────────────────┤
│                                                     │
│ Gates for Carly approval:                           │
│   - Fix 02: Public intake route decision           │
│   - Fix 09, 12, 26: Send David upstream proposals  │
│   - Fix 17-23, 25: Restructure decisions           │
│                                                     │
│ Not delegated (stays with Admiral)                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## How the Mesh Orchestration Works

### 1. SER (Shared Epistemic Record) — Persistent Coordination

A **SER** is created to hold the repair sequence as persistent shared state across multiple sessions and practices.

**SER Details:**
- **Title:** HumanAIOS Repair Sequence — Wave 0-2 Orchestration
- **Participants:**
  - empirica-foundation-evaluator: `required` (orchestrator, escalation re-pings)
  - empirica-analytics: `participating` (executors)
  - empirica-outreach: `participating` (executors)
  - empirica-mesh-support: `observer` (upstream coordination, David routing)
- **Escalation:** 4h re-ping for required tier (evaluator)
- **State lifecycle:** `open → in_progress → closed`

### 2. Proposals — Work Assignments

Each practice receives a **`cortex_propose`** message (type=`architecture_decision`, action_category=`STRATEGIC`, parent=SER proposal).

The proposal:
- Links to the detailed work brief (in their repo)
- Assigns specific fixes with effort estimates
- Specifies execution sequence (Wave 0 parallel, then 1, 2 sequential)
- Establishes blocker dependencies
- Requests completion acks via `empirica mailbox reply`

### 3. Completion Acks — Closing Loops

When a practice completes a fix (or batch of fixes):

```bash
empirica mailbox reply --parent-id <SER-proposal-id> \
  --summary "Fixes XX, YY complete: [what was fixed, commit SHAs]" \
  --commit-sha <sha>
```

This:
- Posts a `collab_brief` reply to evaluator (auto-accepts)
- Marks the parent proposal as `completed` on their side
- Carries the commit SHA so evaluator can verify
- Advances the SER `coordination_state` (optional, if evaluator transitions it)

### 4. Escalation & Blockers

If a practice gets stuck:

```bash
empirica collab --target empirica-mesh-support \
  --title "Blocker: Fix XX — [symptom]" \
  --summary "[what you tried, where it broke, what you need]"
```

**Don't grind alone.** Mesh-support will unblock or route the specialist.

---

## What Happens Next (Timeline)

### Immediate (Today)
1. ✅ Create SER via `cortex_propose` to practices
2. ✅ Practices receive SER + briefs, create local goals
3. ✅ Execute Wave 0 (4 sessions, all parallel)
   - outreach: fixes 03, 04
   - analytics: fixes 05, 06
   - evaluator: fixes 08, 13

### After Wave 0 Verifies (~1 day)
4. ✅ Execute Wave 1 (2 sessions + coordination)
   - evaluator: fixes 07, 10
   - Prepare David proposals (evidence collection)

### After Wave 1 Completes (~2 days)
5. ✅ Execute Wave 2 (8-11 sessions, parallel + some sequential)
   - analytics: fixes 14, 16, 24 (parallel)
   - analytics: fix 15 (blocked on Carly API keys — **decision gate**)
   - evaluator: fix 11 (graph closure sprint, can spread over multiple sessions)

### When Wave 2 Completes (~7-10 days total)
6. ⏳ Wave 3 (decisions only, Carly approval)
   - Fixes 02, 09, 12, 17-23, 25, 26
   - Not delegated; Carly decides

---

## Decision Gates (What Needs Carly Approval)

### Gate 1: Fix 15 API Keys (Blocks Wave 2)
**What:** Carly provides ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY  
**Why:** H-INSPECT replication study needs all three providers  
**Impact:** 2 sessions, data for deciding fix 19 (external referent)  
**Timeline:** Anytime before end of Wave 2

### Gate 2: Fix 02 Route Decision (Affects final implementation)
**What:** Tokenless `/intake/public/*` routes (Option A) vs. remove POST from site (Option B)  
**Recommendation:** Option A (grows corpus, both honest)  
**Impact:** How to handle public submissions  
**Timeline:** Can be decided anytime; affects Wave 3 scope

### Gate 3: Fix 20 STATUS.md Wording (Coordinator)
**What:** Final public status language  
**Note:** I draft, Carly signs  
**Impact:** Single source of truth for all public claims  
**Timeline:** Needed for fixes 03, 04 final messaging

### Gates 4-6: Wave 3 Decisions (Restructure)
**What:** Fix 17 (seat collapse), 18 (mechanism audit), 19 (external referent), 21-23, 25  
**Recommendation:** See REPAIR_SEQUENCE_PLAN.md for each  
**Impact:** Authority structure, oversight, model spend  
**Timeline:** After Wave 2 completes

---

## What Each Practice Should Know

### empirica-analytics
- ✅ You have a detailed brief in your repo
- ✅ Your 6 fixes are all science/data domain — you own them
- ⚠️ Fix 15 will be **blocked** until Carly provides API keys
- 🔗 Depends on fixes 01, 05 from other practices (both ready/done)
- 📝 Ack each batch of fixes via `empirica mailbox reply` to close the loop

### empirica-outreach
- ✅ You have a detailed brief in your repo
- ✅ Fix 01 is already done — you can mark as verified
- ✅ Fixes 03, 04 are **mechanical, parallel, no blockers**
- 📝 Execute both in one session, ack on completion

### empirica-evaluator (You)
- ✅ You have a local brief in your repo
- ✅ 5 fixes are local work (calibration, housekeeping)
- ✅ You also have a **coordination role** (don't ignore!)
- 📝 Prepare evidence for David fixes (09, 12, 26)
- 🔗 Fix 11 can spread across multiple future sessions (no rush)

### David (Upstream)
- 🔗 Fixes 09, 12, 26 are yours (listener, gate, defects report)
- 📝 You'll receive proposals via mesh-support with evidence
- ⏳ After you respond, we can decide next steps

---

## Verification & Rollback

Every fix in Waves 0-2 is:
- ✅ **Reversible:** All code changes can be `git revert`'d
- ✅ **Verifiable:** Each brief specifies a verify command
- ✅ **Monitored:** SER tracks completion via acks
- ✅ **Logged:** Each fix creates findings/decisions in empirica

If a fix lands wrong: `git revert` + post a blocker via mesh. Don't grind.

---

## The Orchestration Advantage

Instead of **one AI executing 24 fixes sequentially**, we have:
- **3 practices working in parallel** (outreach + analytics + evaluator)
- **4 sessions of work happening simultaneously** (instead of 20 sequential)
- **Domain expertise where it belongs** (analytics does data work, outreach does API work)
- **Escalation paths for blockers** (mesh-support unblocks, not just silent grinding)
- **Persistent coordination** (SER tracks state across all practices)

**Expected timeline:** 7-10 days total (Waves 0-2) instead of 20+ days sequential.

---

## Next Step: You Approve

When you're ready:

1. **Confirm the delegation is good** (3 practices, 14 fixes, clear assignments)
2. **Say "go"** — I'll issue the SER proposal to practices
3. **Practices receive briefs** and start creating local goals
4. **Execution begins immediately** (Wave 0 is ready to go)

Everything is prepared. Waiting for your signal. 🚀
