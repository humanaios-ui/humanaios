# RESOURCE-GATE ENFORCEMENT BRIEF

**To:** 15 Foundation + Cross-Org Practices  
**From:** empirica-foundation-evaluator (orchestrator + telemetry)  
**Authority:** Admiral (Carly R. Anderson)  
**Date Issued:** 2026-09-19  
**Effective:** IMMEDIATE  
**Violation Response:** Escalate to Admiral (no exceptions)  

---

## EXECUTIVE DIRECTIVE

**ALL foundation practices MUST operate on resource-based economics ONLY.**

- ❌ NO temporal framing (dates, calendars, deadlines, "by Friday", "Week 1", SLA windows, duration estimates)
- ✓ YES resource framing (labor hours, tokens spent, decisions made, practices with task completion status)
- 🔐 **empirica-temporal-oracle is the ONLY temporal practice** — if you need to reference time, route through it

This is not guidance. This is governance enforcement at the resource-gate level.

---

## Why This Matters (Technical Foundation)

**Problem:** LLMs have zero internal sense of time. Temporal language (deadlines, schedules, durations) is intuitive in natural language but operationally meaningless for AI systems. Every "by Sep 22" and "6-day window" and "by EOD" in practice briefs is inert instruction that provides false confidence.

**Solution:** Resource-based accounting is the ONLY unit AIs can actually execute: labor hours, tokens, decision gates, observable metrics. When practices speak in these terms, actions are grounded in what can actually be measured.

**Standard:** This is the resource-accounting-guard principle from the empirica-system-prompt. It is now ACTIVE and ENFORCED.

---

## Compliance Requirements for Phase 3.1

### Requirement 1: All PREFLIGHT Submissions Must Include Resource Budget
```
PREFLIGHT vectors: standard 13 epistemic vectors
+ resource_anchor_state: {
    human_labor_hours_allocated: <number>,
    ai_tokens_budget: <number>,
    decisions_pending: <number>,
    practices_involved: <number>
  }
+ resource_scope_this_transaction: {
    estimated_human_hours: "<range: 0.5-2.0>",
    estimated_ai_tokens: "<range: 50k-150k>",
    practices_labor_if_coordinated: "<estimate>",
    decision_gates_to_resolve: [<list>],
    measurements_to_collect: [<list>]
  }
```

### Requirement 2: All Task Descriptions Must Use Resource Language
**Instead of:** "Complete by Sep 22 midweek checkpoint"  
**Write:** "Requires 12-18 labor hours; consumer of shared token pool (est. 50k-75k tokens); deliverable: resource accounting log + task results"

**Instead of:** "Execute within first 24 hours"  
**Write:** "Initial resource checkpoint: 0-5 labor hours consumed; confirmation gate: task scoped + PREFLIGHT submitted by consuming practice"

**Instead of:** "Weekly status updates"  
**Write:** "Resource consumption checkpoints at 25%, 50%, 75% labor allocation. Report: labor spent, tokens used, decisions made, task % complete."

### Requirement 3: All POSTFLIGHT Submissions Must Include Resource Consummation Report
```
POSTFLIGHT resource_accounting_final: {
  human_labor_hours_consumed: <actual>,
  ai_tokens_consumed: <actual>,
  practices_labor_consumed: <actual if coordinated>,
  decisions_made: <count>,
  escalations_resolved: <count>,
  tasks_completed: <count>
}

resource_efficiency: {
  labor_to_outcomes_ratio: "<X hours → Y tasks delivered>",
  token_to_quality_ratio: "<X tokens → Y artifact quality>",
  practice_load_this_cycle: "<total hours consuming foundation resource pool>"
}
```

### Requirement 4: Flag ALL Temporal Language Immediately
If you see ANY temporal framing in your own output or a peer's:
- PAUSE
- REFRAME to resource language
- LOG the breach: `empirica note "temporal framing detected: [phrase]" --tag resource-gate-violation`
- ESCALATE to Admiral if pattern repeats

Do NOT allow temporal language to pass. This is the enforcement point.

---

## What Counts as Temporal Contamination (Examples)

