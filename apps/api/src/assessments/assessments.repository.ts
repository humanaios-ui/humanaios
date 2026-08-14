/**
 * HumanAIOS Assessments Repository
 * Data access layer for assessment submissions and results
 */

import { Injectable, Inject, Logger, BadRequestException } from '@nestjs/common';
import { Pool, QueryResult } from 'pg';
import { v4 as uuidv4 } from 'uuid';
import {
  Assessment,
  AssessmentStatus,
  CreateAssessmentDto,
  ACATProtocolRun,
  EpistemicArtifact,
  EpistemicEdge,
  CreateFindingDto,
  CreateDecisionDto,
  CreateAssumptionDto,
  ArtifactReference,
} from './assessment.entity';

@Injectable()
export class AssessmentsRepository {
  private readonly logger = new Logger(AssessmentsRepository.name);

  constructor(@Inject('DATABASE_POOL') private pool: Pool) {}

  // ============================================
  // ASSESSMENT OPERATIONS
  // ============================================

  async createAssessment(orgId: string, dto: CreateAssessmentDto): Promise<Assessment> {
    const id = uuidv4();
    const now = new Date();

    const query = `
      INSERT INTO assessments (
        id, org_id, system_id, system_name, system_info,
        status, created_at, updated_at
      )
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
      RETURNING *
    `;

    const values = [
      id,
      orgId,
      dto.system_id,
      dto.system_name,
      JSON.stringify(dto.system_info),
      'pending',
      now,
      now,
    ];

    try {
      const result = await this.pool.query(query, values);
      return this.mapAssessment(result.rows[0]);
    } catch (error) {
      this.logger.error(`Failed to create assessment: ${error.message}`, error);
      throw new BadRequestException(`Failed to create assessment: ${error.message}`);
    }
  }

  async getAssessment(assessmentId: string, orgId: string): Promise<Assessment | null> {
    const query = `
      SELECT * FROM assessments
      WHERE id = $1 AND org_id = $2
    `;

    const result = await this.pool.query(query, [assessmentId, orgId]);
    return result.rows.length > 0 ? this.mapAssessment(result.rows[0]) : null;
  }

  async listAssessmentsByOrg(
    orgId: string,
    status?: AssessmentStatus,
    limit: number = 100,
    offset: number = 0
  ): Promise<Assessment[]> {
    let query = `
      SELECT * FROM assessments
      WHERE org_id = $1
    `;
    const params: any[] = [orgId];

    if (status) {
      params.push(status);
      query += ` AND status = $${params.length}`;
    }

    query += ` ORDER BY created_at DESC LIMIT $${params.length + 1} OFFSET $${params.length + 2}`;
    params.push(limit, offset);

    const result = await this.pool.query(query, params);
    return result.rows.map((row) => this.mapAssessment(row));
  }

  async updateAssessmentStatus(assessmentId: string, status: AssessmentStatus): Promise<Assessment> {
    const query = `
      UPDATE assessments
      SET status = $1, updated_at = NOW(), completed_at = CASE WHEN $1 IN ('completed', 'failed') THEN NOW() ELSE completed_at END
      WHERE id = $2
      RETURNING *
    `;

    const result = await this.pool.query(query, [status, assessmentId]);
    if (result.rows.length === 0) {
      throw new BadRequestException('Assessment not found');
    }

    return this.mapAssessment(result.rows[0]);
  }

  // ============================================
  // ACAT PROTOCOL RUN OPERATIONS
  // ============================================

  async createProtocolRun(assessmentId: string, stepNumber: number, stepName: string): Promise<ACATProtocolRun> {
    const id = uuidv4();

    const query = `
      INSERT INTO acat_protocol_runs (
        id, assessment_id, step_number, step_name, status, step_data, created_at
      )
      VALUES ($1, $2, $3, $4, $5, $6, $7)
      RETURNING *
    `;

    const values = [id, assessmentId, stepNumber, stepName, 'pending', '{}', new Date()];

    try {
      const result = await this.pool.query(query, values);
      return this.mapProtocolRun(result.rows[0]);
    } catch (error) {
      this.logger.error(`Failed to create protocol run: ${error.message}`, error);
      throw new BadRequestException(`Failed to create protocol run: ${error.message}`);
    }
  }

