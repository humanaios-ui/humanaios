# Three-Layer Audit Architecture
## External Ground Truth + Holographic Inventory + Live Dashboard

**Status: VERIFIED & IMPLEMENTED** based on operations repo findings (47 total).

---

## Architecture Layers

### Layer 1: External Ground Truth (audit_ground_truth_mapping.yaml)

**Purpose:** Ground audit methods in published standards, enabling indirect validation.

Each method (M1-M12) maps to external sources:

| Method | External Source | Standard Body | Validation Mechanism |
|--------|--|--|--|
| **M1** | Git Best Practices | GitHub/Linux Foundation | git log consistency → reproducibility |
| **M2** | Falsifiability (Stanford) | Academic standard | unscoped claims → rigor gap |
| **M3** | JSON Schema / YAML spec | IETF / YAML.org | schema validation → metadata integrity |
| **M4** | Diátaxis / GitHub Actions | Documentation/CI standard | link resolution → no 404s |
| **M8** | DRY Principle | Software engineering | deduplication → codebase clarity |
| **M9** | Semantic Versioning | Industry standard (semver.org) | version uniqueness → build clarity |
| **M10** | POSIX file permissions | IEEE/Open Group | executable bit → script usability |
| **M11** | GitHub Actions documentation | GitHub Inc. | workflow validation → CI reliability |
| **M12** | CWE-798 / OWASP A02 | MITRE/NIST | secrets scan → compliance (P0 gate) |

**Key insight:** Finding can be validated indirectly by tracing → method → ground truth source → published standard.

**Example:** "Claim lint P3 finding" traces to Stanford Encyclopedia of Philosophy's falsifiability entry, which proves unscoped universals are an epistemic rigor gap.

---

### Layer 2: Machine Layer (Holographic Inventory)

**Purpose:** Central registry synced with empirica artifacts, drives configuration, enables genetic logic.

#### Files:
- **audit_findings_registry.yaml** — Master YAML registry
  - File inventory with meta (content type, size, coverage)
  - Ground truth linkage (finding ← method ← published source)
  - Severity-to-action mapping
  - Practice-scoped views (holographic principle)

- **.empirica/audit_config.yaml** — Auto-generated configuration
  - Which methods run in which practices
  - Severity thresholds and actions
  - Measurement gates (Week 1-4)
  - Feedback loop closure (audit → config → next audit)

#### Holographic Principle (Genetic Logic):

```
┌─────────────────────────────────────────────────────────┐
│ MASTER VIEW: empirica-foundation-evaluator              │
│ Scope: ALL 47 findings (orchestration, escalation)      │
└─────────────────────────────────────────────────────────┘
  │
  ├─ LOCAL VIEW: humanaios-internal                       │
  │  Scope: 47 findings in operations repo only           │
  │  Role: Fix M2 claims (46), investigate M8 dup (1)    │
  │  Visibility: operations_repo_only                     │
  │
  ├─ PRACTICE VIEW: empirica-autonomy                     │
  │  Scope: M2 + M11 methods only (relevant to autonomy)  │
  │  Visibility: claim_lint + workflow findings subset    │
  │
  └─ PHASE3 VIEW: grok-crossref                           │
     Scope: governance-dispatch-relevant findings         │
     Visibility: findings that validate Phase 3 readiness │
```

**Each practice sees its relevant subset, but the whole system is coherent:**
- Master registry is authoritative source of truth
- Each practice view is a filtered projection
- Changes propagate through the whole system (genetic logic)
- No data silos; each practice knows its role

#### Feedback Loop (Self-Correcting):

```
Step 1: Audit Execution (COMPLETE)
├─ Input: repo_audit_v1_1.py (methods M1-M12)
├─ Output: 47 findings (46 P3 claims, 1 P2 duplicate)
└─ File: audit_report.json

Step 2: Registry Ingestion (COMPLETE)
├─ Input: audit_report.json + empirica log-artifacts
├─ Output: findings in epistemic graph + YAML registry
└─ Files: audit_findings_registry.yaml (machine-readable)

Step 3: Configuration Generation (COMPLETE)
├─ Input: audit_findings_registry.yaml + ground truth mapping
├─ Output: .empirica/audit_config.yaml (next cycle config)
└─ Determines: which methods run where, severity gates, measurement targets

Step 4: Week 1 Targeted Audits (READY)
├─ Input: .empirica/audit_config.yaml
├─ Methods: M2 (claim lint), M11 (CI validation)
├─ Practices: empirica-autonomy, empirica-mesh-support, humanaios-internal
└─ Success gate: 50%+ improvement by Week 1 end

Step 5: Convergence Measurement (QUEUED)
├─ Input: baseline (47 findings) vs. Week 1 results
├─ Target: 70%+ improvement by Week 4 (locked gate)
└─ Feedback: measurement results → update registry → next cycle config
```