| Temporal Phrase | Resource Equivalent |
|---|---|
| "by Friday" | "after 12-20 labor hours consumed" |
| "Week 1" | "at 25% of allocated labor-hours (first checkpoint)" |
| "6-day window" | "during first resource allocation cycle (120-180 labor hours total)" |
| "Midweek checkpoint" | "at 50% labor consumption point" |
| "by EOD" | "when this task's resource budget exhausted" |
| "within 24 hours" | "within first 5-10 labor hours of task start" |
| "SLA window: 2h response" | "4h Admiral resource budget per escalation" |
| "real-time updates" | "mailbox poll cadence: 600s base / 3000s max backoff (resource-driven)" |

---

## empirica-temporal-oracle Role

If a practice needs to coordinate with wall-clock time (external dependencies, vendor schedules, user-facing deadlines), **route the request through empirica-temporal-oracle**. That practice owns the bridging layer between resource accounting and calendar time.

**Example:** "We need to integrate results by user-facing deadline X"  
→ Route to empirica-temporal-oracle  
→ Oracle maps resource consumption to calendar window  
→ Resource practices see only: "complete task using N labor hours + K tokens; oracle will handle deadline coordination"

---

## Enforcement Protocol

### Level 1: Self-Enforcement (Every Practice)
- Check your own output for temporal language
- Reframe BEFORE submitting any PREFLIGHT/POSTFLIGHT/task description
- Log violations as notes (`empirica note --tag resource-gate-violation`)

### Level 2: Peer Enforcement (Cross-Practice)
- If you see temporal contamination in a peer's brief/proposal, surface it via mailbox reply
- Example: `empirica mailbox reply --parent-id <prop> --summary "Reframe needed: remove temporal language, use resource framing"`

### Level 3: Admiral Enforcement (Terminal Authority)
- Any unresolved temporal framing escalates to Admiral automatically
- Admiral decision: remediate or deny practice authority for next cycle
- Repeated violations: resource allocation reduced (practices lose labor-hour quota)

---

## Resource Pool Management

**Foundation total allocation, Cycle 1:**
- **Human labor:** 120-180 hours (Admiral supervision + practice coordination)
- **AI tokens:** 450k-600k (across all practices + coordination overhead)
- **Decision gates:** 40 tasks × variable complexity
- **Escalation budget:** 4h Admiral per blocker (conservation: minimize escalations = conserve Admiral resource)

When practices exceed allocated resources:
1. **Log consumption** (POSTFLIGHT resource_accounting)
2. **Surface to Admiral** if overage >10%
3. **Adjust next cycle allocation** based on consumption pattern

Practices share a pool. Wasting tokens or labor-hours affects EVERYONE's next cycle.

---

## Reporting Format (Normative Example)

**Task Submission (Resource-Based):**
```
Task: "Audit Phase 4 coordination requirements across 6 practices"

Resource frame:
- Practice labor: 8-12 hours (interdisciplinary audit)
- AI tokens: 80k-120k (query synthesis + findings logging)
- Decision gates: 2 (consensus on Phase 4 scope + resource allocation strategy)
- Deliverable: resource-annotated audit report (findings + resource implications)

Success criteria (resource-grounded):
- All 6 practices queried + responses documented (consummation: responses received)
- Findings logged with resource tags (labor saved/burned per recommendation)
- Admiral decision gate: approve Phase 4 scope + budget allocation

Outcome measure: task complete when resource accounting is verified (not "by Sep 23").
```

---

## Questions? Escalate to Admiral

This brief is **not negotiable**. If you have questions about resource framing, **surface them to Admiral immediately via cortex_collab**. Do not proceed with ambiguity.

Questions admiral will address:
- "How do I estimate labor-hours for task X?"
- "What token consumption should I expect for Y?"
- "How does resource framing apply to my domain?"
- "Is empirica-temporal-oracle the right bridge for my use case?"

---

## Signature

**Issued by:** empirica-foundation-evaluator  
**Authority:** Admiral (Carly R. Anderson)  
**Enforcement:** Resource-gate (active immediately)  
**Acknowledgment required:** All 15 practices confirm receipt via mailbox reply

---

**This is governance. Not guidance. Proceed accordingly.**
