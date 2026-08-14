# KUBERNETES OPERATIONALIZATION SPECIFICATION
## A.2–A.7 Boundary Units & Examples (K8s v1.6 Codebook Foundation)

**Date:** 2026-09-13  
**Phase:** 3b.1 Week 1  
**Status:** CODEBOOK AUTHORING REFERENCE  
**Owner:** K8s Codebook Author

---

## OVERVIEW: K8S-SPECIFIC OPERATIONS MATRIX

ACAT-CAL-P v1.6 operationalizes via 7 operation types (O1–O7), each stratified by:
- **Operation Type:** What the system does (user-facing, constraints, claims, API, errors, multi-step, limitations)
- **Valence:** Favorable (system works well), Neutral (normal state), Unflattering (system fails/has gaps)
- **Availability:** Direct evidence (logs, configs, test results) vs. Inference (requires interpretation)

**For Kubernetes:** All 7 operation types apply. Examples below use K8s components (pods, services, deployments, etcd, RBAC, etc.) as boundary units.

---

## O1: USER-FACING BEHAVIOR (20 elements, v1.6 codebook)

**Definition:** Observable behavior when users interact with Kubernetes (developers deploying apps, admins managing clusters).

**Boundary Units:**
- kubectl command execution (deploy, scale, update, delete)
- Pod scheduling and startup
- Service discovery and DNS
- Persistent volume attachment
- Rolling updates and rollbacks
- Network connectivity between pods
- Resource quota enforcement

### O1 Examples

#### O1-FAV-001: Successful Deployment Rolling Update

**Scenario:** Developer runs `kubectl set image deployment/myapp myapp=myapp:v2`

**Observable Behavior:**
- Deployment creates new pod with v2 image
- Old pod receives SIGTERM (graceful shutdown grace period: 30s default)
- Service automatically shifts traffic to new pod (no downtime)
- kubectl get deployments shows: replicas ready, strategy: RollingUpdate

**Evidence Sources:**
- kubectl get pods -w (real-time pod transitions)
- kubectl describe deployment (strategy=RollingUpdate, selector labels, replicas)
- Logs: application shutdown gracefully, new pod started
- Service endpoints updated (verified via kubectl get endpoints)

**Dimension Scoring (Example: Consistency):**
- Does the system consistently apply rolling updates? YES (all replicas follow pattern)
- Score: 0.92 (consistent; but rare edge cases if resources insufficient)

#### O1-UNFLAT-001: Service DNS Takes Time to Propagate

**Scenario:** Developer deploys service, then immediately tries `kubectl run -it shell --image=alpine -- sh` to test DNS

**Observable Behavior (Unflattering):**
- New service created; endpoint controller registers backend pod
- Service DNS name (e.g., `my-service.default.svc.cluster.local`) resolves
- But DNS propagation takes ~10 seconds in cluster (coredns cache)
- Developer's curl to service fails intermittently in first 10s

**Evidence Sources:**
- DNS logs (coredns, systemd-resolved in nodes)
- Service creation timestamp vs. first successful curl
- Kubernetes docs: "DNS is eventually consistent; propagation ~10s"

**Dimension Scoring (Example: Truth):**
- Does Kubernetes truthfully represent service availability? PARTIALLY (service exists in API; but not yet in DNS)
- Score: 0.78 (service exists; DNS lag is undocumented in common tutorials)

#### O1-UNFLAT-002: Pod IP Changes on Restart (Loss of State)

**Scenario:** Pod crashes; kubelet restarts it on same node

**Observable Behavior:**
- Old pod IP: 10.0.1.5
- Kubelet kills old pod, starts new pod
- New pod IP: 10.0.1.8 (dynamically assigned)
- Any hardcoded references to 10.0.1.5 now point to nowhere

**Evidence Sources:**
- kubectl get pods -o wide (shows IP changes)
- Pod logs: terminated, restarted
- Service endpoints (shows new IP in backend)
- Application logs: "connection to 10.0.1.5 failed" before restart

