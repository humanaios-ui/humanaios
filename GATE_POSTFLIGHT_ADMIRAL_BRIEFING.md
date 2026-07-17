# Gate POSTFLIGHT Protocol — Admiral Briefing

**Briefing For:** Carly R. Anderson (Admiral)

**Date:** July 18, 2026

**Duration:** 30 minutes

**Objective:** Ensure Admiral understands Gate POSTFLIGHT protocol and is ready to execute on Aug 1 (Gate 1)

---

## What Is Gate POSTFLIGHT?

A **POSTFLIGHT finding** is created by Admiral within 3 days after each gate decision closes.

It captures:
1. **Predicted** — What was expected to happen (from pre-gate planning)
2. **Measured** — What actually happened (gate results)
3. **Gap** — The difference between predicted and measured
4. **Learning** — What this reveals about the system
5. **Action** — How does this shape the NEXT gate's design?

**Purpose:** Ensure each gate's learning feeds forward to inform the next gate. No knowledge is left on the table.

---

## Why This Matters

### Without POSTFLIGHT
```
Gate 1 closes (Aug 1)
  ↓
Admiral reviews results
  ↓
[Learning might get lost in daily work]
  ↓
Gate 2 begins (Aug 31)
  ↓
[Gate 2 starts somewhat blind, missing Gate 1 insights]
```

### With POSTFLIGHT
```
Gate 1 closes (Aug 1)
  ↓
Admiral creates POSTFLIGHT finding (Aug 1-4)
  → Captures: What we predicted, what happened, gap, learning, action
  ↓
POSTFLIGHT trajectory created: gate_learning_→_next_gate_design
  ↓
Phase 1 planning informed by Gate 1 learning (not blind)
  ↓
Gate 2 begins (Aug 31) - INFORMED by Gate 1 POSTFLIGHT
  ↓
[Gate 2 starts with evidence from Gate 1]
```

---

## The Worked Example: Gate 2 (Month 6)

**Context:** Criterion 4 study (empirica cross-validation) has just finished. Results are in.

### Before Gate 2

**Predicted** (from April planning):
"Empirica will show Learning Index predictive validity r ≥ 0.55 consistently across Claude, GPT-4, and custom models. Model variance expected to be <10%."

### Gate 2 Closes (Aug 31)

**Measured** (actual results):
- Claude: r = 0.72 ✅ Strong
- GPT-4: r = 0.61 ✅ Meets bar
- Custom: r = 0.58 ✅ Meets bar
- **Variance:** Claude 0.72 vs Custom 0.58 = 28% gap (3x higher than expected)

### Admiral's POSTFLIGHT Analysis

**Gap:** 
"Criterion 4 predictive validity holds (all ≥0.55 bar), but model architecture variance (Claude >> Custom) is 3x higher than predicted. This wasn't accounted for in the original design."

**Learning:** 
"Oversight partners will deploy ACAT on their specific models (e.g., Claude for one org, GPT-4 for another). Single-threshold Learning Index may not be sufficient across different model architectures. Model-specific calibration guidance might be needed."

**Action:** 
"Gate 3 (partner selection, Oct 1) should prioritize oversight bodies willing to trial model-specific Learning Index variants. Gate 4 (deployment trial, Jan 1) should measure whether model-specific calibration improves oversight utility over single-threshold approach."

### Admiral Creates POSTFLIGHT (within 3 days of Gate 2 close)

Uses this template:

```bash
empirica finding-log \
  --finding "Gate 2 POSTFLIGHT (Aug 31): Criterion 4 predictive validity established (r≥0.55 across 3 models), but model architecture variance (Claude r=0.72 >> Custom r=0.58) is 3x higher than predicted. Oversight partners will need model-specific calibration guidance." \
  --impact 0.85 \
  --enabled-by "gate-2-postflight" \
  --informs "gate-3-partner-strategy" \
  --trajectory-type "gate_learning_→_next_gate_design" \
  --causal-strength 0.9 \
  --cross-session \
  --visibility shared
```

**What happens next:**
- Finding created in empirica DB
- Trajectory created: Gate 2 POSTFLIGHT → Gate 3 design specification
- SER 1 Monday snapshot (Sep 5) shows: "Gate 2 POSTFLIGHT created and incorporated"
- Gate 3 planning (Oct 1) starts INFORMED by this learning (not blind)

---

## The Protocol: 5 Steps

### Step 1: Gate Closes
Admiral gets decision results (e.g., Longview decision on Aug 1)

### Step 2: Admiral Analyzes
Within 24 hours, Admiral reflects on:
- What we predicted (from charter/gate design)
- What actually happened (results)
- Gap between predicted and measured
- What this reveals about the system
- How should the next gate's design change?

### Step 3: Admiral Logs POSTFLIGHT
Within 3 days of gate closing, Admiral runs:

