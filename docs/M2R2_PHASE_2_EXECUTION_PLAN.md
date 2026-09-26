# M2 Rank 2: Phase 2 Execution Plan
## State Machine Harmonization Across Repositories

**Document ID:** M2R2-PHASE2-PLAN-2026-07-23  
**Status:** IN PROGRESS  
**Approved by:** Admiral Carly R. Anderson (2026-07-23)  
**Timeline:** 2-3 days (parallel harmonization) + 1 day verification = 5 days total  
**Authority:** M2 Rank 2 RFC + Phase 1 State Migration Manifest

---

## Execution Strategy

**Parallel Batches:** 5 parallel harmonization tracks + main coordination

| Batch | Repos | Entity-Types | Lead | Timeline |
|-------|-------|--------------|------|----------|
| **Batch 1** | empirica-autonomy | goals, engagements | Fork Agent A | Day 1-2 |
| **Batch 2** | empirica-outreach | proposals, documents | Fork Agent B | Day 1-2 |
| **Batch 3** | empirica-mesh-support | decisions | Fork Agent C | Day 1-2 |
| **Batch 4** | humanaios | collaborations, projects | Fork Agent D | Day 1-2 |
| **Batch 5** | other practices | goals (p3-verify tier) | Fork Agent E | Day 2 |
| **Main** | coordination, integration, verification | — | This session | Day 1-4 |

---

## Phase 2 Tasks per Batch

### For Each Batch / Repo:

1. **Create feature branch** `feature/m2r2-state-harmonization-{repo-name}`
2. **Update state machine model(s):**
   - Add 4-tier states enum/constants (if not present)
   - Create state_timestamps schema (planned_at, started_at, completed_at, archived_at)
   - Create state_audit schema (transitions, metadata)
   - Add database indices
3. **Implement transition guards:**
   - planned → in_progress requires: approval gate (Z2 doc or CHECK pass)
   - in_progress → completed requires: all tasks closed or explicit signal
   - completed → archived requires: 30d retention window + audit metadata
   - archived ← * requires: reopen request with reason
   - in_progress ← completed requires: rollback authority + reason
4. **Migrate existing state values:**
   - Use mapping from M2R2_STATE_MIGRATION_MANIFEST.yaml
   - Script: `scripts/migrate_states_{entity_type}.py` (template provided)
   - Verify: count before/after matches
5. **Add compatibility layer** (if required):
   - Alias mapping for old state names (1 release cycle)
   - Logging: warn when old names used
6. **Unit tests:**
   - Test all state transitions
   - Test guards (valid transitions pass, invalid fail)
   - Test migration (no data loss, count matches)
   - 100% pass required before commit
7. **Integration tests** (cross-repo queries):
   - "List all in_progress goals across practices" ← should return unified state
   - "Transition goal from planned → archived" ← should respect guards
8. **Commit** with reference to M2 Rank 2 authority:
   ```
   feat({repo-short}): m2r2 state machine harmonization

   Unified 4-tier state model: planned → in_progress → completed → archived.
   Implement transition guards, audit trail, state timestamps.
   Migrate existing states per M2R2_STATE_MIGRATION_MANIFEST.

   - Update state enum/schema
   - Add state_timestamps and state_audit fields
   - Implement transition guards and validation
   - Migrate {N} existing entities
   - Add unit tests (100% pass)

   References: M2R2_RFC_STATE_MACHINE_HARMONIZATION.md
   Authority: M2 Rank 2 (Admiral ratified M2 Rank 1)

   Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
   ```

---

## Batch Details

### Batch 1: empirica-autonomy (Goals + Engagements)

**Current states:**
- goals: active, inactive, closed, on-hold → unified: in_progress, planned, completed, planned
- engagements: active, suspended, completed → unified: in_progress, planned, completed

**Files to update:**
- `src/models/goal.py` (state enum, schema)
- `src/models/engagement.py` (state enum, schema)
- `database/migrations/m2r2_goal_state.sql` (schema + indices)
- `database/migrations/m2r2_engagement_state.sql`
- `scripts/migrate_states_goal.py` (data migration)
- `scripts/migrate_states_engagement.py`
- `tests/state_machine_test.py` (new)

**Estimated effort:** 2-3 hours

---

### Batch 2: empirica-outreach (Proposals + Documents)

**Current states:**
- proposals: pending, approved, executed, rejected, withdrawn → unified: planned, in_progress, completed, archived, archived
- documents: draft, published, deprecated, retired → unified: planned, in_progress, completed, archived

**Files to update:**
- `src/models/proposal.py`
- `src/models/document.py`
- `database/migrations/m2r2_proposal_state.sql`
- `database/migrations/m2r2_document_state.sql`
- `scripts/migrate_states_proposal.py`
- `scripts/migrate_states_document.py`
- `tests/state_machine_test.py`