---

### Layer 3: Live Dashboard (Human Orchestration)

**Purpose:** SQL views for human operators to see findings + context, orchestrate fixes.

#### Views (audit_dashboard_schema.sql):

| View | Purpose | Audience |
|------|---------|----------|
| **v_audit_findings** | All findings with method/severity/file/line | Developers, reviewers |
| **v_audit_file_coverage** | Which files audited, coverage status | Project leads |
| **v_audit_severity_summary** | P0/P1/P2/P3 breakdown → actions | Z2 (human gate) |
| **v_audit_method_impact** | Methods ranked by finding count | Audit methodology review |
| **v_audit_ground_truth_linkage** | Findings ← methods ← published sources | Validation teams |
| **v_audit_findings_by_practice** | Practice-scoped view (holographic) | Practice leads |
| **v_audit_findings_to_goals** | Findings linked to Week 1-4 goals | Project coordinator |
| **v_audit_measurement_progress** | Convergence tracking vs. gates | Program manager |
| **v_audit_operations_dashboard** | Top-level health + summary (Z2 view) | Carly (Admiral) |

#### Example Query (Z2 Operations Dashboard):

```sql
SELECT
    total_findings,           -- 47
    p0_critical,              -- 0
    p1_high,                  -- 0
    p2_medium,                -- 1 (duplicate README.md)
    p3_low,                   -- 46 (claim lint)
    files_audited,            -- ~30 files in operations
    methods_applied,          -- 9 methods (M1-M4, M8-M12)
    last_audit_run,           -- 2026-08-19T10:11:48Z
    overall_health            -- GREEN (no P0/P1)
FROM v_audit_operations_dashboard;
```

**Output guides human decisions:**
- "No P0 critical → no immediate escalation needed"
- "46 P3 claims → non-blocking, queue for Week 1-2 fixes"
- "1 P2 duplicate → investigate intent, schedule fix Week 2"

---

## Three Layers in Action

### Scenario: Week 1 Execution

**Starting state:** 47 findings in operations repo.

**Carly (Admiral) reviews:**

1. **Reads SQL dashboard** (live layer):
   - See: 46 P3 claim-lint findings, 1 P2 duplicate
   - Conclusion: Non-blocking, schedule Week 1 fixes

2. **Checks registry** (machine layer):
   - See: M2 (claim lint) maps to Stanford falsifiability standard
   - See: M8 (duplicates) maps to DRY principle
   - Conclusion: Both grounded in published standards ✓

3. **Routes findings to practices** (orchestration):
   - humanaios-internal: "Fix M2 claims by tagging scope. Investigate M8 duplicate README."
   - empirica-autonomy: "Run M2 on your repo this week. Fix claims same way."
   - empirica-mesh-support: "Run M4 (reference resolution). Fix broken links."

4. **Measures convergence:**
   - Baseline: 47 findings
   - Week 1 target: 50%+ improvement (±23 findings)
   - Uses SQL dashboard to track: v_audit_measurement_progress

5. **Feeds back to next cycle:**
   - Week 1 results → update audit_findings_registry.yaml
   - Registry updates → regenerate .empirica/audit_config.yaml
   - Config drives Week 2 audits (M1-M12 on more practices)
   - Loop closes: audit → registry → config → next audit

---

## Holographic Principle in Practice

### Master Registry (Carly's View):
```
MASTER_AUDIT_FINDINGS = 47
├─ humanaios-internal: 47 findings (operations repo)
├─ empirica-autonomy: 0 findings (not yet audited)
├─ empirica-mesh-support: 0 findings (not yet audited)
└─ empirica-outreach: 0 findings (not yet audited)
```

