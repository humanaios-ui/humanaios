/**
 * Assessment Job Worker Service
 * Processes queued assessment jobs asynchronously
 * Polls active jobs and executes ACAT protocol
 */

import { Injectable, Logger, OnModuleInit, OnModuleDestroy } from '@nestjs/common';
import { AssessmentsService } from './assessments.service';
import { AssessmentsRepository } from './assessments.repository';

@Injectable()
export class AssessmentJobWorkerService implements OnModuleInit, OnModuleDestroy {
  private readonly logger = new Logger(AssessmentJobWorkerService.name);
  private workerInterval: NodeJS.Timer | null = null;
  private isRunning = false;
  private readonly POLL_INTERVAL_MS = 5000; // Poll every 5 seconds

  constructor(
    private assessmentsService: AssessmentsService,
    private assessmentsRepository: AssessmentsRepository
  ) {}

  /**
   * Start worker on module initialization
   */
  onModuleInit() {
    this.startWorker();
  }

  /**
   * Stop worker on module shutdown
   */
  onModuleDestroy() {
    this.stopWorker();
  }

  /**
   * Start the job worker polling loop
   */
  startWorker() {
    if (this.isRunning) {
      this.logger.warn('Worker already running');
      return;
    }

    this.isRunning = true;
    this.logger.log(`Assessment job worker started (polling every ${this.POLL_INTERVAL_MS}ms)`);

    // Start polling loop
    this.workerInterval = setInterval(() => this.processPendingJobs(), this.POLL_INTERVAL_MS);

    // Process immediately on startup
    this.processPendingJobs().catch((e) => {
      this.logger.error(`Error in initial job processing: ${e.message}`, e);
    });
  }

  /**
   * Stop the job worker
   */
  stopWorker() {
    if (this.workerInterval) {
      clearInterval(this.workerInterval);
      this.workerInterval = null;
    }

    this.isRunning = false;
    this.logger.log('Assessment job worker stopped');
  }

  /**
   * Process all pending jobs
   * Fetches assessments with 'pending' or 'queued' status and executes them
   */
  private async processPendingJobs(): Promise<void> {
    try {
      // Get all pending assessments across all orgs
      // Note: In production, would need per-org loop or a global queue table
      // For MVP, this is a simplified implementation

      // Placeholder: In real implementation, would fetch from a job queue table
      // For now, the job execution is triggered synchronously via executeAssessmentJob

      // Clean up old completed jobs
      await this.assessmentsService.cleanupCompletedJobs();
    } catch (error) {
      this.logger.error(`Error processing pending jobs: ${error.message}`, error);
    }
  }

  /**
   * Execute a specific assessment job (called by assessments service)
   * This is the wrapper that handles execution with retry logic
   */
  async executeWithRetry(jobId: string, assessmentId: string, orgId: string, maxRetries: number = 3): Promise<void> {
    let lastError: Error | null = null;

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        this.logger.debug(`[${jobId}] Execution attempt ${attempt}/${maxRetries}`);
        await this.assessmentsService.executeAssessmentJob(jobId, assessmentId, orgId);
        return; // Success
      } catch (error) {
        lastError = error;
        this.logger.warn(`[${jobId}] Attempt ${attempt} failed: ${error.message}`);

        // Exponential backoff between retries
        if (attempt < maxRetries) {
          const delayMs = Math.pow(2, attempt) * 1000; // 2s, 4s, 8s
          await new Promise((resolve) => setTimeout(resolve, delayMs));
        }
      }
    }

    // All retries exhausted
    throw new Error(`Job execution failed after ${maxRetries} attempts: ${lastError?.message}`);
  }

  /**
   * Health check for the worker
   */
  getHealthStatus(): {
    running: boolean;
    pollIntervalMs: number;
    lastPollTime?: Date;
  } {
    return {
      running: this.isRunning,
      pollIntervalMs: this.POLL_INTERVAL_MS,
    };
  }
}
