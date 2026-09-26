---
# Phase 3.9 Deployment Brief
# Practice: opportunity-aggregator
# Tier: 3
# Generated: 2026-09-17T14:44:43.584158
# Status: READY FOR DEPLOYMENT

## SLA Parameters for opportunity-aggregator

| Parameter | Value | SLA Tier |
|---|---|---|
| Query Latency p95 | 2500ms | 3 |
| Query Latency p99 | 3500ms | 3 |
| Ingestion Rate (min) | 8 chunks/sec | 3 |
| Coordination Latency p95 | 15s | 3 |
| Health Score (min) | 0.65 | 3 |
| Trace Correlation (min) | 0.85 | 3 |
| Escalation Response | 20min | 3 |
| Critical Response | 10min | 3 |

## Alert Rules to Deploy

### From alert-rules-tier3.yaml

**Warning Alerts (escalation: 15min):**
- Query Latency p95 approaching (2000ms)
- Health Score warning (0.70)
- Ingestion rate low (8 chunks/sec)
- Trace correlation low (0.85)
- Coordination latency high (15s)

**Critical Alerts (escalation: 10min):**
- Query Latency p95 EXCEEDED (2500ms)
- Health Score BELOW minimum (0.65)

## Deployment Steps

### 1. Validate Alert Rules (mesh-support)
```
Step 1a: Load alert-rules-tier3.yaml
Step 1b: Replace practice-specific threshold values:
  - PRACTICE_P95_MS = 2500
  - PRACTICE_MIN_CPS = 8
  - PRACTICE_COORD_P95_S = 15
Step 1c: Validate syntax: `alert-validator validate <config.yaml>`
Step 1d: Dry-run: `alert-deployer dry-run opportunity-aggregator <config.yaml>`
```

### 2. Instantiate Alert Rules for opportunity-aggregator
```
Step 2a: Apply rules: `alert-deployer apply opportunity-aggregator <config.yaml>`
Step 2b: Verify active: `alert-check status opportunity-aggregator --all-rules`
Step 2c: Log: alert rule count deployed = N
```

### 3. Bind Escalation Protocol
```
L1 (mesh-support):
  - Response time: 15min
  - Action: diagnose + attempt resolution
  - Escalate if unresolved → L2

L2 (evaluator):
  - Response time: 15min
  - Action: governance decision + routing
  - Escalate if critical → L3

L3 (admiral):
  - Response time: 10min (critical only)
  - Action: final authority + broadcast
```

Step 3a: Register escalation chain in Cortex:
  `cortex escalation-bind opportunity-aggregator tier3 L1:mesh-support L2:evaluator L3:admiral`

### 4. Activate Measurement Gates
```
Step 4a: Enable SLA monitoring: `sla-monitor enable opportunity-aggregator`
Step 4b: Set alert thresholds:
  - p95_warning: 2000ms
  - p95_critical: 2500ms
  - health_warning: 0.70
  - health_critical: 0.65
Step 4c: Activate: `sla-monitor activate opportunity-aggregator`
Step 4d: Verify: `sla-monitor status opportunity-aggregator` → should show ACTIVE
```

### 5. Smoke Test (Deploy Pipeline)
```
Step 5a: Generate synthetic alert: `alert-inject opportunity-aggregator query_latency=CRITICAL`
Step 5b: Verify escalation chain fires:
  - L1 notified within 15min ✓
  - L2 paged within 15min ✓
Step 5c: Log: synthetic alert test passed / failed
Step 5d: Clear synthetic alert: `alert-clear opportunity-aggregator synthetic`
```

## Completion Checklist

- [ ] Alert rules syntax validated
- [ ] Rules deployed to opportunity-aggregator
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

1. ✅ Alert rules deployed and active for opportunity-aggregator
2. ✅ Escalation chain functional (L1 → L2 → L3)
3. ✅ Measurement gates reporting SLA violations
4. ✅ Zero escalation response time SLA violations (first 7 days)

---
**Generated:** Phase 3.9 Automation
**Next:** Proceed with step 1 (validation) and acknowledge completion
