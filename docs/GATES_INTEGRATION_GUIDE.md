# Sentinel Validation Gates — Integration Guide

Three validation gates enforce transaction discipline throughout the empirica ecosystem. This guide covers CLI integration, MCP wiring, and deployment patterns.

## Quick Start

### CLI Commands

Three subcommands available via the Python module:

```bash
# Verify noetic phase completion
python3 -m src.gates.cli readiness-check --input-file readiness_config.json

# Validate resource allocation
python3 -m src.gates.cli resource-check --input-file resource_config.json

# Check epistemic vectors
python3 -m src.gates.cli sentinel-verify --input-file vectors_config.json
```

**Exit Codes:**
- `0` = Pass (gate allows proceeding)
- `1` = Warning (gate passes but tight, escalate if needed)
- `2` = Fail (gate blocks, return to prior phase)

### Input Format

All commands accept JSON configuration via:
- `--config '{"..."}` — inline JSON string
- `--input-file path/to/config.json` — from file
- stdin — pipe JSON directly

### Output Format

Default output is human-readable. For structured output:

```bash
python3 -m src.gates.cli readiness-check --input-file config.json --output json
```

---

## 1. Readiness Gate (readiness-check)

**Purpose:** Verify noetic (investigation) phase is complete before moving to praxic (implementation) phase.

**What it checks:**
- Sufficient evidence collected (default: 3+ items)
- Evidence quality (average confidence > 0.6)
- Assumptions documented (default: ≤2 undocumented)
- Uncertainty acceptable (default: ≤0.25 max)

### Configuration Schema

```json
{
  "evidence": [
    {
      "kind": "read",
      "source": "system-prompt.md",
      "confidence": 0.95,
      "notes": "TRANSACTION DISCIPLINE section"
    },
    {
      "kind": "grep",
      "source": "codebase",
      "confidence": 0.85,
      "notes": "Found 5 references to CHECK"
    }
  ],
  "assumptions": [
    {
      "text": "Sentinel state schema matches vector definitions",
      "confidence": 0.75
    }
  ],
  "unknowns": [
    "Exact MCP tool registration format"
  ],
  "min_evidence": 3,
  "max_assumptions": 2,
  "max_uncertainty": 0.25
}
```

### Outcomes

| Level | Meaning | Action |
|-------|---------|--------|
| `ready` | All checks pass | Proceed to implementation (praxic) |
| `partially_ready` | Passes but recommendations exist | Proceed with caution, escalate monitoring |
| `not_ready` | Blockers exist | Return to investigation, gather more evidence |

### Example: Using in Empirica Workflow

```python
# In your work coordinator:
from src.gates.cli import readiness_check
from argparse import Namespace

# Build readiness config from session state
config = {
    "evidence": collected_evidence,
    "assumptions": undocumented_assumptions,
    "unknowns": known_unknowns
}

args = Namespace(config=json.dumps(config), input_file=None, output="json")
result = readiness_check(args)

if result["status"] == "pass":
    # Proceed to implementation
    execute_praxic_phase()
elif result["status"] == "warning":
    # Escalate for review
    escalate_to_mesh("readiness-marginal")
else:
    # Halt and do more investigation
    log_blocker(result["result"]["blockers"])
```

---

## 2. Resource Guard (resource-check)

**Purpose:** Validate that proposed work fits within current resource constraints.

**What it checks:**
- Human labor budget (checks if work < remaining hours)
- AI token budget (checks if work < remaining tokens)
- Practice capacity (checks if new practices < capacity)
- Escalation availability (checks SLA queue)

### Configuration Schema

```json
{
  "budget": {
    "human_labor_hours_remaining": 100.0,
    "ai_tokens_remaining": 500000,
    "practices_active": 5,
    "practices_capacity": 15,
    "escalations_pending": 2,
    "escalation_sla_hours": 4.0
  },
  "estimate": {
    "human_labor_hours": 10.0,
    "ai_tokens": 50000,
    "practices_affected": 1,
    "escalations_required": 0
  }
}
```

### Outcomes

| Level | Meaning | Action |
|-------|---------|--------|
| `sufficient` | Work fits budget | Proceed immediately |
| `warning` | Tight budget (80%+ consumed) | Proceed but scale back if needed |
| `insufficient` | Work exceeds budget | Defer, reduce scope, or escalate for more allocation |

### Thresholds

**Labor threshold:** 80% of remaining hours
**Token threshold:** 75% of remaining tokens
**Practice threshold:** 85% of capacity
**Escalation threshold:** ~1 escalation per 2h of SLA

### Example: Resource-Aware Dispatch

