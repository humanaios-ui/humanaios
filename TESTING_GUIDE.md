# 🧪 HumanAIOS Testing Guide

Complete guide to testing the HumanAIOS API and agent monitoring system.

---

## 📋 Prerequisites

Before testing, ensure you have:

- ✅ Docker Desktop running
- ✅ Node.js installed (v18+)
- ✅ `jq` installed (for JSON parsing in bash scripts)
- ✅ `curl` installed (usually pre-installed on Mac/Linux)

---

## 🚀 Quick Start (3 Steps)

### Step 1: Start the Infrastructure

```bash
cd ~/Desktop/humanaios/infrastructure
docker-compose up -d
```

**What this does:**
- Starts PostgreSQL database (port 5432)
- Starts Redis (port 6379)
- Starts Adminer web UI (port 8080)

**Verify it's running:**
```bash
docker-compose ps
```

You should see 3 containers running.

---

### Step 2: Start the API Server

```bash
cd ~/Desktop/humanaios/apps/api
npm install  # Only needed first time
npm run dev
```

**What this does:**
- Installs dependencies
- Runs database migrations
- Starts API server on port 3001
- Enables hot-reload for development

**Verify it's running:**
Open browser to: http://localhost:3001

You should see: `{"message":"HumanAIOS API","version":"1.0.0"}`

---

### Step 3: Run Tests

**Option A: Automated Test Script (Recommended)**

```bash
cd ~/Desktop/humanaios
chmod +x test-api.sh
./test-api.sh
```

This will:
- Register a test user
- Create 2 agents
- Log 4 different types of activities
- Retrieve agent data
- Show you everything working!

**Option B: Agent Simulator**

```bash
cd ~/Desktop/humanaios
npm install node-fetch  # Only needed first time
npx tsx agent-simulator.ts
```

This simulates real AI agents:
- Customer Support Agent (MCP)
- Data Analysis Agent (LangChain)
- Shows realistic workflows
- Logs activities automatically

---

## 🧪 Manual Testing (Step by Step)

If you want to test manually with curl commands:

### 1. Register a User

```bash
curl -X POST http://localhost:3001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@humanaios.ai",
    "password": "Demo123!",
    "name": "Demo User",
    "org_name": "Demo Organization"
  }'
```

**Expected response:**
```json
{
  "user": {
    "id": "...",
    "email": "demo@humanaios.ai",
    "name": "Demo User"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Save the token!** You'll need it for all other requests.

---

### 2. Create an Agent

```bash
TOKEN="YOUR_TOKEN_HERE"

curl -X POST http://localhost:3001/api/v1/agents \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "My First Agent",
    "type": "mcp",
    "description": "Testing agent creation",
    "metadata": {
      "version": "1.0.0"
    }
  }'
```

**Expected response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "org_id": "...",
  "name": "My First Agent",
  "type": "mcp",
  "status": "active",
  "created_at": "2026-02-07T..."
}
```

**Save the agent ID!** You'll need it to log activities.

---

### 3. List All Agents

```bash
curl -X GET http://localhost:3001/api/v1/agents \
  -H "Authorization: Bearer $TOKEN"
```

**Expected response:**
```json
[
  {
    "id": "...",
    "name": "My First Agent",
    "type": "mcp",
    "status": "active",
    ...
  }
]
```

---

### 4. Log an Activity (Tool Call)

```bash
AGENT_ID="YOUR_AGENT_ID_HERE"

curl -X POST http://localhost:3001/api/v1/agents/$AGENT_ID/activities \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "activity_type": "tool_call",
    "description": "Called weather API",
    "input_data": {
      "location": "San Francisco"
    },
    "output_data": {
      "temperature": 72,
      "conditions": "sunny"
    },
    "duration_ms": 145,
    "status": "success"
  }'
```

---

### 5. Log an LLM Request

```bash
curl -X POST http://localhost:3001/api/v1/agents/$AGENT_ID/activities \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "activity_type": "llm_request",
    "description": "Generated response",
    "tokens_used": 250,
    "cost_usd": 0.0075,
    "duration_ms": 892,
    "status": "success",
    "metadata": {
      "model": "claude-sonnet-4-20250514"
    }
  }'
```

---

### 6. Get Agent Activities

