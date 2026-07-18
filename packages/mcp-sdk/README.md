# @humanaios/mcp-sdk

**Official SDK for HumanAIOS** - Connect AI agents to human workers via Model Context Protocol.

[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)](https://www.typescriptlang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Alpha](https://img.shields.io/badge/Status-Alpha-orange)](https://github.com/humanaios/humanaios)

---

## 🚀 Quick Start

### Installation
```bash
npm install @humanaios/mcp-sdk
```

### Basic Usage
```typescript
import HumanAIOSClient from '@humanaios/mcp-sdk';

// Initialize client
const client = new HumanAIOSClient({
  apiKey: 'your-api-key',
  baseUrl: 'https://api.humanaios.com/v1'
});

// Create an AI agent
const agent = await client.createAgent({
  name: 'My Assistant',
  type: 'crewai',
  description: 'Customer support agent'
});

// Log activity
await client.logActivity(agent.id, {
  activity_type: 'task_completed',
  description: 'Processed 10 support tickets',
  metadata: { tickets: 10, avgTime: 3.5 }
});

// Get activities
const activities = await client.getActivities(agent.id, {
  limit: 100
});
```

---

## 🎯 Features

### Current (v0.1.0)
- ✅ **Agent Management** - Create and manage AI agents
- ✅ **Activity Logging** - Track agent activities
- ✅ **TypeScript Support** - Full type definitions
- ✅ **Error Handling** - Robust error management
- ✅ **Timeout Control** - Configurable request timeouts

### Coming Soon
- 🔄 **Human Task Creation** - Route tasks to human workers
- 🔄 **Worker Matching** - Find workers by skills/location
- 🔄 **Task Tracking** - Monitor task completion
- 🔄 **RentAHuman Integration** - 70K+ worker marketplace
- 🔄 **MCP Server** - Full Model Context Protocol support

---

## 📚 API Reference

### Constructor
```typescript
new HumanAIOSClient(config: HumanAIOSConfig)
```

**Config Options:**
- `apiKey?: string` - Your HumanAIOS API key
- `baseUrl?: string` - API base URL (default: http://localhost:3001/api/v1)
- `timeout?: number` - Request timeout in ms (default: 30000)

---

### Agent Methods

#### `createAgent()`
Create a new AI agent.
```typescript
await client.createAgent({
  name: string,
  type: string,
  description?: string
});
```

**Returns:** `Promise<Agent>`

---

#### `getAgents()`
Get all agents for the authenticated user.
```typescript
await client.getAgents();
```

**Returns:** `Promise<Agent[]>`

---

#### `getAgent(agentId)`
Get a specific agent by ID.
```typescript
await client.getAgent(agentId: string);
```

**Returns:** `Promise<Agent>`

---

### Activity Methods

#### `logActivity()`
Log an activity for an agent.
```typescript
await client.logActivity(agentId: string, {
  activity_type: string,
  description?: string,
  metadata?: any
});
```

**Returns:** `Promise<Activity>`

---

#### `getActivities()`
Get activities for an agent.
```typescript
await client.getActivities(agentId: string, {
  limit?: number,
  offset?: number
});
```

**Returns:** `Promise<Activity[]>`

---

### Human Task Methods (Coming Soon)

#### `createTask()`
Create a task requiring human assistance.
```typescript
await client.createTask({
  agentId: string,
  title: string,
  description: string,
  skillsRequired: string[],
  estimatedDuration?: number,
  budget?: number,
  location?: { lat: number, lng: number }
});
```

**Status:** Not yet implemented (RentAHuman integration pending)

---

## 🔧 Development

### Build
```bash
npm run build
```

### Test
```bash
npx tsx src/test.ts
```

### Watch Mode
```bash
npm run dev
```

---

## 📊 Error Handling

The SDK throws `APIError` for all API-related errors:
```typescript
import { APIError } from '@humanaios/mcp-sdk';

try {
  const agent = await client.createAgent({ name: 'Test' });
} catch (error) {
  if (error instanceof APIError) {
    console.error('API Error:', error.statusCode, error.message);
    console.error('Response:', error.response);
  }
}
```

**Error Properties:**
- `message: string` - Error description
- `statusCode: number` - HTTP status code (0 for network errors)
- `response?: any` - Original error response

---

## 🌟 Real-World Example
```typescript
import HumanAIOSClient from '@humanaios/mcp-sdk';

async function monitorAgent() {
  const client = new HumanAIOSClient({
    apiKey: process.env.HUMANAIOS_API_KEY
  });

  // Create agent
  const agent = await client.createAgent({
    name: 'Customer Support Bot',
    type: 'openai-assistant',
    description: 'Handles tier 1 support tickets'
  });

  console.log('Agent created:', agent.id);

  // Simulate activity logging
  setInterval(async () => {
    await client.logActivity(agent.id, {
      activity_type: 'ticket_processed',
      metadata: {
        ticketId: Math.random().toString(36),
        responseTime: Math.random() * 10
      }
    });
  }, 60000); // Every minute

  // Check recent activities
  const activities = await client.getActivities(agent.id, {
    limit: 10
  });

  console.log(`Processed ${activities.length} activities`);
}

monitorAgent().catch(console.error);
```

---

## 🔗 Related Projects

- **[HumanAIOS Platform](https://github.com/humanaios/humanaios)** - Main platform repository
- **[RentAHuman](https://rentahuman.ai)** - Human worker marketplace (integration coming)
- **[MCP SDK](https://github.com/modelcontextprotocol/sdk)** - Model Context Protocol

---

## 📄 License

MIT © HumanAIOS

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](../../CONTRIBUTING.md).

---

## 📞 Support

- **Documentation:** https://docs.humanaios.com
- **Issues:** https://github.com/humanaios/humanaios/issues
- **Email:** support@humanaios.com
- **Twitter:** [@HumanAIOS](https://twitter.com/HumanAIOS)

---

## 🗺️ Roadmap

**v0.2.0** (March 2026)
- RentAHuman integration
- Task creation and management
- Worker matching API

**v0.3.0** (April 2026)
- Full MCP server support
- Webhook notifications
- Advanced error recovery

**v1.0.0** (May 2026)
- Production-ready release
- Complete API coverage
- Performance optimizations

---

**Built with ❤️ for the future of human-AI collaboration**

*Where AI meets human dignity. Where automation meets purpose.*
