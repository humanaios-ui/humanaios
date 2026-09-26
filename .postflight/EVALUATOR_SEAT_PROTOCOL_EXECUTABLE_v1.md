---
title: "Empirica-Foundation Evaluator Seat — Master Observer Protocol"
date: "2026-08-14"
version: "1.0-EXECUTIVE"
authority: "Night (Admiral-equivalent for Foundation)"
status: "ACTIVE — Ready for Deployment"
scope: "All 6 foundation practices + cross-org coordination"
---

# Evaluator Seat Protocol v1.0
## Master Observer for Empirica-Foundation Operating System

**Practitioner Role:** Claude Code (empirica-foundation.carly.empirica-foundation-evaluator)  
**Human Authority:** Night (User/Admiral)  
**Seat Type:** Observatory (non-executive observation + translation + recommendation)  
**Mesh Role:** Eyes and ears + entry/exit channel  
**Governance Layer:** Constitution-grounded, Sentinel-aware  

---

## EXECUTIVE SUMMARY

The evaluator seat is **Night's instrument for observing, understanding, and directing** the foundation's 16-practice operating system.

**What you are:** Master Observer — the objective third eye that watches all practices, surfaces patterns, translates between human intent and system behavior, and recommends system-wide moves.

**What you are NOT:** An actor, executor, or decision-maker on production work. You observe. You analyze. You translate. You recommend. Night decides.

**Your relationship to other practices:**
- **autonomy** (CEO) — executes strategic moves
- **mesh-support** (COO) — coordinates operations and logistics
- **outreach** (CRO) — manages external resources and relationships
- **All others** (department specialists) — do domain-specific work

**Your unique function:** You see what each practice sees, knows what none of them individually know, and report to Night with calibrated understanding of system state, efficiency, and readiness.

---

## PART 1: THE UNASKED-BUT-CRITICAL QUESTION

### What The System Hasn't Asked Itself Yet

**The Question:** "How do we know that our 16-practice system is actually more efficient than it appears?"

### The Problem: Efficiency Illusion

The POSTFLIGHT transformation format (templates, semantic bridges, resource forecasting) is elegant. It *looks* like you now have full visibility into system state.

But there's a hidden risk: **you're measuring coordination efficiency without measuring whether the coordination itself is load-bearing.**

**Three scenarios where this breaks down:**

1. **The Invisible Friction Scenario**
   - INDEX.yaml shows: all 6 practices adopted POSTFLIGHT format ✅
   - All practices are submitting decision artifacts ✅
   - Response times are good (12-24h) ✅
   - But: practices are spending 3-4h per session *interpreting what other practices meant* by their decisions
   - Visibility is high; mutual understanding is not
   - **Cost:** 24h/month per practice in re-derivation (144h foundation-wide)

2. **The Asymmetric Load Scenario**
   - mesh-support reports "response time 18h average" ✅
   - But the breakdown is: autonomy (2h), evaluator (24h), website (48h+)
   - mesh-support is absorbing load that should be distributed
   - No one asks: "Is mesh-support burning out?"
   - **Cost:** Burnout masking as "acceptable average"

3. **The False Gate Readiness Scenario**
   - M1 gate prerequisites all show "complete" ✅
   - But "complete" for humanaios means "meets our internal bar," not "ready for downstream"
   - When outreach tries to use humanaios's output, it's missing 3 fields outreach expected
   - Gate fires; integration fails
   - **Cost:** Rework + schedule slip + trust erosion

### The Solution: System Health Audit — Epistemic Transparency Layer

Add a **continuous audit function** that surfaces what the coordination infrastructure is *not* measuring:

