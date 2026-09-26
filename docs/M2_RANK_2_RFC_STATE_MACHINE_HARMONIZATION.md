# M2 Rank 2: State Machine Harmonization RFC

**Document ID:** M2R2-RFC-2026-07-23-STATE-MACHINE  
**Status:** ⏳ AWAITING ADMIRAL APPROVAL  
**Submitted by:** empirica-foundation-evaluator (spec-prep fork)  
**Submission Date:** 2026-07-23  
**Target Decision Date:** 2026-07-25  
**Audience:** Admiral (Carly), M2 Rank 2 executor, all 40+ foundation practices

---

## Executive Summary

Across the 40+ empirica-foundation repositories, state machines (goal states, proposal statuses, project phases, decision workflows) use inconsistent naming and transition logic. This RFC proposes a unified state machine model that standardizes naming (active|completed|planned|archived), transition rules, and validation, enabling cross-repo state synchronization without behavioral surprises. Harmonization is a prerequisite for M3 (Witness state sync infrastructure) and future autonomy decisions.

---

## Current State: What's Broken

### Naming Inconsistencies (Sampled Across 5+ Repos)

| Repo | Entity | State Names | Problem |
|------|--------|------------|---------|
| empirica-autonomy | goal | `active`, `inactive`, `closed` | No archive tier; `inactive` vs `completed` ambiguous |
| empirica-outreach | proposal | `pending`, `approved`, `executed`, `rejected` | 5-state vs 4-state models don't map |
| empirica-mesh-support | decision | `open`, `decided`, `archived` | No `planned` tier; unclear if `decided` = executed |
| empirica-autonomy | engagement | `active`, `suspended`, `completed` | `suspended` not in other repos |
| humanaios | collaboration | `draft`, `ratified`, `live`, `end_of_life` | Domain-specific; doesn't fit foundation pattern |

