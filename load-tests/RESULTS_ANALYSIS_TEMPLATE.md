# Load Test Results Analysis

Use this template to document and analyze load test results. Copy and fill in for each test run.

## Test Metadata

| Field | Value |
|-------|-------|
| **Test Date** | YYYY-MM-DD HH:MM:SS |
| **Scenario** | (Baseline / Light / Moderate / Heavy / Sustained) |
| **Duration** | (seconds) |
| **Concurrent Users** | (count) |
| **Total Requests** | (count) |
| **Environment** | (local / staging / production) |
| **API Version** | (git commit) |
| **Database** | (PostgreSQL version, connection pool size) |

---

## Performance Metrics

### Response Times

| Metric | Value (ms) | Status |
|--------|-----------|--------|
| **Min** | | ✅ / ⚠️ / ❌ |
| **Avg** | | ✅ / ⚠️ / ❌ |
| **Median (P50)** | | ✅ / ⚠️ / ❌ |
| **P95** | | ✅ / ⚠️ / ❌ |
| **P99** | | ✅ / ⚠️ / ❌ |
| **Max** | | ✅ / ⚠️ / ❌ |

**Target Thresholds:**
- Baseline: Avg < 2s, P99 < 5s
- Light: Avg < 5s, P99 < 30s
- Moderate: Avg < 8s, P99 < 40s
- Heavy: Avg < 15s, P99 < 60s
- Sustained: Consistent over 10 min

---

### Error Rates

| Endpoint | Errors | Total | Rate | Status |
|----------|--------|-------|------|--------|
| **POST /assessments** | | | | ✅ / ⚠️ / ❌ |
| **GET /assessments/:id** | | | | ✅ / ⚠️ / ❌ |
| **GET /assessments/:id/result** | | | | ✅ / ⚠️ / ❌ |
| **TOTAL** | | | | ✅ / ⚠️ / ❌ |

**Target:** < 1% error rate (< 2% acceptable for heavy load)

---

### Throughput

| Metric | Value | Status |
|--------|-------|--------|
| **Requests/sec** | | ✅ / ⚠️ / ❌ |
| **Assessments/min** | | ✅ / ⚠️ / ❌ |
| **P95 Response Time** | | ✅ / ⚠️ / ❌ |

**Target Throughput:**
- Light (10 users): >= 5 assessments/min
- Moderate (50 users): >= 20 assessments/min
- Heavy (100 users): >= 30 assessments/min

---

## Endpoint Breakdown

### POST /assessments (Job Submission)

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Avg Latency | | < 2s | |
| P99 Latency | | < 5s | |
| Error Rate | | < 1% | |
| Throughput | req/s | >= target | |

**Notes:**
- This is the submission endpoint (fire and forget)
- Should be fastest endpoint (DB INSERT only)
- Errors indicate DB connection exhaustion or validation issues

---

### GET /assessments/:id (Status Polling)

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Avg Latency | | < 1s | |
| P99 Latency | | < 5s | |
| Error Rate | | < 1% | |

**Notes:**
- Polling endpoint used to check job progress
- Should be fast (SELECT query only)
- High error rate may indicate DB connectivity issues

---

### GET /assessments/:id/result (Result Retrieval)

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Avg Latency | | < 2s | |
| P99 Latency | | < 10s | |
| Error Rate | | < 1% | |

**Notes:**
- Called after assessment completion
- Includes JSON parsing of result_summary
- Should be fast unless ACAT result is very large

---

## System Resource Utilization

### CPU

| Metric | Value | Notes |
|--------|-------|-------|
| **Peak Usage** | % | |
| **Average Usage** | % | |
| **Sustained at?** | user / sys | One-sided? |

---

### Memory

| Metric | Value | Notes |
|--------|-------|-------|
| **Initial** | MB | Before test start |
| **Peak** | MB | Highest observed |
| **Final** | MB | After test complete |
| **Growth Rate** | MB/min | Concern if > 10 MB/min |

**Memory Check:**
- Is memory released after jobs complete?
- Any memory leaks in job timeout cleanup?
- Table bloat in assessment_jobs?

---

### Database

| Metric | Value | Notes |
|--------|-------|-------|
| **Max Connections Used** | / 100 | |
| **Avg Query Latency** | ms | From DB logs |
| **Slow Queries** | count | Queries > 100ms |
| **Lock Waits** | count | Contention? |
| **Table Sizes** | | assessment_jobs bloat? |

**Queries to check:**

```sql
-- Connection pool usage
SELECT count(*) FROM pg_stat_activity;

-- Job table size
SELECT pg_size_pretty(pg_total_relation_size('assessment_jobs'));

-- Index health
SELECT schemaname, tablename, indexname, idx_scan FROM pg_stat_user_indexes WHERE tablename = 'assessment_jobs';
```

---

## Bottleneck Analysis

### Where is the system slow?

- [ ] **CPU-bound**: ACAT protocol (Phase 2) is the limiting factor
- [ ] **I/O-bound**: Database queries (INSERT, SELECT) are slow
- [ ] **Memory-bound**: Growing memory usage under load
- [ ] **Network-bound**: Calls to external AI services are slow
- [ ] **Connection Pool**: Exhausted DB connections
- [ ] **Other**: (describe)

**Evidence:**
- (CPU screenshot, query logs, memory graph, etc.)

---

### Performance Degradation Pattern

```
Concurrency | Avg Latency | P99 Latency | Error Rate | Throughput
10 users    |             |             |            |
50 users    |             |             |            |
100 users   |             |             |            |
```

Does latency scale **linearly** or **exponentially**? Indicates where bottleneck is.

---

## Pass/Fail Evaluation

| Criterion | Result | Pass? |
|-----------|--------|-------|
| Avg latency within target | | ✅ / ❌ |
| P99 latency within target | | ✅ / ❌ |
| Error rate < 1% | | ✅ / ❌ |
| Throughput meets target | | ✅ / ❌ |
| No memory leaks observed | | ✅ / ❌ |
| DB connections stable | | ✅ / ❌ |

**Overall Result:** ✅ PASS / ⚠️ MARGINAL / ❌ FAIL

---

## Issues & Recommendations

### Critical Issues (Must Fix)

1. (Issue)
   - Impact: (Severity)
   - Root Cause: (Analysis)
   - Fix: (Recommended action)
   - Priority: P0

---

### Performance Opportunities (Nice to Have)

1. (Opportunity)
   - Impact: (Expected improvement)
   - Effort: (Implementation complexity)
   - Priority: P1 / P2 / P3

---

## Next Steps

- [ ] Address critical issues
- [ ] Re-run test to verify fixes
- [ ] Move to next load level (if current passes)
- [ ] Document findings in operations runbook

---

## Artifacts & Raw Data

- Artillery JSON report: `results/artillery-report-TIMESTAMP.json`
- API logs: (attach)
- Database slow query log: (if enabled)
- System resource snapshots: (attach graphs)
