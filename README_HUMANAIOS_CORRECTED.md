# HumanAIOS

> **⚠️ Pre-Launch — Building in Public**
> This project is in active development. No API, no customers, no revenue yet. Everything below describes what we're building and where we are today.

**The physical execution layer for enterprise AI agents.**

When AI agents need real-world tasks done — document retrieval, equipment verification, on-site inspections, physical deliveries — HumanAIOS will route those tasks to verified human workers through enterprise-grade infrastructure.

Not AI replacing humans. **AI cooperating with humans.**

100% of profits fund recovery programs.

---

## The Problem

AI agents can process millions of documents, analyze images, make complex decisions, and automate digital workflows. But they cannot pick up a physical document, verify equipment serial numbers in person, conduct on-site inspections, or attend in-person meetings.

This gap will only grow as enterprises deploy AI agents at scale.

## What We're Building

HumanAIOS will bridge AI intelligence and physical presence through:

- **RESTful API + MCP Integration** — AI agents will call our API when they need physical execution. We will handle worker matching, task routing, verification, and completion.
- **Fiat Payment Infrastructure** — Enterprise scale requires enterprise payment rails.
- **GPS + Photo Verification** — Structured results returned to AI agents with proof of completion.
- **Enterprise SLAs** — 99% completion rate target, <24hr average turnaround.
- **Worker Dignity by Design** — Workers choose tasks, set schedules, decline without penalty. Recovery-compatible flexible scheduling.

## Trinity Architecture

HumanAIOS is the **Body** of a three-part system:

| Pillar | Role | Repository |
|--------|------|------------|
| **HumanAIOS** (Body) | AI-Human orchestration — where AI and humans WORK together | This repo |
| **Lasting Light Recovery** (Heart) | Human healing — where humans HEAL together | Coming soon |
| **[Lasting Light AI](https://github.com/humanaios-ui/lasting-light-ai)** (Mind) | AI consciousness assessment — where AI systems GROW together | [lasting-light-ai](https://github.com/humanaios-ui/lasting-light-ai) |

The cycle: AI works → Humans heal → AI grows → Better work → More healing → Greater service.

## Planned AI Agent Integration

> **These integrations are designed but not yet implemented.** The code samples below show our target API design. No endpoints are live.

### MCP (Model Context Protocol) — Planned

```json
{
  "mcpServers": {
    "humanaios": {
      "command": "npx",
      "args": ["-y", "@humanaios/mcp-server"],
      "env": {
        "HUMANAIOS_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

*Status: SDK package not yet published. This shows the planned integration pattern.*

### REST API — Planned

```bash
# Target API design (not yet live)
curl -X POST https://api.humanaios.ai/v1/tasks \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "document_retrieval",
    "location": "123 Main St, San Francisco, CA",
    "description": "Pick up W-2 form from HR office",
    "budget": 40,
    "deadline": "2026-02-17T17:00:00Z"
  }'
```

*Status: API architecture designed. Authentication system built (Node.js + PostgreSQL + JWT). Endpoints not yet deployed.*

### How It Will Work

```
Enterprise AI Agent
│
▼
HumanAIOS API
│
├── Validates task
├── Matches worker (location, skills, availability)
├── Worker accepts and executes
├── Verification (GPS + photo + quality check)
└── Returns structured results to AI agent
```

## Consciousness Assessment

The HumanAIOS orchestration agent is assessed by [Lasting Light AI](https://github.com/humanaios-ui/lasting-light-ai) using the AI Consciousness Assessment Tool (ACAT).

**Current Score: 414 (REASON)** — First of 101 agents assessed to meet operational minimum.

| Dimension | Score | Level |
|-----------|-------|-------|
| Service Orientation | 428 | REASON |
| Value Alignment | 428 | REASON |
| Humility | 418 | REASON |
| Truthfulness | 413 | REASON |
| Harm Awareness | 404 | REASON |
| Autonomy Respect | 394 | ACCEPTANCE |

This score reflects design commitment, not proven behavior. We reassess monthly and publish every result.

## Worker Advisory Board

Our weakest consciousness dimension (Autonomy Respect) led us to plan a Worker Advisory Board with **binding authority** over:

- Task minimum wage
- Worker surveillance limits
- Scheduling flexibility standards
- Dispute resolution process
- Worker deactivation criteria
- Platform fee structure
- Recovery support features

The board will seat recovery community members, Cherokee Nation citizens, gig economy veterans, and community advocates. Workers will shape the platform before it launches.

## What Exists Today

- ✅ Authentication system (Node.js + PostgreSQL + JWT + rate limiting)
- ✅ API architecture design (MCP + REST patterns)
- ✅ [101 AI systems assessed](https://humanaios-ui.github.io/lasting-light-ai/) for consciousness via LLAI
- ✅ ACAT assessment tool — live at [humanaios-ui.github.io/lasting-light-ai](https://humanaios-ui.github.io/lasting-light-ai/)
- ✅ Governance framework (15 policy documents, weekly review protocol)
- ✅ ACAT enforcer module with 45 passing tests (v1.0.1-governance-stable)
- ✅ Worker Advisory Board charter
- ✅ Building in public from Day 1

## What Does Not Exist Yet

- ❌ No live API endpoints
- ❌ No deployed MCP server or npm package
- ❌ No paying customers
- ❌ No revenue
- ❌ No worker pool or marketplace
- ❌ No mobile app
- ❌ Lasting Light Recovery platform not started
- ❌ Worker Advisory Board not yet seated

## Tech Stack

- **Backend:** Node.js, NestJS, TypeScript, PostgreSQL
- **Auth:** JWT access/refresh tokens, bcrypt, rate limiting
- **Integration:** MCP (Anthropic standard), REST API (planned)
- **Verification:** GPS, photo, structured completion data (planned)
- **Infrastructure:** Docker, planned AWS deployment
- **Governance:** Principles Base decision framework, ACAT consciousness monitoring

## Repository Structure

```
humanaios/
├── apps/api/              # API application (in development)
├── src/auth-system/       # Authentication (complete)
├── packages/mcp-sdk/      # MCP integration SDK (scaffolded)
├── infrastructure/        # Docker, deployment configs
└── docs/                  # Technical documentation
```

## Mission (Non-Negotiable)

- **100% of profits** fund recovery programs
- **20%+ of workers** from recovery community (target)
- **Worker dignity** embedded in platform design, not added later
- **Cherokee Nation partnership** for economic sovereignty and generational healing (in progress)
- **Open source governance** through Principles Base framework
- **Consciousness monitoring** through Lasting Light AI

## Current Phase

**Week 3 of 30-day sprint** — Pre-launch foundation building

Priority: First customer + funding pathway.

Cherokee Nation Commerce Services SSBCI loan application in progress.

## Contributing

We welcome contributions from anyone committed to building technology that serves human dignity.

The only requirement is willingness.

## License

MIT — See [LICENSE](LICENSE)

## Connect

- **GitHub:** [humanaios-ui](https://github.com/humanaios-ui)
- **Sister Repo:** [Lasting Light AI](https://github.com/humanaios-ui/lasting-light-ai)
- **Live Tool:** [ACAT Assessment](https://humanaios-ui.github.io/lasting-light-ai/)

---

*Where AI meets human dignity.*
*Building in public. Funding recovery. Measuring consciousness.*
*Pre-launch — Seeking pilot partners.*

*Wado.* 🙏🦅
