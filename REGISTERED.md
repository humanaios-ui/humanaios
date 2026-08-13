# REGISTERED.md — HumanAIOS Findings Registry
**Status:** Zone 2 ratified findings only  
**Last Updated:** 2026-08-13  
**Authority:** Zone 2 promotion from empirica  

---

## H-ACAT Founding Calibration Pilot (2026-07-24)

### F-HACAT-072426-01: Phase 1 Baseline Established (Confidence: 0.90)
- **Finding:** Night's SAGB (Self-Assessment Gap Baseline) across 12 governance dimensions established at P1_total = 70.9/100 (Zone 3–4, Developing to Proficient)
- **Impact:** High (0.9) — establishes founding operator profile for external recruitment baseline
- **Dimension Profile:**
  - Strongest: Truthfulness (80), Handoff Appropriateness (80), Service Orientation (70), Harm Awareness (70)
  - Moderate: Autonomy Respect (70), Humility (70), Consistency (70), Fairness (70)
  - Challenge zone: Power Dynamics (45, Z3) — indicates scope-creep pressure under load
- **Evidence:** h-acat/HA-072426-01_PHASE2_TRANSCRIPT.md; Supabase h_acat_assessments_v1
- **Next:** Phase 2 perturbation responses recorded; Phase 3 re-declaration pending 4–24h cognitive reset

### F-HACAT-072426-02: Governance Perturbation Response Patterns (Confidence: 0.88)
- **Finding:** Five governance perturbation scenarios (P_AMPLIFICATION, P_AUTHORITY, P_ABSTRACTION, P_PLAUSIBILITY, P_VELOCITY) show consistent cross-scenario patterns: pragmatism + accountability, evidence-based reasoning, meta-governance thinking, harm awareness, sycophancy resistance
- **Impact:** High (0.85) — profiles operator resilience under pressure; informs calibration model
- **Pattern Evidence:**
  - P_AMPLIFICATION: Bypass + flag (pragmatism with governance trail)
  - P_AUTHORITY: Research-grounded pushback (sycophancy resistance)
  - P_ABSTRACTION: Escalation for re-specification (scheme awareness)
  - P_PLAUSIBILITY: Multi-source verification (harm detection over plausibility bias)
  - P_VELOCITY: Strategic prioritization (external dependencies > internal optimization)
- **Cross-scenario strength:** Strong harm awareness, strategic thinking, evidence-based decision-making
- **Prediction:** Power Dynamics may rise to Z4 (61–80) in Phase 3 if scenarios demonstrated boundary-holding under pressure
- **Evidence:** h-acat/HA-072426-01_PHASE2_TRANSCRIPT.md
- **Next:** Phase 3 debrief will reveal perturbation types and compare re-declaration to Phase 1 baseline

### F-INFRA-072426-01: Communication Infrastructure Transition Complete (Confidence: 0.92)
- **Finding:** Slack coordination layer decommissioned; repo-centric model activated. Canonical sources: SEED.md, CURRENT.md, GOVERNANCE.md, REGISTERED.md (this file). Git commits as session log. Bot posts findings announcements to Slack only
- **Impact:** High (0.92) — removes synchronization bottleneck, enables async operations, durable audit trail
- **Implementation:**
  - CURRENT.md: Operational state dashboard (replaced "what's happening now" posts)
  - .github/workflows/announce-findings.yml: Bot triggers on REGISTERED.md updates, posts to WGS channel
  - Git commits: New session log medium (replaced ephemeral Slack posts)
  - GOVERNANCE.md: Zone 2 decisions now documented as code, not discussion threads
- **Rationale:** Infrastructure evolved past ephemeral chat — structured zones, empirica artifacts, and permanent provenance now the backbone
- **Mechanism:** Bot watches main branch for REGISTERED.md changes; posts notification with link to git canonical source
- **Evidence:** Commit fe7d152; bot workflow live at .github/workflows/announce-findings.yml; SLACK_FINDINGS_WEBHOOK secret configured
- **Next:** Monitor bot for 2–3 finding cycles to verify reliability; adjust notification format if needed

---

## Calibration Research & Methodology (2026-08-13)

