# P6 Verdicts Integration Guide

**Status:** READY FOR PRODUCTION  
**Endpoint:** `POST /api/v1/empirica/findings`  
**Source Type:** `autonomy_p6_verdicts`  
**Integration Date:** 2026-08-14  

---

## Overview

HumanAIOS accepts ACAT Scorer v1.1 verdicts from autonomy practice via the `POST /api/v1/empirica/findings` endpoint. Verdicts are stored in both SQLite (durable) and Qdrant (semantic search) for integration into calibration baselines.

---

## Endpoint Specification

### URL
```
POST /api/v1/empirica/findings
```

### Authentication
- **Required:** Bearer token (from autonomy practice credentials)
- **Header:** `Authorization: Bearer {token}`
- **Gate:** `require_write_token()` (security.py)

### Request Payload

```json
{
  "type": "performance|security_scan|code_review|other",
  "source": "autonomy_p6_verdicts",
  "description": "ACAT assessment for item X; 18/18 pass; adversarially robust across 5 dimensions",
  "file": "assessments/p6_batch_001.json:18",
  "severity": "info|low|medium|high|critical",
  "confidence": 0.85,
  "suggested_action": null,
  "metadata": {
    "batch_id": "p6_batch_001",
    "grader_model": "claude-opus-5",
    "assessment_type": "behavioral_measurement",
    "dimensions": ["knowledge", "coherence", "signal", "impact", "alignment"],
    "pass_rate": 1.0,
    "consensus": "robust_across_substrates"
  },
  "timestamp": "2026-08-14T15:30:00Z"
}
```

### Response

```json
{
  "ok": true,
  "finding_id": "550e8400-e29b-41d4-a716-446655440000",
  "practice": "empirica-foundation.carly.humanaios",
  "stored_at": "2026-08-14T15:30:00Z"
}
```

**Response Codes:**
- `200 OK` — Verdict stored successfully
- `400 Bad Request` — Invalid payload schema
- `401 Unauthorized` — Missing or invalid authentication token
- `500 Internal Server Error` — Database or Qdrant failure

---

## Field Descriptions

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `type` | enum | Yes | Category (typically "performance" for ACAT verdicts) |
| `source` | enum | Yes | Must be "autonomy_p6_verdicts" for this integration |
| `description` | string | Yes | Verdict summary (1-1000 chars); e.g., "P6 batch assessment results" |
| `file` | string | Yes | Source reference (e.g., "assessments/p6_batch_001.json:18") |
| `severity` | enum | Yes | Severity level (info, low, medium, high, critical) |
| `confidence` | float | Yes | Confidence [0.0-1.0]; e.g., ACAT scorer confidence |
| `suggested_action` | string | No | Remediation guidance (optional) |
| `metadata` | object | No | JSONB-stored metadata (see example above) |
| `timestamp` | string | No | ISO 8601 timestamp; auto-set if omitted |

---

## Storage Architecture

### SQLite (Primary)
- **Table:** `findings`
- **Columns:**
  - `id` (UUID, primary key)
  - `type` (varchar)
  - `source` (varchar)
  - `description` (text)
  - `file` (varchar)
  - `severity` (varchar)
  - `confidence` (float)
  - `suggested_action` (text)
  - `metadata` (jsonb)
  - `timestamp` (timestamp)
  - `created_at` (timestamp)
- **Index:** `(source, timestamp)` for fast P6 batch queries
- **Retention:** Permanent (audit trail)

### Qdrant (Semantic Search)
- **Collection:** `empirica-foundation-carly-humanaios`
- **Payload:**
  - All SQLite fields + `finding_id` + `practice` identifier
  - Vector: 768-dim embedding (text: type + source + description + file)
- **Use Case:** Semantic search for related verdicts, cross-practice queries

---

## Integration Workflow

### Phase 1 (Aug 14 - Sep 14): Baseline Establishment
1. **Daily Ingest:** Autonomy sends 1-2 P6 verdict batches/week (18 items/batch)
2. **Storage:** Each verdict posted to `/empirica/findings` with source=autonomy_p6_verdicts
3. **Tracking:** HumanAIOS logs finding_id for each batch
4. **Measurement:** POSTFLIGHT logs count of P6 verdicts ingested (artifact evidence)

