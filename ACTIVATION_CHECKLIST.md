---
doc_id: HAIOS-OPS-107
title: File Intake Pipeline — Activation Checklist
revision: 1
status: draft
owner: "@humanaios-foundation/operations"
created_date: 2026-09-02
---

# File Intake Pipeline — Activation Checklist

**Status:** Ready to activate Phase 1.  
**Decisions confirmed:** ✓ All 4 decisions (maintainer, CODEOWNERS, archive policy, frequency)

---

## What You Have (Delivered)

### Governance Documents
- [x] **DOCUMENT_CONTROL_PLAN.md** — Comprehensive governance (existing, ratified 2026-07-02)
- [x] **FILE_INTAKE_PIPELINE.md (HAIOS-OPS-101)** — Operational process with 6 stages
- [x] **FILE_CONTEXT_GRAPH.md (HAIOS-OPS-102)** — Current state mapping (30+ docs identified)
- [x] **INTAKE_ACTIVATION_SUMMARY.md (HAIOS-OPS-100)** — Executive summary + 4 decisions (NOW CONFIRMED)

### Automation & Configuration
- [x] **frontmatter.schema.json** — JSON Schema for YAML frontmatter validation
- [x] **validate_frontmatter.py** — Validator script (run on any .md file or batch)
- [x] **classify_and_ingest.py** — Classifier + intake orchestrator (heuristics from §5 of pipeline)
- [x] **.github/CODEOWNERS** — Branch protection config (all areas → @carly)

### Phase 1 Instructions
- [x] **PHASE_1_BATCH_INSTRUCTIONS.md** — Step-by-step guide for 5-file proof-of-concept
- [x] **This checklist** — Quick reference for what's ready

---

## Your Confirmed Decisions

| Decision | Your Choice | Impact |
|---|---|---|
| **1. Maintainer Role** | **Hybrid** | mesh-support does tooling (CI, monitor, registry schema); humanaios owns policy & approval |
| **2. CODEOWNERS** | **@carly** (you) for all areas | You are the sole approver for all doc areas (GOV/PROC/SPEC/TEST/VIS/OPS) |
| **3. Archive Policy** | **B) Timestamp-based** | Ingested files moved to `reference/archive/2026-09-02/`; 6-month auto-purge optional |
| **4. Intake Frequency** | **A) On-demand** | You run `empirica intake-run --source /Downloads` manually when you place files |

**These are now hardcoded in:**
- `.github/CODEOWNERS` (owner mappings)
- `FILE_INTAKE_PIPELINE.md` §10 (activation plan)
- Classifier heuristics

---

## Phase 1: Next Steps (This Week)

### TODAY (2026-09-02)
- [ ] Read **PHASE_1_BATCH_INSTRUCTIONS.md** in full
- [ ] Understand the 8 steps (classifier → triage → frontmatter → validate → move → registry → commit)
- [ ] Ensure you have Python 3 + pyyaml installed:
  ```bash
  python3 -m pip install pyyaml jsonschema
  ```

### TOMORROW (2026-09-03)
- [ ] **Step 1:** Run classifier on /Downloads:
  ```bash
  cd /Users/andersonfamily/practices/humanaios
  python .doc-control/classify_and_ingest.py --source /Users/andersonfamily/Downloads --mode classify-only
  ```
- [ ] **Step 2:** Review manifest; decide on 2 quarantined files (BIO_SYSTEMS_MAPPING, SHARED_MEMORY_CENSUS)
  - Record your decisions (area or reference)

### 2026-09-03 AFTERNOON / 2026-09-04
- [ ] **Step 3:** Add frontmatter to all 5 Phase 1 files (templates in instructions)
- [ ] **Step 4:** Validate:
  ```bash
  python .doc-control/validate_frontmatter.py /Users/andersonfamily/Downloads/
  ```
  - Expect: "5/5 files valid"

### 2026-09-04
- [ ] **Step 5:** Move files to canonical paths:
  ```bash
  mv /Users/andersonfamily/Downloads/PLATFORM_AGENTS_GOVERNANCE_V1_0.md \
     /Users/andersonfamily/practices/humanaios/docs/GOV/
  # ... repeat for other 4 files
  ```
- [ ] **Step 6:** Create/update `document-registry.yaml` with 5 entries
- [ ] Verify registry uniqueness (no duplicate doc_ids)

### 2026-09-05
- [ ] **Step 7:** Commit to git:
  ```bash
  cd /Users/andersonfamily/practices/humanaios
  git add docs/ reference/ document-registry.yaml .doc-control/ .github/
  git commit -m "phase-1-ingest: Add 5 controlled documents to registry"
  ```
- [ ] **Step 8:** Validate via CI (or manual):
  ```bash
  python .doc-control/validate_frontmatter.py /Users/andersonfamily/practices/humanaios/docs/
  ```
  - Expect: "5/5 files valid"

---

## Phase 1 Success Criteria