```python
from src.gates.resource_guard import ResourceGuard, ResourceBudget, ResourceEstimate

# Get current state from orchestrator
budget = ResourceBudget(
    human_labor_hours_remaining=get_remaining_labor(),
    ai_tokens_remaining=get_remaining_tokens(),
    practices_active=active_practice_count(),
    practices_capacity=15,
    escalations_pending=get_pending_escalations(),
    escalation_sla_hours=4.0
)

estimate = ResourceEstimate(
    human_labor_hours=task.estimated_labor,
    ai_tokens=task.estimated_tokens,
    practices_affected=task.practice_count,
    escalations_required=task.escalations_needed
)

guard = ResourceGuard(budget)
result = guard.check(estimate)

if result.level == ResourceCheckLevel.SUFFICIENT:
    dispatch_task(task)
elif result.level == ResourceCheckLevel.WARNING:
    log_warning(f"Resource tight: {result.warnings}")
    dispatch_task_with_monitoring(task)
else:
    escalate_with_message(f"Insufficient resources: {result.blockers}")
```

---

## 3. Sentinel Gate (sentinel-verify)

**Purpose:** Verify epistemic vector state is sufficient for the proposed action.

**What it checks:**
- Know (understanding level)
- Uncertainty (doubt level)
- Context (domain knowledge availability)
- Engagement (motivation/urgency)
- Clarity (goal clarity)
- Coherence (finding consistency)

All vectors checked against action-specific thresholds.

### Configuration Schema

```json
{
  "vectors": {
    "know": 0.78,
    "uncertainty": 0.22,
    "context": 0.82,
    "engagement": 0.87,
    "clarity": 0.81,
    "coherence": 0.72
  },
  "action": "implement"
}
```

### Action Types & Thresholds

**INVESTIGATE** (most permissive):
- Suitable for: Learning phases, exploratory work
- Min know: 0.2 | Max uncertainty: 0.8
- Other vectors: 0.2-0.3 minimum

**IMPLEMENT** (moderate):
- Suitable for: Development, code changes
- Min know: 0.75 | Max uncertainty: 0.25
- Other vectors: 0.70-0.85 minimum

**DEPLOY** (most stringent):
- Suitable for: Production releases, breaking changes
- Min know: 0.90 | Max uncertainty: 0.10
- Other vectors: 0.85-0.95 minimum

**ESCALATE** (high urgency):
- Suitable for: Critical issues, incidents
- Knowledge can be low IF engagement is high (0.90+)
- Allows uncertainty if urgency is clear

**PUBLISH** (high quality):
- Suitable for: Documentation, reports, external outputs
- Requires high coherence (0.85+)
- Requires know: 0.85, all others: 0.85+

### Outcomes

| Level | Meaning | Action |
|-------|---------|--------|
| `pass` | Vectors sufficient for action | Proceed immediately |
| `marginal` | Vectors within 10% of threshold | Proceed with caution, escalate monitoring |
| `fail` | Vectors below threshold | Return to noetic work, improve grounding |

### Recommended Action

Gate also returns `recommended_action` — the highest-confidence action the current vectors support. Use this to auto-scale work: if vectors support IMPLEMENT but you want DEPLOY, either improve vectors first or accept risk.

### Example: Action-Driven Gating

```python
from src.gates.sentinel_verify import SentinelGate, ActionType, EpistemicVectors

# Get current epistemic state from session
vectors = EpistemicVectors(
    know=session.vectors["know"],
    uncertainty=session.vectors["uncertainty"],
    context=session.vectors["context"],
    engagement=session.vectors["engagement"],
    clarity=session.vectors["clarity"],
    coherence=session.vectors["coherence"]
)

gate = SentinelGate()
result = gate.verify(vectors, ActionType.DEPLOY)

if result.level == VectorLevel.PASS:
    execute_deployment()
elif result.level == VectorLevel.MARGINAL:
    # Auto-downgrade to safer action
    safe_action = gate.recommend_action(vectors)
    if safe_action.value == "implement":
        log_warning(f"Vectors marginal for DEPLOY, downgrading to {safe_action.value}")
        execute_implementation()
    else:
        escalate_for_review("Vectors too weak to proceed safely")
else:  # FAIL
    escalate_for_review(f"Vector check failed: {result.failed_checks}")
```

---

## 4. Integration Patterns

### Pattern 1: Sequential Gating (Workflow)

Use all three gates in sequence during a transaction:

```
PREFLIGHT
  ↓
  Check readiness → not ready? → Return to investigation
  ↓ ready
  Check resources → insufficient? → Defer or escalate
  ↓ sufficient
  Check vectors → fail? → Invest in grounding
  ↓ pass/marginal
  Proceed to implementation
  ↓
POSTFLIGHT
```

### Pattern 2: Continuous Gating (Loop)

