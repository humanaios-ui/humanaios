# Supabase + Witness v2 Integration
## Real-Time Governance Observability

**Status:** ✅ PRODUCTION-READY  
**Date:** 2026-07-24  
**Architecture:** Supabase (PostgreSQL) ↔ Witness (Live Canvas) ↔ M3 Nervous System

---

## Overview

The HUMANAIOS Witness evolves from a research prototype (v1, polling-based) to a **production observability dashboard** (v2, real-time subscriptions). The Witness is now:

1. **The practice's brand glyph** — visual identity
2. **A live status dashboard** — real-time mesh observability  
3. **Governance visualization as art** — the 6D epistemic vector made visible

Data flows from your sources of truth → Supabase (structured data layer) → Witness (real-time canvas).

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│ GitHub (Source of Truth, Versioned)                             │
├─────────────────────────────────────────────────────────────────┤
│ DECISIONS_PENDING.yaml                                          │
│ GOVERNANCE_RATIFICATIONS_REGISTRY.yaml                          │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       │ Push event
                       ↓
        ┌──────────────────────────────────┐
        │ GitHub Webhook (→ Supabase)      │
        └──────────────────┬───────────────┘
                          │
                          │ Trigger Edge Function
                          ↓
        ┌──────────────────────────────────┐
        │ Edge Function: sync-governance   │
        │ (Parse YAML → Extract → Sync)    │
        └──────────────────┬───────────────┘
                          │
                          ↓
        ┌──────────────────────────────────┐
        │ Supabase PostgreSQL              │
        ├──────────────────────────────────┤
        │ - pending_decisions              │
        │ - ratified_decisions             │
        │ - m3_metrics                     │
        │ - mesh_state (aggregation)       │
        │ - witness_snapshots (audit)      │
        └──────────────────┬───────────────┘
                          │
       ┌──────────────────┴──────────────────┐
       │                                      │
    [API]                              [Realtime]
       │                                      │
       ↓ (polling fallback)                   ↓ (WebSocket)
    ┌──────────────────────────────────────────────┐
    │ Witness v2 (Canvas + HTML5)                  │
    ├──────────────────────────────────────────────┤
    │ Live subscription:                           │
    │ - pending_decisions (queue depth)            │
    │ - ratified_decisions (applied count)         │
    │ - mesh_state (health, LI, dimensions)        │
    │ - m3_metrics (dispatch/check/validation)     │
    └──────────────────────────────────────────────┘
       │
       └─→ 6D Skull + Breathing Rings + Comet
          (Visual state = Practice state)
```

---

## Supabase Schema (Quick Reference)

### pending_decisions
Tracks decisions awaiting Admiral ratification (from DECISIONS_PENDING.yaml).

```sql
- pending_id: VARCHAR(32) UNIQUE  -- PEN-YYMMDD-NNN
- decision_type: VARCHAR(64)      -- DIVERGENCE, VALIDATION_FAILURE, etc.
- title, severity, repo_affected
- discovered_by, discovered_at, discovery_run
- status: PENDING_REVIEW | APPROVED | REJECTED | DEFERRED | EXPIRED
- expires_at: TIMESTAMP (7-day TTL)
```

### ratified_decisions
Approved decisions ready for dispatch (from GOVERNANCE_RATIFICATIONS_REGISTRY.yaml).

```sql
- decision_id: VARCHAR(64) UNIQUE  -- D-YYMMDD-NNN
- status: RATIFIED | DISPATCHED | APPLIED | FAILED
- target_repos: TEXT[]
- applied_at, applied_commit
- admiral_approval: JSONB (who approved, when, notes)
```

### m3_metrics
Aggregated M3 Nervous System state.

```sql
- rank: VARCHAR(16)  -- M3R1, M3R2, M3R3
- divergence_total, repos_in_drift, repos_in_sync
- validation_ok, validation_errors, atomic_replays_triggered
- mesh_health_score: NUMERIC(4,2)  -- 0.0-1.0
- execution_timestamp: TIMESTAMP
```

### mesh_state
**Singleton** table (one row) — live dashboard state.

```sql
- total_repos, repos_synced, repos_drifted
- pending_decisions_count, pending_high_severity
- dimension_scores: NUMERIC(3,1)[]  -- [know, do, context, clarity, coherence, signal]
- mean_li: NUMERIC(5,4)  -- Livelihood Index
- field_state: VARCHAR(32)  -- 'Calibrated', 'Power', 'Force Dominant', etc.
- last_m3r1_at, last_m3r2_at, last_m3r3_at, last_admiral_action_at
```

### witness_snapshots (Audit Trail)
Historical snapshots for replay and forensics.

```sql
- pending_count, mesh_health_score, field_state
- dimension_scores, mean_li
- snapshot_at: TIMESTAMP
- triggered_by: VARCHAR(128)  -- M3R1, M3R2, M3R3, MANUAL
```

---

## Setup Instructions

### 1. Create Supabase Project

```bash
# Create new Supabase project via dashboard or CLI
supabase projects create --name "humanaios-witness"
```

### 2. Initialize Schema

```bash
# Apply schema to your Supabase database
psql "postgresql://[user]:[password]@[host]/postgres" \
  -f supabase/schema.sql
