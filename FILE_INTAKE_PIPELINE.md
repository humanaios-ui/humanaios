---
doc_id: HAIOS-OPS-101
title: File Intake Pipeline — Operational Activation
revision: 1
status: draft
owner: "@humanaios-foundation/operations"
created_date: 2026-09-02
---

# File Intake Pipeline — Operational Activation

**Purpose:** Convert the DOCUMENT_CONTROL_PLAN.md governance (P0 audit complete, phases P1-P6 defined) into an executable, repeatable intake process that routes scattered files into the controlled-document system.

**Scope:** humanaios ecosystem files currently scattered across `/Downloads`, `/Desktop/HAIOS-Main`, `/Desktop/humanaios`, and orphaned practice folders. Integrates with empirica transaction discipline for traceability.

---

## 1. Current State Assessment

| Location | Item Count | File Types | Status |
|---|---|---|---|
| `/Downloads` | ~50 files | MD, YAML, JSON, PDF, PY | **Active intake** — user-placed, unclassified |
| `/Desktop/humanaios/inbox` | ~101 files | Mixed | **Backlog** — accumulated, unreviewed |
| `/Desktop/HAIOS-Main` | 8 subdirs | Multiple | **Staging** — from older imports |
| `/practices/humanaios/` | 20+ files | MD, YAML, JSON | **Canonical** — already under control |

**Problem:** Three parallel intake flows (Downloads, inbox, HAIOS-Main) with no systematic routing. Files manually asked about by name. Orphaned folders exist; no audit trail when they were created or why.

**Objective:** One unified intake funnel; automated classification; traceable routing to either:
1. **Controlled registry** (doc_id issued, frontmatter added, canonical location set)
2. **Workspace reference** (supporting materials, no control needed, linked via project)
3. **Archive** (obsolete, reference-only, marked superseded)
4. **Quarantine** (unclassifiable, requires human triage)

---

## 2. File Classification Schema

Every file entering the pipeline is asked three questions. Answers determine routing.

### 2.1 Question 1: Is this a controlled document?

**Definition:** A controlled document is one that:
- Governs operations, decisions, standards, or compliance
- Has an identified owner/approver
- Will be referenced by others (within or across teams)
- Requires version history and approval record

**Answer options:**
- **Yes → Route to CONTROL INTAKE** (will receive doc_id, frontmatter, registry entry)
- **No → Route to REFERENCE INTAKE** (will be tagged, linked, archived)
- **Unclear → QUARANTINE** (defer to human triage)

### 2.2 Question 2: If controlled — what functional area owns this?

**Areas** (from DOCUMENT_CONTROL_PLAN.md):
- `GOV` — governance, policies, decision frameworks
- `PROC` — processes, runbooks, procedures
- `VIS` — vision, strategy, roadmaps
- `TEST` — testimony, findings, research logs
- `TL` — timelines, milestones, schedules
- `OPS` — operations, infrastructure, deployment
- `F/H/IC` — existing research class IDs (kept as-is)

**Answer:** Selects the area code for `doc_id` scheme (e.g., `HAIOS-GOV-013`).

### 2.3 Question 3: Is this document ready for approval, or still drafting?

**Options:**
- **Ready to approve** → `status: review` (will be routed for CODEOWNERS approval)
- **Still drafting** → `status: draft` (added to registry, owner notified to refine)
- **Reference only** → `status: archived` (supporting material, not governed)

**Answer:** Sets initial state in frontmatter + registry.

---

## 3. Intake Pipeline Stages

```
ENTRY (user places file)
  ↓
STAGE 1: CLASSIFY (Q1–Q3 answered)
  ├─→ Controlled? Yes → STAGE 2: INGEST
  ├─→ Controlled? No  → STAGE 5: ARCHIVE
  └─→ Unclear        → STAGE 6: QUARANTINE
  ↓
STAGE 2: INGEST (frontmatter added, doc_id assigned)
  ├─→ Ready to approve? → STAGE 3: REVIEW_GATE
  ├─→ Still drafting   → STAGE 4: OWNER_NOTIFY
  └─→ Error (bad meta) → STAGE 6: QUARANTINE
  ↓
STAGE 3: REVIEW_GATE (CODEOWNERS approval required)
  └─→ Approved → MOVE_CANONICAL + REGISTRY_ADD → DONE
  └─→ Rejected → STAGE 4: OWNER_NOTIFY (return to draft)
  ↓
STAGE 4: OWNER_NOTIFY (notify owner; await action)
  └─→ Owner refines → recycle to STAGE 1
  └─→ Owner abandons → STAGE 6: QUARANTINE
  ↓
STAGE 5: ARCHIVE (reference file; tag & link)
  └─→ Add to workspace reference index → DONE
  ↓
STAGE 6: QUARANTINE (human review required)
  └─→ Triage & re-route → recycle to STAGE 1
```

