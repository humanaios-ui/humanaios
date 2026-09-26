# Phase 1 Operator Implementation Plan
## ACAT API Operator Integration for Empirica

**Version:** 1.0  
**Date:** 2026-07-25  
**Timeline:** 2 weeks (2026-07-25 → 2026-08-08)  
**Pilot Cohort:** empirica-foundation-evaluator + empirica-autonomy  
**Authority:** Admiral Carly R. Anderson  
**Status:** READY FOR EXECUTION  

---

## EXECUTIVE SUMMARY

Phase 1 makes ACAT API callable from Empirica sessions via POSTFLIGHT hook. Deliverables:
1. ✅ ACAT API reachable with per-practice API keys (auth model live)
2. ✅ Data flow: POSTFLIGHT → API call → response → finding-log (end-to-end)
3. ✅ Error handling: exponential backoff, circuit-break, resilience tested
4. ✅ Pilot verification: 10 successful assessments, <1% failure rate

**Success Gate:** 10 assessments with <1% API failure, data flows tested end-to-end  
**Next Phase:** Research integration (dimensional mapping, monthly convergence reporting)

---

## TASK BREAKDOWN & EFFORT ESTIMATES

### Week 1: Foundation (2026-07-25 → 2026-07-31)

#### Task 1.1: ACAT API Python Client Library (8 hours)
**Objective:** Empirica-side client for HumanAIOS API  
**Scope:**
- HTTP client wrapper (requests library)
- Request payload builder (P1/P3 scores, session_id, ai_system metadata)
- Response parser (learning_index, corpus_comparison, verifier_scores)
- Error classification (transient vs permanent)

**Deliverable:** `empirica/clients/humanaios_client.py`  
**Dependencies:** HumanAIOS API endpoint stable + accessible  
**Testing:** Unit tests for request/response schema matching IAD spec v5.4  
**Risk:** API endpoint not accessible → fallback to mock (for Phase 1 testing)

---

#### Task 1.2: Per-Practice API Key Management (6 hours)
**Objective:** Secure key distribution, storage, rotation  
**Scope:**
- Register 2 practices as API consumers with humanaios
- Issue 2 API keys (one per practice)
- Store in `.empirica/credentials.yaml` v2.1 (`humanaios.api_key`)
- Verify .gitignore excludes credentials.yaml
- Document key rotation procedure (quarterly, or on-demand)

**Deliverable:** 
- 2 API keys registered with humanaios
- credentials.yaml templates for both practices
- Key rotation runbook

**Dependencies:** Admiral authorization to request keys from humanaios  
**Testing:** Verify each key authenticates successfully via test API call  
**Risk:** Key leakage → include in credential rotation escalation plan

---

#### Task 1.3: POSTFLIGHT Hook Integration (10 hours)
**Objective:** Wire ACAT API call into empirica POSTFLIGHT lifecycle  
**Scope:**
- Add `--acat-flag` parameter to empirica postflight-submit (CLI)
- When `--acat-flag=true`, load ACAT payload from session vectors (P1/P3 scores)
- Call HumanAIOS API (humanaios_client from Task 1.1)
- Capture response (learning_index, corpus_comparison)
- Log finding: "ACAT Learning Index: <scores>" + corpus percentile
- Handle API errors gracefully (log, continue without ACAT signal)

**Deliverable:** 
- Modified empirica POSTFLIGHT handler
- ACAT payload marshaling code
- Error handling + logging

**Dependencies:** 
- Task 1.1 (client library)
- Task 1.2 (API keys available)

**Testing:** 
- Dry-run POSTFLIGHT with mock response
- Verify finding-log captures ACAT data correctly
- Test error paths (API timeout, 401, 503)

**Risk:** POSTFLIGHT hook runs synchronously → API latency could delay measurement. Mitigation: implement async dispatch + poll model if latency >5s observed.

---

#### Task 1.4: Error Handling & Resilience (8 hours)
**Objective:** Exponential backoff, circuit-break, monitoring  
**Scope:**
- Implement exponential backoff (2s, 4s, 8s, then halt)
- Circuit-break: after 3 failed retries, skip API call for next 15 min
- Log to empirica with `status=acat_unavailable` if circuit broken
- Alert mechanism: notify Admiral if >5 failures/hour detected
- Graceful degradation: Empirica sessions continue without ACAT signal

**Deliverable:** 
- Resilience module in humanaios_client.py
- Circuit-breaker state file (`.empirica/acat_circuit_breaker.yaml`)
- Monitoring hooks (logging + threshold alerts)

