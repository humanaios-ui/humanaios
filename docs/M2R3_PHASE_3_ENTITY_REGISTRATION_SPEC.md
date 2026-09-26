# M2 Rank 3: Phase 3 Entity Registration Specification

**Document ID:** M2R3-PHASE3-SPEC-2026-07-23  
**Status:** READY FOR EXECUTION (after Phase 2 schema update)  
**Entities to Register:** 11 projects, 5 contacts, 2 organizations, 3 engagements, 3+ users  
**Timeline:** 2-3 days (can parallelize with Phase 4)  
**Depends on:** Phase 2 schema update (canonical_identifier, authority_tier fields)

---

## Phase 3: Entity Registration Execution Plan

### 3.1 Projects (11 entities)

**Source of Truth:** `.empirica/project.yaml` in each practice directory

**Registration Template:**
```yaml
entity_type: "project"
entity_id: <UUID from .empirica/project.yaml>
display_name: <ai_id field>
canonical_identifier: "empirica-foundation.carly.<ai_id>"  # 3-form
authority_tier: "owner"  # or "member" if not Admiral-owned
description: <description from project.yaml>
source_of_truth: ".empirica/project.yaml"
status: "active"
verification_status: "synced"
```

**Projects to Register:**

1. empirica-foundation-evaluator (Admiral seat)
2. empirica-autonomy
3. empirica-mesh-support
4. empirica-outreach
5. humanaios
6. humanaios-internal
7. website
8. flta-app-empirica
9. collaborator-ops
10. grok-crossref
11. opportunity-aggregator

**Execution:**
- Read `.empirica/project.yaml` from each practice
- Extract ai_id, description, owner_contact_id
- Generate canonical_identifier (org.tenant.ai_id)
- Insert into entity_registry with verification_status="synced"
- Verify: 11/11 inserted, no duplicates

---

### 3.2 Contacts (5 entities)

**Source of Truth:** Email addresses (canonical key) + project.yaml owner_contact_id

**Registration Template:**
```yaml
entity_type: "contact"
entity_id: <email hash or UUID>
display_name: <name>
canonical_identifier: <email>
authority_tier: "admiral"  # Carly only; others "member"
description: <role>
contact_info_encrypted: <TBD: encrypted email>
source_of_truth: "project.yaml owner_contact_id or git log"
status: "active"
verification_status: "synced"
```

**Contacts to Register:**

1. Carly R. Anderson (carly.r.anderson@gmail.com) — Admiral
2. AI OS Human (aioshuman@gmail.com) — Contributor
3. Local Developer (andersonfamily@Carlys-MacBook-Pro.local) — Developer
4. [TBD from engagement records] — Team member
5. [TBD from engagement records] — Team member

**Execution:**
- Extract contact emails from:
  - project.yaml owner_contact_id fields
  - git log authors
  - Engagement records
- Normalize emails (lowercase, dedupe)
- Insert into entity_registry
- Mark Carly as authority_tier="admiral", others as "member"
- Verify: 5/5 inserted, canonical_identifier unique

---

### 3.3 Organizations (2 entities)

**Source of Truth:** .empirica/project.yaml org_id + org config

**Registration Template:**
```yaml
entity_type: "organization"
entity_id: <org_id>
display_name: <org name>
canonical_identifier: <org slug>
authority_tier: "owner"  # org-level authority
description: <org description>
source_of_truth: "org configuration + project.yaml"
status: "active"
verification_status: "synced"
```

**Organizations to Register:**

1. empirica-foundation — BDFL: Carly R. Anderson
2. empirica (company) — Cross-org coordination via mesh-support

**Execution:**
- Insert 2 organizations
- Verify: canonical_identifier is unique
- Link to practices (done in Phase 4 relationships)

---

### 3.4 Engagements (3 entities)

**Source of Truth:** Engagement records + project metadata

**Registration Template:**
```yaml
entity_type: "engagement"
entity_id: <engagement_id or UUID>
display_name: <engagement name>
canonical_identifier: <engagement-slug>
authority_tier: "owner"  # engagement owner
description: <engagement description>
source_of_truth: "engagement records"
status: "active"
verification_status: "synced"
```

**Engagements to Register:**

1. ACAT (Pilot) — empirica-foundation-evaluator
2. HumanAIOS Initiative — humanaios, humanaios-internal
3. FLTA Integration — flta-app-empirica

**Execution:**
- Insert 3 engagements
- Link to projects (via Phase 4 relationships)
- Verify: 3/3 inserted

---

### 3.5 Users (3+ entities)

**Source of Truth:** Git log (authors) + session records

**Registration Template:**
```yaml
entity_type: "user"
entity_id: <user_uuid or git_author_email>
display_name: <name from git config>
canonical_identifier: <email>
authority_tier: "observer"  # base level
description: "Contributor"
source_of_truth: "git log"
status: "active"
verification_status: "synced"
```

**Users to Register:**

1. Carly R. Anderson (from git)
2. Local Developer (from git)
3. [Additional contributors from git log]

**Execution:**
- Parse git log --format="%aE %aN"
- Deduplicate by email
- Insert into entity_registry
- Verify: 3+ users inserted

---

## Execution Script

**Script:** `scripts/register_entities.py`

```python
"""
M2 Rank 3 Phase 3: Entity Registration
Reads source-of-truth files and registers all entities.
"""

def register_projects():
    # Find all .empirica/project.yaml files
    # Extract ai_id, description, owner_contact_id
    # Insert into entity_registry
    # Return: count, UUIDs

def register_contacts():
    # Extract from project.yaml + git log
    # Normalize emails
    # Insert into entity_registry
    # Return: count, UUIDs

def register_organizations():
    # Insert empirica-foundation, empirica
    # Return: count, UUIDs

def register_engagements():
    # Extract from engagement records
    # Insert into entity_registry
    # Return: count, UUIDs

def register_users():
    # Parse git log
    # Insert into entity_registry
    # Return: count, UUIDs

def verify_registration():
    # Query entity_registry
    # Count by type: projects, contacts, orgs, engagements, users
    # Verify no duplicates on canonical_identifier
    # Report: X/X registered, 0 conflicts

if __name__ == "__main__":
    register_projects()
    register_contacts()
    register_organizations()
    register_engagements()
    register_users()
    verify_registration()
```

---

## Verification Checklist

- [ ] All 11 projects registered
- [ ] All 5 contacts registered
- [ ] All 2 organizations registered
- [ ] All 3 engagements registered
- [ ] All 3+ users registered
- [ ] No duplicate canonical_identifiers
- [ ] No NULL canonical_identifier values
- [ ] Authority tiers set correctly (admiral for Carly, owner for others)
- [ ] source_of_truth fields populated
- [ ] verification_status="synced" for all

---

## Commit Message

```
feat(m2r3): entity registration — register all 22+ entities

Registered:
- 11 projects (empirica-foundation-evaluator, autonomy, mesh-support, outreach, humanaios, humanaios-internal, website, flta-app-empirica, collaborator-ops, grok-crossref, opportunity-aggregator)
- 5 contacts (Carly, aioshuman, local developer, + 2 TBD)
- 2 organizations (empirica-foundation, empirica)
- 3 engagements (ACAT, HumanAIOS, FLTA)
- 3+ users (from git log)

All entities registered with canonical_identifier (3-form), authority_tier, source_of_truth.
Authority: M2 Rank 3 RFC, Phase 3/6
Prerequisite: Phase 2 schema update (completed)
Next: Phase 4 relationship validation

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
```

---

**Status: Specification ready. Awaiting Phase 2 completion to begin execution.**
