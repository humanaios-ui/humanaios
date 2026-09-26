#!/bin/bash
#
# Autonomous Agent Fleet Health Monitor
# Real-time monitoring of agent status across all practices
#
# Usage: ./monitor_agents.sh [--interval 10] [--json]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="/tmp/autonomous-agents"
INTERVAL=10
JSON_OUTPUT=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --interval)
            INTERVAL="$2"
            shift 2
            ;;
        --json)
            JSON_OUTPUT=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

get_agent_status() {
    local practice="$1"
    local pid_file="$LOG_DIR/$practice.pid"
    local log_file="$LOG_DIR/$practice.log"

    if [ ! -f "$pid_file" ]; then
        echo "not_deployed"
        return
    fi

    local pid=$(cat "$pid_file" 2>/dev/null || echo "")

    if [ -z "$pid" ]; then
        echo "invalid_pid"
        return
    fi

    if kill -0 "$pid" 2>/dev/null; then
        # Process is running, check if it's responsive
        if [ -f "$log_file" ]; then
            # Check log for errors in last 30 seconds
            local recent_errors=$(grep -c "ERROR\|FAIL" "$log_file" 2>/dev/null || echo "0")
            if [ "$recent_errors" -gt 0 ]; then
                echo "running_with_errors"
            else
                echo "healthy"
            fi
        else
            echo "running"
        fi
    else
        echo "crashed"
    fi
}

print_table_header() {
    printf "%-30s %-15s %-8s %-30s\n" "PRACTICE" "STATUS" "PID" "LAST_UPDATE"
    printf "%-30s %-15s %-8s %-30s\n" "$(printf '=%.0s' {1..29})" "$(printf '=%.0s' {1..14})" "$(printf '=%.0s' {1..7})" "$(printf '=%.0s' {1..29})"
}

print_agent_row() {
    local practice="$1"
    local status="$2"
    local pid="$3"
    local last_update="$4"

    # Color codes
    local green='\033[0;32m'
    local red='\033[0;31m'
    local yellow='\033[1;33m'
    local reset='\033[0m'

    local color=""
    case "$status" in
        healthy)
            color="$green"
            status_display="✓ HEALTHY"
            ;;
        running)
            color="$green"
            status_display="✓ RUNNING"
            ;;
        running_with_errors)
            color="$yellow"
            status_display="⚠ ERRORS"
            ;;
        crashed)
            color="$red"
            status_display="✗ CRASHED"
            ;;
        not_deployed)
            color="$yellow"
            status_display="⊘ NOT_DEPLOYED"
            ;;
        *)
            color="$yellow"
            status_display="? UNKNOWN"
            ;;
    esac

    printf "${color}%-30s %-15s %-8s %-30s${reset}\n" "$practice" "$status_display" "$pid" "$last_update"
}

print_json_status() {
    local statuses="$1"

    echo "$statuses" | jq -s '{
        timestamp: (now | todate),
        agents: [.[] | {
            practice: .practice,
            status: .status,
            pid: .pid,
            last_update: .last_update
        }],
        summary: {
            healthy: ([.[] | select(.status == "healthy")] | length),
            running: ([.[] | select(.status == "running")] | length),
            errors: ([.[] | select(.status == "running_with_errors")] | length),
            crashed: ([.[] | select(.status == "crashed")] | length),
            not_deployed: ([.[] | select(.status == "not_deployed")] | length)
        }
    }'
}

monitor_once() {
    if [ -d "$LOG_DIR" ]; then
        local statuses=""

        # Find all .pid files
        for pid_file in "$LOG_DIR"/*.pid; do
            if [ -f "$pid_file" ]; then
                local practice=$(basename "$pid_file" .pid)
                local pid=$(cat "$pid_file" 2>/dev/null || echo "")
                local status=$(get_agent_status "$practice")
                local last_update=$(stat -f %Sm "$LOG_DIR/$practice.log" 2>/dev/null || echo "N/A")

                if [ "$JSON_OUTPUT" = true ]; then
                    statuses+="$(echo "{\"practice\": \"$practice\", \"status\": \"$status\", \"pid\": \"$pid\", \"last_update\": \"$last_update\"}")"$'\n'
                else
                    print_agent_row "$practice" "$status" "$pid" "$last_update"
                fi
            fi
        done

        if [ "$JSON_OUTPUT" = true ] && [ -n "$statuses" ]; then
            print_json_status "$statuses"
        fi
    else
        echo "⚠️  No agents deployed yet ($LOG_DIR does not exist)"
    fi
}

if [ "$JSON_OUTPUT" = true ]; then
    echo "Monitoring in JSON mode (interval: ${INTERVAL}s)"
    echo ""

    while true; do
        monitor_once
        sleep "$INTERVAL"
    done
else
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║  Autonomous Agent Fleet Health Monitor                         ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Monitoring interval: ${INTERVAL}s (Press Ctrl+C to stop)"
    echo ""

    while true; do
        clear

        echo "╔════════════════════════════════════════════════════════════════╗"
        echo "║  Autonomous Agent Fleet Health Monitor                         ║"
        echo "║  $(date '+%Y-%m-%d %H:%M:%S')                                       ║"
        echo "╚════════════════════════════════════════════════════════════════╝"
        echo ""

        print_table_header

        if [ -d "$LOG_DIR" ]; then
            local healthy_count=0
            local running_count=0
            local error_count=0
            local crashed_count=0
            local not_deployed_count=0

            for pid_file in "$LOG_DIR"/*.pid; do
                if [ -f "$pid_file" ]; then
                    local practice=$(basename "$pid_file" .pid)
                    local pid=$(cat "$pid_file" 2>/dev/null || echo "")
                    local status=$(get_agent_status "$practice")
                    local last_update=$(stat -f %Sm "$LOG_DIR/$practice.log" 2>/dev/null || echo "N/A")

                    print_agent_row "$practice" "$status" "$pid" "$last_update"

                    case "$status" in
                        healthy) ((healthy_count++)) ;;
                        running) ((running_count++)) ;;
                        running_with_errors) ((error_count++)) ;;
                        crashed) ((crashed_count++)) ;;
                        not_deployed) ((not_deployed_count++)) ;;
                    esac
                fi
            done

            echo ""
            echo "Summary:"
            echo "  ✓ Healthy: $healthy_count"
            echo "  ✓ Running: $running_count"
            echo "  ⚠ Errors: $error_count"
            echo "  ✗ Crashed: $crashed_count"
            echo "  ⊘ Not Deployed: $not_deployed_count"
        else
            echo "⚠️  No agents deployed yet"
        fi

        echo ""
        echo "Next update in ${INTERVAL}s..."
        sleep "$INTERVAL"
    done
fi
