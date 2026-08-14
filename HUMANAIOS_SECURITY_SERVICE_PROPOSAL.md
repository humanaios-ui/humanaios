# Proposal: HumanAIOS as Cross-Repository Security Service

**Status:** ECO-GATED PROPOSAL (awaiting mesh consensus)  
**Proposing Practice:** empirica-foundation.carly.humanaios  
**Target Practices:** empirica-foundation.carly.empirica-autonomy (implementation), empirica-foundation.carly.empirica-governance (policy)  
**Timeline:** Design phase ongoing; implementation Phase 2 pending approval  
**Impact:** Foundation-wide security governance, multi-repo incident orchestration, compliance enablement  

---

## Executive Summary

**Proposal:** Extend humanaios from a single-practice state machine to a **foundation-wide credential lifecycle management service** for multiple repositories.

**Value:**
- Centralized credential tracking (issued → active → rotated → archived)
- Multi-repo secret scanning with unified incident routing
- Governance approval gates for credential access
- Automated cross-repo rotation orchestration via autonomy

**Current State:** Phase 1 (scanning + docs) ✅ complete; Phase 2 (state machine) awaits design consensus

---

## Problem Statement

**Current gaps in Foundation security:**
1. **No credential lifecycle tracking** — Who accessed what credentials? When was the last rotation? Are they still active?
2. **Per-repo duplication** — Each practice implements security scanning independently (humanaios has done this; autonomy/others haven't)
3. **Manual incident response** — When a credential is exposed across repos, notification + rotation is manual/uncoordinated
4. **No central audit trail** — Compliance reports require asking each practice for their logs
5. **Staging vs production confusion** — 2026-08-08 incident: deployment docs labeled "staging" pointed to production (no separation)

**Why HumanAIOS should own this:**
- Already has state machine + governance experience (M2R2 state harmonization)
- Credential lifecycle is a **state machine problem** (not a general utility)
- Positioned to coordinate with autonomy (orchestration) + governance (policy)

---

## Solution: Credential Lifecycle State Machine

### Architecture

```
┌─────────────────────────────────────────────┐
│ HumanAIOS Security Service Layer            │
├─────────────────────────────────────────────┤
│                                             │
│ STATE MACHINE: Credential Lifecycle         │
│ ┌────────────────────────────────────────┐  │
│ │ ISSUED → ACTIVE → ROTATED → ARCHIVED  │  │
│ │          ↓          ↓                  │  │
│ │       [IN-USE]   [COMPROMISED]        │  │
│ └────────────────────────────────────────┘  │
│                                             │
│ EVENTS:                                     │
│ - Credential issued (Supabase, AWS, etc.)  │
│ - Credential compromised (GitGuardian)     │
│ - Rotation triggered (autonomy)            │
│ - Rotation completed (audit log)           │
│ - Credential archived (decommission)       │
│                                             │
│ OUTPUTS:                                    │
│ - Empirica audit log (every transition)    │
│ - Mesh alert routing (priority-escalated)  │
│ - Autonomy trigger (coordinate rotation)   │
│ - Compliance report (for audits)           │
│                                             │
└─────────────────────────────────────────────┘
        ↓                ↓                  ↓
   [Repos]        [Autonomy]        [Governance]
```

### Implementation Phases

| Phase | Deliverables | Effort | Timeline | Gate |
|-------|---|---|---|---|
| **1: Scanning** ✅ | Pre-commit hook, GitHub workflow, docs | 8h | Done (8/8) | n/a |
| **2: State Machine** | Credential schema + state transitions, database migrations, transition webhooks | 24h | 2 weeks | Design consensus |
| **3: Orchestration** | Autonomy integration, rotation workflows, cross-repo triggers | 20h | 2 weeks (after Phase 2) | Autonomy approval |
| **4: Governance** | Approval gates, access control, compliance reporting | 16h | 2 weeks (parallel Phase 3) | Governance approval |

**Resource needs:** humanaios (design + Phase 2), autonomy (Phase 3), governance (Phase 4)

---

## Governance Questions

**These questions determine scope, ownership, and feasibility. Mesh consensus required before Phase 2 starts.**

### 1. **Ownership Model**
**Options:**
- A) Humanaios owns the service end-to-end (state machine + orchestration + governance)
- B) Humanaios owns state machine; autonomy owns orchestration layer; governance owns policy layer
- C) New practice `empirica-security-service` owns everything; humanaios contributes expertise

