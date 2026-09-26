# SESSION_PRIORS Specification v1.0

**Document ID:** SPEC-2026-07-22-SESSPRIOR-V1  
**Status:** ✅ Z2 RATIFIED (2026-07-22, Admiral decision)  
**Author:** empirica-foundation-evaluator (Claude Code)  
**Date:** 2026-07-22  
**Ratified by:** Admiral (Carly R. Anderson)  
**Ratification decision ID:** f45c201c  
**Scope:** Internal governance tooling (session-level learning system)  

---

## Executive Summary

SESSION_PRIORS is a computable registry of behavioral patterns and remedial rules discovered during empirica sessions. Unlike downstream governance artifacts (CHECK gates, escalation protocols, audit trails), SESSION_PRIORS operates *upstream*: it injects learned constraints into session initialization, making problematic behaviors less likely before execution.

**Core insight:** Laws (or CHECK gates) catch violations *after* they occur. SESSION_PRIORS prevents violations by restructuring the initial conditions—information, incentives, and affordances—so bad outcomes become irrational or difficult before the session begins.

**Root-cause lever:** Session amnesia (priors exist in WGS posts but aren't mechanically consumed at session open) → SESSION_PRIORS solves by making priors discoverable, ratifiable, and automatically injected.

---

## Part 1: Purpose and Rationale

### 1.1 The Problem (Downstream Patch Status)

**Symptom:** Patterns repeat across sessions.
- Example: Claim about corpus state without fresh Supabase query → discovered in one session → logged in WGS post → next session, same pattern occurs again.

**Current mechanism (downstream):**
- CHECK gate fires: "ungrounded_claim" flagged.
- Costs: rework, escalation, Admiral time.
- But: The pattern is caught *after* it's already in motion.

**Why this is brittle:**
- Adding more CHECK gates increases friction and per-session overhead.
- Each new pattern requires a new gate—N patterns → N gates (unbounded growth).
- Rules are hardcoded in CLAUDE.md; updates require commits and deployment.
- Lessons from WGS posts are visible but not *actionable* at session start.

### 1.2 The Root-Cause Solution (Upstream Architecture)

**Mechanism:** Inject prior constraints at session initialization, before Phase 1 begins.

**Why this is high-leverage:**
- Session open is the highest-leverage moment: vectors reset, context is blank, prior state *should* populate before work starts.
- Shifting from runtime gates (CHECK) to initialization (prior injection) reduces execution-time friction.
- Priors are data (JSON), not code—they can evolve without redeployment.
- Feedback loop is faster: session close → candidate prior → WGS post → Z2 ratification → next session uses it.

**Architectural change:**
```
OLD: Session open → [No prior injection] → Execute work → Detect drift (CHECK) → Log lesson
NEW: Session open → [Load SESSION_PRIORS] → Execute work → Check against priors (advisory) → Update priors (Z2)
```

### 1.3 Integration with Existing Governance Layers

**Z1 (Chat/Collab):** Design and discussion of new priors (candidate discovery).  
**Z2 (Authority Decision):** Ratification of candidates into live priors (Z2 gate).  
**Z3 (Terminal Execution):** Application of priors at session open; advisory checks during work.

SESSION_PRIORS is *not* a new decision layer—it's infrastructure for Z2 to manage learned rules operationally.

---

## Part 2: Data Structure and Lifecycle

### 2.1 JSON Schema

**File:** `SESSION_PRIORS_V1_0.json`  
**Structure:** Append-only array of prior objects.

```json
{
  "version": "1.0",
  "last_updated": "2026-07-22T19:45:00Z",
  "priors": [
    {
      "id": "SP-001",
      "discovered_in": "session-uuid-12345",
      "constraint_label": "ungrounded_claim_pattern",
      "rule": "If a claim about corpus state is made without a fresh Supabase query in the same session, flag before Phase 3 declaration. Query costs ~50ms; cost of rework is 30+ minutes.",
      "scope_limit": "Advisory only — see anti-gaming note below.",
      "status": "RATIFIED",
      "ratified_by": "carly",
      "ratified_at": "2026-07-19T14:22:00Z",
      "last_fired_in": "session-uuid-67890",
      "fire_count": 3,
      "fire_timestamps": [
        "2026-07-18T10:15:00Z",
        "2026-07-19T16:40:00Z",
        "2026-07-22T11:33:00Z"
      ],
      "supersession_status": "ACTIVE",
      "superseded_by": null,
      "superseded_at": null,
      "notes": "Pattern emerged in Q3 audits. Remedy: cheap query beats expensive rework."
    },
    {
      "id": "SP-002",
      "discovered_in": "session-uuid-54321",
      "constraint_label": "memory_leakage_candidate",
      "rule": "[Candidate rule — pending Z2 review] Breadcrumbs not written before POSTFLIGHT → uncommitted work invisible to grounded calibration. Discipline: always commit after each task.",
      "scope_limit": "Advisory only.",
      "status": "Z1_CANDIDATE",
      "ratified_by": null,
      "ratified_at": null,
      "last_fired_in": null,
      "fire_count": 0,
      "fire_timestamps": [],
      "supersession_status": "ACTIVE",
      "superseded_by": null,
      "superseded_at": null,
      "notes": "Discovered in M2 Rank 1 audit. Z2 to decide if this pattern is repeatable or one-off."
    },
    {
      "id": "SP-003",
      "discovered_in": "session-uuid-11111",
      "constraint_label": "d_comp_family_incident",
      "rule": "D-COMP pattern: Claim divergence between self-assessed and grounded vectors. When vectors rise but artifact breadth/source coverage stay flat, audit sources and edge density before POSTFLIGHT.",
      "scope_limit": "Advisory only.",
      "status": "SUPERSEDED",
      "ratified_by": "carly",
      "ratified_at": "2026-06-15T09:00:00Z",
      "last_fired_in": "session-uuid-44444",
      "fire_count": 2,
      "fire_timestamps": [
        "2026-07-10T14:20:00Z",
        "2026-07-15T18:50:00Z"
      ],
      "supersession_status": "SUPERSEDED",
      "superseded_by": "SP-005",
      "superseded_at": "2026-07-20T12:00:00Z",
      "notes": "Pattern stopped firing after M2 artifact-logging discipline was implemented. Superseded by SP-005 (generic calibration check)."
    }
  ]
}
```

### 2.2 Field Definitions

| Field | Type | Meaning | Required | Mutable |
|-------|------|---------|----------|---------|
| `id` | string | Unique identifier (e.g., `SP-001`) | ✓ | ✗ |
| `discovered_in` | UUID | Session where pattern was first observed | ✓ | ✗ |
| `constraint_label` | string | Human-readable short label (kebab-case) | ✓ | ✗ |
| `rule` | string | The actual rule/heuristic (markdown allowed) | ✓ | ✓ (Z2 can refine) |
| `scope_limit` | string | Boundary (e.g., "Advisory only") | ✓ | ✗ |
| `status` | enum | `Z1_CANDIDATE`, `RATIFIED`, `SUPERSEDED` | ✓ | ✓ (via Z2) |
| `ratified_by` | string | Username (Z2 decision-maker) | conditional | ✗ |
| `ratified_at` | ISO8601 | Timestamp of Z2 decision | conditional | ✗ |
| `last_fired_in` | UUID | Most recent session where prior was applied | ✓ | ✓ (auto-update) |
| `fire_count` | int | Cumulative times pattern recurred | ✓ | ✓ (auto-increment) |
| `fire_timestamps` | array | Chronological record of firings | ✓ | ✓ (auto-append) |
| `supersession_status` | enum | `ACTIVE` or `SUPERSEDED` | ✓ | ✓ (auto-update) |
| `superseded_by` | string | ID of the prior that replaced this one | conditional | ✗ |
| `superseded_at` | ISO8601 | When this prior was superseded | conditional | ✗ |
| `notes` | string | Rationale, context, related findings | ✓ | ✓ |

### 2.3 Lifecycle States

```
Z1_CANDIDATE
    ↓
    [Z2 Ratification Gate]
    ↓
RATIFIED (active, applied at session open)
    ↓
    [Pattern stops firing for STALE_THRESHOLD sessions]
    ↓
SUPERSEDED (keep in log, don't apply)
```

**Transitions:**
- **Z1_CANDIDATE → RATIFIED:** Z2 decision (Admiral or delegated). Entry goes live; next session loads it.
- **RATIFIED → SUPERSEDED:** Automatic after N sessions with no fires (see §2.5).
- **No delete:** All entries are append-only. Superseded priors remain in JSON for audit trail.

---

## Part 3: Discovery and Candidacy (Z1)

### 3.1 Where Candidates Originate

**Session close, after silent-failures audit, before WGS draft:**

A small analysis pass (analogous to `append_new_lesson` in code audit tools) scans the session transcript for recurring patterns:

1. **Pattern detection:**
   - Does the transcript contain a claim about corpus state without a fresh query? → Candidate: "ungrounded_claim_pattern"
   - Did the session exhibit divergence between self-assessed and grounded vectors? → Candidate: "calibration_divergence_pattern"
   - Did the session repeat a pattern already flagged in prior WGS posts or REGISTERED.md? → Candidate: "repeated_pattern"

2. **Cross-check:**
   - Compare detected patterns against `REGISTERED.md` (past incidents) and prior WGS archives.
   - If pattern is novel, flag it as novel. If it's a repeat, note the repeat count.

3. **Candidate generation:**
   - Draft a candidate prior object (status: `Z1_CANDIDATE`).
   - Do *not* write directly to `SESSION_PRIORS_V1_0.json`.
   - Instead, add to WGS post as a tagged "Candidate Session Priors" section.

### 3.2 Candidate Format in WGS Post

```markdown
## Candidate Session Priors

These patterns emerged this session. They are not yet live—Z2 must ratify them into SESSION_PRIORS before they apply to future sessions.

### Candidate SP-XXX: ungrounded_claim_pattern

**Discovered in:** This session  
**Pattern:** Claim about corpus state made without fresh Supabase query.  
**Rule:** "If a claim about corpus state is made without a fresh query in the same session, flag before Phase 3 declaration."  
**Confidence:** Medium (pattern emerged 1× this session; 2× in prior sessions)  
**Z2 Decision Needed:** Is this a repeatable pattern worth adding to active priors?  
**Evidence:**
- [Link to transcript excerpt]
- [Link to REGISTERED.md entry]

---
```

### 3.3 Anti-Gaming Note (Why Z1 Discovery, Not Z3 Self-Promotion)

Claude never auto-ratifies a candidate prior. Reason: Behavioral patterns are *claims about the system*, and the system being evaluated cannot self-assess whether its own claims are valid without external verification (structural humility).

**Risk:** A Claude could discover a pattern, draft a rule that makes its own behavior look better, and mark it RATIFIED—defeating the whole purpose.

**Safeguard:** Z2 (human, Admiral) decides whether a candidate is:
- A genuine repeatable pattern worth internalizing, or
- A one-off artifact of this session that doesn't generalize.

---

## Part 4: Z2 Ratification Procedure

See **SESSION_PRIORS_Z2_RATIFICATION_PROCEDURE.md** for full operational details.

**Abbreviated summary:**
1. Admiral receives WGS post with candidate priors.
2. Admiral reviews candidates against REGISTERED.md and prior WGS posts.
3. Admiral decides for each candidate: **RATIFY** (add to live JSON) or **REJECT** (comment, defer, or discard).
4. Upon RATIFY decision, candidate entry is added to `SESSION_PRIORS_V1_0.json` with `status: RATIFIED` and `ratified_by`, `ratified_at` filled.
5. **Next session:** Prior is loaded and applied.

---

## Part 5: Application at Session Initialization

### 5.1 Session Open Bootstrap

At session start, after CLAUDE.md and breadcrumbs are loaded:

```
1. Load SESSION_PRIORS_V1_0.json
2. Filter: keep only entries where status == "RATIFIED"
3. For each RATIFIED prior:
   a. Add to pre-flight advisory checklist
   b. Display before Phase 1 begins
4. Continue session initialization (vectors, context, goals)
```

### 5.2 Advisory Checklist Display

**Rendered to the user/Claude at session start:**

```
─────────────────────────────────────────────────────────
SESSION PRIORS (Learned Rules from Prior Sessions)
─────────────────────────────────────────────────────────

These are patterns your project has discovered and ratified. They are ADVISORY — reminders, not gates. But heed them; they've fired repeatedly.

✓ SP-001: Ungrounded Claims
  Rule: If a claim about corpus state is made without a fresh Supabase query in the same session, flag before Phase 3 declaration.
  Last fired: 2026-07-22 (3 total fires)
  
✓ SP-004: Artifact Breadth
  Rule: Before POSTFLIGHT, check that you've logged findings, decisions, AND dead-ends. Narrow breadth → narrow grounding.
  Last fired: 2026-07-20 (5 total fires)

─────────────────────────────────────────────────────────
```

### 5.3 Per-Donella-Meadows L2 Heuristic Pattern Rule

**These are advisory, not gates**, per **L2 (Heuristic Pattern Checks are Advisory)** in your code-audit ledger. Reason: heuristics are fallible; enforcing them as hard gates would block valid work when the heuristic mis-fires.

**But:** Advisory checks can still be *visible* and *loud*. They surface the pattern and let the session decide whether it applies.

---

## Part 6: During-Session Application

### 6.1 Pre-Phase-1 Checklist

Before starting Phase 1, the advisory checklist is displayed. Claude reviews it. This is informational, not a gate—but it shifts the behavior upstream (awareness before execution, not penalty after).

### 6.2 Advisory Checks During Execution (Optional)

If a session detects that a RATIFIED prior's pattern is about to occur, the system can surface a soft warning:

```
⚠ Advisory: This looks like SP-001 (ungrounded claim pattern). 
  Before proceeding, run the Supabase query to ground your claim.
```

Again: advisory, not blocking. But it increases the cost of ignoring the pattern (not from penalties, but from friction + visibility).

### 6.3 Logging When a Prior Fires

When a pattern is detected mid-session:

```python
if detect_pattern(SP_001_ungrounded_claim):
    prior = load_prior("SP-001")
    prior.fire_count += 1
    prior.fire_timestamps.append(now())
    prior.last_fired_in = current_session_id
    # Log to session transcript/findings (not auto-penalizing)
```

Firing is logged but doesn't gate the session. It updates the prior's fire record for staleness calculation.

---

## Part 7: Staleness and Supersession

### 7.1 Supersession Rule

A RATIFIED prior automatically moves to SUPERSEDED status if:
- **Fire count = 0** within the last **N sessions** (default: N = 5)

Meaning: If a pattern you ratified as important stops appearing for 5 sessions, it's superseded.

### 7.2 Implementation

At the end of each session:

```python
def update_prior_staleness():
    for prior in SESSION_PRIORS:
        if prior.status == "RATIFIED":
            sessions_since_fire = current_session_number - prior.last_fired_in
            if sessions_since_fire > STALE_THRESHOLD:
                prior.supersession_status = "SUPERSEDED"
                prior.superseded_at = now()
                # Don't delete; mark in JSON
```

### 7.3 Why Not Delete?

**Append-only discipline:**
- Same as REGISTERED.md—immutability for audit trails.
- If a pattern recurs years later, you have a full history (fire_timestamps, discovery context, etc.).
- Supersession is reversible: if a pattern fires again, flip `supersession_status` back to ACTIVE.

---

## Part 8: Integration Points

### 8.1 REGISTERED.md

**Relationship:** REGISTERED.md catalogs *incidents* (bad things that happened). SESSION_PRIORS derives *rules* from those incidents.

**Workflow:**
1. Incident discovered → logged in REGISTERED.md (Z2 ratification required).
2. After N incidents of the same type → pattern emerges → candidate prior drafted.
3. Z2 ratifies candidate → SESSION_PRIORS entry created with link to REGISTERED.md incidents.

**Field in SESSION_PRIORS:** `notes` field should reference related REGISTERED.md entries.

```json
{
  "id": "SP-007",
  "constraint_label": "d_comp_pattern_type_x",
  "notes": "Extracted from REGISTERED.md incidents D-COMP-001, D-COMP-003, D-COMP-005. Pattern: vectors drift without artifact support. Remedy: check breadth before POSTFLIGHT."
}
```

### 8.2 WGS Posts

**Workflow:**
1. Session close → candidates drafted → added to WGS post.
2. Z2 reviews WGS → ratifies, rejects, or defers candidates.
3. Ratified → added to SESSION_PRIORS_V1_0.json → live next session.

**Field in SESSION_PRIORS:** `discovered_in` points back to WGS post session.

### 8.3 CLAUDE.md Authority Sections

**Relationship:** Authority sections in CLAUDE.md are *static governance* (zones, gates, escalations). SESSION_PRIORS is *dynamic, learned governance* (rules that evolve as patterns emerge).

**They are complementary:**
- CLAUDE.md: "Here's how decisions are made (Z1/Z2/Z3 gates)."
- SESSION_PRIORS: "Here are the lessons we've learned about *how* to work within those gates."

---

## Part 9: Version Control and Deployment

### 9.1 File Location

```
/docs/SESSION_PRIORS_V1_0.json  (the live registry)
```

In git, versioned with all other governance artifacts.

### 9.2 Updates

**Who can update:**
- Z2 (Admiral): Ratify or supersede priors (modify `status`, add `ratified_by`, `ratified_at`).
- Automated system: Update fire records (fire_count, fire_timestamps, last_fired_in, supersession_status). *(Implementation detail; design phase: manual)*

**Commit discipline:**
- Z2 ratification changes: committed with message `governance: ratify session prior SP-XXX: <label>`
- Staleness updates: included in session-close workflow.

### 9.3 Backward Compatibility

Version field in JSON allows future schema evolution. v1.0 is the baseline.

---

## Part 10: Success Metrics and Validation

How do you know SESSION_PRIORS is working?

### 10.1 Metrics

| Metric | Baseline | Target | Meaning |
|--------|----------|--------|---------|
| **CHECK gate fires per session** | N (current) | N-2 or lower | Priors catch patterns upstream; fewer gates needed |
| **Pattern recurrence rate** | High (repeats every 2-3 sessions) | Low (rare after ratification) | Priors are effective |
| **WGS post length: Candidate Prior section** | ~3 candidates/WGS | Declining over time | Fewer new patterns emerging (system learning) |
| **Prior fire count distribution** | N/A | Concentration on top 3-5 priors | Signals which patterns are most critical |
| **Supersession rate** | N/A | ~10-20% of priors superseded per quarter | Staleness control working; old patterns stay gone |
| **False positive advisory checks** | N/A | < 20% of advisory fires ignored | Priors are well-calibrated; high trust |

### 10.2 Validation Workflow (Post-Implementation)

1. **Pilot phase (first 5-10 sessions):** Monitor advisory checklist usage. Do candidates get ratified? Are fires logged?
2. **Scaling phase (sessions 11-30):** Check if CHECK gate count drops as priors mature. Do patterns recur less?
3. **Steady state (sessions 30+):** Are priors stable? Is supersession rate healthy? Do new patterns still emerge?

---

## Part 11: Governance Scope

**Z1 or Z2 or Z3?**

- **Z1:** Design (this document). Candidate discovery and initial drafting happen in Z1 (part of normal session close, no gate).
- **Z2:** Ratification gate. Candidates move from Z1_CANDIDATE to RATIFIED only via Z2 decision.
- **Z3:** Application. Priors are loaded and checked at session start and during work. No Z3 gate (they're advisory).

**Who decides:**
- Admiral (Carly) ratifies priors (Z2 authority).
- Future delegation possible (if another practitioner in the foundation takes on governance review).

---

## Part 12: Known Limitations and Open Questions

### 12.1 Limitations

1. **Heuristics are fallible:** A RATIFIED prior might mis-fire in edge cases (false positives). L2 mitigates by keeping them advisory.
2. **Pattern discovery is coarse:** Early versions detect obvious patterns (ungrounded claims). Subtle patterns might be missed.
3. **Staleness threshold is hard-coded (N=5):** Should it vary by pattern type or severity?
4. **No weighting:** All RATIFIED priors are shown with equal prominence. Should high-fire-count priors be emphasized?

### 12.2 Open Questions for Z2 Ratification

1. **Pilot scope:** Should SESSION_PRIORS start in empirica-foundation-evaluator only, or roll out to all 6 practices?
2. **Stale threshold:** Is N=5 sessions reasonable for the evaluator, or should it be shorter (N=3) or longer (N=10)?
3. **Advisory check UX:** Should soft warnings appear mid-session, or only at session open?
4. **Delegation:** If Admiral ratifies priors, can mesh-support or other practices delegate ratification to their own decision-makers?

---

## Part 13: Example Walkthrough

### Scenario: Ungrounded Claim Pattern

**Session 1 (Discovery):**
- Claude claims "the model is well-calibrated" without a fresh query to calibration_metrics table.
- Session close audit detects this.
- Candidate prior drafted: SP-001.
- Added to WGS post for Z2 review.

**WGS Review (Z2):**
- Admiral sees SP-001 candidate.
- Checks REGISTERED.md: finds 2 prior incidents where ungrounded claims caused rework.
- Decides: RATIFY (this is a real pattern).
- Updates SESSION_PRIORS_V1_0.json: adds SP-001 with status=RATIFIED, ratified_by=carly, ratified_at=[timestamp].

**Session 2 (Application):**
- Session open: SESSION_PRIORS loaded.
- Advisory checklist displayed: "SP-001: Ungrounded Claims — if you claim corpus state, query fresh."
- Claude reads it, understands the rule.
- Later, Claude is tempted to claim "the codebase has N functions." Before asserting, recalls SP-001.
- Runs `git grep -c "^def"` to ground the claim.
- Session close: SP-001 fire_count incremented to 1, last_fired_in updated.

**Session 3 (Continued Application):**
- Advisory checklist shown again: SP-001 with 2 fires now.
- Pattern continues to be relevant.

**Session 8 (Staleness Check, if no fires):**
- It's been 5 sessions with no fires of SP-001.
- Automatic check: sessions_since_fire > 5 → supersession_status = SUPERSEDED.
- SP-001 no longer appears on the advisory checklist (but remains in JSON for audit).

**Session 15 (Pattern Returns):**
- Claude makes an ungrounded claim about corpus state.
- Audit detects it, sees SP-001 is superseded.
- Candidate prior drafted: SP-010 (new variant of the pattern).
- Z2 reviews: "Ah, the pattern is back. Re-activate SP-001 or draft a new one?"
- Decision: re-activate SP-001 (flip supersession_status back to ACTIVE, reset fire_count).

---

## Part 14: Document Status and Next Steps

**Status:** Z1 Design (Finalized)  
**Review Gate:** Z2 Ratification (Admiral decision: approve, conditional, or defer)  
**Implementation Gate:** Building Freeze (queue behind charter gates)

**Next Steps (after Z2 decision):**
1. If approved: finalize Z2 ratification procedure (see companion document).
2. Create pilot implementation plan (scope, timeline, tooling).
3. Integrate with session initialization logic (queue for implementation phase).

---

## Appendix A: JSON Schema (Formal)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "version": { "type": "string", "enum": ["1.0"] },
    "last_updated": { "type": "string", "format": "date-time" },
    "priors": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string", "pattern": "^SP-[0-9]{3,}$" },
          "discovered_in": { "type": "string", "format": "uuid" },
          "constraint_label": { "type": "string" },
          "rule": { "type": "string" },
          "scope_limit": { "type": "string" },
          "status": { "type": "string", "enum": ["Z1_CANDIDATE", "RATIFIED", "SUPERSEDED"] },
          "ratified_by": { "type": ["string", "null"] },
          "ratified_at": { "type": ["string", "null"], "format": "date-time" },
          "last_fired_in": { "type": ["string", "null"], "format": "uuid" },
          "fire_count": { "type": "integer", "minimum": 0 },
          "fire_timestamps": { "type": "array", "items": { "type": "string", "format": "date-time" } },
          "supersession_status": { "type": "string", "enum": ["ACTIVE", "SUPERSEDED"] },
          "superseded_by": { "type": ["string", "null"], "pattern": "^SP-[0-9]{3,}$" },
          "superseded_at": { "type": ["string", "null"], "format": "date-time" },
          "notes": { "type": "string" }
        },
        "required": ["id", "discovered_in", "constraint_label", "rule", "scope_limit", "status", "fire_count", "fire_timestamps", "supersession_status"],
        "additionalProperties": false
      }
    }
  },
  "required": ["version", "last_updated", "priors"],
  "additionalProperties": false
}
```

---

## Appendix B: Glossary

| Term | Definition |
|------|-----------|
| **Prior** | A learned rule derived from a recurring pattern in prior sessions. Applied at session initialization. |
| **Candidate Prior** | A prior that has been discovered but not yet ratified by Z2. Status: Z1_CANDIDATE. |
| **Ratified Prior** | A prior approved by Z2 and live in SESSION_PRIORS_V1_0.json. Status: RATIFIED. |
| **Fire / Firing** | When a pattern recurs and the prior is activated/checked during a session. |
| **Supersession** | When a RATIFIED prior is marked inactive due to staleness (no fires for N sessions). Status: SUPERSEDED. |
| **Advisory Check** | A soft warning or reminder (not a gate) that flags when a prior pattern is about to occur. |

---

## Appendix C: Related Governance Artifacts

- **AUTHORITY_MAPPING_Z3_EMPIRICA_V1.md** — Z1/Z2/Z3 zone definitions (SESSION_PRIORS fits in Z1/Z2/Z3 boundaries).
- **ESCALATION_PROTOCOL.md** — Escalation triggers (SESSION_PRIORS prevents some escalations by catching patterns upstream).
- **REGISTERED.md** — Incident log (priors are derived from repeated incidents).
- **CLAUDE_MD_AUTHORITY_TEMPLATE.md** — Authority layer template (SESSION_PRIORS is a governance data structure, referenced in CLAUDE.md).

---

**End of SESSION_PRIORS_SPECIFICATION_V1_0.md**
