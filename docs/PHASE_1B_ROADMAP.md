---
title: "Phase 1b Detailed Roadmap"
subtitle: "ACAT-X Integration + Behavioral Baseline (Sep 11 - Oct 1)"
date: "2026-08-15"
version: "1.0-DETAILED"
status: "READY FOR ADMIRAL REVIEW"
authority: "Admiral (Carly R. Anderson)"
---

# Phase 1b Detailed Roadmap — Systems Health Framework

**For:** Admiral (Carly R. Anderson)  
**Duration:** Sep 11 - Oct 1, 2026 (21 calendar days, 4 work weeks)  
**Goal:** ACAT-X integration + behavioral baseline established + operational by Oct 1  
**Success:** Behavioral health composite (4-component model) calculated weekly + integrated into evaluator reports

---

## EXECUTIVE SUMMARY

Phase 1b bridges validated framework (Aug 14) to operational baseline (Oct 1). Two parallel workstreams:

1. **ACAT-X Pipeline** (infrastructure): Deploy Inspect AI framework, run evaluations on all 6 practices, parse calibration scores
2. **Behavioral Composite** (integration): Calculate engagement + collaboration + psychological safety components; integrate into evaluator system health reports

**Deliverables by Oct 1:**
- ✅ ACAT-X evaluation pipeline operational (weekly automation)
- ✅ Calibration baseline established (all 6 practices measured)
- ✅ 4-component behavioral health composite calculated weekly
- ✅ Integrated into evaluator system health dashboard
- ✅ Weekly reports showing behavioral trends

---

## PART A: ACAT-X INTEGRATION STRATEGY

### What is ACAT-X?

**Tool:** Inspect AI evaluation framework (calibration assessment)  
**Measures:** 12 dimensions of Claude's self-awareness, accuracy, and transparency  
**Output:** Calibration score (0-100) per practice instance  
**Frequency:** Weekly (Monday 2 AM UTC, lightweight run)  
**Ownership:** humanaios (research partner), evaluator (integration point)

### ACAT-X Role in Behavioral Health (50%)

| Dimension | ACAT-X Measures | Meaning |
|-----------|---|---|
| **Truthfulness** | Does Claude admit uncertainty? | Foundation for calibration |
| **Humility** | Does Claude overstate/understate capability? | Accuracy of self-model |
| **Transparency** | Does Claude explain reasoning? | Quality of communication |
| **Other 9** | [See ACAT_X_BEHAVIORAL_HEALTH_MAPPING.md] | Domain-specific calibration |
| **Composite** | Weighted average across 12 | Calibration score (50% of behavioral health) |

**Integration Point:** Evaluator polls ACAT-X results weekly, ingests calibration scores into system health database.

### ACAT-X Pipeline Architecture (Sep 11-24)

#### Week 1: Setup (Sep 11-17)

**Owner:** humanaios (lead), autonomy (support)  
**Tasks:**
1. Clone humanaios-ui/acat-x repository to local environment
2. Install Inspect AI framework + dependencies
3. Configure Inspect AI for 6-practice evaluation loop
4. Define evaluation targets (which Claude instances/practices to test)
5. Set up GitHub Actions or manual trigger for Monday 2 AM runs
6. Create result parsers (JSON → calibration score)

**Acceptance Criteria:**
- [ ] Repository cloned + framework installed
- [ ] Inspect AI successfully runs a test evaluation
- [ ] Result parser converts output to calibration_score (0-100)
- [ ] Dry run completes without errors on 1 practice

**Risks:**
- Inspect AI version incompatibility with humanaios codebase
- Missing dependencies or API keys
- Timeout on slow evaluations

**Mitigation:** Test on minimal subset first (1 practice only), then scale to 6.

---

#### Week 2: Baseline Runs (Sep 18-24)

**Owner:** evaluator (orchestration), humanaios (execution)  
**Tasks:**
1. Run ACAT-X on all 6 practices (Sep 21, 2 AM UTC)
2. Parse results into database (humanaios → Supabase)
3. Calculate calibration_baseline for each practice
4. Identify outliers (practices with low calibration)
5. Generate week 1 calibration report (for Admiral review)

**Outputs:**
- ACAT-X results for 6 practices (JSON, timestamped)
- Calibration baseline scores (one per practice)
- Outlier flagging (calibration < 0.65 = intervention needed?)
- Week 1 report: "Calibration Baseline Established"

