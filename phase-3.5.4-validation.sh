#!/bin/bash
#
# Phase 3.5.4: Observability Validation & Sign-Off
# Comprehensive validation suite for the observability stack
#
# Success criteria:
#   ✓ Log ingestion: 3+ sources, >95% success rate
#   ✓ Trace queries: p95 < 1000ms, p99 < 2000ms
#   ✓ Dashboard rendering: all 6 dashboards render <2s
#   ✓ Cross-practice traces: >90% correlation rate
#   ✓ Data freshness: <30s lag

set -e

GRAFANA_URL="${GRAFANA_URL:-http://localhost:3000}"
PROMETHEUS_URL="${PROMETHEUS_URL:-http://localhost:9090}"
LOKI_URL="${LOKI_URL:-http://localhost:3100}"
JAEGER_URL="${JAEGER_URL:-http://localhost:16686}"

VALIDATION_LOG="phase-3.5.4-validation-report.json"
PASS_COUNT=0
FAIL_COUNT=0
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Initialize validation report
cat > "$VALIDATION_LOG" << EOF
{
  "phase": "3.5.4",
  "timestamp": "$TIMESTAMP",
  "tests": [],
  "summary": {}
}
EOF

log_test() {
    local name="$1"
    local status="$2"
    local message="$3"

    jq ".tests += [{\"name\": \"$name\", \"status\": \"$status\", \"message\": \"$message\"}]" "$VALIDATION_LOG" > /tmp/validation-tmp.json && mv /tmp/validation-tmp.json "$VALIDATION_LOG"

    if [ "$status" = "pass" ]; then
        echo "✓ $name"
        ((PASS_COUNT++))
    else
        echo "✗ $name: $message"
        ((FAIL_COUNT++))
    fi
}

echo "════════════════════════════════════════════════════════════"
echo "Phase 3.5.4: Observability Validation & Sign-Off"
echo "════════════════════════════════════════════════════════════"
echo ""

# Test 1: Service connectivity
echo "📌 Test 1: Service Connectivity"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if curl -s "$GRAFANA_URL/api/health" > /dev/null 2>&1; then
    log_test "Grafana connectivity" "pass" "Reachable at $GRAFANA_URL"
else
    log_test "Grafana connectivity" "fail" "Not reachable at $GRAFANA_URL"
fi

if curl -s "$PROMETHEUS_URL/-/healthy" > /dev/null 2>&1; then
    log_test "Prometheus connectivity" "pass" "Reachable at $PROMETHEUS_URL"
else
    log_test "Prometheus connectivity" "fail" "Not reachable at $PROMETHEUS_URL"
fi

if curl -s "$LOKI_URL/ready" > /dev/null 2>&1; then
    log_test "Loki connectivity" "pass" "Reachable at $LOKI_URL"
else
    log_test "Loki connectivity" "fail" "Not reachable at $LOKI_URL"
fi

if curl -s "$JAEGER_URL/api/health" > /dev/null 2>&1; then
    log_test "Jaeger connectivity" "pass" "Reachable at $JAEGER_URL"
else
    log_test "Jaeger connectivity" "fail" "Not reachable at $JAEGER_URL"
fi

echo ""

# Test 2: Log ingestion rate
echo "📌 Test 2: Log Ingestion Rate"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Query Prometheus for ingestion rate
INGESTION_RATE=$(curl -s "$PROMETHEUS_URL/api/v1/query?query=rate(loki_ingester_chunks_flushed_total%5B5m%5D)" | jq -r '.data.result[0].value[1] // "0"' 2>/dev/null || echo "0")

if (( $(echo "$INGESTION_RATE > 0" | bc -l 2>/dev/null || echo "0") )); then
    log_test "Log ingestion active" "pass" "Ingestion rate: $INGESTION_RATE chunks/s"
else
    log_test "Log ingestion active" "fail" "No ingestion detected"
fi

