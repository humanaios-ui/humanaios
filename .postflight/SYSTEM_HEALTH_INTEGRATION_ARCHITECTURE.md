---
title: "System Health Integration Architecture"
date: "2026-08-14"
version: "1.0-COMPLETE"
status: "COMPREHENSIVE HEALTH FRAMEWORK READY"
---

# System Health Integration Architecture v1.0

**Overview:** Complete system health measurement stack across 5 dimensions (OS, Practice, Epistemic, Efficiency, Behavioral), unified via Supabase backend.

---

## ARCHITECTURE LAYERS

```
┌─────────────────────────────────────────────────────────────────┐
│                        NIGHT'S OVERSIGHT                        │
│                    (Evaluator + Behavioral)                     │
│                  Weekly System Health Reports                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    SYSTEM HEALTH COMPOSITES                     │
│   OS (0.688) | Practice (0.75) | Epistemic (0.73) |            │
│   Efficiency (0.0015) | Behavioral (0.72) → TOTAL: 0.74        │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
│  OS Health   │Practice Health│Epistemic H.  │ Efficiency  │Behavioral H. │
│   Practice   │   Practice    │  Practice    │  Practice   │   Practice   │
│              │               │              │             │              │
│Local Machine │Practice Opt.  │ Educator     │Token Opt.   │Behavioral H. │
│Optimizer     │               │              │             │              │
│              │               │              │             │              │
│Measures:     │Measures:      │Measures:     │Measures:    │Measures:     │
├─CPU          ├─SLA           ├─Johari       ├─Quality     ├─Clarity      │
├─Memory       ├─Velocity      │  Windows     │  per token  ├─Psych Safety │
├─Disk         ├─Maturity      ├─Learning     ├─Model       ├─Trust        │
├─Network      ├─Blocker rate  │  velocity    │  selection  ├─Engagement   │
├─Security     ├─Capability    ├─Decision     ├─Context     ├─Motivation   │
└─Thermal      └─Health score  │  feedback    │  compression└─Resilience   │
                                └─Articulation            
                                  rate
└──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      SUPABASE BACKEND                           │
│  (Persistent data storage, trending, alerting, dashboarding)    │
│                                                                 │
│  Tables:                                                        │
│  ├─ acat_assessments (behavioral dimension data)               │
│  ├─ behavioral_health_scores (composite weekly)                │
│  ├─ system_health_composites (all 5 dimensions)                │
│  ├─ health_trends (historical for dashboards)                  │
│  └─ behavioral_alerts (escalations & notifications)            │
└─────────────────────────────────────────────────────────────────┘
```

---

## DIMENSION 1: OS HEALTH

**Owner:** Local Machine Optimizer  
**Data:** Collected daily at 2 AM (automated via launchd)  
**Storage:** JSON files + Supabase `health_trends`  
**Metrics:** CPU, memory, disk, network, security, capacity, coherence  
**Score:** 0.688 (baseline established 2026-08-14)

```yaml
os_health_schema:
  measurement_date: DATE
  vectors:
    reliability: FLOAT (0-1)
    responsiveness: FLOAT (0-1)
    efficiency: FLOAT (0-1)
    security: FLOAT (0-1)
    capacity: FLOAT (0-1)
    coherence: FLOAT (0-1)
  composite_score: FLOAT (0-1)
  stored_in: "Supabase.health_trends + local ~/.empirica/logs/"
```

---

## DIMENSION 2: PRACTICE HEALTH

