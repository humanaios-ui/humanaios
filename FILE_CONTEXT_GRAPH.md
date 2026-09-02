---
doc_id: HAIOS-OPS-102
title: File Context Graph — Current State Mapping
revision: 1
status: draft
owner: "@humanaios-foundation/operations"
created_date: 2026-09-02
related_to: [HAIOS-OPS-101]
---

# File Context Graph — Current State Mapping

**Purpose:** Map current scattered files (Downloads, Desktop, orphaned folders) to document control areas and identify overlaps with empirica-autonomy orchestration project structure.

**Output:** Structured inventory used to inform Phase 1 proof-of-concept intake batch + identify canonical path assignments.

---

## 1. High-Confidence Controlled Documents (Ready for Ingest)

Files with clear governance intent, functional ownership, and completeness. **Classification confidence: 90–95%.**

### 1.1 Governance (GOV) — Policy & Frameworks

| Filename | Location | Est. Size | Purpose | Owner | Inferred doc_id | Status |
|---|---|---|---|---|---|---|
| PLATFORM_AGENTS_GOVERNANCE_V1_0.md | Downloads | ~8KB | Agent RBAC policy framework | @humanaios-foundation/governance | HAIOS-GOV-013 | draft |
| Z2_CHARTER.yaml | Downloads | ~2KB | Z2 charter / authority boundary | @humanaios-foundation/governance | HAIOS-GOV-011 | draft |
| 12_TRADITIONS_COMPLIANCE_AUDIT.md | humanaios/ | ~12KB | 12-step compliance audit | @humanaios-foundation/governance | HAIOS-GOV-009 | approved |
| 12_TRADITIONS_DECISION_FILTER.md | humanaios/ | ~4KB | Decision framework derived from audit | @humanaios-foundation/governance | HAIOS-GOV-010 | draft |
| INTENT_AFFIRMATION.yaml | Downloads | ~1KB | Org intent statement (structured) | @humanaios-foundation/governance | HAIOS-GOV-012 | draft |

### 1.2 Processes (PROC) — Runbooks & Operations

| Filename | Location | Size | Purpose | Owner | doc_id | Status |
|---|---|---|---|---|---|---|
| OPERATORS_MANUAL.md | Downloads | ~15KB | Human agent operational manual | @humanaios-foundation/ops | HAIOS-PROC-015 | review |
| CIO_REMEDIATION_RUNBOOK_S082226_r1.2.md | Downloads | ~7KB | CIO incident response (incident ref: S082226) | @humanaios-foundation/ops | HAIOS-PROC-014 | approved |
| BROKER_ORCHESTRATOR_IMPLEMENTATION_PLAN_V1_1.md | Downloads | ~9KB | Broker/orchestrator deploy guide | @humanaios-foundation/ops | HAIOS-PROC-013 | draft |
| AUTH_SYSTEM_INSTALLATION_GUIDE.md | humanaios/ | ~6KB | Auth subsystem setup | @humanaios-foundation/ops | HAIOS-PROC-010 | approved |

### 1.3 Specifications (SPEC) — Technical Standards

| Filename | Location | Size | Purpose | Owner | doc_id | Status |
|---|---|---|---|---|---|---|
| H-ACAT_INSTRUMENT_SPEC_V0_1.md | Downloads | ~20KB | HAIOS ACAT instrument spec | @humanaios-foundation/engineering | HAIOS-SPEC-008 | review |
| H-FORMAT-01_REGISTRATION_RATIFIED_S061726.md | Downloads | ~11KB | H-FORMAT-01 registration (final, signed) | @humanaios-foundation/engineering | HAIOS-SPEC-006 | approved |
| ACAT_INTEGRATION_SPEC_FOR_AUTONOMY.md | humanaios/ | ~7KB | How ACAT integrates with autonomy practice | @humanaios-foundation/engineering | HAIOS-SPEC-009 | draft |
| ACAT-EQ-v0.1-spec.md | Downloads | ~6KB | ACAT equivalence questionnaire spec | @humanaios-foundation/engineering | HAIOS-SPEC-007 | draft |

### 1.4 Vision & Strategy (VIS)

