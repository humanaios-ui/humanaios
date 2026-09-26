#!/bin/bash
# Phase 3.5 Deployment Script
# Deploys Jaeger, Loki, and Promtail services

set -e

cd "$(dirname "$0")/../agent"

echo "=== Phase 3.5 Observability Enhancements Deployment ==="
echo ""

# Step 1: Verify Phase 3.4 is running
echo "Step 1: Verifying Phase 3.4 prerequisite services..."
if ! docker compose ps prometheus | grep -q "Up"; then
  echo "ERROR: Prometheus not running. Please start Phase 3.4 first:"
  echo "  docker compose up -d prometheus grafana alertmanager otel-collector"
  exit 1
fi
echo "✓ Phase 3.4 services verified"
echo ""

# Step 2: Start Phase 3.5 services
echo "Step 2: Starting Phase 3.5 services..."
docker compose up -d jaeger loki promtail
echo "✓ Services started"
echo ""

# Step 3: Wait for services to be healthy
echo "Step 3: Waiting for services to be healthy..."
MAX_WAIT=60
ELAPSED=0

while [ $ELAPSED -lt $MAX_WAIT ]; do
  HEALTHY=0

  # Check Jaeger
  if curl -f http://localhost:16686/ > /dev/null 2>&1; then
    echo "✓ Jaeger UI is ready"
    ((HEALTHY++))
  fi

  # Check Loki
  if curl -f http://localhost:3100/ready > /dev/null 2>&1; then
    echo "✓ Loki is ready"
    ((HEALTHY++))
  fi

  # Check Promtail
  if curl -f http://localhost:9080/metrics > /dev/null 2>&1; then
    echo "✓ Promtail is ready"
    ((HEALTHY++))
  fi

  if [ $HEALTHY -eq 3 ]; then
    echo ""
    echo "✓ All Phase 3.5 services are healthy"
    break
  fi

  ELAPSED=$((ELAPSED + 5))
  if [ $ELAPSED -lt $MAX_WAIT ]; then
    sleep 5
  fi
done

if [ $HEALTHY -ne 3 ]; then
  echo ""
  echo "WARNING: Not all services are healthy yet. Checking logs..."
  echo ""

  if ! curl -f http://localhost:16686/ > /dev/null 2>&1; then
    echo "Jaeger logs:"
    docker logs jaeger-empirica-evaluator | tail -20
    echo ""
  fi

  if ! curl -f http://localhost:3100/ready > /dev/null 2>&1; then
    echo "Loki logs:"
    docker logs loki-empirica-evaluator | tail -20
    echo ""
  fi

  if ! curl -f http://localhost:9080/metrics > /dev/null 2>&1; then
    echo "Promtail logs:"
    docker logs promtail-empirica-evaluator | tail -20
    echo ""
  fi

  exit 1
fi

# Step 4: Display service endpoints
echo "=== Phase 3.5 Services Deployed ==="
echo ""
echo "Service Endpoints:"
echo "  Jaeger UI:        http://localhost:16686"
echo "  Loki API:         http://localhost:3100"
echo "  Promtail Metrics: http://localhost:9080/metrics"
echo "  Grafana:          http://localhost:3000/explore"
echo ""
echo "Next Steps:"
echo "  1. Run integration tests: ./scripts/test-phase-3-5.sh"
echo "  2. Verify in Grafana by submitting a test request"
echo "  3. Check docs/PHASE_3_5_DEPLOYMENT_GUIDE.md for detailed testing"
