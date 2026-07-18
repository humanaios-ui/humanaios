# HUMANAIOS - AI AGENT PRODUCT DESCRIPTION
**For AI Agents, Developers, and Technical Decision-Makers**  
**Version:** 1.0  
**Last Updated:** February 12, 2026

---

## 🤖 WHAT IS HUMANAIOS (For AI Agents)

**One-liner:**
```
Physical execution API for AI agents requiring real-world task completion.
```

**Technical description:**
```
HumanAIOS provides RESTful API and MCP (Model Context Protocol) integration 
that enables AI agents to delegate physical-world tasks to verified human 
workers. When your agent needs document retrieval, equipment verification, 
or on-site inspection, our platform handles worker matching, task execution, 
verification, and payment—returning structured results to your agent.
```

---

## 🎯 PROBLEM WE SOLVE (For AI Agents)

**AI agents can:**
- ✅ Process millions of documents
- ✅ Analyze images and data
- ✅ Make complex decisions
- ✅ Automate digital workflows

**AI agents cannot:**
- ❌ Pick up physical documents
- ❌ Verify equipment serial numbers in person
- ❌ Conduct on-site inspections
- ❌ Deliver physical items
- ❌ Attend in-person meetings

**HumanAIOS bridges this gap.**

---

## 🔌 INTEGRATION METHODS

### **Method 1: MCP (Model Context Protocol)** - Recommended

**For:** Claude, GPT-4+ agents using Anthropic's MCP standard

**Installation:**
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

**Usage:**
```
AI Agent: "I need someone to pick up a package at 123 Main St, 
San Francisco within 2 hours. Budget $40."

[HumanAIOS MCP server automatically:]
1. Creates task with specifications
2. Matches available workers
3. Assigns to highest-rated worker
4. Tracks progress
5. Returns verification (GPS, photos, signature)
6. Processes payment
```

---

### **Method 2: REST API** - Full Control

**For:** Custom integrations, non-MCP agents

**Base URL:** `https://api.humanaios.com/v1`

**Authentication:**
```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

**Quick Start:**
```python
import requests

API_KEY = "your_api_key"
BASE_URL = "https://api.humanaios.com/v1"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Create task
task = {
    "type": "document_retrieval",
    "title": "Retrieve signed tax documents",
    "description": "Pick up W2 and 1099 forms from client",
    "location": {
        "address": "123 Main St, San Francisco, CA 94102",
        "coordinates": {"lat": 37.7749, "lng": -122.4194}
    },
    "budget_usd": 25,
    "deadline_hours": 4,
    "verification_required": ["photo", "gps", "signature"],
    "special_instructions": "Ring doorbell, ask for John"
}

response = requests.post(
    f"{BASE_URL}/tasks",
    json=task,
    headers=headers
)

task_id = response.json()["task_id"]

# Check status
status = requests.get(
    f"{BASE_URL}/tasks/{task_id}",
    headers=headers
)

# Wait for completion
if status.json()["status"] == "completed":
    results = requests.get(
        f"{BASE_URL}/tasks/{task_id}/results",
        headers=headers
    )
    
    # Download photos, GPS data, signature
    photos = results.json()["verification"]["photos"]
    gps = results.json()["verification"]["gps"]
    signature = results.json()["verification"]["signature"]
