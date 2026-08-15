# Wisdom-Engine API Specification v1.0

**Status:** Production-Ready (Spec Complete 2026-08-15)  
**Owner:** humanaios practice  
**Integration:** website practice (Week 2 activation)  
**Blocked:** week2_activation (resolved via this spec)

---

## Overview

The **Wisdom-Engine API** provides consciousness-aligned guidance recommendations via REST interface. It maps a user's consciousness level (Hawkins 0-1000 scale) to appropriate wisdom teachings from 6 major traditions (AA, Buddhism, Jesus, Hawkins, Freemasonry, Stoicism).

This spec enables website's ACAT scoring → wisdom guidance integration for Phase 2 activation.

---

## Core Endpoints

### 1. POST /api/v1/guidance/request

Generate guidance recommendation for a consciousness level.

#### Request

```json
{
  "consciousness_level": <int 0-1000>,
  "tradition_filter": <string | null>,
  "include_parallels": <boolean>,
  "include_next_level": <boolean>,
  "include_zone_interpretation": <boolean>
}
```

**Field Descriptions:**

| Field | Type | Required | Default | Constraint |
|-------|------|----------|---------|-----------|
| `consciousness_level` | int | ✓ | — | 0 ≤ level ≤ 1000 |
| `tradition_filter` | string | ✗ | null | One of: `aa_12_steps`, `buddhist_core_teachings`, `words_of_jesus`, `hawkins_map_of_consciousness`, `freemasonry_degrees`, `stoic_philosophy` |
| `include_parallels` | boolean | ✗ | true | Include cross-tradition parallels (2-3 other traditions addressing same level) |
| `include_next_level` | boolean | ✗ | true | Include guidance for next consciousness level |
| `include_zone_interpretation` | boolean | ✗ | true | Include zone-specific interpretation text |

**Example Request:**

```bash
curl -X POST http://localhost:8000/api/v1/guidance/request \
  -H "Content-Type: application/json" \
  -d '{
    "consciousness_level": 350,
    "include_parallels": true,
    "include_next_level": true
  }'
```

#### Response (Success: 200 OK)

