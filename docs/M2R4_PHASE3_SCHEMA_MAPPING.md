# M2R4 Phase 3: project.yaml v2.0 → v3.0 Migration Mapping

**Document ID:** M2R4-PHASE3-MAPPING-2026-08-11  
**Prepared by:** Claude (M2R4 Phase 3 Task 1)  
**Based on:** M2R4_PHASE2_SCHEMA_DESIGN_SPEC.md (Admiral-approved)  
**Status:** READY FOR MIGRATION SCRIPT IMPLEMENTATION

---

## Overview

This document maps the current v2.0 project.yaml field ordering to the v3.0 target structure with alphabetical ordering within logical sections. The migration is **semantic-preserving** — no data transformation, only field reordering and version bump.

---

## v2.0 Current Structure (Observed from empirica-autonomy project.yaml)

**Current field order (non-deterministic, varies by practice):**

```yaml
version: '2.0'
name: <str>
description: <str>
project_id: <uuid>
ai_id: <str>
type: <str>
domain: <str>
org_id: <str>
tenant_slug: <str>
mesh_id_prefix: <str>
canonical_seat: <str>
classification: <str>
status: <str>
evidence_profile: <str>
languages: <list>
tags: <list>
created_at: <date>
created_by: <str>
contacts: <list>
engagements: <list>
edges: <list>
beads: <dict>
subjects: <dict>
auto_detect: <dict>
domain_config: <dict>
calibration_weights: <dict>
```

**Characteristics:**
- Version explicitly set to "2.0"
- Fields appear in ad-hoc order (not alphabetical)
- No logical grouping/sectioning
- All 25 fields present (no additions/removals required)

---

## v3.0 Target Structure (Alphabetical Ordering)

**Target structure from M2R4_PHASE2_SCHEMA_DESIGN_SPEC (DM5):**

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

**Characteristics:**
- Version bumped to "3.0" (string format, consistent with Admiral DM5)
- Fields grouped into 4 logical sections with section comments
- Within each section, fields are alphabetically ordered
- All 25 fields preserved (no semantic change)
- Type clarifications: `<bool>` for binary, `<dict>` for structured, `<list>` for arrays

---

## Field-by-Field Mapping

### Section 1: Metadata (6 fields)

| v2.0 Position | Field | v3.0 Position | Notes |
|---|---|---|---|
| 2 | `name` | Configuration (T6) | Moved from top-level to Configuration section, alphabetically ordered |
| 3 | `description` | Metadata (M3) | Moved from top-level to Metadata section, alphabetically ordered |
| 7 | `ai_id` | Metadata (M1) | Core identity field, elevated to Metadata section |
| 8 | `project_id` | Configuration (C11) | Moved to Configuration section |
| 11 | `canonical_seat` | Metadata (M2) | Authority identifier, grouped with Metadata |
| 14 | `classification` | Metadata (M3) | Access level, grouped with Metadata |
| 17 | `created_at` | Metadata (M4) | Creation timestamp, grouped with Metadata |
| 18 | `created_by` | Metadata (M5) | Audit trail, grouped with Metadata |

### Section 2: Organization & Authority (3 fields)

| v2.0 Position | Field | v3.0 Position | Notes |
|---|---|---|---|
| 9 | `org_id` | Org & Authority (O1) | Org scope, elevated to dedicated section |
| 10 | `tenant_slug` | Org & Authority (O2) | Tenant scope, grouped with org |
| 6 | `type` | Org & Authority (O3) | Entity type, grouped with org scope |

### Section 3: Configuration (15 fields)

