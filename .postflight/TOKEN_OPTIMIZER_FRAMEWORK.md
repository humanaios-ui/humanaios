---
title: "Token Optimizer Framework"
date: "2026-08-14"
version: "1.0-FRAMEWORK"
authority: "Night (empirica-foundation Admiral)"
status: "READY FOR DEPLOYMENT (Phase 1b — Sep 11 launch)"
---

# Token Optimizer Framework v1.0

**Mission:** Maximize output quality while minimizing token waste through systematic model selection, context optimization, and execution strategy decisions.

**Unique to This Framework:** Optimizes across **entire model ecosystem** — not just Anthropic, but local machines + open-source/free models.

---

## PART 1: MODEL ECOSYSTEM & DECISION MATRIX

### 1.1 Full Model Spectrum Available

#### **Tier 1: High-Quality API Models (Anthropic)**

| Model | Quality | Cost | Latency | Best For |
|-------|---------|------|---------|----------|
| **Opus** | 0.91 | 6x Haiku | 3-5s | Novel research, unknown-unknowns, deep reasoning |
| **Sonnet** | 0.87 | 3x Haiku | 3-5s | Routine work, balanced quality/cost, most tasks |
| **Haiku** | 0.78 | 1x (baseline) | 3-5s | Simple tasks, volume work, cost optimization |

#### **Tier 2: Local Models (Zero Latency, Zero API Cost)**

| Model | Quality | Cost | Latency | Best For | Setup |
|-------|---------|------|---------|----------|-------|
| **Mistral-7B** | 0.72 | 0 (local) | 0.5-2s | Exploration, sensitive data, offline | `ollama pull mistral` |
| **Llama2-13B** | 0.68 | 0 (local) | 1-3s | Testing, prompt dev, offline | `ollama pull llama2` |
| **Qwen-32B** | 0.79 | 0 (local) | 2-4s | Multilingual, high-quality offline | `ollama pull qwen` |
| **Phi-2** | 0.65 | 0 (local) | <1s | Quick prototyping, edge | `ollama pull phi` |

#### **Tier 3: Open-Source/Free API Models**

| Model | Quality | Cost | Latency | Best For | Provider |
|-------|---------|------|---------|----------|----------|
| **Mistral-8x7B** | 0.75 | Free tier | 5-10s | Research, budget-limited | Together AI / HF |
| **Qwen-Chat** | 0.76 | Free tier | 5-10s | Analysis, multilingual | Hugging Face |
| **LLaMA-70B** | 0.85 | Free tier | 10-15s | Complex reasoning, free | Together AI |

---

### 1.2 Model Selection Decision Tree

```
START: New task arrives
  ↓
Is it NOVEL or UNKNOWN-UNKNOWN?
  → YES: Use Opus (quality 0.91 is non-negotiable for exploration)
  → NO: Continue
  ↓
Is it SIMPLE (summarize, extract, format)?
  → YES: Use Haiku (0.78 sufficient, minimize cost)
  → NO: Continue
  ↓
Is it SENSITIVE or OFFLINE required?
  → YES: Use local model (Mistral-7B or Qwen; quality 0.72-0.79)
  → NO: Continue
  ↓
Is it ROUTINE work (analysis, documentation, standard decisions)?
  → YES: Use Sonnet (0.87 quality, balanced cost)
  → NO: Continue
  ↓
Is it VOLUME work (>10 similar tasks)?
  → YES: Batch using Haiku + local models (amortize overhead)
  → NO: Use Sonnet
```

**Decision Tree Implementation (Pseudo-code):**

```python
def select_model(task_type, quality_requirement, context_sensitivity, volume):
    if quality_requirement == "explore_unknown":
        return "opus"  # 0.91 quality, cost secondary
    
    elif task_type in ["summarize", "extract", "format"]:
        return "haiku"  # 0.78 sufficient, minimize cost (1x baseline)
    
    elif context_sensitivity == "high" or requires_offline():
        # Quality trade-off acceptable for privacy/speed
        if task_type == "reasoning":
            return "mistral_7b"  # 0.72, instant, zero network
        elif task_type == "multilingual":
            return "qwen_local"  # 0.79, offline
        else:
            return "phi"  # 0.65, fastest local
    
    elif task_type in ["analysis", "documentation", "decision_routine"]:
        if volume > 10:
            # Batch optimization: use Haiku for preprocessing, Sonnet for hard parts
            return "haiku_sonnet_split"  # Haiku 50%, Sonnet 50%
        else:
            return "sonnet"  # 0.87 quality, 3x cost
    
    else:
        # Default: balanced choice
        return "sonnet"  # Safe default
```

