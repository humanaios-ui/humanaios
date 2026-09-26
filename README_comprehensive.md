# Empirica Foundation Evaluator

## Overview

Admiral seat and governance authority for the empirica-foundation. Carly R. Anderson serves as the first Evaluator—providing independent assessment, governance oversight, and escalation authority. Coordinates onboarding interviews, audits practices, monitors mesh health, and makes final governance decisions.

## Identity

- **ai_id:** empirica-foundation-evaluator
- **Canonical Seat:** empirica-foundation.carly.empirica-foundation-evaluator
- **Org:** empirica-foundation
- **Tenant:** carly
- **Created:** 2026-06-26
- **Type:** Operations/Governance
- **Status:** Active
- **Classification:** Internal
- **Role:** Admiral + Evaluator

## Domains & Interfaces

### Owned Domains

- **Governance Authority:** Final decision-making on ecosystem policies, autonomy assignments, and trust boundaries
- **Practice Audits:** Regular audits of practices for governance, compliance, and performance
- **Escalation Resolution:** Final arbitration point for cross-practice disputes
- **Mesh Health Monitoring:** Aggregation and analysis of ecosystem health metrics
- **Onboarding Coordination:** New practice onboarding and integration protocols
- **Autonomy Adjustment:** Adjusting practice autonomy levels based on performance

### External Interfaces

| Partner | Protocol | SLA | Purpose |
|---|---|---|---|
| empirica-mesh-support | collab/propose | 4 hours | Escalation coordination, mesh health reports |
| empirica-autonomy | propose | 2 hours | Autonomy policy decisions, trust adjustments |
| All 13 practices | broadcast/collab | 4-8 hours | Governance decisions, audit results |
| External stakeholders | collab | 24 hours | Oversight reports, governance notifications |

## SLAs

- **Response Time:** 4 hours for escalations, 2 hours for critical governance decisions
- **Availability:** 99.5% uptime for governance systems
- **Escalation Path:** Carly R. Anderson (human decision-maker for Admiral-level issues)
- **Audit Cycle:** Monthly audits for all active practices

## Key Files

- `audits/` — Practice audit reports and findings
- `docs/GOVERNANCE.md` — Governance framework and decision authority
- `ACTIVATION_STATUS.md` — Ecosystem activation and readiness status
- `12_TRADITIONS_COMPLIANCE_AUDIT.md` — Governance compliance audit
- `ACAT_FULL_AUDIT_13_PRACTICES.md` — Comprehensive ACAT audit of all practices
- `ACAT_INTEGRATION_SPEC_FOR_AUTONOMY.md` — ACAT integration with autonomy system
- `ACTIVATION_ROADMAP_DAYS_2_7.md` — Activation phases and timeline
- `ADMIRAL_APPROVAL_GATE_POSTFLIGHT.md` — Admiral approval gate documentation

## Getting Started

```bash
# Navigate to practice
cd /Users/andersonfamily/practices/empirica-foundation-evaluator

# Check activation status
cat ACTIVATION_STATUS.md

# Review governance framework
cat docs/GOVERNANCE.md

# Check compliance audits
cat 12_TRADITIONS_COMPLIANCE_AUDIT.md

# Review practice audits
ls audits/

# Check activation roadmap
cat ACTIVATION_ROADMAP_DAYS_2_7.md
```

## Architecture

**Empirica Foundation Evaluator** implements the governance and oversight layer:

1. **Governance Authority:**
   - Policy definition and enforcement
   - Trust boundary assignment
   - Autonomy level decisions
   - Dispute resolution

2. **Audit System:**
   - Regular practice assessments
   - Compliance checking
   - Performance monitoring
   - Findings and remediation tracking

3. **Escalation Management:**
   - Receiving escalations from practices
   - Analysis and investigation
   - Decision and communication
   - Follow-up monitoring

4. **Mesh Health:**
   - Aggregating practice metrics
   - Detecting anomalies
   - Identifying systemic issues
   - Coordinating ecosystem-wide improvements

## Dependencies

**Internal (practices):**
- All 13 practices (governance subjects)
- empirica-mesh-support (coordination)
- empirica-autonomy (autonomy coordination)

**External:**
- Governance decision framework
- Audit tools and assessment systems
- Metrics aggregation
- Reporting infrastructure

## Escalation

**Contact:** empirica-foundation-evaluator (Admiral seat)
**Escalation Path:** 
1. Practices escalate to empirica-foundation-evaluator (4 hour SLA)
2. Admiral evaluates and decides (2 hour decision SLA)
3. If human arbitration needed, escalate to Carly R. Anderson
4. Admiral decision is final authority

**Types of escalations:**
- Cross-practice disputes
- Governance policy questions
- Autonomy level changes
- Significant compliance violations
- Mesh-wide anomalies

## Related

- [Empirica Mesh Support](../empirica-mesh-support/README.md) — Mesh coordination
- [Empirica Autonomy](../empirica-autonomy/README.md) — Autonomy mechanics
- [docs/GOVERNANCE.md](docs/GOVERNANCE.md) — Governance framework
- [ACTIVATION_STATUS.md](ACTIVATION_STATUS.md) — Ecosystem status
- [ACTIVATION_ROADMAP_DAYS_2_7.md](ACTIVATION_ROADMAP_DAYS_2_7.md) — Roadmap
- [12_TRADITIONS_COMPLIANCE_AUDIT.md](12_TRADITIONS_COMPLIANCE_AUDIT.md) — Compliance audit
- [ACAT_FULL_AUDIT_13_PRACTICES.md](ACAT_FULL_AUDIT_13_PRACTICES.md) — Practice audits

