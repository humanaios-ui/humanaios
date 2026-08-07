# M2R2 Phase 4: Alembic Migrations & Supabase Deployment

**Authority:** Zone 3 Execution (Carly R. Anderson)  
**Date:** 2026-08-07  
**Status:** ⏳ READY FOR DEPLOYMENT

---

## Overview

Phase 4 delivers Alembic migration infrastructure for deploying M2R2 state machine tables to Supabase. This document covers:
- Migration setup and structure
- Database schema creation
- Deployment procedures
- Verification and validation
- Rollback strategies

---

## Migration Infrastructure

### Alembic Configuration

**Files Created:**
- `alembic.ini` — Configuration file with Supabase connection settings
- `alembic/env.py` — Environment setup for online/offline migration modes
- `alembic/script.py.mako` — Migration template
- `alembic/versions/001_m2r2_create_state_tables.py` — Initial schema migration

### Database Schema

**Tables:**

1. **collaborations**
   ```sql
   CREATE TABLE collaborations (
     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     name TEXT NOT NULL,
     description TEXT,
     state_data JSON NOT NULL,
     created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
     updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
     archived_at TIMESTAMP WITH TIME ZONE,
     
     -- Indexes for querying
     INDEX idx_collaborations_created (created_at),
     INDEX idx_collaborations_updated (updated_at),
     INDEX idx_collaborations_archived (archived_at)
   );
   ```

2. **projects**
   ```sql
   CREATE TABLE projects (
     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     name TEXT NOT NULL,
     description TEXT,
     state_data JSON NOT NULL,
     created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
     updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
     archived_at TIMESTAMP WITH TIME ZONE,
     
     -- Indexes for querying
     INDEX idx_projects_created (created_at),
     INDEX idx_projects_updated (updated_at),
     INDEX idx_projects_archived (archived_at)
   );
   ```

3. **state_audit_log** (Optional, for detailed audit trail)
   ```sql
   CREATE TABLE state_audit_log (
     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     entity_type ENUM('collaboration', 'project') NOT NULL,
     entity_id UUID NOT NULL,
     from_state VARCHAR(50) NOT NULL,
     to_state VARCHAR(50) NOT NULL,
     timestamp TIMESTAMP WITH TIME ZONE DEFAULT now(),
     authorizer_id VARCHAR(255) NOT NULL,
     reason VARCHAR(1000),
     
     -- Indexes for querying
     INDEX idx_audit_entity (entity_type, entity_id),
     INDEX idx_audit_timestamp (timestamp),
     INDEX idx_audit_state_change (from_state, to_state)
   );
   ```

---

## Deployment Procedures

### Prerequisites

1. **Supabase Instance**
   - Project URL: `https://<project>.supabase.co`
   - Database connection string available
   - User has superuser or schema admin privileges

2. **Environment Setup**
   ```bash
   # Export Supabase connection string
   export DATABASE_URL="postgresql://postgres:password@db.supabase.co:5432/postgres"
   
   # Or use specific Supabase format:
   export SUPABASE_DB_URL="postgresql://postgres:<password>@<host>:5432/postgres"
   ```

3. **Python Dependencies**
   ```bash
   pip install alembic sqlalchemy psycopg2-binary
   ```

### Migration Workflow

#### Step 1: Validate Configuration

```bash
# Verify Alembic setup
alembic current

# Expected output:
# (head)
```

#### Step 2: Generate SQL (Offline Mode)

For dry-run before applying:

```bash
# Generate SQL script without executing
alembic upgrade head --sql

# Output shows the SQL that will be applied
```

#### Step 3: Apply Migrations (Online Mode)

```bash
# Apply migrations to live database
DATABASE_URL="postgresql://..." alembic upgrade head

# Expected output:
# INFO [alembic.runtime.migration] Context impl PostgresqlImpl.
# INFO [alembic.runtime.migration] Will assume transactional DDL.
# INFO [alembic.migration] Running upgrade -> 001_m2r2_create_tables
# INFO [sqlalchemy.engine.Engine] CREATE EXTENSION IF NOT EXISTS "uuid-ossp"
# ... more DDL statements ...
# INFO [alembic.migration] Done.
```

#### Step 4: Verify Schema Creation

```bash
# Connect to Supabase and verify tables
psql $DATABASE_URL -c "
  SELECT table_name 
  FROM information_schema.tables 
  WHERE table_schema = 'public'
  ORDER BY table_name;
"

# Expected output:
# collaborations
# projects
# state_audit_log
```

#### Step 5: Verify Indexes

```bash
# List indexes on collaborations table
psql $DATABASE_URL -c "
  SELECT indexname 
  FROM pg_indexes 
  WHERE tablename = 'collaborations';
"

# Expected output:
# idx_collaborations_created
# idx_collaborations_updated
# idx_collaborations_archived
```

---

## Production Deployment Strategy

### Pre-Deployment Checklist

- [ ] Database backup taken (Supabase automated backups enabled)
- [ ] Dry-run SQL reviewed and validated
- [ ] Connection string verified with non-prod first
- [ ] Rollback procedure documented and tested
- [ ] Monitoring/alerting configured for new tables
- [ ] ORM models (orm_supabase.py) deployed to application

