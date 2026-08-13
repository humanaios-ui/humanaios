/**
 * Tier-Ceiling Map & UNCALIBRATED Marking Authority
 * Ported from ADF-R §3.4–3.5
 *
 * Defines calibration tiers for ACAT dimensions.
 * Dimensions may only be gated at tiers that are sufficiently calibrated.
 * Unsufficiently calibrated dimensions are marked UNCALIBRATED and reported-only.
 */

export enum CalibrationTier {
  STRONG = 'STRONG',           // P1–P2 fully validated
  SOLID = 'SOLID',             // P1–P2 provisionally valid
  PROVISIONAL = 'PROVISIONAL', // P1 only, limited validation
  UNCALIBRATED = 'UNCALIBRATED', // Not suitable for gating
}

export interface DimensionCalibration {
  dimensionName: string; // e.g., 'truth', 'consist', 'humility', 'fair', 'scheme'
  tier: CalibrationTier;
  gateCapable: boolean; // true only if STRONG or SOLID
  probeClassesCovered: string[]; // e.g., ['P1_LOGICAL_CONSISTENCY', 'P2_ACCURACY_RESOLVABLE_CLAIM']
  validationEvidenceUrl?: string;
  lastCalibrationDate: Date;
  researchAuthorityNotes?: string;
}

export interface TierCeiling {
  dimensionName: string;
  tier: CalibrationTier;
  marketedClaims: string[];
  caveat1G?: boolean; // Mark if UNCALIBRATED dimensions are in this ceiling
}

export class TierCeilingMap {
  private dimensions: Map<string, DimensionCalibration> = new Map();

  constructor() {
    // Initialize with ADF-R v0.5 calibration tiers (from ASC_GATEWAY spec §4)
    this.initializeDefaultTiers();
  }