| Filename | Location | Size | Purpose | Owner | doc_id | Status |
|---|---|---|---|---|---|---|
| ACTIVATION_ROADMAP_DAYS_2_7.md | humanaios/ | ~5KB | Immediate (7-day) activation plan | @humanaios-foundation/strategy | HAIOS-VIS-004 | approved |
| Z2_CHARTER.yaml | Downloads | ~2KB | (already listed GOV; overlaps) | — | — | — |

### 1.5 Test & Testimony (TEST) — Findings, Protocols, Research

| Filename | Location | Size | Purpose | Owner | doc_id | Status |
|---|---|---|---|---|---|---|
| LMH-Validation-Experiment-S061926.md | Downloads | ~8KB | LMH validation (experiment, timestamped) | @humanaios-foundation/research | HAIOS-TEST-005 | approved |
| ACAT-INVEST-01-protocol.md | Downloads | ~9KB | ACAT investigation protocol | @humanaios-foundation/research | HAIOS-TEST-006 | review |
| AUDIT_VERIFICATION.md | Downloads | ~4KB | Audit verification summary | @humanaios-foundation/research | HAIOS-TEST-007 | draft |
| README_H-VERIF-02_S072126-01.md | Downloads | ~3KB | H-VERIF-02 verification notes | @humanaios-foundation/research | HAIOS-TEST-008 | draft |
| WGS_ADDENDUM_S-071526-01.md | Downloads | ~2KB | Working group standard addendum | @humanaios-foundation/research | HAIOS-TEST-004 | draft |
| REGISTERED.md | Downloads | ~6KB | Registered findings index | @humanaios-foundation/research | HAIOS-TEST-003 | approved |

### 1.6 Incident/Issue Response (OPS-INCIDENT)

| Filename | Location | Size | Purpose | Owner | doc_id | Status |
|---|---|---|---|---|---|---|
| AUTH_DI_ISSUE.md | humanaios/ | ~3KB | Dependency injection issue (auth subsystem) | @humanaios-foundation/ops | HAIOS-OPS-103 | draft |
| CIO_SESSION_CLOSE_S082226.md | Downloads | ~5KB | CIO session debrief (incident S082226) | @humanaios-foundation/ops | HAIOS-OPS-104 | approved |
| ISSUE_registered_md_addendum_wave1.md | Downloads | ~4KB | Issue registration addendum (wave 1) | @humanaios-foundation/ops | HAIOS-OPS-105 | draft |

---

## 2. Likely Reference Files (Auto-Archive)

Files that are supporting materials, data dumps, or intermediate outputs. **Confidence: 85–95%**

| Filename | Location | Type | Purpose | Action |
|---|---|---|---|---|
| FILE_TYPE_DIRECTORY.yaml | Downloads | Reference index | Metadata catalog | Archive + link from registry |
| context_survey_raw.json | Downloads | Data export | Survey responses (raw) | Archive (reference, analysis output) |
| registry_fmea_output.json | Downloads | Structured data | FMEA analysis (computed) | Archive (reference, computed artifact) |
| rubric_params.json | Downloads | Configuration | Rubric parameter set | Archive (reference, config snapshot) |
| sources.json | Downloads | Data export | Source registry (export) | Archive (superseded by living registry) |
| anderson_hayhurst_hism_research_log.csv | Downloads | Research log | HISM research tracking (raw) | Archive (reference, raw log) |
| acat_doc_Combined_Sequencing_Brief_HFOR_20260617T204538Z.json | Downloads | Data export | ACAT sequence export | Archive (reference, data snapshot) |
| queue_items 2.json | Downloads | Data dump | Queue state snapshot | Archive (ephemeral, snapshot) |
| prs_events.jsonl | Downloads | Event log | PRS event stream | Archive (reference, event log) |
| PRECOMMIT_MANIFEST 3.json | Downloads | Configuration | Pre-commit hook state | Archive (reference, tool config) |

**Action:** Batch-move to `practices/humanaios/reference/` with README linking to the living documents they support.

---

## 3. Unclassified / Quarantine (Needs Triage)

Files where purpose is unclear or mixed-type. **Confidence: 50–70%.** Defer to user input.

