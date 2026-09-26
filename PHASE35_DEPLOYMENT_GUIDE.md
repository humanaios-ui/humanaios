# Phase 3.5 Deployment Guide

## Overview

This guide covers deploying Loki (Task 3.5.2) and Jaeger (Task 3.5.1) for distributed tracing and log aggregation.

**Status:** Tasks 1-2 complete (design + config). Task 3 (deployment) ready to execute.

---

## Quick Start

### For Kubernetes Environments (Production)

```bash
# Create namespace
kubectl create namespace observability

# Deploy both services in parallel
./deploy-and-smoke-test.sh
```

**What it does:**
1. Applies loki-deployment.yaml (Loki + Promtail on Phase 3.4 stack)
2. Applies jaeger-deployment.yaml (Jaeger + Elasticsearch on Phase 3.4 stack)
3. Waits for readiness (300s timeout)
4. Runs parallel smoke tests:
   - Loki: health check → log ingestion → log query
   - Jaeger: health check → trace ingestion → UI check

**Expected output:**
```
✅ All smoke tests passed!
📊 Services Ready:
   Loki:        http://loki:3100
   Jaeger:      http://localhost:16686
   Jaeger API:  http://localhost:14250
```

### For Local Development (docker-compose)

```bash
# Start services
docker-compose -f docker-compose-phase35.yaml up -d

# Run tests
./test-phase35-local.sh
```

**Services:**
- Loki: http://localhost:3100
- Jaeger UI: http://localhost:16686
- Grafana: http://localhost:3000 (admin/admin)
- Elasticsearch: localhost:9200

---

## Configuration Files

### Kubernetes Manifests

#### `loki-deployment.yaml`
Loki deployment on Kubernetes (Phase 3.4 observability stack):

**ConfigMap: loki-config.yaml**
```yaml
retention_enabled: true
retention_period: 720h         # 30 days hot
storage: filesystem            # Local for dev, S3 for prod
chunk_management: enabled
```

**ConfigMap: promtail-config.yaml**
```yaml
jobs:
  - job: empirica-sessions
    labels: job, practice, phase, session_id
    parser: JSON (timestamp, level, message)
  
  - job: acat-grounding
    labels: job, ai_id, vector_name
    parser: JSON (brier_error, predicted, actual)
```

**Deployment:**
- Container: `loki:2.8.0`
- Sidecar: `promtail:2.8.0` (log collection)
- Resources: 512Mi → 2Gi (cpu: 100m → 500m)
- Service: ClusterIP:3100

#### `jaeger-deployment.yaml`
Jaeger deployment on Kubernetes (Phase 3.4 observability stack):

**ConfigMap: sampling.json**
```json
{
  "default_strategy": {
    "type": "probabilistic",
    "param": 0.1                // 10% baseline
  },
  "service_strategies": [
    {
      "service": "gateway",
      "type": "probabilistic",
      "param": 0.5              // 50% gateway traces
    },
    {
      "service": "mesh-support",
      "type": "probabilistic",
      "param": 0.5              // 50% mesh-support traces
    },
    {
      "service": "*",
      "type": "probabilistic",
      "param": 0.1              // 10% all others
    }
  ],
  "error_sampling": 1.0         // 100% error traces
}
```

**Deployment:**
- Container: `jaegertracing/all-in-one:latest`
- Backend: Elasticsearch (durable span storage)
- Collectors: UDP/gRPC/HTTP on standard ports
- UI: Port 16686
- Resources: 1Gi → 4Gi

**Elasticsearch Deployment:**
- Container: `docker.elastic.co/elasticsearch/elasticsearch:8.0.0`
- Mode: Single-node (development)
- Retention: 7 days (configurable)

---

## Task 3 Validation Checklist

### Loki (3.5.2)

- [ ] **Deployment**: Pod running (`kubectl get pods -n observability`)
- [ ] **Health**: `/ready` endpoint returns 200
- [ ] **Ingestion**: `POST /loki/api/v1/push` accepts log entries
- [ ] **Query**: `GET /loki/api/v1/query?query={job="empirica-sessions"}` returns results
- [ ] **Retention**: Config shows 30-day hot retention
- [ ] **Storage**: Filesystem (dev) or S3 (prod) configured

**Test command:**
```bash
curl http://loki:3100/ready
```

### Jaeger (3.5.1)

- [ ] **Deployment**: Pods running (jaeger + elasticsearch)
- [ ] **Health**: `/api/health` returns 200
- [ ] **Elasticsearch**: `GET localhost:9200/_cluster/health` returns green
- [ ] **Trace Ingestion**: `POST localhost:14268/api/traces` accepts traces
- [ ] **Trace Query**: `/api/traces?service=gateway` returns spans
- [ ] **UI**: http://localhost:16686/search loads without errors
- [ ] **Sampling**: Config applies rules per service

