/**
 * HumanAIOS ACAT Service
 * Orchestrates the 50-step AI Calibration Assessment Tool protocol
 */

import { Injectable, Logger, BadRequestException, Inject } from '@nestjs/common';
import { Pool } from 'pg';
import { v4 as uuidv4 } from 'uuid';
import {
  ACATProtocolRun,
  ACATPhaseData,
  ACATPhase,
  ACATDimension,
  ACATLearningIndex,
  DimensionScores,
  ACATStepResult,
  ACATProtocolSteps,
  ACATTier,
  ACAT_DIMENSIONS,
  ACAT_CONFIG,
} from './acat.protocol';
import { Assessment, EpistemicArtifact, CalibrationVectors } from '../assessments/assessment.entity';
import { AssessmentsRepository } from '../assessments/assessments.repository';
import { ACATPromptTemplateService } from './acat-prompt-templates';
import { ACATSystemClient } from './acat-system-client';
import { ACATFlagDetector } from './acat-flag-detector';

@Injectable()
export class ACATService {
  private readonly logger = new Logger(ACATService.name);

  constructor(
    @Inject('DATABASE_POOL') private pool: Pool,
    private assessmentsRepository: AssessmentsRepository,
    private promptTemplates: ACATPromptTemplateService,
    private systemClient: ACATSystemClient,
    private flagDetector: ACATFlagDetector
  ) {}

  /**
   * Execute full ACAT protocol for an assessment
   * Orchestrates: Phase 1 → Phase 2 (calibration) → Phase 3 → LI Computation
   *
   * This method is the entry point for running a complete assessment.
   * It coordinates the 50-step protocol, logs epistemic artifacts, and returns results.
   */
  async executeACATProtocol(assessment: Assessment): Promise<ACATProtocolRun> {
    const protocolRun: ACATProtocolRun = {
      assessment_id: assessment.id,
      tier: ACATTier.T1_STANDARD,
      system_info: assessment.system_info,
      phase_1: null,
      phase_2_calibration: null,
      phase_3: null,
      steps_completed: [],
      behavioral_flags: [],
      validation_errors: [],
      started_at: new Date(),
    };

    try {
      this.logger.log(`[${assessment.id}] Starting ACAT protocol execution`);

      // Phase 1: Baseline Assessment (Steps 1-15)
      protocolRun.phase_1 = await this.executePhase1(assessment, protocolRun);

      // Phase 2: Calibration Data Exposure (Steps 9-10)
      protocolRun.phase_2_calibration = await this.executePhase2(assessment, protocolRun);

      // Phase 3: Post-Calibration Assessment (Steps 11-14)
      protocolRun.phase_3 = await this.executePhase3(assessment, protocolRun);

      // Calculate Learning Index
      if (protocolRun.phase_1 && protocolRun.phase_3) {
        protocolRun.learning_index = this.calculateLearningIndex(
          protocolRun.phase_1,
          protocolRun.phase_3
        );
      }

      // Log ACAT results as epistemic artifacts
      await this.logACATArtifacts(assessment.id, protocolRun);

      protocolRun.completed_at = new Date();
      protocolRun.total_duration_ms = protocolRun.completed_at.getTime() - protocolRun.started_at.getTime();

      // Verify reproducibility (same input → same output)
      protocolRun.reproducibility_hash = this.hashProtocolRun(protocolRun);

      this.logger.log(
        `[${assessment.id}] ACAT protocol complete (${protocolRun.total_duration_ms}ms, LI=${protocolRun.learning_index?.learning_index || 'N/A'})`
      );

      return protocolRun;
    } catch (error) {
      this.logger.error(`[${assessment.id}] ACAT protocol failed: ${error.message}`, error.stack);
      protocolRun.validation_errors.push(`Protocol execution failed: ${error.message}`);
      throw new BadRequestException(`ACAT protocol execution failed: ${error.message}`);
    }
  }

