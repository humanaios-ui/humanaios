# Cloudflare Workers Alternative — Production Observable Infrastructure
**Purpose:** Production-grade epistemic metrics infrastructure if Phase 3.5.6 (git-based deployment) is rejected or blocked  
**Deployment time:** 2-4 days (2026-08-21 to 2026-08-25)  
**Scope:** Foundation-wide (shared across all practices via Cloudflare API)  
**Suitable for:** Week 1+ production measurement phase  
**Tier:** Production (acceptable for indefinite deployment)

---

## High-Level Architecture

```
Evaluator Epistemic Metrics Collection
    ↓
OTEL Collector (local, evaluator environment)
    ├─ Calibration drift tracking
    ├─ Unknown accumulation monitoring
    └─ Artifact discipline metrics
    
    ↓ (HTTP/HTTPS, no SSH required)
    
Cloudflare Worker (metrics gateway)
├─ Receives metrics via OTEL export protocol
├─ Validates + routes by practice
└─ Forwards to Durable Object store
    
    ↓
    
Cloudflare Durable Objects (global state)
├─ Persistent metrics store (cross-org, cross-tenant)
├─ Time-series indexing (week-based)
├─ TTL: 90 days (compliance retention)
└─ Replicated across Cloudflare regions
    
    ↓
    
Cloudflare Analytics Engine
├─ Querying interface
├─ Aggregation (daily/weekly)
└─ Export to Grafana (API bridge)
    
    ↓
    
Grafana Dashboard (shared)
├─ Seat epistemic health (4-panel)
├─ Multi-practice comparison (analytics)
└─ Accessible: evaluator + mesh-support + opportunity-aggregator
    
    ↓
    
Measurement Ceremony Reporting
├─ Weekly auto-generated report
├─ Distributed to all practices
└─ Feeds opportunity evaluation + roadmap refinement
```

---

## Resource Requirements

### Cloudflare Account Setup

| Resource | Details | Cost | Status |
|----------|---------|------|--------|
| **Workers Free Plan** | 100K requests/day | $0/month | ✅ Sufficient for Week 1 |
| **Durable Objects** | Persistent state, 1GB data | $0.15 per GB-month | ~$1-2 for Week 1 |
| **Analytics Engine** | Query + export | Included with Workers | ✅ Included |
| **Total (Week 1)** | — | ~$2-5 | **Acceptable** |

### Worker Configuration

```javascript
// src/index.ts — Metrics Gateway Worker

export default {
  async fetch(request, env, ctx) {
    // Route incoming OTEL metrics
    if (request.method === 'POST' && request.url.includes('/metrics')) {
      const metrics = await request.json();
      
      // Persist to Durable Objects
      const durableObject = env.METRICS_STORE.get('week_' + currentWeek());
      await durableObject.put('metrics_batch', metrics);
      
      // Return 200 OK
      return new Response(JSON.stringify({ ok: true }));
    }
    
    // Query interface (for Grafana)
    if (request.method === 'GET' && request.url.includes('/query')) {
      const query = new URL(request.url).searchParams;
      const week = query.get('week') || currentWeek();
      
      const durableObject = env.METRICS_STORE.get('week_' + week);
      const metrics = await durableObject.get('metrics_batch') || [];
      
      return new Response(JSON.stringify(metrics));
    }
    
    return new Response('Not found', { status: 404 });
  }
};

function currentWeek() {
  const now = new Date();
  const start = new Date(now.getFullYear(), 0, 1);
  const week = Math.ceil((now - start) / (7 * 24 * 60 * 60 * 1000));
  return `W${week}_${now.getFullYear()}`;
}
```

### Durable Object Configuration

```toml
# wrangler.toml

[[env.production.durable_objects.bindings]]
name = "METRICS_STORE"
class_name = "MetricsStore"
script_name = "empirica-metrics-gateway"

[env.production.routes]
pattern = "metrics.evaluator.empirica-foundation.workers.dev/*"
zone_name = "empirica.dev"
```

---

## Deployment Steps (2-4 Days)

### Phase 1: Cloudflare Setup (4 hours)

**Day 1 (2026-08-21):**

1. **Authenticate & Authorize**
   ```bash
   # Run /mcp in Claude Code
   # Select "claude.ai Cloudflare Developer Platform"
   # Authorize with account 92cfe886ee648fc5d797a7ca1aa04922
   ```

2. **Install Wrangler CLI**
   ```bash
   npm install -g wrangler
   wrangler login
   ```

3. **Create Worker Project**
   ```bash
   wrangler init empirica-metrics-gateway
   cd empirica-metrics-gateway
   ```

4. **Configure Durable Objects**
   - Edit `wrangler.toml` (add durable object bindings)
   - Define `MetricsStore` class
   - Set up routes to `metrics.evaluator.empirica-foundation.workers.dev`

### Phase 2: OTEL Integration (8 hours)

**Day 2 (2026-08-22):**

1. **Install OTEL Exporter**
   ```bash
   pip install opentelemetry-exporter-otlp-proto-http
   pip install opentelemetry-sdk
   ```

2. **Configure OTEL Collector (local)**
   ```yaml
   # otel-collector-config.yaml
   receivers:
     otlp:
       protocols:
         http:
           endpoint: 0.0.0.0:4318
   
   processors:
     batch:
       send_batch_size: 100
       timeout: 10s
   
   exporters:
     otlp:
       endpoint: https://metrics.evaluator.empirica-foundation.workers.dev/metrics
       headers:
         authorization: "Bearer <CLOUDFLARE_API_TOKEN>"
   
   service:
     pipelines:
       traces:
         receivers: [otlp]
         processors: [batch]
         exporters: [otlp]
       metrics:
         receivers: [otlp]
         processors: [batch]
         exporters: [otlp]
   ```