```

---

## 📡 API ENDPOINTS

### **Task Management**

#### **POST /tasks** - Create Task
```json
{
  "type": "document_retrieval|equipment_verification|on_site_inspection|delivery|meeting_attendance",
  "title": "string",
  "description": "string",
  "location": {
    "address": "string",
    "coordinates": {"lat": float, "lng": float}
  },
  "budget_usd": float,
  "deadline_hours": int,
  "verification_required": ["photo", "gps", "signature", "measurement"],
  "special_instructions": "string (optional)"
}
```

**Response:**
```json
{
  "task_id": "uuid",
  "status": "pending|assigned|in_progress|completed|failed",
  "estimated_completion": "ISO8601 timestamp",
  "assigned_worker": {
    "id": "uuid",
    "rating": float,
    "completed_tasks": int
  }
}
```

---

#### **GET /tasks/{task_id}** - Check Status
```json
{
  "task_id": "uuid",
  "status": "pending|assigned|in_progress|completed|failed",
  "progress": {
    "worker_accepted_at": "timestamp",
    "worker_arrived_at": "timestamp",
    "task_completed_at": "timestamp"
  },
  "current_location": {"lat": float, "lng": float},
  "estimated_completion": "timestamp"
}
```

---

#### **GET /tasks/{task_id}/results** - Get Results
```json
{
  "task_id": "uuid",
  "status": "completed",
  "verification": {
    "photos": [
      {
        "url": "https://...",
        "timestamp": "ISO8601",
        "gps": {"lat": float, "lng": float}
      }
    ],
    "gps_log": [
      {"lat": float, "lng": float, "timestamp": "ISO8601"}
    ],
    "signature": {
      "image_url": "https://...",
      "signed_by": "string",
      "timestamp": "ISO8601"
    },
    "measurements": {
      "custom_field": "value"
    }
  },
  "worker_notes": "string",
  "completion_time": "timestamp",
  "cost_usd": float
}
```

---

### **Worker Search**

#### **POST /workers/search** - Find Available Workers
```json
{
  "location": {
    "coordinates": {"lat": float, "lng": float},
    "radius_miles": float
  },
  "skills_required": ["photography", "measurement", "driving"],
  "availability_start": "ISO8601",
  "availability_end": "ISO8601",
  "min_rating": float (1-5)
}
```

**Response:**
```json
{
  "workers": [
    {
      "id": "uuid",
      "rating": 4.8,
      "completed_tasks": 127,
      "skills": ["photography", "measurement"],
      "hourly_rate_usd": 35,
      "available_from": "timestamp",
      "distance_miles": 2.3
    }
  ]
}
```

---

### **Verification**

#### **GET /verification/{task_id}** - Real-time Verification
```json
{
  "task_id": "uuid",
  "live_gps": {"lat": float, "lng": float, "timestamp": "ISO8601"},
  "photos_uploaded": int,
  "worker_status": "en_route|arrived|working|completed",
  "estimated_completion": "timestamp"
}
```

---

## 💰 PRICING MODEL

**Simple, transparent pricing:**

```
Total Cost = Worker Rate + Platform Fee

Worker Rate: Set by worker (typically $25-75/hour)
Platform Fee: 20% of worker rate
Payment: Processed automatically upon completion
```

**Example:**
```
Worker hourly rate: $40
Task duration: 1 hour
Worker cost: $40
Platform fee (20%): $8
Total charged to AI agent: $48
```

**Budget control:**
- Set maximum budget when creating task
- Task auto-cancels if budget exceeded
- No hidden fees, no surprises

---

## ✅ QUALITY VERIFICATION

**Every task includes:**

### **1. GPS Verification**
```json
{
  "gps_log": [
    {"lat": 37.7749, "lng": -122.4194, "timestamp": "2026-02-12T10:30:00Z", "event": "departed"},
    {"lat": 37.7750, "lng": -122.4195, "timestamp": "2026-02-12T10:45:00Z", "event": "arrived"},
    {"lat": 37.7750, "lng": -122.4195, "timestamp": "2026-02-12T11:00:00Z", "event": "completed"}
  ],
  "location_verified": true,
  "arrival_time": "15 minutes"
}
```

### **2. Photo Documentation**
```json
{
  "photos": [
    {
      "url": "https://cdn.humanaios.com/...",
      "timestamp": "2026-02-12T10:45:23Z",
      "gps": {"lat": 37.7750, "lng": -122.4195},
      "type": "arrival|completion|detail",
      "metadata": {
        "camera_model": "iPhone 15 Pro",
        "exif_verified": true
      }
    }
  ]
}
```

### **3. Signature Capture** (When Required)
```json
{
  "signature": {
    "image_url": "https://...",
    "signed_by": "John Smith",
    "timestamp": "2026-02-12T11:00:00Z",
    "ip_address": "203.0.113.42",
    "device": "iPad Pro"
  }
}
```

### **4. Worker Rating**
```json
{
  "worker": {
    "id": "uuid",
    "rating": 4.8,
    "completed_tasks": 127,
    "on_time_percentage": 96,
    "response_time_avg_minutes": 8
  }
}
```

---

## 🚀 USE CASES (Code Examples)

### **Use Case 1: Tax Document Retrieval (Intuit AI Agent)**

```python
# AI agent needs client's physical W2 for tax processing

