---
title: "Educator Practice Activation Plan"
date: "2026-08-14"
version: "1.0-ACTIVATED"
authority: "Night (empirica-foundation Admiral)"
status: "READY FOR IMMEDIATE DEPLOYMENT"
phase: "Phase 1b (Aug 21-Sep 4)"
---

# Educator Practice Activation Plan v1.0

**Mission:** Recursive learning, epistemic management, question-generation, and knowledge organization using Johari Window framework — with expanded model ecosystem awareness.

**Unique Addition:** Educator serves as knowledge architect for **model selection across entire ecosystem** (Anthropic + local machines + open-source/free models), not just a single vendor.

---

## PART 1: CORE ACTIVATION (Week 1 — Aug 21-28)

### Week 1 Function: Johari Window Assessment

**What:** Categorize all artifacts into four quadrants of knowledge.

**Quadrants:**

```
                Known to System       Unknown to System
Known to       ________________      ________________
Humans         | KNOWN-KNOWNS |     | BLIND SPOTS   |
               | (documented) |     | (we don't     |
               |              |     | see)          |
               |______________|     |_______________|

Unknown to     ________________      ________________
Humans         | UNKNOWN-KNOWNS|    | UNKNOWN-UNK   |
               | (implicit     |     | (truly        |
               | knowledge)    |     | unknown)      |
               |______________|     |_______________|
```

**Artifacts to Categorize (ALL of them):**
- Findings (in findings-log entries)
- Decisions (in decisions.yaml across practices)
- Unknowns (unknown-log entries)
- Assumptions (assumption-log entries)
- Dead-ends (deadend-log entries)
- Mistakes (mistake-log entries)

**Tasks for Week 1:**

| Task | Executor | Output | Deadline |
|------|----------|--------|----------|
| 1. Query all artifacts from past 8 weeks | Educator | CSV: 500+ artifacts with metadata | Aug 23 |
| 2. Categorize into Johari quadrants | Educator | Quadrant distribution + trend | Aug 25 |
| 3. Identify over/under-represented areas | Educator | Report: "40% known-knowns, 35% unknown-knowns, 15% blind spots, 10% unknown-unknowns" | Aug 25 |
| 4. Flag opportunities (unknown-knowns → known-knowns) | Educator | List: "5 implicit knowledges ready to articulate" | Aug 26 |
| 5. Surface blind spots (unknown-unknowns) | Educator | List: "3 potential blind spots to investigate" | Aug 26 |
| 6. Present to Evaluator + Night | Educator | First Johari Window assessment report | Aug 28 |

**Deliverable:** `JOHARI_WINDOW_ASSESSMENT_2026-08-14.md`

---

### Week 2 Function: Decision Feedback Loops (Aug 28-Sep 4)

**What:** Validate whether predictions about decisions matched reality.

**For Each Ratified Decision (d001, d002, etc.):**

```yaml
decision_feedback_loop:
  decision_id: "d001"
  title: "Resource-Gate Timeline Model"
  
  # What was predicted
  predicted_impact:
    vector: "resource_efficiency"
    predicted_delta: +0.12
    confidence: 0.75
    predicted_by: "autonomy"
    ratified_date: "2026-08-14"
  
  # When to measure (30 days post-ratification)
  validation_trigger: "2026-09-13 (30 days after ratification)"
  
  # What actually happened (post-validation)
  actual_impact:
    measured_delta: +0.09  # Measured at validation_trigger
    matches_prediction: false  # ±0.05 tolerance
    variance: -0.03
    root_cause: "Underestimated non-calendar bottlenecks"
  
  # Learning signal
  calibration_signal:
    insight: "Calendar gates matter less than we thought (20% of efficiency loss, not 50%)"
    confidence_adjustment: -0.15  # Reduce confidence on 'deadlines hurt efficiency'
    applies_to: ["d005", "d008"]  # Other timeline decisions
```

**Tasks for Week 2:**