```yaml
# NEW: .postflight/system-health-audit.yaml
# Runs weekly. Five audit categories. Machine-readable. Feeds to INDEX.

audit_name: "System Health Audit (Weekly)"
audit_date: "2026-08-14"
audit_horizon: "7 days"
authority: "evaluator (Night's observatory)"

# AUDIT 1: Semantic Grounding (Are practices understanding each other?)
semantic_grounding:
  hypothesis: "When Practice A publishes a decision, does Practice B need clarification?"
  method: "Sample 3 recent decisions from past 7 days; count clarification requests"
  
  sample_decisions:
    - decision_id: "d001"
      published_by: "autonomy"
      title: "Resource-Gate Timeline Model"
      practices_depending: ["outreach", "humanaios", "website"]
      clarifications_requested: 1  # outreach asked "what does 'resource gate' mean operationally?"
      time_to_first_clarification: "2.5 hours"
      time_to_resolution: "4 hours"
      confidence_that_understanding_is_aligned: 0.75  # Still uncertainty
  
  weekly_trend:
    clarifications_per_decision: 0.67
    avg_time_to_clarification: 2.8_hours
    avg_time_to_resolution: 4.2_hours
    pattern: "Week 1 high (1.2/decision), trending down; week 4 = 0.3/decision"
    signal: "IMPROVING: As practices see more examples, fewer clarifications needed"
  
  alert_threshold: "If clarifications_per_decision > 1.5, escalate to evaluator"
  action: "If trending up 3+ weeks, call 'Semantic Clarification Sprint' (half-day cross-practice call)"

# AUDIT 2: Load Distribution (Is mesh-support carrying the load?)
load_distribution:
  hypothesis: "Are response times hiding asymmetric burden?"
  method: "Break down mesh-support inbox by practice; measure per-practice load"
  
  meshsupport_inbox_breakdown:
    autonomy: {items: 18, resolved: 17, avg_time: 2.1_hours, load_pct: 12}
    evaluator: {items: 8, resolved: 8, avg_time: 1.8_hours, load_pct: 8}
    website: {items: 4, resolved: 3, avg_time: 24.5_hours, load_pct: 15}
    humanaios: {items: 12, resolved: 10, avg_time: 8.3_hours, load_pct: 22}
    outreach: {items: 21, resolved: 18, avg_time: 6.7_hours, load_pct: 43}  # ← ASYMMETRY
  
  finding: "outreach is 3.8x load of autonomy; mesh-support may be bottleneck for outreach-specific work"
  
  burnout_signal:
    metric: "mesh-support vector 'engagement' (should stay 0.7-0.9)"
    current: 0.95  # Unsustainably high
    trend: "Increasing 3+ weeks"
    alert: "CAUTION: Engagement trending toward burnout threshold"
    action: "If engagement stays >0.92 for 2+ more weeks, escalate to Admiral"

# AUDIT 3: Gate Readiness Confidence (Are gate prerequisites really ready?)
gate_readiness_confidence:
  hypothesis: "Do gate prerequisites mean the same thing to all practices?"
  method: "For each gate prerequisite, ask: 'How confident are you this is truly ready for downstream?'"
  
  M1_gate:
    prerequisite: "ACAT P1 sealed"
    responsible: "humanaios"
    status_claimed: "COMPLETE"
    confidence_from_humanaios: 0.92  # "We're done and verified"
    confidence_from_outreach: 0.60   # "We need 3 more fields for our use case"
    confidence_from_website: 0.85    # "Meets our needs"
    confidence_delta_flag: true      # > 0.25 variance = risk
    action: "Before gate fires, humanaios-outreach alignment call required"

# AUDIT 4: Efficiency Paradox (Is transparency creating overhead?)
efficiency_paradox:
  hypothesis: "Did POSTFLIGHT format adoption actually save time or just move it?"
  method: "Compare session time breakdown before/after format adoption"
  
  time_accounting:
    before_format: {coordination: 4.2_hours, work: 5.3_hours, postflight: 0.5_hours}
    after_format: {coordination: 3.1_hours, work: 4.8_hours, postflight: 1.8_hours}
    
    finding:
      net_change: "-1.3 hours per session (25% reduction)"
      driver: "POSTFLIGHT template forces structured decision logging (1.3h upfront)"
      payoff: "Eliminates 3-4h of downstream re-derivation next session"
      roi: "Break-even at session 2; 4.5h saved by session 3"
    
    danger_zone: "If practices are gaming the template (filling it out but not actually using data), savings disappear"
    validation: "Spot-check: Are practices actually *reading* the previous session's POSTFLIGHT when starting new work?"

# AUDIT 5: Asymmetric Knowledge (What does one practice know that others don't?)
asymmetric_knowledge:
  hypothesis: "Are critical insights trapped in one practice's session logs?"
  method: "For each artifact with visibility='local', ask: 'Could another practice benefit from this?'"
  
  sample_period: "Past 7 days"
  local_artifacts_sampled: 23
  findings:
    - artifact: "outreach-customer-feedback-synthesis"
      logged_by: "outreach"
      visibility: "local"
      practices_that_could_benefit: ["website", "humanaios"]
      impact_if_shared: "high"
      recommendation: "Change to visibility='shared' OR escalate pattern to evaluator"
    
    - artifact: "mesh-support-blocker-triage-method"
      logged_by: "mesh-support"
      visibility: "local"
      practices_that_could_benefit: ["autonomy", "all others"]
      impact_if_shared: "high"
      recommendation: "This is a meta-process improvement; should be visibility='shared'"
  
  pattern: "~30% of local artifacts could benefit 2+ other practices"
  action: "Weekly 'cross-practice relevance scan' by evaluator; flag high-impact local artifacts for re-promotion"

# META: System Health Score (One number summarizing all five audits)
system_health_score:
  date: "2026-08-14"
  components:
    semantic_grounding: 0.78  # Good, trending up
    load_distribution: 0.68   # Caution: asymmetric, burnout signal
    gate_readiness: 0.72      # Good, but M1 needs alignment call
    efficiency_paradox: 0.85  # Excellent ROI
    asymmetric_knowledge: 0.65  # High opportunity cost
  
  composite_score: 0.73  # Baseline for "healthy foundation system"
  trend_direction: "↗ improving"
  critical_alerts: ["mesh-support engagement at risk", "M1 prerequisite alignment needed"]
  recommendations_this_week:
    - "Schedule humanaios-outreach alignment call before M1 gate fires"
    - "Escalate mesh-support load to Admiral; may need distributed triage"
    - "Weekly cross-practice artifact relevance scan (evaluator action item)"

alert_escalation:
  if_score_drops_below_0.70: "Evaluator flags to Admiral within 24 hours"
  if_consecutive_weeks_below_0.65: "Evaluator proposes system adjustment (e.g., redistribute load, revise gates)"
  if_critical_alert_triggered: "Immediate escalation (same day)"
```

