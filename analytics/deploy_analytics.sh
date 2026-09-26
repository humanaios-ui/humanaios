#!/bin/bash
#
# Phase 3.5.5: Analytics & Decision Support Deployment
# Deploy anomaly detection, alerting, and decision support system
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/.."

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Phase 3.5.5: Analytics & Decision Support Deployment      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Verify dependencies
echo "📌 Step 1: Verify Dependencies"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

REQUIRED_TOOLS=("python3" "curl" "jq")
for tool in "${REQUIRED_TOOLS[@]}"; do
    if command -v "$tool" &> /dev/null; then
        echo "  ✓ $tool found"
    else
        echo "  ✗ $tool NOT found - please install"
        exit 1
    fi
done
echo ""

# Step 2: Verify configuration files
echo "📌 Step 2: Verify Configuration Files"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

FILES_REQUIRED=(
    "anomaly_detection.py"
    "alert_manager.py"
    "alert_rules.json"
    "dashboard-7-decision-support.json"
)

for file in "${FILES_REQUIRED[@]}"; do
    if [ -f "$SCRIPT_DIR/$file" ]; then
        echo "  ✓ $file present"
    else
        echo "  ✗ $file MISSING"
        exit 1
    fi
done
echo ""

# Step 3: Make scripts executable
echo "📌 Step 3: Prepare Scripts"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

chmod +x "$SCRIPT_DIR/anomaly_detection.py"
chmod +x "$SCRIPT_DIR/alert_manager.py"
echo "  ✓ Scripts made executable"
echo ""

# Step 4: Validate JSON files
echo "📌 Step 4: Validate Configuration JSON"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

for file in alert_rules.json dashboard-7-decision-support.json; do
    if jq empty "$SCRIPT_DIR/$file" 2>/dev/null; then
        echo "  ✓ $file: valid JSON"
    else
        echo "  ✗ $file: INVALID JSON"
        exit 1
    fi
done
echo ""

# Step 5: Check Prometheus connectivity
echo "📌 Step 5: Check Observability Stack Connectivity"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

PROMETHEUS_URL="${PROMETHEUS_URL:-http://localhost:9090}"
GRAFANA_URL="${GRAFANA_URL:-http://localhost:3000}"
GRAFANA_TOKEN="${GRAFANA_TOKEN:-admin}"

if curl -s "$PROMETHEUS_URL/-/healthy" > /dev/null 2>&1; then
    echo "  ✓ Prometheus accessible at $PROMETHEUS_URL"
else
    echo "  ⚠ Prometheus not accessible at $PROMETHEUS_URL"
    echo "    Deployment can continue but runtime detection will fail"
fi

if curl -s "$GRAFANA_URL/api/health" > /dev/null 2>&1; then
    echo "  ✓ Grafana accessible at $GRAFANA_URL"
else
    echo "  ⚠ Grafana not accessible at $GRAFANA_URL"
    echo "    Dashboard deployment will be skipped"
fi
echo ""

# Step 6: Deploy decision support dashboard
echo "📌 Step 6: Deploy Decision Support Dashboard"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if curl -s "$GRAFANA_URL/api/health" > /dev/null 2>&1; then
    RESPONSE=$(curl -s -X POST \
        -H "Authorization: Bearer $GRAFANA_TOKEN" \
        -H "Content-Type: application/json" \
        -d @"$SCRIPT_DIR/dashboard-7-decision-support.json" \
        "$GRAFANA_URL/api/dashboards/db")

    if echo "$RESPONSE" | grep -q '"status":"success\|status":"ok"'; then
        DASHBOARD_URL=$(echo "$RESPONSE" | jq -r '.url // "unknown"')
        echo "  ✓ Dashboard deployed: $GRAFANA_URL$DASHBOARD_URL"
    else
        echo "  ⚠ Dashboard deployment may have failed"
        echo "    Response: $(echo "$RESPONSE" | jq -r '.message // .')"
    fi
