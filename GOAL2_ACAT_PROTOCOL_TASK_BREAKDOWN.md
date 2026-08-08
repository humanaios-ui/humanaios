# Goal 2: ACAT Protocol Service — Task Breakdown

**Goal ID:** 699438a3-ca32-488f-a1a7-fb01340b2d52  
**Objective:** Build repeatable ACAT assessment workflow as first-class API service  
**Status:** Ready for Task Creation  
**Estimated Duration:** 2 weeks (2 engineers)

---

## Codebase State Verification

### ✅ Confirmed Ready
- Auth Module: JWT + Passport (production pattern)
- Database Module: PostgreSQL connection pooling, 20 max connections
- AgentsService: CRUD + activity tracking pattern established
- Schema: UUID primary keys, JSONB metadata, proper indexing
- M2R2 State Tables: Collaborations, Projects, state_audit_log with full traceability

### ⚠️ Needs Adding (This Goal)
1. **Assessments table** — Store assessment submissions + results
2. **ACAT Protocol table** — Track protocol steps (evaluation, expert review, reporting)
3. **Epistemic artifacts table** — Store findings, vectors, decisions, assumptions
4. **Assessment Status & Results** — Async job tracking (pending/in_progress/completed/failed)

---

## Task Breakdown (8 tasks total)

### Task 1: Database Schema Extension
**Objective:** Add assessment + epistemic artifact tables to Supabase

**Deliverables:**
- `assessments` table: id, org_id, system_id (UUID), system_info (JSONB), status, created_at, updated_at
- `acat_protocol_runs` table: id, assessment_id, step (enum), step_data (JSONB), duration_ms, created_at
- `epistemic_artifacts` table: id, assessment_id, type (enum: finding/decision/assumption/unknown/deadend), data (JSONB), confidence (0-1), created_at
- Indexes on org_id, status, created_at for query performance

**Success Criteria:**
- Schema migration created (Alembic)
- Tables indexed correctly (no N+1 queries)
- Foreign key constraints enforced
- Timezone handling correct (all timestamps UTC)

**Effort:** 2-4 hours  
**Owner:** Backend engineer

**Code Location:**
```
alembic/versions/002_acat_protocol_tables.py  (migration)
apps/api/src/database/acat.schema.ts           (TypeScript types)
```

---

### Task 2: ACAT Methodology Service
**Objective:** Implement standardized 50-step ACAT evaluation protocol

**Deliverables:**
- ACATService class with protocol orchestration
- 50-step evaluation sequence (from arXiv 2503.09618)
- Step handlers: info_collection → evaluation → calibration → expert_review → reporting
- Each step produces structured findings (what was measured)
- Parallelizable: multiple assessments can run concurrently

**Success Criteria:**
- Protocol deterministic (same input = same output)
- All 50 steps implemented
- Results reproducible within 0.01% tolerance
- Unit tests for each step (100% coverage)
- Load-tested: 50 concurrent assessments, <1s per step

**Effort:** 4-5 days  
**Owner:** Backend engineer

**Code Location:**
```
apps/api/src/acat/acat.service.ts
apps/api/src/acat/acat.steps.ts              (step handlers)
tests/unit/acat.service.spec.ts
```

**Dependencies:** Task 1 (schema)

---

### Task 3: Assessment Submission API (Async Job Pattern)
**Objective:** Build `POST /api/v1/assessments` endpoint with polling

**Deliverables:**
- AssessmentsController: POST endpoint for submitting AI system
- AssessmentsService: async job management (enqueue, poll, retrieve results)
- Response format: `{ job_id, status, poll_url }`
- Job states: pending → running → completed / failed
- Redis queue for job orchestration (optional, but recommended for concurrency)

**Success Criteria:**
- API contract defined (OpenAPI spec)
- Validation: AI system info required fields checked
- Rate limiting: 100 assessments/hour per org
- Error handling: validation errors, queue full, timeout scenarios
- Unit tests: happy path + error cases
- Load test: 1000 concurrent requests, <500ms P99 latency

**Effort:** 3-4 days  
**Owner:** Backend engineer

