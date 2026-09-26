# M2 Rank 3: Entity Registry Harmonization RFC

**Document ID:** M2R3-RFC-2026-07-23-REGISTRY  
**Status:** ⏳ AWAITING ADMIRAL APPROVAL (Post-Rank 2)  
**Submitted by:** empirica-foundation-evaluator (spec-prep fork)  
**Submission Date:** 2026-07-23  
**Target Decision Date:** 2026-07-27 (after Rank 2 completes)  
**Audience:** Admiral (Carly), M2 Rank 3 executor, empirica infrastructure team

---

## Executive Summary

The foundation's entity registry (currently in SQLite `workspace.db` with partial data) lacks authoritative status for all 40+ practices. Duplicate registrations, missing relationships, and inconsistent metadata make cross-practice queries unreliable. This RFC proposes completing the registry with canonical entity types (project|contact|organization|engagement|user), strict relationship rules (member-of|serves|uses|owns), and automated sync so registry state always matches git source-of-truth. Registry harmonization is a prerequisite for Witness v2 state sync (M3 work) and future Evaluator audit workflows.

---

## Current State: What's Broken

### Incomplete Registration

| Entity Type | Expected | Registered | Gap | Impact |
|-----------|----------|------------|-----|--------|
| project (practices) | 9 | 8 | empirica-mesh-support missing | Cross-practice queries incomplete |
| contact (people) | ~5 | 2 | Admiral, one teammate only | Can't track who owns what |
| organization | 2 (empirica-foundation, empirica) | 1 | Only empirica-foundation | Cross-org routing (mesh-support ↔ company) broken |
| engagement | 3 (ACAT pilot, HumanAIOS, FLTA) | 0 | None registered | Can't link projects to business context |
| user | ~3 | 0 | Not tracked | Can't audit who made which decisions |

### Broken Relationships (entity_memberships)

| Relationship | Should Exist | Currently Exists | Problem |
|--------------|-------------|-----------------|---------|
| empirica-autonomy `member-of` empirica-foundation | Yes | No | autonomy appears to be solo |
| Carly (contact) `owns` empirica-foundation-evaluator | Yes | No | Ownership chain missing |
| empirica-mesh-support `serves` empirica-foundation + empirica | Yes | No | Can't verify mesh-support's reach |
| empirica-outreach `uses` empirica-autonomy | Yes | No | Dependency graph incomplete |

### Schema Gaps

**Current `entity_registry` schema:**
```sql
entity_type, entity_id, display_name, description, source_db, source_table, 
emoji_state, status, created_at, updated_at, metadata
```

**Missing fields:**
- `canonical_identifier` — the 3-form (org.tenant.project) for routing
- `authority_tier` — for permission models (Admiral, Owner, Member, Observer)
- `contact_info` — email, Slack handle (encrypted or reference)
- `last_verified_at` — when was this entry checked against source-of-truth?
- `verification_status` — synced|stale|conflict

---

## Proposed Unified Registry Model

### Authoritative Entity Types

| Type | Count | Canonical Key | Example |
|------|-------|---------------|---------|
| **project** | 9 | `ai_id` from `.empirica/project.yaml` | empirica-foundation-evaluator |
| **contact** | ~5 | email (canonical) | carly.r.anderson@gmail.com |
| **organization** | 2 | org slug | empirica-foundation |
| **engagement** | 3 | engagement ID (UUID) | acat-pilot-001 |
| **user** | ~3 | user UUID (from sessions) | session creator UUID |

### Authoritative Relationships (entity_memberships)

| Relationship | Source-of-Truth | Validation |
|--------------|-----------------|-----------|
| `project` `member-of` `organization` | `.empirica/project.yaml` `org_id` field | Check org_id resolves |
| `contact` `owns` `project` | `project.yaml` `owner_contact_id` (new field) | Verify contact exists |
| `project` `serves` `contact` (or org) | Engagement records + project metadata | Cross-ref in engagement table |
| `user` `contributor_to` `project` | Git log (author emails) | Parse `git log --format=%aE` |
| `project` `uses` `project` (dependency) | Explicit dependency declaration in `project.yaml` | Document inter-practice deps |

