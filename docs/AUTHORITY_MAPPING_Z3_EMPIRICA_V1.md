# Authority Mapping: Z3 Protocol ↔ Empirica Transaction Discipline

**Version:** 1.0  
**Status:** M2 Rank 1 Foundation Document (DRAFT — awaiting Admiral ratification)  
**Authority:** empirica-foundation Admiral  
**Date:** 2026-07-18  

---

## Executive Summary

The **Z3 Authority Protocol** (3-tier governance for terminal execution) and the **Empirica Transaction Discipline** (PREFLIGHT → NOETIC → CHECK → PRAXIC → POSTFLIGHT) describe the same governance cycle using different terminology. This document maps them 1:1 so both frameworks align without contradiction.

**Result:** All 40+ repositories across the foundation can follow either protocol interchangeably — they describe the same authority boundaries, just at different layers of abstraction.

---

## Conceptual Alignment

### Z3 Protocol Framing
- **Zone 1:** Chat deliberation (what should happen?)
- **Zone 2:** Authority documents (approval gates)
- **Zone 3:** Terminal execution (make it happen)

### Empirica Transaction Framing
- **PREFLIGHT:** Declare scope + initial vectors
- **NOETIC:** Investigate (gather evidence)
- **CHECK:** Gate readiness (approve to proceed)
- **PRAXIC:** Implement (execute changes)
- **POSTFLIGHT:** Measure + close transaction

---

## Direct Mapping (The Core Alignment)

| Z3 Zone | Empirica Phase | Purpose | Authority Role | Evidence Required |
|---------|---|---------|---|---|
| **Zone 1** | PREFLIGHT + NOETIC | Deliberation: what? why? | **Chat/discussion** (Slack, collab mesh, proposals) | Questions, assumptions, findings logged |
| **Zone 2** | CHECK gate | Approval: is this ready? | **Authority document** (spec, RFC, design doc) | Known vectors ≥ threshold, uncertainty < 0.4 |
| **Zone 3** | PRAXIC + POSTFLIGHT | Execution: how? verify. | **Terminal execution** (git commit, code review, verification ledger) | Commit SHA, P3 verification, grounded calibration |

---

## Detailed Phase-by-Phase Mapping

### Phase 1: DELIBERATION (Z1 + PREFLIGHT)

**What happens:** Peers (or an individual) surface a proposal, gather questions, explore options.

**Z3 Zone 1 equivalent:** "Chat deliberation — no mutations"
- Happens in Slack channels, mesh collabs, or proposal threads
- No code commits, no file edits, no external calls
- Goal: Build shared understanding

**Empirica equivalent:** PREFLIGHT + early NOETIC
- Run `empirica preflight-submit` to open the transaction
- Log initial vectors (know, uncertainty, context, etc.)
- Investigate (Read, Grep, investigate tools)
- Log findings, unknowns, assumptions as you learn

**Output:** Well-logged findings + knowable unknowns

**Who decides to proceed?** Anyone with initial context can answer "do I know enough?" If yes → move to Zone 2. If no → log the unknown and continue investigation.

---

### Phase 2: AUTHORITY (Z2 + CHECK)

**What happens:** A decision-maker reviews the proposal + findings, gates it (PROCEED / INVESTIGATE MORE / BLOCKED).

**Z3 Zone 2 equivalent:** "Authority document"
- Authority lives in a spec, design doc, or RFC (written, committed, tracked)
- Specifies WHAT to change + WHO must approve + UNDER WHAT CONDITIONS
- Is the single source of truth for whether a Z3 session is authorized

**Empirica equivalent:** CHECK gate
- `empirica check-submit` with grounded vectors (know, uncertainty, context, etc.)
- Sentinel enforces thresholds (know ≥ 0.7, uncertainty < 0.4, etc.)
- If vectors pass → `proceed` (move to PRAXIC)
- If not → `investigate` (go back to NOETIC)
- **CHECK is the authority gate** — before CHECK passes, you have no authority to act

**Output:** CHECK response (proceed | investigate | blocked)

**Who decides?** The Admiral (Carly), or per-zone delegated authority (see §Authority Delegation below).

---

### Phase 3: EXECUTION (Z3 + PRAXIC + POSTFLIGHT)

**What happens:** Authorized practitioner executes the change per the approved spec, verifies it landed, closes the transaction.

**Z3 Zone 3 equivalent:** "Terminal execution" per Z3_PROTOCOL.md
- Pre-flight checklist (10 items: authority doc loaded, files confirmed, git clean, etc.)
- Execution discipline (one file at a time, diff before staging, commit per Z3 standard, push immediately)
- P3 verification (curl raw URL, confirm change landed, log verification ledger)

