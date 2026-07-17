# Gate 1 POSTFLIGHT Template — Ready for Aug 1, 2026

**Status:** Template prepared (ready to fill on Aug 1)

**Admiral:** Carly R. Anderson

**Gate:** Gate 1 — Longview Funding Decision

**Timeline:** Aug 1 decision → Aug 1-4 POSTFLIGHT creation

---

## Instructions for Aug 1

1. Longview decision arrives (Aug 1)
2. Fill in the **MEASURED** section below with actual outcome
3. Copy-paste the **CLI Command** at the bottom and run it
4. That's it — the finding is logged and trajectory is created

---

## GATE 1 POSTFLIGHT — LONGVIEW FUNDING DECISION

### Predicted (Set in June 2026)

**What we expected:** 
"Longview will fund Track A ($420k, 12 months) for full criterion 8 execution by end of Q3 2026."

(See CHARTER_FINAL_BEHAVIORAL_CALIBRATION_OS.md for full context on Tracks A/B/C)

---

### Measured (Fill this in on Aug 1)

**What actually happened:**

[**TO FILL ON AUG 1 - Copy below, fill in, delete this line:**]

- Longview decision: [Track A / Track B / Track C / Rejected / Pending]
- Decision date: [actual date]
- Funding amount (if approved): [$$]
- Timeline (if approved): [months]
- Key conditions (if any): [describe]
- Expected notification/documentation: [date/format]

**Example filled version:**
```
- Longview decision: Track A (Approved)
- Decision date: Aug 1, 2026
- Funding amount: $420,000 (full track)
- Timeline: 12 months (Aug 1, 2026 - Aug 1, 2027)
- Key conditions: Monthly milestone reporting required
- Expected documentation: Grant agreement by Aug 15, fund transfer by Sep 1
```

Or (if conditional):
```
- Longview decision: Track A (Conditional approval)
- Funding amount: $420k subject to protocol review
- Timeline: Funding contingent on governance documentation completion
- Key condition: Submit governance docs (criterion 7) for final sign-off
- Remediation deadline: Aug 30 to unblock funding
```

Or (if Track B):
```
- Longview decision: Track B (Approved)
- Funding amount: $185k (minimum viable track)
- Timeline: 6 months (Aug 1 - Jan 31, 2027)
- Key conditions: Criterion 4 study deferred to subsequent funding
- Opportunity: Position for next-round funding round (submission by Nov 1)
```

---

### Gap Analysis

**What's the difference between predicted and measured?**

[**TO FILL ON AUG 1:**]

**If Track A approved as predicted:**
```
Gap: NONE — Longview funded full Track A as expected.
Implications: Full criterion 8 execution proceeds on timeline.
```

**If Track B instead:**
```
Gap: Funding is 56% of full track ($185k vs $420k).
Implications: Criteria 4-5 deferred. Criterion 8 trial deferred. 
Research-grade completion (criteria 1-3, 6-7) remains on track.
```

**If rejected or pending:**
```
Gap: Funding not confirmed. Charter contingent on alternative funding.
Implications: Track C (volunteer/fellowship path) activated. 
Seek alternative funders. Adjust timeline to match volunteer capacity.
```

---

### Learning

**What does this decision reveal about the funding landscape / market / priorities?**

[**TO FILL ON AUG 1:**]

Examples:

**If Track A approved:**
```
Learning: Oversight funders prioritize operational deployment proof (criterion 8) 
over research publication. Longview sees behavioral calibration OS as time-critical capability.
Market signal: Deployment-first positioning was correct.
```

**If Track B:**
```
Learning: Longview values the methodology (criteria 1-3, 6-7) but sees criterion 4-5 
(operational validation) as optional for this funding round. 
Market signal: Research-first funding cycle, operational funding follows.
```

**If rejected:**
```
Learning: Longview didn't fund. Possible reasons: timing, strategic misalignment, 
alternative solutions, or insufficient criterion-validity evidence pre-submission.
Market signal: Need stronger pre-submission evidence for next funder pitch.
```

---

### Action

**How does this shape Phase 1 planning? What changes?**

[**TO FILL ON AUG 1:**]

Examples:

**If Track A:**
```
Action: 
- Activate full Phase 1 (Aug-Sep): Hire research support, finalize criterion 4 study design, 
  identify deployment partners
- Resource allocation: Full budget ($420k) available
- Timeline: Criterion 8 trial by Jan 1, 2027 (on charter schedule)
- Priority: Criterion 4 predictive validity by Aug 31 (Gate 2)
```

**If Track B:**
```
Action:
- Activate Phase 1 (Aug-Sep): Hire PI personal support (fellowship), finalize criterion 4 
  study design (scaled scope)
- Resource constraint: Stretch budget over 6 months instead of 12
- Timeline: Criteria 1-3, 6-7 complete by Jan 31, 2027
- Defer: Criterion 4-5 and criterion 8 to next funding round
- Priority: Position for next-round funding (Nov 1 submission)
```