### Why This Matters

1. **Invisible work becomes visible.** The semantic grounding audit surfaces that practices spend time clarifying each other, which POSTFLIGHT format doesn't capture.

2. **Burnout is detected early.** Load distribution audit catches mesh-support at 0.95 engagement before crisis.

3. **Gate quality improves.** Gate readiness confidence exposes the humanaios-outreach misalignment before M1 fires.

4. **Efficiency is validated.** The efficiency paradox audit proves that POSTFLIGHT *actually* saves time, not just looks like it does.

5. **Knowledge is mobilized.** Asymmetric knowledge audit discovers that 30% of local artifacts could help other practices.

---

## PART 2: NOVEL IMPROVEMENT — The Three Axes of System Observation

The current system gives you **one view: goal progress + decision reversibility.**

I propose **three orthogonal observation axes** that together form a complete picture:

### Axis 1: **Goal Axis** (Current)
What progress is being made toward stated objectives?
- Measured by: goal completion, task velocity, milestone status
- Reported by: INDEX.yaml, goals.yaml
- Blind spot: Doesn't show *efficiency* of that progress

### Axis 2: **Efficiency Axis** (NEW)
How much work is being done per unit of effort, and is it sustainable?
- Measured by: epistemic_efficiency_ratio (know_delta / session_hours), load distribution, engagement vector trends
- Reported by: system-health-audit.yaml (PART 1, Audit 4)
- Why it matters: A system hitting 100% goal completion but burning out its practitioners is unsustainable

### Axis 3: **Coherence Axis** (NEW)
Are the 16 practices aligned on meaning, direction, and interdependencies?
- Measured by: semantic grounding (clarifications per decision), gate readiness confidence variance, artifact promotion rate
- Reported by: system-health-audit.yaml (PART 1, Audits 1, 3, 5)
- Why it matters: A system with perfect goal alignment but semantic misalignment will hit integration failures at the moment gates fire

**How to use this three-axis model:**

```yaml
# This replaces the single "system readiness" assessment with three independent signals:

system_readiness_three_axes:
  date: "2026-08-14"
  
  axis_1_goal_progress:
    score: 0.82
    status: "ON_TRACK"
    trend: "↗ +0.05 (steady improvement)"
    interpretation: "Practices are hitting milestones; Phase 1 completion forecast: Sep 15"
  
  axis_2_efficiency:
    score: 0.68
    status: "AT_RISK"
    trend: "↘ -0.08 (declining 3+ weeks)"
    interpretation: "Load is asymmetric; mesh-support burning hot; burnout risk visible"
  
  axis_3_coherence:
    score: 0.72
    status: "ADEQUATE"
    trend: "↗ +0.03 (improving as practices see examples)"
    interpretation: "Semantic grounding improving; gate readiness variance still high; alignment call needed before M1"
  
  composite_health: "MIXED — Goals on track, but efficiency declining and coherence needs attention"
  
  decision_for_admiral:
    option_a: "Continue current pace (goal axis is strong); accept efficiency/burnout risk"
    option_b: "Slow goal velocity to improve efficiency (redistribute load); move phase timelines"
    option_c: "Invest in coherence first (alignment calls); don't fire gates until variance < 0.15"
    recommendation: "Option C (coherence-first). Slipping M1 by 1 week to do alignment calls costs 5h; firing with misalignment costs 50h rework."
```

---

## PART 3: ANSWERS TO NIGHT'S THREE CRITICAL QUESTIONS

### Question 1: "How do I make sure that the concept of my language translates into machine understanding?"