### Enhanced Schema

**New fields on entity_registry:**

```yaml
# Existing
entity_type: "project"
entity_id: "428902a7-19dd-4598-b655-51a4a689934f"
display_name: "empirica-foundation-evaluator"
status: "active"

# NEW
canonical_identifier: "empirica-foundation.carly.empirica-foundation-evaluator"
authority_tier: "admiral"  # admiral|owner|member|observer
source_of_truth: ".empirica/project.yaml"
verification:
  last_verified_at: 1721758800
  verification_status: "synced"  # synced|stale|conflict
  verification_hash: "sha256:abc123..."  # hash of source file
contact_info_encrypted: "..." # TBD: key management
```

**Example: Complete entry**

```yaml
entity_registry:
  - entity_type: "project"
    entity_id: "428902a7-19dd-4598-b655-51a4a689934f"
    display_name: "empirica-foundation-evaluator"
    description: "Carly R. Anderson — Admiral + Evaluator seat"
    status: "active"
    canonical_identifier: "empirica-foundation.carly.empirica-foundation-evaluator"
    authority_tier: "admiral"
    source_db: "workspace.db"
    source_table: "projects"
    source_of_truth_path: ".empirica/project.yaml"
    source_of_truth_hash: "sha256:c4fa45212345..."
    verification:
      last_verified_at: 1721758800
      verification_status: "synced"
    created_at: 1656201600
    updated_at: 1721758800
    metadata:
      ai_id: "empirica-foundation-evaluator"
      mesh_id_prefix: "empirica-foundation.carly"
      domain: "evaluation"
      team_members: ["carly"]
```

---

## Migration Path

### Phase 1: Audit Current State (1 day)

Scan all 40+ repos and generate an inventory:

**Script:** `scripts/audit_registry_state.sh`

```bash
for practice in $(ls -d practices/*/); do
  name=$(basename $practice)
  ai_id=$(grep '^ai_id:' $practice/.empirica/project.yaml)
  canonical=$(grep '^canonical_seat:' $practice/.empirica/project.yaml)
  registered=$(sqlite3 workspace.db "SELECT COUNT(*) FROM entity_registry WHERE display_name='$name'")
  echo "$name | $ai_id | $canonical | registered=$registered"
done > registry_audit.csv
```

**Output:** `registry_audit.csv` (all 40+ repos with registration status).

### Phase 2: Populate Missing Entities (1 day)

For each unregistered entity, create registry entry:

```bash
empirica entity-register \
  --type project \
  --entity-id <uuid-from-project.yaml> \
  --canonical <canonical-3-form> \
  --source .empirica/project.yaml
```

**For contacts & engagements:** Manually add (small set, ~5 entries).

### Phase 3: Validate Relationships (1 day)

Walk the entity graph and verify relationships are valid:

**Script:** `scripts/validate_registry_relationships.sh`

```bash
# For each project, verify:
# 1. organization exists
# 2. owner contact exists (if specified)
# 3. engagement references resolve

for entity_id in $(empirica entity-list --type project --output json | jq -r '.[].entity_id'); do
  org_id=$(empirica entity-show project:$entity_id --output json | jq '.metadata.org_id')
  verify_entity_exists "organization:$org_id" || flag_conflict
done
```

### Phase 4: Sync Source-of-Truth & Verification (2 days)

Build sync pipeline that keeps registry in sync with `.empirica/project.yaml`:

**Service:** `empirica-registry-sync` (runs hourly)

```python
def sync_registry():
  for practice_dir in all_practices:
    project_yaml = read_yaml(f"{practice_dir}/.empirica/project.yaml")
    registry_entry = query_registry(project_yaml['ai_id'])
    
    if registry_entry is None:
      # New practice — register it
      create_registry_entry(project_yaml)
    else:
      # Existing — verify checksums match
      if hash(project_yaml) != registry_entry['source_of_truth_hash']:
        flag_verification_status("stale")
        alert_admin("Registry stale: {practice_dir}")
      else:
        flag_verification_status("synced")
```

