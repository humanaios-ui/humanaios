#!/bin/bash
# Deploy Phase 3.5.3 Dashboards to Grafana
#
# Task 2: Framework - Deploy dashboard infrastructure
# Task 3: Per-practice dashboards
#
# Prerequisites:
#   - Grafana running on localhost:3000
#   - Dashboards generated (python3 grafana-dashboard-builder.py)
#   - Loki + Jaeger datasources configured

set -e

GRAFANA_URL="${GRAFANA_URL:-http://localhost:3000}"
GRAFANA_USER="${GRAFANA_USER:-admin}"
GRAFANA_PASSWORD="${GRAFANA_PASSWORD:-admin}"
DASHBOARD_DIR="."

echo "🚀 Phase 3.5.3: Dashboard Deployment"
echo "======================================"
echo ""
echo "Grafana URL: $GRAFANA_URL"
echo "Dashboard dir: $DASHBOARD_DIR"
echo ""

# Step 1: Check Grafana is reachable
echo "📌 Step 1: Check Grafana connectivity"
if ! curl -s "$GRAFANA_URL/api/health" > /dev/null; then
    echo "  ✗ Grafana not reachable at $GRAFANA_URL"
    echo "  Start Grafana: docker-compose -f docker-compose-phase35.yaml up -d grafana"
    exit 1
fi
echo "  ✓ Grafana accessible"
echo ""

# Step 2: Verify datasources
echo "📌 Step 2: Verify Loki + Jaeger datasources"

# Check Loki datasource
if curl -s -u "$GRAFANA_USER:$GRAFANA_PASSWORD" \
    "$GRAFANA_URL/api/datasources" | grep -q "Loki"; then
    echo "  ✓ Loki datasource found"
else
    echo "  ⚠ Loki datasource not configured"
    echo "  Creating Loki datasource..."
    curl -s -u "$GRAFANA_USER:$GRAFANA_PASSWORD" -X POST \
      -H "Content-Type: application/json" \
      -d '{"name":"Loki","type":"loki","url":"http://loki:3100","access":"proxy","isDefault":false}' \
      "$GRAFANA_URL/api/datasources" > /dev/null
    echo "  ✓ Loki datasource created"
fi

# Check Jaeger datasource
if curl -s -u "$GRAFANA_USER:$GRAFANA_PASSWORD" \
    "$GRAFANA_URL/api/datasources" | grep -q "Jaeger"; then
    echo "  ✓ Jaeger datasource found"
else
    echo "  ⚠ Jaeger datasource not configured"
    echo "  Creating Jaeger datasource..."
    curl -s -u "$GRAFANA_USER:$GRAFANA_PASSWORD" -X POST \
      -H "Content-Type: application/json" \
      -d '{"name":"Jaeger","type":"jaeger","url":"http://jaeger:16686","access":"proxy","isDefault":false}' \
      "$GRAFANA_URL/api/datasources" > /dev/null
    echo "  ✓ Jaeger datasource created"
fi
echo ""

# Step 3: Build dashboards (if not already built)
echo "📌 Step 3: Generate dashboard JSON"
if [ ! -f "dashboard-1-phase-latency.json" ]; then
    echo "  Building dashboards..."
    python3 grafana-dashboard-builder.py
else
    echo "  ✓ Dashboards already built"
fi
echo ""

# Step 4: Deploy dashboards
echo "📌 Step 4: Deploy dashboards to Grafana"
DEPLOY_COUNT=0

