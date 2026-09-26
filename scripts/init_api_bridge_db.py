#!/usr/bin/env python3
"""
API Bridge Database Initialization
Ensures PostgreSQL schema is ready for registry_submissions persistence.

Steps:
1. Create organizations table (if not exists)
2. Create users table (if not exists)
3. Create registry_submissions table
4. Create registry_feedback table
5. Create harness_modes table
6. Create intent_reconciliation table
7. Create all indexes
8. Test the connection with a sample query

Usage:
  python3 init_api_bridge_db.py                    # Check status
  python3 init_api_bridge_db.py --init             # Initialize tables
  python3 init_api_bridge_db.py --test             # Test connection + query
"""

import os
import sys
import psycopg2
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

def get_db_url():
    """Get DATABASE_URL from environment or .env file."""
    if os.getenv('DATABASE_URL'):
        return os.getenv('DATABASE_URL')

    # Try to load from .env file
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.startswith('DATABASE_URL='):
                    return line.split('=', 1)[1].strip().strip('"\'')

    # Fallback to .env.example
    env_example = Path(__file__).parent.parent / '.env.example'
    if env_example.exists():
        print("⚠️  No .env found. Using .env.example defaults (postgresql://user:password@localhost/empirica)")
        return 'postgresql://user:password@localhost/empirica'

    raise ValueError("DATABASE_URL not set and no .env file found")