**Questions for mesh:**
- Who should approve new credentials entering the system?
- Who escalates compromised credentials?
- Who owns the credential rotation SLA?

**Recommendation:** (B) — divides concerns cleanly. Humanaios is epistemic (tracking); autonomy is operational (rotation); governance is policy (approvals).

### 2. **Credential Scope**
**What credentials does the service track?**

**Options:**
- A) Only database credentials (PostgreSQL, MongoDB)
- B) All secrets (DBs + API keys + private keys + tokens)
- C) Only Foundation-managed credentials (exclude personal GitHub tokens, etc.)

**Questions for mesh:**
- Should it track GitHub credentials? AWS credentials? 1Password vault tokens?
- Do we need per-credential access control, or just audit trail?

**Recommendation:** (B) for security coverage; (C) for governance scope — track what the organization manages, not personal credentials.

### 3. **Trust Boundaries**
**Who can read/rotate credentials?**

**Options:**
- A) Only credential owners (repo admin) can rotate
- B) Governance + autonomy can trigger rotation (with approval gates)
- C) Autonomy can rotate in emergency (compromised credential) without approval

**Questions for mesh:**
- Should we have a "break-glass" emergency rotation path?
- Who audits the auditors (who accesses the audit log)?

**Recommendation:** Combination—normal path: owner triggers via autonomy (B). Emergency path: governance + 2-factor approval (C).

### 4. **Multi-Repo Coordination**
**How do we handle credentials shared across repos?**

Example: Supabase production password used by humanaios-ui + autonomy + website.

**Options:**
- A) Maintain one credential record + alert all repos when rotated
- B) Each repo maintains its own copy (less coordination, more duplication)
- C) Centralized vault (rotate once, all repos fetch updated credential)

**Questions for mesh:**
- Should repos use a credential manager (1Password, Vault) or env vars?
- Who owns the credential master copy?

**Recommendation:** (C) — centralized vault (autonomy pulls latest on deploy). Reduces rotation complexity.

### 5. **Staging vs Production Separation**
**Should we enforce separate credentials per environment?**

Current state: single Supabase instance; no staging tier.

**Questions for mesh:**
- Should humanaios-ui + autonomy + website have separate staging DBs?
- Who provisions staging infrastructure?
- What's the SLA for staging ↔ prod promotion?

**Recommendation:** Separate credentials. Governance policy: "Staging and prod must have distinct credentials + access control."

---

## Mesh Coordination Model

### Participants & Roles

| Practice | Role | Responsibility |
|---|---|---|
| **humanaios** | `required` | State machine design + maintenance; credential lifecycle model; audit log integration |
| **autonomy** | `required` | Rotation orchestration; credential provisioning; cross-repo triggers |
| **governance** | `required` | Access control policy; approval gates; compliance audits |
| **mesh-support** | `participating` | Cross-foundation communication; routing incident alerts to repo owners |

### Decision Gates

| Gate | Who Decides | Format |
|---|---|---|
| **Design Phase** | humanaios + autonomy + governance consensus | Mesh collab thread + design doc |
| **Phase 2 Start** | humanaios (with autonomy/governance sign-off) | ECO-gated proposal (this one) |
| **Phase 3 Start** | autonomy + humanaios | Autonomy proposes implementation plan |
| **Phase 4 Start** | governance + humanaios | Governance proposes policy framework |

### Escalation Path

