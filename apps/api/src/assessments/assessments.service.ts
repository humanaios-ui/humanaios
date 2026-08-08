/**
 * HumanAIOS Assessments Service
 * Orchestrates assessment submissions, job queuing, and result retrieval
 */

import { Injectable, Logger, BadRequestException, NotFoundException } from '@nestjs/common';
import { v4 as uuidv4 } from 'uuid';
import { AssessmentsRepository } from './assessments.repository';
import { ACATService } from '../acat/acat.service';
import { Assessment, CreateAssessmentDto, AssessmentStatus } from './assessment.entity';

export interface JobStatus {
  job_id: string;
  assessment_id: string;
  status: 'queued' | 'running' | 'completed' | 'failed';
  progress_percent: number;
  current_phase: number;
  total_phases: 3;
  started_at?: Date;
  completed_at?: Date;
  error_message?: string;
}

export interface AssessmentSubmitRequest {
  system_id: string;
  system_name: string;
  system_info: {
    endpoint?: string;
    model?: string;
    api_key?: string;
    provider?: string;
  };
  tier?: 'T1_STANDARD' | 'T2_IDENTITY_CHALLENGE';
}

@Injectable()
export class AssessmentsService {
  private readonly logger = new Logger(AssessmentsService.name);
  private activeJobs: Map<string, JobStatus> = new Map(); // In-memory for MVP; DB-backed in production

  constructor(
    private assessmentsRepository: AssessmentsRepository,
    private acatService: ACATService
  ) {
    this.logger.log('AssessmentsService initialized');
  }

  /**
   * Submit an AI system for ACAT assessment
   * Returns immediately with job_id; assessment runs asynchronously
   */
  async submitAssessment(orgId: string, request: AssessmentSubmitRequest): Promise<{ job_id: string; assessment_id: string; status_url: string }> {
    // Validate request
    if (!request.system_id || !request.system_name) {
      throw new BadRequestException('system_id and system_name are required');
    }

    if (!request.system_info?.endpoint && !request.system_info?.api_key) {
      throw new BadRequestException('Either endpoint or api_key must be provided');
    }

    try {
      // Create assessment record
      const dto: CreateAssessmentDto = {
        system_id: request.system_id,
        system_name: request.system_name,
        system_info: request.system_info,
      };

      const assessment = await this.assessmentsRepository.createAssessment(orgId, dto);
      const jobId = uuidv4();

      // Create job record
      const jobStatus: JobStatus = {
        job_id: jobId,
        assessment_id: assessment.id,
        status: 'queued',
        progress_percent: 0,
        current_phase: 0,
        total_phases: 3,
        started_at: undefined,
      };

      this.activeJobs.set(jobId, jobStatus);

      this.logger.log(`Assessment submitted: ${assessment.id} (job: ${jobId})`);

      return {
        job_id: jobId,
        assessment_id: assessment.id,
        status_url: `/api/v1/assessments/${assessment.id}`,
      };
    } catch (error) {
      this.logger.error(`Failed to submit assessment: ${error.message}`, error);
      throw error;
    }
  }

  /**
   * Get job status
   */
  async getJobStatus(assessmentId: string, orgId: string): Promise<JobStatus | null> {
    // Check if assessment exists
    const assessment = await this.assessmentsRepository.getAssessment(assessmentId, orgId);
    if (!assessment) {
      throw new NotFoundException(`Assessment not found: ${assessmentId}`);
    }

    // Find corresponding job (by assessment_id)
    for (const [jobId, status] of this.activeJobs.entries()) {
      if (status.assessment_id === assessmentId) {
        return status;
      }
    }

    // If no active job, return completed status if assessment is done
    if (assessment.status === 'completed') {
      return {
        job_id: 'unknown',
        assessment_id: assessmentId,
        status: 'completed',
        progress_percent: 100,
        current_phase: 3,
        total_phases: 3,
        completed_at: assessment.completed_at || new Date(),
      };
    }

    return null;
  }

