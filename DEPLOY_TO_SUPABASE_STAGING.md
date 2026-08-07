# M2R2 Schema Deployment to Supabase Staging

**Status:** Ready for execution  
**Credentials:** ✅ Provided  
**Location:** /Users/andersonfamily/practices/humanaios  

---

## Quick Start (Copy & Paste)

### On Your Local Machine (with Python 3.8+)

```bash
# 1. Clone/navigate to humanaios repo
cd /Users/andersonfamily/practices/humanaios

# 2. Set Supabase staging connection
export DATABASE_URL="postgresql://postgres:***REDACTED***@db.ksinisdzgtnqzsymhfya.supabase.co:5432/postgres"

# 3. Install dependencies (one-time)
pip install alembic sqlalchemy psycopg2-binary

# 4. Run deployment script
./deploy-m2r2-staging.sh

# 5. Script will prompt for confirmation before applying
```

---

## What Gets Deployed

### Tables Created
```sql
-- Collaborations table
CREATE TABLE collaborations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  description VARCHAR(2000),
  state_data JSON NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  archived_at TIMESTAMP WITH TIME ZONE
);

-- Projects table  
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  description VARCHAR(2000),
  state_data JSON NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  archived_at TIMESTAMP WITH TIME ZONE
);

-- State audit log
CREATE TABLE state_audit_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  entity_type ENUM('collaboration', 'project') NOT NULL,
  entity_id UUID NOT NULL,
  from_state VARCHAR(50) NOT NULL,
  to_state VARCHAR(50) NOT NULL,
  timestamp TIMESTAMP WITH TIME ZONE DEFAULT now(),
  authorizer_id VARCHAR(255) NOT NULL,
  reason VARCHAR(1000)
);
```

### Indexes Created
```sql
-- Collaboration indexes
CREATE INDEX idx_collaborations_created ON collaborations(created_at);
CREATE INDEX idx_collaborations_updated ON collaborations(updated_at);
CREATE INDEX idx_collaborations_archived ON collaborations(archived_at);

-- Project indexes
CREATE INDEX idx_projects_created ON projects(created_at);
CREATE INDEX idx_projects_updated ON projects(updated_at);
CREATE INDEX idx_projects_archived ON projects(archived_at);

-- Audit indexes
CREATE INDEX idx_audit_entity ON state_audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_timestamp ON state_audit_log(timestamp);
CREATE INDEX idx_audit_state_change ON state_audit_log(from_state, to_state);
```

---

## Verification After Deployment

### 1. Verify Tables Exist
```bash
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

### 2. Verify Indexes
```bash
psql $DATABASE_URL -c "
  SELECT indexname, tablename
  FROM pg_indexes
  WHERE tablename IN ('collaborations', 'projects', 'state_audit_log')
  ORDER BY tablename, indexname;
"
```

### 3. Test ORM Integration
```bash
python3 << 'EOF'
import os
from src.models.orm_supabase import Collaboration, Project, create_collaboration
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

db_url = os.environ.get("DATABASE_URL")
engine = create_engine(db_url)

with Session(engine) as session:
    # Create test collaboration
    collab = create_collaboration(
        session, 
        "M2R2 Staging Test",
        "Validates schema deployment"
    )
    session.commit()
    
    # Verify state
    retrieved = session.query(Collaboration).filter_by(id=collab.id).first()
    assert retrieved is not None
    assert retrieved.current_state.value == "planned"
    
    print("✅ ORM integration verified")
    print(f"   Created collaboration: {collab.id}")
    print(f"   State: {retrieved.current_state.value}")
    
    # Cleanup
    session.delete(retrieved)
    session.commit()
    print("✅ Test data cleaned up")
EOF
```

### 4. Run Full Test Suite
```bash
python3 -m pytest tests/test_orm_supabase.py -v
python3 -m pytest tests/test_m2r2_state_harmonization.py -v
```

---

## Manual Step-by-Step (If Script Fails)

### Step 1: Preview SQL
```bash
alembic upgrade head --sql > /tmp/m2r2_staging.sql
cat /tmp/m2r2_staging.sql
```

### Step 2: Apply Migrations
```bash
alembic upgrade head
```

### Step 3: Check Current Revision
```bash
alembic current
# Expected: (head)
```

---

## Troubleshooting

### Connection Refused
```
Error: could not connect to server: Connection refused

Fix: Verify Supabase project is running
     Check DATABASE_URL is correct
     Ensure your IP is whitelisted in Supabase
```

### psycopg2 Installation Issues
```bash
# Try installing with system packages
sudo apt-get install python3-psycopg2  # Linux
brew install libpq && pip install psycopg2  # macOS
```

### Alembic Not Found
```bash
# Ensure it's in PATH
which alembic

# If not found:
python3 -m alembic upgrade head
```

### UUID Extension Missing
```
Error: relation "public.uuid_ossp" does not exist

Fix: Already handled in migration - Alembic creates it
     If error persists: 
     CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

---

## Post-Deployment Steps

### 1. Document Deployment
```bash
git log --oneline -5
# Commit your deployment notes
git add -A
git commit -m "docs: Record M2R2 staging schema deployment - $(date +%Y-%m-%d)"
```

### 2. Notify Team
```bash
# Update status in CURRENT.md or team channel
echo "✅ M2R2 schema deployed to Supabase staging"
```

### 3. Plan Production Deployment
- [ ] Create prod Supabase instance
- [ ] Backup staging data
- [ ] Dry-run prod migration
- [ ] Execute prod migration
- [ ] Validate prod ORM
- [ ] Update lasting-light-ai integration

### 4. Coordinate lasting-light-ai Updates
- [ ] Create ACAT assessment UI updates
- [ ] Connect to state machine API endpoints
- [ ] Test end-to-end workflows
- [ ] Deploy to staging
- [ ] Validate with users

---

## Success Checklist

After running deployment script:

- [ ] Script ran without errors
- [ ] Schema tables created in Supabase
- [ ] All indexes created
- [ ] ORM models test successfully
- [ ] Connection string works
- [ ] Test collaboration/project created
- [ ] Audit trail table populated
- [ ] No cascading failures

---

## Next Steps

1. **Run deployment script** with the DATABASE_URL provided
2. **Run verification** commands to confirm success
3. **Test ORM integration** with Python script
4. **Update CURRENT.md** with deployment status
5. **Plan lasting-light-ai integration** (next phase)

---

**Deployment Date:** 2026-08-07  
**Supabase Project:** db.ksinisdzgtnqzsymhfya.supabase.co  
**Authority:** Zone 3 Execution (Carly R. Anderson)  
**Status:** Ready for immediate execution
