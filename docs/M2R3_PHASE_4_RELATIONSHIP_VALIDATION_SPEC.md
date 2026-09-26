# M2 Rank 3: Phase 4 Relationship Validation Specification

**Document ID:** M2R3-PHASE4-SPEC-2026-07-23  
**Status:** READY FOR EXECUTION (parallel with Phase 3)  
**Relationships to Establish:** 8+ edges across 5 relationship types  
**Timeline:** 1-2 days (parallel with Phase 3 registration)  
**Depends on:** Phase 3 entity registration (all entities must exist first)

---

## Phase 4: Relationship Validation Execution Plan

### 4.1 Relationship Types & Sources of Truth

| Relationship | Source | Validation | Count |
|--------------|--------|-----------|-------|
| `member-of` | `.empirica/project.yaml` org_id field | Verify target org exists | 9 |
| `owns` | `.empirica/project.yaml` owner_contact_id | Verify owner contact exists | 9 |
| `serves` | Engagement records + project metadata | Link project to engagement | 3 |
| `uses` | Explicit dependency in project.yaml | Verify dependency project exists | 2-3 |
| `contributor_to` | Git log (authors) | Map users to projects | 20+ |

---

### 4.2 Relationship: `member-of` (Projects belong to Organization)

**Pattern:** `project` `member-of` `organization`

**Execution:**

1. For each project (11 total):
   - Read `.empirica/project.yaml`
   - Extract `org_id` field (should be "empirica-foundation")
   - Look up organization entity in registry
   - If org exists: create relationship
   - If org missing: log error, skip

2. **Expected edges:**
   - empirica-foundation-evaluator → empirica-foundation
   - empirica-autonomy → empirica-foundation
   - empirica-mesh-support → empirica-foundation
   - (9 total)

3. **Validation:**
   ```sql
   SELECT COUNT(*) FROM entity_memberships 
   WHERE relationship_type = 'member-of' 
   AND source_entity_type = 'project'
   AND target_entity_type = 'organization';
   -- Expected: 9
   ```

---

### 4.3 Relationship: `owns` (Contact owns Project)

**Pattern:** `contact` `owns` `project`

**Execution:**

1. For each project (11 total):
   - Read `.empirica/project.yaml`
   - Extract `owner_contact_id` (email or canonical identifier)
   - Look up contact entity in registry
   - If contact exists: create "owns" relationship
   - If contact missing: attempt to register first, then create relationship

2. **Expected edges:**
   - Carly R. Anderson → empirica-foundation-evaluator (Admiral seat)
   - (other owners as defined in project.yaml)

3. **Validation:**
   ```sql
   SELECT COUNT(*) FROM entity_memberships 
   WHERE relationship_type = 'owns' 
   AND source_entity_type = 'contact';
   -- Expected: 9
   ```

---

### 4.4 Relationship: `serves` (Project serves Engagement)

**Pattern:** `project` `serves` `engagement`

**Execution:**

1. From engagement records, identify which projects support each engagement:
   - ACAT → empirica-foundation-evaluator
   - HumanAIOS → humanaios, humanaios-internal
   - FLTA → flta-app-empirica

2. For each project-engagement pair:
   - Look up both entities in registry
   - Create "serves" relationship

3. **Validation:**
   ```sql
   SELECT COUNT(*) FROM entity_memberships 
   WHERE relationship_type = 'serves' 
   AND source_entity_type = 'project'
   AND target_entity_type = 'engagement';
   -- Expected: 3-4
   ```

---

### 4.5 Relationship: `uses` (Project uses Project — Dependencies)

**Pattern:** `project` `uses` `project`

**Execution:**

1. For projects with explicit dependencies in `.empirica/project.yaml`:
   - Read `dependencies` or `uses` field (if present)
   - Map each dependency to another project
   - Create "uses" relationship

2. **Examples (to discover):**
   - empirica-outreach might use empirica-autonomy
   - humanaios might use empirica-foundation-evaluator
   - (others to be determined from project.yaml inspection)

3. **Validation:**
   ```sql
   SELECT COUNT(*) FROM entity_memberships 
   WHERE relationship_type = 'uses' 
   AND source_entity_type = 'project'
   AND target_entity_type = 'project';
   -- Expected: 2-3
   ```

---

### 4.6 Relationship: `contributor_to` (User contributes to Project)

