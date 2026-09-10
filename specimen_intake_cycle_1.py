#!/usr/bin/env python3
"""
specimen_intake_cycle_1.py — Q-SI-C1-B0

Specimen-intake Cycle 1 initialization and orchestration.

Cycle 1 runs weekly starting 2026-09-13 through 2026-09-20 (first 7 days).
- Specimen: SPC-01 (pseudonymous; identity in private register)
- Work period: 2026-09-13 00:00 UTC to 2026-09-20 00:00 UTC
- Evaluation: Z1 compiles input, Z2 ratifies
- Constants: PRIOR_QUALITY=0.75, PRIOR_ACCEPTANCE=0.85, SHRINK=0.3
- Ledgers: NF_LEDGER records PIN predictions; molt_cycle evaluates Brier

RQ1: Does behavioral assessment predict expert task performance?
  - Hypothesis: Engagement (acceptance, revisions, velocity) forecast quality
  - Measurement: Brier over resolved forecasts; REVERT rate
  - Falsifier: Brier > 0.4 OR REVERT rate > 30%
  - Window: 30 days rolling (Cycles 1-5)

RQ2: Can resource allocation be reproduced from behavioral data?
  - Hypothesis: CredPolicy forecasts task category without discretion
  - Measurement: Agreement (predicted_choice vs actual_choice)
  - Falsifier: Agreement < 60% on 3+ consecutive cycles
  - Window: 30 days rolling (Cycles 2-5)

RQ3: Does intake evaluation improve performance (audit-as-molt)?
  - Hypothesis: Being audited raises subsequent quality
  - Measurement: Quality delta cycle-over-cycle
  - Falsifier: No improvement in 2 consecutive cycles OR rejection rate rises
  - Window: 14 days per cycle

Acceptance gate: receipt_hash ratified by Z2 (Ed25519 signature binding hash).
Publication gate: only PUBLISHED status if ratification_signature verifies.
"""

from __future__ import annotations

import json
import hashlib
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional
from pathlib import Path


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Cycle1Config:
    """Cycle 1 configuration from specimen-intake.yml."""
    specimen_id: str = "SPC-01"
    cycle_number: int = 1
    cycle_start: datetime = None
    cycle_end: datetime = None
    evaluation_lag_hours: int = 24
    z2_ratification_lag_hours: int = 48
    molt_window_days: int = 30

    def __post_init__(self):
        if self.cycle_start is None:
            # First cycle: 2026-09-13 00:00 UTC to 2026-09-20 00:00 UTC
            self.cycle_start = datetime(2026, 9, 13, 0, 0, 0, tzinfo=timezone.utc)
        if self.cycle_end is None:
            self.cycle_end = self.cycle_start + timedelta(days=7)


@dataclass
class SpecimenInput:
    """Specimen behavioral input for Cycle 1 (RQ1, RQ3 data)."""
    cycle_id: str
    specimen_id: str
    work_period_start: datetime
    work_period_end: datetime
    platform: str  # e.g., "external-contractor"
    tasks_assigned: int
    tasks_completed: int
    tasks_revised: int
    task_categories: List[str]
    verification_sources: List[str]  # e.g., ["platform-export:sha256"]

    # Behavioral observations
    task_acceptance_rate: float  # [0,1]
    revision_cycles_per_task: float
    response_time_minutes: float
    quality_score: Optional[float] = None  # [0,100] or null
    guideline_adherence: float = 1.0  # [0,1]
    annotation_variance: float = 0.0  # [0,1]
    error_rate: float = 0.0  # [0,1]

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class MoltPrediction:
    """RQ1, RQ3 molt prediction for Cycle 1."""
    prediction_id: str  # e.g., "molt-rq1-quality-c1-09-13"
    variable: str  # e.g., "quality_forecast", "acceptance_rate"
    prediction_value: float  # [0,1] normalized
    confidence: float  # [0,1]
    measurement_window_days: int
    predicted_at: datetime
    revert_rule: Dict  # {"kind": "abs_above", "threshold": 0.3}
    scale_max: float  # max raw scale
    binary: bool = False
    resolved_at: Optional[datetime] = None
    actual_value: Optional[float] = None
    brier_score: Optional[float] = None
    reverted: bool = False

    def to_dict(self) -> Dict:
        d = asdict(self)
        d['predicted_at'] = self.predicted_at.isoformat()
        if self.resolved_at:
            d['resolved_at'] = self.resolved_at.isoformat()
        return d


