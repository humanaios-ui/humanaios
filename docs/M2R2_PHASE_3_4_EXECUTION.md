# M2 Rank 2: Phase 3 & 4 Execution Plan
## Verification + Rollout (2-3 Days)

**Document ID:** M2R2-PHASE34-EXEC-2026-07-23  
**Status:** IN EXECUTION  
**Approved by:** Admiral Carly R. Anderson (2026-07-23)  
**Authority:** M2 Rank 2 RFC + Admiral approval  
**Timeline:** Phase 3 (1 day) + Phase 4 (1-2 days) = 2-3 days total

---

## Phase 3: Verification (1 Day)

### 3.1 Test Suite Execution

**Test File:** `tests/m2r2_verification_suite.py`

**4 Core Tests:**

| # | Test | Purpose | Pass Criteria |
|---|------|---------|---------------|
| 1 | Unified States Present | Verify all 4 states (planned, in_progress, completed, archived) exist in each entity type | All 4 states found OR table empty (fresh) |
| 2 | No Legacy States | Verify old state names (active, inactive, closed, draft, etc.) are gone | 0 legacy states in any repo |
| 3 | State Timestamps | Verify state_timestamps field exists and is populated | Column present + some entries have timestamps |
| 4 | State Audit Trail | Verify state_audit field exists for transition tracking | Column present |

**Execution:**
```bash
cd /Users/andersonfamily/practices/empirica-foundation-evaluator
python3 tests/m2r2_verification_suite.py
```

**Expected Output:**
```
M2 RANK 2 PHASE 3: VERIFICATION SUITE
======================================

--- GOALS ---
✓ goals: All unified states present
✓ goals: No legacy states found
✓ goals: State timestamp field present
✓ goals: State audit field present
  Entities: [N]

--- ENGAGEMENTS ---
✓ engagements: All unified states present
✓ engagements: No legacy states found
✓ engagements: State timestamp field present
✓ engagements: State audit field present
  Entities: [N]

--- COLLABORATIONS ---
✓ collaborations: All unified states present
✓ collaborations: No legacy states found
✓ collaborations: State timestamp field present
✓ collaborations: State audit field present
  Entities: [N]

--- PROJECTS ---
✓ projects: All unified states present
✓ projects: No legacy states found
✓ projects: State timestamp field present
✓ projects: State audit field present
  Entities: [N]

RESULTS: 16 passed, 0 failed
======================================
✓ Phase 3 Verification: PASS (All tests passed)
```

**Success Criteria:**
- All 4 entity types pass all 4 tests
- 0 failures
- Cross-repo queries work without per-repo translation

### 3.2 Verification Checkpoints

**Checkpoint 1: Code Review**
- [ ] Review harmonization commits (fe315f6 autonomy, 4b23603 humanaios)
- [ ] Verify: state enum/schema updated
- [ ] Verify: transition guards implemented
- [ ] Verify: migration scripts executed
- [ ] Verify: tests passing

**Checkpoint 2: Database State**
- [ ] All goals use unified states (0 legacy states)
- [ ] All engagements use unified states (0 legacy states)
- [ ] All collaborations use unified states (0 legacy states)
- [ ] All projects use unified states (0 legacy states)

**Checkpoint 3: Cross-Repo Integrity**
- [ ] Query "SELECT DISTINCT state FROM goals UNION SELECT DISTINCT state FROM collaborations" returns only {planned, in_progress, completed, archived}
- [ ] No queries need per-repo translation logic
- [ ] Audit metadata present on recent transitions

---

## Phase 4: Rollout (1-2 Days)

### 4.1 Merge & Release

**Step 1: Create Release Branch**
```bash
git checkout -b release/m2r2-state-harmonization-v1.0
git merge feature/m2r2-state-harmonization-autonomy
git merge feature/m2r2-state-harmonization-humanaios
```

**Step 2: Verify All Tests Pass**
```bash
# Run full test suite (all practices)
pytest tests/m2r2_verification_suite.py -v
pytest tests/test_m2r2_state_machine.py -v  # from autonomy fork
pytest tests/state_machine_test.py -v       # from humanaios fork
```

**Pass Requirement:** 100% of tests pass before proceeding

**Step 3: Tag Release**
```bash
git tag -a m2r2-state-harmonization-v1.0 \
  -m "M2 Rank 2 State Machine Harmonization v1.0

Unified 4-tier state model (planned, in_progress, completed, archived)
across 4 core entity types: Goals, Engagements, Collaborations, Projects.

Includes transition guards, audit trails, state timestamps.
Compatibility layer enabled (1 release cycle).

Commits:
- fe315f6 (empirica-autonomy)
- 4b23603 (humanaios)

Authority: M2 Rank 2 RFC, Admiral approved 2026-07-23"

git push origin m2r2-state-harmonization-v1.0
```

