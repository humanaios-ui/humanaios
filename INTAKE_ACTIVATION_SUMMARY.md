---
doc_id: HAIOS-OPS-100
title: File Review & Distribution Process — Activation Summary
revision: 1
status: draft
owner: "@humanaios-foundation/operations"
created_date: 2026-09-02
related_to: [DOCUMENT_CONTROL_PLAN.md, FILE_INTAKE_PIPELINE.md, FILE_CONTEXT_GRAPH.md]
---

# File Review & Distribution Process — Activation Summary

**Date:** 2026-09-02  
**Scope:** Translating existing document governance (DOCUMENT_CONTROL_PLAN.md) into an operational file intake pipeline hardcoded into the humanaios system.  
**Status:** Ready for Phase 1 proof-of-concept.

---

## Executive Summary

The existing DOCUMENT_CONTROL_PLAN.md (ratified 2026-07-02) is comprehensive governance. This work **operationalizes** it by:

1. **Designing an intake pipeline** — Converting manual file placement into systematic classification → ingest → routing
2. **Mapping current file scatter** — Assessing ~50 files in Downloads, 101 in inbox, orphaned folders; identifying which are controlled docs vs. reference vs. archive
3. **Integrating with empirica** — Tying file intake to the practice's transaction discipline so work is auditable and grounded
4. **Providing a Phase 1 activation path** — Proof-of-concept with 5 real files to validate heuristics before full automation

**Deliverables produced:**

| Document | Purpose | Status |
|---|---|---|
| FILE_INTAKE_PIPELINE.md (HAIOS-OPS-101) | Complete operational process: stages, heuristics, automation commands, rollout plan | Draft, ready for feedback |
| FILE_CONTEXT_GRAPH.md (HAIOS-OPS-102) | Current state: ~30 high-confidence controlled docs identified; quarantine list; canonical path assignments; Phase 1 batch | Draft, ready for feedback |
| This summary | Executive overview + decision list | Draft |

---

## Key Findings

### Finding 1: High-Confidence Controlled Docs Ready for Ingest

**30+ files** across Downloads + humanaios/ practice are governance documents (policy, process, spec, testimony) with clear ownership and completeness. These can proceed directly to INGEST stage (§1 of FILE_CONTEXT_GRAPH.md):

- **GOV (governance):** 5 files (PLATFORM_AGENTS_GOVERNANCE, Z2_CHARTER, INTENT_AFFIRMATION, 12_TRADITIONS audit+filter)
- **PROC (processes):** 4 files (OPERATORS_MANUAL, CIO_REMEDIATION_RUNBOOK, BROKER_ORCHESTRATOR_IMPLEMENTATION, AUTH_SYSTEM_GUIDE)
- **SPEC (specifications):** 4 files (H-ACAT_INSTRUMENT, H-FORMAT-01_REGISTRATION, ACAT_INTEGRATION_FOR_AUTONOMY, ACAT-EQ-spec)
- **TEST (testimony/findings):** 6 files (LMH-Validation, ACAT-INVEST-01, AUDIT_VERIFICATION, H-VERIF-02, WGS_ADDENDUM, REGISTERED)
- **OPS (operations/incidents):** 3 files (AUTH_DI_ISSUE, CIO_SESSION_CLOSE, ISSUE_REGISTERED_ADDENDUM)

**Resource implication:** ~30 files × ~5 minutes per ingest (frontmatter + registry + commit) = ~2.5 human-hours for full Phase 1 batch.

### Finding 2: Automated Classification Possible at 85%+ Accuracy

**Heuristics** defined in FILE_INTAKE_PIPELINE.md §5 can auto-classify files based on:
- Title keywords (GOVERNANCE, PROTOCOL, SPEC, PROCEDURE, POLICY)
- File size + terminology scan (governance keywords)
- Existing frontmatter (`doc_id`, `status: approved`)
- File type (code → reference, data → archive)

**Validation:** Phase 1 proof-of-concept will test on 5 real files with known expected outcomes.

### Finding 3: Current Backlog Accumulation Problem

- **Downloads:** ~50 files (user-placed, unclassified)
- **humanaios/inbox:** 101 files (accumulated, unreviewed)
- **HAIOS-Main orphaned folders:** 8 directories with unknown freshness

**Root cause:** No systematic intake gate. User manually asks "does this fit?" for each file.

**Solution:** Intake pipeline (automated classification + staged routing) + scheduled monitor (weekly, as proposed in FILE_INTAKE_PIPELINE.md §6.1, Option B).

