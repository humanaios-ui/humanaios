#!/bin/bash
# Phase 3.5.1 Observability Stack Deployment
# Deploys Jaeger + Loki + Promtail infrastructure

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$SCRIPT_DIR/docker-compose.observability.yml"

echo "📦 Phase 3.5.1: Observability Stack Deployment"
echo "================================================"
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Install Docker and try again."
    exit 1
fi

if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker daemon is not running."
    exit 1
fi

echo "✓ Docker available"
echo ""

# Deploy
echo "Starting services..."
docker-compose -f "$COMPOSE_FILE" up -d

echo "Waiting 15s for services to initialize..."
sleep 15

echo ""
echo "🔍 Health Checks"
echo "==============="

# Jaeger health check
echo -n "Jaeger (port 16686): "
if curl -sf http://localhost:16686/api/health > /dev/null 2>&1; then
    echo "✓ Healthy"
else
    echo "✗ Unreachable (check Docker logs: docker logs empirica-jaeger)"
    exit 1
fi

# Loki health check
echo -n "Loki (port 3100): "
if curl -sf http://localhost:3100/loki/api/v1/status/buildinfo > /dev/null 2>&1; then
    echo "✓ Healthy"
else
    echo "✗ Unreachable (check Docker logs: docker logs empirica-loki)"
    exit 1
fi

echo ""
echo "📊 Container Status"
echo "==================="
docker-compose -f "$COMPOSE_FILE" ps

echo ""
echo "✅ Phase 3.5.1 Deployment Complete"
echo ""
echo "Access points:"
echo "  - Jaeger UI: http://localhost:16686"
echo "  - Loki API: http://localhost:3100"
echo ""
echo "Next steps:"
echo "  1. Run Phase 3.5.2 (Observability Instrumentation) to wire up log sources"
echo "  2. Verify log ingestion: curl http://localhost:3100/loki/api/v1/query?query={job=\"docker\"}"
echo ""
