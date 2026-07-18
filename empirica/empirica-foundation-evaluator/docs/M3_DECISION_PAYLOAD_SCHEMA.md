# M3 Decision Payload Schema (Design)

**Purpose:** Define the exact structure of decisions that CNS dispatches to all repos via `repository_dispatch` events.

**Versioning:** Each decision payload includes `schema_version` field. Repos must validate incoming payloads against their local schema.

---

## Decision Types (Corresponding to M2 Ranks 1-6)

| M2 Rank | Decision Type | Triggered By | Affects |
|---------|---------------|--------------|---------|
| Rank 1 | `authority_boundary_change` | Authority matrix updates | CLAUDE.md zone delegation sections |
| Rank 2 | `state_machine_gate_update` | ACAT phase ↔ charter gate mapping | acat_contracts/gates_*.json |
| Rank 3 | `config_standard_update` | project.yaml template changes | .empirica/project.yaml |
| Rank 4 | `dependency_version_pin` | Dependency coordination matrix | requirements.txt, package.json, etc. |
| Rank 5 | `naming_versioning_standard` | SemVer / file naming rules | validation rules + tags |
| Rank 6 | `schema_lock_update` | ACAT schema version lock | acat_contracts/decisions.schema.json |

---

## Canonical Decision Envelope Structure

```json
{
  "envelope_version": "1.0",
  "decision_id": "D-YYMMDD-NNN",
  "decision_type": "authority_boundary_change | state_machine_gate_update | config_standard_update | dependency_version_pin | naming_versioning_standard | schema_lock_update",
  
  "decision_body": {
    "type": "string (one of decision_type values)",
    "description": "string (human-readable summary)",
    "change": "string (specific change being made)",
    "target_practices": ["practice-1", "practice-2", ...],
    "effective_date": "2026-07-21T00:00:00Z (ISO8601)",
    "rollback_clause": "string (conditions for reverting this decision)",
    "metadata": {
      "priority": "CRITICAL | STANDARD | OPTIONAL",
      "created_by": "empirica-foundation-evaluator",
      "created_at": "2026-07-19T14:23:00Z",
      "links": ["https://github.com/.../docs/...", ...]
    }
  },
  
  "schema_version": "acat_contracts/decisions_v1.schema.json",
  "decision_checksum": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "admiral_signature": "-----BEGIN SIGNATURE-----\n[RSA-2048 signature]\n-----END SIGNATURE-----",
  
  "dispatch_metadata": {
    "target_repos": [
      "humanaios-ui/operations",
      "humanaios-ui/lasting-light-ai",
      "humanaios-ui/humanaios",
      "LastingLightAI/HAIOSCC"
    ],
    "rollback_path": null,
    "expected_behavior": "auto-apply | manual-review | hold-pending-resolution"
  }
}
```

---

## Decision Body Schema by Type

### Type 1: authority_boundary_change

```json
{
  "type": "authority_boundary_change",
  "description": "Expand Zone 2 authority from Admiral-only to practice owners (local decisions)",
  "change": "authority_owner_expansion: admiral_only → practice_owners_with_admiral_oversight",
  "target_practices": ["empirica-autonomy", "empirica-outreach", "empirica-mesh-support"],
  "effective_date": "2026-07-21T00:00:00Z",
  "rollback_clause": "If escalation_rate > 30% in first 7 days, revert to Admiral-only",
  "metadata": {
    "priority": "CRITICAL",
    "authority_mapping_ref": "AUTHORITY_MATRIX.yaml section 2.1",
    "zone_affected": [1, 2, 3],
    "approval_body": "Admiral + practice owners"
  }
}
```

**Expected behavior on repo:** AUTO-APPLY
- Repo updates CLAUDE.md Authority Layer section
- Repo confirms Zone 2 delegation rules in CLAUDE.md
- Repo acknowledges with `status=APPLIED, applied_at_commit=<sha>`

---

### Type 2: state_machine_gate_update

```json
{
  "type": "state_machine_gate_update",
  "description": "Update ACAT Phase 3 gate mapping for charter milestone M2.5",
  "change": "acat_phase_3_gate_threshold: 0.7 → 0.75",
  "target_practices": ["all"],
  "effective_date": "2026-07-21T00:00:00Z",
  "rollback_clause": "Revert if Phase 3 assessment rate drops >20%",
  "metadata": {
    "priority": "STANDARD",
    "acat_phase": 3,
    "gate_dimension": "calibration_readiness",
    "gate_file": "acat_contracts/gates_phase3.json",
    "old_threshold": 0.70,
    "new_threshold": 0.75
  }
}
```

**Expected behavior on repo:** AUTO-APPLY
- Repo updates acat_contracts/gates_phase3.json
- Repo confirms validation: Phase 3 submissions now require >= 0.75 calibration

---

### Type 3: config_standard_update

```json
{
  "type": "config_standard_update",
  "description": "Standardize project.yaml ai_id format across foundation",
  "change": "project_yaml_template_v1.2 → v1.3 (hyphen canonical form)",
  "target_practices": ["all"],
  "effective_date": "2026-07-21T00:00:00Z",
  "rollback_clause": "Maintain backward compatibility; old format still accepted",
  "metadata": {
    "priority": "STANDARD",
    "template_ref": "https://github.com/.../empirica/project.yaml.template",
    "old_ai_id_format": "empirica_foundation_evaluator (underscore)",
    "new_ai_id_format": "empirica-foundation-evaluator (hyphen, canonical)",
    "config_file": ".empirica/project.yaml"
  }
}
```

