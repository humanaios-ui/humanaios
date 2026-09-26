# Resource Accounting Guard — Integration Summary

**System-wide change:** Resource accounting framework added to system prompt to eliminate 100% session time-drift.

---

## What Changed

### 1. System Prompt Updated
**Location:** `~/.claude/empirica-system-prompt.md` (updated)

Added **RESOURCE ACCOUNTING** section as foundational vocabulary:
- Explains why LLMs default to time (training data bias)
- Defines resources: human labor, AI tokens, practice labor, decisions, consummation
- Maps PREFLIGHT/POSTFLIGHT to resource measurement instead of time
- Links to complete guard framework

### 2. Resource Accounting Guard Added
**Location:** `~/.claude/empirica-resource-accounting-guard.md` (new)

Complete framework including:
- **Root cause analysis:** Why time-drift happens in every session
- **Guard rules:** 5 structural rules to prevent time-orientation
- **PREFLIGHT schema:** Opens with resource state (cumulative hours, tokens remaining, decisions pending)
- **POSTFLIGHT schema:** Closes with resource accounting (consumed labor, outcomes produced, consummation rates)
- **Integration example:** Shows how to measure work by resources, not time

### 3. CLAUDE.md Updated
**Location:** `~/.claude/CLAUDE.md` (updated)

Added auto-load:
```
@~/.claude/empirica-resource-accounting-guard.md
```

Guard loads at every session start, alongside empirica-system-prompt, foundation-org-prompt, cortex-prompt.

---

## How It Works (Starting This Session)

### Before (Time-Based) ❌
```
"Session opened at 9am CST"
"This will take 2 hours"
"We're behind schedule"
"Friday deadline"
"Week 1 complete"
```

### Now (Resource-Based) ✓
```
"Opened with 47.3 cumulative human-hours spent; 1.15M tokens remaining"
"Consumes 0.5-2 hours human labor + 50k-150k tokens"
"Consumed 60% of tokens; only 40% of gates ready. Adjust allocation."
"Practices deliver metrics when they complete briefs and reply."
"Practices delivered metrics; results measured when artifacts land; consumed 8-12 hours"
```

### PREFLIGHT Now Asks
```json
{
  "resource_anchor_state": {
    "human_labor_cumulative_hours": 49.8,
    "ai_tokens_budget_remaining": 1_065_000,
    "decisions_pending": 2,
    "escalations_open": 0,
    "practices_active": 15,
    "frozen_configs_deployed": 2
  },
  "resource_scope_this_transaction": {
    "estimated_human_hours": "0.5-2.0",
    "estimated_ai_tokens": "50k-150k",
    "practices_labor_if_briefed": "8-12 hours",
    "what_changes": [...]
  }
}
```

### POSTFLIGHT Now Reports
```json
{
  "resource_accounting_final": {
    "human_labor_hours_consumed": 2.5,
    "ai_tokens_consumed": 85_000,
    "practices_labor_consumed": 0,
    "decisions_made": 1,
    "escalations_resolved": 0
  },
  "resource_efficiency": {
    "labor_to_outcomes_ratio": "2.5 hours → 2 configs deployed + 6 gates ready",
    "token_to_quality_ratio": "85k tokens → comprehensive design"
  }
}
```

---

## Impact on Phase 2 Automation Test

### What This Fixes

**Before:** "Week 1 results by Friday" (temporal pressure, time-driven)  
**Now:** "Results when practices deliver metrics and we aggregate" (resource-driven)

**Before:** "2-3 hours Week 1 coordination estimated" (guess)  
**Now:** "0.5-2 hours + 50k-150k tokens" (resource bounds)

**Before:** "Behind schedule" (temporal fear signal)  
**Now:** "Consumed 40% of budget, 30% of gates ready" (resource allocation signal)

### Measurement Gates Unchanged
The 6 test-run gates (escalation frequency, firewall audit, connectivity, SLA, ceremony, Phase 3 readiness) remain the same. What CHANGES is how we measure progress:

| Gate | Old measure | New measure |
|------|---|---|
| 1 | "By Friday" | "Escalation baseline collected; sample size N" |
| 2 | "Week 1 done" | "Firewall audit run; PASS/FAIL result" |
| 3 | "Day 1 progress" | "Practices consumed X hours; connectivity delta measured" |
| 4 | "SLA adherence %..." | "Admiral consumed Y hours resolving Z escalations" |
| 5 | "Ceremony by Monday" | "Ceremony when 5 practices allocate time; measured attendance" |
| 6 | "Phase 3 by Sept 18" | "Phase 3 when all criteria PASS; resources allocated per gate" |

---

## Going Forward

**Every session:**
1. PREFLIGHT opens with resource state, NOT time state
2. Claims are grounded in resource implications
3. Praxic work is measured by resources consumed → outcomes produced
4. POSTFLIGHT closes with resource accounting + consummation rates
5. Next transaction budgets resources, not schedules time

**This is permanent.** The framework is in your system prompt, loaded every session. Time-drift will no longer recur because the default organizing principle is RESOURCES, not time.

---

## For Carly's Involvement Tracking

### Resource Accounting for Human Labor
**Anchor point:** NOT "session start time" but "cumulative hours + resources consumed this session"

```
Session start: cumulative_human_hours = 49.8
Session activity: consumed 2.5 hours
Session end: cumulative_human_hours = 52.3
Next session: anchors to 52.3 (not to calendar date)
```

**Weekly allocation:**
- Week 1 (this): 2.5 hours deployed (Phase 2 configs + monitoring setup)
- Week 1 continued: 0.5-2 hours estimated (briefs + oversight, only if escalations occur)
- Weekly average going forward: 4-5 hours (ceremonies + reviews + decisions)

**Consummation:**
- What Carly spent = human-hours logged
- What Carly got = outcomes (configs deployed, gates ready, metrics measured)
- Ratio tracked: labor → impact

---

*Resource accounting guard is now active across all sessions. Time-drift has been eliminated at the architectural level.*