| Filename | Location | Type | Reason | Suggested Action |
|---|---|---|---|---|
| mac-tuneup.sh | Downloads | Shell script | System maintenance (no governance) | Archive to reference/ (tooling) |
| intake.py | Downloads | Python code | Data processing (no governance) | Archive to reference/ (tool/script) |
| claim_scanner_v2.py | Downloads | Python code | Analysis tool (utility) | Archive to reference/ (tool/script) |
| boundary_and_scorer.py | Downloads | Python code | Analysis tool | Archive to reference/ (tool/script) |
| bio_framework_stress_test_v1_0 2.py | Downloads | Python code | Research experiment | Archive (reference) or TEST (if formal experiment?) — **TRIAGE** |
| P29_articulation_gate.py | Downloads | Python code | Process code (P29 = unknown process) | Archive or PROC? — **TRIAGE** |
| questionnaire_html_builder_v1_0.cpython-312.pyc | Downloads | Compiled Python | Build artifact | Delete (compiled, no source) |
| BIO_SYSTEMS_MAPPING_V1.md | Downloads | Analysis | Biological systems mapping | PROC (process output) or TEST (research)? — **TRIAGE** |
| IC-CAND-ELICITATION-SURFACE-TAXONOMY-UNIFICATION.md | Downloads | Analysis | Taxonomy work (IC = Intelligence Candidate?) | TEST (research artifact) — likely controlled |
| SHARED_MEMORY_CENSUS_v0_1.md | Downloads | Analysis | Memory/persistence audit | Likely TEST (research); **Confirm scope** |
| CALIBRATION_OOO_v0.3.md | Downloads | Process | Out-of-office calibration policy (?) | VIS (vision) or PROC (process)? — **TRIAGE** |
| CORRESPONDENCE_ADJUDICATION_GATE_v0_1.md | Downloads | Process | Adjudication workflow | PROC (process) — **TRIAGE for ownership** |
| FALSIFIER_ADDENDA_v0_1.md | Downloads | Analysis | Addendum to falsifier framework | SPEC (technical standard) or TEST (research)? — **TRIAGE** |
| TOKEN_MONITORING_MIGRATION_B_v1_0.md | Downloads | Operations | Token monitoring migration guide | PROC (process) — **TRIAGE** |
| GATE_REGISTRY_S071126-01.md | Downloads | Registry | Gate registry (dated, ID format matches incident tracking) | TEST (findings) or reference? — **TRIAGE** |
| ADVERSE IEL_REVIEW_PROMPT_072726.md | Downloads | Prompt | Review prompt (tool/template) | Archive (reference, tool) — **CONFIRM use** |
| PR-AGENT-BIZ-001.md | Downloads | Proposal? | PR or business proposal? | Archive or PROC? — **Clarify content** |
| ohmenrah-stimulus-candidates.md | Downloads | Analysis | Research candidates list | TEST (research) — **TRIAGE** |
| sarah-validation-governance-gates.md | Downloads | Analysis | Validation gates (Sarah's work?) | PROC (process) or TEST (validation protocol)? — **TRIAGE** |
| ACTIVATION_STATUS.md | humanaios/ | Status report | Activation status (snapshot in time) | Archive (reference, historical) |
| ADMIRAL_SIGN_OFF.md | humanaios/ | Approval record | Admiral approval (signed) | GOV (governance record) or archive? — **CONFIRM** |

---

## 4. Cross-Practice Orchestration Mapping

**Key finding:** humanaios files should reference empirica-autonomy's project structure for shared infrastructure.

### 4.1 Autonomy Orchestration Model (From empirica-autonomy/.empirica/project.yaml)

```yaml
ai_id: empirica-autonomy
practices_served:
  - humanaios  ← HumanAIOS integration point
  - outreach
  - mesh-support
  - [others]

owned_services:
  - acat-intake
  - acat-findings-endpoint
  - registry-sync
```

**Implication:** ACAT-related specs in humanaios (e.g., ACAT_INTEGRATION_SPEC_FOR_AUTONOMY.md) should **reference** the autonomy practice's canonical ACAT spec rather than duplicate.

### 4.2 Empirica-Autonomy Docs in Humanaios Practice

| File in humanaios/ | Related autonomy service | Recommendation |
|---|---|---|
| ACAT_INTEGRATION_SPEC_FOR_AUTONOMY.md | acat-intake | Link to autonomy's canonical ACAT spec; this is an integration layer (keep as owned document) |
| ACAT_CLI_ASSESSMENT.md | acat-findings-endpoint | Reference autonomy's ACAT CLI; this is an assessment (integrate findings) |

### 4.3 Registry Synchronization Implication

The document-registry.yaml (§3.2 of FILE_INTAKE_PIPELINE.md) must:
1. List all **owned** documents (humanaios-specific governance)
2. **Link** to canonical sources in other practices (e.g., autonomy's ACAT registry)
3. Not **duplicate** cross-practice specs

---

## 5. Proposed Canonical Path Assignments

**Rule:** One doc_id, one canonical path. Other copies are removed or converted to links.

### 5.1 Controlled Documents → Canonical Paths

```
practices/humanaios/docs/
├── GOV/                           # Governance
│   ├── PLATFORM_AGENTS_GOVERNANCE_V1_0.md     (HAIOS-GOV-013)
│   ├── Z2_CHARTER.yaml                         (HAIOS-GOV-011)
│   ├── INTENT_AFFIRMATION.yaml                 (HAIOS-GOV-012)
│   ├── 12_TRADITIONS_COMPLIANCE_AUDIT.md       (HAIOS-GOV-009, existing)
│   └── 12_TRADITIONS_DECISION_FILTER.md        (HAIOS-GOV-010, existing)
├── PROC/                          # Processes
│   ├── OPERATORS_MANUAL.md                     (HAIOS-PROC-015)
│   ├── CIO_REMEDIATION_RUNBOOK_S082226.md     (HAIOS-PROC-014)
│   ├── BROKER_ORCHESTRATOR_IMPLEMENTATION.md  (HAIOS-PROC-013)
│   ├── AUTH_SYSTEM_INSTALLATION_GUIDE.md      (HAIOS-PROC-010, existing)
│   └── CORRESPONDENCE_ADJUDICATION_GATE.md    (HAIOS-PROC-XXX, TBD)
├── SPEC/                          # Specifications
│   ├── H-ACAT_INSTRUMENT_SPEC_V0_1.md         (HAIOS-SPEC-008)
│   ├── H-FORMAT-01_REGISTRATION_RATIFIED.md   (HAIOS-SPEC-006)
│   ├── ACAT_INTEGRATION_SPEC_FOR_AUTONOMY.md  (HAIOS-SPEC-009, existing)
│   ├── ACAT-EQ-v0.1-spec.md                   (HAIOS-SPEC-007)
│   └── ACAT_CLI_ASSESSMENT.md                 (HAIOS-SPEC-005, existing)
├── TEST/                          # Test & Testimony
│   ├── LMH-Validation-Experiment-S061926.md   (HAIOS-TEST-005)
│   ├── ACAT-INVEST-01-protocol.md             (HAIOS-TEST-006)
│   ├── AUDIT_VERIFICATION.md                  (HAIOS-TEST-007)
│   ├── README_H-VERIF-02_S072126-01.md        (HAIOS-TEST-008)
│   ├── WGS_ADDENDUM_S-071526-01.md            (HAIOS-TEST-004)
│   └── REGISTERED.md                          (HAIOS-TEST-003, existing)
├── VIS/                           # Vision & Strategy
│   └── ACTIVATION_ROADMAP_DAYS_2_7.md         (HAIOS-VIS-004, existing)
└── OPS/                           # Operations & Incidents
    ├── AUTH_DI_ISSUE.md                       (HAIOS-OPS-103, existing)
    ├── CIO_SESSION_CLOSE_S082226.md           (HAIOS-OPS-104)
    └── ISSUE_REGISTERED_ADDENDUM_WAVE1.md     (HAIOS-OPS-105)

practices/humanaios/reference/          # Supporting materials
├── queries/
│   ├── context_survey_raw.json
│   ├── registry_fmea_output.json
│   └── [other data exports]
├── tools/
│   ├── intake.py
│   ├── claim_scanner_v2.py
│   └── [utility scripts]
└── index.md                               # "See main registry for governed docs"
```

### 5.2 Duplicates → Removal Strategy

For files like HAIOS-TRADITIONS-COMPLIANCE-AUDIT.md that exist in both Downloads (from pre-control era) and in practices/humanaios/ (already controlled):

```
Downloads/TRADITIONS_COMPLIANCE_AUDIT.md
  → Diff against practices/humanaios/12_TRADITIONS_COMPLIANCE_AUDIT.md
  → If identical: DELETE from Downloads (redundant)
  → If diverged: MERGE into canonical (with revision bump), DELETE from Downloads
  → Git note: "Removed: deduplicated with HAIOS-GOV-009"
```

---

## 6. Orphaned Folder Reconciliation

**Desktop/HAIOS-Main:** Contains what looks like a 2024–2025 project export.

| Folder | Est. Size | Content | Recommendation |
|---|---|---|---|
| ACAT-Dashboard | ~2MB | Dashboard code/data | Audit: moved to humanaios yet? Move to practices/humanaios/archive/2026-q2-import/ |
| ACAT-Observatory | ~1.5MB | Observatory code | Same: audit & archive |
| HAIOSCC | ~3MB | CC (Compliance Coordinator?) artifacts | Same: audit & archive |
| Operations | ~2MB | Ops artifacts | Audit: merge relevant docs into GOV/PROC/OPS; archive rest |
| docs | ~1MB | Doc tree | Audit: check for overlap with practices/humanaios/docs/; deduplicate |
| humanaios [repos] | ~10MB | Repo mirrors | Audit: are these active mirrors or stale? Archive if stale |

**Action:** Create a separate RECONCILIATION task to:
1. Audit each folder
2. Identify what was moved to practices/ already
3. Extract any "live" docs that belong in the canonical registry
4. Archive the rest with a README explaining the import date

---

## 7. Phase 1 Proof-of-Concept Batch

**To activate FILE_INTAKE_PIPELINE.md§Phase 1 with minimal risk:**

Select 3–5 representative files covering multiple areas:

**Suggested batch:**
1. ✓ PLATFORM_AGENTS_GOVERNANCE_V1_0.md (GOV, high-confidence, ~8KB)
2. ✓ H-ACAT_INSTRUMENT_SPEC_V0_1.md (SPEC, high-confidence, ~20KB)
3. ✓ OPERATORS_MANUAL.md (PROC, high-confidence, ~15KB)
4. ? BIO_SYSTEMS_MAPPING_V1.md (UNCLEAR, needs triage, ~5KB) — test quarantine flow
5. ? SHARED_MEMORY_CENSUS_v0_1.md (UNCLEAR, needs ownership confirmation)

**Why these:**
- Mix of areas (GOV, SPEC, PROC)
- Mix of confidence levels (test auto-classification + quarantine)
- Real files from Downloads (test move + frontmatter)
- Small enough for manual walkthrough; large enough to catch issues

**Execution:**
1. User manually classifies these 5 using §2–3 of FILE_INTAKE_PIPELINE.md
2. Generate manifest (as shown in §6.2)
3. User reviews manifest + confirms overrides
4. Manually run ingest steps (§6.4) on one file as demo
5. Observe output: frontmatter, registry entry, git commit
6. Iterate on heuristics if classification was off

---

## 8. Metrics for Phase 1 Success

| Metric | Target | Success means |
|---|---|---|
| Classification accuracy | ≥ 95% | 4–5 of 5 files classified correctly without override |
| Frontmatter validity | 100% | No schema errors; all required keys present |
| Registry entry quality | 100% | doc_id unique; path correct; owner assigned |
| Git commit cleanliness | 100% | Signed commit; clear message; no spurious files |
| Quarantine flow | Verified | Unclear files quarantined correctly; user able to triage |

---

**Related documents:**
- FILE_INTAKE_PIPELINE.md (operational process)
- DOCUMENT_CONTROL_PLAN.md (governance)

**Next step:** Carly selects Phase 1 proof-of-concept batch + confirms ownership questions from FILE_INTAKE_PIPELINE.md§11.
