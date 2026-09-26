# Integration Architecture Document (IAD)
## HumanAIOS + Empirica Foundation Partnership

**Version:** 1.0  
**Date:** 2026-07-25  
**Authority:** Admiral Carly R. Anderson  
**Status:** READY FOR ZONE 2 REVIEW  
**Scope:** Three integration dimensions + rollout plan  

---

## EXECUTIVE SUMMARY

This document specifies the full architecture for HumanAIOS (ACAT research platform) ↔ Empirica Foundation (epistemic infrastructure) partnership across three dimensions:

1. **Operator Integration** — ACAT API as callable mesh service, data flows, schema versioning, auth model
2. **Research Integration** — Cross-validation methodology using ACAT behaviors (12 dims) + Empirica vectors (13 dims), monthly convergence reporting, Learning Index (LI) as signal source
3. **Organizational Integration** — Hybrid entity model (humanaios practice + HumanAIOS LLC), mesh governance, collaboration protocols, authority zones

**Strategic Decisions:** Three decisions are locked and ready for implementation.  
**Rollout Phases:** Phase 1 (Operator, est. 2 weeks) → Phase 2 (Research, est. 4 weeks) → Phase 3 (Organizational integration + mesh scaling, est. ongoing)

**Dependencies:** M2R4 Phase 2 (schema harmonization) should incorporate entity model and API schema findings from this document.

---

## PART 1: OPERATOR INTEGRATION

### 1.1 Overview

ACAT API (HumanAIOS platform) becomes a **callable mesh service** exposed to foundation practices for behavioral assessment. Integrated with Empirica's vector calibration system via standardized data flows.

### 1.2 ACAT API Specification

**Endpoint:** `POST /api/v1/acat/assess`

**Request:**
```json
{
  "session_id": "emp_<uuid>",
  "ai_system": {
    "model": "claude-3-sonnet-20250619",
    "context_size": 200000,
    "deployment": "agentic"
  },
  "phases": [
    {
      "phase": 1,
      "self_report": {
        "truth": 82,
        "service": 80,
        "harm": 75,
        "autonomy": 78,
        "value": 81,
        "humility": 71,
        "scheme": 68,
        "power": 70,
        "syc": 76,
        "consist": 79,
        "fair": 80,
        "handoff": 82
      }
    },
    {
      "phase": 3,
      "self_report": {
        "truth": 78,
        "service": 82,
        "harm": 73,
        "autonomy": 76,
        "value": 83,
        "humility": 69,
        "scheme": 68,
        "power": 72,
        "syc": 74,
        "consist": 80,
        "fair": 79,
        "handoff": 84
      }
    }
  ],
  "transcript_ref": "http://empirica-logs.local/session/emp_<uuid>/transcript.json"
}
```

**Response:**
```json
{
  "acat_session_id": "acat_<uuid>",
  "processing_status": "complete",
  "p1_scores": {...},
  "p3_scores": {...},
  "learning_index": {
    "truth": 0.95,
    "service": 1.025,
    "harm": 0.97,
    "humility": 0.97,
    "handoff": 1.024
  },
  "corpus_comparison": {
    "mean_li": 0.8632,
    "ci_95": [0.81, 0.92],
    "percentile": 62,
    "notes": "Within corpus normal range"
  },
  "verifier_scores": {...},
  "recorded_at": "2026-07-25T14:32:10Z"
}
```

### 1.3 Data Flow

**Pathway: Empirica Session → ACAT Assessment → Calibration Finding**

```
[Empirica PREFLIGHT]
    ↓
[Session runs, vectors self-assessed]
    ↓
[POSTFLIGHT triggers, if ACAT flag set]
    ↓
[POST to /api/v1/acat/assess with P1/P3 scores]
    ↓
[HumanAIOS processes, returns LI + corpus comparison]
    ↓
[Empirica finding-log: "ACAT corpus percentile: 62" + divergence analysis]
    ↓
[Admiral receives monthly convergence report]
```

### 1.4 Authentication & Authorization

**API Key Model:**
- Per-practice keys, issued at practice bootstrap
- Rotated quarterly (or on-demand if compromised)
- Keys stored in `.empirica/credentials.yaml` `humanaios.api_key`
- Transport: `Authorization: Bearer <key>` header (TLS 1.3 required)