| Task | Executor | Output | Deadline |
|------|----------|--------|----------|
| 1. Extract all ratified decisions from past 30 days | Educator | List: ["d001", "d002", "d003", ...] | Aug 29 |
| 2. Design validation experiments | Educator | Plan: When/how to measure each decision's impact | Aug 30 |
| 3. Set up measurement calendar | Educator | Schedule: "d001 validation Sep 13, d002 validation Sep 20, ..." | Aug 31 |
| 4. Begin collecting baseline metrics for comparison | Evaluator | Weekly system-health vectors @ baseline | Sep 1 |
| 5. Build feedback loop dashboard | Educator | UI: predicted vs actual impact, by decision | Sep 4 |

**Deliverable:** `DECISION_FEEDBACK_LOOPS_FRAMEWORK.md`

---

## PART 2: MODEL ECOSYSTEM KNOWLEDGE (Integrated into Educator)

### Model Selection Knowledge Curriculum

**Unique to This Educator:** Maintains living knowledge of:

1. **Anthropic Models** (Claude suite)
2. **Local Machine Models** (Ollama, LM Studio, custom)
3. **Open-Source Models** (Mistral, Llama, Qwen, Phi)
4. **Free/Research Models** (HuggingFace, academic releases)

**Educator's Model Knowledge Functions:**

#### Function A: Model Capability Mapping (Ongoing)

```yaml
model_ecosystem_knowledge:
  
  anthropic_suite:
    haiku:
      capabilities: [simple_reasoning, coding, summarization]
      quality_score: 0.78
      token_cost: "1x (baseline)"
      latency: "3-5s API"
      best_for: [simple_tasks, volume_work, cost_sensitive]
      avoid: [novel_research, complex_reasoning, unknown_unknowns]
    
    sonnet:
      capabilities: [reasoning, coding, analysis, creativity]
      quality_score: 0.87
      token_cost: "3x Haiku"
      latency: "3-5s API"
      best_for: [routine_work, balanced_quality_cost]
      avoid: [none - solid all-rounder]
    
    opus:
      capabilities: [complex_reasoning, novel_problems, deep_analysis]
      quality_score: 0.91
      token_cost: "6x Haiku"
      latency: "3-5s API"
      best_for: [unknown_unknowns, research, complex_decisions]
      avoid: [simple_tasks, volume_work]
  
  local_models:
    mistral_7b:
      capabilities: [reasoning, coding, moderate_analysis]
      quality_score: 0.72
      token_cost: "0 (local compute)"
      latency: "0.5-2s (on MacBook Pro M3)"
      best_for: [exploration, sensitive_work, offline]
      setup: "Ollama: ollama pull mistral"
      limitations: [slower_than_api, lower_quality_than_opus]
    
    llama2_13b:
      capabilities: [reasoning, coding, some_analysis]
      quality_score: 0.68
      token_cost: "0 (local)"
      latency: "1-3s (on MacBook)"
      best_for: [testing_prompts, offline_work]
      setup: "Ollama: ollama pull llama2"
      limitations: [quality < mistral, slower]
  
  open_source_free:
    mistral_8x7b:
      source: "Hugging Face / Together API"
      capabilities: [reasoning, coding, analysis]
      quality_score: 0.75
      token_cost: "free tier available (Together AI)"
      latency: "5-10s"
      best_for: [research, budget_limited]
      setup: "pip install together; api_key from together.ai"
    
    qwen_32b:
      source: "Alibaba / HuggingFace"
      capabilities: [reasoning, multilingual, coding]
      quality_score: 0.79
      token_cost: "free (self-hosted)"
      latency: "2-4s (local)"
      best_for: [multilingual_work, open_source_preference]
      setup: "Ollama: ollama pull qwen (experimental)"
    
    phi_2:
      source: "Microsoft / HuggingFace"
      capabilities: [simple_reasoning, coding]
      quality_score: 0.65
      token_cost: "free"
      latency: "fast (<1s local)"
      best_for: [quick_prototyping, edge_deployment]
      setup: "Ollama: ollama pull phi"
```

#### Function B: Model Selection Decision Framework (Integrated into Token Optimizer)

Educator teaches practices:

```yaml
when_to_use_which_model:
  
  "Simple tasks (summarize, extract, reformat)":
    use: "Haiku or Phi or local Llama2"
    reasoning: "Quality 0.65-0.78 sufficient; maximize cost efficiency"
    example_tasks: [summarize_meeting, extract_json, reformat_yaml]
  
  "Routine work (analysis, documentation, standard decisions)":
    use: "Sonnet or Mistral-7B or Qwen"
    reasoning: "Quality 0.72-0.87; good balance cost/quality"
    example_tasks: [code_review, architecture_docs, routine_decisions]
  
  "Research or novel problems (unknown-unknowns, hypothesis testing)":
    use: "Opus or Mistral-8x7B"
    reasoning: "Maximum quality needed; cost secondary"
    example_tasks: [novel_architecture, research_questions, blindspot_investigation]
  
  "Sensitive or offline work (no API, data privacy)":
    use: "Local models (Mistral-7B, Llama2, Phi)"
    reasoning: "Zero network traffic; instant response"
    example_tasks: [personal_notes, sensitive_analysis, offline_work]
  
  "Volume work (many tasks, cost optimization)":
    use: "Haiku + Mistral-7B (batch locally) + Qwen free tier"
    reasoning: "Amortize costs across quantity"
    example_tasks: [bulk_labeling, batch_processing, monitoring]
```

#### Function C: Model Knowledge Curriculum (Quarterly)

For each practice, Educator designs learning roadmap:

```yaml
practice_model_knowledge_curriculum:
  
  autonomy:
    current_state: "Uses Opus for all work (expensive baseline)"
    target_state: "30% Haiku, 50% Sonnet, 20% Opus (optimized)"
    learning_path:
      week_1: "Learn Haiku capability boundaries"
      week_2: "Train 3 Haiku tasks; measure quality"
      week_3: "Learn Sonnet best uses"
      week_4: "Implement tiered model strategy"
    expected_outcome: "40% token cost reduction while maintaining quality"
  
  outreach:
    current_state: "Unaware of local models; API-only"
    target_state: "Use Mistral-7B for sensitive customer data"
    learning_path:
      week_1: "Set up Ollama + Mistral-7B"
      week_2: "Test on non-critical customer work"
      week_3: "Build confidence; train team"
    expected_outcome: "Zero data privacy risk; faster iteration"
  
  mesh-support:
    current_state: "Ad-hoc model choices"
    target_state: "Systematic model selection per task type"
    learning_path:
      week_1: "Learn decision framework"
      week_2: "Audit recent decisions; map to framework"
      week_3: "Implement selection rules"
    expected_outcome: "Consistency + efficiency"
```

---

## PART 3: WEEKLY OPERATIONS (Sep 4+)

### Weekly "Unasked Questions" Report

Every Friday, Educator publishes 5-10 high-quality questions:

```markdown
## Unasked Questions Report (Week of Aug 28)

### Known-Knowns We Should Question
1. "We assume calendar gates hurt efficiency. Do they really? (d001 feedback loop will validate)"
2. "Are we using the most cost-effective models? (or just familiar ones?)"

### Blind Spots (Unknown-Unknowns)
1. "What local model capabilities are we leaving on the table?"
2. "What cross-practice knowledge isn't being shared?"

### Research Questions (For Educator to Drive)
1. "How much quality loss is acceptable to reduce tokens by 30%?"
2. "What's the optimal model selection strategy for our 16-practice system?"
3. "Are we over-using Opus when Sonnet would suffice?"

### Opportunities for Known-Knowns Expansion
1. "Model X performs well on task Y. Should all practices know this?"
2. "Decision feedback from d001 suggests new understanding about X. Articulate it."
```

### Cross-Practice Learning Summaries (Monthly)

```markdown
## Cross-Practice Learning (August)

### Knowledge Transfers Completed
- **From autonomy to outreach:** "Decision framework for model selection" (20% adoption so far)
- **From evaluator to all:** "ACAT calibration vectors; apply to your domain" (60% adoption)

### Knowledge Gaps Identified
- "Local model setup (Ollama)" — autonomy knows it, outreach doesn't
- "Johari Window categorization" — new process, all practices need training

### Learning Transfer Rate
- **Target:** 60% (practices adopt cross-practice learning)
- **Current:** 45% (autonomy excellent, website lagging)
- **Action:** "Double-down on website knowledge transfer"
```