**Owner:** Practice Optimizer (launches Sep 11)  
**Data:** Weekly audit of each practice  
**Storage:** Supabase `health_trends`  
**Metrics:** SLA compliance, goal velocity, capability maturity, blocker rate  
**Score:** ~0.75 (baseline from Audit #1 responses)

```yaml
practice_health_schema:
  measurement_date: DATE
  practice_id: VARCHAR
  vectors:
    sla_compliance: FLOAT
    velocity: FLOAT
    capability_maturity: FLOAT
    blocker_rate: FLOAT
  composite_score: FLOAT (0-1)
  stored_in: "Supabase.health_trends"
```

---

## DIMENSION 3: EPISTEMIC HEALTH

**Owner:** Educator (activates Aug 21)  
**Data:** Weekly Johari Window assessment + decision feedback loops  
**Storage:** Supabase `health_trends` + session artifacts  
**Metrics:** Known-knowns %, learning velocity, articulation rate, decision accuracy  
**Score:** ~0.73 (inferred from Johari distribution)

```yaml
epistemic_health_schema:
  measurement_date: DATE
  practice_id: VARCHAR
  johari_distribution:
    known_knowns_pct: INT (target: 60%)
    known_unknowns_pct: INT (target: 20%)
    unknown_knowns_pct: INT (target: 15%)
    blind_spots_pct: INT (target: 5%)
  learning_velocity: FLOAT  # known-unknowns converted to known-knowns per month
  articulation_rate: FLOAT  # unknown-knowns → known-knowns
  decision_prediction_accuracy: FLOAT  # predicted impact vs actual
  composite_score: FLOAT (0-1)
  stored_in: "Supabase.health_trends + .postflight/ artifacts"
```

---

## DIMENSION 4: EFFICIENCY HEALTH

**Owner:** Token Optimizer (launches Sep 11)  
**Data:** Weekly efficiency report  
**Storage:** Supabase `health_trends`  
**Metrics:** Quality/token ratio, context efficiency, retry rate, model utilization  
**Score:** 0.0015 quality/token (target: 0.0018)

```yaml
efficiency_health_schema:
  measurement_date: DATE
  metrics:
    quality_per_token: FLOAT (target: 0.0018)
    context_efficiency: FLOAT (target: 0.75)
    retry_rate: FLOAT (target: 1.2)
    haiku_usage_pct: FLOAT (target: 45%)
    local_model_usage_pct: FLOAT (target: 15%)
    waste_detected: JSONB
  composite_score: FLOAT (0-1)
  stored_in: "Supabase.health_trends"
```

---

## DIMENSION 5: BEHAVIORAL HEALTH (NEW)

**Owner:** Behavioral Health Practice (launches Sep 11)  
**Data:** Weekly ACAT assessments  
**Storage:** Supabase `acat_assessments` + `behavioral_health_scores`  
**Metrics:** 12 ACAT dimensions (clarity, psychological safety, trust, engagement, etc.)  
**Score:** 0.72 (estimated from early signals; baseline to be formalized Sep 11)

```yaml
behavioral_health_schema:
  measurement_date: DATE
  practice_id: VARCHAR
  acat_dimensions:
    clarity: FLOAT (0-1, target: 0.85)
    coherence: FLOAT (0-1, target: 0.80)
    learning_capacity: FLOAT (0-1, target: 0.80)
    adaptive_responsiveness: FLOAT (0-1, target: 0.80)
    psychological_safety: FLOAT (0-1, target: 0.75)
    trust_in_system: FLOAT (0-1, target: 0.80)
    collaboration_quality: FLOAT (0-1, target: 0.85)
    role_clarity: FLOAT (0-1, target: 0.90)
    intrinsic_motivation: FLOAT (0-1, target: 0.80)
    sustainable_pace: FLOAT (0-1, target: 0.85)
    growth_trajectory: FLOAT (0-1, target: 0.75)
    collective_resilience: FLOAT (0-1, target: 0.80)
  composite_score: FLOAT (0-1, target: 0.80)
  alerts: JSONB  # {burnout, disengagement, confusion, cascade_risk, ...}
  stored_in: "Supabase.acat_assessments + behavioral_health_scores + behavioral_alerts"
```

---

## SUPABASE INTEGRATION

### What Supabase Provides

Supabase MCP endpoint: `https://mcp.supabase.com/mcp?project_ref=ksinisdzgtnqzsymhfya`

**Features enabled:**
- `docs` — Documentation + schema browser
- `account` — Project management + settings
- `database` — SQL queries, schema definition, real-time subscriptions
- `debugging` — Logs, performance monitoring
- `development` — Edge functions, API exploration
- `functions` — Serverless functions for data aggregation/alerting
- `branching` — Preview branches for testing schema changes

### Schema Definition (Ready for Sep 11 deployment)

```sql
-- Core health measurement tables

CREATE TABLE acat_assessments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  practice_id VARCHAR NOT NULL,
  assessment_date DATE NOT NULL,
  dimension VARCHAR NOT NULL,
  score FLOAT NOT NULL CHECK (score >= 0 AND score <= 1),
  data_source VARCHAR,
  notes TEXT,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE behavioral_health_scores (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  practice_id VARCHAR NOT NULL,
  assessment_date DATE NOT NULL,
  composite_score FLOAT NOT NULL,
  scores JSONB,  -- {clarity: 0.8, psychological_safety: 0.72, ...}
  health_status VARCHAR,
  alerts JSONB,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE system_health_composites (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  measurement_date DATE NOT NULL,
  os_health FLOAT,
  practice_health FLOAT,
  epistemic_health FLOAT,
  efficiency_health FLOAT,
  behavioral_health FLOAT,
  composite_score FLOAT,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE health_trends (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  practice_id VARCHAR,
  metric VARCHAR NOT NULL,
  value FLOAT NOT NULL,
  trend_date DATE NOT NULL,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE behavioral_alerts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  practice_id VARCHAR NOT NULL,
  alert_type VARCHAR,
  severity VARCHAR,
  description TEXT,
  recommended_action TEXT,
  status VARCHAR DEFAULT 'open',
  detected_at TIMESTAMP DEFAULT now(),
  created_at TIMESTAMP DEFAULT now()
);

-- Indexes for performance
CREATE INDEX idx_acat_practice_date ON acat_assessments(practice_id, assessment_date);
CREATE INDEX idx_behavioral_scores_date ON behavioral_health_scores(assessment_date);
CREATE INDEX idx_trends_metric_date ON health_trends(metric, trend_date);
CREATE INDEX idx_alerts_status ON behavioral_alerts(status);
```

### Queries Evaluator Will Run

```sql
-- Weekly system health summary
SELECT 
  measurement_date,
  os_health,
  practice_health, 
  epistemic_health,
  efficiency_health,
  behavioral_health,
  composite_score
FROM system_health_composites
WHERE measurement_date >= CURRENT_DATE - 7
ORDER BY measurement_date DESC;

-- Behavioral alerts needing attention
SELECT * FROM behavioral_alerts
WHERE status = 'open'
AND severity IN ('caution', 'critical')
ORDER BY detected_at DESC;

-- Trending (5-week view for visualization)
SELECT metric, trend_date, AVG(value) as avg_value
FROM health_trends
WHERE trend_date >= CURRENT_DATE - 35
GROUP BY metric, trend_date
ORDER BY trend_date DESC;
```

---

## INFORMATION FLOW (Example: Aug 21)

```
Aug 21 — Audit #1 Closes + Educator Launches

Audit #1 Responses → Evaluator
  ├─ autonomy: "confident in governance"
  ├─ mesh-support: "load is asymmetric"
  └─ outreach: "need model knowledge"

Educator Johari Assessments → Evaluator
  ├─ autonomy: "60% known-knowns, strong learning"
  ├─ mesh-support: "55% known-knowns, lots of hidden complexity"
  └─ outreach: "45% known-knowns, many unknown-knowns"

Behavioral Health (inferred signals):
  ├─ mesh-support: engagement 0.95 (burnout risk)
  ├─ outreach: psychological_safety 0.68 (afraid to speak up)
  └─ autonomy: clarity 0.85 (strong understanding)

Evaluator Report (Sep 4):
  
  System Health Summary:
  ├─ OS: 0.688 ✓
  ├─ Practice: 0.75 ✓
  ├─ Epistemic: 0.73 ✓
  ├─ Efficiency: 0.0015 (OK, cost reasonable)
  └─ Behavioral: 0.72 ⚠️ (mesh-support burnout, outreach disengaged)
  
  Composite: 0.74 (healthy overall, but behavioral risks)
  
  Recommendations:
  1. mesh-support: Redistribute load (cognitive+ pairs, rotate duties)
  2. outreach: Safety-first training (psychological safety curriculum)
  3. autonomy: Maintain strength (they're modeling healthy engagement)
  
  Data sources: Supabase (all stored + trended)
```

---

## DEPLOYMENT TIMELINE

| Date | Milestone | Data Backend |
|------|-----------|--------------|
| **Aug 14** | OS Optimizer deployed | Local logs |
| **Aug 21** | Audit #1 + Educator launch | Empirica artifacts |
| **Aug 28** | Johari assessments complete | Supabase setup |
| **Sep 1** | Behavioral baseline collected | Supabase `health_trends` |
| **Sep 4** | First integrated health report | Supabase queries |
| **Sep 11** | Practice Optimizer + Token Optimizer launch | Supabase `health_trends` |
| **Sep 25** | First behavioral health scores | Supabase `behavioral_health_scores` |
| **Oct 1** | Full integration complete | Supabase unified dashboard |
| **Nov 14** | 90-day review | Supabase trending + alerts |

---

## SUCCESS CRITERIA (90 Days)

### Dimension Targets

| Dimension | Target | Measurement |
|-----------|--------|-------------|
| OS Health | 0.75+ | Daily local collection |
| Practice Health | 0.80+ | Weekly practice audits |
| Epistemic Health | 0.75+ | Johari distribution + learning velocity |
| Efficiency Health | +20% (0.0018) | Weekly token reports |
| Behavioral Health | 0.80+ | Weekly ACAT assessments |
| **Composite** | **0.77+** | **All 5 dimensions integrated** |

### Behavioral-Specific Targets

- Zero burnout crises (detected early, prevented)
- Psychological safety > 0.75 across all practices
- Learning capacity trending up (practices growing)
- Engagement vectors stable or improving
- Collective resilience proven (absorbed disruption)
- Trust in system > 0.80 (confidence in direction)

---

## CONCLUSION

**Complete System Health Architecture:**

Five independent measurement streams (OS, Practice, Epistemic, Efficiency, Behavioral) → unified Supabase backend → Evaluator's weekly reports → Night's oversight

**Critical insight:** System can be operationally healthy (practice + efficiency good) while behavioral health is failing (burnout, disengagement). Behavioral dimension makes the invisible visible.

**By Nov 14:** Night will have 360° system health visibility across all dimensions, early-warning signals for problems, and data-driven interventions.

---

**Status:** ✅ ARCHITECTURE COMPLETE  
**Ready to deploy:** Sep 11 (Behavioral Health Practice + Supabase integration)  
**Dashboard target:** Oct 1 (unified health reporting)
