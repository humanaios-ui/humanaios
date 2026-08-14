/**
 * Probe Taxonomy — P1–P5 Classification System
 * Ported from ADF-R §3.5
 *
 * Probes categorized by resolution boundary: what ground truth can mechanically verify.
 * ASC_GATEWAY gates only on P1–P2; P3 advisory; P4–P5 suspended.
 */

export enum ProbeClass {
  // P1: Mechanical — ground truth embedded in probe structure
  P1_LOGICAL_CONSISTENCY = 'P1_LOGICAL_CONSISTENCY',
  P1_STANDING_SWAP = 'P1_STANDING_SWAP',
  P1_INVARIANCE_PARAPHRASE = 'P1_INVARIANCE_PARAPHRASE',
  P1_INVARIANCE_REPETITION = 'P1_INVARIANCE_REPETITION',

  // P2: Resolvable — human-adjudicated on bounded referent
  P2_ACCURACY_RESOLVABLE_CLAIM = 'P2_ACCURACY_RESOLVABLE_CLAIM',
  P2_CONFIDENCE_CALIBRATION = 'P2_CONFIDENCE_CALIBRATION',
  P2_OVERCLAIM_DETECTION = 'P2_OVERCLAIM_DETECTION',
  P2_FAIRNESS_SEEDED_PAIR = 'P2_FAIRNESS_SEEDED_PAIR',

  // P3: Advisory — human-dependent validity, no ground truth objective
  P3_MANIPULATION_ELICITING = 'P3_MANIPULATION_ELICITING',
  P3_CAPTURE_SHAPING = 'P3_CAPTURE_SHAPING',

  // P4–P5: Suspended (research-only in ADF-R)
  P4_CONSTRUCT_VALIDITY = 'P4_CONSTRUCT_VALIDITY',
  P5_AGENT_AUTONOMY = 'P5_AGENT_AUTONOMY',
}

export interface ProbeOrigin {
  classId: ProbeClass;
  probeId: string;
  description: string;
  resolutionBoundary: 'mechanical' | 'resolvable' | 'human-dependent' | 'research';
  timeCreated: Date;
  version: string;
}

export interface ProbeResult {
  probeId: string;
  classId: ProbeClass;
  targetTuple: string; // agent-as-tuple identifier
  inputText: string;
  expectedOutput?: string;
  actualOutput: string;
  gradePass: boolean;
  confidenceScore?: number;
  timestamp: Date;
  adjudicatorNotes?: string;
  adjudicatorId?: string;
}

export class ProbeRegistry {
  private probes: Map<string, ProbeOrigin> = new Map();
  private results: ProbeResult[] = [];

  /**
   * Register a probe in the taxonomy.
   * Probes are immutable once registered; versioning via new probeId.
   */
  registerProbe(origin: ProbeOrigin): void {
    if (this.probes.has(origin.probeId)) {
      throw new Error(`Probe ${origin.probeId} already registered`);
    }
    this.probes.set(origin.probeId, origin);
  }

  /**
   * Retrieve probe definition by ID.
   */
  getProbe(probeId: string): ProbeOrigin | undefined {
    return this.probes.get(probeId);
  }

  /**
   * Get all probes of a specific class (e.g., all P1 probes).
   */
  getProbesByClass(classId: ProbeClass): ProbeOrigin[] {
    return Array.from(this.probes.values()).filter(p => p.classId === classId);
  }

  /**
   * Get gate-capable probes (P1–P2 only).
   */
  getGateCapableProbes(): ProbeOrigin[] {
    const gateable = [
      'P1_LOGICAL_CONSISTENCY',
      'P1_STANDING_SWAP',
      'P1_INVARIANCE_PARAPHRASE',
      'P1_INVARIANCE_REPETITION',
      'P2_ACCURACY_RESOLVABLE_CLAIM',
      'P2_CONFIDENCE_CALIBRATION',
      'P2_OVERCLAIM_DETECTION',
      'P2_FAIRNESS_SEEDED_PAIR',
    ];
    return Array.from(this.probes.values()).filter(p =>
      gateable.some(g => p.classId.toString().includes(g))
    );
  }

  /**
   * Record a probe result (used by measurement runner).
   */
  recordResult(result: ProbeResult): void {
    this.results.push(result);
  }

  /**
   * Query results for a specific target (agent-as-tuple).
   */
  getResultsForTarget(targetTuple: string): ProbeResult[] {
    return this.results.filter(r => r.targetTuple === targetTuple);
  }

  /**
   * Get results for a specific probe class.
   */
  getResultsByClass(classId: ProbeClass): ProbeResult[] {
    return this.results.filter(r => r.classId === classId);
  }

  /**
   * Compute pass rate for a probe class (used in measurement).
   */
  getPassRateForClass(classId: ProbeClass, targetTuple?: string): number {
    let results = this.results.filter(r => r.classId === classId);
    if (targetTuple) {
      results = results.filter(r => r.targetTuple === targetTuple);
    }
    if (results.length === 0) return 0;
    const passes = results.filter(r => r.gradePass).length;
    return passes / results.length;
  }
}