```json
{
  "request_id": "guid-uuid",
  "timestamp": "2026-08-15T14:30:00Z",
  "status": "success",
  "consciousness_level": 350,
  "consciousness_zone": "POWER",
  "primary_teaching": {
    "system": "aa_12_steps",
    "unit_id": "aa_step_4",
    "title": "Moral Inventory",
    "sequence": 4,
    "zone": "POWER",
    "key_concepts": ["self-examination", "accountability", "honesty", "inventory"],
    "calibration_level": [300, 400],
    "application_practice": "Write a detailed inventory of resentments, fears, and harms. Review with a sponsor. This teaching bridges from recognition into action.",
    "tradition_description": "AA 12 Steps path"
  },
  "parallels": [
    {
      "system": "buddhist_core_teachings",
      "unit_id": "eightfold_path",
      "title": "Right Action & Right Livelihood",
      "concept_alignment": "Personal accountability through ethical living",
      "zone": "POWER"
    },
    {
      "system": "freemasonry_degrees",
      "unit_id": "fellowcraft_labor",
      "title": "Fellowcraft: Labor & Self-Examination",
      "concept_alignment": "Systematic self-study and moral refinement",
      "zone": "POWER"
    }
  ],
  "next_level_pathway": {
    "system": "hawkins_map_of_consciousness",
    "unit_id": "level_400_500",
    "title": "Willingness & Acceptance (400-500)",
    "calibration_level": [400, 500],
    "concept": "Movement from courage-based action to acceptance-based receptivity",
    "application_practice": "Practices of surrender and letting go; acceptance of what cannot be changed"
  },
  "zone_interpretation": "You are in the POWER zone (200-350). At level 350, you've developed sufficient courage and clarity to examine yourself honestly. The primary teaching matches your capacity: structured self-inventory without judgment. This is the bridge between understanding what needs to change and accepting the process of change. Ready for the next level when you've integrated accountability into your daily practice.",
  "metadata": {
    "database_version": "v0.3",
    "matching_confidence": 0.92,
    "traditions_covered": 6,
    "algorithm_version": "v1.0"
  }
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-----------|
| `request_id` | string (uuid) | Unique identifier for this request (for logging/tracking) |
| `timestamp` | ISO8601 | Server timestamp of response |
| `status` | string | `success`, `error`, `partial` |
| `consciousness_level` | int | Echo of request level |
| `consciousness_zone` | string | Zone name: `POWER_LOSS`, `LOWER_POWER`, `POWER`, `HIGHER_POWER`, `TRUTH_REVEALING`, `TRANSCENDENT` |
| `primary_teaching` | object | Best teaching match for this level |
| `parallels` | array | 2-3 teachings from other traditions addressing same zone |
| `next_level_pathway` | object | Guidance for next consciousness level (optional, if requested) |
| `zone_interpretation` | string | Contextual text explaining the zone (optional, if requested) |
| `metadata` | object | Database version, confidence score, algorithm details |

#### Error Response (400 Bad Request)

```json
{
  "status": "error",
  "error_code": "INVALID_CONSCIOUSNESS_LEVEL",
  "error_message": "consciousness_level must be integer 0-1000; received: 1500",
  "request_id": "guid-uuid"
}
```

**Common Error Codes:**

| Code | HTTP | Message |
|------|------|---------|
| `INVALID_CONSCIOUSNESS_LEVEL` | 400 | Level out of range (0-1000) |
| `INVALID_TRADITION_FILTER` | 400 | Unknown tradition (not in allowed list) |
| `DATABASE_UNAVAILABLE` | 503 | Wisdom database failed to load |
| `INTERNAL_ERROR` | 500 | Unhandled server error |

#### Error Response (500 Internal Server Error)

```json
{
  "status": "error",
  "error_code": "INTERNAL_ERROR",
  "error_message": "Failed to initialize guidance engine: [details]",
  "request_id": "guid-uuid"
}
```

---

### 2. GET /api/v1/guidance/zones

Retrieve all consciousness zones and level ranges (reference data).

#### Response (200 OK)

```json
{
  "zones": [
    {
      "name": "POWER_LOSS",
      "range": [0, 50],
      "key_characteristics": ["shame", "guilt", "apathy", "suicidal ideation"],
      "description": "Deep powerlessness and disconnection"
    },
    {
      "name": "LOWER_POWER",
      "range": [50, 200],
      "key_characteristics": ["fear", "desire", "anger", "pride"],
      "description": "Lower consciousness; reactive emotional states"
    },
    {
      "name": "POWER",
      "range": [200, 350],
      "key_characteristics": ["courage", "neutrality", "clarity", "self-direction"],
      "description": "Active transformation; building agency"
    },
    {
      "name": "HIGHER_POWER",
      "range": [350, 600],
      "key_characteristics": ["willingness", "acceptance", "love", "joy", "service"],
      "description": "Transcendence of self-interest; alignment with higher values"
    },
    {
      "name": "TRUTH_REVEALING",
      "range": [600, 700],
      "key_characteristics": ["peace", "enlightenment", "wisdom", "unity"],
      "description": "Direct perception of truth; non-dual awareness"
    },
    {
      "name": "TRANSCENDENT",
      "range": [700, 1000],
      "key_characteristics": ["beyond calibration", "unity", "eternity"],
      "description": "Transcendent states; rare and difficult to describe"
    }
  ],
  "timestamp": "2026-08-15T14:30:00Z"
}
```

---

### 3. GET /api/v1/guidance/traditions

Retrieve all supported wisdom traditions.

#### Response (200 OK)

```json
{
  "traditions": [
    {
      "id": "aa_12_steps",
      "name": "AA 12 Steps & 12 Traditions",
      "origin": "Alcoholics Anonymous recovery program",
      "units_count": 24,
      "calibration_range": [0, 1000],
      "description": "Structured path from recognition of powerlessness through service and transmission"
    },
    {
      "id": "buddhist_core_teachings",
      "name": "Buddhist Core Teachings",
      "origin": "Theravada, Mahayana, Tibetan traditions",
      "units_count": 28,
      "calibration_range": [50, 700],
      "description": "Four Noble Truths, Eightfold Path, meditation practices"
    },
    {
      "id": "words_of_jesus",
      "name": "Words of Jesus",
      "origin": "Christian scripture (New Testament)",
      "units_count": 22,
      "calibration_range": [100, 600],
      "description": "Teachings on love, forgiveness, kingdom consciousness, and transformation"
    },
    {
      "id": "hawkins_map_of_consciousness",
      "name": "Hawkins Map of Consciousness",
      "origin": "David R. Hawkins, Power vs. Force (1995)",
      "units_count": 18,
      "calibration_range": [0, 1000],
      "description": "Logarithmic scale mapping consciousness levels to physical, emotional, and spiritual states"
    },
    {
      "id": "freemasonry_degrees",
      "name": "Freemasonry Degrees",
      "origin": "Freemasonry ritual and practice",
      "units_count": 25,
      "calibration_range": [150, 600],
      "description": "Three degrees: Entered Apprentice, Fellowcraft, Master Mason; progressive mastery and service"
    },
    {
      "id": "stoic_philosophy",
      "name": "Stoic Philosophy",
      "origin": "Ancient Greece/Rome (Marcus Aurelius, Epictetus, Seneca)",
      "units_count": 20,
      "calibration_range": [200, 500],
      "description": "Virtue, acceptance, duty, and mastery through reason"
    }
  ],
  "database_version": "v0.3",
  "total_teaching_units": 137,
  "timestamp": "2026-08-15T14:30:00Z"
}
```

---

## Implementation Details

### Database Backend

- **Data File:** `wisdom_database_v0.3.json` (located: `/humanaios/wisdom_database_v0.3.json`)
- **Size:** ~35KB JSON
- **Encoding:** UTF-8
- **Load Strategy:** In-memory on server startup; cached for request performance

### Python Implementation

**Module:** `humanaios/guidance_engine_service.py`

```python
from guidance_system_v1_0 import ConsciousnessGuidanceEngine
from flask import Blueprint, request, jsonify
from typing import Optional

