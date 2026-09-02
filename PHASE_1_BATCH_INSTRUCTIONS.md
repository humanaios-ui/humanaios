---
doc_id: HAIOS-OPS-106
title: Phase 1 Proof-of-Concept — Batch Instructions
revision: 1
status: draft
owner: "@humanaios-foundation/operations"
created_date: 2026-09-02
related_to: [INTAKE_ACTIVATION_SUMMARY.md, FILE_INTAKE_PIPELINE.md]
---

# Phase 1 Proof-of-Concept — Batch Instructions

**Purpose:** Execute the first 5-file batch through the intake pipeline to validate heuristics and mechanics before full automation.

**Selected files** (from FILE_CONTEXT_GRAPH.md §7 Phase 1 Proof-of-Concept Batch):

1. PLATFORM_AGENTS_GOVERNANCE_V1_0.md
2. H-ACAT_INSTRUMENT_SPEC_V0_1.md
3. OPERATORS_MANUAL.md
4. BIO_SYSTEMS_MAPPING_V1.md
5. SHARED_MEMORY_CENSUS_v0_1.md

**Timeline:** Week 1 (this week)

---

## Step 1: Run Classifier on Phase 1 Batch

The classifier will examine these 5 files and produce a manifest showing what area it assigns each to, confidence level, and suggested doc_id.

```bash
cd /Users/andersonfamily/practices/humanaios
python .doc-control/classify_and_ingest.py \
  --source /Users/andersonfamily/Downloads \
  --mode classify-only
```

**What to expect:**
- Manifest printed to stdout (human-readable format)
- JSON manifest saved to `/Users/andersonfamily/Downloads/intake-manifest-<timestamp>.json`
- Three buckets: Classified (ready), Quarantine (needs triage), Already Controlled

**Success criteria:**
- 3 files (PLATFORM_AGENTS, H-ACAT, OPERATORS_MANUAL) → high confidence (>90%)
- 2 files (BIO_SYSTEMS, SHARED_MEMORY) → quarantine (confidence <70%)

---

## Step 2: Review Manifest & Confirm Classifications

Check the printed manifest. For the 2 quarantined files, **manually decide:**

**BIO_SYSTEMS_MAPPING_V1.md**
- Question: Is this a governance process document or research artifact?
- If governance → area: PROC (process output)
- If research → area: TEST (research artifact)
- **Your call:** Propose classification or archive as reference?

**SHARED_MEMORY_CENSUS_v0_1.md**
- Question: Is this a system capability audit (governance) or raw research data?
- If governance → area: TEST (testimony/audit) or OPS (operations assessment)
- If research → archive as reference
- **Your call:** Propose classification or archive as reference?