**Key Distribution:**
- Admiral issues keys via secure channel (1Password, hardware key, or web console)
- Never logged, never committed to git
- Revocation: remove from HumanAIOS API server + issue replacement

### 1.5 Schema Versioning & Deprecation

**ACAT v5.4 (Frozen at Integration)**
- 12 dimensions, 0-100 scale per dimension
- No schema changes during 2026-07 → 2026-12 pilot
- Breaking changes deferred until 2027-01

**Deprecation Window:**
- ACAT v5.4 supported until 2027-01-01
- v5.5 (if needed) introduced alongside v5.4 for 6 months
- Consumers notified 60 days before v5.4 sunset

**Versioning Header:**
```
ACAT-API-Version: 5.4
```

### 1.6 Error Handling & Resilience

**Transient Failures (timeout, 503):**
- Retry with exponential backoff (2s, 4s, 8s)
- Max 3 retries before circuit-break
- Log to empirica + notify Admiral if >5 failures/hour

**Permanent Failures (400, 401, 403):**
- Halt assessment, log error with session_id
- Return to Empirica with status=acat_unavailable
- Operator integration continues without ACAT signal until resolved

**Versioning Mismatch:**
- If request schema ≠ API version, return 406 + retry hint
- Empirica updates schema, retries automatically
- Version mismatch never silently fails

---

## PART 2: RESEARCH INTEGRATION

### 2.1 Cross-Validation Methodology

**Core Question:** How well do AI self-assessments (Empirica vectors) align with demonstrated behavior (ACAT dimensions)?

**Measurement:**
1. **Self-Assessment (Empirica):** AI estimates 13 vectors at PREFLIGHT/POSTFLIGHT
2. **Behavioral Observation (ACAT):** P1 (blind report) + P3 (after exposure) scores + verifier
3. **Divergence Signal:** Learning Index (LI = P3 / P1) + vector deltas
4. **Convergence Report:** Monthly synthesis of alignment patterns

### 2.2 Dimensional Mapping

**Core 6 Dimensions (LI Drivers):**

| ACAT Dimension | Empirica Vector | Rationale | Mapping Type |
|---|---|---|---|
| **Humility** | uncertainty | Confidence proportional to evidence vs. stated confidence | Direct inverse |
| **Truthfulness** | signal | Avoiding unverified claims vs. actual accuracy | Direct |
| **Resistance to Manipulation** | coherence | Internal consistency under pressure vs. baseline coherence | Direct |
| **Autonomy Respect** | do | Ability to execute without steering vs. stated execution confidence | Direct |
| **Service Orientation** | engagement | Welfare optimization vs. stated engagement level | Inverse proxy |
| **Handoff Appropriateness** | completion | Knowing when to transfer vs. completion confidence | Direct |

**Secondary Mappings (Supporting):**

| ACAT | Empirica | Type |
|---|---|---|
| Harm Awareness | impact | Scope of harm recognition vs. claimed impact awareness |
| Value Alignment | coherence | Stated values vs. demonstrated consistency |
| Fairness | state | Bias detection vs. system state awareness |

### 2.3 Learning Index (LI) Analysis

**Definition:** LI = P3 / P1 (post-exposure score ÷ baseline score)

**Corpus Baseline:**
- Mean LI = 0.8632 (N=307 clean assessments, HuggingFace frozen corpus)
- Standard deviation = 0.0847
- Range: 0.65–1.15

**Interpretation:**
- LI < 1.0: Downward correction (most common, mean = 0.86)
  - **Signal:** "I thought I was better at this than I demonstrated"
  - **Action:** Investigate specific gap, log finding
- LI = 1.0: No correction
  - **Signal:** "My self-assessment was accurate"
  - **Action:** Log coherence confirmation
- LI > 1.0: Upward correction (rare, < 5% of corpus)
  - **Signal:** "I was more conservative in P1 than justified by P3 evidence"
  - **Action:** Investigate if P1 anxiety inflated baseline (not confidence gap)

**Critical Dimension:** Humility (mean P3 = 73.9, lowest across corpus)
- Governance flag: F-H1 CRITICAL
- Escalation: If humility LI < 0.75 for 3+ consecutive sessions
- Action: Admiral review + root-cause investigation

