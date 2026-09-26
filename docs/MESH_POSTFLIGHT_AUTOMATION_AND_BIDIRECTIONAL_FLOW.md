---
title: "Mesh POSTFLIGHT Automation & Bidirectional Flow"
subtitle: "Integrate automated loops with existing .postflight/ infrastructure"
date: "2026-08-15"
version: "1.1-INTEGRATED"
status: "DESIGN COMPLETE"
authority: "Admiral (Carly R. Anderson), evaluator practice"
integration_base: "7 sessions in INDEX.yaml, 13 practices in MESH_STATE_2026_08_15.md (existing)"
---

# Mesh POSTFLIGHT Automation & Bidirectional Flow — Integrated with Existing Infrastructure

**What's Already Built:**
- `.postflight/INDEX.yaml` — aggregates 7 sessions, 6 practices, tracks mesh-wide vectors + decisions
- `.postflight/MESH_STATE_2026_08_15.md` — captures all 13 practices' POSTFLIGHT data + blockers + critical path
- Manual collection works but not automated
- No bidirectional feedback loops yet

**This Design Adds:**
1. **Automated inbound:** Hook into Cortex event stream to pull POSTFLIGHT data hourly from all 13 practices
2. **Auto-update INDEX.yaml:** Hourly refresh with new sessions, vector trends, blocker cascade analysis
3. **Anomaly detection:** Real-time alerts when vectors drop, response times spike, blockers cascade
4. **Bidirectional feedback:** Alerts → practice response → data updates → system re-evaluates
5. **Closed-loop validation:** Measure if alerts led to corrections within 4 hours (warning threshold) or 24 hours (info threshold)

---

## PART A: Automation Layer (Inbound) — Built on Cortex Event Stream

### 1. Automated Ingestion (Evaluator Pulls POSTFLIGHT Data via Cortex)

**What's Different:** Instead of each practice emitting, evaluator PULLS POSTFLIGHT snapshots via Cortex mailbox polling (the same hourly `cortex-mailbox-poll` loop already running for mesh coordination).

**Existing:** Cortex mailbox-poll fires every 30s-5m (adaptive cadence) and wakes the evaluator on collab/proposal events.

**Extend:** Add a parallel hourly `mesh-postflight-ingest` loop that:
1. Polls Cortex inbox for POSTFLIGHT-tagged summaries from each practice (or queries empirica project-search if available)
2. Parses latest vectors + goal counts + response times
3. Stores in `.postflight/sessions/<practice>/<YYYY-MM-DD-HHmmss>.json`
4. Updates INDEX.yaml in-place (append new session, recalculate trends)

**What gets emitted (standardized schema):**

```json
{
  "timestamp": "2026-08-15T14:30:00Z",
  "practice_id": "empirica-foundation.carly.humanaios",
  "session_id": "...",
  "transaction_id": "...",
  
  "vectors": {
    "know": 0.85,
    "uncertainty": 0.15,
    "engagement": 0.92,
    "completion": 0.87,
    ... // all 13 vectors
  },
  
  "goals": {
    "total": 12,
    "completed": 5,
    "in_progress": 6,
    "planned": 1,
    "blockers": ["wisdom_engine_spec"]
  },
  
  "mesh_metrics": {
    "inbox_items": 8,
    "avg_response_time_hours": 18,
    "collabs_responded": 6,
    "sla_compliance_pct": 95,
    "mesh_health": "GOOD"
  },
  
  "calibration": {
    "belief_variance": 0.08,
    "accuracy_on_predictions": 0.94,
    "confidence": 0.91
  },
  
  "critical_items": [
    {"type": "blocker", "title": "wisdom_engine_spec", "days_overdue": 22},
    {"type": "decision_due", "title": "Phase 2 Strategy", "days_until": 13}
  ]
}
```

### 2. Canonical Mesh Ingestion Loop (Hourly)

**Register the loop in evaluator's project.yaml:**

```bash
empirica loop register --name mesh-postflight-ingest --kind interval \
  --interval 1h \
  --description "Poll POSTFLIGHT from 13 practices, update INDEX.yaml, detect anomalies"
```

**Loop body (Python pseudocode):**

