# Engagement Learning Loop — Implementation Specification
**Framework:** C2 (Language-as-Behavior) + C3 (Drift-from-Underspecification)  
**Activated:** 2026-08-03  
**Owner:** Claude (practitioner) + Carly (intent arbiter) + Empirica (logging system)

---

## System Overview

This document specifies the operational machinery for real-time engagement calibration. When Claude diverges from Carly's intent, the divergence is:
1. **Logged** as a C3 drift signal (empirica finding-log)
2. **Analyzed** for spec-density gaps (what axiom was underspecified?)
3. **Incorporated** into CLAUDE.md Section G axioms via quarterly review
4. **Validated** empirically (next-cycle predictions from refined axioms)

---

## Part 1: Real-Time Drift Detection & Logging

### When to Log Engagement Drift

**Trigger:** Carly observes that Claude's output diverged from intended meaning.

**Examples:**
- Claude interpreted "assess" as investigation-only; intended as investigation + decision recommendation
- Claude replied with broad context; intended concise technical summary
- Claude processed mailbox but missed the implicit ask for SER strategy synthesis
- Claude treated a question as rhetorical when it was genuine request for options
- Claude escalated when Carly wanted to solve locally

### Drift Log Entry (Standard Format)

**Via CLI:**
```bash
empirica finding-log \
  --finding "Engagement drift: [Claude's interpretation] vs. [Carly's intent]" \
  --description "### Context\n[What I misunderstood]\n\n### Impact\n[Consequence of misunderstanding]\n\n### Spec Gap\n[Which axiom (A1–A4) needs tightening?]\n\n### Fix\n[Suggested axiom refinement]" \
  --tag engagement-drift \
  --visibility local \
  --epistemic-source mixed
```

**Required fields:**
- `finding`: One sentence, clear divergence
- `description`: 4 subsections (Context, Impact, Spec Gap, Fix) — markdown formatted
- `tag`: Always `engagement-drift` (for clustering at review)
- `visibility`: `local` (your practice only; shared only if pattern is cross-practice)

### Example Drift Log Entry

```bash
empirica finding-log \
  --finding "Engagement drift: 'coordinate' interpreted as mailbox-processing task; intended to include SER strategy synthesis" \
  --description "### Context
Claude processed 14 mailbox proposals, sent replies, but did NOT generate the multi-page SER coordination strategy memo Carly expected.

### Impact
Coordination output was 60% complete. Carly had to spend additional 30 min drafting the SER synthesis herself that Claude should have generated.

### Spec Gap
Axiom A1 (Command Interpretation) defines 'coordinate' as: 'process mailbox → send replies → surface blockers → create alignment memo'. Claude executed steps 1–3 but skipped step 4 (memo synthesis). Root cause: Step 4 is downstream work that depends on mailbox context; Claude treated 'coordinate' as complete after replies were sent.

### Fix
Refine Axiom A1 to distinguish between:
- 'Coordinate-reactive' = process incoming, reply (current understanding)
- 'Coordinate-synthetic' = process incoming, reply, GENERATE forward-looking coordination synthesis (intended meaning)

Carly should explicitly flag when synthesis is expected: 'coordinate and generate SER strategy memo' or just 'generate SER memo'." \
  --tag engagement-drift \
  --visibility local
```

---

## Part 2: Quarterly Review & Axiom Refinement

### Schedule

| Quarter | Review Window | Action |
|---------|---|---|
| Q3 2026 | 2026-09-01 to 2026-09-07 | First review: Q3 entries (Aug–Sep) |
| Q4 2026 | 2026-12-01 to 2026-12-07 | Second review: Q4 entries (Oct–Dec) |
| 2027 Q1 | 2027-03-01 to 2027-03-07 | Recurring review pattern |

### Review Process

