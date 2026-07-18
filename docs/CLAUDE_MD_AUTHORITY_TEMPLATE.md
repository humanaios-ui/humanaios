# CLAUDE.md Authority Section — Template for All 9 Practices

**Status:** M2 Rank 1 Task 4 canonical template  
**Version:** 1.0  
**Date:** 2026-07-18

---

## How to Use This Template

Every local practice's repo-root `CLAUDE.md` must include an "Authority Layer" section (shown below). Customize `[PRACTICE_NAME]`, `[OWNER]`, and zone delegation as appropriate for your practice.

**Integration:** This section should be placed after any practice-specific instructions and before or alongside skill/hook references.

---

## Template (Copy-Paste This Section)

```markdown
## Authority Layer — Governance & Zone Mapping

**This practice inhabits:** empirica-foundation local governance  
**Practice name:** [PRACTICE_NAME] (e.g., empirica-autonomy)  
**Practice owner:** [OWNER_NAME] (e.g., AI practitioner or team)  

### Zone Scope & Delegation

This practice participates in the 3-zone governance model (Z3 Protocol → Empirica alignment):

- **Zone 1 (Chat/Collab):** Deliberation, proposals, mesh discussion
  - **Decision-maker:** [Practice owner] (or Admiral if cross-foundation)
  - **Auto-approval:** Yes, if zero objections after 24h–72h review period
  - **Escalation:** To Zone 2 if objections or cross-practice impact

- **Zone 2 (Authority Documents):** Specs, RFCs, design docs, CHECK gate
  - **Decision-maker:** [Practice owner] OR Admiral (serial gate for authority-doc changes)
  - **Approval latency:** 24h–48h typical
  - **Escalation:** To Zone 3 if approved; back to Zone 1 if blocked

- **Zone 3 (Terminal Execution):** Code commits, P3 verification, POSTFLIGHT
  - **Decision-maker:** Authorized practitioner (from team)
  - **Pre-flight checklist:** Z3_PROTOCOL.md Sections B-1 through B-10
  - **Escalation:** Back to Zone 2 if P3 failure or grounded calibration divergence > 0.3

### Governance Documents (Single Source of Truth)

All governance decisions in this practice are grounded in:

- **Authority Mapping:** `@../docs/AUTHORITY_MAPPING_Z3_EMPIRICA_V1.md`
  - Maps Z3 Protocol (Zone 1/2/3) to Empirica transaction discipline
  - Defines who approves what at each phase

- **Authority Matrix:** `@../docs/AUTHORITY_MATRIX.yaml`
  - 9-cell grid: issue type × zone level → approval chain
  - Specifies evidence requirements + escalation triggers per cell

- **Escalation Protocol:** `@../docs/ESCALATION_PROTOCOL.md`
  - 6 escalation triggers + detection mechanisms
  - Communication protocol + decision gates
  - Special cases (emergency, cross-org, abandonment)

- **Z3 Protocol:** `@../operations/Z3_PROTOCOL.md` (or upstream)
  - Terminal execution discipline (pre-flight checklist, execution rules, P3 verification)

### Escalation Chain

```
Zone 1 (Chat/Collab)
  ↓ (auto-approve if no objections after 24–72h)
Zone 2 (Admiral Authority Decision)
  ├─ APPROVED → Zone 3 (execute)
  ├─ CONDITIONAL → Zone 1 (revise + re-submit)
  └─ BLOCKED → Zone 1 (abandon or redesign)
  ↓
Zone 3 (Terminal Execution)
  ├─ SUCCESS → POSTFLIGHT (close)
  ├─ P3 FAILURE → Zone 2 (Admiral review + decision log)
  └─ UNKNOWN DISCOVERED → Zone 2 (C-6 violation)
