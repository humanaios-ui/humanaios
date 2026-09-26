# M2 Rank 4: Schemas Harmonization RFC

**Document ID:** M2R4-RFC-2026-07-23-SCHEMAS  
**Status:** ⏳ AWAITING ADMIRAL APPROVAL (Post-Rank 3)  
**Submitted by:** empirica-foundation-evaluator (spec-prep fork)  
**Submission Date:** 2026-07-23  
**Target Decision Date:** 2026-07-29 (after Rank 3 completes)  
**Audience:** Admiral (Carly), M2 Rank 4 executor, empirica infrastructure team

---

## Executive Summary

Configuration and metadata schemas across the foundation (project.yaml, CLAUDE.md, AUTHORITY_MATRIX.yaml, .empirica/config.yaml) lack a canonical definition, making validation tooling impossible and cross-practice scripts fragile. This RFC proposes JSON Schema definitions for all foundational schemas, plus validation tooling and a "lint" command to catch schema violations early. Harmonized schemas enable automated rollout verification (M2 Phase 4) and future tooling that depends on reliable config structure.

---

## Current State: What's Broken

### Schema Variations

**project.yaml**

Current file shows version `2.0`, but variations exist:
- Some repos: missing `canonical_seat` field (causes routing failures)
- Some repos: `calibration_weights` structure differs (noetic vs praxic keys optional vs required)
- Some repos: `metadata` field varies (some use YAML, some JSON strings)

**Example inconsistencies:**

```yaml
# Style A (empirica-foundation-evaluator)
calibration_weights:
  noetic:
    know: 1.0
    context: 0.8

# Style B (flta-app-empirica)
calibration_weights:
  know: 1.0
  context: 0.8
  # (missing noetic/praxic tier structure)

# Style C (empirica-autonomy)
calibration_weights: null
  # (not set; uses defaults, but tooling can't verify)
```

### CLAUDE.md Variations

Authority sections have no schema:
- Some use `Decision-maker: Carly` as string
- Some use `decision_maker: { name: "Carly", tier: "admiral" }` as object
- Some missing sections entirely

**Impact:** Authority matrix queries can't reliably extract decision-makers.

### AUTHORITY_MATRIX.yaml

No schema validation; manually edited. Possible errors:
- Typo in `escalation_target` → breaks escalation logic
- Missing `zone_1` for a new issue type → incomplete governance
- Inconsistent field names across issue types

### .empirica/config.yaml

No schema; varies per practice. Content unclear (sentinel config? runtime config? both?).

---

## Proposed Canonical Schemas

### 1. project.yaml Schema (JSON Schema)

**File:** `schemas/project-v2.0.schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "empirica Project Configuration (v2.0)",
  "type": "object",
  "required": ["version", "name", "ai_id", "type", "status"],
  "properties": {
    "version": {
      "type": "string",
      "enum": ["2.0"],
      "description": "Schema version"
    },
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 128,
      "description": "Human-readable project name"
    },
    "ai_id": {
      "type": "string",
      "pattern": "^[a-z0-9-]+$",
      "description": "Canonical AI ID (ai_id from canonical seat)"
    },
    "canonical_seat": {
      "type": "string",
      "pattern": "^[a-z0-9-]+\\.[a-z0-9-]+\\.[a-z0-9-]+$",
      "description": "Full 3-form: org.tenant.project (required for mesh routing)"
    },
    "type": {
      "type": "string",
      "enum": ["software", "operations", "research"],
      "description": "Project type"
    },
    "status": {
      "type": "string",
      "enum": ["active", "archived", "planned"],
      "description": "Project status (from M2 Rank 2 unified model)"
    },
    "calibration_weights": {
      "type": "object",
      "properties": {
        "noetic": {
          "type": "object",
          "properties": {
            "know": { "type": "number", "minimum": 0, "maximum": 1 },
            "do": { "type": "number", "minimum": 0, "maximum": 1 },
            "context": { "type": "number", "minimum": 0, "maximum": 1 }
            # ... (all 13 vectors)
          },
          "additionalProperties": false
        },
        "praxic": {
          "type": "object",
          "properties": {
            # ... (same as noetic)
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false,
      "description": "Calibration weight overrides per phase"
    }
  },
  "additionalProperties": true  # Allow extensions
}
```