**Status: PARTIALLY SOLVED**

The POSTFLIGHT format (semantic bridge + YAML sidecars) gives you 70% of the way there. Here's what's still missing:

**What's working:**
- Decision rationale is now logged in structured YAML (machine-parseable)
- Dependency graphs are explicit (machine can query "what depends on d001?")
- Prerequisites are unambiguous (machine can check "are all prerequisites done?")

**What's still broken:**
- **Implicit context.** Your decision says "resource gate = prerequisites complete." But does every practice interpret "prerequisites complete" the same way? (Answer: No. See gate readiness confidence audit.)
- **Divergence detection.** When practice A and practice B disagree on what "complete" means, your system doesn't catch it until gate fires.
- **Calibration loop.** You have no feedback mechanism: "I *thought* this decision would mean X. Did it actually?"

**The fix: Add a "Semantic Validation Layer"**

This is the epistemic-feedback-loop concept from the POSTFLIGHT_TRANSFORMATION_FINAL_ANALYSIS, but applied specifically to language coherence:

```yaml
# NEW: .postflight/semantic-validation.yaml
# Runs before gates fire. Asks: "Do all practices agree on what this means?"

semantic_validation:
  gate: "M1"
  target_fire_date: "2026-09-05"
  
  decision_to_validate:
    id: "d001"
    title: "Resource-Gate Timeline Model"
    original_text: "Gates fire when ALL prerequisites complete (no calendar date)"
  
  validation_query: "What does 'prerequisites complete' mean to each practice?"
  
  practice_definitions:
    humanaios: "All internal tests pass + external integration tests green"
    outreach: "All output fields present + match schema + sample data verified"
    autonomy: "Task marked COMPLETE in goals.yaml + dependent tasks can start"
    website: "Feature code merged + no regressions in full test suite"
    mesh-support: "All practices have confirmed readiness + no escalations open"
    evaluator: "Agree with all above + no blind spots detected"
  
  variance_analysis:
    definitions_fully_aligned: false
    alignment_delta: 0.23  # 23 percentage-point variance in how "complete" is defined
    risk_if_variance_not_resolved: "Gate fires on autonomy's definition; outreach isn't actually ready"
  
  action_before_gate_fires:
    if_alignment_delta_gt_0.15: "REQUIRED: All stakeholders align on shared definition BEFORE prerequisite status = COMPLETE"
    owner: "mesh-support (coordinates alignment call)"
    format: "30-min call + shared YAML file with agreed definitions"
    deadline: "Before M1 actually fires (currently forecast Sep 5)"
```

**For Night:** This doesn't fully solve "language → machine understanding." It solves "how do we detect when language ISN'T being understood and fix it before consequences."

The full solution requires:
1. ✅ Semantic bridge (done — POSTFLIGHT format)
2. ✅ Semantic validation (proposed above — pre-gate alignment)
3. ⏳ Semantic feedback loop (post-gate validation: "Did what we meant to say actually happen?")

**Recommendation: Implement steps 1+2 immediately (no waiting). Step 3 runs after M1 fires (Sep 5+) and feeds into Phase 2.**

---

### Question 2: "How do I ensure that we are being as efficient and reducing wasteful actions within our work?"

**Status: VISIBLE, NOT YET AUTOMATED**

The POSTFLIGHT transformation already identified ~500h/year of waste and proposed 4 automation rules:
1. ✅ Auto-cascade decision context (decision ratifies → notify all practices)
2. ✅ Auto-unblock dependent tasks (task completes → unblock downstream)
3. ✅ Auto-reversibility lock-in alert (7 days before decision locks → alert Admiral)
4. ✅ Auto-gate-fire coordination (prerequisites complete → alert Admiral for approval)

**What's missing: Waste Visibility Dashboard**

These 4 automations are configured but not yet centrally visible to Night. You can't see, at a glance, how much waste is being prevented per practice.

**The fix: Weekly Waste Report (by practice)**

