# Assessment API Load Testing

Load testing framework for HumanAIOS assessment API using Artillery. Measures performance, durability, and capacity limits under concurrent load.

## Setup

### Prerequisites

- Node.js 18+ (Artillery requires it)
- Running assessment API on `http://localhost:3000`
- Docker or local PostgreSQL for persistent job state

### Installation

```bash
# From repo root
cd load-tests

# Install Artillery CLI
npm install -g artillery

# Verify installation
artillery --version
```

## Test Scenarios

### Baseline Test (Single User)
Tests happy path: submit → poll → retrieve results with one user.

```bash
artillery run assessment-submission.yml --target http://localhost:3000
```

**Measures:**
- Single-user latency (avg, P50, P95, P99)
- Job state persistence
- Result retrieval accuracy
- Error rate (expected: 0%)

**Duration:** 2 minutes

---

### Light Load (10 Concurrent Users)
Tests system behavior with light concurrent load.

```bash
artillery run --target http://localhost:3000 <<EOF
config:
  target: http://localhost:3000
  phases:
    - duration: 120
      arrivalRate: 10
      rampTo: 10
      name: "Light Load (10 users)"

scenarios:
  - name: "Assessment Submission"
    flow:
      - post:
          url: "/api/v1/assessments"
          json:
            system_id: "gpt-4"
            system_name: "GPT-4 Light"
            system_info:
              endpoint: "https://api.openai.com/v1/chat/completions"
              model: "gpt-4"
              api_key: "sk-test-key"
            tier: "T1_STANDARD"
          expect:
            - statusCode: 201
          capture:
            json: "$.assessment_id"
            as: "assessment_id"

      - think: 1

      - loop:
          - get:
              url: "/api/v1/assessments/{{ assessment_id }}"
              expect:
                - statusCode: 200
              capture:
                json: "$.status"
                as: "job_status"
          - think: 2
        count: 10
        whileTrue: "{{ job_status != 'completed' }}"

      - get:
          url: "/api/v1/assessments/{{ assessment_id }}/result"
          expect:
            - statusCode: 200
EOF
```

**Expected metrics:**
- Avg latency: < 5s
- P99 latency: < 30s
- Error rate: < 1%
- Throughput: >= 5 assessments/min

---

### Moderate Load (50 Concurrent Users)
Tests system scaling with moderate concurrent load.

```bash
artillery run --target http://localhost:3000 --ramp 50
```

(Replace `--ramp 50` with config parameter to test 50 concurrent users)

**Expected metrics:**
- Avg latency: < 8s (slight increase OK)
- P99 latency: < 40s
- Error rate: < 1%
- Throughput: >= 20 assessments/min

---

### High Load (100 Concurrent Users)
Tests system limits with high concurrent load.

**Expected metrics:**
- Avg latency: < 15s (performance degrades gracefully)
- P99 latency: < 60s
- Error rate: < 2% (acceptable under stress)
- Throughput: >= 30 assessments/min

---

### Sustained Load (50 Users, 10 Minutes)
Tests system stability and memory usage over extended period.

```bash
artillery run --target http://localhost:3000 --duration 600 --ramp 50
```

**Checks:**
- No memory leaks (monitor via `docker stats` or `top`)
- Consistent latency (no degradation over time)
- Job recovery works (restart app mid-test, verify jobs resume)

---

## Results & Reporting

Results are saved to `results/` directory (auto-created):

```bash
# View latest results
cat results/artillery-report-*.json | jq '.summary'

# Extract key metrics
artillery run assessment-submission.yml --output results/baseline-report.json
```

**Key metrics to track:**

| Metric | Baseline | Light (10) | Moderate (50) | High (100) |
|--------|----------|-----------|--------------|-----------|
| Avg Latency (ms) | <2000 | <5000 | <8000 | <15000 |
| P99 Latency (ms) | <5000 | <30000 | <40000 | <60000 |
| Throughput (req/s) | 0.5 | 5 | 20 | 30 |
| Error Rate | 0% | <1% | <1% | <2% |

---

## Durability Testing

Tests job persistence across app restarts.

### Test Script

```bash
# Terminal 1: Start API in foreground
npm run start

# Terminal 2: Run sustained load
artillery run --target http://localhost:3000 --duration 300 --ramp 50

# At T=60 seconds: Kill API (Ctrl+C in Terminal 1)
# Wait 5 seconds, restart API
npm run start

# Monitor logs for recovery:
# "Recovering X incomplete jobs from database"
```

**Verification:**
- [ ] Jobs submitted before crash persist in DB
- [ ] Jobs resume execution on restart
- [ ] No duplicate job executions
- [ ] Final results match expectations

---

## Load Test Configuration Examples

### Config Template

```yaml
config:
  target: http://localhost:3000
  phases:
    - duration: 120
      arrivalRate: X          # Users per second
      rampTo: Y               # Ramp to Y users
      name: "Test Name"

scenarios:
  - name: "Flow Name"
    flow:
      # Your requests here
```

### Variable Substitution

```yaml
variables:
  orgs: ["org-1", "org-2"]
  systems:
    - id: "gpt-4"
      name: "GPT-4"
    - id: "claude"
      name: "Claude"

scenarios:
  - flow:
      - post:
          url: "/api/v1/assessments"
          json:
            system_id: "{{ $randomChoice(systems).id }}"
            org_id: "{{ $randomChoice(orgs) }}"
```

---

## Monitoring During Tests

### Watch API Logs

```bash
# In separate terminal
tail -f logs/assessment-api.log | grep -E "submitted|Assessment|Job"
```

### Monitor System Resources

```bash
# CPU, memory, disk I/O
top -p $(pgrep -f "node.*api")

# Database connections
psql $DATABASE_URL -c "SELECT count(*) FROM pg_stat_activity;"
```

### Database Job Queue Depth

```bash
# Check pending jobs
psql $DATABASE_URL -c "SELECT status, COUNT(*) FROM assessment_jobs GROUP BY status;"
```

---

## Troubleshooting

### "Connection refused" error
- Verify API running: `curl http://localhost:3000/health`
- Check port in `artillery.yml` config

### "Assessment not found" errors
- Ensure org_id header matches API expectations
- Check API org validation logic

### High latency / timeout errors
- Check if DB connection pool is exhausted
- Verify ACAT protocol execution time (Phase 2 expected bottleneck)
- Monitor API logs for errors

### Memory usage climbing
- Check if job cleanup runs (`cleanupCompletedJobs` method)
- Verify timeouts clear properly
- Monitor assessment_jobs table size (query for old records)

---

## Next Steps

1. **Run baseline test** to establish baseline metrics
2. **Run load tests** (10, 50, 100 concurrent) and capture results
3. **Identify bottleneck** (CPU? DB? Network?)
4. **Optimize if needed** (connection pooling, query tuning, etc.)
5. **Document capacity limits** in operations runbook

See `TASK7_STRESS_TESTING_BREAKDOWN.md` for full task details.