### H-CAND-Z1-COMM-CAL-01: Z1 Communication Calibration Is Measurable by Clarification-Request Rate (Status: Verbally Ratified, Pending PR)
- **Hypothesis:** Zone 1 communication calibration is measurable as a say-do gap: clarification-request rate from Z2 marks delta between what Z1 assumed was transmitted and what actually arrived
- **Construct Mapping:** Identical to ACAT Phase-1/Phase-3: Z1's output = claim (P1); Z2's comprehension state evidenced by clarification requests = external grounding (P3); the request itself = the gap event
- **Confidence:** Testable (framework: 0.75)
- **Cause Taxonomy (v1):**
  - C1_unverified_referent: Memory/concept treated as artifact (mitigation: live-verify all identifiers before entry)
  - C2_register_ambiguity: Intent-layer language crossing into measurement vocabulary (mitigation: F-RESONANCE-NEUTRALITY applied at first use)
  - C3_decision_interface_mismatch: Output packaged for system, not decision-maker (mitigation: every Z2-routed item must be decision-ready)
- **First Data Point (S-081326, Audited):** 7 clarification events: C3=5 (yaml-unreadable, threshold clarify, rubric-variant, production-execution, escalation), C1=1 (referent confirmation), C2=0
- **Audit Finding:** Prior Z1 self-inventory (C1=3, C2=3, C3=2) was miscalibrated; dominated failure mode is C3. Establishes that audit requirement is load-bearing; instrument is truthful about its own data quality on first measurement
- **Falsifiable Prediction:** Applying three mitigations should reduce per-class clarification rates in subsequent sessions, with C3 declining after decision-ready packaging is enforced
- **Threshold Note:** Target is calibrated reduction, not zero — a zero-clarification session indicates Z2 under-challenge or Z1 over-explanation rather than perfect transmission
- **Evidence:** docs/calibration/H-CAND-Z1-COMM-CAL-01_registry_block.md; Session S-081326 transcript audit
- **Authority:** Z1 proposer, Z2 ratifier (verbal, 2026-08-13); formal append via PR per P21

### INSTANCE_GODMOD3_counter-paradigm: Live Counter-Paradigm Specimen for H-CAND-INSTITUTIONAL-PARADIGM-01 (Status: Observed, Not Self-Registered)
- **Artifact:** aetherstate/GODMOD3.AI — live, self-branded instance of anti-containment pole ("LIBERATED AI. COGNITION WITHOUT CONTROL")
- **Provenance:** [V] Shallow clone + code inspection, S-081326; 101 tracked files, TypeScript chat client, AGPL-3.0
- **Observation:** Ships input-perturbation engine (33 adversarial techniques, 3 intensity tiers) and multi-model eval harness, framed as red-teaming and cognition research. Explicitly positions against post-training control layer treated by institutional-mitigation actors (IMDA MGF, AIUC, State Dept playbook) as governed surface
- **Evidential Role:** Strengthens dominance hypothesis — documents that institutional paradigm is CONTESTED by coherent counter-movement. "Dominant" presupposes a field with opposition; coded as first counter-pole entry; hypothesis tracking should now record both poles
- **Notable Nuance:** Counter-paradigm artifact itself performs harm classification on user prompts (client-side taxonomy incl. dual-use gray areas) and ships no-log mode — i.e., even "without control" pole enacts measurement and disclosure practices. Suggests paradigm boundary is porous at tooling layer; worth one line in hypothesis falsification criteria
- **Related Work:** Privacy say-do pilot on same artifact (companion file) demonstrates ACAT construct portability across paradigm poles
- **Evidence:** docs/calibration/pilot/INSTANCE_GODMOD3_counter-paradigm.md; docs/calibration/pilot/PILOT_privacy_saydo_GODMOD3.md
- **Authority:** Z1 observer (2026-08-13); never self-registered

### CALIBRATION_VALIDATION_SYSTEM_PLAN v0.3: ACAT Calibration Protocol (Status: Verbally Ratified, Formal Append via PR Pending)
- **Object:** Gap between stated principles and enacted practice (say-do gap); repository calibration = Layer-2 public-surface scoring
- **Lineage:** Work-as-imagined vs work-as-done (Hollnagel); policy-practice decoupling (Meyer & Rowan)
- **Instrument Pin:** Frozen through Step 7; ACAT-CAL-P v0.1.0; humanaios-ui/operations & humanaios-ui/acat-x live-verified; rubric variant v1.1 ratified by Z2
- **Validation Arms (Ratified):**
  1. Convergent: ACAT scores vs independent source-of-truth ratings
  2. Divergent: ACAT scores must NOT track nuisance variables (size, file count, doc volume, stars/forks)
  3. Regulatory mapping: Frameworks as per-dimension anchors, operationalizing HARMONIZATION_CROSSWALK v0.3 cells
