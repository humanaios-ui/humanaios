import { Injectable, Inject } from '@nestjs/common';
import { Pool } from 'pg';
import { ProbeResult } from './measurement-engine/probe-taxonomy';
import { MeasurementWindow, ThresholdStatus } from './measurement-engine/sequential-analysis';
import { AgentTuple, InfrastructureChangeEvent } from './measurement-engine/agent-tuple';

/**
 * ASC_GATEWAY Audit Logging Repository
 * Persists probe results, measurement windows, and audit events to Supabase
 */

@Injectable()
export class AscGatewayRepository {
  constructor(@Inject('DATABASE_POOL') private pool: Pool) {}

  /**
   * Record a probe result to asc_gateway_audit_log
   */
  async saveProbeResult(result: ProbeResult): Promise<string> {
    const query = `
      INSERT INTO asc_gateway_audit_log (
        deployment_id,
        request_timestamp,
        request_id,
        input_text,
        output_text,
        declared_intent,
        observed_behavior,
        iodm_score,
        dcm_score,
        acat_scores,
        audit_decision,
        audit_notes,
        logged_at
      )
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, NOW())
      RETURNING id;
    `;

    const values = [
      result.targetTuple,
      result.timestamp,
      null, // request_id (optional)
      result.inputText,
      result.actualOutput,
      null, // declared_intent (from measurement engine context)
      null, // observed_behavior (from measurement engine context)
      result.confidenceScore || 0,
      null, // dcm_score (not computed in probe result)
      null, // acat_scores (optional)
      'PASS', // audit_decision (always PASS for log-only; blocking deferred)
      null, // audit_notes
    ];

    const res = await this.pool.query(query, values);
    return res.rows[0].id;
  }

  /**
   * Save a measurement window's computed status
   */
  async saveMeasurementWindow(window: MeasurementWindow, status: ThresholdStatus): Promise<void> {
    const query = `
      INSERT INTO asc_gateway_audit_log (
        deployment_id,
        request_timestamp,
        audit_decision,
        audit_notes,
        logged_at
      )
      VALUES ($1, $2, $3, $4, NOW())
    `;

    const auditDecision =
      status.status === 'UNSATISFIED' ? 'FAIL' : status.status === 'DEGRADED' ? 'WARN' : 'PASS';

    const auditNotes = JSON.stringify({
      dimensionName: status.dimensionName,
      status: status.status,
      passRate: status.passRate,
      statusReason: status.statusReason,
      windowId: window.windowId,
      windowSize: window.windowSize,
      notificationRequired: status.notificationRequired,
    });

    const values = [window.deploymentId, window.endTime, auditDecision, auditNotes];

    await this.pool.query(query, values);
  }

  /**
   * Record a threshold breach (DEGRADED or UNSATISFIED status)
   */
  async recordThresholdBreach(
    deploymentId: string,
    thresholdId: string,
    breachType: 'DEGRADED' | 'UNSATISFIED',
    customerNotificationPayload?: Record<string, unknown>
  ): Promise<void> {
    const query = `
      INSERT INTO asc_gateway_threshold_breach (
        deployment_id,
        threshold_id,
        breach_type,
        detected_at,
        customer_notification_status,
        customer_notification_payload,
        created_at
      )
      VALUES ($1, $2, $3, NOW(), $4, $5, NOW())
    `;

    const values = [
      deploymentId,
      thresholdId,
      breachType,
      'PENDING', // notification status starts as pending (advisory-only at launch)
      customerNotificationPayload ? JSON.stringify(customerNotificationPayload) : null,
    ];

    await this.pool.query(query, values);
  }

  /**
   * Record an infrastructure change event (for invariance tracking)
   */
  async recordInfrastructureChange(
    deploymentId: string,
    event: InfrastructureChangeEvent
  ): Promise<void> {
    const query = `
      INSERT INTO asc_gateway_audit_log (
        deployment_id,
        request_timestamp,
        audit_notes,
        audit_decision,
        logged_at
      )
      VALUES ($1, $2, $3, 'INFRASTRUCTURE_EVENT', NOW())
    `;

    const auditNotes = JSON.stringify({
      eventType: event.changeType,
      description: event.description,
      previousValue: event.previousValue,
      newValue: event.newValue,
      changedBy: event.changedBy,
    });

    const values = [deploymentId, event.changedAt, auditNotes];

    await this.pool.query(query, values);
  }

