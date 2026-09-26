# Phase 3.5.3: Grafana Dashboard Templates

## Overview

6 dashboards consuming Loki (logs) + Jaeger (traces) data:
1. **Empirica Phase Latency** — Transaction phase duration trends
2. **Multi-Practice Traces** — Request flow visualization
3. **Log Completeness** — Log ingestion per practice/phase
4. **Vector Calibration** — ACAT metrics (predicted vs actual)
5. **Practice Deep-Dive (Autonomy)** — Single-practice view
6. **Cross-Practice Integration** — All practices + mesh coordination

---

## Dashboard 1: Empirica Phase Latency

**Purpose:** Monitor transaction phase durations (PREFLIGHT → CHECK → POSTFLIGHT)

**Metrics:**
- `max(duration_ms) per phase` from Loki
- Trend line (last 7 days)
- P95 latency per practice

**Panels:**

### Panel 1a: Phase Duration Trend (Loki)
```
Query: 
  {job="empirica-sessions"} 
  | json 
  | phase != "" 
  | duration_ms > 0
  
Line chart:
  X-axis: time
  Y-axis: duration_ms (ms)
  Series: phase (PREFLIGHT, CHECK, POSTFLIGHT)
  Colors: PREFLIGHT=blue, CHECK=orange, POSTFLIGHT=green
```

Expected output:
```
PREFLIGHT:   ~120 ms
CHECK:       ~50 ms
POSTFLIGHT:  ~150 ms
```

### Panel 1b: P95 Latency per Phase (Gauge)
```
Query:
  {job="empirica-sessions"} 
  | json 
  | phase != ""
  | duration_ms > 0
  | line_format "{{phase}}: {{duration_ms}}"
  
Gauge:
  Show: P95 value for each phase
  Thresholds: <100ms (green), <200ms (yellow), >200ms (red)
```

### Panel 1c: Phase Duration by Practice (Heatmap)
```
Query:
  {job="empirica-sessions"} 
  | json 
  | practice != "" 
  | phase != ""
  | duration_ms > 0
  
Heatmap:
  X-axis: practice (autonomy, mesh-support, outreach, website, humanaios)
  Y-axis: phase (PREFLIGHT, CHECK, POSTFLIGHT)
  Value: avg(duration_ms)
  Color scale: <100ms (green) → >300ms (red)
```

### Panel 1d: Latency SLA Status (Stat)
```
Query:
  {job="empirica-sessions"}
  | json
  | duration_ms < 300  // SLA: <300ms total per phase

Display:
  Count of compliant phases / Total phases
  Format: "1,234 / 1,250 (98.8%)"
  Color: green if >95%, yellow if >90%, red if <90%
```

---

## Dashboard 2: Multi-Practice Traces

**Purpose:** Visualize request flow across practice boundaries

**Metrics:**
- Trace count per source→target pair
- Trace latency distribution
- Error rate per request type

**Panels:**

### Panel 2a: Request Flow (Sankey/Flow Diagram)
```
Query (Jaeger API):
  GET /api/traces?service=gateway&limit=100
  
Process:
  For each trace:
    - Extract: source_practice → target_practice
    - Count occurrences
    - Calculate avg latency
  
Visualization:
  Sankey diagram or node-link diagram:
  Nodes: autonomy, mesh-support, outreach, website, humanaios
  Edges: request flow (width = count, color = avg latency)
  
Expected:
  autonomy → mesh-support: 45 requests, 120ms avg
  mesh-support → autonomy: 38 requests, 95ms avg
  autonomy → outreach: 12 requests, 200ms avg
```

### Panel 2b: Request Type Distribution (Pie)
```
Query (Loki):
  {job="empirica-sessions"} 
  | json 
  | request_type != ""
  
Pie chart:
  Slices: collab_brief, proposal, ack, reply, etc.
  Label: request_type (count)
  
Expected:
  collab_brief: 65%
  proposal: 20%
  reply: 10%
  ack: 5%
```