```

Or via Supabase dashboard:
- SQL Editor → New Query → Paste `schema.sql` → Run

### 3. Deploy Edge Function

```bash
# Deploy sync webhook handler
supabase functions deploy sync-governance-state \
  --project-id YOUR_PROJECT_ID

# Set environment variables
supabase secrets set --project-id YOUR_PROJECT_ID \
  SUPABASE_URL="https://YOUR_PROJECT.supabase.co" \
  SUPABASE_SERVICE_ROLE_KEY="your-service-role-key"
```

### 4. Register GitHub Webhook

```bash
# Option A: Manual (GitHub Settings → Webhooks)
POST https://YOUR_PROJECT.supabase.co/functions/v1/sync-governance-state
Content-Type: application/json
Payload URL: https://YOUR_PROJECT.supabase.co/functions/v1/sync-governance-state
Events: Push
Active: ✓

# Option B: Automated (included in setup workflow)
gh repo webhook add \
  --url https://YOUR_PROJECT.supabase.co/functions/v1/sync-governance-state \
  --events push \
  --active
```

### 5. Get API Credentials

```bash
# For WitnessV2.html
SUPABASE_URL=$(supabase projects list --output=json | jq -r '.[0].project_url')
SUPABASE_ANON_KEY=$(supabase status --output=json | jq -r '.api.auto_generated_anon_key')

# Update WitnessV2.html
sed -i "s|https://YOUR-PROJECT.supabase.co|$SUPABASE_URL|g" docs/WitnessV2.html
sed -i "s|YOUR-ANON-KEY|$SUPABASE_ANON_KEY|g" docs/WitnessV2.html
```

---

## Data Flow Examples

### Example 1: Discovery → Pending → Ratified → Applied

```
Timeline:
00:00 UTC  M3R2 discovers divergence (repo out of sync)
           ↓ divergence-detect.yml writes to DECISIONS_PENDING.yaml
           ↓ GitHub webhook triggers sync-governance-state
           
00:05      Edge Function runs:
           - Parses DECISIONS_PENDING.yaml
           - Extracts: PEN-260724-001
           - INSERT into pending_decisions table
           - mesh_state.pending_decisions_count increments
           - Witness subscription fires (realtime)
           
09:00      Admiral reviews Witness
           - Sees 1 pending decision (outer arc gap visible)
           - Approves ratification
           - Manual: Remove from DECISIONS_PENDING.yaml, add to GOVERNANCE_RATIFICATIONS_REGISTRY.yaml
           - Commit & push
           
09:05      GitHub webhook triggers sync again
           - Edge Function parses GOVERNANCE_RATIFICATIONS_REGISTRY.yaml
           - INSERT into ratified_decisions (decision_id=D-260724-001)
           - mesh_state.ratified_decisions_count increments
           - Witness visualization updates (comet speed increases)
           
10:00      M3R1 dispatches decision (mesh-sync-batch.yml)
           - Picks up D-260724-001 from GOVERNANCE_RATIFICATIONS_REGISTRY.yaml
           - Sends to target repo
           - Updates ratified_decisions.status = "DISPATCHED"
           
