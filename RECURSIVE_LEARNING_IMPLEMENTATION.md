# Recursive Learning Implementation — Charter Integration

**Admiral:** Carly R. Anderson

**Date:** July 17, 2026 (updated)

**Status:** ✅ Charter enhanced with recursive learning + Gate POSTFLIGHT protocol + HumanAIOS ↔ Empirica coordination wired

---

## What Was Added to the Charter

The charter now includes a new section: **"Recursive Learning & Gate POSTFLIGHT Protocol"**

This makes the charter SELF-CORRECTING across gates. Each gate produces learnings that feed forward to inform the next gate's design.

---

## How Recursive Learning Works

### Gate POSTFLIGHT Template

After each gate decision, Admiral logs a finding capturing:

1. **Predicted** — What was supposed to happen (from pre-gate planning)
2. **Measured** — What actually happened (gate results)
3. **Gap** — Difference between predicted and measured
4. **Learning** — What this reveals about the system
5. **Action** — How does this change the NEXT gate's design?

### Worked Example: Gate 2 (Month 6)

**Before Gate 2:** Criterion 4 study launches to test whether Learning Index predicts behavior

**Predicted:** Empirica will show r ≥ 0.55 consistently across Claude, GPT-4, and custom models

**Gate 2 closes (Month 6):** Admiral gets results

**Measured:** 
- Claude: r = 0.72 ✅ Strong
- GPT-4: r = 0.61 ✅ Meets bar
- Custom: r = 0.58 ✅ Meets bar
- **Variance:** Claude >> Custom (28% gap)

**Gap:** Criterion 4 predictive validity holds, but model architecture variance is higher than anticipated (3x higher than expected range)

**Learning:** Oversight partners will deploy ACAT on their specific models. Single-threshold Learning Index may not be sufficient. Model-specific calibration guidance may be needed.

**Action:** Gate 3 partner selection should prioritize oversight bodies willing to trial model-specific Learning Index variants. Gate 4 trial should measure whether model-specific calibration improves oversight utility.

### CLI Command (Gate 2 POSTFLIGHT)

```bash
empirica finding-log \
  --finding "Gate 2 POSTFLIGHT (Month 6): Criterion 4 predictive validity established (r≥0.55 across 3 models), but model architecture variance (Claude r=0.72 >> Custom r=0.58) is 3x higher than predicted. Oversight partners will need model-specific calibration guidance." \
  --impact 0.85 \
  --enabled-by "gate-2-postflight" \
  --informs "gate-3-partner-strategy" \
  --trajectory-type "gate_learning_→_next_gate_design" \
  --causal-strength 0.9 \
  --cross-session \
  --visibility shared
```

**Key flags:**
- `--trajectory-type "gate_learning_→_next_gate_design"` — marks this as a recursive learning loop closure
- `--cross-session` — persists across sessions (not ephemeral)
- `--visibility shared` — other practices can see this learning (e.g., HumanAIOS)

---

## The Recursive Loop Closes Here

**Gate 3 (Month 9):** Admiral plans partner selection and trial scope

Admiral now has Gate 2 POSTFLIGHT finding in context:
- "Model variance is load-bearing. Don't select a partner with just one model type. Pick oversight bodies willing to test model-specific calibration."

**Result:** Gate 3 is INFORMED by Gate 2's discovery. No knowledge is lost. Gate 3 doesn't start blind.

---

## HumanAIOS ↔ Empirica: Two Loops, Interlocked

### Loop 1: HumanAIOS SMAG (Organizational Learning Density)

**Measure:** Does research finding flow to implementation?

**Metric:** Learning trajectory density (via SMAG ledger)

**Cadence:** Weekly (tight loop, compounding)

**Current state:** 26% density (low) → improving via empirica CLI wiring

**What it tracks:** Finding created → Code implemented → Link tracked = learning happened

### Loop 2: Empirica Charter (Deployment Readiness)

**Measure:** Do charter criteria flow to oversight deployment?

**Metric:** Criterion 8 readiness (via Gate 4)

**Cadence:** Gates every 2-4 months (discrete milestones)

**Current state:** Criteria 1-3 ✅ ready; Criteria 4-7 ❓ in progress

**What it tracks:** Criterion evidence → Gate decision → Next gate design → Deployment trial

### How They Coordinate: Cross-Project Findings

**When Gate 2 reveals model variance:**