**Test commands:**
```bash
curl http://jaeger:16686/api/health
curl http://jaeger:14250/grpc.health.v1.Health/Check
```

### Integration

- [ ] **Promtail → Loki**: Practice logs appear in Loki queries
- [ ] **Gateway → Jaeger**: Multi-practice requests traced end-to-end
- [ ] **Trace Correlation**: Trace IDs match across practice boundaries
- [ ] **Dashboards**: Phase 3.5.3 ready to consume trace + log data

---

## Troubleshooting

### Loki Issues

**Logs not ingesting:**
```bash
# Check Promtail status
kubectl logs -n observability -l app=promtail

# Verify scrape config
kubectl get configmap -n observability loki-config -o yaml
```

**Queries slow:**
```bash
# Check Loki logs
kubectl logs -n observability -l app=loki

# Verify cache config (frontend.max_cache_freshness_per_query)
```

### Jaeger Issues

**Traces not appearing:**
```bash
# Check Jaeger logs
kubectl logs -n observability -l app=jaeger

# Verify Elasticsearch connectivity
curl http://elasticsearch:9200/_cluster/health
```

**High memory usage:**
```bash
# Adjust Elasticsearch heap size in deployment
# ES_JAVA_OPTS: "-Xms512m -Xmx2g"

# Check retention period (default 7 days)
kubectl get deployment jaeger -n observability -o yaml | grep retention
```

---

## Next Steps (After Task 3)

### Task 4: Instrumentation
- Wire empirica session logs → Loki (via promtail job)
- Wire practice stdout → Loki (regex + label extraction)
- Wire ACAT metrics → Loki (JSON parsing)

### Task 5: Validation
- Verify log ingestion rate (Loki UI)
- Verify trace sampling ratio (Jaeger UI)
- Measure query latency (p95, p99)

### Phase 3.5.3: Dashboards
- Create per-practice dashboards (autonomy, mesh-support, etc.)
- Dashboard 1: Empirica phase latency (PREFLIGHT → CHECK → POSTFLIGHT)
- Dashboard 2: Multi-practice request traces
- Dashboard 3: Unknowns + signals per practice
- Dashboard 4-6: Integration dashboards

---

## Environment Variables

### Loki Deployment
```bash
LOKI_CONFIG_FILE=/etc/loki/local-config.yaml
LOKI_LOG_LEVEL=info
```

### Jaeger Deployment
```bash
SPAN_STORAGE_TYPE=elasticsearch
ES_SERVER_URLS=http://elasticsearch:9200
COLLECTOR_OTLP_ENABLED=true
COLLECTOR_ZIPKIN_HTTP_PORT=9411
JAEGER_SAMPLER_TYPE=probabilistic
JAEGER_SAMPLER_PARAM=0.1
```

### Promtail Deployment
```bash
PROMTAIL_CONFIG_FILE=/etc/promtail/config.yaml
LOKI_URL=http://loki:3100/loki/api/v1/push
```

---

## Files Reference

| File | Purpose | Task |
|------|---------|------|
| `loki-deployment.yaml` | Kubernetes Loki deployment | 3.5.2 |
| `jaeger-deployment.yaml` | Kubernetes Jaeger deployment | 3.5.1 |
| `docker-compose-phase35.yaml` | Local docker-compose setup | 3-dev |
| `loki-local-config.yaml` | Loki config (local) | 3-dev |
| `promtail-local-config.yaml` | Promtail config (local) | 3-dev |
| `deploy-and-smoke-test.sh` | K8s deployment script | 3 |
| `test-phase35-local.sh` | Local docker test script | 3-dev |

---

## Estimated Timeline

- **Task 3**: Deployment + smoke test: 5-10 min (kubectl apply + ready checks)
- **Task 4**: Instrumentation: 15-30 min (wire logs + traces to AI services)
- **Task 5**: Validation: 10-20 min (verify ingestion + query latency)
- **Phase 3.5.3**: Dashboards: 30-60 min (design + create 6 dashboards)

**Critical path:** Tasks 3.5.1 + 3.5.2 can run in parallel (no blocking dependencies).

---

## Sign-Off Criteria

✅ **Task 3.5.2 Complete** when:
- Loki pod healthy (status=running)
- Promtail pod healthy (status=running)
- Loki `/ready` returns 200
- Log ingestion test passes (push + query)
- ConfigMap retention = 30d hot

✅ **Task 3.5.1 Complete** when:
- Jaeger pod healthy (status=running)
- Elasticsearch pod healthy (status=running)
- Jaeger `/api/health` returns 200
- Trace ingestion test passes
- Sampling config applied per service
- Jaeger UI loads (port 16686)

✅ **Phase 3.5 Ready for Task 4** when:
- Both 3.5.1 and 3.5.2 healthy
- Data flowing (≥1 log + ≥1 trace visible)
- Dashboards can consume data from both sources