**Code Location:**
```
apps/api/src/assessments/assessments.controller.ts
apps/api/src/assessments/assessments.service.ts
apps/api/src/assessments/assessments.module.ts
tests/unit/assessments.spec.ts
tests/e2e/assessments.e2e.spec.ts
```

**Dependencies:** Task 1 (schema), Task 2 (ACAT service)

---

### Task 4: Epistemic Artifact Logging (Integration)
**Objective:** Automatic artifact logging during ACAT execution

**Deliverables:**
- EpistemicLogger service: logs findings/decisions/assumptions to DB
- Each ACAT step produces a finding (what was measured)
- Calibration step produces vectors (know, do, context, etc.)
- Expert review step produces decision (expert's judgment)
- Automatic tagging: assessment_id, step_number, timestamp
- Audit trail: who (API key), what (finding), when (timestamp)

**Success Criteria:**
- Every ACAT step produces ≥1 epistemic artifact
- Artifacts linked to assessment (traceability)
- Confidence levels assigned automatically
- Query performance: retrieve assessment artifacts in <100ms
- Integration test: end-to-end assessment produces correct artifacts

**Effort:** 2-3 days  
**Owner:** Backend engineer (same as Task 2)

**Code Location:**
```
apps/api/src/epistemic/epistemic-logger.service.ts
apps/api/src/epistemic/epistemic.module.ts
tests/integration/epistemic-logging.spec.ts
```

**Dependencies:** Task 1 (schema), Task 2 (ACAT)

---

### Task 5: Poll Endpoint & Result Retrieval
**Objective:** Build `GET /api/v1/assessments/{job_id}` endpoint

**Deliverables:**
- GET endpoint: return job status + progress
- Completed assessments: return full results (calibration vectors, findings, expert notes)
- Format: `{ status, progress_pct, completed_at, result: { vectors, findings, recommendations } }`
- WebSocket optional: real-time status updates (can defer to Goal 5)

**Success Criteria:**
- Status updates accurate (within 1s of actual completion)
- Results include all epistemic artifacts
- Security: user can only see own org's assessments
- Performance: <100ms query time
- Unit + E2E tests

**Effort:** 1-2 days  
**Owner:** Backend engineer

**Code Location:**
```
apps/api/src/assessments/assessments.controller.ts (GET handler)
tests/e2e/assessments.polling.spec.ts
```

**Dependencies:** Task 1, 2, 3

---

### Task 6: Error Handling & Resilience
**Objective:** Production-grade error handling + recovery

**Deliverables:**
- Timeout handling: if ACAT step takes >5min, log as error + graceful abort
- Retry logic: failed assessments retry once (once)
- Error logging: structured logs with job_id, step, error message
- Database failover: graceful degradation if DB connection lost
- Dead letter queue: assessments that fail after retry moved to manual review

**Success Criteria:**
- All error paths tested
- No silent failures (every error logged)
- Error messages helpful (no stack traces to customers)
- Retry logic tested with simulated failures
- Timeout test: forced timeout → graceful abort

**Effort:** 1-2 days  
**Owner:** Backend engineer

**Code Location:**
```
apps/api/src/assessments/assessments-error-handler.ts
tests/integration/error-scenarios.spec.ts
```

**Dependencies:** Task 3

---

### Task 7: Integration Tests (Assessment Pipeline)
**Objective:** End-to-end testing of full assessment workflow

**Deliverables:**
- E2E test: submit assessment → ACAT executes → results retrieved
- Test data: 5 diverse AI systems (GPT variants, Claude, open-source)
- Assertions: results reproducible, artifacts logged correctly, latency acceptable
- Performance assertions: P99 latency <5s total (submit + execute + retrieve)

**Success Criteria:**
- All 5 test assessments complete successfully
- Results reproducible (run twice, get <0.01% difference)
- Artifacts logged: ≥20 per assessment
- No data corruption in results
- Latency targets met

**Effort:** 1-2 days  
**Owner:** QA / Backend engineer

**Code Location:**
```
tests/integration/acat-pipeline.spec.ts
tests/fixtures/test-ai-systems.json
```

**Dependencies:** Task 1-6

---

### Task 8: Documentation & API Contract
**Objective:** OpenAPI spec + architecture decisions logged

**Deliverables:**
- OpenAPI 3.0 spec: `/api/v1/assessments` endpoints documented
- Request/response examples
- Architecture decisions logged: why async job pattern, why Redis queue, etc.
- Runbook: how to debug a failing assessment
- Integration guide: how to add new ACAT steps

**Success Criteria:**
- OpenAPI spec valid (validates against 3.0 schema)
- All decisions logged as findings/decisions in epistemic system
- Runbook tested (team can follow it to debug)

**Effort:** 1 day  
**Owner:** Backend engineer / Documentation

**Code Location:**
```
docs/api/assessments.openapi.yaml
docs/architecture/acat-async-pattern.md
docs/runbooks/debug-assessment-failure.md
```

**Dependencies:** All prior tasks

---

## Transaction Sequencing

**Serial Path (Must complete in order):**
1. Task 1 (Schema) → Foundation
2. Task 2 (ACAT Service) → Core logic
3. Task 3 (Submission API) → Customer interface
4. Task 4 (Epistemic Logging) → Traceability
5. Task 5 (Poll Endpoint) → Result retrieval

**Parallel Path (Can overlap with serial):**
- Task 6 (Error Handling) — Start after Task 3, don't block
- Task 7 (Integration Tests) — Start after Task 5, run continuously
- Task 8 (Documentation) — Start after Task 2, update as code completes

**Recommended Execution:**
```
Week 1:
  Day 1-2: Task 1 (Schema)
  Day 2-4: Task 2 (ACAT Service) + Task 6 (Error Handling start)
  Day 5: Task 3 (Submission API)

Week 2:
  Day 1: Task 4 (Epistemic Logging)
  Day 2: Task 5 (Poll Endpoint)
  Day 3-4: Task 7 (Integration Tests, concurrent with Task 8)
  Day 5: Task 8 (Documentation, finalization)
```

---

## Epistemic Discipline for Goal 2

### Every Task Closes With Artifacts

**Task 1 (Schema):**
- `finding-log`: "Confirmed TimescaleDB extension available, indexes optimal for query patterns"
- `decision-log`: "Chose JSONB for protocol_data vs separate tables — why: flexibility for step variations"
- `assumption-log`: "Assuming < 10M assessments in Year 1" (confidence: 0.7)

**Task 2 (ACAT Service):**
- `finding-log`: "ACAT protocol steps 1-50 implemented, step execution time distribution logged"
- `decision-log`: "Chosen parallelization model: steps 1-20 sequential (dependency chain), steps 21-50 parallelizable"
- `deadend-log`: "Tried simple queue for concurrency, N+1 query problem emerged, switched to batch processing"

**Task 3 (Submission API):**
- `finding-log`: "Rate limit: 100 assessments/hour handles enterprise load (conservative estimate)"
- `decision-log`: "Chose async job pattern over sync (3+ min ACAT execution time)"
- `assumption-log`: "Assuming 1000 concurrent API requests during peak" (confidence: 0.5)

...and so on for each task.

---

## Success Metrics (Before moving to Goal 3)

| Metric | Target | Verification |
|--------|--------|--------------|
| All 8 Tasks Completed | ✅ | Task completion checklist |
| ACAT Protocol Deterministic | ✅ | Run same assessment 3x, get identical results |
| Reproducibility | <0.01% difference | Comparison test |
| API Load Test | 1000 concurrent, P99 <500ms | k6 load test results |
| Integration Test | 0 failures on 5 AI systems | E2E test suite passing |
| Artifact Logging | ≥20 per assessment | Audit trail verified |
| Error Handling | 0 silent failures | Error scenario tests pass |
| Documentation | All decisions logged | Epistemic artifact review |

---

## Notes for Engineers

1. **Incremental Testing:** Test each task independently before moving to the next. Don't wait until the end.
2. **Epistemic Logging:** Log findings/decisions as you go, not at the end. This is non-negotiable — it's how we maintain discipline.
3. **Load Testing:** Start load testing after Task 5 completes. Don't wait for Task 7.
4. **Code Review:** Every task needs 2-person review before close. Check for: type safety, error handling, test coverage >90%.
5. **No Shortcuts:** If a task feels "almost done" but has unknowns, log them. Don't hide them.

---

**Ready to begin. Which task should we start with: Task 1 (Schema) or Task 2 (ACAT Service)?**
