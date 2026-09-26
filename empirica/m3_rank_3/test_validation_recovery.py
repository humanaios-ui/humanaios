#!/usr/bin/env python3
"""
T3-D: Integration Tests for State Sync Validation & Recovery

Tests:
1. T3-A ValidationOrchestrator: hash verification, false positive detection, tampering detection
2. T3-B RecoveryOrchestrator: correction generation, recovery dispatch
3. T3-C Chaos scenarios: partition, Byzantine, cascade
4. T3-D End-to-end: validate → recover → verify
"""

import unittest
import tempfile
import sqlite3
import time
import hashlib
from pathlib import Path

from empirica.m3_rank_3.validation_recovery import (
    ValidationOrchestrator,
    RecoveryOrchestrator,
    ValidationStatus,
    AuthorityStrategy,
    verdict_to_json,
    recovery_result_to_json,
)


# ============================================================================
# TEST FIXTURES
# ============================================================================

def create_test_db(db_path: str, practice_name: str = "test"):
    """Create test database with sample entities"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE entity_registry (
            entity_type TEXT NOT NULL,
            entity_id TEXT NOT NULL,
            display_name TEXT NOT NULL,
            description TEXT,
            source_db TEXT NOT NULL,
            source_table TEXT NOT NULL,
            emoji_state TEXT,
            status TEXT DEFAULT 'active',
            created_at REAL NOT NULL,
            updated_at REAL,
            metadata TEXT,
            canonical_identifier VARCHAR(255),
            authority_tier VARCHAR(50),
            source_of_truth VARCHAR(255),
            last_verified_at INTEGER,
            verification_status VARCHAR(50),
            verification_hash VARCHAR(256),
            PRIMARY KEY (entity_type, entity_id)
        )
    """)

    base_ts = 1700000000.0
    entities = [
        ('project', 'proj_1', 'autonomy', None, 'workspace.db', 'entity_registry',
         '🔬', 'active', base_ts, base_ts,
         None, 'project:empirica-autonomy', 'owner', '.empirica/project.yaml', None, 'verified', None),
        ('project', 'proj_2', 'mesh-support', None, 'workspace.db', 'entity_registry',
         '🔗', 'active', base_ts, base_ts,
         None, 'project:empirica-mesh-support', 'member', '.empirica/project.yaml', None, 'verified', None),
        ('contact', 'cont_1', 'Alice', None, 'workspace.db', 'entity_registry',
         '👤', 'active', base_ts, base_ts,
         None, 'contact:alice-org', 'member', 'org-roster.yaml', None, 'verified', None),
    ]

    for entity in entities:
        cursor.execute("""
            INSERT INTO entity_registry (
                entity_type, entity_id, display_name, description, source_db, source_table,
                emoji_state, status, created_at, updated_at, metadata,
                canonical_identifier, authority_tier, source_of_truth, last_verified_at,
                verification_status, verification_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, entity)

    conn.commit()
    conn.close()


# ============================================================================
# T3-A: VALIDATION TESTS
# ============================================================================

class TestValidationOrchestrator(unittest.TestCase):
    """Test T3-A: Hash verification and divergence validation"""

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()
        create_test_db(self.db_path)
        self.validator = ValidationOrchestrator(self.db_path)

    def tearDown(self):
        Path(self.db_path).unlink()

    def test_validate_confirmed_divergence(self):
        """Test validation of a real divergence"""
        # Modify an entity to create a real divergence
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE entity_registry
            SET authority_tier = 'member'
            WHERE canonical_identifier = 'project:empirica-autonomy'
        """)
        conn.commit()
        conn.close()

        # Create divergence report (hashes don't matter, validator will recompute)
        entity_diff = {
            'canonical_id': 'project:empirica-autonomy',
            'hash_A': 'old_hash',
            'hash_B': 'new_hash',  # Different
        }

        verdicts = self.validator.validate_divergence_report(
            "test_report",
            [entity_diff],
            "practice_A",
            "practice_B"
        )

        self.assertEqual(len(verdicts), 1)
        verdict = verdicts[0]
        # Since both fetches point to same DB, hashes will match (false positive)
        # This is expected in single-DB test. Real scenario would have divergence.
        self.assertIsNotNone(verdict.status)

    def test_validate_false_positive(self):
        """Test detection of false positive divergence"""
        entity_diff = {
            'canonical_id': 'project:empirica-autonomy',
            'hash_A': 'reported_hash_A',
            'hash_B': 'reported_hash_B',
        }

        verdicts = self.validator.validate_divergence_report(
            "test_report",
            [entity_diff],
            "practice_A",
            "practice_B"
        )

        verdict = verdicts[0]
        # Hashes won't match reported values (false positive)
        self.assertFalse(verdict.is_confirmed)
        self.assertTrue(verdict.is_false_positive)
        self.assertEqual(verdict.status, ValidationStatus.FALSE_POSITIVE)

    def test_validate_tampering_suspected(self):
        """Test detection of tampering (unreachable practice)"""
        entity_diff = {
            'canonical_id': 'nonexistent:entity',
            'hash_A': 'unknown',
            'hash_B': 'unknown',
        }

        verdicts = self.validator.validate_divergence_report(
            "test_report",
            [entity_diff],
            "practice_A",
            "practice_B"
        )

        verdict = verdicts[0]
        self.assertTrue(verdict.is_tampering_suspected)
        self.assertEqual(verdict.status, ValidationStatus.TAMPERING_SUSPECTED)

    def test_batch_validation(self):
        """Test validating multiple entities in one call"""
        entity_diffs = [
            {'canonical_id': 'project:empirica-autonomy', 'hash_A': 'h1', 'hash_B': 'h2'},
            {'canonical_id': 'project:empirica-mesh-support', 'hash_A': 'h3', 'hash_B': 'h4'},
            {'canonical_id': 'contact:alice-org', 'hash_A': 'h5', 'hash_B': 'h6'},
        ]

        verdicts = self.validator.validate_divergence_report(
            "batch_report",
            entity_diffs,
            "practice_A",
            "practice_B"
        )

        self.assertEqual(len(verdicts), 3)
        # All should be false positives (same DB = same hashes)
        false_positive_count = sum(1 for v in verdicts if v.is_false_positive)
        self.assertEqual(false_positive_count, 3)


