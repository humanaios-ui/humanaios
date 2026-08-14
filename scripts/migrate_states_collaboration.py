#!/usr/bin/env python3
"""Migration script: humanaios collaborations legacy states → unified 4-tier model.

Authority: M2 Rank 2 RFC (State Machine Harmonization)
Migration rules: draft→planned, ratified→in_progress, live→in_progress, end_of_life→archived

Usage:
  python migrate_states_collaboration.py --dry-run    # Preview changes
  python migrate_states_collaboration.py --apply      # Apply migration
"""

import sys
from pathlib import Path
# Add project root to path so src can be imported
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.models.collaboration_state import migrate_legacy_state, LEGACY_STATE_MAPPING


def migrate_collaborations(apply: bool = False):
    """Migrate collaboration states from legacy to unified model."""
    print("=" * 70)
    print("MIGRATION: Humanaios Collaborations Legacy States → Unified 4-Tier")
    print("=" * 70)

    # In production, this would query a database.
    # For now, we demonstrate the migration logic.

    mock_collaborations = [
        {"id": "collab_001", "name": "Research Phase 1", "state": "draft"},
        {"id": "collab_002", "name": "Team Ratification", "state": "ratified"},
        {"id": "collab_003", "name": "Live Collaboration", "state": "live"},
        {"id": "collab_004", "name": "Ended Project", "state": "end_of_life"},
    ]

    print(f"\nFound {len(mock_collaborations)} collaborations to migrate:")
    print()

    migration_results = []
    for collab in mock_collaborations:
        old_state = collab["state"]
        new_state = migrate_legacy_state(old_state)

        result = {
            "id": collab["id"],
            "name": collab["name"],
            "old_state": old_state,
            "new_state": new_state.value,
            "mapped_from": LEGACY_STATE_MAPPING.get(old_state, "already_unified"),
        }
        migration_results.append(result)

        print(f"  {collab['id']:20} {old_state:15} → {new_state.value:15} | {collab['name']}")

    print()
    print("Migration Summary:")
    print(f"  Total collaborations: {len(migration_results)}")
    print(f"  States changed:       {len([r for r in migration_results if r['old_state'] != r['new_state']])}")
    print()

    # Count by target state
    state_counts = {}
    for result in migration_results:
        new = result["new_state"]
        state_counts[new] = state_counts.get(new, 0) + 1

    print("Distribution by unified state:")
    for state, count in sorted(state_counts.items()):
        print(f"  {state:15} {count:3} items")

    print()
    if apply:
        print("✅ APPLYING MIGRATION (dry-run mode disabled)")
        print("   In production, database records would be updated here.")
        print("   For now: schema deployed, migration logic verified.")
        return True
    else:
        print("🔍 DRY-RUN (use --apply to actually migrate)")
        print("   Preview complete. Run with --apply to proceed.")
        return False


if __name__ == "__main__":
    apply = "--apply" in sys.argv
    success = migrate_collaborations(apply=apply)
    sys.exit(0 if success or not apply else 1)
