# Governance Document Index — Single Source of Truth

**Version:** 1.0  
**Status:** M2 Rank 1 Task 6  
**Authority:** empirica-foundation Admiral (Carly R. Anderson)  
**Last Updated:** 2026-09-09  

---

## Purpose

This index is the **canonical reference** for all governance documents across empirica-foundation practices. It serves as:

1. **Navigation hub** — where to find each document
2. **Status tracker** — which documents are DRAFT, RATIFIED, DEPLOYED
3. **Dependency mapper** — which documents depend on which others
4. **Conformance checklist** — verification that all practices have the required documents

---

## Document Registry

### Authority Layer (Zone Mapping)

| Document | Location | Version | Status | Ratified By | Ratification Date |
|----------|----------|---------|--------|---|---|
| **AUTHORITY_MAPPING_Z3_EMPIRICA_V1.md** | `docs/` | 1.0 | **DRAFT** | — | — |
| **AUTHORITY_MATRIX.yaml** | `docs/` | 1.0 | **DRAFT** | — | — |
| **ESCALATION_PROTOCOL.md** | `docs/` | 1.0 | **DRAFT** | — | — |

### Schema & Configuration

| Document | Location | Version | Status | Ratified By | Ratification Date |
|----------|----------|---------|--------|---|---|
| **SCHEMA_VERSIONING_STRATEGY.md** | `docs/` | 1.0 | **DRAFT** | — | — |
| **CLAUDE.md** (Authority Layer section) | Repository root | 2.0 | **ACTIVE** | Admiral | 2026-07-24 |

### Cross-Practice Coordination

| Document | Location | Version | Status | Ratified By | Ratification Date |
|----------|----------|---------|--------|---|---|
| **EVALUATOR_SEAT.md** | `docs/` | 1.0 | **ACTIVE** | Admiral | 2026-07-24 |
| **EVALUATOR_RULES.md** | `docs/` | 1.0 | **ACTIVE** | Admiral | 2026-07-24 |

### Registry & Measurement

| Document | Location | Version | Status | Ratified By | Ratification Date |
|----------|----------|---------|--------|---|---|
| **REGISTERED.md** | `operations/` | 1.0 | **ACTIVE** | Admiral | 2026-07-24 |
| **ARTIFACT_REGISTRY_INDEX.yaml** | `.empirica/governance/` | 1.0 | **ACTIVE** | Admiral | 2026-09-09 |

---

## Status Definitions

| Status | Meaning | Action Required |
|--------|---------|---|
| **DRAFT** | Document complete, awaiting Admiral ratification | Awaiting Zone 2 approval signature |
| **RATIFIED** | Admiral has signed off with timestamp | Ready for DEPLOYED deployment in practices |
| **DEPLOYED** | Ratified document is now governing 9 practices | Enforce via Zone 2/3 gates |
| **ACTIVE** | Currently governing cross-practice behavior | Monitor for drift via quarterly audits |
| **DEPRECATED** | Superseded by newer version | Migration period to new version begins |

---

## Dependency Map

```
AUTHORITY_MAPPING_Z3_EMPIRICA_V1.md (Z3 ↔ Empirica phases)
  ↓ depends on ↓
AUTHORITY_MATRIX.yaml (per-practice delegation)
  ↓ depends on ↓
ESCALATION_PROTOCOL.md (zone transition triggers)
  ↓ depends on ↓
SCHEMA_VERSIONING_STRATEGY.md (schema compat rules)
  ↓ depends on ↓
CLAUDE.md Authority Layer (local governance reference)
  ↓ enables ↓
Cross-practice verification (Step 7)
  ↓ enables ↓
Ratification + POSTFLIGHT closure
```

**Key insight:** All 3 governance documents (AUTHORITY_MAPPING, AUTHORITY_MATRIX, ESCALATION_PROTOCOL) must be ratified **together** — they are interdependent. Ratifying one without the others creates ambiguity in escalation paths.

---

## Registry Entries

This section maps governance decisions to registry IDs for cross-reference and historical tracking.

### Governance Directives (GD-*)

| GD ID | Document | Status | Triggered By |
|-------|----------|--------|---|
| **GD-10** | AUTHORITY_MATRIX.yaml (claim-class gate obligation) | **PROVISIONAL** | IC-052 (receipt overstatement) |
| **GD-11** | ESCALATION_PROTOCOL.md (6 escalation triggers operationalized) | **DRAFT** | M2 Rank 1 execution |
| **GD-12** | SCHEMA_VERSIONING_STRATEGY.md (schema compat enforcement) | **DRAFT** | M2 Rank 1 execution |

