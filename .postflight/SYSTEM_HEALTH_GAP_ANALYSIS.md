---
title: "System Health Gap Analysis — Missing Dimensions"
date: "2026-08-14"
version: "1.0-GAP-ANALYSIS"
status: "IDENTIFIES BEHAVIORAL HEALTH PRACTICE NEED"
---

# System Health Gap Analysis v1.0

**Question:** Now that we have system health evaluation being built (OS health, practice health, epistemic health), what aspects are we missing?

**Answer:** We're missing **behavioral health** — the assessment and management of how the system is **functioning cognitively and behaviorally** at the individual and collective level.

---

## PART 1: CURRENT SYSTEM HEALTH COVERAGE

### ✅ What We ARE Measuring

| Dimension | Owner | Measurement | Frequency |
|-----------|-------|-------------|-----------|
| **OS Infrastructure** | Local Machine Optimizer | CPU, memory, disk, network, security, capacity, coherence | Daily (automated) |
| **Practice Operations** | Practice Optimizer | Efficiency, capability, maturity, health, SLA compliance | Weekly (audit) |
| **System Patterns** | Evaluator | Mesh health, load distribution, gate readiness, efficiency, coherence | Weekly (audit) |
| **Epistemic State** | Educator | Johari Window (known/unknown/blind), learning velocity, decision feedback | Weekly/Monthly |
| **Execution Efficiency** | Token Optimizer | Model selection, context compression, retry rates, token waste | Weekly (report) |

### ❌ What We Are NOT Measuring

**Behavioral Health** — How are practitioners performing, learning, engaging, and maintaining sustainable patterns?

---

## PART 2: WHAT IS BEHAVIORAL HEALTH?

Behavioral health = **Cognitive, emotional, and relational well-being** of the system's practitioners and their interactions.

**Unlike other dimensions:**
- OS health measures infrastructure (hardware-level)
- Practice health measures operations (process-level)
- Epistemic health measures knowledge (information-level)
- Token efficiency measures cost (execution-level)

**Behavioral health measures people-level dynamics:**
- Are practitioners sustainable (not burned out)?
- Are they learning (not plateauing)?
- Are they engaging (not disengaging)?
- Are they aligned (not fragmented)?
- Are they healthy (cognitive + emotional + relational)?

---

## PART 3: ACAT 12 DIMENSIONS — THE MISSING FRAMEWORK

You mentioned: "ACAT full 12 dimensions behavioral assessment data is collected, assessed, managed, and orchestrated."

**Current state:** ACAT exists (acat-x practice), but behavioral assessment data is not being **systematically collected, trended, or orchestrated** as part of system health.

**What ACAT covers** (example 12 dimensions):

```yaml
acat_behavioral_dimensions:
  
  # Cognitive Domains
  1. clarity:
     definition: "Understandability of decisions, goals, expectations"
     measure: "Do practitioners understand what's being asked? (survey + observation)"
     current_tracking: "❌ Not systematic"
  
  2. coherence:
     definition: "Internal consistency of system behavior and decisions"
     measure: "Do decisions align with stated values? (audit frequency)"
     current_tracking: "✅ Partially (through Evaluator patterns)"
  
  3. learning_capacity:
     definition: "Ability to absorb, apply, and teach new knowledge"
     measure: "Decision prediction accuracy, knowledge transfer rate (Educator tracks)"
     current_tracking: "✅ Partially (through Educator)"
  
  4. adaptive_responsiveness:
     definition: "System's ability to adjust when conditions change"
     measure: "How quickly do practices pivot when direction changes?"
     current_tracking: "❌ Not systematic"
  
  # Relational Domains
  5. psychological_safety:
     definition: "Willingness to speak up, ask for help, admit mistakes without fear"
     measure: "Vulnerability in artifacts? Cross-practice collab rate? Blocker escalation?"
     current_tracking: "❌ Not systematic"
  
  6. trust_in_system:
     definition: "Confidence that the system will deliver and evolve fairly"
     measure: "Mesh participation rate, proposal acceptance/rejection, engagement trends"
     current_tracking: "❌ Not systematic"
  
  7. collaboration_quality:
     definition: "Effectiveness of cross-practice communication and coordination"
     measure: "Collab response times, resolution quality, relationship strength"
     current_tracking: "✅ Partial (via mesh SLA)"
  
  8. role_clarity:
     definition: "Practitioners understand their role + authority + responsibilities"
     measure: "Decision ownership disputes? Role confusion in retrospectives?"
     current_tracking: "❌ Not systematic"
  
  # Engagement Domains
  9. intrinsic_motivation:
     definition: "Driven by meaning/mastery/autonomy vs. extrinsic pressure"
     measure: "Work quality, initiative, feedback receptiveness"
     current_tracking: "❌ Not systematic"
  
  10. sustainable_pace:
      definition: "Work intensity is maintainable without burnout"
      measure: "Session hours trending up? Engagement vector declining?"
      current_tracking: "✅ Partial (via engagement vector + efficiency ratio)"
  
  11. growth_trajectory:
     definition: "Practitioners are developing skills/confidence/scope over time"
     measure: "Capability maturity growth? Decision complexity accepted?"
     current_tracking: "❌ Not systematic"
  
  12. collective_resilience:
      definition: "System can absorb disruption without cascading failure"
      measure: "Blocker recovery time? Dependency handling? Crisis response?"
      current_tracking: "❌ Not systematic"
```