@dataclass
class CredPolicyOutput:
    """RQ2 credential policy forecast (task allocation) for Cycle 1."""
    priority_score: float  # [0,100]
    recommended_next_tasks: List[str]
    envelope_constraint: str
    rationale: str
    predicted_choice: str
    registered_at: datetime
    disclosed_at: Optional[datetime] = None
    actual_choice: Optional[str] = None
    actual_choice_at: Optional[datetime] = None
    agreement: Optional[bool] = None
    agreement_pre_disclosure: Optional[bool] = None

    def to_dict(self) -> Dict:
        d = asdict(self)
        d['registered_at'] = self.registered_at.isoformat()
        if self.disclosed_at:
            d['disclosed_at'] = self.disclosed_at.isoformat()
        if self.actual_choice_at:
            d['actual_choice_at'] = self.actual_choice_at.isoformat()
        return d


@dataclass
class IntakeRecord:
    """Complete Cycle 1 intake record with all RQ data, predictions, and receipt."""
    intake_id: str
    cycle_number: int
    specimen_id: str
    timestamp: datetime
    evaluator: str  # "Z1" | "Z2"
    evaluation_status: str  # PENDING | PRELIMINARY | VERIFIED | PUBLISHED | REVERTED

    specimen_input: SpecimenInput
    molt_predictions: List[MoltPrediction]
    credpolicy_output: CredPolicyOutput

    receipt_hash: str  # sha256 over COMMITMENT
    resolution_hash: Optional[str] = None
    receipt_status: str = "CLAIM"  # CLAIM | CLAIM_WITH_LINK | VERIFIED | VOID
    chain_link_prior: Optional[str] = None  # receipt_hash of prior cycle

    ratification_signature: Optional[str] = None  # Ed25519 hex-encoded
    ratified_by: Optional[str] = None
    ratified_at: Optional[datetime] = None

    def compute_receipt_hash(self) -> str:
        """SHA256 over the commitment (predictions + forecasts as issued)."""
        commitment = {
            'metadata': {
                'intake_id': self.intake_id,
                'specimen_id': self.specimen_id,
                'cycle_number': self.cycle_number,
                'timestamp': self.timestamp.isoformat(),
            },
            'specimen_input': self.specimen_input.to_dict(),
            'molt_predictions': [p.to_dict() for p in self.molt_predictions],
            'credpolicy_commitment': {
                'predicted_choice': self.credpolicy_output.predicted_choice,
                'registered_at': self.credpolicy_output.registered_at.isoformat(),
                'priority_score': self.credpolicy_output.priority_score,
            },
            'chain_link_prior': self.chain_link_prior,
        }
        commitment_json = json.dumps(commitment, sort_keys=True, default=str)
        return hashlib.sha256(commitment_json.encode()).hexdigest()

    def to_dict(self) -> Dict:
        return asdict(self)