def init_database(db_url):
    """Initialize database schema."""
    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        print(f"✓ Connected to database")

        # Enable required extensions
        print("Creating extensions...")
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"timescaledb\" CASCADE;")
        conn.commit()

        # Create core tables (organizations, users)
        print("Creating core tables...")

        # Organizations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS organizations (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                name VARCHAR(255) NOT NULL,
                slug VARCHAR(100) UNIQUE NOT NULL,
                plan VARCHAR(50) NOT NULL DEFAULT 'free',
                settings JSONB DEFAULT '{}',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

                CONSTRAINT valid_plan CHECK (plan IN ('free', 'starter', 'pro', 'enterprise'))
            );
        """)

        # Users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255),
                name VARCHAR(255),
                role VARCHAR(50) NOT NULL DEFAULT 'viewer',
                auth_provider VARCHAR(50) NOT NULL DEFAULT 'email',
                avatar_url TEXT,
                is_active BOOLEAN DEFAULT true,
                last_login_at TIMESTAMP WITH TIME ZONE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

                CONSTRAINT valid_role CHECK (role IN ('admin', 'operator', 'viewer')),
                CONSTRAINT valid_auth_provider CHECK (auth_provider IN ('email', 'google', 'github'))
            );
        """)
        conn.commit()

        # Create registry tables
        print("Creating registry tables...")

        # Registry submissions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registry_submissions (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
                record JSONB NOT NULL,
                source_id VARCHAR(255),
                attest_hash VARCHAR(255),
                source_license VARCHAR(100),
                outcome VARCHAR(50) NOT NULL,
                outcome_reason TEXT,
                score JSONB,
                pipeline_status VARCHAR(50) NOT NULL DEFAULT 'proposed',
                submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                decided_at TIMESTAMP WITH TIME ZONE,
                landed_at TIMESTAMP WITH TIME ZONE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

                CONSTRAINT valid_outcome CHECK (outcome IN ('ACCEPT', 'QUARANTINE', 'CANDIDATE')),
                CONSTRAINT valid_pipeline_status CHECK (pipeline_status IN ('proposed', 'ratified', 'landed', 'rejected'))
            );
        """)

        # Registry feedback
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registry_feedback (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
                submission_id UUID REFERENCES registry_submissions(id) ON DELETE SET NULL,
                source VARCHAR(50) NOT NULL,
                type VARCHAR(100) NOT NULL,
                severity VARCHAR(50) DEFAULT 'medium',
                message TEXT NOT NULL,
                status VARCHAR(50) DEFAULT 'open',
                resolved_at TIMESTAMP WITH TIME ZONE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

                CONSTRAINT valid_source CHECK (source IN ('user', 'machine')),
                CONSTRAINT valid_severity CHECK (severity IN ('low', 'medium', 'high', 'critical')),
                CONSTRAINT valid_status CHECK (status IN ('open', 'acknowledged', 'resolved'))
            );
        """)

        # Harness modes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS harness_modes (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
                mode VARCHAR(50) NOT NULL,
                human_allocation DECIMAL(3,2) NOT NULL,
                machine_allocation DECIMAL(3,2) NOT NULL,
                capital_allocation DECIMAL(3,2) NOT NULL,
                created_by UUID REFERENCES users(id),
                active BOOLEAN DEFAULT true,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

                CONSTRAINT valid_mode CHECK (mode IN ('balanced', 'ai-led', 'human-led', 'capital-injection', 'custom')),
                CONSTRAINT allocations_sum CHECK (human_allocation + machine_allocation + capital_allocation = 1.0)
            );
        """)

        # Intent reconciliation
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS intent_reconciliation (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
                stated_intent TEXT,
                revealed_intent TEXT,
                gap_analysis TEXT,
                measurement_date TIMESTAMP WITH TIME ZONE NOT NULL,
                gap_score DECIMAL(3,2),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
        """)

        conn.commit()
        print("✓ Tables created")

        # Create indexes
        print("Creating indexes...")
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_organizations_slug ON organizations(slug);",
            "CREATE INDEX IF NOT EXISTS idx_users_org_id ON users(org_id);",
            "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);",
            "CREATE INDEX IF NOT EXISTS idx_registry_org ON registry_submissions(org_id);",
            "CREATE INDEX IF NOT EXISTS idx_registry_outcome ON registry_submissions(outcome);",
            "CREATE INDEX IF NOT EXISTS idx_registry_status ON registry_submissions(pipeline_status);",
            "CREATE INDEX IF NOT EXISTS idx_registry_source_id ON registry_submissions(source_id);",
            "CREATE INDEX IF NOT EXISTS idx_registry_submitted_at ON registry_submissions(submitted_at DESC);",
            "CREATE INDEX IF NOT EXISTS idx_feedback_org ON registry_feedback(org_id);",
            "CREATE INDEX IF NOT EXISTS idx_feedback_submission ON registry_feedback(submission_id);",
            "CREATE INDEX IF NOT EXISTS idx_feedback_type ON registry_feedback(type);",
            "CREATE INDEX IF NOT EXISTS idx_feedback_severity ON registry_feedback(severity);",
            "CREATE INDEX IF NOT EXISTS idx_feedback_status ON registry_feedback(status);",
            "CREATE INDEX IF NOT EXISTS idx_harness_org ON harness_modes(org_id);",
        ]

        for idx in indexes:
            cursor.execute(idx)

        conn.commit()
        print("✓ Indexes created")

        # Ensure default org exists
        print("Ensuring default organization...")
        cursor.execute("""
            INSERT INTO organizations (id, name, slug, plan)
            VALUES ('00000000-0000-0000-0000-000000000001'::UUID, 'Default Org', 'default', 'enterprise')
            ON CONFLICT DO NOTHING;
        """)
        conn.commit()
        print("✓ Default organization ready")

        cursor.close()
        conn.close()
        print("\n✓ Database initialization complete")
        return True

    except psycopg2.OperationalError as e:
        print(f"\n✗ Database connection failed: {e}")
        print("  Make sure PostgreSQL is running and DATABASE_URL is correct")
        print(f"  DATABASE_URL = {db_url[:50]}...")
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False

def test_connection(db_url):
    """Test database connection and run sample query."""
    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()

        # Test query
        cursor.execute("SELECT COUNT(*) FROM registry_submissions;")
        count = cursor.fetchone()[0]
        print(f"✓ Database connection successful")
        print(f"  registry_submissions: {count} rows")

        # Show schema version
        cursor.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = [row[0] for row in cursor.fetchall()]
        print(f"  Tables: {', '.join(tables)}")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

def main():
    """Main entry point."""
    db_url = get_db_url()

    if '--init' in sys.argv:
        print(f"\n{'='*70}")
        print("API Bridge Database Initialization")
        print(f"{'='*70}\n")
        init_database(db_url)
    elif '--test' in sys.argv:
        print(f"\n{'='*70}")
        print("API Bridge Database Connection Test")
        print(f"{'='*70}\n")
        test_connection(db_url)
    else:
        print(f"\n{'='*70}")
        print("API Bridge Database Status")
        print(f"{'='*70}\n")
        print(f"DATABASE_URL: {db_url[:50]}...")
        print("\nUsage:")
        print("  python3 init_api_bridge_db.py --init    # Initialize database")
        print("  python3 init_api_bridge_db.py --test    # Test connection")

if __name__ == "__main__":
    main()
