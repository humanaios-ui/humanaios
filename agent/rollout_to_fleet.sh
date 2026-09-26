#!/bin/bash
# Deploy Autonomous Agent to all 15 foundation practices

# Usage:
#   ./rollout_to_fleet.sh [stagger_minutes] [poll_interval]
#
# Example (30 minute stagger between startups, 30s poll interval):
#   ./rollout_to_fleet.sh 30 30

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STAGGER_MINUTES="${1:-30}"
POLL_INTERVAL="${2:-30}"

# All 15 foundation practices
PRACTICES=(
    "empirica-foundation"
    "empirica-autonomy"
    "empirica-mesh-support"
    "empirica-outreach"
    "humanaios"
    "website"
    "empirica-resource-miner"
    "opportunity-aggregator"
    "local-machine-optimizer"
    "acat-x"
    "grok-crossref"
    "integrations-hub"
    "metrics-collector"
    "event-bridge"
    "governance-sync"
)

echo "🚀 Autonomous Agent Fleet Rollout"
echo "=================================="
echo "Practices: ${#PRACTICES[@]}"
echo "Stagger: ${STAGGER_MINUTES}m"
echo "Poll interval: ${POLL_INTERVAL}s"
echo ""

LOG_DIR="/tmp/fleet-rollout"
mkdir -p "$LOG_DIR"

ROLLOUT_LOG="$LOG_DIR/rollout-$(date +%Y%m%d_%H%M%S).log"
echo "Rollout log: $ROLLOUT_LOG"
echo ""

deployed=0
failed=0

for practice in "${PRACTICES[@]}"; do
    ai_id="empirica-foundation.carly.$practice"
    echo "→ Deploying $practice..."

    if bash "$SCRIPT_DIR/start_autonomous_agent.sh" "$ai_id" "$POLL_INTERVAL" 2>&1 | tee -a "$ROLLOUT_LOG"; then
        echo "  ✓ $practice deployed"
        ((deployed++))
    else
        echo "  ❌ $practice failed"
        ((failed++))
    fi

    if [ $deployed -lt ${#PRACTICES[@]} ]; then
        echo "  ⏳ Waiting ${STAGGER_MINUTES}m before next deployment..."
        sleep $((STAGGER_MINUTES * 60))
    fi

    echo ""
done

echo ""
echo "========================================"
echo "Rollout Complete"
echo "========================================"
echo "Deployed: $deployed/${#PRACTICES[@]}"
echo "Failed: $failed/${#PRACTICES[@]}"
echo "Rollout log: $ROLLOUT_LOG"
echo ""

if [ $failed -eq 0 ]; then
    echo "✓ All practices deployed successfully"
    exit 0
else
    echo "❌ $failed practices failed deployment"
    exit 1
fi
