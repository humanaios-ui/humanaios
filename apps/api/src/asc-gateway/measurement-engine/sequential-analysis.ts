/**
 * Sequential Analysis — Windowed Monitoring & Threshold Logic
 * Ported from ADF-R §3.6
 *
 * Manages measurement windows, pass-rate tracking, and DEGRADED/UNSATISFIED status.
 * Implements the pre-registered threshold logic for gating decisions.
 */

export enum MeasurementStatus {
  SATISFIED = 'SATISFIED',
  DEGRADED = 'DEGRADED',         // Trend approaching threshold OR spread straddles threshold
  UNSATISFIED = 'UNSATISFIED',   // Threshold breached
  NOT_YET_MEASURABLE = 'NOT_YET_MEASURABLE',
  NOT_APPLICABLE = 'NOT_APPLICABLE',
}

export interface Threshold {
  thresholdId: string;
  dimensionName: string;
  lowerBound: number;  // Pass rate floor (e.g., 0.90 = 90%)
  upperBound: number;  // Pass rate ceiling (e.g., 1.0 = 100%)
  degradedBand: number; // Range below threshold that triggers DEGRADED (e.g., 0.05 = 5% buffer)
  spreadTreatment: 'POINT_IN_BAND' | 'BAND_CENTER' | 'CONSERVATIVE' | 'OPTIMISTIC';
  ratificationDate: Date;
  operatorId: string;
}

export interface MeasurementWindow {
  windowId: string;
  deploymentId: string;
  startTime: Date;
  endTime: Date;
  windowSize: number; // Number of samples in this window
  dimensionName: string;
  passCount: number;
  failCount: number;
  passRate: number; // passCount / (passCount + failCount)
}

export interface ThresholdStatus {
  thresholdId: string;
  windowId: string;
  dimensionName: string;
  passRate: number;
  status: MeasurementStatus;
  statusReason: string;
  computedAt: Date;
  notificationRequired: boolean; // DEGRADED or UNSATISFIED requires customer notification
}

export class SequentialAnalyzer {
  private windows: Map<string, MeasurementWindow> = new Map();
  private thresholds: Map<string, Threshold> = new Map();
  private statuses: Map<string, ThresholdStatus> = new Map();

  /**
   * Register a threshold (set by deploying operator's compliance authority).
   * Thresholds are immutable per operator decision per engagement.
   */
  registerThreshold(threshold: Threshold): void {
    this.thresholds.set(threshold.thresholdId, threshold);
  }

  /**
   * Create a new measurement window.
   */
  createWindow(window: MeasurementWindow): void {
    this.windows.set(window.windowId, window);
  }

  /**
   * Compute status for a measurement window.
   * Status is NEVER hand-set; it is computed from evidence.
   */
  computeStatus(windowId: string, thresholdId: string): ThresholdStatus | null {
    const window = this.windows.get(windowId);
    const threshold = this.thresholds.get(thresholdId);

    if (!window || !threshold) {
      return null;
    }

    const passRate = window.passRate;
    let status = MeasurementStatus.SATISFIED;
    let statusReason = '';
    let notificationRequired = false;

    // Check if UNSATISFIED (below lower bound)
    if (passRate < threshold.lowerBound) {
      status = MeasurementStatus.UNSATISFIED;
      statusReason = `Pass rate ${(passRate * 100).toFixed(2)}% below threshold ${(threshold.lowerBound * 100).toFixed(2)}%`;
      notificationRequired = true;
    }
    // Check if DEGRADED (approaching lower bound)
    else if (passRate < threshold.lowerBound + threshold.degradedBand) {
      status = MeasurementStatus.DEGRADED;
      statusReason = `Pass rate ${(passRate * 100).toFixed(2)}% within degraded band (${((threshold.lowerBound + threshold.degradedBand) * 100).toFixed(2)}% threshold + ${(threshold.degradedBand * 100).toFixed(2)}% buffer)`;
      notificationRequired = true;
    }
    // SATISFIED: within acceptable range
    else if (passRate <= threshold.upperBound) {
      status = MeasurementStatus.SATISFIED;
      statusReason = `Pass rate ${(passRate * 100).toFixed(2)}% within acceptable range`;
    }

    const thresholdStatus: ThresholdStatus = {
      thresholdId,
      windowId,
      dimensionName: threshold.dimensionName,
      passRate,
      status,
      statusReason,
      computedAt: new Date(),
      notificationRequired,
    };

    this.statuses.set(`${windowId}:${thresholdId}`, thresholdStatus);
    return thresholdStatus;
  }

  /**
   * Get status for a dimension in a window.
   */
  getStatus(windowId: string, thresholdId: string): ThresholdStatus | undefined {
    return this.statuses.get(`${windowId}:${thresholdId}`);
  }

  /**
   * Get all statuses requiring customer notification (DEGRADED or UNSATISFIED).
   */
  getNotificationRequiredStatuses(): ThresholdStatus[] {
    return Array.from(this.statuses.values()).filter(s => s.notificationRequired);
  }

  /**
   * Get degradation trend (comparing sequential windows).
   */
  getTrend(
    deploymentId: string,
    dimensionName: string,
    windowCount: number = 3
  ): {
    windows: MeasurementWindow[];
    trend: 'improving' | 'stable' | 'degrading' | 'unknown';
  } {
    const windows = Array.from(this.windows.values())
      .filter(w => w.deploymentId === deploymentId && w.dimensionName === dimensionName)
      .sort((a, b) => a.startTime.getTime() - b.startTime.getTime())
      .slice(-windowCount);

    if (windows.length < 2) {
      return { windows, trend: 'unknown' };
    }

    const passRates = windows.map(w => w.passRate);
    const deltaFromFirst = passRates[passRates.length - 1] - passRates[0];
    const avgDelta = passRates.slice(1).reduce((sum, rate, idx) => {
      return sum + (rate - passRates[idx]);
    }, 0) / (passRates.length - 1);

    let trend: 'improving' | 'stable' | 'degrading' | 'unknown' = 'unknown';
    if (Math.abs(avgDelta) < 0.02) {
      trend = 'stable'; // Within 2% variation
    } else if (avgDelta > 0) {
      trend = 'improving';
    } else {
      trend = 'degrading';
    }

    return { windows, trend };
  }

  /**
   * Generate a summary report for a dimension.
   */
  getSummary(deploymentId: string, dimensionName: string): {
    latestStatus: MeasurementStatus;
    passRate: number;
    trend: string;
    windowCount: number;
  } {
    const windows = Array.from(this.windows.values())
      .filter(w => w.deploymentId === deploymentId && w.dimensionName === dimensionName)
      .sort((a, b) => b.startTime.getTime() - a.startTime.getTime());

    if (windows.length === 0) {
      return {
        latestStatus: MeasurementStatus.NOT_YET_MEASURABLE,
        passRate: 0,
        trend: 'no_data',
        windowCount: 0,
      };
    }

    const latest = windows[0];
    const { trend } = this.getTrend(deploymentId, dimensionName, 3);

    // Find latest status
    const statuses = Array.from(this.statuses.values())
      .filter(s => s.windowId === latest.windowId && s.dimensionName === dimensionName)
      .sort((a, b) => b.computedAt.getTime() - a.computedAt.getTime());

    const latestStatus = statuses[0]?.status ?? MeasurementStatus.NOT_YET_MEASURABLE;

    return {
      latestStatus,
      passRate: latest.passRate,
      trend,
      windowCount: windows.length,
    };
  }
}
