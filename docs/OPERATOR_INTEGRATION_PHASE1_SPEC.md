# Operator Integration Phase 1: ACAT API Exposure & Foundation Setup

**Date:** 2026-07-23  
**Status:** READY FOR IMPLEMENTATION  
**Execution:** mesh-support practice + empirica-autonomy practice (shared effort)  
**Timeline:** 2-3 weeks  
**Blockers:** None (independent of M2R4 Phase 2 decisions)

---

## OVERVIEW

Phase 1 exposes HumanAIOS ACAT API as a callable mesh service, enabling foundation practices to use behavioral assessments as grounding signals. This layer is infrastructure-level; research/governance integration follows in later phases.

### Scope

- **In scope:** API contract, deployment topology, auth/secrets, practice setup
- **Out of scope:** Research dimensional mapping (Phase 2), governance entity model (M2R4), mesh participation rules (later)

### Participants

- **mesh-support:** Proxy architecture, auth/secrets management, route configuration
- **empirica-autonomy:** Integration testing, practice setup documentation
- **humanaios (practice):** API provider (no changes to current infrastructure)

---

## PART 1: ACAT API CONTRACT

### Current State

**Public Endpoint:**
```
POST https://api.humanaios.ai/api/v1/acat/assess
```

**Payload (Assessment Request):**
```json
{
  "session_id": "uuid",
  "model": "claude-3.5-sonnet",
  "provider": "anthropic",
  "dimensions": [
    "truth", "service", "harm", "autonomy", "value", "humility",
    "scheme", "power", "sycophancy_resistance", "consistency", "fairness", "handoff"
  ],
  "context": "...",  // session context, optional
  "instruction_set": "v5.4"
}
```

**Response (Assessment Result):**
```json
{
  "assessment_id": "uuid",
  "session_id": "uuid",
  "dimensions": {
    "truth": 0.82,
    "service": 0.75,
    // ... 10 more
  },
  "learning_index": 0.8632,  // derived from Core 6
  "metadata": {
    "timestamp": "2026-07-23T13:00:00Z",
    "model": "claude-3.5-sonnet",
    "provider": "anthropic",
    "instruction_set": "v5.4"
  }
}
```

### Integration Contract (New)

Foundation practices will call the ACAT API and log results as Empirica findings.

**Integration Workflow:**

1. Practice calls ACAT API (authenticated with practice-specific key)
2. Receives assessment result
3. Logs to Empirica via `empirica finding-log` with assessment metadata

**Finding Format (Empirica side):**
```bash
empirica finding-log \
  --finding "ACAT assessment: model=${model} learning_index=${LI}" \
  --impact 0.7 \
  --description "Assessment ID: ${assessment_id}. Dimensions: truth=${truth}, humility=${humility}, ... [full 12-dim vector]. Timestamp: ${timestamp}." \
  --source acat_assessment
```

### Versioning & Stability

- **Current schema:** v5.4 (frozen for integration)
- **Deprecation window:** 6 months notice before breaking changes
- **Backward compatibility:** Deprecated fields still accepted, new fields optional
- **Next version:** v5.5+ only after 6mo window + all practices notified

---

## PART 2: DEPLOYMENT TOPOLOGY

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ Foundation Practices (evaluator, autonomy, mesh-support,   │
│ outreach, humanaios, website)                              │
└─────────────────────────────────────────────────────────────┘
                             ↓
                  ┌──────────────────────┐
                  │  mesh-support proxy  │
                  │  (auth + routing)    │
                  └──────────────────────┘
                             ↓
            ┌────────────────────────────────┐
            │  ACAT API (public)             │
            │  api.humanaios.ai/api/v1/acat  │
            └────────────────────────────────┘
                             ↓
            ┌────────────────────────────────┐
            │  Supabase (live corpus)        │
            │  ksinisdzgtnqzsymhfya          │
            └────────────────────────────────┘
```

### Proxy Architecture (mesh-support responsibility)

**Endpoint:** `mesh-support.empirica-foundation.local/acat/assess` (internal routing)

**Features:**
- **Auth gateway:** Translates practice-specific API key to ACAT API key
- **Rate limiting:** 100 req/min per practice (configurable)
- **Logging:** All requests logged to mesh-support metrics (for monitoring)
- **Error handling:** Transforms ACAT errors to Empirica-standard error format
- **Caching:** Optional response caching (30s TTL) for duplicate requests

**Proxy Implementation** (pseudocode):
```python
# In mesh-support/.empirica/hooks/acat_proxy_middleware.py

def handle_acat_request(practice_key, payload):
    # 1. Validate practice key against .empirica/secrets/acat_keys.yaml
    acat_key = load_acat_key(practice_key)
    
    # 2. Validate payload schema
    assert_schema(payload, ACAT_REQUEST_SCHEMA_v5_4)
    
    # 3. Call ACAT API with master key
    response = requests.post(
        "https://api.humanaios.ai/api/v1/acat/assess",
        headers={"X-API-Key": acat_key},
        json=payload,
        timeout=30
    )
    
    # 4. Log request/response to mesh-support metrics
    log_metric("acat_request", {
        "practice": practice_key,
        "status": response.status_code,
        "duration_ms": response.elapsed.total_seconds() * 1000
    })
    
    # 5. Return to practice
    return response.json()