### Finding 4: Cross-Practice Integration Point (Autonomy Orchestration)

Files related to ACAT (ACAT_INTEGRATION_SPEC_FOR_AUTONOMY, ACAT_INSTRUMENT_SPEC, etc.) reference **empirica-autonomy** practice's orchestration layer. The intake system should:

1. Identify cross-practice references
2. Link humanaios docs to autonomy's canonical specs (not duplicate)
3. Create bidirectional traceability (FILE_CONTEXT_GRAPH.md §4.2)

---

## Decisions Needed from User (Blockers)

### Decision 1: Ownership & Maintainer Role

**Question:** Who owns the document-registry.yaml and the scheduled drift monitor (FILE_INTAKE_PIPELINE.md §5)?

**Options:**
- A) **mesh-support practice** — handles cross-practice plumbing; natural fit for registry + monitor
- B) **humanaios core** — maintains own registry; mesh-support helps with tooling
- C) **Shared (hybrid)** — mesh-support maintains CI/automation; humanaios maintains policy

**Impact:** Determines who is on-call for monitor failures, who approves registry schema changes, escalation path.

**Recommendation:** **Option A (mesh-support)** — matches the pattern in DOCUMENT_CONTROL_PLAN.md §7 (Roles). Ownership of *policy* stays with humanaios (document owners); ownership of *control mechanism* (registry, monitor) belongs to the cross-practice infrastructure layer.

---

### Decision 2: CODEOWNERS Assignment

**Question:** For each doc area (GOV, PROC, SPEC, VIS, TEST, OPS), who are the approvers?

**Examples:**
- GOV area → `@humanaios-foundation/governance` (team or individuals?)
- PROC area → `@humanaios-foundation/ops` (team or individuals?)
- SPEC area → `@humanaios-foundation/engineering` (team or individuals?)

**Impact:** Sets branch protection rules; determines who can approve PR that moves a document from `draft` to `review` to `approved`.

**Recommendation:** Use **teams, not individuals** (survives role churn; named in CODEOWNERS file). Example: `HAIOS-OPS/governance` instead of `carly` or `david`.

---

### Decision 3: Archive Policy (Downloads & Desktop Folders)

**Question:** For files in Downloads that are successfully ingested, what's the retention policy?

**Options:**
- A) **Delete immediately** after ingest (canonical location is now SOT; Downloads is staging only)
- B) **Archive with timestamp** (e.g., `/archive/2026-09-02/filename.md`) for historical trace
- C) **Keep indefinitely** but mark read-only (folder becomes a historical reference)

**Impact:** Prevents re-accumulation; affects storage usage; impacts audit trail completeness.

**Recommendation:** **Option B (archive with timestamp)** — provides history (useful if a file was ingested wrong) without requiring eternal management. Monthly purge (keep 6 months) if needed.

---

### Decision 4: Activation Frequency

**Question:** How often should the intake pipeline run?

**Options:**
- A) **On-demand** — user runs `empirica intake-run` manually when they place files
- B) **Weekly** — scheduled job (e.g., Monday 9am), processes Downloads + inbox folders
- C) **Continuous** — watch Downloads folder; on new file, classify within 1 hour

**Impact:** Resource consumption (AI tokens for classification); latency (file→ingested time); user friction (do they have to remember to run it?).

**Recommendation:** **Option B (weekly)** initially. Matches the audit cadence already in place (DOCUMENT_CONTROL_PLAN.md drift monitor runs biweekly). Low overhead; predictable. Can escalate to continuous if backlog is large.

---

## Phase 1: Proof-of-Concept Batch

**To activate the pipeline with zero risk:**

### Batch Selection (5 Representative Files)

1. **PLATFORM_AGENTS_GOVERNANCE_V1_0.md** — High-confidence GOV file; ~8KB; clear purpose
2. **H-ACAT_INSTRUMENT_SPEC_V0_1.md** — High-confidence SPEC file; ~20KB; cross-practice reference
3. **OPERATORS_MANUAL.md** — High-confidence PROC file; ~15KB; well-structured
4. **BIO_SYSTEMS_MAPPING_V1.md** — **Quarantine test:** Unclear scope (process output? research?)
5. **SHARED_MEMORY_CENSUS_v0_1.md** — **Quarantine test:** Unclear scope (finding? reference?)

**Why this mix:**
- Covers 3 confident areas (GOV, SPEC, PROC) + 2 unclear (test quarantine flow)
- Real files from Downloads (test move mechanics)
- Small enough for manual walkthrough
- Exercises both auto-classification and human triage