### 2. CLAUDE.md Authority Section Schema

**File:** `schemas/claude-md-authority-v1.0.schema.json`

Define the structure for the "Authority Layer — Governance & Zone Mapping" section:

```json
{
  "title": "CLAUDE.md Authority Layer",
  "type": "object",
  "required": ["zone_scope"],
  "properties": {
    "zone_scope": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["zone", "decision_maker", "approval_rule"],
        "properties": {
          "zone": { "enum": ["1", "2", "3"] },
          "decision_maker": { "type": "string" },
          "approval_rule": { "type": "string" },
          "escalation": { "type": "string" }
        }
      }
    },
    "governance_documents": {
      "type": "array",
      "items": { "type": "string" },
      "description": "File paths to governance docs (@docs/...)"
    }
  }
}
```

### 3. AUTHORITY_MATRIX.yaml Schema

**File:** `schemas/authority-matrix-v1.0.schema.json`

Validate the structure of the authority matrix:

```json
{
  "title": "Authority Matrix",
  "type": "object",
  "required": ["matrix"],
  "properties": {
    "matrix": {
      "type": "object",
      "required": ["issue_type"],
      "properties": {
        "issue_type": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["name", "zone_1", "zone_2", "zone_3"],
            "properties": {
              "name": { "type": "string" },
              "zone_1": {
                "type": "object",
                "required": ["decision_maker", "approval_rule", "evidence_required", "escalation_trigger", "escalation_target"]
              },
              "zone_2": { /* same structure as zone_1 */ },
              "zone_3": { /* same structure as zone_1 */ }
            }
          }
        }
      }
    }
  }
}
```

---

## Validation Tooling

### 1. CLI Validator: `empirica lint`

```bash
$ empirica lint .empirica/project.yaml
✅ project.yaml valid (schema v2.0)
  - canonical_seat: empirica-foundation.carly.empirica-foundation-evaluator ✓
  - calibration_weights.noetic: all 13 vectors present ✓
  - status: active (valid enum) ✓

$ empirica lint CLAUDE.md
✅ CLAUDE.md valid
  - Authority Layer section found ✓
  - All 3 zones defined ✓
  - governance_documents resolve ✓ ✓ ✓

$ empirica lint docs/AUTHORITY_MATRIX.yaml
⚠️  AUTHORITY_MATRIX.yaml has warnings
  - issue_type "code_commit" zone_2 missing "approval_rule" field
  - escalation_trigger in zone_3 references undefined state "suspicious" (hint: use "in_progress")

$ empirica lint --all
📊 Foundation schema audit (40 repos)
  ✅ 38 repos fully compliant
  ⚠️  2 repos have warnings (see above)
```

### 2. Pre-Commit Hook

**File:** `.empirica/hooks/pre-commit-schema-lint.sh`

```bash
#!/bin/bash
# Hook: Prevent commits with schema violations

files_changed=$(git diff --cached --name-only)
for file in $files_changed; do
  if [[ $file == *"project.yaml" ]] || [[ $file == "CLAUDE.md" ]]; then
    if ! empirica lint "$file"; then
      echo "❌ Commit blocked: schema violations in $file"
      exit 1
    fi
  fi
done
```

### 3. GitHub Actions Workflow

**File:** `.github/workflows/schema-validation.yml`

```yaml
name: Schema Validation
on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Lint all schemas
        run: empirica lint --all
      - name: Fail if warnings in PRs
        if: github.event_name == 'pull_request'
        run: |
          if empirica lint --all 2>&1 | grep -q "⚠️"; then
            exit 1
          fi
```

---

## Migration Path

### Phase 1: Define & Publish Schemas (1 day)

Create JSON Schema files and publish to a canonical location:

```
schemas/
  ├── project-v2.0.schema.json
  ├── claude-md-authority-v1.0.schema.json
  ├── authority-matrix-v1.0.schema.json
  └── config-v1.0.schema.json
```

**Publish to:** GitHub + documentation site (so every practice can reference).

### Phase 2: Build Validator Tooling (1 day)

