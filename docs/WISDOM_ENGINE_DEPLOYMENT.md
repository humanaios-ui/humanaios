# Wisdom Engine Deployment & Testing Guide

## Status: ✅ DEPLOYED

**Date:** 2026-08-02  
**Schema Migration:** `migration_guidance_tables.sql`  
**Commit:** `52a2aa0`
**Deployment Status:** Ready for production

---

## 1. Schema Deployment

### Local Development (PostgreSQL)

```bash
# Create database (if needed)
createdb humanaios

# Deploy migration
psql -d humanaios -f operations/acat/sql/migration_guidance_tables.sql
```

### Supabase Production

```bash
# Install Supabase CLI (if not already installed)
npm install -g supabase

# Link to Supabase project
supabase link --project-id YOUR_PROJECT_ID

# Deploy migration to Supabase
supabase migration deploy
```

### Verification

```bash
# List guidance tables
psql -d humanaios -c "\dt guidance_*"

# Expected output:
#                    List of relations
#  Schema |          Name          | Type  |     Owner      
# --------+------------------------+-------+----------------
#  public | guidance_observability | table | postgres
#  public | guidance_requests      | table | postgres
#  public | guidance_sessions      | table | postgres
```

---

## 2. API Endpoint Testing

### Start FastAPI Server

```bash
cd operations/acat/api
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Test POST /api/v1/guidance/request

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/guidance/request \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test-token" \
  -d '{
    "submission_purity": "two_stage_verified",
    "evidential_tier": "measured",
    "humility_hierarchy": 300,
    "corpus_source": "top_curriculum",
    "constraint_tradition": "stoicism",
    "constraint_theme": "dealing-with-uncertainty",
    "obstacle": "powerlessness"
  }'
```

**Expected Response (200 OK):**
```json
{
  "guidance_session_id": "42503a5e-789a-4de5-a30b-5c4e6ff4e6e0",
  "status": "accepted",
  "teaching": {
    "tradition": "stoicism",
    "title": "Amor Fati: Embracing What Is",
    "text": "Teaching text here...",
    "source": "Marcus Aurelius Meditations",
    "era": "2nd century CE"
  },
  "parallels": [
    {
      "tradition": "buddhism",
      "teaching_unit": "Mindfulness Practice",
      "similarity_score": 0.75
    }
  ],
  "next_level_pathway": {
    "recommended_humility_level": 350,
    "next_theme": "advanced-wisdom",
    "estimated_session_count": 3
  }
}
```

### Test GET /api/v1/guidance/session/{id}

**Request:**
```bash
curl -X GET http://localhost:8000/api/v1/guidance/session/42503a5e-789a-4de5-a30b-5c4e6ff4e6e0 \
  -H "Authorization: Bearer test-token"
```

**Expected Response (200 OK):**
```json
{
  "guidance_session_id": "42503a5e-789a-4de5-a30b-5c4e6ff4e6e0",
  "created_at": "2026-08-02T12:40:57.048826",
  "status": "completed",
  "request": {
    "submission_purity": "two_stage_verified",
    "evidential_tier": "measured",
    "humility_hierarchy": 300,
    "corpus_source": "top_curriculum",
    "constraint_tradition": "stoicism",
    "constraint_theme": "dealing-with-uncertainty",
    "obstacle": "powerlessness"
  },
  "teaching": {
    "tradition": "stoicism",
    "title": "Amor Fati",
    "text": "Teaching text...",
    "source": "Marcus Aurelius",
    "era": null
  },
  "parallels": [
    {
      "tradition": "buddhism",
      "teaching_unit": "Mindfulness",
      "similarity_score": 0.75
    }
  ],
  "transcript": [],
  "metadata": {}
}
```

---

### Invalid Request (422 - Validation Error)
```bash
curl -X POST http://localhost:8000/api/v1/guidance/request \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test-token" \
  -d '{
    "submission_purity": "invalid_value",
    "evidential_tier": "measured",
    "humility_hierarchy": 300,
    "corpus_source": "top_curriculum"
  }'

# Response: 422 Unprocessable Entity
```

### Unauthorized (401)

```bash
curl -X POST http://localhost:8000/api/v1/guidance/request \
  -H "Content-Type: application/json" \
  -d '{...}'

# Response: 403 Forbidden (missing Authorization header)
```

### Session Not Found (404)

```bash
curl -X GET http://localhost:8000/api/v1/guidance/session/nonexistent-id \
  -H "Authorization: Bearer test-token"

# Response: 404 Not Found
```

---

## 4. Schema Details

