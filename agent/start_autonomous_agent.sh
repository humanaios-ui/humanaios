#!/bin/bash
# Start Autonomous Agent for a practice

# Usage:
#   ./start_autonomous_agent.sh <practice-ai-id> [poll_interval_seconds]
#
# Example:
#   ./start_autonomous_agent.sh empirica-foundation.carly.empirica-autonomy 30

set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <practice-ai-id> [poll_interval_seconds]"
    echo ""
    echo "Example:"
    echo "  $0 empirica-foundation.carly.empirica-autonomy 30"
    exit 1
fi

AI_ID="$1"
POLL_INTERVAL="${2:-30}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Validate AI ID format
if [[ ! "$AI_ID" =~ ^empirica-foundation\.carly\.[a-z0-9-]+$ ]]; then
    echo "❌ Invalid AI ID format. Expected: empirica-foundation.carly.<practice-name>"
    exit 1
fi

PRACTICE_NAME="${AI_ID##*.}"
LOG_DIR="/tmp/autonomous-agents"
LOG_FILE="$LOG_DIR/$PRACTICE_NAME.log"
PID_FILE="$LOG_DIR/$PRACTICE_NAME.pid"

mkdir -p "$LOG_DIR"

echo "🚀 Starting Autonomous Agent: $AI_ID"
echo "   Poll interval: ${POLL_INTERVAL}s"
echo "   Log file: $LOG_FILE"
echo ""

# Check if agent already running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if kill -0 "$OLD_PID" 2>/dev/null; then
        echo "❌ Agent already running (PID: $OLD_PID)"
        exit 1
    else
        rm "$PID_FILE"
    fi
fi

# Start agent in background
cd "$SCRIPT_DIR"
python3 autonomous_agent.py "$AI_ID" "$POLL_INTERVAL" >> "$LOG_FILE" 2>&1 &
PID=$!

echo "$PID" > "$PID_FILE"
echo "✓ Agent started (PID: $PID)"
echo "✓ Logs: tail -f $LOG_FILE"
echo ""
echo "To stop: kill $PID"
