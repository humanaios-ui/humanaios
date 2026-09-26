# Phase 3.9 Tier 1 Deployment Plan

**Status:** READY FOR DISTRIBUTION (Sep 17 EOD)
**Target Practices:** 4 (empirica-autonomy, empirica-mesh-support, empirica-foundation-evaluator, empirica-outreach)
**Deployment Window:** Sep 17 EOD → Sep 18 morning (12-16 hours)
**Escalation SLAs:** Tier 1 practices have strictest SLAs (2-5min response)

## Tier 1 Practices Roster

| Practice | p95 SLA | Health Min | Critical Response | Brief Location |
|---|---|---|---|---|
| **empirica-autonomy** | 1000ms | 0.75 | 2 min | phase39-deployment-briefs-v2/empirica-autonomy_deployment_brief.md |
| **empirica-mesh-support** | 1500ms | 0.70 | 5 min | phase39-deployment-briefs-v2/empirica-mesh-support_deployment_brief.md |
| **empirica-foundation-evaluator** | 1200ms | 0.75 | 2 min | phase39-deployment-briefs-v2/empirica-foundation-evaluator_deployment_brief.md |
| **empirica-outreach** | 2000ms | 0.70 | 10 min | phase39-deployment-briefs-v2/empirica-outreach_deployment_brief.md |

## Deployment Steps (Per Practice)

### Each Brief Includes:

1. **Step 1: Add JSON Alert Rules** (5 rules per practice)
   - Query latency warning (80% of SLA)
   - Query latency critical (100% of SLA)
   - Health score warning (5% below minimum)
   - Health score critical (at minimum)
   - Ingestion rate low (80% of minimum)
   - **Action:** Edit `analytics/alert_rules.json`, paste JSON rule objects, validate syntax

2. **Step 2: Instantiate via AlertEscalationOrchestrator**
   - Run: `python3 phase36_orchestration.py`
   - Verify: Rules load and conditions evaluate against live Prometheus/Loki metrics

3. **Step 3: Bind Escalation Chain**
   - Update `cortex_escalation_proposer.py` with practice name
   - Verify: L1/L2/L3 routing configured

4. **Step 4: Activate Measurement Gate**
   - Add per-practice gate to `phase37_measurement_gates.py`
   - Run: `python3 phase37_measurement_gates.py`
   - Verify: Gate shows PENDING → PASS (once metrics flow)

5. **Step 5: Smoke Test**
   - Inject synthetic alert for {practice}
   - Verify escalation chain fires within SLA
   - Verify L1 alert within {l1_minutes}min
   - Verify L2 escalation within {l2_minutes}min
   - Verify L3 critical within {l3_minutes}min
   - Clear synthetic alert

## Completion Checklist (Per Practice)

- [ ] Brief received and reviewed
- [ ] Step 1: Alert rules added to alert_rules.json (5 rules)
- [ ] Step 1: JSON syntax validated
- [ ] Step 2: AlertEscalationOrchestrator executed
- [ ] Step 3: Escalation targets registered
- [ ] Step 4: MeasurementGate added and verified
- [ ] Step 5: Smoke test executed
- [ ] Step 5: Escalation SLA met (response times within targets)
- [ ] **COMPLETE:** Evidence logged (files, test output)

## Timeline

**Sep 17 EOD:** Issue briefs to all 4 Tier 1 practices (simultaneous)

**Sep 17-18:** Practices execute deployments (4-hour window per practice)
- empirica-autonomy: Sep 17-18 morning
- empirica-mesh-support: Sep 17-18 morning (parallel with autonomy)
- empirica-foundation-evaluator: Sep 17-18 morning (parallel)
- empirica-outreach: Sep 17-18 morning (parallel)

**Sep 18 EOD:** Verification of Tier 1 deployment completion
- Confirm all 4 practices report: Alert rules active, measurement gates PASS, escalation chain responsive
- Log completion evidence per practice
- Prepare for Tier 2 briefing (5 practices)

**Sep 18 evening:** Issue briefs to Tier 2 (5 practices)

## Success Criteria

1. ✅ All 4 practices receive briefs
2. ✅ Each practice completes 5-step deployment pipeline
3. ✅ Alert rules instantiated and evaluating metrics
4. ✅ Measurement gates report SLA status
5. ✅ Escalation chain fires on synthetic alerts
6. ✅ Escalation response times within Tier 1 SLAs:
   - L1: 5 min (warning alerts)
   - L2: 5 min (governance escalation)
   - L3: 2 min (critical escalation)
7. ✅ Zero false positives in first 7 days of monitoring

## Escalation Contacts (Tier 1)

**If practices encounter issues:**
- **L1 Support:** empirica-mesh-support (4h response SLA)
- **L2 Decision:** empirica-foundation-evaluator (2-5min response SLA)
- **L3 Critical:** Admiral.Leadership (immediate, 2min SLA)

---

**Next:** Distribute briefs to 4 Tier 1 practices simultaneously. All 4 should be able to deploy in parallel (4-hour window, but staggered across Sep 17-18).
