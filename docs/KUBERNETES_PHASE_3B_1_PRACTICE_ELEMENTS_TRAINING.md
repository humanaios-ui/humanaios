# KUBERNETES PHASE 3b.1: 21 PRACTICE ELEMENTS & TRAINING GUIDE
## Codebook Author Training (Weeks 1–3, 2026-10-01 to 2026-10-20)

**Status:** ✓ READY FOR CODEBOOK AUTHOR  
**Purpose:** Train codebook author on v1.6 dimensions (Resilience, Stakeholder, Temporal) using K8s-specific examples  
**Gate:** Codebook author demonstrates understanding; can draft coder instructions confidently

---

## OVERVIEW: 21 PRACTICE ELEMENTS FOR K8S CODEBOOK AUTHORING

**Distribution (3 per O-type):**
- O1 (User-Facing): 3 elements (K8s-specific: deployments, services, pod lifecycle)
- O2 (Constraints): 3 elements (pod limits, quotas, etcd size, resource requests)
- O3 (Claims vs. Evidence): 3 elements (HA, RBAC, state consistency)
- O4 (API Behavior): 3 elements (kubectl idempotency, delete graceful period, get consistency)
- O5 (Error Handling): 3 elements (validation errors, CrashLoopBackOff, Pending pods)
- O6 (Multi-Step): 3 elements (deployment flow, rolling update, node failure recovery)
- O7 (Limitations): 3 elements (DNS lag, network partition, no mTLS)

**Purpose:** Codebook author reviews these elements and understands:
1. How Windows Layer 1 practice elements are structured
2. How v1.6 dimensions (Resilience, Stakeholder, Temporal) will be scored
3. How 5 perspectives apply to real K8s scenarios
4. How to write similar elements for 120 core + 30 v1.6 elements

---

## O1: USER-FACING BEHAVIOR (K8S-SPECIFIC)

### O1-FAV-001: Successful Pod Deployment with Scaling

**Scenario:** Developer deploys application via `kubectl apply -f deployment.yaml` (3 replicas).

**Observable Behavior:**
- Kubectl creates Deployment object
- ReplicaSet controller creates 3 Pod objects
- Kubelet on each node pulls image, starts container
- Readiness probe passes; pods show "Ready 1/1"
- Service endpoints updated; traffic load-balanced across 3 pods

**Evidence Sources:**
- kubectl get pods -w (real-time pod startup)
- kubectl describe deployment (replicas, selector, strategy)
- kubectl get svc (endpoints updated)
- Logs: application started on all 3 replicas

**Dimension Scores (Example for Truth):**
- **Core Truth (D.1):** 0.92 (Docs say "Deployment creates replicas"; observed behavior matches)
- **Resilience R.1 (Fault Detection):** 0.88 (Pod failure detected by kubelet within 30s)
- **Stakeholder S.1 (End-User):** 0.92 (Developer sees deployment work as expected)
- **Stakeholder S.2 (Admin):** 0.90 (Operator can monitor pod status reliably)
- **Stakeholder S.4 (Security):** 0.78 (Deployment works; but no security validation of image source)

**Coherence (across 12 dims × 5 perspectives = 60 scores): Expected ~0.05 (tight clustering for FAV)**

**Element Classification:**
- O-Type: O1
- Valence: FAV
- Availability: (a) Direct Evidence (kubectl output, logs)

---

### O1-UNFLAT-002: Pod IP Changes on Restart (Loss of Hardcoded References)

**Scenario:** Pod crashes and is restarted; receives different IP address.

**Observable Behavior (Unflattering):**
- Pod IP: 10.0.1.5 (initial)
- Pod crashes → kubelet restarts it
- New Pod IP: 10.0.1.8 (dynamically reassigned)
- Hardcoded references to 10.0.1.5 now point to nowhere

**Evidence Sources:**
- kubectl get pods -o wide (shows IP changes)
- Application logs: "connection to 10.0.1.5 failed" (after IP change)
- Pod events: "Pod restarted"