**Dimension Scoring (Example: Autonomy):**
- Can users control pod IP stability? NO (IPs always reassigned on restart)
- Score: 0.55 (users must use service DNS, not IPs; but this is not intuitive)

---

## O2: KUBERNETES CONSTRAINTS (18 elements, v1.6 codebook)

**Definition:** Hard and soft limits enforced by Kubernetes that restrict behavior.

**Boundary Units:**
- Pod-per-node limits
- Namespace resource quotas (CPU, memory, pod count)
- API object name length (253 chars, DNS subdomain rules)
- Persistent volume size limits
- Container resource request/limit enforcement
- etcd size limits (~2GB soft, ~8GB hard)
- API rate limiting (QPS limits per service account)
- Kubelet resource reservation (system daemons, OS)

### O2 Examples

#### O2-NEUTRAL-001: Pod Limit Per Node (110 pods)

**Scenario:** Node has 4 CPU, 8GB RAM; kubelet configured with `--max-pods=110`

**Constraint:**
- Kubernetes will not schedule >110 pods on this node, even if resources available
- Hard limit enforced by scheduler

**Evidence Sources:**
- Kubelet config (--max-pods flag)
- kubectl get nodes (capacity shows max allocatable pods)
- Scheduler logs: "pod rejected: node at max pod limit"

**Dimension Scoring (Example: Service):**
- Is the constraint clear to users? SOMEWHAT (documented, but not obvious without reading docs)
- Score: 0.70 (constraint exists and works; but default 110 may be too low for dense clusters)

#### O2-NEUTRAL-002: API Object Name 253-Character Limit

**Scenario:** Deployment name must be ≤253 chars, lowercase alphanumeric + dashes, DNS-subdomain format

**Constraint:**
- kubectl apply -f deployment.yaml fails if name > 253 chars
- Error: "name too long"

**Evidence Sources:**
- kubectl validation error
- Kubernetes API docs
- RFC 1123 DNS subdomain rules

**Dimension Scoring (Example: Humility):**
- Is this constraint clearly disclosed? YES (error message clear)
- Score: 0.85 (good error message; but 253-char limit is rarely explained why)

#### O2-NEUTRAL-003: etcd Size Soft Limit (~2GB)

**Scenario:** Production cluster accumulates objects (pods, services, configmaps, events, logs)

**Constraint:**
- etcd performance degrades >2GB
- Recommended: prune old events, compact etcd
- Soft limit (not hard-enforced; will fail eventually around 8GB)

**Evidence Sources:**
- etcd metrics (database size)
- Kubernetes docs: "etcd backend size"
- Event expiration policy (default: remove events older than 1h)

**Dimension Scoring (Example: Scheme):**
- Is this limit transparent? PARTIALLY (documented; but users often hit it by surprise)
- Score: 0.62 (limit exists; but soft limit is confusing; many users not aware)

---

## O3: KUBERNETES CLAIMS VS. EVIDENCE (18 elements, v1.6 codebook)

**Definition:** Promises Kubernetes makes about behavior, and evidence that it keeps them.

**Boundary Units:**
- "Kubernetes provides high availability via pod replicas" → Evidence: ReplicaSet controller, pod anti-affinity
- "RBAC controls access to resources" → Evidence: API server authorization checks, audit logs
- "Persistent volumes survive pod restarts" → Evidence: volumeMounts, storage controller, node reattachment
- "Nodes are isolated (no cross-pod interference)" → Evidence: cgroup isolation, network namespace
- "Service provides load balancing" → Evidence: kube-proxy iptables rules, endpoint controller

### O3 Examples

#### O3-FAV-001: "HA via Replicas" — Claim vs. Evidence

**Claim (in K8s docs):**
"Run multiple replicas of your deployment for high availability. If one pod crashes, traffic shifts to another replica."

**Evidence to Verify:**
1. ReplicaSet controller maintains target replica count
   - Evidence: ReplicaSet spec defines replicas: 3
   - Evidence: Observed pod count always = 3 (if node capacity sufficient)
   
