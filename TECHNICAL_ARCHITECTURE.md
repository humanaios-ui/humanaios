# HumanAIOS - AI-Human Orchestration Platform
## Technical Architecture v1.0

**Project Name**: HumanAIOS
**Domain**: humainos.ai
**Mission**: The operating system for human-AI workflow orchestration

---

## System Overview

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Applications                      │
│              (Web Dashboard + Mobile App)                    │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────┴─────────────────────────────────────┐
│                      API Gateway                             │
│            (Authentication, Rate Limiting, Routing)          │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼──────┐ ┌─────▼──────┐ ┌─────▼──────────┐
│ Agent        │ │ Human      │ │ Orchestration  │
│ Monitoring   │ │ Task       │ │ Engine         │
│ Service      │ │ Service    │ │                │
└──────┬───────┘ └─────┬──────┘ └─────┬──────────┘
       │               │              │
┌──────▼───────────────▼──────────────▼──────────┐
│           Core Data Layer                      │
│    (PostgreSQL + Redis + TimescaleDB)          │
└────────────────────────────────────────────────┘
```

---

## Phase 1: MVP (Weeks 1-12)

### Core Features

**1. Agent Monitoring Dashboard**
- Real-time activity feed
- Cost tracking per agent/task
- Error monitoring and alerts
- Performance metrics
- Audit logs

**2. MCP Integration Layer**
- Connect to MCP servers
- Intercept agent tool calls
- Track agent decisions and actions
- Store conversation history

**3. Basic Human Task Detection**
- Identify when agent requests human help
- Flag physical-world tasks
- Manual approval workflow
- Basic task tracking

---

## Tech Stack

### Backend
- **Runtime**: Node.js 20+ (TypeScript)
- **Framework**: NestJS (enterprise-grade, modular architecture)
- **API**: REST + GraphQL (Apollo Server)
- **Authentication**: JWT + OAuth 2.0
- **Real-time**: WebSockets (Socket.io)

### Database
- **Primary**: PostgreSQL 15+ (relational data, ACID compliance)
- **Time-series**: TimescaleDB (agent activity logs, metrics)
- **Cache**: Redis (real-time data, session management)
- **Search**: PostgreSQL Full-Text (initial), Elasticsearch (later)

### Frontend
- **Framework**: Next.js 14+ (React, Server Components)
- **UI Library**: shadcn/ui + Tailwind CSS
- **State Management**: Zustand + React Query
- **Charts**: Recharts + D3.js
- **Real-time**: Socket.io client

### Mobile (Phase 2)
- **Framework**: React Native + Expo
- **Target**: iOS & Android

### Infrastructure
- **Hosting**: AWS (initial) - easy to migrate later
- **Compute**: ECS Fargate (containerized, auto-scaling)
- **Storage**: S3 (logs, artifacts, attachments)
- **CDN**: CloudFront
- **Monitoring**: CloudWatch + Sentry

### AI/ML Components
- **Agent Analysis**: OpenAI API (GPT-4) for classification
- **Cost Prediction**: Simple regression models (Python microservice)
- **Task Routing**: Rule-based initially, ML later

---

## Data Models (Core Entities)

### 1. Organization
```typescript
{
  id: uuid
  name: string
  plan: 'free' | 'starter' | 'pro' | 'enterprise'
  settings: jsonb
  created_at: timestamp
}
```

### 2. Agent
```typescript
{
  id: uuid
  org_id: uuid
  name: string
  type: 'mcp' | 'langchain' | 'crewai' | 'custom'
  config: jsonb
  status: 'active' | 'paused' | 'error'
  created_at: timestamp
}
```

### 3. AgentActivity
```typescript
{
  id: uuid
  agent_id: uuid
  type: 'tool_call' | 'decision' | 'error' | 'human_request'
  payload: jsonb
  cost_usd: decimal
  duration_ms: integer
  timestamp: timestamp (indexed)
}
```

### 4. HumanTask
```typescript
{
  id: uuid
  agent_id: uuid
  title: string
  description: text
  status: 'pending' | 'approved' | 'assigned' | 'in_progress' | 'completed' | 'failed'
  task_type: 'verification' | 'pickup' | 'inspection' | 'attendance' | 'other'
  location: geography (PostGIS)
  budget_usd: decimal
  assigned_to: uuid (nullable)
  result: jsonb (nullable)
  created_at: timestamp
  completed_at: timestamp (nullable)
}
```

### 5. User
```typescript
{
  id: uuid
  org_id: uuid
  email: string
  role: 'admin' | 'operator' | 'viewer'
  auth_provider: 'email' | 'google' | 'github'
  created_at: timestamp
}
```

---

## API Endpoints (MVP)

### Agent Monitoring
```
GET    /api/v1/agents                    # List all agents
POST   /api/v1/agents                    # Register new agent
GET    /api/v1/agents/:id                # Get agent details
GET    /api/v1/agents/:id/activities     # Get activity log
GET    /api/v1/agents/:id/metrics        # Get performance metrics
```

### Human Tasks
```
GET    /api/v1/tasks                     # List all tasks
POST   /api/v1/tasks                     # Create task
GET    /api/v1/tasks/:id                 # Get task details
PATCH  /api/v1/tasks/:id                 # Update task
POST   /api/v1/tasks/:id/approve         # Approve pending task
POST   /api/v1/tasks/:id/complete        # Mark task complete
```

### Analytics
```
GET    /api/v1/analytics/costs           # Cost breakdown
GET    /api/v1/analytics/performance     # Performance metrics
GET    /api/v1/analytics/tasks           # Task completion rates
```

---

## MCP Integration Strategy

### How We Connect to Agents

**1. SDK/Library Approach**
- Provide NPM package: `@humainos/mcp-monitor`
- Developers add to their MCP servers
- Auto-reports activity to our platform

```typescript
import { HumanAIOSMonitor } from '@humainos/mcp-monitor';

