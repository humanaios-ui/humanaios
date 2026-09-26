# M2 Rank 3: Phase 5 Sync Pipeline Specification

**Document ID:** M2R3-PHASE5-SPEC-2026-07-23  
**Status:** READY FOR EXECUTION (after Phase 4)  
**Objective:** Automated entity synchronization from authoritative sources  
**Timeline:** 1-2 days  
**Depends on:** Phase 4 (all entities + relationships registered)

---

## Phase 5: Automated Entity Sync

### 5.1 Sync Architecture

**Sources of Truth:**
1. `.empirica/project.yaml` files (project identity + ownership)
2. Git log (user/contributor tracking)
3. Engagement records (project-engagement mappings)
4. Organization configuration (org membership)

**Sync Flow:**
```
Poll Sources → Detect Changes → Update Registry → Validate → Log Changes
        ↓              ↓              ↓              ↓           ↓
    Hourly        File hash      Insert/Update   Schema     Change log
   (CronCreate)    matching       queries        validation   entry
```

**Conflict Resolution:** Manual Admiral review (conflict_resolution="manual_admiral_review")

---

### 5.2 Sync Task 1: Project Sync (`.empirica/project.yaml`)

**Frequency:** Hourly via CronCreate

**Execution:**
1. For each `.empirica/project.yaml`:
   - Read ai_id, org_id, owner_contact_id, description
   - Compute file hash (SHA256 of content)
   - Query entity_registry for project by canonical_id
   - If project exists:
     - Compare hashes: if changed, update record
     - Log update: "project updated: ai_id=X, field=Y, old=Z, new=W"
   - If project missing:
     - Register project (as Phase 3)
     - Log: "project discovered and registered: ai_id=X"

**Validation:**
- Canonical identifier must be 3-form
- ai_id must be non-empty
- org_id must reference registered organization
- owner_contact_id must reference registered contact

**Conflict Handling:**
- If canonical_id already exists but ai_id differs: CONFLICT
  - Log: "canonical_id collision: ai_id1=X, ai_id2=Y"
  - Action: Notify Admiral, halt sync until resolved

**Expected Sync Rate:** 0-2 changes/hour (projects rarely change)

---

### 5.3 Sync Task 2: Contact Sync (git log + project.yaml)

**Frequency:** Hourly via CronCreate

**Execution:**
1. Collect all contacts from:
   - `.empirica/project.yaml` owner_contact_id fields (all projects)
   - Git log --format="%aE %aN" (all projects)
   - Engagement records (manual list)

2. For each unique email:
   - Normalize email (lowercase, strip whitespace)
   - Query entity_registry for contact by canonical_id (email)
   - If contact exists:
     - Check if name changed (git log may have updated name)
     - If changed: update contact record
     - Log: "contact updated: email=X, name_old=A, name_new=B"
   - If contact missing:
     - Determine authority_tier:
       - If Carly: authority_tier="admiral"
       - If owner_contact_id in any project: authority_tier="owner"
       - Otherwise: authority_tier="member"
     - Register contact
     - Log: "contact discovered: email=X, tier=Y"

**Deduplication:**
- Emails are canonical keys (case-insensitive)
- If duplicate emails found: keep first occurrence, log warning

**Conflict Handling:**
- If contact authority_tier differs from previous sync: log as warning, keep existing tier (manual review)

**Expected Sync Rate:** 0-1 changes/hour

---

### 5.4 Sync Task 3: Engagement Sync (engagement records)

**Frequency:** Hourly via CronCreate

**Execution:**
1. Query engagement records for:
   - Engagement name, description, status
   - Associated projects (serves relationships)
   - Participants (contacts)

2. For each engagement:
   - Query entity_registry for engagement by canonical_id
   - If engagement exists:
     - Check status, description, associated projects
     - If changed: update record
     - Log: "engagement updated: name=X, field=Y, old=Z, new=W"
   - If engagement missing:
     - Register engagement
     - Create serves relationships to associated projects
     - Log: "engagement discovered: name=X"

**Validation:**
- Engagement canonical_id must be slug format
- All associated projects must exist in registry
- All participants must exist as contacts

**Conflict Handling:**
- If project.serves.engagement references nonexistent engagement: log as error, skip relationship

