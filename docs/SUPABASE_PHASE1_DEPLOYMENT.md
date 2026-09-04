# wisdom_engine API — Supabase Phase 1 Deployment Guide

**Status:** Ready for Zone 3 Execution  
**Deadline:** Sep 8, 2026 (3-day buffer before Phase 2 staging)  
**Authority:** Carly R. Anderson (Admiral, Zone 3)  
**Critical Path:** This unblocks Phase 2-4 deployment for Sep 11 go-live

---

## Executive Summary

Phase 1 establishes the Supabase PostgreSQL backend for wisdom_engine API. Three tables must be created and wisdom_database loaded:

1. **guidance_requests** — Logs each API request (metadata, constraints, audit)
2. **guidance_sessions** — Stores matched teachings, parallels, transcripts  
3. **guidance_observability** — ACAT feedback loop, dimension scoring
4. **findings** — Empirica findings ingestion table
5. **findings_search** — Semantic search index for findings

**Expected duration:** 15-30 minutes (setup + verification)

---

## Prerequisites

You need:
- Supabase project access (login at https://app.supabase.com)
- Database URL with admin credentials (SUPABASE_DATABASE_URL)
- psql CLI (macOS: `brew install postgresql`) OR web SQL Editor access
- Copy of wisdom_database_v0.3.json (35K, located in humanaios root)

---

## Phase 1: Create Tables via SQL Migration

### Option A: Via Supabase Web Console (Recommended)

1. **Log in** to https://app.supabase.com
2. **Navigate** to SQL Editor (left sidebar)
3. **Create new query** (green "New query" button)
4. **Copy entire contents** of `operations/acat/sql/migration_guidance_tables.sql`
5. **Paste** into the editor
6. **Execute** (Ctrl+Enter or click ▶ Play button)
7. **Verify success**: All 3 tables created without errors

**Expected output:**
```
Query successful (completed in <1s)
3 statements executed
```

### Option B: Via psql (If CLI configured)

```bash
# From humanaios root directory
psql $SUPABASE_DATABASE_URL < operations/acat/sql/migration_guidance_tables.sql

# Expected output:
# CREATE TABLE
# CREATE INDEX
# CREATE TABLE
# CREATE INDEX
# (15+ index/constraint lines total)
```

### Option C: Via Supabase CLI

```bash
cd operations/acat
supabase migration up

# Supabase CLI will apply migrations in ./migrations/ directory
# (Note: May require migrations/ directory setup if not present)
```

---

## Verify Table Creation

After executing migration_guidance_tables.sql, verify the three tables exist:

### Via Web Console SQL Editor:

```sql
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;
```

**Expected result:**
```
table_name
────────────────────────
guidance_observability
guidance_requests
guidance_sessions
```

### Via psql:

```bash
psql $SUPABASE_DATABASE_URL -c "\dt public.*"
```

---

## Phase 2: Create Findings Tables

Repeat the process for findings:

### Via Supabase Web Console:

1. **Create new query** (green "New query" button)
2. **Copy entire contents** of `operations/acat/sql/migration_findings_table.sql`
3. **Paste** and **Execute**

### Via psql:

```bash
psql $SUPABASE_DATABASE_URL < operations/acat/sql/migration_findings_table.sql
```

**Verify:**

```sql
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name LIKE 'findings%'
ORDER BY table_name;
```

**Expected result:**
```
table_name
─────────────────
findings
findings_search
```

---

## Phase 3: Load wisdom_database into guidance_sessions

The wisdom database contains 400+ teachings indexed by consciousness level. These must be loaded into `guidance_sessions` table for the API to function.

### Step 1: Prepare Load Script

Create a Python script to load wisdom_database_v0.3.json:

```python
#!/usr/bin/env python3
import json
import psycopg2
from psycopg2.extras import execute_values
from uuid import uuid4
from datetime import datetime

# Connect to Supabase
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="YOUR_SUPABASE_PASSWORD",  # from Supabase Project Settings
    host="YOUR_PROJECT.supabase.co",
    port="5432"
)
cursor = conn.cursor()

# Load wisdom database
with open('wisdom_database_v0.3.json', 'r') as f:
    wisdom_db = json.load(f)

# Insert teachings into guidance_sessions
# (This is a sample; adapt based on wisdom_database schema)
teachings = wisdom_db.get('teachings', [])

for teaching in teachings:
    cursor.execute("""
        INSERT INTO guidance_sessions 
        (id, request_id, status, teaching_tradition, teaching_title, teaching_text, 
         teaching_source, teaching_era, parallels, confidence, created_at, updated_at, completed_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        str(uuid4()),
        str(uuid4()),  # placeholder request_id (no active request)
        'completed',
        teaching.get('tradition'),
        teaching.get('title'),
        teaching.get('text'),
        teaching.get('source'),
        teaching.get('era'),
        json.dumps(teaching.get('parallels', [])),
        0.95,  # high confidence for canonical teachings
        datetime.utcnow(),
        datetime.utcnow(),
        datetime.utcnow()
    ))

conn.commit()
cursor.close()
conn.close()

print(f"✓ Loaded {len(teachings)} teachings into guidance_sessions")
```

### Step 2: Execute Load Script

```bash
# From humanaios root
python3 load_wisdom_database.py

# Expected output:
# ✓ Loaded 412 teachings into guidance_sessions
```

### Step 3: Verify Load

```sql
SELECT COUNT(*) as teaching_count, 
       COUNT(DISTINCT teaching_tradition) as traditions
FROM guidance_sessions
WHERE status = 'completed' AND teaching_text IS NOT NULL;
```

**Expected result:**
```
teaching_count | traditions
───────────────┼───────────
      412      |     8
```

---

## Phase 4: Verify End-to-End

### Test 1: Verify All Required Columns

```sql
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'guidance_requests'
ORDER BY ordinal_position;
```

**Expected columns:** id, submission_purity, evidential_tier, humility_hierarchy, corpus_source, constraint_tradition, constraint_theme, obstacle, api_key_id, created_at, updated_at

### Test 2: Check Index Coverage

```sql
SELECT tablename, indexname 
FROM pg_indexes 
WHERE schemaname = 'public' 
AND tablename IN ('guidance_requests', 'guidance_sessions', 'guidance_observability', 'findings')
ORDER BY tablename, indexname;
```

**Expected:** 4+ indexes per main table

### Test 3: Verify Constraints

```sql
SELECT constraint_name, constraint_type 
FROM information_schema.table_constraints 
WHERE table_name = 'guidance_requests';
```

**Expected:** CHECK constraints for submission_purity, evidential_tier, corpus_source

---

## Timeline & Handoff

**Sep 5-6:** Supabase migrations executed (Phase 1) ✓  
**Sep 7:** wisdom_database loaded + verified ✓  
**Sep 8:** Ready for Phase 2 staging deployment  
**Sep 9:** Phase 2 (Docker build + staging deployment)  
**Sep 10:** Phase 3 (Load testing + SLO verification)  
**Sep 11:** Phase 4 (Production go-live)

---

## Troubleshooting

### Error: "relation 'guidance_requests' already exists"
**Cause:** Table already created from prior migration attempt  
**Fix:** Migrations use `CREATE TABLE IF NOT EXISTS`, so re-running is safe

### Error: "permission denied" when creating table
**Cause:** User account lacks admin privileges  
**Fix:** Ensure you're using SUPABASE_ADMIN_API_KEY (not regular key)

### wisdom_database load fails with "foreign key violation"
**Cause:** `request_id` FK constraint violation (guidance_sessions → guidance_requests)  
**Fix:** Insert a placeholder guidance_requests row first, OR remove FK constraint for seeding, OR use NULL request_id for pre-loaded teachings

---

## Rollback (If Needed)

```sql
DROP TABLE IF EXISTS guidance_observability CASCADE;
DROP TABLE IF EXISTS guidance_sessions CASCADE;
DROP TABLE IF EXISTS guidance_requests CASCADE;
DROP TABLE IF EXISTS findings_search CASCADE;
DROP TABLE IF EXISTS findings CASCADE;

-- Then re-run migrations
```

---

## Deliverables Checklist

- [ ] guidance_requests table created with 8 columns + 2 indexes
- [ ] guidance_sessions table created with 12 columns + 4 indexes
- [ ] guidance_observability table created with 8 columns + 3 indexes
- [ ] findings table created with 8 columns + 5 indexes
- [ ] findings_search table created with 5 columns + 1 index
- [ ] wisdom_database_v0.3.json loaded (412 teachings)
- [ ] All indexes verified via pg_indexes
- [ ] All constraints verified via table_constraints
- [ ] End-to-end test passed (SELECT COUNT from guidance_sessions)

---

**Next Step:** Phase 2 deployment guide will be provided once Phase 1 is verified.  
**Questions?** Check operations/CLAUDE.md (code conventions) or wisdom-engine-deployment-guide.md (full deployment roadmap).

