# RentAHuman Integration Specification

**Created:** February 9, 2026  
**Purpose:** Technical specification for HumanAIOS ↔ RentAHuman integration  
**Target:** Partnership agreement by Feb 28, 2026

---

## 🎯 INTEGRATION OVERVIEW

**What:** HumanAIOS routes enterprise AI agent tasks to RentAHuman's worker marketplace  
**Value:** We provide demand, they provide supply (70K+ workers)  
**Result:** Circular economy - AI agents → tasks → human workers → results

---

## 🔌 TECHNICAL ARCHITECTURE

Production-ready MCP integrationcd ~/Desktop/humanaios

cat > RENTAHUMAN_INTEGRATION_SPEC.md << 'EOF'
# RentAHuman Integration Specification

**Created:** February 9, 2026  
**Purpose:** Technical specification for HumanAIOS ↔ RentAHuman integration  
**Target:** Partnership agreement by Feb 28, 2026

---

## 🎯 INTEGRATION OVERVIEW

**What:** HumanAIOS routes enterprise AI agent tasks to RentAHuman's worker marketplace  
**Value:** We provide demand, they provide supply (70K+ workers)  
**Result:** Circular economy - AI agents → tasks → human workers → results

---

## 🔌 TECHNICAL ARCHITECTURE

### Flow Diagram
```
┌─────────────────┐
│  AI AGENT       │
│  (Customer's)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  HUMANAIOS      │ 1. Monitors agent activity
│  Platform       │ 2. Detects human task needed
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  MCP SDK        │ 3. Formats task for MCP
│  @humanaios/mcp │ 4. Calls RentAHuman API
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  RENTAHUMAN     │ 5. Matches worker
│  Marketplace    │ 6. Worker completes task
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  TASK RESULT    │ 7. Evidence collected
│  (back to agent)│ 8. Payment processed
└─────────────────┘
```

---

## 🛠️ INTEGRATION METHODS

### Option A: MCP Server Integration (Preferred)

**RentAHuman's MCP Server:**
- URL: `mcp://rentahuman.ai/v1`
- Protocol: Model Context Protocol
- Status: Already implemented by RentAHuman

**Our Implementation:**
```typescript
import { MCPClient } from '@modelcontextprotocol/sdk';

const rentahumanMCP = new MCPClient({
  server: 'mcp://rentahuman.ai/v1',
  apiKey: process.env.RENTAHUMAN_API_KEY
});

// Create task via MCP
const task = await rentahumanMCP.call('create_task', {
  title: 'Pick up package',
  description: '...',
  location: { lat: 37.7749, lng: -122.4194 },
  budget: 40
});
```

**Pros:**
- ✅ Standard protocol (MCP is becoming industry standard)
- ✅ Already built by RentAHuman
- ✅ Future-proof (OpenAI, Anthropic adopting MCP)

**Cons:**
- ⚠️ Depends on their MCP implementation quality
- ⚠️ Less direct control

---

### Option B: REST API Integration (Backup)

**RentAHuman's API:**
- Endpoint: `https://api.rentahuman.ai/v1`
- Auth: API key in header
- Format: JSON

**Our Implementation:**
```typescript
const response = await fetch('https://api.rentahuman.ai/v1/tasks', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'Pick up package',
    skills: ['delivery'],
    location: { lat: 37.7749, lng: -122.4194 },
    budget: 40
  })
});
```

**Pros:**
- ✅ Direct control
- ✅ Simple debugging
- ✅ Well-understood pattern

**Cons:**
- ⚠️ Need to maintain API wrapper
- ⚠️ Less "MCP native"

---

### Recommendation: **Start with Option A (MCP), fallback to Option B**

---

## 📊 DATA MAPPING

### HumanAIOS Task → RentAHuman Task