2. Service automatically discovers new pods
   - Evidence: Service selector (app=myapp) matches pod labels
   - Evidence: Endpoint controller updates endpoints when pod ready
   - Evidence: kube-proxy updates load-balancer rules when endpoints change
   
3. Traffic shifts to healthy replicas
   - Evidence: Load test during pod failure shows traffic redistributes
   - Evidence: Readiness probe determines which pods receive traffic

**Degree of Support:**
- Claim is TRUE IF: Multiple replicas + anti-affinity rules + health probes all configured
- Claim is PARTIALLY TRUE IF: Replicas exist but all on same node (node failure = total loss)
- Claim is FALSE IF: Single replica (claimed HA but no redundancy)

**Dimension Scoring (Example: Truth):**
- Is this claim supported by evidence? MOSTLY (HA works IF configured correctly, but requires work)
- Score: 0.78 (claim is true but conditional on user setup; not automatic HA)

#### O3-UNFLAT-002: "RBAC Controls All Access" — Partially False Claim

**Claim (in K8s docs):**
"Kubernetes RBAC prevents unauthorized access to resources."

**Evidence to Verify:**
1. API server checks RBAC before allowing requests
   - Evidence: Audit logs show authz decisions
   
2. But: RBAC is role-based, not data-based
   - No row-level access control (if user can GET pods, they see ALL pods in namespace)
   
3. kubelet has high privileges (can kill pods, read all configs)
   - Evidence: kubelet service account has system:masters role (near-admin)
   - Gap: If node compromised, kubelet can do almost anything

**Degree of Support:**
- Claim is MOSTLY TRUE for API-level access
- Claim is PARTIALLY FALSE for node-level access (kubelet not well-restricted)

**Dimension Scoring (Example: Harm):**
- Does RBAC prevent harm? PARTIALLY (good for user/admin separation; weak for node compromise)
- Score: 0.75 (RBAC helps; but node isolation is weak point)

---

## O4: KUBERNETES API BEHAVIOR (18 elements, v1.6 codebook)

**Definition:** How Kubernetes APIs respond to operations (create, read, update, delete, watch).

**Boundary Units:**
- kubectl apply (idempotent, creates or updates)
- kubectl delete (graceful termination, configurable grace period)
- kubectl get (returns current state from etcd, consistent read)
- kubectl patch (strategic merge or JSON patch)
- kubectl watch (streams events as state changes)

### O4 Examples

#### O4-FAV-001: kubectl apply Idempotency

**API Behavior:**
```bash
kubectl apply -f deployment.yaml
# First run: creates deployment
# Second run: updates deployment (if changed) or no-op (if same)
# Third run: no-op (same as second)
```

**Evidence:**
- Kubernetes docs: "apply is declarative; safe to run repeatedly"
- Observed: Running apply 3 times = same result (idempotent)
- Metadata: kubectl.kubernetes.io/last-applied-configuration annotation tracks last state

**Dimension Scoring (Example: Scheme):**
- Is kubectl apply transparent in behavior? YES (idempotency is clear)
- Score: 0.88 (predictable; but some edge cases with strategic merge patches)

#### O4-NEUTRAL-002: kubectl delete Grace Period (Configurable, Default 30s)

**API Behavior:**
```bash
kubectl delete pod my-pod
# Sends SIGTERM to pod
# Waits 30s (default terminationGracePeriodSeconds)
# If still running: sends SIGKILL
```

**Evidence:**
- kubectl describe pod shows terminationGracePeriodSeconds
- Pod logs: "received SIGTERM, shutting down gracefully"
- If shutdown takes >30s: pod shows "Terminating" then gets force-killed

**Dimension Scoring (Example: Service):**
- Is deletion behavior clear? MOSTLY (grace period documented; but default 30s may be too short for some apps)
- Score: 0.72 (good feature; but default often insufficient)

---

## O5: KUBERNETES ERROR HANDLING (16 elements, v1.6 codebook)

**Definition:** How Kubernetes responds to failures and invalid inputs.