| v2.0 Position | Field | v3.0 Position | Notes |
|---|---|---|---|
| 13 | `status` | Configuration (C10) | Operational status, moved to Configuration |
| 15 | `evidence_profile` | Configuration (C7) | Calibration profile, moved to Configuration |
| 12 | `mesh_id_prefix` | Configuration (C9) | Mesh addressing, moved to Configuration |
| 16 | `languages` | Configuration (C8) | Supported languages, grouped in Configuration |
| 19 | `tags` | Configuration (C14) | Metadata tags, grouped in Configuration |
| 21 | `subjects` | Configuration (C13) | Domain subjects, grouped in Configuration |
| 22 | `auto_detect` | Configuration (C1) | Auto-discovery flag, alphabetically first in Configuration |
| 23 | `domain_config` | Configuration (C5) | Domain-specific config, grouped in Configuration |
| 5 | `domain` | Configuration (C4) | Domain classification, moved to Configuration section |
| 24 | `calibration_weights` | Configuration (C2) | Calibration params, grouped in Configuration |
| 20 | `contacts` | Configuration (C3) | Contact list, grouped in Configuration |
| 1 | `engagements` | Configuration (C6) | Engagement list, grouped in Configuration |
| — | `name` | Configuration (C9) | From top-level, moved to Configuration |
| 4 | `project_id` | Configuration (C11) | From top-level, moved to Configuration |

### Section 4: Relationships (2 fields)

| v2.0 Position | Field | v3.0 Position | Notes |
|---|---|---|---|
| 24 | `beads` | Relationships (R1) | First alphabetically in Relationships section |
| 21 | `edges` | Relationships (R2) | Relationship edges, grouped in Relationships section |

---

## Version Bump Rule

**Field:** `version`  
**v2.0 value:** `'2.0'` (string with leading quote)  
**v3.0 value:** `"3.0"` (string, YAML-safe quote style)  
**Migration:** Replace `version: '2.0'` with `version: "3.0"` on all files

---

## Field Type Clarifications (v3.0)

The spec document clarifies expected types for v3.0 validation:

| Field | v3.0 Type | Notes |
|---|---|---|
| `auto_detect` | bool | Binary flag, not dict with `enabled` subkey |
| `beads` | list | Array of bead identifiers, not dict |
| `calibration_weights` | dict | Nested dict (noetic/praxic sub-dicts) |
| `contacts` | list | Array of contact identifiers |
| `created_at` | datetime | ISO 8601 format (string) |
| `created_by` | str | Identifier or email |
| `domain_config` | dict | Domain-specific settings |
| `engagements` | list | Array of engagement identifiers |
| `evidence_profile` | dict | Profile config (structure TBD by domain) |
| `languages` | list | Array of language codes |
| `subjects` | list | Array of subject tags (changed from dict → list) |

**Note on `subjects`:** Current v2.0 has `subjects: {}` (empty dict). v3.0 changes to `subjects: []` (list). Migration script must convert empty dict to empty list.

---

## Alphabetical Ordering Rules

### Rule 1: Case-Sensitive ASCII Sort

- All fields within a section sort alphabetically (ASCII/Unicode code point order)
- Capital letters sort before lowercase (A-Z, then a-z)
- Example: `ai_id` < `canonical_seat` < `classification`

### Rule 2: Within-Section Strictness