```bash
curl -X GET "http://localhost:3001/api/v1/agents/$AGENT_ID/activities?limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

**Expected response:**
```json
[
  {
    "id": "...",
    "agent_id": "...",
    "activity_type": "llm_request",
    "description": "Generated response",
    "tokens_used": 250,
    "cost_usd": 0.0075,
    "created_at": "2026-02-07T..."
  },
  ...
]
```

---

## 📊 View Data in Database

### Option 1: Adminer Web UI

1. Open browser to: http://localhost:8080
2. Login with:
   - System: PostgreSQL
   - Server: postgres
   - Username: postgres
   - Password: postgres
   - Database: humainos

3. Browse tables:
   - `organizations` - Your organization
   - `users` - Your user account
   - `agents` - Registered agents
   - `agent_activities` - All logged activities

### Option 2: Command Line

```bash
docker exec -it infrastructure-postgres-1 psql -U postgres -d humainos
```

Then run SQL queries:
```sql
-- See all agents
SELECT id, name, type, status FROM agents;

-- See recent activities
SELECT 
  activity_type, 
  description, 
  tokens_used, 
  cost_usd, 
  created_at 
FROM agent_activities 
ORDER BY created_at DESC 
LIMIT 10;

-- Calculate total cost
SELECT 
  SUM(cost_usd) as total_cost,
  COUNT(*) as total_activities
FROM agent_activities;
```

---

## 🎯 Testing Scenarios

### Scenario 1: Customer Support Workflow

1. Create agent: "Customer Support Bot"
2. Log tool call: search_knowledge_base
3. Log LLM request: generate_response
4. Log task completion: "Resolved customer issue"
5. View all activities

### Scenario 2: Error Handling

1. Create agent: "Flaky Agent"
2. Log successful activity
3. Log error activity with error_message
4. Check that both are logged correctly

### Scenario 3: Cost Tracking

1. Create agent: "Expensive Agent"
2. Log 5 LLM requests with different token counts
3. Query activities to calculate total cost
4. Verify cost calculations

---

## 🐛 Troubleshooting

### "Connection refused" error

**Problem:** API server not running

**Solution:**
```bash
cd ~/Desktop/humanaios/apps/api
npm run dev
```

### "Database connection error"

**Problem:** PostgreSQL not running

**Solution:**
```bash
cd ~/Desktop/humanaios/infrastructure
docker-compose up -d
```

### "Token invalid" error

**Problem:** Token expired or incorrect

**Solution:** Re-login to get a new token:
```bash
curl -X POST http://localhost:3001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@humanaios.ai",
    "password": "Demo123!"
  }'
```

### "jq: command not found"

**Problem:** jq not installed (needed for test script)

**Solution on Mac:**
```bash
brew install jq
```

---

## 📈 What to Test

### ✅ Core Functionality
- [ ] User registration
- [ ] User login
- [ ] Create agent
- [ ] List agents
- [ ] Get single agent
- [ ] Log activity
- [ ] Get activities
- [ ] Pagination works (limit/offset)

### ✅ Data Validation
- [ ] Required fields enforced
- [ ] Invalid agent types rejected
- [ ] Invalid activity types rejected
- [ ] Negative numbers rejected for tokens/cost

### ✅ Authentication
- [ ] Endpoints require valid token
- [ ] Invalid tokens rejected
- [ ] Users can only see their own org's data

### ✅ Performance
- [ ] Response times < 200ms for simple queries
- [ ] Can handle 100+ activities per agent
- [ ] Database queries are efficient

---

## 🎉 Success Criteria

You know the system works when:

1. ✅ You can register and login
2. ✅ You can create agents
3. ✅ Activities are logged correctly
4. ✅ Data shows up in database
5. ✅ Cost calculations are accurate
6. ✅ Multi-tenant isolation works (can't see other orgs' data)

---

## 📝 Next Steps After Testing

Once basic testing is complete:

1. **Week 2:** Build MCP SDK package
2. **Week 2:** Create dashboard UI
3. **Week 3:** Add human task system
4. **Week 4:** Polish and launch beta

---

## 💡 Tips

- Keep a notepad with your token and agent IDs
- Use Postman if you prefer GUI over curl
- Check the database directly to verify data
- Run the automated test script regularly
- The agent simulator is great for demos!

---

**Need help?** The API returns helpful error messages. Check the console output for details.

**Ready to ship?** Once tests pass, you have a working MVP! 🚀
