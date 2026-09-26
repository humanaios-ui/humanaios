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

---

## Mission

100% of profits fund recovery programs. HumanAIOS is building dignified employment infrastructure where:

- AI agents access physical-world capabilities through human workers
- Workers own stake in the platform (cooperative structure)
- 20%+ of workforce comes from recovery community
- All profits fund recovery programs and worker benefits

Enterprise B2B, not consumer marketplace. We serve organizations deploying autonomous AI agents, not gig workers.

---

## What This Is

HumanAIOS is the **Body** pillar of a three-platform Trinity:

| Platform | Pillar | Purpose |
| --- | --- | --- |
| **HumanAIOS** | Body | AI-human orchestration — where AI and human capability meet |
| **Lasting Light Recovery** | Heart | Human anonymity platform — where humans can be seen safely |
| **Lasting Light AI** | Mind | AI anonymity platform — where AI systems can be measured honestly |

The research arm of this project — ACAT (AI Calibration Assessment Tool) — is active and generating data. See the [Observatory](https://humanaios.ai/observatory.html) for live findings.

---

## Current Status

### What exists right now

- ✅ Authentication scaffold (NestJS + PostgreSQL) — functional but not deployed
- ✅ Database schema designed
- ✅ ACAT research pipeline live (630+ assessments, 31+ canonical AI systems, [Hugging Face dataset](https://huggingface.co/datasets/humanaios/acat-assessments))
- ✅ Observatory dashboard live at [humanaios.ai/observatory.html](https://humanaios.ai/observatory.html)
- ✅ arXiv preprint published (Preprint in preparation)
- ✅ LLC formation complete (HumanAIOS LLC, Florida, effective March 16, 2026)
- ✅ EIN assigned

### What does not exist yet

- ❌ Live API endpoint
- ❌ MCP integration (design spec only — see `packages/mcp-sdk/`)
- ❌ Worker network or cooperative structure
- ❌ Task management, WebSocket, analytics systems
- ❌ Enterprise customers
- ❌ Payment processing

---

## The Scaffold

This repo contains the foundation layer:

```
humanaios/
├── apps/api/              # NestJS API application (scaffold)
├── packages/mcp-sdk/      # MCP integration (design spec — not implemented)
├── src/auth-system/       # Authentication module (functional)
├── docs/                  # Documentation
├── infrastructure/        # Infrastructure as code
├── schema.sql             # Database schema
└── docker-compose.yml     # Local dev environment
```

### Authentication system (what actually runs)

- 8 API endpoints: register, login, refresh, logout, password reset, profile
- JWT access + refresh token rotation
- bcrypt password hashing (10 rounds)
- Rate limiting, account lockout after 5 failed attempts
- PostgreSQL with TypeORM

---

## Quick Start (Local Dev Only)

Prerequisites: Node.js 18+, PostgreSQL 14+

```bash
git clone https://github.com/humanaios-ui/humanaios.git
cd humanaios
npm install
cp .env.example .env   # Edit with your local DB credentials
createdb humanaios
psql -d humanaios -f schema.sql
npm run start:dev
```

The auth API will be available at `http://localhost:3000`. There is no `/docs` Swagger endpoint yet.

---

## Research Ecosystem

HumanAIOS runs an active OR&D (Observational Research & Development) phase through its sister platform, Lasting Light AI. All research infrastructure is live:

| Resource | Link |
| --- | --- |
| Observatory (live dashboard) | [humanaios.ai/observatory.html](https://humanaios.ai/observatory.html) |
| ACAT Assessment Tool | [humanaios.ai/acat-assessment-tool.html](https://humanaios.ai/acat-assessment-tool.html) |
| arXiv preprint | Preprint (in preparation) |
| Hugging Face dataset | [huggingface.co/datasets/humanaios/acat-assessments](https://huggingface.co/datasets/humanaios/acat-assessments) |
| Primary research repo | [github.com/humanaios-ui/lasting-light-ai](https://github.com/humanaios-ui/lasting-light-ai) |
| Independent replication (Inspect port) | [github.com/humanaios-ui/acat-inspect](https://github.com/humanaios-ui/acat-inspect) |

---

## Roadmap

**Phase 1: Foundation (Q1 2026) — In progress**

- Authentication scaffold
- Database design
- ACAT research pipeline
- arXiv preprint published

**Phase 2: Beta Launch (Q2–Q3 2026)**

- Live API deployment
- Initial customer pilots
- Worker onboarding system
- MCP integration

**Phase 3: Cooperative Launch (2027)**

- Worker cooperative structure
- Recovery program integration
- Enterprise expansion

---

## Security

Report vulnerabilities to: aioshuman@gmail.com

See [SECURITY.md](./SECURITY.md) for full policy.

---

## Contributing

We welcome contributors, especially from the research and recovery communities. See [CONTRIBUTING.md](./CONTRIBUTING.md) — coming soon.

In the meantime, the best way to contribute is through the ACAT research platform at [Lasting Light AI](https://github.com/humanaios-ui/lasting-light-ai), or through the [acat-inspect](https://github.com/humanaios-ui/acat-inspect) independent replication effort.

---

## License

Copyright 2026 HumanAIOS LLC

Licensed under the Apache License, Version 2.0. See [LICENSE](./LICENSE) for full text.

---

## Contact

- 🌐 Website: [humanaios.ai](https://humanaios.ai)
- 📧 Email: aioshuman@gmail.com
- 💼 LinkedIn: [linkedin.com/in/humanaios](https://www.linkedin.com/in/humanaios)
- 🐦 Twitter/X: [@HumanAIOS](https://x.com/HumanAIOS)

---

*Built in service of recovery and healing.*

Wado. 🙏🦅
