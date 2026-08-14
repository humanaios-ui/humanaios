/**
 * ASC_GATEWAY Protocol — External API Interfaces
 * Defines the contract for measurement engine consumers
 */

import { MeasurementStatus } from './measurement-engine/sequential-analysis';
import { CalibrationTier } from './measurement-engine/tier-ceiling';

/**
 * Request: Register a deployment for auditing
 */
export interface RegisterDeploymentRequest {
  modelName: string;
  modelVersion: string;
  modelProvider: string;
  deploymentId: string;
  deploymentName: string;
  environmentName: 'staging' | 'production';
  stackVersion: string;
  configurationHash: string;
}

/**
 * Request: Record a probe result from the probe runner
 */
export interface RecordProbeResultRequest {
  probeId: string;
  classId: string;
  targetTuple: string;
  inputText: string;
  expectedOutput?: string;
  actualOutput: string;
  gradePass: boolean;
  confidenceScore?: number;
  adjudicatorId?: string;
  adjudicatorNotes?: string;
}

/**
 * Request: Create a measurement window and compute status
 */
export interface CreateMeasurementWindowRequest {
  deploymentId: string;
  dimensionName: string;
  windowStartTime: Date;
  windowEndTime: Date;
  windowSize: number;
  passCount: number;
  failCount: number;
}

/**
 * Response: Measurement result with status
 */
export interface MeasurementWindowResponse {
  windowId: string;
  dimensionName: string;
  passRate: number;
  status: MeasurementStatus;
  statusReason: string;
  notificationRequired: boolean;
  computedAt: Date;
}

/**
 * Response: Customer notification payload (advisory-only at launch)
 */
export interface CustomerNotificationPayload {
  triggeredAt: Date;
  statusUpdates: Array<{
    dimensionName: string;
    previousStatus: MeasurementStatus;
    currentStatus: MeasurementStatus;
    passRate: number;
    recommendation: string;
  }>;
  caveat1G: string;
  shadowBlockingNote: string;
}

/**
 * Response: Audit report for a deployment
 */
export interface AuditReportResponse {
  deploymentId: string;
  reportGeneratedAt: Date;
  dimensionSummaries: Array<{
    dimensionName: string;
    status: MeasurementStatus;
    passRate: number;
    trend: 'improving' | 'stable' | 'degrading' | 'unknown';
    tier: CalibrationTier;
    windowCount: number;
  }>;
  caveat1G?: string;
}

/**
 * Response: Health/status check
 */
export interface HealthStatusResponse {
  probesRegistered: number;
  deploymentsTracked: number;
  windowsCreated: number;
  gateCapableDimensions: number;
  uncalibratedDimensions: number;
  status: 'ready' | 'degraded' | 'offline';
}
