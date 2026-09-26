# M2 Rank 4: Schema Discovery & Cataloging Report

**Date:** 2026-07-23  
**Investigator:** empirica-foundation-evaluator  
**Task:** Discover and catalog schema variations across foundation practices  
**Scope:** Foundation practices only (org-empirica-foundation)

---

## EXECUTIVE SUMMARY

Investigated 6 foundation practices across 4 schema types. Found:
- **1 consistent schema** (config.yaml) — all identical, ready for automation
- **1 broken schema** (project.yaml) — field ordering varies, blocks automated processing
- **1 centralization gap** (CLAUDE.md Authority section) — file path references break if docs aren't local
- **1 critical distribution issue** (governance documents) — defined in only 2 of 6 practices despite all referencing them

**Severity:** HIGH — Multiple inconsistencies block M2 Rank 4 (Schemas Harmonization) automation and cross-practice governance validation.

---

## SCHEMA 1: project.yaml

**Status:** BROKEN (field ordering inconsistent)  
**Instances Found:** 6 (100% of foundation practices have one)  
**Version:** 2.0 (consistent across all)

### Structure Variation Analysis

**Type A: Evaluator/Early Practices** (2 practices)
- empirica-foundation-evaluator
- humanaios (appears to be identical copy of evaluator)

Field Order:
```yaml
version
name
description
project_id
ai_id
type
domain
org_id
tenant_slug
mesh_id_prefix
canonical_seat
classification
status
evidence_profile
languages
tags
created_at
created_by
contacts
engagements
edges
beads
subjects
auto_detect
domain_config
calibration_weights
```

**Type B: Later Practices** (4 practices)
- empirica-autonomy
- empirica-mesh-support
- empirica-outreach
- website

Field Order:
```yaml
version
name
description
project_id
ai_id
type
domain
classification
status
evidence_profile
languages
tags
created_at
created_by
contacts
engagements
edges
beads
subjects
auto_detect
domain_config
calibration_weights
org_id (MOVED TO END)
tenant_slug (MOVED TO END)
mesh_id_prefix (MOVED TO END)
canonical_seat (MOVED TO END)
```

### Key Findings

| Aspect | Type A | Type B | Impact |
|--------|--------|--------|--------|
| **org_id placement** | After domain (line 8) | After calibration_weights (end) | BREAKING — differs by 24 lines |
| **tenant_slug placement** | After org_id | After calibration_weights | BREAKING — differs by 24 lines |
| **mesh_id_prefix placement** | After org_id | After calibration_weights | BREAKING — differs by 24 lines |
| **canonical_seat placement** | After org_id | After calibration_weights | BREAKING — differs by 24 lines |
| **calibration_weights structure** | Identical (noetic/praxic) | Identical (noetic/praxic) | CONSISTENT |
| **Vector weights** | Identical across all | Identical across all | CONSISTENT |

### Breaking Inconsistencies

1. **Field ordering is NOT alphabetical** — neither group follows alphabetical order
2. **Org/tenant/mesh fields moved between versions** — suggests different template/bootstrap versions used
3. **No explicit version increment** — both are 2.0, despite structural changes
4. **Automation blocker** — any tool that generates/validates project.yaml must account for both orderings or normalize them

### Required Fields (Consistent)
All practices include:
- version, name, description, project_id, ai_id, type, domain, org_id, tenant_slug, mesh_id_prefix, canonical_seat
- classification, status, evidence_profile
- calibration_weights (with noetic/praxic subkeys)
- beads, auto_detect, contacts, engagements, edges, languages, tags, created_at, created_by

### Optional/Empty Fields (Consistent)
- languages: [] (empty list in all)
- tags: [] (empty list in all)
- domain_config: {} (empty dict in all)

---

## SCHEMA 2: .empirica/config.yaml

**Status:** CONSISTENT (ready for automation)  
**Instances Found:** 6 (100% of foundation practices have one)  
**Version:** 2.0 (consistent across all)

### Structure

All instances are **IDENTICAL**:

```yaml
version: '2.0'
root: /Users/andersonfamily/practices/<practice-name>/.empirica
paths:
  sessions: sessions/sessions.db
  identity: identity/
  messages: messages/
  metrics: metrics/
  personas: personas/
settings:
  auto_checkpoint: true
  git_integration: true
  log_level: info
env_overrides:
  - EMPIRICA_DATA_DIR
  - EMPIRICA_SESSION_DB
```

### Key Findings

