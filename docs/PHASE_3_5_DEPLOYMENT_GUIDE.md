# Phase 3.5 Observability Enhancements — Deployment & Integration Guide

**Date:** 2026-07-31  
**Status:** Ready for Deployment  
**Scope:** Complete Phase 3.5 (Jaeger, Loki, Per-Practice Dashboards)

---

## Executive Summary

Phase 3.5 builds on Phase 3.4's observability foundation with three orthogonal enhancements:

1. **Jaeger Tracing** (3.5.1) — Distributed trace analysis ✅ Complete
2. **Loki Log Aggregation** (3.5.2) — Centralized log ingestion ✅ Config Fixed
3. **Per-Practice Dashboards** (3.5.3) — Practice-specific metrics ✅ Complete

This guide covers deployment, integration testing, and verification procedures.

---

## Prerequisites

- Phase 3.4 observability stack running (Prometheus, Grafana, AlertManager)
- Docker Compose 2.0+
- ~1GB additional disk space for Loki storage (30-day retention)
- ~700MB additional RAM for Jaeger + Loki services

---

## Deployment Steps

### Step 1: Verify Phase 3.4 Stability (Pre-requisite)

Before deploying Phase 3.5 enhancements, verify Phase 3.4 is stable:

```bash
# Start Phase 3.4 stack
cd agent
docker compose up -d prometheus grafana alertmanager otel-collector

# Verify services are healthy
docker compose ps
# Should show: prometheus, grafana, alertmanager, otel-collector all "Up"

# Check metrics are flowing into Prometheus
curl -s http://localhost:9090/api/v1/query?query=up | jq '.data.result | length'
# Should return > 3 (at least Prometheus, Grafana, AlertManager)

# Verify Grafana dashboard loads
curl -s http://localhost:3000/api/health | jq '.database'
# Should return "ok"
```

### Step 2: Start Phase 3.5 Services

All three services can be started simultaneously (they are independent):

```bash
# Start all Phase 3.5 services
docker compose up -d jaeger loki promtail

# Verify all services are running and healthy
docker compose ps

# Expected: jaeger, loki, promtail all "Up" with "(healthy)" status
```

### Step 3: Verify Service Connectivity

Test each service individually:

#### 3a. Verify Jaeger is reachable

```bash
# Jaeger UI should be accessible
curl -f http://localhost:16686/ > /dev/null && echo "✓ Jaeger UI accessible"

# Jaeger health endpoint
curl -s http://localhost:14250/healthz | jq .
# Should return 200 OK
```

#### 3b. Verify Loki is reachable

```bash
# Loki ready endpoint (health check)
curl -f http://localhost:3100/ready && echo "✓ Loki is ready"

# Loki health endpoint
curl -s http://localhost:3100/loki/api/v1/status/buildinfo | jq .
# Should return Loki version info
```

#### 3c. Verify Promtail is running

```bash
# Promtail metrics endpoint
curl -s http://localhost:9080/metrics | head -20

# Should return Prometheus-format metrics starting with "# HELP"
```

---

## Integration Testing

### Test 1: Jaeger Trace Collection

Verify that OpenTelemetry traces from the Task Service are reaching Jaeger:

```bash
# 1. Start the task service (if not already running)
python3 agent/task_service.py &

# 2. Generate a test request
curl -X POST http://localhost:8000/submit \
  -H "Content-Type: application/json" \
  -d '{
    "practice": "autonomy",
    "task_type": "understanding",
    "input": "Test trace flow"
  }'

# 3. Open Jaeger UI and verify trace appears
# Navigate to: http://localhost:16686
# - Service: should show "task-service"
# - Look for recent traces in the last 1 minute
# - Click on a trace to see full span details

# 4. Expected span structure:
# - http.request.submit (top-level)
#   └── queue.enqueue
#       └── worker.execute
```

**Success Criteria:**
- ✅ Traces visible in Jaeger UI within 30 seconds of request
- ✅ Span hierarchy matches task submission flow
- ✅ Latency data accurate (queue wait + worker execution time)
- ✅ Error traces include exception details if applicable

### Test 2: Loki Log Aggregation

Verify that container logs are being collected and are queryable:

```bash
# 1. Trigger some application logs
# (Task service should be running from Test 1)

# 2. Query Loki directly via curl
curl -G \
  -d 'query={container="task-service-empirica-evaluator"}' \
  -d 'limit=10' \
  http://localhost:3100/loki/api/v1/query_range

# Should return recent logs in JSON format

# 3. Query via Grafana (recommended for exploration)
# - Open http://localhost:3000/explore
# - Select "Loki" datasource
# - Use LogQL query: {service="task-service"} | json
# - Click "Run query"
# - Should show logs from the last hour

# 4. Test log filtering
# Query by service label
curl -G \
  -d 'query={service="prometheus"}' \
  http://localhost:3100/loki/api/v1/query_range

# Query by stream (stderr = errors)
curl -G \
  -d 'query={stream="stderr"}' \
  http://localhost:3100/loki/api/v1/query_range
```

**Success Criteria:**
- ✅ Container logs appear in Loki within 10 seconds
- ✅ Service labels are populated correctly
- ✅ Stream labels distinguish stdout from stderr
- ✅ Log pagination works (limit parameter respected)
- ✅ Grafana Explore can query and display logs

### Test 3: Per-Practice Dashboard Filtering

Verify that per-practice dashboards show only their respective metrics:

```bash
# 1. Generate requests for multiple practices
for practice in autonomy mesh-support outreach; do
  curl -X POST http://localhost:8000/submit \
    -H "Content-Type: application/json" \
    -d "{
      \"practice\": \"$practice\",
      \"task_type\": \"understanding\",
      \"input\": \"Test for $practice\"
    }"
done

# 2. Open Grafana Dashboards
# Navigate to http://localhost:3000/dashboards

# 3. For each practice dashboard (autonomy, mesh-support, outreach):
# - Click the dashboard
# - Verify request_rate shows only that practice's metrics
# - Verify success/failure rates are per-practice
# - Verify alerts route to practice-specific Slack channel

# 4. Verify shared metrics (queue depth, error rate) appear on all dashboards
```

**Success Criteria:**
- ✅ Each practice dashboard shows only its metrics
- ✅ Request rates by practice are isolated
- ✅ Success/failure rates per practice are accurate
- ✅ Shared metrics (queue depth) appear on all dashboards
- ✅ No metric crossover between practices

### Test 4: Observability Stack End-to-End

Complete integration test covering all three enhancements:

```bash
# 1. Create a test scenario with multiple requests
python3 << 'PYTHON'
import requests
import time

# Submit requests for trace and log generation
for i in range(5):
    requests.post("http://localhost:8000/submit", json={
        "practice": "autonomy",
        "task_type": "understanding",
        "input": f"Test request {i}"
    })
    time.sleep(1)

print("✓ Requests submitted")
PYTHON

# 2. Verify Prometheus metrics
curl -s http://localhost:9090/api/v1/query?query=task_requests_total | jq '.data.result[0].value[1]'
# Should show a number > 5

# 3. Verify Jaeger traces
curl -s 'http://localhost:16686/api/traces?service=task-service&limit=5' | jq '.data | length'
# Should show at least 5 traces

# 4. Verify Loki logs
curl -s -G -d 'query={service="task-service"}' -d 'limit=50' \
  http://localhost:3100/loki/api/v1/query_range | jq '.data.result | length'
# Should show logs from recent requests

# 5. Verify Grafana can display all three data sources
# - Open http://localhost:3000/explore
# - Switch between Prometheus, Jaeger, and Loki datasources
# - Each should show live data from the previous requests
```

**Success Criteria:**
- ✅ All three data sources working in parallel
- ✅ Metrics, traces, and logs correlated by timestamp
- ✅ No service interference or cascading failures
- ✅ Latency from request to Grafana visibility < 30 seconds

---

## Troubleshooting

### Loki Startup Issues

**Problem:** Loki container exits immediately

```bash
# Check logs
docker logs loki-empirica-evaluator | tail -50

# Common causes:
# 1. Permission denied on /loki volumes
#    Solution: docker compose down && docker volume rm loki_data loki_wal
#    Then restart: docker compose up -d loki

# 2. Schema compatibility (v11/v12 mismatch)
#    Check config: grep "schema: v" agent/loki-config.yml
#    Solution: Ensure schema: v12 in config and volumes are clean

# 3. Port conflict (3100 already in use)
#    Check: lsof -i :3100
#    Solution: Change docker-compose port mapping if needed
```

### Promtail Not Shipping Logs

**Problem:** No logs appearing in Loki after Promtail is running