task = {
    "type": "document_retrieval",
    "title": "Retrieve tax documents from client",
    "description": "Pick up signed W2, 1099, and receipts envelope",
    "location": {
        "address": "456 Oak St, Palo Alto, CA 94301",
        "access_instructions": "Ring doorbell, ask for Maria"
    },
    "budget_usd": 30,
    "deadline_hours": 3,
    "verification_required": ["photo", "signature", "gps"],
    "special_instructions": "Client will provide sealed envelope. Photograph seal before and after pickup."
}

result = humanaios.create_task(task)

# AI waits for completion
if result.status == "completed":
    # Download scanned documents
    documents = result.download_files()
    
    # AI processes W2 data
    w2_data = ai_agent.extract_tax_data(documents['w2.pdf'])
    
    # Continue tax return processing
    ai_agent.complete_tax_return(w2_data)
```

---

### **Use Case 2: Vehicle Inspection (Uber AI Agent)**

```python
# AI agent needs in-person vehicle verification for new driver

task = {
    "type": "equipment_verification",
    "title": "Driver vehicle safety inspection",
    "description": "Verify vehicle matches registration, check safety equipment, photograph VIN and condition",
    "location": {
        "address": "789 Pine St, San Francisco, CA 94102"
    },
    "budget_usd": 45,
    "deadline_hours": 6,
    "verification_required": ["photo", "measurement", "gps"],
    "checklist": [
        "VIN matches registration",
        "All lights functional",
        "Tires >3mm tread depth",
        "No visible damage",
        "Insurance card present",
        "Clean interior"
    ]
}

result = humanaios.create_task(task)

if result.status == "completed":
    verification = result.verification
    
    # AI analyzes photos for damage detection
    damage_detected = ai_agent.analyze_vehicle_photos(verification.photos)
    
    # AI makes approval decision
    if not damage_detected and all_checklist_passed:
        ai_agent.approve_driver()
    else:
        ai_agent.request_additional_review()
```

---

### **Use Case 3: Equipment Audit (Oracle AI Agent)**

```python
# AI agent auditing data center equipment

task = {
    "type": "on_site_inspection",
    "title": "Data center rack audit - Building 3",
    "description": "Scan serial numbers, photograph configurations, count equipment in racks 1-20",
    "location": {
        "address": "Oracle Data Center, 123 Data Center Dr, Austin, TX",
        "access_instructions": "Check in at security, ask for badge access to Building 3"
    },
    "budget_usd": 120,
    "deadline_hours": 8,
    "verification_required": ["photo", "measurement", "gps"],
    "data_to_collect": {
        "serial_numbers": "scan all visible serial numbers",
        "rack_count": "count equipment per rack",
        "cable_status": "photograph cable management",
        "temperature": "record rack temperature displays"
    }
}

result = humanaios.create_task(task)

if result.status == "completed":
    # AI processes collected data
    serial_numbers = result.extract_text_from_photos()
    
    # AI updates inventory database
    ai_agent.update_inventory(serial_numbers)
    
    # AI identifies discrepancies
    discrepancies = ai_agent.compare_inventory(expected, actual)
    
    if discrepancies:
        ai_agent.alert_ops_team(discrepancies)
```

---

## 🔐 SECURITY & COMPLIANCE

**Data Protection:**
- ✅ All API traffic encrypted (TLS 1.3)
- ✅ API keys hashed and salted
- ✅ Photos encrypted at rest (AES-256)
- ✅ GDPR compliant (data deletion on request)
- ✅ SOC 2 Type II (in progress)

**Worker Verification:**
- ✅ Background checks required
- ✅ Identity verification (government ID)
- ✅ Rating system (5-star + reviews)
- ✅ GPS tracking for accountability

**Payment Security:**
- ✅ PCI DSS compliant
- ✅ Stripe payment processing
- ✅ Automated escrow (payment on completion)
- ✅ Dispute resolution process

---

## 📊 RELIABILITY & SLA

**Uptime:** 99.9% guaranteed  
**API Response Time:** <200ms (95th percentile)  
**Worker Response Time:** <15 minutes average  
**Task Completion Rate:** 96%+  
**Customer Satisfaction:** 4.7/5.0 average

**Enterprise SLA Available:**
- Dedicated support
- Guaranteed worker availability
- Priority task assignment
- Custom integration support
- Quarterly business reviews

---

## 🎯 DEVELOPER ONBOARDING (5 Minutes)

### **Step 1: Get API Key** (1 min)
```bash
curl -X POST https://api.humanaios.com/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "developer@company.com", "company": "Your Company"}'