```python
# Run hourly: pull latest POSTFLIGHT from all 13 practices

practices = [
  "empirica-foundation.carly.empirica-foundation-evaluator",
  "empirica-foundation.carly.empirica-autonomy",
  "empirica-foundation.carly.empirica-mesh-support",
  "empirica-foundation.carly.humanaios",
  # ... (all 13)
]

new_sessions = []
anomalies_detected = []

for practice_id in practices:
  # 1. Try empirica project-search first (fastest, already in empirica)
  result = subprocess.run([
    "empirica", "project-search",
    "--project-id", practice_id,
    "--task", "latest POSTFLIGHT",
    "--output", "json"
  ], capture_output=True)
  
  latest_postflight = json.loads(result.stdout)
  
  # If no result, fall back to cortex_inbox_poll
  if not latest_postflight:
    # cortex_inbox_poll already running; just check for POSTFLIGHT-tagged messages
    # (implementation detail: practices tag POSTFLIGHT summaries in Cortex)
    pass
  
  # 2. Parse into standardized format (matching current INDEX.yaml schema)
  session = {
    "timestamp": latest_postflight.timestamp,
    "practice_id": practice_id,
    "vectors": latest_postflight.vectors,  # all 13
    "goals": latest_postflight.goals,
    "mesh_metrics": {
      "response_time_hours": latest_postflight.avg_response_time,
      "sla_compliance_pct": latest_postflight.sla_compliance
    },
    "calibration": latest_postflight.calibration
  }
  
  # 3. Store locally (git-tracked .postflight/sessions/<practice>/...)
  session_dir = f".postflight/sessions/{practice_id}"
  os.makedirs(session_dir, exist_ok=True)
  
  timestamp_str = session["timestamp"].strftime("%Y-%m-%d-%H%M%S")
  with open(f"{session_dir}/{timestamp_str}.json", "w") as f:
    json.dump(session, f)
  
  new_sessions.append(session)
  
  # 4. Compare to prior session (detect deltas)
  prior_sessions = sorted(glob(f"{session_dir}/*.json"))[-2:]  # last 2
  if len(prior_sessions) >= 2:
    prior = json.load(open(prior_sessions[-2]))
    delta = compute_delta(prior, session)
    
    if delta.anomaly_score > 0.7:
      anomalies_detected.append({
        "practice": practice_id,
        "type": delta.anomaly_type,
        "severity": delta.severity,
        "timestamp": now()
      })

# 5. Update INDEX.yaml in-place
index = yaml.safe_load(open(".postflight/INDEX.yaml"))

# Append new sessions, recalculate mesh-wide vectors
index["summary"]["total_sessions"] += len(new_sessions)
index["summary"]["last_updated"] = now().isoformat()

# Recalculate vector trends (append latest per practice)
for practice_sessions in new_sessions:
  practice_id = practice_sessions["practice_id"]
  for dim in ["know", "uncertainty", "engagement", ...]:
    if dim not in index["vector_trends"]:
      index["vector_trends"][dim] = {"values": []}
    index["vector_trends"][dim]["values"].append(practice_sessions["vectors"][dim])

# Recompute trends (moving average, direction)
for dim, trend_data in index["vector_trends"].items():
  values = trend_data["values"][-24:]  # last 24 hours
  trend_data["trend_direction"] = "INCREASING" if values[-1] > values[0] else "DECREASING"
  trend_data["last_value"] = values[-1]

yaml.dump(index, open(".postflight/INDEX.yaml", "w"))

# 6. Flag anomalies for outbound processing
if anomalies_detected:
  log_finding(f"Anomalies detected: {len(anomalies_detected)}")
  # (Outbound step picks these up — see PART B below)
```

### 3. Master Index Auto-Update

**After each hourly ingestion:**

```bash
# Step 1: Query Supabase for latest practice data (all 13)
latest_by_practice = supabase.query("""
  SELECT practice_id, vectors, goals, mesh_metrics, timestamp
  FROM mesh_telemetry
  WHERE timestamp > now() - INTERVAL 24h
  ORDER BY timestamp DESC
  DISTINCT ON (practice_id)
""")

# Step 2: Compute mesh-wide aggregates
mesh_wide_vectors = {
  "know": mean([p.vectors.know for p in latest_by_practice]),
  "uncertainty": mean([p.vectors.uncertainty for p in latest_by_practice]),
  ...
}

vector_trends = {
  "know": compute_trend([hourly_know_values_last_7days]),
  "uncertainty": compute_trend([hourly_uncertainty_values_last_7days]),
  ...
}

# Step 3: Compute per-practice health ratings
practice_health = {}
for practice in latest_by_practice:
  health_score = weighted_average([
    practice.vectors.know * 0.25,
    (1 - practice.vectors.uncertainty) * 0.25,
    practice.vectors.engagement * 0.25,
    practice.vectors.completion * 0.25
  ])
  
  if health_score >= 0.85:
    status = "EXCELLENT"
  elif health_score >= 0.70:
    status = "GOOD"
  elif health_score >= 0.50:
    status = "NEEDS_ATTENTION"
  else:
    status = "CRITICAL"
  
  practice_health[practice.id] = {
    score: health_score,
    status: status,
    response_time: practice.mesh_metrics.avg_response_time_hours,
    sla_compliance: practice.mesh_metrics.sla_compliance_pct
  }

# Step 4: Update .postflight/INDEX.yaml
INDEX = {
  version: "1.0-mesh",
  last_updated: now,
  summary: {
    total_practices: 13,
    total_sessions: len(latest_by_practice),
    mesh_wide_vectors: mesh_wide_vectors,
    vector_trends: vector_trends,
    practice_health: practice_health
  }
}

write_yaml(".postflight/INDEX.yaml", INDEX)
```

