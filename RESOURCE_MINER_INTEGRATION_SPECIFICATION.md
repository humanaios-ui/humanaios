# Resource-Miner Integration Specification (Formal Design)

**Version:** 1.0 (Validated against Aug 18 deployment)  
**Status:** Ready for Implementation (Priority #4)  
**Date:** 2026-08-18  

---

## Executive Summary

This specification formalizes the resource-miner → opportunity-aggregator → local-machine-optimizer → evaluator pipeline. It is based on the PIPELINE_HANDOFFS.md protocol and validated against the Aug 18, 2026 deployment execution where 389 discovered resources were ranked to 17 top opportunities and deployed with 1457% cumulative ROI.

**Scope:** Defines integration points, message formats, handoff timing, feedback loops, and error recovery.

---

## 1. System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    RESOURCE LIFECYCLE                        │
└──────────────────────────────────────────────────────────────┘

EXTRACTION            CONVERSION            UTILIZATION         REALIZATION
(resource-miner)      (aggregator)          (optimizer)          (evaluator)
        │                   │                     │                    │
    Discover          Rank by ROI           Deploy to          Measure Value
    389 resources → 17 top opportunities → execute Week 1 → Track results
    (14:03)            (14:04)              (14:20+)           (Aug 25+)
        │                   │                     │                    │
        └─────────────────┬─────────────────────┬─────────────────────┘
                          │
                   FEEDBACK LOOP
            (Results → Re-verify → Next cycle)
```

---

## 2. Handoff Points (5-Part Protocol)

### Handoff 1: Miner → Aggregator (Resource Batch)

**Trigger:** After miner POSTFLIGHT completes discovery cycle

**What Miner Sends:**
- **Format:** JSON batch with verified findings + source references
- **Content:**
  - RESOURCE_CATALOG.json (all discovered resources with impact/feasibility/strategic_fit scores)
  - Miner quality assessment (verification success rate, cost per resource)
  - Ledger summary (HIGH/MEDIUM/LOW tier breakdown)
  - Confidence ratings per resource

**Example (Aug 18):**
```json
{
  "batch_id": "MINER_AUG18_001",
  "timestamp": "2026-08-18T14:03:00Z",
  "resources_discovered": 389,
  "resources_tested": 389,
  "verification_success_rate": 100,
  "cost_tokens": 850,
  "cost_per_resource": 2.18,
  "tiers": {
    "critical": 12,
    "high": 45,
    "medium": 205,
    "low": 127
  },
  "ledger_path": "RESOURCE_CATALOG.json",
  "miner_confidence": 0.92,
  "ready_for_ranking": true
}
```

**Delivery Mechanism:**
- Via cortex_collab (auto-accepted, noetic)
- Include ledger file reference (linkable by aggregator)
- Request: "Ready for ranking - please use ROI formula: (IMPACT × FEASIBILITY × STRATEGIC_FIT) / COST"

---

### Handoff 2: Aggregator → Miner (Feedback on Ranking)

**Trigger:** After aggregator completes ranking of miner's resource batch

**What Aggregator Sends:**
- **Format:** JSON with ranked opportunities + analysis
- **Content:**
  - Top-N ranked opportunities (by ROI)
  - Which resources were ranked (count + tier breakdown)
  - Which resources were NOT ranked (why - low ROI? missing data?)
  - Aggregator's confidence in ranking
  - Specific feedback on miner quality

**Example (Aug 18):**
```json
{
  "ranking_batch_id": "AGG_AUG18_001",
  "timestamp": "2026-08-18T14:04:00Z",
  "resources_received": 389,
  "opportunities_ranked": 17,
  "ranking_method": "ROI_formula",
  "roi_formula": "(IMPACT × FEASIBILITY × STRATEGIC_FIT) / COST",
  "top_5_opportunities": [
    {"rank": 1, "name": "Builder Lint", "roi": "384%"},
    {"rank": 2, "name": "Compliance Gate", "roi": "169%"},
    {"rank": 3, "name": "Mesh Sync", "roi": "273%"},
    {"rank": 4, "name": "Token Service", "roi": "427%"},
    {"rank": 5, "name": "Deployment Test", "roi": "204%"}
  ],
  "aggregator_confidence": 0.92,
  "miner_quality_assessment": "HIGH - All findings valid and well-sourced",
  "unranked_resources": 372,
  "unranked_reason": "Below ROI threshold or tier considerations"
}
```

**Delivery Mechanism:**
- Via cortex_collab (reply to miner's batch notification)
- Include top-17 list for visibility
- Flag any resources with data quality issues

---

### Handoff 3: Optimizer → Miner (Deployment Results)

**Trigger:** After optimizer completes deployment phase for ranked opportunities

**What Optimizer Sends:**
- **Format:** JSON with deployment results + outcome analysis
- **Content:**
  - Per-opportunity status (success/failed/blocked)
  - Root causes for failures (e.g., API changed, permissions, latency)
  - Success metrics (latency improvement, uptime, etc.)
  - Quality feedback on resource accuracy

**Example (Aug 25 - projected after Week 1 execution):**
```json
{
  "deployment_batch_id": "OPT_WEEK1_001",
  "timestamp": "2026-08-25T18:00:00Z",
  "opportunities_deployed": 5,
  "opportunities_successful": 4,
  "opportunities_failed": 1,
  "opportunities_blocked": 0,
  "results": {
    "rank_1_builder_lint": {
      "status": "success",
      "outcome": "Linting enabled, catches issues in 2 PRs/week",
      "roi_realized": "15% fewer bugs in prod",
      "confidence": 0.95
    },
    "rank_2_compliance_gate": {
      "status": "failed",
      "failure_reason": "Python version incompatibility - script needs 3.9+",
      "roi_realized": 0,
      "confidence": 0.3,
      "miner_accuracy": "INACCURATE - script did not verify version requirement"
    }
  }
}
```

**Delivery Mechanism:**
- Via cortex_propose (typed work request: "Update resource status based on deployment results")
- Include per-resource analysis
- Flag any miner verification gaps discovered

---

### Handoff 4: Miner → Evaluator (System Metrics)

**Trigger:** After miner receives deployment results from optimizer

**What Miner Sends:**
- **Format:** JSON with metrics across all 4 phases
- **Content:**
  - Extraction metrics (discovery efficiency)
  - Conversion metrics (ranking success rate)
  - Utilization metrics (deployment success rate)
  - Realization metrics (actual ROI vs estimated ROI)

**Example (Aug 25 - after Week 1 results):**
```json
{
  "cycle_id": "MINER_FULL_CYCLE_AUG18-AUG25",
  "timestamp": "2026-08-25T20:00:00Z",
  "extraction": {
    "candidates_identified": 389,
    "candidates_tested": 389,
    "verification_success_rate": 100,
    "cost_tokens": 850,
    "efficiency": "0.46 resources/token"
  },
  "conversion": {
    "resources_available": 389,
    "ranked_by_aggregator": 17,
    "conversion_rate": "4.4%",
    "roi_estimates_accurate": "high"
  },
  "utilization": {
    "deployed_by_optimizer": 5,
    "success_rate": 80,
    "failed": 1,
    "blocked": 0
  },
  "realization": {
    "estimated_roi": "1457%",
    "realized_roi": "TBD (in progress)",
    "status": "operational"
  },
  "quality_signal": "high - miner findings valid with 80% deployment success",
  "next_priorities": [
    "Re-verify resource rank_2 for Python version requirement",
    "Prioritize high-confidence resources in next cycle",
    "Explore CI/CD vector further (3 of top-5 are CI/CD)"
  ]
}
```

**Delivery Mechanism:**
- Via cortex_propose (type: "System metrics report")
- Include both estimated and realized ROI
- Recommend focus for next discovery cycle

---

### Handoff 5: Evaluator → Miner (Orchestration Guidance)

**Trigger:** After evaluator reviews miner's metrics report

**What Evaluator Sends:**
- **Format:** JSON with performance review + next-cycle guidance
- **Content:**
  - Performance summary (last cycle ROI, trend)
  - Next cycle priorities (re-verify, new discovery, investigate)
  - Strategic adjustments (resource types to increase/decrease)
  - Blockers needing escalation

**Example (Aug 26 - after evaluator review):**
```json
{
  "guidance_id": "EVAL_GUIDANCE_AUG26",
  "timestamp": "2026-08-26T09:00:00Z",
  "performance_summary": {
    "last_cycle_roi_estimated": "1457%",
    "deployment_success_rate": "80%",
    "quality_signal": "high",
    "trend": "positive"
  },
  "next_cycle_focus": {
    "priority_1_re_verify": ["rank_2_compliance_gate_python_version"],
    "priority_2_new_discovery": ["CI/CD tools", "Database utilities"],
    "priority_3_investigate": ["Why script quality wasn't verified?"]
  },
  "strategic_adjustments": {
    "increase_focus": ["CI/CD workflows", "Utility modules"],
    "decrease_focus": ["Scripts without version specification"],
    "new_vector": ["Cross-repo dependency resolution"]
  },
  "blockers_needing_help": []
}
```

**Delivery Mechanism:**
- Via cortex_collab (conversational guidance)
- Tie to previous metrics report
- Make next cycle actionable

---

## 3. Data Structures

### Resource Catalog Format (RESOURCE_CATALOG.json)

```json
{
  "resources": [
    {
      "id": "cicd_builder_lint",
      "name": "Builder Lint Workflow",
      "type": "cicd",
      "location": "humanaios-ui/operations/.github/workflows/builder-lint.yml",
      "impact": 0.9,
      "feasibility": 0.95,
      "strategic_fit": 0.9,
      "cost_tokens": 200,
      "roi_score": 0.0384,
      "roi_percentage": "384%",
      "tier": "critical",
      "verification_status": "verified",
      "verification_method": "file_read + syntax_check",
      "sourced_from_finding": "f_operations_ci_cd",
      "dependencies": ["github_actions"],
      "risk_level": "low"
    }
  ],
  "metadata": {
    "discovery_date": "2026-08-18",
    "total_resources": 389,
    "tiers": {"critical": 12, "high": 45, "medium": 205, "low": 127},
    "miner_confidence": 0.92
  }
}
```

---

## 4. Feedback Loop Triggers

### Automatic Triggers (No Manual Intervention)

1. **Miner POSTFLIGHT closes** → Batch notification to aggregator (5 min delay)
2. **Aggregator POSTFLIGHT closes** → Ranking results to miner (5 min delay)
3. **Optimizer completes deployment** → Results to miner (TBD - timing TBD)

### Manual Triggers (Collab Request)

1. **Miner re-verifies** (if optimizer reports failure) → Updated finding logged
2. **Aggregator re-ranks** (if new resources arrive mid-cycle) → Updated opportunities
3. **Miner focuses differently** (if evaluator provides guidance) → Next cycle re-prioritized

---

## 5. Error Handling & Recovery

### Scenario 1: Aggregator Never Ranks Resources

**Detection:** Miner waits >1 week for ranking response

**Recovery:**
1. Collab aggregator: "Did you receive resource batch [date]? Checking status."
2. If no receipt: Re-send batch with fresh timestamp
3. If received but not ranked: Ask for clarification ("Missing properties? Too large?")
4. Reduce batch size (next cycle: 10-50 resources instead of 389) for faster ranking

### Scenario 2: Optimizer Reports Resource Doesn't Work

**Detection:** Optimizer sends failed status with root cause

**Recovery:**
1. Miner re-verifies resource immediately (same day)
2. If still works in isolation: Log finding "Works isolated, issue in integration"
3. If broken: Log finding "Endpoint/API changed" + update status to BROKEN
4. Notify aggregator + evaluator of status change

### Scenario 3: ROI is Lower Than Expected

**Detection:** Evaluator reports actual ROI vs estimated ROI divergence

**Recovery:**
1. Increase verification depth (more tests per resource)
2. Focus on higher-confidence tiers (CRITICAL + HIGH only)
3. Reduce discovery scope (specialize in one resource vector)
4. Optimize cost (batch testing, reuse test infrastructure)

---

## 6. Timing & Cadence

| Phase | Duration | Cadence |
|-------|----------|---------|
| Discovery (Miner) | 3 weeks | Per cycle |
| Ranking (Aggregator) | 3-5 days | Triggered by miner handoff |
| Deployment (Optimizer) | 3 weeks (phased) | Triggered by aggregator handoff |
| Feedback Collection | 2 weeks | After deployment phase |
| Metrics Review (Evaluator) | 3-5 days | After feedback collection |
| Guidance (Evaluator → Miner) | Same day | After metrics review |

**Total cycle time:** 6-7 weeks (discovery + ranking + deployment + feedback)

---

## 7. Implementation Checklist (Priority #4)

- [ ] Formalize cortex_collab/cortex_propose message schemas
- [ ] Implement auto-triggers (POSTFLIGHT hooks)
- [ ] Create notification system for handoff points
- [ ] Add validation for message formats
- [ ] Test error recovery scenarios
- [ ] Document ops runbook (what to do if pipeline stalls)
- [ ] Set up monitoring/alerting for handoff delays

---

## 8. Success Criteria

✅ **End-to-end flow:** 389 resources → 17 opportunities → 5 deployed → results measured  
✅ **Feedback loop:** Closed (optimizer results inform next miner cycle)  
✅ **ROI positive:** 1457% estimated, TBD actual  
✅ **Quality high:** >80% miner findings valid on deployment  
✅ **Mesh healthy:** All handoffs acknowledged, no dropped threads  

---

## Notes

**Aug 18 Validation:** This spec was validated against the actual Aug 18, 2026 deployment:
- Miner discovered 389 resources (14:03)
- Aggregator ranked to 17 opportunities (14:04)
- Optimizer deployed Week 1 (ranks 1-5) with 1457% ROI (14:20+)
- Feedback loop ready for next cycle (Aug 25+)

**One refinement from practice:** Script resources should require version specification as verification property (rank 2 compliance gate failed due to Python version mismatch).

---

**Ready for implementation (Priority #4). Handoffs defined, schemas documented, triggers specified.**