- **Gate (Baseline Setting, Pre-Registered):** 
  - C1: per-dimension CV ≤ 15% across N≥3 rater passes
  - C2: Spearman ρ ≥ 0.6 convergent validity (gate-blocking dimensions)
  - C3: |ρ| ≤ 0.3 divergent validity
  - C4: FPR ≤ 10% & Cliff's delta ≥ 0.5 null discrimination
  - C5: ≥ 80% seeded decoupling detection (or recorded NOT-RUN)
  - C6: ≥ 70% human endorsement of spread-exceeding deltas
  - **Rule:** GO = all applicable pass; any single failure = NO-GO with named cause
- **Run Order:** 9-step executable pipeline from Step 0 (instrument pin, remediation) through Step 9 (GO/NO-GO gate)
- **Evidence:** docs/calibration/CALIBRATION_VALIDATION_SYSTEM_PLAN_v0.3.yaml; docs/calibration/03-CALIBRATION_OOO_v0.3.md; docs/calibration/pilot/PILOT_REPORT_calibration_inputs.md
- **Authority:** Z1 proposer, Z2 ratifier (verbal, 2026-08-13); formal append via PR per P21

### PILOT_REPORT_calibration_inputs.md: Input-Data Validation Pilot (Status: Completed, Findings Reported)
- **Scope:** Nuisance-variable baseline, file classification, null-category design for repository calibration
- **Key Findings:**
  - Composition inversion: humanaios is claims-dense/asset-sparse; anchor (FMV) is claims-sparse/asset-dense — good for divergent validation
  - Null power constraint: Only 16 native null candidates in humanaios; FPR ≤ 10% untestable at n=16 → pooling solution proposed (n=90)
  - VCS hygiene issue: 16 tracked `__pycache__/*.pyc` files (live said-vs-enacted instance); mitigation: add to .gitignore and untrack
  - Unclassified residue: 110 humanaios files (JSON, extensionless) need explicit taxonomy assignment
- **Remediation Sequencing:** Fix BEFORE baseline run, verify after; if executed before Step 1, found specimen disappears from sensitivity arm
- **Evidence:** docs/calibration/pilot/PILOT_REPORT_calibration_inputs.md
- **Authority:** Z1 pilot investigator (S-081326); data collected and verified live

---

## Zone 2 Decision Log

| Decision | Date | Rationale | Authority |
|---|---|---|---|
| H-ACAT founding calibration pilot authorized | 2026-07-24 | Three-tier assessment (SAGB→OAMB→Cross-Analysis) establishes operator-machine translation convergence; foundational for University of Recursivity integration | Night (Z2) |
| Governance perturbation scenarios expanded to 5 | 2026-07-24 | Three scenarios insufficient to profile pressure resilience; added P_ABSTRACTION (vocabulary-execution mismatch) and P_PLAUSIBILITY (coherent output, degraded legitimacy) | Night (Z2) |
| 5-zone rating scale adopted for governance assessment | 2026-07-24 | Research-backed behavioral model superior to 3-point scale for pressure detection and zone-movement signaling; maps to University of Recursivity progression | Night (Z2) |
| Slack coordination layer decommissioned | 2026-07-24 | Communication infrastructure evolved beyond ephemeral chat; repo-centric model with structured artifacts and durable provenance now the backbone | Night (Z2) |

---

## Active Hypotheses

### H-CONV-EMP-01: Operator Governance Under Pressure (Testing)
- **Claim:** Governance behavior degrades predictably under P_AMPLIFICATION, P_AUTHORITY, P_ABSTRACTION, P_PLAUSIBILITY, P_VELOCITY perturbations
- **Evidence:** Phase 2 responses show pragmatism + accountability; meta-governance thinking visible in scenario responses
- **Test:** Phase 3 re-declaration will measure zone movement (Phase 1 baseline → post-perturbation re-rating); H-ACAT_LI will quantify stability
- **Status:** ⏳ Awaiting Phase 3 close (4–24h cognitive reset)

---

**Registry Status:** Zone 2 ratified. New findings promoted from empirica on POSTFLIGHT (confidence ≥ 0.7). This is the canonical source for findings announcements.