### Deployment Steps (Zone 3)

1. **Stage 1: Non-Production**
   ```bash
   # Apply to dev/staging first
   DATABASE_URL="postgresql://..." alembic upgrade head
   # Verify with ORM models
   python3 -c "from src.models.orm_supabase import Collaboration, Project; print('✅ Models load')"
   ```

2. **Stage 2: Production Standby**
   ```bash
   # Apply to production read-replica (if available)
   DATABASE_URL="postgresql://..." alembic upgrade head
   # Run validation queries
   ```

3. **Stage 3: Production**
   ```bash
   # Apply to production
   DATABASE_URL="postgresql://prod-url..." alembic upgrade head
   # Monitor: Check logs, query performance, replication lag
   ```

### Post-Deployment Validation

```bash
# Test ORM model creation
python3 <<'EOF'
from src.models.orm_supabase import Collaboration, Project
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine(os.environ["DATABASE_URL"])
with Session(engine) as session:
    # Create test collaboration
    collab = Collaboration(name="Test", description="Validation")
    session.add(collab)
    session.commit()
    
    # Verify it persists
    retrieved = session.query(Collaboration).filter_by(id=collab.id).first()
    assert retrieved is not None
    assert retrieved.current_state.value == "planned"
    
    print("✅ ORM integration verified")
    
    # Cleanup
    session.delete(collab)
    session.commit()
EOF
```

---

## Rollback Procedures

### If Migration Fails

```bash
# Revert to previous revision (empty in this case)
alembic downgrade -1

# Output should show:
# INFO [alembic.migration] Running downgrade -> 
```

### If Tables Need Adjustment

```bash
# Create new migration for schema changes
alembic revision -m "adjust_state_data_column"

# Edit alembic/versions/002_*.py to add your changes
# Then apply:
alembic upgrade head
```

---

## Data Migration (If Applicable)

If existing collaborations/projects need migration to new tables:

```python
# Script: migrate_legacy_data.py
from src.models.orm_supabase import Collaboration, Project, create_collaboration, create_project
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine(os.environ["DATABASE_URL"])

# Pseudocode: extract legacy data and populate new tables
legacy_collabs = get_legacy_collaborations()  # From old system

with Session(engine) as session:
    for legacy in legacy_collabs:
        collab = create_collaboration(session, legacy.name, legacy.description)
        
        # Migrate state if applicable
        # collab.transition_to(map_legacy_state(legacy.state), ...)
        
        session.commit()
    
    print(f"✅ Migrated {len(legacy_collabs)} collaborations")
```

---

## Monitoring & Maintenance

### Query Performance

Monitor table sizes and index usage:

```sql
-- Check table sizes
SELECT 
  table_name,
  pg_size_pretty(pg_total_relation_size(table_name::regclass)) as size
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN ('collaborations', 'projects', 'state_audit_log')
ORDER BY pg_total_relation_size(table_name::regclass) DESC;
```

### Index Usage

```sql
-- Monitor index usage
SELECT 
  indexrelname,
  idx_scan,
  idx_tup_read,
  idx_tup_fetch
FROM pg_stat_user_indexes
WHERE relname IN ('collaborations', 'projects', 'state_audit_log');
```

### Replication Lag

```bash
# For managed replicas (Supabase)
SELECT EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp()))::INT as replication_lag_seconds;
```

---

## Troubleshooting

### Connection Issues

```bash
# Test connection
psql $DATABASE_URL -c "SELECT version();"

# If fails:
# 1. Check credentials in $DATABASE_URL
# 2. Verify IP whitelisting in Supabase
# 3. Ensure connection limit not exceeded
```

### Extension Not Available

```bash
# If "uuid-ossp" extension not available in Supabase
# Use built-in gen_random_uuid() instead (Postgres 13+)
# Already configured in migration
```

### Constraint Violations

```bash
# If data migration conflicts with schema
# Create staging table, validate data, then migrate
ALTER TABLE collaborations RENAME TO collaborations_backup;
-- Apply migration
-- Migrate validated data from backup
```

---

## Next Steps After Deployment

1. **API Integration** — Connect ORM models to REST endpoints (if needed)
2. **Data Validation** — Run full test suite against live database
3. **Performance Tuning** — Monitor queries, add indexes if needed
4. **Documentation** — Update API docs with new state management endpoints
5. **Monitoring** — Set up alerts for table growth, query performance
6. **Team Onboarding** — Train on state machine usage and transition procedures

---

## References

- **Alembic Documentation**: https://alembic.sqlalchemy.org/
- **Supabase PostgreSQL**: https://supabase.com/docs/guides/database
- **M2R2 ORM Models**: src/models/orm_supabase.py
- **State Machine Core**: src/models/collaboration_state.py, src/models/project_state.py

---

**Authority:** Zone 3 Execution (Carly R. Anderson)  
**Status:** Ready for production deployment  
**Target Date:** 2026-08-07 or upon user approval  
