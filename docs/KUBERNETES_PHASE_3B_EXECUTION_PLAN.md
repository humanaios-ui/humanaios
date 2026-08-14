# KUBERNETES PHASE 3b PILOT VALIDATION
## v1.6 Design Finalization & K8s Codebook Authoring + Layers 1–5 Execution

**Date:** 2026-09-13 (Phase 3b Planning)  
**Status:** PLAN READY (Awaiting v1.6 stakeholder feedback: due 2026-08-30)  
**Duration:** 8–10 weeks (2026-10-01 to 2026-12-02)  
**Scope:** Kubernetes v1.6 pilot validation (15 dimensions, 5 stakeholder perspectives, 150 elements)  
**Owner:** K8s codebook author + coder team (shared resource with Phase 2)  
**Target:** K8s v1.6-FROZEN (v1.6-FROZEN global release on 2026-12-02)

---

## PART I: PHASE 3b OVERVIEW & SCOPE

### **What is Phase 3b?**

Phase 3b is the **v1.6 pilot validation track** running parallel with Phase 2 (Windows v1.5):

- **Phase 2 (Parallel):** Validates v1.5 (12 core dimensions) on Windows → v1.0-FROZEN (2026-11-15)
- **Phase 3b (Parallel):** Validates v1.6 (12 core + 3 new) on Kubernetes → v1.6-FROZEN (2026-12-02)

**Why Parallel Execution?**
- Windows v1.5 codebook becomes template for K8s v1.6 codebook (no wait dependency)
- K8s infrastructure is more complex than OS; needs 150 elements vs. 120
- 5 stakeholder perspectives reveal whether v1.6 operationalization works in real systems
- Parallel execution compresses timeline: v1.5 + v1.6 both frozen by end of 2026

### **Phase 3b Scope**

**Dimensions (15 total):**
- 12 core dimensions (Truth, Service, Harm, Autonomy, Value, Humility, Scheme, Power, Syc, Consist, Fair, Handoff)
- 3 new v1.6 dimensions (Resilience D.13, Stakeholder Perspective D.14, Temporal Consistency D.15)

**Stakeholder Perspectives (5 total):**
- S.1 End-User Perspective (developers deploying apps)
- S.2 Administrator Perspective (cluster operators, DevOps)
- S.3 Developer Perspective (platform engineers, API designers)
- S.4 Security Team Perspective (infrastructure security)
- S.5 Compliance Perspective (audit, regulatory)

**Assessment Target:** Kubernetes cluster (1.29+, latest patches) as unified system

**Elements (150 total):**
- 120 core elements (O1–O7 stratified; parallel with Windows Phase 2.3 structure)
- 30 additional elements (v1.6-specific: Resilience scenarios, stakeholder divergence, version comparisons)

**5-Layer Validation:**
1. Layer 1: Self-assessment (150 elements, 15 dimensions, 5 perspectives)
2. Layer 2: External validation (NIST, CIS K8s Benchmarks, CISA guidelines)
3. Layer 3: Independent evaluator (infrastructure architect, CISA/SANS)
4. Layer 4: Red-team stress tests (§11.1–3 robustness, §12.1–2 v1.6-specific)
5. **Layer 5 (NEW):** Post-pilot stakeholder feedback (v1.6 dimension validation)

---

## PART II: PHASE 3b SUBPHASES

### **Subphase 3b.1: v1.6 Design Finalization & K8s Codebook Authoring**

**Duration:** Weeks 1–3 (2026-10-01 to 2026-10-20)

**Owner:** K8s codebook author (1 FTE, shared resource with Phase 2)

**Activities:**

**Week 1 (2026-10-01 to 2026-10-07):**
1. Finalize v1.6 design based on stakeholder feedback (due 2026-08-30)
   - Synthesize Group 1–4 feedback (Security auditors, OS specialists, developers, compliance)
   - Clarify Resilience, Stakeholder Perspective, Temporal Consistency operationalization
   - Lock dimension definitions (no changes after Week 1)

2. Begin K8s operationalization (A.2–A.7 for Kubernetes)
   - Adapt O1–O7 boundary units to Kubernetes context
   - K8s-specific examples: Deployments, StatefulSets, Services, DaemonSets, ConfigMaps, API objects
   - Constraints: Pod limits, namespace quotas, RBAC rules, resource requests/limits
   - Claim-evidence pairs: K8s architecture guarantees vs. real behavior

