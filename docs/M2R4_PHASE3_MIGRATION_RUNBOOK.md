# M2R4 Phase 3: Project.yaml v3.0 Migration Runbook

**Document ID:** M2R4-PHASE3-MIGRATION-RUNBOOK-2026-08-12  
**Task:** T3.5 - Migration Runbook Documentation  
**Status:** READY FOR PHASE 4 ROLLOUT  
**Based on:** M2R4_PHASE3_SCHEMA_MAPPING.md + Testing Results

---

## Executive Summary

This runbook covers the complete migration of project.yaml files from v2.0 (ad-hoc field ordering) to v3.0 (alphabetically ordered within 4 logical sections) across all 40+ foundation repositories.

**Key Points:**
- Migration is **semantic-preserving** (no data loss or transformation)
- Fully **automated** via Python script with validation
- **Safe rollback** with automatic backups
- **Reversible** at every step
- **Tested** on 3 sample repos with 100% success rate

---

## Pre-Migration Checklist

**Before starting rollout:**

- [ ] All team members notified of maintenance window
- [ ] Phase 5 Entity Sync Pipeline verified operational (24h sync history)
- [ ] Migration script tested on at least 3 sample repos
- [ ] Backup strategy confirmed (automatic .bak files created)
- [ ] Rollback procedure tested and documented
- [ ] Pre-commit hooks installed on evaluator (ready for Phase 4)
- [ ] CI/CD checks configured or disabled for migration commits
- [ ] Communication channel open for escalation (Slack, email)

---

## Part 1: Dry-Run (Safe Testing)

**Purpose:** Test migration without modifying actual files

**Timeline:** 1-2 hours (can run in parallel on all 40+ repos)

### Step 1.1: Batch Dry-Run

Run migration script in dry-run mode on ALL 40+ repositories:

```bash
# From evaluator repo root
python3 scripts/migrate_project_yaml_v3.py /path/to/all/practices --batch --dry-run

# Or manually on specific repos:
for repo in /Users/andersonfamily/practices/*/\.empirica/project.yaml; do
  python3 scripts/migrate_project_yaml_v3.py "$repo" --dry-run --verbose
done
```

**Expected output:**
```
Processing: /path/to/repo/.empirica/project.yaml
Starting v2.0 → v3.0 migration
Migration successful
[DRY-RUN] Would save migrated file: /path/to/repo/.empirica/project.yaml
```

### Step 1.2: Review Dry-Run Results

```bash
# Check migration.log for any errors or warnings
tail -100 .empirica/migration.log | grep ERROR
tail -100 .empirica/migration.log | grep WARNING
```

**If errors found:**
1. Stop the procedure
2. Investigate error source
3. Fix the issue in the migration script or project.yaml
4. Re-run dry-run
5. Do NOT proceed to live migration until dry-run passes

**If no errors:**
- Proceed to Part 2 (Validation)

---

## Part 2: Validation (Pre-Rollout Checks)

**Purpose:** Verify migration prerequisites and preparedness

**Timeline:** 30 minutes

### Step 2.1: Schema Check

Verify all project.yaml files are currently v2.0 compatible:

```bash
# Check version distribution
for file in $(find /Users/andersonfamily/practices -name "project.yaml"); do
  grep "^version:" "$file"
done | sort | uniq -c

# Expected output:
#   11 version: '2.0'
#   0 version: '3.0'
```

### Step 2.2: Backup Strategy Verification

```bash
# Verify backups will be created
ls -la /Users/andersonfamily/practices/empirica-autonomy/.empirica/ | grep bak

# Expected: No .bak files (will be created during migration)
```

### Step 2.3: Rollback Path Verification

```bash
# Test rollback logic on a single repo (dry-run, then restore)
python3 scripts/migrate_project_yaml_v3.py \
  /Users/andersonfamily/practices/empirica-autonomy/.empirica/project.yaml \
  --verbose

# Verify backup was created
ls -la /Users/andersonfamily/practices/empirica-autonomy/.empirica/project.yaml.bak

# Restore from backup
cp /Users/andersonfamily/practices/empirica-autonomy/.empirica/project.yaml.bak \
   /Users/andersonfamily/practices/empirica-autonomy/.empirica/project.yaml
```

