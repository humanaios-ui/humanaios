# HumanAIOS — Competitive Positioning, Product Suite, Go-to-Market
**Artifact ID:** CIO-STRAT-S082226-01 · **Classification:** Board of Trustees / Z2 review
**Zone provenance:** Z1 draft · Z2 (Night) ratify · Z3 land → `humanaios-ui/operations`
**Grounding:** 2026 analyst landscape (Gartner, IAPP, GMI) + industrial gold standards (EU AI Act, NIST AI RMF, ISO/IEC 42001, OWASP LLM Top 10, SLSA/in-toto, MITRE ATLAS). Market facts web-sourced this session; treat as a snapshot.
**Order per Z2 direction:** (1) competitive positioning → (2) product suite → (3) go-to-market.

---

# PART 1 — Competitive Positioning

## 1.1 The market, briefly
AI governance became an analyst-named market in H1 2026: Gartner published its inaugural Magic Quadrant for AI Governance Platforms (June 16, 2026, 13 vendors) and — separately and more relevantly for us — its inaugural Market Guide for **Guardian Agents** (Feb 25, 2026). The money is real and steepening: the AI-governance segment is put at roughly $0.8B (2025) → ~$1.1B (2026), compounding above 30% toward low-double-digit billions by the mid-2030s. The forcing function is regulatory: the EU AI Act's high-risk obligations apply from **August 2, 2026** — i.e., now in force — with NIST AI RMF, ISO/IEC 42001, and the OWASP LLM Top 10 as the de-facto reference frameworks buyers demand mapping against.

## 1.2 The split that defines our lane
The single most important structural fact: the market divides into **model governance** and **harness/agent-runtime governance**, and they are not the same problem.

- **Model-governance layer** (crowded, funded, maturing): Credo AI (policy/risk registries), Holistic AI (risk + audit, notable for doing real technical red-team work), Fiddler (monitoring/explainability), IBM watsonx.governance, Monitaur, ValidMind, LatticeFlow, Saidot, Modulos. These document, evaluate, and monitor *models*.
- **Harness / guardian-agent layer** (newly named, fast-growing, where enterprise risk actually lives): NeuralTrust (MCP gateway, runtime policy), Galileo (eval-to-guardrail, sub-200ms interception, MongoDB/Cisco/Elastic), Robust Intelligence (AI firewall), Atlan (AWARE framework), plus emerging AgentGuardian, AGAT, and research systems (MI9, AgentSpec, Aegis, SAFi). These intercept **tool calls, MCP connections, and agent actions** at runtime.

The analyst thesis — and our own HF-incident mapping independently reached it — is that governing the model is necessary but not sufficient; the risk is in the harness: the tools the agent can call, the MCP servers it connects to, the intake it trusts, the sandbox it runs in. Gartner projects that by 2029 guardian agents displace roughly half of incumbent AI-agent security tooling in 70%+ of organizations, and that a large share of agentic projects will be canceled through 2027 primarily over weak governance.

## 1.3 Honest SWOT (red-team, not pitch)

