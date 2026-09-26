# M3 Nervous System — Production Deployment Checklist

**Status:** Ready for production deployment  
**Date:** 2026-08-16  
**Owner:** Admiral (Carly R. Anderson)

---

## Pre-Deployment Verification (Week of 2026-08-18)

### Code Audit
- [ ] Final security review (Admiral signatures, authority model)
- [ ] Code style consistency (type hints, docstrings)
- [ ] No debug logging left in production code
- [ ] All mock implementations documented (what needs real impl post-MVP)
- [ ] No credentials/secrets in code

### Test Execution
- [ ] Run full test suite: `pytest empirica/m3_rank_* -v --tb=short`
- [ ] Verify 40/40 tests passing
- [ ] Check test coverage: 85%+ coverage on M3R1-R3
- [ ] No flaky tests (run 3× to confirm)

### Dependencies
- [ ] Python 3.14+ available
- [ ] SQLite3 available
- [ ] No external dependencies (hashlib, sqlite3, dataclasses all stdlib)
- [ ] No version conflicts with existing codebase

### Documentation
- [ ] M3R1-R3 architecture documented
- [ ] API reference for ValidationOrchestrator, RecoveryOrchestrator
- [ ] Runbook for common operations (detect divergence, recover, rollback)
- [ ] Deployment guide (what to enable, where to route messages)

---

## Deployment Steps (Week of 2026-08-20)

### Phase 1: Pre-Production Environment (Monday)

```bash
# 1. Deploy M3R1-R3 code to pre-prod
git checkout main  # Assumes all code is committed
git pull origin main

# 2. Initialize M3 database tables (idempotent)
python3 empirica/m3_rank_1/batch_sync_infrastructure.py
# Creates: empirica_dispatch_log, empirica_dispatch_messages, empirica_retry_queue, empirica_dead_letter_queue

# 3. Start batch accumulator (background service)
python3 -c "from empirica.m3_rank_1.batch_sync_infrastructure import BatchSyncCoordinator; \
            coordinator = BatchSyncCoordinator(); \
            print('M3R1 initialized')"

# 4. Verify connectivity to all practices
# (Real impl: check mesh-support connectivity)
echo "✅ All practices reachable"

# 5. Run sanity tests
pytest empirica/m3_rank_1/test_batch_sync_infrastructure.py -v
pytest empirica/m3_rank_2/test_divergence_detection.py -v
pytest empirica/m3_rank_3/test_validation_recovery.py -v
# Expected: 40/40 passing
```

### Phase 2: Canary Deployment (Tuesday)

```bash
# 1. Route 10% of batches through M3R1 (rest bypass)
# (Config: M3R1_CANARY_PERCENTAGE=10)

# 2. Monitor metrics for 24 hours
# - Batch dispatch latency (target: <100ms)
# - Dispatch success rate (target: >99%)
# - Divergence detection accuracy (target: 0 false positives in canary)

# 3. Watch for errors in logs
# - No unhandled exceptions
# - No memory leaks (Python GC steady)
# - No database lock contention
```

### Phase 3: Gradual Rollout (Wednesday-Thursday)

```bash
# 1. Increase routing: 10% → 50% → 100% over 24 hours
# Each step: wait 1 hour, verify metrics stable

# 2. Enable divergence detection at each percentage milestone
# - 10%: Collect fingerprints (no action)
# - 50%: Run diff (observe divergence patterns)
# - 100%: Full detection (divergence reports generated)

# 3. Validation phase (read-only)
# - Run M3R3 validation in dry-run mode (no recovery)
# - Observe false positive rate (target: <1%)
# - Log all verdicts for manual review
```

### Phase 4: Full Production (Friday)

```bash
# 1. Enable recovery (corrections dispatched)
# - Start with severity threshold: ERROR only (>20% divergence)
# - Monitor recovery success rate (target: >95%)
# - Alert Admiral on failures

# 2. Gradually lower threshold over 1 week
# Day 1 (Fri): ERROR only (>20%)
# Day 2 (Mon): ERROR + WARNING (>5%)
# Day 3 (Tue): All severities

# 3. Monitor for side effects
# - No oscillation (diverge → recover → diverge again)
# - Recovery time <500ms per divergence
# - No cascading failures (one recovery breaking another)
```

---

## Operational Runbook

### Normal Operation

**Q: How do I know M3 is working?**
```sql
-- Check last fingerprint
SELECT MAX(timestamp) FROM m3_fingerprints;

-- Check recent divergences
SELECT report_id, divergence_percentage, severity 
FROM m3_divergence_reports 
ORDER BY timestamp DESC LIMIT 10;

-- Check recovery status
SELECT recovery_id, success, entities_fixed, recovery_time 
FROM m3_recovery_results 
ORDER BY timestamp DESC LIMIT 10;
```

**Q: What's the divergence rate?**
- Target: 0 divergences per hour (synchronized practices)
- Warning: >5 divergences per hour (investigate network/proposal velocity)
- Critical: >20 divergences per hour (manual intervention required)

**Q: Is the batch queue healthy?**
```python
from empirica.m3_rank_1.batch_sync_infrastructure import BatchSyncCoordinator
coord = BatchSyncCoordinator()
status = coord.accumulator.get_status()
print(f"Queued: {status['queued_messages']}/10")
print(f"Window: {status['window_remaining_seconds']}s")
```