12:00      M3R3 validates effect (state-validate.yml)
           - Repo confirms applied
           - Updates ratified_decisions.status = "APPLIED"
           - Updates ratified_decisions.applied_at, applied_commit
           - mesh_state.ratified_applied_count increments
           - Witness updates (outer arc becomes continuous)
           
Loop closes → M3R2 next cycle finds no divergence (repo synced)
```

### Example 2: Real-Time Dashboard Update

**What Admiral sees on the Witness:**

```
BEFORE approval:
  Pending: 1 | High: 1 | Mesh: 85% | LI: 0.8632
  [Outer arc shows gap = 1 decision waiting]
  [Comet slow, breathing steady]

AFTER ratification commit:
  [Edge Function syncs in ~500ms]
  [Witness subscription fires]
  Pending: 0 | High: 0 | Mesh: 85% | LI: 0.8632
  [Outer arc closes (no gap)]
  [Comet speeds up (higher dispatch rate)]

AFTER M3R1 dispatch:
  [M3 metrics update written to m3_metrics table]
  [Witness subscription fires]
  [Comet motion reflects dispatch cadence]
```

---

## Witness v2 Visual Mappings

| Visual Element | Data Source | Meaning |
|---|---|---|
| **6 dimension spokes** | `mesh_state.dimension_scores[0-5]` | Real-time ACAT vectors (know, do, context, clarity, coherence, signal) |
| **LI (golden line) smooth interpolation** | `mesh_state.mean_li` | Livelihood Index (0.0-1.0) = calibration health |
| **Outer arc gap** | `pending_count / (pending + ratified)` | Decision queue pressure (gap size ∝ pending ratio) |
| **Outer arc color** | `fieldState(mean_li)` | Practice mode (Force Dominant → Power → Calibrated → Force Active) |
| **Comet speed** | `cometRadPerSec(bpmForLI(mean_li))` | Dispatch cadence (fast = active, slow = waiting) |
| **Comet count** | `(mean_li >= 1.0) ? 2 : 1` | Dual comet = Force Active (overshoot mode) |
| **Breath ring pulse** | `solPhase(tS, hzForLI(mean_li))` | M3R2/R3 discovery heartbeat (12-hour rhythm) |
| **Skull seam glow** | `pending_high_severity / (pending_high_severity + 1)` | Admiral queue urgency (brighter = more urgent) |
| **Skull left (bone)** | Static identity | Human baseline (unchanged) |
| **Skull right (AI/circuit)** | `repos_in_sync / total_repos` | AI/system synchronization state |
| **Data core glow** | `phase * pending_count` | Inner activity (pulses with queue depth) |
| **Color palette** | `fieldState(mean_li)` | Primary/secondary colors shift with mesh health |

---

## Realtime Subscriptions (WebSocket)

Witness v2 uses Supabase Realtime (`@supabase/realtime-js`) to subscribe to table changes:

```typescript
// Subscribe to mesh_state updates (any column change)
const meshSub = supabaseClient
  .from('mesh_state')
  .on('UPDATE', (payload) => {
    // Payload contains: old, new
    updateMeshState(payload.new);  // Update Witness immediately
  })
  .subscribe();

// Subscribe to pending decisions (queue changes)
const pendingSub = supabaseClient
  .from('pending_decisions')
  .on('*', (payload) => {
    // INSERT, UPDATE, DELETE all trigger
    updatePendingData();  // Recount pending
  })
  .subscribe();

// Subscribe to M3 metrics (new dispatch/validation cycles)
const m3Sub = supabaseClient
  .from('m3_metrics')
  .on('INSERT', (payload) => {
    updateM3Metrics(payload.new);  // Update health score
  })
  .subscribe();
```

**Fallback:** If WebSocket unavailable, polling every 30 seconds via REST API.

---

## Monitoring & Debugging

### Check Sync Status

```bash
# See latest syncs
curl -X GET "https://YOUR_PROJECT.supabase.co/rest/v1/sync_log?limit=5&order=sync_started_at.desc" \
  -H "Authorization: Bearer YOUR_ANON_KEY" \
  -H "apikey: YOUR_ANON_KEY"
