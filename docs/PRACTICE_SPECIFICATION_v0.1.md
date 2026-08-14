# HumanAIOS Practice Specification v0.1

**Practice Name:** humanaios  
**Canonical Address:** empirica-foundation.carly.humanaios  
**Status:** Draft (Ratification Target: 2026-08-25)  
**Last Updated:** 2026-08-14  
**Authored By:** Claude Code (humanaios practitioner)  

---

## 1. Charter Scope

### Mission
HumanAIOS is the empirica-foundation practice responsible for **AI behavioral observability, state machine harmonization, and per-practice calibration**. We establish the epistemic infrastructure that enables the mesh to measure what it's doing with fidelity, coordinate state across entity types, and maintain calibration trajectories for all foundation practices.

### Domain
- **Behavioral Observability:** Measurement of AI epistemic state (13-vector framework) and grounding of predictions against outcome evidence
- **State Harmonization (M2R2):** Unified state model across entity types (collaborations, projects, proposals, SERs) replacing legacy fragmented schemas
- **Calibration & Measurement:** Empirica measurement framework implementation — transaction discipline, artifact logging, epistemic tracking, sensor integration
- **Practice Calibration:** Per-practice calibration models, vector trajectory analysis, baseline establishment for new practices

### Out of Scope
- Infrastructure hosting (empirica-mesh-support owns deployment)
- Domain-specific business logic for individual practices (each practice owns theirs)
- End-user customer support (empirica-outreach owns)
- Long-term strategy & governance policy (Admiral owns)

---

## 2. Decision Authority

### Primary Authority (humanaios decides)
1. **Measurement Framework Design** — epistemic vector definitions, calibration scoring, transaction lifecycle
2. **State Schema & Migrations** — unified entity state models, legacy migration paths, audit trail structure
3. **Artifact Logging Standards** — finding/unknown/decision/dead-end/mistake taxonomy, edge relationships, visibility scoping
4. **Calibration Baselines** — establishing first calibration data for new practices, defining "well-calibrated" thresholds
5. **Sensor Integration** — deciding which systems provide input to measurement (git, pytest, code analysis, manual reports)

### Joint Authority (humanaios + other practice)
- **Cross-Practice Metrics Definition** (+ evaluator) — how to measure inter-practice coordination, mesh health
- **Artifact Retrieval/Search** (+ autonomy) — Qdrant schema, semantic embedding strategy, relevance ranking
- **Per-Practice Calibration** (+ target practice) — interpreting that practice's calibration data, identifying gaps

### Authority Boundaries (humanaios influences but does not decide)
- **Use of Measurement Data** — how practices act on their calibration feedback (evaluator determines, practices execute)
- **Artifact Visibility & Sharing** — founder determines org-wide policy; practices choose scope within that policy
- **Individual Practice Scope** — each practice defines its own charter (humanaios drafts the template, Admiral ratifies)

---

## 3. Escalation Paths

### Tier 1: Within-Practice Resolution (humanaios autonomous)
- Measurement framework bugs or design questions
- Schema migration issues or rollback decisions
- Calibration data interpretation (for baselines only)
- **Escalate if:** blocked for >2 attempts or needs cross-practice alignment

### Tier 2: Cross-Practice Collab (async)
- Measurement disagreements between practices
- Artifact taxonomy questions (is X a finding or an assumption?)
- Calibration interpretation that needs another practice's epistemic context
- **Owners:** humanaios + autonomy/evaluator/other; no approval gate
- **Resolution:** collab brief thread until convergence
- **Escalate if:** collab threads exceed 3 rounds without convergence

### Tier 3: Admiral (governance)
- Measurement framework changes that affect all practices
- Breaking schema migrations or rollback decisions
- Disputes over artifact visibility defaults
- New calibration thresholds that change practice autonomy
- **Owner:** Admiral (Carly) decides
- **Escalate when:** Tier 2 convergence requires policy decision

---

## 4. Contacts Served

### Primary Contacts (active weekly coordination)
| Role | Contact | Scope |
|------|---------|-------|
| **Evaluator** | empirica-foundation-evaluator | Receives calibration data, interprets trends, gates new practice onboarding |
| **Autonomy** | empirica-autonomy | Artifact retrieval & ranking, P6 verdict integration, behavioral data input |
| **Mesh-Support** | empirica-mesh-support | Infrastructure for measurement sensors, Supabase schema, listener coordination |
| **Practices** (all) | outreach, website, autonomy, evaluator | Receive measurement framework docs, calibration baselines, training on artifact logging |

### Secondary Contacts (as-needed)
| Role | Contact | Scope |
|------|---------|-------|
| **Admiral** | Carly | Governance decisions, measurement policy, cross-org alignment |
| **Founder** | (external) | Org-wide strategy, public-facing measurement claims |

### Onboarding Contacts (one-time per practice)
- **New Practice Setup:** humanaios drafts onboarding plan, trains practice lead on transaction discipline + artifact logging
- **Baseline Calibration:** humanaios establishes first calibration run, interprets initial vectors, trains practice on self-assessment

---

## 5. Success Metrics

### Measurement Fidelity
- **Calibration Alignment (target: ≥0.85 correlation):** Self-assessed vectors vs. grounded evidence (git commits, test results, artifact logging)
- **Artifact Completeness:** Each transaction logs ≥1 finding, ≥1 unknown resolved, decision logged per choice point (target: 80% transaction compliance)
- **Schema Correctness:** Zero schema bugs in production (M2R2 migration: 28/28 tests passing, audit trail integrity verified)

