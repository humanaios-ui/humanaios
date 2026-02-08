# 🚀 Quick Start - Day 2 Demo

**Time to test:** ~5 minutes  
**What you'll see:** Working agent monitoring system

---

## ⚡ Fastest Way to See It Working

### 1. Start Everything (One Command)

```bash
# From your Mac terminal
cd ~/Desktop/humanaios

# Start database
cd infrastructure && docker-compose up -d && cd ..

# Wait 5 seconds for database to be ready
sleep 5

# Start API (in new terminal tab)
cd apps/api && npm run dev
```

---

### 2. Run Automated Tests (One Command)

**In another terminal:**

```bash
cd ~/Desktop/humanaios
./test-api.sh
```

**What you'll see:**
```
🚀 HumanAIOS API Test Suite
================================

📝 Step 1: Register Test User
✅ Authenticated! Token: eyJhbGciOiJIUzI1NiI...

📝 Step 2: Create MCP Agent
✅ Created Agent 1: 550e8400-e29b-41d4...

📝 Step 3: Create LangChain Agent
✅ Created Agent 2: 660e8400-e29b-41d4...

📝 Step 4: List All Agents
✅ Listed all agents

📝 Step 5: Log Tool Call Activity
✅ Logged tool call activity

📝 Step 6: Log LLM Request Activity
✅ Logged LLM request

📝 Step 7: Log Task Completion
✅ Logged task completion

📝 Step 8: Log Error Activity
✅ Logged error activity

📝 Step 9: Get Activities for Agent 1
✅ Retrieved agent activities

🎉 All Tests Completed!
```

---

### 3. Run Agent Simulator (One Command)

**Even cooler - simulate real agents:**

```bash
cd ~/Desktop/humanaios
npm run simulate
```

**What you'll see:**
```
╔════════════════════════════════════════════╗
║  HumanAIOS Agent Simulator v1.0            ║
║  The Operating System for Human-AI Workflows║
╚════════════════════════════════════════════╝

🚀 Starting Customer Support Agent Simulation

🔐 Authenticating...
✅ Logged in successfully

🤖 Registering agent: Customer Support Agent
✅ Agent registered with ID: 770e8400-e29b...

📞 Simulating customer inquiry...

🔧 Calling tool: search_knowledge_base
  ✓ Tool call logged (234ms)

🧠 Making LLM request...
  ✓ LLM request logged (892ms, 150 tokens, $0.0045)

✅ Completing task: Resolved password reset inquiry
  ✓ Task completion logged

📊 Retrieving activity log...
📋 Logged 3 activities

✅ Customer Support Agent simulation complete!
```

---

## 🎯 What Just Happened?

You just:
1. ✅ Started PostgreSQL database
2. ✅ Started HumanAIOS API server
3. ✅ Registered 2 AI agents
4. ✅ Logged 4 different types of activities
5. ✅ Retrieved agent data
6. ✅ Proved the system works end-to-end!

---

## 🌐 View in Browser

**Option 1: Database UI**
- Open: http://localhost:8080
- Login: postgres / postgres / humainos
- Browse tables: `agents`, `agent_activities`

**Option 2: API Health**
- Open: http://localhost:3001
- Should see: `{"message":"HumanAIOS API","version":"1.0.0"}`

---

## 📊 What to Show Potential Customers

**The Demo Flow:**

1. Show them the test script running ✅
2. Show the database with real data ✅
3. Explain: "This is how your AI agents will log activities" ✅
4. Show the cost tracking ($0.0045 per LLM request) ✅
5. Explain: "Soon you'll have a dashboard to visualize this" ✅

**The Value Prop:**

> "Every time your AI agent makes a decision, calls a tool, or spends money on LLMs - HumanAIOS tracks it. You get complete visibility, cost optimization, and the ability to route tasks to humans when needed."

---

## 🐛 Quick Troubleshooting

**Database won't start?**
```bash
docker ps  # Check if running
docker-compose logs  # Check errors
```

**API won't start?**
```bash
# Make sure you're in the right directory
cd ~/Desktop/humanaios/apps/api
npm install  # Install dependencies
npm run dev  # Try again
```

**Test script fails?**
```bash
# Make sure jq is installed
brew install jq

# Make script executable
chmod +x test-api.sh
```

---

## 🎉 Success!

If everything works, you have:
- ✅ Working authentication system
- ✅ Working agent registration
- ✅ Working activity logging
- ✅ Working database
- ✅ Complete test suite
- ✅ Agent simulator for demos

**You're 20% through the 30-day MVP!** 🚀

---

## 📅 Tomorrow (Day 3)

We'll build:
- MCP SDK package
- Better error handling
- Start on dashboard UI

**Current time:** 6:15pm  
**Remaining today:** Test on your Mac, celebrate wins!

**See you tomorrow at 4pm!** 💪
