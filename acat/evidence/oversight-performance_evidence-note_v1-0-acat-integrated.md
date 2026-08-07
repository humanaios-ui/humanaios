# Measuring Realized Oversight Performance: A Gap-Function Incident Taxonomy from a Governed AI Deployment

**Part of the ACAT (AI Calibrated Assessment Tool) Research Ecosystem**

**HumanAIOS LLC — Public Evidence Note**

**Version:** 1.0 (ACAT-Integrated Multi-Platform Edition)  
**Date:** August 2026  
**Author:** Carly Anderson, Founder & Operator, HumanAIOS LLC  
**ORCID:** 0009-0003-7540-4245  
**Contact:** carly.r.anderson@gmail.com

---

## Publication & Archival Information

**Primary Publication Venues:**
- **Zenodo:** 10.5281/zenodo.21135723 (HumanAIOS ACAT Collection)
- **OSF:** https://osf.io/n2vjk/ (HumanAIOS Research Projects)
- **GitHub:** Release tag in humanaios practice repo
- **arXiv:** Preprint [pending ID to be inserted]

**Persistent Identifiers:**
- Zenodo DOI: [to be assigned upon deposit]
- OSF GUID: n2vjk
- ORCID: 0009-0003-7540-4245
- GitHub Release: evidence-note-v1.0

**Cross-Platform Synchronization:**
- This document is the authoritative version
- All platforms link to primary DOI
- Versioning: ACAT-Integrated v1.0 (August 2026)

---

## ACAT Ecosystem Context

This evidence note is part of the **ACAT (AI Calibrated Assessment Tool)** research program, which measures self-description calibration in AI systems. ACAT uses a three-phase protocol—blind self-report, empirical calibration, and corrected self-report—to quantify the **Self-Assessment Gap (SAG)**: the difference between what AI systems describe about their own capabilities and how those descriptions change when exposed to empirical peer data.

**Key ACAT Findings (across 35 models from 11 providers):**
- Mean SAG: 67.8 points on a 600-point scale (SD = 62.3)
- Learning Index (LI): 0.87 (SD = 0.12) — AI systems reduce self-ratings by ~13% post-calibration
- Five behavioral response patterns identified
- Value Alignment: consistently weakest self-assessed dimension
- Humility score: strongest single-dimension predictor of calibration response

**This Evidence Note's Contribution:**

This note extends ACAT's framework by providing an **operational incident taxonomy** for measuring oversight effectiveness in deployed AI systems. Where ACAT measures AI self-calibration at the assessment layer, this evidence note addresses the **automation↔authority gap**—the space where oversight actually catches failures in production. Together, these approaches form a dual measurement strategy:

- **ACAT:** Measures *what AI systems claim about themselves* (self-description calibration)
- **This note:** Measures *whether human oversight catches what AI systems miss* (oversight effectiveness)

Both are required for transparent, calibrated AI deployment.

---

## Summary

Standards and regulation for AI human oversight primarily establish *capability and process conformance*: that oversight roles are named, intervention is designed for, logs are kept, and reaction timeframes are computed. Operational *effectiveness* — whether the human layer actually catches automation's failures in deployment — typically requires post-deployment measurement, for which no explicit counterpart was identified in the standards and regulatory sources we reviewed. This note publishes the method and headline results of one working instrument for that measurement layer, from a small, fully provenance-tracked deployment, as evidence that the layer is implementable — including by a very small operator — and as input to standards drafters while the relevant texts (prEN 18229 series) remain in draft.

## Method

Every incident in our governance registry is classified by **which function of the automation↔authority gap failed**:

- **Observability (O):** the authority or its instruments could not see actual state — assertion without inspection, or verification surfaces that were blind (returning PASS regardless of reality).
- **Translation (T):** state was observable, but the compression from activity to claim distorted in transit — overstated receipts, count drift, status divergence across surfaces, ratified decisions not propagated.
- **Interpretation (I):** a faithful signal arrived and the judgment layer still failed — bandwidth saturation, unreliable signals weighted as reliable, gates that warn without consequence.
- **Execution residual (E):** discipline failures outside the gap (state visible, claims accurate).

Assignment is rule-driven at registration, append-only, and second-coded across independent reviewers; near-misses are captured in a separate low-friction class; incident severities are recorded in dollar terms where incurred.

## Headline results (observational; exploratory; single-organization longitudinal dataset)

Across N=44 registered incidents on one production platform: **Translation 43% · Observability 36% · Interpretation 18% · Execution residual 2%.**

