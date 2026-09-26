# M2 Rank 4: Phase 2 Schema Design Specification

**Document ID:** M2R4-PHASE2-SPEC-2026-08-07  
**Status:** APPROVED FOR EXECUTION  
**Admiral Decisions:** All 8 prompts resolved (2026-08-07)  
**Timeline:** 2-3 days  
**Depends on:** Phase 1 (schema discovery complete)

---

## Phase 2 Overview

Design canonical schemas for all 4 schema types discovered in Phase 1, incorporating Admiral's governance + path convention decisions. Output: v3.0 schema specs + migration rules.

---

## Design Decisions (Admiral-Approved)

### DM1: Governance Document Distribution — DISTRIBUTED + EXPLICIT SYNC

**Rationale:** Each practice owns its governance docs locally (autonomy, charter, authority). Central updates propagate via CI/CD sync hooks on evaluator/docs.

**Implementation:**
- Master docs live in `evaluator/docs/` (AUTHORITY_MATRIX.yaml, AUTHORITY_MAPPING.md, ESCALATION_PROTOCOL.md)
- Each practice has local copies in `docs/` (read-only reference)
- CI/CD hook: On evaluator/docs/* change, run `sync-governance-docs.sh` to update all other practices
- Validation: Pre-commit hook checks that all @-includes resolve locally

**Sync Frequency:** On-demand (evaluator docs change) + weekly validation

---

### DM2: Z3_PROTOCOL Ownership — HYBRID

**Rationale:** evaluator + humanaios keep local Z3_PROTOCOL (foundational autonomy practice); autonomy keeps local (phase-specific). Others reference upstream via @~/.claude/ path.

**Implementation:**
- **Local Z3_PROTOCOL:** evaluator, autonomy, humanaios (practice-specific variants)
- **Upstream Reference:** mesh-support, outreach, website use `@~/.claude/empirica-system-prompt.md` for core
- **Authority:** Each practice's Z3_PROTOCOL overrides upstream on conflict (local > global)

---

### DM3: Path Reference Convention — MIXED PER-PRACTICE

**Rationale:** Reflects practice maturity + scope.

**Rules:**
- **evaluator, humanaios (mature, independent):** Use @docs/ (local references)
- **autonomy (foundational):** Use @docs/ (local)
- **mesh-support, outreach, website (supporting):** Use @~/.claude/ for core + @docs/ for local governance (hybrid)
- All practices validate @-includes at project-init time

---

### DM4: Practice Charters — AUTONOMY-SPECIFIC ONLY

**Rationale:** Charter is autonomy's practice-defining document (scope, decision authority). Others inherit from autonomy's charter or reference it explicitly.

**Implementation:**
- **autonomy/CHARTER.md** (canonical, defines autonomy role + scope)
- **evaluator/CHARTER.md** (ALREADY EXISTS, define independent oversight scope)
- **humanaios/CHARTER.md** (ALREADY EXISTS, define open research scope)
- **Others (mesh-support, outreach, website):** No local charter; reference autonomy/CHARTER.md + governance docs

---

### DM5: Field Ordering Rule — ALPHABETICAL

**Rationale:** Deterministic, machine-processable, eliminates field-order variants.

**Implementation:**
- **project.yaml v3.0:** All fields alphabetically ordered within logical sections
- **Migration Script:** Auto-reorder v2.0 → v3.0 without semantic change
- **Validation:** Pre-commit hook enforces alphabetical order
- **Versioning:** Bump version field to "3.0" on migration

**New project.yaml v3.0 Structure:**
```yaml
version: "3.0"
# -- Metadata --
ai_id: <str>
canonical_seat: <str>
classification: <str>
created_at: <datetime>
created_by: <str>
description: <str>
# -- Organization & Authority --
org_id: <str>
tenant_slug: <str>
type: <str>
# -- Configuration --
auto_detect: <bool>
calibration_weights: <dict>
contacts: <list>
domain: <str>
domain_config: <dict>
engagements: <list>
evidence_profile: <dict>
languages: <list>
mesh_id_prefix: <str>
name: <str>
project_id: <str>
status: <str>
subjects: <list>
tags: <list>
# -- Relationships --
beads: <list>
edges: <list>
```

---

## Integration Design Approvals (All Approved)

### IA1: ACAT API as Public Mesh Service ✅

**Authority:** mesh-support + autonomy jointly operate ACAT endpoint  
**Deployment:** Standalone at api.humanaios.ai + internal proxy via empirica-mesh-support  
**Schema:** ACAT Assessment Payload v5.4 (frozen, 6mo deprecation window)  
**Auth:** API key per practice, rotated quarterly  
**Next Phase:** Phase 1 operator integration (mesh-support implementation)

---

### IA2: Hybrid Organizational Model ✅

**Entity Model:**
- **humanaios practice** (open research, foundation governance)
- **HumanAIOS LLC** (commercial/confidential, separate entity in registry)

**Governance:**
- humanaios: Inherits foundation protocols (@docs/ references, Z3 via humanaios/Z3_PROTOCOL)
- HumanAIOS LLC: Separate Zone 2 (Carly's commercial decisions), no automatic mesh routing

**Registry:**
- Create entity_type="commercial_entity" for HumanAIOS LLC
- Create serves relationship: humanaios_practice → HumanAIOS_LLC (research feeds business operations)

---

### IA3: ACAT as Calibration Signal Source ✅

**Dimensions Mapping:**
- ACAT humility ↔ Empirica uncertainty
- ACAT truth-seeking ↔ Empirica signal
- ACAT scheme ↔ Empirica coherence
- ACAT autonomy ↔ Empirica do

**Convergence Report:** Monthly (compare Empirica vectors vs ACAT assessments, flag divergences)  
**Methodology:** Canonical mapping @ empirica-autonomy (shared research)

---

## Phase 2 Deliverables

### 2.1 Canonical Schemas (3 specs)

**Spec A: project.yaml v3.0**
- Alphabetical field ordering (defined above)
- Migration script (v2.0 → v3.0)
- Validation rules (pre-commit hook)

**Spec B: Governance Document Schema**
- Master docs (evaluator/docs/)
- Per-practice copies (docs/)
- Sync mechanism (CI/CD hook)
- Validation (all @-includes resolve)

**Spec C: CLAUDE.md Authority Section Template**
- Standardized Z3_PROTOCOL reference (hybrid: local or upstream per practice)
- Path convention rules (mixed per DM3)
- Auto-approval logic (role-based)
- Escalation protocol (clear zones)

### 2.2 Conflict Resolution Rules

- Field ordering conflicts → Auto-reorder v3.0
- Governance doc divergence → Sync from master, log diff
- Z3_PROTOCOL mismatch → Local wins, log override
- Authority tier disagreements → Manual Admiral review (conflict_resolution="manual_admiral_review")

### 2.3 Migration Tooling

- `scripts/migrate-project-yaml-v3.py` — Auto-convert v2.0 → v3.0
- `scripts/sync-governance-docs.sh` — Push evaluator/docs/* to all practices
- `scripts/validate-schemas.py` — Pre-commit validation
- `.pre-commit-config.yaml` — Git hooks for all validation

### 2.4 Testing Plan

- Unit tests: Each migration rule (field ordering, governance refs, Z3 variants)
- Integration tests: All 6 foundation practices pass schema validation
- Regression tests: Verify no semantic change in v2.0 → v3.0 conversion
- Smoke test: Deploy validation hooks to all practices, zero false positives

---

## Phase 2 Timeline

| Day | Task |
|-----|------|
| **Day 1** | Spec A: project.yaml v3.0 + migration script |
| **Day 2** | Spec B: Governance sync + Spec C: CLAUDE.md template |
| **Day 3** | Testing + tooling + documentation |

**Completion:** 2026-08-10

---

## Phase 3 Preview

After Phase 2 design → Phase 3-4 implementation:
- **Phase 3:** Build migration tooling + validation hooks
- **Phase 4:** Deploy to all practices + verify no breaking changes
- **Phase 5:** Document governance-as-code patterns
- **Phase 6:** Automate schema versioning + deprecation

---

## Commit Message

```
feat(m2r4): schema design — canonical schemas + governance harmonization

Designed canonical schemas for project.yaml, governance docs, and CLAUDE.md
Authority section per Admiral decisions:

- DM1: Distributed governance docs + explicit sync (evaluator master)
- DM2: Hybrid Z3_PROTOCOL (local for autonomy/evaluator/humanaios, upstream for others)
- DM3: Mixed path convention per practice maturity
- DM4: Autonomy-specific charters only
- DM5: Alphabetical field ordering (v3.0)

Approved integrations:
- IA1: ACAT as public mesh service
- IA2: Hybrid org model (humanaios practice + HumanAIOS LLC)
- IA3: ACAT as calibration signal source

Deliverables:
- project.yaml v3.0 spec + migration rules
- Governance document sync mechanism
- CLAUDE.md Authority template
- Pre-commit validation hooks
- Testing plan (unit + integration + regression)

Next: Phase 3 implementation (migration tooling)

Authority: M2 Rank 4 RFC, Admiral decisions 2026-08-07
Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
```

---

**Status: Ready for Phase 3 (implementation). All Admiral decisions incorporated.**