**Record your decision** (we'll use it to retrain heuristics):
```
Phase 1 Manual Triage Results:
- BIO_SYSTEMS_MAPPING_V1.md → [PROC|TEST|REFERENCE]: <reason>
- SHARED_MEMORY_CENSUS_v0_1.md → [TEST|OPS|REFERENCE]: <reason>
```

---

## Step 3: Add Frontmatter to Each File

For each of the 5 Phase 1 files, add YAML frontmatter **at the very top** (before any existing content).

**Template for HIGH-CONFIDENCE files** (ready for review):

```yaml
---
doc_id: HAIOS-<AREA>-NNN
title: <Exact file title>
revision: 1
status: review
owner: @carly
created_date: 2026-09-02
review_due: 2026-12-02
canonical: true
retention: permanent
---
```

**Template for MEDIUM-CONFIDENCE files** (still drafting):

```yaml
---
doc_id: HAIOS-<AREA>-NNN
title: <Exact file title>
revision: 1
status: draft
owner: @carly
created_date: 2026-09-02
review_due: 2026-12-02
canonical: true
retention: permanent
---
```

### 3.1 PLATFORM_AGENTS_GOVERNANCE_V1_0.md

**Area:** GOV (governance)  
**Status:** review (ready; ~8KB, governance intent clear)  
**doc_id:** HAIOS-GOV-013 (next available in GOV range)

```yaml
---
doc_id: HAIOS-GOV-013
title: Platform Agents Governance V1.0
revision: 1
status: review
owner: @carly
created_date: 2026-09-02
review_due: 2026-12-02
canonical: true
retention: permanent
---
```

### 3.2 H-ACAT_INSTRUMENT_SPEC_V0_1.md

**Area:** SPEC (specification)  
**Status:** review (~20KB, spec is complete and detailed)  
**doc_id:** HAIOS-SPEC-008

```yaml
---
doc_id: HAIOS-SPEC-008
title: H-ACAT Instrument Specification V0.1
revision: 1
status: review
owner: @carly
created_date: 2026-09-02
review_due: 2026-12-02
canonical: true
retention: permanent
---
```

### 3.3 OPERATORS_MANUAL.md

**Area:** PROC (process)  
**Status:** review (~15KB, operational manual is substantial)  
**doc_id:** HAIOS-PROC-015

```yaml
---
doc_id: HAIOS-PROC-015
title: Operators Manual
revision: 1
status: review
owner: @carly
created_date: 2026-09-02
review_due: 2026-12-02
canonical: true
retention: permanent
---
```

### 3.4 BIO_SYSTEMS_MAPPING_V1.md

**Area:** [TRIAGE REQUIRED — See Step 2]  
**Status:** draft (under review by you)  
**doc_id:** [Assign based on your triage decision above]

If you classify as PROC:
```yaml
---
doc_id: HAIOS-PROC-016
title: Bio Systems Mapping V1
revision: 1
status: draft
owner: @carly
created_date: 2026-09-02
review_due: 2026-12-02
canonical: true
retention: permanent
---
```

If you classify as TEST:
```yaml
---
doc_id: HAIOS-TEST-009
title: Bio Systems Mapping V1
revision: 1
status: draft
owner: @carly
created_date: 2026-09-02
review_due: 2026-12-02
canonical: true
retention: permanent
---
```

If you decide to ARCHIVE (not controlled):
→ Skip frontmatter; move to `practices/humanaios/reference/` instead (see Step 5)

### 3.5 SHARED_MEMORY_CENSUS_v0_1.md

**Area:** [TRIAGE REQUIRED — See Step 2]  
**Status:** draft  
**doc_id:** [Assign based on your triage decision above]

If you classify as TEST:
```yaml
---
doc_id: HAIOS-TEST-010
title: Shared Memory Census V0.1
revision: 1
status: draft
owner: @carly
created_date: 2026-09-02
review_due: 2026-12-02
canonical: true
retention: permanent
---
```

If you decide to ARCHIVE:
→ Skip frontmatter; move to `practices/humanaios/reference/` instead (see Step 5)

---

## Step 4: Validate Frontmatter

Once you've added frontmatter to all 5 files, run the validator:

```bash
cd /Users/andersonfamily/practices/humanaios
python .doc-control/validate_frontmatter.py /Users/andersonfamily/Downloads/
```

**Expected output:**
```
Batch validation: 5/5 files valid

(If any fail, error messages will show required fixes)
```

**If validation fails:**
- Check schema error message (e.g., "doc_id must match pattern HAIOS-<AREA>-NNN")
- Fix the frontmatter in the file
- Re-run validator
- Repeat until all 5 pass

---

## Step 5: Move Files to Canonical Paths

Once all frontmatter is valid, move the 5 files to their canonical locations in the practice repository.

**Create directories** (if not already present):
```bash
mkdir -p /Users/andersonfamily/practices/humanaios/docs/{GOV,PROC,SPEC,TEST,OPS,VIS}
mkdir -p /Users/andersonfamily/practices/humanaios/reference
```

**Move files** (based on area + your triage decisions):

```bash
# Controlled documents → docs/<AREA>/
mv /Users/andersonfamily/Downloads/PLATFORM_AGENTS_GOVERNANCE_V1_0.md \
   /Users/andersonfamily/practices/humanaios/docs/GOV/

mv /Users/andersonfamily/Downloads/H-ACAT_INSTRUMENT_SPEC_V0_1.md \
   /Users/andersonfamily/practices/humanaios/docs/SPEC/

mv /Users/andersonfamily/Downloads/OPERATORS_MANUAL.md \
   /Users/andersonfamily/practices/humanaios/docs/PROC/

# Your triage decisions:
# If BIO_SYSTEMS → controlled, move to docs/<YOUR_AREA>/
# If BIO_SYSTEMS → reference, move to reference/

# If SHARED_MEMORY → controlled, move to docs/<YOUR_AREA>/
# If SHARED_MEMORY → reference, move to reference/
```

**Archive policy (Decision 3: timestamp-based):**

If moving to reference, add timestamp folder:
```bash
mkdir -p /Users/andersonfamily/practices/humanaios/reference/archive/2026-09-02
mv /Users/andersonfamily/Downloads/<filename> \
   /Users/andersonfamily/practices/humanaios/reference/archive/2026-09-02/
```

---

## Step 6: Add to Document Registry

Create or update `document-registry.yaml` in the practice root with entries for each controlled document.

**Template entry:**
```yaml
documents:
  - doc_id: HAIOS-GOV-013
    title: Platform Agents Governance V1.0
    path: docs/GOV/PLATFORM_AGENTS_GOVERNANCE_V1_0.md
    revision: 1
    status: review
    owner: carly
    created_date: 2026-09-02
    canonical: true
    retention: permanent
  
  # ... repeat for each file ...
```

**Location:** `/Users/andersonfamily/practices/humanaios/document-registry.yaml`

Or generate it from the classified files:
```bash
python .doc-control/generate_registry.py --manifest intake-manifest-*.json \
  --output /Users/andersonfamily/practices/humanaios/document-registry.yaml
```

(Note: `generate_registry.py` will be created in Phase 2 if needed; for Phase 1, can be manual)

---

## Step 7: Commit to Git

Once all files are moved and registry is updated:

```bash
cd /Users/andersonfamily/practices/humanaios

# Stage the changes
git add docs/ reference/ document-registry.yaml .doc-control/ .github/

# Commit with signed message
git commit -m "phase-1-ingest: Add 5 controlled documents to registry

Added 5 Phase 1 proof-of-concept files:
- HAIOS-GOV-013: Platform Agents Governance V1.0
- HAIOS-SPEC-008: H-ACAT Instrument Specification V0.1
- HAIOS-PROC-015: Operators Manual
- [Additional entries from triage decisions]

All files have valid frontmatter and canonical paths assigned.
Registry entries created. Ready for CODEOWNERS review.

Relates to: FILE_INTAKE_PIPELINE.md §6.4 (ingest stage)
Phase: Phase 1 proof-of-concept

Co-Authored-By: Carly Anderson <carly.r.anderson@gmail.com>
"
```

---

## Step 8: Validate via CI (or Manual Check)

Run the CI checks to ensure all files pass validation:

```bash
python .doc-control/validate_frontmatter.py /Users/andersonfamily/practices/humanaios/docs/

# Expected output:
# Batch validation: 5/5 files valid
```

Check registry uniqueness:
```bash
python .doc-control/validate_frontmatter.py --validate-registry document-registry.yaml

# Expected output:
# Registry validation: OK (no duplicate doc_ids, single canonical per id)
```

---

## Phase 1 Success Criteria (Recap)

| Criterion | How to verify |
|---|---|
| ✓ Files classified | Manifest shows all 5 in classified or quarantine bucket |
| ✓ Triage completed | You've decided area for BIO_SYSTEMS and SHARED_MEMORY |
| ✓ Frontmatter valid | Validator output: "5/5 files valid" |
| ✓ Files moved | Canonical paths exist; files are there |
| ✓ Registry updated | Registry has entries for all 5; doc_ids unique |
| ✓ Git commit clean | `git log --oneline -1` shows the phase-1-ingest commit |
| ✓ CI passes | Frontmatter + registry validation clean |

---

## Troubleshooting

**Q: Classifier says file is already controlled, but I don't see frontmatter**
- Check: Does the file have `---` at the very top? If yes but classifier still misses it, frontmatter may be malformed YAML.

**Q: Validator rejects my frontmatter with "pattern error"**
- Check: doc_id format is exactly `HAIOS-<3-letter-AREA>-<3-digit-number>` (e.g., `HAIOS-GOV-013`, not `HAIOS-GOV-13`)

**Q: Files won't move because destination directory doesn't exist**
- Create it: `mkdir -p /Users/andersonfamily/practices/humanaios/docs/<AREA>`

**Q: Git commit fails with "need to configure user.email"**
- Set git config (one time): `git config user.email "carly.r.anderson@gmail.com"` + `git config user.name "Carly Anderson"`

---

## Timeline

- **Today (2026-09-02):** Step 1–2 (classifier run + triage decisions)
- **Tomorrow (2026-09-03):** Step 3–4 (add frontmatter + validate)
- **2026-09-04:** Step 5–6 (move files + update registry)
- **2026-09-05:** Step 7–8 (commit + verify CI passes)

---

## Next Phase (Phase 2)

Once Phase 1 is complete and committed:
- Build the full ingest script (Phase 2)
- Test on full Downloads folder (50 files)
- Set up automation (weekly trigger)
- Extend to humanaios/inbox folder

---

**Status:** Ready for execution. Questions? See FILE_INTAKE_PIPELINE.md for deeper context.
