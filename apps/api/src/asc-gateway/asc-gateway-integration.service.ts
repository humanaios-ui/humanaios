import { Injectable } from '@nestjs/common';
import { AscGatewayService } from './asc-gateway.service';
import { AscGatewayRepository } from './asc-gateway.repository';
import { AscGatewayAuditEventService, AuditEvent } from './asc-gateway-audit-event.service';
import { ProbeResult } from './measurement-engine/probe-taxonomy';
import { MeasurementWindow, MeasurementStatus } from './measurement-engine/sequential-analysis';
import { AgentTuple } from './measurement-engine/agent-tuple';

/**
 * ASC_GATEWAY Integration Service (Task 2.3)
 * Wires measurement engine → repository persistence → event streaming
 *
 * Provides end-to-end audit pipeline:
 * API request → probe execution → measurement → threshold evaluation →
 * persistence → event emission → customer notifications
 */

@Injectable()
export class AscGatewayIntegrationService {
  constructor(
    private readonly measurementService: AscGatewayService,
    private readonly repository: AscGatewayRepository,
    private readonly eventService: AscGatewayAuditEventService
  ) {}

  /**
   * End-to-end probe execution pipeline.
   * Orchestrates: probe → measurement → persistence → events.
   */
  async executeProbePipeline(
    deploymentId: string,
    probeResult: ProbeResult
  ): Promise<{
    auditLogId: string;
    event: AuditEvent;
  }> {
    // Step 1: Record in measurement engine
    this.measurementService.recordProbeResult(probeResult);

    // Step 2: Persist to database
    const auditLogId = await this.repository.saveProbeResult(probeResult);

    // Step 3: Emit event
    const event: AuditEvent = {
      eventType: 'probeResultRecorded',
      deploymentId,
      timestamp: probeResult.timestamp,
      severity: probeResult.gradePass ? 'info' : 'warn',
      data: {
        probeId: probeResult.probeId,
        classId: probeResult.classId,
        passed: probeResult.gradePass,
        confidence: probeResult.confidenceScore,
      },
    };

    await this.eventService.emitEvent(event);

    return { auditLogId, event };
  }

  /**
   * End-to-end measurement window pipeline.
   * Orchestrates: window creation → status computation → persistence → breach detection → notifications.
   */
  async measurementWindowPipeline(
    deploymentId: string,
    window: MeasurementWindow
  ): Promise<{
    statuses: Array<{
      dimensionName: string;
      status: MeasurementStatus;
      passRate: number;
    }>;
    breaches: Array<{
      dimensionName: string;
      breachType: 'DEGRADED' | 'UNSATISFIED';
      event: AuditEvent;
    }>;
  }> {
    // Step 1: Measure in engine
    const result = this.measurementService.measureWindow(window);

    // Step 2: Persist and check for breaches
    const breaches: Array<{
      dimensionName: string;
      breachType: 'DEGRADED' | 'UNSATISFIED';
      event: AuditEvent;
    }> = [];

    for (const status of result.statuses) {
      // Persist the measurement
      await this.repository.saveMeasurementWindow(window, {
        thresholdId: `threshold:${status.dimensionName}`,
        windowId: window.windowId,
        dimensionName: status.dimensionName,
        passRate: status.passRate,
        status: status.status,
        statusReason: status.statusReason,
        computedAt: new Date(),
        notificationRequired: status.notificationRequired,
      });

      // Detect breaches
      if (status.notificationRequired) {
        const breachType = status.status === 'DEGRADED' ? 'DEGRADED' : 'UNSATISFIED';

        // Record breach
        const notificationPayload = this.measurementService.getNotificationPayload();
        await this.repository.recordThresholdBreach(
          deploymentId,
          `threshold:${status.dimensionName}`,
          breachType,
          notificationPayload
        );

        // Emit breach event
        const event: AuditEvent = {
          eventType: breachType === 'DEGRADED' ? 'degradationDetected' : 'thresholdBreach',
          deploymentId,
          timestamp: new Date(),
          severity: breachType === 'DEGRADED' ? 'warn' : 'error',
          data: {
            dimensionName: status.dimensionName,
            breachType,
            passRate: status.passRate,
            statusReason: status.statusReason,
            windowId: window.windowId,
          },
        };

        await this.eventService.emitEvent(event);
        breaches.push({
          dimensionName: status.dimensionName,
          breachType,
          event,
        });
      }
    }

    // Step 3: Emit window-completed event
    const windowEvent: AuditEvent = {
      eventType: 'measurementWindowCompleted',
      deploymentId,
      timestamp: new Date(),
      severity: 'info',
      data: {
        windowId: window.windowId,
        dimensionName: window.dimensionName,
        passRate: window.passRate,
        breachCount: breaches.length,
      },
    };

    await this.eventService.emitEvent(windowEvent);

    return {
      statuses: result.statuses,
      breaches,
    };
  }

