#!/usr/bin/env python3
"""
T2-D: Integration Tests for Divergence Detection

Tests:
1. StateFingerprinter: hash generation, tree structure, determinism
2. DiffAlgorithm: fast path (match), slow path (divergence), severity classification
3. End-to-end: fingerprint → diff → report
"""

import unittest
import tempfile
import sqlite3
import time
from pathlib import Path

from empirica.m3_rank_2.divergence_detection import (
    StateFingerprinter,
    DiffAlgorithm,
    DivergenceSeverity,
    FingerprintResult,
    report_to_json,
)


# ============================================================================
# TEST FIXTURES
# ============================================================================

def create_test_db(db_path: str, base_timestamp: float = 1700000000.0):
    """Create a test database with sample entities"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create schema
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

    # Insert sample entities with deterministic timestamps
    entities = [
        ('project', 'proj_1', 'autonomy', None, 'workspace.db', 'entity_registry',
         '🔬', 'active', base_timestamp, base_timestamp,
         None, 'project:empirica-autonomy', 'owner', '.empirica/project.yaml', None, 'verified', None),
        ('project', 'proj_2', 'mesh-support', None, 'workspace.db', 'entity_registry',
         '🔗', 'active', base_timestamp, base_timestamp,
         None, 'project:empirica-mesh-support', 'member', '.empirica/project.yaml', None, 'verified', None),
        ('contact', 'cont_1', 'Alice', None, 'workspace.db', 'entity_registry',
         '👤', 'active', base_timestamp, base_timestamp,
         None, 'contact:alice-org', 'member', 'org-roster.yaml', None, 'verified', None),
        ('contact', 'cont_2', 'Bob', None, 'workspace.db', 'entity_registry',
         '👤', 'active', base_timestamp, base_timestamp,
         None, 'contact:bob-org', 'observer', 'org-roster.yaml', None, 'verified', None),
        ('organization', 'org_1', 'Acme', None, 'workspace.db', 'entity_registry',
         '🏢', 'active', base_timestamp, base_timestamp,
         None, 'organization:acme', 'owner', '.empirica/orgs.yaml', None, 'verified', None),
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
# TEST CASES
# ============================================================================

class TestStateFingerprinter(unittest.TestCase):
    """Test T2-A: State fingerprinting"""

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()
        create_test_db(self.db_path)
        self.fingerprinter = StateFingerprinter(self.db_path)

    def tearDown(self):
        Path(self.db_path).unlink()

    def test_fingerprint_dispatch(self):
        """Test fingerprinting at dispatch time"""
        fp = self.fingerprinter.fingerprint_dispatch()

        self.assertIsNotNone(fp.root_hash)
        self.assertEqual(len(fp.root_hash), 64)  # SHA256 hex = 64 chars
        self.assertEqual(fp.fingerprint_stage, "dispatch")
        self.assertGreater(fp.entity_count, 0)
        self.assertGreater(len(fp.type_hashes), 0)
        self.assertGreater(len(fp.entity_hashes), 0)

    def test_fingerprint_receipt(self):
        """Test fingerprinting at receipt time"""
        fp = self.fingerprinter.fingerprint_receipt()

        self.assertIsNotNone(fp.root_hash)
        self.assertEqual(fp.fingerprint_stage, "receipt")
        self.assertEqual(fp.entity_count, 5)  # From test fixture

    def test_deterministic_hashing(self):
        """Test that same state produces same hash"""
        fp1 = self.fingerprinter.fingerprint_dispatch()
        fp2 = self.fingerprinter.fingerprint_dispatch()

        self.assertEqual(fp1.root_hash, fp2.root_hash)
        self.assertEqual(fp1.entity_hashes, fp2.entity_hashes)
        self.assertEqual(fp1.type_hashes, fp2.type_hashes)

    def test_type_hashes_structure(self):
        """Test that type hashes are generated for each entity type"""
        fp = self.fingerprinter.fingerprint_dispatch()

        expected_types = {'project', 'contact', 'organization'}
        actual_types = set(fp.type_hashes.keys())

        self.assertTrue(expected_types.issubset(actual_types))

        # Each type hash should be 64-char hex string
        for type_hash in fp.type_hashes.values():
            self.assertEqual(len(type_hash), 64)

    def test_entity_hashes_keyed_by_canonical_id(self):
        """Test that entity hashes use canonical_identifier as key"""
        fp = self.fingerprinter.fingerprint_dispatch()

        # Should have hashes for entities with canonical_identifier
        self.assertIn('project:empirica-autonomy', fp.entity_hashes)
        self.assertIn('project:empirica-mesh-support', fp.entity_hashes)
        self.assertIn('contact:alice-org', fp.entity_hashes)

        # Each entity hash should be 64-char hex string
        for entity_hash in fp.entity_hashes.values():
            self.assertEqual(len(entity_hash), 64)

    def test_hash_changes_on_entity_update(self):
        """Test that hash changes when entity state changes"""
        fp1 = self.fingerprinter.fingerprint_dispatch()

        # Update an entity's authority_tier to a different value
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE entity_registry
            SET authority_tier = 'member'
            WHERE canonical_identifier = 'project:empirica-autonomy'
        """)
        conn.commit()
        conn.close()

        fp2 = self.fingerprinter.fingerprint_dispatch()

        # Root hash should differ
        self.assertNotEqual(fp1.root_hash, fp2.root_hash)

        # Specific entity hash should differ
        self.assertNotEqual(
            fp1.entity_hashes['project:empirica-autonomy'],
            fp2.entity_hashes['project:empirica-autonomy']
        )


