# Task 7: Stress Testing + Persistence — Detailed Breakdown

## Goal: Production-Ready Reliability (Task 7)

**Objective:** Verify system can handle concurrent assessment submissions, persist job state, and recover from restarts without data loss.

**Success Criteria:**
1. System handles 100+ concurrent submissions without data loss
2. Jobs persist to DB (survive app restart)
3. Latency: P50 < 5s response time for submission (P99 < 30s)
4. Throughput: >= 50 assessments/minute sustained
5. Error rate: < 1% under sustained load

---

## Task Breakdown

### Task 7.1: Database Persistence Layer (Blocking — must do first)
**Why first:** Current in-memory implementation loses jobs on restart. Production showstopper.

**Deliverables:**
- [ ] 7.1a: Create Alembic migration `003_assessment_jobs_persistence.py`
  - New table: `assessment_jobs` (job_id PK, assessment_id FK, status, progress, started_at, completed_at, error_message)
  - Add indexes: (assessment_id), (status, created_at) for queries
  - Add index: (org_id, status) for org-scoped list queries

- [ ] 7.1b: Update AssessmentsService to persist job state
  - Replace in-memory `activeJobs` Map with DB queries
  - Add `persistJobStatus()` method (insert/update)
  - Add `recoverJobsOnStartup()` method (fetch incomplete jobs from DB)
  - Wire into OnModuleInit()

- [ ] 7.1c: Wire job recovery into app startup
  - AssessmentsModule.onModuleInit() calls `recoverJobsOnStartup()`
  - Incomplete jobs ('queued', 'running') re-queued for execution
  - Log recovery: N jobs recovered from DB

**Effort:** 2-3 hours (schema + service layer updates)

**Dependencies:** None (Task 2-3 complete)

---

### Task 7.2: Load Testing Framework Setup
**Why:** Need systematic way to measure behavior under load.

**Deliverables:**
- [ ] 7.2a: Choose & setup load testing tool
  - Option A: Artillery (simple JSON config, good for HTTP APIs)
  - Option B: k6 (JavaScript-based, more flexible)
  - Decision: Artillery (simpler, built for API testing)

- [ ] 7.2b: Create load test scenario
  - File: `load-tests/assessment-submission.yml`
  - Scenario: POST /assessments → wait 1s → GET /assessments/:id (poll) → GET /assessments/:id/result
  - Concurrency config: 10, 50, 100 users
  - Duration: 2 minutes per concurrency level
  - Ramp-up: 10 users/second

- [ ] 7.2c: Create baseline test (single submission, verify happy path)
  - Single user, single submission
  - Verify: job_id returned, status queryable, result retrievable
  - Document baseline latency

**Effort:** 1-2 hours (tool setup + scenario scripting)

**Dependencies:** 7.1 (DB persistence — required for durability testing)

---

### Task 7.3: Execute Load Tests & Collect Metrics
**Why:** Measure actual performance under load.

**Deliverables:**
- [ ] 7.3a: Baseline test (10 concurrent users, 2 min)
  - Measure: response time (avg, P50, P95, P99), error rate, throughput
  - Expected: < 5s P50, < 1% error rate

- [ ] 7.3b: Moderate load test (50 concurrent users, 2 min)
  - Same metrics
  - Check: does throughput scale linearly?

- [ ] 7.3c: High load test (100 concurrent users, 2 min)
  - Same metrics
  - Identify: where do errors start appearing?

- [ ] 7.3d: Sustained load test (50 concurrent, 10 min)
  - Check: degradation over time? Memory leaks?

- [ ] 7.3e: Document results in CSV + markdown report
  - Table: Concurrency, Avg Latency, P50, P95, P99, Throughput, Error Rate
  - Graph: Concurrency vs Latency (if tools support)

**Effort:** 3-4 hours (actual test runs + result analysis)

**Dependencies:** 7.2 (load test framework)

---

### Task 7.4: Durability Testing (Restart Resilience)
**Why:** Verify jobs don't vanish when app crashes/restarts.

**Deliverables:**
- [ ] 7.4a: Start 50 concurrent submissions
- [ ] 7.4b: At T=1min (mid-test), kill app (simulate crash)
- [ ] 7.4c: Restart app
- [ ] 7.4d: Verify:
  - All submitted jobs still in DB
  - Queued jobs re-queued and execute
  - Running jobs resume (or restart from phase 1)
  - No duplicate executions
  - Final results match expected LI values

- [ ] 7.4e: Document recovery time (how long to resume after restart)

**Effort:** 1-2 hours (test orchestration + verification)

**Dependencies:** 7.1 (DB persistence)

---

### Task 7.5: Analysis, Optimization, Documentation
**Why:** Understand bottlenecks, optimize if needed, document for operations.

**Deliverables:**
- [ ] 7.5a: Identify bottleneck (CPU? DB? Network?)
  - Profile ACAT execution time (is it the limiting factor?)
  - Check DB query performance (is persistence layer fast enough?)
  - Measure app memory usage at scale

- [ ] 7.5b: Optimization (if needed)
  - If DB is slow: add connection pooling, query optimization
  - If ACAT is slow: already optimized (Task 2 did that)
  - If memory grows: check for leaks (timeout cleanup?)

- [ ] 7.5c: Document findings
  - Max concurrent assessments: X
  - Max throughput: Y assessments/minute
  - Recommended deployment: Z instances for production load
  - Known limitations: [list]

- [ ] 7.5d: Create runbook for operators
  - How to scale horizontally (add more instances)
  - How to monitor job queue depth
  - Alerting rules (queue depth > 100? latency > 30s?)

**Effort:** 2-3 hours (profiling + documentation)

**Dependencies:** 7.3 (load test results)

---

## Execution Order (Sequential → Parallel)

```
7.1 (DB Persistence) [BLOCKING — 2-3h]
  ↓
7.2 (Framework Setup) [1-2h, parallel with 7.1 if urgent]
  ↓
7.3 (Load Tests) [3-4h, can be parallel with 7.4]
7.4 (Durability) [1-2h, parallel with 7.3]
  ↓
7.5 (Analysis) [2-3h, after 7.3-7.4 complete]
```

**Total Estimated Effort:** 12-18 hours spread over 2-3 days

---

## Production Readiness Gate

This task is the **final gate before production**. After Task 7:
- ✅ System handles concurrent load
- ✅ Jobs persist (no data loss)
- ✅ Capacity limits documented
- ✅ Operations runbook ready

**Sign-off:** When all tests pass + documentation complete = **ALPHA READY**