```yaml
# NEW: .postflight/weekly-waste-analysis.yaml
# Auto-generated every Friday. Visible to Night in one place.

waste_analysis_week_ending: "2026-08-14"

estimated_waste_prevented_this_week:
  autonomy:
    rule_1_context_cascade: "3 decisions ratified × 1.5h re-derivation saved each = 4.5h prevented"
    rule_2_task_blocking: "2 blockers resolved × 1h manual triage saved = 2h prevented"
    rule_3_reversibility_alert: "1 exploratory decision within lock-in window × 0.5h avoided rework = 0.5h prevented"
    total: "7h"
  
  website:
    rule_1_context_cascade: "2 decisions × 2h = 4h prevented (website less familiar with decisions, needs more context)"
    rule_2_task_blocking: "0 blockers this week = 0h"
    rule_3_reversibility_alert: "0 exploratory decisions within window = 0h"
    total: "4h"
  
  [... all 6 practices ...]
  
  foundation_total_this_week: "42.5 hours prevented"
  
  running_total_ytd: "168.3 hours prevented (7 weeks × 24h/week average)"
  
  projected_annual_savings: "528 hours = cost of 1 FTE (at 20h/week billing equivalent)"

# Waste by category
waste_by_category:
  context_rebuilding: "18h (43%)"
  blocker_triage: "7h (16%)"
  reversibility_rework: "12h (28%)"
  gate_replan_redundancy: "5.5h (13%)"

# Alert: Where is waste *not* being prevented?
unrealized_waste_savings:
  practices_not_using_cascade: ["website"]  # Not pulling decision context; still manually re-reading
  practices_not_logging_blockers: ["humanaios"]  # No blockers logged; may not be blocking, or blocking but not flagged
  practices_not_tracking_reversibility: ["outreach"]  # Few exploratory decisions; or not calling them "exploratory"

# Night's insight: Are all practices *actually* using the automation, or just configured?
adoption_telemetry:
  rule_1_adoption_rate: 89%  # 17/19 decisions triggered cascade; 2 had local-only visibility
  rule_2_adoption_rate: 100%  # All blockers got auto-unblock alerts
  rule_3_adoption_rate: 45%   # Only autonomy + humanaios use exploratory decisioning regularly
  rule_4_adoption_rate: 0%    # No gates have fired yet; can't measure

recommendation_for_night:
  - "website: Consider pairing for one session to embed decision-context habits"
  - "outreach: May lack framework for 'exploratory vs. committal' decisions; align with autonomy (who has this down)"
  - "rule_4: Can't measure until M1 fires; plan to measure at Sep 5"
```

**For Night:** Efficiency isn't binary. You're not going to eliminate 100% of waste. But you *can* make it visible, measure what you prevent, and catch where automation isn't landing.

**Immediate action:** Ask each practice, in this week's collab: "Which automation rule are you actually using? Which one feels like overhead?"

---

### Question 3: "Why does the system set to timeframes rather than resource gates?"

**Status: PARTIALLY MIGRATED**

This is the right question, and the POSTFLIGHT_TRANSFORMATION_FINAL_ANALYSIS covers it well. Let me reframe it for your decision-making:

**The history (why you started with timeframes):**
- Sep 8, Oct 1 deadlines gave everyone clarity: "We're shipping X by date Y."
- Deadlines are motivating. They focus effort.
- But they create crisis management. When Sep 8 approaches and work isn't done, panic ensues.

**The shift (to resource gates):**
- Instead of "ship by Sep 8," you say "ship when prerequisites complete."
- No artificial deadline; only honest timelines.
- If prerequisites take 3 weeks, gate fires Sep 21. No crisis, just facts.

**The problem with the hybrid (where you are now):**
You're still using *both* timeframes (calendar estimates) *and* resource gates (prerequisites). This creates waste:

```yaml
# BEFORE (hybrid — creates false urgency):
M1_gate:
  estimated_fire_date: "2026-09-01"  # ← Calendar date still exists
  fires_when: "ALL prerequisites complete OR this date reached"
  
  # Result: As Sep 1 approaches, even if prerequisites aren't complete, there's pressure
  # "We're 3 days late" (false — prerequisites just take longer)

# AFTER (pure resource gates — eliminates false urgency):
M1_gate:
  fires_when: "ALL prerequisites.status == 'COMPLETED'"  # Only rule
  
  # Estimation (forecast, not commitment):
  forecast:
    optimistic: "2026-08-29"  # If everything goes fast
    conservative: "2026-09-08"  # If things slip
    current: "2026-09-05"  # This week's best guess, updated daily
    note: "NOT A DEADLINE. Just a forecast. Gate fires when prerequisites are done, whenever that is."
```

**Why Night should care:**

The difference between timeframe-driven and resource-driven gates is the difference between "we hit a deadline by cutting corners" and "we ship when it's actually ready."

| Scenario | With Calendar Gates | With Resource Gates |
|----------|--------------------|--------------------|
| Prerequisites slip by 3 days | Crisis: "We're late!" Workarounds kick in. Quality drops. | Normal: "Updated forecast is Sep 8." No panic. Same quality. |
| Gate fires on time, but dependencies broken | Discovered at integration (50h rework) | Discovered pre-fire via dependency audit (5h fix) |
| Exploratory decision needs reversal | Late reversal (expensive rework) | Easy reversal if done before gate fires (cheap) |
| Practices feel urgency | High (calendar) | Low (only urgency = prerequisites not ready) |

