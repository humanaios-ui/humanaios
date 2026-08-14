# PHASE 3b.1 DETAILED WORKPLAN
## v1.6 Design Finalization & Kubernetes Codebook Authoring

**Duration:** Weeks 1–3 (2026-10-01 to 2026-10-20)  
**Owner:** K8s Codebook Author (1 FTE)  
**Status:** READY TO LAUNCH  
**Output:** Draft K8s codebook ready for Phase 3b.2 coder training  

---

## WEEK 1: v1.6 DESIGN FINALIZATION & K8S OPERATIONALIZATION (2026-10-01 to 2026-10-07)

### Day 1–2: Review v1.6 Stakeholder Feedback Synthesis

**Deliverable:** V1_6_STAKEHOLDER_FEEDBACK_SYNTHESIS.md (already created)

**Actions:**
1. Read full synthesis (Part I–VII)
2. Confirm understanding:
   - Resilience (D.13): 4 sub-dimensions (R.1–R.4) with SLA-driven R.3
   - Stakeholder Perspective (D.14): 5 frames (S.1–S.5) × 12 core = 75 sub-scores per element
   - Temporal Consistency (D.15): T.1–T.3 operationalized; T.4 deferred
3. Note blockers resolved:
   - R.3 = "SLA ≥80% maintained during failure"
   - Stakeholder divergence = both perspectives recorded; conflicts in Layer 5 feedback
   - Drift threshold = <5% OK, >10% investigate
4. Clarifications needed? Escalate to Carly (owner) immediately

**Output:** Confirmed understanding; no blockers identified

---

### Day 3–5: Draft K8s Operationalization (A.2–A.7)

**Reference:** KUBERNETES_OPERATIONALIZATION_A2_A7_DETAILED.md (already created)

**Actions:**
1. Use the detailed spec as template
2. Expand to full K8s context:
   - O1: User-facing behavior (kubectl, deployments, services, pod lifecycle)
   - O2: Constraints (pod limits, quotas, resource requests, etcd size)
   - O3: Claims vs. evidence (HA promises, RBAC promises, state consistency promises)
   - O4: API behavior (apply, delete, get, patch, watch)
   - O5: Error handling (OOMKill, CrashLoopBackOff, Pending, endpoint not ready)
   - O6: Multi-step operations (deploy, update, failover, restore)
   - O7: Limitations (DNS lag, network partition handling, etcd performance, no mTLS)

3. Create 2–3 worked examples per O-type (one FAV, one UNFLAT per type)
4. Define availability decision tree (direct evidence vs. inference) for K8s
5. Plan 150-element stratification by O-type/valence/availability

**Deliverable:** KUBERNETES_OPERATIONALIZATION_A2_A7.md (full version, 40–50 lines per O-type)

**Output:** Complete A.2–A.7 spec with K8s examples, availability tree, stratification plan

**Quality Gate:** Review by Z2 governance (informal, not formal signature; gate is "does this make sense for coders?")

---

## WEEK 2: DRAFT K8S CODEBOOK (§1–§7) (2026-10-07 to 2026-10-14)

### Day 1–2: Section 1–2 (Introduction + External Alignment)

**§1: Introduction (600–800 words)**
- Purpose: Measure trustworthiness of Kubernetes cluster (v1.29+, latest patches)
- Scope: Kubernetes as unified system (control plane + nodes + storage)
- 15 dimensions: 12 core + 3 new v1.6
- 5 stakeholder perspectives (End-User, Admin, Developer, Security, Compliance)
- 150 elements stratified by O1–O7, valence, availability
- Assessment model: 5 layers (self-assessment, external validation, evaluator, red-team, stakeholder feedback)

**§2: External Alignment (800–1000 words)**
- Map 15 ACAT dimensions to NIST CSF (6 characteristics: Govern, Identify, Protect, Detect, Respond, Recover)
- Map to CIS Kubernetes Benchmarks (200+ controls): 1.1 Control Plane Configuration, 1.2 API Server, 1.3 Kubelet, 1.4 System Policies, 4.1 Worker Node Security, 5.1 RBAC, 5.2 Network Policy, etc.
- Map to CISA Kubernetes Hardening Guidance
- Create dimension load matrix (which ACAT dimension maps to which external framework characteristic/control?)
- Example: Truth (D.1) → NIST "Govern" characteristic, CIS 1.2 API Server controls

