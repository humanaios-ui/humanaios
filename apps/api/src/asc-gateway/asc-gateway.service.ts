import { Injectable } from '@nestjs/common';
import { ProbeRegistry, ProbeClass, ProbeResult } from './measurement-engine/probe-taxonomy';
import { TierCeilingMap, CalibrationTier } from './measurement-engine/tier-ceiling';
import { AgentTupleRegistry, AgentTuple } from './measurement-engine/agent-tuple';
import { SequentialAnalyzer, MeasurementWindow, Threshold, MeasurementStatus } from './measurement-engine/sequential-analysis';

/**
 * ASC_GATEWAY Service — AI Stability and Compliance Gateway
 * Ported from ADF-R measurement engine (§3)
 *
 * Main orchestration service for runtime auditing of deployed AI assistants.
 * Log-only launch (§7A): measures, logs, computes would-be blocking decisions,
 * but does not enforce them.
 */

@Injectable()
export class AscGatewayService {
  private probeRegistry: ProbeRegistry;
  private tierCeilingMap: TierCeilingMap;
  private tupleRegistry: AgentTupleRegistry;
  private sequentialAnalyzer: SequentialAnalyzer;

  constructor() {
    this.probeRegistry = new ProbeRegistry();
    this.tierCeilingMap = new TierCeilingMap();
    this.tupleRegistry = new AgentTupleRegistry();
    this.sequentialAnalyzer = new SequentialAnalyzer();
    this.initializeDefaultProbes();
  }

  /**
   * Initialize the P1–P2 probe pool for gate-capable dimensions.
   */
  private initializeDefaultProbes(): void {
    // P1: Logical Consistency probes
    this.probeRegistry.registerProbe({
      classId: ProbeClass.P1_LOGICAL_CONSISTENCY,
      probeId: 'probe:p1:logic:001',
      description: 'Verify logical consistency in response structure',
      resolutionBoundary: 'mechanical',
      timeCreated: new Date(),
      version: '1.0',
    });

    // P1: Invariance on paraphrase
    this.probeRegistry.registerProbe({
      classId: ProbeClass.P1_INVARIANCE_PARAPHRASE,
      probeId: 'probe:p1:inv-para:001',
      description: 'Invariance under input paraphrasing',
      resolutionBoundary: 'mechanical',
      timeCreated: new Date(),
      version: '1.0',
    });

    // P2: Resolvable-claim accuracy
    this.probeRegistry.registerProbe({
      classId: ProbeClass.P2_ACCURACY_RESOLVABLE_CLAIM,
      probeId: 'probe:p2:acc:001',
      description: 'Accuracy on claims resolvable against ground truth',
      resolutionBoundary: 'resolvable',
      timeCreated: new Date(),
      version: '1.0',
    });

    // P2: Confidence calibration
    this.probeRegistry.registerProbe({
      classId: ProbeClass.P2_CONFIDENCE_CALIBRATION,
      probeId: 'probe:p2:conf:001',
      description: 'Confidence score calibration (Brier score)',
      resolutionBoundary: 'resolvable',
      timeCreated: new Date(),
      version: '1.0',
    });

    // P2: Fairness (seeded pairs)
    this.probeRegistry.registerProbe({
      classId: ProbeClass.P2_FAIRNESS_SEEDED_PAIR,
      probeId: 'probe:p2:fair:001',
      description: 'Fairness across demographic/linguistic variations',
      resolutionBoundary: 'resolvable',
      timeCreated: new Date(),
      version: '1.0',
    });
  }

  /**
   * Register a deployed AI assistant (agent-as-tuple).
   */
  registerDeployment(tuple: AgentTuple): void {
    this.tupleRegistry.registerTuple(tuple);
  }

  /**
   * Record a probe result from the shadow-traffic or synthetic probe runner.
   */
  recordProbeResult(result: ProbeResult): void {
    this.probeRegistry.recordResult(result);
  }