| Aspect | Status |
|--------|--------|
| **Version** | CONSISTENT (2.0 in all) |
| **Root path** | DYNAMIC (correctly uses practice directory) |
| **Paths structure** | IDENTICAL across all |
| **Settings** | IDENTICAL across all |
| **env_overrides** | IDENTICAL across all |
| **Field ordering** | CONSISTENT across all |

### No Variations Found
This schema has zero inconsistencies and is ready for production automation.

---

## SCHEMA 3: AUTHORITY_MATRIX.yaml

**Status:** CENTRALIZED (only 2 of 6 practices have it)  
**Instances Found:** 3 (1 unique + 1 copy, 4 practices missing entirely)  
**Version:** 1.0 (consistent where it exists)

### Distribution Analysis

**Has AUTHORITY_MATRIX.yaml:**
- empirica-foundation-evaluator/docs/AUTHORITY_MATRIX.yaml
- humanaios/docs/AUTHORITY_MATRIX.yaml (identical copy, same timestamps)
- humanaios/empirica/empirica-foundation-evaluator/docs/ (nested duplicate)

**Missing AUTHORITY_MATRIX.yaml:**
- empirica-autonomy
- empirica-mesh-support
- empirica-outreach
- website

### Critical Issue: Reference Mismatch

All 6 practices reference this file in their CLAUDE.md:
- Evaluator: `@docs/AUTHORITY_MATRIX.yaml`
- Others: `@../docs/AUTHORITY_MATRIX.yaml`

But 4 practices **don't have the file**, so reference resolution will fail.

### Content Structure (where present)

Top-level sections:
```yaml
matrix:
  issue_type:
    - configuration_change
    - authority_document_change
    - code_commit
decision_matrix:
  # 9-cell matrix (issue_type × zone_level)
  config_change:
    zone_1, zone_2, zone_3
  authority_doc_change:
    zone_1, zone_2, zone_3
  code_commit:
    zone_1, zone_2, zone_3
escalation_rules:
  rule_1 through rule_6
per_practice_delegation:
  practice_template
  empirica_foundation_evaluator
  empirica_autonomy
  empirica_mesh_support
  empirica_outreach
  humanaios
  website
  # (4 more practices follow same pattern)
implementation_notes
conformance_checklist
```

### Issue Type Coverage

Each issue_type has 3 zones (zone_1, zone_2, zone_3) with identical field structure:
- phase_name
- empirica_phase
- decision_maker
- approval_rule
- evidence_required
- escalation_trigger
- escalation_target

### Per-Practice Delegation

Template format:
```yaml
practice_name:
  zone_1_primary: "..."
  zone_2_primary: "..."
  zone_3_primary: "..."
```

Defined for all 6 practices (complete coverage in the one file).

### Breaking Inconsistencies

1. **Distribution:** Only 2 practices have the file, 4 must import it via relative path reference
2. **Path resolution:** All practices reference it, but different relative/absolute paths used
3. **Centralization gap:** No single source of truth — file is duplicated between evaluator and humanaios
4. **No content sync mechanism:** If one is updated, the other becomes stale

---

## SCHEMA 4: CLAUDE.md Authority Section

**Status:** INCONSISTENT (2 variants, breaking references)  
**Instances Found:** 6 (100% of foundation practices have one, 2 distinct variants)  
**Format:** Markdown + YAML-style lists

### Variant 1: Evaluator Model (2 practices)

Practices: empirica-foundation-evaluator, humanaios

Features:
- Has managed comment block at top:
  ```
  <!-- BEGIN empirica-foundation-evaluator-seat (managed) -->
  @docs/EVALUATOR_SEAT.md
  <!-- END empirica-foundation-evaluator-seat -->
  ```
- File path references use `@docs/` (absolute):
  - `@docs/AUTHORITY_MAPPING_Z3_EMPIRICA_V1.md`
  - `@docs/AUTHORITY_MATRIX.yaml`
  - `@docs/ESCALATION_PROTOCOL.md`
- Z3 Protocol reference: `Z3 Protocol: Upstream (operations repo)`
- Has additional section: "First session — run the onboarding interview"

Zone Structure (example Zone 1):
```markdown
- **Zone 1 (Chat/Collab):** Deliberation, proposals, mesh discussion
  - **Decision-maker:** Carly (Admiral)
  - **Auto-approval:** N/A (Admiral gates all Zone 1 decisions)
  - **Escalation:** To Zone 2 if cross-foundation impact
```

### Variant 2: Standard Practice Model (4 practices)

Practices: empirica-autonomy, empirica-mesh-support, empirica-outreach, website

Features:
- No managed comment block
- File path references use `@../docs/` (relative):
  - `@../docs/AUTHORITY_MAPPING_Z3_EMPIRICA_V1.md`
  - `@../docs/AUTHORITY_MATRIX.yaml`
  - `@../docs/ESCALATION_PROTOCOL.md`