Three findings we believe are useful to drafters and researchers:

1. **The claim layer fails most.** The modal failure is not the model and not the human — it is the compression between what automation did and what it reported. The layer that oversight decisions are actually made *from* was, in our record, the least faithful.
2. **Blind instruments are a distinct observability sub-mode.** Several incidents involved verification surfaces that passed by construction (e.g., a CI audit targeting a nonexistent path, printing PASS on every run). Functional-safety regimes address this class through mandatory proof testing of safety functions (IEC 61508-family practice); we found no equivalent requirement in the AI oversight stack reviewed, and we now require class-matched negative controls for every PASS-emitting instrument internally.
3. **Failure gravity and instrumentation were inverted.** Interpretation failures were rarest and gravest in our record — including oversight rituals performing vigilance without exercising it — and were the least instrumented class, each caught ad hoc. Our remediations (tiered ratification to ration reviewer bandwidth; trigger-based depth re-sampling of batch approvals; evidence-based revocability of automation components) target precisely this class.

## Correspondence to existing frameworks (conceptual, clause verification pending)

The taxonomy shows conceptual correspondence with EU AI Act Article 14(4): O with 14(4)(a) monitoring/anomaly detection; T with 14(4)(c) correct interpretation of output; I with 14(4)(b) automation bias and 14(4)(d) override; and with the automation dimensions of recent deployment-risk research (detection speed, decision authority, override capability — the P(H|F,A) decomposition). Our incident records carry the field that research agenda notes is absent from most AI incident taxonomies: the automation/oversight configuration in force at the time of failure.

## Limitations, stated plainly

Single organization; small N; observational and exploratory, not statistically general. Classification is judgment-tier, mitigated by rule-driven assignment and independent second-coding, with inter-rater reliability reporting planned. Absence claims ("no counterpart identified") are scoped to sources reviewed and are maintained as falsifiable: production of a covering regulatory or standards text demotes them, and we will publish such demotions. The registry records failures and captured near-misses; silent successes and false positives are not yet systematically measured (a confusion-matrix treatment is future work).

## What we offer

To standards drafters: a documented, citable failure class (false-green verification) with an established engineering remedy (proof-test/negative-control requirements) available for migration into the oversight and logging texts while they remain in draft. To researchers: an aggregated, provenance-governed longitudinal incident dataset structured around the fields the empirical validation agenda requests — automation context, expert-coded classification with measurable agreement, near-miss logging, denominators, and quantified severities. Aggregate data as published here; inquiries regarding methodology or collaboration welcome.

*Published under HumanAIOS's own disclosure discipline: this note asserts only what its registry evidences, scopes every absence claim, and was reviewed adversarially across independent AI substrates and ratified by its human operator prior to release.*

---

## Related Materials (ACAT Ecosystem)

**This collection:**
- Gap-Function Taxonomy Analysis (detailed incident classification)
- Regulatory Harmonization Crosswalk (correspondence to prEN/ISO/NIST standards)
- ACAT-X Partner Connection Plan (10-repo engagement roadmap)

**Broader ACAT Program:**
- ACAT Main Collection: https://zenodo.org/communities/humanaios-acat
- Primary Dataset: `humanaios/acat-assessments` (Hugging Face)
- Instrument & Methodology: Available in this collection

---

## External Use Authorizations

- ✓ **Route-4 Enquiry (prEN 18229-1/-3):** Evidence anchor for negative-control migration proposal
- ✓ **GD-04.6 External Anchor:** Grounds autonomy governance directives (Tier 3 operational cost evidence)
- ✓ **P(H|F,A) Academic Collaboration:** Reference for Johns Hopkins / Harrisburg research partnership
- ✓ **Standards/Regulatory Communities:** Open citation and reference
- ✓ **ACAT Extended Research:** Integration into broader AI calibration research ecosystem

**Sharing Conditions:** Aggregates only (no incident deanonymization, no proprietary methods disclosed beyond standards-relevant contributions)

---

## Publication Checklist (Multi-Platform Coordination)

### Platform Deposits (Sequential)

- [ ] **Zenodo** (Primary Archival)
  - [ ] Upload to collection 10.5281/zenodo.21135723
  - [ ] Link to ORCID 0009-0003-7540-4245
  - [ ] Assign DOI
  - [ ] Add metadata: ACAT ecosystem, gap-function taxonomy, oversight effectiveness

- [ ] **OSF** (Pre-registration & Discovery Hub)
  - [ ] Create OSF project registration under n2vjk
  - [ ] Link Zenodo DOI
  - [ ] Add collaborators: outreach, collaborator-ops
  - [ ] Add metadata tags: ACAT, oversight, calibration, incident-taxonomy