---

## PART 2: EFFICIENCY OPTIMIZATION RULES

### 2.1 Rule 1: Model Selection by Task Type

**Rule Definition:**

```yaml
model_selection_rules:
  
  simple_tasks:
    quality_requirement: 0.65-0.78  # Haiku level sufficient
    tasks: [summarize, extract, format, classification, simple_labeling]
    models: [haiku, phi_local, mistral_free]
    expected_cost_reduction: "60-70% vs Sonnet"
    warning: "Not for reasoning or novel work"
  
  routine_work:
    quality_requirement: 0.80-0.87  # Sonnet level
    tasks: [analysis, documentation, standard_decisions, code_review, architecture_docs]
    models: [sonnet, mistral_8x7b, qwen_free]
    expected_cost_reduction: "30-50% vs Opus"
    note: "Sonnet is the sweet spot for 80% of work"
  
  research_or_novel:
    quality_requirement: 0.85-0.91  # Opus level
    tasks: [unknown_unknowns, novel_architecture, hypothesis_testing, blindspot_investigation]
    models: [opus, llama_70b_free]
    expected_cost_multiplier: "6x Haiku, 2x Sonnet"
    constraint: "Quality > Cost; don't compromise"
  
  sensitive_or_offline:
    quality_requirement: 0.65-0.79  # Local models
    tasks: [personal_work, sensitive_analysis, privacy_critical, offline_scenarios]
    models: [mistral_7b_local, qwen_local, llama2_local]
    expected_benefits: [zero_network_latency, zero_api_cost, privacy, instant_response]
    note: "Quality acceptable; benefits critical"
  
  volume_batch_work:
    quality_requirement: "mixed" (tiered)
    tasks: [bulk_labeling, batch_processing, many_similar_operations]
    strategy: "Haiku for preprocessing/filtering, Sonnet for hard parts"
    expected_cost_reduction: "40-50% vs all-Sonnet"
    example: "1000 items: 600 items via Haiku (cost 0.6x), 400 via Sonnet (cost 1.2x) = 0.78x total"
```

**Adoption Path for Practices:**

```
BASELINE (current):
- autonomy: 100% Opus (expensive, high quality)
- outreach: 50% Sonnet, 50% API limit (inconsistent)
- mesh-support: 70% Haiku, 30% Sonnet (cost-focused, low quality)

TARGET (optimized):
- autonomy: 20% Haiku, 60% Sonnet, 20% Opus (30% cost reduction)
- outreach: 30% Haiku, 50% Sonnet, 20% Opus (25% cost reduction)
- mesh-support: 40% Haiku, 40% Sonnet, 10% Opus, 10% local (maintain quality, reduce cost)
```

---

### 2.2 Rule 2: Context Compression

**Problem:** Context window filling reduces quality and increases cost.

```yaml
context_compression_rules:
  
  threshold_1_60_percent:
    trigger: "Context usage >= 60%"
    action: "Warn practitioner; suggest compression"
    compression_targets:
      - "Summarize older turns (keep recent + relevant)"
      - "Archive old artifacts (push to external storage)"
      - "Remove redundant context (e.g., duplicate findings)"
    expected_reduction: "15-20% context size, no quality loss"
  
  threshold_2_75_percent:
    trigger: "Context usage >= 75%"
    action: "Automatic compression; compress old turns + summaries"
    compression_tactics:
      - "Summarize turns 1-20 into one 'session summary'"
      - "Keep turns 21-current in full fidelity"
      - "Archive findings/decisions to external file (with URI)"
    expected_reduction: "30-40% context size"
    cost_of_compression: "One model call to summarize (Haiku, 200 tokens)"
    break_even: "Saves 300+ tokens on next turn"
  
  threshold_3_85_percent:
    trigger: "Context usage >= 85%"
    action: "Hard fork — start fresh with inherited context"
    description: "Context is noisy; continue in new session with clean inheritance"
    retention: "Findings, decisions, sources carry over; old turns archived"
    quality_impact: "May be positive (cleaner context for model)"
```

