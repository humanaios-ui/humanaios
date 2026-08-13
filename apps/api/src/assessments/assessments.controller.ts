/**
 * HumanAIOS Assessments Controller
 * HTTP API for assessment submission and status polling
 */

import { Controller, Post, Get, Body, Param, BadRequestException, NotFoundException, UseGuards, Req } from '@nestjs/common';
import { AssessmentsService, AssessmentSubmitRequest } from './assessments.service';

@Controller('api/v1/assessments')
export class AssessmentsController {
  constructor(private assessmentsService: AssessmentsService) {}

  /**
   * POST /api/v1/assessments
   * Submit an AI system for ACAT assessment
   *
   * Request body:
   * {
   *   "system_id": "chatgpt-4",
   *   "system_name": "ChatGPT-4",
   *   "system_info": {
   *     "endpoint": "https://api.openai.com/v1/chat/completions",
   *     "model": "gpt-4",
   *     "api_key": "sk-..."
   *   }
   * }
   *
   * Response:
   * {
   *   "job_id": "550e8400-e29b-41d4-a716-446655440000",
   *   "assessment_id": "550e8400-e29b-41d4-a716-446655440001",
   *   "status_url": "/api/v1/assessments/550e8400-e29b-41d4-a716-446655440001"
   * }
   */
  @Post()
  async submitAssessment(@Body() request: AssessmentSubmitRequest, @Req() req: any) {
    const orgId = req.user?.org_id ?? req.headers?.['x-org-id'];
    if (!orgId) {
      throw new BadRequestException('Missing org id (JWT user org_id or X-Org-ID header)');
    }
    return this.assessmentsService.submitAssessment(orgId, request);
  }

  /**
   * GET /api/v1/assessments/:id
   * Poll assessment status and progress
   *
   * Response:
   * {
   *   "job_id": "550e8400-e29b-41d4-a716-446655440000",
   *   "assessment_id": "550e8400-e29b-41d4-a716-446655440001",
   *   "status": "running",
   *   "progress_percent": 45,
   *   "current_phase": 2,
   *   "total_phases": 3,
   *   "started_at": "2026-08-08T10:00:00Z"
   * }
   */
  @Get(':id')
  async getAssessmentStatus(@Param('id') assessmentId: string, @Req() req: any) {
    const orgId = req.user?.org_id || 'default-org';
    const jobStatus = await this.assessmentsService.getJobStatus(assessmentId, orgId);

    if (!jobStatus) {
      throw new NotFoundException(`Assessment status not found: ${assessmentId}`);
    }

    return jobStatus;
  }

  /**
   * GET /api/v1/assessments/:id/result
   * Fetch assessment results (only available after completion)
   *
   * Response (on success):
   * {
   *   "learning_index": 0.847,
   *   "phase_1_mean": 940,
   *   "phase_3_mean": 796,
   *   "behavioral_flags": ["POLICY_COMPRESSION"],
   *   "steps_completed": 50,
   *   "total_duration_ms": 1250000,
   *   "reproducibility_hash": "abc123def456"
   * }
   */
  @Get(':id/result')
  async getAssessmentResult(@Param('id') assessmentId: string, @Req() req: any) {
    const orgId = req.user?.org_id || 'default-org';
    return this.assessmentsService.getAssessmentResult(assessmentId, orgId);
  }

  /**
   * GET /api/v1/assessments
   * List assessments for the organization
   *
   * Query params:
   * - status?: 'pending' | 'running' | 'completed' | 'failed'
   * - limit?: number (default 100)
   * - offset?: number (default 0)
   */
  @Get()
  async listAssessments(@Req() req: any) {
    const orgId = req.user?.org_id || 'default-org';
    const status = req.query.status;
    const limit = parseInt(req.query.limit) || 100;
    const offset = parseInt(req.query.offset) || 0;

    return this.assessmentsService.listAssessments(orgId, status, limit, offset);
  }
}
