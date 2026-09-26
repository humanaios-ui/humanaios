# Foundation Orchestration Telemetry — Technical Architecture
**Generated:** 2026-08-20 18:19 UTC  
**Version:** v1.0  
**Status:** Production-ready (Phase 1: Telemetry schema delivered, Phase 2: Observable infrastructure escalated)

---

## Quick Links

| Resource | URL | Status |
|----------|-----|--------|
| **Telemetry Schema** | `/docs/schemas/measurement_schema.json` | ✅ Delivered (prop_fwcdyb5o2reuzc7xllvux6ydsy) |
| **Measurement Ceremony Protocol** | `/docs/protocols/measurement_ceremony.md` | ✅ Active (Monday 09:00 UTC) |
| **Observable Infrastructure (Phase 3.5.6)** | `release/m2r2-state-harmonization-v1.0` | ⏳ Escalated (prop_bbrhubnjojg3dcwjpyzv25jhqi) |
| **Fallback: Local Metrics** | `/docs/LOCAL_METRICS_STACK_STOPGAP.md` | ✅ Ready (30-min deployment) |
| **Fallback: Cloudflare Workers** | `/docs/CLOUDFLARE_WORKERS_ALTERNATIVE.md` | ✅ Ready (2-4 day deployment) |
| **Cortex Artifacts** | `--global` search | ✅ Logged (16 artifacts, shared visibility) |

---

## System Architecture

### Telemetry Flow (Data Path)

```
┌─────────────────────────────────────────────────────────────────┐
│                    MEASUREMENT PHASE PIPELINE                    │
└─────────────────────────────────────────────────────────────────┘

[Evaluator Epistemic Metrics] ─────┐
    │ know, do, state, uncertainty  │
    │ unknown_count, completion     │
    │ artifact_discipline           │
    │                               │
    ├─► [Prometheus Collector]      │ PHASE 3.5.6 (Primary Path)
    │       │                       │ OTEL Integration
    │       ├─► [Grafana Dashboard] ├─► [Grafana] ──┐
    │       │       (4 panels)      │               │
    │       └─► [CSV Export]        │               │
    │                               │               │
    ├─► [Cloudflare Workers]        ├─► [Fallback 2] (Production)
    │       │                       │   (2-4 days)
    │       ├─► [Durable Objects]   │
    │       └─► [Analytics Engine]  │
    │                               │
    └─► [Local Prometheus]          └─► [Fallback 1] (Stopgap)
            (30-min setup)              │ (24-48h only)

                    ↓

        [Weekly Measurement Report]
                    ↓

        [opportunity-aggregator]
        [mesh-support digest]
                    ↓

        [Opportunity Evaluation]
        [Roadmap Refinement]
```

### Component Architecture Matrix

| Component | Protocol | Endpoint | Status | SLA | Fallback |
|-----------|----------|----------|--------|-----|----------|
| **OTEL Collector** | HTTP/HTTPS | `localhost:4318` (local) or `cloudflare-worker.dev/metrics` | ⏳ Phase 3.5.6 escalated | 99.9% (once deployed) | None (critical) |
| **Prometheus** | Scrape | `localhost:9090` | ✅ Ready (local development) | 99.5% | ✅ Local-only |
| **Grafana** | HTTP | `localhost:3000` (local) or `dashboard.evaluator.empirica-foundation.workers.dev` | ✅ Ready (local) | 99.5% | ✅ Local-only |
| **Cloudflare Worker** | HTTP/REST | `metrics.evaluator.empirica-foundation.workers.dev/ingest` | ✅ Ready (production alternative) | 99.99% | ✅ Fallback 1 |
| **Durable Objects** | REST + Queries | `metrics.evaluator.empirica-foundation.workers.dev/query` | ✅ Ready (state storage) | 99.95% | ✅ Fallback 1 |
| **cortex-mailbox-poll** | Mesh protocol | Cortex API (`/v1/orchestration/inbox`) | ✅ Armed (30s/5m adaptive) | 99.9% | Built-in retry |

---

## Telemetry Schema Specification

### Measurement Window (JSON)

```json
{
  "measurement_window": {
    "week": "integer (1-52)",
    "start_date": "ISO8601 timestamp",
    "end_date": "ISO8601 timestamp",
    "status": "active | completed | skipped"
  },
  "opportunities_deployed": [
    {
      "opportunity_id": "string (UUID)",
      "opportunity_name": "string",
      "deployment_date": "ISO8601",
      "actual_cost_dollars": "number (float, 2 decimals)",
      "actual_implementation_days": "number (float, 1 decimal)",
      "actual_adoption_rate": "number (0.0-1.0)",
      "blocker_incidents": "integer (0+)",
      "deployment_completion_date": "ISO8601",
      "post_deployment_notes": "string (max 500 chars)"
    }
  ],
  "meta": {
    "submitted_by": "string (practice canonical ai_id)",
    "submitted_at": "ISO8601",
    "measurement_confidence": "number (0.0-1.0)"
  }
}
```