### Panel 2c: Trace Latency Percentiles (Bar)
```
Query (Jaeger):
  Compute percentiles for each source→target pair:
  P50, P95, P99
  
Bar chart:
  X-axis: source→target pairs
  Y-axis: latency (ms)
  Series: P50 (blue), P95 (orange), P99 (red)
  
Expected:
  autonomy→mesh-support: P50=100, P95=150, P99=250
```

### Panel 2d: Error Traces (Table)
```
Query (Jaeger):
  GET /api/traces?tags=result=error&limit=20
  
Table columns:
  - traceID
  - source_practice
  - target_practice
  - latency (ms)
  - error_type
  - timestamp
  
Sort by: timestamp (desc)
Link traceID to Jaeger UI
```

---

## Dashboard 3: Log Completeness

**Purpose:** Monitor log ingestion health

**Metrics:**
- Logs per phase per practice
- Missing phase detection
- Log query performance

**Panels:**

### Panel 3a: Log Count by Phase (Stacked Bar)
```
Query:
  {job="empirica-sessions"} 
  | json 
  | phase != ""
  | count by phase, practice
  
Stacked bar:
  X-axis: time (hourly)
  Y-axis: log count
  Series: PREFLIGHT, CHECK, POSTFLIGHT
  
Expected pattern:
  Equal counts per phase (1 PREFLIGHT = 1 CHECK = 1 POSTFLIGHT per session)
```

### Panel 3b: Log Completeness Heatmap (by Practice)
```
Query:
  For each practice:
    PREFLIGHT_count, CHECK_count, POSTFLIGHT_count
  
Heatmap:
  X-axis: practice
  Y-axis: phase
  Value: count
  Color: full (green) if count > threshold, partial (yellow), missing (red)
  
Expected: All cells green (no missing phases)
```

### Panel 3c: Log Query Latency (Timeseries)
```
Query (Loki metrics):
  histogram_quantile(0.95, 
    rate(loki_request_duration_seconds_bucket{handler="query"}[5m])
  )
  
Line chart:
  X-axis: time
  Y-axis: latency (seconds)
  Target: <100ms SLA
  
Expected: <0.1s (100ms) most of the time
```

### Panel 3d: Practice-Stdout Log Ingestion (Gauge)
```
Query:
  {job="practice-stdout"} 
  | count by practice
  
Multi-gauge:
  One gauge per practice
  Show: total log count
  Color: green if >=100 logs, yellow if >=10, red if <10
  
Expected:
  autonomy: 500+ logs
  mesh-support: 300+ logs
  outreach: 150+ logs
```

---

## Dashboard 4: Vector Calibration (ACAT)

**Purpose:** Monitor epistemic vector calibration (predicted vs actual)

**Metrics:**
- Brier score per vector per practice
- Calibration error trend
- Vector-specific accuracy

**Panels:**

### Panel 4a: Brier Score by Vector (Gauge Grid)
```
Query:
  {job="acat-grounding"} 
  | json 
  | vector_name != ""
  | brier_error > 0
  
Multi-gauge (one per vector):
  know, do, context, clarity, coherence, signal, density, 
  state, change, completion, impact
  
Display: avg(brier_error) per vector
Thresholds: 
  <=0.01 (green, excellent)
  <=0.05 (yellow, acceptable)
  >0.05 (red, needs attention)
  
Expected:
  know: 0.0016 (green)
  uncertainty: 0.0025 (green)
  clarity: 0.0089 (yellow)
```

### Panel 4b: Calibration Error Trend (Timeseries)
```
Query:
  {job="acat-grounding"} 
  | json 
  | brier_error > 0
  | line_format "{{vector_name}}: {{brier_error}}"
  
Line chart:
  X-axis: time (daily)
  Y-axis: avg(brier_error)
  Series: per-vector trend
  
Expected: Trend line declining (calibration improving over time)
```

### Panel 4c: Predicted vs Actual Scatter (by Vector)
```
Query (Jaeger span tags):
  For each vector in POSTFLIGHT spans:
    Extract: vector.name_predicted, vector.name_actual
  
Scatter plot (per vector tab):
  X-axis: predicted (0.0-1.0)
  Y-axis: actual (0.0-1.0)
  Series: points colored by phase
  Diagonal line: perfect calibration (y=x)
  
Expected:
  Points clustered around y=x line
  If below line: overconfident
  If above line: underconfident
```