const monitor = new HumanAIOSMonitor({
  apiKey: 'your-api-key',
  agentId: 'agent-uuid'
});

// Wraps MCP tool calls
server.tool('get_weather', monitor.wrap(async (params) => {
  // Original tool logic
}));
```

**2. Proxy Approach** (Phase 2)
- MCP requests route through our proxy
- We intercept, log, forward
- No code changes required
- More powerful but harder to implement

---

## Security & Compliance

### Authentication
- JWT tokens (short-lived: 1 hour)
- Refresh tokens (30 days)
- API keys for agent SDK (rotatable)

### Authorization
- Role-based access control (RBAC)
- Organization-level isolation
- Resource-level permissions

### Data Protection
- Encryption at rest (AES-256)
- Encryption in transit (TLS 1.3)
- PII redaction in logs
- GDPR compliance (data export, deletion)

### Audit Trail
- All actions logged
- Immutable audit logs
- 90-day retention (free), unlimited (paid)

---

## Deployment Strategy

### Environments
1. **Local Development**: Docker Compose
2. **Staging**: AWS ECS (single instance)
3. **Production**: AWS ECS (auto-scaling)

### CI/CD Pipeline
```
GitHub → GitHub Actions → Docker Build → ECR → ECS Deploy
         ↓
         Jest Tests
         ESLint
         TypeScript Check
```

### Monitoring
- Application: Sentry (errors)
- Infrastructure: CloudWatch (metrics, logs)
- Uptime: UptimeRobot
- APM: New Relic (later)

---

## Development Workflow

### Week 1-2: Setup
- [ ] Repository setup (monorepo with Turborepo)
- [ ] Database schema
- [ ] Authentication system
- [ ] Basic API structure
- [ ] Development environment (Docker)

### Week 3-4: Agent Monitoring
- [ ] Agent registration
- [ ] Activity logging
- [ ] Cost tracking
- [ ] Basic dashboard UI

### Week 5-6: MCP Integration
- [ ] MCP SDK package
- [ ] Activity interception
- [ ] Tool call logging
- [ ] Error handling

### Week 7-8: Human Tasks
- [ ] Task creation workflow
- [ ] Approval system
- [ ] Task tracking
- [ ] Status updates

### Week 9-10: Dashboard Polish
- [ ] Real-time updates
- [ ] Charts and visualizations
- [ ] Responsive design
- [ ] User onboarding

### Week 11-12: Beta Launch
- [ ] Documentation
- [ ] Example integrations
- [ ] Landing page
- [ ] First 5 design partners

---

## Success Metrics (MVP)

### Technical
- API response time: <200ms (p95)
- Uptime: >99.5%
- Error rate: <0.1%
- Dashboard load time: <2s

### Product
- 5 design partner companies
- 20+ agents monitored
- 50+ human tasks tracked
- Positive feedback from all partners

### Business
- Clear value proposition validated
- Pricing model tested
- Feature requests prioritized
- Path to Phase 2 defined

---

## Phase 2 Preview (Months 4-6)

- RentAHuman API integration
- Mobile app for human workers
- Advanced task routing
- Webhook system for notifications
- Multi-agent coordination
- Custom integrations (Slack, email, etc.)

---

## Risk Mitigation

### Technical Risks
- **MCP adoption is slow**: Build adapters for LangChain, CrewAI
- **Performance issues at scale**: TimescaleDB + Redis caching
- **Integration complexity**: Start simple, iterate based on feedback

### Business Risks
- **Market fit uncertainty**: 5 design partners validate before scaling
- **Competition**: Focus on human-AI orchestration angle
- **Pricing**: Test multiple models during beta

### Operational Risks
- **Team capacity**: Use managed services (AWS, Auth0, etc.)
- **Support load**: Build comprehensive docs, self-service
- **Security incidents**: Regular audits, bug bounty later

---

## Next Immediate Steps

1. **Set up GitHub repository** (monorepo structure)
2. **Initialize database schema** (PostgreSQL + migrations)
3. **Build authentication system** (JWT + user management)
4. **Create basic API** (NestJS + first endpoints)
5. **Start dashboard** (Next.js + basic layout)

Let's build this. 🚀
