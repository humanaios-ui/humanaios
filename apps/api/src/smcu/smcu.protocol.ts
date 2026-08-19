/**
 * SMCU (Smallest Machine Computable Unit) Protocol
 *
 * Defines the types, schema, and method enumerations for the SMCU telemetry
 * and autonomous learning system. Every file/function processed by the
 * pipeline is tracked at this granularity to enable closed-loop optimization.
 *
 * Architecture:
 *   Detect (new SMCU) → Predict (best method) → Execute → Observe (telemetry)
 *   → Learn (update weights) → Optimize (mutate policy)
 */

/**
 * Processing methods available for a given SMCU.
 * The contextual bandit selects from these "arms" based on SMCU features.
 */
export enum SmcuMethod {
  FULL_LINT = 'full_lint',
  QUICK_LINT = 'quick_lint',
  DEEP_SECURITY_SCAN = 'deep_security_scan',
  SKIP_CACHE_HIT = 'skip_cache_hit',
  PARALLEL_BUILD = 'parallel_build',
}

/**
 * System load level at the time of execution.
 * Used as a contextual feature for the method router.
 */
export type SmcuSystemState = 'low_load' | 'normal_load' | 'high_load';

/**
 * Contextual features extracted from the SMCU at routing time.
 * These form the "context" input to the bandit model.
 */
export interface SmcuFeatures {
  /** McCabe cyclomatic complexity estimate */
  complexity: number;
  /** Total lines in the file */
  lines: number;
  /** Commits touching this file in the last 7 days */
  churn: number;
  /** File extension (e.g. 'go', 'py', 'ts') */
  extension: string;
  /** Days since the file was last modified */
  days_since_last_edit: number;
  /** Estimated author experience score (0–1) */
  author_experience: number;
}

/**
 * Single SMCU telemetry record stored after each execution.
 * Persisted in the smcu_telemetry table and indexed for bandit lookups.
 *
 * Matches the JSON schema defined in the issue:
 * {
 *   "smu_id": "payment/card.go-L45",
 *   "features": { "complexity": 12, "lines": 89, "churn": 7 },
 *   "action_taken": "deep_scan",
 *   "reward": 0.85,
 *   "outcome": "found 0 bugs, took 4.2s",
 *   "system_state": "high_load"
 * }
 */
export interface SmcuTelemetryRecord {
  /** Unique identifier, format: "<org>/<file_path>-L<line>" */
  smcu_id: string;
  /** Org that owns this SMCU */
  org_id: string;
  /** Contextual features at time of processing */
  features: SmcuFeatures;
  /** Method applied */
  action_taken: SmcuMethod;
  /**
   * Composite reward: (bugs_caught * 10) - (duration_s) - (cloud_cost_units)
   * Normalised to [-1, 1] range.
   */
  reward: number;
  /** Human-readable outcome description */
  outcome: string;
  /** System load at execution time */
  system_state: SmcuSystemState;
  /** Bugs or issues found (raw count) */
  bugs_caught: number;
  /** Wall-clock execution time in seconds */
  duration_s: number;
  /** Estimated cloud cost in abstract units */
  cloud_cost: number;
  /** Whether this run was an exploration (random) or exploitation (model) run */
  is_exploration: boolean;
  recorded_at: Date;
}

/**
 * Parameters for creating a new telemetry record.
 */
export type CreateSmcuTelemetryDto = Omit<SmcuTelemetryRecord, 'recorded_at'>;

/**
 * Routing decision returned by the contextual bandit.
 */
export interface SmcuRoutingDecision {
  smcu_id: string;
  selected_method: SmcuMethod;
  /** Predicted reward for the selected method */
  predicted_reward: number;
  /** True if this was an exploration (10 % random) run */
  is_exploration: boolean;
  /** Top-5 most similar past records used for prediction */
  similar_smcu_ids: string[];
}

/**
 * Aggregated performance statistics for a given SMCU over time.
 */
export interface SmcuPerformanceSummary {
  smcu_id: string;
  total_runs: number;
  avg_duration_s: number;
  avg_reward: number;
  best_method: SmcuMethod;
  /** p95 duration across all runs */
  p95_duration_s: number;
  /** Alert flag: true if latest duration > 10× rolling average */
  anomaly_detected: boolean;
}

/**
 * Configuration constants for the SMCU engine.
 */
export const SMCU_CONFIG = {
  /** Fraction of traffic routed by the model (exploitation) */
  EXPLOITATION_RATE: 0.9,
  /** Fraction of traffic randomly routed (exploration) */
  EXPLORATION_RATE: 0.1,
  /** Number of similar past SMCUs to retrieve for routing */
  SIMILARITY_LOOKBACK: 5,
  /** Reward multiplier for each bug caught */
  REWARD_BUG_WEIGHT: 10,
  /** Reward penalty per second of execution */
  REWARD_DURATION_WEIGHT: -1,
  /** Reward penalty per cloud cost unit */
  REWARD_COST_WEIGHT: -1,
  /** Anomaly threshold: flag if duration > factor × rolling average */
  ANOMALY_DURATION_FACTOR: 10,
} as const;

/**
 * Compute the composite reward for a completed SMCU run.
 *
 * Utility = (bugs_caught × 10) + (duration_s × -1) + (cloud_cost × -1)
 * Normalised to a [-1, 1] range using a soft tanh-like clamp.
 */
export function computeSmcuReward(
  bugs_caught: number,
  duration_s: number,
  cloud_cost: number,
): number {
  const raw =
    bugs_caught * SMCU_CONFIG.REWARD_BUG_WEIGHT +
    duration_s * SMCU_CONFIG.REWARD_DURATION_WEIGHT +
    cloud_cost * SMCU_CONFIG.REWARD_COST_WEIGHT;
  // Soft-clamp to [-1, 1]
  return Math.max(-1, Math.min(1, raw / 100));
}