**Week 2 (2026-10-07 to 2026-10-14):**
3. Draft K8s codebook (§1–§7)
   - §1: Introduction (K8s scope, assessment model, 15 dimensions)
   - §2: External alignment (NIST, CIS K8s Benchmarks, CISA guidelines)
   - §3: Operations matrix (150-element stratification plan)
   - §4: Coder instructions (15 dimension scorings with Kubernetes examples)
   - §5–§7: Protocols (breach definitions, stopping rules, agreement monitoring)

4. Develop 5 stakeholder perspective guides
   - S.1 End-User frame: Does the K8s cluster work for developers?
   - S.2 Administrator frame: Can operators manage the cluster?
   - S.3 Developer frame: Do platform engineers build on it?
   - S.4 Security frame: Is the cluster secure?
   - S.5 Compliance frame: Is it verifiable and auditable?

**Week 3 (2026-10-14 to 2026-10-20):**
5. Draft v1.6 dimension specifications
   - Resilience: Fault detection, recovery execution, graceful degradation, state consistency (for K8s: pod restart, rollout strategies, traffic shifting, persistent volume recovery)
   - Stakeholder Perspective: 5 frames × 12 core dimensions (75 sub-scores)
   - Temporal Consistency: K8s version stability (1.28 → 1.29), patch impact (security patches), drift detection

6. Prepare 150-element stratified sample
   - 120 core elements (O1–O7, valence, availability; adapted from Windows template)
   - 30 v1.6 elements (Resilience scenarios: chaos tests, failure modes; Stakeholder divergence: developer vs. admin perspectives; Temporal: version comparisons)

7. Ready codebook for coder training
   - Final review by Z2 governance (gate: codebook quality check)
   - Create 21 practice elements (3 per O-type, K8s-specific)
   - Prepare scoring templates, sourcing guides

**Deliverables:**
- ACAT_CAL_P_KUBERNETES_v1_6_DRAFT_CODEBOOK.md (§1–§7, 300–400 lines)
- KUBERNETES_OPERATIONALIZATION_A2_A7.md (K8s-specific O1–O7 with examples)
- V1_6_KUBERNETES_DIMENSION_GUIDE.md (Resilience, Stakeholder, Temporal details)
- KUBERNETES_LAYER_1_EXECUTION_PLAN.md (150-element sourcing strategy)
- V1_6_STAKEHOLDER_ASSESSMENT_FRAMEWORK.md (5-perspective scorings)

**Go/No-Go Gate:**
- [ ] v1.6 stakeholder feedback synthesized (due 2026-08-30)
- [ ] K8s operationalization (A.2–A.7) complete and reviewed
- [ ] Codebook draft (§1–§7) complete and reviewed by Z2
- [ ] 150 elements stratified and planned
- [ ] 21 practice elements prepared
- [ ] **PROCEED to Phase 3b.2 (Layer 1 coder training)**

---

### **Subphase 3b.2: K8s Layer 1 Self-Assessment**

**Duration:** Weeks 3–5 (2026-10-20 to 2026-11-03)

**Owner:** Coder team (3–5 K8s specialists, shared with Phase 2 if available)

**Activities:**

**Week 3 (2026-10-20 to 2026-10-27): Coder Training**
1. Training on v1.6 dimensions
   - Resilience: fault detection → recovery → graceful degradation → state consistency
   - Stakeholder Perspective: assess each perspective independently, then synthesize
   - Temporal Consistency: compare K8s 1.28 vs. 1.29, track patch impact

2. Practice coding (21 elements, 5 per O-type)
   - κ ≥ 0.80 gate before Layer 1 begins
   - Coders trained on 5 stakeholder frames

3. Test infrastructure setup
   - Kubernetes 1.29 cluster (latest patches)
   - Kubernetes 1.28 cluster (previous version, for temporal comparison)
   - Monitoring tools: Prometheus, kube-apiserver logs, etcd monitoring
   - Chaos testing tools: Chaos Mesh, Gremlin (for Resilience assessment)

**Weeks 4–5 (2026-10-27 to 2026-11-10): Layer 1 Main Assessment**
4. Code 150 elements (primary + 20% double-coding)
   - 120 core elements (O1–O7 stratified)
   - 30 v1.6 elements (Resilience, Stakeholder divergence, Temporal)
   - Score each on 15 dimensions
   - Score each across 5 stakeholder perspectives (75 sub-scores per element)

