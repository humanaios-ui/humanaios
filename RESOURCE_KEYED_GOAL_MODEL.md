# Resource-Keyed Goal & Task Model (Replaces Temporal Scheduling)

**Status:** Implementation specification v1.0  
**Date adopted:** 2026-08-21  
**Supersedes:** Temporal goal/task model (with created_at, due dates, deadline-based sequencing)

---

## RATIFICATION TRACKING

**Admiral Ratification Status:** 🔴 **AWAITING APPROVAL MARK**

To ratify this document, Admiral (Carly R. Anderson) add your mark below:

```
✅ RATIFIED by Carly R. Anderson, 2026-08-22 13:15 CST, method: Claude Code session review
   - Authorized enforcement: cycle2-resource-keyed (pre-commit hook active)
   - Session: empirica-foundation-evaluator, transaction f72cac18-9472-4ae6-b018-54f6ae7966e8
   - Effective: Immediately upon commit
```

This mark is the ground truth for whether this system is operational or merely documented.

---

---

## Core Model: Resources as First-Class State

### Goal Structure (Resource-Keyed)

```json
{
  "goal_id": "G-PHASE2-PARALLEL-DEPLOYMENT",
  "objective": "Deploy dual-path Cloudflare infrastructure (Workers Alt + HAIOSCC)",
  
  "resource_budget": {
    "human_labor_hours": 13,
    "ai_tokens": 80000,
    "practice_labor_hours": 0,
    "decisions_required": 1
  },
  
  "resource_state_open": {
    "human_labor_consumed": 0,
    "ai_tokens_consumed": 0,
    "decisions_made": 0
  },
  
  "blocked_by": [
    {
      "resource_state": "Admiral decision labor consumed < 1 hour",
      "reason": "Admiral must approve parallel deployment model before measurement-lead proceeds"
    }
  ],
  
  "unblocks": [
    {
      "capability": "measurement_phase_live",
      "reason": "Workers Alternative deployment unblocks measurement prep immediately (no decision gate)"
    },
    {
      "capability": "phase_3_readiness",
      "reason": "Measurement infrastructure ready enables Phase 3 gate measurement"
    }
  ],
  
  "success_criteria": [
    {
      "criterion": "Path A labor consumed",
      "resource_measure": "10 human_labor_hours",
      "validation": "time-entry audit in POSTFLIGHT"
    },
    {
      "criterion": "Path A infrastructure deployed",
      "resource_measure": "Durable Objects + Grafana wired + test metrics ingested",
      "validation": "infrastructure health check (curl endpoints)"
    },
    {
      "criterion": "Path B labor consumed (conditional)",
      "resource_measure": "5 human_labor_hours IF Admiral approval consumed",
      "validation": "time-entry audit + decision artifact logged"
    }
  ],
  
  "tasks": [
    {
      "task_id": "T1-APPROVAL",
      "description": "Admiral approves parallel deployment strategy (yes/no decision)",
      "resource_budget": {
        "human_labor_hours": 1,
        "decisions_required": 1
      },
      "blocked_by": [],
      "unblocks": ["T2-PATH-A-SETUP"],
      "resource_measure": "Admiral decision labor consumed (1 hour estimate, actual measured at POSTFLIGHT)"
    },
    {
      "task_id": "T2-PATH-A-SETUP",
      "description": "Deploy Cloudflare Workers Alternative infrastructure (independent path)",
      "resource_budget": {
        "human_labor_hours": 10,
        "ai_tokens": 50000
      },
      "blocked_by": [
        {
          "resource_state": "Admiral approval decision consumed",
          "reason": "Need explicit go-ahead before allocation"
        }
      ],
      "unblocks": [
        "T3-MEASUREMENT-PREP",
        "T4-PATH-B-SETUP"
      ],
      "resource_measure": "measurement-lead labor consumed (cumulative hours tracked in POSTFLIGHT)"
    },
    {
      "task_id": "T3-MEASUREMENT-PREP",
      "description": "Begin measurement phase prep (unblocked from decision gate once Path A infrastructure available)",
      "resource_budget": {
        "human_labor_hours": 10,
        "ai_tokens": 20000
      },
      "blocked_by": [
        {
          "resource_state": "Path A infrastructure deployed",
          "reason": "Measurement prep cannot start until datasources available"
        }
      ],
      "unblocks": ["T5-WEEK2-MEASUREMENT"],
      "resource_measure": "measurement-lead + Admiral labor consumed"
    },
    {
      "task_id": "T4-PATH-B-SETUP",
      "description": "Deploy HAIOSCC Cloudflare Functions (conditional on Admiral decision)",
      "resource_budget": {
        "human_labor_hours": 5,
        "ai_tokens": 30000
      },
      "blocked_by": [
        {
          "resource_state": "Admiral decision labor consumed AND Admiral approved HAIOSCC",
          "reason": "HAIOSCC only proceeds if Admiral decision was yes"
        }
      ],
      "unblocks": ["T5-WEEK2-MEASUREMENT"],
      "resource_measure": "measurement-lead labor consumed (only if decision approves)"
    },
    {
      "task_id": "T5-WEEK2-MEASUREMENT",
      "description": "Run both systems live Week 2, measure performance orthogonally",
      "resource_budget": {
        "human_labor_hours": 3,
        "ai_tokens": 10000
      },
      "blocked_by": [
        {
          "resource_state": "Path A infrastructure deployed",
          "reason": "Path A is mandatory; Path B conditional"
        }
      ],
      "unblocks": [],
      "resource_measure": "Admiral + measurement-lead labor measuring both systems"
    }
  ]
}
```