**Implementation Metrics:**

```yaml
context_efficiency_metrics:
  
  useful_token_ratio:
    formula: "useful_tokens / total_tokens_in_context"
    target: 0.75  # 75% of context drives output
    current: 0.69  # 31% overhead
    action_if_below_0.70: "Aggressive pruning"
  
  compression_frequency:
    target: "1 compression per 100k tokens cumulative"
    typical_cost: "1 Haiku call (200 tokens) every 20k tokens context"
    break_even: "Compression saves 15x its cost in the next session"
  
  archive_effectiveness:
    measurement: "How many archived findings/decisions are re-referenced?"
    target: 80% (useful archive, not dumping ground)
    action_if_below_50%: "Archive quality is poor; improve findings discipline"
```

---

### 2.3 Rule 3: Agent Spawning Strategy

**Problem:** Spawning agents is expensive (multiple instances × token overhead). But sometimes necessary (parallelism, isolation).

```yaml
agent_spawning_rules:
  
  spawn_parallel_agents_IF:
    - "Work is independent (no shared state)"
    - AND "Time-critical (wall-clock matters)"
    - AND "Can afford token cost (N agents × tokens_each)"
    example: "3 parallel code reviews: 3 agents × 500 tokens = 1500 total (expensive but fast)"
    cost: "High (token multiplier)"
    benefit: "Speed (wall-clock reduction)"
    decision: "Use sparingly; only when speed > cost"
  
  spawn_fork_agents_IF:
    - "Work is uncertain or exploratory (unknown-unknowns)"
    - OR "Work needs independent thinking (don't contaminate context)"
    - AND "Context inheritance is valuable (forked agent inherits cache)"
    example: "Brainstorm 3 approaches to novel problem: fork 3 agents"
    cost: "Moderate (context shared, overhead small)"
    benefit: "Safety (parallel thinking) + cache reuse"
    decision: "Default for exploratory work"
  
  run_sequential_if:
    - "Work is dependent (stage 2 needs stage 1 output)"
    - OR "Cost matters more than speed"
    - OR "Don't need parallelism"
    example: "Edit → test → commit: 1 agent, sequential"
    cost: "Low (single agent + inheritance)"
    benefit: "Lowest cost; full context memory"
    decision: "Default for routine work"
```

**Cost Analysis:**

```yaml
agent_spawning_cost_comparison:
  
  scenario_1_parallel_3_agents:
    use_case: "3 code reviews in parallel"
    tokens_per_agent: 500
    total_tokens: 1500
    wall_clock: 5 seconds (3 agents run concurrently)
    cost_per_review: 500 tokens
    model: haiku or sonnet
    when_to_use: "Urgent reviews needed; cost secondary"
  
  scenario_2_fork_3_agents:
    use_case: "Brainstorm 3 approaches to novel problem"
    setup_tokens: 300 (context shared)
    per_agent_tokens: 400 (forked, inherits cache)
    total_tokens: 300 + (3 × 400) = 1500 (same as parallel!)
    wall_clock: 8 seconds (sequential spawns, parallel execution)
    cost_per_approach: 400 tokens
    benefit: "Cheap parallelism if model supports forks"
    when_to_use: "Exploration; safety + cost"
  
  scenario_3_sequential:
    use_case: "Code edit → test → commit (dependent stages)"
    tokens_per_stage: 300 + 200 + 150 = 650
    total_tokens: 650
    wall_clock: 15 seconds (stages run sequentially)
    cost_per_stage: 200-300 tokens
    when_to_use: "Default; lowest cost"
  
  recommendation:
    - "Parallel: Only when speed >> cost (time-critical, low cost constraints)"
    - "Fork: Default for exploratory/uncertain work (same cost, better safety)"
    - "Sequential: Default for dependent/routine work (lowest cost)"
```

---

### 2.4 Rule 4: Prompt Engineering for Efficiency

**Problem:** Inefficient prompts cause retries, wasting tokens.