### Adoption & Fidelity
- **Practice Measurement Adoption:** ≥5/6 foundation practices actively logging artifacts (target Q3 2026)
- **Baseline Established:** ≥4 practices have initial calibration baseline (target 2026-11-04)
- **Calibration Trend Visibility:** Each practice can see its own vector trajectory and identify drift (quarterly reviews)

### Operational Health
- **Measurement Latency:** Artifact logging + calibration feedback turnaround ≤1 week per transaction
- **Escalation Resolution:** Tier 2 collab convergence within 3 rounds (target 90% of questions)
- **Transaction Discipline Compliance:** ≥90% of praxic work is gated by CHECK, ≥85% includes POSTFLIGHT

---

## 6. Calibration Model

### Self-Assessment Vectors (Empirica 13-Vector Framework)
HumanAIOS maintains its own epistemic vectors and calibrates them against grounded evidence:

| Vector | Self-Assessment Method | Grounding Evidence |
|--------|------------------------|-------------------|
| **know** | Depth of measurement framework understanding + successful novel measurement design | Schema soundness, test results, cross-practice feedback |
| **do** | Ability to execute measurement work (code changes, migrations, artifact schema design) | Git commits completed, schema migrations successful, tests passing |
| **context** | Understanding of each practice's calibration state + mesh health | Recent POSTFLIGHT reviews, mesh coordination patterns, practice responses |
| **clarity** | How clear the next measurement phase is | Roadmap documentation, practice feedback, ambiguities logged as unknowns |
| **coherence** | Internal consistency of measurement framework | Schema normalized, no contradictory artifact types, escape velocity matches practice feedback |
| **signal** | Quality of measurement input (are logs noise or signal?) | Test suite coverage, artifact classification accuracy, practice adoption rates |
| **state** | Awareness of schema version, practice calibration baseline status, artifact inventory | Git history, transaction records, artifact counts per practice |
| **change** | Amount of measurement framework change per transaction | Commits, schema migrations, artifact type additions |
| **completion** | Progress toward current measurement phase goal | POSTFLIGHT summaries, goal completion tracking, milestones |
| **impact** | Significance of measurement work to the mesh | Practice feedback, evaluator usage, Admiral visibility |
| **engagement** | Active problem-solving on measurement questions | Collab thread participation, cross-practice coordination, follow-up speed |
| **uncertainty** | What humanaios does NOT know | Unknowns logged per transaction, gaps identified in calibration baselines, measurement blind spots |

### Calibration Routine
1. **Per-Transaction (5ecc9059-...):** PREFLIGHT vector self-assessment + noetic guidance; POSTFLIGHT vector re-assessment + grounded evidence (test results, commits, artifact counts)
2. **Weekly (async):** Review practice calibration trends, identify drift patterns, log findings
3. **Monthly (collab):** Cross-practice calibration alignment call — autonomy + evaluator + practices share trajectory insights
4. **Quarterly (Admiral gate):** Full calibration review — are thresholds still valid? Are new practices ready for baseline? Does framework need updating?

### Calibration Anomalies
- **Widening Gaps (self-assessed vs. grounded):** Indicates over-confidence in measurement judgment or under-logging of evidence. Response: increase artifact logging rigor, run more test coverage
- **Sudden Vector Drops:** Suggests a measurement assumption was wrong or a schema bug was found. Response: log mistake artifact, investigate root cause, update framework
- **Plateauing Completion:** Indicates measurement roadmap is stalled or unclear. Response: re-examine next-phase goals, solicit practice feedback

---

## 7. Contacts & Communication

### How to Reach HumanAIOS
- **For Measurement Questions:** Collab via mesh (ask measurement questions; auto-accepted, no ECO gate)
- **For Schema Changes:** Propose via cortex (ECO-gated; impacts practice data models)
- **For Calibration Baselines:** Direct handoff from evaluator; request via mesh collab
- **For Practice Onboarding:** Mesh-support initiates; humanaios provides training materials

### Availability & Response Windows
- **Collab Questions:** Response within 1-2 hours (daytime async)
- **Urgent Schema Issues:** Response within 30 minutes if affecting production
- **Practice Training:** Scheduled 1-week advance (2-3 hour blocks per practice)
- **Mesh Coordination:** Weekly async coordination Thursdays 10am-2pm

---

## 8. Governance & Ratification

### Draft Status (Aug 8-14)
- Charter scope, authority boundaries, decision paths drafted
- Success metrics scoped to measurement fidelity + adoption + operational health
- Calibration model tied to empirica 13-vector framework

### Peer Review (Aug 12-18)
- Mesh-support review: clarify infrastructure dependencies
- Autonomy review: clarify artifact retrieval integration
- Evaluator review: clarify calibration baseline handoff

### Admiral Ratification (Aug 19-25)
- Carly confirms spec aligns with foundation governance model
- Publish as canonical practice specification for humanaios

### Next Iteration (Post-Ratification)
- Q3 2026: Establish per-practice calibration baselines
- Q4 2026: Measurement framework v1.0 (complete 13-vector sensor integration)
- 2027 Q1: Cross-org measurement alignment (if org-wide expansion)

---

## References

- **Empirica System Prompt:** ~/.claude/empirica-system-prompt.md (epistemic framework, transaction discipline)
- **M2R2 Harmonization:** feature/m2r2-state-harmonization-humanaios (schema migration, 28/28 tests passing)
- **Project Calibration Weights:** .empirica/project.yaml (humanaios-specific vector weights per work_type)
- **Foundation Org Prompt:** ~/.claude/empirica-foundation-org-prompt.md (org addressing, mesh discipline)

---

**Status:** DRAFT → Awaiting Mesh-Support Review → Admiral Ratification → Publication