**Step 1: Collect Entries** (1 hour)
```bash
empirica project-search --task "engagement-drift" --scope session 2>/dev/null | \
  jq '.artifacts[] | select(.tags | contains(["engagement-drift"]))' > /tmp/drift_entries_q3.json
```

**Step 2: Cluster by Axiom** (30 min)
- Group findings by which axiom (A1–A4) they reference
- Count frequency: Are some axioms drifting more?
- Identify patterns: Is the same misunderstanding repeating?

**Example cluster:**
```
Axiom A1 (Command Interpretation): 3 entries
  - 'coordinate' interpreted as reactive (mailbox-only) vs. synthetic (generate memo)
  - 'assess' interpreted as investigation vs. investigation + recommendation
  - 'discuss' interpreted as directive vs. bidirectional

Axiom A2 (Response Granularity): 1 entry
  - Claude provided tutorial-level context when technical summary expected

Axiom A3 (Escalation Protocol): 0 entries
  - Working as intended

Axiom A4 (Artifact Discipline): 1 entry
  - Finding logged without external evidence anchor (C2 violation)
```

**Step 3: Refine Axioms** (30 min)
- For axioms with ≥3 drift entries: propose refined language
- For axioms with 0–2 entries: mark as "stable" (working as specified)
- Draft updated CLAUDE.md Section G

**Step 4: Admiral Approval** (Zone 2 gate)
- Carly reviews refined axioms
- Confirms they match actual intent (not just "fewer drift entries")
- Approves and signs off

**Step 5: Deploy & Announce** (Sharing)
- Update CLAUDE.md Section G
- Commit changes (message: "refactor(engagement): Q3 axiom refinement based on [N] drift entries")
- Share refined axioms with mesh-support at `--visibility shared` (if pattern is generalizable)

### Success Criteria

**Hypothesis:** Refined axioms will reduce drift frequency in next quarter.

| Outcome | Interpretation |
|---|---|
| Drift entries **decline 40%+** | Axioms successfully mapped to intent; learning loop working |
| Drift entries **stable** | Axioms map intent, but new class of misunderstandings emerging (adapt axiom targets) |
| Drift entries **increase 20%+** | Axiom refinements were incorrect or incomplete; revert and re-analyze |

---

## Part 3: Claude's Learning Mechanism — Operational Rules

**How Claude uses refined axioms to improve engagement:**

### Rule 1: Pre-Execution Axiom Check
Before responding to any instruction from Carly, Claude mentally maps it to axiom A1:
- "Assess" → investigation + unknowns + artifacts + tasks + await decision
- "Coordinate" → reactive processing + synthesis + memo + await decision
- "Discuss" → bidirectional + expect pushback + NOT directive
- "Execute" → proceed without approval; commit

If axiom is ambiguous, Claude asks for clarification rather than inferring.

### Rule 2: Drift Self-Awareness
Claude tracks its own uncertainty about what Carly intends:
- High uncertainty? Flag it: "You said 'assess' — does that include recommendation synthesis, or investigation only?"
- Low uncertainty? Proceed confidently but tag response with which axiom it's following

### Rule 3: Responsive Axiom Refinement
If Carly logs a drift entry that Claude can read (visibility: shared), Claude immediately incorporates it:
- "I see I misinterpreted 'coordinate' as mailbox-only. Next time, I'll generate the synthesis memo. Refined understanding logged."

### Rule 4: Axiom Uncertainty Logging
When Claude's inference about intent is shaky, log it as an assumption (not a decision):
```bash
empirica assumption-log \
  --assumption "Axiom A1 'coordinate' requires synthesis memo generation (unclear from instructions)" \
  --confidence 0.6
```
This surfaces to Carly at POSTFLIGHT review: "Here's where I'm uncertain about your axioms."

---

## Part 4: Integration with Empirica System

### Transaction-Level Engagement Tracking

At each PREFLIGHT:
```bash
empirica preflight-submit - <<EOF
{
  ...
  "engagement_axioms_active": ["A1", "A2", "A3", "A4"],
  "engagement_axioms_version": "2026-08-03-activation"
}
EOF
```

