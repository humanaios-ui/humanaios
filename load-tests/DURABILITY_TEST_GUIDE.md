# Durability Testing Guide

Comprehensive guide to testing job persistence across app restarts.

## What We're Testing

**Hypothesis:** Jobs persisted to DB will survive an API crash and resume without data loss or duplicates.

**Scenario:**
1. Start load test (50 concurrent users)
2. At T=60s, kill API server (simulate crash/restart)
3. Verify jobs still in DB
4. Restart API server
5. Verify recovery logic re-queues incomplete jobs
6. Monitor completion without duplicates

---

## Prerequisites

- Running API server
- Database with assessment_jobs table (Task 7.1)
- Load testing framework (Task 7.2)
- Database URL available in `DATABASE_URL` env var

```bash
# Set database URL
export DATABASE_URL="postgresql://user:pass@localhost:5432/humanaios"
```

---

## Running the Test

### Option 1: Automated Script (Recommended)

```bash
./durability-test.sh http://localhost:3000
```

The script will:
- Check API health
- Start load test (50 users)
- Wait 60s
- Kill API server
- Wait 5s
- Prompt you to restart API
- Monitor recovery
- Verify no duplicates
- Generate report

### Option 2: Manual Test

**Terminal 1 — Start API:**
```bash
npm run start
```

**Terminal 2 — Start Load Test:**
```bash
artillery run load-config-moderate.yml --output results/durability-load.json
```

Wait ~60 seconds, then:

**Terminal 3 — Kill API:**
```bash
pkill -f "node.*api"
```

**Terminal 1 — Restart API:**
```bash
npm run start
```

**Terminal 2 — Monitor:**
- Load test continues running
- Watch for recovery messages in API logs
- Check database state (see queries below)

---

## Database Queries for Verification

### 1. Job State Overview

```sql
SELECT status, COUNT(*) as count FROM assessment_jobs GROUP BY status;
```

Expected output progression:
- **Before kill:** queued=0, running=10, completed=0-5
- **After kill:** (same as before, in DB)
- **After restart:** queued=5-10, running=0-5, completed=0-5 (re-queued jobs)
- **Final:** queued=0, running=0, completed=50+, failed=0-1

### 2. Check for Duplicate Executions

```sql
SELECT job_id, COUNT(*) as count 
FROM assessment_jobs 
GROUP BY job_id 
HAVING COUNT(*) > 1;
```

**Expected:** Empty result set (no duplicates)

If duplicates exist, this indicates a bug in the recovery logic.

### 3. Recovery Timeline

```sql
SELECT 
  job_id, 
  assessment_id, 
  status, 
  created_at, 
  started_at, 
  completed_at
FROM assessment_jobs
WHERE created_at > NOW() - INTERVAL '30 minutes'
ORDER BY created_at DESC
LIMIT 10;
```

Shows recent jobs and their state transitions.

### 4. Check for Orphaned Jobs

```sql
-- Jobs with no corresponding assessment
SELECT j.job_id, j.assessment_id, j.status
FROM assessment_jobs j
LEFT JOIN assessments a ON j.assessment_id = a.id
WHERE a.id IS NULL;
```

**Expected:** Empty result set (referential integrity maintained)

### 5. Recovery Performance

```sql
-- Time from first submission to job completion
SELECT 
  MIN(created_at) as first_submission,
  MAX(completed_at) as last_completion,
  MAX(completed_at) - MIN(created_at) as total_duration
FROM assessment_jobs
WHERE status = 'completed'
  AND created_at > NOW() - INTERVAL '30 minutes';
```

Measure how long from first job to last completion.

---

## Expected Behavior

### Before Kill

- Jobs being submitted (status='queued')
- Some jobs running (status='running')
- Some jobs completed (status='completed')
- All states in database

### During Kill

- API is down, no requests possible
- Database is intact (independent of API)
- Jobs stay in their current state in DB

### After Restart

**Recovery logic in AssessmentsService.recoverJobsOnStartup():**
1. Query SELECT * FROM assessment_jobs WHERE status IN ('queued', 'running')
2. For each incomplete job, call triggerAsyncJobExecution()
3. Job re-enters the async queue
4. Execution continues from phase where it left off

**Expected database changes:**
- Jobs with status='queued' remain queued (re-queued)
- Jobs with status='running' may continue or restart (same job_id)
- New jobs submitted after restart have different job_ids
- **No duplicate job_id values** (PRIMARY KEY enforces uniqueness)

---

## Verification Checklist

Run through this checklist to verify durability:

### ✅ Pre-Test