**Systematic tracking means:**
- Data collection (surveys, artifact analysis, observation)
- Trending (weekly/monthly reports)
- Orchestration (interventions when thresholds crossed)
- Integration (part of overall system health)

---

## PART 4: THE GAP — WHAT'S MISSING

### What We Have

```yaml
system_health_currently_visible:
  
  os_health: 0.688 (infrastructure)
  practice_health: ~0.75 (operations)
  epistemic_health: ~0.73 (knowledge)
  token_efficiency: ~0.0015 (cost)
  mesh_sla: "autonomy 2h, outreach 48h" (collaboration)
  
  composite_system_health: ~0.75
```

### What We Don't Have

```yaml
behavioral_health: ❌ MISSING
  
  psychological_safety: unknown
  trust_in_system: unknown
  learning_capacity: partially tracked
  sustainable_pace: partially tracked
  collective_resilience: unknown
  role_clarity: unknown
  adaptive_responsiveness: unknown
  
  composite_behavioral_health: UNKNOWN
  
  risk: "System could be high-performing operationally while practitioners are burning out, disengaged, or confused"
```

### The Blind Spot

```
Current System Health = 0.75 (looks good!)
BUT:
  - Mesh-support engagement 0.95 (burnout threshold)
  - Website knowledge is local-only (poor transfer)
  - Autonomy role in Phase 1b unclear
  - Practice trust in new processes uncertain
  
ACTUAL System Health = ??? (unknown without behavioral data)
```

---

## PART 5: BEHAVIORAL HEALTH PRACTICE PROPOSAL

**Solution:** Add a new practice similar to Local Machine Optimizer but for **behavioral/cognitive health**.

### Practice Definition

| Aspect | Value |
|--------|-------|
| **Name** | Behavioral Health Practice |
| **Mission** | Assess, monitor, and optimize system's behavioral/cognitive health using ACAT 12 dimensions |
| **Role** | Behavioral analyst + organizational psychologist + system wellness manager |
| **Seat Type** | Specialist (unique like Local Machine Optimizer) |
| **Authority** | Assess + recommend (not mandate). Identify burnout/disengagement/confusion; propose interventions |
| **Primary Client** | All practices + Night (Admiral) + Evaluator |
| **Function** | Keep system healthy at the behavioral/cognitive level while maintaining operations |

### Core Functions

