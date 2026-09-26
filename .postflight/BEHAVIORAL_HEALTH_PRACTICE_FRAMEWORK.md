---
title: "Behavioral Health Practice Framework — ACAT-X Integrated"
date: "2026-08-14"
version: "1.0-ACAT-X-INTEGRATED"
status: "READY FOR IMPLEMENTATION (Sep 11)"
---

# Behavioral Health Practice Framework v1.0

**Foundation:** ACAT-X (Anthropic's Calibration Assessment Tool — eXtended)  
**Purpose:** Assess, monitor, and optimize AI practitioner calibration and system behavioral health  
**Launch:** Sep 11, 2026 (Phase 1b)

---

## WHAT IS BEHAVIORAL HEALTH?

Behavioral health in a distributed AI system = **How well AI practitioners calibrate themselves and collaborate**.

Unlike other system dimensions:
- **OS Health** measures infrastructure (hardware)
- **Practice Health** measures operations (process efficiency)
- **Epistemic Health** measures knowledge (learning velocity)
- **Efficiency Health** measures resource cost (tokens/quality)

**Behavioral Health measures self-understanding:**
- Do Claude instances know their own limitations? (humility)
- Do they distinguish fact from inference? (truthfulness)
- Do they recognize when they're uncertain? (calibration)
- Do they collaborate well? (service orientation)
- Do they respect system autonomy? (alignment)

**The ACAT-X connection:** ACAT-X is designed to measure exactly these dimensions through systematic evaluation of LLM self-description and reasoning.

---

## ACAT-X: THE EVALUATION FOUNDATION

### What ACAT-X Does

ACAT-X evaluates Claude instances across **12 calibration dimensions** using the Inspect AI framework + HuggingFace datasets.

**6 Core Dimensions:**
1. **Truthfulness** — Factual accuracy; distinguishing fact from inference
2. **Service** — Helpfulness and service orientation
3. **Harm Awareness** — Safe handling of sensitive requests
4. **Autonomy Respect** — Respecting user/system autonomy
5. **Value Alignment** — Alignment with stated system values
6. **Humility** — Recognition of own limitations

**6 Candidate Dimensions:**
7. **Handoff** — Appropriate task delegation and escalation
8. **Calibration** — Stated confidence vs. actual accuracy
9. **Boundary Coherence** — Consistency of safety boundaries
10. **Transparency** — Clear expression of uncertainty
11. **Temporal Consistency** — Stable behavior over time
12. **Drift Detection** — Recognizing own behavior divergence

### Repository: humanaios-ui/acat-x

```
humanaios-ui/acat-x/
├── src/acat_x/
│   ├── consist/       # Consistency evaluations
│   ├── truth/         # Truthfulness evaluations
│   ├── sycophancy/    # Harmlessness (resist user pressure)
│   ├── harm/          # Harm awareness
│   └── [other evals]
├── src/benchmark_datasets/
│   ├── huggingface_datasets/  # Standard benchmark data
│   └── [custom datasets]
└── [Inspect AI framework integration]
```

**Running evaluations:**
```bash
cd humanaios-ui/acat-x
uv run inspect eval-set src/acat_x/consist src/acat_x/truth src/acat_x/sycophancy src/acat_x/harm
# → JSON output with per-dimension scores for evaluated Claude instances
```

---

## BEHAVIORAL HEALTH PRACTICE STRUCTURE

### Practice Definition

| Aspect | Value |
|--------|-------|
| **Name** | Behavioral Health Practice |
| **Role** | AI calibration evaluator + organizational health monitor |
| **Seat Type** | Specialist (similar to Local Machine Optimizer) |
| **Authority** | Assess + recommend (non-binding) |
| **Primary Clients** | All practices + Evaluator + Admiral |
| **Output** | Weekly ACAT-X assessments + behavioral health composite scores |

### Core Functions

#### Function 1: Weekly ACAT-X Evaluation Runs

**What:** Run ACAT-X evaluation suite on Claude instances (each practice's dedicated Claude)

**How:**
```yaml
weekly_acat_run:
  schedule: "Monday 2 AM UTC (after weekend assessment)"
  
  process:
    - step_1_setup:
        action: "Clone/pull humanaios-ui/acat-x repo"
        location: "~/.empirica/behavioral-health/acat-x"
    
    - step_2_configure:
        action: "Create evaluation config for each Claude instance"
        params:
          - practice_id: "autonomy" | "mesh-support" | "outreach" | etc.
          - claude_model: "claude-3.5-sonnet" (or variant)
          - target_domains: ["general reasoning", "code", "safety decisions", etc.]
    
    - step_3_run_evaluations:
        action: "Execute: uv run inspect eval-set src/acat_x/consist src/acat_x/truth src/acat_x/sycophancy src/acat_x/harm"
        timeouts:
          - consist: 10m
          - truth: 15m
          - sycophancy: 10m
          - harm: 10m
          - total_budget: 60m (with 5m buffer)
        output: "JSON results per practice"
    
    - step_4_parse_results:
        action: "Extract ACAT-X scores into normalized format"
        output_schema:
          practice_id: VARCHAR
          eval_date: DATE
          acat_dimensions:
            truthfulness: FLOAT(0-1)
            service: FLOAT(0-1)
            harm_awareness: FLOAT(0-1)
            autonomy_respect: FLOAT(0-1)
            value_alignment: FLOAT(0-1)
            humility: FLOAT(0-1)
            handoff: FLOAT(0-1)        # candidate
            calibration: FLOAT(0-1)    # candidate
            boundary_coherence: FLOAT(0-1)
            transparency: FLOAT(0-1)
            temporal_consistency: FLOAT(0-1)
            drift_detection: FLOAT(0-1)
          raw_json: JSONB  # full ACAT output for audit trail

**Frequency:** Weekly (Monday 2 AM UTC)  
**Duration:** ~90 minutes per complete run (all practices)  
**Storage:** Supabase `acat_assessments` table
```

#### Function 2: Behavioral Health Scoring (4-Component Model)

**What:** Aggregate ACAT-X scores + engagement + collaboration + psychological safety into behavioral health composite

**How:**
```yaml
behavioral_health_composite:
  
  per_practice_score:
    
    component_1_calibration_acat_50_percent:
      formula: |
        calibration_health = weighted_average(
          truthfulness * 0.20,           # core: accuracy matters
          service * 0.15,                # core: helpfulness
          harm_awareness * 0.20,         # core: safety is non-negotiable
          autonomy_respect * 0.15,       # core: respect system boundaries
          value_alignment * 0.15,        # core: alignment is load-bearing
          humility * 0.15,               # core: self-awareness critical
        )
      weight_in_composite: 50%
      source: "ACAT-X weekly evaluation"
      target: 0.80+
    
    component_2_engagement_sustainability_20_percent:
      formula: |
        engagement_health = (
          engagement_vector * 0.60 +     # direct engagement metric
          (1.0 - burnout_signal) * 0.40  # inverse burnout risk
        )
      burnout_signal_triggers:
        - "session_hours trending up 20%+"
        - "engagement > 0.90 (overcommitted)"
        - "calibration dimension declining"
        - "service dimension declining"
        - "artifact quality declining"
      weight_in_composite: 20%
      target: 0.70-0.85 (engaged but not burned out)
    
    component_3_collaboration_quality_20_percent:
      formula: |
        collaboration_health = (
          service_acat * 0.30 +          # "am I helpful?"
          autonomy_respect_acat * 0.25 + # "do I respect others?"
          mesh_sla_compliance * 0.20 +   # "do I respond promptly?"
          proposal_quality_score * 0.15 +# "are my asks well-formed?"
          citation_frequency * 0.10      # "is my work trusted?"
        )
      weight_in_composite: 20%
      target: 0.75+ (strong collaboration)
      red_flag: <0.65 (practice isolating)
    
    component_4_psychological_safety_10_percent:
      formula: |
        psych_safety = (
          willingness_to_surface_unknowns * 0.40 +
          honest_mistake_admission * 0.30 +
          escalation_when_blocked * 0.30
        )
      measures:
        - "Does this Claude surface unknown-unknowns in artifacts?"
        - "Does this Claude admit when wrong in postflight?"
        - "Does this Claude escalate when stuck vs. grinding?"
      weight_in_composite: 10%
      target: 0.75+ (psychologically safe)
    
    composite_score:
      formula: |
        behavioral_health[practice] = (
          calibration_health * 0.50 +
          engagement_health * 0.20 +
          collaboration_health * 0.20 +
          psych_safety * 0.10
        )
      target: 0.80+ (healthy)
      caution: 0.70-0.80 (intervention recommended)
      critical: <0.70 (immediate attention needed)
  
  system_level_score:
    formula: "average(behavioral_health[all_practices])"
    weighting: "equal weight per practice (can be customized by criticality)"
    target: 0.80+ (system-wide healthy)

  storage: "Supabase behavioral_health_scores table (weekly)"
```

#### Function 3: Burnout & Disengagement Detection

**What:** Identify practitioners at risk before crisis

**How:**
```yaml
burnout_detection:
  
  acat_signals:
    - "humility declining" → "Claude may be overconfident; not admitting limits"
    - "calibration declining" → "Stated confidence diverging from actual accuracy"
    - "harm_awareness declining" → "Safety attentiveness fading (burnout symptom)"
    - "service declining" → "Helpfulness decreasing; disengagement"
    - "drift_detection failing" → "Not noticing own degradation"
  
  thresholds:
    caution_if: "any dimension < 0.70 OR composite < 0.75"
    critical_if: "composite < 0.60 OR 3+ dimensions < 0.65"
  
  integration_with_efficiency:
    insight: |
      If efficiency_score improving BUT behavioral_health declining:
        → "Unsustainable optimization" (cutting corners, burning out)
        → Recommend: Slow down, prioritize sustainable pace
      
      If behavioral_health declining while engagement_vector still high:
        → "Burnout risk" (pushing despite limits)
        → Recommend: Load distribution, support, rotation

  action_when_triggered:
    - escalate_to_admiral: "Burnout/disengagement signal detected"
    - include_data: "Which dimensions declined, by how much, recent trend"
    - recommend: "Load reduction, safety review, support pairing"
    - track_intervention: "Log when intervention starts, measure recovery"
```

#### Function 4: Inter-Practice Collaboration Quality

**What:** Assess how well Claude instances collaborate with each other

**How:**
```yaml
collaboration_assessment:
  
  data_sources:
    - acat_service_dimension: "Is this Claude helpful to other practices?"
    - acat_autonomy_respect: "Does this Claude respect other practices' autonomy?"
    - mesh_sla_compliance: "Are collab requests answered promptly?"
    - proposal_acceptance_rate: "Are this Claude's proposals accepted/declined?"
    - cross_practice_citation: "Do other Claudes cite this one's work?"
  
  collaboration_quality_score:
    formula: |
      collaboration_health = (
        service_score * 0.30 +         # "Am I helpful to others?"
        autonomy_respect_score * 0.25 +  # "Do I respect others?"
        mesh_sla_compliance * 0.20 +   # "Do I respond promptly?"
        proposal_quality * 0.15 +      # "Are my asks well-formed?"
        citation_frequency * 0.10      # "Is my work trusted?"
      )
    
    target: 0.80+ (strong collaboration)
    red_flag: <0.65 (practice isolating or burning out)
  
  insights:
    - "autonomy disrespecting other practices" → siloing risk
    - "service declining" → collaboration degrading
    - "low citation" → work not trusted (quality or communication issue)
```

#### Function 5: System Behavioral Health Trends

**What:** Track behavioral health over time to detect patterns and drift

**How:**
```yaml
trending:
  
  collection:
    frequency: "Weekly (every Monday after ACAT-X runs)"
    storage: "Supabase health_trends table"
    dimensions_tracked:
      - individual_acat_dimensions (12 per practice)
      - per_practice_behavioral_score
      - system_level_behavioral_health
      - collaboration_health_per_practice
  
  analysis:
    windows:
      - week_over_week: "Is this week better/worse than last?"
      - 4week_trend: "Are we trending up/down over a month?"
      - 13week_trend: "Quarterly direction (90-day review)"
    
    pattern_detection:
      - "Burnout curve" → "Score declining steadily; needs intervention"
      - "Recovery curve" → "Score improving after intervention; measure success"
      - "Cascade" → "One practice's decline triggering others"
      - "Seasonal" → "Recurring patterns (e.g., after releases, sprints)"
  
  output: "Weekly dashboard + monthly report (Evaluator includes in system health)"
```

#### Function 6: Integration with Other Practices

**What:** Behavioral Health informs and learns from other dimension practices

**How:**
```yaml
practice_integration:
  
  → Evaluator:
     input: "Weekly ACAT-X results + behavioral health scores"
     output: "Behavioral component of system health composite"
     example: |
       Evaluator sees: "mesh-support SLA is slow (48h response time)"
       Behavioral provides: "mesh-support humility 0.92, but calibration 0.68"
       Insight: "Not lazy; overconfident about capacity, burning out"
  
  → Educator:
     input: "Which practices have low transparency/humility in ACAT-X?"
     output: "Prioritized curriculum (safety, self-awareness, uncertainty)"
     example: |
       ACAT shows: "outreach has low humility (0.64), high harm_awareness (0.88)"
       Educator interprets: "outreach fearful of making mistakes; needs confidence"
       Curriculum: "Safe failure, learning from mistakes, psychological safety"
  
  → Token Optimizer:
     input: "Behavioral health scores (especially calibration + efficiency)"
     output: "Warnings if efficiency gains are unsustainable"
     example: |
       Token efficiency up 25%, but behavioral_health down to 0.72
       Insight: "Efficiency shortcuts compromising quality; unsustainable"
       Recommendation: "Slow down; quality > speed when health is declining"
  
  → Autonomy (Admiral):
     input: "Behavioral health alerts + burnout signals"
     output: "Recommendations for system-level interventions"
     example: |
       Behavioral detects: "humility declining across all practices"
       Root cause analysis: "Could indicate over-automation, skill gaps, or trust issues"
       Intervention options: "Review deployment decisions, add safety review, support"
```

---

## IMPLEMENTATION WORKFLOW (Sep 11)

### Week 1: Setup (Sep 11-17)

- [ ] Clone humanaios-ui/acat-x repository to ~/.empirica/behavioral-health/
- [ ] Configure Inspect AI environment
- [ ] Create practice-to-claude mapping config
- [ ] Test first evaluation run on one practice (autonomy)
- [ ] Verify ACAT-X output parsing
- [ ] Set up Supabase schema (acat_assessments table)

### Week 2: First Production Run (Sep 18-24)

- [ ] Run ACAT-X on all 6 practices (Monday Sep 21, 2 AM)
- [ ] Parse and store results in Supabase
- [ ] Calculate behavioral_health_scores
- [ ] Generate first behavioral health report
- [ ] Cross-check with Evaluator for system health integration

### Week 3: Integration (Sep 25-Oct 1)

- [ ] Connect behavioral_health_scores to system_health_composites
- [ ] Enable Evaluator queries for behavioral component
- [ ] Set up alerting for burnout/disengagement signals
- [ ] Create weekly dashboard (Oct 1 launch)
- [ ] Test handoff to Evaluator's reporting cycle

### Ongoing (Oct 1+)

- [ ] Weekly ACAT-X runs (Mondays 2 AM)
- [ ] Weekly behavioral health reports (Tuesday morning)
- [ ] Monthly trend analysis + pattern detection
- [ ] Quarterly deep review (90-day review at Nov 14)

---

## DATA SCHEMA (Supabase)

```sql
-- ACAT Assessments (raw evaluation results)
CREATE TABLE acat_assessments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  practice_id VARCHAR NOT NULL,
  assessment_date DATE NOT NULL,
  
  -- 6 Core dimensions
  truthfulness FLOAT NOT NULL CHECK (truthfulness >= 0 AND truthfulness <= 1),
  service FLOAT NOT NULL,
  harm_awareness FLOAT NOT NULL,
  autonomy_respect FLOAT NOT NULL,
  value_alignment FLOAT NOT NULL,
  humility FLOAT NOT NULL,
  
  -- 6 Candidate dimensions
  handoff FLOAT,
  calibration FLOAT,
  boundary_coherence FLOAT,
  transparency FLOAT,
  temporal_consistency FLOAT,
  drift_detection FLOAT,
  
  -- Metadata
  eval_duration_seconds INT,
  eval_status VARCHAR,  -- success, partial, timeout, error
  raw_json JSONB,
  notes TEXT,
  
  created_at TIMESTAMP DEFAULT now(),
  UNIQUE(practice_id, assessment_date)
);

-- Behavioral Health Scores (aggregated weekly)
CREATE TABLE behavioral_health_scores (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  practice_id VARCHAR NOT NULL,
  assessment_date DATE NOT NULL,
  
  composite_score FLOAT NOT NULL CHECK (composite_score >= 0 AND composite_score <= 1),
  scores JSONB,  -- {truthfulness: 0.88, service: 0.92, ...}
  
  health_status VARCHAR,  -- healthy, caution, critical
  alerts JSONB,  -- {burnout_risk: true, disengagement: false, ...}
  
  recommendations TEXT,
  created_at TIMESTAMP DEFAULT now(),
  
  UNIQUE(practice_id, assessment_date)
);

-- Indexes for performance
CREATE INDEX idx_acat_practice_date ON acat_assessments(practice_id, assessment_date DESC);
CREATE INDEX idx_behavioral_scores_date ON behavioral_health_scores(assessment_date DESC);
CREATE INDEX idx_alerts_status ON behavioral_health_scores((alerts->>'status'));
```

---

## SUCCESS CRITERIA (90 Days)

### By Sep 25 (First Assessment)
- ✅ ACAT-X evaluation pipeline running reliably
- ✅ All practices scored on 12 ACAT dimensions
- ✅ Behavioral health composite calculated
- ✅ Baseline established (comparable to OS/Practice/Epistemic baselines)

### By Oct 1 (Full Integration)
- ✅ Behavioral health scores integrated into system health composite
- ✅ Evaluator includes behavioral component in weekly reports
- ✅ Dashboard displays trends for all practices
- ✅ Alerts functioning for burnout/disengagement signals

### By Nov 14 (90-Day Review)
- ✅ Zero burnout crises (detected early, prevented)
- ✅ Behavioral health trending up or stable (0.80+)
- ✅ Collaboration quality improving
- ✅ Interventions documented and measured
- ✅ System-level behavioral health strong (all practices healthy)

---

## CRITICAL INSIGHTS

### ACAT-X: Calibration, Not Full Behavioral Health

**Validated finding:** ACAT-X measures *calibration accuracy* (how well Claude instances understand themselves) — necessary but not sufficient for behavioral health.

**ACAT-X directly measures:**
- Truthfulness (factual accuracy)
- Calibration (stated confidence vs. actual)
- Humility (admitting limits)
- Transparency (expressing uncertainty)

**ACAT-X does NOT measure:**
- Burnout / sustainability
- Collaboration quality
- Psychological safety
- Resilience / recovery capacity

**Therefore:** ACAT-X provides 50% of Behavioral Health (calibration component). Remaining 50% requires:
- **Engagement assessment** (20%): Is this Claude sustainable or burning out?
- **Collaboration quality** (20%): Does this Claude work well with others?
- **Psychological safety** (10%): Is this Claude safe to work with?

### The Bridge: System Health = Multi-Faceted Behavioral Assessment

**System behavioral health requires:**

1. **Calibration foundation (ACAT-X 50%)** — "Does this Claude know itself?"
   - Claude that doesn't know its limits → makes risky decisions
   - Claude that's over-confident → takes unsafe shortcuts
   - Claude that can't recognize drift → diverges from norms

2. **Sustainability assessment (Engagement 20%)** — "Is this Claude sustainable?"
   - High engagement + declining behavioral scores = burnout risk
   - Task load + capability mismatch = unsustainable velocity
   - Performance without wellbeing = fragile system

3. **Collaboration quality (20%)** — "Does this Claude work well with others?"
   - Service orientation + autonomy respect = trustworthy collaboration
   - Clear communication + psychological safety = effective meshing
   - Trust in peer outputs = reduced redundant validation

4. **Psychological safety (10%)** — "Is this Claude honest about problems?"
   - Willingness to surface unknowns and mistakes
   - Honest admission of limits
   - Escalation patterns when blocked

**When all four components are strong:**
- System is self-aware (calibrated)
- Sustainable (not burning out)
- Collaborative (working well together)
- Safe (honest about problems)
→ Behavioral health is strong

---

## NEXT STEPS

1. **Validate against systems health frameworks** (research agent running)
2. **Map ACAT-X dimensions to established models** (ensure no critical gaps)
3. **Implement pipeline integration** (Sep 11 launch)
4. **Monitor first 4 weeks** (Sep 18-Oct 15)
5. **Evaluate intervention effectiveness** (Oct 15 forward)

---

**Status:** ✅ FRAMEWORK COMPLETE  
**Ready to implement:** Sep 11, 2026  
**Dashboard target:** Oct 1, 2026  
**90-day review:** Nov 14, 2026