  /**
   * Deployment registration pipeline.
   * Orchestrates: tuple creation → registration → persistence → event emission.
   */
  async registerDeploymentPipeline(tuple: AgentTuple): Promise<{
    deploymentId: string;
    event: AuditEvent;
  }> {
    // Step 1: Register in measurement engine
    this.measurementService.registerDeployment(tuple);

    // Step 2: Persist to database
    await this.repository.registerDeployment(tuple);

    // Step 3: Emit event
    const event: AuditEvent = {
      eventType: 'deploymentRegistered',
      deploymentId: tuple.deploymentId,
      timestamp: new Date(),
      severity: 'info',
      data: {
        modelName: tuple.modelName,
        modelVersion: tuple.modelVersion,
        deploymentName: tuple.deploymentName,
        environment: tuple.deploymentId,
      },
    };

    await this.eventService.emitEvent(event);

    return { deploymentId: tuple.deploymentId, event };
  }

  /**
   * Notification processing pipeline.
   * Orchestrates: fetch pending → send → mark sent → emit event.
   */
  async processNotificationsPipeline(deploymentId: string): Promise<{
    sent: number;
    events: AuditEvent[];
  }> {
    // Fetch pending notifications
    const pending = await this.repository.getPendingNotifications(deploymentId);

    const sentEvents: AuditEvent[] = [];

    for (const notification of pending) {
      try {
        // In production, this would actually send via webhook/email/SMS
        console.log(`[SIMULATION] Sending notification for deployment ${deploymentId}`);

        // Mark as sent
        await this.repository.markNotificationSent(notification.id);

        // Emit event
        const event: AuditEvent = {
          eventType: 'notificationSent',
          deploymentId,
          timestamp: new Date(),
          severity: 'info',
          data: {
            notificationId: notification.id,
            breachType: notification.breach_type,
            dimensionName: notification.customer_notification_payload?.dimensionName,
          },
        };

        await this.eventService.emitEvent(event);
        sentEvents.push(event);
      } catch (error) {
        console.error(`Failed to process notification ${notification.id}:`, error);
      }
    }

    return {
      sent: sentEvents.length,
      events: sentEvents,
    };
  }

  /**
   * Get full audit report for a deployment.
   * Combines measurement stats + event history + notification status.
   */
  async getFullAuditReport(deploymentId: string): Promise<{
    stats: Awaited<ReturnType<AscGatewayRepository['getDeploymentStats']>>;
    eventStats: Awaited<ReturnType<AscGatewayAuditEventService['getEventStats']>>;
    recentEvents: AuditEvent[];
    pendingNotifications: number;
  }> {
    const stats = await this.repository.getDeploymentStats(deploymentId);
    const eventStats = this.eventService.getEventStats(deploymentId);
    const recentEvents = this.eventService.getEventStream(deploymentId, undefined, 50);

    const pending = await this.repository.getPendingNotifications(deploymentId);

    return {
      stats,
      eventStats,
      recentEvents,
      pendingNotifications: pending.length,
    };
  }
}