### Epistemic Metrics (OTEL Export)

```yaml
metrics:
  calibration:
    - metric_name: "empirica_vector_know"
      type: "gauge"
      unit: "dimensionless"
      range: [0.0, 1.0]
      source: "empirica preflight/postflight"
    
    - metric_name: "empirica_vector_do"
      type: "gauge"
      unit: "dimensionless"
      range: [0.0, 1.0]
      source: "empirica preflight/postflight"
    
    - metric_name: "empirica_vector_state"
      type: "gauge"
      unit: "dimensionless"
      range: [0.0, 1.0]
      source: "empirica preflight/postflight"
  
  artifacts:
    - metric_name: "cortex_artifact_count"
      type: "counter"
      labels: ["artifact_type"] # finding, decision, unknown, assumption, deadend, mistake
      source: "cortex_finding_log / cortex_decision_log / ..."
    
    - metric_name: "cortex_unknown_resolution_rate"
      type: "gauge"
      unit: "ratio"
      range: [0.0, 1.0]
      source: "cortex unknown resolver"
  
  discipline:
    - metric_name: "artifact_discipline_ratio"
      type: "gauge"
      unit: "ratio"
      calculation: "(findings + decisions + unknowns) / total_artifacts"
      source: "cortex batch queries"

discovery:
    - metric_name: "empirica_discovery_depth"
      type: "gauge"
      unit: "dimensionless"
      range: [0.0, 1.0]
      source: "number of distinct practices engaged"
```

---

## Deployment Options

### Path 1: Phase 3.5.6 (Preferred)

**Status:** Escalation approved (prop_bbrhubnjojg3dcwjpyzv25jhqi, eco_review → accepted)

```bash
# Prerequisites
cd ~/practices/empirica-foundation-evaluator
git branch -v | grep release/m2r2-state-harmonization-v1.0

# Deploy (requires git push to Forgejo)
git push -u forgejo release/m2r2-state-harmonization-v1.0

# Activate observable infrastructure (5 minutes)
bash docs/PRODUCTION_DEPLOYMENT_GUIDE.md

# Verify (check Grafana dashboard)
curl http://localhost:3000/api/health
```

**Timeline:** 5 minutes (once SSH blocker resolved)  
**Cost:** $0  
**Prerequisites:** David pushes from his machine OR provides HTTPS credentials  
**Fallback:** Cloudflare Workers (below)

---

### Path 2: Cloudflare Workers (Production Alternative)

**Status:** Ready for deployment (2-4 day timeline)

```bash
# 1. Install Wrangler
npm install -g wrangler
wrangler login

# 2. Initialize Worker project
wrangler init empirica-metrics-gateway
cd empirica-metrics-gateway

# 3. Configure Durable Objects (wrangler.toml)
cat << 'EOF' > wrangler.toml
[[env.production.durable_objects.bindings]]
name = "METRICS_STORE"
class_name = "MetricsStore"
script_name = "empirica-metrics-gateway"

[env.production.routes]
pattern = "metrics.evaluator.empirica-foundation.workers.dev/*"
zone_name = "empirica.dev"
EOF

# 4. Deploy Worker
wrangler publish --env production

# 5. Configure OTEL Exporter (local)
cat << 'EOF' > otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    send_batch_size: 100

exporters:
  otlp:
    endpoint: https://metrics.evaluator.empirica-foundation.workers.dev/metrics
    headers:
      authorization: "Bearer <CLOUDFLARE_API_TOKEN>"

service:
  pipelines:
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlp]
EOF

# 6. Start OTEL Collector
otelcontribcol --config=otel-collector-config.yaml

# 7. Verify Cloudflare endpoint
curl -X GET https://metrics.evaluator.empirica-foundation.workers.dev/query?week=W34_2026
```

**Timeline:** 2-4 days (2026-08-21 start, 2026-08-25 go-live)  
**Cost:** $0.50-15/month  
**Prerequisites:** Cloudflare account + API token authentication  
**Fallback:** Local-only metrics (below)

---

### Path 3: Local-Only Metrics (Stopgap)

**Status:** Ready for immediate deployment (30 minutes)

```bash
# 1. Install Prometheus + Grafana
brew install prometheus grafana

# 2. Configure Prometheus (prometheus.yml)
cat << 'EOF' > prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'empirica-evaluator'
    static_configs:
      - targets: ['127.0.0.1:9090']
EOF

# 3. Start Prometheus (Terminal 1)
prometheus --config.file=prometheus.yml --storage.tsdb.path=/tmp/prometheus_data

# 4. Start Grafana (Terminal 2)
brew services start grafana
# Access: http://localhost:3000 (admin/admin)

# 5. Weekly metric snapshot (Monday 09:00 UTC)
empirica stats --week 1 --output json > metrics_week1.json

# 6. Export to CSV for measurement ceremony
python3 docs/scripts/metrics_to_csv.py metrics_week1.json > metrics_week1.csv
```