**Expected behavior on repo:** MANUAL-REVIEW or AUTO-APPLY (depending on repo setup)
- Repo validates project.yaml against new schema
- Repo either auto-updates or flags for manual review
- Repo confirms with updated project.yaml committed

---

### Type 4: dependency_version_pin

```json
{
  "type": "dependency_version_pin",
  "description": "Pin acat_contracts schema library to v5.4 (security update)",
  "change": "acat_contracts_schema: >=5.0 → ==5.4.0",
  "target_practices": ["all"],
  "effective_date": "2026-07-21T00:00:00Z",
  "rollback_clause": "If v5.4 breaks backward compat, revert to v5.3.1",
  "metadata": {
    "priority": "CRITICAL",
    "package_manager": "pip | npm | cargo (repo-specific)",
    "old_version_spec": ">=5.0,<6.0",
    "new_version_spec": "==5.4.0",
    "reason": "Security patch: CVE-2026-XXXXX",
    "affected_files": ["requirements.txt", "package.json", "Cargo.toml"]
  }
}
```

**Expected behavior on repo:** AUTO-APPLY with CREATE-PR (not direct commit)
- Repo creates a PR with pinned version
- Repo runs CI to confirm compatibility
- Human maintainer merges the PR
- Repo acknowledges with PR link in ACK

---

### Type 5: naming_versioning_standard

```json
{
  "type": "naming_versioning_standard",
  "description": "Enforce SemVer + hyphen-separated file naming across mesh",
  "change": "naming_convention_v0 → v1 (empirica-foundation-evaluator style)",
  "target_practices": ["all"],
  "effective_date": "2026-07-21T00:00:00Z",
  "rollback_clause": "Grandfathering: old files allowed but new files must follow v1",
  "metadata": {
    "priority": "OPTIONAL",
    "naming_rules": {
      "repo_name": "empirica-foundation-evaluator (hyphens, lowercase)",
      "file_name": "M3_5_RESILIENCE_SPEC.md (underscore between components)",
      "doc_version": "v1.0-RATIFIED (semver + status tag)",
      "commit_style": "docs: component brief-description"
    },
    "validation_rules": "https://github.com/.../docs/NAMING_STANDARD_V1.md"
  }
}
```

**Expected behavior on repo:** HOLD-PENDING-RESOLUTION
- Repo logs decision but does NOT rename existing files
- Repo applies naming standard to NEW files going forward
- Repo flags if existing files violate standard (manual remediation)

---

### Type 6: schema_lock_update

```json
{
  "type": "schema_lock_update",
  "description": "Lock ACAT schema to v5.4 (no breaking changes until M4 release)",
  "change": "acat_assessments.schema.json: MUTABLE → LOCKED_TO_V5.4",
  "target_practices": ["all"],
  "effective_date": "2026-07-21T00:00:00Z",
  "rollback_clause": "Schema remains locked until M4 release decision",
  "metadata": {
    "priority": "CRITICAL",
    "schema_file": "acat_contracts/assessments.schema.json",
    "locked_version": "5.4",
    "reason": "Mesh harmonization requires schema stability during M2-M3",
    "unlock_condition": "M4 release approved by Admiral + empirica-foundation consensus"
  }
}
```

**Expected behavior on repo:** AUTO-APPLY (read-only enforcement)
- Repo validates acat_assessments.schema.json == v5.4
- Repo refuses to accept submissions with different schema version
- Repo logs schema version mismatch attempts (for observability)

---

## Query Schema Reference

Repos will query decisions like this:

```json
{
  "decision_id": "D-0719-042",
  "status": "APPLIED | SCHEMA_MISMATCH | SIGNATURE_FAILED | HELD_PENDING_RESOLUTION",
  "applied_at_commit": "7a3f2c1e...",
  "applied_at_timestamp": "2026-07-19T14:30:00Z",
  "repo": "humanaios-ui/humanaios",
  "decision_body": { ... },
  "ack_payload": {
    "status": "APPLIED",
    "message": "Decision applied successfully",
    "repo_state": "main branch at commit 7a3f2c1e",
    "files_modified": ["CLAUDE.md", ".empirica/project.yaml"],
    "validation_passed": true
  }
}
```

---

## Versioning Rules

**Backward Compatibility:**
- `schema_version` field is immutable per decision
- Repo receiving older schema_version should still process (graceful degradation)
- If repo doesn't understand a schema_version, escalate to Admiral

**Forward Compatibility:**
- Schema v1.0 can accept new optional fields in decision_body (ignore unknown fields)
- Required fields are locked per version (no surprises)

**Schema Lock (M2-M3 Phase):**
- ACAT schema locked to v5.4 via Type 6 decisions
- No schema changes permitted until M4 release

---

## Payload Size and Delivery Guarantees

**Size constraints:**
- Single decision: < 50 KB (keep crypto signature small)
- Batch of 10 decisions: < 200 KB (webhook timeout safe)
- Over-size decision: escalate as OVERSIZED, retry with smaller scope

**Delivery guarantees:**
- At-least-once delivery (repo receives decision, even if network glitch)
- Idempotent application (applying decision twice = same state)
- Atomic apply (decision fully applies or not at all, no partial state)

---

## Success Criteria for Decision Payload Design

- ✅ All M2 Rank 1-6 decision types can be represented
- ✅ Admiral signature + checksum validate integrity
- ✅ Backward-compatible schema versioning
- ✅ Repo can query applied decisions and state
- ✅ Payload fits in GitHub webhook (< 200 KB for 10 decisions)
- ✅ ACK message includes repo commit hash (proof of application)
- ✅ Rollback clause documented for each decision
- ✅ Integration point: repo updates correct files (CLAUDE.md, project.yaml, acat_contracts/*, etc.)

