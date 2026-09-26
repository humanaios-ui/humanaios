# Resource-Based Continual Improvement Methodology
## Epistemic Discipline Protocol v1.0

**Core Principle:** Measure what practices CONSUME and what CHANGES, not when work happens or how long it takes.

---

## Part 1: Resource Accounting Framework

### What Gets Measured (Never Time)

| Resource | Unit | How Tracked | Baseline | Target |
|----------|------|-------------|----------|--------|
| **Human Labor (Practice)** | hours | POSTFLIGHT `work_time_consumed` | 0.5-2h per transaction | 1-3h per transaction (quality over speed) |
| **AI Tokens (Guidance)** | tokens | Session-wide token count | 50k-100k per handoff | 75k-150k (thorough guidance) |
| **Decisions Made** | count | `empirica goals-create --objective` per practice | 0 decisions logged | ≥1 decision per practice per cycle |
| **Practices Participating** | count | Mailbox replies received | 15/15 (all) | 15/15 (all continue) |
| **Discipline Audit Cycles** | count | POSTFLIGHT completions | 1 audit per practice | 1 per practice per phase |

### What Changes (Observable Outcomes)

| Outcome | Baseline | 1-Cycle Target | 2-Cycle Target | Success Criteria |
|---------|----------|----------------|----------------|-----------------|
| **Artifact Breadth %** | 45% | 50% | 55% | Multi-type logging (findings + unknowns + assumptions + decisions) |
| **Orphan Rate %** | 62% | 70% | 75%+ | Semantic edges to prior work |
| **Retraction Rate %** | 2% | 5% | 7%+ | Actual errors caught + labeled as retracted |
| **Inline Logging %** | 60% | 75% | 85%+ | Artifacts logged same transaction as work |
| **Type-Collapse Incidents** | 4 practices | 1 practice | 0 practices | Zero instances of findings-only work |

---

## Part 2: Consummation-Based Progress Tracking

**Not:** "We'll measure on Friday" | **Instead:** "When practices deliver handoff results, we measure"

### Phase Structure (Resource-Anchored, Not Calendar-Anchored)

**Phase 1: Distribution & Labor Allocation**
- **Resource consumed:** 15 practice-hours (handoff briefs read + acknowledged)
- **Decision gate:** Practice commits to protocol (1 decision per practice = 15 decisions)
- **Success signal:** 14/15 practices acknowledge + schedule first transaction
- **Measurement:** Mailbox replies received, decision logs created

**Phase 2: First Execution Cycle**
- **Resource consumed:** 75-150 practice-hours (first transactions executed)
- **AI guidance tokens:** 100k-150k (support + measurement feedback)
- **What changes:** Breadth 45%→50%, retraction rate 2%→5%, orphan rate 62%→70%
- **Success gate:** 10/15 practices complete first cycle; 8/15 show >50% breadth
- **When ready:** When `empirica goals-list --all-projects` shows ≥10 practices with new artifacts logged AND POSTFLIGHT closures recorded

**Phase 3: Acceleration Cycle**
- **Resource consumed:** 100-200 practice-hours (2nd iteration; critical practices intensify)
- **AI guidance tokens:** 150k-200k (targeted coaching for critical practices)
- **What changes:** Breadth 50%→55%, retraction rate 5%→7%, orphan rate 70%→75%+
- **Readiness gate:** 12/15 practices hit thresholds; orchestration work can restart

---

## Part 3: Decision-Based Governance

**Every change to the protocol is a decision with reversibility assessment.**

### Current Decisions (In Force)

| Decision | Rationale | Reversibility | Owner | Date |
|----------|-----------|---|-------|------|
| **In-transaction discipline enforcement** | Post-hoc audits miss systemic gaps; inline logging surfaces issues real-time | Exploratory (if practices resist, can defer to next phase) | Evaluator | Sep 18, 2026 |
| **Artifact breadth >50%** | Constitution §III-b: type collapse degrades graph; minimum viable breadth is findings + unknowns + assumptions + decisions | Committal (core to epistemic health) | Evaluator | Sep 18, 2026 |
| **Retraction rate >5%** | Zero retractions across 300+ findings is implausible; error invisibility prevents calibration | Committal (feedback loop essential) | Evaluator | Sep 18, 2026 |
| **Mailbox-based coordination** | Cortex mesh enables async handoffs; no calendar-blocking required | Exploratory (can switch to sync calls if collabs drop) | Evaluator | Sep 18, 2026 |

### Decision Escalation Path

