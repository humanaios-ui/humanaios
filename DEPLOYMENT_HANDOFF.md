# Production Deployment Handoff

**Date:** 2026-08-15  
**From:** HumanAIOS Practice (Claude Code)  
**To:** Deployment Team  
**Status:** ✓ READY FOR PRODUCTION  

---

## Quick Start

### Prerequisites
```bash
# 1. Ensure you have access to:
# - Docker registry (push credentials)
# - Production infrastructure (k8s/Docker/SCP)
# - API server deployment method
# - Frontend CDN/web server

# 2. Set environment variables:
export DEPLOYMENT_ENV="production"
export API_HOST="humanaios-api.example.com"
export DOCKER_REGISTRY="your-registry"
export HUMANAIOS_TOKEN="your_prod_token"
```

### Execute Deployment
```bash
# Run automated deployment script:
cd /Users/andersonfamily/practices/humanaios
bash DEPLOYMENT_EXECUTION.sh

# Or follow manual steps in docs/TRACK2_QA_TEST_DEPLOYMENT.md Section 2
```

**Timeline:** ~35 minutes (build + deploy + smoke tests)

---

## What's Being Deployed

### Backend Components
- **Track 2 SSE Streaming:** Real-time marker event streaming via SSE
- **Marker Ingestion:** Cortex event → marker conversion + broker distribution
- **Marker Palette:** Metadata endpoint (9 marker types, frequencies, icons)
- **Authentication:** Bearer token via require_read_token gate
- **Location:** `/api/v1/sonify/` endpoints (prefix in app.py)

### Frontend Components
- **useMarkerEvents Hook:** SSE connection + event parsing
- **MarkerNotification Component:** Individual toast display + auto-close
- **MarkerToastContainer:** Toast stack manager (max 5, auto-remove oldest)
- **Integration Example:** App.example.tsx shows integration pattern

### Testing & Monitoring
- **QA Suite:** 10-point manual checklist + automated test script
- **Smoke Tests:** 5 post-deployment verifications
- **Monitoring Window:** 72 hours (2026-08-15 to 2026-08-17)
- **Health Checks:** /api/v1/acat/health + /api/v1/sonify/markers/palette

---

## Files Provided

### Deployment
- `DEPLOYMENT_EXECUTION.sh` — Automated deployment script (customize for your infra)
- `docs/TRACK2_QA_TEST_DEPLOYMENT.md` — Detailed QA + deployment procedures
- `docs/DEPLOYMENT_READINESS_SIGN_OFF.md` — Approval + risk assessment
- `test_track2_qa.sh` — Automated QA test suite

### Documentation
- `docs/TRACK2_UI_INTEGRATION_COMPLETE.md` — Full backend + frontend guide
- `docs/TRACK2_FRONTEND_IMPLEMENTATION_STATUS.md` — React components + integration
- `docs/P6_VERDICTS_INTEGRATION.md` — P6 verdicts ingestion guide
- `MESH_COORDINATION_MESSAGES.md` — Ready-to-send collab messages (5 messages)

### Code
- `operations/track2_ui_integration.py` — Backend SSE + broker implementation
- `operations/acat/api/app.py` — Track 2 router wired (updated)
- `lasting-light-ai/src/hooks/useMarkerEvents.ts` — React hook (SSE connection)
- `lasting-light-ai/src/components/MarkerNotification.tsx` — Toast component
- `lasting-light-ai/src/components/MarkerToastContainer.tsx` — Stack manager
- `lasting-light-ai/src/App.example.tsx` — Integration example

---

## Pre-Deployment Checklist

### Infrastructure Setup
- [ ] Docker registry accessible (push credentials configured)
- [ ] Production API server ready (k8s/Docker/manual deployment method)
- [ ] Frontend deployment target ready (S3/web server/CDN)
- [ ] Health check endpoints accessible
- [ ] Database backups current (safety net for rollback)

### Configuration
- [ ] DEPLOYMENT_ENV set to "production"
- [ ] API_HOST and DOCKER_REGISTRY configured
- [ ] Auth token (HUMANAIOS_TOKEN) available
- [ ] Infrastructure-specific deployment commands customized in DEPLOYMENT_EXECUTION.sh
- [ ] Frontend deployment target path/URL configured

### Verification
- [ ] Git branch is feature/m2r2-state-harmonization-humanaios
- [ ] All commits pushed to remote
- [ ] Code review approved (if required)
- [ ] QA tests passing locally (run `bash test_track2_qa.sh`)
- [ ] Rollback procedure understood

---

## Deployment Steps (Summary)

1. **Build Backend** (5 min)
   ```bash
   cd operations
   docker build -t $DOCKER_REGISTRY/humanaios-api:latest .
   docker push $DOCKER_REGISTRY/humanaios-api:latest
   ```

2. **Build Frontend** (5 min)
   ```bash
   cd lasting-light-ai
   npm ci && npm run build
   ```

3. **Deploy Infrastructure** (10 min, customizable)
   - Kubernetes: `kubectl set image deployment/humanaios-api api=...`
   - Docker Compose: `docker-compose -f prod.yml up -d`
   - Manual: SSH + docker pull + restart

4. **Deploy Frontend** (5 min, customizable)
   - S3: `aws s3 sync build/ s3://bucket/`
   - Web server: `scp -r build/* user@host:/var/www/`
   - Cloudflare: `wrangler publish`