```bash
empirica finding-log \
  --finding "[Your analysis of predicted vs measured vs gap vs learning vs action]" \
  --impact [0.7-0.95] \
  --enabled-by "gate-[N]-postflight" \
  --informs "gate-[N+1]-design" \
  --trajectory-type "gate_learning_→_next_gate_design" \
  --causal-strength 0.9 \
  --cross-session \
  --visibility shared
```

### Step 4: Trajectory Created
SMAG auto-creates trajectory:
- Source: Gate N POSTFLIGHT finding
- Target: Gate N+1 design
- Type: `gate_learning_→_next_gate_design`
- Causal strength: 0.9 (high confidence gate learning informs next gate)

### Step 5: Next Phase Informed
Phase N+1 planning begins with Gate N's POSTFLIGHT finding in context. Next gate starts INFORMED, not blind.

---

## Escalation Rule: 3-Day POSTFLIGHT Rule

**Trigger:** Gate closes on date X

**Deadline:** POSTFLIGHT finding must be created by date X + 3 days

**Escalation:** If no POSTFLIGHT created by X + 3 days, SER 1 escalates to Admiral

**Rationale:** Knowledge loses value over time. Capturing it within 3 days ensures freshness while impact is clear.

---

## Your Role: Admiral POSTFLIGHT Responsibilities

### Gate 1 (Aug 1): Longview Funding Decision

You will:
1. Receive Longview decision (Track A / B / C / rejection)
2. Analyze: "What does this decision mean for our timeline and priorities?"
3. Create POSTFLIGHT finding (by Aug 4) using template
4. Phase 1 planning is then shaped by Gate 1 learning

**Template ready:** GATE_1_POSTFLIGHT_TEMPLATE.md (just fill in the measured outcome on Aug 1)

### Gate 2 (Aug 31): Criterion 4 Evidence

You will:
1. Review empirica cross-validation results
2. Analyze: "Does this match our prediction? What variance is meaningful?"
3. Create POSTFLIGHT finding (by Sep 4)
4. Gate 3 partner strategy shaped by Gate 2 learning (e.g., prioritize model-diverse partners)

**Template ready:** GATE_2_POSTFLIGHT_TEMPLATE.md (similar structure)

### Gate 3 (Oct 1): Partner Confirmed

You will:
1. Review partner readiness and trial scope
2. Analyze: "Are we incorporating Gate 2's model-variance learning?"
3. Create POSTFLIGHT finding (by Oct 4)
4. Gate 4 trial protocol shaped by Gate 3 learning

### Gate 4 (Jan 1): Trial Success

You will:
1. Review deployment trial results
2. Analyze: "Did criterion 8 proof work? What did deployment teach us?"
3. Create POSTFLIGHT finding (by Jan 4)
4. Scaling strategy shaped by Gate 4 learning (next-round funding, expansion)

---

## Key Points to Remember

✅ **Create within 3 days** — Knowledge freshness matters. Escalation triggers at day 3.

✅ **Trajectory type is always `gate_learning_→_next_gate_design`** — This flags it as recursive learning closure.

✅ **Cross-session flag** — POSTFLIGHT findings persist across sessions (not ephemeral).

✅ **Visibility shared** — Other practices (HumanAIOS, mesh-support) can see and reference your learnings.

✅ **Causal strength typically 0.9** — Gate N evidence directly informs Gate N+1 design (high causal confidence).

✅ **Next gate uses your learning** — When Gate N+1 planning begins, your POSTFLIGHT is part of the context. No blind starts.

---

## Templates Ready to Use

### Gate 1 (Aug 1, Longview Decision)

File: `GATE_1_POSTFLIGHT_TEMPLATE.md`

Just fill in on Aug 1 when Longview decision arrives. Copy-paste the CLI command.

### Gate 2 (Aug 31, Criterion 4 Evidence)

File: `GATE_2_POSTFLIGHT_TEMPLATE.md`

Use same structure. Example: Model variance insight → shapes Gate 3 partner selection.

### Gate 3 & 4

Templates follow same pattern.

---

## Questions for Admiral

1. **Do you understand the protocol?** (Predicted vs Measured vs Gap vs Learning vs Action)
2. **Are you comfortable creating POSTFLIGHT within 3 days?** (Escalation triggers at day 3)
3. **Are you ready for Aug 1?** (Gate 1 template ready, just needs Longview outcome filled in)
4. **Any concerns about the escalation rule?** (3 days is firm, ensures freshness)

---

## Next Steps

✅ **Ready:** GATE_1_POSTFLIGHT_TEMPLATE.md (for Aug 1 use)

✅ **Ready:** Weekly rhythm templates (Monday snapshot includes "POSTFLIGHT pending?" check)

✅ **Ready:** Escalation automation (SER 1 will flag if POSTFLIGHT not created by day 3)

🟡 **Pending:** Longview decision (Aug 1) → triggers Gate 1 POSTFLIGHT

---

**Briefing complete. Admiral ready to proceed.**

**Next:** Confirm Admiral understands. Answer any questions. Approve protocol.

**Then:** Move to Week 1 Days 2-3 (engineering wiring).
