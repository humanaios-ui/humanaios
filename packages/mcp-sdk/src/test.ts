/**
 * Quick test of the HumanAIOS SDK
 * Run with: npx tsx test.ts
 */

import HumanAIOSClient from './index';

async function test() {
  console.log('🚀 Testing HumanAIOS SDK\n');

  const client = new HumanAIOSClient({
    baseUrl: 'http://localhost:3001/api/v1',
  });

  try {
    // Test 1: Create an agent
    console.log('📝 Test 1: Creating agent...');
    const agent = await client.createAgent({
      name: 'SDK Test Agent',
      type: 'test',
      description: 'Testing the SDK implementation',
    });
    console.log('✅ Agent created:', agent);
    console.log();

    // Test 2: Get all agents
    console.log('📋 Test 2: Getting all agents...');
    const agents = await client.getAgents();
    console.log('✅ Found', agents.length, 'agents');
    console.log();

    // Test 3: Get specific agent
    console.log('🔍 Test 3: Getting specific agent...');
    const fetchedAgent = await client.getAgent(agent.id);
    console.log('✅ Fetched agent:', fetchedAgent.name);
    console.log();

    // Test 4: Log activity
    console.log('📊 Test 4: Logging activity...');
    const activity = await client.logActivity(agent.id, {
      activity_type: 'test_execution',
      description: 'SDK test completed successfully',
      metadata: { test: 'successful', timestamp: new Date().toISOString() },
    });
    console.log('✅ Activity logged:', activity.id);
    console.log();

    // Test 5: Get activities
    console.log('📜 Test 5: Getting activities...');
    const activities = await client.getActivities(agent.id, { limit: 10 });
    console.log('✅ Found', activities.length, 'activities');
    console.log();

    console.log('🎉 All tests passed!\n');
  } catch (error: any) {
    console.error('❌ Test failed:', error?.message || error);
    if (error?.response) {
      console.error('Response:', error.response);
    }
    process.exit(1);
  }
}

test();