**Empirica equivalent:** PRAXIC + POSTFLIGHT
- Make the changes (code edits, commits)
- One task per commit (per epistemic transaction discipline)
- Each commit closes one task (`goals-complete-task --evidence "commit SHA"`)
- `empirica postflight-submit` closes the transaction
- Sentinel scores grounded calibration (predicted vs actual vectors)

**Output:** Committed change + verification ledger + grounded calibration measurement

**Who executes?** Any practitioner authorized by Zone 2 authority document.

---

## Authority Delegation — Who Approves What

The **Z3 Authority Matrix** below specifies approval chains for common issue types across all 9 local practices:

| Issue Type | Zone 1 (Chat) | Zone 2 (Authority) | Zone 3 (Executor) | Decision Maker |
|---|---|---|---|---|
| **Configuration change** (project.yaml, CLAUDE.md, env var) | Collab proposal or informal chat | Short RFC in repo `.authority/` folder | Local practice commit | Zone 1 opener (auto-approved if no objections after 24h) |
| **Authority document update** (CLAUDE.md, EVALUATOR_RULES.md, charter docs) | Collab + mesh discussion | Full design doc + 48h review period | Admiral ratification + commit | Admiral (Carly) — serial gate |
| **Cross-practice decision** (standardization, dependency pins, schema locks) | Mesh collab (multiple practices) | Design doc + empirica finding-log | Parallel implementation per practice | Admiral (Carly) or delegated zone authority |
| **Security/credentials** (key rotation, secret management, access control) | NO CHAT (skip to Zone 2) | Formal authority doc + sign-off checklist | Immediate execution per Z3_PROTOCOL Sections B-C | Admiral (Carly) — high urgency |
| **Release/deployment** (version pin, schema migration, production deployment) | WGS sync (weekly governance sync) meeting | Release notes + breaking changes documented | Tagged release + deployment checklist | Admiral (Carly) + release owner |

---

## §Authority Delegation — Per-Zone Rules

### Zone 1 Authority (Chat/Collab)

**Who decides:** Anyone in the relevant practice or mesh.

**Decision rule:** Proposal stays open 24h. If 0 objections → proceeds to Zone 2. If objections → escalate or resolve in chat.

**Common triggers:** Config tweaks, documentation updates, procedure refinements (low risk).

---

### Zone 2 Authority (Specs/RFCs)

**Who decides:** The practice owner (or delegated peer) + Admiral review.

**Decision rule:** 
- Practice owner drafts/approves the spec (authority document)
- Admiral reviews for cross-practice impact + consistency
- Admiral approves → signed off (commit message references it)
- If Admiral blocks → returned for revision

**Latency:** 24h–48h typical.

**Common triggers:** Feature design, schema changes, dependency upgrades, standardization.

---

### Zone 3 Authority (Terminal Execution)

**Who decides:** The person with the signed Zone 2 authority document + Z3 pre-flight checklist approval.

**Decision rule:** Execute per spec + Z3 discipline. No changes outside the authority document's matrix. Verify every file immediately.

**Latency:** Immediate (per-file timing).

**Common triggers:** All changes that pass Zone 2.

---

## Escalation Path (When to escalate between zones)

```
Zone 1 (Chat) — discovery, proposals, unknowns
          ↓
   (24h-48h wait, then)
          ↓
Zone 2 (Authority) — decision + spec writing
          ↓
   (Approval decision: YES/NO)
          ↓
Zone 3 (Execution) — terminal changes, verification
          ↓
   (Verification ledger + POSTFLIGHT)
          ↓
Grounded Calibration (measurement)
```

**Escalation triggers (Zone 1 → Zone 2):**
- A collab or proposal needs a decision
- A practice owner signals readiness to author a spec
- 24h deliberation period elapsed

**Escalation triggers (Zone 2 → Zone 3):**
- Admiral approves the authority document
- Pre-flight checklist (B-1 through B-10) passes
- CHECK gate (empirica) returns `proceed`