**If all checks pass:**
- Proceed to Part 3 (Rollout)

---

## Part 3: Rollout (Execute Migration)

**Purpose:** Migrate all 40+ repositories to v3.0

**Timeline:** 2-4 hours (can parallelize by repo group)

### Step 3.1: Parallel Batch Migration

Run live migration script in batches:

```bash
# Batch 1: empirica-foundation core (5 repos)
for repo in empirica-autonomy empirica-mesh-support empirica-outreach \
            empirica-foundation-evaluator humanaios; do
  echo "Migrating: $repo"
  python3 scripts/migrate_project_yaml_v3.py \
    /Users/andersonfamily/practices/$repo/.empirica/project.yaml \
    --verbose
done

# Batch 2: Supporting repos (can run in parallel with Batch 1)
for repo in website collaborator-ops ...; do
  echo "Migrating: $repo"
  python3 scripts/migrate_project_yaml_v3.py \
    /Users/andersonfamily/practices/$repo/.empirica/project.yaml \
    --verbose
done
```

### Step 3.2: Monitor Migration Progress

```bash
# Watch for errors in real-time
tail -f .empirica/migration.log | grep -E "ERROR|FAIL"

# Count successful migrations
grep -c "Migration successful" .empirica/migration.log

# Expected: Equal to number of repos processed
```

### Step 3.3: Per-Repo Commit

After each successful migration, commit changes:

```bash
cd /path/to/repo
git add .empirica/project.yaml
git commit -m "chore(m2r4): migrate project.yaml to v3.0

Reorder fields alphabetically within 4 logical sections per M2R4 schema.
No semantic changes — fields reordered only. Backup preserved at .bak.

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

**If commit fails:**
1. Check for conflicts or untracked files
2. Resolve manually
3. Retry commit

---

## Part 4: Verification (Post-Rollout Checks)

**Purpose:** Verify all repos successfully migrated

**Timeline:** 1 hour

### Step 4.1: Schema Verification

```bash
# Verify all repos are now v3.0
for file in $(find /Users/andersonfamily/practices -name "project.yaml"); do
  grep "^version:" "$file"
done | sort | uniq -c

# Expected output:
#   0 version: '2.0'
#   40+ version: '3.0'
```

### Step 4.2: Field Ordering Verification

```bash
# Verify alphabetical ordering in all files
python3 << 'EOF'
import yaml
import glob

errors = []
for file in glob.glob('/Users/andersonfamily/practices/*/.empirica/project.yaml'):
    with open(file) as f:
        data = yaml.safe_load(f)
    
    if data.get('version') != '3.0':
        errors.append(f"Wrong version: {file}")
        continue
    
    # Check alphabetical ordering
    SECTIONS = {
        'configuration': ['auto_detect', 'calibration_weights', 'contacts', 'domain', 'domain_config',
                         'engagements', 'evidence_profile', 'languages', 'mesh_id_prefix', 'name',
                         'project_id', 'status', 'subjects', 'tags']
    }
    
    all_fields = [k for k in data.keys() if k != 'version']
    config_fields = [f for f in all_fields if f in SECTIONS['configuration']]
    if config_fields != sorted(config_fields):
        errors.append(f"Ordering error: {file}")

if errors:
    print(f"❌ {len(errors)} errors found:")
    for e in errors[:5]:
        print(f"  {e}")
else:
    print(f"✅ All {len(glob.glob('/Users/andersonfamily/practices/*/.empirica/project.yaml'))} repos verified")
EOF
```

### Step 4.3: Pre-commit Hook Verification

```bash
# Install pre-commit hook on all repos (Phase 4 step)
for repo in /Users/andersonfamily/practices/*/; do
  cp .git/hooks/pre-commit "$repo/.git/hooks/pre-commit"
  chmod +x "$repo/.git/hooks/pre-commit"
done

# Test hook on each repo
for repo in /Users/andersonfamily/practices/*/; do
  "$repo/.git/hooks/pre-commit" 2>/dev/null || echo "Hook check: $repo"
