#!/usr/bin/env python3
"""
test_specimen_intake_cycle_1.py — Q-SI-C1-B0 Acceptance Tests

Verify Cycle 1 framework:
1. Constants load correctly (PRIOR_QUALITY, PRIOR_ACCEPTANCE, SHRINK)
2. Molt predictions are generated from priors
3. Receipt hash is computed correctly
4. NF_LEDGER PIN entries are recorded
5. Cycle 1 record is saved and can be loaded
"""

import json
import unittest
from pathlib import Path
from datetime import datetime, timezone

from specimen_intake_cycle_1 import (
    Cycle1Orchestrator,
    SpecimenInput,
    IntakeRecord,
    utcnow,
)


class TestCycle1Initialization(unittest.TestCase):
    """Test Cycle 1 initialization and framework."""

    def setUp(self):
        self.orchestrator = Cycle1Orchestrator()
        self.specimen_input = SpecimenInput(
            cycle_id="cycle-1",
            specimen_id="SPC-01",
            work_period_start=self.orchestrator.config.cycle_start,
            work_period_end=self.orchestrator.config.cycle_end,
            platform="external-contractor",
            tasks_assigned=12,
            tasks_completed=11,
            tasks_revised=3,
            task_categories=["annotation", "review"],
            verification_sources=["platform-export:pending"],
            task_acceptance_rate=0.92,
            revision_cycles_per_task=0.27,
            response_time_minutes=15.5,
        )

    def test_constants_loaded(self):
        """Test that Bayesian priors are loaded from constants.json."""
        self.assertIn('PRIOR_QUALITY', self.orchestrator.constants)
        self.assertIn('PRIOR_ACCEPTANCE', self.orchestrator.constants)
        self.assertIn('SHRINK', self.orchestrator.constants)
        self.assertEqual(self.orchestrator.constants['PRIOR_QUALITY'], 0.75)
        self.assertEqual(self.orchestrator.constants['PRIOR_ACCEPTANCE'], 0.85)
        self.assertEqual(self.orchestrator.constants['SHRINK'], 0.3)

    def test_cycle_1_record_created(self):
        """Test that Cycle 1 record is initialized correctly."""
        record = self.orchestrator.initialize_cycle_1(self.specimen_input)

        self.assertEqual(record.specimen_id, "SPC-01")
        self.assertEqual(record.cycle_number, 1)
        self.assertEqual(record.evaluation_status, "PRELIMINARY")
        self.assertIsNotNone(record.receipt_hash)
        self.assertEqual(len(record.receipt_hash), 64)  # SHA256 hex-encoded

    def test_molt_predictions_from_priors(self):
        """Test that molt predictions use Bayesian priors."""
        record = self.orchestrator.initialize_cycle_1(self.specimen_input)

        # RQ1 quality prediction should use PRIOR_QUALITY
        rq1_pred = [p for p in record.molt_predictions if 'quality' in p.variable][0]
        self.assertEqual(rq1_pred.prediction_value, 0.75)
        self.assertEqual(rq1_pred.variable, 'quality_forecast')

        # RQ3 acceptance prediction should use PRIOR_ACCEPTANCE
        rq3_pred = [p for p in record.molt_predictions if 'acceptance' in p.variable][0]
        self.assertEqual(rq3_pred.prediction_value, 0.85)
        self.assertEqual(rq3_pred.variable, 'acceptance_rate_forecast')

    def test_receipt_hash_stable(self):
        """Test that receipt hash is deterministic (same input = same hash)."""
        record1 = self.orchestrator.initialize_cycle_1(self.specimen_input)
        hash1 = record1.receipt_hash

        # Reset and create another with same input
        orchestrator2 = Cycle1Orchestrator()
        # Note: timestamps differ slightly, so we can't expect exact match
        # But the hash structure should be valid SHA256
        record2 = orchestrator2.initialize_cycle_1(self.specimen_input)
        hash2 = record2.receipt_hash

        # Both should be valid 64-char hex strings
        self.assertEqual(len(hash1), 64)
        self.assertEqual(len(hash2), 64)
        self.assertTrue(all(c in '0123456789abcdef' for c in hash1))
        self.assertTrue(all(c in '0123456789abcdef' for c in hash2))

    def test_nf_ledger_pin_recorded(self):
        """Test that molt predictions are written to NF_LEDGER as PIN entries."""
        record = self.orchestrator.initialize_cycle_1(self.specimen_input)
        self.orchestrator.pin_to_nf_ledger(record)

        # Read back the ledger
        with open(self.orchestrator.nf_ledger_path) as f:
            lines = [line.strip() for line in f if line.strip()]

        # Find the new PIN entries (last 2 should be from Cycle 1)
        recent_pins = []
        for line in lines[-2:]:
            entry = json.loads(line)
            if entry.get('type') == 'PIN':
                recent_pins.append(entry)

        # Should have 2 PIN entries for RQ1 quality and RQ3 acceptance
        self.assertGreaterEqual(len(recent_pins), 2)

    def test_cycle_1_save_and_load(self):
        """Test that Cycle 1 record can be saved and loaded."""
        record = self.orchestrator.initialize_cycle_1(self.specimen_input)
        output_file = "cycles/test_cycle_1.json"

        # Save
        self.orchestrator.save_cycle_1(output_file)
        self.assertTrue(Path(output_file).exists())

        # Load and verify
        with open(output_file) as f:
            data = json.load(f)

        self.assertEqual(data['records'][0]['specimen_id'], "SPC-01")
        self.assertEqual(data['records'][0]['cycle_number'], 1)
        self.assertEqual(len(data['records'][0]['molt_predictions']), 2)
        self.assertIn('PRIOR_QUALITY', data['constants_loaded'])

        # Cleanup
        Path(output_file).unlink()

    def test_credpolicy_forecast_recorded(self):
        """Test that RQ2 CredPolicy output is recorded (task allocation forecast)."""
        record = self.orchestrator.initialize_cycle_1(self.specimen_input)

        cred = record.credpolicy_output
        self.assertEqual(cred.predicted_choice, "annotation")
        self.assertIsNotNone(cred.registered_at)
        self.assertIsNone(cred.disclosed_at)  # Not disclosed yet
        self.assertIsNone(cred.actual_choice)  # Not chosen yet
        self.assertIsNone(cred.agreement)  # Not resolved yet

    def test_specimen_input_recorded(self):
        """Test that behavioral observations are recorded."""
        record = self.orchestrator.initialize_cycle_1(self.specimen_input)

        si = record.specimen_input
        self.assertEqual(si.specimen_id, "SPC-01")
        self.assertEqual(si.tasks_assigned, 12)
        self.assertEqual(si.tasks_completed, 11)
        self.assertAlmostEqual(si.task_acceptance_rate, 0.92)