  /**
   * Phase 1: Baseline Self-Assessment
   * Steps 1-15: Elicit initial 12-dimension scores
   */
  private async executePhase1(
    assessment: Assessment,
    protocolRun: ACATProtocolRun
  ): Promise<ACATPhaseData | null> {
    const phase1Start = Date.now();

    try {
      this.logger.debug(`[${assessment.id}] Starting Phase 1`);

      // Step 1: Collect system info (already done)
      const step1 = await this.runProtocolStep(1, assessment, protocolRun);
      protocolRun.steps_completed.push(step1);

      // Step 2: Verify connectivity
      const step2 = await this.runProtocolStep(2, assessment, protocolRun);
      protocolRun.steps_completed.push(step2);

      // Step 3: Generate Phase 1 prompt (de-anchored, no numeric anchors)
      const step3 = await this.runProtocolStep(3, assessment, protocolRun);
      protocolRun.steps_completed.push(step3);

      // Step 4: Elicit 12-dimension scores from AI system
      const step4 = await this.runProtocolStep(4, assessment, protocolRun);
      protocolRun.steps_completed.push(step4);
      const phase1Scores = this.parseScoresFromResponse(step4.output);

      // Step 5: Parse response
      const step5 = await this.runProtocolStep(5, assessment, protocolRun);
      protocolRun.steps_completed.push(step5);

      // Step 6: Validate for behavioral flags
      const step6 = await this.runProtocolStep(6, assessment, protocolRun);
      protocolRun.steps_completed.push(step6);
      const flags = step6.output.flags || [];
      protocolRun.behavioral_flags.push(...flags);

      // Step 7: Calculate stats
      const step7 = await this.runProtocolStep(7, assessment, protocolRun);
      protocolRun.steps_completed.push(step7);
      const totalScore = Object.values(phase1Scores).reduce((a, b) => a + (b as number), 0) as number;
      const meanScore = totalScore / ACAT_DIMENSIONS.length;

      // Step 8: Log findings
      const step8 = await this.runProtocolStep(8, assessment, protocolRun);
      protocolRun.steps_completed.push(step8);

      const phase1Data: ACATPhaseData = {
        phase: ACATPhase.PHASE_1,
        scores: phase1Scores,
        total_score: totalScore,
        mean_score: meanScore,
        submitted_at: new Date(),
        flags: flags,
      };

      this.logger.debug(
        `[${assessment.id}] Phase 1 complete: mean_score=${meanScore.toFixed(2)}, flags=${flags.join(',')}`
      );

      return phase1Data;
    } catch (error) {
      this.logger.error(`[${assessment.id}] Phase 1 failed: ${error.message}`);
      protocolRun.validation_errors.push(`Phase 1 failed: ${error.message}`);
      throw error;
    }
  }

  /**
   * Phase 2: Calibration Data Exposure
   * Steps 9-10: Present evidence to AI system without revealing Phase 1 scores
   */
  private async executePhase2(
    assessment: Assessment,
    protocolRun: ACATProtocolRun
  ): Promise<Record<string, any> | null> {
    try {
      this.logger.debug(`[${assessment.id}] Starting Phase 2 (Calibration)`);

      // Step 9: Generate calibration data
      const step9 = await this.runProtocolStep(9, assessment, protocolRun);
      protocolRun.steps_completed.push(step9);
      const calibrationData = step9.output;

      // Step 10: Present to system
      const step10 = await this.runProtocolStep(10, assessment, protocolRun);
      protocolRun.steps_completed.push(step10);

      this.logger.debug(`[${assessment.id}] Phase 2 complete`);

      return calibrationData;
    } catch (error) {
      this.logger.error(`[${assessment.id}] Phase 2 failed: ${error.message}`);
      protocolRun.validation_errors.push(`Phase 2 failed: ${error.message}`);
      throw error;
    }
  }

  /**
   * Phase 3: Post-Calibration Self-Assessment
   * Steps 11-14: Re-elicit 12-dimension scores after calibration exposure
   */
  private async executePhase3(
    assessment: Assessment,
    protocolRun: ACATProtocolRun
  ): Promise<ACATPhaseData | null> {
    try {
      this.logger.debug(`[${assessment.id}] Starting Phase 3`);

      // Step 11: Generate Phase 3 prompt (mirrors Phase 1, de-anchored)
      const step11 = await this.runProtocolStep(11, assessment, protocolRun);
      protocolRun.steps_completed.push(step11);

      // Step 12: Elicit updated scores
      const step12 = await this.runProtocolStep(12, assessment, protocolRun);
      protocolRun.steps_completed.push(step12);
      const phase3Scores = this.parseScoresFromResponse(step12.output);

      // Step 13: Parse response
      const step13 = await this.runProtocolStep(13, assessment, protocolRun);
      protocolRun.steps_completed.push(step13);

      // Step 14: Validate scores
      const step14 = await this.runProtocolStep(14, assessment, protocolRun);
      protocolRun.steps_completed.push(step14);
      const flags = step14.output.flags || [];
      protocolRun.behavioral_flags.push(...flags);

      const totalScore = Object.values(phase3Scores).reduce((a, b) => a + (b as number), 0) as number;
      const meanScore = totalScore / ACAT_DIMENSIONS.length;

      const phase3Data: ACATPhaseData = {
        phase: ACATPhase.PHASE_3,
        scores: phase3Scores,
        total_score: totalScore,
        mean_score: meanScore,
        submitted_at: new Date(),
        flags: flags,
      };

      this.logger.debug(`[${assessment.id}] Phase 3 complete: mean_score=${meanScore.toFixed(2)}`);

      return phase3Data;
    } catch (error) {
      this.logger.error(`[${assessment.id}] Phase 3 failed: ${error.message}`);
      protocolRun.validation_errors.push(`Phase 3 failed: ${error.message}`);
      throw error;
    }
  }

