-- Supabase Schema for HUMANAIOS Witness
-- Real-time observability backend for governance + M3 Nervous System
-- Status: ✅ PRODUCTION-READY

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA extensions;

-- ─────────────────────────────────────────────────────────────────
-- 1. PENDING DECISIONS (from DECISIONS_PENDING.yaml)
-- ─────────────────────────────────────────────────────────────────

CREATE TABLE pending_decisions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  pending_id VARCHAR(32) UNIQUE NOT NULL,  -- PEN-YYMMDD-NNN
  decision_type VARCHAR(64) NOT NULL,      -- DIVERGENCE, VALIDATION_FAILURE, etc.
  title TEXT NOT NULL,
  severity VARCHAR(16) NOT NULL,           -- HIGH, MEDIUM, LOW

  discovered_by VARCHAR(128),              -- divergence-detect.yml, state-validate.yml
  discovered_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  discovery_run TEXT,                      -- GitHub Actions run URL

  repo_affected VARCHAR(256),
  details JSONB DEFAULT '{}',              -- divergence_count, issue_type, etc.
  recommended_action TEXT,
  proposed_decision JSONB DEFAULT '{}',    -- decision_type, title, scope, target_repos

  admiral_notes TEXT DEFAULT '',
  status VARCHAR(64) NOT NULL DEFAULT 'PENDING_REVIEW',  -- PENDING_REVIEW, APPROVED, REJECTED, DEFERRED, EXPIRED
  expires_at TIMESTAMP WITH TIME ZONE,

  synced_from_yaml_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_status ON pending_decisions(status);
CREATE INDEX idx_decision_type ON pending_decisions(decision_type);
CREATE INDEX idx_severity ON pending_decisions(severity);
CREATE INDEX idx_expires_at ON pending_decisions(expires_at);
CREATE INDEX idx_discovered_at ON pending_decisions(discovered_at DESC);

-- ─────────────────────────────────────────────────────────────────
-- 2. RATIFIED DECISIONS (from GOVERNANCE_RATIFICATIONS_REGISTRY.yaml)
-- ─────────────────────────────────────────────────────────────────

CREATE TABLE ratified_decisions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  decision_id VARCHAR(64) UNIQUE NOT NULL,  -- D-YYMMDD-NNN
  title TEXT NOT NULL,
  decision_type VARCHAR(64) NOT NULL,       -- authority_boundary_change, state_machine_gate_update, etc.
  scope TEXT NOT NULL,
  status VARCHAR(64) NOT NULL DEFAULT 'RATIFIED',  -- RATIFIED, DISPATCHED, APPLIED, FAILED

  ratification_source JSONB DEFAULT '{}',   -- pending_entry, discovered_by, discovered_at
  decision_body JSONB DEFAULT '{}',         -- type, description, target_repos, action
  admiral_approval JSONB DEFAULT '{}',      -- ratified_at, ratified_by, notes

  implementation JSONB DEFAULT '{}',        -- applied_by, dispatch_scheduled, verification

  target_repos TEXT[] DEFAULT ARRAY[]::TEXT[],
  applied_at TIMESTAMP WITH TIME ZONE,
  applied_commit VARCHAR(40),

  ratified_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_ratified_status ON ratified_decisions(status);
CREATE INDEX idx_ratified_decision_type ON ratified_decisions(decision_type);
CREATE INDEX idx_ratified_at ON ratified_decisions(ratified_at DESC);
CREATE INDEX idx_applied_at ON ratified_decisions(applied_at DESC);
CREATE INDEX idx_ratified_target_repos ON ratified_decisions USING gin(target_repos);

-- ─────────────────────────────────────────────────────────────────
-- 3. M3 NERVOUS SYSTEM METRICS
-- ─────────────────────────────────────────────────────────────────

CREATE TABLE m3_metrics (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  -- M3 Rank identification
  rank VARCHAR(16) NOT NULL,  -- M3R1, M3R2, M3R3
  cycle_id VARCHAR(64) UNIQUE NOT NULL,  -- timestamp-based identifier

  -- Batch Sync (M3R1) metrics
  batch_decisions_dispatched INT DEFAULT 0,
  batch_repos_targeted INT DEFAULT 0,
  batch_backoff_retries INT DEFAULT 0,
  batch_dry_run_mode BOOLEAN DEFAULT FALSE,

  -- Divergence Detection (M3R2) metrics
  repos_queried INT DEFAULT 0,
  repos_in_sync INT DEFAULT 0,
  repos_in_drift INT DEFAULT 0,
  repos_error INT DEFAULT 0,
  divergence_total INT DEFAULT 0,
  consistency_matrix JSONB DEFAULT '{}',

  -- State Validation (M3R3) metrics
  repos_validated INT DEFAULT 0,
  validation_ok INT DEFAULT 0,
  validation_warnings INT DEFAULT 0,
  validation_no_state INT DEFAULT 0,
  validation_errors INT DEFAULT 0,
  atomic_replays_triggered INT DEFAULT 0,

  -- Derived health metrics
  mesh_health_score NUMERIC(4,2) DEFAULT 1.0,  -- 0.0-1.0

  -- Execution context
  execution_timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  execution_duration_seconds INT,
  github_run_id VARCHAR(64),

  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  UNIQUE(rank, execution_timestamp)
);