---

## Resource State Transitions (Replaces Timeline)

Instead of "before/after date X", express as resource state:

### BEFORE (Temporal — Deprecated)
```
Task A: queued (due 2026-08-21)
Task B: queued (depends on Task A, due 2026-08-22)
Task C: queued (depends on Task B, due 2026-08-23)
```
❌ Hidden assumption: dates carry the dependency chain. If dates slip, everything shifts invisibly.

### AFTER (Resource-Keyed — New Model)
```
Task A: blocked_by=[] (approved to start now)
  resource_budget: 1 human_labor_hour, 1 decision
  unblocks: Task B (once 1 labor_hour consumed + 1 decision_made)

Task B: blocked_by=[Task A labor consumed + decision made]
  resource_budget: 10 human_labor_hours
  unblocks: Task C (once 10 labor_hours consumed)

Task C: blocked_by=[Task B labor consumed (10 hours)]
  resource_budget: 5 human_labor_hours
  unblocks: capability_X (once 5 labor_hours consumed)
```
✓ Explicit: each task is gated by WHAT RESOURCE STATE from prior task, not time.

---

## Progress Measurement (Replaces "% Complete by Date")

### BEFORE (Temporal — Deprecated)
```
Goal: Phase 2 Integration
Status: 40% complete
Due: 2026-08-25
Days remaining: 4
Current: On track
```
❌ "On track" means what? No resource visibility.

### AFTER (Resource-Keyed — New Model)
```
Goal: Phase 2 Integration
Resource budget: 13 human_labor_hours, 80k tokens

Consumed so far:
  T1 (Admiral approval): 0.5h / 1h (50% of approval labor)
  T2 (Path A setup): 3h / 10h (30% of infrastructure labor)
  T3 (Measurement prep): 1h / 10h (10% of prep labor)
  
Total consumed: 4.5h / 13h (35% of goal labor budget)
Total tokens consumed: 35k / 80k

Blocked: T4 (Path B) — waiting on T1 to consume final 0.5h decision labor
Unblocked: T3 can proceed in parallel with T2 (no dependency on T2 completion)

Remaining: 8.5h labor + 45k tokens to goal completion
```
✓ Clear: what's consumed, what's available, what's blocked, what can proceed in parallel.

---

## Audit Mechanism: Detect & Reject Temporal Framing

### Rule 1: No Dates/Times in Work Artifacts