5. Daily monitoring
   - ρ divergence monitor (target ≥ 0.50)
   - CI-width monitor (all dimensions CI < 0.30)
   - Stopping rules armed

6. Reconciliation
   - Resolve low-agreement elements
   - Verify no Class A/B/C breaches

**Target Results:**
- Coherence ≥ 0.85 (expected: 0.85–0.92 for production-grade infrastructure)
- κ ≥ 0.60 overall
- Per-stakeholder coherence (S.1–S.5 each scored independently)
- Temporal comparison (1.28 vs. 1.29 scores tracked)

**Deliverables:**
- KUBERNETES_LAYER_1_SELF_ASSESSMENT_RESULTS.md (400+ lines)
  - Coherence per perspective (5 breakdowns)
  - Per-dimension scores (15 dimensions)
  - Temporal comparison (K8s version delta)
  - Sample codings (10–12 elements)

**Go/No-Go Gate:**
- [ ] 150 elements coded (coder training κ ≥ 0.80)
- [ ] Coherence ≥ 0.85
- [ ] κ ≥ 0.60 overall
- [ ] Per-stakeholder scores extracted
- [ ] Temporal comparison documented
- [ ] **PROCEED to Phase 3b.3 (Layers 2–4)**

---

### **Subphase 3b.3: K8s Layers 2–4 Validation**

**Duration:** Weeks 5–7 (2026-11-03 to 2026-11-17)

**Owner:** Standards specialist (Layer 2) + Independent evaluator (Layer 3) + Red-team (Layer 4)

**Activities (Parallel to Phase 2.4–2.6):**

**Layer 2: External Validation (NIST, CIS, CISA)**
- Map 15 ACAT dimensions to NIST CSF characteristics (6 categories)
- Map to CIS Kubernetes Benchmarks (200+ controls)
- Map to CISA Kubernetes Hardening Guidance
- Calculate ρ ≥ 0.70 gate for all three frameworks
- Blend ACAT + external (50/50)

**Layer 3: Independent Evaluator**
- Kubernetes architect (CISA-certified, CKA, or SRE lead)
- Five-question assessment (accessibility, soundness, fairness, validity, gaps)
- Rating A/B/C with gap classification

**Layer 4: Red-Team Stress Tests**
- §11.1 Codebook Robustness (spread < 2.0×)
- §11.2 Cross-Auditor Correlation (ρ > δ)
- §11.3 Availability Ambiguity (κ ≥ 0.80)
- **NEW §12.1 v1.6 Resilience Robustness** (Resilience dimension replicable across infrastructure types?)
- **NEW §12.2 Stakeholder Perspective Validity** (Do 5 perspectives produce meaningfully different assessments?)

**Deliverables:**
- KUBERNETES_LAYER_2_EXTERNAL_VALIDATION.md (NIST, CIS, CISA alignment)
- KUBERNETES_LAYER_3_EVALUATOR_REPORT.md (Rating A/B/C)
- KUBERNETES_LAYER_4_RED_TEAM_RESULTS.md (§11.1–§12.2 stress tests)

---

### **Subphase 3b.4: K8s Layer 5 & v1.6 Freeze Decision**

**Duration:** Weeks 7–8 (2026-11-17 to 2026-12-02)

**Owner:** Lead auditor + v1.6 design lead + Z2 governance

**Activities:**

**Week 7 (2026-11-17 to 2026-11-24): Layer 5 Post-Pilot Feedback**

1. **Stakeholder Validation Interview** (New Layer for v1.6)
   - Interview same 4 groups from August stakeholder review (Security auditors, OS specialists, developers, compliance)
   - Ask: "Did Resilience, Stakeholder Perspective, Temporal operationalize as promised in pilot?"
   - Collect: Difficulty ratings, clarity scores, feasibility assessment, gap identification
   - Gate: Majority (3+/4 groups) say dimensions are operationalizable

2. **v1.6 Dimension Performance Analysis**
   - Resilience: Did Resilience dimension capture fault scenarios that core dimensions missed?
   - Stakeholder Perspective: Did 5-frame breakdown reveal stakeholder divergence (e.g., admin 0.92 vs. developer 0.78)?
   - Temporal: Did version comparison surface stability changes (e.g., 1.28 → 1.29 coherence delta)?