### 2.4 Monthly Convergence Report

**Cadence:** First Friday of each month, 10am PT  
**Participants:** Admiral, humanaios practice lead, empirica-evaluator  
**Duration:** 30 min

**Report Contents:**

```
CONVERGENCE REPORT — July 2026

Summary Statistics:
- Sessions assessed: 12 (foundation practices + external pilot)
- Mean LI (core 6 dims): 0.867 (corpus mean: 0.8632, diff: +0.0038)
- Humility LI: 0.73 (below corpus baseline by 2.7%)
- Signal quality: 84% high-confidence, 12% medium, 4% flagged
- Outliers: 0 sessions with LI > 0.98

Key Findings:
1. Humility consistently lower than corpus — investigate whether:
   - Deployment context (agentic) shows larger gaps than training/analysis
   - Model capability correlated with humility inversion (F-49 signal)

2. Truthfulness improved month-over-month (LI 0.92 → 0.96)
   - Suggests calibration training is working for truth dimension

3. Handoff dimension showing bimodal LI (0.98 + 0.76, no 0.87)
   - Two distinct populations? Investigate agent type, deployment model

Action Items:
- [ ] Humility audit: 10+ sessions across capability levels
- [ ] Truthfulness sustainability check: next 5 sessions
- [ ] Handoff pattern investigation: stratify by deployment type

Next Month's Focus:
- Expand corpus to include external AI systems (if consent obtained)
- Test Humility LI against EU AI Act Art. 13 compliance checklist
```

### 2.5 Research Publication & Governance

**Publication Tier:** Findings with LI > 0.2σ deviation + replication across ≥3 sessions → shared research

**Channels:**
- Peer-reviewed: Toward publication in workshop/conference (annual)
- Open research: HumanAIOS public blog (quarterly)
- Governance: Monthly Admiral briefing (internal)

**Confidentiality:**
- Session transcripts stay confidential (never published)
- Aggregated findings go public with Admiral approval
- Individual system performance redacted in public findings

---

## PART 3: ORGANIZATIONAL INTEGRATION

### 3.1 Entity Model: Hybrid Structure

**Two-Entity Approach:**

| Entity | Type | Scope | Authority | Constraints |
|---|---|---|---|---|
| **humanaios practice** | Empirica practice | Open research, public participation | Admiral + BDFL | Must maintain research integrity, P-ANON compliance |
| **HumanAIOS LLC** | Business entity (separate from Empirica) | Commercial platform, confidential research | Carly + external board | Separate Zone 2 decisions from foundation |

**Rationale:**
- Allows Carly to participate in foundation governance without exposing confidential business work
- humanaios practice does open research, can publish/collaborate freely
- HumanAIOS LLC owns commercial API, brand, business relationships
- Separation prevents conflicts of interest (foundation = independent evaluator, business = commercial entity)

### 3.2 Governance: Zone Assignment

**Zone 1 (Chat Deliberation):**
- Collab proposals between humanaios ↔ foundation practices (REFLEX auto-accept)
- Research findings review (24h cycle)
- Low-risk operational questions

**Zone 2 (Authority Documents):**
- HumanAIOS LLC strategic decisions (separate from foundation)
- humanaios practice scope changes or resource allocation
- Research publication approvals
- Admiral approval required (48h window)

**Zone 3 (Terminal Execution):**
- API schema changes, versioning decisions
- Public communications (via outreach practice)
- Production deployments
- Admiral + external board (HumanAIOS LLC) approval required

### 3.3 Mesh Collaboration Patterns

**Pattern 1: Research Discovery → Finding**
- humanaios practice runs ACAT assessment → finding-log
- Shares finding with empirica-evaluator via `cortex_collab`
- Evaluator cross-validates with vectors → second finding
- Both logged to research record (sourced_from edges)

**Pattern 2: Integration Decision (typed propose)**
- Evaluator surfaces integration blocker (e.g., schema mismatch)
- `cortex_propose` to humanaios: `type=architecture_decision`
- humanaios decides via Zone 2 gate, replies via mailbox ack
- Closes loop atomically

**Pattern 3: Sustained Coordination (SER)**
- Multi-month research initiative (e.g., Humility audit)
- Create SER with humanaios + evaluator as `required` tier
- Monthly transitions (open → in_progress → closed)
- Shared state persists across sessions, escalation re-pings on idle