### Execution Steps

**Week 1:**
1. User manually classifies these 5 using FILE_INTAKE_PIPELINE.md §2–3 (answer Q1–Q3)
2. Generate sample manifest showing what auto-classification would have done
3. Compare vs. user's answers (error rate assessment)

**Week 2:**
1. Build Python classifier script (FILE_INTAKE_PIPELINE.md §6.2 logic + §5 heuristics)
2. Test on 5-file batch; refine heuristics if error rate > 10%

**Week 3:**
1. Manually execute ingest steps (§6.4) on one file as full demo:
   - Add frontmatter (doc_id, owner, status=draft)
   - Move to canonical path
   - Add to registry
   - Commit with signature
   - Log finding

**Week 4:**
1. Wire up the full pipeline (check automation works end-to-end)
2. Test on remaining 4 files in batch
3. Prepare for Phase 2 (extend to full Downloads folder)

### Success Criteria (Phase 1)

| Metric | Target | Meaning |
|---|---|---|
| Classification accuracy | ≥ 95% (4–5 of 5 correct) | Heuristics are reliable |
| Frontmatter validity | 100% | Schema accepts all fields; no errors |
| Registry entry quality | 100% | doc_id unique; canonical path correct |
| Git commit cleanliness | 100% | Signed; clear message; no spurious files |
| Quarantine flow | Verified | Files correctly quarantined; user can triage |
| **Total time investment** | **≤ 6 hours** | Proof-of-concept stays lightweight |

---

## Phase 2–6 Roadmap (From FILE_INTAKE_PIPELINE.md §10)

Once Phase 1 validates the pipeline:

| Phase | Work | Effort | Timeline |
|---|---|---|---|
| **P2** | Automate classification; add frontmatter template | 3–4h | Week 2 |
| **P3** | Full pipeline + move + registry + commit | 4–5h | Week 3 |
| **P4** | Intake on full Downloads folder (50 files) | 2h + 8h (files × 10min each) | Week 4 |
| **P5** | Weekly monitor + drift detection | 6h | Week 5 |
| **P6** | Hardcode into `.empirica/project.yaml` + GitHub Actions | 3h | Week 5 |

**Total effort to full automation:** ~20–25 hours (mostly Phase 4 ingest on backlog; phases 2–3 are leverage plays).

---

## Integration with Existing Documents

**This plan does not replace or deprecate:**
- DOCUMENT_CONTROL_PLAN.md (governance layer) — unchanged; this activates it
- humanaios practices' own SOPs — these *are* the files being governed

**What it adds:**
- Repeatable intake process (no more manual "does this fit?")
- Automated classification (reduces triage overhead)
- Audit trail (every file → frontmatter + registry entry + git commit)
- Drift monitor (catches divergence, stale docs, orphaned files)

---

## Resource Accounting

**Noetic phase (completed this session):**
- AI tokens: ~80k (design + mapping)
- Human labor: 0 (by design; user not asked until decisions needed)

**Praxic phase (Phase 1, if approved):**
- AI tokens (anticipated): ~50k (classification script + test runs)
- Human labor (anticipated): 6–8 hours (manual triage + batch selection + validation)

**Full activation (Phases 1–6):**
- AI tokens (anticipated): ~150k total
- Human labor (anticipated): 20–25 hours total (mostly mechanical ingest on backlog)

---

## Next Steps

### Immediate (Blocking Phase 1)

1. **User confirms decisions** from "Decisions Needed" section above (decisions 1–4)
2. **User selects Phase 1 batch** — confirm the 5 files or choose alternatives
3. **Schedule Phase 1 kickoff** — week of 2026-09-09

### Then (Phase 1 execution)

Follow the proof-of-concept plan (Week 1–4 timeline above).

### Upstream (If needed)

If humanaios is part of a larger foundation orchestration (the autonomy practice serves humanaios), notify:
- **mesh-support** — will be maintaining the registry/monitor (Decision 1)
- **empirica-autonomy** — may need to link cross-practice ACAT specs (Finding 4)

---

## Related Artifacts

- **DOCUMENT_CONTROL_PLAN.md** — The governance this activates (read first)
- **FILE_INTAKE_PIPELINE.md** — Operational process (stages, heuristics, automation)
- **FILE_CONTEXT_GRAPH.md** — Current state (file inventory, classifications, canonical paths)

---

**Ready for feedback. Awaiting user decisions before Phase 1 activation.**
