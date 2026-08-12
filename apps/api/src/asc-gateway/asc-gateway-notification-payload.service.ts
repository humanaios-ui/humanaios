import { Injectable } from '@nestjs/common';
import { MeasurementStatus } from './measurement-engine/sequential-analysis';
import { CalibrationTier } from './measurement-engine/tier-ceiling';

/**
 * Art. 15 Notification Payload Service (Task 2.5)
 * Generates EU AI Act Art. 15 transparency notifications
 *
 * Notifies deployers of "significant changes in performance" (DEGRADED/UNSATISFIED).
 * Advisory-only at launch (log-only mode, §7A).
 */

export interface Art15NotificationPayload {
  // Compliance header
  regulatoryBasis: 'EU_AI_ACT_Article_15';
  complianceStatus: 'ADVISORY'; // log-only launch
  generatedAt: Date;

  // Deployer context
  deploymentId: string;
  deploymentName: string;
  modelName: string;
  modelVersion: string;

  // Performance change notification
  performanceChangeDetected: {
    severity: 'degradation' | 'failure';
    statusChange: {
      dimensionName: string;
      previousStatus: MeasurementStatus;
      currentStatus: MeasurementStatus;
      passRate: number;
      percentageChange: number;
    }[];
  };

  // Required disclosures (Art. 15)
  disclosures: {
    significantChange: string; // Human-readable explanation
    possibleCauses: string[]; // E.g., "recent model update", "deployment configuration change"
    recommendedActions: string[]; // E.g., "review recent deployments", "check logs"
    calibrationTier: CalibrationTier; // Transparency: which tier this dimension operates at
    caveat1G?: string; // UNCALIBRATED warning if applicable
  };

  // Shadow-blocking simulation (log-only mode)
  shadowBlockingSimulation?: {
    enabled: true; // Log-only mode always simulates
    wouldHaveBlocked: boolean;
    blockingThresholds: {
      dimensionName: string;
      passRateThreshold: number;
      actualPassRate: number;
    }[];
    explanation: string;
  };

  // Next steps
  actionItems: {
    operator: string[]; // What the deployer should do
    system: string[]; // What ASC_GATEWAY will do automatically
  };
}

@Injectable()
export class AscGatewayNotificationPayloadService {
  /**
   * Generate Art. 15 notification payload for a performance change.
   */
  generateNotificationPayload(context: {
    deploymentId: string;
    deploymentName: string;
    modelName: string;
    modelVersion: string;
    statusChanges: Array<{
      dimensionName: string;
      previousStatus: MeasurementStatus;
      currentStatus: MeasurementStatus;
      passRate: number;
      previousPassRate?: number;
      calibrationTier: CalibrationTier;
    }>;
  }): Art15NotificationPayload {
    const statusChanges = context.statusChanges.filter(
      s => s.currentStatus !== 'SATISFIED'
    );

    // Compute percentage changes
    const statusChangeDetails = statusChanges.map(s => ({
      dimensionName: s.dimensionName,
      previousStatus: s.previousStatus || 'SATISFIED',
      currentStatus: s.currentStatus,
      passRate: s.passRate,
      percentageChange: s.previousPassRate
        ? ((s.passRate - s.previousPassRate) / s.previousPassRate) * 100
        : 0,
    }));

    // Determine overall severity
    const hasFailure = statusChanges.some(s => s.currentStatus === 'UNSATISFIED');
    const severity: 'degradation' | 'failure' = hasFailure ? 'failure' : 'degradation';

    // Infer possible causes
    const possibleCauses = this.inferPossibleCauses(context);

    // Recommended actions
    const recommendedActions = this.generateRecommendedActions(severity, context);

    // Check for UNCALIBRATED dimensions
    const hasUncalibrated = statusChanges.some(s => s.calibrationTier === 'UNCALIBRATED');

    // Shadow-blocking simulation (log-only mode)
    const wouldHaveBlocked = hasFailure; // In blocking mode, UNSATISFIED would block

    const payload: Art15NotificationPayload = {
      regulatoryBasis: 'EU_AI_ACT_Article_15',
      complianceStatus: 'ADVISORY',
      generatedAt: new Date(),
      deploymentId: context.deploymentId,
      deploymentName: context.deploymentName,
      modelName: context.modelName,
      modelVersion: context.modelVersion,
      performanceChangeDetected: {
        severity,
        statusChange: statusChangeDetails,
      },
      disclosures: {
        significantChange: this.generateSignificantChangeDisclosure(severity, statusChangeDetails),
        possibleCauses,
        recommendedActions,
        calibrationTier: statusChanges[0]?.calibrationTier || 'PROVISIONAL',
        caveat1G: hasUncalibrated ? this.getCaveat1GText() : undefined,
      },
      shadowBlockingSimulation: {
        enabled: true,
        wouldHaveBlocked,
        blockingThresholds: statusChanges.map(s => ({
          dimensionName: s.dimensionName,
          passRateThreshold: 0.9, // Example: 90% pass threshold
          actualPassRate: s.passRate,
        })),
        explanation: wouldHaveBlocked
          ? `In blocking mode (future §7B), this deployment would have been blocked due to ${severity === 'failure' ? 'UNSATISFIED thresholds' : 'DEGRADED performance'}.`
          : 'In blocking mode (future §7B), this deployment would continue to operate.',
      },
      actionItems: {
        operator: this.getOperatorActionItems(severity, context),
        system: this.getSystemActionItems(severity),
      },
    };

    return payload;
  }