**Estimated effort:** 2-3 hours

---

### Batch 3: empirica-mesh-support (Decisions)

**Current states:**
- decisions: open, decided, archived, disputed → unified: in_progress, completed, archived, in_progress

**Files to update:**
- `src/models/decision.py`
- `database/migrations/m2r2_decision_state.sql`
- `scripts/migrate_states_decision.py`
- `tests/state_machine_test.py`

**Estimated effort:** 1-2 hours

---

### Batch 4: humanaios (Collaborations + Projects)

**Current states:**
- collaborations: draft, ratified, live, end_of_life → unified: planned, in_progress, in_progress, archived
- projects: conception, active, paused, complete, archived → unified: planned, in_progress, in_progress, completed, archived

**Files to update:**
- `src/models/collaboration.py`
- `src/models/project.py`
- `database/migrations/m2r2_collaboration_state.sql`
- `database/migrations/m2r2_project_state.sql`
- `scripts/migrate_states_collaboration.py`
- `scripts/migrate_states_project.py`
- `tests/state_machine_test.py`

**Estimated effort:** 2-3 hours

---

### Batch 5: Other Practices (Goals - p3 verify)

**Current states:**
- goals: planned, in_progress, completed (already aligned!)

**Actions:**
- Add archived tier (simple, non-breaking)
- Add state_timestamps and state_audit fields
- No data migration needed
- Verification tests only

**Estimated effort:** 1 hour per repo

---

## Phase 3: Verification (Day 4)

After all batches complete harmonization:

1. **Run cross-repo state queries:**
   ```sql
   SELECT repo, entity_type, state, COUNT(*) as count
   FROM entities
   WHERE state IN ('planned', 'in_progress', 'completed', 'archived')
   GROUP BY repo, entity_type, state;
   -- Expected: 0 entities in non-unified states
   ```

2. **Test suite:**
   - `tests/m2r2_state_harmonization_test.py` (template in RFC)
   - Verifies: all 4-tier states present, guards enforced, transitions work
   - Coverage: goals, engagements, proposals, decisions (main entity types)

3. **Regression testing:**
   - Run full test suite for each repo (100% pass required)
   - Check logs for state-related warnings/errors

4. **Admiral verification:**
   - Admiral reviews results
   - Approves rollout (or requests fixes)

---

## Phase 4: Rollout & Archive (Day 5)

1. **Merge all feature branches** → main
2. **Tag release:** `m2r2-state-harmonization-v1.0`
3. **Deploy to staging** (full integration test)
4. **Production rollout** (rolling, 5 repos/hour, 40+ repos = 8 hours)
5. **Monitor:**
   - Watch logs for state-related exceptions
   - Verify no data corruption
   - Check cross-repo queries working
6. **After 7 days:** Remove compatibility layer (old state names no longer aliased)
7. **Commit cleanup:** `chore(m2r2): remove state compatibility layer`

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Data loss during migration | Pre-migration audit (count), post-migration count verification, rollback branch ready |
| Breaking changes in API | Compatibility layer (1 release), deprecation warnings logged |
| Test suite failures | Required: 100% pass before commit; failing commits blocked |
| Cross-repo inconsistency | Phase 3 verification queries; Admiral review |
| Rollback needed | Full rollback branch exists; can revert merged commits if needed |

---

## Deliverables Checklist

- [ ] All feature branches created and harmonization started
- [ ] Batch 1 (autonomy) complete + merged
- [ ] Batch 2 (outreach) complete + merged
- [ ] Batch 3 (mesh-support) complete + merged
- [ ] Batch 4 (humanaios) complete + merged
- [ ] Batch 5 (other practices) complete + merged
- [ ] Phase 3 verification tests passing
- [ ] Cross-repo state queries returning unified states
- [ ] Admiral approval for production rollout
- [ ] Production rollout complete (40+ repos)
- [ ] 7-day compatibility window completed
- [ ] Cleanup commit (remove alias layer)

---

## Success Criteria

✅ **M2 Rank 2 Phase 2 Complete When:**
1. All 40+ repos have unified 4-tier states (planned, in_progress, completed, archived)
2. Transition guards enforced across all entity types
3. State audit trails populated on every transition
4. Cross-repo state queries work without per-repo translation
5. Test coverage 100% (unit + integration)
6. Admiral approves rollout results
7. Production deployment stable (7+ days, no rollbacks)

---

**Status: Ready to begin. Parallel batches launching now.**
**Coordination point: This session (main coordinator).**
**Expected completion: 2026-07-28 (5 days from start).**
