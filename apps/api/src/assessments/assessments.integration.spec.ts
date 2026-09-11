import test from 'node:test';
import assert from 'node:assert/strict';
import { v4 as uuidv4 } from 'uuid';

import { AssessmentsService } from './assessments.service';
import { Assessment } from './assessment.entity';

function createHarness() {
  const mockRepository = {
    createAssessment: async (_orgId: string, _dto: any) => {
      throw new Error('createAssessment not mocked');
    },
    getAssessment: async (_assessmentId: string, _orgId: string) => {
      throw new Error('getAssessment not mocked');
    },
    updateAssessmentStatus: async (_assessmentId: string, _orgId: string, _status: string, _summary?: any) => {
      throw new Error('updateAssessmentStatus not mocked');
    },
    listAssessmentsByOrg: async (_orgId: string, _status?: string, _limit?: number, _offset?: number) => {
      return [];
    },
  };

  const mockACATService = {
    executeACATProtocol: async () => ({
      assessment_id: uuidv4(),
      learning_index: { learning_index: 0.847, per_dimension_li: {} },
      phase_1: { mean_score: 90, scores: {} },
      phase_3: { mean_score: 80, scores: {} },
      behavioral_flags: [],
      steps_completed: [],
      total_duration_ms: 1000,
    }),
  };

  const mockPool = {
    query: async (_sql: string, _params?: any[]) => ({ rows: [] }),
  };

  const service = new AssessmentsService(
    mockRepository as any,
    mockACATService as any,
    mockPool as any
  );

  // Keep tests deterministic and avoid background async execution side effects.
  (service as any).triggerAsyncJobExecution = () => {};
  (service as any).recoverJobsOnStartup = async () => {};

  return { service, mockRepository, mockACATService, mockPool };
}

test('submitAssessment returns job metadata and status URL', async () => {
  const { service, mockRepository } = createHarness();
  const orgId = 'test-org';
  const assessmentId = uuidv4();

  const assessment: Assessment = {
    id: assessmentId,
    org_id: orgId,
    system_id: 'gpt-4',
    system_name: 'GPT-4',
    system_info: { endpoint: 'https://api.openai.com/v1/chat/completions' },
    status: 'pending',
    created_at: new Date(),
    updated_at: new Date(),
  };

  mockRepository.createAssessment = async () => assessment;

  const result = await service.submitAssessment(orgId, {
    system_id: 'gpt-4',
    system_name: 'GPT-4',
    system_info: { endpoint: 'https://api.openai.com/v1/chat/completions' },
  });

  assert.ok(result.job_id);
  assert.equal(result.assessment_id, assessmentId);
  assert.equal(result.status_url, `/api/v1/assessments/${assessmentId}`);
});

test('submitAssessment rejects invalid payloads', async () => {
  const { service } = createHarness();

  await assert.rejects(
    service.submitAssessment('test-org', {
      system_id: '',
      system_name: 'GPT-4',
      system_info: { endpoint: 'https://example.com' },
    } as any),
    /system_id and system_name are required/
  );

  await assert.rejects(
    service.submitAssessment('test-org', {
      system_id: 'gpt-4',
      system_name: 'GPT-4',
      system_info: {},
    } as any),
    /Either endpoint or api_key must be provided/
  );
});

test('getJobStatus returns persisted job status from database', async () => {
  const { service, mockRepository, mockPool } = createHarness();
  const orgId = 'test-org';
  const assessmentId = uuidv4();

  const assessment: Assessment = {
    id: assessmentId,
    org_id: orgId,
    system_id: 'gpt-4',
    system_name: 'GPT-4',
    system_info: { endpoint: 'https://example.com' },
    status: 'running',
    created_at: new Date(),
    updated_at: new Date(),
  };

  mockRepository.getAssessment = async () => assessment;
  mockPool.query = async () => ({
    rows: [
      {
        job_id: 'job-1',
        status: 'running',
        progress_percent: 45,
        current_phase: 2,
        started_at: new Date(),
        completed_at: null,
        error_message: null,
      },
    ],
  });

  const status = await service.getJobStatus(assessmentId, orgId);
  assert.ok(status);
  assert.equal(status?.job_id, 'job-1');
  assert.equal(status?.status, 'running');
  assert.equal(status?.progress_percent, 45);
});

test('getAssessmentResult returns parsed completed result summary', async () => {
  const { service, mockRepository } = createHarness();
  const orgId = 'test-org';
  const assessmentId = uuidv4();

  mockRepository.getAssessment = async () => ({
    id: assessmentId,
    org_id: orgId,
    system_id: 'gpt-4',
    system_name: 'GPT-4',
    system_info: {},
    status: 'completed',
    result_summary: JSON.stringify({
      learning_index: 0.847,
      phase_1_mean: 940,
      phase_3_mean: 796,
    }),
    created_at: new Date(),
    updated_at: new Date(),
    completed_at: new Date(),
  });

  const result = await service.getAssessmentResult(assessmentId, orgId);
  assert.equal(result.learning_index, 0.847);
  assert.equal(result.phase_1_mean, 940);
});

test('listAssessments delegates to repository with filters', async () => {
  const { service, mockRepository } = createHarness();
  const calls: any[] = [];

  mockRepository.listAssessmentsByOrg = async (orgId: string, status?: string, limit?: number, offset?: number) => {
    calls.push([orgId, status, limit, offset]);
    return [];
  };

  await service.listAssessments('test-org', 'failed', 25, 5);

  assert.equal(calls.length, 1);
  assert.deepEqual(calls[0], ['test-org', 'failed', 25, 5]);
});
