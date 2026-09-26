# SESSION_PRIORS Z2 Ratification Procedure

**Document ID:** PROC-2026-07-22-RATIF-SESSPRIOR  
**Status:** ✅ Z2 RATIFIED (2026-07-22, Admiral decision)  
**Author:** empirica-foundation-evaluator (Claude Code)  
**Date:** 2026-07-22  
**Ratified by:** Admiral (Carly R. Anderson)  
**Ratification decision ID:** f45c201c  
**Audience:** Admiral (Carly) and Z2 Authority Layer  

---

## Executive Summary

This procedure defines how candidate SESSION_PRIORS move from Z1 design (discovered in sessions, drafted in WGS posts) to Z2 authority (ratified and live in SESSION_PRIORS_V1_0.json).

**Core rule:** Candidate priors never self-promote. Z2 (Admiral) is the sole decision-maker for ratification, preventing structural conflicts of interest (a Claude cannot judge whether its own behavioral rules are valid).

---

## Part 1: Decision Authority

### 1.1 Who Decides

**Primary Authority:** Admiral (Carly R. Anderson)  
**Scope:** All SESSION_PRIORS ratification decisions for empirica-foundation practices.  
**Delegation:** Optional. Admiral may delegate ratification decisions to other Z2 holders (e.g., future governance reviewers) via explicit Authority Matrix update.

**Current Z2 Authority Structure (M2 Rank 1):**
```
Decision Type: SESSION_PRIORS Ratification (new authority)
Decision-Maker: Admiral (primary)
Approval Rule: Single decision-maker (Admiral alone)
Escalation: To Admiral if unclear or cross-practice impact
```

### 1.2 When Ratification Happens

**Trigger:** WGS post review window (within 24–48 hours after session close).

**Workflow timeline:**
```
Session close (T0)
  ↓
Silent-failures audit + candidate discovery (within session)
  ↓
WGS post draft + Candidate Priors section added (T+2h)
  ↓
Admiral reviews WGS post (T+24h to T+48h)
  ↓
Ratification decision recorded (T+48h)
  ↓
SESSION_PRIORS_V1_0.json updated (T+48h)
  ↓
Next session loads updated priors (T+72h or later)
```

---

## Part 2: Ratification Decision Criteria

### 2.1 What Makes a Candidate Worthy of Ratification?

**A candidate prior should be ratified if:**

1. **Repeatability:** The pattern has occurred ≥ 2 times in the past 3 sessions.
   - *Rationale:* One-off artifacts aren't worth internalizing. Repeats signal a structural behavior.
   - *Exception:* If pattern is severe enough to cause significant rework/escalation, ratify even on first occurrence (judgment call).

2. **Actionability:** The prior is specific enough that a Claude can *change behavior* in response.
   - *Good example:* "If asserting corpus state, run fresh query first."
   - *Bad example:* "Be more careful." (Too vague; no actionable guidance.)

3. **Leverage:** The pattern, if addressed, reduces CHECK gate fires or escalation probability.
   - *Metric:* "Fixing this prior would have saved X minutes of rework in past sessions" (rough estimate).
   - *Threshold:* If estimated savings > 10 minutes per occurrence, ratify.

4. **Non-interference:** The prior doesn't conflict with existing CLAUDE.md rules or Z3 phase logic.
   - *Check:* Does the prior advocate something that contradicts established governance? If yes, it needs escalation, not ratification.

5. **Clarity:** The rule is written clearly enough that future Claude instances (or humans) can apply it.
   - *Check:* Can a new Claude read the rule and say "I will do X" or "I will avoid Y"?

### 2.2 What Should NOT Be Ratified