**If rejected:**
```
Action:
- Activate Track C (volunteer path): PI personal effort + fellowship support
- Resource: No dedicated budget; reliance on volunteer collaboration
- Timeline: Extend to match volunteer capacity (likely 18-24 months instead of 12)
- Priority: Seek alternative funders (next RFP cycle, foundation cold outreach)
- Interim: Publish criteria 1-3 (methodology + corpus) to strengthen next pitch
```

---

## CLI Command — Ready to Copy-Paste on Aug 1

### Full Command (Recommended)

```bash
empirica finding-log \
  --finding "Gate 1 POSTFLIGHT (Aug 1, 2026): Longview funding decision [OUTCOME]. [Your gap analysis]. [Your learning from the decision]. [Your action for Phase 1 planning]." \
  --impact 0.9 \
  --enabled-by "gate-1-postflight" \
  --informs "phase-1-planning" \
  --trajectory-type "gate_learning_→_next_gate_design" \
  --causal-strength 0.95 \
  --cross-session \
  --visibility shared
```

### Example (Track A Approved)

```bash
empirica finding-log \
  --finding "Gate 1 POSTFLIGHT (Aug 1, 2026): Longview approved Track A ($420k, 12mo). Full criterion 8 execution confirmed. Gap: none — decision matches prediction. Learning: Oversight funders prioritize deployment-first (operational readiness over publication). Action: Phase 1 activates full resource allocation; criterion 4 predictive validity by Aug 31 (Gate 2); deployment partners identified by Oct 1 (Gate 3)." \
  --impact 0.95 \
  --enabled-by "gate-1-postflight" \
  --informs "phase-1-planning" \
  --trajectory-type "gate_learning_→_next_gate_design" \
  --causal-strength 0.95 \
  --cross-session \
  --visibility shared
```

### Example (Track B Approved)

```bash
empirica finding-log \
  --finding "Gate 1 POSTFLIGHT (Aug 1, 2026): Longview approved Track B ($185k, 6mo). Criteria 1-3,6-7 on track; criteria 4-5,8 deferred to next funding. Gap: 56% funding vs predicted full track. Learning: Longview prioritizes research-grade (methodology+corpus) in this cycle, operational deployment (criterion 8) is next-cycle ask. Action: Phase 1 scales to 6-month horizon with fellowship support for PI; position for next-round funding submission (Nov 1)." \
  --impact 0.85 \
  --enabled-by "gate-1-postflight" \
  --informs "phase-1-planning" \
  --trajectory-type "gate_learning_→_next_gate_design" \
  --causal-strength 0.90 \
  --cross-session \
  --visibility shared
```

### Example (Rejected)

```bash
empirica finding-log \
  --finding "Gate 1 POSTFLIGHT (Aug 1, 2026): Longview rejected Track A/B. Gap: funding not approved. Learning: Oversight funders may require stronger criterion-validity evidence pre-submission. Market signal: publication-first approach needed before next pitch. Action: Activate Track C (volunteer path); publish criteria 1-3 to strengthen portfolio; identify alternative funders for next RFP cycle (Q4 2026)." \
  --impact 0.80 \
  --enabled-by "gate-1-postflight" \
  --informs "phase-1-planning" \
  --trajectory-type "gate_learning_→_next_gate_design" \
  --causal-strength 0.85 \
  --cross-session \
  --visibility shared
```

---

## What Happens After You Run the CLI Command

1. ✅ Finding created in empirica DB
2. ✅ Trajectory created: `Gate 1 POSTFLIGHT → Phase 1 design`
3. ✅ SMAG registers trajectory type: `gate_learning_→_next_gate_design`
4. ✅ SER 1 sees the finding on Monday snapshot (Aug 5)
5. ✅ Phase 1 planning begins INFORMED by Gate 1 learning (not blind)
6. ✅ Gate 2 (Aug 31) will later be informed by Gate 1's discovery

---

## Timeline

| Date | Event |
|---|---|
| **Aug 1** | Longview decision arrives |
| **Aug 1-4** | [3-day window] Create Gate 1 POSTFLIGHT (fill template + run CLI) |
| **Aug 5** | SER 1 Monday snapshot shows POSTFLIGHT status |
| **Aug 15** | Phase 1 planning complete (informed by Gate 1 learning) |
| **Aug 31** | Gate 2 closes (Criterion 4 evidence) → Gate 2 POSTFLIGHT created |

---

## Reminder: Why This Matters

Gate 1's POSTFLIGHT finding ensures that:
- Longview's decision is captured (not forgotten)
- Its implications for Phase 1 are explicit (not assumed)
- Phase 1 planning is INFORMED by this learning (not blind)
- Phase 2 (and Gate 2) can build on Phase 1's grounded discoveries

**No knowledge is left on the table.**

---

## Ready?

On Aug 1:
1. ✅ Longview decision arrives
2. ✅ Fill in **Measured** section (above)
3. ✅ Write **Gap Analysis** (above)
4. ✅ Write **Learning** (above)
5. ✅ Write **Action** (above)
6. ✅ Copy-paste the CLI Command and run it

That's it. The POSTFLIGHT is logged. Trajectory created. Phase 1 informed.

---

**Template Status:** ✅ READY FOR AUG 1

**Location:** This file (GATE_1_POSTFLIGHT_TEMPLATE.md)

**Next:** Gate 2 template (similar structure, ready Aug 31)