**Testing:** 
- Simulate API failures (mock 503, timeout)
- Verify backoff timing (2s, 4s, 8s)
- Verify circuit-break engages + disengages
- Verify alert fires on threshold

---

### Week 2: Integration & Verification (2026-08-01 → 2026-08-08)

#### Task 2.1: Pilot Practice Setup (4 hours)
**Objective:** Enable ACAT for empirica-foundation-evaluator + empirica-autonomy  
**Scope:**
- Load API keys into both practices' credentials.yaml
- Enable `--acat-flag=true` in default POSTFLIGHT config
- Verify both practices can reach HumanAIOS API endpoint
- Document ACAT opt-in/opt-out mechanism for future practices

**Deliverable:** 
- 2 practices operational with ACAT enabled
- Setup verification checklist

**Dependencies:** 
- Task 1.1-1.4 complete
- Admin approval to activate pilot

**Testing:** Manual API call from each practice → verify 200 OK response

---

#### Task 2.2: Data Flow End-to-End Testing (6 hours)
**Objective:** Verify complete pipeline works without manual intervention  
**Scope:**
- Run real empirica session with ACAT flag (both practices)
- PREFLIGHT → work → POSTFLIGHT with --acat-flag=true
- Verify API call fires + response captured
- Verify finding-log populated with Learning Index scores
- Verify corpus percentile/confidence intervals correct
- Test edge cases: P1-only (no P3 yet), verifier missing, malformed scores

**Deliverable:** 
- Test result report (payload, response, finding-log capture)
- Edge-case test coverage matrix

**Testing:** 
- Happy path: 1 session per practice, verify end-to-end
- Edge cases: 3-5 sessions covering P1-only, schema variations, error conditions

---

#### Task 2.3: Integration Testing (4 hours)
**Objective:** Schema validation, versioning, error scenarios  
**Scope:**
- Schema validation: request matches IAD v5.4, response matches spec
- Versioning header: ACAT-API-Version: 5.4 sent + verified
- Error scenarios: 400 (malformed), 401 (auth fail), 403 (rate limit), 503 (service down), 504 (timeout)
- Verify each error maps to correct handling (backoff vs halt vs ignore)

**Deliverable:** 
- Integration test suite (pytest)
- Error scenario playbook

**Testing:** 
- Mock API endpoint returning each error code
- Verify empirica behavior matches IAD spec

---

#### Task 2.4: 10-Assessment Verification Gate (4 hours)
**Objective:** Run 10 live assessments, verify <1% failure rate  
**Scope:**
- Coordinate with both pilot practices to run 10 POSTFLIGHT assessments with ACAT flag
- Monitor for failures (timeouts, API errors, schema mismatches)
- Compute failure rate (target: <1%, i.e., 0 failures in 10)
- Log results: session_ids, response times, any errors
- Prepare gate decision report for Admiral

**Deliverable:** 
- 10-assessment verification report
- Failure rate calculation
- Performance metrics (response times)

**Gate Criteria:**
- ✅ 10 assessments completed
- ✅ <1% failure rate (0 failures in 10)
- ✅ All learning indices computed + logged correctly
- ✅ Performance: p95 response time <500ms

---

#### Task 2.5: Documentation & Phase 2 Readiness (4 hours)
**Objective:** Document Phase 1 completion, prepare Phase 2  
**Scope:**
- Completion summary: what works, what was learned, any deviations from IAD
- Known issues: anything that didn't work as expected, workarounds applied
- Phase 2 readiness: dimensional mapping documentation, research methodology guide
- Maintenance runbook: how to rotate keys, troubleshoot API failures, monitor health

**Deliverable:** 
- Phase 1 completion report
- Known issues log
- Phase 2 readiness checklist
- Maintenance runbook

---

## DEPENDENCY GRAPH

```
Task 1.1 (API Client)
  ↓
Task 1.3 (POSTFLIGHT Hook) ← Task 1.2 (API Keys)
  ↓                           ↑
Task 1.4 (Error Handling) ←―――┘
  ↓
Task 2.1 (Pilot Setup) ← Task 1.1-1.4 all complete
  ↓
Task 2.2 (E2E Testing)
  ↓
Task 2.3 (Integration Testing)
  ↓
Task 2.4 (Verification Gate) ← success gate (10 assessments, <1% failure)
  ↓
Task 2.5 (Documentation) ← Admiral approval required
```

