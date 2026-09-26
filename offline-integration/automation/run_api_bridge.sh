#!/bin/bash
# API Bridge Startup Script
# Initializes database, runs migrations, and starts the Flask API bridge
#
# Usage:
#   ./run_api_bridge.sh [--init] [--test] [--port 5000]
#
# Options:
#   --init              Initialize database tables (first time setup)
#   --test              Test database connection before starting
#   --port PORT         Port to run on (default: 5000)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
SCRIPTS_DIR="$PROJECT_ROOT/scripts"

PORT="${PORT:-5000}"
DB_INIT=false
DB_TEST=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --init)
            DB_INIT=true
            shift
            ;;
        --test)
            DB_TEST=true
            shift
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

# Load environment
if [ -f "$PROJECT_ROOT/.env" ]; then
    export $(cat "$PROJECT_ROOT/.env" | grep -v '^#' | xargs)
elif [ -f "$PROJECT_ROOT/.env.example" ]; then
    echo "⚠️  No .env file found. Using .env.example as reference."
    echo "    Create .env with your actual DATABASE_URL"
    export $(cat "$PROJECT_ROOT/.env.example" | grep -v '^#' | xargs)
fi

# Initialize database if requested
if [ "$DB_INIT" = true ]; then
    echo "Initializing database..."
    python3 "$SCRIPTS_DIR/init_api_bridge_db.py" --init
    echo ""
fi

# Test database connection if requested
if [ "$DB_TEST" = true ]; then
    echo "Testing database connection..."
    python3 "$SCRIPTS_DIR/init_api_bridge_db.py" --test
    echo ""
fi

# Check database connectivity
echo "Checking database connectivity..."
python3 "$SCRIPTS_DIR/init_api_bridge_db.py" --test || {
    echo ""
    echo "✗ Database connection failed."
    echo "  Run with --init flag first: ./run_api_bridge.sh --init"
    exit 1
}

echo ""
echo "Starting API Bridge (Database v2)..."
echo "Listening on http://localhost:$PORT"
echo "Database: $DATABASE_URL"
echo ""
echo "Endpoints:"
echo "  POST /gate/registry       — Submit record to registry gate (DB persisted)"
echo "  GET  /state/sync          — Get system state from DB"
echo "  POST /harness/set         — Set resource harness mode (DB persisted)"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run the API bridge
cd "$SCRIPT_DIR"
python3 -c "
import sys
sys.path.insert(0, '.')
from api_bridge_db import create_app
app = create_app()
app.run(debug=True, port=$PORT, host='0.0.0.0')
"