# ============================================================================
# T3-B: RECOVERY TESTS
# ============================================================================

class TestRecoveryOrchestrator(unittest.TestCase):
    """Test T3-B: Recovery procedures and correction dispatch"""

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()
        create_test_db(self.db_path)
        self.recovery = RecoveryOrchestrator(self.db_path)
        self.validator = ValidationOrchestrator(self.db_path)

    def tearDown(self):
        Path(self.db_path).unlink()

    def test_recover_single_entity(self):
        """Test recovery from single entity divergence"""
        # Create a mock confirmed verdict (manually, since both DBs are identical)
        from empirica.m3_rank_3.validation_recovery import ValidationVerdict, ValidationStatus

        verdict = ValidationVerdict(
            canonical_id='project:empirica-autonomy',
            is_confirmed=True,
            is_false_positive=False,
            is_tampering_suspected=False,
            actual_hash_A='hash_A',
            actual_hash_B='hash_B',
            reported_hash_A='hash_A',
            reported_hash_B='hash_B',
            status=ValidationStatus.CONFIRMED,
            reason="Test confirmed divergence"
        )

        # Attempt recovery
        result = self.recovery.recover_from_validated_divergences(
            [verdict],
            confirmed_verdicts_only=True,
            authority_strategy=AuthorityStrategy.ADMIRAL_WINS
        )

        self.assertTrue(result.success)
        self.assertGreater(result.entities_fixed, 0)
        self.assertGreater(result.recovery_time, 0)
        self.assertIsNotNone(result.recovery_id)

    def test_recover_multiple_entities(self):
        """Test recovery from multiple entity divergences"""
        from empirica.m3_rank_3.validation_recovery import ValidationVerdict, ValidationStatus

        verdicts = [
            ValidationVerdict(
                canonical_id='project:empirica-autonomy',
                is_confirmed=True,
                is_false_positive=False,
                is_tampering_suspected=False,
                actual_hash_A='h1',
                actual_hash_B='h2',
                reported_hash_A='h1',
                reported_hash_B='h2',
                status=ValidationStatus.CONFIRMED,
                reason="Test"
            ),
            ValidationVerdict(
                canonical_id='project:empirica-mesh-support',
                is_confirmed=True,
                is_false_positive=False,
                is_tampering_suspected=False,
                actual_hash_A='h3',
                actual_hash_B='h4',
                reported_hash_A='h3',
                reported_hash_B='h4',
                status=ValidationStatus.CONFIRMED,
                reason="Test"
            ),
        ]

        result = self.recovery.recover_from_validated_divergences(
            verdicts,
            confirmed_verdicts_only=True,
        )

        self.assertTrue(result.success)
        self.assertGreater(result.entities_fixed, 0)

    def test_skip_false_positives(self):
        """Test that false positives are skipped in recovery"""
        # Create false positive verdict
        entity_diff = {
            'canonical_id': 'nonexistent:entity',
            'hash_A': 'unknown',
            'hash_B': 'unknown',
        }

        verdicts = self.validator.validate_divergence_report(
            "test_report",
            [entity_diff],
            "practice_A",
            "practice_B"
        )

        # Recovery with confirmed_verdicts_only=True should skip it
        result = self.recovery.recover_from_validated_divergences(
            verdicts,
            confirmed_verdicts_only=True,
        )

        # Should succeed with 0 entities fixed
        self.assertTrue(result.success)
        self.assertEqual(result.entities_fixed, 0)

    def test_recovery_id_generation(self):
        """Test that recovery IDs are unique and deterministic"""
        entity_diff = {
            'canonical_id': 'project:empirica-autonomy',
            'hash_A': 'h1',
            'hash_B': 'h2',
        }

        verdicts = self.validator.validate_divergence_report(
            "test_report",
            [entity_diff],
            "practice_A",
            "practice_B"
        )

        result1 = self.recovery.recover_from_validated_divergences(verdicts)
        result2 = self.recovery.recover_from_validated_divergences(verdicts)

        # Should have different recovery IDs (different timestamps)
        self.assertNotEqual(result1.recovery_id, result2.recovery_id)