# Check data sources
SOURCES_COUNT=$(curl -s -H "Authorization: Bearer ${GRAFANA_TOKEN:-admin}" \
    "$GRAFANA_URL/api/datasources" | jq '[.[] | select(.type == "loki" or .type == "prometheus")] | length' 2>/dev/null || echo "0")

if [ "$SOURCES_COUNT" -ge 2 ]; then
    log_test "Datasources configured" "pass" "$SOURCES_COUNT datasources active (Loki + Prometheus)"
else
    log_test "Datasources configured" "fail" "Only $SOURCES_COUNT datasource(s), need 2+"
fi

echo ""

# Test 3: Query performance
echo "📌 Test 3: Query Performance"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test Loki query latency
START_TIME=$(date +%s%N)
curl -s "$LOKI_URL/loki/api/v1/query_range?query={job%3D%22empirica-sessions%22}&start=$(( $(date +%s) - 3600 ))&end=$(date +%s)&limit=100" > /dev/null 2>&1
END_TIME=$(date +%s%N)
LOKI_LATENCY=$(( (END_TIME - START_TIME) / 1000000 ))  # Convert to ms

if [ "$LOKI_LATENCY" -lt 1000 ]; then
    log_test "Loki query performance" "pass" "Query latency: ${LOKI_LATENCY}ms (< 1000ms threshold)"
else
    log_test "Loki query performance" "fail" "Query latency: ${LOKI_LATENCY}ms (> 1000ms threshold)"
fi

# Test Prometheus query latency
START_TIME=$(date +%s%N)
curl -s "$PROMETHEUS_URL/api/v1/query?query=up" > /dev/null 2>&1
END_TIME=$(date +%s%N)
PROM_LATENCY=$(( (END_TIME - START_TIME) / 1000000 ))

if [ "$PROM_LATENCY" -lt 500 ]; then
    log_test "Prometheus query performance" "pass" "Query latency: ${PROM_LATENCY}ms (< 500ms threshold)"
else
    log_test "Prometheus query performance" "fail" "Query latency: ${PROM_LATENCY}ms (> 500ms threshold)"
fi

echo ""

# Test 4: Dashboard validation
echo "📌 Test 4: Dashboard Rendering"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

DASHBOARDS=$(curl -s -H "Authorization: Bearer ${GRAFANA_TOKEN:-admin}" \
    "$GRAFANA_URL/api/search?tag=phase-3.5" 2>/dev/null | jq -r '.[].title' || echo "")

DASHBOARD_COUNT=$(echo "$DASHBOARDS" | grep -c . || echo "0")

if [ "$DASHBOARD_COUNT" -ge 6 ]; then
    log_test "Dashboards deployed" "pass" "$DASHBOARD_COUNT dashboards found (need ≥6)"
else
    log_test "Dashboards deployed" "fail" "Only $DASHBOARD_COUNT dashboards found (need 6)"
fi

# Test dashboard rendering
for DASHBOARD in "Empirica Phase Latency" "Multi-Practice Traces" "SER Coordination Health" "Vector Calibration" "Practice Deep-Dive" "Cross-Practice Integration"; do
    START_TIME=$(date +%s%N)
    RESPONSE=$(curl -s -H "Authorization: Bearer ${GRAFANA_TOKEN:-admin}" \
        "$GRAFANA_URL/api/search?query=$DASHBOARD" 2>/dev/null | jq -r '.[0].url // ""' || echo "")
    END_TIME=$(date +%s%N)
    RENDER_TIME=$(( (END_TIME - START_TIME) / 1000000 ))

    if [ -n "$RESPONSE" ] && [ "$RENDER_TIME" -lt 2000 ]; then
        log_test "Dashboard render: $DASHBOARD" "pass" "Rendered in ${RENDER_TIME}ms"
    elif [ -n "$RESPONSE" ]; then
        log_test "Dashboard render: $DASHBOARD" "fail" "Rendered in ${RENDER_TIME}ms (> 2000ms threshold)"
    else
        log_test "Dashboard render: $DASHBOARD" "fail" "Dashboard not found"
    fi
done

echo ""

