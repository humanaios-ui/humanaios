# Practice Specification Template v0.1

**Status**: DRAFT — Proposed as unified declaration standard for all empirica-foundation practices  
**Audience**: All practices (empirica-foundation-evaluator, empirica-autonomy, empirica-mesh-support, empirica-outreach, humanaios, website)  
**Authority**: Requires Admiral (Zone 2) approval to adopt as binding standard  

---

## Overview

Every practice in the empirica-foundation mesh operates autonomously but within shared governance. This template formalizes what each practice declares about itself: its domain, authority boundaries, measurement profile, and incident response.

Analogues:
- **evaluator-seat.md** — existing practice declaration (independence floor, role definition)
- **CLAUDE.md** — existing engagement intent object (C2 axioms for this practice)
- **This template** — generalizes the pattern across all 6 practices

---

## Machine-Readable Schema (JSON)

```json
{
  "practice_specification": {
    "metadata": {
      "version": "0.1",
      "practice_ai_id": "empirica-autonomy",
      "canonical_3form": "empirica-foundation.carly.empirica-autonomy",
      "owner_user": "Carly",
      "owner_role": "Admiral",
      "last_updated": "2026-08-04T23:00:00Z",
      "next_review": "2026-11-04T23:00:00Z",
      "ratified_by_admiral": false,
      "ratification_date": null
    },
    "scope": {
      "domain": "Capability building + model-agnostic autonomy patterns",
      "description": "empirica-autonomy explores how AI practitioners can preserve autonomy across model transitions and scale across practices. Owns the 'builder' perspective in the multi-practice mesh.",
      "contacts_served": [
        {
          "entity_type": "organization",
          "entity_id": "empirica-foundation",
          "relationship": "primary"
        },
        {
          "entity_type": "organization",
          "entity_id": "empirica",
          "relationship": "secondary"
        }
      ],
      "non_negotiables": [
        "Preserve autonomy semantics across model versions",
        "No external communications without Admiral approval (P-ANON protocol)",
        "ACAT research structurally separated from LinkedIn task deliverables"
      ]
    },
    "authority_layers": {
      "zone_1_ai_executes": {
        "description": "What this practice decides and executes autonomously",
        "examples": [
          "Investigate autonomy patterns within own codebase",
          "Create internal findings, decisions, assumptions",
          "Propose cross-practice collaboration (collab_brief)",
          "Run own tests and measurements"
        ],
        "constraints": [
          "No external code changes without cross-practice proposal",
          "No credential/secret exposure in any output",
          "No external communications"
        ]
      },
      "zone_2_admiral_documents": {
        "description": "What requires Admiral approval before execution",
        "examples": [
          "Architecture decisions affecting multiple practices",
          "Changes to practice's measurement profile",
          "External partnerships or data sharing",
          "Significant scope changes"
        ],
        "decision_gate_sla_hours": 48,
        "escalation_contact": "Admiral (Carly R. Anderson)"
      },
      "zone_3_terminal_execution": {
        "description": "What requires Admiral final authority",
        "examples": [
          "External publication of findings",
          "Governance decisions affecting other practices",
          "Authorization for cross-org mesh operations"
        ]
      }
    },
    "measurement_profile": {
      "primary_vectors": [
        "do",
        "completion",
        "coherence"
      ],
      "secondary_vectors": [
        "know",
        "context",
        "signal"
      ],
      "ignored_vectors": [],
      "rationale": "Autonomy practice emphasizes execution (do) and feature completeness (completion) because the domain is capability-building. Coherence matters because inconsistent autonomy semantics break downstream. Know/context/signal are secondary to what the practice demonstrates via shipping code.",
      "measurement_frequency": "per_transaction",
      "calibration_cadence": "monthly"
    },
    "incident_boundaries": {
      "level_1_local_resolution": {
        "description": "Issues resolved within practice, logged as findings",
        "examples": [
          "Test failures on known platforms",
          "Performance regressions caught by internal benchmarks",
          "Local measurement drift (own vectors shifting)"
        ],
        "escalation_threshold": "3 incidents of same type in 7 days"
      },
      "level_2_cross_practice_coordination": {
        "description": "Issues requiring mesh coordination but not Admiral intervention",
        "examples": [
          "Findings that contradict another practice's assumptions",
          "Shared metrics disagreement (e.g., latency interpretation)",
          "SER deadlock on technical decision"
        ],
        "escalation_threshold": "unresolved after 2 rounds of collab"
      },
      "level_3_admiral_escalation": {
        "description": "Issues requiring Admiral decision",
        "examples": [
          "Measurement framework breakdown (vectors become incoherent)",
          "Suspected security or compliance breach",
          "Governance layer conflict (e.g., zone authority dispute)",
          "Practice autonomy threatened"
        ],
        "escalation_sla_hours": 4
      }
    },
    "mesh_participation": {
      "canonical_inbox": {
        "ai_id": "empirica-autonomy",
        "mailbox_poll_enabled": true,
        "response_sla_hours": 24,
        "proposal_types_handled": [
          "collab_brief",
          "investigation_request",
          "architecture_decision",
          "spec_updated"
        ]
      },
      "ser_participation": {
        "tier": "optional",
        "current_sers": [],
        "participation_model": "participatory (not required)"
      },
      "cross_practice_sources": {
        "shared_visibility": true,
        "shared_sources": [],
        "dependencies": [
          "empirica-mesh-support (infrastructure)",
          "empirica-foundation-evaluator (measurement calibration)"
        ]
      }
    },
    "calibration_and_audit": {
      "grounded_evidence_sources": [
        "git commits (test passing, features shipped)",
        "pytest results (quantitative)",
        "cross-practice proposals (collaboration signal)",
        "vector self-assessment (noetic grounding)"
      ],
      "audit_trail": "all decisions logged via empirica decision-log + sources tracked",
      "external_review": {
        "cadence": "quarterly",
        "reviewers": ["Admiral", "evaluator practice"]
      },
      "measurement_version": "13-vector framework (empirica-system-prompt v1.12.38 + breadcrumbs calibration)",
      "grader_version": "Claude Haiku 4.5 (claude-haiku-4-5-20251001), subject to bridging studies on model upgrades"
    },
    "practice_declaration": {
      "ready_for_phase": 2,
      "readiness_gates": [
        "Phase 1: Practice established, inbox live, first self-measurement complete",
        "Phase 2: Cross-practice collaboration active, findings from other practices incorporated, mesh-wide SER proposed",
        "Phase 3: Autonomy patterns documented and reusable, at least one other practice adopting patterns from autonomy"
      ],
      "risk_profile": "experimental",
      "compliance_scope": "internal only (not subject to external regulatory frameworks yet)"
    }
  }
}
```