**Escalation triggers (reverse: Zone 3 → Zone 2):**
- Discovery of unauthorized changes (C-6 violation)
- Verification failure (P3 check doesn't confirm change)
- Grounded calibration shows large divergence (predicted vs actual vectors)
- → Halt execution, log decision-log (mistake or dead-end), escalate back to Admiral

---

## CLAUDE.md Authority Section (Template for all 9 practices)

Every local practice's repo-root `CLAUDE.md` must include:

```markdown
## Authority Layer (Zone Mapping)

**This practice inhabits:** [Zone 1 | Zone 2 | Zone 3] scopes

**Authority delegates to:**
- **Zone 1 decisions** (config tweaks, doc updates): Practice owner (auto-approval if no objections 24h)
- **Zone 2 authority** (specs, schema changes): Admiral (serial gate)
- **Zone 3 execution** (terminal changes): Practitioner with Z2 authority doc

**Escalation chain:** Zone 1 (practice chat) → Zone 2 (Admiral) → Zone 3 (execution)

**Reference:** `@docs/AUTHORITY_MAPPING_Z3_EMPIRICA_V1.md`
```

---

## Practical Examples

### Example 1: Config Change (Low Risk)

```
ZONE 1 (Chat)
  Practitioner in #wgs-sync: "Should we add calibration_weights to project.yaml?"
  Responses: "Yes" + "Agreed" (no objections)
  24h wait ✓
  
→ ZONE 2 (Authority)
  Brief RFC in repo: "Add calibration_weights field to project.yaml (optional, defaults provided)"
  Admiral response: "APPROVED"
  
→ ZONE 3 (Execution)
  Pre-flight checklist (B-1 to B-10): ✓ PASS
  Edit project.yaml, run diff, stage, commit (per C-1 to C-5)
  git push
  P3 verification: curl raw.githubusercontent.com, grep "calibration_weights" ✓
  
→ POSTFLIGHT
  goals-complete-task --evidence "commit abc123 — add calibration_weights field"
  Grounded calibration: ✓ MEASURED
```

### Example 2: Security (High Priority)

```
ZONE 1: SKIP (security items don't chat)

→ ZONE 2 (Authority)
  Formal document: "Key Rotation Protocol v1.0"
  Admiral signs off: "AUTHORIZED"
  References: IC-025 (secrets management), EVALUATOR_RULES.md
  
→ ZONE 3 (Execution)
  Pre-flight B-9: "Confirm any tokens/keys needed are in macOS Keychain" ✓
  Execute per Z3 Sections B-C (one file at a time, no diffs exposed)
  P3 verification: "Key ID updated in secrets-manager" ✓
  
→ POSTFLIGHT
  Grounded calibration: UNGROUNDED (work_type=remote-ops for credential handling)
  Calibration status: self-assessment stands (no external sensors available)
```

### Example 3: Cross-Practice Harmonization (Medium Complexity)

```
ZONE 1 (Mesh Collab)
  empirica-autonomy + empirica-mesh-support + empirica-outreach
  Collab message: "All 3 practices need to align on dependency versions"
  Outcome: "Let's use Rank 2 gate decision"
  
→ ZONE 2 (Authority)
  Design doc: "Dependency Pin Coordination — mcp@1.5.2, empirica-cli@1.12.14"
  Ratification: Admiral approves + signs
  Per-practice specs: Each practice author commits the RFC to their repo
  
→ ZONE 3 (Execution) — PARALLEL ACROSS 3 PRACTICES
  Practice 1: Edit package.json, commit, verify (per C-1 to C-5)
  Practice 2: Edit requirements.txt, commit, verify
  Practice 3: Edit mix.exs, commit, verify
  
  All 3 verify independently, then message back: "✓ empirica-autonomy landed"
  
→ POSTFLIGHT (per practice)
  Each closes its own goals-complete-task
  Empirica: Merged findings from all 3 practices into cross-practice decision-log
```

---

## Implementation Checklist (M2 Rank 1)

- [ ] **Map T1:** Z3 Protocol ↔ Empirica phases documented (this file) ✓
- [ ] **Map T2:** Authority matrix created (AUTHORITY_MATRIX.yaml)
- [ ] **Map T3:** Escalation protocol documented (ESCALATION_PROTOCOL.md)
- [ ] **Map T4:** CLAUDE.md updated across 9 practices with authority section
- [ ] **Map T5:** Admiral ratifies via governance proposal + sign-off

---

## Next Phases (M2 Rank 2+)

Once authority mapping is complete and ratified:

1. **Rank 2:** State machine harmonization (ACAT phases ↔ charter gates)
2. **Rank 3:** Configuration standardization (project.yaml canonical template)
3. **Rank 4:** Dependencies (version pin coordination)
4. **Rank 5:** Naming consistency (SemVer enforcement)
5. **Rank 6:** Schemas (ACAT v5.4 corpus lock)

---

**Status:** ✅ AUTHORITY MAPPING COMPLETE (M2 T1)  
**Next:** Create AUTHORITY_MATRIX.yaml (M2 T2)  
**Ratification:** Pending Admiral sign-off