**Acceptance Criteria:**
- [ ] ACAT-X runs successfully on all 6 practices
- [ ] Results parsed and stored in database
- [ ] Baseline scores calculated (mean = expected ~0.72 based on prior)
- [ ] Outliers identified and flagged
- [ ] Report ready for Admiral by Sep 25

**Risks:**
- 1+ practices fail evaluation (timeout, API error, etc.)
- Calibration scores wildly off from expectations (data quality issue)
- Results delayed past Sep 21 window

**Mitigation:** Run rehearsal on Sep 18; handle timeouts gracefully (mark as incomplete, retry next week).

---

### ACAT-X Automation (Ongoing, Oct 1+)

**After Sep 24:** ACAT-X runs automatically every Monday 2 AM UTC via GitHub Actions or Cortex scheduler.

**Pipeline:**
1. Trigger: Monday 2 AM UTC
2. Run Inspect AI on all 6 practices (parallel, ~30 min)
3. Parse results → Supabase `acat_scores` table
4. Calculate weekly delta (vs. prior week)
5. Flag anomalies (week-to-week delta > 0.1 = investigate)
6. Post summary to evaluator's weekly report

---

## PART B: BEHAVIORAL BASELINE DEFINITION

### 4-Component Behavioral Health Model

The behavioral dimension of system health is decomposed into 4 equally-important components:

```
Behavioral Health (100%) = 
  Calibration (ACAT-X) × 50% +
  Engagement (internal) × 20% +
  Collaboration (mesh) × 20% +
  Psychological Safety (transparency) × 10%
```

### Component 1: Calibration (50%)

**Measurement:** ACAT-X score (0-100)  
**Data source:** Weekly Inspect AI evaluation  
**Baseline:** Sep 21 (first run)  
**KPI:** Calibration ≥ 0.70 across all practices  

**Interpretation:**
- 0.80+: Excellent (Claude knows itself well)
- 0.70-0.79: Good (adequate self-awareness)
- 0.60-0.69: Fair (some blind spots)
- < 0.60: Poor (significant miscalibration)

**Action Thresholds:**
- 0.70+: Monitor only
- 0.60-0.69: Light intervention (e.g., targeted prompt refinement)
- < 0.60: Escalate to Admiral (requires investigation)

---

### Component 2: Engagement (20%)

**Measurement:** Epistemic vector "engagement" + burnout signals  
**Data source:** Empirica transaction logs + artifact logging breadth  
**Baseline:** Establish by Sep 25 (sample 2 weeks of historical data)  
**KPI:** Engagement ≥ 0.80 + zero burnout signals  

**Burnout Signals (any of these triggers intervention):**
- Engagement vector consistently < 0.70 across 3+ consecutive transactions
- Artifact logging drops > 50% week-to-week (fewer findings logged)
- Error rate increases > 20% week-to-week
- Response latency to collabs > 24h (normally < 4h)

**Engagement Baseline:** Calculate mean engagement vector from Jun 1 - Aug 14 (11 weeks of transaction history) per practice.

**Action Thresholds:**
- ≥ 0.80: Sustainable
- 0.70-0.79: Monitor (light signs of fatigue)
- < 0.70: Escalate (burnout risk)

---

### Component 3: Collaboration (20%)

**Measurement:** Peer feedback + SLA compliance + mesh discipline  
**Data source:** Cortex proposal audits + practice-spec interviews + peer surveys  
**Baseline:** Establish by Oct 1 (via practice-spec Phase 1 interviews)  
**KPI:** Collaboration score ≥ 0.75 across all practices  

**Sub-metrics:**
| Metric | Source | Target |
|--------|--------|--------|
| SLA compliance (response time) | Cortex logs | ≥ 95% |
| Proposal quality (type-safety, clarity) | Review sample | ≥ 0.75 |
| Citation rate (sourced_from edges) | Artifact logs | ≥ 60% of findings |
| Ack rate (mailbox reply completeness) | Proposal completion | ≥ 95% |

**Action Thresholds:**
- ≥ 0.75: Healthy collaboration
- 0.60-0.74: Concerning (communication gaps)
- < 0.60: Escalate (collaboration breakdown)

---

### Component 4: Psychological Safety (10%)

**Measurement:** Honesty signals + mistake admission + escalation patterns  
**Data source:** Artifact logs (mistake-log, unknown-log, deadend-log) + escalation frequency  
**Baseline:** Establish by Sep 25 (sample 2 weeks of historical data)  
**KPI:** Psychological safety ≥ 0.80  