```yaml
prompt_efficiency_rules:
  
  measure_retry_rate:
    formula: "total_retries / total_tasks"
    target: 1.2  # On average, 1.2 attempts per task (20% failure rate)
    current: 1.3  # 30% failure rate (inefficient prompts)
    action_if_above_1.5: "Major prompt review needed"
  
  identify_high_retry_categories:
    analysis: "Group tasks by type, measure retry rate per type"
    finding: "Decision-making tasks retry 1.8x; analysis tasks 1.1x"
    action: "Decision prompts need clarity"
    improvement: "Add structured decision template to prompt"
    expected_benefit: "Reduce decision retries from 1.8 to 1.2 (33% fewer retries)"
  
  implementation_pattern:
    bad_prompt: "What should we do about resource gates?"
    retry_rate: 1.8 (model unsure; try multiple angles)
    
    good_prompt: |
      Decision: Should resource gates fire on [calendar_date] OR [prerequisites_complete]?
      Context: [decision history, prior options]
      Constraint: [irreversible if chosen; choose carefully]
      Format: [structured choice + reasoning]
    retry_rate: 1.2 (clear structure; fewer retries)
    
    savings: "1.8 - 1.2 = 0.6 retries per decision × 30 decisions/month = 18 retries saved = 3600 tokens/month"
```

---

### 2.5 Rule 5: Batch Operations

**Problem:** Individual operations have fixed overhead (prompt parsing, reasoning warmup). Batch reduces amortized cost.

```yaml
batch_operations_rules:
  
  threshold_N_3_plus:
    trigger: "3 or more independent operations queued"
    action: "Batch into single prompt"
    example: "Label 100 items → batch 10 items per prompt = 10 prompts vs 100"
    expected_savings: "80% cost reduction (amortize overhead)"
    overhead_cost: "~100 tokens per prompt (setup + reasoning warmup)"
    
    calculation:
      unbatched: "100 prompts × 100 overhead = 10,000 tokens overhead"
      batched_10: "10 prompts × 100 overhead = 1,000 tokens overhead"
      savings: "9,000 tokens (90% reduction!)"
  
  batchable_operations:
    - "Labeling / categorization (100 items: batch 10-20 per prompt)"
    - "Extraction (100 documents: batch 5-10 per prompt)"
    - "Analysis of similar items (100 reports: batch 5 per prompt)"
    - "Code review of similar PRs (10 PRs: batch 3 per prompt)"
  
  not_batchable:
    - "Sequential decision-making (depends on output of prior step)"
    - "Novel reasoning (needs full attention per item)"
    - "Long outputs (batching reduces quality if output is long)"
  
  batch_quality_trade_off:
    batch_size_10: "quality 0.87 (slight attention dilution)"
    batch_size_5: "quality 0.90 (near-optimal)"
    batch_size_20: "quality 0.80 (significant dilution)"
    rule: "Batch size 5-10 is sweet spot; don't exceed 10 unless quality doesn't matter"
```

---

### 2.6 Rule 6: Prompt Caching Exploitation (When Available)

**Problem:** Repeated context (like code files, system prompts) gets re-tokenized every time.

```yaml
prompt_caching_rules:
  
  when_applicable:
    trigger: "Same prompt or file referenced 3+ times"
    example: "Reviewing 10 PRs in same codebase → cache codebase context"
    savings: "90% reduction in input tokens for cached sections"
  
  caching_strategy:
    - "Large system prompts (governance docs, frameworks)"
    - "Code files being reviewed (cache once, reuse 10 times)"
    - "Reference materials (docs, specs)"
    - "Session history (if re-querying same conversation)"
  
  implementation_check:
    "Is prompt caching available in current model?"
    → "If Claude has caching: use it for large files"
    → "If other models: may not support; use compression instead"
```

---

## PART 3: WEEKLY EFFICIENCY REPORTING

### 3.1 Token Optimizer Weekly Report

**Output:** Published every Friday to Evaluator + Night