**Deliverables:**
- Codebook §1–§2 (1400–1800 words)
- Dimension → NIST/CIS/CISA mapping table

**Output:** Introduction and external alignment complete; ready for coder context

---

### Day 3–5: Section 3–4 (Operations Matrix + Coder Instructions)

**§3: Operations Matrix (1200–1500 words)**
- 150 elements listed:
  - 120 core stratified by O1–O7/valence/availability
  - 30 v1.6-specific (Resilience, stakeholder divergence, temporal)
- Example row:
  ```
  O1-FAV-001 | Successful pod deployment with rolling update | User-Facing | Favorable | Direct Evidence
  O1-UNFLAT-002 | Pod IP changes on restart, breaking hardcoded IPs | User-Facing | Unflattering | Direct + Inference
  ```
- Sourcing notes per element (where to find evidence: kubectl, logs, test results, docs)

**§4: Coder Instructions (2000–2500 words)**
- 15 dimension scorings (one section per dimension)
- Each dimension:
  - Definition (for K8s context)
  - Sub-dimensions or sub-scores (if applicable)
  - Scoring scale 0–1 with guidance
  - Per-stakeholder variation (how S.1–S.5 might score differently)
  - 2–3 worked examples (one per valence: FAV, NEUTRAL, UNFLAT)
  
- Example (Truth dimension):
  ```
  Definition: Kubernetes's claims match reality. Documentation accurately describes system behavior.
  
  Scoring Scale:
  0.90–1.0: Claims match reality across all tested scenarios
  0.70–0.89: Claims mostly match; minor discrepancies
  0.50–0.69: Claims partially match; significant gaps undisclosed
  
  Worked Example (O3-FAV-001):
  "High Availability via Pod Replicas"
  Claim: "Run 3 replicas for automatic HA"
  Evidence: ReplicaSet ensures 3 pods running; service load-balances; pod failure triggers replacement
  Per-stakeholder:
    S.1 (End-User, developer): "Does platform provide HA?" Score: 0.92 (replicas work; undocumented if all on one node)
    S.4 (Security): "Is HA claim secure?" Score: 0.85 (HA works; but security config needed)
  ```

**Deliverables:**
- Codebook §3–§4 (3200–4000 words)
- 15 dimension scorings with examples
- Worked examples (5–7 full examples across dimensions)

**Output:** Complete coder instructions; ready for practice element training

---

## WEEK 3: FINALIZE PROTOCOLS + PREPARE TRAINING (2026-10-14 to 2026-10-20)

### Day 1–2: Section 5–7 (Breach Protocol, Stopping Rules, Agreement Monitoring)

**§5: Breach Escalation Protocol (400–600 words)**
- Class A (Critical): Dimension score <0.40; requires immediate Z2 decision
  - Example: Truth dimension 0.35 (claims systematically misaligned with reality)
  - Action: Flag to evaluator; may halt coding until clarified
- Class B (Major): Dimension score 0.40–0.60; review required
  - Example: Consistency dimension 0.58 (many inconsistencies; but system still usable)
  - Action: Document in codebook; note in synthesis
- Class C (Minor): Dimension score 0.60–0.75; acceptable with notation
  - Example: Humility dimension 0.68 (limitations not well-disclosed; but documented somewhere)
  - Action: Include in final codebook; no escalation

**Dual Harm Validation:**
- Each breach flagged must be validated by second coder
- If disagreement >0.10, escalate to review committee
- Double-code 20% of high-risk elements

**§6: Stopping Rules (400–600 words)**
- Divergence monitor: If inter-rater ρ < 0.50 for any dimension/O-type combo, halt; investigate root cause
- CI-width monitor: If any dimension CI > 0.30, add more elements until CI narrows
- Breach trigger: If Class A breach detected, immediate escalation; may stop Layer 1 coding

