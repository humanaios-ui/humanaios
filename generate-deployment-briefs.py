#!/usr/bin/env python3
"""
Phase 3.9: Deployment Brief Generator
Generates per-practice deployment briefs for SLA enforcement + alert rule instantiation
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
    # Tier 1 (4 practices)
    "empirica-autonomy": 1,
    "empirica-mesh-support": 1,
    "empirica-foundation-evaluator": 1,
    "empirica-outreach": 1,
    # Tier 2 (5 practices)
    "empirica-analytics": 2,
    "empirica-resource-miner": 2,
    "empirica-temporal-oracle": 2,
    "humanaios": 2,
    "humanaios-ui": 2,
    # Tier 3 (8 practices)
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
    1: {"response_l1": 5, "response_l2": 5, "response_l3": 2},
    2: {"response_l1": 10, "response_l2": 10, "response_l3": 5},
    3: {"response_l1": 15, "response_l2": 15, "response_l3": 10},
}

def generate_brief(practice_name: str, sla: dict, tier: int) -> str:
    """Generate deployment brief for a single practice"""
    
    escalation = TIER_ESCALATION[tier]
    
    brief = f"""---
# Phase 3.9 Deployment Brief
# Practice: {practice_name}
# Tier: {tier}
# Generated: {datetime.now().isoformat()}
# Status: READY FOR DEPLOYMENT

## SLA Parameters for {practice_name}

| Parameter | Value | SLA Tier |
|---|---|---|
| Query Latency p95 | {sla['query_latency_p95_ms']}ms | {tier} |
| Query Latency p99 | {sla['query_latency_p99_ms']}ms | {tier} |
| Ingestion Rate (min) | {sla['ingestion_rate_min_cps']} chunks/sec | {tier} |
| Coordination Latency p95 | {sla['coordination_latency_p95_s']}s | {tier} |
| Health Score (min) | {sla['health_score_min']} | {tier} |
| Trace Correlation (min) | {sla['trace_correlation_min']} | {tier} |
| Escalation Response | {sla['escalation_response_minutes']}min | {tier} |
| Critical Response | {sla['critical_response_minutes']}min | {tier} |

## Alert Rules to Deploy

### From alert-rules-tier{tier}.yaml

**Warning Alerts (escalation: {escalation['response_l1']}min):**
- Query Latency p95 approaching ({int(sla['query_latency_p95_ms'] * 0.8)}ms)
- Health Score warning ({sla['health_score_min'] + 0.05:.2f})
- Ingestion rate low ({sla['ingestion_rate_min_cps']} chunks/sec)
- Trace correlation low ({sla['trace_correlation_min']})
- Coordination latency high ({sla['coordination_latency_p95_s']}s)

**Critical Alerts (escalation: {escalation['response_l3']}min):**
- Query Latency p95 EXCEEDED ({sla['query_latency_p95_ms']}ms)
- Health Score BELOW minimum ({sla['health_score_min']})

## Deployment Steps

### 1. Validate Alert Rules (mesh-support)
```
Step 1a: Load alert-rules-tier{tier}.yaml
Step 1b: Replace practice-specific threshold values:
  - PRACTICE_P95_MS = {sla['query_latency_p95_ms']}
  - PRACTICE_MIN_CPS = {sla['ingestion_rate_min_cps']}
  - PRACTICE_COORD_P95_S = {sla['coordination_latency_p95_s']}
Step 1c: Validate syntax: `alert-validator validate <config.yaml>`
Step 1d: Dry-run: `alert-deployer dry-run {practice_name} <config.yaml>`
```

### 2. Instantiate Alert Rules for {practice_name}
```
Step 2a: Apply rules: `alert-deployer apply {practice_name} <config.yaml>`
Step 2b: Verify active: `alert-check status {practice_name} --all-rules`
Step 2c: Log: alert rule count deployed = N
```

### 3. Bind Escalation Protocol
```
L1 (mesh-support):
  - Response time: {escalation['response_l1']}min
  - Action: diagnose + attempt resolution
  - Escalate if unresolved → L2

L2 (evaluator):
  - Response time: {escalation['response_l2']}min
  - Action: governance decision + routing
  - Escalate if critical → L3

L3 (admiral):
  - Response time: {escalation['response_l3']}min (critical only)
  - Action: final authority + broadcast
```

Step 3a: Register escalation chain in Cortex:
  `cortex escalation-bind {practice_name} tier{tier} L1:mesh-support L2:evaluator L3:admiral`

### 4. Activate Measurement Gates
```
Step 4a: Enable SLA monitoring: `sla-monitor enable {practice_name}`
Step 4b: Set alert thresholds:
  - p95_warning: {int(sla['query_latency_p95_ms'] * 0.8)}ms
  - p95_critical: {sla['query_latency_p95_ms']}ms
  - health_warning: {sla['health_score_min'] + 0.05:.2f}
  - health_critical: {sla['health_score_min']}
Step 4c: Activate: `sla-monitor activate {practice_name}`
Step 4d: Verify: `sla-monitor status {practice_name}` → should show ACTIVE
```

### 5. Smoke Test (Deploy Pipeline)
```
Step 5a: Generate synthetic alert: `alert-inject {practice_name} query_latency=CRITICAL`
Step 5b: Verify escalation chain fires:
  - L1 notified within {escalation['response_l1']}min ✓
  - L2 paged within {escalation['response_l2']}min ✓
Step 5c: Log: synthetic alert test passed / failed
Step 5d: Clear synthetic alert: `alert-clear {practice_name} synthetic`
```

## Completion Checklist

- [ ] Alert rules syntax validated
- [ ] Rules deployed to {practice_name}
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

1. ✅ Alert rules deployed and active for {practice_name}
2. ✅ Escalation chain functional (L1 → L2 → L3)
3. ✅ Measurement gates reporting SLA violations
4. ✅ Zero escalation response time SLA violations (first 7 days)

---
**Generated:** Phase 3.9 Automation
**Next:** Proceed with step 1 (validation) and acknowledge completion
"""
    
    return brief


def main():
    briefs_dir = Path("phase39-deployment-briefs")
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
    
    print(f"\n📊 Summary: {total_practices}/17 deployment briefs generated")
    print(f"📁 Output: {briefs_dir.absolute()}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