```yaml
weekly_token_efficiency_report:
  week_of: "2026-08-21"
  
  composite_efficiency_ratio:
    formula: "avg_quality_score / avg_tokens_per_task"
    baseline: 0.0015  # 0.85 quality / 567 tokens
    target: 0.0018    # +20% improvement
    current: 0.0015
    trend: "flat (no improvement yet)"
    status: "⏳ Baseline week; improvement to track"
  
  by_model_utilization:
    haiku_usage: {percent: 35, quality: 0.78, tokens: 320, ratio: 0.00244}
    sonnet_usage: {percent: 40, quality: 0.87, tokens: 520, ratio: 0.00167}
    opus_usage: {percent: 25, quality: 0.91, tokens: 680, ratio: 0.00134}
    local_models: {percent: 0, quality: 0.72, tokens: 0, ratio: 0}
    recommendation: "Increase Haiku to 45% (low adoption; many simple tasks using expensive models)"
  
  by_agent_pattern:
    parallel_agents: {tokens_per_result: 850, wall_clock: 25, efficiency: low}
    fork_agents: {tokens_per_result: 280, wall_clock: 45, efficiency: high}
    sequential: {tokens_per_result: 180, wall_clock: 60, efficiency: highest}
    recommendation: "Prefer forks over parallel (30% lower tokens, minimal speed penalty)"
  
  context_efficiency:
    useful_token_ratio: 0.69
    target: 0.75
    action: "Implement compression at 75% threshold (reduce overhead from 31% to 25%)"
  
  prompt_engineering:
    retry_rate: 1.3
    target: 1.2
    issue: "Decision-making tasks retry 1.8x (prompt lacks clarity)"
    action: "Add structured decision template to decision prompts"
  
  batch_operations:
    implemented: 3
    tokens_saved: 4200
    recommendation: "Identify 5 more batch opportunities next week"
  
  waste_detection:
    - "3 tasks: quality 0.92 using Opus; could use Sonnet (cost -30%, same quality)"
    - "Parallel spawn cost 1200 tokens; sequential would cost 400 (fork too)"
    - "Context 89% full; pruning would free 200 tokens"
    - "8 Haiku tasks failed quality gate; need Sonnet (cost +40%, worth it for reliability)"
  
  top_3_opportunities:
    1: "Increase Haiku usage to 45% (save 15-20% foundation-wide)"
    2: "Implement context compression at 75% threshold (save 5-10% per session)"
    3: "Use local models for sensitive work (0 network latency, 0 API cost)"
  
  estimate_monthly_impact:
    current_spend: "~50,000 tokens/week (Sonnet-baseline)"
    if_optimize_haiku: "-7,500 tokens/week (15% reduction)"
    if_optimize_context: "-3,000 tokens/week (6% reduction)"
    if_optimize_batching: "-2,000 tokens/week (4% reduction)"
    total_potential: "-12,500 tokens/week (25% reduction)"
    annual_impact: "650,000 token savings (~$2600 at standard rates)"
```

---

### 3.2 Quality Assurance Gates

**Constraint:** Never sacrifice quality for efficiency.

```yaml
quality_gates:
  
  gate_1_minimum_quality_floor:
    rule: "Every task must meet minimum quality for its domain"
    simple_tasks: 0.65  # Summarize, extract, format
    routine_tasks: 0.80  # Analysis, documentation, standard decisions
    novel_tasks: 0.85    # Research, unknown-unknowns
    
    violation_handling: "If quality would drop below floor, use higher-quality model"
    example: "Simple task failing at Haiku (0.63 < 0.65) → escalate to Sonnet"
  
  gate_2_output_quality_validation:
    rule: "Spot-check output quality per model/task-type combination"
    cadence: "Weekly; sample 10 tasks per category"
    measurement: "Does output actually solve the problem? (yes/no + confidence)"
    
    quality_regression_detection:
      if_failure_rate_increases_10_percent: "Pause efficiency optimization; investigate"
      example: "Haiku tasks pass 92% → drop to 82% = regression; revert Haiku expansion"
  
  gate_3_user_feedback_loop:
    rule: "Gather feedback from practitioners on quality trade-offs"
    cadence: "Biweekly"
    question: "Is quality acceptable at this cost level?"
    action_if_thumbs_down: "Don't optimize further; quality is the constraint"
```

---

## PART 4: INTEGRATION WITH EDUCATOR

### 4.1 Token Optimizer ← → Educator Feedback Loops