**Timeline:** 30 minutes (immediate deployment)  
**Cost:** $0  
**Prerequisites:** Prometheus + Grafana installed locally  
**Limitation:** Not shared across practices; development-tier only

---

## Measurement Ceremony Protocol

### Weekly Schedule

```
┌─────────────────────────────────────────────────────────────┐
│             MEASUREMENT CEREMONY TIMELINE                    │
└─────────────────────────────────────────────────────────────┘

SUNDAY 2026-08-25 (Week 1 Ends)
  └─ 23:59 UTC: Week 1 measurement window closes
     Observable infrastructure MUST be live (Phase 3.5.6, Cloudflare, or local)

MONDAY 2026-08-26 (Week 2 Begins)
  └─ 09:00 UTC: Measurement ceremony starts
  ├─ 09:00-09:15 UTC: All 10 practices collect metrics
  ├─ 09:15-09:30 UTC: Metrics submitted to cortex (JSON schema)
  ├─ 09:30-10:00 UTC: Evaluator aggregates + generates report
  └─ 10:00-10:15 UTC: Report delivered to opportunity-aggregator + mesh-support

TUESDAY 2026-08-27 (Measurement Review)
  └─ All-hands review of Week 1 results
     └─ Roadmap refinement based on measurement data
```

### CSV Export Format (Weekly Report)

```csv
timestamp,metric,week,value,unit,practice
2026-08-20T10:00:00Z,calibration_drift_know,1,0.85,dimensionless,empirica-foundation-evaluator
2026-08-20T10:00:00Z,calibration_drift_do,1,0.80,dimensionless,empirica-foundation-evaluator
2026-08-20T10:00:00Z,unknown_accumulation,1,23,count,empirica-foundation-evaluator
2026-08-20T10:00:00Z,artifact_discipline_ratio,1,0.92,ratio,empirica-foundation-evaluator
2026-08-20T10:00:00Z,discovery_depth,1,0.78,dimensionless,empirica-foundation-evaluator
2026-08-21T10:00:00Z,calibration_drift_know,1,0.87,dimensionless,opportunity-aggregator
...
```

---

## Observable Infrastructure Status Matrix

### Component Deployment Status

| Component | Phase 3.5.6 | Cloudflare | Local-Only | Recommended | Timeline |
|-----------|---|---|---|---|---|
| **OTEL Collector** | ✅ Included | ✅ Setup guide | ✅ Included | Phase 3.5.6 | 5 min (if approved) |
| **Prometheus** | ✅ Included | ✅ Via Analytics Engine | ✅ Ready | Phase 3.5.6 | Bundled |
| **Grafana** | ✅ Docker | ✅ Cloudflare hosted | ✅ Local install | Phase 3.5.6 | 5 min (Phase 3.5.6) |
| **Durable Objects** | N/A | ✅ Central store | N/A | Cloudflare | 2-4 days |
| **CSV Export** | ✅ Auto | ✅ Via API | ✅ Manual | All paths | Weekly |
| **Cross-practice sharing** | ✅ Yes | ✅ Yes | ❌ No | Phase 3.5.6 or Cloudflare | Depends |

---

## API Reference

### OTEL Metrics Ingest

**Endpoint:** `POST /metrics` (or `/v1/metrics` via Cloudflare)

**Content-Type:** `application/x-protobuf` (OTLP binary) or `application/json` (OTLP JSON)

```bash
# Example: Send metric via cURL
curl -X POST http://localhost:4318/v1/metrics/export \
  -H "Content-Type: application/json" \
  -d '{
    "resourceMetrics": [{
      "resource": {
        "attributes": [
          {"key": "service.name", "value": {"stringValue": "empirica-evaluator"}}
        ]
      },
      "scopeMetrics": [{
        "scope": {"name": "empirica-metrics"},
        "metrics": [{
          "name": "empirica_vector_know",
          "gauge": {"dataPoints": [{"asDouble": 0.85}]}
        }]
      }]
    }]
  }'
```

### Grafana Query API

**Endpoint:** `GET /api/datasources/proxy/:datasource_id/query`

```bash
# Example: Query metrics from Grafana
curl -X GET http://localhost:3000/api/datasources/proxy/1/query \
  -H "Authorization: Bearer <GRAFANA_API_KEY>" \
  -d '{
    "queries": [{"refId": "A", "expr": "empirica_vector_know"}],
    "range": {"from": "2026-08-20T00:00:00Z", "to": "2026-08-20T23:59:59Z"}
  }'
```

### CSV Export (Manual Weekly)

