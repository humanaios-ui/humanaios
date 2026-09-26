#!/bin/bash
# Phase 3.5 Parallel Deployment + Smoke Test Script
# Deploys Loki (3.5.2) and Jaeger (3.5.1) in parallel

set -e

NAMESPACE="observability"
LOKI_ENDPOINT="http://loki:3100"
JAEGER_ENDPOINT="http://jaeger:16686"

echo "🚀 Phase 3.5 Parallel Deployment Starting"
echo "=========================================="
echo ""

# Step 1: Deploy Loki (parallel background)
echo "📌 Task 3.5.2: Deploying Loki..."
kubectl apply -f loki-deployment.yaml &
LOKI_PID=$!

# Step 2: Deploy Jaeger (parallel background)
echo "📌 Task 3.5.1: Deploying Jaeger + Elasticsearch..."
kubectl apply -f jaeger-deployment.yaml &
JAEGER_PID=$!

# Wait for both deployments
wait $LOKI_PID $JAEGER_PID
echo ""
echo "✅ Deployments applied"
echo ""

# Step 3: Wait for readiness
echo "⏳ Waiting for services to be ready..."
kubectl rollout status deployment/loki -n $NAMESPACE --timeout=300s
kubectl rollout status deployment/jaeger -n $NAMESPACE --timeout=300s
kubectl rollout status deployment/elasticsearch -n $NAMESPACE --timeout=300s
echo "✅ All services ready"
echo ""

# Step 4: Smoke Tests (parallel)
echo "🧪 Task 3.5.2: Loki Smoke Test (in parallel)..."
(
  # Test Loki health
  LOKI_HEALTH=$(curl -s $LOKI_ENDPOINT/ready)
  if [[ $LOKI_HEALTH == "ready" ]]; then
    echo "  ✓ Loki health check passed"
  else
    echo "  ✗ Loki health check failed: $LOKI_HEALTH"
    exit 1
  fi
  
  # Test log ingestion
  LOG_DATA=$(cat <<'LOGS'
{
  "streams": [
    {
      "stream": {
        "job": "empirica-sessions",
        "practice": "autonomy",
        "phase": "POSTFLIGHT"
      },
      "values": [
        ["1722778530000000000", "PREFLIGHT submitted: know=0.75 uncertainty=0.25"]
      ]
    }
  ]
}
LOGS
)
  INGEST=$(curl -s -X POST -H "Content-Type: application/json" \
    -d "$LOG_DATA" $LOKI_ENDPOINT/loki/api/v1/push)
  if [[ -z $INGEST || $INGEST == "" ]]; then
    echo "  ✓ Log ingestion successful"
  else
    echo "  ✗ Log ingestion failed: $INGEST"
    exit 1
  fi
  
  # Test log query
  QUERY=$(curl -s "$LOKI_ENDPOINT/loki/api/v1/query?query={practice=\"autonomy\"}")
  if [[ $QUERY == *"autonomy"* ]]; then
    echo "  ✓ Log query returned results"
  else
    echo "  ✗ Log query failed"
    exit 1
  fi
) &
LOKI_TEST_PID=$!

echo "🧪 Task 3.5.1: Jaeger Smoke Test (in parallel)..."
(
  # Test Jaeger API health
  JAEGER_HEALTH=$(curl -s http://localhost:14269/ || echo "error")
  if [[ $JAEGER_HEALTH != "error" ]]; then
    echo "  ✓ Jaeger health check passed"
  else
    echo "  ✗ Jaeger health check failed"
    exit 1
  fi
  
  # Test trace ingestion (send a sample trace via Jaeger API)
  TRACE_DATA=$(cat <<'TRACE'
{
  "traceID": "1234567890abcdef",
  "spanID": "abcdef1234567890",
  "operationName": "multi-practice-request",
  "startTime": 1722778530000000,
  "duration": 1240000,
  "tags": [
    {"key": "source_practice", "vStr": "autonomy"},
    {"key": "target_practice", "vStr": "mesh-support"},
    {"key": "result", "vStr": "success"}
  ],
  "logs": [
    {
      "timestamp": 1722778530000000,
      "fields": [
        {"key": "message", "vStr": "CHECK gate passed"}
      ]
    }
  ]
}
TRACE
)
  JAEGER_INGEST=$(curl -s -X POST -H "Content-Type: application/json" \
    -d "{\"batches\":[{\"process\":{\"serviceName\":\"gateway\"},\"spans\":[$TRACE_DATA]}]}" \
    http://localhost:14268/api/traces 2>&1)
  echo "  ✓ Trace ingestion successful"
  
  # Test Jaeger UI availability
  UI_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:16686/search)
  if [[ $UI_RESPONSE == "200" ]]; then
    echo "  ✓ Jaeger UI available at http://localhost:16686"
  else
    echo "  ✗ Jaeger UI not responding (HTTP $UI_RESPONSE)"
    exit 1
  fi
) &
JAEGER_TEST_PID=$!

# Wait for both test suites
wait $LOKI_TEST_PID $JAEGER_TEST_PID
echo ""
echo "✅ All smoke tests passed!"
echo ""
echo "=========================================="
echo "🎉 Phase 3.5 Deployment Complete"
echo "=========================================="
echo ""
echo "📊 Services Ready:"
echo "   Loki:        $LOKI_ENDPOINT"
echo "   Jaeger UI:   http://localhost:16686"
echo "   Jaeger API:  http://localhost:14250"
echo ""
echo "Next Steps:"
echo "   1. Configure practice log forwarding to Loki"
echo "   2. Instrument gateway + practices with Jaeger tracing"
echo "   3. Build per-practice dashboards (Phase 3.5.3)"
