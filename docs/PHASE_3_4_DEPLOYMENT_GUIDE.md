# Phase 3.4 Deployment Guide: Observability Stack

Complete guide for deploying and testing the observability stack (Prometheus, OpenTelemetry, Grafana, AlertManager).

## Prerequisites

- Docker & Docker Compose installed
- Task service running on localhost:5000 with `/metrics` endpoint
- OPENROUTER_API_KEY environment variable set (for Bifrost)
- Optional: Slack webhook URL for alert notifications

## Directory Structure

```
agent/
├── docker-compose.yaml           # All services definition
├── prometheus.yml                # Prometheus scrape config
├── alerting_rules.yaml           # 7 alert rules
├── otel-collector-config.yml    # OpenTelemetry Collector config
├── grafana-datasources.yml      # Grafana datasource provisioning
└── alertmanager.yml             # AlertManager routing config
```

## Quick Start (5 minutes)

### 1. Set environment variables

```bash
# Optional: Slack integration for alerts
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# Optional: Custom webhook for testing
export WEBHOOK_URL="http://localhost:5001/alerts"
```

### 2. Deploy the stack

```bash
cd agent/
docker-compose up -d
```

### 3. Verify services are running

```bash
# Check all services
docker-compose ps

# Expected output:
# CONTAINER            STATUS
# bifrost-empirica...  Up
# prometheus-empirica  Up (healthy)
# otel-collector-...   Up (healthy)
# grafana-empirica...  Up (healthy)
# alertmanager-...     Up (healthy)
```

### 4. Access services

| Service | URL | Default Credentials |
|---------|-----|-------------------|
| **Prometheus** | http://localhost:9090 | None |
| **Grafana** | http://localhost:3000 | admin / admin |
| **AlertManager** | http://localhost:9093 | None |
| **Task Service** | http://localhost:5000/metrics | None |

---

## Task 3: Grafana Integration Verification

### Step 1: Verify Prometheus datasource

1. Open Grafana: http://localhost:3000
2. Login: admin / admin
3. Navigate to **Configuration → Data Sources**
4. Check that **Prometheus** datasource exists
   - URL: `http://prometheus:9090`
   - Access: Proxy
   - Status: Green (connected)

### Step 2: Import observability dashboard

1. In Grafana, navigate to **Create → Import**
2. Copy-paste content from `docs/PHASE_3_GRAFANA_DASHBOARD.json`
3. Select Prometheus as datasource
4. Click "Import"

### Step 3: Verify dashboard displays data

1. Open the imported dashboard: "Phase 3.3 - Task Service Observability"
2. Verify panels are populated with metrics:
   - ✅ Queue Depth (should show current queue size)
   - ✅ Active Workers (should show worker count)
   - ✅ Request Rate (should show requests/sec)
   - ✅ Error Rate (should show error percentage)
   - ✅ Latency Percentiles (should show p50/p95/p99)
   - ✅ Queue Wait Time (should show average wait)
   - ✅ Tasks Processed (success/failed split)

**If data doesn't appear:**
- Check Prometheus targets: http://localhost:9090/targets
- Verify task-service is reachable on the docker network
- Check docker logs: `docker-compose logs prometheus`

---

## Task 4: Alert Routing Verification

### Step 1: Verify Prometheus alerting rules loaded

1. Open Prometheus: http://localhost:9090
2. Navigate to **Alerts**
3. Verify all 7 alert rules are listed:
   - ✅ HighErrorRate
   - ✅ QueueDepthHigh
   - ✅ TaskLatencyHigh
   - ✅ WorkerPoolUnavailable
   - ✅ RequestLatencyHigh
   - ✅ QueueWaitTimeHigh
   - ✅ TaskFailureRateHigh

**If rules are missing:**
- Check docker logs: `docker-compose logs prometheus`
- Verify alerting_rules.yaml syntax: `docker-compose exec prometheus promtool check rules /etc/prometheus/alerting_rules.yaml`

### Step 2: Verify AlertManager is receiving alerts

1. Open AlertManager: http://localhost:9093
2. Check **Status** page - should show:
   - Uptime status
   - Configuration version
   - Message queue stats

### Step 3: Test alert routing (webhook simulation)

Create a simple webhook receiver to test routing:

```bash
# Start a simple HTTP server to receive alerts (in another terminal)
python3 -m http.server 5001 --directory /tmp
```

Set webhook URL:
```bash
export WEBHOOK_URL="http://localhost:5001"
docker-compose restart alertmanager
```

### Step 4: Trigger a test alert

Manually trigger the error rate alert by causing failures:

```bash
# Submit an invalid task to trigger error rate increase
for i in {1..20}; do
  curl -X POST http://localhost:5000/api/tasks/submit \
    -H "Content-Type: application/json" \
    -d '{
      "requesting_practice": "invalid",
      "title": "Test",
      "description": "Test"
    }' 2>/dev/null
done

# Wait 5 minutes for evaluation
# Then check AlertManager Alerts page - should show HighErrorRate alert
```

**Expected:** Alert fires in AlertManager → Routed to webhook → Alert message appears

### Step 5: Verify Slack integration (if webhook configured)

