# @humanaios/mcp-sdk

MCP SDK for HumanAIOS - Connect AI agents to human workers.

## Installation
```bash
npm install @humanaios/mcp-sdk
```

## Quick Start
```typescript
import HumanAIOSClient from '@humanaios/mcp-sdk';

const client = new HumanAIOSClient({
  apiKey: 'your-api-key'
});

// Create a task
const task = await client.createTask({
  agentId: 'my-agent-123',
  title: 'Pick up package from downtown',
  description: 'Collect package from USPS and deliver to office',
  skillsRequired: ['delivery', 'local-pickup'],
  estimatedDuration: 60, // minutes
  budget: 40 // USD
});

// Check status
const status = await client.getTask(task.id);
console.log('Task status:', status.status);
```

## Features

- ✅ Create tasks for AI agents
- ✅ Find and assign human workers  
- ✅ Track task progress
- ✅ Get results with evidence
- 🔄 MCP protocol integration (coming soon)
- 🔄 RentAHuman marketplace integration (coming soon)

## Status

**Version:** 0.1.0 (Early Development)  
**Created:** February 9, 2026  
**Next:** API integration, MCP server implementation

## License

MIT
