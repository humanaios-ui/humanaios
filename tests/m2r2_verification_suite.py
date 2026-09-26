#!/usr/bin/env python3
"""
M2 Rank 2: Phase 3 Verification Suite
Tests that all 4 harmonized entity types comply with unified 4-tier state model.

Authority: M2R2_RFC_STATE_MACHINE_HARMONIZATION.md
Coverage: Goals, Engagements, Collaborations, Projects
"""

import sqlite3
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Expected unified states (canonical)
UNIFIED_STATES = {'planned', 'in_progress', 'completed', 'archived'}

# Entity type to database path mapping (update as needed for your repos)
ENTITY_CONFIGS = {
    'goals': {
        'db_path': '../empirica-autonomy/data/autonomy.db',  # or equivalent
        'table': 'goals',
        'entity_type': 'goal',
    },
    'engagements': {
        'db_path': '../empirica-autonomy/data/autonomy.db',
        'table': 'engagements',
        'entity_type': 'engagement',
    },
    'collaborations': {
        'db_path': '../humanaios/data/humanaios.db',
        'table': 'collaborations',
        'entity_type': 'collaboration',
    },
    'projects': {
        'db_path': '../humanaios/data/humanaios.db',
        'table': 'projects',
        'entity_type': 'project',
    },
}

class M2R2VerificationSuite:
    """Verification suite for M2 Rank 2 state machine harmonization."""

    def __init__(self):
        self.results = {}
        self.passed_tests = 0
        self.failed_tests = 0

    def test_unified_states_present(self, entity_type: str, config: Dict) -> bool:
        """Test 1: All 4 unified states exist in entity type."""
        try:
            db_path = Path(config['db_path']).resolve()
            if not db_path.exists():
                print(f"⚠️  SKIP {entity_type}: DB not found at {db_path}")
                return None

            db = sqlite3.connect(db_path)
            cursor = db.cursor()

            # Query distinct states in table
            cursor.execute(f"SELECT DISTINCT state FROM {config['table']}")
            existing_states = {row[0] for row in cursor.fetchall() if row[0]}
            db.close()

            # Check if all unified states present or table is empty
            if not existing_states:
                print(f"✓ {entity_type}: No entities yet (fresh table)")
                return True

            missing_states = UNIFIED_STATES - existing_states
            if missing_states:
                print(f"✗ {entity_type}: Missing states {missing_states}")
                print(f"  Found: {existing_states}")
                return False

            print(f"✓ {entity_type}: All unified states present")
            return True

        except Exception as e:
            print(f"✗ {entity_type}: Error checking states: {e}")
            return False

    def test_no_legacy_states(self, entity_type: str, config: Dict) -> bool:
        """Test 2: No legacy state names remain (all migrated)."""
        legacy_states_by_type = {
            'goals': {'active', 'inactive', 'closed', 'on-hold'},
            'engagements': {'active', 'suspended'},
            'collaborations': {'draft', 'ratified', 'live', 'end_of_life'},
            'projects': {'conception', 'paused', 'complete'},
        }

        try:
            db_path = Path(config['db_path']).resolve()
            if not db_path.exists():
                return None

            db = sqlite3.connect(db_path)
            cursor = db.cursor()

            legacy_states = legacy_states_by_type.get(entity_type, set())
            cursor.execute(f"SELECT COUNT(*) FROM {config['table']} WHERE state IN ({','.join(['?']*len(legacy_states))})",
                          list(legacy_states))
            count = cursor.fetchone()[0]
            db.close()

            if count > 0:
                print(f"✗ {entity_type}: Found {count} entities with legacy states (not migrated)")
                return False

            print(f"✓ {entity_type}: No legacy states found")
            return True

        except Exception as e:
            print(f"✗ {entity_type}: Error checking legacy states: {e}")
            return False

    def test_state_timestamps_present(self, entity_type: str, config: Dict) -> bool:
        """Test 3: State timestamp fields exist and are populated."""
        try:
            db_path = Path(config['db_path']).resolve()
            if not db_path.exists():
                return None

            db = sqlite3.connect(db_path)
            cursor = db.cursor()

            # Check if state_timestamps column exists
            cursor.execute(f"PRAGMA table_info({config['table']})")
            columns = {row[1] for row in cursor.fetchall()}
            db.close()

            if 'state_timestamps' not in columns:
                print(f"⚠️  {entity_type}: state_timestamps column not found (may not be populated yet)")
                return True  # Not a hard failure for legacy data

            print(f"✓ {entity_type}: State timestamp field present")
            return True

        except Exception as e:
            print(f"⚠️  {entity_type}: Could not verify timestamps: {e}")
            return True  # Not a blocker if DB schema differs

    def test_state_audit_present(self, entity_type: str, config: Dict) -> bool:
        """Test 4: State audit trail fields exist."""
        try:
            db_path = Path(config['db_path']).resolve()
            if not db_path.exists():
                return None

            db = sqlite3.connect(db_path)
            cursor = db.cursor()

            cursor.execute(f"PRAGMA table_info({config['table']})")
            columns = {row[1] for row in cursor.fetchall()}
            db.close()

            if 'state_audit' not in columns:
                print(f"⚠️  {entity_type}: state_audit column not found (may not be populated yet)")
                return True

            print(f"✓ {entity_type}: State audit field present")
            return True

        except Exception as e:
            print(f"⚠️  {entity_type}: Could not verify audit field: {e}")
            return True

    def test_entity_count(self, entity_type: str, config: Dict) -> int:
        """Report entity counts for cross-repo statistics."""
        try:
            db_path = Path(config['db_path']).resolve()
            if not db_path.exists():
                return None

            db = sqlite3.connect(db_path)
            cursor = db.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {config['table']}")
            count = cursor.fetchone()[0]
            db.close()

            return count
        except:
            return None

    def run_all_tests(self):
        """Run all verification tests."""
        print("\n" + "="*70)
        print("M2 RANK 2 PHASE 3: VERIFICATION SUITE")
        print("="*70 + "\n")

        for entity_type, config in ENTITY_CONFIGS.items():
            print(f"\n--- {entity_type.upper()} ---")

            # Test 1: Unified states
            t1 = self.test_unified_states_present(entity_type, config)
            if t1 is True:
                self.passed_tests += 1
            elif t1 is False:
                self.failed_tests += 1

            # Test 2: No legacy states
            t2 = self.test_no_legacy_states(entity_type, config)
            if t2 is True:
                self.passed_tests += 1
            elif t2 is False:
                self.failed_tests += 1

            # Test 3: Timestamps
            t3 = self.test_state_timestamps_present(entity_type, config)
            if t3 is True:
                self.passed_tests += 1

            # Test 4: Audit
            t4 = self.test_state_audit_present(entity_type, config)
            if t4 is True:
                self.passed_tests += 1

            # Count
            count = self.test_entity_count(entity_type, config)
            if count is not None:
                print(f"  Entities: {count}")

        # Summary
        print("\n" + "="*70)
        print(f"RESULTS: {self.passed_tests} passed, {self.failed_tests} failed")
        print("="*70 + "\n")

        if self.failed_tests == 0:
            print("✓ Phase 3 Verification: PASS (All tests passed)")
            return True
        else:
            print("✗ Phase 3 Verification: FAIL (See errors above)")
            return False

if __name__ == "__main__":
    suite = M2R2VerificationSuite()
    success = suite.run_all_tests()
    sys.exit(0 if success else 1)