5. **Smoke Tests** (10 min)
   - Health check: `curl /api/v1/acat/health`
   - Palette: `curl /api/v1/sonify/markers/palette`
   - SSE stream: Browser console EventSource check
   - End-to-end: Emit test marker, verify in UI

---

## Mesh Coordination (Concurrent)

While deployment is running, **send these mesh coordination messages** to coordinate next steps:

```bash
# Send all 5 messages (or follow MESH_COORDINATION_MESSAGES.md):
# 1. Track 2 deployment ready → mesh-support
# 2. P6 verdicts ready → autonomy
# 3. Practice spec review kickoff → mesh-support
# 4. Phase 1 alignment complete → autonomy + evaluator
# 5. M2R2 Phase 4 rollout ready → 5 repos
```

**Effect:** Parallelizes next phase work (Phase 1 ACAT scoring, Phase 4 M2R2 rollout, practice spec review) while deployment verification runs.

---

## Post-Deployment Verification

### Immediate (within 1 hour)
- [ ] Backend service is running and healthy
- [ ] Frontend is accessible in browser
- [ ] SSE stream connects without errors (DevTools Network tab)
- [ ] Test marker emits successfully (backend → browser)
- [ ] Toast notification appears in UI

### Monitoring Window (72 hours: 2026-08-15 to 2026-08-17)
- [ ] SSE connection success rate >99%
- [ ] Marker ingestion latency <100ms
- [ ] Frontend error rate = 0%
- [ ] Backend error rate <0.1%
- [ ] No console errors or warnings

### Sign-Off
- [ ] QA Lead: Verification tests passed
- [ ] Deployment Lead: Infrastructure healthy
- [ ] Product Owner: User acceptance confirmed
- [ ] Ops: Monitoring configured for 72h

---

## Rollback Procedure

**If deployment fails or issues arise:**

### Quick Rollback (<10 minutes)
```bash
# Revert to previous backend version:
docker pull $DOCKER_REGISTRY/humanaios-api:previous
docker push $DOCKER_REGISTRY/humanaios-api:previous
# Restart using previous image

# Revert frontend (if applicable):
# Revert to previous S3/web server version
```

### Full Rollback (if severe issues)
```bash
# 1. Switch load balancer to previous environment
# 2. Notify ops team (incident response)
# 3. Investigate root cause
# 4. Plan re-deployment once fixed
```

**Recovery Window:** <30 minutes to stable state

---

## Support & Escalation

### During Deployment
- **Deployment Issues:** Check DEPLOYMENT_EXECUTION.sh output, verify infrastructure access
- **Build Failures:** Read Docker build output, check dependencies
- **Health Check Failures:** Run `curl /api/v1/acat/health` manually, check logs

### Post-Deployment Issues
- **SSE Connection Fails:** Check auth token, verify endpoint, check CORS headers
- **Marker Toasts Don't Appear:** Check browser console, verify backend sending events
- **Performance Issues:** Monitor CPU/memory, check SSE connection count

### Escalation Path
1. Deployment Team: Check logs, verify infrastructure
2. Backend Lead: Check Track 2 backend implementation
3. Frontend Lead: Check React components, browser compatibility
4. Ops Lead: Infrastructure health, service restart

---

## Next Phase Work (Coordinated)

After deployment verification (24-48h):

1. **Phase 1 ACAT Scoring** (autonomy)
   - Start baseline assessment with ACAT Scorer v1.1
   - P6 verdicts ingest to humanaios
   - Continue until Phase 1 closes (2026-09-14)

2. **Phase 1.5 Bridging Study** (humanaios + autonomy)
   - Compare synthetic (P6) vs real (Phase 1) divergence patterns
   - Analyze grader alignment across substrates
   - Prepare for Phase 2 grader composition decision

3. **M2R2 Phase 4 Rollout** (all 5 repos)
   - Apply schema migration to autonomy, website, outreach, mesh-support, evaluator
   - Coordinate staging + production deployment
   - 48-hour post-rollout monitoring

4. **Practice Specification Review** (mesh-support + Admiral)
   - Mesh-support reviews spec (Aug 12-18)
   - Admiral ratification (Aug 19-25)
   - Publish (Aug 25)

---

## Sign-Off Checklist

| Item | Owner | Status |
|------|-------|--------|
| Deployment execution | Deployment Lead | [ ] Ready |
| Infrastructure access | Ops | [ ] Ready |
| QA test suite run | QA Lead | [ ] Ready |
| Post-deployment verification | QA Lead | [ ] Ready |
| 72-hour monitoring setup | Ops | [ ] Ready |
| Mesh coordination messages sent | HumanAIOS | [ ] Ready |
| Product owner acceptance | Product Owner | [ ] Ready |

---

## Contact & Support

- **HumanAIOS Practice:** Available for deployment support and mesh coordination
- **Deployment Lead:** [TO BE ASSIGNED]
- **QA Lead:** [TO BE ASSIGNED]
- **Ops Lead:** [TO BE ASSIGNED]

---

**Handoff Complete:** ✓  
**Deployment Target:** 2026-08-15 afternoon  
**Estimated Duration:** 35 minutes  
**Risk Level:** LOW  
**Rollback Available:** Yes (<10 minutes)  

🚀 **Ready for production deployment.**