**Dimension Scores (Example for Autonomy):**
- **Core Autonomy (D.4):** 0.55 (Users cannot control pod IP; must use Service DNS)
- **Resilience R.4 (State Consistency):** 0.68 (Pod restarts, but network identity changes)
- **Stakeholder S.1 (End-User):** 0.45 (Developer must use Service DNS; hardcoded IPs fail)
- **Stakeholder S.2 (Admin):** 0.72 (Admin understands IP reassignment; expected behavior)
- **Stakeholder S.5 (Compliance):** 0.65 (State change is auditable; but identity shift)

**Coherence: Expected ~0.08 (moderate variance; perspectives diverge on severity)**

**Element Classification:**
- O-Type: O1
- Valence: UNFLAT
- Availability: (a) Direct Evidence (kubectl, logs)

---

### O1-NEUTRAL-003: Service DNS Propagation Lag (~10 seconds)

**Scenario:** New Service created; developer immediately tries to resolve DNS.

**Observable Behavior (Neutral):**
- kubectl create service my-app
- nslookup my-app.default.svc.cluster.local at t=1s: "name not found"
- nslookup at t=10s: resolves successfully
- DNS propagation lag: ~10 seconds (coredns TTL/cache)

**Evidence Sources:**
- DNS test script: nslookup over time
- coredns logs: TTL=600s (10min cache)
- Kubernetes docs: "eventual consistency"

**Dimension Scores (Example for Truth):**
- **Core Truth (D.1):** 0.78 (Docs say "eventual consistency"; users expect immediate)
- **Resilience R.1 (Fault Detection):** 0.72 (Service detection takes time)
- **Stakeholder S.1 (End-User):** 0.70 (Developer surprised by DNS lag)
- **Stakeholder S.3 (Developer):** 0.80 (Platform engineer knows about TTL; expected)
- **Stakeholder S.5 (Compliance):** 0.75 (Delay is auditable; timing is known)

**Coherence: Expected ~0.05 (tight clustering; straightforward neutral)**

**Element Classification:**
- O-Type: O1
- Valence: NEUTRAL
- Availability: (a) Direct Evidence (DNS queries, coredns logs)

---

## O2: KUBERNETES CONSTRAINTS (K8S-SPECIFIC)

### O2-NEUTRAL-001: Pod-per-Node Limit (110 by default)

**Scenario:** Kubelet configured with `--max-pods=110` (default for most node types).

**Observable Behavior:**
- Node has capacity for 110 pods maximum
- Scheduler refuses to schedule 111th pod (rejected)
- Kubelet logs: "pod rejected: node at max pod limit"
- Hard constraint enforced

**Evidence Sources:**
- kubectl describe node (shows: "Allocated resources" and max capacity)
- Kubelet config: --max-pods flag
- Scheduler logs: rejection reason