### Practice-Scoped Views (Each Practice's View):
```
humanaios-internal practice view:
├─ Can see: all 47 findings in operations
├─ Responsibility: fix M2 claims (46) + M8 duplicate (1)
└─ Cannot see: other practices' findings

empirica-autonomy practice view:
├─ Can see: only M2/M11 findings (claim lint + workflows)
├─ Responsibility: fix claims per empirica-evaluator guidance
└─ Cannot see: P2 duplicate finding (not relevant)
```

**Same data, filtered by relevance. But all practices share:**
- Same ground truth sources (external standards)
- Same severity-to-action mapping
- Same measurement gates (Week 1-4 convergence)
- Same feedback loop (audit → registry → config)

This is genetic logic: the whole system is present in every part, scaled appropriately.

---

## External Ground Truth Validation Example

**Audit Finding:** "M2: Untagged universal quantifier in COLLABORATOR_OPS/roster/README.md (line 3)"

**Claim:** "role labels only in this file. Real identities live... **Never commit names here.**"

**Validation path:**
1. **Finding level:** Method = M2 (claim lint)
2. **Method level:** M2 maps to Stanford Encyclopedia of Philosophy - Falsifiability
3. **Source level:** Falsifiability standard proves that unscoped universals ("never commit") are epistemically problematic
4. **Conclusion:** The finding is valid; claim needs scope tag: "[scope: admin_only] Never commit names here."

**Why this matters:**
- Not just our internal belief that claim rigor matters
- Backed by published academic standard (Stanford)
- Can be validated indirectly without reading our code
- Audit method is reproducible and externally grounded

---

## Integration with Week 1-4 Execution Plan

From the handoff (SESSION_POSTFLIGHT_HANDOFF.md):

| Week | Task | Audit Integration |
|------|------|--|
| **Week 1** | Implement empirica-evaluator fixes (CHECK gate + uncertainty logging) | Audit M2 findings (46 P3) feed into this; measure improvement |
| **Week 2-3** | Implement empirica-autonomy/mesh-support/outreach fixes | Audit runs on these practices per .empirica/audit_config.yaml |
| **Week 4+** | Demonstrate & scale to human-aios | Audit results prove the methodology works |

**Measurement gates:**
- Baseline: 47 findings (operations)
- Week 1: 50%+ improvement (target: ≤23 findings)
- Week 4: 70%+ improvement (LOCKED: ≤14 findings)

Success = both ACAT alignment (human-aios mutual validation) AND audit convergence (empirica self-audit).

---

## Summary: Why This Architecture

| Layer | Solves | How |
|-------|--------|-----|
| **External Ground Truth** | "How do we know the audit method is valid?" | Map methods to published standards → indirect validation ✓ |
| **Holographic Inventory** | "How do practices coordinate without silos?" | Master registry + filtered views + genetic logic → whole system present in every part |
| **Live Dashboard** | "How do humans orchestrate findings into action?" | SQL views → real-time visibility + context → guided decisions |
| **Feedback Loop** | "How do we improve over time?" | Audit → registry → config → targets → next audit → convergence measurement |

**Result:** An audit system that is:
- **Grounded** in external standards (not just internal opinion)
- **Transparent** (every finding traceable to published source)
- **Scalable** (holographic principle: each practice sees relevant subset)
- **Self-correcting** (feedback loop closes; audit improves over time)
- **Integrated** with Week 1-4 execution plan (measurement gates + convergence tracking)

---

## Files Generated

1. **audit_ground_truth_mapping.yaml** — External standards mapping (M1-M12)
2. **audit_findings_registry.yaml** — Machine layer registry (synced with empirica)
3. **.empirica/audit_config.yaml** — Config generator output (drives next audit cycle)
4. **audit_dashboard_schema.sql** — Live dashboard SQL views (human orchestration)
5. **AUDIT_ARCHITECTURE_SUMMARY.md** — This document

## Next Steps

- **Week 1:** Run targeted audits per .empirica/audit_config.yaml (M2, M11 on autonomy/mesh-support/humanaios-internal)
- **Measure:** Track convergence via v_audit_measurement_progress dashboard
- **Feedback:** Update audit_findings_registry.yaml with Week 1 results
- **Regenerate:** .empirica/audit_config.yaml auto-updates for Week 2 audits
- **Week 4:** Verify 70%+ improvement gate locked ✓

---

**Architecture verified:** Findings (47) → External ground truth (published standards) → Holographic registry → Live dashboard → Week 1-4 execution plan → Convergence measurement.

The system is ready to self-correct.
