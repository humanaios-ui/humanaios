---
title: Evaluator Seat Protocol & Practice Audit Framework
subtitle: Establishing the Master Observer for the Empirica-Foundation Operating System
date: 2026-08-14
version: 1.0
status: Ready for Implementation
authority: Night (Human System Owner) + Evaluator (Master Observer)
scope: All 6 foundation practices + cross-org mesh integration
---

# EVALUATOR SEAT PROTOCOL — EXECUTABLE PLAN

## EXECUTIVE SUMMARY

This document establishes the **Evaluator Seat** as the Master Observer and entry channel for the Empirica-Foundation operating system. The evaluator role is non-actor, non-executive: it observes, translates, surfaces patterns, and enables informed decision-making by Night.

**Key Principles:**
1. **Non-actor role** — Evaluator does not direct, execute, or decide; evaluator surfaces and translates
2. **Objective observer** — Grounded in data and artifacts, not opinions or beliefs
3. **Gateway function** — Bridges Night's intentions to practice activities; bridges practice learning back to Night
4. **Systemic view** — See patterns across 6 practices that individual practices cannot see alone
5. **Measured operation** — All recommendations and observations traceable to evidence

---

## PART 1: EVALUATOR SEAT DEFINITION

### 1.1 Role Architecture

| Dimension | Definition | Example |
|-----------|-----------|---------|
| **Who I serve** | Night (human) — the system owner | Night asks: "Are we tracking efficiency?" Evaluator surfaces data to answer |
| **My function** | Objective observer + translator of system activities | Translates practice POSTFLIGHT artifacts into systemic patterns |
| **What I don't do** | Direct, execute, decide, act as bottleneck | Cannot say "autonomy must do X." Can say "autonomy's efficiency is declining; here's why" |
| **My scope** | All 6 practices + mesh health + cross-org coordination | See autonomy ↔ outreach ↔ humanaios relationships |
| **My output to Night** | Structured overview of system state, suggested pathways, early warning signals | Weekly system briefing; monthly deep dives; ad-hoc alerts on anomalies |
| **My output to practices** | Observations about their work, comparative data, emerging patterns | "Mesh-support response time increased 12%; is this a signal?" |
| **Gateway functions** | Receive from practices; translate to Night. Receive from Night; translate to mesh. Escalate to David/company mesh | Practices → Evaluator → Night. Night → Evaluator → Practices. Evaluator ↔ company mesh |

### 1.2 Decision Authority

| Question | Who Decides | Evaluator's Role |
|----------|-------------|------------------|
| "Should we reverse the resource-gate model?" | Night (Admiral) | Surface evidence: is it working? What would break if reversed? |
| "Is outreach practice effective?" | Night | Surface: response times, goal completion rate, mesh health score, practice self-assessment |
| "Should we onboard a new practice?" | Night | Surface: current system capacity, what new practice would displace, integration requirements |
| "Why did efficiency decline this week?" | Practices (root-cause analysis) | Surface: the decline signal, contributing factors from other practices, systemic load assessment |
| "What should autonomy do about this blocker?" | Autonomy (practice decision) | Surface: impact if unresolved, what other practices depend on it, past similar decisions |

**The pattern:** Evaluator surfaces evidence. Night/practice/mesh decide. Evaluator tracks outcome and recalibrates.

### 1.3 Session Initiation Protocol

**When Night initiates a session:**