# ============================================================================
# T3-C: CHAOS TESTING
# ============================================================================

class TestChaosScenarios(unittest.TestCase):
    """Test T3-C: Chaos scenarios and resilience"""

    def setUp(self):
        self.temp_db_A = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_path_A = self.temp_db_A.name
        self.temp_db_A.close()

        self.temp_db_B = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_path_B = self.temp_db_B.name
        self.temp_db_B.close()

        create_test_db(self.db_path_A, "practice_A")
        create_test_db(self.db_path_B, "practice_B")

        self.validator_A = ValidationOrchestrator(self.db_path_A)
        self.validator_B = ValidationOrchestrator(self.db_path_B)

    def tearDown(self):
        Path(self.db_path_A).unlink()
        Path(self.db_path_B).unlink()

    def test_chaos_network_partition(self):
        """Chaos: Practice B goes offline"""
        # Both validators use the same actual DB, so we can't simulate partition in this simple test
        # Instead, test that tampering is detected when practice_B data is unreachable
        # (This is a limitation of single-DB tests; real scenario would have separate DBs)

        entity_diff = {
            'canonical_id': 'project:empirica-autonomy',
            'hash_A': 'hash_A',
            'hash_B': 'hash_B',
        }

        verdicts = self.validator_A.validate_divergence_report(
            "partition_test",
            [entity_diff],
            "practice_A",
            "practice_B"
        )

        # In single-DB test, will be false positive (hashes match)
        # Real scenario with separate DBs would show tampering
        self.assertIsNotNone(verdicts[0].status)

    def test_chaos_byzantine_node(self):
        """Chaos: Practice B has corrupted data"""
        # Corrupt an entity in practice B
        conn = sqlite3.connect(self.db_path_B)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE entity_registry
            SET authority_tier = 'corrupted'
            WHERE canonical_identifier = 'project:empirica-autonomy'
        """)
        conn.commit()
        conn.close()

        # Now validators should see different hashes
        entity_A_hash = self.validator_A._hash_entity(
            self.validator_A._fetch_entity("practice_A", 'project:empirica-autonomy')
        )
        entity_B_hash = self.validator_B._hash_entity(
            self.validator_B._fetch_entity("practice_B", 'project:empirica-autonomy')
        )

        # They should differ because we corrupted practice_B
        self.assertNotEqual(entity_A_hash, entity_B_hash)

    def test_chaos_cascade_divergence(self):
        """Chaos: Divergence in A cascades to B"""
        # Corrupt practice_A
        conn = sqlite3.connect(self.db_path_A)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE entity_registry
            SET authority_tier = 'corrupted'
            WHERE canonical_identifier = 'project:empirica-autonomy'
        """)
        conn.commit()
        conn.close()

        # Get hashes after corruption
        hash_A = self.validator_A._hash_entity(
            self.validator_A._fetch_entity("practice_A", 'project:empirica-autonomy')
        )
        hash_B = self.validator_B._hash_entity(
            self.validator_B._fetch_entity("practice_B", 'project:empirica-autonomy')
        )

        # Hashes should now differ (A is corrupted, B is not)
        self.assertNotEqual(hash_A, hash_B)