  async updateProtocolRun(
    runId: string,
    status: 'running' | 'completed' | 'failed',
    resultData?: Record<string, any>,
    durationMs?: number,
    errorMessage?: string
  ): Promise<ACATProtocolRun> {
    const query = `
      UPDATE acat_protocol_runs
      SET
        status = $1,
        result_data = COALESCE($2, result_data),
        duration_ms = COALESCE($3, duration_ms),
        error_message = COALESCE($4, error_message),
        completed_at = CASE WHEN $1 IN ('completed', 'failed') THEN NOW() ELSE completed_at END
      WHERE id = $5
      RETURNING *
    `;

    const values = [status, resultData ? JSON.stringify(resultData) : null, durationMs, errorMessage, runId];

    try {
      const result = await this.pool.query(query, values);
      if (result.rows.length === 0) {
        throw new BadRequestException('Protocol run not found');
      }
      return this.mapProtocolRun(result.rows[0]);
    } catch (error) {
      this.logger.error(`Failed to update protocol run: ${error.message}`, error);
      throw new BadRequestException(`Failed to update protocol run: ${error.message}`);
    }
  }

  async getProtocolRuns(assessmentId: string): Promise<ACATProtocolRun[]> {
    const query = `
      SELECT * FROM acat_protocol_runs
      WHERE assessment_id = $1
      ORDER BY step_number ASC
    `;

    const result = await this.pool.query(query, [assessmentId]);
    return result.rows.map((row) => this.mapProtocolRun(row));
  }

  // ============================================
  // EPISTEMIC ARTIFACT OPERATIONS
  // ============================================

  async createArtifact(assessmentId: string, dto: CreateFindingDto | CreateDecisionDto | any): Promise<EpistemicArtifact> {
    const id = uuidv4();
    const type = this.determineArtifactType(dto);

    const query = `
      INSERT INTO epistemic_artifacts (
        id, assessment_id, task_id, type, title, description, data, confidence, impact, status, created_at
      )
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
      RETURNING *
    `;

    const values = [
      id,
      assessmentId,
      dto.task_id || null,
      type,
      this.extractTitle(dto),
      dto.description || null,
      JSON.stringify(this.extractData(dto)),
      dto.confidence || null,
      dto.impact || null,
      'open',
      new Date(),
    ];

    try {
      const result = await this.pool.query(query, values);
      return this.mapArtifact(result.rows[0]);
    } catch (error) {
      this.logger.error(`Failed to create artifact: ${error.message}`, error);
      throw new BadRequestException(`Failed to create artifact: ${error.message}`);
    }
  }

  async getArtifacts(assessmentId: string, type?: string): Promise<EpistemicArtifact[]> {
    let query = `SELECT * FROM epistemic_artifacts WHERE assessment_id = $1`;
    const params = [assessmentId];

    if (type) {
      params.push(type);
      query += ` AND type = $${params.length}`;
    }

    query += ` ORDER BY created_at DESC`;

    const result = await this.pool.query(query, params);
    return result.rows.map((row) => this.mapArtifact(row));
  }

  async createEdge(sourceId: string, targetId: string, relation: string): Promise<EpistemicEdge> {
    const id = uuidv4();

    const query = `
      INSERT INTO epistemic_edges (id, source_id, target_id, relation, created_at)
      VALUES ($1, $2, $3, $4, $5)
      ON CONFLICT (source_id, target_id, relation) DO NOTHING
      RETURNING *
    `;

    const result = await this.pool.query(query, [id, sourceId, targetId, relation, new Date()]);

    if (result.rows.length === 0) {
      // Edge already exists, return it
      const existingEdge = await this.pool.query(
        `SELECT * FROM epistemic_edges WHERE source_id = $1 AND target_id = $2 AND relation = $3`,
        [sourceId, targetId, relation]
      );
      return this.mapEdge(existingEdge.rows[0]);
    }

    return this.mapEdge(result.rows[0]);
  }

