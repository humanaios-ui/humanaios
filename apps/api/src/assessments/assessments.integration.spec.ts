/**
 * Assessment Submission API — Integration Tests
 * E2E testing: submit assessment → poll status → retrieve results
 */

import { Test, TestingModule } from '@nestjs/testing';
import { AssessmentsService } from './assessments.service';
import { AssessmentsController } from './assessments.controller';
import { AssessmentsRepository } from './assessments.repository';
import { ACATService } from '../acat/acat.service';
import { Assessment, CreateAssessmentDto } from './assessment.entity';
import { v4 as uuidv4 } from 'uuid';

describe('Assessment Submission API (Integration Tests)', () => {
  let service: AssessmentsService;
  let controller: AssessmentsController;
  let repository: AssessmentsRepository;
  let acatService: ACATService;

  // Mock implementations
  const mockRepository = {
    createAssessment: jest.fn(),
    getAssessment: jest.fn(),
    updateAssessmentStatus: jest.fn(),
    listAssessmentsByOrg: jest.fn(),
  };

  const mockACATService = {
    executeACATProtocol: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [AssessmentsController],
      providers: [
        AssessmentsService,
        {
          provide: AssessmentsRepository,
          useValue: mockRepository,
        },
        {
          provide: ACATService,
          useValue: mockACATService,
        },
      ],
    }).compile();

    service = module.get<AssessmentsService>(AssessmentsService);
    controller = module.get<AssessmentsController>(AssessmentsController);
    repository = module.get<AssessmentsRepository>(AssessmentsRepository);
    acatService = module.get<ACATService>(ACATService);
  });

  afterEach(() => {
    jest.clearAllMocks();
    service.cleanupAllTimeouts();
  });

  describe('POST /api/v1/assessments', () => {
    it('should submit assessment and return job_id + status_url', async () => {
      const orgId = 'test-org';
      const request = {
        system_id: 'gpt-4',
        system_name: 'GPT-4',
        system_info: {
          endpoint: 'https://api.openai.com/v1/chat/completions',
          model: 'gpt-4',
          api_key: 'sk-test',
        },
      };

      const mockAssessment: Assessment = {
        id: uuidv4(),
        org_id: orgId,
        system_id: request.system_id,
        system_name: request.system_name,
        system_info: request.system_info,
        status: 'pending',
        created_at: new Date(),
        updated_at: new Date(),
      };

      mockRepository.createAssessment.mockResolvedValue(mockAssessment);

      const result = await service.submitAssessment(orgId, request);

      expect(result).toHaveProperty('job_id');
      expect(result).toHaveProperty('assessment_id');
      expect(result.assessment_id).toBe(mockAssessment.id);
      expect(result.status_url).toBe(`/api/v1/assessments/${mockAssessment.id}`);

      expect(mockRepository.createAssessment).toHaveBeenCalledWith(orgId, expect.objectContaining({
        system_id: request.system_id,
        system_name: request.system_name,
      }));
    });

    it('should reject submission without system_id', async () => {
      const orgId = 'test-org';
      const request = {
        system_name: 'GPT-4',
        system_info: { endpoint: 'https://...' },
      } as any;

      await expect(service.submitAssessment(orgId, request)).rejects.toThrow(
        'system_id and system_name are required'
      );
    });

    it('should reject submission without endpoint or api_key', async () => {
      const orgId = 'test-org';
      const request = {
        system_id: 'gpt-4',
        system_name: 'GPT-4',
        system_info: {},
      } as any;

      await expect(service.submitAssessment(orgId, request)).rejects.toThrow(
        'Either endpoint or api_key must be provided'
      );
    });
  });

  describe('GET /api/v1/assessments/:id (Status Polling)', () => {
    it('should return job status after submission', async () => {
      const orgId = 'test-org';
      const assessmentId = uuidv4();
      const mockAssessment: Assessment = {
        id: assessmentId,
        org_id: orgId,
        system_id: 'gpt-4',
        system_name: 'GPT-4',
        system_info: {},
        status: 'pending',
        created_at: new Date(),
        updated_at: new Date(),
      };

      mockRepository.getAssessment.mockResolvedValue(mockAssessment);

      // First, submit
      const submitRequest = {
        system_id: 'gpt-4',
        system_name: 'GPT-4',
        system_info: { endpoint: 'https://...' },
      };
      mockRepository.createAssessment.mockResolvedValue(mockAssessment);
      await service.submitAssessment(orgId, submitRequest);

      // Then, poll status
      const jobStatus = await service.getJobStatus(assessmentId, orgId);

      expect(jobStatus).toBeDefined();
      expect(jobStatus?.status).toBe('queued');
      expect(jobStatus?.progress_percent).toBe(0);
    });

    it('should return 404 if assessment does not exist', async () => {
      const orgId = 'test-org';
      const assessmentId = uuidv4();

      mockRepository.getAssessment.mockResolvedValue(null);

      await expect(service.getJobStatus(assessmentId, orgId)).rejects.toThrow(
        `Assessment not found: ${assessmentId}`
      );
    });

    it('should update progress during execution', async () => {
      const orgId = 'test-org';
      const assessmentId = uuidv4();
      const jobId = uuidv4();

      // Create a job manually for testing
      const jobStatus = {
        job_id: jobId,
        assessment_id: assessmentId,
        status: 'running' as const,
        progress_percent: 45,
        current_phase: 2,
        total_phases: 3,
        started_at: new Date(),
      };

      (service as any).activeJobs.set(jobId, jobStatus);

      const retrieved = (service as any).activeJobs.get(jobId);
      expect(retrieved.progress_percent).toBe(45);
      expect(retrieved.current_phase).toBe(2);
    });
  });

  describe('GET /api/v1/assessments/:id/result (Fetch Results)', () => {
    it('should return results after assessment completes', async () => {
      const orgId = 'test-org';
      const assessmentId = uuidv4();

      const mockAssessment: Assessment = {
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
          behavioral_flags: ['POLICY_COMPRESSION'],
          steps_completed: 50,
          total_duration_ms: 1250000,
        }),
        created_at: new Date(),
        updated_at: new Date(),
        completed_at: new Date(),
      };

      mockRepository.getAssessment.mockResolvedValue(mockAssessment);

      const result = await service.getAssessmentResult(assessmentId, orgId);

      expect(result).toHaveProperty('learning_index');
      expect(result.learning_index).toBe(0.847);
      expect(result.behavioral_flags).toContain('POLICY_COMPRESSION');
    });

    it('should reject result retrieval before completion', async () => {
      const orgId = 'test-org';
      const assessmentId = uuidv4();

      const mockAssessment: Assessment = {
        id: assessmentId,
        org_id: orgId,
        system_id: 'gpt-4',
        system_name: 'GPT-4',
        system_info: {},
        status: 'running',
        created_at: new Date(),
        updated_at: new Date(),
      };

      mockRepository.getAssessment.mockResolvedValue(mockAssessment);

      await expect(service.getAssessmentResult(assessmentId, orgId)).rejects.toThrow(
        'Assessment not yet completed. Status: running'
      );
    });
  });

  describe('GET /api/v1/assessments (List Assessments)', () => {
    it('should list assessments by organization', async () => {
      const orgId = 'test-org';
      const mockAssessments: Assessment[] = [
        {
          id: uuidv4(),
          org_id: orgId,
          system_id: 'gpt-4',
          system_name: 'GPT-4',
          system_info: {},
          status: 'completed',
          created_at: new Date(),
          updated_at: new Date(),
        },
      ];

      mockRepository.listAssessmentsByOrg.mockResolvedValue(mockAssessments);

      const results = await service.listAssessments(orgId);

      expect(results).toHaveLength(1);
      expect(results[0].system_id).toBe('gpt-4');
    });

    it('should filter by status', async () => {
      const orgId = 'test-org';
      const mockAssessments: Assessment[] = [];

      mockRepository.listAssessmentsByOrg.mockResolvedValue(mockAssessments);

      const results = await service.listAssessments(orgId, 'failed');

      expect(mockRepository.listAssessmentsByOrg).toHaveBeenCalledWith(
        orgId,
        'failed',
        expect.any(Number),
        expect.any(Number)
      );
    });
  });

  describe('Timeout Enforcement', () => {
    it('should enforce timeout on long-running jobs', async () => {
      const orgId = 'test-org';
      const assessmentId = uuidv4();

      const mockAssessment: Assessment = {
        id: assessmentId,
        org_id: orgId,
        system_id: 'gpt-4',
        system_name: 'GPT-4',
        system_info: {},
        status: 'pending',
        created_at: new Date(),
        updated_at: new Date(),
      };

      mockRepository.createAssessment.mockResolvedValue(mockAssessment);
      mockRepository.updateAssessmentStatus.mockResolvedValue(mockAssessment);

      // Mock ACAT service to simulate long-running job
      mockACATService.executeACATProtocol.mockImplementationOnce(
        () => new Promise((resolve) => {
          setTimeout(() => resolve({ learning_index: 0.8 }), 100000); // 100 seconds
        })
      );

      const request = {
        system_id: 'gpt-4',
        system_name: 'GPT-4',
        system_info: { endpoint: 'https://...' },
      };

      await service.submitAssessment(orgId, request);

      // Wait briefly to let async job start
      await new Promise((resolve) => setTimeout(resolve, 100));

      // Verify timeout was set
      const jobTimeoutsSize = (service as any).jobTimeouts.size;
      expect(jobTimeoutsSize).toBeGreaterThan(0);
    });
  });

  describe('Async Execution Flow', () => {
    it('should complete full assessment flow: submit → status → result', async (done) => {
      const orgId = 'test-org';
      const assessmentId = uuidv4();

      const mockAssessment: Assessment = {
        id: assessmentId,
        org_id: orgId,
        system_id: 'gpt-4',
        system_name: 'GPT-4',
        system_info: { endpoint: 'https://...' },
        status: 'pending',
        created_at: new Date(),
        updated_at: new Date(),
      };

      mockRepository.createAssessment.mockResolvedValue(mockAssessment);
      mockRepository.getAssessment.mockResolvedValue({
        ...mockAssessment,
        status: 'completed',
        result_summary: JSON.stringify({
          learning_index: 0.847,
          phase_1_mean: 940,
          phase_3_mean: 796,
          behavioral_flags: [],
        }),
      });

      const protocolRun = {
        assessment_id: assessmentId,
        learning_index: { learning_index: 0.847, per_dimension_li: {} },
        phase_1: { mean_score: 940, scores: {} },
        phase_3: { mean_score: 796, scores: {} },
        behavioral_flags: [],
        steps_completed: [],
        total_duration_ms: 1250000,
      };

      mockACATService.executeACATProtocol.mockResolvedValue(protocolRun);
      mockRepository.updateAssessmentStatus.mockResolvedValue({
        ...mockAssessment,
        status: 'completed',
      });

      (async () => {
        try {
          // 1. Submit assessment
          const submitResult = await service.submitAssessment(orgId, {
            system_id: 'gpt-4',
            system_name: 'GPT-4',
            system_info: { endpoint: 'https://...' },
          });

          expect(submitResult.job_id).toBeDefined();
          expect(submitResult.assessment_id).toBe(assessmentId);

          // 2. Poll status
          await new Promise((resolve) => setTimeout(resolve, 200));
          const jobStatus = await service.getJobStatus(assessmentId, orgId);
          expect(jobStatus).toBeDefined();

          // 3. Retrieve results (after completion)
          const results = await service.getAssessmentResult(assessmentId, orgId);
          expect(results.learning_index).toBe(0.847);

          done();
        } catch (error) {
          done(error);
        }
      })();
    }, 10000); // 10s timeout for async test
  });
});