Admiral logs a finding in HumanAIOS project (not evaluator seat):

```bash
empirica finding-log \
  --project-id humanaios \
  --finding "Charter Gate 2 reveals: ACAT criterion validity varies by model architecture (Claude r=0.72 >> Custom r=0.58). Recommend corpus expansion to prioritize model diversity." \
  --impact 0.8 \
  --enabled-by "empirica-gate-2-postflight" \
  --informs "humanaios-corpus-expansion-criterion-5" \
  --trajectory-type "charter_learning_→_framework_refinement" \
  --cross-session \
  --visibility shared
```

**Result:**
- Gate 2 discovery (model variance) → HumanAIOS responds (corpus expansion)
- Criterion 5 (corpus stability) improves faster due to targeted diversity
- Gate 3 partner selection has better data (more diverse corpus validates model variance finding)
- Gate 4 trial protocol is shaped by joint evidence (empirica + humanaios)

**Loop closes and tightens:** Empirica → HumanAIOS → Empirica (recursive)

---

## Weekly Rhythm (With Recursive Checks)

### Monday 9am: SER 1 State Snapshot

```bash
empirica smag-metrics --ser-id ser_1 --output json
```

**Check:**
- Learning density per criterion (SMAG)
- Any Gate POSTFLIGHT findings pending? (if gate just closed)
- Has prior gate's POSTFLIGHT learning been incorporated? (check SER 1 trajectories)

**Example Monday snapshot (Week after Gate 2):**

```
Monday Jul 27 (1 week after Gate 2 POSTFLIGHT):

Criterion 1: ✅ Complete (published)
Criterion 2: ✅ Complete (live)
Criterion 3: ✅ Complete (documented)
Criterion 4: ✅ Evidence gathered (Gate 2 POSTFLIGHT logged)
Criterion 5: ⚠️ Corpus expansion starting (responding to Gate 2 learning)
Criterion 6: 🔄 Paper refinement per Gate 2 variance finding
Criterion 7: 🔄 Governance docs updated per new model-specific requirements
Criterion 8: ⏳ Not started (gated on Gate 3)

Gate 2 POSTFLIGHT: ✅ LOGGED
Gate 2 learning incorporated into:
  - SER 2: David's criterion 4 refined (model-specific focus)
  - SER 2: DeMarius' governance audit (model-specific mitigations)
  - SER 3: Partner strategy (prioritize model-diverse oversight bodies)

HumanAIOS ↔ Empirica coordination:
  - Gate 2 learning logged in humanaios project ✅
  - Corpus expansion prioritizing model diversity ✅
  - Cross-project SMAG trajectory created ✅

Next: Gate 3 (Oct 1) ready if SER 2/3 stay on track
```

### Wednesday 2pm: Advisory Sync

**Agenda:**
1. Review POSTFLIGHT findings from most recent gate
2. Discuss: "Are next gate's design changes clear?"
3. Check: "Are SER 2 and SER 3 incorporating prior gate's learning?"
4. Monitor: "Is HumanAIOS SMAG density improving? Is organizational learning accelerating?"

**Example Wednesday sync (1 week after Gate 2):**

- Berlin call (30/60-day cadence): "Gate 2 revealed model variance. How should this shape Gate 3 partner strategy?"
- David check-in: "Are you testing model-specific Learning Index variants per Gate 2 POSTFLIGHT?"
- DeMarius check-in: "Are governance docs including model-specific dual-use mitigations?"
- HumanAIOS check-in: "Is corpus expansion on track? Any blockers?"

### Friday 4pm: Escalation & Loop Tightness Check

```bash
empirica smag-escalations --threshold 3days
```

**Check:**
1. Any Gate POSTFLIGHT findings created this week? (if gate closed Mon-Fri)
2. Any SER 2 trajectories stalled due to POSTFLIGHT learnings not incorporated?
3. Is HumanAIOS ↔ Empirica coordination tight? (are learnings flowing both directions?)
4. Are loop tightness metrics improving? (organizational learning density + deployment readiness both advancing?)

**Example Friday check (Week after Gate 2):**