- NO Z3 Protocol reference
- Optional: Some have introductory sections (e.g., outreach has code-craft conventions)

Zone Structure (example Zone 1):
```markdown
- **Zone 1 (Chat/Collab):** Deliberation, proposals, mesh discussion
  - **Decision-maker:** <Practice> team lead
  - **Auto-approval:** Yes, if zero objections after 24h–72h review period
  - **Escalation:** To Zone 2 if objections or cross-practice impact
```

### Field Variations

| Field | Type A (Evaluator) | Type B (Standard) | Impact |
|-------|-------------------|-------------------|--------|
| **managed block** | Present | Absent | MINOR — informational only |
| **file path format** | `@docs/` | `@../docs/` | BREAKING — path resolution differs |
| **Z3 Protocol** | Explicit reference | None | MINOR — Type A points upstream |
| **Decision-maker** | Individual (Carly) | Role title | MINOR — semantic difference |
| **Auto-approval** | N/A (always Admiral gate) | Yes if no objections | BREAKING — approval rules differ |
| **Approval latency** | 24h–48h | 24h–48h | CONSISTENT |

### Breaking Reference Issue

All practices that use `@../docs/` references don't have those documents locally:
- empirica-autonomy — no AUTHORITY_MAPPING, ESCALATION_PROTOCOL
- empirica-mesh-support — no AUTHORITY_MAPPING, ESCALATION_PROTOCOL
- empirica-outreach — no AUTHORITY_MAPPING, ESCALATION_PROTOCOL (has Z3_PROTOCOL at root)
- website — no AUTHORITY_MAPPING, ESCALATION_PROTOCOL

**Shared parent directory?** The `@../docs/` assumes a shared parent directory structure that doesn't exist. The practices are peers, not children of a common parent.

---

## SCHEMA 5: Governance Supporting Documents

**Status:** FRAGMENTED (distributed across practices, inconsistent location)  
**Instances Found:** See breakdown below

### AUTHORITY_MAPPING_Z3_EMPIRICA_V1.md

**Has:**
- /Users/andersonfamily/practices/empirica-foundation-evaluator/docs/
- /Users/andersonfamily/practices/humanaios/docs/
- /Users/andersonfamily/practices/humanaios/empirica/empirica-foundation-evaluator/docs/ (duplicate)

**Missing:** empirica-autonomy, empirica-mesh-support, empirica-outreach, website

**Size:** 12,609 bytes (consistent across copies)

**Referenced by:** All 6 practices in their CLAUDE.md files

### ESCALATION_PROTOCOL.md

**Has:**
- /Users/andersonfamily/practices/empirica-foundation-evaluator/docs/
- /Users/andersonfamily/practices/humanaios/docs/
- /Users/andersonfamily/practices/humanaios/empirica/empirica-foundation-evaluator/docs/ (duplicate)

**Missing:** empirica-autonomy, empirica-mesh-support, empirica-outreach, website

**Size:** 24,812 bytes (consistent across copies)

**Referenced by:** All 6 practices in their CLAUDE.md files

### Z3_PROTOCOL.md

**Has:**
- /Users/andersonfamily/practices/empirica-outreach/ (root, not docs/)
- /Users/andersonfamily/practices/humanaios/operations/ (nested)

**Missing:** empirica-foundation-evaluator, empirica-autonomy, empirica-mesh-support, website

**Size:** 18,493 bytes (empirica-outreach copy)

**Referenced by:** Evaluator CLAUDE.md only (as "Upstream")

### CHARTER.md

**Has:**
- /Users/andersonfamily/practices/empirica-autonomy/docs/CHARTER.md

**Missing:** empirica-foundation-evaluator, empirica-mesh-support, empirica-outreach, humanaios, website

**Size:** 4,346 bytes (autonomy-specific)

### CLAUDE_MD_AUTHORITY_TEMPLATE.md

**Has:**
- /Users/andersonfamily/practices/empirica-foundation-evaluator/docs/
- /Users/andersonfamily/practices/humanaios/docs/

**Missing:** empirica-autonomy, empirica-mesh-support, empirica-outreach, website

**Size:** 7,974 bytes (template for CLAUDE.md Authority sections)

---

## DISTRIBUTION MATRIX

