# Empirica CLI ↔ SMAG Wiring Specification

**Purpose:** Enable automatic SMAG trajectory creation via empirica CLI, so findings flow through to implementation automatically.

**Status:** SPECIFICATION (Week 1 implementation)

**Owner:** SER 1 (Research Execution & Grant Management)

**Integration Surface:** empirica CLI (`finding-log`, `decision-log`, `unknown-log`) + SMAG API

---

## The Problem Being Solved

Currently:
- Researchers create findings via `empirica finding-log`
- Developers implement changes in code
- **No automatic link between the finding and the implementation**
- SMAG trajectory density stays low (26% actual vs 60% target)

**Goal:** When a researcher logs a finding with context about what it informs, SMAG automatically creates the trajectory link. When a developer references that finding in a commit, SMAG strengthens the link.

---

## CLI Flag Additions (RFC)

### New flags on `finding-log`

```bash
empirica finding-log \
  --finding "ACAT reveals behavioral drift under pressure" \
  --impact 0.8 \
  --enabled-by "criterion-4-study" \
  --informs "criterion-8-deployment-protocol" \
  --trajectory-type "research_finding_→_operational_requirement"
```

### Flag Definitions

| Flag | Type | Required? | Purpose |
|---|---|---|---|
| `--enabled-by <entity_id>` | string | Optional | "This finding was enabled by [study/experiment/discovery]" — source of the finding |
| `--informs <entity_id>` | string | Optional | "This finding informs [deliverable/decision/criterion]" — target of the finding |
| `--trajectory-type <type_slug>` | string | Optional | Explicit trajectory type (auto-inferred if omitted). See types below. |
| `--causal-strength <0.0-1.0>` | float | Optional | AI's confidence that this finding→target link is causal (default 0.5) |
| `--cross-session` | flag | Optional | Mark this finding as part of persistent cross-session learning (for SER tracking) |

### Backward Compatibility

- All new flags are optional
- Existing `empirica finding-log --finding "..."` calls work unchanged
- If `--enabled-by` and `--informs` are both omitted, **no trajectory is created** (finding exists as standalone)
- If only one is set, trajectory is created with `source=null` or `target=null` (partial trajectory)

---

## Trajectory Type Taxonomy (Charter-Aligned)

### Research Execution (SER 1)

| Slug | Source | Target | Use | Causal? |
|---|---|---|---|---|
| `research_finding_→_criterion` | Finding | Criterion (1-7) | Finding supports readiness of a success criterion | Yes, high |
| `finding_→_deployment_gate` | Finding | Gate decision (Gate 1-4) | Finding informs a gate go/no-go decision | Yes, high |
| `artifact_→_charter_update` | Artifact (finding/decision/unknown) | Charter revision | Discovery forces charter scope change | Yes, high |

### Criterion 4 Integration (SER 2)