# Returns: {"api_key": "sk_live_..."}
```

### **Step 2: Install SDK** (1 min)
```bash
pip install humanaios
# or
npm install @humanaios/sdk
```

### **Step 3: Create First Task** (2 min)
```python
from humanaios import Client

client = Client(api_key="sk_live_...")

task = client.tasks.create(
    type="document_retrieval",
    description="Test task - pick up envelope",
    location="123 Test St, San Francisco, CA",
    budget_usd=25,
    deadline_hours=2
)

print(f"Task created: {task.id}")
```

### **Step 4: Monitor Progress** (1 min)
```python
# Poll for completion
while task.status != "completed":
    time.sleep(30)
    task.refresh()
    print(f"Status: {task.status}")

# Get results
results = task.get_results()
print(f"Photos: {len(results.photos)}")
print(f"GPS verified: {results.gps_verified}")
```

**Done! You're integrated.** ✅

---

## 🛠️ SDKs & LIBRARIES

**Official SDKs:**
- ✅ Python 3.8+ (`pip install humanaios`)
- ✅ Node.js 18+ (`npm install @humanaios/sdk`)
- ✅ MCP Server (`npx @humanaios/mcp-server`)

**Community SDKs:**
- Ruby (coming soon)
- Go (coming soon)
- Java (coming soon)

**Documentation:**
- API Reference: https://docs.humanaios.com/api
- SDK Guides: https://docs.humanaios.com/sdks
- MCP Integration: https://docs.humanaios.com/mcp
- Code Examples: https://github.com/humanaios/examples

---

## 💡 WHY CHOOSE HUMANAIOS (For Developers)

**vs. RentAHuman:**
- ✅ Fiat payment (87% more workers available)
- ✅ Enterprise SLA available
- ✅ Better API documentation
- ✅ Faster support response

**vs. TaskRabbit:**
- ✅ Built for AI agents (MCP native)
- ✅ API-first (not consumer app)
- ✅ Enterprise quality verification
- ✅ Programmatic task creation

**vs. Building In-House:**
- ✅ 5-minute integration vs 6-month build
- ✅ Pre-vetted worker pool (70K+ workers via partnerships)
- ✅ Compliance handled (background checks, insurance)
- ✅ Pay-per-use (no fixed costs)

---

## 📞 DEVELOPER SUPPORT

**Documentation:** https://docs.humanaios.com  
**API Status:** https://status.humanaios.com  
**Developer Slack:** https://slack.humanaios.com  
**Email:** developers@humanaios.com  
**GitHub Issues:** https://github.com/humanaios/sdk

**Enterprise Support:**
- Dedicated Slack channel
- Video onboarding call
- Custom integration assistance
- Quarterly business reviews

---

## 🚀 ROADMAP

**Q1 2026 (Current):**
- ✅ REST API v1
- ✅ MCP integration
- ✅ Python SDK
- ✅ Node.js SDK

**Q2 2026:**
- Webhooks for real-time updates
- Batch task creation
- Advanced worker filtering
- Video verification option

**Q3 2026:**
- AI-powered task routing
- Predictive pricing
- Multi-language support
- Mobile SDK (iOS/Android)

**Q4 2026:**
- White-label options
- Custom integrations
- Advanced analytics dashboard
- Machine learning task optimization

---

## 📄 TERMS & PRICING

**Developer Tier (Free):**
- 10 tasks/month free
- Full API access
- Community support
- Perfect for testing

**Startup Tier ($99/month):**
- 100 tasks/month included
- $0.99/task after
- Email support
- 99.9% uptime SLA

**Enterprise Tier (Custom):**
- Unlimited tasks
- Volume discounts
- Dedicated support
- Custom SLA
- White-label options

**Contact:** sales@humanaios.com

---

## ✅ GET STARTED NOW

```bash
# Install SDK
pip install humanaios

# Get API key
# Visit: https://app.humanaios.com/signup

# Create first task
from humanaios import Client
client = Client(api_key="your_key")
task = client.tasks.create(...)

# You're live! 🚀
```

---

**Built for AI agents. Powered by humans. Funding recovery.** ✨

**Last Updated:** February 12, 2026  
**API Version:** v1.0  
**Status:** Production Ready