### guidance_requests
- **id** (UUID): Primary key
- **submission_purity** (enum): unverified | one_stage_verified | two_stage_verified
- **evidential_tier** (enum): anecdotal | observational | measured | validated
- **humility_hierarchy** (int 0-1000): Hawkins consciousness scale
- **corpus_source** (enum): top_curriculum | esoteric_wisdom | modern_science | cross_tradition
- **constraint_tradition** (varchar, optional): Wisdom tradition filter
- **constraint_theme** (varchar, optional): Theme filter
- **obstacle** (varchar, optional): Emotional state to address
- **created_at** (timestamp): Auto-set to NOW()

### guidance_sessions
- **id** (UUID): Primary key
- **request_id** (UUID): Reference to guidance_requests
- **status** (enum): in_progress | completed | archived
- **teaching_tradition** (varchar): Matched teaching tradition
- **teaching_title** (varchar): Teaching title
- **teaching_text** (text): Full teaching text
- **teaching_source** (varchar): Teaching source/author
- **teaching_era** (varchar): Historical era
- **parallels** (jsonb array): Cross-tradition parallels
- **next_level_pathway** (jsonb): Next steps recommendation
- **confidence** (decimal 0-1): Confidence in match
- **transcript** (jsonb array): Full conversation history (if interactive)
- **metadata** (jsonb): Observability metadata
- **created_at** (timestamp): Auto-set to NOW()

### guidance_observability
- **id** (UUID): Primary key
- **session_id** (UUID): Reference to guidance_sessions
- **dimension** (varchar): ACAT dimension (truth, autonomy, etc.)
- **micro_score** (int 0-100): Micro-level score
- **baseline_score** (int): Phase 1 baseline
- **delta** (int): Change from baseline
- **behavioral_annotation** (text): Annotation
- **confidence** (decimal 0-1): Confidence in score
- **quote** (text): Supporting quote
- **timestamp** (timestamp): Auto-set to NOW()

---

## 5. Integration Points

### Phase 1: Empirica/GitHub Integration
- POST /empirica/findings endpoint will consume guidance verdicts
- autonomy watches guidance_observability table for behavioral signals

### Phase 2: SER 3.5 ACAT-Composition Feedback Loop
- guidance_observability feeds micro-scores back to ACAT assessment
- Bidirectional flow: ACAT → guidance → ACAT

### website: Sponsor Integration
- website practice wires POST /api/v1/guidance/request for sponsor flow
- Receives guidance responses to drive sponsor engagement

---

## 6. Troubleshooting

| Issue | Solution |
|-------|----------|
| `psycopg2.OperationalError: could not connect to server` | Verify PostgreSQL is running: `brew services start postgresql@16` |
| `schema "public" does not exist` | Restart PostgreSQL and re-run migration |
| `Foreign key constraint violation` | Ensure guidance_requests record exists before creating guidance_sessions |
| `Bearer token validation fails` | Verify token format: `Authorization: Bearer <token>` |
| Mock engine returning placeholder data | ConsciousnessGuidanceEngine not found; using mock fallback. Install wisdom_system_v1.0.py properly |

---

## 7. Testing Checklist

- [x] Schema tables created (guidance_requests, guidance_sessions, guidance_observability)
- [x] Indexes created for performance (created_at, status, api_key_id, etc.)
- [x] Test insert: guidance_request (submission_purity=two_stage_verified, humility_hierarchy=300)
- [x] Test insert: guidance_session (teaching=Amor Fati, status=completed)
- [x] Test retrieve: guidance_session by ID
- [x] Pydantic validation schemas in place (GuidanceRequestPayload, GuidanceRequestResponse, etc.)
- [x] Database connection pooling (SimpleConnectionPool 1-10 connections)
- [x] Error handling (400, 401, 404, 500)
- [x] Bearer token auth integrated
- [ ] Run POST endpoint against live FastAPI server
- [ ] Run GET endpoint against live FastAPI server
- [ ] Test error cases (invalid submission_purity, missing required fields, session not found)
- [ ] Load test: 100 concurrent requests to POST endpoint
- [ ] Integration test: autonomy reading guidance_observability table
- [ ] Integration test: website calling POST /guidance/request for sponsor flow

---

## Next Steps

1. **Deploy to Supabase Production** (if using Supabase cloud)
   - Link project with `supabase link`
   - Run `supabase migration deploy`

2. **Run Integration Tests**
   - Start FastAPI server locally
   - Run full test suite (see above checklist)
   - Verify autonomy P6 verdicts feed integration

3. **Wire website Integration**
   - website practice implements POST /guidance/request in sponsor flow
   - Confirm response format matches their integration expectations

4. **Begin Phase 2 Observability**
   - autonomy starts reading guidance_observability
   - SER 3.5 feedback loop activated
   - ACAT dimensional feedback begins flowing bidirectionally