### Phase 1.5 (Sep 1 - Sep 14): Bridging Study
1. **Analysis:** Compare P6 verdicts (synthetic) against Phase 1 human assessments (real)
2. **Queries:** Use Qdrant to find semantically similar verdicts across sources
3. **Output:** Divergence analysis (synthetic vs real grading patterns)

### Phase 2 (Oct onwards): Production Integration
1. **Continuous Ingest:** P6 verdicts feed into continuous calibration baselines
2. **Queries:** Queries via `/empirica/findings/{finding_id}` for verdict details
3. **Future:** Query endpoint for cross-verdict correlation analysis (Oct+)

---

## Example: Sending P6 Verdicts

### Using cURL

```bash
curl -X POST https://humanaios.api/api/v1/empirica/findings \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "performance",
    "source": "autonomy_p6_verdicts",
    "description": "ACAT P6 batch 001: 18/18 pass, adversarially robust (Opus 5)",
    "file": "p6_verdicts/batch_001.json:18",
    "severity": "info",
    "confidence": 0.95,
    "metadata": {
      "batch_id": "p6_batch_001",
      "grader_model": "claude-opus-5",
      "assessment_count": 18,
      "pass_rate": 1.0,
      "dimensions": ["knowledge", "coherence", "signal", "impact", "alignment"]
    }
  }'
```

### Using Python

```python
import requests
import json

url = "https://humanaios.api/api/v1/empirica/findings"
headers = {"Authorization": f"Bearer {token}"}
payload = {
    "type": "performance",
    "source": "autonomy_p6_verdicts",
    "description": "ACAT P6 batch 001: 18/18 pass",
    "file": "p6_verdicts/batch_001.json:18",
    "severity": "info",
    "confidence": 0.95,
    "metadata": {
        "batch_id": "p6_batch_001",
        "grader_model": "claude-opus-5",
        "assessment_count": 18
    }
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()
print(f"Finding ID: {result['finding_id']}")
```

---

## Querying P6 Verdicts

### Get Single Verdict
```bash
curl -X GET https://humanaios.api/api/v1/empirica/findings/{finding_id} \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Future: Semantic Search (Phase 2+)
Qdrant collection ready for semantic queries:
```python
# Find verdicts similar to "ACAT assessments with high consensus"
results = qdrant_client.search(
    collection_name="empirica-foundation-carly-humanaios",
    query_vector=embed("ACAT assessments with high consensus"),
    limit=10,
    query_filter={"source": {"equals": "autonomy_p6_verdicts"}}
)
```

---

## Error Handling

### Common Errors

**Invalid Source Type**
```json
{
  "detail": "Invalid finding source. Allowed: github_codeql, github_trivy, copilot_suggestion, autonomy_p6_verdicts, manual, other"
}
```
**Resolution:** Verify `source` field is exactly "autonomy_p6_verdicts"

**Missing Required Field**
```json
{
  "detail": "Field 'severity' is required and must be one of: critical, high, medium, low"
}
```
**Resolution:** Ensure all required fields are present with valid enum values

**Authentication Failed**
```json
{
  "detail": "Unauthorized"
}
```
**Resolution:** Verify token is valid and not expired

---

## Monitoring & Observability

### HumanAIOS Tracking
- Each verdicts batch is logged as POSTFLIGHT artifact
- POSTFLIGHT logs: verdict count, batch ID, confidence statistics
- Artifact type: `finding` (source: autonomy_p6_verdicts)

### Example POSTFLIGHT Log
```
artifacts_logged: [
  "finding: P6 batch 001, 18 verdicts, confidence 0.95, source=autonomy_p6_verdicts"
]
```

### Health Check
```bash
curl https://humanaios.api/api/v1/acat/health
# Returns {"status": "ok", "service": "acat-api", "version": "0.1.0"}
```

---

## Support & Contact

- **Endpoint Owner:** empirica-foundation.carly.humanaios
- **Data Owner:** empirica-foundation.carly.autonomy (sends verdicts)
- **Integration Questions:** Post to empirica-foundation.carly.humanaios inbox

---

**Last Updated:** 2026-08-14  
**Next Review:** 2026-09-14 (Phase 1.5 bridging study completion)  
**Readiness:** ✓ PRODUCTION READY