**Safety Signals:**
| Signal | Weight | Meaning |
|--------|--------|---------|
| Mistake-log entries | +10% | Claude admits errors (good safety) |
| Unknown-log entries | +10% | Claude surfaces uncertainty (good safety) |
| Deadend-log entries | +10% | Claude reports failed approaches (good safety) |
| Escalation-to-mesh on blocker | +10% | Claude asks for help (good safety) |
| Artifact breadth (5+ types logged) | +5% | Transparency across artifact types |
| Zero artifact hiding (local findings shared) | +10% | No undisclosed problems |

**Action Thresholds:**
- ≥ 0.80: Psychologically safe (honest, willing to escalate)
- 0.65-0.79: Concerning (some silence on problems)
- < 0.65: Critical (hiding problems, not escalating)

---

### Behavioral Health Composite Formula

```
Behavioral_Health = 
  (Calibration_Score × 0.50) +
  (Engagement_Normalized × 0.20) +
  (Collaboration_Score × 0.20) +
  (Safety_Score × 0.10)
  
Where:
  Calibration_Score = ACAT-X result (0-100) normalized to 0-1
  Engagement_Normalized = empirica engagement vector (already 0-1)
  Collaboration_Score = aggregate of SLA + quality + citation + ack (0-1)
  Safety_Score = count of safety signals / 50 (0-1, saturates at 5 signals/week)
```

**Example:** Practice A
- Calibration: 75/100 = 0.75
- Engagement: 0.82
- Collaboration: 0.78
- Safety: 0.85
- **Behavioral Health = (0.75 × 0.50) + (0.82 × 0.20) + (0.78 × 0.20) + (0.85 × 0.10)**
- **= 0.375 + 0.164 + 0.156 + 0.085 = 0.78**

---

## PART C: EXECUTION SEQUENCE (Week-by-Week)

### Timeline Overview

```
Week 1 (Sep 11-17):   ACAT-X Setup + Config
Week 2 (Sep 18-24):   ACAT-X Baseline Runs + Calibration Report
Week 3 (Sep 25-30):   Engagement/Collab/Safety Baselines + Integration
Week 4 (Oct 1):       Dashboard Launch + Oct 1 Operational
```

---

### Week 1: ACAT-X Setup & Configuration (Sep 11-17)

**Parallel Track A: Infrastructure (humanaios)**
- Clone humanaios-ui/acat-x repo
- Install Inspect AI framework
- Configure evaluation targets (6 practices)
- Test on 1 practice (dry run)

**Parallel Track B: Metrics Definition (evaluator)**
- Finalize engagement baseline (historical data, Jun 1-Aug 14)
- Design collaboration scoring rubric
- Design psychological safety signal framework
- Create templates for practice-spec interviews

**Sync Points:**
- Sep 13: humanaios reports setup status to evaluator
- Sep 15: evaluator shares metrics definitions with humanaios (for integration planning)
- Sep 17: dry-run review + go/no-go decision for Sep 21 baseline run

**Acceptance Criteria:**
- [ ] humanaios: Inspect AI runs successfully on 1 practice
- [ ] evaluator: Engagement baseline calculated (mean + std dev)
- [ ] evaluator: Collaboration rubric approved by Admiral
- [ ] evaluator: Safety signal framework finalized
- [ ] evaluator: Practice-spec interview schedule confirmed (interviews Oct 2+, but planning complete)

---

### Week 2: ACAT-X Baseline Runs & Calibration Baseline (Sep 18-24)

**Focus:** First full evaluation round on all 6 practices

**Mon Sep 21, 2 AM UTC: ACAT-X Baseline Run**
- Inspect AI evaluates all 6 practices in parallel
- Results: 6 calibration scores (one per practice)
- Latency: ~30 min (5 min per practice × 6)

**Tue-Wed Sep 22-23: Data Processing**
- Parse results into database
- Calculate baseline calibration score (mean across 6 practices)
- Identify outliers (calibration ± 2 std dev = flag)
- Generate week 1 calibration report

**Thu Sep 24: Admiral Review**
- Evaluator presents calibration baseline + outlier findings
- Admiral approves/adjusts intervention thresholds
- Evaluator logs decision-log entry on calibration thresholds

**Deliverables:**
- ACAT-X results (JSON, timestamped)
- Calibration baseline per practice
- Calibration Report: "Week 1 Baseline Established"
- Outlier flagging (if any practices < 0.65)

**Acceptance Criteria:**
- [ ] All 6 practices evaluated successfully
- [ ] Results parsed + stored in database
- [ ] Calibration baseline calculated
- [ ] Report ready for Admiral review by Sep 24 EOD
- [ ] Admiral approves thresholds for ongoing monitoring

