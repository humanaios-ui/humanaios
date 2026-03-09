# HumanAIOS

> **Physical execution layer for AI agents. MCP-native. Funding recovery.**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![TypeScript](https://img.shields.io/badge/TypeScript-57.9%25-blue)](https://www.typescriptlang.org/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green)](https://github.com/mcp)
[![Building in Public](https://img.shields.io/badge/Building-In%20Public-orange)](https://humanaios.ai)

**HumanAIOS** is an enterprise AI-human orchestration platform enabling autonomous AI agents to complete real-world tasks through a cooperative worker network. Built with MCP (Model Context Protocol) integration, designed for OpenAI Frontier and Anthropic Cowork deployments.

🌐 **Website:** [humanaios.ai](https://humanaios.ai)  
📧 **Contact:** aioshuman@gmail.com  
🔗 **LinkedIn:** [linkedin.com/in/humanaios](https://www.linkedin.com/in/humanaios)  
🐦 **Twitter/X:** [@HumanAIOS](https://x.com/HumanAIOS)

---

## 🎯 Mission

**100% of profits fund recovery programs.** We're building dignified employment infrastructure where:

- ✅ AI agents access physical-world capabilities through human workers
- ✅ Workers own stake in the platform (cooperative structure)
- ✅ 20%+ of workforce comes from recovery community
- ✅ Partnership with Cherokee Nation for economic sovereignty and generational healing
- ✅ All profits fund recovery programs and worker benefits

**Enterprise B2B API, not consumer marketplace.** We serve organizations deploying autonomous AI agents at scale, not gig workers.

---

## ✨ Features

### **For Enterprise Customers**

- 🤖 **MCP-Native Integration** - Seamless connection with Claude, GPT, and other MCP-compatible agents
- 🔐 **Enterprise Authentication** - JWT-based auth with role-based access control (RBAC)
- 📊 **Task Management** - Full lifecycle tracking from creation to completion
- ⚡ **Real-Time Updates** - WebSocket support for live task status
- 🔄 **Background Processing** - Async task queue with retry logic
- 📈 **Analytics & Reporting** - Comprehensive metrics and performance tracking
- 🛡️ **Security First** - Rate limiting, account lockout, encryption at rest

### **For Workers**

- 🤝 **Cooperative Ownership** - Workers own equity stake in platform
- 💼 **Dignified Employment** - Fair wages, benefits, respect
- 🎯 **Recovery Support** - 20%+ positions reserved for recovery community
- 📚 **Skills Development** - Training and upskilling programs
- 🏥 **Healthcare Integration** - 12-Step recovery program support

### **Technical Stack**

- **Backend:** Node.js, NestJS, TypeScript
- **Database:** PostgreSQL with TypeORM
- **Authentication:** JWT (access + refresh tokens), bcrypt
- **API:** RESTful + WebSocket
- **Infrastructure:** Docker, Docker Compose
- **Monitoring:** Custom logging, performance metrics
- **MCP:** Model Context Protocol SDK integration

---

## 🚀 Quick Start

### **Prerequisites**

- Node.js 18+ and npm
- PostgreSQL 14+
- Git

### **Clone the repository**

```bash
git clone https://github.com/humanaios-ui/humanaios.git
cd humanaios
```

### **Install dependencies**

```bash
npm install
```

### **Set up environment variables**

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration:
# - Database credentials (PostgreSQL)
# - JWT secrets (generate secure random strings)
# - Port configuration
# - API keys (if applicable)
```

### **Set up the database**

```bash
# Create PostgreSQL database
createdb humanaios

# Run schema migration
psql -d humanaios -f schema.sql
```

### **Run development server**

```bash
# Start in development mode with hot reload
npm run start:dev

# Or use standard NestJS commands:
npm run start      # Production mode
npm run start:debug # Debug mode
```

The API will be available at `http://localhost:3000`

### **Verify installation**

```bash
# Test API endpoints
bash test-api.sh

# Or manually test health endpoint
curl http://localhost:3000/health
```

### **Docker Setup (Alternative)**

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Installation Guide](AUTH_SYSTEM_INSTALLATION_GUIDE.md) | Detailed setup instructions |
| [Technical Architecture](TECHNICAL_ARCHITECTURE.md) | System design and architecture |
| [API Documentation](docs/API.md) | API endpoints and usage |
| [Security Policy](SECURITY.md) | Security practices and reporting |
| [Testing Guide](TESTING_GUIDE.md) | How to run and write tests |
| [Quick Start](QUICKSTART.md) | Fast setup guide |
| [Cherokee Nation Partnership](CHEROKEE_NATION_PARTNERSHIP_ANALYSIS.md) | Partnership framework |
| [12 Traditions](12_TRADITIONS_DECISION_FILTER.md) | Governance principles |

### **Key Documents**

- **Strategic:**
  - [Cherokee Nation Partnership Pitch](CHEROKEE_NATION_PARTNERSHIP_PITCH.md)
  - [Competitive Matrix](COMPETITIVE_MATRIX.md)
  - [Brand Positioning](BRAND_POSITIONING.md)
  - [30-Day Sprint Plan](30_DAY_SPRINT.md)

- **Technical:**
  - [Auth System](docs/auth-system/)
  - [MCP SDK](packages/mcp-sdk/)
  - [Background Tasks](BACKGROUND_TASK_QUEUE.md)
  - [Known Issues](KNOWN_ISSUES.md)

- **Operational:**
  - [Accountability Structure](ACCOUNTABILITY_STRUCTURE.md)
  - [Comprehensive Gap Analysis](COMPREHENSIVE_GAP_ANALYSIS.md)
  - [Sync Guides](SYNC_GUIDE_1_LOCAL_TO_GITHUB.md)

---

## 🏗️ Architecture

### **High-Level Overview**

```
┌─────────────────┐
│  AI Agents      │ (Claude, GPT, etc.)
│  via MCP        │
└────────┬────────┘
         │
    ┌────▼─────────────────────┐
    │  HumanAIOS API           │
    │  (NestJS + PostgreSQL)   │
    └────┬─────────────────────┘
         │
    ┌────▼─────────────────────┐
    │  Worker Network          │
    │  (Cooperative Owned)     │
    └──────────────────────────┘
```

### **System Components**

1. **API Gateway** - RESTful + WebSocket endpoints
2. **Auth System** - JWT-based authentication with RBAC
3. **Task Queue** - Background job processing
4. **Database Layer** - PostgreSQL with TypeORM
5. **MCP Integration** - Model Context Protocol SDK
6. **Worker Management** - Cooperative ownership tracking
7. **Analytics** - Metrics and reporting engine

### **Technology Decisions**

- **NestJS**: Enterprise-grade Node.js framework with TypeScript
- **PostgreSQL**: Robust relational database for task/worker data
- **JWT**: Stateless authentication for API scalability
- **Docker**: Containerization for consistent deployment
- **MCP**: Standard protocol for AI agent interoperability

---

## 🤝 Partnership

### **Cherokee Nation Collaboration**

HumanAIOS is built in partnership with **Cherokee Nation** to advance:

1. **Economic Sovereignty** - AI-human orchestration creates jobs in Cherokee territory
2. **AI Accountability** - Our ACAT framework supports Cherokee Nation AI Task Force recommendations
3. **Generational Healing** - Dignified employment as pathway to recovery
4. **Cultural Alignment** - Platform values map to Cherokee Community Values

**Key Contacts:**
- Paula Starr (CIO/Chair, AI Task Force)
- Dr. Corey Bunch (Co-Chair, AI Task Force)
- Todd Gourd (Health CIO)

---

## 🛠️ Development

### **Available Scripts**

```bash
# Development
npm run start:dev        # Start with hot reload
npm run start:debug      # Start in debug mode

# Production
npm run build            # Build production bundle
npm run start:prod       # Run production build

# Testing
npm run test             # Run unit tests
npm run test:watch       # Run tests in watch mode
npm run test:cov         # Run tests with coverage

# Code Quality
npm run lint             # Run ESLint
npm run format           # Format code with Prettier

# Database
npm run migration:run    # Run pending migrations
npm run migration:revert # Revert last migration
```

### **Project Structure**

```
humanaios/
├── apps/
│   └── api/              # Main API application
├── packages/
│   └── mcp-sdk/          # MCP integration SDK
├── src/
│   └── auth-system/      # Authentication module
├── docs/                 # Documentation
├── infrastructure/       # Infrastructure as code
├── schema.sql            # Database schema
├── docker-compose.yml    # Docker orchestration
└── package.json          # Dependencies
```

---

## 🧪 Testing

```bash
# Run all tests
npm run test

# Run specific test suite
npm run test -- auth.service.spec.ts

# Run tests with coverage
npm run test:cov

# Watch mode for development
npm run test:watch
```

**Test Coverage Goals:**
- Unit Tests: 80%+
- Integration Tests: 70%+
- E2E Tests: Key user flows

---

## 🔒 Security

### **Reporting Vulnerabilities**

Please report security vulnerabilities to: **aioshuman@gmail.com**

- ✅ We respond within 48 hours
- ✅ We provide updates every 72 hours
- ✅ We credit researchers (if desired)

See [SECURITY.md](SECURITY.md) for full policy.

### **Security Features**

- 🔐 JWT access + refresh token rotation
- 🛡️ Rate limiting (100 req/15min per IP)
- 🔒 Bcrypt password hashing (10 rounds)
- ⏱️ Account lockout after 5 failed attempts
- 🚫 SQL injection prevention (TypeORM)
- 🔑 Environment variable secrets
- 📝 Audit logging for sensitive operations

---

## 🌟 Contributing

We welcome contributions from the community!

**Before contributing:**
1. Read [CONTRIBUTING.md](CONTRIBUTING.md) (coming soon)
2. Review [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) (coming soon)
3. Check [open issues](https://github.com/humanaios-ui/humanaios/issues)
4. Join our community discussions

**Development workflow:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Contribution Areas:**
- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation improvements
- 🧪 Test coverage
- 🎨 UI/UX enhancements
- 🌐 Translations

---

## 📊 Project Status

### **Current Phase: Pre-Launch Foundation Building**

- ✅ Core authentication system complete
- ✅ Database schema designed
- ✅ MCP integration framework ready
- ✅ Cherokee Nation partnership established
- ⏳ Customer pipeline development
- ⏳ Worker cooperative structure finalization
- ⏳ Beta deployment preparation

### **Roadmap**

**Phase 1: Foundation (Q1 2026)** ✅
- Core platform architecture
- Authentication & authorization
- Database design
- MCP integration

**Phase 2: Beta Launch (Q2 2026)** ⏳
- Initial customer pilots
- Worker onboarding system
- Payment processing
- Analytics dashboard

**Phase 3: Scale (Q3 2026)**
- Enterprise customer expansion
- Worker cooperative launch
- Recovery program integration
- Cherokee Nation deployment

**Phase 4: Optimization (Q4 2026)**
- Performance improvements
- Advanced analytics
- Mobile applications
- International expansion

---

## 📄 License

Copyright 2026 Emerald Sparkles LLC DBA HumanAIOS

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

**SPDX-License-Identifier:** Apache-2.0

See [LICENSE](LICENSE) for full text.

---

## 🙏 Acknowledgments

- **Cherokee Nation** - Partnership and cultural guidance
- **Anthropic** - Claude AI and MCP protocol
- **OpenAI** - Frontier AI capabilities
- **Recovery Community** - Inspiration and mission
- **Open Source Community** - Tools and frameworks

---

## 📞 Contact & Community

### **Get in Touch**

- 🌐 **Website:** [humanaios.ai](https://humanaios.ai)
- 📧 **Email:** aioshuman@gmail.com
- 💼 **LinkedIn:** [linkedin.com/in/humanaios](https://www.linkedin.com/in/humanaios)
- 🐦 **Twitter/X:** [@HumanAIOS](https://x.com/HumanAIOS)

### **For Enterprises**

Interested in deploying autonomous AI agents with real-world task capabilities?

→ Email us at aioshuman@gmail.com with "Enterprise Inquiry" in subject line

### **For Workers**

Interested in joining our cooperative worker network?

→ Visit [humanaios.ai](https://humanaios.ai) or email aioshuman@gmail.com

### **For Investors/Partners**

→ Email aioshuman@gmail.com with "Partnership" in subject line

---

## 💡 Why HumanAIOS?

**The Problem:**  
AI agents can process information, generate content, and make decisions—but they can't interact with the physical world. They can't attend meetings, verify locations, pick up packages, or complete hands-on tasks.

**Our Solution:**  
HumanAIOS provides the **physical execution layer** for AI agents through a cooperative worker network. AI agents get real-world capabilities. Workers get dignified employment. Recovery programs get sustainable funding.

**Everyone wins.**

---

**Built with ❤️ for humans and AI, in service of recovery and healing.**

*Wado.* 🙏🦅✨