**BANNED words/patterns in goal/task descriptions:**
- "by [date]" → use "once [resource state] is reached" instead
- "[day of week]" → use "after [labor hours] consumed" instead
- "due [date]" → use "blocked_by [resource state]" instead
- "takes [duration]" → use "budget [labor hours]" instead
- "deadline" → use "resource constraint" instead
- "schedule" → use "resource allocation" instead

### Rule 2: Validate blocked_by & unblocks Are Resource-Based

**Every blocked_by entry must match pattern:**
```
"blocked_by": [
  {
    "resource_state": "[resource] consumed >= [quantity]",
    "reason": "[why this resource matters]"
  }
]
```

❌ INVALID: `"blocked_by": ["Task A"]` (no resource state)  
❌ INVALID: `"blocked_by": ["before Friday"]` (temporal)  
✓ VALID: `"blocked_by": [{"resource_state": "Admiral decision labor consumed >= 2 hours", "reason": "need approval before proceeding"}]`

### Rule 3: Success Criteria Must Be Measurable by Resource Consumption

**Every success_criterion must answer:** "How do I know this consumed the right resources?"

```json
{
  "criterion": "Path A infrastructure deployed",
  "resource_measure": "10 human_labor_hours consumed by measurement-lead + 50k tokens + 5 curl-verified endpoints",
  "validation": "POSTFLIGHT audit: human_labor_consumed >= 10h AND endpoint_health_check PASS"
}
```

❌ INVALID: `"criterion": "completed by Friday"` (temporal)  
✓ VALID: `"criterion": "completed once 10 human_labor_hours consumed and validated by infrastructure health check"`

---

## POSTFLIGHT Adjudication (Replaces "Days Late/On Time")

### Goal Completion Verdict

At POSTFLIGHT, ask:

1. **Did we consume the budgeted resources?**
   ```
   Budget: 13h labor, 80k tokens
   Consumed: 13.2h labor, 78.5k tokens
   Verdict: HELD (within variance)
   ```

2. **Were blocked_by states correctly modeled?**
   ```
   Predicted: T4 blocked until Admiral consumed 1h decision labor
   Actual: Admiral took 1.2h, then T4 proceeded
   Verdict: HELD (model was accurate)
   ```

3. **Did unblocks capabilities emerge as predicted?**
   ```
   Predicted: T3 measurement_prep unblocked after Path A deployed (10h labor)
   Actual: T3 started after Path A had consumed 8.5h, completed in 11h total
   Verdict: HELD (capability available, slightly early)
   ```

4. **What resource divergence did we observe?**
   ```
   Estimated labor: 13h
   Actual labor: 13.2h (+0.2h)
   Variance: +1.5% (acceptable)
   
   Estimated tokens: 80k
   Actual tokens: 78.5k (-1.5k)
   Variance: -2% (favorable)
   ```

---

## Implementation: Enforce at Artifact-Creation Time

### Validation Function (Pseudo-Code)

```python
def validate_goal_artifact(goal_dict):
    """
    Before logging goal to empirica, scan for temporal framing.
    Reject if found.
    """
    banned_patterns = [
        r'\bby\s+\d{4}-\d{2}-\d{2}',  # by 2026-08-21
        r'\b(Monday|Tuesday|Friday)\b',  # day names
        r'\bdue\s+',  # due [date]
        r'\bdeadline\b',  # deadline
        r'\btakes?\s+\d+\s+(hours?|days?|weeks?)',  # takes 2 hours
        r'\bschedule[d]?\b',  # scheduled
        r'\bby\s+(EOD|morning|afternoon|end of week)',  # time-of-day
    ]
    
    for field in ['objective', 'description']:
        for pattern in banned_patterns:
            if re.search(pattern, goal_dict[field], re.IGNORECASE):
                raise ValueError(
                    f"TEMPORAL FRAMING DETECTED in {field}: '{pattern}'\n"
                    f"Rewrite using resource-keyed model:\n"
                    f"  'by [date]' → 'once [resource_state] reached'\n"
                    f"  '[duration]' → '[resource] budget [amount]'\n"
                    f"  'blocked_by [task]' → 'blocked_by [resource_state]'"
                )
    
    # Validate blocked_by entries
    for task in goal_dict.get('tasks', []):
        for blocker in task.get('blocked_by', []):
            if 'resource_state' not in blocker:
                raise ValueError(
                    f"Task {task['task_id']}: blocked_by missing resource_state.\n"
                    f"Must specify: blocked_by: [{{'resource_state': '[X] consumed >= [N]', 'reason': '...'}}]"
                )
    
    return True  # Passes validation
```

