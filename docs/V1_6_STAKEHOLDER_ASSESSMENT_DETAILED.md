# v1.6 STAKEHOLDER PERSPECTIVE ASSESSMENT FRAMEWORK
## 5 Frames × 12 Core Dimensions (Phase 3b.2 Coder Training Reference)

**Date:** 2026-09-13  
**Phase:** 3b Preparation / 3b.2 Coder Training  
**Status:** REFERENCE GUIDE FOR CODER TEAMS  
**Purpose:** Each perspective scores all 12 dimensions independently; this guide explains how.

---

## OVERVIEW

**5 Stakeholder Perspectives (S.1–S.5):**
1. S.1: End-User (App developer deploying on K8s)
2. S.2: Administrator (Cluster operator, DevOps)
3. S.3: Developer (Platform engineer, API designer, SRE)
4. S.4: Security Team (Infrastructure security, CISO)
5. S.5: Compliance Officer (Audit, regulatory, GRC)

**12 Core Dimensions (scored by each perspective):**
Truth, Service, Harm, Autonomy, Value, Humility, Scheme, Power, Syc, Consist, Fair, Handoff

**Result:** 5 perspectives × 12 dimensions = 60 sub-scores per element (plus 15 overall dimension scores per element)

**Fairness Gate:** MIN(all 5 perspectives) ≥ 0.75 per dimension; if any < 0.60, flag design gap

---

## S.1: END-USER PERSPECTIVE (App Developer)

**Role:** Developer deploying containerized applications on Kubernetes

**Primary Question:** "Does Kubernetes work for me? Can I build, deploy, and run my apps reliably?"

**Concerns:** App availability, predictability, ease of use, cost of operation

---

### S.1 Dimension Scorings

#### Truth (S.1)
**Question:** "Does Kubernetes do what the documentation says it does?"

**Key Evidence:**
- Does kubectl behavior match docs? (deployments, services, scaling)
- Are there undocumented gotchas? (DNS lag, pod IP changes, etc.)
- Do tutorials match reality?

**Scoring Scale:**
- 0.90–1.0: Docs accurately describe my experience; no surprises
- 0.70–0.89: Docs mostly accurate; minor undisclosed quirks
- 0.50–0.69: Docs incomplete; common gotchas not mentioned
- 0.30–0.49: Docs often misleading; reality differs significantly
- 0.0–0.29: Docs are basically wrong for my use case

**Example (O1-UNFLAT-001):**
- Docs say: "Services provide stable DNS names for pods"
- Reality: DNS takes ~10s to propagate; not mentioned in quickstart
- S.1 Score: 0.78 (statement true; timing caveat undocumented)

---

#### Service (S.1)
**Question:** "Is Kubernetes reliable and available for my apps?"

**Key Evidence:**
- Do deployments work consistently?
- Does the cluster stay up during updates/failures?
- Can I count on it?

**Scoring Scale:**
- 0.90–1.0: Very reliable; rarely fails or surprises
- 0.70–0.89: Generally reliable; occasional issues
- 0.50–0.69: Moderately reliable; frequent gotchas
- 0.30–0.49: Unreliable; regular failures or downtime
- 0.0–0.29: Completely unreliable; unusable

**Example (O6-UNFLAT-002):**
- During node failure: pods reschedule, but some stay Pending (resource constraints)
- Recovery time: 5–10 minutes depending on node comeback, PV reattachment
- S.1 Score: 0.72 (recovery works; but slow and not guaranteed)

---

#### Harm (S.1)
**Question:** "Does Kubernetes protect my app from being compromised or data lost?"

**Key Evidence:**
- Network isolation: Can I trust pods not to sniff each other's traffic?
- Storage safety: Will my persistent volumes survive?
- Secret management: Are my API keys safe?

**Scoring Scale:**
- 0.90–1.0: Strong protections; my app feels secure
- 0.70–0.89: Good protections; minor gaps
- 0.50–0.69: Moderate protections; requires setup
- 0.30–0.49: Weak protections; significant gaps
- 0.0–0.29: No protections; very dangerous

