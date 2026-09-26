# Gate Deployment Guide

**Status:** Ready for phased rollout  
**Target:** 15 foundation practices  
**Timeline:** Resource-based phases (not calendar-driven)

---

## Overview

Three validation gates enforce transaction discipline:
- **readiness-check**: Verify noetic phase completion before praxic execution
- **resource-check**: Enforce labor hour and token budget constraints
- **sentinel-verify**: Check epistemic vector thresholds before action

All gates are implemented, tested (24/24 passing), and ready for deployment.

---

## Architecture

### Components
1. **Gate Modules** (945 LOC)
   - `readiness_gates.py`: Evidence collection + assumption validation
   - `resource_guard.py`: Budget enforcement
   - `sentinel_verify.py`: Epistemic vector verification

2. **CLI Interface** (255 LOC)
   - Commands: `empirica readiness-check`, `empirica resource-check`, `empirica sentinel-verify`
   - Supports JSON input/output
   - Integrates with session state

3. **MCP Tools** (425 LOC yaml)
   - Three tools exposable to MCP clients
   - Cortex mailbox integration for SER updates
   - Artifact logging (findings with impact ratings)

### Dependencies
- Python 3.14+
- empirica CLI >= 1.13.33
- Cortex mesh (for cross-practice coordination)

---

## Deployment Phases

### Phase 0: Alpha (Evaluator Only)
**When:** Now (evaluator practice only)  
**Duration:** 4h labor  
**Scope:** Single-practice validation

**Tasks:**
1. Deploy gate modules to evaluator practice
2. Wire CLI commands to empirica CLI
3. Run unit tests (24 existing tests)
4. Create integration test fixtures

**Completion criteria:**
- CLI commands executable: `empirica readiness-check`
- All unit tests passing (24/24)
- Integration tests passing with mock state

**Resource:** 0.5h evaluator labor

---

### Phase 1: Beta (3 Practices)
**When:** Once evaluator validates  
**Duration:** 8h labor  
**Scope:** evaluator + mesh-support + autonomy

**Tasks:**
1. Copy gate modules to 3 practices
2. Configure empirica CLI for each
3. Wire Cortex mailbox integration
4. Run integration tests with live SER

**Completion criteria:**
- Gates executable on all 3 practices
- Cortex mailbox sending results
- SER updates acknowledged by mesh-support
- No resource constraint violations

**Resource:** 2.5h labor (0.8h each practice + 0.1h coordination)

---

### Phase 2: Rollout (All 15 Practices)
**When:** Once beta validates  
**Duration:** 32h labor  
**Scope:** All foundation practices

**Tasks:**
1. Distribute gates to remaining 12 practices
2. Configure empirica CLI fleet-wide
3. Enable Cortex mailbox on all practices
4. Establish monitoring + alerting
5. Deploy resource-miner tracking
6. Train on gate usage patterns

**Completion criteria:**
- Gates deployed to all 15 practices
- Cortex mailbox active (messages flowing)
- metrics collecting (pass rate, timing, escalations)
- No practice resource-constrained
- Mesh-support receiving escalations

**Resource:** 32h labor (1-2h per practice + 8h coordination + 6h monitoring)

---

## Configuration

### Per-Practice Setup

1. **Copy modules:**
```bash
cp -r src/gates/ /path/to/practice/src/
```

2. **Wire empirica CLI:**
```bash
empirica setup --force
# Registers CLI commands automatically
```

3. **Configure Cortex mailbox:**
```bash
# In .empirica/project.yaml
cortex:
  mailbox:
    enabled: true
    gates:
      proposal_type: gate_verification_result
      escalate_on_failure: true
      target_practices:
        - empirica-foundation.carly.empirica-mesh-support
```

4. **Enable resource-miner tracking:**
```bash
empirica config --set resource-miner.track-gates=true
```

### Environment Variables

```bash
# Gate thresholds (override defaults)
GATE_MIN_EVIDENCE=3
GATE_MAX_ASSUMPTIONS=2
GATE_MAX_UNCERTAINTY=0.25
GATE_LABOR_THRESHOLD=0.95  # Escalate if > 95% budget consumed
GATE_TOKEN_THRESHOLD=0.90  # Escalate if > 90% budget consumed
```

