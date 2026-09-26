#!/usr/bin/env python3
"""
M2 Rank 3 Phase 2: Entity Registry Schema Migration

Adds 6 new columns to entity_registry for verification tracking:
- canonical_identifier (3-form: org.tenant.project)
- authority_tier (admiral|owner|member|observer)
- source_of_truth (.empirica/project.yaml, git, engagement records)
- last_verified_at (Unix timestamp)
- verification_status (synced|stale|conflict)
- verification_hash (SHA256 for change detection)

Authority: M2 Rank 3 RFC
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime

DB_PATH = Path.home() / ".empirica" / "workspace" / "workspace.db"

def get_authority_tier(entity_type):
    """Map entity_type to authority_tier."""
    mapping = {
        'project': 'owner',
        'contact': 'observer',
        'organization': 'admiral',
        'engagement': 'member',
        'user': 'observer',
    }
    return mapping.get(entity_type, 'member')

def get_source_of_truth(entity_type):
    """Map entity_type to source_of_truth."""
    mapping = {
        'project': '.empirica/project.yaml',
        'contact': 'contacts.yaml',
        'organization': 'org.yaml',
        'engagement': 'engagements.yaml',
        'user': 'git_log',
    }
    return mapping.get(entity_type, 'metadata')

def run_migration(dry_run=True):
    """Execute schema migration."""
    if not DB_PATH.exists():
        print(f"ERROR: Database not found at {DB_PATH}")
        return False

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Get current entity count
        cursor.execute("SELECT COUNT(*) FROM entity_registry")
        entity_count = cursor.fetchone()[0]
        print(f"Found {entity_count} entities in registry")

        if dry_run:
            print("\n[DRY RUN] Would execute:")
        else:
            print("\n[APPLY] Executing migration...")

        # Add new columns
        new_columns = [
            "canonical_identifier VARCHAR(255)",  # Without UNIQUE initially
            "authority_tier VARCHAR(50)",
            "source_of_truth VARCHAR(255)",
            "last_verified_at INTEGER",
            "verification_status VARCHAR(50)",
            "verification_hash VARCHAR(256)",
        ]

        for col in new_columns:
            sql = f"ALTER TABLE entity_registry ADD COLUMN {col}"
            print(f"  {sql}")
            if not dry_run:
                try:
                    cursor.execute(sql)
                except sqlite3.OperationalError as e:
                    if "duplicate column" not in str(e):
                        raise

        # Add UNIQUE constraint after populating data
        if not dry_run:
            print("  CREATE UNIQUE INDEX idx_canonical_identifier ON entity_registry(canonical_identifier)")
            try:
                cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_canonical_identifier ON entity_registry(canonical_identifier)")
            except sqlite3.OperationalError as e:
                if "unique" not in str(e).lower():
                    raise

        # Create verification_log table
        verification_log_sql = """
        CREATE TABLE IF NOT EXISTS verification_log (
            id INTEGER PRIMARY KEY,
            entity_id VARCHAR(255),
            verified_at INTEGER,
            old_status VARCHAR(50),
            new_status VARCHAR(50),
            hash_before VARCHAR(256),
            hash_after VARCHAR(256),
            notes TEXT
        )
        """
        print(f"  CREATE TABLE verification_log (...)")
        if not dry_run:
            cursor.execute(verification_log_sql)

        # Create indices (only if entity_memberships table exists)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='entity_memberships'")
        if cursor.fetchone():
            indices = [
                "CREATE INDEX IF NOT EXISTS idx_membership_source ON entity_memberships(source_entity_id)",
                "CREATE INDEX IF NOT EXISTS idx_membership_target ON entity_memberships(target_entity_id)",
                "CREATE INDEX IF NOT EXISTS idx_membership_type ON entity_memberships(relationship_type)",
            ]
            for idx in indices:
                print(f"  {idx.split('IF NOT EXISTS')[1].strip()}")
                if not dry_run:
                    try:
                        cursor.execute(idx)
                    except sqlite3.OperationalError as e:
                        if "already exists" not in str(e) and "no such column" not in str(e):
                            raise
        else:
            if not dry_run:
                print("  (entity_memberships table not found, skipping indices)")

        # Populate new fields
        if not dry_run:
            print("\nPopulating new fields...")
            cursor.execute("SELECT entity_type, entity_id, display_name FROM entity_registry")
            rows = cursor.fetchall()

            for entity_type, entity_id, display_name in rows:
                authority_tier = get_authority_tier(entity_type)
                source_of_truth = get_source_of_truth(entity_type)
                canonical_id = f"{entity_type}:{entity_id}"  # Simple form for now

                cursor.execute("""
                    UPDATE entity_registry
                    SET authority_tier = ?, source_of_truth = ?,
                        canonical_identifier = ?, verification_status = ?
                    WHERE entity_type = ? AND entity_id = ?
                """, (authority_tier, source_of_truth, canonical_id, 'synced', entity_type, entity_id))

            conn.commit()
            print(f"  Updated {len(rows)} entities")

        # Verify migration
        cursor.execute("PRAGMA table_info(entity_registry)")
        columns = [row[1] for row in cursor.fetchall()]
        new_cols_present = all(col in columns for col in [
            'canonical_identifier', 'authority_tier', 'source_of_truth',
            'last_verified_at', 'verification_status', 'verification_hash'
        ])

        if new_cols_present:
            print("\n✓ All new columns present")
            return True
        else:
            print("\n✗ Migration incomplete")
            return False

    except Exception as e:
        print(f"ERROR: {e}")
        return False
    finally:
        if not dry_run:
            conn.commit()
        conn.close()

if __name__ == "__main__":
    dry_run = "--apply" not in sys.argv
    mode = "DRY RUN" if dry_run else "APPLY"
    print(f"\n{'='*70}")
    print(f"M2 Rank 3 Phase 2: Entity Registry Schema Migration [{mode}]")
    print(f"{'='*70}\n")

    success = run_migration(dry_run=dry_run)

    if dry_run:
        print("\nRun with --apply flag to execute migration")

    sys.exit(0 if success else 1)