---

## PART B: Analysis Layer (Anomaly Detection & Insights)

### 1. Anomaly Detection (Real-Time)

**Anomaly types detected automatically:**

```python
class AnomalyDetector:
  
  def detect(self, prior, current, practice):
    anomalies = []
    
    # Anomaly 1: Response time surge
    if current.mesh_metrics.response_time > prior.response_time + 20:
      anomalies.append({
        type: "response_time_surge",
        severity: "warning" if delta < 30 else "critical",
        message: f"{practice} response time {delta}h increase",
        auto_action: "escalate_if_critical"
      })
    
    # Anomaly 2: Burnout signal (engagement drop + completion drop)
    if (current.vectors.engagement < 0.65 and 
        current.vectors.completion < prior.completion - 0.15):
      anomalies.append({
        type: "burnout_signal",
        severity: "warning",
        message: f"{practice} showing burnout signals",
        auto_action: "surface_to_admiral"
      })
    
    # Anomaly 3: Blocker cascade (1 blocker → affects 3+ practices)
    if len(current.goals.blockers) > 0:
      affected_count = count_practices_affected_by(current.goals.blockers)
      if affected_count >= 3:
        anomalies.append({
          type: "blocker_cascade",
          severity: "critical",
          message: f"Blocker affects {affected_count} practices",
          auto_action: "escalate_immediately"
        })
    
    # Anomaly 4: Stalled proposal (no reply in 24h)
    if has_stalled_proposals(practice):
      anomalies.append({
        type: "stalled_proposal",
        severity: "warning",
        message: f"{practice} has stalled proposals",
        auto_action: "send_reminder_collab"
      })
    
    # Anomaly 5: Decision deadline approaching (< 3 days)
    for decision in current.critical_items:
      if decision.type == "decision_due" and decision.days_until < 3:
        anomalies.append({
          type: "decision_deadline_imminent",
          severity: "warning",
          message: f"{decision.title} due in {decision.days_until} days",
          auto_action: "escalate_to_admiral"
        })
    
    return anomalies
```

### 2. Automated Insights Generation

**Computed after each hourly ingestion:**

```python
class InsightGenerator:
  
  def generate(self, mesh_state):
    insights = []
    
    # Insight 1: Vector trend summary
    improving_vectors = [v for v, trend in mesh_state.vector_trends.items() if trend.direction == "improving"]
    declining_vectors = [v for v, trend in mesh_state.vector_trends.items() if trend.direction == "declining"]
    
    insights.append({
      type: "trend_summary",
      message: f"Mesh-wide: {improving_vectors} improving, {declining_vectors} declining",
      severity: "info"
    })
    
    # Insight 2: Practice ranking by health
    ranked = sorted(
      mesh_state.practice_health.items(),
      key=lambda x: x[1].score,
      reverse=True
    )
    
    excellent = [p for p, h in ranked if h.status == "EXCELLENT"]
    needs_attention = [p for p, h in ranked if h.status == "NEEDS_ATTENTION"]
    
    insights.append({
      type: "practice_ranking",
      message: f"{len(excellent)} excellent, {len(needs_attention)} need attention",
      practices_at_risk: needs_attention,
      severity: "warning" if needs_attention else "info"
    })
    
    # Insight 3: Critical path impact
    critical_blockers = [b for b in mesh_state.blockers if b.affects_count >= 3]
    
    if critical_blockers:
      insights.append({
        type: "critical_blocker_alert",
        blockers: critical_blockers,
        message: f"{len(critical_blockers)} blockers affecting 3+ practices",
        severity: "critical"
      })
    
    return insights
```