---

## 4. Empirica Integration (Making It Auditable)

**Why integration matters:** The DOCUMENT_CONTROL_PLAN is governance; this pipeline is praxis. Without tying intake to empirica's transaction/artifact layer, the process becomes a parallel system that inevitably drifts.

### 4.1 Transaction Model

Each intake run is **one transaction** per file or file batch:

```
PREFLIGHT
  objective: "Ingest file: <filename>"
  claims: [
    "Classified as: <area>-<type>",
    "Owner assigned: <owner>",
    "Ready for approval: yes/no"
  ]
  ↓
CHECK (gates praxic moves)
  "Can I assign doc_id, add frontmatter, move canonical?"
  ↓
PRAXIC WORK
  1. Add frontmatter with doc_id + metadata
  2. Move to canonical location (or link if reference)
  3. Add to document-registry.yaml
  4. Commit with signed message
  5. Log finding: "File ingested: <doc_id>"
  ↓
POSTFLIGHT
  resource_accounting:
    human_labor: N/A (mostly automated)
    ai_tokens_used: ~2-5k per file
  what_changed:
    doc_id_issued: HAIOS-<area>-NNN
    frontmatter_valid: yes
    registry_entry: added
  next: "Route to CODEOWNERS if status=review"
```

### 4.2 Artifact Logging (Per Constitution §III-b)

| Artifact Type | When | What to Log |
|---|---|---|
| **finding** | File ingested successfully | `"File classified and ingested: <doc_id>, owner=<owner>, status=<status>"` |
| **decision** | Area assignment chosen | `"Routed to area: <HAIOS-AREA> based on functional scope"` |
| **unknown** | Can't classify | `"Unclassifiable file: <filename>. Reason: <why>"` → QUARANTINE |
| **assumption** | Inferring file purpose | `"Assumed <file> belongs to area <X>; owner may correct"` |

**Edges matter:** Link each finding to:
- The original file (if stored as reference)
- The doc_id (if issued)
- Prior intake decisions (creates audit trail)

---

## 5. Automated Classification Heuristics

Not every file needs human triage. Most can be classified by pattern.

### 5.1 Strong signals → Automatic `Yes, controlled`

**File content:**
- Contains YAML frontmatter with `doc_id:` field → already controlled, just update
- Title includes "PROTOCOL", "SPEC", "CHARTER", "POLICY", "PROCEDURE", "STANDARD" → controlled
- Contains `status: approved` and `approved_by:` → already controlled

**File metadata:**
- Filename starts with one of the area prefixes (`GOV_`, `PROC_`, `VIS_`, etc.) → route to that area
- File size > 5KB and mentions "RFC", "review", "approval", "governance" → likely controlled
- In `practices/humanaios/` already → controlled (likely already registered)

### 5.2 Strong signals → Automatic `No, reference`

- File is code (`.py`, `.js`, `.sh`) without governance intent → reference only
- File is a log, dump, or data export (`.json`, `.csv`, `.log`) → reference only
- File title includes "example", "draft", "scratch", "temp", "test" → reference/archive
- File < 1KB and is a config snippet or single measurement → reference only

### 5.3 Gray zone → `Unclear, quarantine`

- File title ambiguous (e.g., "findings.md" — findings of what process?)
- Multiple document types mixed in one file (governance + research + data)
- File appears complete but missing author/date metadata
- File references external decisions not in the repo

---

## 6. Execution (The Repeatable Process)

### 6.1 Trigger: When to run the pipeline

**Option A: On-demand** (user says "please classify the Downloads folder")
```bash
empirica intake-run --source /Users/andersonfamily/Downloads \
  --mode classify-only  # just bucket; no moves
```

**Option B: Scheduled** (weekly, matches audit cadence from DOCUMENT_CONTROL_PLAN)
```bash
# in .empirica/project.yaml or via cron:
empirica intake-run --source /Users/andersonfamily/Downloads \
  --mode full  # classify → ingest → route
```