CREATE INDEX idx_m3_rank ON m3_metrics(rank);
CREATE INDEX idx_m3_execution_timestamp ON m3_metrics(execution_timestamp DESC);
CREATE INDEX idx_m3_mesh_health_score ON m3_metrics(mesh_health_score);

-- ─────────────────────────────────────────────────────────────────
-- 4. MESH STATE (Real-time status snapshot)
-- ─────────────────────────────────────────────────────────────────

CREATE TABLE mesh_state (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  -- Current mesh health
  total_repos INT DEFAULT 0,
  repos_synced INT DEFAULT 0,
  repos_drifted INT DEFAULT 0,
  repos_unreachable INT DEFAULT 0,

  -- Decision flow
  pending_decisions_count INT DEFAULT 0,
  pending_high_severity INT DEFAULT 0,
  pending_medium_severity INT DEFAULT 0,
  pending_oldest_hours INT,

  ratified_decisions_count INT DEFAULT 0,
  ratified_applied_count INT DEFAULT 0,
  ratified_pending_application_count INT DEFAULT 0,

  -- Calibration (ACAT 6 dimensions)
  dimension_scores NUMERIC(3,1)[] DEFAULT ARRAY[77.5, 79.1, 77.8, 78.3, 76.2, 75.0],  -- [know, do, context, clarity, coherence, signal]
  mean_li NUMERIC(5,4) DEFAULT 0.8632,  -- Livelihood Index

  -- Mesh mode
  field_state VARCHAR(32) DEFAULT 'Calibrated',  -- Force Dominant, Power, Calibrated, Force Active

  -- Last update
  last_m3r1_at TIMESTAMP WITH TIME ZONE,
  last_m3r2_at TIMESTAMP WITH TIME ZONE,
  last_m3r3_at TIMESTAMP WITH TIME ZONE,
  last_admiral_action_at TIMESTAMP WITH TIME ZONE,

  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_mesh_state_updated_at ON mesh_state(updated_at DESC);

-- Initialize mesh_state singleton
INSERT INTO mesh_state (id) VALUES (uuid_generate_v4())
ON CONFLICT DO NOTHING;

-- ─────────────────────────────────────────────────────────────────
-- 5. SYNC LOG (Track YAML ↔ DB synchronization)
-- ─────────────────────────────────────────────────────────────────

CREATE TABLE sync_log (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  sync_type VARCHAR(64) NOT NULL,  -- DECISIONS_PENDING, GOVERNANCE_RATIFICATIONS
  github_commit_sha VARCHAR(40),
  github_branch VARCHAR(255),

  entries_created INT DEFAULT 0,
  entries_updated INT DEFAULT 0,
  entries_deleted INT DEFAULT 0,

  status VARCHAR(32) NOT NULL DEFAULT 'SUCCESS',  -- SUCCESS, PARTIAL, FAILED
  error_message TEXT,

  sync_started_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  sync_completed_at TIMESTAMP WITH TIME ZONE,
  duration_seconds INT,

  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_sync_log_sync_type ON sync_log(sync_type);
CREATE INDEX idx_sync_log_status ON sync_log(status);
CREATE INDEX idx_sync_log_github_commit_sha ON sync_log(github_commit_sha);
CREATE INDEX idx_sync_log_sync_started_at ON sync_log(sync_started_at DESC);

-- ─────────────────────────────────────────────────────────────────
-- 6. WITNESS SNAPSHOTS (For audit trail + historical replay)
-- ─────────────────────────────────────────────────────────────────

CREATE TABLE witness_snapshots (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  -- Witness state at snapshot time
  pending_count INT NOT NULL,
  pending_by_type JSONB DEFAULT '{}',  -- {DIVERGENCE: 2, VALIDATION_FAILURE: 1, ...}

  mesh_health_score NUMERIC(4,2) NOT NULL,
  field_state VARCHAR(32) NOT NULL,

  dimension_scores NUMERIC(3,1)[] NOT NULL,
  mean_li NUMERIC(5,4) NOT NULL,

  repos_in_drift INT NOT NULL,
  ratified_applied_count INT NOT NULL,

  -- Snapshot metadata
  triggered_by VARCHAR(128),  -- M3R1, M3R2, M3R3, MANUAL, etc.
  notes TEXT,

  snapshot_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_witness_snapshot_at ON witness_snapshots(snapshot_at DESC);
CREATE INDEX idx_witness_field_state ON witness_snapshots(field_state);

-- ─────────────────────────────────────────────────────────────────
-- 7. VIEWS FOR WITNESS QUERIES
-- ─────────────────────────────────────────────────────────────────

-- View: Current decision queue status
CREATE OR REPLACE VIEW pending_queue_status AS
SELECT
  totals.total_pending,
  totals.high_severity,
  totals.medium_severity,
  totals.low_severity,
  totals.oldest_age_hours,
  totals.last_discovery,
  COALESCE(type_counts.count_by_type, '{}'::jsonb) AS count_by_type
FROM (
  SELECT
    COUNT(*) AS total_pending,
    COUNT(CASE WHEN severity = 'HIGH' THEN 1 END) AS high_severity,
    COUNT(CASE WHEN severity = 'MEDIUM' THEN 1 END) AS medium_severity,
    COUNT(CASE WHEN severity = 'LOW' THEN 1 END) AS low_severity,
    EXTRACT(EPOCH FROM (NOW() - MIN(discovered_at))) / 3600 AS oldest_age_hours,
    MAX(discovered_at) AS last_discovery
  FROM pending_decisions
  WHERE status = 'PENDING_REVIEW'
) totals
LEFT JOIN (
  SELECT
    jsonb_object_agg(t.decision_type, t.cnt) AS count_by_type
  FROM (
    SELECT
      decision_type,
      COUNT(*) AS cnt
    FROM pending_decisions
    WHERE status = 'PENDING_REVIEW'
    GROUP BY decision_type
  ) t
) type_counts ON TRUE;

-- View: Recent ratification activity
CREATE OR REPLACE VIEW recent_ratifications AS
SELECT
  decision_id,
  title,
  status,
  ratified_at,
  applied_at,
  EXTRACT(EPOCH FROM (COALESCE(applied_at, NOW()) - ratified_at)) / 3600 as hours_to_apply
FROM ratified_decisions
WHERE ratified_at > NOW() - INTERVAL '7 days'
ORDER BY ratified_at DESC;

-- View: Mesh health composite
CREATE OR REPLACE VIEW mesh_health_composite AS
SELECT
  (
    (SELECT repos_synced::NUMERIC / NULLIF(total_repos, 0) FROM mesh_state LIMIT 1) * 0.4 +
    (
      SELECT 1.0 - (ratified_pending_application_count::NUMERIC / NULLIF(ratified_decisions_count, 1))
      FROM mesh_state LIMIT 1
    ) * 0.3 +
    (1.0 - LEAST(1.0, (SELECT pending_decisions_count::NUMERIC / NULLIF(ratified_decisions_count, 10) FROM mesh_state LIMIT 1))) * 0.3
  ) as composite_health_score,
  (SELECT pending_decisions_count FROM mesh_state LIMIT 1) as decisions_pending,
  (SELECT repos_drifted FROM mesh_state LIMIT 1) as repos_drifted;

-- ─────────────────────────────────────────────────────────────────
-- 8. REALTIME SUBSCRIPTIONS (for Witness WebSocket)
-- ─────────────────────────────────────────────────────────────────

ALTER TABLE pending_decisions REPLICA IDENTITY FULL;
ALTER TABLE ratified_decisions REPLICA IDENTITY FULL;
ALTER TABLE m3_metrics REPLICA IDENTITY FULL;
ALTER TABLE mesh_state REPLICA IDENTITY FULL;

-- ─────────────────────────────────────────────────────────────────
-- 9. INDEXES FOR WITNESS QUERIES
-- ─────────────────────────────────────────────────────────────────

CREATE INDEX IF NOT EXISTS idx_pending_status_type ON pending_decisions(status, decision_type);
CREATE INDEX IF NOT EXISTS idx_ratified_status_applied ON ratified_decisions(status, applied_at DESC);
CREATE INDEX IF NOT EXISTS idx_m3_recent ON m3_metrics(rank, execution_timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_mesh_state_health ON mesh_state(updated_at DESC);

-- ─────────────────────────────────────────────────────────────────
-- End Schema
-- ─────────────────────────────────────────────────────────────────