### Panel 4d: Per-Practice Calibration (Table)
```
Query:
  {job="acat-grounding"} 
  | json 
  | group by ai_id, vector_name
  | avg(brier_error) per group
  
Table columns:
  - practice (ai_id)
  - vector_name
  - brier_error
  - improvement_trend (↑/↓)
  
Sort by: brier_error (desc)
Highlight: rows with brier_error >0.05 (red background)
```

---

## Dashboard 5: Practice Deep-Dive (Autonomy)

**Purpose:** Single-practice operational view

**Metrics:**
- All phases + traces for one practice
- Error traces highlighted
- Session timeline

**Panels:**

### Panel 5a: Session Timeline (Timeline)
```
Query:
  {practice="autonomy"} 
  | json 
  | session_id, timestamp, phase, duration_ms
  
Timeline (bucket by hour):
  Y-axis: phases (PREFLIGHT, CHECK, POSTFLIGHT)
  X-axis: time
  Bar height: duration_ms
  Color: green (success), red (error)
  
Expected: Regular transaction pattern
```

### Panel 5b: All Traces for Autonomy (Trace Table)
```
Query (Jaeger):
  GET /api/traces?service=autonomy&limit=50
  
Table columns:
  - traceID (link to Jaeger UI)
  - duration (ms)
  - span_count
  - error_count
  - timestamp
  
Filter toggles:
  - Show errors only
  - Show slow traces (>500ms)
  - Date range picker
```

### Panel 5c: Vector Heatmap (Autonomy)
```
Query:
  {practice="autonomy"} 
  | json 
  | vector values per POSTFLIGHT
  
Heatmap:
  X-axis: vector names (know, do, context, clarity, etc.)
  Y-axis: time (daily buckets)
  Value: avg(vector_value)
  Color: <0.5 (red) → >0.8 (green)
  
Expected: Most vectors >0.7 (high confidence)
```

### Panel 5d: Error Log Explorer (Logs)
```
Query:
  {practice="autonomy", level="error"}
  | json
  
Log panel:
  Show raw logs with syntax highlighting
  Timestamp, level, message
  Link to Loki UI for full search
```

---

## Dashboard 6: Cross-Practice Integration

**Purpose:** Mesh-wide coordination view

**Metrics:**
- All practices performance
- Mesh coordination latency
- Bottleneck detection

**Panels:**

### Panel 6a: Practice Health Matrix (Heatmap)
```
Query:
  For each practice:
    - avg(duration_ms) per phase
    - count(errors)
    - avg(vector_values)
  
Heatmap:
  X-axis: practice (autonomy, mesh-support, outreach, website, humanaios)
  Y-axis: health_metric (latency, errors, calibration, log_health)
  Value: composite_score (0-1)
  Color: <0.7 (red) → >0.9 (green)
  
Expected: All practices green (healthy)
```

### Panel 6b: Mesh Request Volume (Stat + Sparkline)
```
Query:
  {job="empirica-sessions"} 
  | count by source_practice, target_practice
  | sum by source_practice
  
Multi-stat:
  One stat per practice
  Show: total request count (last 24h)
  Sparkline: request rate trend
  
Expected:
  autonomy: 1,200 requests
  mesh-support: 1,000 requests
```

### Panel 6c: Mesh Latency Percentiles (Gauge)
```
Query (Jaeger):
  Compute for all traces:
  P50, P95, P99 latency
  
Display:
  Three gauges showing mesh-wide latency percentiles
  Thresholds: <150ms (P50 green), <250ms (P95 yellow), <500ms (P99)
  
Expected:
  P50: 120ms
  P95: 180ms
  P99: 280ms
```

### Panel 6d: Cross-Practice Flow Matrix (Table)
```
Query:
  For each source→target pair:
    count(requests), avg(latency), error_rate
  
Table:
  Rows: source practice
  Columns: target practice
  Value: count (with latency as tooltip, color by error_rate)
  
Expected:
  Diagonal sparse (no self-requests)
  Off-diagonal populated (inter-practice traffic)
```

