# HumanAIOS Practice (Empirica Foundation)

Open-source AI calibration research and assessment infrastructure. Home of ACAT (AI Calibration Assessment Tool) methodology, corpus, and toolkit.

**See [docs/CLAUDE.md](docs/CLAUDE.md) for Claude Code seat instructions.**

## Quick Links
- [Practice Charter](docs/CHARTER.md)
- [Governance](docs/governance/)
- [Research Documentation](docs/)

## Scope
This practice houses the open research side of HumanAIOS. Confidential business operations are managed separately by HumanAIOS LLC.

---

**For product documentation, see [PRODUCT.md](PRODUCT.md).**

---

## 🎯 Mission

Technology serving AI-human cooperation. Every dollar of profit funds recovery services for marginalized communities.

**Not AI replacing humans. AI cooperating WITH humans.**

## 🎯 For Enterprise AI Agent Teams

If you're deploying **OpenAI Frontier** or **Anthropic Cowork** at enterprise scale, you've discovered AI agents can't execute physical-world tasks:

❌ Property inspections  
❌ Document pickups  
❌ Equipment verifications  
❌ In-person meetings  

**HumanAIOS provides the enterprise-grade physical execution layer:**

✅ 374K verified workers (via RentAHuman partnership)  
✅ Fiat payment infrastructure (unlock 87% crypto-blocked workers)  
✅ Quality SLA (photo/GPS/rating verification)  
✅ MCP integration (seamless Frontier/Cowork connectivity)  

**Early customers include Fortune 500 companies in:**
- Insurance (claims inspections)
- Technology (product testing)  
- Healthcare (lab sample logistics)
- Finance (document verification)

📧 **Enterprise inquiries:** aioshuman@gmail.com

---

## 🚀 What We're Building

When AI agents (OpenAI Frontier, Anthropic Claude) need physical-world execution:
- On-site inspections
- Package retrieval
- Document handling
- Local verification
- In-person meetings

HumanAIOS automatically routes these tasks to qualified human workers via established marketplaces (TaskRabbit, RentAHuman).

**Result:** AI agents get seamless access to the physical world. Humans get dignified income.

---

## 📊 Status

🚧 **Active Development** - Day 5 of 30-day sprint to $10K MRR

**Building in public:**
- Real progress ✅
- Real failures ✅
- Transparent journey ✅

