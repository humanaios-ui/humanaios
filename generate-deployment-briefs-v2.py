#!/usr/bin/env python3
"""
Phase 3.9: Deployment Brief Generator (v2 - Corrected Architecture)
Generates per-practice deployment briefs using actual infrastructure:
  - JSON alert rule format (Prometheus metrics + conditions)
  - Python orchestration (AlertEscalationOrchestrator, CortexEscalationProposer)
  - Measurement gate binding
  - NO non-existent CLI tools
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Load SLA roster from Phase 3.8
sla_roster_path = Path("analytics/sla_roster_complete.json")
if not sla_roster_path.exists():
    print(f"Error: {sla_roster_path} not found", file=sys.stderr)
    sys.exit(1)

with open(sla_roster_path) as f:
    sla_data = json.load(f)

TIER_MAPPING = {
    "empirica-autonomy": 1,
    "empirica-mesh-support": 1,
    "empirica-foundation-evaluator": 1,
    "empirica-outreach": 1,
    "empirica-analytics": 2,
    "empirica-resource-miner": 2,
    "empirica-temporal-oracle": 2,
    "humanaios": 2,
    "humanaios-ui": 2,
    "humanaios-internal": 3,
    "website": 3,
    "acat-x": 3,
    "collaborator-ops": 3,
    "flta-app-empirica": 3,
    "grok-crossref": 3,
    "local-machine-optimizer": 3,
    "opportunity-aggregator": 3,
}

TIER_ESCALATION = {
    1: {"l1_minutes": 5, "l2_minutes": 5, "l3_minutes": 2},
    2: {"l1_minutes": 10, "l2_minutes": 10, "l3_minutes": 5},
    3: {"l1_minutes": 15, "l2_minutes": 15, "l3_minutes": 10},
}

def generate_brief(practice_name: str, sla: dict, tier: int) -> str:
    """Generate corrected deployment brief for a single practice"""

    escalation = TIER_ESCALATION[tier]
    p95_warning_threshold = int(sla['query_latency_p95_ms'] * 0.8)
    p95_critical_threshold = sla['query_latency_p95_ms']

    brief = f"""---
# Phase 3.9 Deployment Brief (v2 - Corrected Architecture)
# Practice: {practice_name}
# Tier: {tier}
# Generated: {datetime.now().isoformat()}
# Status: READY FOR DEPLOYMENT

## SLA Parameters for {practice_name}

| Parameter | Value | Tier {tier} |
|---|---|---|
| Query Latency p95 | {sla['query_latency_p95_ms']}ms | Target SLA |
| Query Latency p99 | {sla['query_latency_p99_ms']}ms | Target SLA |
| Ingestion Rate (min) | {sla['ingestion_rate_min_cps']} chunks/sec | Minimum |
| Coordination Latency p95 | {sla['coordination_latency_p95_s']}s | Target SLA |
| Health Score (min) | {sla['health_score_min']} | Minimum |
| Trace Correlation (min) | {sla['trace_correlation_min']} | Minimum |
| Escalation Response (L1) | {escalation['l1_minutes']}min | Warning alerts |
| Escalation Response (L2) | {escalation['l2_minutes']}min | Governance |
| Escalation Response (L3) | {escalation['l3_minutes']}min | Critical (Admiral) |

## Deployment Architecture

**This brief uses actual Phase 3.6-3.7 infrastructure:**
- Alert rules: JSON format (alerts defined in alert_rules.json)
- Alert evaluation: Prometheus/Loki metrics + Python conditions
- Escalation: Python classes (AlertEscalationOrchestrator, CortexEscalationProposer)
- Measurement gates: MeasurementGates (phase37_measurement_gates.py)

## Deployment Steps

### Step 1: Add Per-Practice Alert Rules to JSON

**File: analytics/alert_rules.json**

Add these 5 alert rules for {practice_name} (Tier {tier}):