for dashboard in dashboard-*.json; do
    if [ ! -f "$dashboard" ]; then
        continue
    fi

    DASHBOARD_NAME=$(jq -r '.dashboard.title' "$dashboard")
    echo -n "  Deploying: $DASHBOARD_NAME ... "

    RESPONSE=$(curl -s -X POST \
        -u "$GRAFANA_USER:$GRAFANA_PASSWORD" \
        -H "Content-Type: application/json" \
        -d @"$dashboard" \
        "$GRAFANA_URL/api/dashboards/db")

    if echo "$RESPONSE" | grep -q '"status":"success"'; then
        DASHBOARD_URL=$(echo "$RESPONSE" | jq -r '.url')
        echo "✓ ($GRAFANA_URL$DASHBOARD_URL)"
        ((DEPLOY_COUNT++))
    elif echo "$RESPONSE" | grep -q '"status":"ok"'; then
        DASHBOARD_URL=$(echo "$RESPONSE" | jq -r '.url')
        echo "✓ (updated)"
        ((DEPLOY_COUNT++))
    else
        echo "✗ Failed"
        echo "  Response: $(echo $RESPONSE | jq -r '.message // .error // .')"
    fi
done
echo ""

# Step 5: Create per-practice dashboard variants
echo "📌 Step 5: Create per-practice deep-dive dashboards"
for practice in mesh-support outreach website humanaios; do
    DASHBOARD_FILE="dashboard-5-practice-$practice.json"

    if [ ! -f "$DASHBOARD_FILE" ]; then
        echo "  Creating: $practice variant"

        # Copy autonomy template and replace practice name
        jq ".dashboard.title |= \"Practice Deep-Dive: $(echo $practice | sed 's/-/ /g' | sed 's/\b\(.\)/\U\1/g')\" | \
            .dashboard.panels[].targets[].expr |= gsub(\"autonomy\"; \"$practice\")" \
            dashboard-5-practice-autonomy.json > "$DASHBOARD_FILE"

        # Deploy it
        RESPONSE=$(curl -s -X POST \
            -u "$GRAFANA_USER:$GRAFANA_PASSWORD" \
            -H "Content-Type: application/json" \
            -d @"$DASHBOARD_FILE" \
            "$GRAFANA_URL/api/dashboards/db")

        if echo "$RESPONSE" | grep -q '"status"'; then
            echo "  ✓ $practice dashboard deployed"
            ((DEPLOY_COUNT++))
        fi
    fi
done
echo ""

# Step 6: Create dashboard index
echo "📌 Step 6: Create dashboard index"

DASHBOARDS_INDEX=$(curl -s -u "$GRAFANA_USER:$GRAFANA_PASSWORD" \
    "$GRAFANA_URL/api/search?tag=phase-3.5" | \
    jq -r '.[] | "\(.title) (\(.url))"' 2>/dev/null || echo "")

echo "  Dashboards created:"
while IFS= read -r line; do
    [ -z "$line" ] && continue
    echo "    • $line"
done <<< "$DASHBOARDS_INDEX"
echo ""

# Step 7: Verify dashboards
echo "📌 Step 7: Verify dashboard integrity"
VERIFIED=0

for dashboard in dashboard-*.json; do
    if [ ! -f "$dashboard" ]; then
        continue
    fi

    # Check that each dashboard has panels
    PANEL_COUNT=$(jq '.dashboard.panels | length' "$dashboard")
    if [ "$PANEL_COUNT" -gt 0 ]; then
        echo "  ✓ $(jq -r '.dashboard.title' "$dashboard") ($PANEL_COUNT panels)"
        ((VERIFIED++))
    fi
done
echo ""

# Summary
echo "════════════════════════════════════════"
echo "✅ Dashboard Deployment Complete"
echo "════════════════════════════════════════"
echo ""
echo "📊 Dashboards deployed: $DEPLOY_COUNT"
echo "📊 Dashboards verified: $VERIFIED"
echo ""
echo "Access dashboards at:"
echo "  $GRAFANA_URL/dashboards?tag=phase-3.5"
echo ""
echo "Navigation:"
for dashboard in dashboard-*.json; do
    if [ -f "$dashboard" ]; then
        TITLE=$(jq -r '.dashboard.title' "$dashboard")
        echo "  • $TITLE"
    fi
done
echo ""
echo "Next steps:"
echo "  1. Open Grafana: $GRAFANA_URL"
echo "  2. Navigate to: Dashboards → phase-3.5 tag"
echo "  3. Verify data is flowing (check time range: last 7 days)"
echo "  4. Customize as needed"
echo ""