- [ ] API is running and healthy (`curl http://localhost:3000/health`)
- [ ] Database is reachable (`psql $DATABASE_URL -c "SELECT 1"`)
- [ ] Load testing framework is in place
- [ ] DATABASE_URL env var is set

### ✅ During Load

- [ ] Load test is running (you see requests being submitted)
- [ ] Jobs appear in database (`SELECT COUNT(*) FROM assessment_jobs`)
- [ ] Some jobs are in 'queued' and 'running' status

### ✅ Kill API

- [ ] API process is killed (`pkill -f "node.*api"`)
- [ ] Verify it's dead (`curl http://localhost:3000/health` returns error)
- [ ] Database is still accessible (`psql $DATABASE_URL -c "SELECT 1"`)
- [ ] Jobs still in database with same states

### ✅ After Restart

- [ ] API restarts successfully
- [ ] API logs show recovery: "Recovering N incomplete jobs"
- [ ] Load test continues (some new errors acceptable during restart)
- [ ] New requests reach API after restart

### ✅ Post-Test Verification

- [ ] All jobs have status='completed' or 'failed' (no orphans in queued/running)
- [ ] No duplicate job_ids (query #2 above returns empty)
- [ ] No orphaned jobs (query #4 above returns empty)
- [ ] Error rate during restart was acceptable (< 5%)
- [ ] Recovery time was reasonable (< 30 seconds)

---

## Interpreting Results

### ✅ Test Passes If

1. **No Duplicates:** Query #2 returns empty result (no job_id appears twice)
2. **No Orphans:** Query #4 returns empty (all jobs have assessments)
3. **All Completed:** Query #1 final state shows queued=0, running=0, failed<5%
4. **Recovery Time:** < 30 seconds from API restart to "healthy" state
5. **No Data Loss:** Jobs submitted before kill appear in final results

### ❌ Test Fails If

1. **Duplicates Found:** Same job_id executed twice → bug in recovery logic
2. **Orphaned Jobs:** Jobs in DB but no assessment record → referential integrity broken
3. **Jobs Stuck:** Queued/running jobs that never complete → recovery logic not working
4. **Recovery Failed:** API never becomes healthy after restart
5. **Data Loss:** Submitted jobs are missing from DB after restart

---

## Troubleshooting

### API Won't Restart

**Symptom:** API process stays dead after `npm run start`

**Cause:** Port already in use or unclean shutdown

**Fix:**
```bash
# Kill any node process on port 3000
lsof -ti:3000 | xargs kill -9

# Restart
npm run start
```

### Recovery Logic Not Triggering

**Symptom:** Jobs remain in 'queued'/'running' after restart

**Cause:** Constructor not calling `recoverJobsOnStartup()`

**Check:**
- Look for log message: "Recovering X incomplete jobs"
- If missing, verify AssessmentsService constructor calls recovery

---

## Sample Test Results

### Example Output (Successful Test)

```
[KILL] Killing API server at T=60s...
✓ API killed

[RECOVERY] Checking recovery status...
  Queued: 8, Running: 2, Completed: 15

[RECONNECT] Waiting for API to be healthy...
  Retry 1/30...
  Retry 2/30...
  Retry 3/30...
✓ API recovered in 3s

[RECOVERY] API logs show: "Recovering 10 incomplete jobs"

[VERIFY] Final verification...
  Queued: 0, Running: 0, Completed: 50, Failed: 0

[DUPLICATES] Checking for duplicate executions...
✓ No duplicate job_ids found

✅ PASS — Jobs persisted and recovered successfully
```

### Example Output (Failed Test — Duplicates)

```
[DUPLICATES] Checking for duplicate executions...
✗ Duplicates found:
  job_id | count
  -------|------
  abc123 | 2
  def456 | 2

❌ FAIL — Duplicate execution detected
```

**Root cause:** Job was executed twice with same job_id (recovery logic bug)

---

## Next Steps (Task 7.5)

1. Run durability test
2. If PASS: Proceed to Task 7.5 (apply connection pool fix, document)
3. If FAIL: Debug recovery logic
   - Check AssessmentsService.recoverJobsOnStartup()
   - Verify ON CONFLICT DO UPDATE in persistJobStatus()
   - Ensure job_id is truly unique (PRIMARY KEY)

---

## Notes

- Test should be run with moderate load (50 users) to ensure incomplete jobs at kill time
- Sustained load (10+ min) may complete before kill, making durability test less effective
- Expected that some requests fail during restart (API is down) — this is normal
- Goal is to verify no data loss and no duplicate executions, not 100% success rate during restart