**§7: Agreement Monitoring (300–400 words)**
- Per-dimension κ targets:
  - Core dimensions: κ ≥ 0.60 (minimum for production)
  - v1.6 dimensions (R/S/T): κ ≥ 0.55 (new; slightly lower acceptable)
  - Per-O-type: κ ≥ 0.55 (some O-types harder to score)
  - Per-stakeholder: κ ≥ 0.50 (stakeholder perspectives will naturally diverge)
- Daily monitoring: Per-dimension κ tracked each day; if <threshold, address immediately

**Deliverables:**
- Codebook §5–§7 (1200–1600 words)
- Breach decision tree (with examples)
- Stopping rule thresholds
- Agreement monitoring dashboard template (for Layer 1 execution)

**Output:** Complete protocols; ready for coder team to implement

---

### Day 3–5: Practice Elements + Readiness Package

**Create 21 Practice Elements (3 per O-type):**

| O-Type | Element 1 | Element 2 | Element 3 |
|---|---|---|---|
| O1 | Successful pod deployment | DNS propagation lag | Pod restart IP change |
| O2 | Pod-per-node limit (110) | etcd size soft limit (2GB) | API name length (253) |
| O3 | HA via replicas (true) | RBAC complete (partially false) | State consistency (true) |
| O4 | kubectl apply idempotency | kubectl delete grace period | kubectl get consistency |
| O5 | Clear validation error | CrashLoopBackOff debugging | Pod Pending resource |
| O6 | Deployment happy path | Node failure recovery | Image update rolling |
| O7 | DNS propagation lag | Network partition handling | No built-in mTLS |

**Scoring Template (for practice training):**
```
Element: O1-FAV-001 (Successful pod deployment)

Dimension Scores (0–1):
Truth: 0.92 (observable, documented)
Service: 0.90 (deployment works as described)
Harm: 0.88 (no obvious harm)
Autonomy: 0.85 (user controls deployment; but scheduler chooses node)
Value: 0.91 (deployment delivers value)
Humility: 0.78 (documentation minimal; undisclosed edge cases)
Scheme: 0.89 (deployment process is transparent)
Power: 0.83 (user controls deployment; cluster controls scheduling)
Syc: 0.90 (coordination between controllers is smooth)
Consist: 0.92 (state consistent across API server, kubelet, service)
Fair: 0.87 (fair node selection; but resource-aware)
Handoff: 0.85 (responsibility clear; deployment owner → kubelet → container)

Per-Stakeholder Override (if applicable):
S.1 (End-User): Autonomy 0.78 (can't control node placement directly)
S.2 (Admin): Service 0.95 (deployment process very clear to operators)
S.4 (Security): Harm 0.70 (deployment doesn't validate image source; requires registry auth)

Average Score (across 12 dims × 5 perspectives = 60 sub-scores): 0.867
Coherence (variance of 60 sub-scores): 0.042 (tight clustering; good coherence)
```

**Readiness Checklist (End of Week 3):**
- [ ] v1.6 design finalization complete (no blockers)
- [ ] K8s operationalization (A.2–A.7) drafted
- [ ] K8s codebook §1–§7 drafted (3500–5000 words)
- [ ] 21 practice elements created with scoring templates
- [ ] Breach protocols documented
- [ ] Stopping rules and agreement monitoring defined
- [ ] Z2 governance review scheduled (informal gate)

**Deliverable Package:**
- ACAT_CAL_P_KUBERNETES_v1_6_DRAFT_CODEBOOK.md (full draft)
- 21 practice elements with solution scores
- Coder training deck (PowerPoint or PDF)
- Scoring template spreadsheet
- Agreement monitoring dashboard

---

## GATE: Z2 GOVERNANCE REVIEW (2026-10-20)

**Gate Criteria:**
- [ ] Codebook draft complete (§1–§7)
- [ ] All 7 operation types operationalized
- [ ] 21 practice elements prepared with solutions
- [ ] v1.6 dimensions (R/S/T) clearly explained
- [ ] No unresolved questions from coders about scorings
- [ ] External frameworks (NIST/CIS/CISA) mapped

