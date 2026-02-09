# HumanAIOS

**Bridge the gap between AI capability and human dignity.**

Monitor AI agents, route tasks to humans, create meaningful work in the age of automation.

[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)](https://www.typescriptlang.org/)
[![NestJS](https://img.shields.io/badge/NestJS-10.0-red)](https://nestjs.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 Vision

**AI will transform work. We're building the infrastructure to make it dignified.**

- **For Enterprises:** Monitor AI agents, ensure human oversight, maintain quality
- **For Workers:** Meaningful employment doing what AI cannot
- **For Society:** Proof that automation can create work, not just eliminate it

**Read the full vision:** [MASTER_VISION.md](./MASTER_VISION.md)

---

## 🚀 Quick Start

### Prerequisites

- Node.js 20+
- Docker Desktop
- PostgreSQL (via Docker)

### Installation
```bash
# Clone repository
git clone https://github.com/humanaios/humanaios.git
cd humanaios

# Install dependencies
npm install

# Start infrastructure
cd infrastructure
docker-compose up -d

# Start API server
cd ../apps/api
npm run dev

# API running at http://localhost:3001
```

---

## 📦 Packages

### [@humanaios/mcp-sdk](./packages/mcp-sdk)
Official SDK for integrating with HumanAIOS.
```typescript
import HumanAIOSClient from '@humanaios/mcp-sdk';

const client = new HumanAIOSClient({ apiKey: 'your-key' });
const agent = await client.createAgent({ name: 'My Agent' });
```

**Status:** Alpha (v0.1.0)  
**[Documentation →](./packages/mcp-sdk/README.md)**

---

## 🏗️ Architecture
```
┌─────────────────┐
│   AI AGENTS     │  Monitor activity, detect human needs
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   HUMANAIOS     │  Route tasks, manage workers
│   Platform      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ HUMAN WORKERS   │  Complete tasks, provide results
└─────────────────┘
```

**Key Components:**
- **API Server** - NestJS backend with PostgreSQL
- **MCP SDK** - Client library for integration
- **Worker Marketplace** - RentAHuman integration (coming)
- **Admin Dashboard** - Management interface (planned)

---

## 🎯 Current Status (Feb 9, 2026)

### ✅ Completed (Day 1-4)
- Infrastructure (Docker, PostgreSQL, Redis)
- API Server (NestJS, TypeScript)
- Database schema (10 tables)
- MCP SDK (v0.1.0, tested end-to-end)
- Agent management endpoints
- Activity logging system
- Vision documents

### 🔄 In Progress
- Authentication system (DI fix pending)
- RentAHuman integration
- Payment processing

### 📋 Next Up
- Complete auth implementation
- MCP server for AI agents
- First enterprise customer
- Public beta launch

---

## 📚 Documentation

- **[Master Vision](./MASTER_VISION.md)** - Complete strategic vision
- **[Financial Covenant](./FINANCIAL_COVENANT.md)** - Revenue allocation & commitments
- **[AI Recovery Explained](./AI_RECOVERY_EXPLAINED.md)** - Public-facing mission
- **[RentAHuman Integration](./RENTAHUMAN_INTEGRATION_SPEC.md)** - Partnership framework
- **[Auth DI Issue](./AUTH_DI_ISSUE.md)** - Technical debugging notes

---

## 🤝 Key Partnerships

### RentAHuman (In Progress)
- **70,000+ human workers**
- MCP integration ready
- Partnership outreach active
- Target: Agreement by Feb 28, 2026

**[View Integration Spec →](./RENTAHUMAN_INTEGRATION_SPEC.md)**

---

## 🌍 Market Validation

**February 2026 - Perfect Timing:**

- ✅ TechCrunch: "2026 is the Year of the Humans"
- ✅ MCP donated to Linux Foundation (becoming standard)
- ✅ OpenAI Frontier validates enterprise AI agents
- ✅ Security concerns creating demand for monitoring
- ✅ No direct competitors in AI + human orchestration

**[View Market Intelligence →](./DAY_4_MARKET_INTELLIGENCE.md)**

---

## 💰 Business Model

**B2B SaaS** - Enterprises pay for AI agent monitoring + human task routing

**Pricing:**
- Starter: $499/month (5 agents, 100 tasks)
- Professional: $1,499/month (25 agents, 500 tasks)
- Enterprise: $2,999/month (unlimited agents/tasks)

**Revenue Flows:**
1. Enterprise → HumanAIOS (platform fee)
2. HumanAIOS → Family (stability)
3. Surplus → Lasting Light (recovery mission)
4. Lasting Light → Employment (workers)

**Circular economy:** Tech → Family → Mission → Employment → Success

---

## 🙏 Mission: Lasting Light

**HumanAIOS is the revenue engine for [Lasting Light](./MASTER_VISION.md#lasting-light-the-recovery-infrastructure):**

- Healthcare (Bridgeway Clinic)
- Recovery (12-step, peer support)
- Cooperative economics (CSA, wellness)
- Employment (AI-generated work)

**Goal:** Prove AI can fund human dignity through meaningful work.

**[Read Full Mission →](./AI_RECOVERY_EXPLAINED.md)**

---

## 🛠️ Development

### Scripts
```bash
# Install dependencies
npm install

# Start infrastructure
npm run infra:up

# Stop infrastructure  
npm run infra:down

# Start API server (development)
cd apps/api && npm run dev

# Build MCP SDK
cd packages/mcp-sdk && npm run build

# Test MCP SDK
cd packages/mcp-sdk && npx tsx src/test.ts
```

### Tech Stack

**Backend:**
- NestJS 10
- TypeScript 5
- PostgreSQL 16
- Redis 7
- Docker

**SDK:**
- TypeScript 5
- Fetch API
- Model Context Protocol

---

## 📊 Progress Tracking

**30-Day Sprint** (Started Feb 6, 2026)

- ✅ **Day 1-2:** Infrastructure + strategy
- ✅ **Day 3-4:** Database + MCP SDK + vision
- 🔄 **Day 5:** Auth fix + API completion
- 📋 **Day 6-10:** RentAHuman integration
- 📋 **Day 11-20:** First enterprise customer
- 📋 **Day 21-30:** Beta launch

**Goal:** $10K MRR by March 31, 2026

---

## 🤝 Contributing

We welcome contributions! Areas of focus:

- Auth system debugging
- MCP server implementation
- RentAHuman integration
- Documentation improvements
- Test coverage

**[Contributing Guide →](./CONTRIBUTING.md)** (coming soon)

---

## 📄 License

MIT © 2026 HumanAIOS

---

## 📞 Connect

- **Website:** humanaios.com (coming soon)
- **Email:** hello@humanaios.com
- **Twitter:** [@HumanAIOS](https://twitter.com/HumanAIOS)
- **LinkedIn:** [HumanAIOS](https://linkedin.com/company/humanaios)
- **GitHub:** [humanaios](https://github.com/humanaios)

---

**Built with purpose. Funded by innovation. Guided by meditation. Serving recovery.**

*Every line of code serves dignity. Every feature serves flourishing.*

---

**Current Version:** 0.1.0 (Alpha)  
**Last Updated:** February 9, 2026  
**Status:** Active Development 🚀