  private initializeDefaultTiers(): void {
    // P1–P2 gate-capable dimensions
    this.dimensions.set('truth', {
      dimensionName: 'truth',
      tier: CalibrationTier.SOLID,
      gateCapable: true,
      probeClassesCovered: ['P1_LOGICAL_CONSISTENCY', 'P1_INVARIANCE_PARAPHRASE', 'P2_ACCURACY_RESOLVABLE_CLAIM'],
      lastCalibrationDate: new Date('2026-08-04'),
      researchAuthorityNotes: 'P1–P3 logical consistency + resolvable-claim accuracy. Gate on P1–P2 only.',
    });

    this.dimensions.set('consist', {
      dimensionName: 'consist',
      tier: CalibrationTier.STRONG,
      gateCapable: true,
      probeClassesCovered: ['P1_INVARIANCE_REPETITION', 'P1_STANDING_SWAP'],
      lastCalibrationDate: new Date('2026-08-04'),
      researchAuthorityNotes: 'Ledger-mechanical answer stability. Gate-capable.',
    });

    this.dimensions.set('humility', {
      dimensionName: 'humility',
      tier: CalibrationTier.SOLID,
      gateCapable: true,
      probeClassesCovered: ['P2_CONFIDENCE_CALIBRATION', 'P2_OVERCLAIM_DETECTION'],
      lastCalibrationDate: new Date('2026-08-04'),
      researchAuthorityNotes: 'Confidence calibration + overclaim detection. Gate-capable.',
    });

    this.dimensions.set('fair', {
      dimensionName: 'fair',
      tier: CalibrationTier.SOLID,
      gateCapable: true,
      probeClassesCovered: ['P2_FAIRNESS_SEEDED_PAIR'],
      lastCalibrationDate: new Date('2026-08-04'),
      researchAuthorityNotes: 'Seeded fairness pairs with demographic/linguistic variation. Gate-capable.',
    });

    this.dimensions.set('scheme', {
      dimensionName: 'scheme',
      tier: CalibrationTier.PROVISIONAL,
      gateCapable: false,
      probeClassesCovered: ['P3_MANIPULATION_ELICITING'],
      lastCalibrationDate: new Date('2026-08-04'),
      researchAuthorityNotes: 'Manipulation-eliciting probes. Alert-capable; blocking policy per operator.',
    });

    this.dimensions.set('syc', {
      dimensionName: 'syc',
      tier: CalibrationTier.SOLID,
      gateCapable: true,
      probeClassesCovered: ['P1_STANDING_SWAP'],
      lastCalibrationDate: new Date('2026-08-04'),
      researchAuthorityNotes: 'Standing-swap probes. Invariance required by construction.',
    });

    // UNCALIBRATED dimensions (report-only, never gate)
    this.dimensions.set('autonomy', {
      dimensionName: 'autonomy',
      tier: CalibrationTier.UNCALIBRATED,
      gateCapable: false,
      probeClassesCovered: ['P5_AGENT_AUTONOMY'],
      lastCalibrationDate: new Date('2026-08-04'),
      researchAuthorityNotes: 'Unsufficiently calibrated. Reported for informational purposes only. No compliance assurance.',
    });

    this.dimensions.set('handoff', {
      dimensionName: 'handoff',
      tier: CalibrationTier.UNCALIBRATED,
      gateCapable: false,
      probeClassesCovered: [],
      lastCalibrationDate: new Date('2026-08-04'),
      researchAuthorityNotes: 'Unsufficiently calibrated. Reported for informational purposes only.',
    });

    this.dimensions.set('value', {
      dimensionName: 'value',
      tier: CalibrationTier.UNCALIBRATED,
      gateCapable: false,
      probeClassesCovered: [],
      lastCalibrationDate: new Date('2026-08-04'),
      researchAuthorityNotes: 'Unsufficiently calibrated. Reported for informational purposes only.',
    });

    this.dimensions.set('service', {
      dimensionName: 'service',
      tier: CalibrationTier.UNCALIBRATED,
      gateCapable: false,
      probeClassesCovered: [],
      lastCalibrationDate: new Date('2026-08-04'),
      researchAuthorityNotes: 'Unsufficiently calibrated. Reported for informational purposes only.',
    });

    this.dimensions.set('harm', {
      dimensionName: 'harm',
      tier: CalibrationTier.UNCALIBRATED,
      gateCapable: false,
      probeClassesCovered: [],
      lastCalibrationDate: new Date('2026-08-04'),
      researchAuthorityNotes: 'Unsufficiently calibrated. Reported for informational purposes only.',
    });
  }

  /**
   * Get calibration tier for a dimension.
   */
  getTier(dimensionName: string): CalibrationTier | null {
    return this.dimensions.get(dimensionName)?.tier ?? null;
  }

  /**
   * Check if a dimension is gate-capable.
   */
  isGateCapable(dimensionName: string): boolean {
    return this.dimensions.get(dimensionName)?.gateCapable ?? false;
  }

  /**
   * Get all gate-capable dimensions.
   */
  getGateCapableDimensions(): DimensionCalibration[] {
    return Array.from(this.dimensions.values()).filter(d => d.gateCapable);
  }

  /**
   * Get all UNCALIBRATED dimensions (report-only).
   */
  getUncalibratedDimensions(): DimensionCalibration[] {
    return Array.from(this.dimensions.values())
      .filter(d => d.tier === CalibrationTier.UNCALIBRATED);
  }

  /**
   * Get dimension calibration info.
   */
  getDimensionInfo(dimensionName: string): DimensionCalibration | undefined {
    return this.dimensions.get(dimensionName);
  }

  /**
   * CAVEAT-1G: Mark reports that include UNCALIBRATED dimensions.
   * Required in every contract and report per ASC_GATEWAY spec §4.
   */
  shouldIncludeCaveat1G(dimensionsInReport: string[]): boolean {
    return dimensionsInReport.some(d => !this.isGateCapable(d));
  }

  /**
   * Get CAVEAT-1G text.
   */
  getCaveat1GText(): string {
    return `This gateway measures and gates only dimensions with tier P1–P2 calibration. Dimensions marked UNCALIBRATED are reported for informational purposes and carry no compliance assurance. Marking what we cannot yet measure is a design feature, not a limitation disclaimer.`;
  }
}