If SLACK_WEBHOOK_URL is set:
1. Alerts should post to configured Slack channel
2. Check channel for alert messages
3. Verify both critical and warning alerts appear

---

## Task 5: End-to-End Integration Testing

### Full System Test Checklist

#### 1. Metrics Flow (Task Service → Prometheus)

```bash
# Check task service metrics endpoint
curl http://localhost:5000/metrics | head -20

# Expected: Prometheus-formatted metrics with:
# - requests_total
# - queue_depth
# - active_workers
# - task_latency_seconds
```

#### 2. Prometheus Scraping

```bash
# Verify Prometheus scrapes task-service
curl http://localhost:9090/api/v1/query?query=requests_total
# Expected: JSON response with metric values
```

#### 3. Grafana Data Display

```bash
# Test Grafana datasource API
curl http://localhost:3000/api/datasources
# Expected: Prometheus datasource listed
```

#### 4. Alerting Pipeline

```bash
# Verify alert evaluation
curl http://localhost:9090/api/v1/query?query=ALERTS
# Expected: JSON with alert states
```

#### 5. Distributed Tracing (OTel)

```bash
# Check if task service is sending traces
docker-compose logs otel-collector | grep "span"
# Expected: Trace ingestion logs from gRPC receiver
```

### Load Test & Threshold Verification

Generate load to trigger alerts:

```bash
# Task 1: Queue load (to test QueueDepthHigh alert)
for i in {1..100}; do
  curl -X POST http://localhost:5000/api/tasks/submit \
    -H "Content-Type: application/json" \
    -d '{
      "requesting_practice": "empirica-foundation.carly.empirica-autonomy",
      "title": "Load test $i",
      "description": "Testing queue depth",
      "priority": 1
    }' 2>/dev/null &
done
# Wait 5 minutes, check if QueueDepthHigh alert fires

# Task 2: Error rate (to test HighErrorRate alert)
for i in {1..100}; do
  curl -X POST http://localhost:5000/api/tasks/submit \
    -H "Content-Type: application/json" \
    -d '{"invalid": "request"}' 2>/dev/null &
done
# Wait 5 minutes, check if HighErrorRate alert fires
```

### Monitoring Commands

```bash
# Watch Prometheus targets
watch -n 5 'curl -s http://localhost:9090/api/v1/query?query=up | jq .'

# Watch active alerts
watch -n 5 'curl -s http://localhost:9090/api/v1/query?query=ALERTS | jq .'

# Tail Prometheus logs
docker-compose logs -f prometheus | grep -E "alert|scrape"

# Tail AlertManager logs
docker-compose logs -f alertmanager | grep -E "send|webhook"
```

---

## Troubleshooting

### Prometheus can't scrape task-service

**Symptom:** No data in Grafana  
**Cause:** Task service unreachable at http://task-service:5000  
**Fix:**
```bash
# Verify task service is running on host
curl http://localhost:5000/metrics

# If running externally, update prometheus.yml:
# Change: targets: ['task-service:5000']
# To: targets: ['host.docker.internal:5000']  # macOS/Windows
# Or: targets: ['172.17.0.1:5000']             # Linux
docker-compose restart prometheus
```

### Grafana datasource shows "No Data Source"

**Symptom:** Grafana can't query Prometheus  
**Cause:** Datasource provisioning not applied  
**Fix:**
```bash
# Restart Grafana to reload provisioning
docker-compose restart grafana

# Verify datasource was created
curl http://localhost:3000/api/datasources | jq '.[] | {name, url}'
```

### Alerts not firing

**Symptom:** No alerts in AlertManager despite high error rate  
**Cause:** Alert evaluation interval not reached or threshold not exceeded  
**Fix:**
```bash
# Verify alert rules syntax
docker-compose exec prometheus promtool check rules /etc/prometheus/alerting_rules.yaml

# Check alert evaluation in Prometheus
curl http://localhost:9090/api/v1/query?query=ALERTS

# Increase evaluation frequency temporarily (for testing)
# Edit prometheus.yml: evaluation_interval: 5s
docker-compose restart prometheus
```

### AlertManager not sending webhooks

**Symptom:** Alerts in Prometheus but not in AlertManager  
**Cause:** AlertManager configuration or webhook URL incorrect  
**Fix:**
```bash
# Check AlertManager config
docker-compose exec alertmanager cat /etc/alertmanager/alertmanager.yml

# Verify AlertManager can reach webhook
docker-compose exec alertmanager curl -X GET ${WEBHOOK_URL} 2>&1

# Check AlertManager logs
docker-compose logs alertmanager | tail -20
```

---

## Cleanup

```bash
# Stop all services
docker-compose down

# Remove volumes (persistent data)
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

---

## Next Steps (Phase 3.5)

- [ ] Integrate Jaeger for distributed trace visualization
- [ ] Add Loki for log aggregation
- [ ] Set up PagerDuty escalation for critical alerts
- [ ] Implement custom dashboards for per-practice metrics
- [ ] Add SLO/SLI tracking via Prometheus recording rules

---

**Last Updated:** 2026-07-30  
**Applicable:** Phase 3.4 Deployment  
**Status:** Production-Ready (pending docker deployment verification)
