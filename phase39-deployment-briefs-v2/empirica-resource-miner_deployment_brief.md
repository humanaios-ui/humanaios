---
# Phase 3.9 Deployment Brief (v2 - Corrected Architecture)
# Practice: empirica-resource-miner
# Tier: 2
# Generated: 2026-09-17T15:09:18.640070
# Status: READY FOR DEPLOYMENT

## SLA Parameters for empirica-resource-miner

| Parameter | Value | Tier 2 |
|---|---|---|
| Query Latency p95 | 2000ms | Target SLA |
| Query Latency p99 | 3000ms | Target SLA |
| Ingestion Rate (min) | 8 chunks/sec | Minimum |
| Coordination Latency p95 | 12s | Target SLA |
| Health Score (min) | 0.65 | Minimum |
| Trace Correlation (min) | 0.85 | Minimum |
| Escalation Response (L1) | 10min | Warning alerts |
| Escalation Response (L2) | 10min | Governance |
| Escalation Response (L3) | 5min | Critical (Admiral) |

## Deployment Architecture

**This brief uses actual Phase 3.6-3.7 infrastructure:**
- Alert rules: JSON format (alerts defined in alert_rules.json)
- Alert evaluation: Prometheus/Loki metrics + Python conditions
- Escalation: Python classes (AlertEscalationOrchestrator, CortexEscalationProposer)
- Measurement gates: MeasurementGates (phase37_measurement_gates.py)

## Deployment Steps

### Step 1: Add Per-Practice Alert Rules to JSON

**File: analytics/alert_rules.json**

Add these 5 alert rules for empirica-resource-miner (Tier 2):

```json
{
  "id": "tier2_empirica-resource-miner_query_latency_warning",
  "name": "Tier 2: Query Latency Warning (empirica-resource-miner)",
  "description": "Query latency p95 approaching SLA (1600ms)",
  "type": "query_latency",
  "severity": "warning",
  "metric": "loki_query_duration_seconds",
  "condition": {
    "quantile": 0.95,
    "operator": ">",
    "threshold": 2.0,
    "duration": "5m"
  },
  "scope": "per_practice",
  "practice_filter": "empirica-resource-miner",
  "routing": "alert",
  "escalation_minutes": 10,
  "message_template": "🟡 WARNING: {practice} query latency p95 = {current_value:.3f}s (threshold: 2000ms)"
}
```

```json
{
  "id": "tier2_empirica-resource-miner_query_latency_critical",
  "name": "Tier 2: Query Latency Critical (empirica-resource-miner)",
  "description": "Query latency p95 EXCEEDED SLA (2000ms)",
  "type": "query_latency",
  "severity": "critical",
  "metric": "loki_query_duration_seconds",
  "condition": {
    "quantile": 0.95,
    "operator": ">",
    "threshold": 2.0,
    "duration": "2m"
  },
  "scope": "per_practice",
  "practice_filter": "empirica-resource-miner",
  "routing": "escalation",
  "escalation_minutes": 5,
  "message_template": "🔴 CRITICAL: {practice} query latency p95 = {current_value:.3f}s - SLA EXCEEDED"
}
```

```json
{
  "id": "tier2_empirica-resource-miner_health_warning",
  "name": "Tier 2: Health Score Warning (empirica-resource-miner)",
  "description": "Health score approaching minimum (0.65)",
  "type": "health_degradation",
  "severity": "warning",
  "metric": "empirica_practice_health_score",
  "condition": {
    "operator": "<",
    "threshold": 0.7000000000000001,
    "duration": "10m"
  },
  "scope": "per_practice",
  "practice_filter": "empirica-resource-miner",
  "routing": "alert",
  "escalation_minutes": 10,
  "message_template": "🟡 WARNING: {practice} health score = {current_value:.2f} (minimum: 0.65)"
}
```

```json
{
  "id": "tier2_empirica-resource-miner_health_critical",
  "name": "Tier 2: Health Score Critical (empirica-resource-miner)",
  "description": "Health score BELOW minimum (0.65)",
  "type": "health_degradation",
  "severity": "critical",
  "metric": "empirica_practice_health_score",
  "condition": {
    "operator": "<",
    "threshold": 0.65,
    "duration": "5m"
  },
  "scope": "per_practice",
  "practice_filter": "empirica-resource-miner",
  "routing": "escalation",
  "escalation_minutes": 5,
  "message_template": "🔴 CRITICAL: {practice} health CRITICAL - score {current_value:.2f}"
}
```

```json
{
  "id": "tier2_empirica-resource-miner_ingestion_low",
  "name": "Tier 2: Ingestion Rate Low (empirica-resource-miner)",
  "description": "Log ingestion rate below minimum",
  "type": "ingestion_rate",
  "severity": "warning",
  "metric": "loki_ingester_chunks_flushed_total",
  "condition": {
    "operator": "<",
    "baseline_pct": 80,
    "duration": "10m"
  },
  "scope": "per_practice",
  "practice_filter": "empirica-resource-miner",
  "routing": "alert",
  "escalation_minutes": 10,
  "message_template": "🟡 WARNING: {practice} ingestion rate = {current_value}/s (minimum: 8)"
}
```

