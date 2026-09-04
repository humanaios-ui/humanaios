#!/usr/bin/env python3
"""
Load wisdom_database_v0.3.json into Supabase guidance_sessions table.

Parses teachings by tradition, maps to consciousness levels, stores with
cross-tradition parallels and metadata.
"""

import json
import sys
import os
from uuid import uuid4
from datetime import datetime
from typing import Dict, Any, List, Optional

try:
    import psycopg2
    from psycopg2.extras import execute_values, RealDictCursor
except ImportError:
    print("ERROR: psycopg2 not installed. Install with: pip install psycopg2-binary")
    sys.exit(1)


def load_wisdom_database(db_url: str, wisdom_db_path: str = "wisdom_database_v0.3.json") -> None:
    """Load wisdom_database.json into Supabase guidance_sessions table."""

    # Load wisdom database
    print(f"📖 Loading wisdom database from {wisdom_db_path}...")
    if not os.path.exists(wisdom_db_path):
        raise FileNotFoundError(f"wisdom_database not found at {wisdom_db_path}")

    with open(wisdom_db_path, 'r') as f:
        wisdom_db = json.load(f)

    # Extract metadata
    version = wisdom_db.get('version', '0.3')
    traditions_meta = wisdom_db.get('metadata', {}).get('traditions', [])
    wisdom_obj = wisdom_db.get('wisdom', {})

    print(f"✓ Loaded wisdom_database v{version}")
    print(f"✓ Traditions: {', '.join(traditions_meta)}")

    # Connect to Supabase
    print(f"\n🔌 Connecting to Supabase...")
    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        print("✓ Connected")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        sys.exit(1)

    # Build teaching records
    teachings: List[Dict[str, Any]] = []
    tradition_count = {}

    for tradition_key, tradition_data in wisdom_obj.items():
        tradition_name = tradition_data.get('tradition', tradition_key)
        units = tradition_data.get('units', [])

        print(f"\n📚 Tradition: {tradition_name} ({len(units)} teachings)")
        tradition_count[tradition_name] = len(units)

        for unit in units:
            teaching = {
                'id': str(uuid4()),
                'request_id': str(uuid4()),  # Placeholder (no active request)
                'status': 'completed',
                'teaching_tradition': tradition_name,
                'teaching_title': unit.get('title', ''),
                'teaching_text': unit.get('teaching', ''),
                'teaching_source': tradition_key,
                'teaching_era': unit.get('unit_id', unit.get('id', '')),
                'parallels': json.dumps([]),  # Will populate cross-tradition later
                'confidence': 0.95,  # High confidence for canonical teachings
                'dimensions_assessed': [],
                'metadata': json.dumps({
                    'consciousness_level': unit.get('level', 0),
                    'challenge': unit.get('challenge', ''),
                    'code_mapping': unit.get('code_mapping', ''),
                    'obstacle': unit.get('obstacle', ''),
                    'unit_id': unit.get('unit_id', unit.get('id', '')),
                    'teaching_id': unit.get('id', '')
                }),
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
                'completed_at': datetime.utcnow()
            }
            teachings.append(teaching)

    print(f"\n✅ Extracted {len(teachings)} total teachings")

    # Insert into guidance_sessions
    print(f"\n📤 Inserting into guidance_sessions...")
    try:
        insert_query = """
            INSERT INTO guidance_sessions
            (id, request_id, status, teaching_tradition, teaching_title, teaching_text,
             teaching_source, teaching_era, parallels, confidence, dimensions_assessed,
             metadata, created_at, updated_at, completed_at)
            VALUES %s
        """

        values = [
            (
                t['id'],
                t['request_id'],
                t['status'],
                t['teaching_tradition'],
                t['teaching_title'],
                t['teaching_text'],
                t['teaching_source'],
                t['teaching_era'],
                t['parallels'],
                t['confidence'],
                t['dimensions_assessed'],
                t['metadata'],
                t['created_at'],
                t['updated_at'],
                t['completed_at']
            )
            for t in teachings
        ]

        execute_values(cursor, insert_query, values, page_size=100)
        conn.commit()
        print(f"✓ Inserted {len(teachings)} teachings")

    except Exception as e:
        conn.rollback()
        print(f"❌ Insert failed: {e}")
        cursor.close()
        conn.close()
        sys.exit(1)

    # Verify load
    print(f"\n🔍 Verifying load...")
    try:
        cursor.execute("""
            SELECT
                COUNT(*) as total,
                COUNT(DISTINCT teaching_tradition) as traditions,
                MIN(metadata::jsonb->>'consciousness_level')::int as min_level,
                MAX(metadata::jsonb->>'consciousness_level')::int as max_level
            FROM guidance_sessions
            WHERE status = 'completed' AND teaching_text IS NOT NULL
        """)
        result = cursor.fetchone()

        print(f"✓ Total teachings: {result['total']}")
        print(f"✓ Traditions: {result['traditions']}")
        print(f"✓ Consciousness range: {result['min_level']}-{result['max_level']}")

        # Show breakdown by tradition
        cursor.execute("""
            SELECT teaching_tradition, COUNT(*) as count
            FROM guidance_sessions
            WHERE status = 'completed'
            GROUP BY teaching_tradition
            ORDER BY teaching_tradition
        """)
        print(f"\n📊 Breakdown by tradition:")
        for row in cursor.fetchall():
            print(f"   • {row['teaching_tradition']}: {row['count']} teachings")

    except Exception as e:
        print(f"⚠️  Verification query failed: {e}")

    cursor.close()
    conn.close()
    print(f"\n✅ Load complete!")


if __name__ == '__main__':
    # Get Supabase DATABASE_URL from environment
    db_url = os.environ.get('SUPABASE_DATABASE_URL')
    if not db_url:
        print("ERROR: SUPABASE_DATABASE_URL environment variable not set")
        print("\nSet it with:")
        print("  export SUPABASE_DATABASE_URL='postgresql://postgres:password@project.supabase.co:5432/postgres'")
        sys.exit(1)

    wisdom_db_path = sys.argv[1] if len(sys.argv) > 1 else 'wisdom_database_v0.3.json'

    load_wisdom_database(db_url, wisdom_db_path)