**Option C: Continuous** (watch the folder; on new file, classify within 1 hour)
```bash
# Setup:
empirica intake-watch --source /Users/andersonfamily/Downloads \
  --debounce 60s  # wait 60s after last file added before run
```

### 6.2 What the `intake-run` command does

**Input:** Source folder path, mode (classify-only | full | archive-only)

**Process:**
1. Scan source for new files (diff against last-run manifest)
2. For each file:
   - Extract text + metadata (filename, size, creation date)
   - Run classification heuristics (§5)
   - If confident → auto-classify (skip Q1–Q3)
   - If uncertain → create quarantine entry (defer Q1–Q3)
3. Generate intake report (classified files, quarantine bucket, counts)

**Output:** Manifest file (JSON, timestamped) listing:
```json
{
  "run_timestamp": "2026-09-02T14:30:00Z",
  "source": "/Users/andersonfamily/Downloads",
  "files_scanned": 50,
  "classified": [
    {
      "filename": "PLATFORM_AGENTS_GOVERNANCE_V1_0.md",
      "classification": {
        "controlled": true,
        "area": "GOV",
        "inferred_doc_id": "HAIOS-GOV-013",
        "confidence": 0.95,
        "reason": "Title contains GOVERNANCE; size > 5KB; governance scope clear"
      },
      "status": "ready_for_ingest",
      "owner_inferred": "@humanaios-foundation/governance"
    }
  ],
  "quarantine": [
    {
      "filename": "mac-tuneup.sh",
      "reason": "Code file; no governance intent detected",
      "classification": "likely_reference",
      "action": "auto-archive (high confidence)"
    }
  ],
  "already_controlled": [
    "12_TRADITIONS_COMPLIANCE_AUDIT.md",  # already in registry
  ]
}
```

### 6.3 Human verification step

**Before moves happen, the manifest is shown to the user:**

```
Intake Manifest Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Classified (ready to ingest): 42 files
   ✓ Auto-confidence > 90%: 38 files (proceed)
   ? Auto-confidence 70–90%: 4 files (review before ingest)

📦 Quarantine (needs triage): 5 files
   • mac-tuneup.sh (code, no governance)
   • research-log-raw.csv (raw data, no structure)
   • [3 others]

✓ Already registered: 3 files
   (no changes needed)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next steps:
  1. Review the 4 low-confidence items (see below)
  2. Triage quarantine (keep/archive/reclassify)
  3. Run: empirica intake-confirm --manifest-id <uuid> --action proceed
```

User is shown the low-confidence items for a quick yes/no, then proceeds.

### 6.4 The ingest step

Once approved:

```bash
empirica intake-confirm --manifest-id <uuid> --action proceed \
  --overrides '{"filename": "example.md", "area": "PROC"}'  # if user overrode
```

Then for each file:

```bash
# 1. Add frontmatter (if not already present)
empirica doc-add-frontmatter --file /path/to/file.md \
  --doc_id HAIOS-GOV-013 \
  --owner "@humanaios-foundation/governance" \
  --area GOV

# 2. Move to canonical location
mv /Downloads/PLATFORM_AGENTS_GOVERNANCE_V1_0.md \
   /practices/humanaios/docs/GOV/PLATFORM_AGENTS_GOVERNANCE_V1_0.md

# 3. Add to registry
empirica registry-add --doc_id HAIOS-GOV-013 \
  --path docs/GOV/PLATFORM_AGENTS_GOVERNANCE_V1_0.md \
  --status draft \
  --owner "@humanaios-foundation/governance"

# 4. Commit with signing
git add docs/GOV/PLATFORM_AGENTS_GOVERNANCE_V1_0.md document-registry.yaml
git commit -m "ingest: HAIOS-GOV-013 Platform Agents Governance

  doc_id: HAIOS-GOV-013
  area: GOV
  owner: @humanaios-foundation/governance
  status: draft (awaiting approval)
  source: /Downloads/PLATFORM_AGENTS_GOVERNANCE_V1_0.md

  Log: empirica finding-log --finding 'File ingested: HAIOS-GOV-013'"
```

---

## 7. Integration with Document Review Gate

Once in the registry with `status: draft`, the file lifecycle continues:

```
User → reads file, verifies content → opens PR to set status=review → 
CODEOWNERS approval required (branch protection) → 
approval record created → merged with status=approved → 
file is now "live" (referenced, cited, governed)
```

The intake pipeline stops at `status: draft` (file is safe, in registry, but not yet approved). The DOCUMENT_CONTROL_PLAN's review/approval gates take it from there.

---

## 8. Hardcoding the Control into humanaios System

**This pipeline is not a one-off tool—it's a standing operational layer.** To hardcode it:

### 8.1 Add to `.empirica/project.yaml`

```yaml
ai_id: humanaios
# ... existing config ...

file_intake:
  enabled: true
  sources:
    - path: /Users/andersonfamily/Downloads
      frequency: on-demand  # or: weekly, continuous
      action_on_classify: quarantine_unconfident  # or: auto_archive_ref
    - path: /Users/andersonfamily/Desktop/humanaios/inbox
      frequency: weekly
      action_on_classify: auto_archive_ref
  
  classification:
    heuristics_confidence_threshold: 0.80
    auto_archive_low_confidence: false  # require human yes/no
  
  registry:
    path: document-registry.yaml
    validate_on_merge: true
```

### 8.2 Add to workflow (GitHub Actions or empirica loop)

```yaml
# .github/workflows/intake.yml (run weekly)
name: Document Intake Pipeline
on:
  schedule:
    - cron: '0 9 * * MON'  # Monday 9am
  workflow_dispatch:

jobs:
  intake:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run intake pipeline
        run: |
          empirica intake-run \
            --source /Users/andersonfamily/Downloads \
            --manifest-output intake-manifest-${{ github.run_id }}.json
      - name: Upload manifest as artifact
        uses: actions/upload-artifact@v3
        with:
          name: intake-manifest
          path: intake-manifest-*.json
```

### 8.3 Add to empirica loop

```bash
# .empirica/project.yaml
loops:
  - name: document-intake-monitor
    kind: interval
    interval: 1w  # weekly
    description: "Classify and ingest scattered documents into controlled registry"
    command: |
      empirica intake-run --source /Users/andersonfamily/Downloads --mode full
      empirica intake-run --source /Users/andersonfamily/Desktop/humanaios/inbox --mode full
```

---

## 9. Metrics & Success Criteria

| Metric | Target | Current | Owner |
|---|---|---|---|
| Downloads backlog size | < 10 files (new items) | ~50 | intake monitor |
| humanaios/inbox pending | 0 (weekly drain) | 101 | owner-notify cycle |
| Registry coverage | 100% of approved docs | ~90% (pre-ingest) | mesh-support |
| Intake latency (new file → classified) | < 24 hours | manual, unbounded | automation |
| Classification accuracy (auto) | > 95% | N/A (new) | heuristic tuning |

---

## 10. Rollout Plan (Minimal Viable Process)

**Phase 0 (Now):** Design ✓ (this document)

**Phase 1 (Week 1):** Proof of concept
- Manually classify one batch from Downloads using the schema (§2)
- Generate sample manifest (§6.2)
- Demo to user; get feedback

**Phase 2 (Week 2):** Automate classification
- Build heuristics (§5) and classifier script
- Add frontmatter templates
- Test on 10 files; iterate

**Phase 3 (Week 3):** Full pipeline
- Wire ingest steps; test move + registry update + commit
- Add branch protection to operations repo
- Run full intake on Downloads folder

**Phase 4+:** Hardcode
- Add to `.empirica/project.yaml`
- Set up weekly automation
- Monitor; extend to other source folders

---

## 11. Questions for User/Team

Before full activation, confirm:

1. **Ownership:** Is `mesh-support` the right maintainer for the registry + monitor, or should it be `humanaios` core?
2. **Approval bottleneck:** Who are the CODEOWNERS for each area (GOV, PROC, VIS, OPS, etc.)? Should approvals be delegated?
3. **Retention policy:** Downloads backlog — archive everything older than 60 days? Or keep indefinitely (at risk of re-accumulation)?
4. **Desktop folders:** Should HAIOS-Main and humanaios orphaned folders be reconciled into practice paths, or archived?
5. **Frequency:** Weekly intake-run, or on-demand (user triggers)? Schedule determines resource allocation.

---

**Status:** Draft, awaiting feedback on scope + ownership questions above.

**Next:** Phase 1 proof-of-concept on a representative batch from Downloads (Carly selects 3-5 files to manually classify as demo).