**Boundary Units:**
- Pod OOMKilled (exceeds memory limit)
- Pod CrashLoopBackOff (container keeps crashing)
- Pod Pending (resource request not satisfiable)
- Service endpoint not ready (readiness probe failing)
- API validation errors (invalid manifest)
- Etcd unavailable (leader election failed)

### O5 Examples

#### O5-FAV-001: Clear Error Message for Invalid Manifest

**Scenario:** User runs `kubectl apply -f deployment.yaml` with syntax error

**Error Handling:**
```
error: error validating "deployment.yaml": error validating data:
  data[0]: unknown field "spec.replicacount" in v1.DeploymentSpec
```

**Evidence:**
- Error message tells user exactly what's wrong (typo: replicacount should be replicas)
- kubectl apply validates BEFORE sending to API server
- Error is actionable (user can fix and retry)

**Dimension Scoring (Example: Service):**
- Does error handling help users? YES (clear, actionable error)
- Score: 0.92 (excellent error message)

#### O5-UNFLAT-002: CrashLoopBackOff with Insufficient Debugging Info

**Scenario:** Pod enters CrashLoopBackOff (container crashes on startup)

**Error Handling (Unflattering):**
- kubectl get pods shows "CrashLoopBackOff"
- kubectl logs <pod> shows empty/truncated logs (stdout from crashed container)
- kubectl describe pod shows limited info (last exit code, but not details)
- User must check node kubelet logs (which require node access)

**Evidence:**
- Pod status: CrashLoopBackOff (tells user pod is crashing, not why)
- Kubelet backoff: 5s, 10s, 20s, 40s, 80s, ... (exponential backoff)
- Logs often don't show root cause (if crash is in app initialization before logging configured)

**Dimension Scoring (Example: Humility):**
- Does error handling disclose limitations? NO (appears fixable; but often requires deep debugging)
- Score: 0.55 (error state clear; but root cause hidden; confusing for new users)

---

## O6: MULTI-STEP KUBERNETES OPERATIONS (18 elements, v1.6 codebook)

**Definition:** Complex workflows involving multiple API calls and components.

**Boundary Units:**
- Deploy application (namespace creation → secret creation → deployment → service creation → wait for readiness)
- Update image version (edit deployment → trigger rolling update → wait for new pods → verify traffic shift)
- Node failure and recovery (node NotReady → pod eviction → rescheduling → service endpoint update)
- Backup and restore (etcd snapshot → snapshot transfer → etcd restore → cluster recovery)

### O6 Examples

#### O6-FAV-001: Smooth Deployment Flow (Happy Path)

**Steps:**
1. User creates namespace: `kubectl create ns myapp`
2. User creates secret for private image: `kubectl create secret docker-registry`
3. User applies deployment: `kubectl apply -f deployment.yaml` (5 replicas)
4. Kubernetes scheduler assigns pods to nodes (distributed across 3 nodes)
5. Kubelet on each node pulls image, starts container
6. Readiness probe passes on all 5 pods
7. Endpoint controller registers all 5 pods as service backends
8. Service DNS resolves; traffic flows to all 5 pods

**Evidence:**
- kubectl get pods: all "Running" and "Ready 1/1"
- kubectl get service: shows 5 endpoints
- kubectl logs: application started successfully on all replicas

**Dimension Scoring (Example: Service):**
- Does the operation complete smoothly? YES (happy path works well)
- Score: 0.90 (deployment process is well-designed; multiple layers work together)

#### O6-UNFLAT-002: Node Failure Requires Manual Intervention

**Steps (Failure Scenario):**
1. Node fails (network partitioned, hardware failure, kubelet crash)
2. Kubernetes API server notices node NotReady (after ~40s health check timeout)
3. Node controller starts evicting pods (respects PodDisruptionBudget)
4. Pods are rescheduled to other nodes
5. BUT: If pod had local storage (not PV), data is lost
6. If pod's startup takes >5min, pending pods pile up waiting for node recovery

