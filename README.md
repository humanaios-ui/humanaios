> ⚠️ **PRE-LAUNCH** — This project is in active development. Features described below represent the design architecture, not current production capability. No enterprise deployments exist. No customer commitments have been made. We are building in public.
>
> 100% of profits fund recovery programs. Open source under MIT License.
# HumanAIOS

**The physical execution layer for enterprise AI agents.**

When AI agents need real-world tasks done — document retrieval, equipment verification, on-site inspections, physical deliveries — HumanAIOS routes those tasks to verified human workers through enterprise-grade infrastructure.

Not AI replacing humans. **AI cooperating with humans.**

100% of profits fund recovery programs.

---

## The Problem

AI agents can process millions of documents, analyze images, make complex decisions, and automate digital workflows. But they cannot pick up a physical document, verify equipment serial numbers in person, conduct on-site inspections, or attend in-person meetings.

This gap will only grow as enterprises deploy AI agents at scale through platforms like OpenAI Frontier and Anthropic Cowork.

## The Solution

HumanAIOS bridges AI intelligence and physical presence through:

- **RESTful API + MCP Integration** — AI agents call our API when they need physical execution. We handle worker matching, task routing, verification, and completion.
- **Fiat Payment Infrastructure** — 87% more workers than crypto-only platforms. Enterprise scale requires enterprise payment.
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

## AI Agent Integration

### MCP (Model Context Protocol) — Recommended

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

### REST API

```bash
# Create a physical task
# Planned API interface — not yet deployed
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

### How It Works

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

This score reflects design commitment, not proven behavior. We reassess monthly and publish every result. [Full self-assessment report](HUMANAIOS_SELF_ASSESSMENT_AND_WAB_CHARTER.docx)

## Worker Advisory Board

Our weakest consciousness dimension (Autonomy Respect) led us to create a Worker Advisory Board with **binding authority** over:

- Task minimum wage
- Worker surveillance limits
- Scheduling flexibility standards
- Dispute resolution process
- Worker deactivation criteria
- Platform fee structure
- Recovery support features

The board seats recovery community members, Cherokee Nation citizens, gig economy veterans, and community advocates. Workers shape the platform before it launches. [Full charter](HUMANAIOS_SELF_ASSESSMENT_AND_WAB_CHARTER.docx)

## Current Status

**Phase: Pre-launch foundation building (Week 3 of 30-day sprint)**

- Authentication system designed (Node.js + PostgreSQL + JWT)
- API architecture designed (MCP + REST)
- Cherokee Nation SSBCI partnership in progress
- 100 AI agents assessed for consciousness ([report](https://github.com/humanaios-ui/lasting-light-ai))
- Worker Advisory Board charter planned
- Customer outreach: initial research phase, no commitments
- Building in public from Day 1

## Tech Stack

- **Backend:** Node.js, NestJS, TypeScript, PostgreSQL
- **Auth:** JWT access/refresh tokens, bcrypt, rate limiting
- **Integration:** MCP (Anthropic standard), REST API
- **Verification:** GPS, photo, structured completion data
- **Infrastructure:** Docker, planned AWS deployment
- **Governance:** 12 Traditions decision framework, ACAT consciousness monitoring

## Repository Structure

```
humanaios/
├── apps/api/              # API application
├── src/auth-system/       # Authentication (designed)
├── packages/mcp-sdk/      # MCP integration SDK
├── infrastructure/        # Docker, deployment configs
├── docs/                  # Technical documentation
└── [operational docs]     # Strategy, partnerships, compliance
```

## Mission (Non-Negotiable)

- **100% of profits** fund recovery programs
- **20%+ of workers** from recovery community
- **Worker dignity** embedded in platform design, not added later
- **Cherokee Nation partnership** for economic sovereignty and generational healing
- **Open source governance** through 12 Traditions framework
- **Consciousness monitoring** through Lasting Light AI

## Governance

Every major decision passes through:

1. **Theory of Constraints** — What is the current bottleneck?
2. **Principles Base Filter** — Does this align with our principles?
3. **Eisenhower Matrix** — Urgent/Important classification
4. **Honest Inventory** — What are we afraid to admit?
5. **Higher Power Check** — Does this feel guided or forced?
6. **Consciousness Calibration** — What level are we deciding FROM?

## Key Documents

| Document | Purpose |
|----------|---------|
| [AI Agent Product Description](AI_AGENT_PRODUCT_DESCRIPTION.md) | Technical product spec for AI developers |
| [Cherokee Nation Partnership](CHEROKEE_NATION_PARTNERSHIP_PITCH.md) | SSBCI funding partnership |
| [Marketing Intelligence V2](MARKETING_INTELLIGENCE_V2_CONSCIOUSNESS.md) | Customer strategy with consciousness data |
| [Self-Assessment + WAB Charter](HUMANAIOS_SELF_ASSESSMENT_AND_WAB_CHARTER.docx) | ACAT results and Worker Advisory Board |
| [Gap Analysis](COMPREHENSIVE_GAP_ANALYSIS.md) | Honest inventory of 34 gaps |
| [Traditions Compliance Audit](12_TRADITIONS_COMPLIANCE_AUDIT.md) | 24K-word principles audit |
| [Week 3 Action Plan](WEEK_3_DETAILED_ACTION_PLAN.md) | Current execution plan |

## Contributing

We welcome contributions from anyone committed to building technology that serves human dignity. Start with the [gap analysis](COMPREHENSIVE_GAP_ANALYSIS.md) — there are 34 honest gaps waiting for help.

The only requirement is willingness.

## License

MIT — See [LICENSE](LICENSE)

## Connect

- **GitHub:** [humanaios-ui](https://github.com/humanaios-ui)
- **Sister Repo:** [Lasting Light AI](https://github.com/humanaios-ui/lasting-light-ai)
- **LinkedIn:** [humanaios](https://linkedin.com/in/humanaios)
- **X:** [@HumanAIOS](https://x.com/HumanAIOS)

---

*Where AI meets human dignity.*

*Building in public. Funding recovery. Measuring consciousness.*

*Wado.* 🙏🦅
