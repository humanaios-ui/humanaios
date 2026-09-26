#!/bin/bash
# Integration script: Wire empirica CLI to forward logs to Loki
#
# Task 6: Deploy instrumentation to empirica CLI
# Task 7: Enable log forwarding from empirica commands
#
# This script patches empirica's logging config to use LokiHandler

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EMPIRICA_HOME="${HOME}/.empirica"
LOKI_URL="${LOKI_URL:-http://localhost:3100}"

echo "🚀 Empirica → Loki Integration"
echo "======================================"
echo ""

# Step 1: Copy instrumentation modules
echo "📌 Step 1: Install instrumentation modules"
SITE_PACKAGES=$(python3 -c "import site; print(site.getsitepackages()[0])")

cp "${SCRIPT_DIR}/empirica-loki-logging.py" "${SITE_PACKAGES}/"
cp "${SCRIPT_DIR}/empirica-jaeger-tracing.py" "${SITE_PACKAGES}/"

echo "  ✓ Modules installed to ${SITE_PACKAGES}"
echo ""

# Step 2: Create empirica logging config
echo "📌 Step 2: Create logging configuration"
mkdir -p "${EMPIRICA_HOME}/logging"

cat > "${EMPIRICA_HOME}/logging/loki.yaml" <<'EOF'
# Empirica → Loki Logging Configuration
# Applied to all empirica CLI commands

handlers:
  loki:
    class: empirica_loki_logging.EmpirikaLokiHandler
    loki_url: "http://localhost:3100"
    batch_size: 10

  acat:
    class: empirica_loki_logging.AcatMetricsLokiHandler
    loki_url: "http://localhost:3100"

loggers:
  empirica.sessions:
    handlers: [loki]
    level: DEBUG

  empirica.acat:
    handlers: [acat]
    level: INFO

  empirica.cli:
    handlers: [loki]
    level: INFO
EOF

echo "  ✓ Config created at ${EMPIRICA_HOME}/logging/loki.yaml"
echo ""

# Step 3: Create Python wrapper for empirica CLI
echo "📌 Step 3: Create empirica CLI wrapper"
mkdir -p "${EMPIRICA_HOME}/bin"

cat > "${EMPIRICA_HOME}/bin/empirica-with-loki" <<'EOF'
#!/usr/bin/env python3
"""
Empirica CLI wrapper that enables Loki logging

Usage:
    empirica-with-loki preflight-submit -
    empirica-with-loki check-submit -
    empirica-with-loki postflight-submit -
"""

import sys
import logging
import os
from pathlib import Path

# Import empirica and Loki handlers
sys.path.insert(0, '/usr/local/lib/python3.11/site-packages')
from empirica_loki_logging import setup_empirica_loki_logging, setup_acat_metrics_logging

# Get session context from environment
session_id = os.getenv('EMPIRICA_SESSION_ID', 'unknown')
practice = os.getenv('EMPIRICA_PRACTICE', 'unknown')
phase = os.getenv('EMPIRICA_PHASE', 'unknown')
loki_url = os.getenv('LOKI_URL', 'http://localhost:3100')

# Setup loggers
logger = setup_empirica_loki_logging(session_id, practice, phase, loki_url)
acat_logger = setup_acat_metrics_logging(loki_url)

# Log CLI invocation
logger.info(f"Empirica CLI: {' '.join(sys.argv[1:])}", extra={
    'session_id': session_id,
    'practice': practice,
    'phase': phase,
    'command': sys.argv[1] if len(sys.argv) > 1 else 'unknown'
})

# Import and run empirica CLI
try:
    from empirica.cli import main
    main()
except SystemExit as e:
    if e.code == 0:
        logger.info("Command completed successfully")
    else:
        logger.error(f"Command failed with exit code {e.code}")
    raise
EOF

chmod +x "${EMPIRICA_HOME}/bin/empirica-with-loki"
echo "  ✓ Wrapper created at ${EMPIRICA_HOME}/bin/empirica-with-loki"
echo ""

# Step 4: Create environment setup script
echo "📌 Step 4: Create environment setup script"
cat > "${EMPIRICA_HOME}/setup-loki.sh" <<'EOF'
#!/bin/bash
# Setup script: Load environment for Loki logging

# Session context (set these before running empirica)
export EMPIRICA_SESSION_ID="${EMPIRICA_SESSION_ID:-sess_$(date +%s)}"
export EMPIRICA_PRACTICE="${EMPIRICA_PRACTICE:-unknown}"
export EMPIRICA_PHASE="${EMPIRICA_PHASE:-PREFLIGHT}"
export LOKI_URL="${LOKI_URL:-http://localhost:3100}"

# Python path
export PYTHONPATH="${HOME}/.empirica/lib:${PYTHONPATH}"

# Alias empirica CLI to use wrapper
alias empirica="${HOME}/.empirica/bin/empirica-with-loki"

echo "✓ Loki logging enabled"
echo "  Session ID: $EMPIRICA_SESSION_ID"
echo "  Practice: $EMPIRICA_PRACTICE"
echo "  Loki URL: $LOKI_URL"
EOF

chmod +x "${EMPIRICA_HOME}/setup-loki.sh"
echo "  ✓ Setup script created at ${EMPIRICA_HOME}/setup-loki.sh"
echo ""

# Step 5: Instructions
echo "════════════════════════════════════════"
echo "✅ Integration Complete"
echo "════════════════════════════════════════"
echo ""
echo "To enable Loki logging in empirica:"
echo ""
echo "  1. Source the setup script:"
echo "     source ~/.empirica/setup-loki.sh"
echo ""
echo "  2. Run empirica commands (logs auto-forward to Loki):"
echo "     empirica preflight-submit -"
echo "     empirica check-submit -"
echo "     empirica postflight-submit -"
echo ""
echo "  3. View logs in Loki UI:"
echo "     http://localhost:3100/loki/ui/"
echo ""
echo "  4. Query logs:"
echo "     curl \"http://localhost:3100/loki/api/v1/query?query={practice=\\\"autonomy\\\"}\""
echo ""