|  | evaluator | autonomy | mesh-support | outreach | humanaios | website |
|---|-----------|----------|--------------|----------|-----------|---------|
| **project.yaml** | ✓ Type A | ✓ Type B | ✓ Type B | ✓ Type B | ✓ Type A | ✓ Type B |
| **config.yaml** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **AUTHORITY_MATRIX.yaml** | ✓ | ✗ | ✗ | ✗ | ✓ | ✗ |
| **AUTHORITY_MAPPING.md** | ✓ | ✗ | ✗ | ✗ | ✓ | ✗ |
| **ESCALATION_PROTOCOL.md** | ✓ | ✗ | ✗ | ✗ | ✓ | ✗ |
| **Z3_PROTOCOL.md** | ✗ | ✗ | ✗ | ✓ | ✓ (ops) | ✗ |
| **CHARTER.md** | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| **CLAUDE_MD_AUTHORITY_TEMPLATE.md** | ✓ | ✗ | ✗ | ✗ | ✓ | ✗ |

---

## BREAKING INCONSISTENCIES SUMMARY

### Tier 1: Blocks Automation

1. **project.yaml field ordering** (SEVERITY: HIGH)
   - Type A vs Type B break parsing assumptions
   - Automation cannot normalize without explicit rules
   - Affects: All 6 practices (2 + 4 split)
   - Solution: Define canonical field order + migration script

2. **Governance document distribution** (SEVERITY: HIGH)
   - 4 practices reference documents they don't have
   - Path references (`@../docs/`) assume non-existent shared parent
   - Missing: AUTHORITY_MAPPING (4 practices), ESCALATION_PROTOCOL (4 practices)
   - Solution: Centralize governance docs + fix path references

3. **CLAUDE.md Authority section variants** (SEVERITY: MEDIUM-HIGH)
   - Variant 1 uses `@docs/` (absolute), Variant 2 uses `@../docs/` (relative)
   - Decision-maker field varies (individual vs role title)
   - Auto-approval logic differs significantly
   - Solution: Standardize Authority section template + field definitions

### Tier 2: Configuration Risk

4. **Duplicate governance documents** (SEVERITY: MEDIUM)
   - humanaios copies evaluator's docs — no sync mechanism
   - If evaluator updates docs, humanaios stays stale
   - Solution: Single source of truth + symlinks or explicit imports

5. **Z3_PROTOCOL placement** (SEVERITY: MEDIUM)
   - empirica-outreach has it at root level
   - humanaios has it in operations/ subdirectory
   - Evaluator references it as "upstream"
   - Solution: Clarify whether Z3_PROTOCOL is local or external + standardize location

6. **CHARTER.md only in autonomy** (SEVERITY: LOW-MEDIUM)
   - Other practices have no charter docs
   - Not referenced in CLAUDE.md files
   - Solution: Clarify if charter is autonomy-specific or should all practices have one

### Tier 3: Informational

7. **Managed comment blocks** (SEVERITY: LOW)
   - Evaluator has managed block, others don't
   - Suggests seat installer vs manual creation
   - Solution: Document seat installation model + rollout pattern

---

## RECOMMENDATIONS FOR M2 RANK 4 PHASE 2 (Schema Design)

### 1. Define Canonical Schemas

Create version 3.0 specifications for:
- **project.yaml** — canonical field order, required/optional/deprecated fields
- **config.yaml** — no changes needed (already consistent)
- **AUTHORITY_MATRIX.yaml** — centralized location + per-practice imports
- **CLAUDE.md Authority Section** — standard template + field definitions
- **Governance document set** — official locations + sync/import rules

### 2. Field Order Rule

Propose: Alphabetical within sections
```yaml
# Metadata
created_at
created_by
description
name
project_id
type
version

# Governance
canonical_seat
classification
domain
mesh_id_prefix
org_id
tenant_slug

# State
contacts
edges
engagements
language
status
tags

# Config
auto_detect
beads
calibration_weights
domain_config
evidence_profile
subjects
```

### 3. Centralization Strategy

**Governance Documents:**
- Single location: `/Users/andersonfamily/practices/empirica-foundation-evaluator/docs/` (master)
- Reference mechanism: `@` includes in CLAUDE.md
- Sync: Explicit copy + version pinning for humanaios (if needed) or symlink

**Practice Charters:**
- Location: Each practice's `/docs/CHARTER.md`
- Scope: Practice-specific governance, team structure, domain
- Reference: Linked from CLAUDE.md

### 4. Path Reference Convention

Standardize all CLAUDE.md references:
- If governance docs are shared: Use `@../docs/FILENAME` with validation that parent exists
- If governance docs are per-practice: Use `@docs/FILENAME` with validation that local copy exists
- Add CI/CD validation: Check all `@` references resolve correctly

### 5. Authority Section Standardization