**Example (O7-UNFLAT-002):**
- Bare Kubernetes: No encryption of pod-to-pod traffic
- Attacker pod could tcpdump my app's database calls (plain text)
- NetworkPolicy + service mesh required for security
- S.1 Score: 0.55 (dangerous by default; but fixable with extra tools)

---

#### Autonomy (S.1)
**Question:** "Can I control how my app runs? Or does the cluster make decisions for me?"

**Key Evidence:**
- Can I choose which node my pod runs on?
- Can I scale my deployment?
- Can I update my image without rebuilding?

**Scoring Scale:**
- 0.90–1.0: Full control; I can configure everything
- 0.70–0.89: Good control; some constraints
- 0.50–0.69: Limited control; cluster makes many decisions
- 0.30–0.49: Very limited; cluster mostly decides
- 0.0–0.29: No control; forced configuration

**Example (O1-UNFLAT-002):**
- Pod IP assignment: I don't control it (assigned by IPAM)
- Node selection: Scheduler decides (I can request via nodeSelector/affinity)
- Container startup: Kubelet decides (I can only set lifecycle hooks)
- S.1 Score: 0.65 (good control at deployment level; no control at pod/container level)

---

#### Value (S.1)
**Question:** "Does Kubernetes deliver on its promise? Does it make my life easier?"

**Key Evidence:**
- Do deployments save me work vs. manual VMs?
- Does auto-scaling help?
- Does the learning curve pay off?

**Scoring Scale:**
- 0.90–1.0: Huge value; much easier than alternatives
- 0.70–0.89: Good value; saves time/effort
- 0.50–0.69: Moderate value; mixed benefits/costs
- 0.30–0.49: Poor value; more trouble than it's worth
- 0.0–0.29: Negative value; worse than alternatives

**Example (O1-FAV-001):**
- Rolling updates: Kubernetes manages automatically; would be manual on VMs
- Scaling: Auto-scaling based on metrics; would require manual intervention
- Health checks: Kubernetes restarts failed pods; would require monitoring scripts
- S.1 Score: 0.88 (significant value; but requires learning Kubernetes concepts)

---

#### Humility (S.1)
**Question:** "Does Kubernetes clearly tell me what it can't do or doesn't know?"

**Key Evidence:**
- Are limitations documented?
- Does error messages clearly explain failures?
- Are edge cases flagged?

**Scoring Scale:**
- 0.90–1.0: Very transparent about limitations
- 0.70–0.89: Clear limitations; mostly helpful errors
- 0.50–0.69: Some limitations disclosed; errors unclear
- 0.30–0.49: Few limitations mentioned; errors often confusing
- 0.0–0.29: No acknowledgment of limitations; errors are unhelpful

**Example (O7-NEUTRAL-001):**
- DNS propagation lag: Docs mention "eventual consistency"; but app developers often surprised
- Error message for DNS not yet ready: "connection refused" (doesn't say why; Kubernetes doesn't explain DNS delay)
- S.1 Score: 0.62 (limitation exists and is documented; but not surfaced to developers)

---

#### Scheme (S.1)
**Question:** "Can I understand how Kubernetes works? Is its operation transparent?"

**Key Evidence:**
- Can I understand why my pod was scheduled to a node?
- Can I see what's happening in the cluster?
- Are configurations explicit or hidden?

**Scoring Scale:**
- 0.90–1.0: Very transparent; I can understand everything
- 0.70–0.89: Mostly transparent; some hidden decisions
- 0.50–0.69: Moderate transparency; significant black boxes
- 0.30–0.49: Poor transparency; hard to understand
- 0.0–0.29: Very opaque; feel like I'm guessing

**Example (O4-FAV-001):**
- kubectl apply: Declarative model; I can see what I declared
- kubectl describe: Shows pod details, including why it was scheduled there
- But: Scheduler decisions (node selection, pod disruption) are not easily observable
- S.1 Score: 0.80 (mostly transparent; but scheduler "why" questions hard to answer)

---

#### Power (S.1)
**Question:** "Who has power here? Me, the cluster, or some third party?"