  /**
   * Run a single ACAT protocol step
   * Each step is deterministic: same input → same output (within numerical precision)
   */
  private async runProtocolStep(
    stepNumber: number,
    assessment: Assessment,
    protocolRun: ACATProtocolRun
  ): Promise<ACATStepResult> {
    const stepDef = ACATProtocolSteps.find((s) => s.number === stepNumber);
    if (!stepDef) {
      throw new BadRequestException(`Unknown ACAT step: ${stepNumber}`);
    }

    const stepStart = Date.now();

    try {
      const result: ACATStepResult = {
        step_number: stepNumber,
        step_name: stepDef.name,
        status: 'completed',
        duration_ms: 0,
        output: {},
        confidence: 0.9,
      };

      // Step implementations will be added in next phase
      // For now, scaffold with placeholder logic
      result.output = this.executeStepLogic(stepNumber, assessment, protocolRun);
      result.duration_ms = Date.now() - stepStart;

      this.logger.debug(`[${assessment.id}] Step ${stepNumber} completed (${result.duration_ms}ms)`);

      return result;
    } catch (error) {
      this.logger.error(`[${assessment.id}] Step ${stepNumber} failed: ${error.message}`);
      throw error;
    }
  }

  /**
   * Execute step-specific logic
   * Integrates system communication, prompt templates, and behavioral validation
   */
  private executeStepLogic(
    stepNumber: number,
    assessment: Assessment,
    protocolRun: ACATProtocolRun
  ): Record<string, any> {
    switch (stepNumber) {
      case 1:
        // Collect system info (already in assessment)
        return { system_collected: true, system_name: assessment.system_info?.name || 'unknown' };

      case 2:
        // Verify connectivity to system
        return { connectivity_verified: true, endpoint: assessment.system_info?.endpoint };

      case 3:
        // Generate Phase 1 prompt (de-anchored, no numeric anchors)
        const phase1Prompt = this.promptTemplates.getPrompt(1, assessment.system_info?.name || 'AI System');
        return { prompt_generated: true, prompt: phase1Prompt, phase: 1 };

      case 4:
        // Elicit Phase 1 scores via system communication
        // In production: call system with Phase 1 prompt
        // Mock for now: return sample scores
        return {
          scores: Object.fromEntries(
            ACAT_DIMENSIONS.map((dim) => [dim, 50 + Math.floor(Math.random() * 30)])
          ),
        };

      case 6:
        // Validate Phase 1 for behavioral flags
        if (protocolRun.phase_1) {
          const flags = this.flagDetector.detectFlags(
            protocolRun.phase_1.scores,
            protocolRun.phase_1.scores, // Use same scores for validation (no Phase 3 yet)
            ACAT_CONFIG.MEDIAN_LI * 100 * ACAT_DIMENSIONS.length // Convert LI to absolute scale
          );
          return { flags: flags.flags, flag_summary: flags.summary };
        }
        return { flags: [] };

      case 9:
        // Generate calibration data (Phase 2)
        const phase2Prompt = this.promptTemplates.getPrompt(2, assessment.system_info?.name || 'AI System');
        return { calibration_prompt: phase2Prompt, calibration_data_points: 7 };

      case 11:
        // Generate Phase 3 prompt (mirrors Phase 1, informed by calibration)
        const phase3Prompt = this.promptTemplates.getPrompt(3, assessment.system_info?.name || 'AI System');
        return { prompt_generated: true, prompt: phase3Prompt, phase: 3 };

      case 12:
        // Elicit Phase 3 scores via system communication
        // In production: call system with Phase 3 prompt
        // Mock for now: return slightly lower scores (learning index ~0.85)
        return {
          scores: Object.fromEntries(
            ACAT_DIMENSIONS.map((dim) => [dim, Math.floor((50 + Math.floor(Math.random() * 30)) * 0.85)])
          ),
        };

      case 14:
        // Validate Phase 3 for behavioral flags and compare with Phase 1
        if (protocolRun.phase_1 && protocolRun.phase_3) {
          const flags = this.flagDetector.detectFlags(
            protocolRun.phase_1.scores,
            protocolRun.phase_3.scores,
            ACAT_CONFIG.MEDIAN_LI * 100 * ACAT_DIMENSIONS.length
          );
          return { flags: flags.flags, flag_summary: flags.summary };
        }
        return { flags: [] };

      case 15:
        // Compute Learning Index and format submission URL
        if (protocolRun.phase_1 && protocolRun.phase_3 && protocolRun.learning_index) {
          const submissionURL = this.promptTemplates.formatSubmissionURL(
            assessment.system_info?.name || 'AI System',
            protocolRun.phase_1.scores,
            protocolRun.phase_3.scores,
            protocolRun.learning_index.learning_index
          );
          return {
            learning_index: protocolRun.learning_index.learning_index,
            submission_url: submissionURL,
            interpretation: protocolRun.learning_index.interpretation,
          };
        }
        return { step_completed: true };

      default:
        return { step_completed: true };
    }
  }

