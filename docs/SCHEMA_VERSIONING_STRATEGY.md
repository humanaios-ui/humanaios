# Schema Versioning Strategy — Backward Compatibility & Migration

**Version:** 1.0  
**Status:** M2 Rank 1 Task 5 (DRAFT — awaiting Admiral ratification per AUTHORITY_MAPPING)  
**Authority:** empirica-foundation Admiral (Carly R. Anderson)  
**Date:** 2026-09-09  

---

## Executive Summary

This document defines how schema changes (project.yaml, ACAT, governance specs) are versioned, validated, and migrated across the empirica-foundation practices. It ensures:

1. **Backward compatibility** — old schemas continue working during migration windows
2. **Drift detection** — schema divergence between practices is caught and remediated
3. **Migration paths** — clear procedures for rolling out schema upgrades
4. **Enforcement points** — CI/CLI gates that block incompatible operations

---

## What This Covers

| Item | Current Version | Backward Compat | Enforcement |
|------|---|---|---|
| **project.yaml** | 2.1 | Supported down to v1.0 | CI gate + empirica CLI schema-check |
| **ACAT dimensions.yaml** | 5.4 (frozen at Phase 1b) | Supported down to v4.0 | acat_loader.py validation |
| **Governance specs** (AUTHORITY_MATRIX, ESCALATION_PROTOCOL) | 1.0 | None yet (first release) | empirica check-submit gate |
| **Calibration vectors** | 1.0 (13-vector set) | None yet (foundational) | Sentinel enforcement |
| **empirica artifact schema** | core v1.13.33 | Supported down to v1.12.0 | empirica CLI version check |

---

## project.yaml Versioning

### Schema Versions

```yaml
# project.yaml v2.1 (CURRENT)
version: "2.1"
ai_id: humanaios
canonical_seat: empirica-foundation.carly.humanaios
mesh_id_prefix: empirica-foundation.carly

# New in v2.1: calibration_weights (optional, with defaults)
calibration_weights:
  know: {floor: 0.5, ceiling: 1.0, decay_per_session: -0.05}
  uncertainty: {floor: 0.0, ceiling: 0.5, decay_per_session: -0.03}
  # ... (other 11 vectors)
```

### Backward Compatibility Rules

| Reader | v2.1 | v2.0 | v1.5 |
|--------|---|---|---|
| empirica CLI v1.13 | ✓ reads + uses defaults | ✓ reads, no defaults | ✗ fails (required fields missing) |
| humanaios code | ✓ full | ✓ full (defaults applied) | ✗ error |
| CI schema-check | ✓ passes | ✓ passes | ✗ fails |

**Migration window:** Practices running v1.5 MUST upgrade to v2.0 by 2026-10-15. After that date, humanaios CLI will not accept v1.5 schemas.

### Detection: Schema Drift Audit

Run this to find schema divergence across practices:

```bash
for practice in humanaios empirica-autonomy empirica-mesh-support empirica-outreach empirica-foundation-evaluator website; do
  SCHEMA_VERSION=$(grep "^version:" /Users/andersonfamily/practices/$practice/.empirica/project.yaml | awk '{print $2}')
  echo "$practice: $SCHEMA_VERSION"
done
```

**Expected output:** all practices report `"2.1"` (or latest agreed version).

**If divergence found:** escalate to Admiral via Zone 2 (cross-practice coordination required).

---

## ACAT dimensions.yaml Versioning

### Frozen at Phase 1b (v5.4)

The ACAT corpus was locked at the end of Phase 1b to ensure **measurement stability** during Phase 2–3:

- Version: 5.4
- Locked: 2026-08-31
- Frozen dimensions: 15 (see Phase 1b UI Integration report)
- No modifications permitted until Phase 3 opens (2026-10-01 earliest)

### Backward Compatibility: Not Applicable

Phase 1 measured v4.0 corpus. Phase 1b validated v5.4. There is **no bridge** — Phase 1 and 1b measurements are not directly comparable due to corpus drift.

