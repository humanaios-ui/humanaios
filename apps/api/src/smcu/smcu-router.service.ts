/**
 * SMCU Router Service — Contextual Bandit Method Router
 *
 * Implements a lightweight Thompson-sampling-inspired contextual bandit over
 * the set of SmcuMethod "arms".  90 % of the time it exploits the best known
 * method for a given SMCU context; 10 % of the time it explores a random
 * method to gather new telemetry.
 *
 * Routing decision flow:
 *   1. Roll an exploration die.
 *   2. If exploiting: fetch the top-N similar past records from telemetry,
 *      average their per-method rewards, select the highest-scoring arm.
 *   3. If exploring: pick a uniform-random arm.
 *   4. Return a SmcuRoutingDecision for the caller to execute.
 */

import { Injectable, Logger } from '@nestjs/common';
import {
  SmcuFeatures,
  SmcuMethod,
  SmcuRoutingDecision,
  SmcuTelemetryRecord,
  SMCU_CONFIG,
} from './smcu.protocol';
import { SmcuTelemetryService } from './smcu-telemetry.service';

const ALL_METHODS = Object.values(SmcuMethod);

@Injectable()
export class SmcuRouterService {
  private readonly logger = new Logger(SmcuRouterService.name);

  constructor(private telemetry: SmcuTelemetryService) {}

  /**
   * Determine the best processing method for a given SMCU.
   *
   * @param smcu_id  Unique SMCU identifier (e.g. "payment/card.go-L45")
   * @param features Contextual features extracted from the SMCU
   * @returns        Routing decision with selected method and exploration flag
   */
  async route(
    smcu_id: string,
    features: SmcuFeatures,
  ): Promise<SmcuRoutingDecision> {
    const is_exploration = Math.random() > SMCU_CONFIG.EXPLOITATION_RATE;

    if (is_exploration) {
      const selected_method = this.randomMethod();
      this.logger.debug(
        `[SMCU] Exploration for ${smcu_id}: selected ${selected_method}`,
      );
      return {
        smcu_id,
        selected_method,
        predicted_reward: 0,
        is_exploration: true,
        similar_smcu_ids: [],
      };
    }

    // Exploitation: find similar past records and pick the best arm.
    const similar = await this.telemetry.findSimilar(
      features,
      SMCU_CONFIG.SIMILARITY_LOOKBACK,
    );

    if (similar.length === 0) {
      // No history yet — fall back to a safe default.
      this.logger.debug(
        `[SMCU] No history for ${smcu_id}, defaulting to QUICK_LINT`,
      );
      return {
        smcu_id,
        selected_method: SmcuMethod.QUICK_LINT,
        predicted_reward: 0,
        is_exploration: false,
        similar_smcu_ids: [],
      };
    }

    const { method, predicted_reward } = this.selectBestMethod(similar);

    this.logger.debug(
      `[SMCU] Exploit for ${smcu_id}: ${method} (predicted reward=${predicted_reward.toFixed(3)})`,
    );

    return {
      smcu_id,
      selected_method: method,
      predicted_reward,
      is_exploration: false,
      similar_smcu_ids: similar.map((r) => r.smcu_id),
    };
  }

  // ── private helpers ────────────────────────────────────────────────────────

  /**
   * Average the rewards across similar records grouped by method, then return
   * the method with the highest average reward.
   */
  private selectBestMethod(records: SmcuTelemetryRecord[]): {
    method: SmcuMethod;
    predicted_reward: number;
  } {
    const rewardsByMethod: Map<SmcuMethod, number[]> = new Map();

    for (const record of records) {
      const bucket = rewardsByMethod.get(record.action_taken) ?? [];
      bucket.push(record.reward);
      rewardsByMethod.set(record.action_taken, bucket);
    }

    let bestMethod: SmcuMethod = SmcuMethod.QUICK_LINT;
    let bestAvg = -Infinity;

    for (const [method, rewards] of rewardsByMethod.entries()) {
      const avg = rewards.reduce((s, r) => s + r, 0) / rewards.length;
      if (avg > bestAvg) {
        bestAvg = avg;
        bestMethod = method;
      }
    }

    return { method: bestMethod, predicted_reward: bestAvg };
  }

  private randomMethod(): SmcuMethod {
    return ALL_METHODS[Math.floor(Math.random() * ALL_METHODS.length)];
  }
}
