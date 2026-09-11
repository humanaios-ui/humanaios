import test from 'node:test';
import assert from 'node:assert/strict';

import { AuthController } from './auth/auth.controller';
import { AgentsController } from './agents/agents.controller';
import { AssessmentsController } from './assessments/assessments.controller';

test('AuthController delegates register, login, and verify to the canonical auth path', async () => {
  const authService = {
    registerCalls: [] as unknown[],
    loginCalls: [] as unknown[],
    async register(payload: unknown) {
      this.registerCalls.push(payload);
      return { access_token: 'token', user: payload };
    },
    async login(user: unknown) {
      this.loginCalls.push(user);
      return { access_token: 'token', user };
    },
  };

  const controller = new AuthController(authService as any);
  const createUserDto = { email: 'test@example.com', password: 'pw', name: 'Test', org_name: 'Test Org' };
  const user = { id: 'user-1', org_id: 'org-1', email: 'test@example.com', role: 'admin' };

  const registerResponse = await controller.register(createUserDto);
  const loginResponse = await controller.login({ user } as any, { email: 'test@example.com', password: 'pw' });
  const verifyResponse = await controller.verify({ user } as any);

  assert.equal(authService.registerCalls.length, 1);
  assert.deepEqual(authService.registerCalls[0], createUserDto);
  assert.equal(authService.loginCalls.length, 1);
  assert.deepEqual(authService.loginCalls[0], user);
  assert.equal(registerResponse.access_token, 'token');
  assert.deepEqual(loginResponse.user, user);
  assert.deepEqual(verifyResponse, { valid: true, user });
});

test('AgentsController uses authenticated org_id and delegates to the real service', async () => {
  const calls: Record<string, unknown[]> = {
    createAgent: [],
    findAllByOrg: [],
    findOne: [],
    createActivity: [],
    findActivities: [],
  };

  const agentsService = {
    async createAgent(orgId: string, dto: unknown) {
      calls.createAgent.push([orgId, dto]);
      return { id: 'agent-1', org_id: orgId };
    },
    async findAllByOrg(orgId: string) {
      calls.findAllByOrg.push([orgId]);
      return [{ id: 'agent-1', org_id: orgId }];
    },
    async findOne(agentId: string, orgId: string) {
      calls.findOne.push([agentId, orgId]);
      return { id: agentId, org_id: orgId };
    },
    async createActivity(agentId: string, orgId: string, dto: unknown) {
      calls.createActivity.push([agentId, orgId, dto]);
      return { id: 'activity-1', agent_id: agentId, org_id: orgId };
    },
    async findActivities(agentId: string, orgId: string, limit: number, offset: number) {
      calls.findActivities.push([agentId, orgId, limit, offset]);
      return [{ id: 'activity-1', agent_id: agentId, org_id: orgId }];
    },
  };

  const controller = new AgentsController(agentsService as any);
  const req = { user: { org_id: 'org-1' } };

  await controller.create(req as any, { name: 'Agent', type: 'mcp' });
  await controller.findAll(req as any);
  await controller.findOne(req as any, 'agent-1');
  await controller.createActivity(req as any, 'agent-1', {
    activity_type: 'tool_call',
    description: 'called a tool',
  });
  await controller.findActivities(req as any, 'agent-1', '25', '5');

  assert.deepEqual(calls.createAgent[0], ['org-1', { name: 'Agent', type: 'mcp' }]);
  assert.deepEqual(calls.findAllByOrg[0], ['org-1']);
  assert.deepEqual(calls.findOne[0], ['agent-1', 'org-1']);
  assert.deepEqual(calls.createActivity[0], [
    'agent-1',
    'org-1',
    { activity_type: 'tool_call', description: 'called a tool' },
  ]);
  assert.deepEqual(calls.findActivities[0], ['agent-1', 'org-1', 25, 5]);
});

test('AssessmentsController requires authenticated org_id and delegates when present', async () => {
  const calls: Record<string, unknown[]> = {
    submitAssessment: [],
    getJobStatus: [],
    getAssessmentResult: [],
    listAssessments: [],
  };

  const assessmentsService = {
    async submitAssessment(orgId: string, payload: unknown) {
      calls.submitAssessment.push([orgId, payload]);
      return { assessment_id: 'assessment-1' };
    },
    async getJobStatus(assessmentId: string, orgId: string) {
      calls.getJobStatus.push([assessmentId, orgId]);
      return { assessment_id: assessmentId, org_id: orgId, status: 'queued' };
    },
    async getAssessmentResult(assessmentId: string, orgId: string) {
      calls.getAssessmentResult.push([assessmentId, orgId]);
      return { assessment_id: assessmentId, org_id: orgId };
    },
    async listAssessments(orgId: string, status?: string, limit?: number, offset?: number) {
      calls.listAssessments.push([orgId, status, limit, offset]);
      return [];
    },
  };

  const controller = new AssessmentsController(assessmentsService as any);
  const req = { user: { org_id: 'org-1' }, query: { status: 'queued', limit: '25', offset: '5' } };
  const missingReq = { user: {}, query: {} };

  await controller.submitAssessment(
    { system_id: 'sys-1', system_name: 'System 1', system_info: { endpoint: 'https://example.com' } },
    req as any
  );
  await controller.getAssessmentStatus('assessment-1', req as any);
  await controller.getAssessmentResult('assessment-1', req as any);
  await controller.listAssessments(req as any);

  await assert.rejects(
    controller.submitAssessment(
      { system_id: 'sys-1', system_name: 'System 1', system_info: { endpoint: 'https://example.com' } },
      missingReq as any
    ),
    /Missing org_id/
  );

  assert.deepEqual(calls.submitAssessment[0], [
    'org-1',
    { system_id: 'sys-1', system_name: 'System 1', system_info: { endpoint: 'https://example.com' } },
  ]);
  assert.deepEqual(calls.getJobStatus[0], ['assessment-1', 'org-1']);
  assert.deepEqual(calls.getAssessmentResult[0], ['assessment-1', 'org-1']);
  assert.deepEqual(calls.listAssessments[0], ['org-1', 'queued', 25, 5]);
});