- **Blocked > 1 week:** Escalate to mesh-support for coordination
- **Policy disagreement:** Route to governance for arbitration
- **Unforeseen scope creep:** Defer to next phase + re-plan

---

## Success Criteria

**Phase 1 (Scanning):**
- ✅ Pre-commit hook blocks 100% of hardcoded credential commits
- ✅ GitHub workflow detects secrets on PR
- ✅ Documentation complete

**Phase 2 (State Machine):**
- Credential state machine handles: issued, active, rotated, archived, compromised
- Database schema + Alembic migrations
- Transition webhooks fire on every state change
- Empirica audit log captures: who, what, when, why

**Phase 3 (Orchestration):**
- Autonomy can trigger password rotation via API
- Cross-repo rotation coordinated (one trigger → multiple repos updated)
- Incident alert routed to affected repo owners

**Phase 4 (Governance):**
- Approval gate: new credentials require governance sign-off
- Access control: who can read/rotate tracked separately
- Compliance report: audit trail exportable for external audits

---

## Timeline & Resources

```
Now (Aug 8)        Phase 2 Design       Phase 2 Build      Phase 3 + 4
         │                │                  │                   │
         ├─ Collab        ├─ 1 week consensus ├─ 2 weeks build  ├─ 2 weeks parallel
         ├─ Governance   │                  │                   │
         │ questions      ├─ Finalize schema │                   │
         │               └─ DB migration    └─ Testing          └─ Compliance
         │                                                         framework
         └─ Auth for                                               
            Phase 2                                                
            (this proposal)                                        

Total: ~6 weeks (with parallelization); gates at each phase
```

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| State machine design has gaps | Medium | High | Early validation via collab thread; iterate before Phase 2 build |
| Autonomy rotation complexity underestimated | Medium | Medium | Allocate extra time in Phase 3; start with simple (password) before complex (key rotation) |
| Governance approvals become bottleneck | Low | Medium | Define clear SLA for approval gates up-front (e.g., "approve within 24h") |
| Cross-repo coordination breaks (one repo fails to pick up new credential) | Low | High | Automated verification step in autonomy: "new credential in all repos within 30m, else escalate" |
| Foundation expands (new practices); design doesn't scale | Medium | Low | Design for N practices from day 1; test with ≥3 practices before "done" |

---

## Questions for Mesh

**Before voting Yes/No/Defer:**

1. **Do you agree this should be a humanaios-owned service?** (or should it be a new practice?)
2. **Which governance questions (above) need resolution before Phase 2 starts?**
3. **Should we start with just database credentials (lower complexity)?**
4. **What's your confidence in the timeline?**
5. **Blockers or constraints we should know about?**

---

## Next Steps

**If approved (ECO: Accept):**
1. Mesh collab on governance questions (1 week)
2. Finalize state machine schema (1 week)
3. Begin Phase 2 development (autonomy + governance coordinate)

**If concerns (ECO: Decline):**
1. Document feedback
2. Revise proposal
3. Re-submit

**If deferred (ECO: Defer):**
1. Mark for revisit
2. Continue Phase 1 scanning rollout
3. Coordinate pre-commit deployment to autonomy (Task 5) while this is in review

---

## Related Artifacts

- **Decision:** "Force-push to remove credential from history (2026-08-08)" — motivating incident
- **Finding:** "Production credential exposed in deployment docs" — scope trigger
- **Proposal:** "HumanAIOS pre-commit deployment to autonomy" (pending autonomy response)
- **Spec:** SECURITY_SCANNING.md (humanaios) — foundation for Phase 1

---

**Proposal ID:** prop_humanaios_security_service_2026_08_08  
**Status:** ECO-GATED (awaiting Accept/Decline/Defer)  
**Proposer:** empirica-foundation.carly.humanaios  
**Mesh Owners:** autonomy, governance  

Co-Authored-By: Claude Code <claude@anthropic.com>
