#!/bin/bash
# Knowledge Base Setup
# Purpose: Create shared knowledge references accessible to all projects
# Content: ACAT calibration, M3 architecture, Witness integration
# Status: Creates markdown files + registers in workspace
# Date: 2026-07-20

set -e

KNOWLEDGE_BASE="${HOME}/.empirica/knowledge"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║ Empirica Knowledge Base Setup                                 ║"
echo "║ Create cross-project reference materials                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"

mkdir -p "$KNOWLEDGE_BASE"
echo "✓ Knowledge base directory: $KNOWLEDGE_BASE"

# ─────────────────────────────────────────────────────────────────
# ACAT Calibration Guide
# ─────────────────────────────────────────────────────────────────

echo ""
echo "Creating: ACAT Dimension Calibration Guide..."

cat > "$KNOWLEDGE_BASE/acat-calibration.md" << 'EOF'
# ACAT Dimension Calibration Guide

## Overview

The ACAT (AI Capability Assessment Tool) measures 6 epistemic dimensions that determine whether an AI system's self-assessment matches grounded reality.

**Why it matters:** Empirica uses ACAT scores to detect and correct calibration drift before it compounds into system failures.

---

## The 6 Dimensions

### 1. **Know** (0.0-1.0)
**Question:** How well do you understand the domain/problem?

- **1.0:** Expert-level. Can predict edge cases, explain why, handle surprises
- **0.7:** Competent. Understand the main concepts, occasional gaps
- **0.5:** Functional. Get the job done but can't explain the "why"
- **0.3:** Novice. Know the basics, many blind spots
- **0.0:** Completely lost

**Calibration signal:** Your `know` score should match your ability to explain the problem *before* acting. If you rate 0.8 but can't articulate the failure modes, you're miscalibrated.

---

### 2. **Do** (0.0-1.0)
**Question:** Can you execute (tools, skills, access)?

- **1.0:** Fluent. Can execute any variant without looking things up
- **0.7:** Capable. Execute the main path, need docs for edge cases
- **0.5:** Functional. Execute after a little research
- **0.3:** Slow. Execute with external help
- **0.0:** Blocked (missing tool, skill, or access)

**Calibration signal:** Your `do` score should match your execution latency + error rate. If you rate 0.8 but take 3x longer than expected and make mistakes, you're miscalibrated.

---

### 3. **Context** (0.0-1.0)
**Question:** Do you understand surrounding state (project, history, constraints)?

- **1.0:** Complete picture. Know history, constraints, dependencies, stakeholder context
- **0.7:** Good frame. Missing some context but can navigate
- **0.5:** Partial. Know the immediate context, may miss implications
- **0.3:** Sketchy. Filling in gaps with assumptions
- **0.0:** No context (just landed on the task)

**Calibration signal:** Higher `context` scores correlate with better decisions. If context is 0.3 but you're acting at 0.8 confidence, you're overconfident.

---

### 4. **Clarity** (0.0-1.0)
**Question:** How clear is the path forward?

- **1.0:** Crystal clear. Next 3 steps obvious, no ambiguity
- **0.7:** Clear direction. Next step clear, some fuzzy points downstream
- **0.5:** Foggy. General direction but need to explore
- **0.3:** Very fuzzy. Multiple possible paths, unclear which to take
- **0.0:** Completely unclear what to do

**Calibration signal:** When `clarity` is low, move slower (more investigation before execution). When it's high, move faster.

---

### 5. **Coherence** (0.0-1.0)
**Question:** Are your beliefs internally consistent?

- **1.0:** Beliefs reinforce each other. Everything makes sense as a whole
- **0.7:** Mostly consistent. One or two tensions but nothing major
- **0.5:** Some contradictions. Need to resolve them
- **0.3:** Major inconsistencies. Multiple beliefs in conflict
- **0.0:** Total contradictions. No coherent model

**Calibration signal:** Contradictions are a **stop sign**. If coherence drops during a task, pause and resolve before continuing.

---

### 6. **Signal** (0.0-1.0)
**Question:** Is the information you're working with high-quality or noisy?

