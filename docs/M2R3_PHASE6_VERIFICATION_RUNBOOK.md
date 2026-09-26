# M2 Rank 3: Phase 6 Verification & Testing Runbook

**Document ID:** M2R3-PHASE6-RUNBOOK-2026-08-07  
**Status:** READY FOR EXECUTION  
**Trigger:** Phase 5 sync pipeline operational (running hourly)  
**Timeline:** 1-2 days  
**Depends on:** Phase 5 (sync pipeline running + 24h of change logs)

---

## Phase 6 Overview

Run verification suite against entity_registry after Phase 5 has been syncing for ≥24 hours. Validate:
- All 22+ entities present + current
- All 51+ relationships intact
- No orphaned records
- No duplicate canonical_identifiers
- All conflicts logged (if any)

---

## Verification Checklist

### 6.1 Entity Counts

```bash
# Expected counts (from Phase 3-4):
# - Projects: 6 (all foundation practices)
# - Contacts: 15+ (contributors + owners + Admiral)
# - Engagements: 8+ (active research + infrastructure)
# - Organizations: 2 (empirica-foundation, empirica)
```

**Verification:**
```bash
empirica entities-count --type project
# Expected: 6

empirica entities-count --type contact
# Expected: ≥15

empirica entities-count --type engagement
# Expected: ≥8

empirica entities-count --type organization
# Expected: 2
```

**Pass Criteria:** Within ±1 of expected counts (minor discovery variance acceptable)

---

### 6.2 Sync Log Audit

**Location:** `.empirica/sync.log` (append-only, Phase 5 generates)

**Verify:**
- ✓ No ERROR level entries (warnings OK)
- ✓ Hourly entries for each sync task (≥24 hours = ≥24 project syncs)
- ✓ All timestamps in UTC (ISO format)
- ✓ No truncated lines (complete records)

**Sample log lines:**
```
2026-08-07T01:00:00Z | INFO | Sync Task 1: Projects
2026-08-07T01:00:00Z | INFO | Discovered 6 project.yaml files
2026-08-07T01:00:15Z | INFO | Project synced: canonical_id=empirica-foundation.carly.empirica-autonomy, ai_id=empirica-autonomy, hash=a1b2c3d4...
2026-08-07T01:00:15Z | INFO | Sync Task 2: Contacts
2026-08-07T01:00:15Z | INFO | Extracted 14 contacts from git log
2026-08-07T01:00:20Z | INFO | Contact synced: email=carly@example.com, name=Carly Anderson
...
```

**Pass Criteria:** ≥24 complete sync cycles with no ERRORS

---

### 6.3 Relationship Integrity

**Verify:**
- No orphaned projects (every project references existing org)
- No orphaned contacts (every contact referenced exists)
- No orphaned engagements (all serves relationships point to existing projects)
- No circular relationships (acyclic graph)

**Query template:**
```bash
empirica entities-edges --from-type project --to-type organization
# Expected: 6 projects → 1 organization (empirica-foundation)

empirica entities-edges --from-type engagement --to-type project
# Expected: all engagement.serves edges point to registered projects

empirica entities-edges --find-orphans
# Expected: 0 orphaned edges
```

**Pass Criteria:** Zero orphaned edges, zero circular relationships

---

### 6.4 Canonical Identifier Uniqueness

**Verify:** No two entities share the same canonical_id (database constraint, but verify)

```bash
empirica entities-canonical-ids --check-duplicates
# Expected output: "No duplicates found"
```

**Pass Criteria:** Zero duplicate canonical_identifiers

---

### 6.5 Conflict Log Review

**Location:** `.empirica/sync.log` (search for CONFLICT)

**If conflicts present:**
- Log entry format: `[timestamp] | CONFLICT | description`
- Example: `CONFLICT | canonical_id collision: ai_id1=empirica-autonomy, ai_id2=autonomy`

**Action:**
- Review each conflict (Admiral to resolve manually per spec)
- Document resolution in separate CONFLICTS_RESOLVED.md
- Re-sync after resolution (manual trigger: `python scripts/sync_entity_registry.py`)

**Pass Criteria:** Zero conflicts, OR all conflicts documented + resolved

---

### 6.6 Change Log Summary

**Generate:** Daily summary from sync.log

```bash
cat .empirica/sync.log | grep "Project synced\|Contact synced\|Engagement synced" | wc -l
# Expected: ≥72 (24 hours × 3 tasks/hour)
```