Use gates in a continuous coordination loop:

```python
while practice_has_work():
    # Check if we're ready to proceed
    readiness = readiness_check(evidence)
    if readiness.status != "pass":
        practice.log_blocker(readiness.blockers)
        continue
    
    # Check if we have resources
    resources = resource_check(budget, estimate)
    if resources.level == "insufficient":
        practice.defer_work()
        continue
    
    # Check if vectors support the action
    action = determine_action(work_type)
    vectors = practice.get_epistemic_vectors()
    verify = sentinel_verify(vectors, action)
    if verify.level == "fail":
        practice.escalate(f"Vectors too weak for {action}")
        continue
    
    # All gates passed, execute work
    practice.execute_work()
```

### Pattern 3: Gated SER Transitions

Use gates to control Shared Epistemic Record (SER) state transitions:

```python
# Before transitioning SER from "open" to "in_progress"
def transition_to_in_progress(ser_id):
    ser = get_ser(ser_id)
    
    # Verify work is ready
    readiness = readiness_check(ser.noetic_state)
    if readiness.status != "pass":
        return error(f"Blocker: {readiness.blockers}")
    
    # Verify resources allocated
    resources = resource_check(ser.budget, ser.estimate)
    if resources.level == "insufficient":
        return error(f"Resource blocker: {resources.blockers}")
    
    # All gates pass, advance SER state
    ser.state = "in_progress"
    ser.save()
    emit_sers_update(ser)
    return success()
```

---

## 5. Deployment Checklist

### Pre-Deployment (Sep 12)

- [ ] Three gate modules tested (50 tests, all passing)
- [ ] CLI commands working (10 tests, manual verification)
- [ ] MCP tool definitions written (mcp_tools.yaml)
- [ ] Integration guide complete (this document)
- [ ] Example configs provided for each gate
- [ ] Threshold tuning guide available

### Beta Deployment (Sep 13-30)

- [ ] Wire gates into empirica CLI via MCP server
- [ ] Test against live Sentinel state
- [ ] Measure gate effectiveness (true positive rate)
- [ ] Calibrate thresholds based on feedback
- [ ] Document any threshold overrides per practice
- [ ] Escalation procedures validated

### Production Rollout (Oct 1-15)

- [ ] All practices briefed on gate behavior
- [ ] Threshold tuning finalized
- [ ] Monitoring/alerting configured
- [ ] Documentation published to wiki
- [ ] Support channel established
- [ ] Week 1 measurement gates ready
- [ ] Go/no-go decision gates active

---

## 6. Troubleshooting

### Gate Always Fails

**Symptom:** Even with good input, gate returns fail.

**Diagnosis:** Check threshold configuration. Thresholds are calibrated conservatively.

**Fix:**
1. Review threshold values in source code
2. Check if practice has custom thresholds in `.breadcrumbs.yaml`
3. Escalate to mesh-support for threshold tuning

### Marginal Results Blocking Work

**Symptom:** Gate returns marginal (within 10% of threshold), blocking progress.

**Diagnosis:** Vectors are on boundary. Normal in early phases.

**Fix:**
1. Use `recommended_action()` to auto-scale to safer action
2. Invest minimally in noetic work to improve specific vector
3. Accept risk and proceed with explicit escalation

### Resource Check Always Warns

**Symptom:** Resource guard frequently returns warning level.

**Diagnosis:** Practice is operating near capacity.

**Fix:**
1. Request additional budget from orchestrator
2. Defer non-critical work
3. Escalate to Admiral for resource reallocation

---

## 7. Advanced: Threshold Tuning

Gates ship with empirically-calibrated thresholds. Per-practice tuning is possible via `.breadcrumbs.yaml`:

```yaml
gate_thresholds:
  empirica-foundation-evaluator:
    readiness:
      min_evidence: 2  # Lower threshold for evaluator
      max_uncertainty: 0.35
    resource:
      labor_warning_threshold: 0.85
    sentinel:
      # Override action thresholds
      implement:
        min_know: 0.70  # Lower than default 0.75
```

Changes take effect on next gate invocation. Measure outcomes and adjust iteratively.

---

## 8. Compliance & Audit

All gate invocations are logged in empirica:
- `empirica finding-log`: For gate results
- `empirica decision-log`: For gate-driven decisions
- `git notes`: For commit-time gate decisions

Pull audit trail with:

```bash
empirica finding-log | grep "gate"
git notes show | grep "gate"
```

---

## Support

**Questions?** Escalate to `empirica-foundation.carly.empirica-mesh-support`

**Issues?** File via `empirica issue-report --component gates`

**Threshold tuning?** Contact Admiral via `empirica collab` (practice-specific guidance)