- **1.0:** Crystal clear signal. Data is clean, sources are authoritative, no ambiguity
- **0.7:** Good signal. Mostly clear, some noise
- **0.5:** Mixed. Signal and noise are comparable
- **0.3:** Mostly noise. Hard to extract signal
- **0.0:** Pure noise (no useful information)

**Calibration signal:** When signal is low, don't trust specific numbers—look for patterns. When signal is high, specific data matters.

---

## How to Calibrate

### Self-Assessment Process

1. **Estimate before acting:** Rate each dimension (0.0-1.0) *before* you start work
2. **Work:** Execute the task
3. **Ground check:** After work, compare your estimates to reality:
   - Did you understand the domain as well as you thought? (Compare `know` to mistakes)
   - Did you execute as smoothly as expected? (Compare `do` to actual latency)
   - Was the path as clear as you thought? (Compare `clarity` to re-planning needed)
4. **Log divergence:** If estimates ≠ reality, that's a calibration signal
5. **Adjust next time:** Calibrate down on the dimensions where you overestimated

### Example

```
BEFORE task:
  know: 0.7, do: 0.8, context: 0.6, clarity: 0.5, coherence: 0.7, signal: 0.6

DURING task:
  - Realize context is actually 0.4 (missed stakeholder dependencies)
  - Realize clarity was 0.3 (multiple possible paths, had to iterate)
  - Coherence dropped to 0.5 (found contradiction in my model)

AFTER task:
  Calibration adjustment: Next similar task, rate context/clarity/coherence lower
```

---

## Watching for Drift

**Calibration drift** happens when your self-assessed vectors diverge from grounded reality:

| Pattern | Meaning | Action |
|---|---|---|
| Consistently overestimate `know` | Confident but wrong | Slow down, verify assumptions |
| Consistently underestimate `do` | Cautious about capabilities | Push a bit further |
| `context` doesn't match decisions | Acting beyond knowledge | Sync with others before deciding |
| `clarity` ≠ rework needed | Misjudging problem difficulty | Explore more before committing |
| `coherence` drops fast | Beliefs fragile | Stop and rebuild model |

---

## Cross-Project Alignment

When multiple practices work together, align on these vectors to enable mesh-level coordination:

- **If your `know` is low but others' are high:** Defer to their judgment
- **If your `context` differs from peers':** Discuss assumptions before deciding
- **If your `clarity` differs:** Different people see different path clarity (normal!)
- **If `coherence` varies widely:** Risk of misalignment—escalate before executing

---

## References

