---
# Phase 3.9 Deployment Brief
# Practice: empirica-foundation-evaluator
# Tier: 1
# Generated: 2026-09-17T14:44:43.578901
# Status: READY FOR DEPLOYMENT

## SLA Parameters for empirica-foundation-evaluator

| Parameter | Value | SLA Tier |
|---|---|---|
| Query Latency p95 | 1200ms | 1 |
| Query Latency p99 | 1800ms | 1 |
| Ingestion Rate (min) | 15 chunks/sec | 1 |
| Coordination Latency p95 | 8s | 1 |
| Health Score (min) | 0.75 | 1 |
| Trace Correlation (min) | 0.95 | 1 |
| Escalation Response | 5min | 1 |
| Critical Response | 2min | 1 |

## Alert Rules to Deploy

### From alert-rules-tier1.yaml

**Warning Alerts (escalation: 5min):**
- Query Latency p95 approaching (960ms)
- Health Score warning (0.80)
- Ingestion rate low (15 chunks/sec)
- Trace correlation low (0.95)
- Coordination latency high (8s)

**Critical Alerts (escalation: 2min):**
- Query Latency p95 EXCEEDED (1200ms)
- Health Score BELOW minimum (0.75)

## Deployment Steps

### 1. Validate Alert Rules (mesh-support)
```
Step 1a: Load alert-rules-tier1.yaml
Step 1b: Replace practice-specific threshold values:
  - PRACTICE_P95_MS = 1200
  - PRACTICE_MIN_CPS = 15
  - PRACTICE_COORD_P95_S = 8
Step 1c: Validate syntax: `alert-validator validate <config.yaml>`
Step 1d: Dry-run: `alert-deployer dry-run empirica-foundation-evaluator <config.yaml>`
```

### 2. Instantiate Alert Rules for empirica-foundation-evaluator
```
Step 2a: Apply rules: `alert-deployer apply empirica-foundation-evaluator <config.yaml>`
Step 2b: Verify active: `alert-check status empirica-foundation-evaluator --all-rules`
Step 2c: Log: alert rule count deployed = N
```

### 3. Bind Escalation Protocol
```
L1 (mesh-support):
  - Response time: 5min
  - Action: diagnose + attempt resolution
  - Escalate if unresolved → L2

L2 (evaluator):
  - Response time: 5min
  - Action: governance decision + routing
  - Escalate if critical → L3

L3 (admiral):
  - Response time: 2min (critical only)
  - Action: final authority + broadcast
```

Step 3a: Register escalation chain in Cortex:
  `cortex escalation-bind empirica-foundation-evaluator tier1 L1:mesh-support L2:evaluator L3:admiral`

### 4. Activate Measurement Gates
```
Step 4a: Enable SLA monitoring: `sla-monitor enable empirica-foundation-evaluator`
Step 4b: Set alert thresholds:
  - p95_warning: 960ms
  - p95_critical: 1200ms
  - health_warning: 0.80
  - health_critical: 0.75
Step 4c: Activate: `sla-monitor activate empirica-foundation-evaluator`
Step 4d: Verify: `sla-monitor status empirica-foundation-evaluator` → should show ACTIVE
```

### 5. Smoke Test (Deploy Pipeline)
```
Step 5a: Generate synthetic alert: `alert-inject empirica-foundation-evaluator query_latency=CRITICAL`
Step 5b: Verify escalation chain fires:
  - L1 notified within 5min ✓
  - L2 paged within 5min ✓
Step 5c: Log: synthetic alert test passed / failed
Step 5d: Clear synthetic alert: `alert-clear empirica-foundation-evaluator synthetic`
```

## Completion Checklist

- [ ] Alert rules syntax validated
- [ ] Rules deployed to empirica-foundation-evaluator
- [ ] All rules active and monitoring
- [ ] Escalation chain bound (L1/L2/L3)
- [ ] Measurement gates activated
- [ ] Smoke test passed
- [ ] Evidence logged (commit SHA, test output)

## Timeline

- **Deployment Window:** Sep 17-19 (48 hours)
- **Validation Window:** Sep 20-22 (daily status checks)
- **Post-Deployment:** Sep 23+ (monitoring SLA violations, escalation chain testing)

## Escalation Contacts

- **L1 (mesh-support):** `empirica-mesh-support` SER (4h escalation cycle)
- **L2 (evaluator):** `empirica-foundation-evaluator` (direct)
- **L3 (admiral):** `Admiral.Leadership` (critical authority)

## Success Criteria

1. ✅ Alert rules deployed and active for empirica-foundation-evaluator
2. ✅ Escalation chain functional (L1 → L2 → L3)
3. ✅ Measurement gates reporting SLA violations
4. ✅ Zero escalation response time SLA violations (first 7 days)

---
**Generated:** Phase 3.9 Automation
**Next:** Proceed with step 1 (validation) and acknowledge completion