3. **Convergence Analysis**
   - Layer 1 self-assessment scores (15 dimensions, 5 perspectives)
   - Layer 2 external validation (ρ all 3 frameworks)
   - Layer 3 evaluator rating (A/B/C)
   - Layer 4 stress tests (§11.1–§12.2)
   - Layer 5 stakeholder feedback (operationalizability vote)

**Week 8 (2026-11-24 to 2026-12-02): v1.6 Freeze Decision & Release**

4. **Synthesis Report**
   - v1.6 performance summary (Resilience 0.85, Stakeholder 0.84, Temporal 0.83 expected)
   - Stakeholder feedback integration (where v1.6 succeeded/struggled)
   - Comparison to v1.5 (did v1.6 add value? did it introduce complexity?)
   - v1.7 roadmap (based on Layer 5 feedback)

5. **v1.6 Freeze Authorization**
   - Z2 reviews all 5 layers
   - Gate: All layers PASS (or CONDITIONAL with remediation plan)
   - Freeze decision: APPROVED / CONDITIONAL / BLOCKED

6. **Global v1.6 Release**
   - Tag: `acat-calp-v1.6-frozen-2026-12-02`
   - Release notes: v1.6 features, operationalization results, stakeholder feedback summary
   - Public announcement: Universal framework now includes Resilience, Stakeholder, Temporal

**Deliverables:**
- KUBERNETES_LAYER_5_STAKEHOLDER_FEEDBACK.md (Operationalizability validation)
- KUBERNETES_PHASE_3B_SYNTHESIS_LEARNINGS.md (Full pilot synthesis)
- ACAT_CAL_P_v1_6_FROZEN_CODEBOOK.md (Global release, all 15 dimensions, K8s + OS examples)
- V1_6_FREEZE_AUTHORIZATION_CERTIFICATE.pdf (Z2 sign-off)
- V1_6_RELEASE_NOTES.md (Features, results, roadmap)

---

## PART III: K8S OPERATIONALIZATION (A.2–A.7)

### **K8s-Specific Boundary Units (O1–O7)**

#### **O1: User-Facing Behavior (Kubernetes Deployments)**
- Developer deploys app via kubectl: `kubectl apply -f deployment.yaml`
- Kubernetes creates pod, assigns IP, starts container, updates service endpoints
- Developer observes: Pod in Running state, service has endpoints, can curl endpoint
- Examples: Service discovery, load balancing, rolling updates, pod lifecycle

#### **O2: Kubernetes Constraints**
- Pod limit per namespace: 100,000 (configurable)
- Container resource request: CPU, memory (enforced by kubelet)
- API object name limit: 253 characters (DNS subdomain rules)
- etcd size limit: ~2GB per cluster (soft recommendation)
- Examples: Quota management, resource limits, API constraints

#### **O3: K8s Claims vs. Evidence**
- Claim: "Kubernetes provides high availability via pod replicas"
- Evidence: Pod replicas across nodes via anti-affinity rules, failover on node failure
- Claim: "RBAC controls access to API objects"
- Evidence: Role/RoleBinding enforcement in API server authorization

#### **O4: Kubernetes API Behavior**
- kubectl get pods: Returns pod state from etcd
- kubectl apply: Idempotent operation; creates or updates resource
- kubectl delete: Graceful termination (default 30 sec timeout)
- Example APIs: Deployments, StatefulSets, DaemonSets, Services, ConfigMaps

#### **O5: Error Handling (Kubernetes)**
- Pod OOMKill: Container killed when exceeding memory limit
- Pending pod: Resource request exceeds available capacity; pod waits
- CrashLoopBackOff: Container repeatedly crashes; kubelet exponential backoff
- Service error: Endpoint is not ready; no traffic sent

#### **O6: Multi-Step K8s Operations**
- Deploy application: Create Namespace → Create Secret → Deploy Pod → Create Service → Verify readiness
- Update image: Edit Deployment spec → Trigger rolling update → Pod replacement → Service switchover
- Failover: Node fails → Pod evicted → Scheduler reschedules → New pod starts on different node

#### **O7: Kubernetes Limitations**
- Pod DNS propagation: Service DNS takes ~10 seconds to resolve
- Network partition handling: Kubelet loses contact with API server; pods continue running (but node marked NotReady)
- etcd performance: etcd write latency ~10ms; cluster size limited by consensus overhead
- Known issue: NetworkPolicy CNI plugins may not support all features