**Pattern:** `user` `contributor_to` `project`

**Execution:**

1. For each project (11 total):
   - Run `git log --format="%aE %aN"`
   - Extract unique author emails
   - For each author:
     - Look up or register user entity
     - Create "contributor_to" relationship

2. **Expected edges:**
   - 20+ edges (users × projects)
   - Most projects will have 2-3 contributors
   - Carly likely contributor_to all 11

3. **Validation:**
   ```sql
   SELECT COUNT(*) FROM entity_memberships 
   WHERE relationship_type = 'contributor_to' 
   AND source_entity_type = 'user';
   -- Expected: 20+
   ```

---

## Execution Script

**Script:** `scripts/validate_relationships.py`

```python
"""
M2 Rank 3 Phase 4: Relationship Validation
Establishes and validates all entity relationships.
"""

def establish_member_of():
    # Read project.yaml org_id for each project
    # Create member-of relationships to organizations
    # Validate: 9 relationships created

def establish_owns():
    # Read project.yaml owner_contact_id for each project
    # Create owns relationships to contacts
    # Validate: 9 relationships created

def establish_serves():
    # From engagement records, map projects to engagements
    # Create serves relationships
    # Validate: 3-4 relationships created

def establish_uses():
    # From project.yaml dependencies field
    # Create uses relationships
    # Validate: 2-3 relationships created

def establish_contributor_to():
    # Parse git log for each project
    # Create contributor_to relationships
    # Validate: 20+ relationships created

def validate_all_relationships():
    # Query each relationship type
    # Verify no broken edges (orphaned relationships)
    # Verify no duplicate relationships
    # Report: total relationships, by type

if __name__ == "__main__":
    establish_member_of()
    establish_owns()
    establish_serves()
    establish_uses()
    establish_contributor_to()
    validate_all_relationships()
```

---

## Relationship Validation Checklist

- [ ] member-of: 9 edges (projects → organizations)
- [ ] owns: 9 edges (contacts → projects)
- [ ] serves: 3-4 edges (projects → engagements)
- [ ] uses: 2-3 edges (projects → projects)
- [ ] contributor_to: 20+ edges (users → projects)
- [ ] No orphaned relationships (target entity doesn't exist)
- [ ] No duplicate relationships (same source-target-type pair)
- [ ] All edges resolve correctly (no broken references)
- [ ] Cross-practice relationships validate (e.g., mesh-support serves foundation orgs)

---

## Relationship Graph Queries (Validation Examples)

```sql
-- Find all projects and their owning organization
SELECT p.display_name, o.display_name 
FROM entity_registry p
JOIN entity_memberships em ON p.entity_id = em.source_entity_id
JOIN entity_registry o ON em.target_entity_id = o.entity_id
WHERE p.entity_type = 'project' 
AND em.relationship_type = 'member-of';

-- Find all contacts and the projects they own
SELECT c.display_name, COUNT(p.entity_id)
FROM entity_registry c
JOIN entity_memberships em ON c.entity_id = em.source_entity_id
JOIN entity_registry p ON em.target_entity_id = p.entity_id
WHERE c.entity_type = 'contact'
AND em.relationship_type = 'owns'
GROUP BY c.entity_id;

-- Find projects that contribute to an engagement
SELECT p.display_name, e.display_name
FROM entity_registry p
JOIN entity_memberships em ON p.entity_id = em.source_entity_id
JOIN entity_registry e ON em.target_entity_id = e.entity_id
WHERE p.entity_type = 'project'
AND em.relationship_type = 'serves';
```

---

## Commit Message

```
feat(m2r3): entity relationship validation — establish 35+ edges

Relationships established:
- member-of: 9 (projects → organizations)
- owns: 9 (contacts → projects)
- serves: 3-4 (projects → engagements)
- uses: 2-3 (projects → projects)
- contributor_to: 20+ (users → projects)

Total edges: 35+ (all validated, no orphaned relationships)

All relationships resolved correctly:
- No broken references
- No duplicate edges
- Cross-org routing (mesh-support → empirica + empirica-foundation) validated

Authority: M2 Rank 3 RFC, Phase 4/6
Parallel execution: Phase 3 entity registration
Next: Phase 5 sync pipeline

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
```

---

**Status: Specification ready. Will execute parallel with Phase 3 after Phase 2 completion.**