| HumanAIOS Field | RentAHuman Field | Notes |
|-----------------|------------------|-------|
| `task.title` | `title` | Direct mapping |
| `task.description` | `description` | Direct mapping |
| `task.skillsRequired[]` | `skills[]` | Direct mapping |
| `task.location.lat/lng` | `location.lat/lng` | Direct mapping |
| `task.budget` | `budget` | In USD |
| `task.estimatedDuration` | `estimated_time` | In minutes |
| `task.agentId` | `metadata.agent_id` | For tracking |

### RentAHuman Worker → HumanAIOS Worker

| RentAHuman Field | HumanAIOS Field | Notes |
|------------------|-----------------|-------|
| `worker.id` | `workerId` | Direct mapping |
| `worker.name` | `workerName` | Direct mapping |
| `worker.skills[]` | `skills[]` | Direct mapping |
| `worker.rating` | `rating` | 0-5 scale |
| `worker.hourly_rate` | `hourlyRate` | In USD |

---

## 💰 PAYMENT FLOW

### Current RentAHuman Model (Crypto)

**Issue:** Only accepts crypto (limits enterprise adoption)
```
Enterprise → USDC → Worker
```

**Our Enhancement:** Add fiat payment layer
```
Enterprise → HumanAIOS (USD) → Convert to USDC → RentAHuman → Worker
```

### Revenue Sharing Proposal

**Option 1: Commission Model**
- Enterprise pays HumanAIOS
- HumanAIOS takes 10% platform fee
- Pays RentAHuman 70% (worker gets this)
- RentAHuman takes 20% marketplace fee

**Example:** $100 task
- Enterprise pays: $100
- HumanAIOS keeps: $10
- RentAHuman receives: $90
- Worker receives: $70
- RentAHuman keeps: $20

**Option 2: Subscription + Pass-Through**
- Enterprise pays HumanAIOS monthly subscription
- Task payments pass through 100% to RentAHuman
- We make money on platform fees, not task fees

**Recommendation:** Start with Option 1 (simpler)

---

## 🔐 SECURITY & QUALITY

### Worker Verification

**RentAHuman handles:**
- Identity verification
- Skill validation
- Rating system

**We add:**
- Enterprise-specific vetting (optional)
- Background checks for sensitive tasks
- Additional insurance layer

### Task Verification

**Evidence Collection:**
- Photos with metadata (location, timestamp)
- GPS tracking for delivery tasks
- Digital signatures for documents
- Worker notes and explanations

**Our Quality Control:**
- Automated evidence verification
- Dispute resolution system
- Performance analytics
- Worker blacklist/whitelist

---

## 🚀 ROLLOUT PLAN

### Phase 1: Basic Integration (Week 1-2)

**Goals:**
- Connect to RentAHuman MCP server
- Create tasks successfully
- Receive task completions
- Process payments

**Deliverables:**
- MCP client implementation
- Task creation API
- Webhook for task updates
- Payment flow (crypto for now)

---

### Phase 2: Enterprise Features (Week 3-4)

**Goals:**
- Add fiat payment option
- Enterprise worker vetting
- Quality control dashboard
- Analytics and reporting

**Deliverables:**
- Payment gateway integration (Stripe)
- Worker screening API
- Admin dashboard
- Usage metrics

---

### Phase 3: Scale & Optimize (Week 5-8)

**Goals:**
- Handle 100+ concurrent tasks
- Worker matching optimization
- Cost optimization
- Partnership terms formalization

**Deliverables:**
- Load testing results
- ML-based worker matching
- Cost reduction features
- Legal partnership agreement

---

## 📞 PARTNERSHIP DISCUSSION POINTS

### For Initial Call with Alexander

**What we bring:**
1. **Enterprise demand** - B2B customers with budgets
2. **Stable task flow** - Recurring work, not one-off gigs
3. **Fiat payment option** - Removes crypto friction (13% conversion currently)
4. **Quality layer** - Verification, insurance, enterprise vetting
5. **Professional support** - Account management for customers

**What we need from them:**
1. **MCP API access** - Dedicated API key, documentation
2. **Priority support** - Direct line to technical team
3. **Revenue sharing terms** - Mutually beneficial split
4. **Worker prioritization** - Our tasks get first-class treatment
5. **Co-marketing** - Joint press releases, case studies