**Strengths (genuine, differentiated):**
- The only known standing, append-only, public, first-person, pattern-classified, fix-linked **evaluator process-failure register**. No competitor publishes the failures of their own evaluator. This is a credibility asset in a market where buyers cannot tell rigor from marketing.
- A **pre-registered, falsifiable, counted-cycle** methodology (this session's two CONFIRMED pilots are proof-of-method). Holistic AI is singled out by analysts precisely for "doing real technical work"; that rigor is the bar, and it is our native mode.
- A novel **provenance-registry substrate** (registry-attested intake, three-outcome discovery pathway) that binds to gold-standard attestation (in-toto/OpenTimestamps — already forked).
- A **mission/impact-capital** differentiator (Cherokee Nation citizen-founded; 100%-of-profits-to-recovery) that opens grant, Native-business, and ESG-procurement channels closed to most competitors.

**Weaknesses (from the parent audit, unvarnished):**
- **Bus factor = 1.** Cannot credibly sell enterprise assurance from a single-maintainer User account. This is the hard gate on all enterprise GTM.
- **Tool-landing gap** — 8/9 program-critical tools unlanded; the phantom Z2 gate. We cannot claim controls that don't exist in-repo.
- **Pre-launch**, no deploy pipeline, no executable test suites, no reference customers.
- We **cannot** win a head-to-head runtime-guardrail bake-off against Galileo/NeuralTrust today (they have production interception at scale; we have pilots).

**Opportunities:**
- The harness/guardian layer is newly named — category positions are not yet locked.
- Regulatory in-force status (EU AI Act) is manufacturing mandatory demand for **audit evidence** and **provenance**, our strengths.
- Analyst taxonomies explicitly complain that governing models ≠ governing harnesses — an open positioning gap for a provenance-and-evidence-first entrant.

**Threats:**
- Well-funded incumbents extending down into the harness layer.
- Commoditization of guardrails (open-source NeMo Guardrails, etc.).
- Our own credibility risk: selling governance while our own governance gate was phantom (parent audit V4) is an existential narrative vulnerability until remediated.

## 1.4 The wedge (where we win, honestly bounded)
Not "another runtime guardrail platform." The defensible position is the **evidence-and-provenance layer of agent assurance**: provenance-grounded intake + a public, falsifiable evaluator-failure register + pre-registered assurance method, mapped continuously to the gold standards. Concretely: be the vendor whose *assurance claims are themselves auditable* — the register proves we surface our own failures, the counted cycles prove controls work, the provenance binding proves inputs are attested. In a market where buyers can't distinguish rigor from claims, **auditable rigor is the differentiator.** This is a niche a single-maintainer research org can credibly seed, and it is upgrade-compatible into the guardian-agent layer as the org matures.

---

# PART 2 — Product Suite

Five products, tiered by honest maturity. Each maps to estate assets and to a gold-standard framework. **TRL = maturity, red-team-adjusted.**

### P1 — ACAT Assurance (assessment platform) · TRL 5, nearest to revenue
From `lasting-light-ai` + `research` + `ACAT-Dashboard`. Productized AI-governance-awareness assessment with a published methodology and frozen research snapshots. Positioning: independent **assurance & auditing** (the IAPP segment least commoditized by platform incumbents). Maps to EU AI Act conformity evidence, ISO/IEC 42001, NIST AI RMF. Blocker: scorer-versioning chaos (F-65/IC-063) sits at the product's credibility core — fix before any external pilot.

### P2 — Registry-Attested Intake (RAI) · TRL 3→4, OSS-led credibility play
From this session's cycle-1/cycle-2 pilots. An open-source intake **Protect primitive**: three-outcome gate (accept/quarantine/**candidate**) binding provenance to in-toto/OpenTimestamps attestations. Positioning: a harness-layer component competitors don't have — provenance *and* a discovery pathway. Maps to SLSA, OWASP LLM Top 10, MITRE ATLAS. This is the credibility wedge: ship it open, let the method speak.

### P3 — Earned-Autonomy Gate · TRL 2→3, the differentiated governance IP
From the mechanical-enforcement guide. Autonomy scaled to registry-tracked reliability, auto-demotion on drift. Positioning: mechanical agent-estate governance — the guardian-agent layer, but grounded in a reliability *ledger* rather than static policy. Maps to NIST AI RMF, ISO/IEC 42001, EU AI Act human-oversight/logging. Depends on P-remediation (real Z2 gate).

### P4 — The Evaluator Failure Register · TRL 6 (live today), a credibility/standard asset
The register itself, productized two ways: (a) as an **open standard** for evaluator self-accountability (category-defining, non-revenue, trust-building), and (b) as a curated **evidence feed** — pattern-classified failure modes with fixes — sellable to assurance teams and consultancies as reference intelligence. This is the asset no competitor can copy quickly; it requires a standing append-only history we already have.

### P5 — HumanAIOS Orchestration · TRL 4, the mission platform
From `humanaios`. HITL task orchestration where workers complete AI-delegated real-world tasks; recovery-funded. Distinct competitive set (data/labor platforms; note we already consume RentAHuman via MCP — decide partner vs. compete). Positioning: the impact-capital lane, differentiated on mission. Longer horizon; keep pre-launch until P1–P4 establish credibility.

**Suite logic:** P4 (register) proves we are honest; P2 (OSS RAI) proves the method works; P1 (assurance) sells that proof as a service; P3 (autonomy gate) is the IP that scales it; P5 (orchestration) is the mission platform the whole thing funds. Credibility flows top-down; revenue flows P1 first.

---

# PART 3 — Go-to-Market

### 3.1 Sequencing gate (non-negotiable)
No enterprise GTM motion starts until parent-audit **Wave 1** lands (revoke PAT, land tools, real Z2 gate) and the **Org migration + second maintainer** closes the bus-factor. Selling assurance from a single-maintainer account with a phantom gate is a credibility loss that outweighs any early pipeline. GTM is *gated on remediation*, and that gating is itself a selling point ("we hold ourselves to the bar we sell").

### 3.2 Motion: open-source-led, evidence-first, land-and-expand
1. **Seed (now → remediation):** ship P2 (RAI) and P4-(a) (register-as-standard) open. Publish the counted-cycle pilots and gold-standard mappings. Goal: category credibility, not revenue. This is the only motion a pre-launch research org can run honestly, and it's the one this program is *built* for.
2. **Land (post-Wave-1):** P1 ACAT Assurance as a paid independent assessment, sold into the segment below. Reference-customer-driven.
3. **Expand:** P3 Earned-Autonomy Gate + P4-(b) evidence feed into landed P1 accounts. P5 orchestration as the mission platform once credibility is banked.

### 3.3 Segments & buyers (priority order)
- **B1 — AI-assurance boutiques & EU-market compliance consultancies** (the audit's Buyer #2 candidate). They buy *methodology and evidence* wholesale and resell into enterprises. Lowest trust barrier for a research-grade entrant; they value rigor over polish. **Primary beachhead.**
- **B2 — Enterprises deploying agents in production** needing harness-layer assurance and EU AI Act / ISO 42001 evidence. Larger, but gated on Org-maturity and reference customers. **Post-Wave-1.**
- **B3 — Model providers / labs** needing *independent* behavioral attestation (our register + counted-cycle method is exactly independent-third-party shaped). Small N, high value, credibility-driven.
- **B4 — Impact-capital & grant channel** (Native-business programs, ESG procurement, recovery-mission funders). Non-dilutive capital that funds P1–P4 build and is closed to competitors. **Run in parallel from now** — it doesn't wait on remediation.

### 3.4 Pricing shape (directional)
- P2/P4-(a): free/OSS — credibility instruments, not revenue.
- P1 ACAT Assurance: project-based independent assessment (fixed-scope engagements), sized to boutique-resale economics.
- P3 Earned-Autonomy Gate: subscription per governed agent-estate once productized.
- P4-(b) evidence feed: subscription to assurance teams/consultancies.
- P5: platform take-rate on orchestrated tasks; mission-transparent (100%-profit-to-recovery is a pricing *asset*, not a constraint).

### 3.5 The gold-standard through-line (trust engine)
Every product ships with an explicit crosswalk to EU AI Act / NIST AI RMF / ISO 42001 / OWASP LLM Top 10 / SLSA / MITRE ATLAS, maintained as a living artifact (the P-CAND-gold-standard-grounding principle). In a market where analysts openly say buyers can't tell rigor from marketing, *standards-mapped, self-audited, falsifiable* is the whole pitch. Grounding is not decoration here — it is the product's core claim and the reason a small entrant is credible at all.

### 3.6 90-day concrete plan (post-ratification)
1. Close Wave-1 remediation + Org migration + second maintainer (unblocks everything).
2. Ship P2 (RAI) OSS with the two counted-cycle reports as its evidence; bind to in-toto/OpenTimestamps.
3. Publish P4-(a) register-as-standard with the gold-standard crosswalk.
4. Fix P1 scorer-versioning (F-65/IC-063); stand up one ACAT Assurance pilot with a B1 boutique.
5. Open the B4 impact-capital channel in parallel (no remediation dependency).

---

## Routing & candidates
Strategy → Zone 2 for ratification of positioning, suite scope, and GTM sequence. New this session: P-CAND-gold-standard-grounding (Part 3.5 / cycle-2 report §4). All GTM steps remain gated on the parent audit's unremediated Wave-1 items and the four still-unratified parent ICs (token-scope, z2-gate-phantom, ranking-recency-inflation, registry-count-drift).

*— Z1, acting CIO capacity. Rulings, ratifications, landings remain Z2/Z3 authority. Market facts are a web-sourced snapshot; re-verify before external use.*