```bash
# Check Promtail logs
docker logs promtail-empirica-evaluator | grep -i error

# Common causes:
# 1. Loki connection refused
#    Solution: Verify loki service is healthy
#    docker compose ps loki  # Should show "(healthy)"

# 2. Docker socket permission denied
#    Solution: May need to run: sudo usermod -aG docker $USER
#    Then restart docker: docker compose restart promtail

# 3. Positions file locked
#    Solution: Remove and restart
#    rm -f /tmp/positions.yaml && docker compose restart promtail
```

### Jaeger Not Receiving Traces

**Problem:** Jaeger UI shows no traces from task service

```bash
# Check OTEL Collector config
grep -A 5 "jaeger:" agent/otel-collector-config.yml

# Check OTEL Collector logs
docker logs otel-collector-empirica-evaluator | grep -i jaeger

# Common causes:
# 1. OTEL Collector not exporting to Jaeger
#    Verify config exports to: jaeger:14250 (gRPC)

# 2. Task service not sending traces
#    Check task_service.py for OTEL initialization
#    Verify OTEL_EXPORTER_OTLP_ENDPOINT is set

# 3. Jaeger gRPC receiver port misconfigured
#    Check docker-compose mapping: 14250:14250
```

### Performance Issues

**Problem:** High CPU/memory usage from Loki or Promtail

```bash
# Monitor resource usage
docker stats loki promtail

# Check for known issues:

# 1. Too many concurrent log streams
#    Promtail may create stream per container if labels are too granular
#    Review promtail-config.yml relabel_configs
#    Reduce label cardinality if needed

# 2. Compactor running continuously
#    Add to loki-config.yml compactor section:
#    compaction_interval: 30m  # Increase from 10m

# 3. Retention not working
#    Verify in loki-config.yml:
#    retention_enabled: true
#    retention_delete_delay: 2h
```

---

## Verification Checklist

Before considering Phase 3.5 complete, verify:

- [ ] **Jaeger**
  - [ ] Jaeger UI accessible at http://localhost:16686
  - [ ] Traces from task-service visible in UI
  - [ ] Span timing data accurate
  - [ ] Error traces captured with exception details
  
- [ ] **Loki**
  - [ ] Loki ready endpoint returns 200: `curl -f http://localhost:3100/ready`
  - [ ] Promtail healthy: `docker compose ps promtail` shows "(healthy)"
  - [ ] Container logs queryable in Grafana Explore
  - [ ] Log filtering by service/stream working
  
- [ ] **Per-Practice Dashboards**
  - [ ] Each practice has its own dashboard
  - [ ] Dashboards filter by practice label correctly
  - [ ] Request rates per practice are isolated
  - [ ] Shared metrics (queue depth) visible on all dashboards
  
- [ ] **Integration**
  - [ ] All services coexist without interference
  - [ ] No port conflicts or cascading failures
  - [ ] Health checks passing for all services
  - [ ] Logs show no errors or warnings

---

## Performance Baselines

Expected resource usage and latency:

| Component | CPU | Memory | Disk | Startup |
|-----------|-----|--------|------|---------|
| Jaeger | <5% idle | ~150MB | 2GB (week) | <30s |
| Loki | <5% idle | ~300MB | 5GB (30d) | <40s |
| Promtail | <2% idle | ~50MB | <100MB | <10s |
| **Total** | **<12%** | **~500MB** | **~7GB** | **<60s** |

Latency from event to visibility:
- Jaeger traces: < 2 seconds
- Promtail logs: < 10 seconds
- Prometheus metrics: < 15 seconds (scrape interval)

---

## Next Steps

1. **Phase 3.6:** SLO/SLI tracking
   - Define SLOs for request latency, error rate, availability
   - Implement SLI dashboards in Grafana
   - Connect to alerting rules

2. **Phase 3.7:** Cost optimization
   - Analyze Loki retention vs. storage cost
   - Implement log sampling for high-volume services
   - Archive old traces to cold storage

3. **Documentation:**
   - Update runbook with Loki/Jaeger troubleshooting
   - Create dashboarding best practices guide
   - Document metrics naming conventions for new services

---

## References

- Phase 3.3: Observability Instrumentation
- Phase 3.4: Observability Stack Deployment
- Phase 3.5 Assessment: `docs/PHASE_3_5_ASSESSMENT.md`
- Loki Configuration: `agent/loki-config.yml`
- Promtail Configuration: `agent/promtail-config.yml`
- OTEL Collector Config: `agent/otel-collector-config.yml`
- Grafana Datasources: `agent/grafana-datasources.yml`

---

**Prepared by:** Claude (empirica-foundation-evaluator)  
**Status:** Ready for Deployment