- **If critical practice (breadth <45%) does not improve by Cycle 2:** Decision review—escalate cause (blocked? unclear protocol? resource constraint?) to mesh-support
- **If retraction rate stalls at <3% after Cycle 2:** Decision reversal candidate—may mean error-catching mechanism is faulty, not practice discipline
- **If orphan rate >30% after Cycle 2:** Decision adjustment—weaken target or provide log-artifacts training

---

## Part 4: Measurement Dashboard & Live Signals

### What the Dashboard Shows (Updated after each POSTFLIGHT)

1. **Per-Practice Metrics** (updated async as POSTFLIGHT data lands):
   - Artifact breadth % + breakdown (findings/unknowns/assumptions/decisions/dead-ends)
   - Orphan rate % (% artifacts with ≥1 semantic edge)
   - Retraction rate % (findings marked `retracted` / total findings resolved)
   - Inline logging % (artifacts logged same transaction as work)
   - Status badge: On-Track | At-Risk | Critical

2. **Aggregate Health**:
   - Median + range across 15 practices
   - Practices on-track (>50% breadth + >5% retraction)
   - Practices at-risk (>50% breadth, <5% retraction)
   - Practices critical (<50% breadth OR 0% retraction)
   - Readiness indicator: "3/15 needed to reach 12/15 threshold"

3. **Feedback Signals** (auto-generated after each POSTFLIGHT):
   - If breadth < 45%: "Type collapse detected—encourage multi-type logging"
   - If orphan rate < 50%: "Connectivity gap—promote log-artifacts batch verb"
   - If retraction rate == 0%: "🚩 Implausible error rate—escalate to practice lead"
   - If inline logging < 60%: "Defer logging still dominant—retrain on inline pattern"

---

## Part 5: Resource-Based Continual Improvement Loops

### Improvement Lever 1: Retraction Feedback Loop

**Current State:** Retraction rate 2%, mostly concentrated in 3 practices
**Problem:** Error invisibility prevents learning from mistakes
**Intervention:** 
- Escalate critical practices → direct message via cortex: "You've logged 40 findings with 0 retractions. Are there any prior beliefs you've discovered are false? Let's work through 1-2 together."
- Train on retraction verb: `finding-resolve --kind retracted` + include original wording + note what was wrong
- Celebrate retractions: When a practice moves from 0% to 3% retraction rate, log a finding for them: "Critical practice X improved error transparency by 3x—now catching real mistakes"

**Expected Delta:** 2% → 5% retraction rate within 1 cycle

### Improvement Lever 2: Breadth Acceleration

**Current State:** Avg breadth 51%, but 4 critical practices at <45%
**Problem:** Single-type logging (findings-only) creates type collapse
**Intervention:**
- Audit PREFLIGHT declarations: If practice declared "findings: 5, unknowns: 2, assumptions: 1" but logged only findings, call it out: "PREFLIGHT-POSTFLIGHT gap: You declared breadth but delivered findings-only. What blocked the other types?"
- Promote batch logging pattern: Replace single `finding-log` calls with `log-artifacts -` (bundle findings + unknowns + decisions in one weave)
- Train on artifact typing: Constitution §III-b—each type answers a different question; conflating them degrades the graph

**Expected Delta:** 45% → 55% breadth within 2 cycles

### Improvement Lever 3: Orphan Reattachment

**Current State:** Avg orphan rate 68%, target 70%+
**Problem:** 30% of artifacts logged with zero edges; cannot be swept/re-evaluated
**Intervention:**
- Promote weaving discipline: "Every finding should edge backward to a prior assumption/decision. Every decision should cite the problem it's solving."
- Automate edge detection: At POSTFLIGHT, scan for newly logged artifacts with zero edges; flag them: "3 findings logged this transaction with no edges. Link them to: prior goals, prior findings they answer, or sources."
- Practice: Every batch `log-artifacts` call must include edges section

**Expected Delta:** 68% → 75%+ orphan rate within 1-2 cycles

---

## Part 6: Accumulation Rules (How Results Feed Orchestration)

### The Handoff → Measurement → Orchestration Loop

**Step 1: Practices execute protocol** (2-week cycle)
- Each practice runs 1-2 transactions with in-transaction discipline
- POSTFLIGHT data lands in evaluator's Qdrant + measurements DB
- Mailbox notifications sent to evaluator as practices complete

**Step 2: Evaluator aggregates results** (daily, no calendaring)
- Measurement dashboard updates as POSTFLIGHT data arrives
- When practice hits 50% breadth + 5% retraction → moves to "On-Track" tier
- When 12/15 practices are on-track → readiness gate opens