```
Friday Jul 29 (3 days after Gate 2 POSTFLIGHT):

Gate 2 POSTFLIGHT: ✅ Logged (trajectory type: gate_learning_→_next_gate_design)

SER 2 escalations:
  - David's trajectories: ✅ Active (empirica findings flowing)
  - DeMarius' trajectories: ✅ Active (governance audit incorporating model variance)
  - No stalls ✅

HumanAIOS ↔ Empirica coordination:
  - Cross-project finding logged: ✅ charter_learning_→_framework_refinement
  - Corpus expansion responding: ✅ Model diversity priority increased
  - Loop tightness: 🟢 GOOD (both systems learning and adjusting)

Next week's focus:
  - Ensure SER 3 partnership conversations incorporate Gate 2 learning
  - Verify Gate 3 partner selection criteria refined per model variance finding
```

---

## Gate Timeline (With POSTFLIGHT Recursion)

| When | Event | POSTFLIGHT? | Informs |
|---|---|---|---|
| **Aug 1** | Gate 1: Longview decision → Track A/B/C | ✅ Gate 1 POSTFLIGHT | Track A plan (resource allocation, timeline confirmation) |
| **Aug 15** | Phase 1: Team hired, criterion 4 study designed | (Ongoing) | Per Gate 1 POSTFLIGHT learning |
| **Aug 31** | Gate 2: Criterion 4 evidence → model variance found | ✅ Gate 2 POSTFLIGHT | Gate 3 partner strategy (model-specific focus) |
| **Sep 15** | Phase 2: Criterion 4 refined per model variance; HumanAIOS corpus expanded | (Ongoing) | Per Gate 2 POSTFLIGHT learning + cross-project coordination |
| **Oct 1** | Gate 3: Partner ready? Trial scope confirmed? | ✅ Gate 3 POSTFLIGHT | Gate 4 trial protocol (model-specific testing) |
| **Oct 15** | Phase 3: Deployment trial starts with model-aware protocol | (Ongoing) | Per Gate 3 POSTFLIGHT learning |
| **Jan 1** | Gate 4: Trial success measured; criterion 8 proven? | ✅ Gate 4 POSTFLIGHT | Scaling strategy (next-round funding, expansion) |

**Key insight:** Every gate starts INFORMED by the prior gate's POSTFLIGHT learning. No gate ever starts blind.

---

## Implementation: Week 1 Actions

### Action 1: Wire Gate POSTFLIGHT Trajectory Type (Days 1-2)

Add trajectory type `gate_learning_→_next_gate_design` to SMAG:

```json
{
  "trajectory_type_slug": "gate_learning_→_next_gate_design",
  "source_type": "finding",
  "source_entity": "gate_N_postflight",
  "target_type": "gate_planning",
  "target_entity": "gate_N+1_design",
  "link_semantics": "Gate N learning shapes Gate N+1 design",
  "causal_strength_min": 0.85,
  "escalation_days": 3,
  "escalation_trigger": "No POSTFLIGHT finding created within 3 days of gate decision"
}
```

### Action 2: Define Gate POSTFLIGHT Template (Day 2)

Standardize what Admiral logs after each gate:

```bash
# Template: Gate N POSTFLIGHT (copy and fill in)

empirica finding-log \
  --finding "Gate [N] POSTFLIGHT ([Date]): [Predicted vs Measured summary]. [Gap]. [Learning]. [Action for Gate N+1]." \
  --impact [0.7-0.95] \
  --enabled-by "gate-[N]-postflight" \
  --informs "gate-[N+1]-design" \
  --trajectory-type "gate_learning_→_next_gate_design" \
  --causal-strength 0.9 \
  --cross-session \
  --visibility shared
```

### Action 3: Brief Admiral on Gate POSTFLIGHT Protocol (Day 3)

- Gate decision made → Admiral creates POSTFLIGHT finding within 3 days
- POSTFLIGHT captures: Predicted vs Measured vs Gap vs Learning vs Action
- POSTFLIGHT logged as shared finding (other practices can reference)
- SER 1 escalation: No POSTFLIGHT within 3 days → escalate

### Action 4: Wire HumanAIOS ↔ Empirica Cross-Project Findings (Days 3-4)

When Gate 2 (or any gate) reveals learnings relevant to HumanAIOS:

```bash
# Log in humanaios project (not evaluator seat)

empirica finding-log \
  --project-id humanaios \
  --finding "[Gate N finding relevant to framework]. [How it should shape humanaios development]." \
  --impact [0.7-0.9] \
  --enabled-by "empirica-gate-[N]-postflight" \
  --informs "humanaios-[relevant-criterion]" \
  --trajectory-type "charter_learning_→_framework_refinement" \
  --cross-session \
  --visibility shared
```

