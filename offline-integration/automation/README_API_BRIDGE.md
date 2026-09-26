# API Bridge — Database-Integrated Registry Gateway

The API Bridge connects the HTML dashboard (intent-os-universal-v2.html) to Python automation gates and the empirica PostgreSQL database layer.

## Architecture

```
HTML Dashboard
    ↓
API Bridge (Flask)
    ↓
Registry Gate (cycle2_registry_gate.py)
    ↓
Scorer (boundary_and_scorer.py)
    ↓
PostgreSQL Database (schema_registry_extension.sql)
    ↓
Measurement Harness & Telemetry
```

## Files

| File | Purpose |
|------|---------|
| `api_bridge.py` | v1: In-memory only (for testing) |
| `api_bridge_db.py` | v2: Database-integrated (production) |
| `run_api_bridge.sh` | Startup script with database initialization |
| `cycle2_registry_gate.py` | Registry submission gate (3-outcome routing) |
| `boundary_and_scorer.py` | Scoring logic for accepted submissions |

## Setup

### 1. Install Dependencies

```bash
pip install flask sqlalchemy psycopg2-binary
```

### 2. Set Up Database Connection

Create a `.env` file in the project root:

```bash
cp .env.example .env
# Edit .env and set DATABASE_URL to your PostgreSQL connection
# Example: DATABASE_URL=postgresql://user:password@localhost/empirica
```

### 3. Initialize Database

```bash
cd offline-integration/automation
chmod +x run_api_bridge.sh
python3 ../../scripts/init_api_bridge_db.py --init
```

This creates:
- `organizations` table
- `users` table
- `registry_submissions` table (stores submissions + outcomes + scores)
- `registry_feedback` table (stores issues/rejections)
- `harness_modes` table (resource allocation configuration)
- `intent_reconciliation` table (stated vs revealed intent tracking)
- All necessary indexes

### 4. Start the API Bridge

```bash
./run_api_bridge.sh
# Or with database initialization:
./run_api_bridge.sh --init
```

The bridge will start on `http://localhost:5000`

## Endpoints

### POST /gate/registry
Submit a record to the registry gate for evaluation.

**Request:**
```json
{
  "title": "Record title",
  "company": "Company name",
  "location": "Location",
  "salary": 100000,
  "desc": "Description",
  "source_id": "attested_source_uuid",
  "attest_hash": "sha256_hash",
  "source_license": "CC-BY-4.0"
}
```

**Response:**
```json
{
  "outcome": "ACCEPT",
  "reason": "Meets all validation criteria",
  "record_id": "abc123def456",
  "timestamp": "2026-08-22T18:30:45.123456Z",
  "score": {
    "score": 85,
    "adversarial_signatures_at_input": [],
    ...
  }
}
```

**Outcomes:**
- `ACCEPT` — Record passed all gates, scoring computed, routed to proposal queue
- `QUARANTINE` — Security/validation failure, rejected
- `CANDIDATE` — Interesting but uncertain, routed to discovery pathway

### GET /state/sync
Get current system state (pipeline, intent, harness, feedback).

**Response:**
```json
{
  "pipeline": {
    "propose": 5,
    "ratify": 2,
    "land": 1
  },
  "intent": {
    "stated": "Assess human-AI collaboration",
    "revealed": "Assess system reliability",
    "gap": 0.3
  },
  "harness": {
    "human": 0.5,
    "machine": 0.3,
    "capital": 0.2
  },
  "feedback_count": 3,
  "feedback_recent": [...]
}
```

### POST /harness/set
Set resource allocation mode.

**Request:**
```json
{
  "mode": "ai-led"
}
```

**Response:**
```json
{
  "ok": true,
  "mode": "ai-led",
  "harness": {
    "human": 0.2,
    "machine": 0.6,
    "capital": 0.2
  }
}
```

**Available modes:**
- `balanced` — 50% human, 30% machine, 20% capital
- `ai-led` — 20% human, 60% machine, 20% capital
- `human-led` — 70% human, 20% machine, 10% capital
- `capital-injection` — 30% human, 20% machine, 50% capital

## Database Schema

### registry_submissions
Stores all submitted records and their outcomes.

| Column | Type | Purpose |
|--------|------|---------|
| `id` | UUID | Primary key |
| `org_id` | UUID | Organization (for multi-tenancy) |
| `record` | JSONB | Full submission data |
| `outcome` | VARCHAR | ACCEPT \| QUARANTINE \| CANDIDATE |
| `outcome_reason` | TEXT | Why the outcome was assigned |
| `score` | JSONB | Scoring details (for ACCEPT) |
| `pipeline_status` | VARCHAR | proposed \| ratified \| landed \| rejected |
| `submitted_at` | TIMESTAMP | When submitted |
| `created_at` | TIMESTAMP | Record creation time |

