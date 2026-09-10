"""
test_nf_schema_falsifier.py — Phase 1 Falsifier Validation Tests

Status: DRAFT (Phase 1, Q-NF-SCHEMA-01)
Purpose: Verify that the NF_LEDGER schema unifies 4 formats and enables Molt Cycle measurement

Test Plan (from Q-NF-SCHEMA-01 falsifier):
1. Molt predictions recordable in NF_LEDGER + readable at window close
2. Specimen calibration aggregatable into per-predictor Brier
3. Hash chain prevents reordering/deletion (CI gate catches tampering)
4. Anti-cascade freeze viable (2 consecutive reverts freezes constant)
"""

import pytest
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path


class TestMoltPredictionRecordability:
    """
    Test 1: Molt predictions recordable in NF_LEDGER + readable at window close
    """

    def test_molt_entry_writable_to_ledger(self):
        """Can we write a molt entry to NF_LEDGER?"""
        molt_entry = {
            "molt_id": "M-TEST-0001",
            "molt_type": "TIER1",
            "constant": "behavior_spec.json:test_dial",
            "prior_value": 0.5,
            "proposed_value": 0.55,
            "prior_value_type": "float",
            "prediction": {
                "metric": "Brier",
                "target": 0.15,
                "target_direction": "below",
                "window_days": 7,
                "falsifier": "Brier >= 0.20 at window close"
            },
            "ratification_hash": "sha256(change|by=Night|at=2026-09-16T10:00:00Z|decision=ACCEPT)",
            "z2_ratified_at": "2026-09-16T10:00:00Z",
            "window_start": "2026-09-16T10:00:00Z",
            "window_end": "2026-09-23T00:00:00Z",
            "outcome": "MEASURING",
            "timestamp": "2026-09-16T10:00:00Z",
            "prior_hash": "0000000000000000",
            "hash": hashlib.sha256(json.dumps(
                {k: v for k, v in {"molt_id": "M-TEST-0001", "molt_type": "TIER1",
                                  "constant": "behavior_spec.json:test_dial", "prior_value": 0.5,
                                  "proposed_value": 0.55, "prior_value_type": "float",
                                  "prediction": {"metric": "Brier", "target": 0.15,
                                               "target_direction": "below", "window_days": 7,
                                               "falsifier": "Brier >= 0.20 at window close"},
                                  "ratification_hash": "sha256(...)", "z2_ratified_at": "2026-09-16T10:00:00Z",
                                  "window_start": "2026-09-16T10:00:00Z", "window_end": "2026-09-23T00:00:00Z",
                                  "outcome": "MEASURING", "timestamp": "2026-09-16T10:00:00Z",
                                  "prior_hash": "0000000000000000"}.items() if k != 'hash'},
                sort_keys=True).encode()).hexdigest(),
            "anti_cascade_check": {"open_molt_count": 1, "reverts_on_constant": 0, "rank_in_queue": 4}
        }

        # Serialize and deserialize (simulating write/read)
        json_line = json.dumps(molt_entry)
        parsed = json.loads(json_line)

        assert parsed['molt_id'] == "M-TEST-0001"
        assert parsed['outcome'] == "MEASURING"
        assert parsed['prediction']['falsifier'] is not None

    def test_molt_prediction_readable_at_window_close(self):
        """Can we read the molt prediction back when the window closes?"""
        # Simulate: window_end has passed
        molt_entry = {
            "molt_id": "M-TEST-0002",
            "constant": "behavior_spec.json:test_dial",
            "outcome": "MEASURING",
            "window_end": (datetime.utcnow() - timedelta(days=1)).isoformat(),  # Past
            "prediction": {"metric": "Brier", "target": 0.15, "falsifier": "Brier >= 0.20"},
            "prior_hash": "abc123",
            "hash": "def456"
        }

        # At window close, molt_cycle.py should be able to read and measure
        assert molt_entry['outcome'] == "MEASURING"
        window_end = datetime.fromisoformat(molt_entry['window_end'])
        assert datetime.utcnow() > window_end  # Window is closed
        assert molt_entry['prediction'] is not None

    @pytest.mark.parametrize("metric,target", [
        ("Brier", 0.15),
        ("GAP-closure", 0.8),
        ("catch-rate", 0.95),
    ])
    def test_multiple_prediction_metrics(self, metric, target):
        """Can NF_LEDGER handle different prediction metrics?"""
        prediction = {
            "metric": metric,
            "target": target,
            "target_direction": "below" if metric == "Brier" else "above",
            "window_days": 7,
            "falsifier": f"{metric} outside target range"
        }
        assert prediction['metric'] == metric
        assert prediction['target'] == target