**Step 4: Merge to Main**
```bash
git checkout main
git merge release/m2r2-state-harmonization-v1.0
```

### 4.2 Deployment

**Deployment Phase 1: Staging (12 hours)**
- Deploy release tag to staging environment
- Run full integration test suite
- Verify: cross-repo state queries work
- Verify: no data loss during migration
- Verify: API responses include new state fields

**Deployment Phase 2: Production (8 hours, rolling)**
- Rolling deployment: 5 repos/hour
- Sequence:
  1. Hour 1: empirica-autonomy (goals, engagements)
  2. Hour 2: humanaios (collaborations, projects)
  3. Hour 3-8: Remaining practices
  
- Monitoring during each deploy:
  - Watch logs for state-related exceptions
  - Monitor API response times (should be stable)
  - Check for data corruption signals
  - Verify cross-repo queries work

### 4.3 Monitoring & Validation (7 Days)

**Days 1-7 Post-Deployment:**
- [ ] Daily: Check logs for state-related errors (should be 0)
- [ ] Daily: Run verification suite against production DBs
- [ ] Daily: Spot-check cross-repo queries
- [ ] Track: Any rollback requests or emergency fixes

**Go/No-Go Decision Points:**

| Day | Decision | Criteria |
|-----|----------|----------|
| Day 1 (end of shift) | Continue or Rollback | No critical state-related errors; queries working |
| Day 3 | Continue or Pause | < 5 reported issues; no data corruption |
| Day 7 | Compatibility Layer Removal | All systems stable; no legacy state references |

**If Issues Found:**
1. Log as incident (date, time, symptom, affected entities)
2. If critical: Rollback to prior release
3. If minor: Fix + redeploy in next cycle
4. All incidents reviewed at POSTFLIGHT

### 4.4 Cleanup (After 7-Day Window)

**Step 1: Remove Compatibility Layer**
```bash
# Remove old state name aliases
# Remove deprecation warnings
# Update any remaining code references

Commit: chore(m2r2): remove state compatibility layer
```

**Step 2: Archive Feature Branches**
```bash
git branch -d feature/m2r2-state-harmonization-autonomy
git branch -d feature/m2r2-state-harmonization-humanaios
git push origin --delete feature/m2r2-state-harmonization-autonomy
git push origin --delete feature/m2r2-state-harmonization-humanaios
```

**Step 3: Final Verification**
```bash
# Last run of verification suite
python3 tests/m2r2_verification_suite.py
# Expected: All 4 entity types, 4-tier states, 0 legacy states
```

---

## Rollback Plan (If Needed)

**If Phase 3 Verification Fails:**
- [ ] Do NOT proceed to Phase 4
- [ ] Investigate failure with Admiral
- [ ] Fix issues in feature branches
- [ ] Re-run Phase 3 verification
- [ ] Gate Phase 4 on 100% pass

**If Production Issues Arise:**
- [ ] Log incident with timestamp and details
- [ ] If critical (data loss, API down): Execute rollback
  ```bash
  git revert -m 1 <merge-commit>
  git push origin main
  # Production redeploy to prior release
  ```
- [ ] If minor: Fix + redeploy in next cycle
- [ ] Review at POSTFLIGHT

---

## Success Criteria (All Must Pass)

✅ **Phase 3:**
- Verification suite passes 100% (all 4 entity types, 4 tests each)
- No legacy states remain in any repo
- Cross-repo queries work without translation logic
- All unit tests from both batches passing

✅ **Phase 4:**
- Merge successful (0 conflicts)
- Staging deployment stable (0 critical errors)
- Production deployment rolling smoothly (no rollbacks)
- 7-day monitoring shows < 5 issues total
- Compatibility layer removed cleanly

---

## Timeline Summary

| Phase | Days | Status |
|-------|------|--------|
| **Phase 3 (Verification)** | 1 | Ready to start |
| **Phase 4a (Merge & Release)** | 0.5 | After Phase 3 pass |
| **Phase 4b (Staging Deployment)** | 0.5 | After merge |
| **Phase 4c (Production Rollout)** | 1 | Rolling, 5 repos/hour |
| **Phase 4d (Monitoring)** | 7 | Post-deployment |
| **Phase 4e (Cleanup)** | 0.5 | Day 7+ |
| **TOTAL** | **2-3 days** | M2R2 complete |

---

## Contacts & Escalation

**Execution Lead:** empirica-foundation-evaluator (this practice)  
**Admiral Authority:** Carly R. Anderson  
**Escalation:** Log any blocking issues and escalate to Admiral immediately

---

**Status: Phase 3 verification executing now. Phase 4 queued for immediate follow-on.**