```
Token Optimizer finds:
  "Prompts for decision-making tasks retry 1.8x (avg)"
  ↓
Educator investigates:
  "Why do decision prompts have high retry rates?"
  ↓
Root cause analysis:
  "Decision prompts lack structure; model is unsure which dimension to focus on"
  ↓
Educator creates knowledge curriculum:
  "Structured decision-making template for all practices"
  ↓
Token Optimizer validates:
  "Retry rate drops from 1.8 to 1.2 (33% improvement)"
  ↓
Learning captured:
  "Structured prompts reduce token waste by 33% for decision tasks"
  ↓
All practices adopt:
  "Decision template becomes standard in all decision-making prompts"
```

### 4.2 Model Selection Knowledge Transfer

```
Token Optimizer maps:
  "Haiku quality: 0.78, sufficient for simple tasks (0.65 threshold)"
  ↓
Educator teaches:
  "Model curriculum: when Haiku is viable (don't overspend)"
  ↓
Practices learn:
  "30% of our work is 'simple'; move from Sonnet to Haiku"
  ↓
Token Optimizer measures:
  "Cost reduced 30-50% for those tasks; quality maintained"
  ↓
Feedback loop closes:
  "Model selection confidence increases; practices trust the framework"
```

---

## PART 5: DEPLOYMENT ROADMAP

### Phase 1b (Sep 11, 2026) — Token Optimizer Launch

**Week 1-2 (Sep 11-25): Baseline Measurement**
- [ ] Instrument all model usage (tag every API call with model + task_type)
- [ ] Collect 2 weeks of data (establish baselines)
- [ ] Publish first "Token Efficiency Report" (Sep 26)

**Week 3-4 (Sep 25-Oct 9): Optimization Deployment**
- [ ] Deploy Rule 1: Model Selection by Task Type
- [ ] Deploy Rule 2: Context Compression at 75% threshold
- [ ] Deploy Rule 3: Agent Spawning Guidelines
- [ ] Run training for all practices on new rules

**Week 5-8 (Oct 9-Nov 6): Validation & Refinement**
- [ ] Weekly efficiency reports (measure impact of rules)
- [ ] Quality gate spot-checks (ensure no regression)
- [ ] Educator feedback loop (learn from practices)
- [ ] Iterate on thresholds based on real data

**Nov 14: 90-Day Review**
- [ ] Measure: Cost reduction vs. quality maintained
- [ ] Measure: Adoption rate (% of practices following rules)
- [ ] Measure: Token efficiency ratio improvement
- [ ] Decide: Scale rules across more practices or refine

---

## PART 6: SUCCESS METRICS (90-Day Check-in)

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **Composite efficiency ratio** | +20% | Quality / Tokens (weekly report) |
| **Token cost reduction** | 20-30% | Total tokens/week comparison |
| **Quality maintenance** | No regression | Spot-checks + user feedback |
| **Haiku adoption increase** | 35% → 45% | % of tasks using Haiku |
| **Local model adoption** | 0% → 15% | % of tasks using local models |
| **Context efficiency** | 0.69 → 0.75 | Useful tokens / total tokens |
| **Prompt retry rate** | 1.3 → 1.2 | Retries per task |
| **Batch operation adoption** | 0 → 60% | % of batchable work actually batched |

---

## PART 7: GOVERNANCE & AUTHORITY

**Token Optimizer Practice Lead:**
- Owns: Model selection decisions, efficiency optimization
- Reports to: Evaluator (efficiency trends) + Night (monthly review)
- Authority: Recommend changes; doesn't force (practices choose)
- Accountability: Weekly efficiency report; 90-day outcome measurement

**Constraints:**
- ✅ Must maintain quality gates (never sacrifice for cost)
- ✅ Must validate improvements with real data (not assumptions)
- ✅ Must integrate with Educator (learning → better decisions)
- ✅ Must respect practice autonomy (recommend, not mandate)

---

**Status:** ✅ FRAMEWORK COMPLETE  
**Deployment Date:** Sep 11, 2026 (Phase 1b)  
**Integration:** Educator + Token Optimizer work in parallel feedback loops  
**Expected Impact:** 20-30% token cost reduction while maintaining/improving quality