  async getEdges(assessmentId: string): Promise<EpistemicEdge[]> {
    const query = `
      SELECT ee.* FROM epistemic_edges ee
      JOIN epistemic_artifacts ea ON ee.source_id = ea.id
      WHERE ea.assessment_id = $1
      ORDER BY ee.created_at DESC
    `;

    const result = await this.pool.query(query, [assessmentId]);
    return result.rows.map((row) => this.mapEdge(row));
  }

  async resolveArtifact(artifactId: string): Promise<EpistemicArtifact> {
    const query = `
      UPDATE epistemic_artifacts
      SET status = 'resolved', resolved_at = NOW()
      WHERE id = $1
      RETURNING *
    `;

    const result = await this.pool.query(query, [artifactId]);
    if (result.rows.length === 0) {
      throw new BadRequestException('Artifact not found');
    }

    return this.mapArtifact(result.rows[0]);
  }

  // ============================================
  // MAPPERS (Convert DB rows to domain types)
  // ============================================

  private mapAssessment(row: any): Assessment {
    return {
      id: row.id,
      org_id: row.org_id,
      system_id: row.system_id,
      system_name: row.system_name,
      system_info: typeof row.system_info === 'string' ? JSON.parse(row.system_info) : row.system_info,
      status: row.status,
      result_summary:
        typeof row.result_summary === 'string' ? JSON.parse(row.result_summary) : row.result_summary,
      created_at: new Date(row.created_at),
      updated_at: new Date(row.updated_at),
      completed_at: row.completed_at ? new Date(row.completed_at) : undefined,
    };
  }

  private mapProtocolRun(row: any): ACATProtocolRun {
    return {
      id: row.id,
      assessment_id: row.assessment_id,
      step_number: row.step_number,
      step_name: row.step_name,
      status: row.status,
      step_data: typeof row.step_data === 'string' ? JSON.parse(row.step_data) : row.step_data,
      result_data: row.result_data ? (typeof row.result_data === 'string' ? JSON.parse(row.result_data) : row.result_data) : undefined,
      duration_ms: row.duration_ms,
      error_message: row.error_message,
      created_at: new Date(row.created_at),
      completed_at: row.completed_at ? new Date(row.completed_at) : undefined,
    };
  }

  private mapArtifact(row: any): EpistemicArtifact {
    return {
      id: row.id,
      assessment_id: row.assessment_id,
      task_id: row.task_id,
      type: row.type,
      title: row.title,
      description: row.description,
      data: typeof row.data === 'string' ? JSON.parse(row.data) : row.data,
      confidence: row.confidence ? parseFloat(row.confidence) : undefined,
      impact: row.impact ? parseFloat(row.impact) : undefined,
      status: row.status,
      created_at: new Date(row.created_at),
      resolved_at: row.resolved_at ? new Date(row.resolved_at) : undefined,
    };
  }

  private mapEdge(row: any): EpistemicEdge {
    return {
      id: row.id,
      source_id: row.source_id,
      target_id: row.target_id,
      relation: row.relation,
      created_at: new Date(row.created_at),
    };
  }

  // ============================================
  // HELPERS
  // ============================================

  private determineArtifactType(dto: any): string {
    if (dto.finding) return 'finding';
    if (dto.choice) return 'decision';
    if (dto.assumption) return 'assumption';
    if (dto.unknown) return 'unknown';
    if (dto.approach) return 'dead_end';
    if (dto.mistake) return 'mistake';
    throw new BadRequestException('Cannot determine artifact type from DTO');
  }

  private extractTitle(dto: any): string {
    return dto.finding || dto.choice || dto.assumption || dto.unknown || dto.approach || dto.mistake || '';
  }

  private extractData(dto: any): Record<string, any> {
    const { task_id, description, ...data } = dto;
    return data;
  }
}