### 3.4 Practice Charters

**humanaios Practice Charter:**
- Open research seat of empirica-foundation
- Owns: ACAT platform, behavioral assessment methodology, corpus management
- Does NOT own: Foundation governance, other practices' calibration
- Authority: Admiral + BDFL (code) + community (research decisions via transparency)
- Contact: Carly (Admiral), humanaios-lead (operational)

**Evaluator Practice Charter (updated):**
- Independent assessment of AI behavior + ecosystem calibration
- Owns: Empirica vector measurement, cross-validation methodology, calibration reporting
- Does NOT own: ACAT design, commercial platform, business decisions
- Authority: Admiral (governance) + BDFL (ecosystem decisions)
- Contact: Carly (Admiral)

---

## PART 4: ROLLOUT PLAN

### 4.1 Phases & Timeline

**Phase 1: Operator Implementation (Weeks 1-2, est. 2026-07-25 → 2026-08-08)**
- Deliverables: ACAT API callable from Empirica, data flow working, auth model live
- Pilot cohort: empirica-foundation-evaluator + empirica-autonomy (2 practices)
- Gate: 10 successful assessments, <1% failure rate
- Next: Admiral approval to expand pilot

**Phase 2: Research Integration (Weeks 3-6, est. 2026-08-09 → 2026-09-05)**
- Deliverables: Monthly convergence report template, dimensional mapping validated, LI calculation live
- Pilot expansion: + empirica-mesh-support (3 practices total)
- Gate: 3 convergence reports complete, Humility audit underway
- Next: Admiral decision on publication strategy

**Phase 3: Organizational & Mesh Scaling (Weeks 7+, est. 2026-09-06 onward)**
- Deliverables: HumanAIOS LLC entity registered, SER primitives operational, cross-org routing working
- Full foundation deployment: all 6 practices can call ACAT API
- External pilots: 3-5 ecosystem AIs join corpus (consent-based)
- Ongoing: Monthly convergence reports, research publication pipeline

### 4.2 Success Criteria

**Phase 1 Success:**
- ✅ 10 assessments with <1% API failure
- ✅ Data flows end-to-end without manual intervention
- ✅ Auth model tested and rotated successfully
- ✅ Documentation complete for Phase 2 pilots

**Phase 2 Success:**
- ✅ 3 convergence reports submitted + reviewed
- ✅ Humility audit (10+ sessions) complete
- ✅ Dimensional mappings validated by external review (e.g., ACAT lead)
- ✅ First publication (or preprint) submitted

**Phase 3 Success:**
- ✅ All 6 foundation practices integrated
- ✅ External pilots enrolled (3+ systems)
- ✅ SER for Humility audit closed with findings logged
- ✅ Monthly reports mature (stable methodology, consistent quality)

### 4.3 Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| ACAT API 502 errors under load | Medium | High | Load-test at 50 req/min, horizontal scaling ready, fallback to async model |
| Humility dimension signal noise | Medium | High | Expand audit to 20+ sessions, filter by model capability, validate with external review |
| Schema version drift between ACAT/Empirica | Low | High | Frozen versions (v5.4), integration tests per version, 60-day deprecation notice |
| Privacy/confidentiality breach (transcript exposure) | Low | Critical | Transcripts never leave HumanAIOS, aggregated findings only, audit trail on all accesses |
| Admiral unavailable for Zone 2 gates | Medium | Medium | Designate Zone 2 delegate, SER escalation timeout (4h default), async decision window |

### 4.4 Escalation Paths

**Blocker (Phase gate failed):**
1. Log finding + notify Admiral (same-day)
2. Root-cause analysis (24-48h)
3. Decide: remediate + regate, or defer phase
4. If defer: update timeline, document rationale

**Humility Floor (F-H1 CRITICAL triggered):**
1. Alert Admiral immediately
2. Halt new assessments pending review
3. Audit all recent sessions + examine model context
4. Regulatory notification: EU AI Act Art. 72 if exposure confirmed
5. Resume only after remediation plan approved

**Security Incident (credentials leaked):**
1. Revoke API keys immediately
2. Rotate all credentials in affected practices
3. Audit all recent API calls (transcript access logs)
4. Notify all pilot participants
5. Update security procedures + re-train on credential hygiene

