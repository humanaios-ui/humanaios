# REGISTERED.md — HumanAIOS Findings Registry
**Status:** Zone 2 ratified findings only  
**Last Updated:** 2026-07-24  
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