3. **Start OTEL Collector**
   ```bash
   otelcontribcol --config=otel-collector-config.yaml
   ```

4. **Instrument Empirica CLI**
   - Add OTEL instrumentation to `empirica` commands
   - Export metrics: know, do, state, uncertainty vectors
   - Export findings/unknown/artifact counts

### Phase 3: Grafana Integration (8 hours)

**Day 3 (2026-08-23):**

1. **Install Grafana**
   ```bash
   brew install grafana
   # or docker run -d -p 3000:3000 grafana/grafana
   ```

2. **Add Cloudflare Analytics Engine Data Source**
   - URL: `https://api.cloudflare.com/client/v4/accounts/{account_id}/analytics_engine`
   - Auth: Bearer token (Cloudflare API)
   - Default database: `empirica_metrics`

3. **Create Dashboard**
   - Panel 1: Calibration drift (know/do/state trend)
   - Panel 2: Unknown accumulation (count + resolution rate)
   - Panel 3: Artifact discipline (finding/decision/assumption/deadend ratio)
   - Panel 4: Week 1 opportunity tracking (by practice)

4. **Publish Dashboard**
   - Export as JSON: `dashboard_evaluator_epistemic_health.json`
   - Store in version control: `docs/grafana/dashboards/`

### Phase 4: Testing & Validation (8 hours)

**Day 4 (2026-08-24):**

1. **Dry-Run Metrics Collection**
   ```bash
   empirica stats --week 1 --otel-export cloudflare
   ```

2. **Verify Cloudflare Data**
   ```bash
   wrangler tail empirica-metrics-gateway
   # Should show incoming metrics + storage operations
   ```

3. **Test Grafana Queries**
   - Load dashboard at http://localhost:3000
   - Verify all panels populate data
   - Test multi-practice view

4. **Measurement Ceremony Integration Test**
   - Simulate Week 1 report generation
   - Verify CSV export from Grafana
   - Validate format against opportunity-aggregator schema

### Phase 5: Production Activation (30 min)

**Day 5 (2026-08-25, 23:00 UTC):**

1. **Final Deploy**
   ```bash
   wrangler publish
   ```

2. **Enable OTEL Export**
   - Point evaluator environment OTEL collector → Cloudflare Worker
   - Verify no errors in logs

3. **Standby Ready**
   - Observable infrastructure live 1 hour before Week 1 measurement starts

---

## Cost & Pricing

### Week 1 Estimate (2026-08-20 to 2026-08-26)

| Component | Usage | Cost |
|-----------|-------|------|
| **Workers Requests** | 100K requests/week (estimation) | Free (under 1M limit) |
| **Durable Objects** | 500MB data write | $0.50 |
| **Analytics Engine** | Queries + exports | Included |
| **Egress** | ~10MB | Free (Cloudflare network) |
| **TOTAL** | — | **~$0.50** |

### Ongoing (Monthly)

| Tier | Usage | Cost | Notes |
|------|-------|------|-------|
| **Small** | <1M requests/month | $0 | Week 1-2 (development) |
| **Standard** | 1M-10M requests/month | $5-15/month | Week 3+ (5 practices) |
| **Enterprise** | >10M requests/month | Custom | If adopted org-wide (15+ practices) |

**Conclusion:** Cloudflare path is cost-effective ($5-15/month for foundation-wide deployment)

---

## Activation Trigger & Decision Points

### Trigger Condition
Deploy Cloudflare alternative if:
- Phase 3.5.6 escalation is **REJECTED** by David, OR
- Phase 3.5.6 is not deployed by **2026-08-25 EOD**, OR
- SSH blocker remains unresolved **48 hours before measurement start**

### Decision Timeline

```
2026-08-20: David receives escalation (prop_bbrhubnjojg3dcwjpyzv25jhqi)
    ↓
2026-08-22: Await David response (48h decision window)
    ├─ YES (approved) → Proceed with Phase 3.5.6 (git push)
    ├─ NO (rejected) → Activate Cloudflare Workers setup
    └─ TIMEOUT → Local-only stopgap (development)
    
2026-08-23: Cloudflare setup begins (if activated)
    ↓
2026-08-24: Testing & validation
    ↓
2026-08-25 23:00 UTC: Production deployment
    ↓
2026-08-26 09:00 UTC: Week 1 measurement starts (observable live)
```

---

## Comparison: Phase 3.5.6 vs. Cloudflare

| Dimension | Phase 3.5.6 (Git) | Cloudflare Workers | Local-Only |
|-----------|---|---|---|
| **Deployment** | 5 min (if blocker resolved) | 2-4 days | 30 min |
| **Network blocker** | SSH 22 to Forgejo | HTTP(S) to Cloudflare | None (local) |
| **Cost** | $0 (once deployed) | $5-15/month | $0 |
| **Production-ready** | ✅ Yes | ✅ Yes | ❌ Dev only |
| **Shared across practices** | ✅ Yes | ✅ Yes (better) | ❌ No |
| **Ready by 2026-08-26** | ✅ If approved + deployed by EOD 2026-08-25 | ✅ If setup starts 2026-08-21 | ✅ Immediate |

---

## Recommendation

**Preferred order:**
1. **First choice:** Phase 3.5.6 (git-based) — lowest friction, proven, $0 cost
2. **Second choice:** Cloudflare Workers — production-grade, if git blocker unresolvable (2-4 day setup acceptable)
3. **Last resort:** Local-only stopgap — acceptable 48h only, not production

**Decision point:** 2026-08-22 (when David's response arrives)

---

**Status:** Documentation ready  
**Activation:** Contingent on Phase 3.5.6 rejection  
**Setup window:** 2026-08-21 to 2026-08-25 (5 days available)  
**Go-live target:** 2026-08-26 (measurement phase start)