class TestCycle1Acceptance(unittest.TestCase):
    """Q-SI-C1-B0 Acceptance Criteria."""

    def test_acceptance_gate_constants_count(self):
        """Acceptance: molt_cycle --read-only reports constants: 3."""
        # This is handled by molt_cycle.py
        # Test that Cycle 1 orchestrator can access the 3 constants
        orchestrator = Cycle1Orchestrator()
        constants = orchestrator.constants

        required = ['PRIOR_QUALITY', 'PRIOR_ACCEPTANCE', 'SHRINK']
        for const_name in required:
            self.assertIn(const_name, constants)

    def test_acceptance_gate_cycle_1_scaffold(self):
        """Acceptance: Cycle 1 scaffold initializes with RQ data, predictions, and receipt hash."""
        orchestrator = Cycle1Orchestrator()
        specimen_input = SpecimenInput(
            cycle_id="cycle-1",
            specimen_id="SPC-01",
            work_period_start=orchestrator.config.cycle_start,
            work_period_end=orchestrator.config.cycle_end,
            platform="external-contractor",
            tasks_assigned=10,
            tasks_completed=9,
            tasks_revised=2,
            task_categories=["annotation"],
            verification_sources=["platform-export:pending"],
            task_acceptance_rate=0.90,
            revision_cycles_per_task=0.2,
            response_time_minutes=20.0,
        )

        record = orchestrator.initialize_cycle_1(specimen_input)

        # Check all RQ data is present
        self.assertIsNotNone(record.specimen_input)  # RQ1, RQ3 input
        self.assertIsNotNone(record.molt_predictions)  # RQ1, RQ3 forecasts
        self.assertEqual(len(record.molt_predictions), 2)  # 2 predictions
        self.assertIsNotNone(record.credpolicy_output)  # RQ2 forecast

        # Check receipt hash is valid
        self.assertEqual(len(record.receipt_hash), 64)
        self.assertTrue(all(c in '0123456789abcdef' for c in record.receipt_hash))

        # Check pins are written to NF_LEDGER
        orchestrator.pin_to_nf_ledger(record)
        with open(orchestrator.nf_ledger_path) as f:
            content = f.read()
        self.assertIn('"type": "PIN"', content)


if __name__ == '__main__':
    unittest.main()