- No field reordering across sections
- Sections must appear in this order: Metadata → Org & Authority → Configuration → Relationships
- Section comments (# -- Section Name --) are not sortable, treated as structural

### Rule 3: No Arbitrary Grouping

- Do NOT add blank lines or sub-comments within sections
- YAML structure must be flat within each section (no nested grouping)
- One comment line per section, immediately before the first field

---

## Migration Validation Checklist

**Pre-Migration (data integrity):**
- [ ] Verify all 25 fields present in v2.0 YAML
- [ ] Check `version` field exists and equals '2.0' or "2.0"
- [ ] Validate no extra undocumented fields
- [ ] Confirm all required fields have non-null values

**Post-Migration (structure validation):**
- [ ] Version field changed to "3.0"
- [ ] All 25 fields present in v3.0 YAML
- [ ] Fields appear in correct section order
- [ ] Fields within each section are alphabetically ordered
- [ ] No extra fields added (except version bump)
- [ ] No data values changed (semantic preservation)
- [ ] YAML is valid and parseable
- [ ] `subjects` dict → list conversion complete (if applicable)

---

## Known Edge Cases

### Case 1: Practices with Custom Fields

**Problem:** Some practices may have added extra fields beyond the 25 canonical ones.

**Solution:** Migration script will:
1. Extract all extra fields during migration
2. Log them to `.empirica/migration.log` with WARNING level
3. Preserve extra fields at end of v3.0 YAML (un-alphabetized)
4. Require manual Admiral review before committing

### Case 2: Inline Structures (calibration_weights)

**Problem:** `calibration_weights` is a nested dict with noetic/praxic sub-dicts.

**Solution:**
- Do NOT sort sub-dict keys (preserve internal structure)
- Sort only top-level fields
- Example: preserve `noetic: {know: 1.0, context: 0.8, ...}` order

### Case 3: Empty or Null Fields

**Problem:** v2.0 may have empty lists/dicts (e.g., `tags: []`, `engagements: []`).

**Solution:** Preserve empty structures as-is during migration. No conversion needed.

---

## Example: Full Migration

### Before (v2.0)

```yaml
version: '2.0'
name: empirica-autonomy
description: "empirica-foundation builder practice..."
project_id: 492482dc-8156-40cd-a110-ce7081212215
ai_id: empirica-autonomy
type: software
domain: ai/autonomy
org_id: org-empirica-foundation
tenant_slug: carly
mesh_id_prefix: empirica-foundation.carly
canonical_seat: empirica-foundation.carly.empirica-autonomy
classification: internal
status: active
evidence_profile: code
languages: []
tags: []
created_at: '2026-06-26'
created_by: andersonfamily
contacts: []
engagements: []
edges: []
beads:
  default_enabled: false
subjects: {}
auto_detect:
  enabled: true
  method: path_match
domain_config: {}
calibration_weights:
  noetic:
    know: 1.0
    context: 0.8
    signal: 0.9
  praxic:
    know: 1.0
    completion: 1.0
    context: 1.0
```

### After (v3.0 - Alphabetically Ordered)

```yaml
version: "3.0"

# -- Metadata --
ai_id: empirica-autonomy
canonical_seat: empirica-foundation.carly.empirica-autonomy
classification: internal
created_at: '2026-06-26'
created_by: andersonfamily
description: "empirica-foundation builder practice..."

# -- Organization & Authority --
org_id: org-empirica-foundation
tenant_slug: carly
type: software

# -- Configuration --
auto_detect:
  enabled: true
  method: path_match
calibration_weights:
  noetic:
    know: 1.0
    context: 0.8
    signal: 0.9
  praxic:
    know: 1.0
    completion: 1.0
    context: 1.0
contacts: []
domain: ai/autonomy
domain_config: {}
engagements: []
evidence_profile: code
languages: []
mesh_id_prefix: empirica-foundation.carly
name: empirica-autonomy
project_id: 492482dc-8156-40cd-a110-ce7081212215
status: active
subjects: []
tags: []

# -- Relationships --
beads:
  default_enabled: false
edges: []
```

**Differences:**
- Version: `'2.0'` → `"3.0"`
- Fields reordered into 4 sections, alphabetically within each
- `subjects: {}` → `subjects: []` (dict to list)
- Semantic data unchanged (same values, just different positions)

---

## Summary: Mapping Complete ✓

**Deliverables for T3.1:**
1. ✓ v2.0 structure documented (25 fields, non-alphabetical)
2. ✓ v3.0 target structure documented (4 sections, alphabetical within each)
3. ✓ Field-by-field mapping (all 25 fields mapped to new positions)
4. ✓ Alphabetical ordering rules (case-sensitive ASCII sort)
5. ✓ Migration validation checklist (pre/post verification steps)
6. ✓ Edge case handling (custom fields, nested structures, empty fields)
7. ✓ Full example (before/after migration)

**Status:** Ready for T3.2 (Build Migration Script)

---

**Generated:** 2026-08-11 (T3.1 completion)  
**Task ID:** e1ec1844-5f55-4311-b5bc-253615b98ac4 (T3.1: Read spec + document mapping)  
**Evidence:** This document (M2R4_PHASE3_SCHEMA_MAPPING.md)