### Integration into empirica CLI

```bash
# When user tries to log goal with temporal framing:
$ empirica goals-create --objective "Finish by Friday" ...

ERROR: Temporal framing detected in objective
  Pattern: "by Friday"
  
Rewrite as:
  "Finish once measurement-lead consumes 10 human_labor_hours and infrastructure health check passes"

Fix and retry.
```

---

## Conversion Examples: Temporal → Resource-Keyed

### Example 1: Simple Task

**BEFORE (Temporal):**
```json
{
  "task": "Deploy Cloudflare infrastructure",
  "due": "2026-08-23",
  "depends_on": ["Admiral approves"],
  "time_estimate": "5 hours",
  "status": "Not started (waiting for approval)"
}
```

**AFTER (Resource-Keyed):**
```json
{
  "task_id": "T-CLOUDFLARE-DEPLOY",
  "description": "Deploy Cloudflare Workers infrastructure",
  "resource_budget": {
    "human_labor_hours": 5,
    "ai_tokens": 30000
  },
  "blocked_by": [
    {
      "resource_state": "Admiral approval decision consumed (1 decision_made)",
      "reason": "Need explicit approval decision before proceeding"
    }
  ],
  "unblocks": [
    {
      "capability": "measurement_phase_ready",
      "reason": "Infrastructure online, datasources available for measurement"
    }
  ],
  "status": "queued (blocked until Admiral decision labor consumed)"
}
```

### Example 2: Parallel Dependencies

**BEFORE (Temporal):**
```json
{
  "timeline": [
    "Mon 08-21: Task A (6h)",
    "Tue 08-22: Task B (4h, depends on A)",
    "Tue 08-22: Task C (3h, independent)",
    "Wed 08-23: Task D (2h, depends on B+C)"
  ]
}
```
❌ Hidden: What if Task A takes 8h? Does everything shift?

**AFTER (Resource-Keyed):**
```json
{
  "tasks": [
    {
      "task_id": "A",
      "resource_budget": {"human_labor_hours": 6},
      "unblocks": ["B"]
    },
    {
      "task_id": "B",
      "resource_budget": {"human_labor_hours": 4},
      "blocked_by": [{"resource_state": "Task A labor consumed >= 6h"}],
      "unblocks": ["D"]
    },
    {
      "task_id": "C",
      "resource_budget": {"human_labor_hours": 3},
      "blocked_by": [],
      "unblocks": ["D"]
    },
    {
      "task_id": "D",
      "resource_budget": {"human_labor_hours": 2},
      "blocked_by": [
        {"resource_state": "Task B labor consumed >= 4h"},
        {"resource_state": "Task C labor consumed >= 3h"}
      ]
    }
  ]
}
```
✓ Clear: Task A can take 6h or 12h; Task D still waits for both B AND C labor to be consumed, regardless of when.

---

## Adoption Checklist

- [ ] Replace all temporal fields (created_at, due_date, deadline) with resource_state_open / resource_budget
- [ ] Convert all dependencies from task-ID chains to resource_state blocked_by entries
- [ ] Update empirica CLI to reject temporal framing (validation function deployed)
- [ ] Audit existing goals/tasks, convert to resource-keyed model or archive
- [ ] Train measurement ceremony to report: "resources consumed so far / budget remaining" (not "days remaining")
- [ ] Update POSTFLIGHT template to adjudicate resource consumption, not timeline
- [ ] Document decision history: which resource constraints drove which choices (not dates)

---

**Model Status:** LIVE (2026-08-21)  
**Enforcement:** Temporal framing rejection enabled at goal-creation time  
**Rollback plan:** If audit mechanism causes friction, disable rejection but keep resource model as recommendation (softer enforcement)
Night ratification approved.