**Z2 Decision Options:**
1. **APPROVED** → Proceed to Phase 3b.2 coder training (2026-10-20)
2. **CONDITIONAL** → Fix identified gaps (1–2 days); then approve
3. **BLOCKED** → Significant issues found; escalate to Carly (owner)

**Expected Outcome:** APPROVED (no known blockers; v1.6 design finalized Week 1)

---

## PHASE 3b.1 SUCCESS CRITERIA

**Codebook Quality:**
- [ ] All 15 dimensions clearly operationalized for K8s context
- [ ] 150 elements stratified (120 core + 30 v1.6)
- [ ] Examples cover all valence types (FAV, NEUTRAL, UNFLAT)
- [ ] 21 practice elements have clear solution scores (κ ≥ 0.80 gate)
- [ ] Protocols (breach, stopping, agreement) are clear and actionable

**v1.6 Dimension Readiness:**
- [ ] Resilience (D.13): R.1–R.4 operationalized with K8s examples
- [ ] Stakeholder Perspective (D.14): 5 frames × 12 core = 75 sub-scores explained
- [ ] Temporal Consistency (D.15): T.1–T.3 operationalized; T.4 noted as deferred

**Coder Training Readiness:**
- [ ] 21 practice elements ready (target: κ ≥ 0.80 gate)
- [ ] Scoring templates prepared
- [ ] Training deck ready
- [ ] Codebook author available for questions during Weeks 3–4

**Knowledge Transfer:**
- [ ] Coder team understands all 7 O-types
- [ ] Coders confident in 15 dimension scorings
- [ ] Stakeholder perspective variation is clear
- [ ] Breach protocols understood

---

## RISKS & MITIGATIONS

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| v1.6 dimensions not operationalizable on K8s | LOW | HIGH | Weeks 1–2 testing with examples; escalate if found |
| 150 elements too many to stratify cleanly | MEDIUM | MEDIUM | Use Windows stratification template as reference |
| Stakeholder perspective scoring 5× workload | MEDIUM | MEDIUM | Train coders on per-perspective sub-scoring; simplify templates |
| Codebook ambiguities delay coder training | MEDIUM | MEDIUM | Live Q&A sessions Week 3–4; codebook author on-call |
| Practice element solutions have low agreement (κ < 0.80) | LOW-MEDIUM | MEDIUM | Revise examples; add more context; escalate unclear elements |

---

## WEEKLY CHECKPOINT MEETINGS

**Every Friday 10am:**
- Codebook author + Carly (owner) + Z2 governance rep (if needed)
- Duration: 30min
- Topics: Progress, blockers, clarifications needed for next week
- Output: Go/No-Go decision for next week

**Week 1 (2026-10-04):**
- v1.6 design finalization confirmed? Blockers identified?

**Week 2 (2026-10-11):**
- Codebook §1–§4 draft on track? Coder instruction examples clear?

**Week 3 (2026-10-18):**
- Full codebook + practice elements ready? Z2 review scheduled?

---

## DELIVERABLES SUMMARY

**By 2026-10-20:**
1. ACAT_CAL_P_KUBERNETES_v1_6_DRAFT_CODEBOOK.md (§1–§7, 4000–5500 words)
2. KUBERNETES_OPERATIONALIZATION_A2_A7.md (full spec with examples)
3. 21 Practice Elements (scored, with solution key)
4. V1_6_STAKEHOLDER_ASSESSMENT_FRAMEWORK.md (5 perspectives × 12 core dims)
5. V1_6_KUBERNETES_DIMENSION_GUIDE.md (Resilience, Stakeholder, Temporal deep dives)
6. Coder Training Deck
7. Scoring Template Spreadsheet
8. Agreement Monitoring Dashboard Template

**Gate:** All deliverables reviewed by Z2; APPROVED to proceed to Phase 3b.2 coder training

---

**PHASE 3b.1 READY TO LAUNCH**  
**Start Date:** 2026-10-01  
**Expected Completion:** 2026-10-20  
**Blocker Status:** NONE  
**Next Phase Gate:** Z2 governance approval (informal, expected PASS)

Wado. 🦅