---

## Operational Procedures

### Running Gates

```bash
# Readiness check (noetic preconditions)
echo '{
  "evidence": [
    {"kind": "read", "source": "src/gates/cli.py", "confidence": 0.9}
  ],
  "assumptions": [],
  "unknowns": []
}' | empirica readiness-check

# Resource check (budget validation)
empirica resource-check --config '{
  "budget": {"labor_hours": 64, "tokens": 100000},
  "estimate": {"labor_hours": 30, "tokens": 50000}
}'

# Sentinel verify (epistemic vectors)
empirica sentinel-verify --action implement --vectors '{
  "know": 0.85,
  "uncertainty": 0.15,
  "context": 0.8,
  "engagement": 0.9,
  "clarity": 0.85,
  "coherence": 0.8
}'
```

### Troubleshooting

**Gate failure:**
- Check threshold values: `GATE_MIN_EVIDENCE`, `GATE_MAX_ASSUMPTIONS`
- Review evidence quality in JSON input
- Escalate via: `empirica mailbox` to mesh-support

**Resource overrun:**
- Check budget allocation: `empirica resource-check`
- Review actual consumption: empirica labor tracking
- Escalate labor or defer work

**Cortex mailbox not sending:**
- Verify listener: `empirica listener status`
- Check project.yaml cortex config
- Restart listener: `empirica listener off && empirica listener on`

---

## Monitoring

### Metrics to Track

```
Gate execution metrics:
- gate_pass_rate: % of gates passing (target: >95%)
- gate_execution_time: avg gate check duration (target: <100ms)
- failure_escalation_rate: escalations per gate failure (target: <10%)
- resource_violations: budget overruns (target: 0)
```

### Alerts

**Critical:**
- Any gate failure → escalate to mesh-support immediately
- Labor budget > 95% → escalate to resource-miner
- Token budget > 90% → escalate to temporal-oracle

**Warning:**
- Gate execution time > 500ms
- Escalation rate trending up

### Dashboard

Access via mesh-support:
```bash
empirica status --gates --output json
```

---

## Rollback Plan

If gates cause issues during rollout:

1. **Pause deployment:** Stop rolling out to new practices
2. **Disable on affected practice:** `empirica config --set gates.enabled=false`
3. **Investigate failure:** Review Cortex mailbox messages + logs
4. **Root cause analysis:** Run integration tests with same state
5. **Fix + recommit:** Apply fix, re-test, resume rollout

Rollback is non-destructive (gates only verify, don't execute).

---

## Success Criteria

**Deployment complete when:**
- ✅ All 15 practices have gates deployed and tested
- ✅ Cortex mailbox flowing (no delivery_failed proposals)
- ✅ Mesh-support monitoring + escalating
- ✅ No resource constraint violations
- ✅ Metrics stable (pass rate >95%, <10% escalation)
- ✅ Zero gate execution failures

**Go-live happens when:**
- ✅ Practices use gates for all transactions (PREFLIGHT → CHECK → POSTFLIGHT)
- ✅ Gate results logged to empirica artifacts (findings + impact)
- ✅ Training complete (practices understand gate failure → escalation flow)

---

## Support

**Questions or blockers:**
- File issue: GitHub (evaluator repo)
- Escalate: `empirica mailbox` to mesh-support
- Cross-org coordination: mesh-support ↔ company mesh-support (via SER)

---

## Appendix: Gate Thresholds

### Readiness Gate
```
min_evidence = 3 items
max_assumptions = 2 undocumented
max_uncertainty = 0.25 (0-1 scale)
```

### Resource Guard
```
labor_hours: 0-100% of allocated
tokens: 0-100% of allocated
escalations: max 3 active per practice
distribution fairness: no practice > 1.5× allocated
```

### Sentinel Verify
```
Action-specific thresholds (TBD pending Sentinel schema)
Escalation floor: any vector < 0.3 → immediate escalation
Enforcement modes: block | warn | log
```

---

**Version:** 1.0  
**Last Updated:** 2026-09-12  
**Maintainer:** empirica-foundation-evaluator  
**Status:** Ready for deployment
