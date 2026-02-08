/**
 * HumanAIOS - The Operating System for Human-AI Workflows
 * Copyright (c) 2026 HumanAIOS
 * All rights reserved.
 * 
 * Agent Simulator
 * Simulates a working AI agent making requests to HumanAIOS API
 */

import fetch from 'node-fetch';

const API_URL = process.env.API_URL || 'http://localhost:3001';

interface AgentConfig {
  name: string;
  type: 'mcp' | 'langchain' | 'crewai' | 'custom';
  description: string;
  email: string;
  password: string;
}

class AgentSimulator {
  private token: string = '';
  private agentId: string = '';
  private config: AgentConfig;

  constructor(config: AgentConfig) {
    this.config = config;
  }

  // Step 1: Register/Login
  async authenticate() {
    console.log('🔐 Authenticating...');
    
    // Try to register
    try {
      const registerResponse = await fetch(`${API_URL}/api/v1/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: this.config.email,
          password: this.config.password,
          name: this.config.name,
          org_name: `${this.config.name} Organization`
        })
      });

      const registerData: any = await registerResponse.json();
      
      if (registerData.token) {
        this.token = registerData.token;
        console.log('✅ Registered successfully');
        return;
      }
    } catch (error) {
      // Registration failed, try login
    }

    // Try to login
    const loginResponse = await fetch(`${API_URL}/api/v1/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: this.config.email,
        password: this.config.password
      })
    });

    const loginData: any = await loginResponse.json();
    this.token = loginData.token;
    console.log('✅ Logged in successfully');
  }

  // Step 2: Register agent with HumanAIOS
  async registerAgent() {
    console.log(`🤖 Registering agent: ${this.config.name}`);
    
    const response = await fetch(`${API_URL}/api/v1/agents`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`
      },
      body: JSON.stringify({
        name: this.config.name,
        type: this.config.type,
        description: this.config.description,
        metadata: {
          simulator: true,
          version: '1.0.0',
          created_by: 'agent-simulator'
        }
      })
    });

    const data: any = await response.json();
    this.agentId = data.id;
    console.log(`✅ Agent registered with ID: ${this.agentId}`);
  }

  // Step 3: Simulate tool call
  async simulateToolCall(toolName: string, input: any, output: any) {
    console.log(`🔧 Calling tool: ${toolName}`);
    
    const startTime = Date.now();
    
    // Simulate some processing time
    await this.sleep(100 + Math.random() * 300);
    
    const duration = Date.now() - startTime;

    await fetch(`${API_URL}/api/v1/agents/${this.agentId}/activities`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`
      },
      body: JSON.stringify({
        activity_type: 'tool_call',
        description: `Called ${toolName} tool`,
        input_data: input,
        output_data: output,
        duration_ms: duration,
        status: 'success'
      })
    });

    console.log(`  ✓ Tool call logged (${duration}ms)`);
  }

  // Step 4: Simulate LLM request
  async simulateLLMRequest(prompt: string, response: string) {
    console.log('🧠 Making LLM request...');
    
    const startTime = Date.now();
    
    // Simulate LLM processing time
    await this.sleep(500 + Math.random() * 1000);
    
    const duration = Date.now() - startTime;
    const tokens = Math.floor(prompt.length / 4 + response.length / 4);
    const cost = tokens * 0.00003; // Rough cost estimate

    await fetch(`${API_URL}/api/v1/agents/${this.agentId}/activities`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`
      },
      body: JSON.stringify({
        activity_type: 'llm_request',
        description: 'Generated response using Claude',
        input_data: { prompt },
        output_data: { response },
        tokens_used: tokens,
        cost_usd: cost,
        duration_ms: duration,
        status: 'success',
        metadata: {
          model: 'claude-sonnet-4-20250514'
        }
      })
    });

    console.log(`  ✓ LLM request logged (${duration}ms, ${tokens} tokens, $${cost.toFixed(4)})`);
  }

  // Step 5: Simulate task completion
  async completeTask(taskDescription: string, success: boolean = true) {
    console.log(`✅ Completing task: ${taskDescription}`);
    
    await fetch(`${API_URL}/api/v1/agents/${this.agentId}/activities`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`
      },
      body: JSON.stringify({
        activity_type: 'task_complete',
        description: taskDescription,
        status: success ? 'success' : 'failed',
        metadata: {
          timestamp: new Date().toISOString()
        }
      })
    });

    console.log('  ✓ Task completion logged');
  }

  // Step 6: Simulate error
  async simulateError(errorMessage: string) {
    console.log(`❌ Error occurred: ${errorMessage}`);
    
    await fetch(`${API_URL}/api/v1/agents/${this.agentId}/activities`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`
      },
      body: JSON.stringify({
        activity_type: 'error',
        description: 'Agent encountered an error',
        error_message: errorMessage,
        status: 'failed',
        metadata: {
          timestamp: new Date().toISOString()
        }
      })
    });

    console.log('  ✓ Error logged');
  }

  // Get agent activities
  async getActivities(limit: number = 10) {
    const response = await fetch(
      `${API_URL}/api/v1/agents/${this.agentId}/activities?limit=${limit}`,
      {
        headers: {
          'Authorization': `Bearer ${this.token}`
        }
      }
    );

    const activities = await response.json();
    return activities;
  }

  private sleep(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Example Usage: Customer Support Agent
async function runCustomerSupportAgent() {
  console.log('🚀 Starting Customer Support Agent Simulation\n');

  const agent = new AgentSimulator({
    name: 'Customer Support Agent',
    type: 'mcp',
    description: 'Handles customer inquiries via MCP protocol',
    email: 'support-agent@humanaios.ai',
    password: 'Agent123!'
  });

  // Initialize
  await agent.authenticate();
  await agent.registerAgent();
  
  console.log('\n📞 Simulating customer inquiry...\n');

  // Simulate handling a customer inquiry
  await agent.simulateToolCall(
    'search_knowledge_base',
    { query: 'How do I reset my password?' },
    { 
      results: [
        { title: 'Password Reset Guide', url: 'https://help.example.com/reset' }
      ]
    }
  );

  await agent.simulateLLMRequest(
    'Customer asked: How do I reset my password?',
    'I can help you reset your password. You can click on "Forgot Password" on the login page...'
  );

  await agent.completeTask('Resolved password reset inquiry', true);

  console.log('\n📊 Retrieving activity log...\n');
  const activities = await agent.getActivities(10);
  console.log(`📋 Logged ${activities.length} activities\n`);

  console.log('✅ Customer Support Agent simulation complete!\n');
}

// Example Usage: Data Analysis Agent
async function runDataAnalysisAgent() {
  console.log('🚀 Starting Data Analysis Agent Simulation\n');

  const agent = new AgentSimulator({
    name: 'Data Analysis Agent',
    type: 'langchain',
    description: 'Analyzes data and generates reports',
    email: 'data-agent@humanaios.ai',
    password: 'Agent123!'
  });

  await agent.authenticate();
  await agent.registerAgent();

  console.log('\n📊 Simulating data analysis task...\n');

  await agent.simulateToolCall(
    'fetch_sales_data',
    { start_date: '2026-01-01', end_date: '2026-01-31' },
    { records: 1250, total_revenue: 125000 }
  );

  await agent.simulateLLMRequest(
    'Analyze this sales data and provide insights',
    'Sales in January 2026 show a 15% increase compared to last month...'
  );

  await agent.completeTask('Generated monthly sales report', true);

  // Simulate an error
  await agent.simulateError('Failed to connect to database server');

  console.log('\n✅ Data Analysis Agent simulation complete!\n');
}

// Run both simulations
async function main() {
  console.log('╔════════════════════════════════════════════╗');
  console.log('║  HumanAIOS Agent Simulator v1.0            ║');
  console.log('║  The Operating System for Human-AI Workflows ║');
  console.log('╚════════════════════════════════════════════╝\n');

  try {
    await runCustomerSupportAgent();
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    await runDataAnalysisAgent();
    
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('🎉 All simulations completed successfully!');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  } catch (error) {
    console.error('❌ Simulation failed:', error);
    process.exit(1);
  }
}

// Run if executed directly
if (require.main === module) {
  main();
}

export { AgentSimulator };