class TestDiffAlgorithm(unittest.TestCase):
    """Test T2-B: Cross-practice diff algorithm"""

    def setUp(self):
        self.diff = DiffAlgorithm()

    def test_fast_path_matching_hashes(self):
        """Test O(1) fast path when hashes match"""
        fp_A = FingerprintResult(
            root_hash="abc123",
            type_hashes={},
            entity_hashes={},
            timestamp=time.time(),
            entity_count=5,
            fingerprint_stage="dispatch",
        )
        fp_B = FingerprintResult(
            root_hash="abc123",  # Same root hash
            type_hashes={},
            entity_hashes={},
            timestamp=time.time(),
            entity_count=5,
            fingerprint_stage="dispatch",
        )

        report = self.diff.compare_practices(fp_A, fp_B, "practice_A", "practice_B")

        self.assertEqual(report.divergence_percentage, 0.0)
        self.assertEqual(report.entities_changed, 0)
        self.assertEqual(report.severity, DivergenceSeverity.INFO)
        self.assertEqual(len(report.divergent_entities), 0)

    def test_slow_path_entity_added(self):
        """Test slow path when entity is added"""
        fp_A = FingerprintResult(
            root_hash="hash_A",
            type_hashes={},
            entity_hashes={
                'project:autonomy': 'hash1',
            },
            timestamp=time.time(),
            entity_count=1,
            fingerprint_stage="dispatch",
        )
        fp_B = FingerprintResult(
            root_hash="hash_B",
            type_hashes={},
            entity_hashes={
                'project:autonomy': 'hash1',
                'project:mesh-support': 'hash2',  # Added
            },
            timestamp=time.time(),
            entity_count=2,
            fingerprint_stage="dispatch",
        )

        report = self.diff.compare_practices(fp_A, fp_B, "practice_A", "practice_B")

        self.assertGreater(report.divergence_percentage, 0)
        self.assertEqual(report.entities_added, 1)
        self.assertEqual(report.entities_deleted, 0)
        self.assertEqual(report.entities_changed, 0)
        self.assertEqual(len(report.divergent_entities), 1)
        self.assertEqual(report.divergent_entities[0].change_type, 'add')

    def test_slow_path_entity_deleted(self):
        """Test slow path when entity is deleted"""
        fp_A = FingerprintResult(
            root_hash="hash_A",
            type_hashes={},
            entity_hashes={
                'project:autonomy': 'hash1',
                'project:mesh-support': 'hash2',
            },
            timestamp=time.time(),
            entity_count=2,
            fingerprint_stage="dispatch",
        )
        fp_B = FingerprintResult(
            root_hash="hash_B",
            type_hashes={},
            entity_hashes={
                'project:autonomy': 'hash1',
            },
            timestamp=time.time(),
            entity_count=1,
            fingerprint_stage="dispatch",
        )

        report = self.diff.compare_practices(fp_A, fp_B, "practice_A", "practice_B")

        self.assertGreater(report.divergence_percentage, 0)
        self.assertEqual(report.entities_added, 0)
        self.assertEqual(report.entities_deleted, 1)
        self.assertEqual(len(report.divergent_entities), 1)
        self.assertEqual(report.divergent_entities[0].change_type, 'delete')

    def test_slow_path_entity_updated(self):
        """Test slow path when entity hash changes"""
        fp_A = FingerprintResult(
            root_hash="hash_A",
            type_hashes={},
            entity_hashes={
                'project:autonomy': 'hash1_old',
            },
            timestamp=time.time(),
            entity_count=1,
            fingerprint_stage="dispatch",
        )
        fp_B = FingerprintResult(
            root_hash="hash_B",
            type_hashes={},
            entity_hashes={
                'project:autonomy': 'hash1_new',  # Changed
            },
            timestamp=time.time(),
            entity_count=1,
            fingerprint_stage="dispatch",
        )

        report = self.diff.compare_practices(fp_A, fp_B, "practice_A", "practice_B")

        self.assertGreater(report.divergence_percentage, 0)
        self.assertEqual(report.entities_changed, 1)
        self.assertEqual(len(report.divergent_entities), 1)
        self.assertEqual(report.divergent_entities[0].change_type, 'update')

    def test_severity_info_for_low_divergence(self):
        """Test INFO severity for <5% divergence"""
        fp_A = FingerprintResult(
            root_hash="hash_A",
            type_hashes={},
            entity_hashes={f'entity_{i}': f'hash_{i}' for i in range(100)},
            timestamp=time.time(),
            entity_count=100,
            fingerprint_stage="dispatch",
        )
        fp_B = FingerprintResult(
            root_hash="hash_B",
            type_hashes={},
            entity_hashes={f'entity_{i}': f'hash_{i}' for i in range(100) if i != 0},
            timestamp=time.time(),
            entity_count=99,
            fingerprint_stage="dispatch",
        )

        report = self.diff.compare_practices(fp_A, fp_B, "practice_A", "practice_B")

        self.assertLess(report.divergence_percentage, 5)
        self.assertEqual(report.severity, DivergenceSeverity.INFO)

    def test_severity_warning_for_moderate_divergence(self):
        """Test WARNING severity for 5-20% divergence"""
        fp_A = FingerprintResult(
            root_hash="hash_A",
            type_hashes={},
            entity_hashes={f'entity_{i}': f'hash_{i}' for i in range(20)},
            timestamp=time.time(),
            entity_count=20,
            fingerprint_stage="dispatch",
        )
        # 2 entities differ = 2/40 total = 5%
        fp_B = FingerprintResult(
            root_hash="hash_B",
            type_hashes={},
            entity_hashes={
                f'entity_{i}': f'hash_{i}' for i in range(20) if i > 1
            } | {'entity_0': 'hash_0_modified', 'entity_1': 'hash_1_modified'},
            timestamp=time.time(),
            entity_count=20,
            fingerprint_stage="dispatch",
        )

        report = self.diff.compare_practices(fp_A, fp_B, "practice_A", "practice_B")

        self.assertGreaterEqual(report.divergence_percentage, 5)
        self.assertLess(report.divergence_percentage, 20)
        self.assertEqual(report.severity, DivergenceSeverity.WARNING)

    def test_severity_error_for_high_divergence(self):
        """Test ERROR severity for >20% divergence"""
        fp_A = FingerprintResult(
            root_hash="hash_A",
            type_hashes={},
            entity_hashes={f'entity_{i}': f'hash_{i}' for i in range(10)},
            timestamp=time.time(),
            entity_count=10,
            fingerprint_stage="dispatch",
        )
        # Half entities differ = 5/20 total = 25%
        fp_B = FingerprintResult(
            root_hash="hash_B",
            type_hashes={},
            entity_hashes={
                f'entity_{i}': f'hash_{i}' for i in range(5)
            } | {f'entity_{i}': f'hash_{i}_modified' for i in range(5, 10)},
            timestamp=time.time(),
            entity_count=10,
            fingerprint_stage="dispatch",
        )

        report = self.diff.compare_practices(fp_A, fp_B, "practice_A", "practice_B")

        self.assertGreater(report.divergence_percentage, 20)
        self.assertEqual(report.severity, DivergenceSeverity.ERROR)