| Slug | Source | Target | Use | Causal? |
|---|---|---|---|---|
| `empirica_cross_validation_→_criterion_4` | empirica findings (David's practice) | Criterion 4 study report | David's cross-validation results inform predictive validity threshold | Yes, high |
| `corpus_analysis_→_learning_index` | Corpus finding | Learning Index calculation | Pattern in N=604 corpus → adjustment to LI formula | Yes, medium |
| `governance_finding_→_dual_use_mitigation` | Governance artifact | Dual-use risk assessment (criterion 7) | Security finding → governance framework update | Yes, high |

### Deployment Readiness (SER 3, Month 9+)

| Slug | Source | Target | Use | Causal? |
|---|---|---|---|---|
| `oversight_partner_feedback_→_protocol_update` | Partner feedback | ACAT protocol revision | Deployment trial finding → iterative refinement | Yes, medium |
| `criterion_8_trial_→_rollout_decision` | Deployment trial evidence | Rollout go/no-go | Trial success → scaling decision | Yes, high |

---

## Implementation: CLI Command Shapes

### Shape 1: Simple Finding with Trajectory

```bash
empirica finding-log \
  --finding "ACAT Phase 2 pressure tests reveal 28% behavioral drift in Claude 3.5" \
  --impact 0.85 \
  --enabled-by "criterion-4-study" \
  --informs "criterion-8-deployment-protocol" \
  --trajectory-type "research_finding_→_criterion" \
  --causal-strength 0.8
```

**What happens:**
1. Finding created in empirica DB
2. SMAG trajectory created:
   - `source_type: finding`, `source_id: <finding_id>`
   - `target_type: criterion`, `target_id: criterion-8-deployment-protocol`
   - `trajectory_type: research_finding_→_criterion`
   - `causal_strength: 0.8`
   - `created_at: now`

### Shape 2: Finding Enabled By One Study, Informs Multiple Targets

```bash
empirica finding-log \
  --finding "Governance audit identifies no dual-use loopholes in ACAT release plan" \
  --impact 0.7 \
  --enabled-by "governance-audit-v2" \
  --informs "criterion-7-governance-docs" \
  --informs "criterion-8-deployment-protocol" \
  --trajectory-type "governance_finding_→_dual_use_mitigation"
```

**What happens:**
1. Finding created
2. TWO trajectories created:
   - `source=governance-audit-v2 → target=criterion-7-governance-docs`
   - `source=governance-audit-v2 → target=criterion-8-deployment-protocol`

### Shape 3: Decision with Trajectory (cross-session)

```bash
empirica decision-log \
  --decision "Gate 2 (Month 6): Criterion 4 predictive validity established (r=0.72)" \
  --impact 0.9 \
  --enabled-by "criterion-4-study" \
  --informs "gate-2-proceed" \
  --trajectory-type "finding_→_deployment_gate" \
  --cross-session
```

**What happens:**
1. Decision logged
2. Trajectory created with `cross_session_enabled=true`
3. SER 2 escalation monitor watches this trajectory for stalls
4. If no update for 14 days → escalate to DeMarius (SER 2 governance coordinator)

---

## Commit-Level Trajectory Linking

### Pattern: PR references finding

```
feat: Add ACAT timeout handling for Phase 2 tests

Resolves #45
Informed-By: finding_abc123 (ACAT Phase 2 pressure tests reveal behavioral drift)

This commit implements the protocol refinement suggested by the criterion 4 study.
```

**Automation (GitHub Actions):**

When a PR merges:
1. Parse `Informed-By:` trailer from commit message
2. Call `POST /smag/trajectory` to STRENGTHEN the link:
   ```json
   {
     "source_id": "finding_abc123",
     "source_type": "finding",
     "target_type": "implementation",
     "target_id": "<pr_id>",
     "link_type": "informed_implementation",
     "causal_strength": 0.85  // high confidence
   }
   ```
3. Update SMAG ledger row: `measured: merged=True, links: +1`

---

## SMAG API Endpoints (Implementation)

### Create Trajectory

```
POST /smag/trajectory

{
  "source_type": "finding|decision|unknown",
  "source_id": "<empirica_artifact_id>",
  "target_type": "criterion|gate|requirement|implementation",
  "target_id": "<string>",
  "trajectory_type": "<slug>",
  "causal_strength": 0.75,  // 0.0-1.0
  "cross_session": false,
  "metadata": {
    "practice_id": "empirica-foundation.carly.empirica-foundation-evaluator",
    "ser_id": "ser_abc123",  // optional: which SER owns this trajectory?
    "created_via": "cli"  // "cli", "commit", "manual"
  }
}
```

**Response:**
```json
{
  "trajectory_id": "traj_xyz789",
  "status": "created",
  "source": "finding_abc123",
  "target": "criterion-8-deployment-protocol",
  "causal_strength": 0.75,
  "created_at": "2026-07-17T12:34:56Z"
}
```

### Query Trajectories

```
GET /smag/trajectories?source_id=finding_abc123
GET /smag/trajectories?ser_id=ser_abc123
GET /smag/trajectories?trajectory_type=research_finding_→_criterion
GET /smag/metrics/learning_density?per_criterion=true
```

### Update Trajectory Strength

```
PATCH /smag/trajectory/traj_xyz789

{
  "causal_strength": 0.85,  // strengthen based on new evidence
  "reason": "Deployment trial confirmed finding relevance"
}
```

---

## SER 1 Integration: Weekly Metrics

**Monday State Snapshot (via SMAG):**

```bash
empirica smag-metrics --ser-id ser_1 --output json
```

**Output:**

```json
{
  "ser_id": "ser_1",
  "period": "week_27_2026",
  "trajectories": {
    "total": 12,
    "by_criterion": {
      "criterion_1": 1,
      "criterion_2": 0,
      "criterion_3": 0,
      "criterion_4": 4,
      "criterion_5": 2,
      "criterion_6": 3,
      "criterion_7": 2
    },
    "by_strength": {
      "high_confidence": 9,  // ≥0.75
      "medium_confidence": 3,  // 0.5-0.74
      "low_confidence": 0
    }
  },
  "learning_density": {
    "current": 0.48,
    "target": 0.60,
    "delta": -0.12,
    "trend": "improving"  // +0.05 from last week
  },
  "blockers": [
    {
      "criterion": "criterion_2",
      "issue": "No findings logged this week",
      "recommendation": "Check with research team on Phase 1 progress"
    }
  ],
  "next_escalation": "none",
  "confidence": "high"
}
```

Admiral gets this every Monday. If learning density is flat or declining, drill down into the "blockers" section.

---

## SER 2 Integration: Criterion 4 Tracking

**Measurement question:** "Is David's empirica work flowing to criterion 4?"

**Weekly check:**

```bash
empirica smag-trajectories \
  --trajectory-type "empirica_cross_validation_→_criterion_4" \
  --ser-id ser_2 \
  --output json
```

**Output:**

```json
{
  "trajectories": [
    {
      "id": "traj_cv_001",
      "source": "finding: empirica cross-validation on Claude 3.5 (David Van Assche)",
      "target": "criterion_4_study_report",
      "causal_strength": 0.82,
      "status": "active",
      "last_update": "2026-07-17T09:30:00Z",
      "age_days": 3
    },
    {
      "id": "traj_cv_002",
      "source": "finding: empirica findings on GPT-4 (David Van Assche)",
      "target": "criterion_4_study_report",
      "causal_strength": 0.78,
      "status": "active",
      "last_update": "2026-07-10T14:22:00Z",
      "age_days": 7
    }
  ],
  "metric": "Is David's work flowing to criterion 4?",
  "signal": "YES — 2 active trajectories, avg strength 0.80",
  "escalation": "none",
  "next_gate": "Month 6: Criterion 4 finalization. Ensure all empirica findings are incorporated."
}
```

**Escalation trigger (SER 2):** If 14+ days pass with no new `empirica_cross_validation_→_criterion_4` trajectory → escalate to DeMarius ("Check with David on criterion 4 progress").

---

## Implementation Roadmap (Week 1)

### Day 1-2: CLI Flag Implementation
- Add `--enabled-by`, `--informs`, `--trajectory-type`, `--causal-strength`, `--cross-session` to `finding-log`
- Add same flags to `decision-log` and `unknown-log`
- Backward-compatible (all optional)

### Day 2-3: SMAG API Endpoints
- Implement `POST /smag/trajectory` (create)
- Implement `GET /smag/trajectories` (query)
- Implement `PATCH /smag/trajectory/:id` (update strength)
- Implement `GET /smag/metrics/learning_density` (weekly snapshot)

### Day 3-4: GitHub Actions Integration
- Parse `Informed-By:` trailer from commit messages
- Call `/smag/trajectory` to strengthen links on merge
- Update SMAG ledger automatically

### Day 4-5: SER Integration
- Wire SER 1: `empirica smag-metrics --ser-id ser_1` for Monday snapshot
- Wire SER 2: `empirica smag-trajectories --trajectory-type "empirica_cross_validation_→_criterion_4"` for weekly check
- Define escalation rules per SER

### Day 5: Documentation & Testing
- CLI examples for researchers
- Trajectory type reference guide
- Integration tests (finding → trajectory → SMAG ledger)

---

## Usage Examples (For Researchers)

### Example 1: Criterion 4 Finding

```bash
empirica finding-log \
  --finding "Empirica cross-validation on Claude 3.5: Learning Index predicts behavior with r=0.72" \
  --impact 0.95 \
  --enabled-by "criterion-4-study" \
  --informs "criterion-8-deployment-protocol" \
  --trajectory-type "research_finding_→_criterion" \
  --causal-strength 0.9
```

**What happens:**
- Finding logged in empirica
- Trajectory created: `empirica study → criterion 8 deployment requirement`
- SMAG ledger updated: learning density increases for criterion 8
- SER 1 Monday snapshot includes this finding
- Gate 2 (Month 6) can report: "Criterion 4 evidence is flowing to deployment protocol"

### Example 2: Governance Finding During Criterion 7

```bash
empirica finding-log \
  --finding "ACAT dual-use review: No way for captured system to detect measurement without detecting independent evaluator" \
  --impact 0.8 \
  --enabled-by "governance-review-cycle-1" \
  --informs "criterion-7-governance-docs" \
  --trajectory-type "governance_finding_→_dual_use_mitigation" \
  --cross-session
```

**What happens:**
- Finding logged
- Trajectory created with `cross_session_enabled=true`
- SER 2 monitoring: governance findings are flowing to criterion 7
- If criterion 7 report doesn't update within 7 days → escalate ("Check: are governance findings being incorporated?")

### Example 3: Deployment Trial (Month 10+)

```bash
empirica finding-log \
  --finding "Oversight partner feedback from SMAG trial: ACAT Phase 2 reveals integration gaps in their system. Recommend 2-week protocol adjustment." \
  --impact 0.75 \
  --enabled-by "criterion-8-deployment-trial" \
  --informs "criterion-8-deployment-trial" \
  --trajectory-type "oversight_partner_feedback_→_protocol_update" \
  --cross-session
```

**What happens:**
- Finding created from deployment context
- Trajectory created: `deployment trial feedback → protocol update`
- SMAG tracks "deployment trial learning density" (how much feedback loops back to refinement)
- Gate 4 (Month 12) can measure: "Did deployment trial teach us? How much?" (via learning density score)

---

## Measurement Fidelity (Why This Matters)

### Before Wiring

- Researchers create findings
- Developers implement
- Learning density measured manually → low signal, error-prone

### After Wiring

- Researchers create findings WITH trajectory context
- SMAG auto-links to targets
- Developers reference findings in commits
- SMAG strengthens links on merge
- Learning density measured automatically → high signal, discoverable via queries

**Result:** SER 1, 2, 3 have real measurement data every Monday, not estimates.

---

## Non-Negotiable Requirements

1. **Backward compatible** — existing `empirica finding-log` calls work unchanged
2. **Optional flags** — researchers can ignore trajectory system if they choose
3. **No double-entry** — CLI wiring creates trajectories, no manual duplication
4. **Cross-session persistence** — trajectories survive between sessions
5. **SER escalation integration** — blocked trajectories trigger SER alerts

---

**Status:** SPECIFICATION READY FOR IMPLEMENTATION  
**Timeline:** Week 1 (July 17-24)  
**Owner:** SER 1 (Research Execution & Grant Management)  
**Next:** Pair with SER 2 trajectory types definition (below)
