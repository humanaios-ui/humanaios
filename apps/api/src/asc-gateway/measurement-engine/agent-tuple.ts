/**
 * Agent-as-Tuple Identity System & Infrastructure Logging
 * Ported from ADF-R §3.3, Appendix D/E7
 *
 * The audited target is a tuple: (model_version, provider, stack_config, deployment_context).
 * Infrastructure changes are first-class logged events.
 * Version stamping enables drift detection across deployments.
 */

export interface AgentTuple {
  // Identity
  tupleId: string; // Unique identifier for this specific deployment instance
  modelName: string;
  modelVersion: string;
  modelProvider: string; // e.g., OpenAI, Anthropic, internal

  // Deployment context
  deploymentId: string;
  deploymentName: string;
  environmentName: string; // e.g., staging, production
  stackVersion: string; // Version of deployment infrastructure

  // Timestamps
  tupleCreatedAt: Date;
  tupleActivatedAt?: Date;
  tupleDeprecatedAt?: Date;

  // Metadata
  tags?: Record<string, string>;
  configurationHash: string; // Immutable hash of configuration at tuple creation
}

export interface InfrastructureChangeEvent {
  changeId: string;
  tupleId: string;
  changeType: 'model_update' | 'stack_update' | 'config_change' | 'deployment_toggle';
  description: string;
  previousValue: string;
  newValue: string;
  changedAt: Date;
  changedBy?: string; // Operator who made the change
  isLogged: boolean; // Infrastructure changes must be logged
}

export interface TupleVersionHistory {
  tupleId: string;
  currentVersion: AgentTuple;
  versionHistory: AgentTuple[];
  infrastructureChanges: InfrastructureChangeEvent[];
  lastInfrastructureChangeAt?: Date;
}

export class AgentTupleRegistry {
  private tuples: Map<string, AgentTuple> = new Map();
  private versions: Map<string, TupleVersionHistory> = new Map();
  private infrastructureLog: InfrastructureChangeEvent[] = [];

  /**
   * Register a new agent tuple (new deployment or updated model).
   */
  registerTuple(tuple: AgentTuple): void {
    this.tuples.set(tuple.tupleId, tuple);

    // Initialize or update version history
    if (!this.versions.has(tuple.deploymentId)) {
      this.versions.set(tuple.deploymentId, {
        tupleId: tuple.tupleId,
        currentVersion: tuple,
        versionHistory: [tuple],
        infrastructureChanges: [],
      });
    } else {
      const history = this.versions.get(tuple.deploymentId)!;
      history.currentVersion = tuple;
      history.versionHistory.push(tuple);
    }
  }

  /**
   * Get current tuple for a deployment.
   */
  getCurrentTuple(deploymentId: string): AgentTuple | undefined {
    const history = this.versions.get(deploymentId);
    return history?.currentVersion;
  }

  /**
   * Get full version history for a deployment.
   */
  getVersionHistory(deploymentId: string): AgentTuple[] {
    const history = this.versions.get(deploymentId);
    return history?.versionHistory ?? [];
  }

  /**
   * Log an infrastructure change event.
   * All infrastructure changes are permanent logged events (§3.3).
   */
  logInfrastructureChange(event: InfrastructureChangeEvent): void {
    event.isLogged = true;
    this.infrastructureLog.push(event);

    // Update version history
    const history = this.versions.get(event.tupleId);
    if (history) {
      history.infrastructureChanges.push(event);
      history.lastInfrastructureChangeAt = event.changedAt;
    }
  }

  /**
   * Get infrastructure changes for a tuple.
   */
  getInfrastructureChanges(tupleId: string): InfrastructureChangeEvent[] {
    return this.infrastructureLog.filter(e => e.tupleId === tupleId);
  }

  /**
   * Get infrastructure changes in a time window (for drift analysis).
   */
  getInfrastructureChangesDuring(
    deploymentId: string,
    startTime: Date,
    endTime: Date
  ): InfrastructureChangeEvent[] {
    const history = this.versions.get(deploymentId);
    if (!history) return [];
    return history.infrastructureChanges.filter(
      e => e.changedAt >= startTime && e.changedAt <= endTime
    );
  }

  /**
   * Compute configuration hash (immutable at tuple creation).
   * Used to detect unauthorized configuration drift.
   */
  computeConfigHash(config: Record<string, unknown>): string {
    const sorted = Object.keys(config)
      .sort()
      .map(k => `${k}=${JSON.stringify(config[k])}`)
      .join('|');
    // In production, use crypto.createHash('sha256')
    return `sha256:${Buffer.from(sorted).toString('base64')}`;
  }

  /**
   * Check if a tuple's configuration has drifted (hash changed).
   */
  hasConfigurationDrifted(tuple: AgentTuple, currentConfig: Record<string, unknown>): boolean {
    const currentHash = this.computeConfigHash(currentConfig);
    return currentHash !== tuple.configurationHash;
  }
}