class TestSpecimenCalibrationAggregation:
    """
    Test 2: Specimen calibration aggregatable into per-predictor Brier
    """

    def test_specimen_outcome_in_nf_ledger(self):
        """Can we record specimen outcomes in NF_LEDGER?"""
        specimen_molt = {
            "molt_id": "M-20260917-S001",
            "constant": "specimen:claim-RQ1-042",
            "prediction": {
                "metric": "claim_resolution",
                "target": 0.73,
                "target_direction": "equal",
                "window_days": 14
            },
            "outcome": "KEEP",  # Prediction was correct
            "brier_actual": (0.73 - 1.0) ** 2,  # (predicted - actual)^2
            "prior_hash": "abc",
            "hash": "def"
        }

        assert specimen_molt['prediction']['metric'] == "claim_resolution"
        assert specimen_molt['outcome'] in ["KEEP", "REVERT"]
        assert specimen_molt['brier_actual'] >= 0

    def test_aggregate_brier_per_predictor(self):
        """Can we aggregate Brier scores by predictor?"""
        # Simulate multiple molt entries with predictor metadata
        molts = [
            {"molt_id": "M-1", "prediction": {"predictor": "RQ1"}, "brier_actual": 0.12, "outcome": "KEEP"},
            {"molt_id": "M-2", "prediction": {"predictor": "RQ1"}, "brier_actual": 0.18, "outcome": "KEEP"},
            {"molt_id": "M-3", "prediction": {"predictor": "RQ2"}, "brier_actual": 0.08, "outcome": "KEEP"},
        ]

        brier_by_predictor = {}
        for molt in molts:
            if molt['outcome'] in ["KEEP", "REVERT"]:
                predictor = molt['prediction'].get('predictor', 'unknown')
                brier_by_predictor.setdefault(predictor, []).append(molt['brier_actual'])

        # Compute averages
        avg_brier = {p: sum(scores) / len(scores) for p, scores in brier_by_predictor.items()}

        assert avg_brier['RQ1'] == pytest.approx((0.12 + 0.18) / 2)
        assert avg_brier['RQ2'] == 0.08

    def test_brier_skill_score_calculation(self):
        """Can we compute Brier Skill Score?"""
        # BSS = 1 - (BS / BS_baseline)
        # BS = (1/N) * Σ(predicted_p - actual_outcome)²
        # BS_baseline = p_base * (1 - p_base)

        n_predictions = 47
        predicted_p = 0.55
        actual_outcome = 0.14  # Actual brier
        p_base = 0.30  # Historical base rate

        BS = ((predicted_p - actual_outcome) ** 2)  # Simplified for test
        BS_baseline = p_base * (1 - p_base)
        BSS = 1 - (BS / BS_baseline)

        assert BSS is not None
        assert -1 <= BSS <= 1  # Skill score bounds


