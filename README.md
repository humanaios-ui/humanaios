# HumanAIOS

> AI-human orchestration research platform. OR&D phase. Pre-launch.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)
[![TypeScript](https://img.shields.io/badge/TypeScript-57.9%25-blue)](https://www.typescriptlang.org/)
[![Building in Public](https://img.shields.io/badge/Building-In%20Public-orange)](https://humanaios.ai)
[![Pre-Launch](https://img.shields.io/badge/Status-Pre--Launch-yellow)](./README.md)

> ⚠️ **Pre-launch.** No live API. No customers. No revenue yet.
> This repository contains an authentication scaffold and research documentation.
> See [Current Status](#current-status) for what actually exists.

🌐 Website: [humanaios.ai](https://humanaios.ai)
📧 Contact: aioshuman@gmail.com
🔗 LinkedIn: [linkedin.com/in/humanaios](https://www.linkedin.com/in/humanaios)
🐦 Twitter/X: [@HumanAIOS](https://x.com/HumanAIOS)
🔬 Research: [Observatory](https://humanaios.ai/observatory.html) · [arXiv preprint](https://arxiv.org/abs/2503.09618) · [Dataset](https://huggingface.co/datasets/humanaios/acat-assessments)

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
- ✅ arXiv preprint published ([2503.09618](https://arxiv.org/abs/2503.09618))
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
| arXiv preprint | [arxiv.org/abs/2503.09618](https://arxiv.org/abs/2503.09618) |
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
