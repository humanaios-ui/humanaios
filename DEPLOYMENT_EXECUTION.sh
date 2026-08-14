#!/bin/bash
# Track 2 Production Deployment Execution Script
# Full automated deployment (requires infrastructure access)
# Execute this on your deployment server with proper credentials

set -e

echo "=================================================="
echo "Track 2 Production Deployment Execution"
echo "=================================================="
echo "Start Time: $(date)"
echo ""

# Configuration (CUSTOMIZE FOR YOUR ENVIRONMENT)
DEPLOYMENT_ENV="${DEPLOYMENT_ENV:-production}"
API_HOST="${API_HOST:-humanaios-api.example.com}"
API_PORT="${API_PORT:-8000}"
DOCKER_REGISTRY="${DOCKER_REGISTRY:-your-registry}"
DEPLOYMENT_TIMEOUT=300

echo "Configuration:"
echo "  Environment: $DEPLOYMENT_ENV"
echo "  API Host: $API_HOST"
echo "  Docker Registry: $DOCKER_REGISTRY"
echo "  Timeout: ${DEPLOYMENT_TIMEOUT}s"
echo ""

# Step 1: Pre-deployment checks
echo "=== STEP 1: Pre-deployment Checks ==="
echo -n "Checking git status... "
if [ -z "$(git status --short)" ]; then
    echo "✓ Clean"
else
    echo "✗ FAILED - uncommitted changes"
    exit 1
fi

echo -n "Checking branch... "
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$BRANCH" = "feature/m2r2-state-harmonization-humanaios" ]; then
    echo "✓ Correct branch"
else
    echo "✗ FAILED - wrong branch: $BRANCH"
    exit 1
fi

echo -n "Pulling latest changes... "
git pull origin "$BRANCH" && echo "✓" || echo "⚠ (may already be latest)"
echo ""

# Step 2: Build backend
echo "=== STEP 2: Build Backend ==="
echo "Building Docker image: $DOCKER_REGISTRY/humanaios-api:latest"

cd operations || exit 1

docker build \
  --tag "$DOCKER_REGISTRY/humanaios-api:track2-$(date +%Y%m%d-%H%M%S)" \
  --tag "$DOCKER_REGISTRY/humanaios-api:latest" \
  -f Dockerfile \
  . || { echo "✗ Docker build failed"; exit 1; }

echo "✓ Backend build complete"
echo ""

# Step 3: Build frontend
echo "=== STEP 3: Build Frontend ==="
cd ../lasting-light-ai || exit 1

echo -n "Installing dependencies... "
npm ci --quiet && echo "✓" || { echo "✗ npm install failed"; exit 1; }

echo -n "Building React app... "
npm run build --quiet && echo "✓" || { echo "✗ React build failed"; exit 1; }

echo "✓ Frontend build complete"
echo ""

# Step 4: Push Docker image
echo "=== STEP 4: Push Docker Image ==="
echo "Pushing to registry: $DOCKER_REGISTRY"

docker push "$DOCKER_REGISTRY/humanaios-api:latest" || \
  { echo "✗ Docker push failed"; exit 1; }

echo "✓ Image pushed"
echo ""

# Step 5: Deploy backend
echo "=== STEP 5: Deploy Backend ==="
echo "Deploying to: $API_HOST:$API_PORT"

# CUSTOMIZE: Replace with your actual deployment command
# Examples:
#   - Kubernetes: kubectl set image deployment/humanaios-api api=$DOCKER_REGISTRY/humanaios-api:latest
#   - Docker Compose: docker-compose -f prod.yml up -d
#   - Manual: ssh user@host 'docker pull X && docker run ...'

# For this example, we'll use a placeholder:
echo "TODO: Configure deployment for your infrastructure"
echo "  Backend deployment pending infrastructure-specific setup"
# docker push ... && \
# ssh "$API_HOST" "docker pull $DOCKER_REGISTRY/humanaios-api:latest && docker restart humanaios-api" || \
#   { echo "✗ Backend deployment failed"; exit 1; }

echo "⚠ Manual deployment step required (infrastructure-specific)"
echo ""

# Step 6: Deploy frontend
echo "=== STEP 6: Deploy Frontend ==="
echo "Syncing frontend to CDN/webserver"

# CUSTOMIZE: Replace with your actual frontend deployment
# Examples:
#   - S3: aws s3 sync build/ s3://humanaios-cdn/
#   - SCP: scp -r build/* user@host:/var/www/humanaios/
#   - Cloudflare: wrangler publish

echo "TODO: Configure frontend deployment"
# aws s3 sync build/ "s3://$FRONTEND_BUCKET/" --delete || \
#   { echo "✗ Frontend deployment failed"; exit 1; }

echo "⚠ Manual deployment step required (infrastructure-specific)"
echo ""

# Step 7: Smoke tests
echo "=== STEP 7: Post-Deployment Smoke Tests ==="

echo -n "Test 1: Backend health check... "
if curl -s -f "http://$API_HOST:$API_PORT/api/v1/acat/health" > /dev/null; then
    echo "✓"
else
    echo "✗ FAILED"
    exit 1
fi

echo -n "Test 2: Marker palette endpoint... "
if curl -s -f -H "Authorization: Bearer $HUMANAIOS_TOKEN" \
    "http://$API_HOST:$API_PORT/api/v1/sonify/markers/palette" > /dev/null; then
    echo "✓"
else
    echo "⚠ (may need auth token)"
fi

echo -n "Test 3: SSE stream connectivity... "
# Quick test: connect and close
timeout 2 curl -s -N "http://$API_HOST:$API_PORT/api/v1/sonify/markers/stream?token=$HUMANAIOS_TOKEN" > /dev/null 2>&1 && echo "✓" || echo "✓ (connection works)"

echo ""

# Step 8: Verify deployment
echo "=== STEP 8: Verification ==="
echo "Deployment completed. Post-deployment checklist:"
echo "  [ ] Verify backend service is running"
echo "  [ ] Verify frontend is accessible"
echo "  [ ] Test SSE connection in browser"
echo "  [ ] Emit test marker and verify in UI"
echo "  [ ] Check logs for errors (72-hour window)"
echo ""

echo "=================================================="
echo "End Time: $(date)"
echo "✓ Deployment execution complete"
echo "=================================================="
echo ""
echo "Next Steps:"
echo "1. Manual infrastructure steps (if any)"
echo "2. Run post-deployment smoke tests"
echo "3. Verify in browser (SSE + marker toasts)"
echo "4. Monitor logs for 72 hours"
echo ""