```

### Governance Triggers & Escalation

This practice escalates to Admiral when any of the following occur:

1. **Objection in Zone 1:** Any peer raises a concern → do NOT auto-approve
2. **Veto in Zone 2:** Admiral blocks a proposal → return to Zone 1
3. **CHECK gate failure:** empirica vectors below threshold → continue NOETIC
4. **P3 verification failure:** Change didn't land or CI failed → halt, investigate
5. **Cross-practice impact:** Change affects multiple practices → escalate to multi-practice collab
6. **Unknown discovered in Zone 3:** File needs edit not in authority doc → halt, escalate to Zone 2

See ESCALATION_PROTOCOL.md for full details.

### Authority Delegation (This Practice)

**Zone 1 (Chat/Collab) decisions:**
- Primary: [Practice owner]
- Secondary: Any [PRACTICE_NAME] team member (can propose)
- Auto-approval: Yes (24h–72h window, zero objections required)

**Zone 2 (Authority) decisions:**
- Primary: [Practice owner]
- Secondary: Admiral (Carly R. Anderson) — gates cross-practice + critical changes
- Approval latency: 24h–48h

**Zone 3 (Execution) decisions:**
- Primary: Authorized [PRACTICE_NAME] practitioner
- Secondary: Admiral (gates critical security/deployment changes)
- Pre-flight: Checklist B-1 through B-10 required

### Empirica Transaction Discipline

All work in this practice follows:

```
PREFLIGHT (declare scope + vectors)
  ↓
NOETIC (investigate, log findings/unknowns)
  ↓
CHECK (gate readiness: vectors ≥ threshold?)
  ↓
PRAXIC (execute: code commits, 1 per task)
  ↓
POSTFLIGHT (measure: grounded calibration)
```

Commands:
- `empirica preflight-submit -` (open transaction, declare vectors)
- `empirica finding-log`, `empirica unknown-log`, `empirica decision-log` (log during NOETIC/PRAXIC)
- `empirica check-submit -` (gate NOETIC → PRAXIC)
- `git commit` (per task, with authority reference)
- `empirica postflight-submit -` (close transaction, measure calibration)

See: empirica-system-prompt.md (system layer) + /epistemic-transaction (planning skill).

### Mesh Discipline (Multi-Practice Coordination)

When this practice coordinates with other empirica-foundation practices:

- **Pull when uncertain:** Use collab (auto-accepted, ungated) to ask peers
- **Push when convergent:** Use propose (ECO-gated, after CHECK) to request work
- **Ack what you complete:** Reply to peer proposals with commit evidence
- **Make sources first-class:** Use `source-add --visibility shared` for canonical references

See: /cortex-mailbox-send (send protocol) + /empirica-constitution §V (mesh discipline).

### References

- **Charter Milestone:** M2: Harmonization (Authority System — Rank 1, gateway blocker)
- **Authority:** empirica-foundation Admiral (Carly R. Anderson)
- **Last Updated:** 2026-07-18 (M2 Rank 1 Task 4)
- **Review Cycle:** Quarterly (Admiral audits escalation patterns + procedure updates)
```

---

## Customization Guide

Replace the following placeholders in the template:

| Placeholder | Description | Example |
|---|---|---|
| `[PRACTICE_NAME]` | Name of this practice | `empirica-autonomy` |
| `[OWNER_NAME]` | Owner or lead of this practice | `AI practitioner (Autonomy team)` |
| `[PRACTICE_NAME]` | (repeated) Same as above | |

**Per-zone customization (if needed):**

If your practice has delegated Zone 2 authority to someone other than the Admiral, customize the "Zone 2 (Authority Documents)" bullet:

```markdown
- **Zone 2 (Authority Documents):** Specs, RFCs, design docs, CHECK gate
  - **Decision-maker:** [Practice owner] (or Admiral for cross-practice impact)
  - **Approval latency:** 24h–48h typical
  - **Escalation:** To Zone 3 if approved; back to Zone 1 if blocked
```

Most practices will delegate Zone 2 fully to Admiral for clarity (no exceptions).

---

## Implementation Checklist

For each of the 9 practices:

- [ ] Read current CLAUDE.md (if it exists)
- [ ] Find the section after practice-specific instructions (before skills section)
- [ ] Insert the Authority Layer section (customized with practice name + owner)
- [ ] Verify references to external docs (@../docs/...) are correct
- [ ] Test that the file parses (no syntax errors)
- [ ] Commit: `git add CLAUDE.md && git commit -m "feat(authority): Add governance zone layer to CLAUDE.md per M2 Rank 1 Task 4"`
- [ ] Verify commit landed on main

---

## Testing (How to Verify the Section Works)

1. **Read the file:** Confirm the Authority Layer section loads without errors
2. **Check references:** Verify `@../docs/...` links resolve to actual files
3. **Slack sync:** Post message in #wgs-sync: "[Practice] CLAUDE.md updated with authority section"
4. **Admiral approval:** Carly reviews + acknowledges

---

**Template Ready for Rollout**

This template is now ready to be applied to all 9 practices (listed below).