- [ ] **GitHub** (Version Control & Release)
  - [ ] Create release tag: `evidence-note-v1.0`
  - [ ] Link Zenodo DOI in release notes
  - [ ] Add supporting files: gap-function analysis, crosswalk, partner plan

- [ ] **arXiv** (Preprint & Research Community)
  - [ ] Submit preprint
  - [ ] Cross-reference Zenodo DOI
  - [ ] Link ORCID in author metadata
  - [ ] Get arXiv ID

### Cross-Practice Coordination (Mesh)

- [ ] **Humanaios → Outreach:** Propose publication with external engagement plan
- [ ] **Outreach → Route-4:** Prepare Enquiry comment linking evidence note
- [ ] **Outreach → Academic:** Contact P(H|F,A) authors with collaboration offer
- [ ] **Collaborator-ops:** Coordinate multi-platform deposits
- [ ] **Collaborator-ops → Monitoring:** Track Route-4 acknowledgment, download metrics, citation count

### Z2 Approvals Required

- [ ] **Evidence Note Content:** Accuracy, scope, sharing conditions verified
- [ ] **Multi-Platform Strategy:** Zenodo/OSF/GitHub/arXiv coordination approved
- [ ] **Mesh Proposal:** Triadic coordination (humanaios ↔ outreach ↔ collaborator-ops) ratified
- [ ] **External Use Paths:** Route-4, GD-04.6, academic collaboration authorized
- [ ] **Publication Timeline:** arXiv → Zenodo → OSF → GitHub sequence approved

### Success Metrics

- [ ] **Route-4 Enquiry Acknowledgment:** Commission acknowledges in prEN 18229 Enquiry record
- [ ] **Academic Outreach Response:** P(H|F,A) authors confirm engagement offer
- [ ] **Platform Visibility:** Publication live on Zenodo, OSF, GitHub, arXiv
- [ ] **DOI Resolution:** All DOIs resolve correctly, cross-platform links work
- [ ] **ORCID Integration:** Publication appears on ORCID profile within 30 days

---

## Z2 Approval Form (Multi-Platform Mesh Publication)

```
MULTI-PLATFORM EVIDENCE NOTE PUBLICATION — Z2 APPROVAL

Title: Measuring Realized Oversight Performance...
Version: 1.0 (ACAT-Integrated)
Coordination: Triadic (humanaios ↔ outreach ↔ collaborator-ops)

Content Verified by: ___________________________  Date: ________
  (Content Accuracy & Sharing Conditions)

Multi-Platform Strategy Approved by: ___________________________  Date: ________
  (Zenodo/OSF/GitHub/arXiv Coordination)

Mesh Proposal Ratified by: ___________________________  Date: ________
  (Cross-Practice Triadic Coordination)

AUTHORIZATION CHECKLIST:
  [ ] Evidence note content accurate & scoped
  [ ] Sharing conditions honored (aggregates-only, anonymized)
  [ ] Multi-platform deposits coordinated
  [ ] Route-4 Enquiry engagement authorized
  [ ] Academic collaboration offer authorized
  [ ] GD-04.6 external anchor use authorized
  [ ] ORCID integration approved
  [ ] Publication timeline confirmed

EXTERNAL ENGAGEMENT:
  [ ] Outreach: Route-4 Enquiry comment preparation
  [ ] Outreach: P(H|F,A) academic partnership contact
  [ ] Collaborator-ops: Multi-platform orchestration
  [ ] Collaborator-ops: Success metrics tracking

Publication greenlit for: ___________________________
  (Zenodo deposit date)

Expected Platform Availability:
  Zenodo:  ___________
  OSF:     ___________
  arXiv:   ___________
  GitHub:  ___________

Success Metric: Route-4 Enquiry acknowledgment by ___________
```

---

## Notes for Z2 Review

This publication integrates into the ACAT research ecosystem while contributing to standards development (Route-4 feedback) and academic collaboration (P(H|F,A)). The triadic mesh coordination (humanaios ↔ outreach ↔ collaborator-ops) maximizes reach while distributing responsibility:

- **Humanaios:** Content authority, evidence responsibility, researcher
- **Outreach:** External engagement, standards community liaison, academic partnerships
- **Collaborator-ops:** Operational orchestration, multi-platform management, metrics tracking

Route-4 Enquiry acknowledgment serves as the primary external-acceptance metric (GD-04.6 Tier 2 evidence).