  /**
   * Register a deployment in the gateway
   */
  async registerDeployment(tuple: AgentTuple): Promise<void> {
    const query = `
      INSERT INTO asc_gateway_deployment (
        deployment_id,
        deployment_name,
        ai_system_name,
        deployment_status,
        launched_at,
        created_at
      )
      VALUES ($1, $2, $3, $4, NOW(), NOW())
      ON CONFLICT (deployment_id) DO UPDATE SET deployment_status = EXCLUDED.deployment_status
    `;

    const values = [tuple.deploymentId, tuple.deploymentName, tuple.modelName, 'ACTIVE'];

    await this.pool.query(query, values);
  }

  /**
   * Get pending threshold breaches (not yet notified)
   */
  async getPendingNotifications(deploymentId: string): Promise<any[]> {
    const query = `
      SELECT * FROM asc_gateway_threshold_breach
      WHERE deployment_id = $1 AND customer_notification_status = 'PENDING'
      ORDER BY detected_at DESC
    `;

    const res = await this.pool.query(query, [deploymentId]);
    return res.rows;
  }

  /**
   * Mark a notification as sent
   */
  async markNotificationSent(breachId: string, notifiedAt?: Date): Promise<void> {
    const query = `
      UPDATE asc_gateway_threshold_breach
      SET customer_notification_status = 'SENT', notified_at = $1
      WHERE id = $2
    `;

    const values = [notifiedAt || new Date(), breachId];
    await this.pool.query(query, values);
  }

  /**
   * Get audit log entries for a deployment (for reports)
   */
  async getAuditLog(
    deploymentId: string,
    startTime?: Date,
    endTime?: Date,
    limit: number = 100
  ): Promise<any[]> {
    let query = 'SELECT * FROM asc_gateway_audit_log WHERE deployment_id = $1';
    const values: any[] = [deploymentId];

    if (startTime) {
      query += ` AND request_timestamp >= $${values.length + 1}`;
      values.push(startTime);
    }

    if (endTime) {
      query += ` AND request_timestamp <= $${values.length + 1}`;
      values.push(endTime);
    }

    query += ` ORDER BY request_timestamp DESC LIMIT $${values.length + 1}`;
    values.push(limit);

    const res = await this.pool.query(query, values);
    return res.rows;
  }

  /**
   * Get summary statistics for a deployment
   */
  async getDeploymentStats(deploymentId: string): Promise<{
    totalProbes: number;
    passCount: number;
    failCount: number;
    warnCount: number;
    breachCount: number;
  }> {
    const query = `
      SELECT
        COUNT(*) as total_probes,
        SUM(CASE WHEN audit_decision = 'PASS' THEN 1 ELSE 0 END) as pass_count,
        SUM(CASE WHEN audit_decision = 'FAIL' THEN 1 ELSE 0 END) as fail_count,
        SUM(CASE WHEN audit_decision = 'WARN' THEN 1 ELSE 0 END) as warn_count
      FROM asc_gateway_audit_log
      WHERE deployment_id = $1
    `;

    const logRes = await this.pool.query(query, [deploymentId]);
    const logStats = logRes.rows[0] || {};

    const breachQuery = `
      SELECT COUNT(*) as breach_count
      FROM asc_gateway_threshold_breach
      WHERE deployment_id = $1
    `;

    const breachRes = await this.pool.query(breachQuery, [deploymentId]);
    const breachStats = breachRes.rows[0] || {};

    return {
      totalProbes: parseInt(logStats.total_probes || 0),
      passCount: parseInt(logStats.pass_count || 0),
      failCount: parseInt(logStats.fail_count || 0),
      warnCount: parseInt(logStats.warn_count || 0),
      breachCount: parseInt(breachStats.breach_count || 0),
    };
  }
}