  /**
   * Get assessment results (only after completion)
   */
  async getAssessmentResult(assessmentId: string, orgId: string): Promise<any> {
    const assessment = await this.assessmentsRepository.getAssessment(assessmentId, orgId);
    if (!assessment) {
      throw new NotFoundException(`Assessment not found: ${assessmentId}`);
    }

    if (assessment.status !== 'completed') {
      throw new BadRequestException(`Assessment not yet completed. Status: ${assessment.status}`);
    }

    // Parse result_summary if available
    if (assessment.result_summary) {
      try {
        return JSON.parse(assessment.result_summary);
      } catch (e) {
        return assessment.result_summary;
      }
    }

    return { status: 'completed', message: 'No results available' };
  }

  /**
   * List assessments by organization
   */
  async listAssessments(orgId: string, status?: AssessmentStatus, limit: number = 100, offset: number = 0): Promise<Assessment[]> {
    return this.assessmentsRepository.listAssessmentsByOrg(orgId, status, limit, offset);
  }

  /**
   * Execute assessment job (called by worker/processor)
   * This is the long-running operation that executes ACAT protocol
   */
  async executeAssessmentJob(jobId: string, assessmentId: string, orgId: string): Promise<void> {
    const job = this.activeJobs.get(jobId);
    if (!job) {
      throw new BadRequestException(`Job not found: ${jobId}`);
    }

    try {
      // Update job status: running
      job.status = 'running';
      job.started_at = new Date();
      job.progress_percent = 10;
      job.current_phase = 1;

      // Fetch assessment
      const assessment = await this.assessmentsRepository.getAssessment(assessmentId, orgId);
      if (!assessment) {
        throw new NotFoundException(`Assessment not found: ${assessmentId}`);
      }

      // Update assessment status to 'running'
      await this.assessmentsRepository.updateAssessmentStatus(assessmentId, 'running');

      // Execute ACAT protocol
      this.logger.log(`[${jobId}] Starting ACAT protocol execution for ${assessmentId}`);

      const protocolRun = await this.acatService.executeACATProtocol(assessment);

      // Update job progress
      job.progress_percent = 90;
      job.current_phase = 3;

      // Store results
      const resultSummary = {
        learning_index: protocolRun.learning_index?.learning_index || null,
        phase_1_mean: protocolRun.phase_1?.mean_score || null,
        phase_3_mean: protocolRun.phase_3?.mean_score || null,
        behavioral_flags: protocolRun.behavioral_flags || [],
        steps_completed: protocolRun.steps_completed?.length || 0,
        total_duration_ms: protocolRun.total_duration_ms || 0,
        reproducibility_hash: protocolRun.reproducibility_hash || null,
      };

      // Update assessment with results
      const completedAssessment = await this.assessmentsRepository.updateAssessmentStatus(assessmentId, 'completed');
      if (completedAssessment) {
        // Store result_summary as JSON
        const updateResult = await (this as any).pool?.query(
          'UPDATE assessments SET result_summary = $1, completed_at = NOW() WHERE id = $2',
          [JSON.stringify(resultSummary), assessmentId]
        );
      }

      // Update job status: completed
      job.status = 'completed';
      job.progress_percent = 100;
      job.completed_at = new Date();

      this.logger.log(`[${jobId}] Assessment completed successfully. LI=${resultSummary.learning_index?.toFixed(3) || 'N/A'}`);
    } catch (error) {
      this.logger.error(`[${jobId}] Assessment execution failed: ${error.message}`, error);

      // Update job status: failed
      job.status = 'failed';
      job.error_message = error.message;
      job.completed_at = new Date();

      // Update assessment status: failed
      try {
        await this.assessmentsRepository.updateAssessmentStatus(assessmentId, 'failed');
      } catch (e) {
        this.logger.error(`Failed to update assessment status to failed: ${e.message}`);
      }

      throw error;
    }
  }

  /**
   * Clean up completed jobs from in-memory store (optional)
   * In production, would archive to DB instead
   */
  async cleanupCompletedJobs(): Promise<void> {
    const now = Date.now();
    const expireAfterMs = 24 * 60 * 60 * 1000; // 24 hours

    for (const [jobId, status] of this.activeJobs.entries()) {
      if (status.status === 'completed' && status.completed_at) {
        const ageMs = now - status.completed_at.getTime();
        if (ageMs > expireAfterMs) {
          this.activeJobs.delete(jobId);
          this.logger.debug(`Cleaned up job: ${jobId}`);
        }
      }
    }
  }
}