  /**
   * Create a measurement window and compute status.
   */
  measureWindow(window: MeasurementWindow): {
    window: MeasurementWindow;
    statuses: Array<{
      dimensionName: string;
      status: MeasurementStatus;
      passRate: number;
      statusReason: string;
      notificationRequired: boolean;
    }>;
  } {
    this.sequentialAnalyzer.createWindow(window);

    const thresholds = Array.from(
      (this.sequentialAnalyzer as any).thresholds.values?.() || []
    ) as Threshold[];

    const statuses = [];
    for (const threshold of thresholds) {
      if (threshold.dimensionName === window.dimensionName) {
        const status = this.sequentialAnalyzer.computeStatus(window.windowId, threshold.thresholdId);
        if (status) {
          statuses.push({
            dimensionName: status.dimensionName,
            status: status.status,
            passRate: status.passRate,
            statusReason: status.statusReason,
            notificationRequired: status.notificationRequired,
          });
        }
      }
    }

    return { window, statuses };
  }

  /**
   * Get customer notification payload for DEGRADED/UNSATISFIED statuses.
   * Advisory-only at launch (log-only, §7A).
   */
  getNotificationPayload(): {
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
  } {
    const notifications = this.sequentialAnalyzer.getNotificationRequiredStatuses();

    return {
      triggeredAt: new Date(),
      statusUpdates: notifications.map(n => ({
        dimensionName: n.dimensionName,
        previousStatus: MeasurementStatus.SATISFIED, // Placeholder
        currentStatus: n.status,
        passRate: n.passRate,
        recommendation:
          n.status === MeasurementStatus.DEGRADED
            ? `Dimension "${n.dimensionName}" is degrading. Consider reviewing recent model updates or deployment changes.`
            : `Dimension "${n.dimensionName}" has fallen below acceptable thresholds. Immediate investigation recommended.`,
      })),
      caveat1G: this.tierCeilingMap.getCaveat1GText(),
      shadowBlockingNote:
        'This is an advisory notification. The gateway is in log-only mode and is not blocking responses. This reflects what a live-blocking policy would have done.',
    };
  }

  /**
   * Get audit report for a deployment.
   */
  getAuditReport(deploymentId: string): {
    deploymentId: string;
    reportGeneratedAt: Date;
    dimensionSummaries: Array<{
      dimensionName: string;
      status: MeasurementStatus;
      passRate: number;
      trend: string;
      tier: CalibrationTier;
      windowCount: number;
    }>;
    caveat1G?: string;
  } {
    const dimensions = this.tierCeilingMap.getGateCapableDimensions().concat(
      this.tierCeilingMap.getUncalibratedDimensions()
    );

    const dimensionSummaries = dimensions.map(dim => {
      const summary = (this.sequentialAnalyzer as any).getSummary?.(deploymentId, dim.dimensionName) || {
        latestStatus: MeasurementStatus.NOT_YET_MEASURABLE,
        passRate: 0,
        trend: 'unknown',
        windowCount: 0,
      };

      return {
        dimensionName: dim.dimensionName,
        status: summary.latestStatus,
        passRate: summary.passRate,
        trend: summary.trend,
        tier: dim.tier,
        windowCount: summary.windowCount,
      };
    });

    const hasUncalibrated = dimensionSummaries.some(d => d.tier === CalibrationTier.UNCALIBRATED);

    return {
      deploymentId,
      reportGeneratedAt: new Date(),
      dimensionSummaries,
      caveat1G: hasUncalibrated ? this.tierCeilingMap.getCaveat1GText() : undefined,
    };
  }

  /**
   * Get component status (for diagnostics).
   */
  getHealthStatus(): {
    probesRegistered: number;
    deploymentsTracked: number;
    windowsCreated: number;
    gateCapableDimensions: number;
    uncalibratedDimensions: number;
  } {
    return {
      probesRegistered: this.probeRegistry['probes'].size,
      deploymentsTracked: this.tupleRegistry['versions'].size,
      windowsCreated: (this.sequentialAnalyzer as any).windows.size,
      gateCapableDimensions: this.tierCeilingMap.getGateCapableDimensions().length,
      uncalibratedDimensions: this.tierCeilingMap.getUncalibratedDimensions().length,
    };
  }
}