| ✓ | Criterion | How to verify |
|---|---|---|
| [ ] | Files classified | Manifest has 3 high-conf + 2 quarantine bucket entries |
| [ ] | Triage completed | You've decided area for BIO_SYSTEMS + SHARED_MEMORY |
| [ ] | Frontmatter valid | Validator output: "5/5 files valid" |
| [ ] | Canonical paths set | Files exist in `docs/<AREA>/` subdirectories |
| [ ] | Registry created | `document-registry.yaml` has 5 entries; doc_ids unique |
| [ ] | Git committed | `git log` shows `phase-1-ingest` commit |
| [ ] | CI passes | Frontmatter + registry validation errors = 0 |

---

## File Locations (Quick Reference)

```
/Users/andersonfamily/practices/humanaios/
├── docs/
│   ├── GOV/                 ← Governance docs
│   ├── PROC/                ← Processes
│   ├── SPEC/                ← Specifications
│   ├── TEST/                ← Testimony/findings
│   ├── VIS/                 ← Vision/strategy
│   └── OPS/                 ← Operations/incidents
├── reference/
│   └── archive/
│       └── 2026-09-02/      ← Archived reference files (timestamp-based)
├── .doc-control/
│   ├── frontmatter.schema.json       ← Schema definition
│   ├── validate_frontmatter.py       ← Validator script
│   └── classify_and_ingest.py        ← Classifier script
├── .github/
│   └── CODEOWNERS                    ← Branch protection (you = approver for all)
├── document-registry.yaml            ← SSOT index (created/updated in Phase 1)
├── DOCUMENT_CONTROL_PLAN.md          ← Governance (existing)
├── FILE_INTAKE_PIPELINE.md           ← Operational process (new)
├── FILE_CONTEXT_GRAPH.md             ← Current state mapping (new)
├── INTAKE_ACTIVATION_SUMMARY.md      ← Executive summary (new)
└── PHASE_1_BATCH_INSTRUCTIONS.md     ← Step-by-step guide (new)
```

---

## Decisions Baked In (Reference)

### Maintainer Role: Hybrid
- **mesh-support:** Maintains CI, registry schema, drift monitor, automation tooling
- **humanaios:** Owns document policy, approval decisions, area assignments
- **Implication:** mesh-support can help troubleshoot; you are the final authority

### CODEOWNERS: @carly
- **All areas:** GOV, PROC, SPEC, TEST, VIS, OPS → You approve
- **All control files:** .doc-control/, .github/, document-registry.yaml → You approve
- **Implication:** Branch protection will require your approval on any PR touching docs

### Archive Policy: Timestamp-Based
- Ingested files → move to `reference/archive/<YYYY-MM-DD>/`
- Optional 6-month auto-purge (can be configured later)
- **Implication:** Audit trail preserved; no unbounded growth; easy manual cleanup

### Frequency: On-Demand
- You manually run intake when you add files to Downloads
- Not scheduled/automated yet (can be added in Phase 2 if desired)
- **Implication:** Control over when things run; zero surprise actions; low overhead

---

## After Phase 1 (Phases 2–6)

Once Phase 1 validates the pipeline:

| Phase | Work | Timeline |
|---|---|---|
| **P2** | Auto-generate doc_ids; build registry generator script | Week 2 |
| **P3** | Full end-to-end pipeline (classif → ingest → commit) | Week 3 |
| **P4** | Run on full Downloads backlog (50 files) | Week 4 |
| **P5** | Schedule + monitor (weekly intake) | Week 5 |
| **P6** | Hardcode into `.empirica/project.yaml`; CI integration | Week 5 |

Each phase is gated on the prior one completing successfully.

---

## Questions / Blockers?

**Before you start Phase 1:**

1. **Do you want mesh-support involved now, or just for later phases?**
   - Now: cc @mesh-support on any Phase 1 commits; get feedback
   - Later: Activate once Phase 1 is stable

2. **Should we auto-assign doc_ids, or do you want to verify each one?**
   - Phase 1 uses manual assignment (you pick the NNN in HAIOS-<AREA>-NNN)
   - Phase 2 can auto-increment from the registry

3. **Do you need the drift monitor before you start Phase 1?**
   - No: Phase 1 is just intake pipeline (classify → move → register)
   - Monitor is Phase 5; can wait

4. **Archive folder naming:** Keep `reference/archive/2026-09-02/` or rename to something else?
   - Current: Timestamp-based (matches decision 3)
   - Alternative: `reference/imported/` or `reference/processed/`

---

## Summary

**You now have:**
1. ✅ Comprehensive governance (DOCUMENT_CONTROL_PLAN.md)
2. ✅ Operational pipeline design (FILE_INTAKE_PIPELINE.md)
3. ✅ Current state mapping (FILE_CONTEXT_GRAPH.md)
4. ✅ Automation scripts (validator, classifier)
5. ✅ Phase 1 step-by-step guide (PHASE_1_BATCH_INSTRUCTIONS.md)
6. ✅ All 4 decisions confirmed + hardcoded

**You're ready to:**
- Run Phase 1 this week (5 real files)
- Validate heuristics
- Commit + prepare for scaling

**Timeline:** ~4–5 hours this week for Phase 1; full automation in 5 weeks (Phases 2–6).

---

**Ready to begin? Start with Step 1 in PHASE_1_BATCH_INSTRUCTIONS.md.**