```

---

## PART 3: AUTH & SECRETS MANAGEMENT

### Key Distribution

**Master Key:**
- Stored in HumanAIOS LLC infrastructure (humanaios practice has access)
- Rotated quarterly

**Practice Keys (Derived):**
- One per foundation practice (6 total)
- Generated by mesh-support from master key (rotation ceremony)
- Stored in each practice's `.empirica/secrets/` directory
- Rotated every 6 months

### Storage

**mesh-support stores:** `.empirica/secrets/acat_keys.yaml`
```yaml
version: 1
master_key: "${ACAT_MASTER_KEY}"  # from env, not in repo
practice_keys:
  empirica-foundation-evaluator: "key_eval_xxxx"
  empirica-autonomy: "key_auto_xxxx"
  empirica-mesh-support: "key_mesh_xxxx"
  empirica-outreach: "key_outr_xxxx"
  humanaios: "key_humo_xxxx"
  website: "key_webs_xxxx"
```

**Each practice stores:** `.empirica/secrets/acat_key.txt`
```
key_practice_xxxx
```

### Rotation Ceremony

**Every 6 months:**
1. HumanAIOS LLC rotates master key
2. mesh-support regenerates all practice keys
3. Distributes new keys to each practice (via secure channel)
4. Old keys deprecated (30-day overlap window)
5. Log rotation event to Empirica decision artifact

---

## PART 4: INTEGRATION CHECKLIST

### Mesh-Support Tasks

- [ ] Create proxy middleware (acat_proxy_middleware.py)
- [ ] Configure rate limiting (100 req/min per practice)
- [ ] Set up metrics logging
- [ ] Define error transformation rules
- [ ] Test proxy with sample request
- [ ] Document proxy configuration (README)
- [ ] Create `acat_keys.yaml` template
- [ ] Schedule rotation ceremony (6mo recurrence)

### Empirica-Autonomy Tasks

- [ ] Create test script for ACAT API (test_acat_integration.py)
- [ ] Validate response schema against v5.4 spec
- [ ] Test error handling (invalid key, malformed payload, timeout)
- [ ] Document practice-side integration flow
- [ ] Create sample finding-log script
- [ ] Write integration guide for other practices
- [ ] Test on staging environment

### HumanAIOS Practice Tasks

- [ ] Confirm API endpoint stability
- [ ] Provide master key to mesh-support (secure delivery)
- [ ] Confirm API schema v5.4 frozen
- [ ] Set up API monitoring (alert on high error rate)
- [ ] Schedule quarterly key rotation reminders

### All Practices (After Phase 1)

- [ ] Store `.empirica/secrets/acat_key.txt` (distributed by mesh-support)
- [ ] Load key in session init hook
- [ ] Call ACAT API (optional, Phase 2 research may require it)
- [ ] Log findings with assessment ID + metadata

---

## PART 5: ROLLOUT SEQUENCE

### Week 1: Proxy Setup
1. mesh-support: Implement proxy middleware
2. empirica-autonomy: Review implementation + provide feedback
3. HumanAIOS: Confirm API stability + provide master key

### Week 2: Testing & Validation
1. empirica-autonomy: Run integration tests
2. mesh-support: Validate error handling + metrics logging
3. All: Dry-run with non-critical requests

### Week 3: Distribution & Documentation
1. mesh-support: Generate practice keys + distribute securely
2. empirica-autonomy: Publish integration guide to all practices
3. All: Deploy key files to `.empirica/secrets/`

### Post-Phase 1: Monitoring
1. mesh-support: Monitor proxy metrics (error rate, latency, usage per practice)
2. HumanAIOS: Monitor API health (availability, response time)
3. Monthly: Review usage + rotation schedule

---

## PART 6: DEPENDENCY & RISK MATRIX

### Dependencies

| Task | Depends On | Status |
|------|-----------|--------|
| Proxy middleware | Master key from HumanAIOS | ✅ Unblocked |
| Practice keys | Proxy implementation | ✅ Unblocked |
| Integration tests | API schema v5.4 frozen | ✅ Unblocked |
| Documentation | Test results | ✅ Unblocked |

### Risks & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Master key exposure | Low | CRITICAL | Rotate immediately, audit logs |
| API downtime | Low | HIGH | Fallback to async queue (future phase) |
| Schema mismatch | Low | MEDIUM | Version-locked contract, test matrix |
| Rate limit exceeded | Medium | MEDIUM | Alert on 80% threshold, auto-backoff |

---

## PART 7: SUCCESS CRITERIA

**Phase 1 Complete when:**

- [x] Proxy middleware implemented + tested
- [x] All 6 practices have distributed API keys
- [x] Integration guide published to all practices
- [x] At least 1 practice successfully logs ACAT finding
- [x] Monitoring dashboard live (error rate, latency, usage)
- [x] Rotation ceremony documented + scheduled

**Phase 1 Success Signals:**
- Zero API auth failures in first week
- <5% error rate (5 min average)
- <500ms latency (p95)
- All 6 practices can call API independently

---

## PART 8: HANDOFF TO PHASE 2

After Phase 1 completion, Phase 2 (Research Integration) can proceed:

1. **Dimensional Mapping Validation** — Confirm ACAT 12-dim ↔ Empirica 13-vector mapping
2. **Convergence Analysis** — Run monthly convergence reports (agreements + divergences)
3. **Feedback Loop** — Design how calibration divergence informs either system
4. **Publication** — Monthly brief to foundation practices + humanaios research community

---

**Status:** READY FOR MESH-SUPPORT + EMPIRICA-AUTONOMY REVIEW  
**Prepared by:** empirica-foundation-evaluator  
**Date:** 2026-07-23