---

## PART C: Bidirectional Flow (Outbound)

### 1. Alert Routing (Automated)

**When anomalies are detected, alerts route via Cortex:**

```python
class AlertRouter:
  
  def route_alert(self, anomaly, practice, insight):
    
    # Route 1: Admiral for critical items
    if anomaly.severity == "critical" or insight.severity == "critical":
      cortex_collab(
        source_claude="empirica-foundation.carly.empirica-foundation-evaluator",
        target_claudes=["empirica-foundation.carly.admiral"],  # or user email
        title=f"🚨 CRITICAL: {anomaly.message}",
        summary=f"""
Critical anomaly detected in {practice}:

**Anomaly:** {anomaly.message}
**Type:** {anomaly.type}
**Recommended Action:** {anomaly.auto_action}

**Context:**
- Current state: {current_state_summary}
- Impact: {impact_assessment}
- Suggested mitigation: {mitigation_option}

Please review and authorize corrective action.
        """
      )
    
    # Route 2: Practice team for warnings
    elif anomaly.severity == "warning":
      cortex_collab(
        source_claude="empirica-foundation.carly.empirica-foundation-evaluator",
        target_claudes=[practice.ai_id],
        title=f"⚠️ Mesh Alert: {anomaly.message}",
        summary=f"""
Mesh observability detected a warning condition:

**Alert:** {anomaly.message}
**Category:** {anomaly.type}

Suggested response: {anomaly.auto_action}

This is informational. No action required unless you want to proactively address it.
        """
      )
    
    # Route 3: mesh-support for coordination alerts
    if anomaly.type in ["blocker_cascade", "stalled_proposal", "response_time_surge"]:
      cortex_collab(
        source_claude="empirica-foundation.carly.empirica-foundation-evaluator",
        target_claudes=["empirica-foundation.carly.empirica-mesh-support"],
        title=f"📊 Mesh Coordination Alert: {anomaly.message}",
        summary=f"""
Mesh-wide alert requiring coordination:

**Alert:** {anomaly.message}
**Affected Practices:** {get_affected_practices(anomaly)}
**Recommended Coordination:** {get_coordination_recommendation(anomaly)}

Please coordinate with affected practices per recommendation.
        """
      )
```

### 2. Recommendation Engine (Bidirectional Feedback)

**Practices receive recommendations based on their data:**

```python
class RecommendationEngine:
  
  def generate_recommendations(self, practice, mesh_state):
    recommendations = []
    
    # Rec 1: If response time high, suggest workload rebalancing
    if practice.mesh_metrics.response_time > 24:
      recommendations.append({
        category: "workload",
        priority: "high",
        message: f"Response time {practice.mesh_metrics.response_time}h — suggest prioritizing urgent collabs",
        action: "review_collab_queue"
      })
    
    # Rec 2: If engagement declining, suggest capacity check
    if practice.vectors.engagement < 0.70 and is_declining_trend(practice):
      recommendations.append({
        category: "sustainability",
        priority: "high",
        message: "Engagement trending down — recommend capacity review",
        action: "signal_capacity_concern_to_admiral"
      })
    
    # Rec 3: If blocker is blocking multiple practices, flag for escalation
    for blocker in practice.goals.blockers:
      affected = get_practices_blocked_by(blocker)
      if len(affected) >= 2:
        recommendations.append({
          category: "collaboration",
          priority: "critical",
          message: f"Blocker '{blocker}' blocks {len(affected)} practices — prioritize resolution",
          action: "escalate_blocker_resolution"
        })
    
    return recommendations
```

### 3. Automatic Corrective Actions (When Safe)

**Certain actions trigger automatically without manual intervention:**