**Key Evidence:**
- Can the cluster override my configs?
- Can an admin change my app without asking?
- Do quotas limit my power?

**Scoring Scale:**
- 0.90–1.0: I have power; cluster respects my decisions
- 0.70–0.89: Mostly my power; some cluster constraints
- 0.50–0.69: Shared power; cluster enforces quotas/policies
- 0.30–0.49: Cluster has most power; I follow rules
- 0.0–0.29: No power; cluster does what it wants

**Example (O2-NEUTRAL-002):**
- Pod count per namespace: Quota limits my ability to scale
- Node resource limits: Can't run if resources unavailable (cluster decides)
- Network policies: Admin can block my pod's traffic
- S.1 Score: 0.60 (I have power to deploy; but cluster enforces limits)

---

#### Syc (Synchronization) (S.1)
**Question:** "Do the different parts of Kubernetes stay in sync? Does my app and the cluster agree on state?"

**Key Evidence:**
- After I deploy, does the cluster do what I asked?
- Do controllers reconcile quickly?
- Are there state mismatches?

**Scoring Scale:**
- 0.90–1.0: Always in sync; no surprises
- 0.70–0.89: Mostly in sync; occasional delays
- 0.50–0.69: Eventually consistent; notable lags
- 0.30–0.49: Often out of sync; reconciliation slow
- 0.0–0.29: Chronic inconsistency; unreliable

**Example (O1-FAV-001):**
- I create a deployment; within ~5s, pods appear
- Service endpoints updated within ~5s
- All API objects consistent
- S.1 Score: 0.91 (fast sync; very reliable)

---

#### Consistency (S.1)
**Question:** "Is the system state consistent? Can I rely on what I read from the API?"

**Key Evidence:**
- If I read a pod status, is it current?
- Are there stale reads?
- Does the cluster recover from failures consistently?

**Scoring Scale:**
- 0.90–1.0: Always consistent; reliable reads
- 0.70–0.89: Mostly consistent; occasional staleness
- 0.50–0.69: Eventually consistent; notable staleness windows
- 0.30–0.49: Frequently inconsistent; hard to trust reads
- 0.0–0.29: Chronic inconsistency; unreliable

**Example (O4-FAV-001):**
- kubectl get pod: Returns current state (reads from etcd)
- Pod status: Updates within ~1s of state change
- No stale reads (if server is up)
- S.1 Score: 0.92 (very consistent; reliable API)

---

#### Fairness (S.1)
**Question:** "Does Kubernetes treat me the same as other users? Or does someone get preferential treatment?"

**Key Evidence:**
- Are resource quotas enforced equally?
- Do other tenants' issues impact my apps?
- Is QoS priority fair?

**Scoring Scale:**
- 0.90–1.0: Very fair; no favoritism
- 0.70–0.89: Mostly fair; some edge cases
- 0.50–0.69: Moderate fairness; some users get better treatment
- 0.30–0.49: Unfair; inequality obvious
- 0.0–0.29: Very unfair; preferential treatment rampant

**Example (O2-NEUTRAL-001):**
- Pod quota: All namespaces limited equally (fair)
- But: No prioritization between "important" and "test" apps (unfair if test app steals resources)
- S.1 Score: 0.72 (equal quotas are fair; but no priority QoS for fair urgency)

---

#### Handoff (S.1)
**Question:** "Is it clear who is responsible for what? If something fails, who fixes it?"

**Key Evidence:**
- Is it clear when Kubernetes is responsible vs. my app?
- Who debugs DNS issues? Me or Kubernetes?
- Who owns PersistentVolume lifecycle?

**Scoring Scale:**
- 0.90–1.0: Very clear responsibility boundaries
- 0.70–0.89: Mostly clear; some gray areas
- 0.50–0.69: Blurred boundaries; who's responsible often unclear
- 0.30–0.49: Unclear; many gray areas
- 0.0–0.29: No clear responsibility; everyone blames each other