Follow along: [@CarlyBuildsAI](https://twitter.com/CarlyBuildsAI)

---

## 🛠️ Tech Stack

**Backend:**
- TypeScript / NestJS
- PostgreSQL / Prisma ORM
- Redis (caching)
- Docker (containerization)

**Integration:**
- MCP (Model Context Protocol) SDK
- RESTful API
- Partner marketplace APIs

**Current Focus:**
- Auth system (Express-style implementation)
- Task routing algorithms
- Worker matching logic
- Quality verification

---

## 💰 Financial Covenant

We're committed to transparent allocation of all profits:

| Revenue Tier | Family/Operations | Recovery Services | Reinvestment |
|--------------|-------------------|-------------------|--------------|
| $0-10K MRR | 100% | 0% | 0% |
| $10K-50K MRR | 60% | 30% | 10% |
| $50K+ MRR | 40% | 50% | 10% |

**Full transparency:** We publish all numbers quarterly.

**Why?** Technology should fund recovery, not just extraction.

---

## 🤝 Get Involved

### For Enterprise Customers

**Deploying AI agents that need human execution?**
- Email: aioshuman@gmail.com
- Twitter: @CarlyBuildsAI

**Pilot Program:** Free 30-day trial, dedicated support, ROI guarantee

### For Human Workers

**Want dignified income working with AI agents?**

We're integrating with:
- TaskRabbit (60K+ Taskers)
- RentAHuman (200K+ workers)

More marketplaces coming soon.

### For Developers

**Want to contribute or build similar?**

The pattern is free. Fork it. Improve it. Share it.

**Issues and PRs welcome.**

---

## 🏗️ Project Structure

```
humanaios/
├── apps/
│   └── api/              # NestJS API server
│       ├── src/
│       │   ├── agents/   # AI agent management
│       │   ├── auth/     # Authentication
│       │   ├── tasks/    # Task routing
│       │   └── workers/  # Worker management
│       └── prisma/       # Database schema
├── packages/
│   └── mcp-sdk/          # Model Context Protocol SDK
└── docs/                 # Documentation
```

---

## 🚦 Getting Started

### Prerequisites

- Node.js 20+
- PostgreSQL 15+
- Redis 7+
- Docker (recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/humanaios/humanaios.git
cd humanaios

# Install dependencies
npm install

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Start database (Docker)
docker-compose up -d

# Run migrations
npm run db:migrate

# Start development server
npm run dev
```

### Environment Variables

```env
DATABASE_URL="postgresql://user:password@localhost:5432/humanaios"
REDIS_URL="redis://localhost:6379"
JWT_SECRET="your-secret-key"
PORT=3000
```

---

## 📖 Documentation

**Coming soon:**
- API documentation
- Integration guides
- Architecture overview
- Deployment instructions

**Building in public = docs evolve with code**

---

## 🧪 Testing

```bash
# Run tests
npm test

# Run integration tests
npm run test:integration

# Test coverage
npm run test:coverage
```

**Current coverage:** Building test suite (Day 6-7 priority)

---

## 🗺️ Roadmap

### Week 1 (Feb 6-12) - Foundation ✅
- [x] Infrastructure setup
- [x] Database schema
- [x] MCP SDK v0.1.0
- [x] Vision documents
- [ ] Auth system (in progress)

### Week 2 (Feb 13-19) - Integration
- [ ] Partnership integration (RentAHuman/TaskRabbit)
- [ ] Task routing engine
- [ ] Worker matching algorithm
- [ ] Quality verification

### Week 3 (Feb 20-26) - Customers
- [ ] First 3 pilot customers
- [ ] Dashboard MVP
- [ ] Analytics & reporting

### Week 4 (Feb 27-Mar 5) - Validation
- [ ] 100+ tasks completed
- [ ] Platform refinement
- [ ] Scaling preparation

### Post-Sprint (Mar 6-31) - Growth
- [ ] Scale to $10K MRR
- [ ] Recovery services funding begins
- [ ] Pattern replication

---

## 🤲 Our Principles

**Based on AA's 12 Traditions:**

1. **Common welfare first** - Mission > individual gain
2. **Higher Power authority** - Guided by prayer/meditation, not ego
3. **Open to all** - No gatekeeping, inclusive service
4. **Autonomous** - Independent operation within ecosystem
5. **Primary purpose** - AI-human cooperation funding recovery
6. **No endorsements** - Partnerships, not affiliations
7. **Self-supporting** - Customer revenue, not donations/VC
8. **Nonprofessional spirit** - Service mindset, not empire-building
9. **Minimal organization** - Lean, focused, mission-driven
10. **No outside issues** - Stay in our lane
11. **Attraction not promotion** - Show results, don't hype
12. **Principles before personalities** - Mission > founder ego

**These are HARD STOPS. We don't compromise.**

---

## 📜 License

MIT License - The pattern is free. Use it. Improve it. Share it.

See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

**Built with:**
- Recovery principles (AA's 12 Traditions)
- 10+ years healthcare operations experience
- Genuine human-AI partnership
- Community support and feedback

**Inspired by:**
- Those who've found recovery and want to serve others
- The belief that technology can restore dignity, not just extract value
- The idea that AI and humans can cooperate, not compete

---

## 📬 Contact

**Founder:** Carly Anderson  
**Email:** aioshuman@gmail.com  
**Twitter:** [@CarlyBuildsAI](https://twitter.com/CarlyBuildsAI)  
**Website:** Coming soon

**Building in public. Join the journey.** 🚀

---

## ⭐ Support

If this resonates with you:
- ⭐ Star this repo
- 🐦 Follow on Twitter
- 📢 Share with others building cooperation infrastructure
- 💬 Join the conversation

**The pattern is free. The relationship is what matters.**

---

*Last updated: February 10, 2026 - Day 5*