**Win-Win Scenario:**
- They get: Enterprise customers, stable revenue, fiat accessibility
- We get: 70K workers instantly, proven infrastructure, time-to-market

---

## 🎯 SUCCESS METRICS

### Month 1 (March 2026)
- ✅ Integration complete
- ✅ 10 tasks completed successfully
- ✅ Payment flow working
- ✅ Zero critical bugs

### Month 3 (May 2026)
- ✅ 100+ tasks/month
- ✅ 50+ active workers
- ✅ 95%+ task completion rate
- ✅ Enterprise customers satisfied

### Month 6 (August 2026)
- ✅ 500+ tasks/month
- ✅ 200+ active workers
- ✅ Revenue profitable
- ✅ Formal partnership agreement signed

---

## 🔧 TECHNICAL REQUIREMENTS

### Our Side

**Infrastructure:**
- MCP SDK implementation
- Task routing system
- Payment processing (Stripe)
- Worker verification API
- Analytics dashboard

**Team Needs:**
- 1 backend developer (task routing, payments)
- 1 integration engineer (MCP, APIs)
- Part-time QA

### Their Side

**Requirements from RentAHuman:**
- Stable MCP server (99%+ uptime)
- Webhook support for task updates
- API rate limits (100 requests/min minimum)
- Documentation (API specs, error codes)
- Support SLA (24-hour response for critical issues)

---

## 🐛 RISK MITIGATION

### Risk 1: RentAHuman Platform Instability

**Likelihood:** Medium (they're growing fast, possible scaling issues)  
**Impact:** High (blocks our service)  
**Mitigation:**
- Build backup marketplace (TaskRabbit API, Fiverr API)
- Monitor their uptime (alerts at <95%)
- Contract SLA terms

### Risk 2: Worker Quality Issues

**Likelihood:** Medium (marketplace quality varies)  
**Impact:** Medium (enterprise customer complaints)  
**Mitigation:**
- Rating threshold (only 4+ star workers for enterprise)
- Evidence verification (photos, GPS required)
- Money-back guarantee for failed tasks

### Risk 3: Payment Processing Problems

**Likelihood:** Low (Stripe is reliable)  
**Impact:** High (revenue affected)  
**Mitigation:**
- Dual payment processors (Stripe + PayPal)
- Crypto fallback option
- Manual processing backup

### Risk 4: Partnership Terms Disagreement

**Likelihood:** Medium (negotiation required)  
**Impact:** High (blocks partnership)  
**Mitigation:**
- Multiple partnership models prepared
- Legal counsel review
- Pilot period with minimal commitment

---

## 📄 NEXT STEPS

### This Week (Feb 9-15)
- [ ] Draft partnership email (with this spec attached)
- [ ] Public Twitter engagement if no DM response
- [ ] MCP SDK basic implementation
- [ ] Payment flow design

### Week 2 (Feb 16-22)
- [ ] Partnership call scheduled
- [ ] Technical integration started
- [ ] Test tasks on RentAHuman platform
- [ ] Payment gateway setup

### Week 3-4 (Feb 23 - Mar 8)
- [ ] Integration complete
- [ ] First enterprise customer using it
- [ ] Partnership terms finalized
- [ ] Co-marketing announcement

---

## 📞 CONTACT

**RentAHuman:**
- Founder: Alexander Liteplo (@AlexanderTw33ts)
- Platform: https://rentahuman.ai
- MCP Server: mcp://rentahuman.ai/v1

**Our Status:**
- Outreach: Feb 7, 2026 (DM sent)
- Follow-up: Feb 8, 2026
- Next: Public engagement by Feb 15 if no response
- Partnership target: Feb 28, 2026

---

**This spec serves as:**
1. Technical blueprint for integration
2. Partnership discussion framework
3. Risk mitigation plan
4. Success criteria definition

**Ready to attach to partnership outreach!** 🚀