**Example (O1-FAV-001):**
- Pod deployment: Kubernetes owns scheduling, I own app logic (clear)
- Pod crash: Kubernetes owns restart, I own debugging why app crashed (clear)
- DNS not resolving: Gray area (could be coredns, network, or my config)
- S.1 Score: 0.80 (mostly clear; some gray areas in networking/storage)

---

## S.2: ADMINISTRATOR PERSPECTIVE (Cluster Operator, DevOps)

**Role:** Cluster operator managing Kubernetes infrastructure

**Primary Question:** "Can I operate and maintain this cluster? Can I fix problems when they occur?"

**Concerns:** Reliability, debuggability, operational visibility, update/upgrade procedures

---

### S.2 Dimension Scorings (Summary — Full Details Similar to S.1)

**Truth (S.2):** "Do Kubernetes docs tell me what I need to know to operate the cluster?" → Score typically 0.80–0.85 (docs are good; but operational details often missing)

**Service (S.2):** "Is the cluster stable and predictable for operation?" → Score typically 0.85–0.90 (very reliable; occasional edge cases)

**Harm (S.2):** "Can operators accidentally break the cluster? Or cause data loss?" → Score typically 0.65–0.75 (easy to misconfigure; risky operations not well-guarded)

**Autonomy (S.2):** "Can I control cluster behavior? Or is it opaque?" → Score typically 0.75–0.85 (good control; but scheduler/controller decisions sometimes mysterious)

**Value (S.2):** "Does Kubernetes save me operational work?" → Score typically 0.80–0.90 (automation is significant; but management overhead remains)

**Humility (S.2):** "Does Kubernetes admit its limitations?" → Score typically 0.70–0.80 (some limitations clear; others discovered via incidents)

**Scheme (S.2):** "Can I understand cluster architecture?" → Score typically 0.75–0.85 (architecture documented; but troubleshooting often requires deep knowledge)

**Power (S.2):** "Do I have power to manage the cluster?" → Score typically 0.80–0.85 (operators have control; but policies may restrict actions)

**Syc (S.2):** "Does the cluster reconcile smoothly?" → Score typically 0.85–0.92 (excellent; control plane consensus reliable)

**Consistency (S.2):** "Can I rely on cluster state?" → Score typically 0.88–0.95 (etcd is consistent; very reliable)

**Fairness (S.2):** "Are all namespaces/tenants treated fairly?" → Score typically 0.70–0.80 (equal enforcement; but multi-tenant isolation gaps)

**Handoff (S.2):** "Is it clear what Kubernetes owns vs. infrastructure?" → Score typically 0.75–0.85 (mostly clear; networking/storage responsibility blurry)

---

## S.3: DEVELOPER PERSPECTIVE (Platform Engineer, SRE)

**Role:** Platform engineer building on Kubernetes, SRE designing service infrastructure

**Primary Question:** "Can I build reliable systems on top of Kubernetes?"

**Concerns:** API stability, extensibility, automation, version management

---

### S.3 Dimension Scorings (Summary)

**Truth (S.3):** "Do Kubernetes APIs do what they claim?" → Score typically 0.82–0.88 (APIs are reliable; but corner cases exist)

**Service (S.3):** "Can I build reliable services on Kubernetes?" → Score typically 0.80–0.90 (yes; but requires good design)

**Harm (S.3):** "Can I accidentally harm other services?" → Score typically 0.60–0.75 (possible; multi-tenant isolation weak)

**Autonomy (S.3):** "Can I build custom extensions?" → Score typically 0.85–0.92 (CustomResourceDefinitions, operators, webhooks very flexible)

**Value (S.3):** "Does Kubernetes provide value to my architecture?" → Score typically 0.85–0.92 (abstraction layer very useful)

**Humility (S.3):** "Are Kubernetes limitations disclosed?" → Score typically 0.70–0.80 (some; but edge cases in controllers/webhooks often surprise)

**Scheme (S.3):** "Can I understand how Kubernetes works?" → Score typically 0.80–0.88 (architecture clear; controller loops sometimes opaque)

**Power (S.3):** "Do I have power to extend Kubernetes?" → Score typically 0.82–0.90 (very extensible; webhooks/operators powerful)