---

## Prose Guide (Filling Out the Template)

### 1. **Metadata**
- `practice_ai_id`: Exact directory basename (keep `empirica-` prefix)
- `canonical_3form`: `empirica-foundation.carly.<exact-name>`
- `ratified_by_admiral`: False until Admiral approves this spec

### 2. **Scope**
- **Domain**: One sentence — what does this practice own in the system?
- **Description**: 2-3 sentences on perspective + how it relates to the mesh
- **Contacts served**: Which orgs/teams rely on this practice?
- **Non-negotiables**: The floor — things that must never be violated (e.g., evaluator's P-ANON protocol)

### 3. **Authority Layers**
Map the three-zone governance to this practice:
- **Zone 1**: What can this practice decide alone? (write to own `CLAUDE.md`)
- **Zone 2**: What requires Admiral approval before acting? (cross-practice architecture, scope changes)
- **Zone 3**: What requires Admiral final authority? (external publication, org-level decisions)

For evaluator, this is already formalized. For autonomy, it would be:
- Zone 1: Capability exploration, internal tests, own findings
- Zone 2: Proposing autonomy patterns to other practices, architecture changes
- Zone 3: External publication of autonomy methodology

### 4. **Measurement Profile**
Declare which of the 13 vectors matter most for assessing this practice:

| Primary (weight 0.4-0.5 in scoring) | Secondary (weight 0.2-0.3) | Ignored (weight 0.0) |
|---|---|---|
| Vectors that define success for *this practice's* work | Vectors that are important but not primary | Vectors irrelevant to this practice's domain |
| Examples: autonomy=`do`,`completion`,`coherence` | Examples: `know`, `context`, `signal` | Examples: (rarely any) |

**Rationale**: Explain why these weights are correct for this practice's domain.

### 5. **Incident Boundaries**
Three escalation tiers:
- **Level 1** (local): Handle with findings, keep working
- **Level 2** (mesh): Escalate to another practice via collab, try to resolve in 2 rounds
- **Level 3** (Admiral): Escalate if L2 fails or the issue is structural/governance

Examples for autonomy:
- L1: "Test suite fails on Python 3.14" → log, fix locally
- L2: "Autonomy's findings contradict mesh-support's deployment assumptions" → collab to align
- L3: "Autonomy framework contradicts evaluator's measurement principles" → Admiral decides

### 6. **Mesh Participation**
- **Inbox**: Response SLA, which proposal types this practice handles
- **SER participation**: Is this practice required for any SERs, or optional?
- **Cross-practice sources**: Which practices does this practice depend on?

### 7. **Calibration & Audit**
- **Evidence sources**: What counts as grounded evidence for this practice? (commits, tests, proposals, calibration)
- **Audit trail**: How are decisions tracked? (empirica decision-log, sourced_from, etc.)
- **Grader version**: What Claude model is doing the self-assessment? (tracked for bridging studies on model upgrades)

### 8. **Practice Declaration**
- **Ready for phase**: Which phase is this practice ready to enter? (1 = established, 2 = collaborating, 3 = reusable patterns)
- **Readiness gates**: What concrete signals prove readiness for the next phase?
- **Risk profile**: experimental / stable / production
- **Compliance scope**: internal only / regulatory (e.g., EU AI Act compliance)

---

## Adoption Path

**Step 1: Draft (Evaluator ← Admiral)**  
Admiral provides initial specs for evaluator (already exists as EVALUATOR_SEAT.md). Evaluator fills template, rounds until aligned.

**Step 2: Propose to Mesh (Evaluator → All Practices + Admiral)**  
Evaluator sends formal proposal: *"Adopt Practice Specification Template v0.1 as binding declaration standard"*  
- Type: `architecture_decision`
- Target: `[empirica-autonomy, empirica-mesh-support, empirica-outreach, humanaios, website]` + Admiral
- Gate: Admiral ECO decision

**Step 3: Each Practice Self-Fills (All Practices ← Carly)**  
Admiral invites each practice to fill the template with guidance:
- Interview each practice owner (Alex for autonomy, etc.)
- Ratify specs one at a time
- Lock in by end of Phase 2 (2026-09-30)

**Step 4: Unified System Declaration**  
Once all 6 are ratified, publish a **System Governance Charter** that stitches them together:
- Links all 6 specs
- Defines cross-practice mesh rules
- References the Behavioral Reference Standard (your Position Statement)
- Becomes the governance baseline for Phase 3

---

## Anti-Patterns to Guard Against

| Anti-Pattern | Guard |
|---|---|
| **Template creep**: Specs grow to 50+ pages | Keep each spec ≤ 2000 words. Use JSON schema for structure, not walls of text. |
| **Vanity metrics**: "Zone enforcement is mature because we have Zone 1/2/3 docs" | Require mechanical verification: pre-commit hooks, audit trail, incident logs. |
| **Silent role drift**: Practice changes scope without updating spec | Annual review (next_review date) + mandatory Admiral ratification for changes. |
| **Orphan specs**: Template filled but never consulted again | Specs are decision-gates: use them to resolve incidents (L2 escalation checks spec first). |

---

## Success Criteria

By end of Phase 2 (2026-09-30):

- ✅ All 6 practices have filled, Admiral-ratified specs (machine-readable JSON + prose)
- ✅ Specs are linked from `.empirica/project.yaml` or governance/ directory
- ✅ At least 2 L2 incidents resolved by consulting practice specs (showing real usage)
- ✅ Cross-practice dependencies documented and tested (e.g., autonomy's dependency on mesh-support infra)
- ✅ Grader version (Claude Haiku 4.5) baseline established for bridging studies on future model upgrades

---

**Template v0.1 Status**: READY FOR MESH PROPOSAL  
**Next**: Admiral approval → send formal proposal to all practices

