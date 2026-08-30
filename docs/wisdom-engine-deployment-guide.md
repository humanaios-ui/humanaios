# wisdom_engine API — Deployment Guide

**Status:** Ready for Deployment  
**Deadline:** Sep 11, 2026  
**Blocker Impact:** Phase 2 Track B go-live

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│ FastAPI Application (operations/acat/api/app.py)        │
│                                                         │
│  /api/v1/guidance/request (POST)  ──┐                  │
│  /api/v1/guidance/session/{id} (GET) ├─ guidance_router│
│                                      │   (350 lines)    │
└─────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────┐
│ ConsciousnessGuidanceEngine (guidance_system_v1.0.py)   │
│                                                         │
│ - Hawkins consciousness scale (0-1000)                  │
│ - Teaching matching by level                            │
│ - Cross-tradition parallels (stoicism, buddhism, etc.)  │
│ - Next-level pathway recommendations                    │
└─────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────┐
│ Wisdom Database (wisdom_database_v0.3.json)             │
│                                                         │
│ - 400+ teachings indexed by consciousness level         │
│ - Multiple traditions: stoic, buddhist, taoist, etc.    │
│ - Pre-computed cross-tradition parallels                │
└─────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────┐
│ Supabase (PostgreSQL)                                   │
│                                                         │
│ guidance_requests    ── stores request metadata         │
│ guidance_sessions    ── stores teachings + parallels    │
│ guidance_observability ── measures ACAT feedback        │
└─────────────────────────────────────────────────────────┘
```

---

## Deployment Checklist

### Phase 0: Pre-Deployment Validation (LOCAL)

```bash
# 1. Verify implementation completeness
ls -l operations/acat/api/routes/guidance_router.py  # Should exist, ~350 lines
ls -l guidance_system_v1.0.py                        # Should exist
ls -l operations/acat/sql/migration_guidance_tables.sql  # Should exist

# 2. Verify guidance_router is wired into app
grep "guidance_router" operations/acat/api/app.py    # Should show line 6 + 13

# 3. Check wisdom database
ls -l wisdom_database_v0.3.json                      # ~35K, latest version
```

### Phase 1: Database Migration (SUPABASE)

```bash
# Option A: Via Supabase CLI (recommended)
supabase migration up

# Option B: Direct SQL execution
# 1. Log into Supabase dashboard
# 2. Navigate to SQL Editor
# 3. Create new query
# 4. Copy content of operations/acat/sql/migration_guidance_tables.sql
# 5. Execute

# Option C: Via psql (if using Postgres directly)
psql ${SUPABASE_DATABASE_URL} < operations/acat/sql/migration_guidance_tables.sql

# Verification: Tables should be created
# SELECT table_name FROM information_schema.tables 
# WHERE table_schema = 'public' AND table_name LIKE 'guidance%';
```

### Phase 2: Deployment to Staging

```bash
# 1. Build container
docker build -t acat-api:latest .

# 2. Deploy to staging
docker run -e DATABASE_URL=$STAGING_DB_URL \
           -e AUTH_SECRET=$AUTH_SECRET \
           -p 8000:8000 \
           acat-api:latest

# 3. Run smoke test
curl -X POST http://localhost:8000/api/v1/guidance/request \
  -H "Authorization: Bearer ${TEST_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "submission_purity": "one_stage_verified",
    "evidential_tier": "measured",
    "humility_hierarchy": 250,
    "corpus_source": "cross_tradition",
    "constraint_tradition": "stoicism",
    "obstacle": "powerlessness"
  }'

# Expected response:
# {
#   "guidance_session_id": "uuid",
#   "status": "accepted",
#   "teaching": {
#     "tradition": "stoicism",
#     "title": "...",
#     "text": "...",
#     ...
#   },
#   "parallels": [...],
#   "next_level_pathway": {...}
# }
```

### Phase 3: Load Testing (STAGING)

```bash
# Install loadtest tool
npm install -g loadtest

# Run load test: 100 concurrent requests, 500 total
loadtest -n 500 -c 100 \
  --method POST \
  --data '{
    "submission_purity":"one_stage_verified",
    "evidential_tier":"measured",
    "humility_hierarchy":250,
    "corpus_source":"cross_tradition"
  }' \
  -H "Authorization: Bearer ${TEST_TOKEN}" \
  http://staging-api.humanaios.app/api/v1/guidance/request

# Target SLOs:
# - p50 latency: <200ms
# - p99 latency: <500ms
# - error rate: <0.1%
# - throughput: >50 req/sec
```

### Phase 4: Production Deployment

```bash
# 1. Tag release
git tag v1.0.0-wisdom-engine