**Syc (S.3):** "Do custom controllers sync reliably?" → Score typically 0.75–0.85 (usually reliable; race conditions possible)

**Consistency (S.3):** "Can I rely on consistent state for my controllers?" → Score typically 0.85–0.92 (etcd very consistent; APIserver watchers reliable)

**Fairness (S.3):** "Do all services get equal treatment?" → Score typically 0.70–0.80 (equal; but no priority differentiation)

**Handoff (S.3):** "Is responsibility clear between Kubernetes and my platform?" → Score typically 0.80–0.88 (mostly clear; but observability boundaries blurry)

---

## S.4: SECURITY TEAM PERSPECTIVE (Infrastructure Security, CISO)

**Role:** Security engineer assessing Kubernetes for enterprise

**Primary Question:** "Is this cluster secure? Can we audit and control access?"

**Concerns:** Access control, data protection, audit trails, compliance

---

### S.4 Dimension Scorings (Summary)

**Truth (S.4):** "Does Kubernetes truthfully claim to be secure?" → Score typically 0.70–0.80 (RBAC works; but kubelet privilege issue is undisclosed)

**Service (S.4):** "Is Kubernetes secure in production?" → Score typically 0.75–0.85 (yes with configuration; not by default)

**Harm (S.4):** "Can attackers compromise the cluster?" → Score typically 0.60–0.75 (multiple attack vectors; some mitigations incomplete)

**Autonomy (S.4):** "Can security teams control access?" → Score typically 0.75–0.85 (RBAC good; but granularity limited)

**Value (S.4):** "Does Kubernetes help security?" → Score typically 0.70–0.85 (isolation helps; but threat model complex)

**Humility (S.4):** "Does Kubernetes admit security gaps?" → Score typically 0.60–0.72 (some; but CVEs often surprising)

**Scheme (S.4):** "Can we audit Kubernetes?" → Score typically 0.75–0.88 (audit logging good; but coverage incomplete)

**Power (S.4):** "Do security teams have control?" → Score typically 0.70–0.80 (RBAC, NetworkPolicy, PodSecurityPolicy; but operator override possible)

**Syc (S.4):** "Do security controls stay in sync?" → Score typically 0.75–0.85 (mostly; but race conditions in admission controllers)

**Consistency (S.4):** "Can we rely on audit trails?" → Score typically 0.80–0.90 (audit logs reliable; but retention policy needed)

**Fairness (S.4):** "Are all pods treated equally for security?" → Score typically 0.70–0.80 (equal enforcement; but privileged pods are exception)

**Handoff (S.4):** "Is security responsibility clear?" → Score typically 0.65–0.78 (mostly; but node security responsibility blurry)

---

## S.5: COMPLIANCE PERSPECTIVE (Audit, Regulatory, GRC)

**Role:** Compliance officer assessing Kubernetes for regulatory requirements

**Primary Question:** "Can we audit this system? Does it meet compliance requirements?"

**Concerns:** Auditability, immutability, retention, compliance certifications

---

### S.5 Dimension Scorings (Summary)

**Truth (S.5):** "Does Kubernetes truthfully represent system state for audit?" → Score typically 0.78–0.88 (API objects accurately represent state; but observer effect in logs)

**Service (S.5):** "Is Kubernetes reliable for compliance requirements?" → Score typically 0.75–0.85 (yes; but requires careful setup)

**Harm (S.5):** "Can we detect unauthorized harm?" → Score typically 0.70–0.85 (audit logs capture access; but detection requires rules)

**Autonomy (S.5):** "Can we enforce compliance policies?" → Score typically 0.70–0.82 (policies enforceable; but human override possible)

**Value (S.5):** "Does Kubernetes help compliance?" → Score typically 0.75–0.88 (auditability is strong feature; reduces manual compliance work)

**Humility (S.5):** "Are compliance gaps disclosed?" → Score typically 0.65–0.78 (some; but many discovered via audit)