**Steps:**
- [ ] Edit analytics/alert_rules.json
- [ ] Paste the 5 JSON alert rule objects above into the "alert_rules" array
- [ ] Validate JSON syntax: `python3 -m json.tool analytics/alert_rules.json > /dev/null && echo "✅ Valid"`

### Step 2: Instantiate Rules via AlertEscalationOrchestrator

**File: phase36_orchestration.py (already exists)**

The orchestrator will:
1. Load alert_rules.json
2. Filter rules matching "practice_filter": "empirica-resource-miner"
3. Evaluate conditions against live Prometheus/Loki metrics
4. Fire escalations when thresholds breached

**Execution:**
```bash
python3 phase36_orchestration.py
```

Expected output: Each alert rule evaluated, escalations routed to L1/L2/L3 per tier.

### Step 3: Bind Escalation Chain via CortexEscalationProposer

**File: analytics/cortex_escalation_proposer.py (already exists)**

Register escalation targets for empirica-resource-miner:

```python
# In cortex_escalation_proposer.py, update:
self.practices["empirica-resource-miner"] = "empirica-foundation.carly.empirica-resource-miner"
```

The proposer will:
- Route L1 alerts to mesh-support (for diagnosis + coaching)
- Route L2 alerts to evaluator (for governance + routing)
- Route L3 critical alerts to admiral (final authority)

### Step 4: Activate Measurement Gate

**File: phase37_measurement_gates.py**

Add per-practice SLA gate for empirica-resource-miner:

```python
# In _define_gates() method, add this MeasurementGate:
MeasurementGate(
  gate_id="sla_empirica-resource-miner_tier2",
  category="escalation",
  name="SLA Enforcement: empirica-resource-miner",
  description="Tier 2 SLA monitoring for empirica-resource-miner",
  success_criteria=dict(query_p95_ms="2000ms"),
  metric="query_latency_p95_ms",
  threshold=2000,
  operator="<",
  current_value=0,
  status=GateStatus.PENDING,
  evidence="Alert rules instantiated"
)
```

**Steps:**
- [ ] Edit phase37_measurement_gates.py
- [ ] Add MeasurementGate to _define_gates() method (copy structure above)
- [ ] Run: `python3 phase37_measurement_gates.py`
- [ ] Verify gate in output: `sla_empirica-resource-miner_tier2: PENDING`

### Step 5: Smoke Test - Synthetic Alert Injection

**Purpose:** Verify end-to-end escalation chain

**Steps:**
```bash
# 1. Manually inject synthetic alert to Prometheus/Loki for empirica-resource-miner
python3 << 'PYTEST'
import time
# Simulate alert: query_latency_p95 = 120% of SLA
synthetic_value = int(2000 * 1.2)
# Write to metrics exporter / Prometheus push gateway
# (Requires local Prometheus setup; skip if not available)
PYTEST

# 2. Monitor escalation chain firing:
# - Watch analytics/escalation_proposals.json for "empirica-resource-miner" entries
# - Verify L1 alert within 10min
# - Verify L2 escalation within 10min
# - Verify L3 critical within 5min

# 3. Check mesh delivery:
cat analytics/mesh_outbox.json | grep -A5 "empirica-resource-miner"

# 4. Clear synthetic alert:
# Remove synthetic value from Prometheus/Loki
```

## Completion Checklist

- [ ] Step 1: Alert rules added to alert_rules.json (5 rules for empirica-resource-miner)
- [ ] Step 1: JSON syntax validated
- [ ] Step 2: AlertEscalationOrchestrator executed (rules loaded)
- [ ] Step 3: Escalation targets registered in CortexEscalationProposer
- [ ] Step 4: MeasurementGate added to phase37_measurement_gates.py
- [ ] Step 5: Smoke test executed (synthetic alert → escalation chain)
- [ ] Step 5: Escalation chain responding within SLA targets
- [ ] **COMPLETE:** Log completion with evidence (files modified, test output)

## Timeline

- **Deployment Window:** Sep 17-19 (48 hours)
- **Alert rules live:** Within 1 hour of JSON edit
- **Measurement gate active:** Within 5 minutes of orchestrator execution
- **Smoke test validation:** Within 10 minutes

## Success Criteria

1. ✅ Alert rules instantiated and loaded
2. ✅ Measurement gate reports SLA status
3. ✅ Escalation chain fires correctly on synthetic alert
4. ✅ Escalation response times within SLA targets:
   - L1: 10min
   - L2: 10min
   - L3: 5min
5. ✅ Zero false positives in first 7 days

---

## Escalation Contacts

- **L1 (mesh-support):** Contact empirica-mesh-support SER
- **L2 (evaluator):** Contact empirica-foundation-evaluator (direct)
- **L3 (admiral):** Admiral.Leadership (critical authority, auto-escalated)

---

**Next:** Complete all checklist items, then report completion with evidence.
