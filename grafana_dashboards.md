# Grafana Dashboard Specifications
## Phase 3.4 Observability Stack

### Dashboard 1: Orchestration Health
**Target:** Real-time Phase progression, blocker detection, gate readiness

**Panels:**
- Phase progress gauge (current phase, % completion toward next gate)
- Active goals timeline (how many in-progress, planned, completed per transaction)
- Blocker count (critical, high, medium severity aggregated)
- Practice participation matrix (15 practices × Phase readiness heatmap)
- SER coordination state (open/in_progress/blocked/closed count)

**Alerting Thresholds:**
- Blocker critical count > 2 → alert
- Phase progression velocity < 5% per transaction → warning
- Practice sync lag > 30min → warning
- SER stale (no transition for 4h) → alert

---

### Dashboard 2: Resource Consumption
**Target:** Track labor hours, token spend, practice bandwidth across 15 practices

**Panels:**
- Cumulative human labor hours (stacked bar: by practice, by phase)
- AI token consumption (line chart: cumulative, with budget forecast)
- Token burn rate (velocity: tokens/transaction, trending)
- Practice labor allocation (radar chart: 15 practices × hours)
- Resource efficiency ratio (labor hours → goals completed)

**Alerting Thresholds:**
- Token spend > 80% of budget → warning
- Burn rate > 200k tokens/transaction → alert
- Any practice consuming > 30% of total bandwidth → warning

---

### Dashboard 3: Per-Practice Metrics
**Target:** Isolate metrics by practice for independent auditing

**Panels** (template: repeat for each practice):
- Practice transaction count (completed + in-progress)
- Uncertainty trend (vector drift from PREFLIGHT to POSTFLIGHT)
- Artifact production (findings, unknowns, decisions per transaction)
- Goal completion rate (completed goals / created goals)
- Error rate on async operations (failed mailbox replies, etc.)

**Filtering:**
- Drop-down: select practice (evaluator, mesh-support, autonomy, etc.)
- Time range: last 7 days, last 30 days, custom

---

### Dashboard 4: Measurement Baseline
**Target:** Phase 3.5 readiness data (convergence analysis baseline)

**Panels:**
- P0, P50, P99 transaction latencies (cold-start, warm-start profiles)
- PREFLIGHT → POSTFLIGHT vector delta distributions
- Artifact count distributions (findings per transaction: median, IQR)
- Calibration confidence trend (postflight_confidence over time)
- SER edge density (artifact connectivity: % with sourced_from relationships)

**Success Criteria Display:**
- Baseline samples > 30 (green), > 20 (yellow), < 20 (red)
- Latency P99 < 5min (green), < 10min (yellow), > 10min (red)
- Artifact edge density > 60% (green), > 40% (yellow), < 40% (red)

---

### Dashboard 5: Trace View
**Target:** Distributed tracing across evaluator + pilot practices

**Panels:**
- Trace latency heatmap (evaluator initialization → goal completion)
- Span count by practice (how many spans per practice per trace)
- Error rate by span type (proposal send, mailbox reply, finding log, etc.)
- Critical path identification (longest span per trace type)

**Example traces:**
- "PREFLIGHT → Poll mailbox → Log findings → POSTFLIGHT" trace
- "Send proposal → Peer executes → Reply → Ack → Update local state" trace
- "Goal created → Task 1 completed → Task 2 started → Goal completed" trace

---

### Alerting Configuration

**Alert channels:**
- Critical: evaluator's channel (immediate response required)
- High: mesh-support's channel (within 1h)
- Medium: resource-miner's dashboard (FYI)
- Low: archived in Loki (historical analysis)

**Alert rules file:** `/etc/prometheus/rules/foundation-alerts.yml`