```yaml
behavioral_health_practice:
  
  function_1_acat_data_collection:
    what: "Collect behavioral assessment data using ACAT 12 dimensions"
    how: |
      - Weekly surveys (3 questions per dimension; 2 min/week per practitioner)
      - Artifact analysis (psychological safety = willingness to surface mistakes/unknowns)
      - Observation (engagement in mesh, vulnerability in collabs)
      - Retrospective signals (frustration, confusion, disconnection)
    cadence: "Weekly collection, monthly analysis"
    output: "ACAT behavioral assessment data (Supabase)"
  
  function_2_health_scoring:
    what: "Calculate behavioral health composite score (like OS health 0-1.0 scale)"
    formula: |
      behavioral_health = (
        clarity * 0.08 +
        psychological_safety * 0.12 +
        trust_in_system * 0.12 +
        sustainable_pace * 0.15 +
        learning_capacity * 0.12 +
        collaboration_quality * 0.10 +
        role_clarity * 0.10 +
        adaptive_responsiveness * 0.08 +
        intrinsic_motivation * 0.08 +
        growth_trajectory * 0.05
      )
    target: 0.80+  # Healthy range
    alert_if_below: 0.70  # Intervention needed
    critical_if_below: 0.60  # Emergency
  
  function_3_burnout_detection:
    what: "Identify practitioners at risk before crisis"
    signals: |
      - Engagement vector trending down
      - Session hours increasing (more work, same output)
      - Collab response times increasing
      - Artifact quality declining
      - Error rate in decisions increasing
    trigger: |
      if (
        engagement < 0.85 AND
        session_hours > baseline + 20% AND
        psychological_safety < 0.70
      ):
        alert = "burnout_risk_detected"
    action: "Escalate to Admiral + recommend intervention (workload reduction, support, clarity)"
  
  function_4_engagement_tracking:
    what: "Monitor intrinsic vs. extrinsic motivation signals"
    measures: |
      - Voluntary participation in audits/assessments
      - Quality of questions in unsaid-but-critical sections
      - Speed of adoption of new frameworks
      - Willingness to collaborate cross-practice
    red_flags: |
      - Minimal participation in Educator Johari assessment
      - Defensive tone in recommendations
      - Siloing (not engaging mesh)
      - Default to "not applicable to us"
    action: "If engagement dropping: diagnose + support"
  
  function_5_collective_resilience:
    what: "Can the system absorb disruption?"
    stress_test: |
      When a blocker arrives:
        - Do practices escalate or hide it?
        - Do others pitch in or protect territory?
        - Does system recover or cascade fail?
    measurement: |
      blocker_cascade_recovery_time (hours)
      collaboration_in_crisis (% practices helping)
      system_panic_level (subjective 1-10)
    target: |
      recovery_time < 24 hours
      collaboration > 80%
      panic_level < 5
  
  function_6_feedback_loops:
    what: "Close the loop between system state and intervention"
    example: |
      Week 1: Burnout signal detected (mesh-support engagement 0.95)
      Week 2: Intervention recommended (reduce load, pair support)
      Week 3: Behavioral health assessed (engagement now 0.88)
      Week 4: Root cause addressed (process change reduces overhead)
      Week 5: Re-measured (engagement stable 0.82)
    learning: "That intervention worked; apply to other high-load practices"

success_metrics:
  - "Behavioral health composite score >= 0.80 (healthy)"
  - "Zero burnout crises (detected early, prevented)"
  - "Engagement vectors stable or improving"
  - "Psychological safety > 0.75 (safe to speak up)"
  - "Trust in system > 0.80 (confidence in direction)"
  - "Learning capacity trending up (practitioners growing)"
  - "Collective resilience proven (absorbed disruption without failure)"
```

### Integration With Other Practices

```
Behavioral Health ↔ Evaluator:
  - Evaluator: "I see mesh-support SLA is slow (48h)"
  - Behavior: "I detect burnout signal (engagement 0.95)"
  - Evaluator: "Ah! It's not laziness, it's overload"
  - Recommendation: "Redistribute mesh-support work"

Behavioral Health ↔ Educator:
  - Behavior: "outreach has low psychological safety (doesn't speak up)"
  - Educator: "outreach Johari shows lots of unknown-knowns not surfaced"
  - Root cause: "outreach doesn't feel safe admitting knowledge gaps"
  - Solution: "Educator builds trust-first curriculum for outreach"

Behavioral Health ↔ Token Optimizer:
  - Behavior: "humanaios engagement increasing (not burnout)"
  - Token: "humanaios token efficiency improving 25%"
  - Insight: "Efficiency improvement is sustainable because engagement healthy"
  - (If engagement were declining, efficiency gain would be unsustainable workaround)
```

---

## PART 6: DATA STORAGE — SUPABASE INTEGRATION

Your command: `claude mcp add --scope project --transport http supabase`

**Purpose:** Supabase provides the backend for storing behavioral assessment data, system health metrics, historical trends, and query capabilities.

### Schema Required