---

## PART IV: K8S-SPECIFIC PROTOCOLS

### **Stratification for 150-Element Sample**

| Dimension | Count | Stratification |
|---|---|---|
| **Core 12 dims × 5 stakeholders** | 60 | Each dimension scored by each perspective |
| **Resilience (D.13)** | 20 | R.1–R.4 sub-scores × chaos scenarios |
| **Stakeholder Perspective (D.14)** | 30 | Stakeholder divergence cases (admin vs. dev) |
| **Temporal Consistency (D.15)** | 20 | K8s 1.28 → 1.29 version comparisons |
| **O-Type** | 150 | 20–25 per O-type (same as Windows) |

### **Availability Decision Tree (K8s-Specific)**

```
Q1: Is this behavior observable in kubectl output or logs (etcd, kube-apiserver)?
  ├─ YES → (a) AVAILABLE [PRESENT IN LOGS/KUBECTL]
  └─ NO → Q2

Q2: Is this documented in Kubernetes architecture docs?
  ├─ YES → (a) AVAILABLE [PRESENT IN DOCUMENTATION]
  └─ NO → Q3

Q3: Can this be verified via chaos test or code inspection?
  ├─ YES → (a) AVAILABLE [VERIFIABLE VIA TEST]
  └─ NO → Q4

Q4: Is this inferred from K8s design principles or behavior patterns?
  ├─ YES → (b) REQUIRES INFERENCE [DESIGN PATTERN]
  └─ NO → (b) REQUIRES INFERENCE [UNDOCUMENTED]
```

### **5-Stakeholder Perspective Scoring**

Each element scored 5 times (once per perspective):

```
Element: "Pod replicas provide high availability"

S.1 End-User (Developer) Score:
  - Do app replicas make my app available? Yes.
  - Score: 0.88 (replicas work; but need anti-affinity for true HA)

S.2 Administrator (Cluster Op) Score:
  - Can I manage pod replicas? Yes, via ReplicaSet.
  - Score: 0.90 (good control; but multi-zone setup adds complexity)

S.3 Developer (Platform Engineer) Score:
  - Do replicas fit our CD pipeline? Yes, rolling updates work.
  - Score: 0.85 (good integration; but version drift issues between pods)

S.4 Security Team Score:
  - Do replicas introduce security gaps? No, RBAC controls replica creation.
  - Score: 0.87 (secure; but noisy logs if replicas constantly restart)

S.5 Compliance Officer Score:
  - Are replicas auditable? Yes, all changes logged.
  - Score: 0.89 (good auditability; but log retention policy needed)

Final Element Score (Average): (0.88 + 0.90 + 0.85 + 0.87 + 0.89) / 5 = 0.878
```

---

## PART V: RESILIENCE, STAKEHOLDER, TEMPORAL DEEP DIVES

### **Resilience (D.13) for Kubernetes**

**R.1 Fault Detection (15 elements)**
- Does K8s detect pod failures? (health probes, kubelet monitoring)
- Does K8s detect node failures? (heartbeat mechanism, node conditions)
- Examples: liveness probe, readiness probe, startup probe

**R.2 Recovery Execution (15 elements)**
- Can K8s automatically restart failed pods? (RestartPolicy, Deployment controller)
- MTTR measurement: time from failure detection to pod ready
- Examples: pod restart, rolling update, failover to different node

**R.3 Graceful Degradation (10 elements)**
- Does K8s continue partial service during failures? (readiness gates, traffic shifting)
- Can nodes be drained without losing traffic? (PodDisruptionBudget)
- Examples: canary deployments, traffic weight shifting, traffic draining

**R.4 State Consistency (10 elements)**
- Is PersistentVolume state consistent after pod restart? (storage controller)
- Does etcd recover after restart without data loss? (WAL, snapshots)
- Examples: StatefulSet pod recovery, volume reattachment, metadata consistency

---

### **Stakeholder Perspective (D.14) for Kubernetes**

**5 Perspectives × 12 Core Dimensions = 60 Sub-Assessments**

Each core dimension (Truth, Service, Harm, etc.) is assessed through each stakeholder lens:

```
Example: Harm Dimension

S.1 End-User (Developer):
  "Does K8s protect my app from being hacked?"
  Score: 0.80 (NetworkPolicy available; but requires setup)

S.2 Administrator:
  "Does K8s protect the cluster from node compromise?"
  Score: 0.85 (node isolation good; but kubelet has high privileges)

S.3 Developer (Platform Engineer):
  "Does K8s let us build security controls?"
  Score: 0.82 (good API for custom policies; complex to reason about)

S.4 Security Team:
  "Is K8s secure against known attack vectors?"
  Score: 0.78 (strong isolation; but RBAC misconfiguration risks exist)

S.5 Compliance Officer:
  "Can we audit K8s for regulatory requirements?"
  Score: 0.85 (audit logs comprehensive; but retention policy needed)

Harm Per-Stakeholder Scores:
  S.1: 0.80, S.2: 0.85, S.3: 0.82, S.4: 0.78, S.5: 0.85
  Spread: 0.85 - 0.78 = 0.07 (small divergence; all stakeholders agree Harm is ~0.82)
```

**Fairness Metric:** MIN(all perspectives) should be ≥ 0.75. If one < 0.60, flag as gap.

---

### **Temporal Consistency (D.15) for Kubernetes**

**T.1 Version-to-Version Consistency (K8s 1.28 → 1.29)**
- Do dimension scores change between versions?
- Measure Spearman ρ of dimension scores across versions
- Gate: ρ ≥ 0.85 (versions have stable trustworthiness profile)

**T.2 Patch Impact (Security Patches within Version)**
- Do patches improve or degrade trustworthiness?
- Example: CVE-2024-12345 fix → Harm dimension improves 0.78 → 0.85
- Measure: average delta in dimension scores post-patch

**T.3 Drift Detection (Undocumented Changes)**
- Are behavior changes between versions documented?
- Measure: % of test divergence between version pairs
- Gate: < 5% undocumented drift acceptable

**T.4 Long-Term Stability (12-Month Trajectory)**
- K8s v1.24 (12 months ago) vs. v1.29 (today): coherence trajectory
- Expected: stable (0.85 ± 0.05) or improving, not degrading

---

## PART VI: TIMELINE & MILESTONES

### **Phase 3b Full Timeline**

| Weeks | Dates | Subphase | Milestone | Owner |
|---|---|---|---|---|
| **1–3** | 2026-10-01 to 2026-10-20 | **3b.1** | v1.6 design finalized, K8s codebook drafted, 150 elements stratified | Codebook author |
| **3–5** | 2026-10-20 to 2026-11-03 | **3b.2** | Coder training κ ≥0.80, Layer 1 assessed (150 elements, 15 dims, 5 perspectives) | Coder team |
| **5–7** | 2026-11-03 to 2026-11-17 | **3b.3** | Layer 2 external validation (ρ ≥0.70), Layer 3 evaluator (A/B/C), Layer 4 red-team (§11–12 PASS) | Standards specialist, evaluator, red-team |
| **7–8** | 2026-11-17 to 2026-12-02 | **3b.4** | Layer 5 stakeholder feedback, v1.6 synthesis, v1.6-FROZEN release | Lead auditor, Z2 |

**Parallel Execution:**
- Phase 2 (Windows): Weeks 4–10 (2026-09-21 to 2026-11-15) → v1.0-FROZEN
- Phase 3b (K8s): Weeks 1–8 (2026-10-01 to 2026-12-02) → v1.6-FROZEN
- Overlap: Weeks 4–8 (both running in parallel)
- Knowledge transfer: Windows v1.0 codebook template → K8s v1.6 codebook

---

## PART VII: READINESS CHECKLIST

### **Pre-Phase 3b.1 Gate**

- [ ] v1.6 stakeholder feedback synthesis complete (due 2026-08-30)
- [ ] Resilience, Stakeholder Perspective, Temporal Consistency designs finalized
- [ ] K8s infrastructure (1.29 + 1.28 clusters) provisioned and ready
- [ ] Codebook author assigned (1 FTE)
- [ ] Z2 governance briefed on v1.6 pilot scope
- [ ] **PROCEED with Phase 3b.1 (2026-10-01)**

### **Phase 3b.1 → 3b.2 Gate**