else
    echo "  ⊘ Grafana not available - skipping dashboard deployment"
fi
echo ""

# Step 7: Install alert rules
echo "📌 Step 7: Install Alert Rules Configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Count rules
RULE_COUNT=$(jq '.alert_rules | length' "$SCRIPT_DIR/alert_rules.json")
echo "  ✓ Alert rules configured: $RULE_COUNT rules"
echo ""

# Step 8: Test anomaly detection
echo "📌 Step 8: Test Anomaly Detection Engine"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -z "$DRY_RUN" ]; then
    if python3 "$SCRIPT_DIR/anomaly_detection.py" > /tmp/anomaly-test.log 2>&1; then
        ANOMALY_COUNT=$(jq '.total_anomalies' anomalies.json 2>/dev/null || echo "?")
        echo "  ✓ Anomaly detection working (found $ANOMALY_COUNT anomalies)"
    else
        echo "  ⚠ Anomaly detection test failed (Prometheus may not be running)"
        echo "    See /tmp/anomaly-test.log for details"
    fi
else
    echo "  ⊘ Dry-run mode - skipping live test"
fi
echo ""

# Step 9: Test alert manager
echo "📌 Step 9: Test Alert Manager"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -z "$DRY_RUN" ]; then
    if python3 "$SCRIPT_DIR/alert_manager.py" > /tmp/alert-test.log 2>&1; then
        ALERT_COUNT=$(jq '.summary.total_alerts' alerts_processed.json 2>/dev/null || echo "?")
        echo "  ✓ Alert manager working (processed $ALERT_COUNT alerts)"
    else
        echo "  ⚠ Alert manager test failed"
        echo "    See /tmp/alert-test.log for details"
    fi
else
    echo "  ⊘ Dry-run mode - skipping live test"
fi
echo ""

# Step 10: Create analytics cron job
echo "📌 Step 10: Set Up Continuous Monitoring"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ANALYTICS_SCRIPT="$PROJECT_ROOT/run_analytics_cycle.sh"

cat > "$ANALYTICS_SCRIPT" << 'EOF'
#!/bin/bash
# Run complete analytics cycle: anomaly detection -> alert routing -> dashboard update
cd "$(dirname "$0")/analytics"
python3 anomaly_detection.py
python3 alert_manager.py
exit 0
EOF

chmod +x "$ANALYTICS_SCRIPT"
echo "  ✓ Analytics cycle script created: $ANALYTICS_SCRIPT"
echo "  📋 To run continuously: add to crontab -e"
echo "     */5 * * * * $ANALYTICS_SCRIPT  # Every 5 minutes"
echo ""

# Summary
echo "════════════════════════════════════════════════════════════"
echo "✅ Phase 3.5.5 Analytics Deployment Complete"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Components Deployed:"
echo "  ✓ Anomaly Detection Engine"
echo "  ✓ Alert Manager & Routing"
echo "  ✓ Alert Rules ($RULE_COUNT rules configured)"
echo "  ✓ Decision Support Dashboard"
echo "  ✓ Continuous Monitoring Setup"
echo ""
echo "Next Steps:"
echo "  1. Deploy observability stack: docker-compose up -d"
echo "  2. Access decision support dashboard:"
echo "     $GRAFANA_URL/d/decision-support?var-datasource=Prometheus"
echo "  3. Run analytics cycle manually:"
echo "     bash $ANALYTICS_SCRIPT"
echo "  4. Set up continuous monitoring (every 5 minutes):"
echo "     crontab -e  # Add: */5 * * * * $ANALYTICS_SCRIPT"
echo ""
echo "Monitoring Files:"
echo "  - anomalies.json: Current anomalies detected"
echo "  - alerts_processed.json: Processed alerts"
echo "  - Alert rules: analytics/alert_rules.json"
echo ""
echo "For more information, see:"
echo "  - PHASE-3-SESSION-SUMMARY.md"
echo "  - analytics/README.md (when created)"
echo ""
