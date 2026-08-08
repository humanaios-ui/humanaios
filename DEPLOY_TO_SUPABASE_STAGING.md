# M2R2 Schema Deployment to Supabase Production

**Status:** Ready for execution  
**Credentials:** ✅ Stored securely in GitHub Secrets  
**Location:** /Users/andersonfamily/practices/humanaios  
**Security:** Production credentials NEVER hardcoded in docs or scripts

---

## Security Notice

⚠️ **CRITICAL:** Database credentials must NEVER be hardcoded in documentation, shell scripts, or version control. This document was previously exposed with credentials (GitHub incident resolved 2026-08-08). All credentials now follow secure patterns below.

---

## Quick Start (Secure Pattern)

### Option A: GitHub Actions (Recommended for CI/CD)

**1. Store credentials in GitHub Secrets:**
```
Settings → Secrets and variables → Actions
+ New repository secret

SUPABASE_PROD_DATABASE_URL = postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres
SUPABASE_STAGING_DATABASE_URL = postgresql://postgres:[PASSWORD]@[STAGING_HOST]:5432/postgres
```

**2. Use in workflow (.github/workflows/deploy.yml):**
```yaml
name: Deploy M2R2 Schema

on:
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production  # Requires approval
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.8'
      - run: |
          pip install alembic sqlalchemy psycopg2-binary
          alembic upgrade head
        env:
          DATABASE_URL: ${{ secrets.SUPABASE_PROD_DATABASE_URL }}
```

### Option B: Local Development (1Pasword / LastPass / Vault)

**1. Use a secrets manager (DO NOT commit credentials):**
```bash
# Install 1Password CLI or similar
brew install 1password-cli

# Load credentials from vault
eval $(op run --env-file=<(op item get humanaios-db-creds --format json | jq -r '.fields[] | "\(.label)=\(.value)"'))

# Run deployment
./deploy-m2r2-staging.sh
```

**2. Ensure .gitignore prevents leaks:**
```bash
# .gitignore
.env
.env.local
.env.production
.secrets*
*.key
*.pem
deploy_config.sh
```

**3. Verify no credentials are staged:**
```bash
git diff --cached | grep -i "postgresql\|password\|secret"  # Should return nothing
```

---

## ⛔ What NOT to Do (Critical Security Rules)

- ❌ **DO NOT** hardcode credentials in shell scripts (e.g., `export DATABASE_URL="..."`)
- ❌ **DO NOT** include credentials in markdown files, READMEs, or documentation
- ❌ **DO NOT** copy/paste credentials into terminals without masking first
- ❌ **DO NOT** share credentials in Slack, email, or pull request comments
- ❌ **DO NOT** commit `.env`, `.secrets`, or credential files
- ❌ **DO NOT** use the same credential across multiple environments (staging ≠ production)

**Violation consequences:** Public exposure → credential rotation → emergency incident → downtime. Use GitHub Secrets or a vault instead.

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