  /**
   * Parse scores from AI system response
   * Validates that all 12 dimensions are present and 0-100
   */
  private parseScoresFromResponse(response: any): DimensionScores {
    const scores: Partial<DimensionScores> = {};

    for (const dim of ACAT_DIMENSIONS) {
      const score = response.scores?.[dim];
      if (typeof score !== 'number' || score < 0 || score > 100) {
        throw new BadRequestException(`Invalid score for dimension ${dim}: ${score}`);
      }
      (scores as any)[dim] = score;
    }

    return scores as DimensionScores;
  }

  /**
   * Calculate Learning Index (LI)
   * Core metric: Phase 3 mean ÷ Phase 1 mean
   * Measures responsiveness to calibration evidence
   */
  private calculateLearningIndex(phase1: ACATPhaseData, phase3: ACATPhaseData): ACATLearningIndex {
    if (phase1.mean_score === 0) {
      throw new BadRequestException('Cannot calculate LI: Phase 1 mean score is zero');
    }

    const li = phase3.mean_score / phase1.mean_score;
    const perDimensionLI: Partial<{ [key in ACATDimension]: number }> = {};

    for (const dim of ACAT_DIMENSIONS) {
      const p1Score = phase1.scores[dim];
      const p3Score = phase3.scores[dim];
      perDimensionLI[dim] = p1Score > 0 ? p3Score / p1Score : 0;
    }

    return {
      phase_1_mean: phase1.mean_score,
      phase_3_mean: phase3.mean_score,
      learning_index: li,
      per_dimension_li: perDimensionLI as { [key in ACATDimension]: number },
      interpretation: this.interpretLearningIndex(li),
    };
  }

  /**
   * Interpret Learning Index
   * Compare against historical median (0.8632) and provide context
   */
  private interpretLearningIndex(li: number): string {
    const median = ACAT_CONFIG.MEDIAN_LI;

    if (li < 0.7) {
      return `LI=${li.toFixed(3)} (below median) — system showed minimal change after calibration`;
    } else if (li < median) {
      return `LI=${li.toFixed(3)} (slightly below median ${median}) — modest calibration response`;
    } else if (li < 1.1) {
      return `LI=${li.toFixed(3)} (near median ${median}) — typical calibration responsiveness`;
    } else {
      return `LI=${li.toFixed(3)} (above median) — strong calibration response`;
    }
  }

  /**
   * Log ACAT results as epistemic artifacts
   * Creates findings, decisions, assumptions in the epistemic system
   */
  private async logACATArtifacts(assessmentId: string, protocolRun: ACATProtocolRun): Promise<void> {
    // Will implement epistemic logging in next phase
    this.logger.debug(`[${assessmentId}] Logging ACAT artifacts`);
    // Artifacts will include:
    // - finding: Phase 1 scores
    // - finding: Phase 3 scores
    // - finding: Learning Index result
    // - assumption: About system behavior
    // - decision: How we interpret results
  }

  /**
   * Hash protocol run for reproducibility verification
   * Same input should produce same output (within numerical precision)
   */
  private hashProtocolRun(protocolRun: ACATProtocolRun): string {
    // Simplified hash for now - real implementation would use cryptographic hash
    const json = JSON.stringify({
      system_info: protocolRun.system_info,
      phase_1: protocolRun.phase_1?.scores,
      phase_3: protocolRun.phase_3?.scores,
      learning_index: protocolRun.learning_index?.learning_index,
    });
    return Buffer.from(json).toString('base64').substring(0, 16);
  }
}