class Cycle1Orchestrator:
    """Orchestrate Specimen-intake Cycle 1: data capture → predictions → evaluation → ratification."""

    def __init__(self, constants_path: str = "constants.json", nf_ledger_path: str = "ledgers/NF_LEDGER.jsonl"):
        self.config = Cycle1Config()
        self.constants_path = constants_path
        self.nf_ledger_path = nf_ledger_path
        self.constants = self._load_constants()
        self.records: List[IntakeRecord] = []

    def _load_constants(self) -> Dict:
        """Load PRIOR_QUALITY, PRIOR_ACCEPTANCE, SHRINK from constants.json."""
        try:
            with open(self.constants_path) as f:
                data = json.load(f)
            constants = {}
            for const in data.get('constants', []):
                constants[const['name']] = const['current_value']
            return constants
        except FileNotFoundError:
            return {'PRIOR_QUALITY': 0.75, 'PRIOR_ACCEPTANCE': 0.85, 'SHRINK': 0.3}

    def initialize_cycle_1(self, specimen_input: SpecimenInput) -> IntakeRecord:
        """Initialize Cycle 1 with specimen input and RQ predictions."""
        intake_id = f"intake-{self.config.specimen_id}-c{self.config.cycle_number}-{self.config.cycle_start.timestamp()}"

        # RQ1: Quality forecast (PRIOR_QUALITY as prior, shrink toward it)
        quality_prior = self.constants.get('PRIOR_QUALITY', 0.75)
        rq1_prediction = MoltPrediction(
            prediction_id=f"molt-rq1-quality-{intake_id}",
            variable="quality_forecast",
            prediction_value=quality_prior,  # Starting at prior
            confidence=0.6,
            measurement_window_days=30,
            predicted_at=utcnow(),
            revert_rule={"kind": "abs_above", "threshold": 0.3},  # RQ1 falsifier: Brier > 0.4
            scale_max=1.0,
            binary=False,
        )

        # RQ3: Acceptance rate forecast (PRIOR_ACCEPTANCE as prior)
        acceptance_prior = self.constants.get('PRIOR_ACCEPTANCE', 0.85)
        rq3_prediction = MoltPrediction(
            prediction_id=f"molt-rq3-acceptance-{intake_id}",
            variable="acceptance_rate_forecast",
            prediction_value=acceptance_prior,  # Starting at prior
            confidence=0.5,
            measurement_window_days=14,
            predicted_at=utcnow(),
            revert_rule={"kind": "abs_above", "threshold": 0.15},
            scale_max=1.0,
            binary=False,
        )

        # RQ2: CredPolicy (task allocation forecast)
        credpolicy = CredPolicyOutput(
            priority_score=75.0,
            recommended_next_tasks=["annotation", "review"],
            envelope_constraint="max_2_tasks_per_day",
            rationale=f"Baseline priority from PRIOR_QUALITY={quality_prior}",
            predicted_choice="annotation",
            registered_at=utcnow(),
        )

        # Compute receipt hash
        record = IntakeRecord(
            intake_id=intake_id,
            cycle_number=self.config.cycle_number,
            specimen_id=self.config.specimen_id,
            timestamp=utcnow(),
            evaluator="Z1",
            evaluation_status="PRELIMINARY",
            specimen_input=specimen_input,
            molt_predictions=[rq1_prediction, rq3_prediction],
            credpolicy_output=credpolicy,
            receipt_hash="",  # Computed below
            chain_link_prior=None,  # Cycle 1 has no prior
        )
        record.receipt_hash = record.compute_receipt_hash()

        self.records.append(record)
        return record

    def save_cycle_1(self, output_path: str = "cycles/cycle_1.json"):
        """Save Cycle 1 record to file."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        data = {
            'config': asdict(self.config),
            'constants_loaded': self.constants,
            'records': [r.to_dict() for r in self.records],
        }
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        return output_path

    def pin_to_nf_ledger(self, record: IntakeRecord):
        """Write molt predictions to NF_LEDGER as PIN entries."""
        Path(self.nf_ledger_path).parent.mkdir(parents=True, exist_ok=True)
        with open(self.nf_ledger_path, 'a') as f:
            for prediction in record.molt_predictions:
                pin_entry = {
                    'type': 'PIN',
                    'target': prediction.variable,
                    'predictor': f"specimen-intake-c{record.cycle_number}",
                    'p': prediction.prediction_value,
                    'at': prediction.predicted_at.isoformat(),
                    'molt_id': None,  # Awaiting Z2 ratification
                    'prediction_id': prediction.prediction_id,
                }
                f.write(json.dumps(pin_entry) + '\n')


# CLI for Q-SI-C1-B0 initialization
def main():
    import sys

    if len(sys.argv) < 2 or sys.argv[1] == "--help":
        print("Specimen-intake Cycle 1 Initialization (Q-SI-C1-B0)")
        print("  --init                : Initialize Cycle 1 with baseline specimen input")
        print("  --save <path>         : Save Cycle 1 to file (default: cycles/cycle_1.json)")
        return

    if sys.argv[1] == "--init":
        orchestrator = Cycle1Orchestrator()

        # Baseline specimen input for Cycle 1
        specimen_input = SpecimenInput(
            cycle_id="cycle-1",
            specimen_id="SPC-01",
            work_period_start=orchestrator.config.cycle_start,
            work_period_end=orchestrator.config.cycle_end,
            platform="external-contractor",
            tasks_assigned=12,
            tasks_completed=11,
            tasks_revised=3,
            task_categories=["annotation", "review", "verification"],
            verification_sources=["platform-export:pending"],  # CLAIM status until verified
            task_acceptance_rate=0.92,
            revision_cycles_per_task=0.27,
            response_time_minutes=15.5,
            quality_score=None,  # To be measured at cycle end
        )

        record = orchestrator.initialize_cycle_1(specimen_input)

        # Save and pin to NF_LEDGER
        output_file = sys.argv[3] if len(sys.argv) > 3 else "cycles/cycle_1.json"
        orchestrator.save_cycle_1(output_file)
        orchestrator.pin_to_nf_ledger(record)

        print(f"✓ Cycle 1 initialized")
        print(f"  Intake ID: {record.intake_id}")
        print(f"  Receipt hash: {record.receipt_hash}")
        print(f"  Molt predictions: {len(record.molt_predictions)}")
        print(f"  Saved to: {output_file}")
        print(f"  PINned to NF_LEDGER: {orchestrator.nf_ledger_path}")
        print(f"\nAwait Z2 ratification of receipt_hash: {record.receipt_hash}")


if __name__ == '__main__':
    main()