**Impact:** Queries like "list all active goals across practices" require per-practice translation. Multi-practice workflows (where one repo checks another's state) are error-prone.

### Transition Logic Gaps

**Current:** Each practice defines state transitions ad-hoc.
- autonomy: no explicit `planned → active` transition rule
- outreach: no rollback path from `executed` back to `pending` for amendments
- mesh-support: `archived` is terminal; no way to reopen old decisions for audit trail extension

**Impact:** State machines are implicit and undocumented. Automatic transitions (e.g., goal auto-completion based on task progress) don't exist — requires manual intervention or silent failures.

### Validation & Guards

**Current:** State machines have no formal guards or preconditions.
- No validation that `archived` entities contain required audit metadata before archival
- No check that a goal's tasks are complete before allowing `goal → completed`
- No enforcement that decision rationale exists before `decision → decided`

**Impact:** Invalid state transitions silently succeed, leading to data integrity issues discovered only at audit time.

---

## Proposed Unified Model

### Core State Machine (4-Tier)

All foundation entities follow this state lifecycle:

```
[planned] ──→ [in_progress] ──→ [completed] ──→ [archived]
   ↑                                  ↑
   └──────── [reopen] ─────────────┘
```

### State Definitions

| State | Meaning | Example | Persistence |
|-------|---------|---------|-------------|
| **planned** | Queued, approved for future work, not yet active | Goal created with `--status planned`; awaiting decision gate | Visible in list; lower priority |
| **in_progress** | Actively being worked or awaiting approval | Goal in execution; proposal under review | Hot; high priority |
| **completed** | Finished, awaiting archival decision | Goal closed; proposal executed + verified | Visible but low priority; audit tier |
| **archived** | Moved to cold storage; no longer in active workflows | Goals >30 days complete; historical decisions | Hidden by default; restorable via `--include-archived` |

### Transition Rules (Explicit Preconditions)

| Transition | Precondition | Guard | Post-Action |
|-----------|--------------|-------|------------|
| `planned → in_progress` | Approval gate (Z2 authority doc or CHECK pass) | Verify: timestamp, authorizer UUID | Update `started_at` |
| `in_progress → completed` | All tasks closed OR explicit completion signal | Verify: task count match, evidence logged | Update `completed_at`, trigger audit ledger |
| `completed → archived` | Retention window expired (30d default, configurable) | Verify: audit metadata present, no open edges | Update `archived_at`, move to cold storage |
| `archived ← *` | Reopen request (manual, with reason) | Verify: reopener has authority, reason logged | Restore to prior state, log `reopened_at` + reason |
| `in_progress ← completed` | Rollback (manual, e.g., failed P3 verification) | Verify: rollback authority, reason documented | Restore to `in_progress`, log decision-log |

### Schema Changes (project.yaml + database)

**New fields on all entities (goal, proposal, decision, engagement, project):**

```yaml
state: in_progress                    # active state
state_timestamps:
  planned_at: 1721755200             # Unix timestamp
  started_at: 1721758800
  completed_at: null
  archived_at: null
state_audit:
  transitions: []                     # [{from, to, timestamp, authorizer, reason}]
  metadata:
    completion_evidence: "commit abc1234, test results 100%"
    archive_reason: "age > 30d"
```

**Database indices:**
```sql
CREATE INDEX idx_state ON entities(state);
CREATE INDEX idx_state_started_at ON entities(started_at);
CREATE INDEX idx_state_completed_at ON entities(completed_at);
```

---

## Migration Path

### Phase 1: Inventory & Mapping (1 day)

Scan all 40+ repos and generate a state-mapping table:
```
repo → entity_type → current_states → proposed_state → conflicts
```

**Tool:** `empirica-find-state-machines` CLI (to be built) or manual grep for state-related fields.

**Output:** `state_migration_manifest.yaml` (reference for Phase 2).

### Phase 2: Feature-Branch Harmonization (2 days, parallel per repo)

For each repo:
1. Create feature branch `feature/m2r2-state-harmonization`
2. Update state machine model file (or create if missing)
3. Migrate existing state values using manifest mapping
4. Add validation guards (ensure preconditions before transitions)
5. Run test suite (must pass 100%)
6. Commit with reference to M2 Rank 2 authority

**Non-breaking:** Old code reading `state == 'inactive'` still works (alias mapping in compatibility layer for 1 release cycle).

### Phase 3: Verification & Testing (1 day)

Run cross-repo state queries to verify:
- All repos now return states in `{planned, in_progress, completed, archived}`
- Transition guards prevent invalid state changes
- Audit metadata is populated on every transition

**Test suite:** `tests/state_machine_harmonization_test.py` (template to follow).

### Phase 4: Rollout & Archive (1 day)

1. Merge all feature branches
2. Deploy to staging (full integration test)
3. Production rollout (rolling, 5 repos/hour)
4. Monitor: watch for state-related exceptions in logs
5. After 7 days: remove compatibility layer, commit cleanup

**Rollback:** If any repo fails P3 verification, revert that repo's branch (safe due to feature-branch isolation).

---

## Verification & Testing

### Unit Tests (per-repo)

**File:** `tests/state_machine/test_harmonized_states.py`

```python
def test_planned_to_in_progress():
    # PRECONDITION: authority doc exists
    authority = create_authority("Approved for execution")
    goal = Goal(state="planned", authority_id=authority.id)
    
    goal.transition("in_progress")
    assert goal.state == "in_progress"
    assert goal.state_timestamps.started_at is not None

def test_invalid_transition_blocked():
    goal = Goal(state="planned")
    with pytest.raises(InvalidStateTransition):
        goal.transition("archived")  # blocked: can't skip in_progress + completed

def test_reopen_restores_state():
    goal = Goal(state="archived")
    goal.reopen("Needs audit trail extension")
    assert goal.state == "completed"  # restored to prior
    assert goal.state_audit.transitions[-1].reason == "Needs audit trail extension"
```

### Integration Tests (cross-repo)

**File:** `tests/state_machine/test_cross_repo_state_sync.py`

```python
def test_all_repos_use_unified_states():
    # Query all repos, verify state ∈ {planned, in_progress, completed, archived}
    states_found = set()
    for repo in all_foundation_repos():
        goals = repo.query_all_goals()
        for goal in goals:
            states_found.add(goal.state)
    
    valid_states = {"planned", "in_progress", "completed", "archived"}
    assert states_found.issubset(valid_states)

def test_goal_completion_triggers_audit():
    goal = Goal(state="in_progress")
    goal.complete(evidence="commit abc1234")
    
    assert goal.state == "completed"
    assert goal.state_audit.metadata.completion_evidence == "commit abc1234"
    assert audit_log.find(goal.id) is not None
```

### Audit Tests (governance)

Verify that state transitions respect M2 Rank 1 authority rules:
- `planned → in_progress` requires Z2 authority (CHECK gate pass)
- `→ archived` requires audit metadata (per ESCALATION_PROTOCOL)
- Rollback (`→ in_progress` from completed) logged as decision-log

---

## Verification Checklist

- [ ] State mapping inventory complete (all 40+ repos scanned)
- [ ] Feature branches pass unit tests (100% pass rate)
- [ ] Cross-repo integration test passes (unified states confirmed)
- [ ] Audit logs show all transitions + metadata
- [ ] Staging deployment successful (7-day burn-in)
- [ ] Production rollout complete (zero failures)
- [ ] Rollback procedure tested (at least one repo exercised)
- [ ] Compatibility layer removed + cleanup commit merged
- [ ] POSTFLIGHT + grounded calibration submitted

---

## Reversibility

### Full Rollback (if needed)

If the harmonization fails during rollout:
1. Revert all feature branches (git revert)
2. Restore original state machines from git history
3. Re-run tests to confirm original behavior
4. Emit decision-log + mistake-log (root cause analysis)

**Window:** Reversible up to 7 days post-staging. After production "bake-in" period (7 days), rollback requires data migration (higher cost).

### Partial Rollback (repo-level)

If one repo's state transitions cause regressions:
1. Revert that repo's feature branch only (others remain harmonized)
2. Flag in `state_migration_manifest.yaml` as "rollback_pending"
3. Re-assess preconditions (may indicate invalid state model for that domain)

### Compatibility Layer (1-release grace period)

Old code querying `state == 'inactive'` continues to work via aliasing:
```python
state_aliases = {
    'inactive': 'completed',
    'closed': 'completed',
    'suspended': 'in_progress'
}
```

After 1 release cycle (30 days), aliases are removed (forces code update).

---

## Risk Assessment

### Low Risk

- **Backward compatible for 30 days** — Alias layer masks old state names, code still works
- **Feature-branch isolation** — Each repo's changes are isolated until merge; failures don't cascade
- **Explicit guard preconditions** — Invalid transitions fail fast with clear error messages

### Medium Risk

- **40+ repos affected** — Coordination across multiple teams. **Mitigation:** Parallel execution, clear rollback window.
- **State-dependent automation** — Scheduled jobs (e.g., "auto-archive goals completed >30d") must account for new state machine. **Mitigation:** Test automation in staging first.

### Monitoring During Rollout

1. **Log state-transition exceptions** — Alert on any `InvalidStateTransition` or guard violations
2. **Track rollback requests** — Any repo requesting rollback signals a problem
3. **Query latency** — Ensure new indices don't slow down `list_goals` queries
4. **Audit completeness** — Sample 5 repos; verify 100% of transitions logged

---

## Timeline

| Phase | Duration | Effort | Dependencies |
|-------|----------|--------|--------------|
| P1: Inventory | 1 day | 4h | None — can start immediately |
| P2: Harmonization (parallel) | 2 days | 4h/repo × ~40 repos (parallelizable) | P1 manifest |
| P3: Verification | 1 day | 8h | P2 complete |
| P4: Rollout | 1 day | 4h + monitoring | P3 passed |
| **Total** | **5 days** | **~60h** (parallelizable to **3 days** at 10 repos/day) | M2 Rank 1 ratified ✅ |

---

## Glossary

| Term | Definition |
|------|-----------|
| **State Machine** | Defined set of states + explicit transition rules (preconditions, guards, post-actions) |
| **Precondition** | Requirement that must be true before a transition is allowed (e.g., CHECK gate passed) |
| **Guard** | Validation that blocks invalid transitions + logs reason |
| **Audit Trail** | Immutable log of state transitions (from, to, timestamp, authorizer, reason) |
| **Feature Branch** | Git branch isolated from main; allows harmonization per-repo without affecting others |
| **Compatibility Layer** | Temporary aliases (old_state → new_state) to unblock code that still references old state names |

---

## References

- **Authority:** AUTHORITY_MAPPING_Z3_EMPIRICA_V1.md (Zone 3 execution rules)
- **Authority Matrix:** AUTHORITY_MATRIX.yaml (escalation rules)
- **Escalation Protocol:** ESCALATION_PROTOCOL.md (when to escalate state-related issues)
- **Next Rank:** M2 Rank 3 (Registry Harmonization) depends on this RFC's state definitions

---

**Status: ⏳ AWAITING ADMIRAL APPROVAL**

This RFC is ready for Admiral decision. Once approved, Phase 1 (inventory) can begin immediately.
