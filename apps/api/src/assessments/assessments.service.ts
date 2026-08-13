/**
 * HumanAIOS Assessments Service
 * Orchestrates assessment submissions, job queuing, and result retrieval
 */

import { Injectable, Inject, Logger, BadRequestException, NotFoundException } from '@nestjs/common';
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
  private jobTimeouts: Map<string, NodeJS.Timeout> = new Map(); // Track timeouts for cleanup (in-memory, regenerated per restart)
  private readonly DEFAULT_TIMEOUT_MS = 30 * 60 * 1000; // 30 minutes

  constructor(
    private assessmentsRepository: AssessmentsRepository,
    private acatService: ACATService,
    @Inject('DATABASE_POOL') private pool: any
  ) {
    this.logger.log('AssessmentsService initialized');
    // Recover incomplete jobs on startup
    this.recoverJobsOnStartup().catch((e) => {
      this.logger.error(`Failed to recover jobs on startup: ${e.message}`, e.stack);
    });
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

      // Persist job to database
      await this.persistJobStatus(jobId, assessment.id, orgId, 'queued', 0, 0);

      // Trigger async job execution (fire and forget)
      this.triggerAsyncJobExecution(jobId, assessment.id, orgId, this.DEFAULT_TIMEOUT_MS);

      this.logger.log(`Assessment submitted: ${assessment.id} (job: ${jobId}, timeout: ${this.DEFAULT_TIMEOUT_MS}ms)`);

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
   * Get job status from database
   */
  async getJobStatus(assessmentId: string, orgId: string): Promise<JobStatus | null> {
    // Check if assessment exists
    const assessment = await this.assessmentsRepository.getAssessment(assessmentId, orgId);
    if (!assessment) {
      throw new NotFoundException(`Assessment not found: ${assessmentId}`);
    }

    // Query job from database
    const result = await this.pool.query(
      'SELECT job_id, status, progress_percent, current_phase, started_at, completed_at, error_message FROM assessment_jobs WHERE assessment_id = $1 LIMIT 1',
      [assessmentId]
    );

    if (result.rows.length > 0) {
      const row = result.rows[0];
      return {
        job_id: row.job_id,
        assessment_id: assessmentId,
        status: row.status,
        progress_percent: row.progress_percent,
        current_phase: row.current_phase,
        total_phases: 3,
        started_at: row.started_at,
        completed_at: row.completed_at,
        error_message: row.error_message,
      };
    }

    // If no job record and assessment is completed, return synthetic status
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
      await this.persistJobStatus(jobId, assessmentId, orgId, 'running', 10, 1);

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
      await this.persistJobStatus(jobId, assessmentId, orgId, 'running', 90, 3);

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
        await this.pool.query(
          'UPDATE assessments SET result_summary = $1, completed_at = NOW() WHERE id = $2',
          [JSON.stringify(resultSummary), assessmentId]
        );
      }

      // Update job status: completed
      await this.markJobCompleted(jobId, assessmentId, orgId);

      this.logger.log(`[${jobId}] Assessment completed successfully. LI=${resultSummary.learning_index?.toFixed(3) || 'N/A'}`);
    } catch (error) {
      this.logger.error(`[${jobId}] Assessment execution failed: ${error.message}`, error);

      // Update job status: failed
      await this.markJobFailed(jobId, assessmentId, orgId, error.message);

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

  /**
   * Trigger async job execution
   * Queues job to run asynchronously without blocking the API response
   */
  private triggerAsyncJobExecution(jobId: string, assessmentId: string, orgId: string, timeoutMs: number): void {
    // Queue job execution asynchronously
    setImmediate(async () => {
      try {
        // Set timeout for this job
        const timeoutHandle = setTimeout(() => {
          this.enforceJobTimeout(jobId, assessmentId);
        }, timeoutMs);

        this.jobTimeouts.set(jobId, timeoutHandle);

        // Execute the job
        await this.executeAssessmentJob(jobId, assessmentId, orgId);

        // Clear timeout if job completed before timeout
        this.clearJobTimeout(jobId);
      } catch (error) {
        this.logger.error(`Async job execution failed: ${error.message}`, error.stack);
        this.clearJobTimeout(jobId);
      }
    });
  }

  /**
   * Enforce job timeout
   * Called when a job exceeds its time limit
   */
  private enforceJobTimeout(jobId: string, assessmentId: string): void {
    this.logger.warn(`Job timeout enforced: ${jobId} (assessment: ${assessmentId})`);

    // Mark job as failed in database
    // Note: we don't have orgId here, but we can query it or use a generic update
    // For now, use a direct DB update since the job record should exist
    this.pool
      .query(
        "UPDATE assessment_jobs SET status = 'failed', error_message = $1, completed_at = NOW() WHERE job_id = $2",
        [`Assessment execution timeout after ${this.DEFAULT_TIMEOUT_MS / 1000}s`, jobId]
      )
      .catch((e: any) => {
        this.logger.error(`Failed to update job status on timeout: ${e.message}`);
      });

    // Update assessment status to failed
    this.assessmentsRepository
      .updateAssessmentStatus(assessmentId, 'failed')
      .catch((e: any) => {
        this.logger.error(`Failed to update assessment status on timeout: ${e.message}`);
      });

    this.clearJobTimeout(jobId);
  }

  /**
   * Clear timeout handle for a job
   */
  private clearJobTimeout(jobId: string): void {
    const timeoutHandle = this.jobTimeouts.get(jobId);
    if (timeoutHandle) {
      clearTimeout(timeoutHandle);
      this.jobTimeouts.delete(jobId);
    }
  }

  /**
   * Cleanup all timeouts on shutdown
   * Called during app teardown
   */
  cleanupAllTimeouts(): void {
    for (const [jobId, timeoutHandle] of this.jobTimeouts.entries()) {
      clearTimeout(timeoutHandle);
    }
    this.jobTimeouts.clear();
    this.logger.log('All job timeouts cleared');
  }

  /**
   * Persist job status to database
   */
  private async persistJobStatus(
    jobId: string,
    assessmentId: string,
    orgId: string,
    status: 'queued' | 'running' | 'completed' | 'failed',
    progressPercent: number,
    currentPhase: number,
    errorMessage?: string
  ): Promise<void> {
    try {
      const query = `
        INSERT INTO assessment_jobs
        (job_id, assessment_id, org_id, status, progress_percent, current_phase, error_message, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7, NOW(), NOW())
        ON CONFLICT (job_id) DO UPDATE SET
          status = $4,
          progress_percent = $5,
          current_phase = $6,
          error_message = $7,
          updated_at = NOW(),
          completed_at = CASE WHEN $4 IN ('completed', 'failed') THEN NOW() ELSE completed_at END
      `;

      await this.pool.query(query, [jobId, assessmentId, orgId, status, progressPercent, currentPhase, errorMessage || null]);
    } catch (error) {
      this.logger.error(`Failed to persist job status: ${error.message}`, error);
      throw error;
    }
  }

  /**
   * Recover incomplete jobs from database on app startup
   * Re-queues jobs that were running when app crashed
   */
  private async recoverJobsOnStartup(): Promise<void> {
    try {
      const result = await this.pool.query(
        "SELECT job_id, assessment_id, org_id FROM assessment_jobs WHERE status IN ('queued', 'running') ORDER BY created_at ASC"
      );

      const jobsToRecover = result.rows;
      if (jobsToRecover.length === 0) {
        this.logger.log('No incomplete jobs to recover');
        return;
      }

      this.logger.log(`Recovering ${jobsToRecover.length} incomplete jobs from database`);

      // Re-queue each incomplete job for execution
      for (const job of jobsToRecover) {
        this.triggerAsyncJobExecution(job.job_id, job.assessment_id, job.org_id, this.DEFAULT_TIMEOUT_MS);
        this.logger.debug(`Re-queued job for recovery: ${job.job_id}`);
      }

      this.logger.log(`Successfully recovered ${jobsToRecover.length} jobs`);
    } catch (error) {
      this.logger.error(`Failed to recover jobs on startup: ${error.message}`, error);
      throw error;
    }
  }

  /**
   * Update job status in database during execution
   * Called from executeAssessmentJob as work progresses
   */
  async updateJobProgress(jobId: string, assessmentId: string, orgId: string, progress: number, phase: number): Promise<void> {
    await this.persistJobStatus(jobId, assessmentId, orgId, 'running', progress, phase);
  }

  /**
   * Mark job as completed with results
   */
  async markJobCompleted(jobId: string, assessmentId: string, orgId: string): Promise<void> {
    await this.persistJobStatus(jobId, assessmentId, orgId, 'completed', 100, 3);
  }

  /**
   * Mark job as failed with error message
   */
  async markJobFailed(jobId: string, assessmentId: string, orgId: string, errorMessage: string): Promise<void> {
    await this.persistJobStatus(jobId, assessmentId, orgId, 'failed', 0, 0, errorMessage);
  }
}