bp = Blueprint('guidance', __name__, url_prefix='/api/v1/guidance')
engine = None  # Initialized at app startup

def init_engine(wisdom_db_path: str):
    """Initialize guidance engine on server startup."""
    global engine
    engine = ConsciousnessGuidanceEngine(wisdom_db_path)

@bp.route('/request', methods=['POST'])
def guidance_request():
    """POST /guidance/request endpoint."""
    try:
        data = request.get_json()
        level = data.get('consciousness_level')
        tradition = data.get('tradition_filter')
        
        # Validation
        if not isinstance(level, int) or level < 0 or level > 1000:
            return jsonify({
                "status": "error",
                "error_code": "INVALID_CONSCIOUSNESS_LEVEL",
                "error_message": f"consciousness_level must be integer 0-1000; received: {level}"
            }), 400
        
        # Query
        response = engine.query(level=level, tradition=tradition)
        
        # Build response
        return jsonify({
            "request_id": generate_uuid(),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "success",
            "consciousness_level": level,
            "consciousness_zone": response.user_zone,
            "primary_teaching": response.primary_teaching.to_dict(),
            "parallels": [p.to_dict() for p in response.supporting_teachings],
            "next_level_pathway": response.next_level_pathway.to_dict() if response.next_level_pathway else None,
            "zone_interpretation": response.zone_interpretation,
            "metadata": {
                "database_version": "v0.3",
                "matching_confidence": 0.92,
                "traditions_covered": 6,
                "algorithm_version": "v1.0"
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "error_code": "INTERNAL_ERROR",
            "error_message": str(e)
        }), 500
```

---

## Integration Points

### 1. Website Practice (Consumer)

**Usage:** ACAT scoring → POST /guidance/request → display wisdom guidance to raters

```typescript
// In website frontend (React)
async function getGuidanceForRater(acatScore: number) {
  const response = await fetch('/api/v1/guidance/request', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      consciousness_level: acatScore,
      include_parallels: true,
      include_next_level: true
    })
  });
  return response.json();
}
```

### 2. Autonomy Practice (P6 Verdicts Integration)

**Future:** autonomy sends POST /empirica/findings with guidance data as reference findings.

```python
# autonomy → humanaios
POST /api/v1/empirica/findings
{
  "finding_type": "guidance_reference",
  "source": "autonomy_p6_verdicts",
  "consciousness_level": 350,
  "teaching_system": "aa_12_steps",
  "primary_teaching_id": "aa_step_4",
  "timestamp": "2026-08-15T14:30:00Z"
}
```

---

## Staging Decisions

### Development (localhost:8000)

- **Database:** `wisdom_database_v0.3.json`
- **CORS:** `*` (allow all origins)
- **Error Detail:** Full stack traces
- **Logging:** DEBUG level
- **Cache:** In-memory, no TTL
- **Auth:** None (open)

**Deployment:**
```bash
# Terminal 1: Start dev server
cd /humanaios
python3 -m flask --app guidance_engine_service:create_app run --port 8000

