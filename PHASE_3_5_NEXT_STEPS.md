# Phase 3.5 — Ready for Deployment

**Status:** ✅ Configuration & Documentation Complete  
**Branch:** `release/m2r2-state-harmonization-v1.0`  
**Last Commit:** `48f43fb` (deployment scripts added)

---

## What's Been Done

### Configuration Fixes
- ✅ Loki config updated for Loki 3.0+ compatibility (schema v11→v12, added compactor)
- ✅ Promtail config enhanced with robust error handling and pipeline stages
- ✅ Docker Compose updated with healthchecks and dependencies

### Documentation
- ✅ Created comprehensive Phase 3.5 Deployment Guide with:
  - 4 integration test procedures
  - Troubleshooting guide (10+ common issues)
  - Verification checklist
  - Performance baselines

### Automation
- ✅ `scripts/deploy-phase-3-5.sh` — Automated deployment with health checks
- ✅ `scripts/test-phase-3-5.sh` — Comprehensive integration test suite

---

## Your Next Steps

### 1. Deploy Phase 3.5 Services

```bash
cd agent
./scripts/deploy-phase-3-5.sh
```

**What it does:**
- Verifies Phase 3.4 is running
- Starts Jaeger, Loki, and Promtail services
- Waits for all services to be healthy
- Displays service endpoints

**Expected output:**
```
✓ Jaeger UI is ready
✓ Loki is ready
✓ Promtail is ready
✓ All Phase 3.5 services are healthy

Service Endpoints:
  Jaeger UI:        http://localhost:16686
  Loki API:         http://localhost:3100
  Promtail Metrics: http://localhost:9080/metrics
```

### 2. Run Integration Tests

```bash
./scripts/test-phase-3-5.sh
```

**What it does:**
- Tests Jaeger connectivity and API
- Tests Loki readiness and health
- Tests Promtail metrics endpoint
- Verifies Grafana datasources are configured
- Checks log collection status
- Displays overall test results

**Expected result:** "All tests passed! Phase 3.5 is ready."

### 3. Manual Verification in Grafana

1. Open http://localhost:3000/ (Grafana)
2. Go to **Explore** (left sidebar)
3. **Test Jaeger:**
   - Select "Jaeger" datasource
   - Look for "task-service" in the service dropdown
   - You should see recent traces
4. **Test Loki:**
   - Select "Loki" datasource
   - Enter query: `{service="task-service"}`
   - Click "Run query" → you should see logs
5. **Test Prometheus:**
   - Select "Prometheus" datasource
   - Enter query: `task_requests_total`
   - Click "Run query" → you should see metrics graph

### 4. Generate Test Data (Optional)

If you want to verify everything is working with real data:

```bash
# Submit a test request to generate traces, logs, and metrics
curl -X POST http://localhost:8000/submit \
  -H "Content-Type: application/json" \
  -d '{
    "practice": "autonomy",
    "task_type": "understanding",
    "input": "Test message for Phase 3.5 verification"
  }'

# Wait 10 seconds, then check:
# - Jaeger UI for the new trace
# - Loki for the new logs
# - Grafana dashboard for the new metrics
```

---

## Expected Timeline

| Step | Time | Notes |
|------|------|-------|
| Deploy | 2-3 min | Services start and health checks run |
| Tests | 1-2 min | All 6 integration tests execute |
| Manual Verification | 5-10 min | Visual inspection in Grafana |
| **Total** | **10-15 min** | Ready to commit and merge |

---

## Troubleshooting

If any service doesn't start:

1. **Check service logs:**
   ```bash
   docker logs loki-empirica-evaluator | tail -50
   docker logs promtail-empirica-evaluator | tail -50
   docker logs jaeger-empirica-evaluator | tail -50
   ```

2. **Common issues:**
   - Loki permission errors → Clean volumes: `docker volume rm loki_data loki_wal`
   - Promtail can't reach Loki → Verify Loki is healthy: `docker compose ps loki`
   - Port conflicts → Check `lsof -i :3100` or change docker-compose ports

3. **Full troubleshooting:** See `docs/PHASE_3_5_DEPLOYMENT_GUIDE.md`

---

## After Successful Testing

### If Tests Pass

1. **Commit the test results** (optional but recommended):
   ```bash
   git add .
   git commit -m "test(phase3.5): integration testing complete and verified"
   ```

2. **Merge to main:**
   ```bash
   git checkout main
   git merge release/m2r2-state-harmonization-v1.0
   git push origin main
   ```

3. **Archive branch:**
   ```bash
   git branch -d release/m2r2-state-harmonization-v1.0
   git push origin --delete release/m2r2-state-harmonization-v1.0
   ```

### If Tests Fail

1. **Review error logs** from the test script output
2. **Consult troubleshooting section** in this guide or in `PHASE_3_5_DEPLOYMENT_GUIDE.md`
3. **Reach out** if issues persist

---

## What Phase 3.5 Delivers

| Component | Function |
|-----------|----------|
| **Jaeger** | Distributed trace visualization for request debugging |
| **Loki** | Centralized log aggregation and search |
| **Per-Practice Dashboards** | Isolated metrics view for each practice (autonomy, mesh-support, outreach) |

**Combined Effect:** Complete observability — understand what happened, when it happened, and why through traces, logs, and metrics all in one system (Grafana).

---

## Next Phase (3.6)

After Phase 3.5 is merged:
- **Phase 3.6:** SLO/SLI tracking
- Define service level objectives (e.g., 99.5% uptime, <500ms latency)
- Implement SLI dashboards in Grafana
- Connect to alerting rules

---

## Quick Reference

| Action | Command |
|--------|---------|
| Deploy Phase 3.5 | `./scripts/deploy-phase-3-5.sh` |
| Run tests | `./scripts/test-phase-3-5.sh` |
| View Jaeger UI | `open http://localhost:16686` |
| View Loki logs in Grafana | `open http://localhost:3000/explore` (select Loki) |
| Check service status | `docker compose ps` |
| View Loki logs | `docker logs loki-empirica-evaluator` |
| View Promtail logs | `docker logs promtail-empirica-evaluator` |
| Merge to main | `git checkout main && git merge release/m2r2-state-harmonization-v1.0` |

---

**Ready to proceed? Run:** `./scripts/deploy-phase-3-5.sh`