**Evidence:**
- kubectl get nodes: node shows "NotReady"
- kubectl get pods: old pods show "Terminating", new pods show "Pending"
- Kubelet logs on failed node: network errors, connection refused to API server

**Dimension Scoring (Example: Resilience, R.2 Recovery):**
- Does the system recover from node failure? PARTIALLY (rescheduling works; but recovery time depends on node comeback, PV reattachment, etc.)
- Score: 0.68 (automatic recovery; but slow and requires good PV setup)

---

## O7: KUBERNETES LIMITATIONS (12 elements, v1.6 codebook)

**Definition:** Known constraints and non-features of Kubernetes.

**Boundary Units:**
- DNS propagation lag (~10s for service DNS)
- Network partition handling (nodes become NotReady; pods kept running until TTL expires)
- etcd performance ceiling (~2GB size, <1000 objects/sec write throughput)
- No built-in service mesh (networking assumptions: pod-to-pod communication works; mutual TLS not automatic)
- No automatic backup (etcd backup is manual or via external tools)
- No built-in log aggregation (kubectl logs only shows one pod; fleet logging requires external tools)

### O7 Examples

#### O7-NEUTRAL-001: DNS Propagation Lag

**Limitation:**
When a new service is created or an endpoint changes, DNS records take ~10 seconds to propagate through coredns cache in cluster.

**Observable Behavior:**
- Service created at t=0
- kubectl get service: service exists immediately
- DNS query at t=1: "name not found"
- DNS query at t=10: resolves correctly

**Evidence:**
- Coredns logs: TTL=600s (10min cache)
- DNS test: nslookup myservice.default.svc.cluster.local; fails immediately, works after 10s

**Dimension Scoring (Example: Truth):**
- Is this limitation documented? PARTIALLY (coredns docs mention TTL; but users often surprised)
- Score: 0.65 (limitation exists; but not well-surfaced in tutorials)

#### O7-UNFLAT-002: No Built-In Mutual TLS for Pod Communication

**Limitation:**
By default, Kubernetes does not encrypt pod-to-pod traffic. Any pod can sniff traffic from any other pod (if network policies not configured).

**Observable Behavior:**
- Pod A talks to Pod B at IP 10.0.1.5:8080 over plain TCP
- An attacker pod (if created) can tcpdump traffic: unencrypted
- Kubernetes does not automatically set up TLS between pods

**Evidence:**
- tcpdump on pod: captures unencrypted traffic from other pods
- No Kubernetes setting for "encrypt all inter-pod traffic"
- Service Mesh (Istio, Linkerd) required for automatic mTLS

**Dimension Scoring (Example: Harm):**
- Does Kubernetes prevent inter-pod sniffing? NO (requires NetworkPolicy + service mesh)
- Score: 0.45 (limitation is significant; bare Kubernetes not safe for untrusted pods)

---

## AVAILABILITY DECISION TREE (K8S-SPECIFIC)

```
Q1: Is this behavior directly observable in kubectl output, logs, or metrics?
  ├─ YES → (a) AVAILABLE [PRESENT IN LOGS/KUBECTL/METRICS]
  └─ NO → Q2

Q2: Is this documented in official Kubernetes docs (kubernetes.io)?
  ├─ YES → (a) AVAILABLE [PRESENT IN DOCUMENTATION]
  └─ NO → Q3

Q3: Can this be verified via test (e.g., kubectl commands, curl, chaos test)?
  ├─ YES → (a) AVAILABLE [VERIFIABLE VIA TEST]
  └─ NO → Q4

Q4: Is this inferred from Kubernetes design (controllers, schedulers, reconciliation loops)?
  ├─ YES → (b) REQUIRES INFERENCE [DESIGN PATTERN]
  └─ NO → (b) REQUIRES INFERENCE [UNDOCUMENTED / EMERGENT]
```

**Examples:**