**Sample report:**
```
=== Sync Summary (24h Period: 2026-08-07 00:00 UTC → 2026-08-08 00:00 UTC) ===
Projects: 6 synced, 0 changes
Contacts: 14 synced, 2 new (discovered via git log)
Engagements: 8 synced, 0 changes
Organizations: 2 verified, 0 changes
Sync cycles: 24 completed
Conflicts: 0
Orphaned edges: 0
---
Status: ✓ All checks passed
```

**Pass Criteria:** All fields present, status = PASSED

---

## Test Procedures

### Test 1: Project Discovery & Update

**Procedure:**
1. Modify a practice's `.empirica/project.yaml` (e.g., add a tag)
2. Run sync: `python scripts/sync_entity_registry.py` (or wait for next hourly run)
3. Verify sync.log contains project update entry
4. Query registry: `empirica entity-get --canonical-id <practice>.carly.<ai_id>`
5. Confirm tag present in retrieved entity

**Expected:** Project update logged within 1 minute

---

### Test 2: Contact Discovery via Git Log

**Procedure:**
1. Create a new commit with an unknown author: `git commit --author="Test User <test@example.com>" --allow-empty -m "test"`
2. Run sync: `python scripts/sync_entity_registry.py`
3. Verify sync.log contains contact discovery entry
4. Query registry: `empirica entity-get --canonical-id test@example.com`
5. Confirm contact created with authority_tier=member

**Expected:** Contact discovered within 1 minute

---

### Test 3: Conflict Handling

**Procedure:**
1. Create a conflict: manually insert duplicate canonical_id into registry (test data)
2. Run sync
3. Verify sync.log contains CONFLICT entry
4. Verify conflict is logged but sync continues (doesn't crash)
5. Clean up: remove test data

**Expected:** Conflict logged, sync continues gracefully

---

### Test 4: Orphan Detection

**Procedure:**
1. Delete a practice from filesystem
2. Keep its entity in registry (orphan)
3. Run validation: `empirica entities-check --find-orphans`
4. Verify orphan is detected and logged

**Expected:** Orphan detected and reported

---

## Verification Sign-Off

**When all checks pass:**

```bash
empirica goals-complete-task --task-id 474da330-b077-4a17-9df0-8109eea4274e \
  --evidence "M2R3 Phase 6 verification complete: sync log audit ✓, entity counts ✓, relationship integrity ✓, canonical uniqueness ✓, 0 conflicts, 4/4 test procedures passed"
```

**Completion artifact:**
- Commit: Phase 6 test results
- Log: Verification checklist (screenshot or txt export from sync.log)
- Decision: M2R3 complete → Ready for Phase 7 (governance automation)

---

## Phase 7 Preview

After Phase 6 verification passes:
- **Phase 7:** Governance automation (CI/CD hooks for governance doc sync, schema validation)
- **Phase 8:** Cross-practice entity synchronization status dashboard
- **Phase 9:** Automated alerts on schema violations (pre-commit hook failures)

---

## Troubleshooting

### Sync cycles not appearing in log

**Check:**
- Is sync_entity_registry.py running? `pgrep -f sync_entity_registry`
- Is .empirica/sync.log writable? `ls -la .empirica/sync.log`
- Are project.yaml files discoverable? `find . -name project.yaml | wc -l`

**Fix:** Restart sync process or run manually: `python scripts/sync_entity_registry.py`

---

### Entity counts don't match expected

**Check:**
- Did a practice get added/removed?
- Did contributors change (new git author)?
- Is git log accessible? `git log --format=%aE | wc -l`

**Fix:** Update expected counts + log delta in VERIFICATION_SUMMARY.md

---

### Conflicts detected

**Check:**
- Which canonical_ids collide? (check sync.log for CONFLICT entries)
- Are there duplicate email addresses (case-sensitive bug)?
- Are there ai_id duplicates across practices?

**Fix:** Review conflict log → Admiral decision → manual entity merge/dedup → re-sync

---

## Commit Message (Phase 6 Complete)

```
feat(m2r3): phase 6 verification — entity registry validation

Completed M2R3 Phase 6 verification suite:
- Entity counts: 6 projects, 15+ contacts, 8+ engagements, 2 organizations
- Sync log audit: 24+ complete cycles, 0 errors
- Relationship integrity: 0 orphaned edges, 0 circular references
- Canonical identifier uniqueness: 0 duplicates
- Conflict log: 0 conflicts (or all resolved)
- Test procedures: 4/4 passed

Verification sign-off: All checks passed, M2R3 ready for production.
Next: Phase 7 (governance automation)

Authority: M2 Rank 3 RFC, Phase 6/6
Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
```

---

**Status: Specification ready. Execute after Phase 5 has logged ≥24 hours of sync activity.**
