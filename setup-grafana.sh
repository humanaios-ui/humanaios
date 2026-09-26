#!/bin/bash
# Setup Grafana datasources and create API key for Phase 3.5.5

set -e

GRAFANA_URL="${GRAFANA_URL:-http://localhost:3000}"
GRAFANA_USER="admin"
GRAFANA_PASSWORD="admin"

echo "🔧 Phase 3.5.5: Grafana Setup"
echo "======================================"
echo ""

# Step 1: Create API key
echo "📌 Step 1: Create API key"
API_KEY_RESPONSE=$(curl -s -X POST \
  -u "$GRAFANA_USER:$GRAFANA_PASSWORD" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "phase-35-automation",
    "role": "Admin",
    "lifetime": 8760
  }' \
  "$GRAFANA_URL/api/auth/keys")

API_KEY=$(echo "$API_KEY_RESPONSE" | jq -r '.key // empty')

if [ -z "$API_KEY" ]; then
  echo "  ✗ Failed to create API key"
  echo "  Response: $API_KEY_RESPONSE"
  exit 1
fi

echo "  ✓ API key created: $API_KEY"
echo ""

# Step 2: Create Loki datasource
echo "📌 Step 2: Create Loki datasource"
LOKI_RESPONSE=$(curl -s -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Loki",
    "type": "loki",
    "url": "http://loki:3100",
    "access": "proxy",
    "isDefault": false
  }' \
  "$GRAFANA_URL/api/datasources")

if echo "$LOKI_RESPONSE" | jq -e '.id' > /dev/null 2>&1; then
  LOKI_ID=$(echo "$LOKI_RESPONSE" | jq -r '.id')
  echo "  ✓ Loki datasource created (ID: $LOKI_ID)"
else
  echo "  ⚠ Loki datasource: $(echo "$LOKI_RESPONSE" | jq -r '.message // .error // .')"
fi
echo ""

# Step 3: Create Jaeger datasource
echo "📌 Step 3: Create Jaeger datasource"
JAEGER_RESPONSE=$(curl -s -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jaeger",
    "type": "jaeger",
    "url": "http://jaeger:16686",
    "access": "proxy",
    "isDefault": false
  }' \
  "$GRAFANA_URL/api/datasources")

if echo "$JAEGER_RESPONSE" | jq -e '.id' > /dev/null 2>&1; then
  JAEGER_ID=$(echo "$JAEGER_RESPONSE" | jq -r '.id')
  echo "  ✓ Jaeger datasource created (ID: $JAEGER_ID)"
else
  echo "  ⚠ Jaeger datasource: $(echo "$JAEGER_RESPONSE" | jq -r '.message // .error // .')"
fi
echo ""

# Step 4: Deploy dashboards with API key
echo "📌 Step 4: Deploy dashboards"
DEPLOY_COUNT=0

for dashboard in dashboard-*.json; do
  if [ ! -f "$dashboard" ]; then
    continue
  fi

  DASHBOARD_NAME=$(jq -r '.dashboard.title' "$dashboard")
  echo -n "  Deploying: $DASHBOARD_NAME ... "

  RESPONSE=$(curl -s -X POST \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d @"$dashboard" \
    "$GRAFANA_URL/api/dashboards/db")

  if echo "$RESPONSE" | grep -q '"status":"success"'; then
    DASHBOARD_URL=$(echo "$RESPONSE" | jq -r '.url')
    echo "✓"
    ((DEPLOY_COUNT++))
  elif echo "$RESPONSE" | grep -q '"status":"ok"'; then
    echo "✓ (updated)"
    ((DEPLOY_COUNT++))
  else
    echo "✗"
    echo "    Error: $(echo "$RESPONSE" | jq -r '.message // .error // .')"
  fi
done
echo ""

# Summary
echo "════════════════════════════════════════"
echo "✅ Grafana Setup Complete"
echo "════════════════════════════════════════"
echo ""
echo "API Key: $API_KEY"
echo "Dashboards deployed: $DEPLOY_COUNT"
echo ""
echo "Access Grafana at:"
echo "  $GRAFANA_URL"
echo ""
echo "Use API key in deploy-dashboards.sh:"
echo "  export GRAFANA_TOKEN=\"$API_KEY\""
echo ""
