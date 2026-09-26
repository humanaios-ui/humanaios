#!/bin/bash
#
# Autonomous Agent Fleet Deployment
# Deploy autonomous agents to all 15 practices in the foundation
#
# Usage: ./deploy_agents.sh [--test-only] [--practice <name>]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/.."
LOG_DIR="/tmp/autonomous-agents"
RESULTS_FILE="$PROJECT_ROOT/deployment-results.json"

# Practices to deploy (foundation + cross-org)
PRACTICES=(
    "empirica-autonomy"
    "empirica-mesh-support"
    "empirica-outreach"
    "humanaios"
    "website"
    # Cross-org (6 additional)
    "empirica-cortex"
    "empirica-mesh-support"
    "empirica-extension"
    "empirica-documentation"
    "empirica-teaching"
    "empirica-research"
)

TEST_ONLY=false
SINGLE_PRACTICE=""
POLL_INTERVAL=30

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --test-only)
            TEST_ONLY=true
            shift
            ;;
        --practice)
            SINGLE_PRACTICE="$2"
            shift 2
            ;;
        --poll-interval)
            POLL_INTERVAL="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

mkdir -p "$LOG_DIR"

echo "╔════════════════════════════════════════════════════════╗"
echo "║  Autonomous Agent Fleet Deployment                     ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "Configuration:"
echo "  Poll interval: ${POLL_INTERVAL}s"
echo "  Test only: $TEST_ONLY"
echo "  Log directory: $LOG_DIR"
echo ""

# Initialize results JSON
cat > "$RESULTS_FILE" << EOF
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "deployment_type": "full_fleet",
  "test_only": $TEST_ONLY,
  "practices": [],
  "summary": {}
}
EOF

DEPLOYED=0
FAILED=0
TESTED=0

test_practice() {
    local practice="$1"
    local ai_id="empirica-foundation.carly.$practice"

    echo ""
    echo "📌 Testing: $practice"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Run test suite
    if python3 "$SCRIPT_DIR/test_autonomous_agent.py" "$ai_id" "$POLL_INTERVAL" > /tmp/test-$practice.log 2>&1; then
        echo "✅ Tests passed for $practice"
        ((TESTED++))
        return 0
    else
        echo "❌ Tests failed for $practice (see /tmp/test-$practice.log)"
        return 1
    fi
}

deploy_practice() {
    local practice="$1"
    local ai_id="empirica-foundation.carly.$practice"

    echo ""
    echo "📌 Deploying: $practice"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Check if already running
    PID_FILE="$LOG_DIR/$practice.pid"

    if [ -f "$PID_FILE" ]; then
        OLD_PID=$(cat "$PID_FILE")
        if kill -0 "$OLD_PID" 2>/dev/null; then
            echo "⚠️  Agent already running (PID: $OLD_PID)"
            echo "   To restart, kill $OLD_PID and re-run deployment"
            return 1
        fi
    fi

    # Start agent
    if bash "$SCRIPT_DIR/start_autonomous_agent.sh" "$ai_id" "$POLL_INTERVAL" > /tmp/start-$practice.log 2>&1; then
        NEW_PID=$(cat "$PID_FILE")
        echo "✅ Agent deployed: $practice (PID: $NEW_PID)"
        echo "   Logs: tail -f $LOG_DIR/$practice.log"
        ((DEPLOYED++))
        return 0
    else
        echo "❌ Deployment failed for $practice"
        cat /tmp/start-$practice.log
        ((FAILED++))
        return 1
    fi
}

# Main deployment loop
if [ -n "$SINGLE_PRACTICE" ]; then
    # Deploy single practice
    if test_practice "$SINGLE_PRACTICE"; then
        if [ "$TEST_ONLY" = false ]; then
            deploy_practice "$SINGLE_PRACTICE"
        fi
    fi
else
    # Deploy all practices
    for practice in "${PRACTICES[@]}"; do
        if [ "$practice" = "empirica-mesh-support" ] && [ "$DEPLOYED" -gt 0 ]; then
            # Skip duplicate
            continue
        fi

        if test_practice "$practice"; then
            if [ "$TEST_ONLY" = false ]; then
                deploy_practice "$practice"
            fi
        else
            ((FAILED++))
        fi
    done
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "Deployment Summary"
echo "════════════════════════════════════════════════════════"
echo "✅ Tested: $TESTED"
echo "✅ Deployed: $DEPLOYED"
echo "❌ Failed: $FAILED"
echo ""

if [ "$FAILED" -eq 0 ]; then
    echo "🎉 All agents ready!"
    if [ "$TEST_ONLY" = false ]; then
        echo ""
        echo "Running agents:"
        ps aux | grep autonomous_agent.py | grep -v grep || echo "  (no agents running yet)"
        echo ""
        echo "Monitor logs:"
        echo "  ls -lh $LOG_DIR/"
        echo "  tail -f $LOG_DIR/*.log"
    fi
else
    echo "⚠️  Some agents failed. Review logs above."
    exit 1
fi

# Update results
jq --arg deployed "$DEPLOYED" --arg tested "$TESTED" --arg failed "$FAILED" \
    '.summary = {deployed: $deployed | tonumber, tested: $tested | tonumber, failed: $failed | tonumber}' \
    "$RESULTS_FILE" > /tmp/results-tmp.json && mv /tmp/results-tmp.json "$RESULTS_FILE"

echo ""
echo "📄 Results: $RESULTS_FILE"