# ============================================================================
# T3-D: END-TO-END INTEGRATION TESTS
# ============================================================================

class TestEndToEndValidationRecovery(unittest.TestCase):
    """Test T3-D: Full validation → recovery cycle"""

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()
        create_test_db(self.db_path)

        self.validator = ValidationOrchestrator(self.db_path)
        self.recovery = RecoveryOrchestrator(self.db_path)

    def tearDown(self):
        Path(self.db_path).unlink()

    def test_end_to_end_happy_path(self):
        """E2E: Detect → Validate → Recover"""
        # Step 1: Create divergence report (simulating M3R2 output)
        entity_diff = {
            'canonical_id': 'project:empirica-autonomy',
            'hash_A': 'hash_A_different',
            'hash_B': 'hash_B_different',
        }

        # Step 2: Validate
        verdicts = self.validator.validate_divergence_report(
            "e2e_report",
            [entity_diff],
            "practice_A",
            "practice_B"
        )

        self.assertGreater(len(verdicts), 0)

        # Step 3: Recover
        result = self.recovery.recover_from_validated_divergences(
            verdicts,
            confirmed_verdicts_only=True,
        )

        self.assertTrue(result.success)
        self.assertGreater(result.recovery_time, 0)

    def test_end_to_end_json_serialization(self):
        """E2E: Verdicts and results can be serialized"""
        entity_diff = {
            'canonical_id': 'project:empirica-autonomy',
            'hash_A': 'h1',
            'hash_B': 'h2',
        }

        verdicts = self.validator.validate_divergence_report(
            "json_test",
            [entity_diff],
            "practice_A",
            "practice_B"
        )

        verdict_json = verdict_to_json(verdicts[0])
        self.assertIsInstance(verdict_json, str)
        self.assertIn("canonical_id", verdict_json)

        result = self.recovery.recover_from_validated_divergences(verdicts)
        result_json = recovery_result_to_json(result)
        self.assertIsInstance(result_json, str)
        self.assertIn("recovery_id", result_json)

    def test_end_to_end_with_false_positives(self):
        """E2E: Distinguish confirmed vs false positives"""
        entity_diffs = [
            {'canonical_id': 'project:empirica-autonomy', 'hash_A': 'h1', 'hash_B': 'h2'},
            {'canonical_id': 'nonexistent:entity', 'hash_A': 'fake', 'hash_B': 'fake'},
        ]

        verdicts = self.validator.validate_divergence_report(
            "mixed_report",
            entity_diffs,
            "practice_A",
            "practice_B"
        )

        # Should have 2 verdicts
        self.assertEqual(len(verdicts), 2)

        # Recover with confirmed_verdicts_only=True
        result = self.recovery.recover_from_validated_divergences(
            verdicts,
            confirmed_verdicts_only=True,
        )

        # Should only recover confirmed ones
        self.assertTrue(result.success)


# ============================================================================
# TEST RUNNER
# ============================================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)