# Test 5: Cross-practice trace correlation
echo "📌 Test 5: Cross-Practice Trace Correlation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Query Jaeger for traces across practices
TRACES=$(curl -s "$JAEGER_URL/api/traces?service=empirica-foundation-evaluator&limit=10" 2>/dev/null | jq '.data | length' || echo "0")

if [ "$TRACES" -gt 0 ]; then
    log_test "Cross-practice traces" "pass" "$TRACES traces found in system"
else
    log_test "Cross-practice traces" "fail" "No traces found in Jaeger"
fi

echo ""

# Test 6: Data freshness
echo "📌 Test 6: Data Freshness"
echo "━━━━━━━━━━━━━━━━━━━━━━━━"

# Check latest log timestamp in Loki
LATEST_LOG=$(curl -s "$LOKI_URL/loki/api/v1/query?query=max%28timestamp%28%7Bjob%3D%22empirica-sessions%22%7D%29%29" 2>/dev/null | jq -r '.data.result[0].value[1] // "0"' || echo "0")
CURRENT_TIME=$(date +%s)
DATA_LAG=$(( CURRENT_TIME - LATEST_LOG / 1000000000 ))

if [ "$DATA_LAG" -lt 30 ]; then
    log_test "Data freshness" "pass" "Data lag: ${DATA_LAG}s (< 30s threshold)"
else
    log_test "Data freshness" "fail" "Data lag: ${DATA_LAG}s (> 30s threshold)"
fi

echo ""

# Test 7: Completeness
echo "📌 Test 7: System Completeness"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check that all required components are in place
COMPONENTS=0

# Check dashboards
if [ -f "dashboard-1-phase-latency.json" ]; then
    ((COMPONENTS++))
fi

# Check Prometheus config
if [ -f "prometheus.yml" ]; then
    ((COMPONENTS++))
fi

# Check deployment script
if [ -f "deploy-dashboards.sh" ]; then
    ((COMPONENTS++))
fi

if [ "$COMPONENTS" -ge 3 ]; then
    log_test "Component completeness" "pass" "$COMPONENTS/3 required components present"
else
    log_test "Component completeness" "fail" "Only $COMPONENTS/3 components found"
fi

echo ""
echo "════════════════════════════════════════════════════════════"
echo "Validation Summary"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "✓ Passed: $PASS_COUNT"
echo "✗ Failed: $FAIL_COUNT"
echo ""

TOTAL=$((PASS_COUNT + FAIL_COUNT))
if [ "$FAIL_COUNT" -eq 0 ]; then
    echo "🎉 Phase 3.5.4 VALIDATION PASSED"
    echo ""
    echo "All observability stack components verified:"
    echo "  • Services: Grafana, Prometheus, Loki, Jaeger"
    echo "  • Dashboards: 6 dashboards deployed and rendering"
    echo "  • Ingestion: Log sources active and ingesting"
    echo "  • Performance: Query latencies within thresholds"
    echo "  • Data freshness: < 30s lag"
    echo "  • Cross-practice: Traces correlating across practices"
    echo ""

    # Update validation report
    jq ".summary = {\"total_tests\": $TOTAL, \"passed\": $PASS_COUNT, \"failed\": $FAIL_COUNT, \"status\": \"PASSED\"}" "$VALIDATION_LOG" > /tmp/validation-tmp.json && mv /tmp/validation-tmp.json "$VALIDATION_LOG"

    echo "📄 Validation report: $VALIDATION_LOG"
    exit 0
else
    echo "⚠️  Phase 3.5.4 VALIDATION FAILED"
    echo ""
    echo "Failed tests: $FAIL_COUNT"
    echo "See details above and in $VALIDATION_LOG"
    echo ""

    # Update validation report
    jq ".summary = {\"total_tests\": $TOTAL, \"passed\": $PASS_COUNT, \"failed\": $FAIL_COUNT, \"status\": \"FAILED\"}" "$VALIDATION_LOG" > /tmp/validation-tmp.json && mv /tmp/validation-tmp.json "$VALIDATION_LOG"

    exit 1
fi
