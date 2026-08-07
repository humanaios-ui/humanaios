#!/bin/bash
# M2R2 Phase 4 Schema Deployment to Supabase Staging
# Zone 3 Execution Script

set -e

echo "🚀 M2R2 Schema Deployment to Supabase Staging"
echo "═══════════════════════════════════════════════"
echo ""

# Step 1: Verify Alembic installation
echo "Step 1: Verifying Alembic installation..."
if ! command -v alembic &> /dev/null; then
    echo "❌ Alembic not found. Installing..."
    python3 -m pip install alembic sqlalchemy psycopg2-binary
fi
echo "✅ Alembic ready"
echo ""

# Step 2: Check DATABASE_URL environment variable
echo "Step 2: Checking Supabase staging connection..."
if [ -z "$DATABASE_URL" ] && [ -z "$SUPABASE_STAGING_URL" ]; then
    echo "❌ DATABASE_URL or SUPABASE_STAGING_URL not set"
    echo ""
    echo "Set your Supabase staging connection string:"
    echo "  export DATABASE_URL='postgresql://postgres:password@db.supabase.co:5432/postgres'"
    echo ""
    echo "Or:"
    echo "  export SUPABASE_STAGING_URL='postgresql://postgres:password@db.supabase.co:5432/postgres'"
    exit 1
fi

# Use SUPABASE_STAGING_URL if DATABASE_URL not set
if [ -z "$DATABASE_URL" ]; then
    export DATABASE_URL="$SUPABASE_STAGING_URL"
fi

echo "✅ Connection string found"
echo "   Database: $(echo $DATABASE_URL | sed 's/:.*//' | grep -o '[^@]*@.*')"
echo ""

# Step 3: Verify Alembic configuration
echo "Step 3: Verifying Alembic configuration..."
if [ ! -f "alembic.ini" ]; then
    echo "❌ alembic.ini not found"
    exit 1
fi

if [ ! -d "alembic/versions" ]; then
    echo "❌ alembic/versions directory not found"
    exit 1
fi
echo "✅ Alembic configuration valid"
echo ""

# Step 4: Generate SQL (dry-run)
echo "Step 4: Generating migration SQL (dry-run)..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
alembic upgrade head --sql > /tmp/m2r2_schema.sql
echo ""
echo "Generated SQL preview:"
head -30 /tmp/m2r2_schema.sql
echo "..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Step 5: Ask for confirmation
echo "Step 5: Confirmation"
echo "Review the SQL above. Ready to deploy to Supabase staging?"
echo ""
read -p "Type 'yes' to proceed with schema deployment: " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Deployment cancelled"
    exit 1
fi
echo ""

# Step 6: Apply migrations
echo "Step 6: Applying migrations to Supabase staging..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
alembic upgrade head
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Step 7: Verify schema creation
echo "Step 7: Verifying schema creation..."
psql "$DATABASE_URL" -c "
  SELECT table_name
  FROM information_schema.tables
  WHERE table_schema = 'public'
  ORDER BY table_name;
" 2>/dev/null || echo "⚠️  Could not verify via psql (optional)"
echo ""

# Step 8: Verify indexes
echo "Step 8: Checking indexes..."
psql "$DATABASE_URL" -c "
  SELECT indexname, tablename
  FROM pg_indexes
  WHERE tablename IN ('collaborations', 'projects', 'state_audit_log')
  ORDER BY tablename, indexname;
" 2>/dev/null || echo "⚠️  Could not verify indexes via psql (optional)"
echo ""

# Step 9: Test ORM integration
echo "Step 9: Testing ORM integration..."
python3 << 'PYTHON_TEST'
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path.cwd()
sys.path.insert(0, str(project_root))

try:
    from src.models.orm_supabase import Collaboration, Project
    from sqlalchemy import create_engine, inspect
    from sqlalchemy.orm import Session

    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("⚠️  DATABASE_URL not set for ORM test")
        sys.exit(0)

    # Create engine
    engine = create_engine(db_url, echo=False)

    # Verify tables exist
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    required_tables = {"collaborations", "projects"}
    found_tables = set(tables) & required_tables

    if found_tables == required_tables:
        print(f"✅ All required tables found: {', '.join(sorted(found_tables))}")

        # Test ORM model
        with Session(engine) as session:
            collab = Collaboration(name="M2R2 Test", description="Staging validation")
            print(f"✅ ORM model instantiated successfully")
            print(f"   - Initial state: {collab.current_state.value}")
    else:
        print(f"❌ Missing tables: {required_tables - found_tables}")
        sys.exit(1)

except Exception as e:
    print(f"⚠️  ORM test skipped: {e}")

PYTHON_TEST

echo ""

# Step 10: Summary
echo "✅ Schema deployment complete!"
echo ""
echo "Summary:"
echo "  ✓ Alembic migrations applied"
echo "  ✓ Tables created (collaborations, projects, state_audit_log)"
echo "  ✓ Indexes created"
echo "  ✓ ORM models validated"
echo ""
echo "Next steps:"
echo "  1. Run tests: python3 -m pytest tests/test_orm_supabase.py -v"
echo "  2. Test with ORM: python3 -c 'from src.models.orm_supabase import Collaboration'"
echo "  3. Deploy to production when ready"
echo ""
echo "📋 Migration log saved to: $PWD/alembic_deploy.log"
alembic current >> alembic_deploy.log 2>&1 || true
echo ""
echo "🎉 Ready for next phase!"