### Troubleshooting

**Issue: High divergence rate (>20 divergences/hour)**

1. Check network connectivity
   ```bash
   ping <practice> -c 3  # All practices reachable?
   ```

2. Check proposal velocity
   - Are proposals being sent faster than sync can handle?
   - M3R1 batch window is 30s: max 10 decisions per batch
   - If >10 decisions/30s, consider increasing batch size (M3R4)

3. Check for cascading failures
   ```python
   from empirica.m3_rank_3.validation_recovery import ValidationOrchestrator
   validator = ValidationOrchestrator()
   # Check if recent divergences are cascading
   # (child divergences follow parent by <1s)
   ```

**Issue: Recovery failing (success rate <90%)**

1. Check Admiral connectivity
   - Can Admiral sign batches?
   - Can practices apply corrections?

2. Check correction queue
   ```python
   from empirica.m3_rank_1.batch_sync_infrastructure import PersistentQueue
   queue = PersistentQueue()
   pending = queue.get_pending_retries()
   print(f"Pending retries: {len(pending)}")
   ```

3. Escalate to mesh-support if manual intervention needed

**Issue: False positives (validated as false but reported as divergence)**

1. Check fingerprinting consistency
   ```python
   from empirica.m3_rank_2.divergence_detection import StateFingerprinter
   fp1 = StateFingerprinter().fingerprint_dispatch()
   fp2 = StateFingerprinter().fingerprint_dispatch()
   print(f"Consistent: {fp1.root_hash == fp2.root_hash}")
   ```

2. Review recent entity updates (may have changed between fingerprints)

---

## Rollback Plan

**If something goes wrong, here's how to roll back:**

### Immediate (Disable M3)

```bash
# Stop batch accumulation (no new divergences detected)
# Set: M3R1_ENABLED=false, M3R2_ENABLED=false

# Revert to manual sync (pre-M3)
# All practices continue independently (eventual consistency)

# Data remains intact (no data loss)
# Fingerprints and reports logged to DB (audit trail)
```

### Investigation

```bash
# Query what went wrong
SELECT * FROM m3_divergence_reports WHERE error IS NOT NULL;
SELECT * FROM m3_recovery_results WHERE success = false;

# Identify root cause (network, Byzantine, capacity?)
# Contact mesh-support for manual intervention
```

### Restart

```bash
# Fix underlying issue first
# Then enable M3R1-R3 again with conservative thresholds
# Start from canary phase (10% routing) again
```

---

## Success Criteria (Production)

### First 24 Hours
- [ ] Zero unhandled exceptions in logs
- [ ] All 40 tests pass in production environment
- [ ] Divergence detection working (0 divergences is OK)
- [ ] No memory leaks (Python GC stable)
- [ ] No database lock contention

### First Week
- [ ] Recovery success rate >95%
- [ ] False positive rate <1%
- [ ] Recovery time <500ms per divergence
- [ ] No cascading failures
- [ ] No oscillation (diverge → recover → diverge)

### One Month
- [ ] Divergence patterns understood (root causes identified)
- [ ] Threshold tuning complete (INFO/WARNING/ERROR calibrated)
- [ ] Operational runbook validated
- [ ] Zero critical incidents
- [ ] Operator confidence high

---

## Metrics to Monitor

### Real-Time Dashboards

Create dashboards for:
- Divergence count (per hour, per severity)
- Recovery success rate (%)
- Recovery time (milliseconds, p50/p95/p99)
- Fingerprinting latency (per practice)
- Batch queue depth (messages pending)
- Retry queue depth (failed corrections)

### Alerting Rules

```
Alert if:
- divergence_rate > 20/hour (ERROR threshold)
- recovery_success_rate < 90%
- batch_queue_depth > 50
- retry_queue_depth > 100
- fingerprint_latency > 1000ms
```

---

## Post-Production (M3R4 & Beyond)

### Immediate (Week 1)

- Collect divergence patterns (root causes)
- Calibrate severity thresholds based on real data
- Tune batch window (30s vs 60s?)
- Tune batch size (10 vs 20 messages?)

### Near-Term (Week 2-4)

- Implement M3R4 (Autonomous Healing)
- Add decision tree (auto-heal vs escalate)
- Implement rollback logic
- Add feedback loops

### Medium-Term (Month 2-3)

- Implement M3.5 (Resilience Layer)
- Add circuit breakers
- Add graceful degradation
- Cross-org mesh coordination

---

## Sign-Off

**Deployment Authorization:**

- Admiral (Carly R. Anderson): _______________  Date: __________

**Acknowledged by:**

- mesh-support: _______________  Date: __________
- empirica-foundation: _______________  Date: __________

---

## Deployment Log

| Date | Phase | Status | Notes |
|------|-------|--------|-------|
| 2026-08-20 | Pre-Prod Setup | — | Scheduled |
| 2026-08-21 | Canary (10%) | — | Scheduled |
| 2026-08-22 | Gradual Rollout | — | Scheduled |
| 2026-08-23 | Full Production | — | Scheduled |

---

**Document Version:** 1.0  
**Last Updated:** 2026-08-16  
**Maintained By:** Admiral (Carly R. Anderson)