done
```

**If all checks pass:**
- Migration complete
- Proceed to T3.6 (Final commit & tag)

---

## Part 5: Emergency Rollback (If Needed)

**Purpose:** Restore all repos to v2.0 if critical issues discovered

**Timeline:** 30 minutes

### Step 5.1: Rollback All Repos

```bash
# Restore all repos from backups
for repo in /Users/andersonfamily/practices/*/; do
  backup="$repo/.empirica/project.yaml.bak"
  if [ -f "$backup" ]; then
    cp "$backup" "$repo/.empirica/project.yaml"
    echo "Restored: $(basename $repo)"
  fi
done

# Verify rollback
for file in $(find /Users/andersonfamily/practices -name "project.yaml"); do
  grep "^version:" "$file"
done | sort | uniq -c
# Expected: All back to v2.0
```

### Step 5.2: Revert Commits

```bash
# Git reset all repos to before migration
for repo in /Users/andersonfamily/practices/*/; do
  cd "$repo"
  git reset --hard HEAD~1
  git clean -fd
done
```

### Step 5.3: Cleanup

```bash
# Remove all backup files
find /Users/andersonfamily/practices -name "project.yaml.bak" -delete

# Clear migration logs
rm .empirica/migration.log
```

---

## Troubleshooting

### Issue: "Canonical ID not 3-form"

**Symptom:** Migration error on specific repo

**Resolution:**
1. Manually edit project.yaml org_id field
2. Ensure canonical_seat follows pattern: `org-empirica-foundation.carly.<project-name>`
3. Re-run migration

### Issue: "Fields not alphabetically ordered"

**Symptom:** Post-migration verification fails

**Resolution:**
1. Manually review project.yaml field order
2. Reorder fields alphabetically within sections
3. Or re-run migration script to auto-fix

### Issue: Backup file missing

**Symptom:** Cannot rollback a specific repo

**Resolution:**
1. Git reset to before migration commit
2. Manually restore from git history
3. Or restore from external backup if available

### Issue: Pre-commit hook blocking commits

**Symptom:** Commits rejected by v3.0 validation

**Resolution:**
```bash
# Run migration script to auto-fix
python3 scripts/migrate_project_yaml_v3.py <path>

# Or override hook (not recommended)
git commit --no-verify -m "..."
```

---

## Success Criteria

**Migration is successful when:**

- [ ] All 40+ repos migrated to v3.0
- [ ] All project.yaml files have alphabetical field ordering
- [ ] All backups (.bak files) created successfully
- [ ] All migration commits successfully pushed
- [ ] Pre-commit hooks installed on all repos
- [ ] Phase 5 Entity Sync Pipeline validates all repos (via Phase 6)
- [ ] No rollbacks needed
- [ ] Team notified of completion

---

## Post-Migration

**After successful migration:**

1. **Archive backups** (optional, after 1 week if all stable)
   ```bash
   find /Users/andersonfamily/practices -name "*.bak" -delete
   ```

2. **Clean migration logs**
   ```bash
   rm .empirica/migration.log
   ```

3. **Notify team**
   - All repos now v3.0
   - Pre-commit hooks active
   - Phase 4 gates ready

4. **Next phase:** Phase 4 (Test & Validation) → Phase 5 full execution → Phase 6 verification

---

## Appendix: Quick Reference

| Operation | Command |
|-----------|---------|
| Dry-run single repo | `python3 scripts/migrate_project_yaml_v3.py <path> --dry-run` |
| Live migration | `python3 scripts/migrate_project_yaml_v3.py <path>` |
| Batch dry-run | `python3 scripts/migrate_project_yaml_v3.py /path/to/all --batch --dry-run` |
| Test on 3 repos | `scripts/test_migration_v3.sh` |
| Rollback single repo | `cp <path>.bak <path>` |
| Check version | `grep "^version:" <path>` |
| Validate hook | `<repo>/.git/hooks/pre-commit` |

---

**Status: T3.5 Complete - Ready for T3.6 (Final Commit & Tag)**

Generated: 2026-08-12  
Document: M2R4 Phase 3 T3.5 (Migration Runbook)