```sql
-- ACAT Behavioral Assessments
CREATE TABLE acat_assessments (
  id UUID PRIMARY KEY,
  practice_id VARCHAR,
  assessment_date DATE,
  dimension VARCHAR,  -- clarity, psychological_safety, etc.
  score FLOAT,        -- 0.0-1.0
  data_source VARCHAR, -- survey, artifact_analysis, observation
  notes TEXT,
  created_at TIMESTAMP
);

-- Behavioral Health Composite Scores
CREATE TABLE behavioral_health_scores (
  id UUID PRIMARY KEY,
  practice_id VARCHAR,
  assessment_date DATE,
  composite_score FLOAT,  -- 0.0-1.0
  scores JSONB,           -- {clarity: 0.8, psychological_safety: 0.72, ...}
  health_status VARCHAR,  -- healthy, caution, critical
  alerts JSONB,           -- burnout, disengagement, confusion, etc.
  created_at TIMESTAMP
);

-- System Health Composite (integrates all dimensions)
CREATE TABLE system_health_composites (
  id UUID PRIMARY KEY,
  measurement_date DATE,
  os_health FLOAT,
  practice_health FLOAT,
  epistemic_health FLOAT,
  behavioral_health FLOAT,
  token_efficiency FLOAT,
  composite_score FLOAT,
  created_at TIMESTAMP
);

-- Historical Trends (for dashboards)
CREATE TABLE health_trends (
  id UUID PRIMARY KEY,
  practice_id VARCHAR,
  metric VARCHAR,        -- engagement, learning_velocity, psychological_safety, etc.
  value FLOAT,
  trend_date DATE,
  created_at TIMESTAMP
);

-- Alerts & Escalations
CREATE TABLE behavioral_alerts (
  id UUID PRIMARY KEY,
  practice_id VARCHAR,
  alert_type VARCHAR,    -- burnout, disengagement, confusion, cascade_failure
  severity VARCHAR,      -- info, caution, critical
  detected_at TIMESTAMP,
  description TEXT,
  recommended_action TEXT,
  status VARCHAR,        -- open, investigating, resolved
  created_at TIMESTAMP
);
```

### Integration With Evaluator

Evaluator's weekly system-health-audit includes:

```yaml
system_health_audit:
  date: "2026-08-21"
  
  components:
    os_health: 0.688
    practice_health: 0.75
    epistemic_health: 0.73
    token_efficiency: 0.0015
    behavioral_health: 0.72  # NEW (from Supabase query)
    
  composite_system_health: 0.74
  
  behavioral_insights:
    mesh_support_engagement: "↘ 0.95 (burnout risk)"
    outreach_psychological_safety: "↗ 0.68 (improving, still low)"
    autonomy_role_clarity: "⏳ awaiting Phase 1b definition"
    website_learning_capacity: "↗ 0.65 (model curriculum working)"
  
  alerts:
    - "mesh-support burnout risk (engagement 0.95 > threshold 0.90)"
    - "outreach psychological safety below healthy (0.68 < target 0.75)"
```

---

## PART 7: DEPLOYMENT ROADMAP

### Phase 1b (Sep 11-Oct 9) — Behavioral Health Baseline

- [ ] Set up Supabase schema (Sep 11)
- [ ] Design ACAT survey (2 min/week per dimension)
- [ ] Start weekly collection (Sep 18+)
- [ ] Publish first assessment (Sep 25)
- [ ] Integrate into Evaluator reports (Oct 1+)

### Phase 2 (Oct 9 onwards) — Behavioral Health Optimization

- [ ] Identify interventions (burnout reduction, engagement, trust)
- [ ] Deploy interventions (staggered by practice)
- [ ] Measure impact (behavioral health trending up)
- [ ] Scale to additional practices (website, others)

### Phase 3 (Nov 1+) — Full Integration

- [ ] Behavioral health is standard part of system health
- [ ] Burnout detection is proactive (not reactive)
- [ ] Learning and engagement are measurable
- [ ] System operates sustainably (healthy + high-performing)

---

## PART 8: WHY THIS MATTERS

**Current Risk:**

```
System looks healthy operationally (practice health 0.75, token efficiency good)
BUT:
  - mesh-support is burning out (engagement 0.95)
  - outreach is disengaged (low participation)
  - autonomy might be confused (role unclear in Phase 1b)
  
Result: System fails not because infrastructure broke,
        but because practitioners broke
```

**With Behavioral Health:**

```
Comprehensive system health = OS + Practice + Epistemic + Efficiency + Behavioral

Admiral (Night) can see EARLY WARNING of burnout/disengagement/confusion
BEFORE they cascade into operational failures

System becomes self-aware of its own stress level
And can proactively intervene
```

---

**Status:** ✅ GAP ANALYSIS COMPLETE  
**Finding:** Behavioral health is critical missing dimension  
**Recommendation:** Add Behavioral Health Practice (Phase 1b, Sep 11)  
**Data Backend:** Supabase integration (already initiated)