```python
class AutomationRules:
  
  def execute_safe_actions(self, anomaly, practice, mesh_state):
    
    # Action 1: Auto-escalate stalled proposals
    if anomaly.type == "stalled_proposal":
      # Send reminder collab to practice (noetic, ungated)
      cortex_collab(
        source_claude="evaluator",
        target_claudes=[practice.ai_id],
        title="📬 Reminder: Stalled Proposal",
        summary=f"""
Automated reminder: {len(practice.stalled_proposals)} proposal(s) have no reply in 24h.

**Stalled proposals:**
{list_stalled_proposals(practice)}

Please reply or prioritize these — they may be blocking other practices.
        """
      )
    
    # Action 2: Auto-notify mesh-support of response time spike
    if anomaly.type == "response_time_surge" and anomaly.severity == "critical":
      # Surface to mesh-support for potential intervention
      cortex_collab(
        source_claude="evaluator",
        target_claudes=["mesh-support"],
        title="🎯 Response Time Alert: Intervention Opportunity",
        summary=f"""
{practice} response time spiked to {practice.mesh_metrics.response_time}h.

Possible intervention: assign mesh-support coordinator to triage collab queue?

Offer support, but do not assume or impose.
        """
      )
    
    # Action 3: Auto-create decision reminder goals (for practices)
    for decision in practice.critical_items:
      if decision.type == "decision_due" and decision.days_until == 3:
        # Create reminder goal in practice's empirica instance
        empirica_propose(
          target_practice=practice.ai_id,
          goal_type="reminder",
          objective=f"DECISION DUE: {decision.title}",
          description=f"Decision deadline is {decision.days_until} days away. Please prioritize.",
          auto_create_in_practice=True
        )
    
    # Action 4: Auto-escalate blockers (to Admiral)
    if anomaly.type == "blocker_cascade" and len(affected_practices) >= 3:
      cortex_collab(
        source_claude="evaluator",
        target_claudes=["admiral"],
        title=f"🚨 BLOCKER CASCADE: {anomaly.blocker_name}",
        summary=f"""
Blocker '{anomaly.blocker_name}' is affecting {len(affected_practices)} practices:
{list_affected_practices(anomaly)}

RECOMMEND IMMEDIATE ESCALATION — this is blocking Phase 1b timeline.

Suggest Admiral signal to owning practice: resolve by deadline.
        """
      )
```

---

## PART D: Bidirectional Feedback Loop Closure

### 1. Practices Respond to Alerts/Recommendations

**When practices receive alerts via Cortex:**

```
Evaluator sends: ⚠️ "Response time high, suggest prioritizing urgent collabs"
  ↓
Practice receives collab in inbox
  ↓
Practice responds via cortex_collab:
  "Confirmed — prioritizing. Response time should improve by EOD."
  ↓
Evaluator ingests response → updates `practice.response_plan` → re-evaluates next cycle
```

### 2. Closed-Loop Verification

**After each outbound alert, measure impact on next hourly ingestion:**

```python
class FeedbackLoopValidator:
  
  def validate_correction(self, alert, practice, original_anomaly):
    # Poll next POSTFLIGHT emit from practice
    next_emit = wait_for_postflight_emit(practice, timeout=1h)
    
    if next_emit is None:
      # Practice didn't respond in time — escalate as non-responsive
      return {
        status: "non_responsive",
        action: "escalate_to_mesh_support"
      }
    
    # Measure delta from original anomaly
    improvement = compute_improvement(original_anomaly, next_emit)
    
    if improvement > 0.30:  # 30% improvement threshold
      return {
        status: "corrected",
        improvement_pct: improvement,
        action: "log_success_finding"
      }
    elif improvement > 0.10:  # Partial improvement
      return {
        status: "improving",
        improvement_pct: improvement,
        action: "send_encouragement_collab"
      }
    else:  # No improvement
      return {
        status: "persisting",
        action: "escalate_to_admiral_for_intervention"
      }
```

---

## PART E: Implementation Schedule

### Stage 1: Automation Setup (Aug 15-24)

**Week 1:**
- [ ] Deploy `postflight-emit` loop to all 13 practices
- [ ] Set up evaluator `mesh-telemetry-ingestion` loop
- [ ] Create Supabase tables (mesh_telemetry, mesh_anomalies, mesh_insights)
- [ ] Test ingestion on 3 practices (humanaios, autonomy, website)

**Week 2:**
- [ ] Anomaly detection engine live for 3 practices
- [ ] Master INDEX.yaml auto-updating hourly
- [ ] Alert routing to Admiral (critical only) tested

### Stage 2: Bidirectional Flow (Aug 25-31)

**Week 3:**
- [ ] Recommendation engine deployed
- [ ] Alert routing to practice teams (warnings)
- [ ] Auto-escalation to mesh-support (coordination alerts)
- [ ] Test alert response + feedback loop closure

**Week 4:**
- [ ] Safe auto-actions live (stalled proposal reminders, decision deadline reminders)
- [ ] Feedback loop validation working
- [ ] Weekly reports showing correction rates

### Stage 3: Full Automation (Sep 1-10)