**Reject (don't ratify) if:**

- **Insufficient evidence:** Pattern has fired ≤ 1 time in the past 3 sessions (and isn't severe).
- **Too vague:** Rule is philosophical or aspirational rather than behavioral (e.g., "be more humble").
- **System-level conflict:** Prior contradicts existing Z1/Z2 governance (e.g., "skip CHECK gates").
- **False positive risk:** Prior is likely to mis-fire in edge cases, adding noise rather than signal.
- **Duplicate:** Prior is essentially the same rule as an existing RATIFIED prior (merge instead of ratify separately).

**Decision:** REJECT or DEFER.
- **REJECT:** Pattern is noise; document why in comments so it's not re-proposed.
- **DEFER:** Pattern looks promising but needs more evidence; re-propose in next quarterly review.

---

## Part 3: Ratification Decision Workflow

### 3.1 Admiral's Review Checklist

When reviewing a WGS post with candidate priors:

**For each candidate prior:**

1. **Read the candidate rule** (from WGS post Candidate Priors section).
2. **Check prior history:**
   - Does REGISTERED.md have related incidents? (Link them in notes.)
   - Do prior WGS posts mention this pattern? (Cross-reference.)
3. **Estimate impact:**
   - If this pattern is addressed, how much rework/escalation would be saved?
   - Fire count in past sessions?
4. **Check for conflicts:**
   - Does this rule conflict with CLAUDE.md authority sections or Z3 phases?
   - Would ratifying this create a governance contradiction?
5. **Assess clarity:**
   - Can you restate the rule in one sentence? If not, it's too vague.
6. **Make decision:**
   - RATIFY / DEFER / REJECT.
   - Document rationale (2-3 sentences) and any modifications to the rule wording.

### 3.2 Decision Options

**RATIFY**
- Entry moves from Z1_CANDIDATE to RATIFIED in SESSION_PRIORS_V1_0.json.
- Fields filled: `status=RATIFIED`, `ratified_by=<admiral_name>`, `ratified_at=<timestamp>`.
- Entry is live immediately; next session loads it.

**DEFER**
- Entry stays Z1_CANDIDATE (not added to SESSION_PRIORS_V1_0.json).
- Comment added to WGS post: "Defer to next quarterly review; need more evidence."
- Candidate is re-evaluated in the next routine governance audit.

**REJECT**
- Entry is explicitly marked as rejected in WGS post.
- Not added to SESSION_PRIORS_V1_0.json.
- Rationale documented so the same pattern isn't re-proposed verbatim.
- Example comment: "This pattern conflicts with L2 heuristic advisory rule. We keep advisory checks soft, not binding."

---

## Part 4: Recording Ratification Decisions

### 4.1 WGS Post Amendment (Z2 Response)

After reviewing candidates, Admiral adds a "Z2 Ratification Decision" section to the WGS post:

```markdown
## Z2 Ratification Decision (Admiral Review)

Reviewed: 2026-07-22  
Reviewed by: carly  

### SP-001: Ungrounded Claims
**Decision:** RATIFY  
**Rationale:** Pattern has fired 3× in past 2 sessions. Clear rule. Leverage: ~15 min saved per fire. No conflicts.  
**Rule finalized:** "If asserting corpus state, run fresh query first. Query costs 50ms; rework costs 30 min."

### SP-002: Memory Leakage
**Decision:** DEFER  
**Rationale:** Only observed this session; too early to ratify. Will re-evaluate in next quarterly audit. Pattern might be idiosyncratic.

### SP-003: D-COMP Variant
**Decision:** REJECT  
**Rationale:** Duplicates SP-015 (existing ratified prior on calibration checks). Merge findings into SP-015 notes instead.

---
```

### 4.2 SESSION_PRIORS_V1_0.json Update

For each RATIFIED candidate:

1. Copy candidate prior structure from WGS post.
2. Add to `SESSION_PRIORS_V1_0.json` `priors` array.
3. Set:
   - `status: "RATIFIED"`
   - `ratified_by: "carly"` (Admiral name)
   - `ratified_at: "2026-07-22T14:30:00Z"` (decision timestamp)
4. Commit to git: `governance: ratify session prior SP-XXX: <label>`

**Example commit:**

```
commit abc123
Author: carly <carly@empirica.dev>
Date: Wed Jul 22 14:30:00 2026 +0000

    governance: ratify session prior SP-001 (ungrounded_claim_pattern)
    
    Pattern detected 3× in past 2 sessions. Rule: assert corpus state only with fresh queries.
    Estimated leverage: 15 min rework saved per occurrence.
    Z2 authority: Admiral (M2 Rank 1).
```

### 4.3 Decision Log Entry (Empirica artifact)

Admiral creates an empirica decision-log entry summarizing the ratification round:

```bash
empirica decision-log \
  --choice "SESSION_PRIORS ratification: 3 candidates (ratified: 1, deferred: 1, rejected: 1)" \
  --rationale "SP-001 ratified (strong evidence, high leverage). SP-002 deferred (insufficient fire count). SP-003 rejected (duplicate of SP-015)." \
  --decision-authority "Z2 / Admiral" \
  --timestamp "2026-07-22T14:30:00Z"
```

---

## Part 5: Communication and Transparency

### 5.1 Communicating Ratification to the Team

After ratification decisions are finalized:

**Via WGS post amendment (immediate):**
- Team sees which candidates were ratified/deferred/rejected and why.

**Via git commit (persistent):**
- Decision is recorded with rationale and timestamp.
- Future Claudes can trace why SESSION_PRIORS evolved.

**Via next-session advisory checklist (applied):**
- Ratified priors appear on the checklist automatically.
- Team experiences the rule in practice.

### 5.2 Quarterly Review Cadence

**Schedule:** End of each calendar quarter (Q1, Q2, Q3, Q4).

**At quarterly review:**
1. Scan all DEFERRED candidates from the quarter.
2. Check fire count and REGISTERED.md updates.
3. Re-decide: ratify if pattern has since fired 2+ times, reject if no new evidence.
4. Review staleness: any RATIFIED priors ready to SUPERSEDE?
5. Publish quarterly governance summary (brief note to team).

---

## Part 6: Edge Cases and Escalation

### 6.1 Conflicting Priors

**Scenario:** Candidate prior SP-004 says "Always commit after each task" but Z3 phase logic allows uncommitted work in certain cases.

**Resolution:**
- Flag as "Authority Conflict" in ratification review.
- Escalate to Admiral for clarification: does Z3 phase logic need updating, or does the prior need revision?
- Decision becomes an empirica decision-log entry (not just a prior).

### 6.2 Cross-Practice Patterns

**Scenario:** Candidate prior discovered in empirica-foundation-evaluator, but pattern also occurs in empirica-autonomy or empirica-outreach.

**Resolution:**
- Admiral tags it: "Cross-practice validation requested."
- Reaches out to other practice leads: "Have you seen this pattern?"
- If yes, ratify as shared prior (add to all practices' priors).
- If no, ratify as practice-specific.

### 6.3 Severe Pattern (One-Off but Critical)

**Scenario:** Pattern fires once but causes a critical incident (e.g., credential exposure, P3 failure).

**Resolution:**
- Ratify immediately (override the "≥2 fires" rule).
- Add to notes: "Critical severity (incident ID: xxx). Ratified on first fire."
- Expect high fire rate in next sessions as team internalizes rule.

---

## Part 7: Governance Integration

### 7.1 Authority Matrix Entry

**Governance Type:** SESSION_PRIORS Ratification  
**Decision-Maker:** Admiral  
**Approval Rule:** Single (Admiral alone; no secondary approval needed)  
**Evidence Required:** WGS post with candidate priors + fire history + REGISTERED.md cross-check  
**Approval Latency:** 24–48 hours (within WGS review window)  
**Escalation Trigger:** Cross-practice impact or authority conflict (escalate to Admiral for extended review)  

### 7.2 Zone Integration

**Z1 (Design):** Candidate priors drafted during session close audit.  
**Z2 (Authority):** Ratification decision made by Admiral within 48 hours.  
**Z3 (Execution):** Priors loaded and applied at session open and during work.

---

## Part 8: Delegation (Optional, Future)

### 8.1 Delegating Ratification Authority

If Admiral decides to distribute ratification decisions:

**Option A: Peer delegation**
- Delegate to empirica-mesh-support or another Z2 holder.
- Requires explicit update to AUTHORITY_MATRIX.yaml.
- Mesh-support (or delegate) assumes responsibility for ratification quality.

**Option B: Practice-specific delegation**
- Each practice (autonomy, outreach, humanaios) ratifies priors discovered in that practice.
- Admiral retains oversight (can override decisions, set standards).
- Requires clear delegation memo + training.

**No self-promotion rule remains:**
- Even delegated ratifiers must be external to the practice generating the prior.
- A Claude in autonomy cannot ratify its own discovered priors.

---

## Part 9: Documentation and Audit Trail

### 9.1 What Gets Logged

**Immutable record of every ratification decision:**
1. WGS post (primary source).
2. git commit message (secondary record).
3. empirica decision-log entry (tertiary record).
4. SESSION_PRIORS_V1_0.json entry (final state).

**Traceability:** Any future Claude can trace a RATIFIED prior back to its discovery session, Admiral's rationale, and related incidents.

### 9.2 Audit Queries

Example: "Why was SP-010 ratified?"
- Read SESSION_PRIORS_V1_0.json → see ratified_at, ratified_by.
- Read git log → see commit message with rationale.
- Read WGS post from that date → see full Z2 decision section.
- Read REGISTERED.md → see related incidents.

---

## Part 10: Success Criteria

How do you know the Z2 ratification procedure is working?

| Signal | Healthy | Unhealthy |
|--------|---------|-----------|
| **Ratification rate** | ~30–40% of candidates ratified per quarter | <10% (too conservative) or >70% (too permissive) |
| **Ratified prior fire rate** | Ratified priors fire ≥ 50% of the time (they're predictive) | <30% fire rate (ratification criteria too loose) |
| **Supersession rate** | ~10–20% of priors superseded per year | 0% (priors never get stale; staleness threshold too high) or >40% (threshold too low) |
| **Escalations due to priors** | <5% of escalations mention priors | High escalation rate mentioning priors (indicates priors are too strict or unclear) |
| **Candidate quality** | Candidates are specific and actionable | High rejection rate due to vagueness (discovery process needs refinement) |

---

## Part 11: Related Procedures

- **SESSION_PRIORS_SPECIFICATION_V1_0.md** — Full spec (data structure, lifecycle, application).
- **AUTHORITY_MATRIX.yaml** — Authority framework (ratification authority entry).
- **WGS_POSTFLIGHT_STANDARD.md** (hypothetical) — Session close standard (where candidates are discovered).

---

## Part 12: Example Ratification Round

**Scenario:** End of session 5 (2026-07-22). Three candidate priors in WGS post.

### Candidates:

**SP-001: Ungrounded Claims**
- Discovered: Session 3
- Fire count: 3 (Sessions 3, 4, 5)
- Rule: "If asserting corpus state, query fresh."
- Notes: Links to REGISTERED.md D-COMP-001, D-COMP-003.

**SP-002: Memory Leakage**
- Discovered: Session 5
- Fire count: 1 (Session 5)
- Rule: "[Candidate] Commit after each task to keep grounded calibration visible."
- Notes: First observed; no prior incidents.

**SP-003: Artifact Breadth**
- Discovered: Session 4
- Fire count: 0 (detected but not yet fired in sessions)
- Rule: "[Candidate] Log findings AND decisions AND dead-ends before POSTFLIGHT."
- Notes: Heuristic from code-audit ledger (L2 advisory rule); question is whether it belongs in SESSION_PRIORS.

### Admiral's Review (T+24h):

**SP-001:**
- Check REGISTERED.md: ✓ Three related incidents (D-COMP-001, D-COMP-003, D-COMP-005).
- Estimate impact: "Each ungrounded claim costs ~30 min of rework. 3 fires = ~90 min saved."
- Clarity check: ✓ "Query fresh before asserting corpus state" is clear and actionable.
- Conflicts: ✗ None.
- **Decision: RATIFY**

**SP-002:**
- Check REGISTERED.md: ✗ No related incidents.
- Fire count: Only 1 fire; insufficient evidence.
- Clarity check: ✓ Rule is clear.
- Conflicts: ✗ None.
- **Decision: DEFER** (comment: "Re-evaluate in Q3 if pattern recurs. Promising but needs validation.")

**SP-003:**
- Conflict check: ⚠ This is already in CLAUDE.md authority sections (L2 heuristic advisory).
- Question: Is SESSION_PRIORS the right place for it, or should it stay in CLAUDE.md?
- Fire count: 0 (hasn't actually fired yet).
- **Decision: REJECT** (comment: "L2 heuristic already covered in CLAUDE.md. Don't duplicate in SESSION_PRIORS. If this becomes a recurring *violation* (not following L2), then create a new prior for the violation, not the rule itself.")

### Admiral's WGS Amendment:

```markdown
## Z2 Ratification Decision (Admiral Review)

Reviewed: 2026-07-22  
Reviewed by: carly  

### SP-001: Ungrounded Claims
**Decision:** RATIFY  
**Evidence:** 3 fires in past 3 sessions; 3 related incidents in REGISTERED.md.  
**Rationale:** Clear rule, high leverage (~90 min rework saved if priors prevent future fires), no conflicts.  
**Live from:** Next session (2026-07-23 onward).

### SP-002: Memory Leakage
**Decision:** DEFER  
**Rationale:** Only 1 fire so far. Promising (commit discipline is critical), but needs 2nd fire in near future to validate repeatability. Re-evaluate in Q3.

### SP-003: Artifact Breadth
**Decision:** REJECT  
**Rationale:** L2 heuristic advisory rule already documented in CLAUDE.md authority sections. Priors should capture *violations* that emerge, not duplicate existing governance rules. If sessions start violating the L2 rule (not logging breadth), create a new prior for *that behavior*, not the rule itself.

---
```

### git Commit:

```
commit abc123
Author: carly <carly@empirica.dev>
Date: Wed Jul 22 14:30:00 2026 +0000

    governance: ratify session prior SP-001 (ungrounded_claim_pattern)
    
    3 fires in past 3 sessions. Related incidents: D-COMP-001, D-COMP-003, D-COMP-005.
    Rule: assert corpus state only with fresh queries.
    Estimated rework saved: ~30 min per fire.
    Z2 authority: Admiral (M2 Rank 1).
    Deferred SP-002; rejected SP-003 (duplicate of CLAUDE.md L2 rule).
```

### SESSION_PRIORS_V1_0.json Update:

```json
{
  "id": "SP-001",
  "discovered_in": "session-uuid-33333",
  "constraint_label": "ungrounded_claim_pattern",
  "rule": "If asserting corpus state, query fresh. Query costs 50ms; rework costs 30 min.",
  "scope_limit": "Advisory only — see anti-gaming note.",
  "status": "RATIFIED",
  "ratified_by": "carly",
  "ratified_at": "2026-07-22T14:30:00Z",
  "last_fired_in": "session-uuid-55555",
  "fire_count": 3,
  "fire_timestamps": [
    "2026-07-18T10:15:00Z",
    "2026-07-19T16:40:00Z",
    "2026-07-22T11:33:00Z"
  ],
  "supersession_status": "ACTIVE",
  "superseded_by": null,
  "superseded_at": null,
  "notes": "Extracted from REGISTERED.md incidents D-COMP-001, D-COMP-003, D-COMP-005. Fire count: 3 in 3 sessions. Ratified by Admiral 2026-07-22."
}
```

---

## Appendix: Admiral Ratification Checklist (Quick Reference)

Print this and use during WGS review:

```
SESSION_PRIORS Z2 RATIFICATION CHECKLIST
────────────────────────────────────────

For each candidate prior:

☐ Repeatability: Pattern fired ≥2× in past 3 sessions? (or critical severity?)
☐ Actionability: Can a Claude change behavior in response to this rule?
☐ Leverage: Estimated rework/escalation savings > 10 min per occurrence?
☐ Non-conflict: Does prior align with CLAUDE.md authority sections?
☐ Clarity: Can you restate the rule in one sentence?
☐ REGISTERED.md: Cross-check for related incidents?

Decision:
☐ RATIFY → add to SESSION_PRIORS_V1_0.json, set status=RATIFIED
☐ DEFER → leave as Z1_CANDIDATE, re-evaluate next quarter
☐ REJECT → document why, close the candidate

Notes: ___________________________________________________________________________
```

---

**End of SESSION_PRIORS_Z2_RATIFICATION_PROCEDURE.md**
