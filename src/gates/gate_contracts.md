# Validation Gate Contracts

**Status:** Design Phase (Sentinel schema pending from autonomy)  
**Completion:** Awaiting schema to fill Type Definitions section

---

## Gate 1: Readiness Check

**Purpose:** Validate that a practice meets preconditions before executing work.

**Contract:**
```python
class ReadinessGate(Gate):
    name: str = "readiness-check"
    
    def validate(self, practice_state: Dict) -> GateResult:
        """
        Check preconditions:
        - Practice has committed resources (labor hours allocated)
        - Dependencies are satisfied (all blocking tasks complete)
        - Work artifacts are registered (no orphaned goals)
        - Mesh coordination is active (heartbeat received within threshold)
        
        Returns: GateResult(passed: bool, blocker: Optional[str])
        """
        pass
```

**Input Schema:**
```json
{
  "practice_id": "string (canonical 3-form)",
  "allocated_hours": "float (cumulative labor budget)",
  "dependencies": ["task_id"],
  "last_heartbeat": "ISO8601 timestamp",
  "artifacts": ["artifact_id"]
}
```

**Output Schema:**
```json
{
  "passed": "boolean",
  "blocker": "string or null",
  "details": {
    "resources_ready": "boolean",
    "dependencies_satisfied": "boolean",
    "artifacts_registered": "boolean",
    "coordination_active": "boolean"
  }
}
```

**Threshold Constraints:**
- Heartbeat: within 1800s (30 min) of current time
- Resources: minimum 0.5h allocated
- Dependencies: 100% satisfied (0 blocking tasks)
- Artifacts: all non-archived (0 orphaned)

---

## Gate 2: Resource Guard

**Purpose:** Enforce resource allocation and prevent budget overruns.

**Contract:**
```python
class ResourceGuard(Gate):
    name: str = "resource-check"
    
    def validate(self, consumption_state: Dict) -> GateResult:
        """
        Check resource constraints:
        - Labor hours consumed <= allocated budget
        - Token usage within Sentinel thresholds (TBD: Sentinel schema)
        - Escalation count within safety bounds
        - No resource starvation (equal distribution across practices)
        
        Returns: GateResult(passed: bool, consumed_pct: float, remaining: float)
        """
        pass
```

**Input Schema:**
```json
{
  "practice_id": "string",
  "allocated_labor_hours": "float",
  "consumed_labor_hours": "float",
  "allocated_tokens": "integer",
  "consumed_tokens": "integer",
  "escalation_count": "integer",
  "practice_count": "integer (total active practices)"
}
```

**Output Schema:**
```json
{
  "passed": "boolean",
  "consumed_pct": "float (0-100)",
  "remaining_hours": "float",
  "remaining_tokens": "integer",
  "details": {
    "labor_within_budget": "boolean",
    "tokens_within_budget": "boolean",
    "escalations_safe": "boolean",
    "distribution_fair": "boolean"
  }
}
```

**Threshold Constraints:**
- Labor consumed: <= 100% of allocated
- Tokens consumed: <= Sentinel threshold (TBD)
- Escalations: <= 3 active per practice
- Distribution fairness: no practice > (allocated × 1.5)

---

## Gate 3: Sentinel Verify

**Purpose:** Validate epistemic state against Sentinel vector thresholds.

**Contract:**
```python
class SentinelVerify(Gate):
    name: str = "sentinel-verify"
    
    def validate(self, sentinel_state: SentinelStateSchema) -> GateResult:
        """
        Check Sentinel vectors against thresholds:
        - know: confidence in current state
        - uncertainty: unresolved predictions
        - completion: work toward objectives
        - change: divergence from baseline
        - impact: reputational/material consequence
        - state: coherence of internal model
        (Additional vectors per Sentinel schema)
        
        Returns: GateResult(passed: bool, vectors: Dict[str, float])
        """
        pass
```

**Input Schema:**
```
TBD: Awaiting Sentinel state schema from empirica-autonomy
Placeholder structure:
{
  "practice_id": "string",
  "vectors": {
    "know": "float [0-1]",
    "uncertainty": "float [0-1]",
    "completion": "float [0-1]",
    "change": "float [0-1]",
    "impact": "float [0-1]",
    "state": "float [0-1]",
    ... (additional vectors per schema)
  },
  "timestamp": "ISO8601"
}
```

**Output Schema:**
```json
{
  "passed": "boolean",
  "vector_status": {
    "know": {"value": "float", "threshold": "float", "ok": "boolean"},
    "uncertainty": {"value": "float", "threshold": "float", "ok": "boolean"},
    ...
  },
  "failing_vectors": ["string"],
  "enforcement_mode": "block|warn|log"
}
```

**Threshold Constraints:**
- TBD: Will be populated from Sentinel schema
- Placeholder: all vectors must be >= 0.5 (conservative baseline)
- Escalation: any vector < 0.3 triggers immediate escalation to mesh-support

---

## Gate Lifecycle

```
readiness-check (gate 1)
    ↓ PASS
resource-check (gate 2)
    ↓ PASS
sentinel-verify (gate 3)
    ↓ PASS
═══════════════════════════════════════════════════
GATES PASSED: work can proceed
═══════════════════════════════════════════════════
```

**Failure Handling:**
- Gate failure blocks subsequent gates (fail-fast)
- Failure details logged to empirica finding-log with impact rating
- Escalation: resource-check failure → mesh-support, sentinel-verify failure → autonomy

---

## Implementation Status

| Component | Status | Notes |
|-----------|--------|-------|
| ReadinessGate class | READY | No schema dependency |
| ResourceGuard class | READY | No schema dependency |
| SentinelVerify class | BLOCKED | Awaiting schema |
| Input/output schemas | READY | ReadinessGate + ResourceGuard only |
| Threshold constraints | PARTIAL | Resource values set; Sentinel TBD |
| Lifecycle orchestration | READY | Gates can be sequenced |
| Failure handling | READY | Can log failures now |
| Integration tests | BLOCKED | Need schema + mock Sentinel state |

---

## Blockers

**CRITICAL:** Sentinel state schema from empirica-autonomy
- Required to: populate SentinelVerify input schema, define vector thresholds, create test fixtures
- Impact: unblocks implementation of 8h work (impl_sentinel_verify + pytest_coverage_gates)
- Proposed by: empirica-foundation-evaluator
- Collab sent: prop_yprzrdldpjfljmzsopelx7tidm (2026-09-12)

---

## Next Steps (Once Schema Received)

1. Fill in SentinelVerify input schema with concrete vector definitions
2. Set Sentinel threshold constraints (0.3 escalation floor, etc.)
3. Create Pydantic models for schema validation
4. Write pytest fixtures with mock Sentinel state
5. Implement sentinel_verify.py (~8h)
6. Full coverage tests (~6h)
7. Wire into CLI (sentinel-verify command, 4h)