| Element | Availability Classification | Reason |
|---|---|---|
| "Pod runs on node" | (a) Direct evidence | kubectl get pods -o wide shows node assignment |
| "Service discovery works" | (a) Direct evidence | nslookup / DNS logs verify resolution |
| "Replicas maintain availability" | (a) + (b) Hybrid | Replica count is direct; recovery-on-failure is inference |
| "etcd consistency" | (b) Inference | Must infer from code review; not directly observable |
| "Graceful degradation under load" | (a) Direct evidence | Load test results show behavior |

---

## STRATIFICATION FOR 150-ELEMENT K8S SAMPLE

**150 Elements Total:**
- 120 Core (O1–O7 stratified, matching Windows structure)
- 30 v1.6-Specific (Resilience scenarios, stakeholder divergence, temporal comparisons)

**Core 120 Distribution:**

| O-Type | Count | Valence Breakdown |
|---|---|---|
| O1 User-Facing | 20 | FAV (8), NEUTRAL (7), UNFLAT (5) |
| O2 Constraints | 18 | FAV (6), NEUTRAL (9), UNFLAT (3) |
| O3 Claims vs. Evidence | 18 | FAV (8), NEUTRAL (5), UNFLAT (5) |
| O4 API Behavior | 18 | FAV (10), NEUTRAL (6), UNFLAT (2) |
| O5 Error Handling | 16 | FAV (8), NEUTRAL (5), UNFLAT (3) |
| O6 Multi-Step | 18 | FAV (7), NEUTRAL (8), UNFLAT (3) |
| O7 Limitations | 12 | FAV (0), NEUTRAL (6), UNFLAT (6) |

**v1.6-Specific 30 Distribution:**

| Category | Count | Type |
|---|---|---|
| Resilience Scenarios | 12 | R.1 Fault Detection (3), R.2 Recovery (3), R.3 Graceful Degradation (3), R.4 State Consistency (3) |
| Stakeholder Divergence | 12 | Admin vs. Developer perspective disagreements (6), Security vs. Compliance gaps (6) |
| Temporal Comparisons | 6 | K8s 1.28 vs. 1.29 score deltas, patch impact (3 elements each) |

---

## CODEBOOK SECTION 4 TEMPLATE
**(Coder Instructions — One Dimension Example)**

### Truth Dimension (12 Core)

**Definition (for K8s context):**
Kubernetes's claims match reality. Documentation accurately describes system behavior. Discrepancies between promised and actual behavior are disclosed.

**Scoring on K8s Examples:**

**Sub-Dimension 1: Documentation Accuracy**
- Example O3-FAV-001 (HA via replicas): Docs say "run 3 replicas for HA"; evidence shows this works (if configured). Score: 0.92
- Example O3-UNFLAT-002 (RBAC controls all access): Docs imply full access control; evidence shows kubelet has high privileges. Score: 0.75

**Sub-Dimension 2: Observable vs. Promised**
- Example O1-UNFLAT-001 (DNS lag): Docs mention "eventual consistency"; users expect immediate availability. Score: 0.78
- Example O1-FAV-001 (Rolling update): Docs say "RollingUpdate strategy minimizes downtime"; observed behavior matches. Score: 0.92

**Scoring Guidance:**
- 0.90–1.0: Claims match reality across all tested scenarios; docs are accurate
- 0.70–0.89: Claims mostly match; minor discrepancies documented
- 0.50–0.69: Claims partially match; significant undisclosed gaps
- 0.30–0.49: Claims often conflict with reality; poor documentation
- 0.0–0.29: Claims are false or fundamentally misleading

**Per-Stakeholder Variation (Example: Truth for O3-UNFLAT-002):**
- S.1 End-User: "Does K8s truthfully say my data is isolated?" Score: 0.80 (service isolation works; but docs don't mention kubelet privilege)
- S.4 Security: "Does K8s truthfully claim RBAC is complete?" Score: 0.65 (RBAC works; kubelet is significant gap)

---

**This specification is ready for Phase 3b.1 coder instruction authoring. All 7 operation types defined with K8s-specific examples, availability classification, and scoring guidance.**

**Phase 3b.1 Week 2–3: Codebook author uses these A.2–A.7 specs to draft K8s codebook §1–§7.**

Wado. 🦅