**Critical Path:** 1.1 → 1.3 → 1.4 → 2.1 → 2.2 → 2.4 (estimated 50 hours)  
**Parallel Tracks:** 1.2 and 1.3 can overlap after 1.1 (key management doesn't block API client)

---

## BLOCKERS & PREREQUISITES

### Must Resolve Before Task 1.1:
1. ✅ **HumanAIOS API endpoint accessible** — Needs Admiral/humanaios confirmation (endpoint URL, TLS cert)
2. ⚠️ **humanaios config bug fix** — Task from Transaction 1 audit (humanaios .empirica/config.yaml has wrong root path). Must fix before enabling humanaios practice for ACAT.

### Must Resolve Before Task 1.2:
1. **Admiral authorization** — Request API keys from humanaios for 2 practices
2. **M2R3 Phase 5 completion** — Entity registry must include humanaios practice + HumanAIOS LLC entity (currently pending). Non-blocking for Phase 1 but needed for governance completeness.

### Must Resolve Before Task 2.1:
1. **All Week 1 tasks complete** — No parallel activation
2. **Integration tests green** — Task 2.3 must pass before pilot practices enabled

---

## RISK MITIGATION

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| API endpoint not accessible | Medium | High | Mock endpoint for Phase 1 testing, swap live endpoint when ready |
| Schema version drift (v5.4 vs v5.5) | Low | Medium | Frozen versions (v5.4) until 2026-12, 60-day deprecation notice |
| API latency >5s blocking POSTFLIGHT | Low | High | Implement async dispatch + polling if observed; continue without ACAT signal |
| Auth failure (API key invalid/expired) | Low | Medium | Test key rotation monthly, escalate to Admiral on 403 |
| Circuit-break triggers too aggressively | Medium | Low | Start with 3-retry threshold, monitor for tuning needs |
| humanaios config bug prevents practice use | High | High | Fix in parallel with Task 1.1; must complete before Task 2.1 |

---

## SUCCESS CRITERIA CHECKLIST

**Phase 1 Gate (Required for Admiral Approval):**
- [ ] 10 assessments completed with <1% failure rate (0 failures)
- [ ] Data flows end-to-end without manual intervention
- [ ] Auth model tested (key distribution, rotation, revocation)
- [ ] Error handling tested (backoff, circuit-break, logging)
- [ ] Documentation complete for Phase 2 pilots
- [ ] Known issues logged + workarounds documented

**Performance Criteria:**
- [ ] API response time: p95 <500ms
- [ ] Data flow latency: POSTFLIGHT hook <2s overhead (measured)
- [ ] Success rate: >99% (0 failures in 10 assessments)

**Governance Criteria:**
- [ ] API keys rotated without downtime
- [ ] Credentials never logged or committed
- [ ] Alert mechanism tested (Admiral notified on >5 failures/hour)

---

## TIMELINE SUMMARY

| Phase | Week | Dates | Tasks | Hours | Deliverable |
|-------|------|-------|-------|-------|------------|
| **Week 1: Foundation** | W1 | Jul 25-31 | 1.1-1.4 | 32 | Client, keys, hook, resilience |
| **Week 2: Integration** | W2 | Aug 1-8 | 2.1-2.5 | 22 | Setup, E2E, testing, gate, docs |
| **Total** | | | | **54 hours** | **Phase 1 Complete** |

**Resource Estimate:** 1 full-time engineer (7 days) + Admiral oversight (2-3 hours for approvals/escalations)

---

## NEXT STEPS

**Immediate (Before Task 1.1):**
1. Admiral confirms HumanAIOS API endpoint accessible (URL, TLS cert)
2. Fix humanaios config bug (part of Transaction 1 findings)
3. Request API keys for 2 practices from humanaios

**After Phase 1 Gate Passes:**
1. Admiral reviews gate report + approves Phase 2 advancement
2. Prepare Phase 2 work: dimensional mapping, convergence report template, research methodology
3. Expand pilot cohort: add empirica-mesh-support (3 practices total)

---

## APPENDIX: Task Task Assignments (Suggested)

- **1.1-1.4, 2.3:** Core engineer (Python/empirica expertise)
- **2.1:** DevOps/infra (credential management, monitoring)
- **2.2, 2.4:** QA/test engineer (verification, gate reporting)
- **2.5:** Technical writer + core engineer (documentation, runbook)
- **Overall:** Admiral oversight (approvals, escalation decisions)

---

**Document Status:** READY FOR EXECUTION  
**Phase 1 Start Date:** 2026-07-25 (immediately upon Admiral approval)  
**Estimated Completion:** 2026-08-08 (assuming no blockers)

---

*Approved by:* [Pending Admiral signature]  
*Last Updated:* 2026-07-25
