# Local-Only Metrics Stack — Stopgap Configuration
**Purpose:** Epistemic metrics collection if Phase 3.5.6 (shared infrastructure) cannot deploy by 2026-08-26  
**Deployment time:** 30 minutes (immediate)  
**Scope:** Evaluator seat only (not shared across practices)  
**Suitable for:** Week 1 development/testing; NOT production measurement phase  
**Fallback tier:** Tier 3 (acceptable 48h, unacceptable beyond)

---

## Architecture: Local Development Stack

```
Evaluator Epistemic Metrics
    ↓
    ├─ Calibration drift (empirica CLI)
    ├─ Unknown accumulation (cortex logs)
    └─ Artifact discipline (git metrics)
    
    ↓ (collected locally)
    
Prometheus (port 9090)
├─ Schema: empirica_seat_metrics
├─ Retention: 30 days
└─ Storage: /tmp/prometheus_data (or ~/metrics)

    ↓
    
Grafana (port 3000)
├─ Dashboard: Evaluator Epistemic Health (4-panel)
├─ Auth: local (no external)
└─ Accessible: http://localhost:3000

    ↓
    
Local CSV Export
├─ Weekly snapshot: metrics_WEEK_N.csv
├─ Location: ./docs/measurements/
└─ Manual upload to measurement ceremony platform
```

---

## Deployment Steps (30 min)

### Step 1: Install Dependencies
```bash
# macOS
brew install prometheus grafana

# Linux
sudo apt-get install prometheus grafana-server

# Verify
prometheus --version
grafana-server -v
```

### Step 2: Configure Prometheus

Create `prometheus.yml`:
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'empirica-evaluator'
    static_configs:
      - targets: ['127.0.0.1:9090']
    
  - job_name: 'epistemic-metrics'
    static_configs:
      - targets: ['127.0.0.1:8000']
```

### Step 3: Start Prometheus
```bash
# Terminal 1
prometheus --config.file=prometheus.yml --storage.tsdb.path=/tmp/prometheus_data
```

### Step 4: Start Grafana
```bash
# Terminal 2
grafana-server --config=/path/to/grafana.conf
# Access: http://localhost:3000 (admin/admin)
```

### Step 5: Configure Grafana Dashboard

Dashboard panels:
1. **Calibration Drift** — empirica vectors (know, do, state) trend
2. **Unknown Accumulation** — unknown-log count + resolution rate
3. **Artifact Discipline** — finding/decision/assumption/deadend ratio
4. **Measurement Phase Progress** — Week 1 opportunity deployment tracking

### Step 6: Metrics Collection (Manual)
```bash
# Weekly snapshot (run Monday after measurement window closes)
empirica stats --week 1 --output json > docs/measurements/metrics_week1.json
empirica project-search --task "calibration drift" --output json >> metrics_week1.json

# Export to CSV for ceremony
python3 docs/scripts/metrics_to_csv.py metrics_week1.json > metrics_week1.csv
```

---

## Limitations

| Limitation | Impact | Workaround |
|-----------|--------|-----------|
| **Local-only** | Not visible to other practices | Manual CSV export to measurement ceremony |
| **No real-time sync** | Week 1 data must be manually collected Monday morning | Schedule snapshot collection |
| **Development-grade** | Not production-ready for multi-week tracking | Suitable only for Week 1 validation |
| **Manual export** | Measurement ceremony requires manual upload | Automate via `docs/scripts/metrics_to_csv.py` |

---

## Measurement Ceremony Integration

**How Week 1 metrics flow with local-only stack:**

1. **Sunday 2026-08-25 EOD:** Prometheus retention includes full Week 1 data
2. **Monday 2026-08-26 09:00 UTC:** Evaluator runs metrics snapshot
3. **Monday 2026-08-26 09:15 UTC:** CSV exported to `docs/measurements/metrics_week1.csv`
4. **Monday 2026-08-26 09:30 UTC:** Upload CSV to measurement ceremony platform (manual)
5. **Monday 2026-08-26 10:00 UTC:** Evaluator report ready for opportunity-aggregator + mesh-support digest

**Format (CSV export):**
```
timestamp,metric,week,value,unit
2026-08-20T10:00:00Z,calibration_drift_know,1,0.85,dimensionless
2026-08-20T10:00:00Z,unknown_accumulation,1,23,count
2026-08-20T10:00:00Z,artifact_discipline_ratio,1,0.92,ratio
...
```

---

## Activation Trigger

**Deploy this stack if:**
- Phase 3.5.6 escalation is REJECTED by David, OR
- Phase 3.5.6 is not deployed by 2026-08-25 EOD, OR
- SSH blocker remains unresolved 48 hours before measurement phase

**Deployment decision point:** 2026-08-24 12:00 UTC (48 hours before measurement start)

---

## Upgrade Path (Week 2+)

Once local-only stack is validated:
1. Pivot to Cloudflare Workers alternative (production-grade, shared)
2. Migrate local metrics to Cloudflare Durable Objects
3. Activate shared Grafana dashboard (cross-practice visibility)
4. Phase out local development stack

See: `docs/CLOUDFLARE_WORKERS_ALTERNATIVE.md` for production upgrade path.

---

**Status:** Ready to deploy (no external dependencies, no network blocker)  
**Effort:** 30 minutes  
**Test:** Tuesday 2026-08-21 (dry-run snapshot)  
**Go-live:** 2026-08-26 (if Phase 3.5.6 unavailable)