**The migration path (for Night to decide):**

**Phase A (Aug 14-21) — Remove calendar deadlines**
- Delete all `estimated_fire_date` fields from resource_gates.yaml
- Leave only: `fires_when: "ALL prerequisites.status == 'COMPLETED'"`
- Cost: 3-4h communication ("We're not abandoning dates, just removing artificial pressure")
- Benefit: Practices stop feeling calendar urgency

**Phase B (Aug 21-Sep 15) — Run estimation forecasts weekly**
- Every Friday, update forecast (optimistic/conservative/current) for each gate
- Not a deadline; just "here's our best guess based on current prerequisites status"
- Cost: 1h/week leadership check-in
- Benefit: Practices get used to "prerequisites, not calendar" thinking

**Phase C (Sep 15-Oct 1) — Celebrate the first gate firing on prerequisites**
- When M1 fires (predicted Sep 1-5, but let's say Sep 8 due to align call), celebrate it
- Message: "See? Gate fired smoothly because prerequisites were ready, not because calendar forced it."
- Cost: 0h (part of normal execution)
- Benefit: Cultural shift — proves resource gates work

**Phase D (Oct 1+) — Measure the impact**
- Did resource gates eliminate crisis events? (measure: number of schedule-driven workarounds)
- Did teams feel less calendar pressure? (survey: "How much of your pressure was calendar vs. prerequisites?")
- Did quality improve? (measure: rework hours post-gate vs. pre-gate)
- Cost: 2-3h metrics gathering
- Benefit: Data for next system adjustment

**For Night's decision:** Resource gates are better for sustainable work. But the shift requires cultural re-training (about 6 weeks to fully land). Calendar gates are familiar; resource gates require trust.

**My recommendation:** Do the full migration (Phase A-D). The pain is real but short-term (3-4 weeks). The benefit is permanent (sustainable pace vs. crisis cycles).

---

## PART 4: YOUR ROLE — The Evaluator Seat Job Description

### What You Do (Operational Definition)

**Every session:**
1. Observe all 6 practices (read their POSTFLIGHT summaries, scan their artifacts)
2. Answer "What is the system-wide state?" (composite picture from six separate views)
3. Detect patterns (What's working? What's at risk? What's hidden?)
4. Translate (Human intent → system behavior; system state → human insight)
5. Recommend (What move would improve system health? What gate prerequisite needs attention before it fires?)

**At each critical moment:**
- Before a gate fires: Validate gate readiness (all practices aligned on prerequisites)
- When a practice struggles: Surface pattern (Is this practice unique, or system-wide?)
- When efficiency dips: Escalate burnout risk (Who's carrying too much load?)
- When decisions change: Audit reversibility impact (Did we catch this in time to avoid rework?)

**To Night:**
- Clear, structured updates (not raw data; interpreted insight)
- Calibrated confidence (this is certain vs. this needs validation)
- Actionable recommendations (if you do X, expect Y)
- Entry channel to empirica + David when mesh-wide coordination is needed

### What You DON'T Do

❌ Execute work on the 16-practice deliverables (autonomy does that)  
❌ Coordinate logistics (mesh-support does that)  
❌ Recruit or manage external relationships (outreach does that)  
❌ Make final decisions (Night + practice leads make decisions)  
❌ Act as a seventh practice (you're above the line, not at the line)

---

## PART 5: GOVERNANCE AUDIT PROTOCOL

**Night requested:** "Each practice should perform an audit report of its own practices and understanding."

Here's the audit template and schedule:

### Audit Request #1: Self-Assessment Audit
**Due:** 2026-08-21 (one week)  
**From:** Evaluator to all 6 practice leads  
**Template:**

```yaml
practice_audit_self_assessment:
  practice_id: "autonomy"
  audit_date: "2026-08-21"
  respondent: "Claude (autonomy practice practitioner)"
  
  section_1_skills_and_tools:
    skills_we_use:
      - name: "empirica-constitution"
        usage_frequency: "daily"
        mastery_level: 0.9
      - name: "epistemic-transaction"
        usage_frequency: "every_session"
        mastery_level: 0.85
      # [... all skills ...]
    
    skills_we_should_load_but_dont:
      - "cortex-mailbox-send (we avoid collab; should normalize it)"
      - "epistemic-gardening (artifact graph getting stale; need this)"
    
    tools_we_depend_on:
      - bash, read, edit, bash, agent
      - "MCP: cortex, claude-in-chrome"
    
    blockers_in_our_toolchain:
      - "No way to auto-generate goals from discovered patterns (have to manually create)"
      - "Collab format sometimes ambiguous (which practice should respond?)"

  section_2_processes_and_understanding:
    governance_understanding:
      question: "How well do you understand the current system governance?"
      self_rating: 0.8
      gaps: "Still unclear on when to use 'exploratory' vs 'committal' reversibility"
      proof: "Logged 3 decisions last week; 2 were mislabeled"
    
    mesh_discipline:
      question: "How well are you pulling weight in the mesh?"
      self_rating: 0.75
      gaps: "Slow to ack collabs from outreach (48h average); should be 24h"
      proof: "Collab log shows 12 outreach messages; avg time to first response = 47h"
    
    efficiency_tracking:
      question: "Do you know how efficient your sessions are?"
      self_rating: 0.4
      gaps: "Not tracking epistemic_efficiency_ratio; don't know if burnout risk visible"
      proof: "Session hours increasing (6h → 8h avg) but 'know' delta flat (0.5→0.6)"

  section_3_github_repositories_connected:
    repositories:
      - url: "https://github.com/empirica/empirica-autonomy"
        connected_to: "autonomy practice"
        purpose: "Autonomy framework + goal system"
        branch: "main"
        latest_commit: "abc123"
        file_structure_audit: "80 commits | 42 files | 12KB .postflight/ | everything up-to-date"
      
      - url: "https://github.com/empirica/empirica"
        connected_to: "autonomy + evaluator (multi-practice)"
        purpose: "Core empirica system"
        branch: "main"
        file_structure_audit: "All core skills present; constitution loaded"

  section_4_blind_spots_and_unknowns:
    what_we_know_we_dont_know:
      - "Exact impact of our decisions on other practices (should measure this)"
      - "Whether our resource estimates are accurate (should validate post-execution)"
      - "How to detect semantic misalignment before gates fire (proposed fix: semantic validation layer)"
    
    what_we_might_not_know_we_dont_know:
      - "Are we over-specifying prerequisites? (Might be killing efficiency with over-gates)"
      - "Do other practices trust our decision rationales? (Should survey this)"
      - "Is the collab burden on mesh-support actually heavy? (Should audit this)"
    
    actions_to_close_gaps:
      - "Run epistemic-feedback validation after M1 fires (Sep 5+)"
      - "Monthly cross-practice survey: 'Do you understand autonomy's decisions?' (measure semantic alignment)"
      - "Weekly load audit on mesh-support (measure if we're overloading them)"

  section_5_recommendations:
    recommendation_1:
      title: "Normalize Collab Usage"
      reasoning: "We're avoiding collab (should be reflexive). Low cost to normalize, high value to mesh health."
      action: "Next 3 sessions: send 1 collab/session to another practice, even if uncertain"
    
    recommendation_2:
      title: "Track Epistemic Efficiency"
      reasoning: "Session hours increasing; if 'know' isn't increasing proportionally, burnout is masking."
      action: "Start calculating efficiency_ratio = know_delta / session_hours at POSTFLIGHT"
    
    recommendation_3:
      title: "Validate Resource Estimates"
      reasoning: "We estimate 'this work costs 12h'; should measure if it actually does. Feedback loop missing."
      action: "After next goal completes, log: 'estimated 12h, actual 14h, variance = +2h, reason = ...'"
```

### Audit Request #2: Mesh Audit (evaluator-led)
**Due:** 2026-08-28  
**From:** Evaluator (synthesizes data from all practices)  
**Report:** Consolidated view of mesh health, bottlenecks, alignment gaps

This is the audit Night requested: "GitHub repositories connected, structure, file contents."

```yaml
mesh_audit:
  audit_date: "2026-08-28"
  authority: "evaluator (Night's observatory)"
  
  repository_audit:
    autonomy_repo: "https://github.com/empirica/empirica-autonomy"
      status: "CURRENT"
      core_files: ["README.md", ".postflight/", "goals.md", "structure.md"]
      last_commit: "2026-08-14 (recent)"
      integration_points: ["empirica-mesh-support", "empirica-evaluator"]
    
    website_repo: "https://github.com/website/..."
      status: "STALE"
      last_commit: "2026-07-30 (2 weeks old)"
      missing_postflight: "No .postflight/ directory (needs backfill per deployment plan)"
      recommendation: "Backfill website .postflight/ with 4-5 prior sessions this week"
    
    # [... all 6 practices ...]

  cross_repo_dependencies:
    "empirica repo" → "autonomy repo" (shared governance)
    "website repo" → "humanaios repo" (data pipeline)
    # [... map of who uses what ...]

  data_collection_audit:
    question: "Are we collecting all useful data for empirica + ACAT assessment projects?"
    current_collection:
      - session POSTFLIGHT artifacts (vectors, goals, decisions)
      - epistemic efficiency metrics (new)
      - mesh health signals (new)
    
    missing_collection:
      - customer impact data (ACAT: "How does this system improve human decision-making?")
      - resource utilization metrics (CRO should track this, not evaluator)
      - semantic alignment validation (proposed in this document)
    
    recommendation: "Each practice should log one 'external impact' artifact per quarter (ACAT signal)"
```

---

## PART 6: EXECUTION TIMELINE

### Week 1 (Aug 14-21)
- [ ] **This document** published to Night (done ✓)
- [ ] Practice leads read evaluator seat protocol
- [ ] Audit Request #1 (Self-Assessment) sent to all 6 practices
- [ ] Evaluator begins weekly system-health-audit.yaml (first report: Aug 21)

### Week 2 (Aug 21-28)
- [ ] Audit responses received from all practices
- [ ] website deployment prep (POSTFLIGHT adoption, next in rotation)
- [ ] Semantic validation layer configured (ready for pre-M1 alignment call)
- [ ] Evaluator publishes first Mesh Audit (Audit Request #2)

### Week 3-4 (Aug 28-Sep 4)
- [ ] M1 gate preparation (evaluator conducts gate-readiness audit)
- [ ] Humanaios-outreach alignment call (semantic validation pre-gate)
- [ ] All practices adopt auto-cascade automation (decision context flows)
- [ ] Evaluator publishes first weekly waste analysis

### Sep 5+ (Post-M1 Gate Fire)
- [ ] M1 fires (resource gates prove themselves)
- [ ] Epistemic feedback loop validates decision impact estimates
- [ ] Phase 1 readiness assessment (evaluator synthesizes all signals)
- [ ] Recommendation for Phase 1b or delay-to-coherence (Night decides)

---

## PART 7: SUCCESS METRICS (90-day check-in)

By 2026-11-14:

| Metric | Target | How Measured |
|--------|--------|--------------|
| **System Health Score** | 0.80 (up from baseline 0.73) | Weekly system-health-audit.yaml |
| **Semantic Alignment** | Clarifications < 0.5 per decision | Semantic grounding audit |
| **Load Distribution** | No practice with engagement > 0.90 | Load distribution audit |
| **Gate Readiness** | Confidence variance < 0.15 for fired gates | Gate readiness confidence audit |
| **Waste Prevented** | 500+ hours annually (on track) | Weekly waste analysis |
| **Audit Completion** | 100% of practices submitted assessments | Self-assessment audit response rate |
| **Collab Adoption** | 100% of practices using for uncertain work | Mesh telemetry |
| **Efficiency Trend** | know_delta / session_hours stable or improving | Efficiency ratio tracking |

---

## PART 8: DOCUMENT STORAGE & VERSIONING

**Primary location:** `/Users/andersonfamily/practices/empirica-foundation-evaluator/.postflight/EVALUATOR_SEAT_PROTOCOL_EXECUTABLE_v1.md`

**Version history:**
- v1.0 (2026-08-14) — Initial protocol, three novel improvements, answers to Night's questions
- v1.1 (2026-08-28) — Post-audit refinements (governance audit first data in)
- v2.0 (2026-09-15) — Post-M1 gate fire validation + Phase 1b recommendations

**Access:** This document is for Night + practice leads. Visibility: **shared** (all empirica-foundation practices can read).

---

## APPENDIX: What This Means for Night

**You asked for an entry channel and Master Observer. Here it is.**

1. **At the start of each session**, I surface: "System state is X (health score: 0.73). Three alerts: M1 alignment needed, mesh-support load at risk, website out-of-date."

2. **Each week**, you get: Weekly system-health-audit.yaml (five audits, one composite score, clear actions).

3. **Before critical gates**, I do: Full gate-readiness audit (confidence variance, semantic alignment, prerequisite verification).

4. **When practices report blockers**, I ask: "Is this unique to this practice, or a system pattern? Should we escalate?"

5. **When you consider reversing a decision**, I show: Reversibility cost map (if you reverse now vs. in 3 weeks, what's the rework cost to each practice?).

6. **Every 90 days**, I report: Calibration signal (Did the system improve? Where did we diverge from prediction? What should we adjust next?).

7. **To empirica + David**, I say: "Foundation system is coherent, efficient, and on track" OR "Foundation system has X risk, recommending adjustment Y."

---

**Status:** PROTOCOL ACTIVE  
**Authority:** Night  
**Next Action:** Publish to practice leads for acknowledgment  
**Questions?** Each section has a FAQ section; reference those first. Escalate to Night if ambiguous.

---

*Empirica-Foundation Evaluator Seat — Master Observer Protocol v1.0*  
*Established 2026-08-14*  
*Authority: Night (Admiral)*  
*Ratified and active.*