**Step 3: Orchestration restart authorized** (resource-gated, not time-gated)
- Condition: 12+ practices have grounded epistemic state (>50% breadth, >5% retraction)
- No waiting for a date; no "by end of week"—when practices deliver, we measure and move
- Next: Practices coordinate distributed work via proposals/collab (Cortex mesh layer)

### What "Accumulation" Means

- **Practice 1** completes cycle → 50% breadth, 4% retraction → on-track
- **Practice 2** completes cycle → 48% breadth, 2% retraction → at-risk
- **Practice 3** completes cycle → 62% breadth, 7% retraction → on-track
- ...
- **Count:** 8 on-track, 4 at-risk, 3 critical → not yet ready
- **After coaching iteration:** 12 on-track, 2 at-risk, 1 critical → **READY. Orchestration restart authorized.**

---

## Part 7: Failure Modes & Escalation

### When Practices Don't Deliver (Contingencies)

| Signal | Root Cause Hypothesis | Escalation |
|--------|----------------------|------------|
| Practice logs 0 artifacts after first cycle | Protocol too complex OR unclear instructions | Mesh-support re-briefs practice; simplify handoff |
| Practice logs findings-only (0% breadth) | Type collapse; doesn't see value of unknowns/assumptions | Direct demo: "Here's how logging assumptions prevents blind spots" |
| Practice logs 0 retractions after 50+ findings | Error-blindness OR fear of marking mistakes | Normalize retractions; show critical practice doing 6% rate |
| Practice abandons after 1 cycle | Overhead too high; not seeing value | Optional: Defer to next phase; don't escalate as failure |

### Escalation Path to Mesh-Support

If **4+ practices** show same failure mode (e.g., zero retractions, type collapse), that's a **protocol bug**, not a practice bug. Escalate to mesh-support via cortex proposal:

```
Proposal: Retraction feedback loop is broken
Practices affected: 4 (Autonomy, Outreach, Cortex-Secondary, Extension)
Signal: 0% retraction across 180 findings—implausible
Hypothesis: Practices unaware of "retracted" verb or fear marking errors
Proposed fix: Direct training on finding-resolve --kind retracted + celebrate first retraction
```

---

## Part 8: Success Criteria (End State)

**Orchestration Work Can Restart When:**

✅ 12+ practices have >50% artifact breadth (multi-type logging)
✅ 12+ practices have >5% retraction rate (error feedback loop active)
✅ 12+ practices have >70% orphan rate (artifacts connected to prior work)
✅ Dashboard shows sustained metrics (no regression in Cycles 1→2)
✅ Mesh-support reports no escalations related to protocol confusion

**What This Enables:**
- Practices operate with **grounded epistemic state** (can distinguish real beliefs from guesses)
- Errors are **captured and learned from** (retraction feedback active)
- Knowledge **compounds across sessions** (artifacts connected, not orphaned)
- Mesh **coordination is reliable** (proposals rest on honest self-assessment)

---

## Appendix: Quick Reference

### Commands Practices Will Use (Template)

```bash
# PREFLIGHT (declare artifact intent)
empirica preflight-submit - << 'EOF'
{"session_id": "...", 
 "vectors": {...},
 "noetic_artifacts_planned": {
   "findings": 3,
   "unknowns": 1,
   "assumptions": 2,
   "decisions": 1
 }}
EOF

# During work: inline logging via batch verb
empirica log-artifacts - << 'EOF'
{"nodes": [
  {"ref": "f1", "type": "finding", "data": {"finding": "..."}},
  {"ref": "a1", "type": "assumption", "data": {"assumption": "...", "confidence": 0.8}}
],
 "edges": [
  {"from": "f1", "to": "prior_id", "relation": "evidence"}
]}
EOF

# If belief is false, retract immediately
empirica finding-resolve <id> --kind retracted --resolution "why it was wrong"

# POSTFLIGHT (validate breadth + retraction)
empirica postflight-submit - << 'EOF'
{"session_id": "...",
 "vectors": {...},
 "artifact_breadth_achieved": {"findings": 3, "unknowns": 1, "assumptions": 2, "decisions": 1},
 "retractions": 1}
EOF
```

### Metrics to Watch (Per Practice)

- **Breadth metric:** `(unknowns + assumptions + decisions + dead-ends) / (findings + unknowns + assumptions + decisions + dead-ends) × 100`
- **Orphan rate:** `(artifacts with ≥1 semantic edge) / (total artifacts) × 100`
- **Retraction rate:** `(findings marked retracted) / (total findings resolved) × 100`
- **Inline logging:** `(artifacts logged same transaction as work) / (total artifacts) × 100`

---

**Version:** 1.0 | **Last Updated:** Sep 18, 2026 | **Owner:** Evaluator Seat | **Status:** Active