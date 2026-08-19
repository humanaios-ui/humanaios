/**
 * SMCU Telemetry Service
 *
 * Persists SMCU execution records and exposes query methods used by the
 * contextual bandit router for similarity-based method selection and
 * performance anomaly detection.
 */

import { Injectable, Logger, Inject } from '@nestjs/common';
import { Pool } from 'pg';
import {
  SmcuTelemetryRecord,
  CreateSmcuTelemetryDto,
  SmcuPerformanceSummary,
  SmcuMethod,
  SmcuFeatures,
  SMCU_CONFIG,
} from './smcu.protocol';

@Injectable()
export class SmcuTelemetryService {
  private readonly logger = new Logger(SmcuTelemetryService.name);

  constructor(@Inject('DATABASE_POOL') private pool: Pool) {}

  /**
   * Persist a completed SMCU telemetry record.
   */
  async record(dto: CreateSmcuTelemetryDto): Promise<SmcuTelemetryRecord> {
    const now = new Date();
    const query = `
      INSERT INTO smcu_telemetry (
        smcu_id, org_id, features, action_taken, reward, outcome,
        system_state, bugs_caught, duration_s, cloud_cost,
        is_exploration, recorded_at
      ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12)
      RETURNING *
    `;
    const values = [
      dto.smcu_id,
      dto.org_id,
      JSON.stringify(dto.features),
      dto.action_taken,
      dto.reward,
      dto.outcome,
      dto.system_state,
      dto.bugs_caught,
      dto.duration_s,
      dto.cloud_cost,
      dto.is_exploration,
      now,
    ];

    const result = await this.pool.query(query, values);
    const row = result.rows[0];

    this.logger.debug(
      `[SMCU] Recorded telemetry for ${dto.smcu_id}: reward=${dto.reward.toFixed(3)}`,
    );

    return this.rowToRecord(row);
  }

  /**
   * Retrieve the most recent telemetry records for a specific SMCU.
   * Used to detect performance anomalies (sudden 10× slowdown).
   */
  async getRecentRecords(
    smcu_id: string,
    limit = 30,
  ): Promise<SmcuTelemetryRecord[]> {
    const result = await this.pool.query(
      `SELECT * FROM smcu_telemetry
       WHERE smcu_id = $1
       ORDER BY recorded_at DESC
       LIMIT $2`,
      [smcu_id, limit],
    );
    return result.rows.map(this.rowToRecord);
  }

  /**
   * Find the top-N most similar past SMCU records based on feature distance.
   * Similarity is computed as Euclidean distance on numeric features.
   *
   * Returns records ordered by similarity (closest first).
   */
  async findSimilar(
    features: SmcuFeatures,
    limit = SMCU_CONFIG.SIMILARITY_LOOKBACK,
  ): Promise<SmcuTelemetryRecord[]> {
    // Euclidean distance on the key numeric dimensions.
    // We use SQL-level arithmetic for performance; non-numeric features are
    // matched exactly (extension filter applied when non-empty).
    const result = await this.pool.query(
      `SELECT *,
        SQRT(
          POWER(CAST(features->>'complexity' AS FLOAT) - $1, 2) +
          POWER(CAST(features->>'lines'      AS FLOAT) - $2, 2) +
          POWER(CAST(features->>'churn'      AS FLOAT) - $3, 2)
        ) AS _dist
       FROM smcu_telemetry
       WHERE ($4 = '' OR features->>'extension' = $4)
       ORDER BY _dist ASC
       LIMIT $5`,
      [
        features.complexity,
        features.lines,
        features.churn,
        features.extension ?? '',
        limit,
      ],
    );
    return result.rows.map(this.rowToRecord);
  }

  /**
   * Compute aggregated performance statistics for a single SMCU.
   */
  async getPerformanceSummary(
    smcu_id: string,
  ): Promise<SmcuPerformanceSummary | null> {
    const result = await this.pool.query(
      `SELECT
         smcu_id,
         COUNT(*)::int                        AS total_runs,
         AVG(duration_s)                      AS avg_duration_s,
         AVG(reward)                          AS avg_reward,
         PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY duration_s) AS p95_duration_s,
         (array_agg(action_taken ORDER BY reward DESC))[1] AS best_method
       FROM smcu_telemetry
       WHERE smcu_id = $1
       GROUP BY smcu_id`,
      [smcu_id],
    );

    if (result.rows.length === 0) return null;

    const row = result.rows[0];

    // Anomaly: check if the most recent duration is > 10× the rolling average.
    const recent = await this.getRecentRecords(smcu_id, 1);
    const anomaly_detected =
      recent.length > 0 &&
      recent[0].duration_s >
        row.avg_duration_s * SMCU_CONFIG.ANOMALY_DURATION_FACTOR;

    return {
      smcu_id: row.smcu_id,
      total_runs: row.total_runs,
      avg_duration_s: parseFloat(row.avg_duration_s),
      avg_reward: parseFloat(row.avg_reward),
      best_method: row.best_method as SmcuMethod,
      p95_duration_s: parseFloat(row.p95_duration_s),
      anomaly_detected,
    };
  }

  // ── helpers ────────────────────────────────────────────────────────────────

  private rowToRecord(row: Record<string, unknown>): SmcuTelemetryRecord {
    return {
      smcu_id: row['smcu_id'] as string,
      org_id: row['org_id'] as string,
      features:
        typeof row['features'] === 'string'
          ? JSON.parse(row['features'] as string)
          : (row['features'] as SmcuFeatures),
      action_taken: row['action_taken'] as SmcuMethod,
      reward: parseFloat(row['reward'] as string),
      outcome: row['outcome'] as string,
      system_state: row['system_state'] as SmcuTelemetryRecord['system_state'],
      bugs_caught: parseInt(row['bugs_caught'] as string, 10),
      duration_s: parseFloat(row['duration_s'] as string),
      cloud_cost: parseFloat(row['cloud_cost'] as string),
      is_exploration: row['is_exploration'] as boolean,
      recorded_at: new Date(row['recorded_at'] as string),
    };
  }
}