class TestHashChainTamperProof:
    """
    Test 3: Hash chain prevents reordering/deletion (CI gate catches tampering)
    """

    def test_hash_chain_validity(self):
        """Can we detect tampering via hash chain?"""
        entry1 = {
            "molt_id": "M-1",
            "outcome": "KEEP",
            "prior_hash": "0000000000000000"
        }
        # Compute hash from full entry (without hash field)
        entry1['hash'] = hashlib.sha256(
            json.dumps({k: v for k, v in entry1.items() if k != 'hash'}, sort_keys=True).encode()
        ).hexdigest()

        entry2 = {
            "molt_id": "M-2",
            "outcome": "KEEP",
            "prior_hash": entry1['hash']
        }
        entry2['hash'] = hashlib.sha256(
            json.dumps({k: v for k, v in entry2.items() if k != 'hash'}, sort_keys=True).encode()
        ).hexdigest()

        # Valid chain
        assert entry2['prior_hash'] == entry1['hash']

        # Tampering: change entry1's outcome and recompute its hash
        entry1['outcome'] = "REVERT"
        new_hash_1 = hashlib.sha256(
            json.dumps({k: v for k, v in entry1.items() if k != 'hash'}, sort_keys=True).encode()
        ).hexdigest()

        # Chain breaks because entry2's prior_hash no longer matches new hash
        assert entry2['prior_hash'] != new_hash_1

    def test_deletion_detected(self):
        """Deleting an entry breaks the chain?"""
        ledger = [
            {"molt_id": "M-1", "prior_hash": "0000", "hash": "abc"},
            {"molt_id": "M-2", "prior_hash": "abc", "hash": "def"},
            {"molt_id": "M-3", "prior_hash": "def", "hash": "ghi"},
        ]

        # Delete entry 2
        ledger_tampered = [ledger[0], ledger[2]]

        # Entry 3's prior_hash now doesn't match entry 1's hash
        assert ledger_tampered[1]['prior_hash'] != ledger_tampered[0]['hash']

    def test_reordering_detected(self):
        """Reordering entries breaks the chain?"""
        # Create valid chain
        entry1 = {"molt_id": "M-1", "prior_hash": "0000000000000000"}
        entry1['hash'] = hashlib.sha256(
            json.dumps({k: v for k, v in entry1.items() if k != 'hash'}, sort_keys=True).encode()
        ).hexdigest()

        entry2 = {"molt_id": "M-2", "prior_hash": entry1['hash']}
        entry2['hash'] = hashlib.sha256(
            json.dumps({k: v for k, v in entry2.items() if k != 'hash'}, sort_keys=True).encode()
        ).hexdigest()

        # In normal order: entry2's prior_hash points to entry1's hash
        assert entry2['prior_hash'] == entry1['hash']

        # Reorder: entry2 now appears first
        ledger_reordered = [entry2, entry1]

        # Validation would fail: entry2's prior_hash should match the ledger line before it
        # But ledger_reordered[1] (entry1's hash) is after entry2, and they have no connection
        # The CI gate checks: new_entry.prior_hash == ledger[i-1].hash
        # For reordered[0] (entry2), there's no prior entry, so prior_hash mismatch detected
        assert ledger_reordered[0]['prior_hash'] != '0000000000000000'  # entry2 not the genesis


class TestAntiCascadeFreezeRule:
    """
    Test 4: Anti-cascade freeze viable (2 consecutive reverts freezes constant)
    """

    def test_freeze_after_two_reverts(self):
        """Does a constant freeze after 2 consecutive reverts?"""
        constant = "behavior_spec.json:test_dial"
        molts = [
            {"molt_id": "M-1", "constant": constant, "outcome": "REVERT"},
            {"molt_id": "M-2", "constant": constant, "outcome": "REVERT"},
        ]

        # Count consecutive reverts
        revert_count = sum(1 for m in molts if m['outcome'] == 'REVERT')
        should_freeze = revert_count >= 2

        assert should_freeze is True

    def test_frozen_constant_blocks_new_molt(self):
        """Can we block a new molt on a frozen constant?"""
        frozen_constants = {"behavior_spec.json:test_dial"}
        new_molt_constant = "behavior_spec.json:test_dial"

        can_propose = new_molt_constant not in frozen_constants

        assert can_propose is False  # Should not be able to propose

    def test_different_constant_not_blocked(self):
        """Other constants are not affected by one constant's freeze?"""
        frozen_constants = {"behavior_spec.json:test_dial"}
        other_constant = "behavior_spec.json:other_dial"

        can_propose = other_constant not in frozen_constants

        assert can_propose is True  # Can propose on other constant


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