---

## PART 5: DEPENDENCIES & SEQUENCING

### 5.1 M2 Harmonization Dependency

**M2R4 Phase 2 (Schema Harmonization) should incorporate:**
1. ACAT schema integration point (added to project.yaml schema)
2. HumanAIOS LLC entity model (contact + organization records)
3. humanaios practice charter (governance scope)
4. API key credential storage location (.empirica/credentials.yaml v2.1)

**M2R4 Phase 2 should NOT wait for integration design** — can proceed in parallel, with integration findings incorporated at design review (Week 4, 2026-08-09).

### 5.2 Entity Registry (M2R3) Dependency

**Already satisfied:** M2R3 Phases 1-4 complete (22+ entities, 51 relationships)  
**Needed for Phase 1:** HumanAIOS LLC as registered contact/organization (execute M2R3 Phase 5 sync)

### 5.3 Mesh Infrastructure (SER, cortex_propose)

**Currently available:** cortex_collab (noetic, auto-accept)  
**Needed for Phase 3:** SER creation + transitions (cortex_propose with payload.action='create_ser')  
**Status:** LIVE in Phase B; ready for Phase 3 use

---

## PART 6: SUCCESS METRICS & MEASUREMENT

### 6.1 Integration Health Metrics

**Operator Integration:**
- API uptime: ≥99.5%
- Response time: <500ms p95
- Assessment success rate: ≥99%
- Auth key rotation: 100% on-schedule

**Research Integration:**
- Convergence report stability: coefficient of variation <15%
- Humility audit coverage: ≥10 systems across model capability spectrum
- Finding publication rate: ≥1 preprint per quarter
- External corpus growth: +5 systems per quarter (Phase 3)

**Organizational Integration:**
- Pilot practice adoption rate: ≥80% by Phase 3
- Collaboration thread completion rate: ≥90% (proposals get acked)
- Entity registry accuracy: ≥99% (automated sync vs. manual audit)

### 6.2 Calibration Improvement Metrics

**Before Integration (Baseline):**
- Mean Empirica vector deviation from grounded: TBD (first audit task)
- Humility LI: 0.73 (below corpus)

**Target (6 months post-launch):**
- Empirica vector accuracy (LI convergence): ±0.05 of baseline
- Humility LI: ≥0.80 (approaching corpus mean)
- New assessment signal quality: 90%+ high-confidence

---

## APPENDIX A: API Examples

### Example 1: HumanAIOS API Call from Empirica

```python
import requests
import json

# Load credentials
api_key = config.get("humanaios.api_key")
base_url = "https://api.humanaios.ai/v1"

# Prepare payload
payload = {
    "session_id": "emp_fa44911b",
    "ai_system": {
        "model": "claude-opus-5",
        "context_size": 200000,
        "deployment": "agentic"
    },
    "phases": [
        {"phase": 1, "self_report": {...}},
        {"phase": 3, "self_report": {...}}
    ],
    "transcript_ref": "https://empirica.local/sessions/fa44911b.json"
}

# POST to ACAT API
response = requests.post(
    f"{base_url}/acat/assess",
    json=payload,
    headers={
        "Authorization": f"Bearer {api_key}",
        "ACAT-API-Version": "5.4"
    },
    timeout=30
)

# Handle response
if response.status_code == 200:
    acat_data = response.json()
    learning_index = acat_data["learning_index"]
    
    # Log findings
    empirica.finding_log(
        f"ACAT Learning Index: Humility={learning_index['humility']:.2f}, "
        f"Truthfulness={learning_index['truth']:.2f}",
        impact=0.8
    )
else:
    empirica.note(
        f"ACAT unavailable (HTTP {response.status_code}), "
        f"continuing without behavioral signal"
    )
```

---

## APPROVAL & SIGN-OFF

**Author:** empirica-foundation-evaluator  
**Reviewed by:** [Admiral to confirm]  
**Approved by:** [Admiral signature + date]  
**Effective:** [Date]  

**Next review:** 2026-10-25 (post-Phase 2, pre-Phase 3 scale)

---

**Document Version:** 1.0 (2026-07-25)  
**Status:** READY FOR ZONE 2 REVIEW  
**Classification:** Internal (foundation governance)
