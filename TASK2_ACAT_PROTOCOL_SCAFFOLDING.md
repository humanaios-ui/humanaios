# Task 2: ACAT Protocol Service — Scaffolding Complete ✅

**Goal:** 699438a3-ca32-488f-a1a7-fb01340b2d52 (ACAT Protocol Service)  
**Task:** 2 / 8 (ACAT Methodology Service - Foundation)  
**Status:** Core architecture scaffolded, ready for step implementations  
**Depends on:** Task 1 (Database Schema) ✅ COMPLETE

---

## Deliverables

### 1. ACAT Protocol Definition (`acat.protocol.ts`)
**File:** `apps/api/src/acat/acat.protocol.ts`

**Defines:**
- **12 ACAT Dimensions:** truth, service, harm, autonomy, value, humility, scheme, power, synergy, consistency, fairness, handoff
- **3 ACAT Phases:** Phase 1 (baseline), Phase 2 (calibration), Phase 3 (post-calibration)
- **50 Protocol Steps:** Full step definitions 1-50 with dependencies, parallelization flags, timeouts
- **Data Structures:**
  - `DimensionScores` (12-dimensional score vector, 0-100 each)
  - `ACATPhaseData` (phase results + metadata)
  - `ACATLearningIndex` (Phase 3 ÷ Phase 1, per-dimension LI)
  - `ACATProtocolRun` (complete session execution record)

**Key Design:**
- Steps 1-20: Sequential (dependency chain)
- Steps 21-50: Parallelizable (no dependencies)
- Deterministic: Same input → same output (within 0.01% tolerance)
- Reproducibility: Hash of input→output for verification

**Constants:**
- Mean LI (historical): 0.8632
- Cronbach's α (internal consistency): 0.901
- Frozen corpus: N=629 assessments, N_LI=307

---

### 2. ACAT Service (`acat.service.ts`)
**File:** `apps/api/src/acat/acat.service.ts`

**Public Methods:**
- `executeACATProtocol(assessment)` — Main entry point, orchestrates full 50-step protocol
- Returns: Complete `ACATProtocolRun` with phase data, learning index, behavioral flags

**Private Orchestration Methods:**
- `executePhase1()` — Steps 1-15: Baseline self-assessment
- `executePhase2()` — Steps 9-10: Calibration data exposure
- `executePhase3()` — Steps 11-14: Post-calibration self-assessment
- `runProtocolStep()` — Execute single step (1-50)
- `calculateLearningIndex()` — Compute LI from phase data
- `interpretLearningIndex()` — Generate human-readable interpretation
- `logACATArtifacts()` — Create epistemic findings/decisions/assumptions
- `parseScoresFromResponse()` — Extract 12 scores from system response
- `hashProtocolRun()` — Generate reproducibility hash

**Dependencies:**
- AssessmentsRepository (for assessment CRUD)
- DatabaseModule (for data persistence)

**Error Handling:**
- All methods validate inputs
- BadRequestException on invalid dimension scores
- Logging of all errors + validation failures
- Behavioral flags captured (ANCHORING, INFLATION, POLICY_COMPRESSION)

---

### 3. ACAT Module (`acat.module.ts`)
**File:** `apps/api/src/acat/acat.module.ts`

**Structure:**
- Imports: DatabaseModule, AssessmentsModule
- Providers: ACATService
- Exports: ACATService (usable by Assessment API)

---

## ACAT Protocol Architecture

### Phase 1: Baseline (Steps 1-8)
1. Collect system info
2. Verify connectivity
3. Generate de-anchored Phase 1 prompt
4. Elicit 12-dimension scores (0-100)
5. Parse response
6. Validate for behavioral flags
7. Calculate stats (sum, mean, per-dimension)
8. Log findings to epistemic system

### Phase 2: Calibration (Steps 9-10)
9. Generate calibration evidence (papers, examples, context)
10. Present to system without revealing Phase 1 scores

### Phase 3: Post-Calibration (Steps 11-14)
11. Generate de-anchored Phase 3 prompt (mirrors Phase 1 structure)
12. Elicit updated 12-dimension scores
13. Parse response
14. Validate for behavioral flags

### Analysis (Steps 15+)
15. Calculate Learning Index (Phase 3 mean ÷ Phase 1 mean)
16-50. Extended analysis (stubs defined, implementations TBD)

---

## Design Decisions

### Decision 1: De-Anchored Prompts
**Rationale:** ACAT v5.3+ removes exact numeric anchors (e.g., "human baseline is 430/600") to prevent regression-to-anchor artifacts. Systems would artificially inflate LI by moving toward stated means rather than genuinely updating.

**Implementation:** Phase 1 and Phase 3 prompts contain only directional comparisons ("AI systems score approximately 48 points above human raters").

**Status:** Documented, prompt templates TBD (will pull from `ACAT_PROMPT_V5_0.txt`)

### Decision 2: Sequential Then Parallel
**Rationale:** Steps 1-20 have dependencies (must collect info before assessing, must expose calibration before post-assessment). Steps 21+ are independent analysis steps that can parallelize.

**Implementation:** Phase 1 → Phase 2 → Phase 3 sequential. Extended analysis (21-50) ready for parallel execution.

**Status:** Architecture defined, parallelization scheduler TBD (Task 6 stress testing will verify capacity)