### Integrity Corrections (IC-*) Resolved by Governance

| IC ID | Issue | Resolution Document | GD ID |
|-------|-------|---|---|
| **IC-052** | Receipt-content overstatement | Claim-class gate (AUTHORITY_MATRIX §) | GD-10 |
| **IC-031** | GitHub verification (P3) | P3 in ESCALATION_PROTOCOL §Trigger 4 | GD-11 |

---

## Conformance Verification

### Pre-Ratification Checklist (M2 Rank 1)

- [ ] Admiral reviewed AUTHORITY_MAPPING_Z3_EMPIRICA_V1.md (target: 2h)
- [ ] Admiral reviewed AUTHORITY_MATRIX.yaml (target: 2h)
- [ ] Admiral reviewed ESCALATION_PROTOCOL.md (target: 1h)
- [ ] Admiral created decision-log entry (target: 0.5h)
- [ ] Admiral committed ratification message to main (target: 0.25h)
- [ ] SCHEMA_VERSIONING_STRATEGY.md linked from AUTHORITY_MATRIX.yaml
- [ ] GOVERNANCE_DOCUMENT_INDEX.md (this file) committed
- [ ] Cross-practice CLAUDE.md files reference this index

**Total estimated time:** 5.75h (can run ~3h in parallel)

### Post-Ratification Deployment Checklist (M2 Rank 2)

- [ ] All 9 practices updated CLAUDE.md to reference ratified governance docs
- [ ] CI schema-check.py updated to enforce AUTHORITY_MATRIX rules
- [ ] empirica CLI version-check enforces Sentinel gate (per SCHEMA_VERSIONING_STRATEGY)
- [ ] Quarterly governance audit scheduled (Admiral + mesh-support)
- [ ] Registry entries GD-10, GD-11, GD-12 all ACTIVE

---

## Access & Updates

### Who Can Update This Index

| Document | Update Authority | Process |
|----------|---|---|
| GOVERNANCE_DOCUMENT_INDEX.md (this file) | Administrator (humanaios Claude) | Zone 1 → Zone 2 RFC → Zone 3 commit |
| Status fields (DRAFT → RATIFIED → DEPLOYED) | Admiral (Carly R. Anderson) | Updated during Admiral ratification sign-off |
| Registry entries (GD-*, IC-*) | Administrator + Admiral co-signature | Zone 2 decision-log entry |

### Quarterly Audit

**When:** First Monday of each quarter (Oct 1, Jan 1, Apr 1, Jul 1)  
**Who:** Admiral (Carly) + mesh-support (cross-org infrastructure)  
**What:** Verify all governance docs are current, no divergence across practices, no stale DRAFT status lingering >90 days

---

## Linking Strategy: How Documents Reference Each Other

### Within humanaios

- AUTHORITY_MAPPING.md references → AUTHORITY_MATRIX.yaml (line 115)
- AUTHORITY_MATRIX.yaml references → ESCALATION_PROTOCOL.md (conformance checklist, line 340)
- ESCALATION_PROTOCOL.md references → SCHEMA_VERSIONING_STRATEGY.md (future; TBD)
- SCHEMA_VERSIONING_STRATEGY.md references → GOVERNANCE_DOCUMENT_INDEX.md (this file)

### Cross-Practice

- Each practice's CLAUDE.md references:
  - `@docs/AUTHORITY_MAPPING_Z3_EMPIRICA_V1.md`
  - `@docs/AUTHORITY_MATRIX.yaml`
  - `@docs/ESCALATION_PROTOCOL.md`
  - `@docs/GOVERNANCE_DOCUMENT_INDEX.md` (navigation hub)

---

## Next Steps

1. **Admiral ratifies** the 3 DRAFT governance documents (AUTHORITY_MAPPING, AUTHORITY_MATRIX, ESCALATION_PROTOCOL)
2. **Status updates:** This index is updated with ratification dates + Admiral signature
3. **M2 Rank 2 begins:** State machine harmonization work (ACAT phases ↔ charter gates)

---

**Maintained by:** empirica-foundation Admiral (Carly R. Anderson)  
**Last audit:** 2026-09-09  
**Next audit:** 2026-10-01  

