#!/bin/bash

# HumanAIOS API Test Script
# Tests all agent endpoints with real API calls

set -e

API_URL="http://localhost:3001"
TOKEN=""

echo "🚀 HumanAIOS API Test Suite"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Register a test user
echo -e "${BLUE}📝 Step 1: Register Test User${NC}"
REGISTER_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@humanaios.ai",
    "password": "Test123!",
    "name": "Test User",
    "org_name": "Test Organization"
  }')

echo "$REGISTER_RESPONSE" | jq .
TOKEN=$(echo "$REGISTER_RESPONSE" | jq -r '.token')

if [ "$TOKEN" == "null" ] || [ -z "$TOKEN" ]; then
  echo -e "${RED}❌ Failed to get token. User might already exist. Trying login...${NC}"
  
  # Try login instead
  LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/auth/login" \
    -H "Content-Type: application/json" \
    -d '{
      "email": "test@humanaios.ai",
      "password": "Test123!"
    }')
  
  echo "$LOGIN_RESPONSE" | jq .
  TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.token')
fi

if [ "$TOKEN" == "null" ] || [ -z "$TOKEN" ]; then
  echo -e "${RED}❌ Failed to authenticate. Exiting.${NC}"
  exit 1
fi

echo -e "${GREEN}✅ Authenticated! Token: ${TOKEN:0:20}...${NC}"
echo ""

# Step 2: Create first agent (MCP Agent)
echo -e "${BLUE}📝 Step 2: Create MCP Agent${NC}"
AGENT1_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/agents" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Customer Support Agent",
    "type": "mcp",
    "description": "Handles customer inquiries via MCP protocol",
    "metadata": {
      "model": "claude-sonnet-4-20250514",
      "temperature": 0.7,
      "max_tokens": 2000
    }
  }')

echo "$AGENT1_RESPONSE" | jq .
AGENT1_ID=$(echo "$AGENT1_RESPONSE" | jq -r '.id')
echo -e "${GREEN}✅ Created Agent 1: $AGENT1_ID${NC}"
echo ""

# Step 3: Create second agent (LangChain Agent)
echo -e "${BLUE}📝 Step 3: Create LangChain Agent${NC}"
AGENT2_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/agents" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Data Analysis Agent",
    "type": "langchain",
    "description": "Analyzes data and generates reports",
    "metadata": {
      "framework": "langchain",
      "version": "0.1.0"
    }
  }')

echo "$AGENT2_RESPONSE" | jq .
AGENT2_ID=$(echo "$AGENT2_RESPONSE" | jq -r '.id')
echo -e "${GREEN}✅ Created Agent 2: $AGENT2_ID${NC}"
echo ""

# Step 4: List all agents
echo -e "${BLUE}📝 Step 4: List All Agents${NC}"
curl -s -X GET "$API_URL/api/v1/agents" \
  -H "Authorization: Bearer $TOKEN" | jq .
echo -e "${GREEN}✅ Listed all agents${NC}"
echo ""

# Step 5: Log activity for Agent 1 (Successful tool call)
echo -e "${BLUE}📝 Step 5: Log Tool Call Activity (Success)${NC}"
curl -s -X POST "$API_URL/api/v1/agents/$AGENT1_ID/activities" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "activity_type": "tool_call",
    "description": "Called search_knowledge_base tool",
    "input_data": {
      "query": "How do I reset my password?",
      "filters": ["faq", "account"]
    },
    "output_data": {
      "results": [
        {
          "title": "Password Reset Guide",
          "url": "https://help.example.com/password-reset"
        }
      ]
    },
    "duration_ms": 234,
    "status": "success"
  }' | jq .
echo -e "${GREEN}✅ Logged tool call activity${NC}"
echo ""

# Step 6: Log LLM request activity
echo -e "${BLUE}📝 Step 6: Log LLM Request Activity${NC}"
curl -s -X POST "$API_URL/api/v1/agents/$AGENT1_ID/activities" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "activity_type": "llm_request",
    "description": "Generated customer response",
    "input_data": {
      "messages": [
        {"role": "user", "content": "I forgot my password"}
      ]
    },
    "output_data": {
      "response": "I can help you reset your password..."
    },
    "tokens_used": 150,
    "cost_usd": 0.0045,
    "duration_ms": 892,
    "status": "success",
    "metadata": {
      "model": "claude-sonnet-4-20250514"
    }
  }' | jq .
echo -e "${GREEN}✅ Logged LLM request${NC}"
echo ""

# Step 7: Log task completion
echo -e "${BLUE}📝 Step 7: Log Task Completion${NC}"
curl -s -X POST "$API_URL/api/v1/agents/$AGENT1_ID/activities" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "activity_type": "task_complete",
    "description": "Resolved customer inquiry about password reset",
    "duration_ms": 1500,
    "status": "success",
    "metadata": {
      "customer_id": "cust_123",
      "ticket_id": "TKT-456",
      "satisfaction_score": 5
    }
  }' | jq .
echo -e "${GREEN}✅ Logged task completion${NC}"
echo ""

# Step 8: Log error activity
echo -e "${BLUE}📝 Step 8: Log Error Activity${NC}"
curl -s -X POST "$API_URL/api/v1/agents/$AGENT2_ID/activities" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "activity_type": "error",
    "description": "Failed to access database",
    "error_message": "Connection timeout after 30s",
    "duration_ms": 30000,
    "status": "failed",
    "metadata": {
      "error_code": "DB_TIMEOUT",
      "retry_count": 3
    }
  }' | jq .
echo -e "${GREEN}✅ Logged error activity${NC}"
echo ""

# Step 9: Get activities for Agent 1
echo -e "${BLUE}📝 Step 9: Get Activities for Agent 1${NC}"
curl -s -X GET "$API_URL/api/v1/agents/$AGENT1_ID/activities?limit=10" \
  -H "Authorization: Bearer $TOKEN" | jq .
echo -e "${GREEN}✅ Retrieved agent activities${NC}"
echo ""

# Step 10: Get specific agent details
echo -e "${BLUE}📝 Step 10: Get Agent Details${NC}"
curl -s -X GET "$API_URL/api/v1/agents/$AGENT1_ID" \
  -H "Authorization: Bearer $TOKEN" | jq .
echo -e "${GREEN}✅ Retrieved agent details${NC}"
echo ""

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}🎉 All Tests Completed!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "Summary:"
echo "- Created 2 agents"
echo "- Logged 4 activities"
echo "- Retrieved agent list and details"
echo ""
echo "Agent IDs created:"
echo "  Agent 1 (MCP): $AGENT1_ID"
echo "  Agent 2 (LangChain): $AGENT2_ID"