---

## PART 4: INTEGRATION WITH SYSTEM

### Educator → Evaluator Information Flow

```
Educator discovers pattern:
  "Model selection is inconsistent; autonomy uses Opus 100% of time"
  ↓
Educator surfaces as finding:
  finding-log --finding "Autonomy could save 40% tokens by using Haiku for 30% of work"
  ↓
Evaluator includes in weekly system-health-audit:
  "Model efficiency opportunity: $X annual savings if practices adopt tiered approach"
  ↓
Night sees it and decides:
  "Deploy model selection training across all practices"
  ↓
Educator executes:
  "Model curriculum rollout across all 6 foundation practices"
```

### Educator → Token Optimizer Collaboration

```
Token Optimizer reports:
  "Haiku-to-Sonnet quality ratio is 0.78/0.87 = 89.6% (acceptable for 67% cost reduction)"
  ↓
Educator learns:
  "Haiku is viable for 30% of our work"
  ↓
Educator teaches practices:
  "Model curriculum: when to use Haiku without quality loss"
  ↓
Practices adopt:
  "Haiku usage increases from 5% to 30%"
  ↓
Feedback loop validates:
  "Quality maintained; token costs reduced 25% foundation-wide"
```

---

## ACTIVATION CHECKLIST (Week of Aug 21)

### By Aug 23
- [ ] Extract all artifacts (findings, decisions, unknowns, assumptions) from past 8 weeks
- [ ] Design Johari Window categorization scheme
- [ ] Build artifact browser tool (query + filter)

### By Aug 25
- [ ] Categorize all artifacts into 4 quadrants
- [ ] Generate distribution report (% in each quadrant)
- [ ] Identify over/under-represented areas

### By Aug 26
- [ ] Flag 5 "unknown-knowns ready for articulation"
- [ ] Flag 3 "blind spots to investigate"
- [ ] Design validation experiments for recent decisions

### By Aug 28
- [ ] Publish first Johari Window Assessment
- [ ] Publish first "Unasked Questions" report (5-10 questions)
- [ ] Set up decision feedback loop dashboard

### By Sep 1
- [ ] Complete decision feedback loop setup
- [ ] Begin weekly "Unasked Questions" cadence
- [ ] Publish first model ecosystem knowledge update

---

## RESOURCES REQUIRED

**Team:** 1 dedicated practice lead (epistemology + learning + model ecosystem knowledge)

**Tools:**
- Artifact browser (query findings, decisions, unknowns, assumptions)
- Johari Window dashboard (quadrant visualization)
- Decision feedback loop tracker (predicted vs. actual validation)
- Model capability matrix (updated quarterly)
- Learning curriculum design system

**Knowledge Base:** 
- Anthropic model docs (Haiku/Sonnet/Opus specs)
- Ollama model registry (local models)
- HuggingFace model cards (open-source)
- Model benchmarks (quality, speed, cost)

---

## SUCCESS METRICS (90-Day Check-in — Nov 14)

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Known-Knowns growth** | +20% | Artifacts categorized as known-knowns in Johari |
| **Unknown-Unknowns reduction** | -10% | Blind spots discovered + investigated |
| **Decision prediction accuracy** | 85%+ | Predicted impact vs. actual, via feedback loops |
| **Questions generated per week** | 5-10 | "Unasked Questions" reports published weekly |
| **Learning transfer rate** | 60%+ | % of practices adopting cross-practice learning |
| **Model selection adoption** | 50%+ | % of practices using tiered model strategy |
| **Recursive learning cycles** | 4+ per quarter | Full feedback loops (predict → validate → learn) |

---

**Status:** ✅ ACTIVATED  
**Authority:** Night (empirica-foundation Admiral)  
**Launch:** Aug 21, 2026  
**First Deliverable:** Johari Window Assessment (Aug 28)