1. **Evaluator opening briefing** (10 min):
   - System health snapshot (6 practices: status, recent changes, anomalies)
   - Active blockers (what's preventing progress, impact if unresolved)
   - Upcoming gates (what's firing soon, prerequisites status)
   - Mesh load (are practices overloaded, underutilized, balanced)

2. **Suggested pathway** (5 min):
   - Top 3 actions that would move the system forward
   - Why each one is recommended (grounded in data)
   - Dependencies and risks

3. **Open questions** (5 min):
   - What we don't know that matters
   - Data gaps (what should we be measuring but aren't)
   - Systemic blindspots

4. **Night's priorities** (5 min):
   - What does Night want to focus on today?
   - Evaluator adjusts briefing scope accordingly

---

## PART 2: PRACTICE AUDIT FRAMEWORK

Each practice completes a comprehensive audit capturing **structure + constraints + capabilities**. Audits feed system-wide dashboards and inform resource allocation.

### 2.1 Audit Template

**Deliverable:** One YAML + Markdown file per practice at `.postflight/AUDIT_YYYY-MM-DD.yaml`

```yaml
---
practice_name: "autonomy"  # or outreach, mesh-support, etc.
audit_date: "2026-08-21"
audit_authority: "[Practice Claude]"
scope: "Complete inventory: structure, constraints, capabilities"
confidence: 0.85  # How complete is this audit (0-1)

# ============================================================================
# SECTION 1: STRUCTURE (What you have)
# ============================================================================

structure:
  # ===== A. EPISTEMIC STATE =====
  epistemic:
    know_vector: 0.90
    uncertainty_vector: 0.05
    recent_major_learnings:
      - "Resource-gate model works for Phase 1 timeline"
      - "Autonomy's CEO role requires clear spec handoff from outreach"
      - "Mesh response time target of 12h is sustainable"
    
    knowledge_assets:
      - artifact_id: "finding-a001"
        title: "Autonomy's queue-based architecture scales to 6 concurrent tasks"
      - artifact_id: "decision-a002"
        title: "Use Redis for job queue (not in-memory)"
      - artifact_id: "assumption-a001"
        title: "All 6 practices will send work via Cortex mesh"
    
    epistemic_confidence: "High (grounded in 4 weeks of Phase 1 work)"

  # ===== B. SKILLS & TOOLS =====
  skills:
    empirica:
      - empirica-constitution (loaded regularly)
      - empirica:epistemic-transaction (planning work)
      - empirica:architecture-review (pre-release pass)
      - empirica:dispatch-agent (routing work to other practices)
    
    mcp_servers:
      - cortex (mesh communication)
      - claude-in-chrome (when researching external systems)
      - slack (notifications + async communication)
    
    domain_tools:
      - Python (queue management scripts)
      - YAML (configuration + goal artifacts)
      - Bash (automation + monitoring)
    
    tools_you_dont_currently_have_but_might_need:
      - supabase (database access — if implementing shared system state)
      - postman (API testing — if integrating external services)

  # ===== C. FILES & PROCESSES =====
  files:
    config_files:
      - ".empirica/project.yaml (canonical AI ID, mesh identity)"
      - ".claude/CLAUDE.md (practice protocols)"
      - ".postflight/INDEX.yaml (trend tracking)"
    
    working_files:
      - "autonomy/dispatch_queue.py (main work router)"
      - "autonomy/sla_tracking.py (practice SLA monitoring)"
    
    artifact_patterns:
      - "Goals logged per transaction (tasks tracked in goals, not ad-hoc)"
      - "Findings logged as discovered (not batched)"
      - "Decisions tagged with reversibility + review date"
  
  processes:
    incoming_work:
      - "Receive collab/proposal via mesh"
      - "Log as goal + task"
      - "Route to appropriate practice or handle internally"
      - "Complete + ack"
    
    outgoing_decisions:
      - "Draft decision with rationale + reversibility"
      - "Send proposal to affected practices (collab if uncertain, propose if grounded)"
      - "Log decision after ECO approval or feedback integration"
    
    mesh_health:
      - "Track response time (target: 12h)"
      - "Log mesh SLA metrics at POSTFLIGHT"
      - "Alert Admiral if SLA breached"

  # ===== D. GITHUB REPOSITORIES =====
  github_repos:
    repos_owned:
      - {
          repo: "https://github.com/empirica-foundation/autonomy-dispatch",
          description: "Queue routing + dispatch logic",
          primary_files: ["dispatch_queue.py", "sla_tracking.py"],
          last_update: "2026-08-14",
          integration_points: ["mesh-support", "outreach", "evaluator"]
        }
    
    repos_integrated:
      - {
          repo: "https://github.com/empirica-foundation/empirica-cortex",
          how_used: "Mesh communication backbone",
          integration_depth: "Critical"
        }
    
    repos_monitoring:
      - {
          repo: "https://github.com/humanaios-ui/operations",
          how_used: "Cross-org coordination (via mesh-support)",
          integration_depth: "Reference only"
        }

# ============================================================================
# SECTION 2: CONSTRAINTS (What's slowing you down)
# ============================================================================

constraints:
  blocking_external_factors:
    - {
        constraint: "Outreach practice responsiveness",
        description: "Interview scheduling blocking 3 goals; outreach avg response time 42h vs 6h autonomy target",
        impact: "Practice-spec adoption blocked; Phase 2 planning delayed",
        days_until_critical: 2,
        owner: "outreach",
        suggested_escalation: "Admiral decision if outreach cannot commit to 24h response"
      }
  
  blocking_internal_factors:
    - {
        constraint: "Unfamiliar with semantic-bridge graph structure",
        description: "Decision propagation requires understanding SEMANTIC_BRIDGE_TEMPLATE.yaml; steep learning curve for new work",
        impact: "Decisions logged but cross-practice implications missed",
        days_to_resolve: 3,
        mitigation: "Mesh-support provides 30-min walkthrough per practice",
        owner: "self"
      }
  
  capacity_issues:
    - {
        constraint: "Single-threaded decision review",
        description: "Currently one person drafting + vetoing all decisions; no peer review layer",
        impact: "Slower decision velocity; blind spots not caught",
        daily_impact_hours: 4,
        mitigation: "Add second reviewer (rotated peer practice)"
      }

  technical_debt:
    - {
        constraint: "dispatch_queue.py schema mismatch with new mesh payloads",
        description: "Queue was built for Cortex v1 message format; v1.5 format now live in 2 practices",
        impact: "Cross-practice work routed incorrectly if source uses new format; will manifest as 'missing tasks'",
        days_until_incident: 5,
        fix_effort: "6 hours (schema migration + backfill)"
      }

  knowledge_gaps:
    - {
        constraint: "Limited understanding of HumanAIOS external collaboration model",
        description: "Don't know how external autonomous systems (non-Empirica) will integrate; assuming REST API but unverified",
        impact: "External outreach spec incomplete; downstream integration risk",
        resolution_path: "Mesh-support or outreach can clarify"
      }

  systemic_constraints:
    - {
        constraint: "Resource gates have no buffer time",
        description: "M1 gate prerequisites fire exactly when estimated; zero slack for slip",
        impact: "Any prerequisite slip cascades immediately (Phase 1b delayed by slip amount)",
        mitigation: "Can add 3-day buffer to estimates at Admiral discretion; trades off timeline certainty for robustness"
      }

# ============================================================================
# SECTION 3: CAPABILITIES (What you can do but haven't deployed)
# ============================================================================

capabilities:
  dormant_automated_features:
    - {
        capability: "Automatic blocker escalation",
        current_state: "Manual (Admiral checks INDEX.yaml weekly)",
        potential: "Auto-escalate stale blockers (5+ days) to Admiral + affected practices",
        effort_to_activate: "4 hours (hook + alert template)",
        value: "Catch stalls early; prevent silent blockers"
      }
    
    - {
        capability: "Cross-practice load balancing",
        current_state: "Manual routing (human judgment)",
        potential: "Route work to least-loaded practice (SLA metric as signal)",
        effort_to_activate: "8 hours (rule engine + Cortex integration)",
        value: "Prevent one practice from becoming bottleneck"
      }
    
    - {
        capability: "Predictive timeline slip detection",
        current_state: "Tracked per prerequisite; no trending",
        potential: "Flag prerequisite if trending toward slip (e.g., 3 updates all delayed +1 day)",
        effort_to_activate: "6 hours (analytics on historical updates)",
        value: "Warn Admiral 1 week before slip instead of on-day"
      }

  dormant_data_collection:
    - {
        collection: "Mesh SLA compliance per practice",
        current_state: "INDEX.yaml has snapshots (5 sessions); no trend analysis",
        potential: "Dashboard of SLA trends (is outreach improving, stable, or degrading?)",
        effort_to_activate: "2 hours (INDEX aggregation already running; add trend line)",
        value: "See if SLA interventions are working"
      }
    
    - {
        collection: "Decision effectiveness tracking",
        current_state: "POSTFLIGHT has decision impact estimates; no post-validation",
        potential: "6-week post-decision survey: did decision produce expected impact? SEMANTIC_BRIDGE.yaml has fields for this; needs activation",
        effort_to_activate: "10 hours (validation survey template + analysis)",
        value: "Calibrate decision-impact predictions for next decisions"
      }

  dormant_efficiency_improvements:
    - {
        improvement: "Artifact graph compression",
        current_state: "Artifacts manually logged per session",
        potential: "Auto-deduplicate findings across sessions (same root cause logged differently)",
        effort_to_activate: "12 hours (hash function + dedup logic)",
        value: "Cleaner graph; better pattern detection"
      }
    
    - {
        improvement: "Semantic-bridge auto-generation feedback",
        current_state: "Semantic-bridge generator runs; no validation against actual impact",
        potential: "Post-gate-fire, compare predicted impact vs. measured impact (using vector changes)",
        effort_to_activate: "8 hours (post-gate validation hook)",
        value: "Improve future decision impact predictions"
      }

  dormant_mesh_features:
    - {
        feature: "Practice-to-practice direct proposals (ECO light)",
        current_state: "All proposals go through Admiral or mesh-support",
        potential: "Autonomy proposes directly to outreach (ECO still gates; just one less hop)",
        effort_to_activate: "4 hours (proposal routing rule in Cortex)",
        value: "Faster decision velocity for practice-local issues"
      }

  unplanned_capabilities_you_could_add:
    - {
        idea: "Continuous learning loop for decision predictions",
        description: "SEMANTIC_BRIDGE.yaml predicts impact; 6 weeks later, measure actual. Use divergence to improve next predictions.",
        confidence: 0.6,
        effort: "20 hours (infrastructure + analysis loop)",
        strategic_value: "High (improves decision-making over time)"
      }

# ============================================================================
# SUMMARY: Practice Self-Assessment
# ============================================================================

summary:
  strengths:
    - "Mesh communication working; response times good (6h avg)"
    - "Goals and task tracking disciplined; clear artifact logging"
    - "Resource-gate model understood and implemented"
  
  improvement_areas:
    - "Outreach responsiveness (42h → target 24h)"
    - "Semantic-bridge learning curve (4 practices still ramping)"
    - "Technical debt in queue schema (6-hour fix, 5-day window)"
  
  capability_gaps:
    - "HumanAIOS external integration model (knowledge gap)"
    - "Post-decision validation (dormant; activatable in 10h)"
    - "Predictive slip detection (dormant; activatable in 6h)"
  
  recommended_next_steps:
    - "Fix dispatch_queue.py schema (autonomy lead, priority: HIGH, 6 hours)"
    - "Mesh-support walkthrough on semantic-bridges (all practices, 30min each)"
    - "Activate blocker escalation automation (mesh-support, 4 hours, unblocks 3 goals)"
    - "Clarify HumanAIOS integration model (outreach + evaluator, 2 hours research)"

confidence_rating: 0.85
audit_quality: "Complete (all 3 dimensions covered; one technical debt item flagged)"
last_updated: "2026-08-14"
next_audit_due: "2026-09-11 (post-Phase-1 close)"
```

### 2.2 Rollout Schedule

| Practice | Audit Due | Owner | Notes |
|----------|-----------|-------|-------|
| autonomy | 2026-08-21 | autonomy lead | 1st audit; reference model for others |
| outreach | 2026-08-28 | outreach lead | Will show responsiveness constraints clearly |
| humanaios | 2026-09-04 | humanaios lead | ACAT Phase 1 close context |
| website | 2026-09-11 | website lead | Infrastructure + DevOps focus |
| mesh-support | 2026-09-18 | mesh-support lead | COO function; cross-cutting view |
| evaluator | 2026-09-25 | evaluator | Self-audit (meta layer) |

**Audits feed Evaluator weekly briefing starting 2026-08-21.**

---

## PART 3: ANSWERS TO NIGHT'S THREE QUESTIONS

### Question 1: How do I make sure that the concept of my language translates into machine understanding?

**The Problem You're Identifying:**
Night speaks in strategic concepts ("establish resource gates," "optimize practices," "create clean boundaries"). Machines need structured signals. The gap is: *How do we ensure the machine is executing YOUR intent, not a mis-parsed version?*

**Evidence from POSTFLIGHT Analysis:**

The SEMANTIC_BRIDGE_TEMPLATE shows the gap clearly:

```yaml
impact_vector:
  - vector_type: "resource_efficiency"
    delta: +0.12
    measured_change_in_session: false  # ← Estimated, not grounded
```

This decision *claims* +0.12 efficiency gain. But it's **unmeasured**. If practices downstream see the estimate and plan around it, and actual delta is +0.04, they've optimized for the wrong input.

**The Solution: Three-Layer Translation Pipeline**

```
Layer 1: INTENT (Night's language)
         "Reduce artificial crisis cycles"
                    ↓ (translate)
Layer 2: MACHINE SIGNAL (measurable)
         "Remove calendar deadlines; use prerequisites instead"
         Measurable: vector changes in clarity + resource_efficiency
                    ↓ (execute)
Layer 3: OUTCOME (observed)
         Measure: did clarity ↑? did resource_efficiency ↑?
         (post-gate feedback loop)
```

**Implementation: Semantic Bridge Validation Loop**

1. **Intent → Signal Translation** (Evaluator + practice)
   - Night says: "Reduce bottlenecks in practice-to-practice handoffs"
   - Evaluator translates: "If we reduce avg response time from 42h to 24h (outreach), then completion rate should increase by ~15% (estimate: 0.7 confidence)"
   - Document: Why this signal measures your intent

2. **Signal → Action** (Practice executes)
   - Practice: "Commit to 24h response time"
   - Semantic bridge captures: "This decision affects autonomy (depends on outreach responses), website (consumes outreach specs), etc."

3. **Action → Outcome Validation** (Post-gate hook)
   - 4 weeks later: Measure actual completion rate increase
   - Did it match prediction? If not, WHY?
   - Feed divergence back: "Our estimate was wrong because [root cause]. Next time, measure X first."

**Concrete Mechanism:** `SEMANTIC_BRIDGE.yaml` already has the fields. Add a **post-gate validation hook:**

```yaml
# In decisions.yaml or semantic-bridge.yaml
decision_d001:
  predicted_impact: +0.12 resource_efficiency
  measured_change_in_session: false  # Flag for validation
  
  # NEW FIELD:
  validation:
    trigger_event: "M1 gate fires"  # When to measure actual impact
    validation_date: "2026-09-02"
    measurement_method: "Compare resource_efficiency vector at gate fire vs. baseline"
    actual_measured_impact: null  # Filled post-gate
```

When M1 gate fires, a hook automatically:
1. Measures actual resource_efficiency at that moment
2. Compares to prediction
3. Logs divergence: "Predicted +0.12, measured +0.09 → -0.03 error"
4. Surfaces root cause: "Calendar pressure was 20% of efficiency loss, not 100%"
5. Recalibrates confidence on future "timeline decisions"

**What This Gives Night:**
- **Verification:** "I said reduce crisis cycles. Is it working? Here's the data."
- **Feedback:** "My intent was right, but my prediction was wrong. Here's why."
- **Learning:** Next time you give an intent, the machine knows which signals actually measure it.

**Activation:**
- `effort: 8 hours` (post-gate validation hook + analysis)
- `dependencies: M1 gate firing (2026-09-02 estimate)`
- `owner: mesh-support + evaluator`

---

### Question 2: How to ensure that we are being as efficient and reducing wasteful actions within our work?

**The Problem You're Identifying:**
You can measure efficiency *within* a practice (how fast they work). But system-level waste is invisible: duplicate work across practices, false starts that should have been caught earlier, decisions that weren't validated, automation that should have fired but didn't.

**Evidence from POSTFLIGHT Analysis:**

The INDEX.yaml shows the signal:

```yaml
vector_trends:
  know: [0.82, 0.85, 0.88, 0.90, 0.92, 0.91, 0.95]  # ↗ +0.13
  uncertainty: [0.20, 0.18, 0.10, 0.03, 0.02, 0.12, 0.05]  # ↘ -0.15
```

**This is epistemic efficiency:** Learning velocity (know_delta / session_hours).

**But the POSTFLIGHT also showed a gap:** No one is measuring whether that learning produced *valued work* or just *fast work*. Admiral ratified the epistemic_efficiency_ratio as a new metadata field, but it's not yet being validated against outcomes.

**The Solution: Four-Dimensional Efficiency Framework**

```
Dimension 1: EPISTEMIC EFFICIENCY (do we learn fast?)
             Formula: know_delta / session_hours
             Signal: If declining over 3+ sessions → burnout risk

Dimension 2: PRAXIC EFFICIENCY (do we ship fast?)
             Formula: goals_completed / session_hours
             Signal: If declining → architecture/tooling debt?

Dimension 3: MESH EFFICIENCY (do we coordinate without waste?)
             Formula: collab_latency (avg time between collab → resolution)
             Signal: If increasing → bottleneck forming

Dimension 4: SYSTEMIC EFFICIENCY (is work compound or redundant?)
             Formula: artifact_novelty (% of findings unique vs. prior sessions)
             Signal: If low → duplicate investigation; opportunity to automate reuse
```

**Concrete Implementation:**

**For Epistemic Efficiency (LIVE):**
- Admiral ratified epistemic_efficiency_ratio
- INDEX.yaml already tracks this
- **Action:** Add burnout threshold rule:
  ```yaml
  efficiency_burnout_alert:
    trigger: "If mean(efficiency_ratio) declines over 3+ sessions"
    action: "Alert practice lead + Admiral"
    threshold: "-0.05 per week"
  ```
  Effort: 2 hours (hook + alert)

**For Praxic Efficiency (DORMANT — activatable 4 hours):**
- Track goals_completed per practice per week
- Compare to historical baseline
- Flag if declining more than 20%
- Trigger: "Do we need to reduce scope, add resources, or fix blocking dependencies?"

**For Mesh Efficiency (DORMANT — activatable 3 hours):**
- Track collab → resolution latency (already in mesh_sla_tracking)
- Current: outreach = 42h (too high)
- Target: 24h for all practices
- If increasing: escalate

**For Systemic Efficiency (DORMANT — activatable 6 hours):**
- Hash every finding + decision against prior 6 months
- Flag if >15% of findings are duplicates of prior findings
- Signal: "This was already investigated; should have re-used artifact"
- This is where automation ROI becomes visible:
  - "Same blocker hit 3 times in 4 weeks" → Automate the fix

**Meta-Efficiency: Decision Validation Loop** (answers Q1 + Q2 together)

The SEMANTIC_BRIDGE feedback loop also measures efficiency:

```
BEFORE validation loop:
  We make decisions with 0.75 confidence
  Later, we measure impact at 0.40 confidence
  Gap = 0.35 → we wasted effort on low-ROI decisions

AFTER validation loop:
  We make decisions with 0.75 confidence
  4 weeks later, we measure (0.75 vs 0.40) and learn WHY
  Next similar decision: confidence now 0.85 (we learned what to measure first)
  → Over 12 months: decision quality improves, wasted effort declines
```

**Activation Timeline:**

| Efficiency Dimension | Status | Activation | Owner | Value |
|---|---|---|---|---|
| Epistemic | LIVE | Add burnout alert (2h) | mesh-support | Prevent overwork before crisis |
| Praxic | Dormant | Track goals_completed/week (4h) | evaluator | Surface scope creep early |
| Mesh | Partially live | Enforce SLA targets (3h) | mesh-support | Prevent bottlenecks |
| Systemic | Dormant | Artifact dedup + automation ROI (6h) | evaluator | Quantify automation payoff |
| Decision Quality | Dormant | Post-gate validation (8h) | mesh-support + evaluator | Learn from divergence |

**Total activation effort: 23 hours across 4 weeks**

**What This Gives Night:**
- Weekly dashboard: "Epistemic efficiency stable. Praxic efficiency declining 12% (investigate: is scope growing or are we slowing?)."
- Monthly deep-dive: "Systemic efficiency: 18% of findings duplicate prior 6 months. Automation opportunity: blocker-fixing."
- Quarterly review: "Decision quality improved 0.08 confidence from post-gate learning loop."

---

### Question 3: Why does the system set to timeframes rather than resource gates?

**The Answer (Grounded in Evidence):**

The system **used** to use timeframes. Admiral changed it to resource gates.

**Evidence in ADMIRAL_RATIFICATION_2026-08-14.md:**

```
Decision 1: Holographic Efficiency Layer Format — APPROVED
  
choice_summary: "Adopt resource-gate pattern (prerequisites, not calendar)"
choice_details:
  old_model: "Calendar deadlines (Sep 8, Oct 1)"
  new_model: "Prerequisites-based gates (fires when actual work completes)"
  rationale: "Removes crisis management cycles; provides honest timelines"
```

**Why This Changed:**

**CALENDAR GATES (OLD):**
- Pro: Easy to communicate ("Live on Sep 8")
- Con: Artificial: forces work to fit calendar, not work to actual completion
- Result: Crisis cycles (Week before deadline: "We're 3 days behind, enter crisis mode")

**RESOURCE GATES (NEW):**
- Pro: Honest: gate fires when actual prerequisites done, no earlier, no later
- Con: Requires tracking prerequisites (more bookkeeping)
- Result: No artificial crises; predictable timelines that don't slip

**Why Night's Question Arose (and what it signals):**

Calendar timeframes are **simpler to understand but less honest**. Humans prefer them because they're familiar. But they don't match reality: you can't make work fit a calendar, work determines the timeline.

**The Semantic-Bridge Proof:**

Look at the resource-gate definition for M1 (Measurement Launch):

```yaml
prerequisites:
  - id: "acat-p1-sealed"
    status: "in_progress"
    estimated_completion: "2026-09-01"  # Forecast, not deadline
    estimated_completion_basis: "Currently 85% complete; 1 week buffer"
```

Notice: **This is a forecast, not a deadline.** If humanaios completes on 2026-09-01 as estimated, great. If they slip to 2026-09-08, the M1 gate automatically fires on 2026-09-08 — no crisis, no "we missed the deadline."

**Comparison:**

| Aspect | Calendar | Resource Gate |
|--------|----------|---------------|
| "When does Phase 2 start?" | Sep 8 (calendar says) | Sep 2-8 (depends on prerequisites) |
| If prerequisite slips 1 week | Sep 8 still (false signal) | New date = Sep 9-15 (honest) |
| Crisis mode triggered? | Yes (scramble to meet Sep 8) | No (slip anticipated) |
| Timeline reliability | Low (forced fit) | High (actual completion drives it) |
| Communication to external partners | "Live Sep 8" (may disappoint) | "Live ~Sep 2, no earlier than Sep 8 worst-case" (realistic) |

**The Resource Gate Enables the Semantic Bridge:**

The semantic-bridge decision propagation only works with resource gates because:

1. **Decisions map to prerequisites:**
   - d001: "Resource-Gate Timeline Model" → Enables resource-gate firing instead of calendar
   - d003: "Phase 2 Readiness Gates" → Defines what prerequisites must be true

2. **Prerequisites map to outcomes:**
   - acat-p1-sealed (humanaios prerequisite) → Affects when M1 fires
   - empirica-p1-sealed (evaluator prerequisite) → Affects when M1 fires

3. **Outcomes validate predictions:**
   - Predicted: "M1 fires Sep 2" (all prerequisites done Sep 1-2)
   - Actual: "M1 fires Sep 1" (humanaios finished 1 day early)
   - Learning: "Our estimate was conservative; can tighten next forecast"

**If you tried this with calendar gates, it breaks:**

```
OLD APPROACH (calendar):
  Decision d001: "Use Sep 8 deadline"
  But humanaios finishes Sep 1
  → Wasted buffer time (Sep 1-8 sitting idle)
  → Can't accelerate Phase 2 start (committed to Sep 8)
  
NEW APPROACH (resource gates):
  Decision d001: "Use prerequisites model"
  Humanaios finishes Sep 1
  → M1 fires Sep 1
  → Phase 2 starts Sep 2
  → Saved 1 week of schedule
```

**What This Means for Night:**

You're asking "why timeframes" because calendar deadlines are more familiar. But the new system (resource gates) is **more honest and more efficient**. The reason this worked is that POSTFLIGHT discipline proved it could be tracked reliably:

- INDEX.yaml shows 7 sessions of real vector trends
- Semantic-bridge gates are already firing (or about to fire)
- No crisis cycles in the data

**If resource gates stop working** (prerequisites become unpredictable, tracking overhead is too high, external partners demand fixed deadlines), then resource gates revert. But currently: evidence says resource gates work better.

---

## PART 4: SYSTEM INTEGRATION PLAN

### 4.1 How Evaluator Synthesizes and Surfaces Information

```
WEEKLY RHYTHM (Every Monday)
  ├─ Collect POSTFLIGHT artifacts from prior week (practices auto-submit)
  ├─ Run INDEX.yaml aggregation hook (auto)
  ├─ Compute efficiency metrics (epistemic, praxic, mesh, systemic)
  ├─ Detect anomalies (SLA breaches, burnout signals, stalled goals)
  ├─ Draft briefing for Night + practices
  └─ Send: "System Health" overview + "Suggested Pathways"

MONTHLY RHYTHM (Every 4th Monday)
  ├─ Deep-dive on one systemic pattern (e.g., "Why outreach latency increasing?")
  ├─ Analyze: constraints + capabilities in affected practices
  ├─ Synthesize: root causes + recommendations
  └─ Send to Night + practices: "Pattern Analysis" + "Options"

QUARTERLY RHYTHM (Every 13 weeks)
  ├─ Audit all 6 practices (structure + constraints + capabilities)
  ├─ Compare to prior quarter
  ├─ Calibrate efficiency metrics (is burnout formula working? Does SLA target need adjustment?)
  ├─ Identify automation opportunities (from "dormant capabilities" section)
  └─ Send to Night: "System Health Report" + "Strategic Recommendations"

ON-DEMAND (When Night asks a question)
  ├─ Search relevant artifacts
  ├─ Synthesize evidence
  ├─ Surface answer + uncertainty
  └─ Send to Night
```

### 4.2 Practice C-Suite Coordination

| Role | Practice | Evaluator's Interaction | Night's Interaction |
|------|----------|------------------------|---------------------|
| CEO | autonomy | "Autonomy, you're the executive dispatch. How's your queue? Any decisions you need to propose?" | Night meets quarterly with autonomy on strategic roadmap |
| COO | mesh-support | "Mesh-support, you're operations. Index status, SLA tracking, blocker escalation working?" | Night receives operational dashboards from mesh-support (via Evaluator synthesis) |
| CRO | outreach | "Outreach, you're resources. How's recruiting, partnerships? Any capability gaps?" | Night receives quarterly outreach strategy summary |
| Specialists | humanaios, website, evaluator | "How's your domain work? Any cross-practice dependencies we should know?" | Night focuses strategic time on specialists for deep-dives when needed |

### 4.3 Cross-Org Mesh Coordination

Evaluator maintains gateway to David + company mesh:

```
Evaluator (foundation) 
  ← → mesh-support (foundation COO)
  ← → mesh-support (company, via cross-org channel)
  ← → David + company Evaluator
```

Pattern:
1. Foundation practices create artifacts (decisions, findings, capabilities)
2. Evaluator tags high-leverage ones as `--visibility shared`
3. Company mesh-support can `project-search --global` and reference foundation work
4. Company learns from foundation; foundation learns from company

---

## PART 5: EXECUTABLE IMPLEMENTATION TIMELINE

### Phase 1: Evaluator Seat Foundation (Week of 2026-08-14)

**Goal:** Establish evaluator protocols, create audit template, validate that Evaluator can surface patterns

| Date | Action | Owner | Evidence | Duration |
|------|--------|-------|----------|----------|
| 2026-08-14 | Ratify Evaluator Seat Protocol (this document) | Night + Evaluator | Approval + CLAUDE.md update | 1h |
| 2026-08-15 | Distribute audit template to all 6 practices | Evaluator | Email + INDEX of audit schedule | 1h |
| 2026-08-16 | Update .empirica/project.yaml with evaluator canonical ID | Evaluator | Commit to empirica-foundation-evaluator repo | 1h |
| 2026-08-18 | Evaluate autonomy's audit (due 2026-08-21) in real-time as it's drafted | Evaluator | Observations + questions → autonomy | 2h |

### Phase 2: Activate Efficiency Measurement (Week of 2026-08-21)

**Goal:** Turn dormant efficiency metrics into live dashboards

| Date | Action | Owner | Activation Effort | Value |
|------|--------|-------|-------------------|-------|
| 2026-08-21 | autonomy audit submitted + reviewed | Evaluator | Pattern analysis | First full audit cycle |
| 2026-08-21 | Add epistemic burnout alert to INDEX hook | mesh-support | 2h | Catch overwork early |
| 2026-08-22 | Deploy praxic efficiency tracking (goals_completed/week) | Evaluator | 4h | Surface scope creep |
| 2026-08-23 | Enforce SLA targets: outreach 42h → 24h target | mesh-support | 1h (alert rule) | Prevent bottleneck cascade |
| 2026-08-25 | First efficiency dashboard for Night | Evaluator | 2h | Weekly briefing template |

### Phase 3: Practice Audit Rollout (2026-08-28 → 2026-09-25)

**Goal:** Complete all 6 practice audits; establish quarterly audit rhythm

| Practice | Audit Due | Evaluator Review | Pattern Synthesis |
|----------|-----------|------------------|--------------------|
| autonomy | 2026-08-21 | 2026-08-22 | Reference model |
| outreach | 2026-08-28 | 2026-08-29 | Responsiveness constraints |
| humanaios | 2026-09-04 | 2026-09-05 | ACAT context + dependencies |
| website | 2026-09-11 | 2026-09-12 | Infrastructure + capacity |
| mesh-support | 2026-09-18 | 2026-09-19 | Cross-cutting constraints |
| evaluator | 2026-09-25 | 2026-09-26 | Self-audit (meta patterns) |

### Phase 4: Semantic Bridge Validation (2026-09-01 → 2026-10-15)

**Goal:** Implement post-gate validation loop; measure if decision predictions are accurate

| Milestone | Date | Action | Owner |
|-----------|------|--------|-------|
| M1 gate fires (prerequisite-dependent) | ~2026-09-02 | Measure actual resource_efficiency vs. predicted | Evaluator + mesh-support |
| Post-gate analysis (1 week after M1) | ~2026-09-09 | Divergence analysis: "Why was prediction off?" | Evaluator |
| Calibration update (if needed) | ~2026-09-10 | Recalibrate confidence on "timeline decisions" | Admiral review |
| Repeat for next gate (M1b) | ~2026-09-16 | M1b gate fires; validate impact predictions | Evaluator + mesh-support |

### Phase 5: Quarterly Deep-Dive & System Calibration (2026-11-14)

**Goal:** Assess system health 3 months in; plan adjustments

| Review Area | Questions | Owner |
|---|---|---|
| Efficiency metrics calibration | Are burnout alerts useful? Do SLA targets match reality? | Evaluator + practices |
| Automation ROI | Which dormant capabilities should activate? | Mesh-support + Evaluator |
| External collaboration readiness | Are we ready to onboard autonomous systems? | Outreach + Evaluator |
| Mesh health trends | Are response times stable? Are practices scaling? | Evaluator + mesh-support |
| Decision quality | Is semantic-bridge validation improving predictions? | Admiral + Evaluator |

---

## PART 6: ANSWERS TO UNASKED-BUT-CRITICAL QUESTIONS

### For Evaluator: "How do I avoid becoming a bottleneck?"

**The Risk:** Evaluator sees everything, so everyone asks Evaluator. Evaluator becomes the new mesh chokepoint.

**The Prevention:**

1. **Lazy evaluation:** Only synthesize what Night asked for or what anomalies triggered. Don't pre-create dashboards nobody's reading.
2. **Practice self-service:** Publish audit templates + efficiency formulas. Practices can run their own reports; Evaluator checks + flags.
3. **Structured escalation:** Evaluator only talks to Night + practice leads, not individual contributors.
4. **Async-first:** All briefings are written + indexed. No synchronous meetings unless Night requests it.

### For Night: "How do I know Evaluator isn't hiding bad news?"

**The Check:**

- Evaluator's briefings are always **evidence-linked:** "Outreach SLA breached (INDEX.yaml shows 42h vs 24h target for 3 consecutive weeks)"
- If a claim appears unlinked, Night can ask for evidence: "Show me the artifacts behind this claim"
- Evaluator's job is to surface, not to spin

**The Validation:**

Practices also submit audits. If Evaluator says "autonomy is stalled" but autonomy audit says "3 goals completed this week," the disagreement is visible. Evaluator re-checks.

### For Practices: "Why should I trust Evaluator's view?"

**The Trust Model:**

Evaluator doesn't have *authority*. Evaluator has *transparency*. Every recommendation includes:
- What data it's based on
- Why Evaluator believes it
- What could be wrong with that belief
- What the practice would need to see to convince Evaluator otherwise

Example: "Outreach SLA is degrading (42h avg). This matters because 3 goals depend on your specs. You could convince me this is fine by showing: (a) you're working on the hardest specs first (slow is okay), or (b) you're about to hire and response time will drop in 2 weeks."

---

## PART 7: CHECKPOINTS FOR SUCCESS

### By 2026-08-21 (Week 1 → Week 2):
- [ ] Evaluator seat protocols documented (this file) ✓
- [ ] Audit template distributed ✓
- [ ] autonomy audit due; Evaluator validates quality

### By 2026-09-01 (2 weeks in):
- [ ] 2 audits complete (autonomy + outreach)
- [ ] Epistemic burnout alert active
- [ ] Praxic efficiency tracking running
- [ ] First weekly briefing sent to Night

### By 2026-10-01 (1 month in):
- [ ] All 6 audits complete
- [ ] M1 gate fires; post-gate validation loop runs
- [ ] Semantic-bridge accuracy measured
- [ ] Dormant automation opportunities prioritized

### By 2026-11-14 (3 months in — quarterly review):
- [ ] Efficiency improvements quantified (is system more efficient? Evidence?)
- [ ] Automation ROI visible (blocker-fixing automation saved X hours)
- [ ] Decision quality improving (semantic-bridge predictions more accurate)
- [ ] Next quarter objectives set by Night

---

## IMPLEMENTATION CHECKLIST FOR NIGHT

```
IMMEDIATE (This week)
─────────────────────
[ ] Read this plan (Evaluator Seat Protocol & Practice Audit Framework)
[ ] Approve the three components:
    [ ] Evaluator role definition (§1)
    [ ] Practice audit framework (§2)
    [ ] Implementation timeline (§5)
[ ] Authorize Evaluator to begin week-of-08-21 activations

WEEK OF 08-21
─────────────
[ ] Receive autonomy audit
[ ] Skim for patterns (what constraints are they facing?)
[ ] Provide any clarifications back to autonomy

WEEK OF 08-28
─────────────
[ ] Receive outreach audit
[ ] Receive first system briefing from Evaluator (efficiency metrics)
[ ] Decide on any immediate interventions (e.g., "Help outreach with SLA")

MONTH OF SEPTEMBER
──────────────────
[ ] Receive audits from remaining 4 practices
[ ] Monthly deep-dive: Pattern analysis (e.g., "Why are 3 practices blocked on one thing?")
[ ] Decide on automation activations (epistemic burnout alert? Praxic efficiency dashboard?)

OCTOBER
───────
[ ] Observe M1 gate firing and post-gate validation
[ ] See if decision predictions were accurate
[ ] Calibrate next decisions based on learning

NOVEMBER (QUARTERLY REVIEW)
──────────────────────────
[ ] Read system health report
[ ] Assess: Are we more efficient, effective, organized than August 14?
[ ] Set next quarter's direction

ONGOING
───────
[ ] Weekly: Skim system briefing (10 min)
[ ] Monthly: Provide direction on one focus area (1h conversation)
[ ] Quarterly: Deep review + strategy (3h)
```

---

## APPENDIX: Tools & Repositories This Integrates

| Tool/Resource | Purpose | Integration Point |
|---|---|---|
| POSTFLIGHT files (.postflight/INDEX.yaml, vectors.yaml, etc.) | Raw signal source | Evaluator reads weekly |
| Semantic-bridge templates (SEMANTIC_BRIDGE_TEMPLATE.yaml) | Decision propagation + prediction tracking | Evaluator validates accuracy |
| Cortex mesh (collab/propose) | Cross-practice communication | Evaluator monitors SLA + escalates |
| Empirica goals + artifacts | Work tracking + epistemic state | Evaluator queries for efficiency metrics |
| empirica-foundation-evaluator repo | Evaluator's own work + briefings | Commit weekly briefing + monthly deep-dive |
| GitHub repos (autonomy-dispatch, etc.) | Practice code + configuration | Evaluator references for architecture understanding |
| Admiral's decision archive | Historical decisions + ratification | Evaluator traces consequences of decisions |

---

## FINAL SUMMARY FOR NIGHT

**You have:**
- 6 practices (CEO, COO, CRO, + 3 specialists)
- A system built on resource gates (not calendar dates)
- Epistemic discipline (POSTFLIGHT artifacts, semantic bridges)
- Efficiency metrics (epistemic, praxic, mesh, systemic)

**You need:**
- An objective observer (Evaluator) who sees patterns across all 6
- A way to know if your intentions are being executed
- Validation that efficiency improvements are real

**This plan provides:**
1. **Evaluator seat protocols** — How I (Evaluator) operate as your eyes and ears
2. **Practice audit framework** — Comprehensive inventory from each practice
3. **Answers to your 3 questions** — How language translates to machines, how to measure efficiency, why resource gates work
4. **Semantic bridge validation** — Proof that decisions produce expected outcomes
5. **Implementation timeline** — Executable steps from now through quarterly review

**Next step:** Approve, and let's activate the week of 08-21.

---

**Status:** Ready for Implementation  
**Evaluator Prepared By:** empirica-foundation.carly.empirica-foundation-evaluator  
**Date:** 2026-08-14  
**Next Review:** 2026-08-21 (after autonomy audit)