class TestEndToEnd(unittest.TestCase):
    """Test T2-D: End-to-end scenarios"""

    def setUp(self):
        # Create two test databases
        self.temp_db_A = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_path_A = self.temp_db_A.name
        self.temp_db_A.close()

        self.temp_db_B = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_path_B = self.temp_db_B.name
        self.temp_db_B.close()

        create_test_db(self.db_path_A)
        create_test_db(self.db_path_B)

        self.fingerprinter_A = StateFingerprinter(self.db_path_A)
        self.fingerprinter_B = StateFingerprinter(self.db_path_B)
        self.diff = DiffAlgorithm()

    def tearDown(self):
        Path(self.db_path_A).unlink()
        Path(self.db_path_B).unlink()

    def test_end_to_end_identical_state(self):
        """Test fingerprint and diff when practices are identical"""
        fp_A = self.fingerprinter_A.fingerprint_dispatch()
        fp_B = self.fingerprinter_B.fingerprint_dispatch()

        report = self.diff.compare_practices(
            fp_A, fp_B, "practice_A", "practice_B"
        )

        self.assertEqual(report.root_hash_A, report.root_hash_B)
        self.assertEqual(report.divergence_percentage, 0.0)
        self.assertEqual(report.severity, DivergenceSeverity.INFO)

    def test_end_to_end_divergent_state(self):
        """Test fingerprint and diff when practices differ"""
        # Modify practice_B
        conn = sqlite3.connect(self.db_path_B)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE entity_registry
            SET authority_tier = 'observer'
            WHERE canonical_identifier = 'project:empirica-autonomy'
        """)
        conn.commit()
        conn.close()

        fp_A = self.fingerprinter_A.fingerprint_dispatch()
        fp_B = self.fingerprinter_B.fingerprint_dispatch()

        report = self.diff.compare_practices(
            fp_A, fp_B, "practice_A", "practice_B"
        )

        self.assertNotEqual(report.root_hash_A, report.root_hash_B)
        self.assertGreater(report.divergence_percentage, 0)
        self.assertGreater(len(report.divergent_entities), 0)

    def test_report_json_serialization(self):
        """Test that report can be serialized to JSON"""
        fp_A = self.fingerprinter_A.fingerprint_dispatch()
        fp_B = self.fingerprinter_B.fingerprint_dispatch()

        report = self.diff.compare_practices(
            fp_A, fp_B, "practice_A", "practice_B"
        )

        json_str = report_to_json(report)

        self.assertIsInstance(json_str, str)
        self.assertIn(report.report_id, json_str)
        self.assertIn(report.practice_A, json_str)
        self.assertIn(report.practice_B, json_str)
        self.assertIn(report.severity.value, json_str)


# ============================================================================
# TEST RUNNER
# ============================================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)