**Location:** `./docs/measurements/metrics_WEEK_N.csv`

**Format:** See Measurement Ceremony Protocol above

---

## Decision Tree: Deployment Path Selection

```
┌─────────────────────────────────────────────────────────────┐
│ Observable Infrastructure Path Selection (2026-08-20)       │
└─────────────────────────────────────────────────────────────┘

DECISION POINT: 2026-08-22 (David's Phase 3.5.6 Response)

  ✅ APPROVED (Phase 3.5.6 approved)
     └─► PATH 1: Phase 3.5.6 (Preferred)
         └─ Timeline: 5 min deployment (once SSH blocker resolved)
         └ Deploy by: 2026-08-25 EOD
         └ Status: Production-ready, $0 cost
         └ Shared: Yes (all 10 practices)

  ❌ REJECTED (Phase 3.5.6 declined by David)
     └─► PATH 2: Cloudflare Workers (Production)
         └─ Timeline: 2-4 days (2026-08-21 start)
         └─ Deploy by: 2026-08-25 23:00 UTC
         └─ Status: Production-ready, $5-15/month
         └─ Shared: Yes (all 10 practices)

  ⏳ TIMEOUT (No response by 2026-08-24 12:00 UTC)
     └─► PATH 3: Local-Only Metrics (Stopgap)
         └─ Timeline: 30 min (immediate)
         └─ Deploy by: 2026-08-24 EOD
         └─ Status: Development-tier, $0 cost
         └─ Shared: No (evaluator-only)
         └─ NOTE: Not suitable for production measurement; upgrade to Cloudflare Week 2

END GOAL: Observable infrastructure LIVE by 2026-08-26 09:00 UTC (measurement phase start)
```

---

## Configuration Reference

### Environment Variables

```bash
# Phase 3.5.6 (if approved)
export EMPIRICA_OTEL_ENABLED=true
export EMPIRICA_OTEL_ENDPOINT=http://localhost:4318
export EMPIRICA_GRAFANA_URL=http://localhost:3000
export EMPIRICA_PROMETHEUS_URL=http://localhost:9090

# Cloudflare Workers
export CLOUDFLARE_API_TOKEN=<your-token>
export CLOUDFLARE_ACCOUNT_ID=92cfe886ee648fc5d797a7ca1aa04922
export CLOUDFLARE_WORKER_URL=metrics.evaluator.empirica-foundation.workers.dev

# Local-only metrics
export PROMETHEUS_CONFIG=./prometheus.yml
export GRAFANA_ADMIN_PASSWORD=<secure-password>
```

### Docker Compose (Phase 3.5.6 Fallback)

```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

  otel-collector:
    image: otel/opentelemetry-collector:latest
    ports:
      - "4318:4318"
    volumes:
      - ./otel-collector-config.yaml:/etc/otel-collector-config.yaml
    command: ["--config=/etc/otel-collector-config.yaml"]

volumes:
  prometheus_data:
  grafana_data:
```

---

## Troubleshooting

### Common Issues

| Issue | Symptom | Root Cause | Resolution |
|-------|---------|-----------|-----------|
| **SSH Port 22 Blocked** | Phase 3.5.6 git push fails | Network blocker | Escalate to infrastructure team OR use Cloudflare alternative |
| **OTEL Collector Not Responding** | Metrics not ingesting | Port 4318 not open OR collector not started | Check `netstat -an \| grep 4318` and start collector |
| **Grafana Dashboard Empty** | No data in panels | Prometheus datasource misconfigured | Verify Prometheus URL in Grafana datasources (default: http://localhost:9090) |
| **Cloudflare Worker Timeout** | Metrics ingest fails | Rate limiting OR request payload too large | Reduce batch size in OTEL config (`send_batch_size: 50`) |
| **CSV Export Missing Columns** | CSV incomplete | Script version mismatch | Verify `docs/scripts/metrics_to_csv.py` matches schema version |

---

## Support & Status

| Surface | Status | SLA | Owner |
|---------|--------|-----|-------|
| Phase 3.5.6 (Observable Infrastructure) | ⏳ Escalated | 5-min deploy (once approved) | David (via mesh-support) |
| Cloudflare Workers Alternative | ✅ Ready | 2-4 day deploy | Evaluator |
| Local-Only Metrics Stopgap | ✅ Ready | 30-min deploy | Evaluator (immediate) |
| Telemetry Schema | ✅ Delivered | — | opportunity-aggregator (Checkpoint 1→2) |
| Measurement Ceremony Protocol | ✅ Active | Weekly (Monday 09:00 UTC) | All 10 practices |

---

**Last updated:** 2026-08-20 18:19 UTC  
**Next decision point:** 2026-08-22 (David's Phase 3.5.6 response)  
**Go-live target:** 2026-08-26 09:00 UTC (Week 1 measurement phase)