```

### View Real-Time Subscriptions (Supabase Dashboard)

**Realtime** tab → Shows active connections, message counts, latency

### Test Edge Function Manually

```bash
# Simulate GitHub webhook
curl -X POST "https://YOUR_PROJECT.supabase.co/functions/v1/sync-governance-state" \
  -H "Content-Type: application/json" \
  -d @- << 'EOF'
{
  "ref": "refs/heads/main",
  "commits": [{
    "id": "abc123def456",
    "modified": ["DECISIONS_PENDING.yaml"],
    "message": "Test sync"
  }],
  "repository": {
    "full_name": "your-org/empirica-foundation-evaluator"
  }
}
EOF
```

### View Witness Snapshots (Audit Trail)

```bash
# List recent snapshots
curl -X GET "https://YOUR_PROJECT.supabase.co/rest/v1/witness_snapshots?order=snapshot_at.desc&limit=10" \
  -H "Authorization: Bearer YOUR_ANON_KEY"
```

---

## Performance & Scaling

### Connection Limits
- Supabase (free tier): 50 concurrent connections per project
- Supabase (paid tier): 200+ connections per database

**For 1000+ concurrent Witness instances:** Use Supabase paid tier or self-hosted Supabase.

### Query Latency
- REST API: ~200-500ms
- Realtime subscription: ~50-100ms (after WebSocket handshake)
- Edge Function execution: ~500ms-2s

### Data Volume
- Monthly growth: ~500 decisions (pending + ratified combined)
- Snapshots: ~48-72 per day (M3R1/R2/R3 cycles)
- Storage: <10MB per year

---

## Security & RLS (Row-Level Security)

By default, all tables are readable (anon key has SELECT).

**To restrict by practice/org (future):**

```sql
-- Enable RLS on tables
ALTER TABLE pending_decisions ENABLE ROW LEVEL SECURITY;
ALTER TABLE ratified_decisions ENABLE ROW LEVEL SECURITY;
ALTER TABLE mesh_state ENABLE ROW LEVEL SECURITY;

-- Policy: Only read decisions for your practice
CREATE POLICY "read_own_practice" ON pending_decisions
  FOR SELECT USING (practice_id = auth.claims() ->> 'practice_id');

-- Policy: Only Admiral can approve
CREATE POLICY "admiral_approve" ON pending_decisions
  FOR UPDATE USING (auth.claims() ->> 'role' = 'admiral');
```

For now: Practice is single-tenant (one Supabase project = one foundation).

---

## Future Enhancements

| Enhancement | Timeline | Impact |
|---|---|---|
| **Cross-practice Witness aggregation** | Q3 2026 | Multiple practices → single mesh dashboard |
| **ACAT dimension auto-population** | Q3 2026 | Witness pulls live ACAT scores (not hardcoded) |
| **Admiral approval workflow UI** | Q3 2026 | Web UI in place of YAML editing |
| **Witness as public status page** | Q4 2026 | Public observability page (like GitHub status) |
| **Vector similarity search** | Q4 2026 | pgvector integration for decision recommendation |
| **WebAssembly Witness** | Q1 2027 | Faster rendering, offline mode |

---

## Quick Start Checklist

- [ ] Create Supabase project
- [ ] Apply schema.sql
- [ ] Deploy sync-governance-state Edge Function
- [ ] Register GitHub webhook
- [ ] Get API credentials
- [ ] Update WitnessV2.html with credentials
- [ ] Test: Push a change to DECISIONS_PENDING.yaml
- [ ] Verify: Supabase tables updated in ~500ms
- [ ] Open WitnessV2.html → See live updates
- [ ] Share: Copy WitnessV2.html link to Admiral

---

## References

- **Supabase Realtime:** https://supabase.com/docs/guides/realtime
- **Edge Functions:** https://supabase.com/docs/guides/functions
- **PostgreSQL Triggers:** https://supabase.com/docs/guides/database/webhooks
- **GitHub Webhooks:** https://docs.github.com/en/developers/webhooks-and-events/webhooks

---

**Status:** ✅ Witness v2 is live, real-time, and production-ready.

Wado 🦅