```json
{{
  "id": "tier{tier}_{practice_name}_query_latency_warning",
  "name": "Tier {tier}: Query Latency Warning ({practice_name})",
  "description": "Query latency p95 approaching SLA ({p95_warning_threshold}ms)",
  "type": "query_latency",
  "severity": "warning",
  "metric": "loki_query_duration_seconds",
  "condition": {{
    "quantile": 0.95,
    "operator": ">",
    "threshold": {sla['query_latency_p95_ms'] / 1000.0},
    "duration": "5m"
  }},
  "scope": "per_practice",
  "practice_filter": "{practice_name}",
  "routing": "alert",
  "escalation_minutes": {escalation['l1_minutes']},
  "message_template": "🟡 WARNING: {{practice}} query latency p95 = {{current_value:.3f}}s (threshold: {sla['query_latency_p95_ms']}ms)"
}}
```

```json
{{
  "id": "tier{tier}_{practice_name}_query_latency_critical",
  "name": "Tier {tier}: Query Latency Critical ({practice_name})",
  "description": "Query latency p95 EXCEEDED SLA ({p95_critical_threshold}ms)",
  "type": "query_latency",
  "severity": "critical",
  "metric": "loki_query_duration_seconds",
  "condition": {{
    "quantile": 0.95,
    "operator": ">",
    "threshold": {sla['query_latency_p95_ms'] / 1000.0},
    "duration": "2m"
  }},
  "scope": "per_practice",
  "practice_filter": "{practice_name}",
  "routing": "escalation",
  "escalation_minutes": {escalation['l3_minutes']},
  "message_template": "🔴 CRITICAL: {{practice}} query latency p95 = {{current_value:.3f}}s - SLA EXCEEDED"
}}
```

```json
{{
  "id": "tier{tier}_{practice_name}_health_warning",
  "name": "Tier {tier}: Health Score Warning ({practice_name})",
  "description": "Health score approaching minimum ({sla['health_score_min']})",
  "type": "health_degradation",
  "severity": "warning",
  "metric": "empirica_practice_health_score",
  "condition": {{
    "operator": "<",
    "threshold": {sla['health_score_min'] + 0.05},
    "duration": "10m"
  }},
  "scope": "per_practice",
  "practice_filter": "{practice_name}",
  "routing": "alert",
  "escalation_minutes": {escalation['l1_minutes']},
  "message_template": "🟡 WARNING: {{practice}} health score = {{current_value:.2f}} (minimum: {sla['health_score_min']})"
}}
```

```json
{{
  "id": "tier{tier}_{practice_name}_health_critical",
  "name": "Tier {tier}: Health Score Critical ({practice_name})",
  "description": "Health score BELOW minimum ({sla['health_score_min']})",
  "type": "health_degradation",
  "severity": "critical",
  "metric": "empirica_practice_health_score",
  "condition": {{
    "operator": "<",
    "threshold": {sla['health_score_min']},
    "duration": "5m"
  }},
  "scope": "per_practice",
  "practice_filter": "{practice_name}",
  "routing": "escalation",
  "escalation_minutes": {escalation['l3_minutes']},
  "message_template": "🔴 CRITICAL: {{practice}} health CRITICAL - score {{current_value:.2f}}"
}}
```

```json
{{
  "id": "tier{tier}_{practice_name}_ingestion_low",
  "name": "Tier {tier}: Ingestion Rate Low ({practice_name})",
  "description": "Log ingestion rate below minimum",
  "type": "ingestion_rate",
  "severity": "warning",
  "metric": "loki_ingester_chunks_flushed_total",
  "condition": {{
    "operator": "<",
    "baseline_pct": 80,
    "duration": "10m"
  }},
  "scope": "per_practice",
  "practice_filter": "{practice_name}",
  "routing": "alert",
  "escalation_minutes": {escalation['l1_minutes']},
  "message_template": "🟡 WARNING: {{practice}} ingestion rate = {{current_value}}/s (minimum: {sla['ingestion_rate_min_cps']})"
}}
```

**Steps:**
- [ ] Edit analytics/alert_rules.json
- [ ] Paste the 5 JSON alert rule objects above into the "alert_rules" array
- [ ] Validate JSON syntax: `python3 -m json.tool analytics/alert_rules.json > /dev/null && echo "✅ Valid"`

### Step 2: Instantiate Rules via AlertEscalationOrchestrator

**File: phase36_orchestration.py (already exists)**