### Action 5: Update Weekly Rhythm Template (Day 4)

Modify SER 1 Monday snapshot to include:
- "Any Gate POSTFLIGHT findings pending?" (check in last 3 days)
- "Has prior gate's POSTFLIGHT learning been incorporated?" (check SER 1/2/3 trajectories)

Modify Friday escalation check to include:
- "Is HumanAIOS ↔ Empirica coordination tight?" (both loops tightening?)

### Action 6: Create Gate 1 POSTFLIGHT Template (Day 5)

Prepare Admiral for Gate 1 (Aug 1, Longview decision):

```bash
# Gate 1 POSTFLIGHT template (ready for Aug 1)

Predicted: Longview will fund Track A ($420k/12mo) for full criterion 8 execution
Measured: [Result: approved/approved-conditional/rejected]
Gap: [If conditional, what conditions? If rejected, what alternatives?]
Learning: [What does Longview's decision reveal about market/prioritization?]
Action: [How does this shape Phase 1 resource planning? Do criteria priorities change?]
```

---

## Congruence Verification

### Are HumanAIOS SMAG and Empirica Charter Congruent?

**YES — after this enhancement.**

| Dimension | HumanAIOS SMAG | Empirica Charter | Aligned? |
|---|---|---|---|
| **Measurement** | Learning trajectory density | Criterion 8 readiness | ✅ Both measure "does learning flow to action?" |
| **Loop type** | Recursive (weekly compounding) | Recursive (gate POSTFLIGHT) | ✅ Both are self-correcting |
| **Knowledge loss** | Zero (trajectories auto-linked) | Zero (POSTFLIGHT captures learning) | ✅ No silent knowledge gaps |
| **Cross-project coordination** | Findings tagged `--visibility shared` | Findings tagged `--visibility shared` | ✅ Both systems aware of each other |
| **Cadence** | Weekly (tight loop) | Gates every 2-4 months (discrete) | ✅ Different cadences, same principle |
| **Escalation** | Trajectory stall → escalate | POSTFLIGHT missing → escalate | ✅ Both escalate knowledge gaps |
| **Next-stage input** | Week N learning → Week N+1 focus | Gate N learning → Gate N+1 design | ✅ Both feed forward |

---

## Measurement: Are Loops Tightening?

**Metric 1: HumanAIOS SMAG Learning Density**
- Current: 26% (Week 1 of empirica CLI wiring)
- Target by Week 4: 40% (with CLI wiring complete)
- Target by Gate 2: 55% (empirica CLI mature, findings flowing automatically)

**Metric 2: Empirica Gate Preparation Quality**
- Current: Gate 2 (Aug 31) planned from June research
- With recursion: Gate 2 designed per Gate 1 POSTFLIGHT learning
- Gate 3 (Oct 1) designed per Gate 2 POSTFLIGHT learning
- Gate 4 (Jan 1) designed per Gate 3 POSTFLIGHT learning
- **Signal:** Each gate's design quality improves as it incorporates prior gate's learning

**Metric 3: Cross-Project Finding Volume**
- Current: 0 (not yet wired)
- Target by Gate 2: ≥5 cross-project findings (Gate discoveries flowing to HumanAIOS)
- Signal: Both systems learning from each other

---

## Admiral Decision

**Question:** Proceed with recursive learning implementation?

**Recommendation:** ✅ **YES — immediately**

**Why:**
1. Charter now self-correcting (Gate POSTFLIGHT ensures no knowledge is lost)
2. HumanAIOS ↔ Empirica loops interlocked (organizational + deployment learning congruent)
3. Weekly rhythm includes recursion checks (loop tightness visible)
4. Minimal implementation cost (1 trajectory type + cross-project finding wiring)
5. High benefit (prevents silent failures, tightens learning loops)

**Week 1 actions:** See Implementation section above (6 actions, Days 1-5)

---

**Status:** ✅ Charter enhanced with recursive learning + Gate POSTFLIGHT protocol

**Commit:** bf6eff3 — "Charter Enhancement: Add Recursive Learning + Gate POSTFLIGHT Protocol + HumanAIOS ↔ Empirica Coordination"

**Next:** Execute Week 1 actions to activate recursive learning