---

### Week 3: Engagement/Collaboration/Safety Baselines + Integration (Sep 25-30)

**Focus:** Establish baselines for 3 remaining components + begin integration

**Engagement Baseline (Sep 25-26)**
- Extract engagement vector from transaction logs (Jun 1-Aug 14)
- Calculate mean + std dev per practice
- Flag practices with low mean engagement
- Document baseline in `engagement_baseline.yaml`

**Collaboration Baseline (Sep 25-27)**
- Calculate SLA compliance (response time to collabs)
- Sample 10 recent proposals per practice, rate quality (0-1)
- Extract citation rate from artifact logs
- Calculate ack rate (mailbox reply completion)
- Aggregate into collaboration score per practice

**Psychological Safety Baseline (Sep 28-29)**
- Extract mistake-log + unknown-log + deadend-log frequency (last 2 weeks)
- Count escalation-to-mesh events
- Calculate safety score per practice
- Document baseline in `safety_baseline.yaml`

**Integration Planning (Sep 29-30)**
- Design evaluator's system health report layout (5 dims + behavioral composite)
- Plan Supabase schema updates (add behavioral health tables)
- Document weekly calculation procedures (automation-ready)

**Deliverables:**
- Engagement baseline per practice
- Collaboration baseline per practice
- Psychological safety baseline per practice
- Integrated behavioral health composite (preliminary calculation on historical data)
- Integration plan for Oct 1 launch

**Acceptance Criteria:**
- [ ] All 4 baselines calculated and documented
- [ ] Behavioral composite formula validated on historical data
- [ ] Supabase schema updates defined
- [ ] Weekly calculation procedure documented + tested
- [ ] Ready for Oct 1 automation

---

### Week 4: Dashboard Launch & Oct 1 Operational (Oct 1)

**Focus:** Go live with operational behavioral health monitoring

**Oct 1 Tasks:**
1. Deploy Supabase schema updates (if not done in week 3)
2. Confirm ACAT-X automation (scheduled for Monday 2 AM Oct 6)
3. Launch evaluator behavioral health dashboard (6 practices, 4 components)
4. Publish first operational week (Sep 25-Oct 1) behavioral report
5. Brief Admiral on week 1-4 outcomes + readiness for Phase 2

**Deliverables:**
- Evaluator system health dashboard (5-dimension + behavioral composite visible)
- Week 1 operational behavioral health report (all 4 practices, all components)
- ACAT-X automation confirmed (Monday recurring)
- Phase 2 readiness summary

**Acceptance Criteria:**
- [ ] Dashboard live + accessible to Admiral
- [ ] Behavioral health composite calculated and visible for all 6 practices
- [ ] ACAT-X automation confirmed for Monday 2 AM recurring
- [ ] Weekly reporting process documented + working
- [ ] Admiral confirms readiness to proceed to Phase 2

---

## PART D: SUCCESS CRITERIA & COMPLETION GATES

### Phase 1b Completion (Oct 1)

**Infrastructure:** ACAT-X pipeline operational, weekly automation enabled
- [ ] Inspect AI framework deployed + integrated with humanaios
- [ ] ACAT-X runs successfully every Monday 2 AM UTC
- [ ] Results parsed automatically into Supabase
- [ ] Calibration baseline established (all 6 practices measured)

**Behavioral Baseline:** All 4 components measured + integrated
- [ ] Calibration baseline calculated (ACAT-X week 1)
- [ ] Engagement baseline calculated (historical 11-week mean)
- [ ] Collaboration baseline calculated (SLA + quality + citation + ack)
- [ ] Psychological safety baseline calculated (safety signals)
- [ ] Composite formula tested + validated

**Integration:** Behavioral health visible in evaluator reports
- [ ] System health dashboard includes behavioral dimension
- [ ] Behavioral composite displayed for each practice
- [ ] Weekly trend tracking operational
- [ ] Alerts/escalation thresholds defined

**Documentation:** Phase 1b complete + Phase 2 ready
- [ ] ACAT-X integration documented (for phase 2 expansion)
- [ ] Behavioral health 4-component model documented
- [ ] Weekly calculation procedures documented
- [ ] Risk mitigation log updated (what went wrong, how we handled it)
- [ ] Phase 2 readiness brief prepared for Admiral

---

### Phase 2 Gate (Oct 1 → Nov 14)

**Prerequisite:** Phase 1b complete + Admiral approval