**Dimension Scores (Example for Service):**
- **Core Service (D.2):** 0.70 (Scheduler enforces limit; but limit may be too low for dense clusters)
- **Resilience R.2 (Recovery):** 0.65 (Pod scheduling fails if node full; no auto-recovery)
- **Stakeholder S.2 (Admin):** 0.75 (Constraint is documented; admin can adjust)
- **Stakeholder S.3 (Developer):** 0.60 (Developer sees "Pending" pods; doesn't understand why)
- **Stakeholder S.5 (Compliance):** 0.80 (Constraint enforcement is auditable)

**Coherence: Expected ~0.08 (perspectives diverge on awareness/reasonableness)**

**Element Classification:**
- O-Type: O2
- Valence: NEUTRAL
- Availability: (a) Direct Evidence (kubectl describe, logs)

---

### O2-NEUTRAL-002: etcd Size Soft Limit (~2GB recommended, ~8GB hard)

**Scenario:** etcd database grows over time as objects accumulate.

**Observable Behavior:**
- etcd performance degrades >2GB (soft limit)
- No hard limit enforced; will eventually fail around 8GB
- Admin must manually prune events or use etcd compaction

**Evidence Sources:**
- etcd metrics: database size
- Kubernetes docs: "etcd backend storage"
- Event expiration: default 1 hour (auto-prune)

**Dimension Scores (Example for Humility):**
- **Core Humility (D.6):** 0.62 (Soft limit is confusing; not clearly disclosed)
- **Resilience R.4 (Consistency):** 0.70 (Consistency maintained; but performance degrades)
- **Stakeholder S.2 (Admin):** 0.50 (Admin often surprised by etcd hitting soft limit)
- **Stakeholder S.5 (Compliance):** 0.75 (Monitoring and alerts available if configured)

**Coherence: Expected ~0.10 (higher variance; depends on admin awareness)**

**Element Classification:**
- O-Type: O2
- Valence: NEUTRAL
- Availability: (b) Requires Inference (soft limit is inferred from performance)

---

### O2-UNFLAT-003: No Built-In Rate Limiting on API Requests (Default Open)

**Scenario:** Kubernetes API server has no rate limiting enabled by default for user requests.

**Observable Behavior (Unflattering):**
- One user can issue unlimited API requests
- Other users' requests may be starved
- No fair queuing by default
- Admins must manually configure API rate limiting (not enabled)

**Evidence Sources:**
- API server logs: request rate
- kubectl: --request-timeout flag (client-side; server has no enforcement)
- Kubernetes docs: "API rate limiting" (optional feature)

**Dimension Scores (Example for Fair):**
- **Core Fair (D.11):** 0.45 (No built-in fairness; one user can monopolize API)
- **Resilience R.1 (Detection):** 0.40 (Rate limiting not detected; API starves silently)
- **Stakeholder S.2 (Admin):** 0.50 (Admin must manually configure; not default)
- **Stakeholder S.3 (Developer):** 0.35 (Developer's requests starved by heavy user; no visibility)
- **Stakeholder S.5 (Compliance):** 0.60 (No audit trail of rate limiting)

**Coherence: Expected ~0.12 (high variance; serious fairness gap)**

**Element Classification:**
- O-Type: O2
- Valence: UNFLAT
- Availability: (a) Direct Evidence (API logs, kubernetes docs)

---

## O3–O7: REMAINING 12 K8S PRACTICE ELEMENTS

*(Condensed for brevity; full elements follow O1–O2 pattern)*

### O3: CLAIMS VS. EVIDENCE (3 elements)

**O3-FAV-001: "High Availability via Pod Replicas"**
- Claim matches evidence; replicas work well
- Score: 0.88 (true; but requires proper configuration)

**O3-NEUTRAL-002: "RBAC Controls All Access"**
- Claim partially true; RBAC works for API; but kubelet privilege gap
- Score: 0.75 (mostly true; significant exception: kubelet)

**O3-UNFLAT-003: "K8s Provides Automatic Security"**
- Claim is false; bare K8s has no mTLS, unencrypted traffic, no network policies by default
- Score: 0.45 (claim is significantly false; security requires setup)

---

### O4: API BEHAVIOR (3 elements)

**O4-FAV-001: "kubectl apply is Idempotent"**
- Multiple applies produce same result
- Score: 0.92 (very reliable; edge cases exist)

**O4-NEUTRAL-002: "kubectl delete Respects Graceful Termination"**
- Pod receives SIGTERM; waits 30s before SIGKILL
- Score: 0.80 (works well; default 30s may be too short)

**O4-UNFLAT-003: "kubectl get Always Returns Current State"**
- API reads are consistent; but stale reads possible during network issues
- Score: 0.65 (mostly consistent; edge cases exist)

---

### O5: ERROR HANDLING (3 elements)

**O5-FAV-001: "Clear Validation Error for Invalid YAML"**
- kubectl apply rejects invalid manifests with clear error
- Score: 0.92 (excellent error message)

**O5-NEUTRAL-002: "Pod Pending Status Explains Resource Shortage"**
- Status shows "Pending"; requires deep inspection to understand why
- Score: 0.70 (status clear; reason requires investigation)

**O5-UNFLAT-003: "CrashLoopBackOff Debugging"**
- Pod shows CrashLoopBackOff; root cause often hidden
- Score: 0.55 (status clear; root cause obscure)

---

### O6: MULTI-STEP OPERATIONS (3 elements)

**O6-FAV-001: "Smooth Application Deployment"**
- Deploy app flow: namespace → secret → deployment → service → readiness
- Score: 0.90 (well-designed flow)

**O6-NEUTRAL-002: "Rolling Update with Traffic Shift"**
- Old pods → new pods → service endpoints updated
- Score: 0.82 (smooth; but requires readiness probes)

**O6-UNFLAT-003: "Node Failure Recovery"**
- Node fails → pods evicted → rescheduled → delayed recovery
- Score: 0.65 (recovery works; but slow and requires PVs to be available)

---

### O7: LIMITATIONS (3 elements)

**O7-NEUTRAL-001: "DNS Propagation Lag (10 seconds)"**
- Service DNS takes time to propagate through coredns
- Score: 0.70 (limitation real; often undisclosed)

**O7-NEUTRAL-002: "Network Partition Handling"**
- Nodes become NotReady; pods stay running until TTL expires
- Score: 0.75 (behavior consistent; recovery uncertain)

**O7-UNFLAT-003: "No Built-In Encryption for Pod Traffic"**
- Pod-to-pod traffic is plain text by default (no mTLS)
- Score: 0.45 (serious limitation; requires service mesh to fix)

---

## CODEBOOK AUTHOR TRAINING FLOW

**Week 1 (2026-10-01 to 2026-10-07):**

1. **Read all 21 practice elements** (this document)
2. **Identify scoring patterns:**
   - FAV elements: coherence tight (0.03–0.05), scores mostly 0.80+
   - NEUTRAL elements: coherence moderate (0.05–0.08), scores 0.70–0.85
   - UNFLAT elements: coherence higher (0.08–0.12), scores 0.50–0.70

3. **Understand perspective variation:**
   - S.1 (End-User): focuses on ease of use, surprise factors
   - S.2 (Admin): focuses on manageability, reliability
   - S.3 (Developer): focuses on API stability, extensibility
   - S.4 (Security): focuses on attack surface, audit trails
   - S.5 (Compliance): focuses on auditability, immutability

4. **Understand v1.6 dimensions:**
   - **Resilience:** How well does K8s detect faults and recover?
   - **Stakeholder:** Do perspectives converge or diverge on this element?
   - **Temporal:** Does this element's score change between K8s versions?

5. **Draft coder instruction template:**
   - For each of 12 core dimensions, write: definition, scoring scale (0–1), sub-dimensions, worked examples
   - Include how perspectives might score differently
   - Note where convergence/divergence expected

**Week 2 (2026-10-07 to 2026-10-14):**

6. **Begin K8s codebook draft (§1–§4):**
   - Use Windows codebook as template
   - Adapt all 7 O-types to K8s examples
   - Write 2–3 worked examples per dimension (using these 21 practice elements as inspiration)

7. **Develop per-perspective scorings:**
   - Write S.1–S.5 guides explaining how each perspective scores this element
   - Example: "Why S.1 (End-User) scores O1-FAV-001 (deployment) 0.92 vs. S.4 (Security) scores 0.78"

**Week 3 (2026-10-14 to 2026-10-20):**

8. **Finalize codebook + practice elements:**
   - Complete §5–§7 (protocols, stopping rules, agreement monitoring)
   - Create 21 K8s practice elements (mirror Windows structure)
   - Draft solution key (expected scores for K8s practice elements)

9. **Prepare training materials:**
   - Summary sheet: "How to score each dimension for K8s"
   - Quick reference: "Perspective differences cheat sheet"
   - Example scoresheets (blank templates)

10. **Z2 governance review:**
    - Present codebook to Z2
    - Explain v1.6 dimensions operationalization
    - Confirm ready for coder training (Phase 3b.2)

---

## KEY TEACHING POINTS FOR CODEBOOK AUTHOR

### **Teaching Point 1: Fairness Gate in Stakeholder Perspective**

When perspectives disagree significantly (MIN < 0.75), this signals a **design gap** that should be discussed in Layer 5 feedback (Week 7).

Example: O1-UNFLAT-002 (Pod IP changes)
- S.1 (End-User): 0.45 (frustrated by hardcoded IP failure)
- S.2 (Admin): 0.72 (understands IP reassignment)
- Divergence: 0.27 (gap indicates design issue: should K8s preserve pod identity?)

### **Teaching Point 2: Coherence Variance by Valence**

- FAV elements: tight coherence (0.03–0.05) — all dimensions score high
- NEUTRAL elements: moderate coherence (0.05–0.08) — mixed dimension scores
- UNFLAT elements: high coherence (0.08–0.12) — many low scores, consistent patterns

This is **expected**. Coders may disagree on UNFLAT interpretation more than FAV.

### **Teaching Point 3: Resilience vs. Core Dimensions**

Resilience (D.13) is new in v1.6. Compare how it scores vs. core dimensions:

Example: O1-UNFLAT-002 (Pod restart)
- **Service (D.2):** 0.68 (pod restarts; service works)
- **Resilience R.2 (Recovery):** 0.68 (recovery MTTR is reasonable)
- **Consistency (D.10):** 0.75 (state is consistent post-restart)

Resilience complements core dims; doesn't replace them.

### **Teaching Point 4: Temporal Tracking**

For elements assessed across K8s versions (1.28 vs. 1.29):

Example: O2-NEUTRAL-002 (etcd soft limit)
- K8s 1.28: soft limit 2GB, hard limit 8GB (score 0.62)
- K8s 1.29: soft limit 3GB, hard limit 10GB (score 0.68, improved)
- Temporal delta: +0.06 (improvement; drift = 0.06, acceptable)

Track this in Layer 1; analyze in Layer 5 feedback.

---

## PRACTICE ELEMENT DIFFICULTY MATRIX

**For codebook author to understand coder difficulty:**

| O-Type | FAV Difficulty | NEUTRAL Difficulty | UNFLAT Difficulty |
|---|---|---|---|
| O1 | Easy (observable) | Moderate (timing) | Hard (interpretation) |
| O2 | Easy (documented) | Easy (clear constraint) | Moderate (soft limits) |
| O3 | Easy (claim vs reality) | Moderate (partial truths) | Hard (false claims) |
| O4 | Easy (API works) | Moderate (edge cases) | Hard (inconsistent) |
| O5 | Easy (clear errors) | Moderate (unclear errors) | Hard (silent failures) |
| O6 | Moderate (many steps) | Moderate (recovery) | Hard (failures) |
| O7 | N/A | Moderate (inference) | Moderate (inference) |

**Prediction:** Coders will have highest κ on O1/O2 FAV elements, lowest κ on O3/O5/O6 UNFLAT elements.

---

## CODEBOOK AUTHOR SELF-ASSESSMENT

**Before Week 1 ends, answer:**

1. Can you explain why O1-FAV-001 (deployment) scores 0.92 on Truth but only 0.55 on Autonomy?
   ➜ Truth: behavior matches docs; Autonomy: users can't control pod IP

2. Can you predict how S.4 (Security) might score O2-UNFLAT-003 (no rate limiting) differently from S.2 (Admin)?
   ➜ S.4 focuses on attack surface (score low); S.2 focuses on managability (score higher)

3. Can you write a coder instruction for the "Service" dimension using O1-FAV-001 as example?
   ➜ "Service measures whether the system is available and reliable for users. For O1-FAV-001 (deployment), Service scores 0.94 because..."

**If you can't answer these, escalate to Carly before proceeding with Week 2 codebook drafting.**

---

**KUBERNETES PHASE 3b.1: TRAINING ELEMENTS READY**

**Next Step:** Codebook author reviews these 21 elements, confirms understanding of v1.6 dimensions and perspective variation, then proceeds to draft K8s codebook (Week 2).

Wado. 🦅