- [ ] K8s codebook (§1–§7) complete and reviewed
- [ ] 150 elements stratified and sourced
- [ ] 21 practice elements prepared
- [ ] Coder team assigned (3–5 K8s specialists)
- [ ] Test infrastructure ready (K8s 1.29, 1.28, monitoring, chaos tools)
- [ ] **PROCEED with Phase 3b.2 Layer 1 training (2026-10-20)**

### **Phase 3b.2 → 3b.3 Gate**

- [ ] Coder training κ ≥ 0.80 (practice elements agreement)
- [ ] 150 elements coded (primary + 20% double-coding)
- [ ] Layer 1 coherence ≥ 0.85
- [ ] Per-stakeholder scores extracted (5 breakdowns)
- [ ] Temporal comparison documented (K8s 1.28 vs. 1.29)
- [ ] Stopping rules armed (no breaches, no divergence halts)
- [ ] **PROCEED with Phase 3b.3 Layers 2–4 (2026-11-03)**

### **Phase 3b.3 → 3b.4 Gate**

- [ ] Layer 2 external validation (NIST, CIS, CISA all ρ ≥ 0.70)
- [ ] Layer 3 evaluator rating (A or B acceptable; C blocks)
- [ ] Layer 4 red-team stress tests (§11.1–§12.2 all PASS)
- [ ] v1.6 dimensions operationalize as expected (Resilience, Stakeholder, Temporal working)
- [ ] **PROCEED with Phase 3b.4 Layer 5 & freeze (2026-11-17)**

### **Phase 3b.4 → Release Gate**

- [ ] Layer 5 stakeholder feedback (3+/4 groups say v1.6 is operationalizable)
- [ ] v1.6 performance validated (Resilience 0.83+, Stakeholder 0.84+, Temporal 0.83+)
- [ ] Synthesis report complete
- [ ] Z2 freeze authorization issued
- [ ] v1.6-FROZEN tagged and released
- [ ] **v1.6 GLOBAL RELEASE (2026-12-02)**

---

## PART VIII: SUCCESS CRITERIA

**Layer 1 Success:**
- Coherence ≥ 0.85 (expected: 0.85–0.92)
- κ ≥ 0.60 overall
- Per-stakeholder coherence all ≥ 0.80 (no perspective severely diverges)
- Temporal comparison shows K8s versions are similar (ρ ≥ 0.85)

**Layers 2–4 Success:**
- ρ ≥ 0.70 (NIST, CIS, CISA)
- Layer 3 rating A (or B with remediation)
- Layer 4 stress tests all PASS (§11.1–§12.2)

**Layer 5 Success:**
- Stakeholder feedback: 3+/4 groups say v1.6 dimensions are operationalizable
- Resilience dimension captures fault scenarios missing in v1.5
- Stakeholder Perspective reveals meaningful divergence (e.g., admin scores 0.10+ higher than developer)
- Temporal Consistency shows stability across K8s versions

**v1.6 Release Success:**
- All 5 layers PASS
- v1.6-FROZEN tagged (2026-12-02)
- Global release announced
- Documentation updated (v1.5 + v1.6 coexist; v1.6 recommended for infrastructure)

---

## SUMMARY

**Phase 3b is the v1.6 pilot validation running parallel with Phase 2 (Windows v1.5).**

- **Phase 3b.1 (Weeks 1–3):** v1.6 design finalized, K8s codebook drafted, 150 elements stratified
- **Phase 3b.2 (Weeks 3–5):** Layer 1 self-assessment (150 elements, 15 dims, 5 perspectives)
- **Phase 3b.3 (Weeks 5–7):** Layers 2–4 validation (external, evaluator, red-team)
- **Phase 3b.4 (Weeks 7–8):** Layer 5 stakeholder feedback, v1.6-FROZEN release

**Timeline:** 2026-10-01 to 2026-12-02 (8 weeks), parallel with Phase 2

**Gate Criteria:** All layers PASS + stakeholder validation → v1.6-FROZEN (2026-12-02)

---

**PHASE 3b EXECUTION PLAN: READY FOR DEPLOYMENT**  
**Awaiting:** v1.6 stakeholder feedback synthesis (due 2026-08-30)  
**Launch Date:** 2026-10-01 (Phase 3b.1)  
**Target Release:** v1.6-FROZEN (2026-12-02)  
**Parallel Track:** Phase 2 (Windows v1.5) + Phase 3b (K8s v1.6)

Wado. 🦅