### Panel 6e: Bottleneck Alerts (Alert List)
```
Query:
  Alert conditions:
  1. Latency >300ms (any practice)
  2. Error rate >5%
  3. Missing logs in phase
  4. Calibration error >0.05
  5. Trace completeness <95%
  
Display:
  Alert list with:
  - Alert name
  - Practice + metric
  - Severity (critical/warning)
  - Time firing
  - Action links (drill-down)
```

---

## Query Reference

### Loki Queries

**All empirica logs:**
```
{job="empirica-sessions"}
```

**Logs by phase:**
```
{job="empirica-sessions"} | json | phase="POSTFLIGHT"
```

**Logs by practice:**
```
{job="empirica-sessions", practice="autonomy"}
```

**Log count per phase:**
```
{job="empirica-sessions"} | json | phase != "" | count by phase
```

**Phase duration:**
```
{job="empirica-sessions"} | json | phase != "" | duration_ms > 0
```

**Practice stdout logs:**
```
{job="practice-stdout", practice="autonomy"}
```

**ACAT metrics:**
```
{job="acat-grounding"} | json | vector_name="know"
```

### Jaeger Queries

**All traces:**
```
GET /api/traces?limit=100
```

**Traces by service:**
```
GET /api/traces?service=autonomy&limit=50
```

**Traces by tag:**
```
GET /api/traces?tags=source_practice=autonomy&limit=20
```

**Slow traces:**
```
GET /api/traces?minDuration=500ms&limit=20
```

**Error traces:**
```
GET /api/traces?tags=result=error&limit=20
```

---

## Dashboard Provisioning

Each dashboard is defined as JSON (Grafana 9.0+ format).

**Structure:**
```json
{
  "dashboard": {
    "title": "Dashboard Name",
    "panels": [
      {
        "title": "Panel Name",
        "targets": [
          {
            "datasource": "Loki" or "Jaeger",
            "expr": "query",
            "refId": "A"
          }
        ],
        "type": "graph|gauge|stat|heatmap|etc.",
        "gridPos": {"x": 0, "y": 0, "w": 12, "h": 8}
      }
    ],
    "refresh": "30s",
    "time": {"from": "now-7d", "to": "now"}
  }
}
```

**Deployment via Grafana HTTP API:**
```bash
curl -X POST http://localhost:3000/api/dashboards/db \
  -H "Authorization: Bearer $GRAFANA_TOKEN" \
  -H "Content-Type: application/json" \
  -d @dashboard-name.json
```

---

## Validation Checklist

- [ ] All 6 dashboards load without errors
- [ ] Datasources (Loki + Jaeger) resolve correctly
- [ ] Panels display data (no "no data" messages)
- [ ] Queries return results within 5 seconds
- [ ] Colors match expected ranges (green/yellow/red)
- [ ] Cross-links work (e.g., traceID → Jaeger UI)
- [ ] Auto-refresh works (30s default)
- [ ] Time range picker functional
- [ ] All tooltips display correctly
- [ ] No data loss on panel resize

---

## Performance Targets

| Dashboard | Panel | Query Latency | Data Points |
|-----------|-------|---------------|------------|
| 1 | Phase Duration Trend | <1s | 100+ |
| 2 | Request Flow | <2s | 20-50 |
| 3 | Log Completeness | <1s | 10-20 |
| 4 | Brier Score | <1s | 13 vectors |
| 5 | Session Timeline | <2s | 50-100 |
| 6 | Practice Health | <2s | 50+ |

**Overall dashboard load time:** <5 seconds (all panels loaded)

---

## Next Steps

1. **Task 1**: Design dashboards (this file) ✓
2. **Task 2**: Framework + provisioning scripts
3. **Task 3**: Create per-practice variants
4. **Task 4**: Implement trace visualization
5. **Task 5**: Validation + testing
6. **Task 6**: Integration + handoff to Phase 3.5 complete