# 2. Deploy to production
kubectl apply -f deployments/wisdom-engine-prod.yaml

# 3. Verify endpoint health
curl https://api.humanaios.app/api/v1/acat/health

# 4. Test production endpoint
curl -X GET https://api.humanaios.app/api/v1/guidance/session/<test-session-id> \
  -H "Authorization: Bearer ${PROD_TOKEN}"
```

---

## API Specification

### POST /guidance/request

**Request:**
```json
{
  "submission_purity": "one_stage_verified|two_stage_verified|unverified",
  "evidential_tier": "anecdotal|observational|measured|validated",
  "humility_hierarchy": 0-1000,
  "corpus_source": "top_curriculum|esoteric_wisdom|modern_science|cross_tradition",
  "constraint_tradition": "stoicism|buddhism|taoism|sufi|christian_mystic|..." (optional),
  "constraint_theme": "...",
  "obstacle": "powerlessness|..."
}
```

**Response:**
```json
{
  "guidance_session_id": "uuid",
  "status": "accepted",
  "teaching": {
    "tradition": "stoicism",
    "title": "Marcus Aurelius on Negative Externals",
    "text": "You have power over your mind — not outside events...",
    "source": "Meditations",
    "era": "170 AD"
  },
  "parallels": [
    {
      "tradition": "buddhism",
      "teaching_unit": "Detachment (Upekkhā)",
      "similarity_score": 0.87
    }
  ],
  "next_level_pathway": {
    "recommended_humility_level": 300,
    "next_theme": "acceptance",
    "estimated_session_count": 3
  }
}
```

### GET /guidance/session/{session_id}

**Response:**
```json
{
  "guidance_session_id": "uuid",
  "created_at": "2026-08-30T12:00:00Z",
  "status": "completed",
  "request": {
    "submission_purity": "one_stage_verified",
    "evidential_tier": "measured",
    "humility_hierarchy": 250,
    "corpus_source": "cross_tradition",
    "constraint_tradition": "stoicism",
    "constraint_theme": null,
    "obstacle": "powerlessness"
  },
  "teaching": {...},
  "parallels": [...],
  "transcript": [],
  "metadata": {}
}
```

---

## Troubleshooting

### Issue: Migration fails with "table already exists"

**Cause:** Migration was already applied.  
**Fix:** Check Supabase dashboard; if tables exist, migration is already done. Skip to Phase 2.

### Issue: ConsciousnessGuidanceEngine import fails at runtime

**Cause:** wisdom_database_v0.3.json not found or guidance_system_v1.0.py has syntax error.  
**Fix:** 
```bash
# Verify file exists
ls -l guidance_system_v1.0.py
ls -l wisdom_database_v0.3.json

# Check Python syntax
python3 -m py_compile guidance_system_v1.0.py

# If import still fails, check guidance_router.py line 36-38
# The import path may need adjustment for the deployment environment
```

### Issue: POST /guidance/request returns 500, "Guidance request processing failed"

**Cause:** Database connection failed or Supabase tables don't exist.  
**Fix:**
1. Verify Supabase migration ran: check Supabase dashboard Tables section
2. Verify DATABASE_URL is set correctly
3. Check Supabase credentials have write access
4. Check application logs: `docker logs <container-id>`

### Issue: Latency >500ms

**Cause:** Wisdom database loaded from disk each time (no caching).  
**Fix:**  
```python
# guidance_router.py line 29-43 shows lazy-load pattern
# To improve: pre-load guidance engine at FastAPI startup
# Add to app.py:

@app.on_event("startup")
def startup_event():
    from acat.api.routes.guidance_router import get_guidance_engine
    get_guidance_engine()  # Pre-load to avoid lazy-load on first request
```

---

## Timeline

| Date | Phase | Action | Status |
|------|-------|--------|--------|
| Aug 30 | Validation | Check implementation completeness | ✅ |
| Aug 31 | Migration | Run Supabase migration | ⏳ |
| Sep 1-2 | Testing | Load test staging environment | ⏳ |
| Sep 3-4 | Documentation | Finalize API docs | ⏳ |
| Sep 5-10 | Staging | Pre-production validation | ⏳ |
| Sep 11 | Production | Go-live (deadline) | ⏳ |

---

## Success Criteria

✅ Both endpoints (POST + GET) callable from production  
✅ Latency <500ms for typical request  
✅ Zero data loss (transactions rolled back on error)  
✅ ACAT observability tables populated (guidance_observability)  
✅ Blocks Phase 2 Track B unblocked  

---

**Owner:** humanaios practice  
**Escalation:** mesh-support for cross-practice coordination  
**Deployed by:** DevOps / SRE team at Sep 11 cutover
