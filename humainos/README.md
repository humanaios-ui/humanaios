# HumanAIOS

> The Operating System for Human-AI Workflows

**Status**: 🚧 In Active Development (Week 1/4 of MVP Sprint)

## What is HumanAIOS?

HumanAIOS is the **only platform that orchestrates BOTH AI agents AND human workers**. While competitors just monitor what your AI does, we help when your AI can't do it alone.

**The Problem**: Companies deploy AI agents but have no visibility into their actions, costs spiral out of control, and there's no system to handle tasks AI can't complete (deliveries, verifications, physical presence).

**Our Solution**: Complete orchestration of hybrid AI-human workflows. Monitor every agent action, track costs in real-time, and automatically delegate physical-world tasks to humans - all in one system.

### How We're Different

**vs. Braintrust, Arize, Maxim (AI Monitoring Platforms)**
- They monitor AI performance → We orchestrate AI + human work
- They show you what happened → We help when AI can't do it
- AI-only visibility → Complete AI-human workflow orchestration

**vs. RentAHuman (Human Task Marketplace)**  
- They connect you to humans → We integrate humans into AI workflows automatically
- Separate system → Unified monitoring + execution platform
- Manual task creation → Automatic detection and routing

**vs. OpenAI Frontier (Agent Management Platform)**
- They build/deploy agents → We monitor + orchestrate with humans
- Agent governance → Complete workflow orchestration
- Enterprise-only → Accessible to all (Free tier to Enterprise)

### Core Value Propositions

- 📊 **Complete Visibility**: See every action your AI agents take in real-time
- 💰 **Cost Control**: Track expenses down to individual tasks
- 🤝 **Human Orchestration**: Seamlessly hand off physical-world tasks to humans
- 🔒 **Enterprise-Grade**: Security, compliance, and reliability from day one

## Quick Start

```bash
# Coming soon - target launch: March 8, 2026
npm install @humainos/mcp-monitor
```

## Architecture

```
📦 HumanAIOS (Monorepo)
├── 📱 apps/
│   ├── web/          # Next.js dashboard
│   └── api/          # NestJS backend
├── 📚 packages/
│   ├── mcp-monitor/  # NPM SDK for MCP integration
│   ├── ui/           # Shared UI components
│   └── types/        # Shared TypeScript types
└── 🗄️ infrastructure/ # Docker, deployment configs
```

## Tech Stack

- **Frontend**: Next.js 14, React, Tailwind CSS, shadcn/ui
- **Backend**: NestJS, PostgreSQL, TimescaleDB, Redis
- **SDK**: TypeScript, MCP Protocol
- **Infrastructure**: AWS ECS, Docker, GitHub Actions

## Development Status

**Current Sprint: Week 1 - Day 2/30 Complete (Ahead of Schedule!)**

**Completed (Day 1-2)**:

- [x] Repository structure
- [x] Technical architecture
- [x] Brand positioning
- [ ] Database schema
- [ ] Authentication system
- [ ] Basic API endpoints
- [ ] Dashboard skeleton

See [30_DAY_SPRINT.md](./30_DAY_SPRINT.md) for detailed timeline.

## Documentation

- [Technical Architecture](./TECHNICAL_ARCHITECTURE.md)
- [30-Day Sprint Plan](./30_DAY_SPRINT.md)
- [Brand & Positioning](./BRAND_POSITIONING.md)

## Contributing

Currently in private beta development. Interested in becoming a design partner? 

Contact: team@humainos.ai

## License

Proprietary - All rights reserved (for now)

---

Built with ❤️ by humans and AI working together.