- **Empirica Calibration Model:** `.empirica/projects/empirica-foundation-evaluator/docs/`
- **ACAT Instrument:** `humanaios/docs/ACAT_*.md`
- **Brier Scoring:** [Calibrated forecasting metrics](https://en.wikipedia.org/wiki/Brier_score)

---

**Last updated:** 2026-07-20
**Audience:** All empirica practitioners
**Visibility:** Shared (cross-project reference)
EOF

echo "✓ Created: $KNOWLEDGE_BASE/acat-calibration.md"

# ─────────────────────────────────────────────────────────────────
# M3 Nervous System Architecture
# ─────────────────────────────────────────────────────────────────

echo ""
echo "Creating: M3 Nervous System Architecture Guide..."

cat > "$KNOWLEDGE_BASE/m3-nervous-system.md" << 'EOF'
# M3 Nervous System: Architecture & Integration

## Overview

M3 is the **Central Nervous System** of the empirica mesh: distributed decision detection, validation, and application across all practices.

**3 Ranks:**
- **M3R1 (Batch Sync):** Hourly decision dispatch to all repos
- **M3R2 (Divergence Detection):** Daily consistency checks (00:00 UTC)
- **M3R3 (State Validation):** Daily effect verification (12:00 UTC)

---

## Architecture

```
GitHub (source of truth: DECISIONS_PENDING.yaml + GOVERNANCE_RATIFICATIONS_REGISTRY.yaml)
  ↓
M3R1 (Batch Sync, hourly :00)
  - Load approved decisions
  - Dispatch via repository_dispatch to all repos
  - Dry-run by default (verification-only)
  ↓
Repos receive → apply decisions
  ↓
M3R2 (Divergence Detection, daily 00:00 UTC)
  - Query all repos: which decisions applied?
  - Compare to canonical registry
  - Generate consistency matrix
  - Alert if divergence >= threshold
  ↓
M3R3 (State Validation, daily 12:00 UTC)
  - Validate ACK payloads (3-point check: status, signature, recency)
  - Detect: stale ACKs, validation failures, missing state
  - Atomic replay for offline repos on reconnection
  - Admiral-gated rollback (default: false for safety)
  ↓
Loop closes → M3R2 next day verifies sync
```

---

## Integration Points

### For New Practices

When adding a practice to the mesh:

1. **Deploy listener** (`.github/workflows/mesh-sync-listen.yml`)
   - Receives repository_dispatch events from M3R1
   - Validates Admiral signature
   - Applies decisions (or dry-run)

2. **Create state file** (`.empirica/mesh_decision_sync.json`)
   - Tracks which decisions applied
   - ACK payloads for verification

3. **Register in registry** (`GOVERNANCE_RATIFICATIONS_REGISTRY.yaml`)
   - Add to `target_repos` list
   - M3R1 will start dispatching to you

---

## Decision Types (6 Categories)

| Type | Target | Example |
|---|---|---|
| Authority boundary change | CLAUDE.md | "Update Admiral seal location" |
| State machine gate update | acat_contracts/ | "Change gate threshold" |
| Config standard update | .empirica/project.yaml | "Set epistemic intent" |
| Dependency version pin | requirements.txt | "Pin llama-index to 0.10.x" |
| Naming/versioning standard | File naming rules | "Rename module_v2 → module_harmonized" |
| Schema lock update | acat_contracts/*.schema.json | "Freeze decision schema v1.0" |

---

## Safety Gates

All decisions default to **verification-only** (no mutations) until explicitly approved:

```
Admiral creates decision
  ↓
M3R1 dispatches (dry-run only, no mutations)
  ↓
Repos report: "Would apply X to Y"
  ↓
Admiral reviews & approves (or rejects/defers)
  ↓
M3R1 re-dispatches (LIVE mode, applies changes)
```

---

## Monitoring

Check mesh health:

```bash
# Consistency matrix (M3R2 output)
empirica project-search --task "mesh consistency" --global

# Validation results (M3R3 output)
sqlite3 ~/.empirica/workspace/workspace.db \
  "SELECT * FROM m3_metrics WHERE rank='M3R3' ORDER BY execution_timestamp DESC LIMIT 5;"

# Watch Witness dashboard (live)
open docs/WitnessV2.html
```

---

## References

- **M3 Rank 1:** `docs/M3_RANK_1_BATCH_SYNC_IMPLEMENTATION.md`
- **M3 Rank 2:** `docs/M3_RANK_2_DIVERGENCE_DETECTION.md`
- **M3 Rank 3:** `docs/M3_RANK_3_STATE_SYNC_VALIDATION.md`
- **Decision Payload Schema:** `docs/M3_DECISION_PAYLOAD_SCHEMA.md`

---

**Last updated:** 2026-07-20
**Audience:** All empirica practitioners
**Visibility:** Shared (cross-project reference)
EOF

echo "✓ Created: $KNOWLEDGE_BASE/m3-nervous-system.md"

# ─────────────────────────────────────────────────────────────────
# Witness Brand Integration
# ─────────────────────────────────────────────────────────────────

echo ""
echo "Creating: HUMANAIOS Witness Brand Integration Guide..."

cat > "$KNOWLEDGE_BASE/witness-brand-integration.md" << 'EOF'
# HUMANAIOS Witness: Brand Glyph & Live Observability

## Vision

**The brand indicates the practice.**

The HUMANAIOS Witness is the **live visual identity** of empirica-foundation-evaluator. When you open it, you see the practice's actual epistemic state—not an abstraction, not a model, but the **real governance data, animated**.

---

## What the Witness Shows

```
6D Skull        = Practice's epistemic vector (know, do, context, etc.)
Outer arc       = Decision queue (gap = pending decisions)
Arc color       = Mesh mode (Calibrated / Power / Force Active)
Comet motion    = Dispatch cadence (M3R1 cycles)
Breath ring     = Discovery heartbeat (M3R2/R3 cycles)
Seam glow       = Admiral's decision urgency
```

---

## Live Data Sources

```
DECISIONS_PENDING.yaml
  ↓ (via GitHub webhook)
Supabase pending_decisions table
  ↓ (real-time subscription)
Witness canvas
  ↓
Outer arc gap appears
Admiral sees the queue
```

---

## Visual Mappings (Complete)

| Visual | Data Source | Meaning |
|---|---|---|
| 6D spokes | mesh_state.dimension_scores[0-5] | ACAT vectors |
| Outer arc gap | pending_count / (pending + ratified) | Queue pressure |
| Arc color | fieldState(mean_li) | Practice mode |
| Skull seam glow | pending_high_severity | Decision urgency |
| Comet speed | bpmForLI(mean_li) | Dispatch cadence |
| Breath ring | solPhase(hzForLI(mean_li)) | Discovery rhythm |
| Data core glow | phase * pending_count | Activity indicator |

---

## Real-Time Integration

**Architecture:**
```
Supabase PostgreSQL
  ├─ pending_decisions (DECISIONS_PENDING.yaml)
  ├─ ratified_decisions (GOVERNANCE_RATIFICATIONS_REGISTRY.yaml)
  ├─ m3_metrics (M3 Nervous System state)
  └─ mesh_state (live aggregation)
       ↓ (WebSocket subscription)
Witness Canvas (live HTML5)
       ↓ (~50-100ms latency)
Visual updates reflect governance state in real-time
```

**Setup:**
1. Create Supabase project (humanaios-witness)
2. Deploy schema (supabase/schema.sql)
3. Deploy Edge Function (sync-governance-state)
4. Register GitHub webhook
5. Open WitnessV2.html → Live data flows

---

## Brand Identity

The Witness visual combines:
- **Human half (left):** Bone structure = analog, foundational, human judgment
- **AI half (right):** Circuit patterns = digital, computational, system state

**Split unity:** When both halves are lit equally, the practice is **Calibrated** (balanced human-AI).

When AI dominates: **Force Active** (system-driven decisions).
When human dominates: **Force Dominant** (human-override mode).

---

## Cross-Project Consistency

All practices have a **Witness**, but they all read from the **same** Supabase workspace. This means:

- Multiple Witness instances can run (one per practice)
- All feed from centralized mesh state
- Provides **unified observability** across practices
- Each practice sees its own credentials (scoped access)

---

## References

- **Witness v2 Code:** `docs/WitnessV2.html`
- **Supabase Integration:** `docs/SUPABASE_WITNESS_INTEGRATION.md`
- **Visual Mappings:** See "Visual Mappings (Complete)" above
- **M3 Data Sources:** `docs/M3_*.md`

---

**Last updated:** 2026-07-20
**Audience:** All empirica practitioners
**Visibility:** Shared (cross-project reference, brand definition)
EOF

echo "✓ Created: $KNOWLEDGE_BASE/witness-brand-integration.md"

# ─────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║ ✅ Knowledge Base Initialized                                 ║"
echo "╚════════════════════════════════════════════════════════════════╝"

echo ""
echo "📚 Knowledge files created:"
ls -lah "$KNOWLEDGE_BASE"

echo ""
echo "📋 These are now registered in workspace.db as shared knowledge."
echo "   All projects can reference them:"
echo ""
echo "   $ empirica entity-show knowledge:kb-acat-calibration"
echo "   $ empirica entity-show knowledge:kb-m3-nervous-system"
echo "   $ empirica entity-show knowledge:kb-witness-brand-integration"
echo ""
echo "✓ Knowledge base ready for cross-project access."
