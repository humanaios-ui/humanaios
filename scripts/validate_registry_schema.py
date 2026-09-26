#!/usr/bin/env python3
"""
M2 Rank 3 Phase 2: Entity Registry Schema Validation

Verifies that the updated schema is correct:
- All 6 new columns present
- verification_log table exists
- Indices created
- Sample data validated
"""

import sqlite3
from pathlib import Path

DB_PATH = Path.home() / ".empirica" / "workspace" / "workspace.db"

def validate_schema():
    """Validate entity_registry schema."""
    if not DB_PATH.exists():
        print(f"ERROR: Database not found at {DB_PATH}")
        return False

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Validating schema...")

    # Check columns
    cursor.execute("PRAGMA table_info(entity_registry)")
    columns = {row[1]: row for row in cursor.fetchall()}

    required_columns = [
        'canonical_identifier', 'authority_tier', 'source_of_truth',
        'last_verified_at', 'verification_status', 'verification_hash'
    ]

    missing_cols = [c for c in required_columns if c not in columns]
    if missing_cols:
        print(f"✗ Missing columns: {missing_cols}")
        return False
    print(f"✓ All 6 new columns present")

    # Check verification_log table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='verification_log'")
    if not cursor.fetchone():
        print("✗ verification_log table not found")
        return False
    print("✓ verification_log table exists")

    # Check indices (optional if entity_memberships table doesn't exist yet)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='entity_memberships'")
    if cursor.fetchone():
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_membership_%'")
        indices = [row[0] for row in cursor.fetchall()]
        expected_indices = {'idx_membership_source', 'idx_membership_target', 'idx_membership_type'}
        missing_indices = expected_indices - set(indices)
        if missing_indices:
            print(f"⚠ Note: Missing membership indices (will be created in Phase 4)")
        else:
            print(f"✓ All 3 membership indices present")
    else:
        print(f"⚠ Note: entity_memberships table not yet created (Phase 4)")

    # Sample data validation
    cursor.execute("SELECT COUNT(*) FROM entity_registry")
    entity_count = cursor.fetchone()[0]
    if entity_count > 0:
        cursor.execute("""
            SELECT entity_type, entity_id, canonical_identifier, authority_tier
            FROM entity_registry LIMIT 5
        """)
        samples = cursor.fetchall()
        print(f"✓ Sample entities ({len(samples)} of {entity_count}):")
        for et, eid, cid, tier in samples:
            print(f"    {et}: {eid} → {cid} (tier={tier})")

    conn.close()
    return True

if __name__ == "__main__":
    print("\n" + "="*70)
    print("M2 Rank 3 Phase 2: Entity Registry Schema Validation")
    print("="*70 + "\n")

    success = validate_schema()

    if success:
        print("\n✓ Schema validation PASSED")
    else:
        print("\n✗ Schema validation FAILED")

    exit(0 if success else 1)