**Expected Sync Rate:** 0-0.5 changes/hour

---

### 5.5 Sync Task 4: Organization Sync (static config)

**Frequency:** On-demand (no hourly changes expected)

**Execution:**
1. Query configuration for:
   - empirica-foundation (BDFL: Carly)
   - empirica (company org)

2. For each organization:
   - Query entity_registry by canonical_id
   - If missing: register
   - If exists: verify status (should be stable)

**Validation:**
- Organization canonical_id must be slug format
- BDFL reference must exist as contact

**Expected Sync Rate:** 0 changes/hour (static)

---

## 5.6 Sync Pipeline Implementation

**Script:** `scripts/sync_entity_registry.py`

```python
def sync_projects():
    """Hourly: Poll project.yaml files, update registry"""
    for project_yaml in discover_project_yamls():
        hash = compute_hash(project_yaml)
        if hash_changed(hash):
            update_registry(project_yaml)
            log_sync_change("project updated", ...)

def sync_contacts():
    """Hourly: Poll git log + project.yaml, sync contacts"""
    contacts = collect_contacts_from_sources()
    for email, contact_info in contacts.items():
        existing = query_registry(canonical_id=email)
        if not existing:
            register_contact(email, contact_info)
            log_sync_change("contact discovered", ...)
        elif contact_info changed:
            update_registry(email, contact_info)
            log_sync_change("contact updated", ...)

def sync_engagements():
    """Hourly: Poll engagement records, sync engagements"""
    engagements = query_engagement_records()
    for engagement in engagements:
        existing = query_registry(canonical_id=engagement.id)
        if not existing:
            register_engagement(engagement)
            log_sync_change("engagement discovered", ...)
        elif engagement changed:
            update_registry(engagement)
            log_sync_change("engagement updated", ...)

def sync_organizations():
    """On-demand: Verify organization records (static)"""
    for org in get_organizations():
        existing = query_registry(canonical_id=org.id)
        if not existing:
            register_organization(org)
            log_sync_change("organization discovered", ...)

def validate_all_syncs():
    """Post-sync validation"""
    # No orphaned relationships
    # All canonical_ids unique
    # All authority_tiers valid
    # All references resolve

if __name__ == "__main__":
    sync_projects()
    sync_contacts()
    sync_engagements()
    sync_organizations()
    validate_all_syncs()
```

---

## 5.7 Sync Schedule

**Hourly Sync (via CronCreate):**
- Projects: every hour
- Contacts: every hour
- Engagements: every hour

**On-Demand Sync:**
- Organizations: on configuration change
- Manual trigger: empirica sync-entities (for emergency re-sync)

**Sync Log Location:** `.empirica/sync.log` (append-only)

**Sync Report (Daily):** Email to Admiral with summary of changes

---

## 5.8 Sync Validation Checklist

- [ ] Projects: all entries synced with latest ai_id, owner, org
- [ ] Contacts: all git contributors discovered and registered
- [ ] Engagements: all active engagements synced
- [ ] Organizations: unchanged (verify only)
- [ ] No orphaned relationships after sync
- [ ] No duplicate canonical_identifiers
- [ ] All conflicts logged for Admiral review
- [ ] Sync log entries complete with timestamps
- [ ] Entity counts stable (or expected changes logged)

---

## 5.9 Commit Message

```
feat(m2r3): sync pipeline — automated entity synchronization

Implemented hourly sync pipeline for:
- Project discovery and update (from .empirica/project.yaml)
- Contact sync (from git log + project.yaml)
- Engagement sync (from engagement records)
- Organization verification (static config)

Sync features:
- Hash-based change detection (avoid redundant updates)
- Conflict logging (manual Admiral review)
- Full audit trail (sync.log)
- Validation post-sync (no orphaned relationships)

Frequency:
- Projects: hourly
- Contacts: hourly
- Engagements: hourly
- Organizations: on-demand

Authority: M2 Rank 3 RFC, Phase 5/6
Prerequisite: Phase 4 complete (all entities + relationships registered)
Next: Phase 6 verification & testing

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
```

---

**Status: Specification ready. Will execute after Phase 4 completion.**