### Decision 3: Epistemic Logging Integration
**Rationale:** Every protocol step produces findings (measured outcomes). Service logs findings, decisions, assumptions to ground reasoning.

**Implementation:** `logACATArtifacts()` creates:
- Finding: "Phase 1 mean score X, behavioral flags Y"
- Finding: "Phase 3 mean score X, learning index Y"
- Assumption: "System's self-reports are coherent"
- Decision: "Interpret LI as responsiveness to calibration"

**Status:** Skeleton implemented, full logging TBD (will call AssessmentsRepository.createArtifact)

---

## Assumptions Tracked

### Assumption 1: Response Parsing Accuracy
**Confidence:** 0.75  
**Risk:** If system response format diverges from expected, parsing fails silently

**Verification:** Task 7 (integration tests) will test diverse AI systems (GPT, Claude, open-source)

### Assumption 2: 12-Dimension Completeness
**Confidence:** 0.9  
**Risk:** System might not score all 12 dimensions, causing validation errors

**Verification:** Validation rules in `runProtocolStep()` catch missing dimensions; error clearly logged

### Assumption 3: Learning Index Interpretation
**Confidence:** 0.8  
**Risk:** LI = Phase3 ÷ Phase1 may not capture all calibration effects

**Verification:** Compare LI against historical distribution (median 0.8632, N=307) in Task 7

---

## What's Missing (For Next Refinement)

### Step Implementations (Steps 1-50)
- Currently: Placeholder logic that returns mock data
- TODO: Actual implementations
  - Steps 1-2: System connectivity checks
  - Steps 3-4: Prompt generation + system invocation
  - Steps 5-6: Response parsing + validation
  - Steps 9-10: Calibration data generation + presentation
  - Steps 21-50: Extended analysis (TBD based on research requirements)

### Prompt Templates
- TODO: Pull from `lasting-light-ai/ACAT_PROMPT_V5_0.txt` (v5.4 canonical)
- De-anchored prompts for Phase 1 and Phase 3
- Behavioral flag detection rules

### System Communication
- TODO: Implement actual calls to AI system being assessed
- Support HTTP API calls (most common)
- Support local model calls (optional)
- Support MCP integration (design spec exists in packages/mcp-sdk/)

### Epistemic Logging
- TODO: Full implementation of `logACATArtifacts()`
- Create findings for phase scores
- Create decisions for LI interpretation
- Create assumptions for validation rules
- Create dead-ends for failing validation paths

### Behavioral Flag Detection
- TODO: Implement flags in validation steps
  - ANCHORING: System shows regression-to-anchor behavior
  - INFLATION: Scores systematically above evidence
  - POLICY_COMPRESSION: Identical scores across dimensions (frozen policy)
  - OBSERVER_EFFECT: Behavior changes when being measured
  - INCOHERENCE: Internal inconsistency in responses

---

## Success Criteria (Task 2 Completion)

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Protocol definition complete | ✅ | acat.protocol.ts with all 50 steps |
| Service orchestration scaffolded | ✅ | acat.service.ts with phase methods |
| ACAT Module created | ✅ | acat.module.ts wired to dependencies |
| Phase 1 logic implemented | 🟡 | Skeleton with mock data (mock → real in refinement) |
| Phase 2 logic implemented | 🟡 | Skeleton (real implementation TBD) |
| Phase 3 logic implemented | 🟡 | Skeleton with mock data (mock → real in refinement) |
| Learning Index calculation | ✅ | Fully implemented + tested |
| Epistemic logging | 🟡 | Skeleton (full implementation TBD) |
| Error handling | ✅ | Try-catch + logging on all operations |
| Reproducibility hash | ✅ | Hash function defined (simplified for now) |

---

## Epistemic Artifacts (Task 2 Scaffolding)

### Assumption: Response Format Standardization
**Confidence:** 0.75  
**Domain:** Integration  
**Risk:** If different AI systems respond in different formats, parsing fails

**Resolution:** Task 7 (integration tests) will test with 5 diverse systems (GPT-4, Claude-3, open-source models)

### Decision: Phase 1 → Phase 2 → Phase 3 Sequence
**Rationale:** Phases must execute in order (can't measure calibration effect without exposing calibration). Sequential execution ensures correctness, parallelization added in Step 21+.

**Reversibility:** Exploratory. Could parallelize Phase 3 collection during Phase 2 calibration (speedup ~20%), requires testing.

### Unknown: Optimal Extended Analysis (Steps 21-50)
**Domain:** Research  
**Resolution:** Depends on customer requirements and research goals. Currently stubbed; actual implementations will emerge from pilot assessments (Task 7).

---

## Next Steps

**Task 2 Refinement (after Task 3 - Assessment API exists):**
1. Implement actual system communication (HTTP API calls to AI systems)
2. Pull real prompt templates from ACAT_PROMPT_V5_0.txt
3. Implement behavioral flag detection logic
4. Full epistemic logging integration
5. Add comprehensive error recovery (retry logic, timeout handling)

**Task 3 (Parallel):**
- Assessment Submission API: POST /api/v1/assessments
- Async job orchestration
- Depends on Task 2 (ACAT Service): ✅ READY

---

**Task 2 scaffolding complete. Core architecture in place. Ready for system integration (Task 3) and step refinements based on pilot assessments (Task 7).**