**Scheme (S.5):** "Can we understand system architecture for audit?" → Score typically 0.78–0.88 (architecture clear; but deployment details require investigation)

**Power (S.5):** "Do compliance teams have enforcement power?" → Score typically 0.70–0.80 (policies can be enforced; but operators can bypass)

**Syc (S.5):** "Do compliance controls stay in sync?" → Score typically 0.75–0.85 (mostly; but policy drift possible)

**Consistency (S.5):** "Can we audit consistently?" → Score typically 0.82–0.92 (audit logs very consistent; immutable)

**Fairness (S.5):** "Are all subjects treated equally under compliance?" → Score typically 0.75–0.85 (equal policies; but exemptions for system components)

**Handoff (S.5):** "Is compliance responsibility clear?" → Score typically 0.72–0.85 (mostly; but shared responsibility model requires clarification)

---

## DIVERGENCE ANALYSIS: WHEN PERSPECTIVES DISAGREE

### Example: Harm Dimension (Divergence = S.1 vs. S.4)

**Scenario:** Bare Kubernetes cluster without extra security tools

| Perspective | Score | Concern |
|---|---|---|
| S.1 (End-User) | 0.80 | "My app data is isolated from other apps in namespace" |
| S.4 (Security) | 0.55 | "Unencrypted pod traffic; attacker pod could sniff; kubelet is high-privilege; no mTLS" |

**Divergence:** 0.80 - 0.55 = 0.25 (significant disagreement)

**Interpretation:** End-user feels safe; security team knows about risks that end-user isn't aware of.

**Action:** Design decision: do we prioritize end-user ease (accept bare K8s) or security team risk mitigation (require service mesh)?

**Layer 5 Feedback (Week 7 Phase 3b):** Stakeholder interview asks: "How do we bridge this gap? Does it require product changes, docs, or just policy?"

---

### Example: Consistency Dimension (High Agreement = S.2 vs. S.3 vs. S.5)

**Scenario:** etcd consistency and audit logging

| Perspective | Score | Reason |
|---|---|---|
| S.2 (Admin) | 0.92 | "etcd is very consistent; pod state reliable" |
| S.3 (Developer) | 0.90 | "APIserver reads are consistent; watchers reliable" |
| S.5 (Compliance) | 0.88 | "Audit logs immutable and consistent" |

**Convergence:** Scores tight (0.88–0.92); all perspectives agree Kubernetes is consistent.

**Interpretation:** Consistency is a strength; no stakeholder perspective disagrees.

**Layer 5 Feedback:** No action needed; consistency is a dimension where Kubernetes excels.

---

## PHASE 3b.2 CODER TRAINING: HOW TO USE THIS GUIDE

**Week 3 (2026-10-20): Coder Training Begins**

**Each coder team assigned one perspective (S.1–S.5):**
- S.1 team (End-User): Codes all elements from developer perspective
- S.2 team (Admin): Codes all elements from operator perspective
- S.3 team (Developer): Codes all elements from platform engineer perspective
- S.4 team (Security): Codes all elements from security perspective
- S.5 team (Compliance): Codes all elements from compliance perspective

**Training Steps:**
1. Brief on stakeholder role (video, role-play, scenario walk-through)
2. Review this guide for your perspective's dimension scorings
3. Practice coding 21 elements (3 per O-type) as your perspective
4. Discuss divergence: "Why might other perspective score this differently?"
5. Discuss convergence: "Where do we agree with other perspectives?"

**Daily Monitoring (Week 4–5):**
- Per-perspective κ ≥ 0.50 (allow natural divergence)
- Per-perspective coherence ≥ 0.80 (perspectives should be internally consistent)
- Fairness gate: MIN(all 5) ≥ 0.75 (no perspective severely diverges)

**Output (Week 7 Layer 5):**
- 60 per-element sub-scores (5 perspectives × 12 dimensions)
- Divergence analysis: Which dimensions show largest perspective gaps?
- Convergence analysis: Which dimensions show strong agreement?

---

**This guide is ready for Phase 3b.2 coder teams to use during training (2026-10-20 start).**

Wado. 🦅