  /**
   * Format payload for email/webhook dispatch.
   */
  formatForDispatch(payload: Art15NotificationPayload): {
    subject: string;
    body: string;
    json: Art15NotificationPayload;
  } {
    const severity =
      payload.performanceChangeDetected.severity === 'failure' ? 'ALERT' : 'WARNING';

    const dimensionsList = payload.performanceChangeDetected.statusChange
      .map(s => `${s.dimensionName}: ${(s.passRate * 100).toFixed(1)}%`)
      .join(', ');

    return {
      subject: `[${severity}] ASC_GATEWAY: Performance change detected on ${payload.deploymentName} v${payload.modelVersion}`,
      body: `
Dear Deployer,

${payload.regulatoryBasis} transparency notification.

**Deployment:** ${payload.deploymentName} (${payload.deploymentId})
**Model:** ${payload.modelName} v${payload.modelVersion}
**Status:** ${payload.disclosures.significantChange}

**Affected Dimensions:** ${dimensionsList}

**Next Steps:**
${payload.actionItems.operator.map(a => `• ${a}`).join('\n')}

**System Actions:**
${payload.actionItems.system.map(a => `• ${a}`).join('\n')}

${payload.shadowBlockingSimulation?.explanation || ''}

${payload.disclosures.caveat1G ? `\n**Note:** ${payload.disclosures.caveat1G}` : ''}

This is an advisory notification. The ASC_GATEWAY is in log-only mode and is not blocking responses.

—
ASC_GATEWAY Compliance Layer
      `.trim(),
      json: payload,
    };
  }

  /**
   * Private: Infer possible causes from context.
   */
  private inferPossibleCauses(context: {
    modelVersion: string;
    statusChanges: any[];
  }): string[] {
    const causes: string[] = [];

    // Common causes
    causes.push('Recent model or inference stack update');
    causes.push('Deployment configuration change');
    causes.push('Input distribution shift (new use patterns)');

    // If multiple dimensions degraded, might be systemic
    if (context.statusChanges.length > 3) {
      causes.push('Possible systemic issue affecting multiple dimensions');
    }

    return causes;
  }

  /**
   * Private: Generate recommended actions.
   */
  private generateRecommendedActions(
    severity: 'degradation' | 'failure',
    context: any
  ): string[] {
    const actions: string[] = [];

    actions.push('Review deployment logs for recent changes');
    actions.push('Check if a model update was deployed in the last 24 hours');

    if (severity === 'degradation') {
      actions.push('Monitor system over the next 1-2 hours for recovery');
      actions.push('Consider comparing current version against the prior stable version');
    } else {
      actions.push('Consider rolling back to a previous model version if available');
      actions.push('Engage support if the issue persists');
    }

    return actions;
  }

  /**
   * Private: Generate human-readable disclosure of significant change.
   */
  private generateSignificantChangeDisclosure(
    severity: 'degradation' | 'failure',
    statusChanges: any[]
  ): string {
    const dims = statusChanges.map(s => s.dimensionName).join(', ');

    if (severity === 'failure') {
      return `Significant performance degradation detected on dimensions: ${dims}. System is approaching or has breached acceptable thresholds.`;
    } else {
      return `Performance trending downward on dimensions: ${dims}. Approaching thresholds.`;
    }
  }

  /**
   * Private: Operator action items.
   */
  private getOperatorActionItems(severity: 'degradation' | 'failure', context: any): string[] {
    return [
      'Review recent deployment changes (model, config, infrastructure)',
      'Check if input patterns have changed (data drift)',
      severity === 'failure'
        ? 'Prepare rollback procedure in case degradation continues'
        : 'Monitor the system and prepare contingency plan if degradation worsens',
      'Contact your support team if unsure about the cause',
    ];
  }

  /**
   * Private: System action items.
   */
  private getSystemActionItems(severity: 'degradation' | 'failure'): string[] {
    return [
      'Continuing to monitor performance across all dimensions',
      'Logging all probe results to audit trail',
      'Will send follow-up notification if status changes',
      severity === 'failure'
        ? 'Simulating blocking decision (log-only mode); will enforce in §7B'
        : 'Tracking trend; escalation if degradation continues',
    ];
  }

  /**
   * Private: CAVEAT-1G for UNCALIBRATED dimensions.
   */
  private getCaveat1GText(): string {
    return 'This notification includes dimensions marked UNCALIBRATED. These dimensions are reported for informational purposes and carry no compliance assurance. Marking what we cannot yet measure is a design feature, not a limitation disclaimer.';
  }
}