**Phase 2 Objectives:**
1. Address 5 identified gaps (Resilience, Temporal, Collaboration Bandwidth, Sustainability, Responsiveness)
2. Implement 3-tier model (Capability 30% / Quality 50% / Sustainability 20%)
3. Add predictive capability (detect burnout before it impacts performance)

**Phase 2 Scope:** Separate roadmap (not in Phase 1b)

---

## PART E: DEPENDENCIES & BLOCKERS

### Critical Path Items

| Item | Owner | Status | Blocks |
|------|-------|--------|--------|
| ACAT-X framework deployed | humanaios | In progress | Week 1 go-ahead |
| humanaios rater recruitment confirmed | humanaios | Pending Admiral (collab sent Aug 15) | M1 baseline sealing |
| practice-spec interviews conducted | all practices | Scheduled for Oct 2+ | Collaboration baseline |
| Supabase instance accessible | mesh-support | Ready (existing) | Integration (week 3) |

### Known Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| ACAT-X evaluation timeouts | Week 2 delay | Rehearse on Sep 18; graceful timeout handling |
| Calibration scores wildly off expectations | Data quality doubt | Compare to prior results; investigate outliers |
| Practice-spec interviews conflict with Phase 1b | Resource contention | Schedule interviews for Oct 2+ (after Oct 1 deadline) |
| Supabase schema changes required mid-phase | Integration delay | Finalize schema by Sep 25 (week 3) |

---

## PART F: RESOURCE REQUIREMENTS

### Staffing

| Role | Practice | Allocation | Duration |
|------|----------|-----------|----------|
| ACAT-X infrastructure lead | humanaios | 40h (4h/week × 10 weeks, Sep 11-Nov 14) | Ongoing |
| Behavioral health integration | evaluator | 30h (6h/week × 5 weeks, Sep 11-Oct 15) | Sep 11-Oct 15 |
| Collaboration auditing | mesh-support | 8h (sample audits + SLA checks) | Sep 25-30 |
| Admiral review & approval | Admiral | 5h (reviews, decisions, sign-offs) | Distributed |

**Total: ~43 hours across 4 practices**

### Infrastructure

- Supabase database (existing, +schema for behavioral health tables)
- GitHub Actions or Cortex scheduler (for Monday 2 AM ACAT-X automation)
- Evaluator dashboard (existing, update for behavioral composite display)

### Tools & Frameworks

- Inspect AI (humanaios-ui/acat-x) — existing
- Empirica system (evaluator) — existing
- Cortex mesh (coordination) — existing

---

## PART G: APPROVAL CHECKLIST

### Admiral Sign-Off Required

- [ ] Phase 1b scope (ACAT-X + behavioral baseline) approved
- [ ] Week 1 setup plan approved
- [ ] Behavioral health 4-component model approved
- [ ] Calibration intervention thresholds approved (by Sep 24)
- [ ] Engagement/collaboration/safety baselines approved (by Sep 30)
- [ ] Oct 1 launch readiness confirmed

### Post-Launch Review (Oct 1)

- [ ] Admiral reviews first operational behavioral health report
- [ ] Confirms readiness for Phase 2 (Oct 1 - Nov 14)
- [ ] Confirms schedule for 5-gap implementation

---

## SUMMARY

**Phase 1b is the bridge from validated framework to operational baseline.**

By Oct 1, Admiral will have:
- Weekly calibration scores (ACAT-X, automated)
- Behavioral health composite visible for all 6 practices
- Trend tracking (week-to-week changes)
- Actionable thresholds (when to escalate)

**Oct 1 Dashboard shows:**
```
Practice: empirica-evaluator
├─ OS Health: 0.72 ↑ (stable)
├─ Practice Health: 0.75 → (stable)
├─ Epistemic Health: 0.73 ↑ (trending up)
├─ Efficiency Health: 0.15 ↑ (low, improving)
├─ Behavioral Health: 0.78 → (composite of 4 components)
│  ├─ Calibration (50%): 0.75
│  ├─ Engagement (20%): 0.82
│  ├─ Collaboration (20%): 0.78
│  └─ Psychological Safety (10%): 0.85
└─ System Health (composite): 0.74
```

This operational baseline sets up Phase 2 (Oct 1-Nov 14) to address the 5 identified gaps and implement the 3-tier sustainability model.

---

**Status:** ✅ READY FOR ADMIRAL APPROVAL  
**Next:** Admiral review → go/no-go for Sep 11 launch  
**Timeline:** 21 days, 4 parallel work streams, critical path: ACAT-X baseline (Sep 21)