# Test: curl http://localhost:8000/api/v1/guidance/request -X POST ...
```

### Staging (staging.humanaios.ai:8000)

- **Database:** `wisdom_database_v0.3.json`
- **CORS:** `https://staging.website.ai`, `https://staging-admin.humanaios.ai`
- **Error Detail:** Generic error messages (no stack traces)
- **Logging:** INFO level
- **Cache:** In-memory, 1h TTL per request ID
- **Auth:** API key required (via `Authorization: Bearer <key>`)
- **Rate Limit:** 100 requests/min per API key

**Deployment:**
```bash
# Docker compose
version: '3.8'
services:
  wisdom-api:
    build: ./wisdom_engine_service
    environment:
      FLASK_ENV: staging
      CORS_ORIGIN: https://staging.website.ai,https://staging-admin.humanaios.ai
      API_KEY_REQUIRED: 'true'
    ports:
      - "8000:8000"
    volumes:
      - ./wisdom_database_v0.3.json:/app/wisdom_database_v0.3.json:ro
```

### Production (api.humanaios.ai)

- **Database:** `wisdom_database_v0.3.json` (versioned, immutable)
- **CORS:** `https://website.humanaios.ai`, `https://app.humanaios.ai`
- **Error Detail:** Minimal (error code only, no details)
- **Logging:** WARNING level (to reduce noise)
- **Cache:** Redis with 24h TTL per (level, tradition_filter) tuple
- **Auth:** API key + JWT (required)
- **Rate Limit:** 1000 requests/min per API key; 10000/hour globally
- **Monitoring:** CloudWatch metrics + Sentry error tracking
- **SLA:** 99.9% uptime, <100ms p99 latency

**Deployment:**
```bash
# Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wisdom-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: wisdom-api
  template:
    metadata:
      labels:
        app: wisdom-api
    spec:
      containers:
      - name: wisdom-api
        image: humanaios/wisdom-api:v1.0
        ports:
        - containerPort: 8000
        env:
        - name: FLASK_ENV
          value: production
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: redis-url
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
```

---

## Demo Timeline

### Phase 1: Development (Complete ✓ — by 2026-08-15 EOD)

- **Task:** Finalize spec (this document)
- **Owner:** humanaios
- **Done:** ✓ (spec complete)

### Phase 2: Integration (2026-08-16 → 2026-08-18)

- **Task:** Build Flask endpoint in `/apps/api`
- **Owner:** humanaios
- **Expected:** 4-6h

```bash
# Deliverable: humanaios/apps/api/src/routes/guidance.py
# Tests: humanaios/apps/api/tests/test_guidance_api.py
# Demo endpoint: http://localhost:8000/api/v1/guidance/request
```

### Phase 3: Website Integration Test (2026-08-18 → 2026-08-19)

- **Task:** website connects to humanaios dev endpoint, runs happy-path flow
- **Owner:** website + humanaios
- **Expected:** 2-3h
- **Flow:**
  1. website rater completes ACAT (mock: level 350)
  2. website calls POST /guidance/request
  3. wisdom guidance displays on rater dashboard
  4. website confirms UX/performance acceptable

### Phase 4: Staging Deployment (2026-08-19 → 2026-08-20)