### registry_feedback
Stores issues, rejections, and user feedback.

| Column | Type | Purpose |
|--------|------|---------|
| `id` | UUID | Primary key |
| `org_id` | UUID | Organization |
| `submission_id` | UUID | Link to submission (if applicable) |
| `source` | VARCHAR | user \| machine |
| `type` | VARCHAR | security_reject \| validation_error \| user_report |
| `severity` | VARCHAR | low \| medium \| high \| critical |
| `message` | TEXT | Feedback message |
| `status` | VARCHAR | open \| acknowledged \| resolved |

### harness_modes
Tracks resource allocation configuration over time.

| Column | Type | Purpose |
|--------|------|---------|
| `mode` | VARCHAR | balanced \| ai-led \| human-led \| capital-injection |
| `human_allocation` | DECIMAL(3,2) | % allocated to human (0.0-1.0) |
| `machine_allocation` | DECIMAL(3,2) | % allocated to machine |
| `capital_allocation` | DECIMAL(3,2) | % allocated to capital |
| `active` | BOOLEAN | Is this the current active mode? |

## Persistence Guarantee

All data written to the API bridge is persisted to PostgreSQL:

1. **Submissions** — Every record submitted via `/gate/registry` is stored in `registry_submissions`
2. **Outcomes** — Gate decision (ACCEPT/QUARANTINE/CANDIDATE) is recorded
3. **Scores** — For accepted records, scoring results are stored as JSONB
4. **Feedback** — Machine-generated rejections and user reports are logged
5. **Harness Configuration** — Resource allocation mode changes are timestamped

If database connection fails, the bridge falls back to in-memory state but logs a warning. On next startup, in-memory data is lost but the database contains the historical record.

## Testing

### Manual Test
```bash
curl -X POST http://localhost:5000/gate/registry \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Record",
    "company": "Test Corp",
    "location": "Boston",
    "salary": 120000,
    "desc": "A test record",
    "source_id": "test-source",
    "source_license": "CC-BY-4.0"
  }'
```

### Database Verification
```bash
# Connect to PostgreSQL
psql $DATABASE_URL

# Check submissions
SELECT COUNT(*) FROM registry_submissions;
SELECT outcome, COUNT(*) FROM registry_submissions GROUP BY outcome;

# Check feedback
SELECT type, COUNT(*) FROM registry_feedback GROUP BY type;

# Check harness configuration
SELECT mode, active FROM harness_modes ORDER BY created_at DESC LIMIT 1;
```

## Troubleshooting

### Database Connection Failed
- Check `DATABASE_URL` in `.env`
- Ensure PostgreSQL is running: `pg_isready`
- Test connection: `psql $DATABASE_URL`

### Tables Not Found
- Run: `python3 ../../scripts/init_api_bridge_db.py --init`
- Check status: `python3 ../../scripts/init_api_bridge_db.py --test`

### Port Already in Use
- Use a different port: `./run_api_bridge.sh --port 5001`
- Or kill the existing process: `pkill -f "python3.*api_bridge"`

## Integration with Empirica

The API bridge integrates with the empirica foundation orchestration:

1. **Submissions** are recorded in `registry_submissions` table
2. **Outcomes** feed into measurement gates (via `/state/sync`)
3. **Scores** inform evaluator assessment dashboard
4. **Feedback** is logged for audit and post-hoc analysis
5. **Harness configuration** tracks resource allocation over time for empirica measurement

## Next Steps

1. ✅ Database initialization (`init_api_bridge_db.py`)
2. ✅ API bridge v2 with ORM models (`api_bridge_db.py`)
3. ✅ Startup script with migrations (`run_api_bridge.sh`)
4. 🔄 **Wire to dashboard** (HTML form submissions → `/gate/registry` endpoint)
5. 🔄 **Dashboard state sync** (read `/state/sync` endpoint, update UI)
6. 🔄 **Measurement pipeline** (aggregate submission outcomes for Phase 3.5.6 metrics)
7. 🔄 **Cross-org orchestration** (send completion ack to mesh-support on measurement launch)

---

**Last Updated:** 2026-08-22  
**Persistence:** ✅ LIVE (PostgreSQL)  
**Status:** Production-ready for Phase 3.5.6