Implement `empirica lint` command using `jsonschema` library:

```python
# scripts/lint.py
import jsonschema
import yaml

def lint_project_yaml(path):
  with open(path) as f:
    config = yaml.safe_load(f)
  with open("schemas/project-v2.0.schema.json") as f:
    schema = json.load(f)
  
  try:
    jsonschema.validate(config, schema)
    return (True, "✅ Valid")
  except jsonschema.ValidationError as e:
    return (False, f"❌ {e.message}")
```

### Phase 3: Add Pre-Commit Hook (1 day)

Install the hook in all 40+ repos:

```bash
for repo in $(ls -d practices/*/); do
  cp .empirica/hooks/pre-commit-schema-lint.sh "$repo/.git/hooks/pre-commit"
  chmod +x "$repo/.git/hooks/pre-commit"
done
```

### Phase 4: Audit & Fix Violations (1 day)

Run `empirica lint --all` and fix any violations:

```bash
empirica lint --all > lint_report.json
# Review report, fix each violation per repo
```

### Phase 5: Enable GitHub Actions (1 day)

Deploy schema validation workflows to all repos.

---

## Verification Checklist

- [ ] All schemas defined (project, CLAUDE.md, authority-matrix, config)
- [ ] Schemas published to public location (docs + repo)
- [ ] `empirica lint` command implemented + tested
- [ ] Pre-commit hooks installed in all 40+ repos
- [ ] GitHub Actions workflows deployed
- [ ] Audit complete (lint --all passes for all repos)
- [ ] Schema validation in CI pipeline working
- [ ] Documentation updated (how to use lint, what schemas mean)
- [ ] POSTFLIGHT + grounded calibration submitted

---

## Reversibility

### Full Rollback

If schema validation breaks workflows:
1. Disable pre-commit hook (`rm .git/hooks/pre-commit`)
2. Disable GitHub Actions (set workflow status to `inactive`)
3. Revert schema definitions to prior versions
4. Notify practitioners

**Window:** Reversible immediately (no data changes, only validation rules).

### Gradual Rollout

Deploy validation warnings-only first (doesn't block commits). After 7 days of zero violations, enable hard errors.

---

## Risk Assessment

### Low Risk

- **Validation only** — No behavior changes, just schema enforcement
- **Fully reversible** — Can disable at any time
- **Gradual rollout** — Warnings first, errors later

### Medium Risk

- **May block valid configs** — If schema is overly strict. **Mitigation:** Phase through warnings first; collect feedback.
- **Pre-commit hook overhead** — May slow local commits. **Mitigation:** Validate in background; don't block.

### Monitoring

1. **Hook performance** — Alert if validation takes >5s per commit
2. **CI failures** — Track how many PRs fail schema validation
3. **False positives** — Collect feedback on invalid rejections; refine schema

---

## Timeline

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| P1: Schemas | 1 day | None |
| P2: Tooling | 1 day | P1 complete |
| P3: Hooks | 1 day | P2 complete |
| P4: Audit | 1 day | P3 complete |
| P5: CI/CD | 1 day | P4 complete |
| **Total** | **5 days** | M2 Rank 3 (Registry) should be complete for ordering |

---

## Glossary

| Term | Definition |
|------|-----------|
| **JSON Schema** | Formal specification defining valid structure of a JSON/YAML file |
| **Validation** | Checking a config file against a schema; rejects if structure invalid |
| **Pre-commit Hook** | Git hook that runs before commit; can block commit if validation fails |
| **Lint** | Static analysis tool that checks code/config against rules |
| **Canonical** | Single source-of-truth location for schema definitions |

---

## References

- **Authority:** M2 Rank 1 (Authority System)
- **Registry:** M2 Rank 3 (Registry Harmonization) — registry schema is input
- **State Machines:** M2 Rank 2 (State Machine Harmonization) — states mentioned in schema validation
- **JSON Schema Standard:** https://json-schema.org/draft/2020-12/

---

**Status: ⏳ AWAITING ADMIRAL APPROVAL (blocked by M2 Rank 3 completion)**

This RFC is ready for queue. Once Rank 3 is complete and merged, Rank 4 can begin immediately.