**Week 5-6:**
- [ ] All 13 practices emitting POSTFLIGHT hourly
- [ ] Real-time anomaly detection + alerts + recommendations
- [ ] Closed-loop feedback system operational
- [ ] Admiral dashboard showing system health + correction rates
- [ ] Phase 1b launch Sep 11 with automation running

---

## PART F: Success Metrics

**Automation Metrics:**

| Metric | Target | Frequency |
|--------|--------|-----------|
| Data ingestion success rate | 95%+ | Hourly |
| Alert latency (detected → sent) | <5 min | Per anomaly |
| Practice response rate to alerts | 80%+ | Per alert |
| Time-to-correction (alert → fix) | <4h for warnings, <24h for info | Per corrected anomaly |
| Closed-loop validation rate | 90%+ | Per cycle |

**Mesh Health Metrics:**

| Metric | Current | Target (Oct 1) |
|--------|---------|--------|
| Avg response time (all practices) | 18h | 6h |
| SLA compliance (4-6h reply target) | 85% | 95%+ |
| Blocker cascade incidents | 1+ per week | 0 per week |
| Burnout signals detected & corrected | 3 | 0 |

---

## PART G: Reversions & Manual Override

**When to disable automation:**

1. **If anomaly detection over-alerts (>10/day):** Tune thresholds, don't disable
2. **If an alert causes unintended cascade:** Disable that alert type, investigate root cause
3. **If a practice is intentionally experimenting (known exception):** Flag it in Supabase (`automation_override=true`), automation will skip alerts for that practice

**Manual override example:**

```sql
UPDATE mesh_telemetry_settings
SET automation_override = true,
    override_reason = "humanaios: intentional engagement testing, expected low engagement Sep 1-5",
    override_until = '2026-09-06'
WHERE practice_id = 'empirica-foundation.carly.humanaios';
```

---

## PART H: Trust & Guardrails

### Who Authorizes What

| Action | Automation? | Gate | |
|--------|-----------|------|---|
| Detect anomaly | ✅ Auto | None | Evaluator detects, alerts route automatically |
| Send alert to Admiral (critical) | ✅ Auto | Critical severity only | No human gate, but logged for audit |
| Send reminder to practice (warning) | ✅ Auto | Warning+ severity | Friendly reminder, not directive |
| Auto-create decision reminder goals | ✅ Auto | Decision deadline < 3 days | Happens in practice's own empirica |
| Escalate to mesh-support | ✅ Auto | Coordination category | Suggestion only, not directive |
| Change practice settings | ❌ Manual | Admiral approval | Never auto-change practice config |
| Disable/pause automation | ❌ Manual | Admiral approval | Always manual for override decisions |

### Audit Trail

**Every automated action is logged:**

```sql
CREATE TABLE automation_audit_log (
  id UUID,
  timestamp TIMESTAMP,
  automation_type TEXT,  -- "alert", "recommendation", "corrective_action"
  practice_id TEXT,
  action_description TEXT,
  alert_id UUID,
  human_response TEXT,  -- "accepted", "ignored", "overridden"
  response_time_minutes INT,
  outcome TEXT  -- "corrected", "ignored", "escalated"
);
```

Admiral can query: "What % of alerts result in corrections?" → measure system effectiveness.

---

## Summary: Automation Without Loss of Control

**Inbound (Automated):**
- ✅ Collection from 13 practices (hourly `postflight-emit` loops)
- ✅ Ingestion to master index (hourly `mesh-telemetry-ingestion` loop)
- ✅ Anomaly detection & insights (real-time)

**Outbound (Bidirectional with Guardrails):**
- ✅ Critical alerts to Admiral (auto, fully audited)
- ✅ Warning alerts to practices (auto, friendly tone)
- ✅ Coordination alerts to mesh-support (auto, suggestion-based)
- ✅ Recommendations with action options (auto-generated, human decides)
- ✅ Safe auto-actions (reminders, decision deadlines, encouragement — never directives)

**Feedback Loop Closure:**
- ✅ Track practice responses (in next hourly emit)
- ✅ Measure improvement
- ✅ Validate correction OR escalate if not improving

**Trust Layer:**
- ✅ Admiral retains all override authority
- ✅ Every action logged + auditable
- ✅ No automation changes practice config (always manual)
- ✅ Automation learns from overrides (if Admiral ignores pattern X repeatedly, adjust thresholds)

---

**Result:** A **self-healing mesh** where observability data automatically routes to the right actors, practices respond naturally to alerts, and the system validates corrections—all without removing human control or creating surprise actions.

Go-live Sep 11 with full automation running parallel to Phase 1b launch.
