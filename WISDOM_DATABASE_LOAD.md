# Load wisdom_database into Supabase

**Prerequisites:** SUPABASE_DATABASE_URL environment variable configured  
**Duration:** 30-60 seconds  
**After Phase 1:** Table creation verified

---

## Quick Start

```bash
# Set your Supabase database URL (find in Project Settings → Database)
export SUPABASE_DATABASE_URL="postgresql://postgres:YOUR_PASSWORD@YOUR_PROJECT.supabase.co:5432/postgres"

# Install psycopg2 (Postgres adapter for Python)
pip install psycopg2-binary

# Run the load script
python3 load_wisdom_database.py

# Expected output:
# ✓ Loaded wisdom_database v0.3
# ✓ Traditions: [all 10 traditions listed]
# ✓ Connected to Supabase
# ✓ Extracted 114 teachings
# ✓ Inserted 114 teachings
# ✓ Total teachings: 114
# ✓ Traditions: 10
# ✓ Consciousness range: 0-1000
# ✓ Load complete!
```

---

## What Gets Loaded

**114 teachings from 10 traditions:**

| Tradition | Teachings | Consciousness Level Range |
|-----------|-----------|---------------------------|
| AA 12 Steps | 12 | 0-600 |
| AA 12 Traditions | 12 | 100-550 |
| Hawkins Consciousness Map | 17 | 0-1000 |
| A Course in Miracles | 12 | 350-700 |
| Book of Five Rings | 12 | 200-500 |
| Living Buddha, Living Christ | 12 | 300-650 |
| Buddhist Core | 15 | 50-600 |
| Words of Jesus | 10 | 200-700 |
| Freemasonry | 6 | 200-500 |
| Stoicism | 6 | 200-400 |
| **TOTAL** | **114** | **0-1000** |

Each teaching is stored with:
- **Title** and **Text** (the actual wisdom)
- **Consciousness Level** (Hawkins scale, 0-1000)
- **Tradition** (which wisdom tradition)
- **Challenge** (what obstacle it addresses)
- **Code Mapping** (ML analogy — clever cross-domain insights)
- **Obstacle** (what might prevent application)

---

## Verify Load Success

### Query 1: Count teachings by tradition

```sql
SELECT teaching_tradition, COUNT(*) as count
FROM guidance_sessions
WHERE status = 'completed'
GROUP BY teaching_tradition
ORDER BY count DESC;
```

**Expected result:** All 10 traditions with their teaching counts

### Query 2: Check consciousness level distribution

```sql
SELECT
  COUNT(*) as total,
  MIN(metadata::jsonb->>'consciousness_level')::int as min_level,
  MAX(metadata::jsonb->>'consciousness_level')::int as max_level,
  AVG((metadata::jsonb->>'consciousness_level')::int) as avg_level
FROM guidance_sessions
WHERE status = 'completed' AND teaching_text IS NOT NULL;
```

**Expected result:** 114 teachings, range 0-1000, avg ~400

### Query 3: Verify teachings are searchable

```sql
SELECT teaching_title, teaching_tradition, metadata::jsonb->>'consciousness_level' as level
FROM guidance_sessions
WHERE status = 'completed'
LIMIT 5;
```

**Expected result:** 5 teachings with title, tradition, and level

---

## If Load Fails

### Error: "psycopg2 not installed"

```bash
pip install psycopg2-binary
# Then retry: python3 load_wisdom_database.py
```

### Error: "SUPABASE_DATABASE_URL not set"

```bash
# Get DATABASE_URL from Supabase Console:
# 1. Go to https://app.supabase.com
# 2. Click your project
# 3. Settings → Database → Connection string
# 4. Copy "URI" connection string
# 5. Export it:

export SUPABASE_DATABASE_URL="postgresql://postgres:YOUR_PASSWORD@YOUR_PROJECT.supabase.co:5432/postgres"

# Verify it's set:
echo $SUPABASE_DATABASE_URL

# Then retry:
python3 load_wisdom_database.py
```

### Error: "connection failed"

- Verify SUPABASE_DATABASE_URL is correct (copy from Supabase console)
- Verify Supabase project is active (not paused)
- Check firewall/network access

### Error: "table 'guidance_sessions' does not exist"

- Verify Phase 1 (Supabase migrations) completed successfully
- Run: `psql $SUPABASE_DATABASE_URL -c "\dt public.*"`
- Should show: guidance_requests, guidance_sessions, guidance_observability

---

## After Load Succeeds

1. **Next step:** Task #3 (Validate guidance_router endpoints)
2. **Then:** Phase 2 staging deployment (Sep 9)
3. **Go-live:** Sep 11

The wisdom_engine API is now ready to serve teachings based on consciousness level queries.

---

**Timeline:**
- Sep 4: Table creation ✓
- Sep 4-5: wisdom_database load (this script)
- Sep 6-7: Endpoint validation (Task #3)
- Sep 8: Ready for Phase 2
- Sep 9: Staging deployment + load testing
- Sep 11: Production go-live
