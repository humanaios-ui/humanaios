# HumanAIOS

> The Operating System for Human-AI Workflows

**Status**: 🚧 In Active Development (Week 1/4 of MVP Sprint)

## What is HumanAIOS?

HumanAIOS is the first platform that monitors AI agents AND orchestrates the human tasks they can't do themselves. Think Datadog meets RentAHuman.

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

Current Sprint: **Week 1 - Foundation**

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
