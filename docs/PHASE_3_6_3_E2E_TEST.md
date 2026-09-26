# Phase 3.6.3 Task 3.2: End-to-End Test — Live Transaction + Dashboard Verification

## Overview
This document provides the end-to-end test plan for verifying the complete OTEL span/metric pipeline:
Application → OTEL SDK → OTEL Collector (4317) → Prometheus (9090) + Jaeger (16686) ← Grafana (3000)

## Prerequisites (All ✓ Met)
- ✅ OTEL Collector running and healthy (Docker, listening on :4317 and :8889)
- ✅ Prometheus running and healthy (Docker, :9090)
- ✅ Jaeger running and healthy (Docker, :16686)
- ✅ Grafana running and healthy (Docker, :3000)
- ✅ Grafana datasources configured (Prometheus + Jaeger)
- ✅ Grafana dashboards imported (epistemic-vectors, transaction-detail)
- ✅ Instrumentation library deployed (empirica/otel_instrumentation.py)
- ✅ CLI hooks deployed (.empirica/hooks/preflight-post.py, postflight-post.py)
- ✅ Epistemic metrics module deployed (empirica/epistemic_metrics.py)

## Part A: Installation Requirements

When running in an environment WITH opentelemetry packages:

```bash
pip install opentelemetry-api opentelemetry-sdk \
  opentelemetry-exporter-otlp-proto-grpc \
  opentelemetry-exporter-prometheus
```

## Part B: Test Execution

When OTEL packages are available, run:

```bash
cd /Users/andersonfamily/practices/empirica-foundation-evaluator
python3 tests/test_phase363_e2e.py
```

Expected output:
- Initialize instrumentation ✓
- Start transaction (txn-<timestamp>) ✓
- Emit PREFLIGHT vectors ✓
- Simulate noetic phase (spans) ✓
- Simulate check phase (spans) ✓
- Simulate praxic phase (spans) ✓
- Emit POSTFLIGHT vectors ✓
- Query Jaeger: 6 spans found ✓
- Query Prometheus: 13 vector metrics recorded ✓
- Verify dashboard auto-update ✓

## Part C: Manual Verification Checklist

### Prometheus (http://localhost:9090)
- [ ] Query `empirica_know_gauge` → shows latest transaction's values
- [ ] Chart shows uptrend from PREFLIGHT → POSTFLIGHT
- [ ] All 13 vectors queryable

### Jaeger (http://localhost:16686)
- [ ] Service: `empirica-foundation-evaluator` listed
- [ ] One transaction span visible with 6 child spans
- [ ] Span timeline shows realistic durations (noetic + praxic phase visible)
- [ ] Operation spans listed under phases (e.g., empirica:op_code-write)

### Grafana — Epistemic Vectors Dashboard (http://localhost:3000/d/epistemic-vectors)
- [ ] Wait 30s for refresh
- [ ] 13-vector chart shows new data point
- [ ] Phase duration breakdown visible
- [ ] Query latency <1s

### Grafana — Transaction Detail Dashboard (http://localhost:3000/d/transaction-detail)
- [ ] Transaction summary table lists latest test transaction
- [ ] Vector progression shows PREFLIGHT → POSTFLIGHT
- [ ] Trace explorer links to Jaeger (click transaction_id)

## Part D: Latency SLAs

When live data is emitted:

| Metric | SLA | Measurement |
|--------|-----|-------------|
| Span → Jaeger | < 5s | Time from `close_transaction()` to span appears in Jaeger API |
| Metric → Prometheus | < 10s | Time from `emit_vector_metrics()` to query returns value |
| Dashboard Auto-Update | < 30s | Time from metric export to dashboard panel updates |

## Part E: Success Criteria

✅ All 10+ test steps pass
✅ Spans appear in Jaeger < 5 seconds
✅ Metrics appear in Prometheus < 10 seconds
✅ All three UIs (Prometheus, Jaeger, Grafana) show consistent data
✅ Dashboard query latency < 1 second
✅ Transaction_id correlation verified (same ID in traces + metrics)

## Current Status (Phase 3.6.3)

**Infrastructure Ready:** ✅ All services running
**Integration Tests:** ✅ 8/10 pass (2 pending live data)
**OTEL Package Availability:** ⚠️ Packages not installed in current environment
**Test Execution:** 🔄 Awaiting OTEL package installation OR proceeding to Task 3.3 (performance measurement)

## Next Steps

1. If OTEL packages become available: Run this test plan end-to-end
2. If OTEL unavailable: Proceed to Task 3.3 (verify instrumentation graceful degradation path)
3. Final: POSTFLIGHT with performance measurements (CPU, memory, latency)

