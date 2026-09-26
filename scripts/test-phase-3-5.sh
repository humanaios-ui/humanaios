#!/bin/bash
# Phase 3.5 Integration Testing Script
# Runs comprehensive tests for Jaeger, Loki, and Per-Practice Dashboards

set -e

PASS=0
FAIL=0
WARN=0

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=== Phase 3.5 Integration Testing ==="
echo ""

# Test 1: Jaeger connectivity
echo "Test 1: Jaeger Connectivity"
echo "---"

if curl -f http://localhost:16686/ > /dev/null 2>&1; then
  echo -e "${GREEN}✓${NC} Jaeger UI is accessible"
  ((PASS++))
else
  echo -e "${RED}✗${NC} Jaeger UI is not accessible"
  ((FAIL++))
fi

if curl -s http://localhost:16686/api/services | jq '.data | length' > /dev/null 2>&1; then
  SERVICE_COUNT=$(curl -s http://localhost:16686/api/services | jq '.data | length')
  echo -e "${GREEN}✓${NC} Jaeger API responding (found $SERVICE_COUNT services)"
  ((PASS++))
else
  echo -e "${RED}✗${NC} Jaeger API not responding"
  ((FAIL++))
fi

echo ""

# Test 2: Loki connectivity
echo "Test 2: Loki Connectivity"
echo "---"

if curl -f http://localhost:3100/ready > /dev/null 2>&1; then
  echo -e "${GREEN}✓${NC} Loki is ready"
  ((PASS++))
else
  echo -e "${RED}✗${NC} Loki is not ready"
  ((FAIL++))
fi

if curl -s http://localhost:3100/loki/api/v1/status/buildinfo | jq '.version' > /dev/null 2>&1; then
  VERSION=$(curl -s http://localhost:3100/loki/api/v1/status/buildinfo | jq -r '.version')
  echo -e "${GREEN}✓${NC} Loki version: $VERSION"
  ((PASS++))
else
  echo -e "${RED}✗${NC} Loki API not responding"
  ((FAIL++))
fi

echo ""

# Test 3: Promtail connectivity
echo "Test 3: Promtail Connectivity"
echo "---"

if curl -s http://localhost:9080/metrics | grep -q "promtail" > /dev/null 2>&1; then
  echo -e "${GREEN}✓${NC} Promtail metrics endpoint is accessible"
  ((PASS++))
else
  echo -e "${RED}✗${NC} Promtail metrics endpoint not accessible"
  ((FAIL++))
fi

echo ""

# Test 4: Grafana datasource verification
echo "Test 4: Grafana Datasource Configuration"
echo "---"

# Get Grafana auth token
GRAFANA_TOKEN=$(curl -s -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"user":"admin","password":"admin"}' | jq -r '.token')

if [ -z "$GRAFANA_TOKEN" ] || [ "$GRAFANA_TOKEN" == "null" ]; then
  echo -e "${YELLOW}⚠${NC} Could not authenticate to Grafana (may be running behind auth wall)"
  ((WARN++))
else
  # Check Prometheus datasource
  if curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
    http://localhost:3000/api/datasources/name/Prometheus | jq '.id' > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Prometheus datasource configured in Grafana"
    ((PASS++))
  else
    echo -e "${YELLOW}⚠${NC} Prometheus datasource not found in Grafana"
    ((WARN++))
  fi

  # Check Jaeger datasource
  if curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
    http://localhost:3000/api/datasources/name/Jaeger | jq '.id' > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Jaeger datasource configured in Grafana"
    ((PASS++))
  else
    echo -e "${YELLOW}⚠${NC} Jaeger datasource not found in Grafana"
    ((WARN++))
  fi

  # Check Loki datasource
  if curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
    http://localhost:3000/api/datasources/name/Loki | jq '.id' > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Loki datasource configured in Grafana"
    ((PASS++))
  else
    echo -e "${YELLOW}⚠${NC} Loki datasource not found in Grafana"
    ((WARN++))
  fi
fi

echo ""

# Test 5: Log collection (requires logs in docker)
echo "Test 5: Log Collection & Querying"
echo "---"

# Query Loki for any logs
LOKI_RESULT=$(curl -s -G \
  -d 'query={container!=""}' \
  -d 'limit=5' \
  'http://localhost:3100/loki/api/v1/query_range' | jq '.data.result | length')

if [ "$LOKI_RESULT" -gt 0 ]; then
  echo -e "${GREEN}✓${NC} Loki collecting logs (found $LOKI_RESULT streams)"
  ((PASS++))
else
  echo -e "${YELLOW}⚠${NC} Loki not collecting logs yet (may need to wait for containers to log)"
  ((WARN++))
fi

echo ""

# Test 6: Service health check
echo "Test 6: Docker Service Health Status"
echo "---"

for service in jaeger loki promtail; do
  STATUS=$(docker compose ps $service --format "{{.Status}}")
  if echo "$STATUS" | grep -q "healthy"; then
    echo -e "${GREEN}✓${NC} $service: $STATUS"
    ((PASS++))
  elif echo "$STATUS" | grep -q "Up"; then
    echo -e "${YELLOW}⚠${NC} $service: $STATUS (still starting)"
    ((WARN++))
  else
    echo -e "${RED}✗${NC} $service: $STATUS"
    ((FAIL++))
  fi
done

echo ""
echo "=== Test Summary ==="
echo -e "Passed: ${GREEN}$PASS${NC}"
echo -e "Failed: ${RED}$FAIL${NC}"
echo -e "Warnings: ${YELLOW}$WARN${NC}"
echo ""

if [ $FAIL -gt 0 ]; then
  echo "Some tests failed. Check logs:"
  echo "  docker logs jaeger-empirica-evaluator"
  echo "  docker logs loki-empirica-evaluator"
  echo "  docker logs promtail-empirica-evaluator"
  exit 1
elif [ $WARN -gt 0 ]; then
  echo "Tests passed with warnings. Some features may not be fully operational yet."
  echo "This is normal during initial deployment. Services may still be initializing."
  exit 0
else
  echo "All tests passed! Phase 3.5 is ready."
  exit 0
fi