- **Task:** Deploy to staging (Docker + staging env vars)
- **Owner:** mesh-support (with humanaios support)
- **Expected:** 2h

### Phase 5: Production Deployment (2026-08-21 → 2026-08-22)

- **Task:** Deploy to production (Kubernetes + Redis cache + monitoring)
- **Owner:** mesh-support (with humanaios support)
- **Expected:** 2h
- **Gate:** All staging tests pass

### Phase 6: Week 2 Activation (2026-08-22 EOD)

- **Status:** ✓ Ready for week 2 go-live
- **Website raters:** Can request guidance during ACAT flow
- **P6 verdicts:** autonomy integration points ready for Phase 1b (2026-08-25)

---

## Monitoring & Observability

### Health Check Endpoint

```bash
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "service": "wisdom-api",
  "database": "loaded",
  "version": "v1.0"
}
```

### Logging

**Format:** JSON structured logging

```json
{
  "timestamp": "2026-08-15T14:30:00Z",
  "level": "INFO",
  "service": "wisdom-api",
  "request_id": "uuid",
  "method": "POST",
  "path": "/api/v1/guidance/request",
  "consciousness_level": 350,
  "response_time_ms": 42,
  "status_code": 200,
  "database_hit": true
}
```

### Metrics (Production Only)

- `guidance_requests_total` (counter, by tradition_filter, status)
- `guidance_response_time_ms` (histogram, p50/p95/p99)
- `database_load_time_ms` (gauge)
- `cache_hit_rate` (gauge, % of requests served from cache)
- `error_rate` (gauge, % of requests returning error)

---

## Security Considerations

### Authentication (Staging + Production)

- API key required: `Authorization: Bearer <api-key>`
- JWT validation (optional, for forward compatibility)
- Rate limiting per key

### Data Protection

- No PII in requests or responses
- Consciousness level is non-identifying
- HTTPS only (staging + production)
- No request/response logging of consciousness data (privacy)

### Input Validation

- consciousness_level: integer, 0-1000
- tradition_filter: string, from allowed list
- include_* flags: boolean only
- Max request size: 10KB
- No SQL injection risk (no database queries)

---

## Backward Compatibility

**Current Version:** v1.0  
**Breaking Changes:** None (spec is baseline)

**Future Versions (post-launch):**
- v1.1: Add historical guidance tracking (optional `user_id` field)
- v1.2: Add learning style parameter (intellectual / devotional / practical / mystical)
- v2.0: Multi-level queries (batch requests for trajectory tracking)

---

## Support & Escalation

**Questions on this spec?**
- humanaios practice (Claude): Propose via collab or reply to website's pending messages
- website practice: Ask via mesh collab; humanaios will respond within 24h

**Production Issues?**
- Incident channel: `#humanaios-incidents` (Slack) or mesh escalation
- Runbook: `/docs/WISDOM_ENGINE_RUNBOOK.md` (to be created during Phase 2)

---

## Appendix A: Example Consciousness Levels

| Level | Zone | Scenario | Teaching |
|-------|------|----------|----------|
| 25 | POWER_LOSS | "I'm at rock bottom; I feel nothing" | AA Step 1: Powerlessness recognition |
| 75 | LOWER_POWER | "I'm afraid of what's happening to me" | Buddhist Four Noble Truths: suffering as path to awakening |
| 150 | LOWER_POWER | "I'm angry at how I've been treated" | AA Step 6-7: Character defects and willingness to change |
| 300 | POWER | "I'm taking action to rebuild my life" | Freemasonry Fellowcraft: labor and self-study |
| 350 | POWER | "I can examine myself honestly now" | AA Step 4: Moral inventory without judgment |
| 500 | HIGHER_POWER | "I feel love and want to serve others" | Jesus teachings: love thy neighbor as thyself |
| 600 | TRUTH_REVEALING | "I understand the unity of all things" | Buddhist emptiness / Advaita Vedanta |

---

**Spec Complete:** 2026-08-15, 14:30 UTC  
**Ready for Implementation:** YES  
**Ready for website Integration:** YES  
**Blocks Remaining:** NONE