**Use case:** Comparing within Phase 1b (Session A vs Session B)? Use v5.4 for both. Comparing Phase 1 → 1b? Use separate statistical analysis (Cronbach's α drift, RMSE, effect size).

### Migration for Phase 2–3 (Future)

When Phase 3 begins:

1. Admiral ratifies Phase 3 corpus version (v5.5 or later, per research review)
2. All practices deploy new dimensions.yaml
3. New measurements anchor to v5.5
4. Phase 1b data stays frozen under v5.4 (historical record)

---

## Governance Specs Versioning

### Versions in Use

| Document | Version | Status | Compat |
|----------|---------|--------|--------|
| AUTHORITY_MAPPING_Z3_EMPIRICA_V1.md | 1.0 | DRAFT | N/A (first release) |
| AUTHORITY_MATRIX.yaml | 1.0 | DRAFT | N/A (first release) |
| ESCALATION_PROTOCOL.md | 1.0 | DRAFT | N/A (first release) |

### Breaking Changes: How to Signal Them

When Admiral needs to change a governance spec (e.g., adding a 7th escalation trigger, or redefining Zone 2 approval latency):

1. **Version increment**: X.Y → X.(Y+1) for compatible changes, (X+1).0 for breaking
2. **Authority document**: File Zone 2 RFC via `@docs/AUTHORITY_MAPPING_Z3_EMPIRICA_V1.md` § Authority Delegation
3. **Migration path**: In the RFC, specify:
   - When the new version takes effect
   - How existing open proposals are handled (grandfather clause, or restart?)
   - What retraining / re-broadcasting is needed

**Example:**

```markdown
## Version 1.1 Proposal (Breaking: adds Trigger 7)

**Current:** ESCALATION_PROTOCOL v1.0 with 6 triggers  
**Proposed:** v1.1 with 7 triggers (new: "Mesh consensus failure")  

**Backward compat:** NONE — v1.0 → v1.1 is breaking
- Practices running v1.0 MUST upgrade to v1.1 by [DATE]
- Proposals in flight: all escalate back to Zone 1 on deployment (re-evaluate under new rules)

**Ratification:** Admiral (Carly) approves this breaking change or requests alternatives
```

---

## Calibration Vectors: Immutable (for now)

The 13-vector set (`know`, `uncertainty`, `context`, `clarity`, `coherence`, `signal`, `density`, `state`, `change`, `completion`, `impact`, `do`, `engagement`) is **foundational to empirica's epistemic model** and is not subject to schema versioning.

**Changes to the vector set are ARCHITECTURAL decisions**, not schema updates:

- Require Admiral approval via Zone 2 RFC
- Require full retraining of the Sentinel
- Require re-measurement of all prior sessions (calibration re-anchor)

---

## Detection & Enforcement Points

### CI/CD Gate: schema-check.py

When a PR is submitted that modifies `.empirica/project.yaml`:

```bash
python scripts/schema-check.py project.yaml
# → Validates: version field, required fields, enum values, defaults
# → Returns: PASS | WARN (deprecation) | FAIL (breaking change)
```

**Result handling:**

- PASS: PR proceeds
- WARN: PR proceeds with reviewer comment ("uses deprecated v1.8; migrate to v2.1 by X")
- FAIL: PR blocked ("v1.5 schema no longer supported")

### empirica CLI: version-check

When running `empirica check-submit` with a POSTFLIGHT:

```bash
empirica postflight-submit - << EOF
{ "vectors": {...}, "project_schema_version": "2.1" }
EOF
```

CLI validates:

```python
if project_schema_version < min_supported_version:
  raise SchemaError(f"project.yaml v{version} is EOL. Minimum: v{min_supported}")
```

### Sentinel: Vector Validation

When vectors are logged, Sentinel checks:

```python
if vector_set != expected_vector_set:
  log_error("vector_set_mismatch", expected=expected, got=vector_set)
  # Calibration proceeds, but grounded=false (ungrounded measurement)
```

---

## Upgrade Procedure: project.yaml v2.0 → v2.1

**When:** 2026-09-15 (target)  
**Who:** Each practice owner (or Admiral for critical practices)  
**Authority:** Zone 2 (Admiral approval not needed for schema updates to non-governance files; approval only for governance-spec changes)

### Steps

1. Read new defaults from SCHEMA_VERSIONING_STRATEGY.md (this file)
2. Backup current project.yaml: `git checkout project.yaml`
3. Merge new v2.1 schema (empirica CLI auto-migrates via a tool):
   ```bash
   empirica schema-upgrade project.yaml --from 2.0 --to 2.1
   # → Creates project.yaml with new calibration_weights section + defaults
   ```
4. Review diff: `git diff project.yaml`
5. Commit: `git commit -m "upgrade: project.yaml v2.0 → v2.1 (calibration_weights defaults)"`
6. Push and verify CI passes

---

## Deprecation Schedule

| Version | Support Until | Action |
|---------|---|---|
| project.yaml v1.0–1.5 | 2026-10-15 | MUST upgrade to v2.0 by this date |
| project.yaml v2.0 | 2027-01-15 | SHOULD upgrade to v2.1 by this date (v2.0 still accepted) |
| ACAT dimensions v4.0 | 2026-09-30 | Phase 1 historical record only; Phase 2+ uses v5.4+ |

---

## Conformance Checklist (M2 Rank 1)

- [ ] All 6 practices running project.yaml v2.0 or v2.1 (verified by audit in Step 2)
- [ ] schema-check.py integrated into CI pipeline (enforcement point 1/3)
- [ ] empirica CLI version check active (enforcement point 2/3)
- [ ] Sentinel vector validation enabled (enforcement point 3/3)
- [ ] ACAT dimensions v5.4 frozen + documented
- [ ] Backward compat rules documented (this file, § project.yaml Versioning)
- [ ] Deprecation schedule published (this file, § Deprecation Schedule)
- [ ] Admiral ratifies schema versioning strategy (POSTFLIGHT gate)

---

## Ratification & Next Steps

Once Admiral signs off (M2 Rank 1 completion), schema versioning becomes **enforceable**:

- CI gates block non-conformant PRs
- empirica CLI rejects EOL schemas
- Sentinel flags ungrounded measurements

M2 Rank 2 (State Machine Harmonization) will build on this schema foundation to align ACAT phases ↔ charter gates.

---

**Status:** ✅ SCHEMA VERSIONING STRATEGY COMPLETE (M2 T5)  
**Next:** Governance Document Linking (Step 6) + Cross-Practice Verification (Step 7)  
**Ratification:** Pending Admiral sign-off  