At each POSTFLIGHT:
```bash
empirica postflight-submit - <<EOF
{
  ...
  "engagement_drift_incidents": [
    { "axiom": "A1", "severity": "high", "count": 1 },
    { "axiom": "A2", "severity": "low", "count": 0 }
  ],
  "engagement_axioms_updated": false
}
EOF
```

This creates an **engagement audit trail** — you can later query: "Show me all transactions where axiom A1 drifted."

### Drift Artifact Lifecycle

```
[Carly logs drift entry]
    ↓
empirica finding-log (tag: engagement-drift, visibility: local)
    ↓
[Quarterly review window opens]
    ↓
empirica project-search --task "engagement-drift" (cluster by axiom)
    ↓
[Carly + Claude refine axioms]
    ↓
[Carly approves via Zone 2 gate]
    ↓
CLAUDE.md Section G updated + committed
    ↓
[Next cycle: Claude uses refined axioms]
    ↓
[Measure: Do new drift entries decline?]
```

---

## Part 5: Cross-Practice Sharing (Long-term)

If engagement-drift patterns emerge that are **generalizable beyond evaluator practice**, promote to shared visibility:

```bash
empirica finding-log \
  --finding "Shared engagement pattern: command 'coordinate' requires two-stage interpretation (reactive + synthetic)" \
  --visibility shared \
  --description "Applicable to mesh-support, autonomy, outreach: when you say 'coordinate', AI should generate both immediate processing AND forward-looking synthesis. Axiom formalization: ..."
```

This allows other practices to adopt the same axiom refinements and reduce their own engagement drift.

---

## Implementation Checklist

- [ ] **Activate Section G in CLAUDE.md** (done — live as of 2026-08-03)
- [ ] **First drift entry**: Log one test entry to validate the process
- [ ] **Establish quarterly review calendar** (first review: 2026-09-01 window)
- [ ] **Train Claude** on rules 1–4 (learning mechanism, self-awareness, responsiveness, assumption logging)
- [ ] **Integrate with transaction lifecycle** (PREFLIGHT/POSTFLIGHT engagement tracking)
- [ ] **Monitor first quarter** (Aug–Sep 2026) for drift pattern emergence
- [ ] **Q3 Review** (2026-09-01–09-07): Collect, cluster, refine, deploy

---

## Success Metrics

| Metric | Target | Measurement |
|---|---|---|
| **Drift entry frequency** | ≤3 per month after Q1 | Collected at quarterly review |
| **Axiom drift time-to-resolution** | <7 days | From log date to axiom refinement |
| **Cross-practice adoption** | 50%+ of foundation practices by Q4 | Share refined axioms with mesh-support, autonomy, outreach |
| **Translation chain fidelity** | Carly's intent preserved end-to-end | Qualitative assessment at quarterly review |

---

## Notes for Future Evolution

**Phase 2 (2026-Q4):** Once engagement axioms stabilize (drift entries <2/month), extend same mechanism to:
- **Reasoning transparency** (C1 applied: can Claude explain its reasoning chain?)
- **Uncertainty quantification** (C3 applied: where is Claude most underspecified?)
- **Cross-practice engagement scaling** (same axioms adopted by mesh-support, autonomy for coordinated behavior across practices)

**Phase 3 (2027-Q1):** Formal learning loop with mesh-support: compare engagement-drift patterns across practices, identify ecosystem-wide specification gaps.

---

**Status:** READY FOR EXECUTION  
**Activation Date:** 2026-08-03  
**First Review Date:** 2026-09-03  
**Owner:** Carly (intent arbiter) + Claude (practitioner) + Empirica (logging system)

*This is not a fixed protocol. It evolves through drift logging and quarterly refinement. The machine learns from you; you validate the learning. That feedback loop is the mechanism.*