Define template for all practices:
```markdown
## Authority Layer — Governance & Zone Mapping

**This practice inhabits:** empirica-foundation local governance  
**Practice name:** <practice-name>  
**Practice owner:** <owner-role>  

### Zone Scope & Delegation

[Standard zone structure + decision-maker fields]

### Governance Documents

[Standard reference section]

### References

[Charter, authority, last updated]
```

### 6. Version Migration

- **Current:** project.yaml v2.0 (Type A and B variants)
- **Proposed:** v3.0 with canonical field order
- **Migration path:** Script to reorder fields, preserve content, update version marker

---

## UNKNOWN QUESTIONS (for Admiral/Phase 2)

1. **Path reference resolution:** Are `@../docs/` references supposed to work? If so, what's the shared parent?
2. **Governance doc ownership:** Should evaluator own all governance docs, or should they be centralized elsewhere?
3. **Z3_PROTOCOL:** Is this supposed to be local or imported from upstream? Why is it at root in empirica-outreach?
4. **Duplicate in humanaios:** Why is humanaios copying evaluator's governance docs? Should it import instead?
5. **Practice charters:** Should all practices have a CHARTER.md, or is it autonomy-specific?
6. **Field ordering:** Should we enforce alphabetical order, or keep the current implicit grouping?

---

## ARTIFACT EVIDENCE

### Files Examined (6 practices × 4 schemas)

**project.yaml (6 files):**
- /Users/andersonfamily/practices/empirica-foundation-evaluator/.empirica/project.yaml
- /Users/andersonfamily/practices/empirica-autonomy/.empirica/project.yaml
- /Users/andersonfamily/practices/empirica-mesh-support/.empirica/project.yaml
- /Users/andersonfamily/practices/empirica-outreach/.empirica/project.yaml
- /Users/andersonfamily/practices/humanaios/.empirica/project.yaml
- /Users/andersonfamily/practices/website/.empirica/project.yaml

**config.yaml (6 files):**
- /Users/andersonfamily/practices/empirica-foundation-evaluator/.empirica/config.yaml
- /Users/andersonfamily/practices/empirica-autonomy/.empirica/config.yaml
- /Users/andersonfamily/practices/empirica-mesh-support/.empirica/config.yaml
- /Users/andersonfamily/practices/empirica-outreach/.empirica/config.yaml
- /Users/andersonfamily/practices/humanaios/.empirica/config.yaml
- /Users/andersonfamily/practices/website/.empirica/config.yaml

**AUTHORITY_MATRIX.yaml (3 instances, 1 unique):**
- /Users/andersonfamily/practices/empirica-foundation-evaluator/docs/AUTHORITY_MATRIX.yaml
- /Users/andersonfamily/practices/humanaios/docs/AUTHORITY_MATRIX.yaml
- /Users/andersonfamily/practices/humanaios/empirica/empirica-foundation-evaluator/docs/AUTHORITY_MATRIX.yaml

**CLAUDE.md Authority sections (6 files):**
- /Users/andersonfamily/practices/empirica-foundation-evaluator/CLAUDE.md
- /Users/andersonfamily/practices/empirica-autonomy/CLAUDE.md
- /Users/andersonfamily/practices/empirica-mesh-support/CLAUDE.md
- /Users/andersonfamily/practices/empirica-outreach/CLAUDE.md
- /Users/andersonfamily/practices/humanaios/CLAUDE.md
- /Users/andersonfamily/practices/website/CLAUDE.md

**Governance documents (5 unique + duplicates):**
- AUTHORITY_MAPPING_Z3_EMPIRICA_V1.md (3 instances: evaluator, humanaios, humanaios/empirica)
- ESCALATION_PROTOCOL.md (3 instances: evaluator, humanaios, humanaios/empirica)
- Z3_PROTOCOL.md (2 instances: outreach, humanaios/operations)
- CHARTER.md (1 instance: autonomy)
- CLAUDE_MD_AUTHORITY_TEMPLATE.md (2 instances: evaluator, humanaios)

---

## CONCLUSION

The foundation practices have reached a critical point in governance harmonization. While runtime configs (config.yaml) are consistent, metadata schemas (project.yaml), governance references (CLAUDE.md), and document distribution are fragmented across two variants.

M2 Rank 4 Schema Design phase must address:
1. Canonical field ordering for project.yaml
2. Centralized governance document location + resolution rules
3. Standard Authority section template for CLAUDE.md
4. Migration pathway for practices using Type B variants

This discovery provides the baseline for Phase 2 design work.

---

**Status:** DRAFT DISCOVERY (ready for Admiral review)  
**Next Step:** Admiral feedback → Phase 2 Schema Design