### Phase 5: Audit & Verification (1 day)

Run full registry validation suite:

**Test:** `tests/registry_harmonization_test.py`

```python
def test_all_projects_registered():
  projects_on_disk = find_all_projects()
  projects_registered = query_registry("type=project")
  assert len(projects_on_disk) == len(projects_registered)

def test_canonical_identifiers_unique():
  # No two projects share same canonical_identifier
  canonicals = [e['canonical_identifier'] for e in registry.all()]
  assert len(canonicals) == len(set(canonicals))

def test_relationships_valid():
  # Every relationship's source AND target exist
  for rel in registry.relationships():
    assert entity_exists(rel.source)
    assert entity_exists(rel.target)

def test_sync_pipeline_updates_registry():
  # Modify a project.yaml, run sync, verify registry updated
  project_yaml['description'] = "Updated"
  write_yaml(project_yaml)
  sync_registry()
  assert query_registry_by_ai_id(project_yaml['ai_id'])['description'] == "Updated"
```

---

## Verification Checklist

- [ ] Registry inventory complete (all 40+ projects scanned + flagged)
- [ ] Missing entities registered (contacts, engagements)
- [ ] Relationship graph validated (no dangling references)
- [ ] Sync pipeline deployed (hourly verification running)
- [ ] Stale-detection working (alerts firing if checksum mismatches)
- [ ] Cross-practice queries working (list all projects serving empirica-foundation)
- [ ] Rollout complete (registry = source-of-truth)
- [ ] POSTFLIGHT + grounded calibration submitted

---

## Reversibility

### Full Rollback

If registry sync breaks:
1. Disable sync pipeline (stop hourly cron)
2. Restore registry from last good backup (daily snapshots kept)
3. Notify practitioners (registry temporarily read-only)
4. Debug + fix, re-enable sync

**Cost:** 1-2h downtime; no data loss due to backups.

### Partial Rollback (entity-level)

If one practice's sync is conflicting:
1. Flag that practice in sync config (`skip_sync_for: [practice_name]`)
2. Manual verification + fix
3. Re-enable sync for that practice

---

## Risk Assessment

### Low Risk

- **Source-of-truth is immutable** (git-tracked `.empirica/project.yaml`)
- **Hourly verification** catches drift early
- **Relationship validation** prevents invalid edges

### Medium Risk

- **Contact information security** — Email addresses stored in DB. **Mitigation:** Encrypt sensitive fields, limit query scope to authorized practitioners.
- **Circular dependencies** — Projects may reference each other. **Mitigation:** Detect cycles at validation time, flag for manual resolution.

### Monitoring

1. **Sync pipeline errors** — Alert if sync fails for >30 min
2. **Stale entries** — Alert if any entity's verification_status = "stale" for >1h
3. **Broken relationships** — Alert if any foreign key check fails

---

## Timeline

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| P1: Audit | 1 day | None |
| P2: Populate | 1 day | P1 audit complete |
| P3: Validate | 1 day | P2 complete |
| P4: Sync pipeline | 2 days | P3 validation passed |
| P5: Verification | 1 day | P4 pipeline stable |
| **Total** | **6 days** | M2 Rank 2 (State Machines) should be complete for ordering |

---

## References

- **Constitution:** `/empirica-constitution` §IV (Practice Model — entity registry foundations)
- **Authority:** M2 Rank 1 (Authority System) + AUTHORITY_MATRIX.yaml
- **Next:** M2 Rank 4 (Schemas Harmonization) — registry schema is input
- **Downstream:** M3 (Witness state sync) depends on authoritative registry

---

**Status: ⏳ AWAITING ADMIRAL APPROVAL (blocked by M2 Rank 2 completion)**

This RFC is ready for queue. Once Rank 2 is complete and merged, Rank 3 can begin immediately.