The orchestrator will:
1. Load alert_rules.json
2. Filter rules matching "practice_filter": "{practice_name}"
3. Evaluate conditions against live Prometheus/Loki metrics
4. Fire escalations when thresholds breached

**Execution:**
```bash
python3 phase36_orchestration.py
```

Expected output: Each alert rule evaluated, escalations routed to L1/L2/L3 per tier.

### Step 3: Bind Escalation Chain via CortexEscalationProposer

**File: analytics/cortex_escalation_proposer.py (already exists)**

Register escalation targets for {practice_name}:

```python
# In cortex_escalation_proposer.py, update:
self.practices["{practice_name}"] = "empirica-foundation.carly.{practice_name}"
```

The proposer will:
- Route L1 alerts to mesh-support (for diagnosis + coaching)
- Route L2 alerts to evaluator (for governance + routing)
- Route L3 critical alerts to admiral (final authority)

### Step 4: Activate Measurement Gate

**File: phase37_measurement_gates.py**

Add per-practice SLA gate for {practice_name}:

```python
# In _define_gates() method, add this MeasurementGate:
MeasurementGate(
  gate_id="sla_{practice_name}_tier{tier}",
  category="escalation",
  name="SLA Enforcement: {practice_name}",
  description="Tier {tier} SLA monitoring for {practice_name}",
  success_criteria=dict(query_p95_ms="{p95_critical_threshold}ms"),
  metric="query_latency_p95_ms",
  threshold={p95_critical_threshold},
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
- [ ] Verify gate in output: `sla_{practice_name}_tier{tier}: PENDING`

### Step 5: Smoke Test - Synthetic Alert Injection

**Purpose:** Verify end-to-end escalation chain

**Steps:**
```bash
# 1. Manually inject synthetic alert to Prometheus/Loki for {practice_name}
python3 << 'PYTEST'
import time
# Simulate alert: query_latency_p95 = 120% of SLA
synthetic_value = int({p95_critical_threshold} * 1.2)
# Write to metrics exporter / Prometheus push gateway
# (Requires local Prometheus setup; skip if not available)
PYTEST

# 2. Monitor escalation chain firing:
# - Watch analytics/escalation_proposals.json for "{practice_name}" entries
# - Verify L1 alert within {escalation['l1_minutes']}min
# - Verify L2 escalation within {escalation['l2_minutes']}min
# - Verify L3 critical within {escalation['l3_minutes']}min

# 3. Check mesh delivery:
cat analytics/mesh_outbox.json | grep -A5 "{practice_name}"

# 4. Clear synthetic alert:
# Remove synthetic value from Prometheus/Loki
```

## Completion Checklist

- [ ] Step 1: Alert rules added to alert_rules.json (5 rules for {practice_name})
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
   - L1: {escalation['l1_minutes']}min
   - L2: {escalation['l2_minutes']}min
   - L3: {escalation['l3_minutes']}min
5. ✅ Zero false positives in first 7 days

---

## Escalation Contacts

- **L1 (mesh-support):** Contact empirica-mesh-support SER
- **L2 (evaluator):** Contact empirica-foundation-evaluator (direct)
- **L3 (admiral):** Admiral.Leadership (critical authority, auto-escalated)

---

**Next:** Complete all checklist items, then report completion with evidence.
"""

    return brief


def main():
    briefs_dir = Path("phase39-deployment-briefs-v2")
    briefs_dir.mkdir(exist_ok=True)

    slas = sla_data["roster"]["slas"]
    total_practices = 0

    for practice_name, sla_params in slas.items():
        tier = TIER_MAPPING.get(practice_name)
        if not tier:
            print(f"⚠️  Warning: {practice_name} not in tier mapping", file=sys.stderr)
            continue

        brief = generate_brief(practice_name, sla_params, tier)
        brief_path = briefs_dir / f"{practice_name}_deployment_brief.md"

        with open(brief_path, "w") as f:
            f.write(brief)

        total_practices += 1
        print(f"✅ {practice_name} (Tier {tier})")

    print(f"\n📊 Summary: {total_practices}/17 deployment briefs generated (v2 - corrected architecture)")
    print(f"📁 Output: {briefs_dir.absolute()}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
