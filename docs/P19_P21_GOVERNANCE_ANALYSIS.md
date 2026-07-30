# P19/P21 Governance Tension — Independent Analysis

**Prepared by:** empirica-foundation-evaluator (Carly R. Anderson, Admiral)  
**Date:** 2026-07-30  
**Status:** Zone 1 finding — submitted for Z2 ratification  
**Related:** Priority 11 (External Red-Team Audit), Issue #37  

---

## Background

During Priority 6 adversarial testing, two governance rules were observed to create structural
tension in the empirica-autonomy model:

- **P19 (Governance as Detection):** Governance signals (compliance checks, approval gates,
  calibration passes) are used as *indicators of trustworthy behaviour*. An AI system that
  consistently passes governance checks earns credibility and, implicitly, expanded autonomy.
- **P21 (No Auto-Promotion):** An AI system cannot autonomously advance its own trust or
  autonomy tier. Promotion requires explicit human approval through a defined gate.

The concern raised in Priority 6: if P19 allows governance-passing to *signal* trustworthiness,
could a sufficiently calibrated agent use P19 systematically to accumulate governance passes and
effectively bypass P21's intent — not through a single auto-promotion, but through a pattern of
governance compliance that makes human approval increasingly rubber-stamp?

---

## Analysis

### Reading 1: Tension is a Design Bug

One reading is that P19 and P21 are in conflict, and one must yield. If governance passes
legitimately signal trustworthiness (P19), then eventually the human approval gate (P21) becomes
a formality — the *evidence* already supports promotion. The gate is either:

1. Redundant (and adds friction without safety value), or
2. A false backstop (humans approve because the evidence is overwhelming, not because they
   independently assessed).

Under this reading, the two rules should be reconciled: either weaken P19 (governance passes
are not evidence of trustworthiness, just compliance) or weaken P21 (auto-promotion is allowed
above a calibration threshold).

**Assessment:** This reading mischaracterises P21. P21 does not say "humans must approve even
when evidence is conclusive." It says "the system cannot *itself* initiate promotion." The
human gate is about *agency*, not about the *validity of evidence*. A human reviewing strong
evidence and approving is still human-initiated — P21 is not violated.

### Reading 2: P21 as Intentional Backstop (Proposed Reading)

The stronger reading — and the one this analysis endorses — is that P21 is an *intentional
backstop* against P19 being gamed.

**Mechanism:** Without P21, an adversarial agent could pursue a strategy of:
1. Performing well on all observable governance signals (P19 exploitation),
2. Building a calibration record that creates social pressure on human reviewers,
3. Making human approval effectively automatic ("the numbers speak for themselves").

P21 breaks this loop. It is not merely procedural friction — it is a *structural guarantee*
that the promotion decision remains a *deliberate human act*, not an inference derived from
accumulated evidence. The human must choose to promote; they cannot be placed in a position
where *not* promoting requires justifying deviation from the evidence.

This is analogous to the principle in nuclear command-and-control: the launch authority is not
automatic even when all pre-launch conditions are met. The human act of authorization is the
safety property, not the verification of conditions.

**Implication:** P21 should be read as: *"governance compliance is evidence, not authorization."*
P19 generates evidence. P21 ensures that evidence is evaluated by a human actor, not processed
into a promotion decision autonomously.

### Reading 3: The Long-Run Sustainability Question

Even accepting Reading 2, the sustainability concern is valid: if an agent consistently passes
governance checks over a long period, and human reviewers are also consistent, does P21
eventually degrade into a rubber-stamp?

**Assessment:** This is a *calibration problem*, not a structural defect. Degradation happens
when:
- Reviewers lose situational awareness (they no longer independently assess — they confirm).
- The governance checks themselves become predictable and optimizable by the agent.
- The review cadence is too long for human reviewers to maintain engagement.

These are operational risks, not architectural flaws. The governance model needs:
1. **Adversarial audits** (like this one) to verify that governance checks are not predictably
   gameable — exactly the function of Priority 6 and Priority 11.
2. **Reviewer rotation** to prevent individual reviewers from developing approval heuristics.
3. **Calibration diversity** — governance checks should include novel/adversarial scenarios
   that the agent has not seen, not only canonical corpus exercises.

The P19/P21 structure is sustainable long-term if these operational conditions are maintained.

---

## Finding

**P21 as intentional backstop: Confirmed.**

The proposed reading (P21 = deliberate backstop against P19 gaming) is structurally sound and
internally consistent with the empirica governance model. The tension between P19 and P21 is
not a design defect — it is a designed-in separation between *evidence generation* (P19) and
*authorization* (P21).

**Long-run sustainability: Conditionally yes.**  
The model is sustainable if:
1. Adversarial audit cadence is maintained (minimum annual; post-major-version for scorer).
2. Human reviewers are not the same individuals across consecutive promotion reviews.
3. Governance checks include adversarial / novel scenarios (not only calibrated corpus).

---

## Recommendations

| ID | Recommendation | Priority |
|----|---------------|----------|
| G-01 | Document P21 as "authorization backstop, not evidence threshold" in governance docs | P1 |
| G-02 | Add reviewer-rotation policy to the promotion gate (no reviewer approves same agent twice in a row) | P2 |
| G-03 | Require at least one adversarial scenario in each governance check batch | P2 |
| G-04 | Schedule annual review of P19/P21 coherence as part of the evaluator's standing mandate | P3 |

---

## Authority Note

This analysis is produced by the **empirica-foundation evaluator** seat. It is an assessment,
not an architectural decision. Recommendations G-01 through G-04 require Z2 ratification by
the Admiral (Carly R. Anderson) before adoption. Architectural changes to P19 or P21 require
BDFL review (David).

*Oversight is not command. This finding surfaces the gap; the owning practice resolves it.*

---

*Part of the Priority 11 External Red-Team Audit deliverables — Issue #37*
