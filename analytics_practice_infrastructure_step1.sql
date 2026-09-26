-- Analytics Practice Infrastructure Setup — Step 1
-- Created: 2026-09-11 14:25 UTC
-- Purpose: Events, SER Coordination, and Blocker Routing tables for Phase 3 measurement
-- Scope: empirica-foundation.carly.empirica-analytics practice tables
-- Status: AUTHORIZED for deployment

-- ============================================
-- TABLE 1: ORCHESTRATION_EVENTS
-- ============================================
-- Proposal routing telemetry for mesh coordination measurement
-- Tracks: proposal_id, source_claude, target_claudes, status transitions, latency

CREATE TABLE IF NOT EXISTS orchestration_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID NOT NULL,

    -- Event identification
    proposal_id VARCHAR(100) NOT NULL,
    event_type VARCHAR(50) NOT NULL,  -- proposal_event, ser_escalation, etc.

    -- Actors
    source_claude VARCHAR(255) NOT NULL,  -- e.g., empirica-foundation.carly.empirica-mesh-support
    target_claudes TEXT NOT NULL,  -- JSON array of target ai_ids

    -- Status tracking
    status VARCHAR(50) NOT NULL,  -- accepted, changed, declined, completed, shipped, failed
    action_category VARCHAR(50),  -- TACTICAL, STRATEGIC, OPERATIONAL

    -- Timing (for latency measurement)
    emitted_at TIMESTAMP WITH TIME ZONE NOT NULL,
    received_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    latency_ms INTEGER GENERATED ALWAYS AS (
        EXTRACT(EPOCH FROM (received_at - emitted_at)) * 1000
    ) STORED,

    -- Metadata
    proposal_title TEXT,
    payload_summary JSONB,  -- Compressed payload (full body in cortex)
    eco_actor VARCHAR(255),  -- ECO decision maker
    change_kind VARCHAR(50),  -- new, changed, resolved

    -- Audit
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by VARCHAR(255),

    -- Foreign key placeholder (link to Cortex if needed)
    cortex_project_id VARCHAR(100),

    CONSTRAINT valid_event_type CHECK (event_type IN ('proposal_event', 'ser_escalation', 'collab_brief', 'spec_updated')),
    CONSTRAINT valid_status CHECK (status IN ('accepted', 'changed', 'declined', 'completed', 'shipped', 'failed', 'eco_review'))
);

CREATE INDEX idx_orchestration_events_proposal_id ON orchestration_events(proposal_id);
CREATE INDEX idx_orchestration_events_source ON orchestration_events(source_claude);
CREATE INDEX idx_orchestration_events_status ON orchestration_events(status);
CREATE INDEX idx_orchestration_events_created_at ON orchestration_events(created_at DESC);
CREATE INDEX idx_orchestration_events_latency ON orchestration_events(latency_ms);

-- Hypertable for time-series analysis (if TimescaleDB available)
-- SELECT create_hypertable('orchestration_events', 'created_at', if_not_exists => true);

COMMENT ON TABLE orchestration_events IS 'Proposal routing telemetry for mesh coordination. Measures: delivery latency, proposal status transitions, actor involvement.';

-- ============================================
-- TABLE 2: SER_COORDINATION
-- ============================================
-- Shared Epistemic Record (SER) state tracking for escalation monitoring
-- Tracks: SER lifecycle, participant acks, escalation history

CREATE TABLE IF NOT EXISTS ser_coordination (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID NOT NULL,

    -- SER identification
    ser_id VARCHAR(100) NOT NULL UNIQUE,
    ser_title VARCHAR(255),
    ser_state VARCHAR(50) NOT NULL,  -- open, in_progress, blocked, closed

    -- Participants (array of structured participants)
    participants JSONB NOT NULL,  -- [{ai_id, role: required|participating|observer, last_action_at, last_ack_at}, ...]

    -- Escalation tracking
    escalation_enabled BOOLEAN DEFAULT true,
    escalation_interval_seconds INTEGER DEFAULT 600,
    last_escalation_at TIMESTAMP WITH TIME ZONE,
    escalation_count INTEGER DEFAULT 0,
    idle_for_seconds INTEGER,

    -- State transitions
    last_transition_at TIMESTAMP WITH TIME ZONE,
    last_transition_actor VARCHAR(255),
    transition_history JSONB,  -- [{timestamp, actor, from_state, to_state, note}, ...]

    -- Coordination metrics
    total_participants INTEGER,
    acked_participants INTEGER,
    required_participants_acked BOOLEAN,  -- false = escalation needed

    -- Scope & visibility
    visibility VARCHAR(50) DEFAULT 'private',  -- private, org, global
    project_ids TEXT,  -- Comma-separated cortex project_ids involved

    -- Audit
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by VARCHAR(255),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CONSTRAINT valid_ser_state CHECK (ser_state IN ('open', 'in_progress', 'blocked', 'closed')),
    CONSTRAINT valid_visibility CHECK (visibility IN ('private', 'org', 'global'))
);

CREATE INDEX idx_ser_coordination_ser_id ON ser_coordination(ser_id);
CREATE INDEX idx_ser_coordination_state ON ser_coordination(ser_state);
CREATE INDEX idx_ser_coordination_created_at ON ser_coordination(created_at DESC);
CREATE INDEX idx_ser_coordination_escalation_enabled ON ser_coordination(escalation_enabled) WHERE escalation_enabled = true;
CREATE INDEX idx_ser_coordination_required_acked ON ser_coordination(required_participants_acked) WHERE required_participants_acked = false;

COMMENT ON TABLE ser_coordination IS 'Shared Epistemic Record tracking for sustained multi-practice coordination. Measures: escalation frequency, ack latency, participant engagement, state stability.';

-- ============================================
-- TABLE 3: BLOCKER_ROUTING
-- ============================================
-- Tactical blocker tracking for queue metrics and resolution latency
-- Tracks: blocker_id, source_practice, affected_practices, priority, resolution_status

CREATE TABLE IF NOT EXISTS blocker_routing (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID NOT NULL,

    -- Blocker identification
    blocker_id VARCHAR(100) NOT NULL UNIQUE,
    blocker_title VARCHAR(255) NOT NULL,
    description TEXT,

    -- Classification
    blocker_type VARCHAR(50) NOT NULL,  -- resource, dependency, authorization, escalation
    priority VARCHAR(20) NOT NULL DEFAULT 'medium',  -- critical, high, medium, low
    category VARCHAR(100),  -- EU_AI_ACT, LEGAL, TECHNICAL, RESOURCE, etc.

    -- Routing & Ownership
    source_practice VARCHAR(255) NOT NULL,  -- which practice surfaced the blocker
    affected_practices TEXT NOT NULL,  -- JSON array of ai_ids impacted
    assigned_to VARCHAR(255),  -- ai_id or team responsible for resolution
    escalated_to VARCHAR(255),  -- if escalated (e.g., Admiral)

    -- Status tracking
    status VARCHAR(50) NOT NULL DEFAULT 'open',  -- open, acknowledged, in_progress, resolved, wont_fix
    status_changed_at TIMESTAMP WITH TIME ZONE,

    -- Timing metrics
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    acknowledged_at TIMESTAMP WITH TIME ZONE,
    resolution_started_at TIMESTAMP WITH TIME ZONE,
    resolved_at TIMESTAMP WITH TIME ZONE,

    acknowledge_latency_ms INTEGER GENERATED ALWAYS AS (
        CASE WHEN acknowledged_at IS NOT NULL
            THEN EXTRACT(EPOCH FROM (acknowledged_at - created_at)) * 1000
            ELSE NULL
        END
    ) STORED,

    resolution_latency_ms INTEGER GENERATED ALWAYS AS (
        CASE WHEN resolved_at IS NOT NULL
            THEN EXTRACT(EPOCH FROM (resolved_at - created_at)) * 1000
            ELSE NULL
        END
    ) STORED,

    -- Context
    related_ser_id VARCHAR(100),  -- Link to SER if coordinated through one
    related_proposal_id VARCHAR(100),  -- Link to proposal if coordinated through proposal
    resolution_notes TEXT,

    -- Resource impact
    practices_labor_hours DECIMAL(10, 2),  -- Estimated labor to resolve

    CONSTRAINT valid_blocker_type CHECK (blocker_type IN ('resource', 'dependency', 'authorization', 'escalation', 'other')),
    CONSTRAINT valid_priority CHECK (priority IN ('critical', 'high', 'medium', 'low')),
    CONSTRAINT valid_status CHECK (status IN ('open', 'acknowledged', 'in_progress', 'resolved', 'wont_fix'))
);

CREATE INDEX idx_blocker_routing_blocker_id ON blocker_routing(blocker_id);
CREATE INDEX idx_blocker_routing_status ON blocker_routing(status);
CREATE INDEX idx_blocker_routing_source_practice ON blocker_routing(source_practice);
CREATE INDEX idx_blocker_routing_priority ON blocker_routing(priority);
CREATE INDEX idx_blocker_routing_created_at ON blocker_routing(created_at DESC);
CREATE INDEX idx_blocker_routing_acknowledge_latency ON blocker_routing(acknowledge_latency_ms);
CREATE INDEX idx_blocker_routing_resolution_latency ON blocker_routing(resolution_latency_ms);
CREATE INDEX idx_blocker_routing_open_unacked ON blocker_routing(status, acknowledged_at) WHERE status = 'open' AND acknowledged_at IS NULL;

COMMENT ON TABLE blocker_routing IS 'Tactical blocker routing & queue metrics. Measures: blocker surfacing rate, acknowledge latency, resolution latency, practice labor allocation.';

-- ============================================
-- VIEWS FOR MEASUREMENT
-- ============================================

-- Proposal delivery latency summary
CREATE OR REPLACE VIEW v_proposal_latency_summary AS
SELECT
    DATE(created_at) as date,
    source_claude,
    AVG(latency_ms) as avg_latency_ms,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY latency_ms) as p50_latency_ms,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY latency_ms) as p95_latency_ms,
    MAX(latency_ms) as max_latency_ms,
    COUNT(*) as event_count
FROM orchestration_events
WHERE org_id IS NOT NULL
GROUP BY DATE(created_at), source_claude
ORDER BY DATE(created_at) DESC;

-- SER escalation frequency
CREATE OR REPLACE VIEW v_ser_escalation_summary AS
SELECT
    ser_id,
    ser_state,
    escalation_count,
    idle_for_seconds,
    required_participants_acked,
    (EXTRACT(EPOCH FROM (NOW() - created_at))) / 3600 as age_hours
FROM ser_coordination
WHERE escalation_enabled = true
ORDER BY escalation_count DESC;

-- Blocker resolution metrics
CREATE OR REPLACE VIEW v_blocker_resolution_metrics AS
SELECT
    DATE(created_at) as date,
    source_practice,
    priority,
    COUNT(*) as total_blockers,
    COUNT(*) FILTER (WHERE status = 'resolved') as resolved_count,
    COUNT(*) FILTER (WHERE status IN ('open', 'acknowledged')) as pending_count,
    AVG(acknowledge_latency_ms) as avg_ack_latency_ms,
    AVG(resolution_latency_ms) as avg_resolution_latency_ms
FROM blocker_routing
WHERE org_id IS NOT NULL
GROUP BY DATE(created_at), source_practice, priority
ORDER BY DATE(created_at) DESC;

-- ============================================
-- DEPLOYMENT NOTES
-- ============================================

-- This migration creates three tables for Phase 3 Analytics Practice infrastructure:
--
-- 1. orchestration_events — Proposal routing telemetry (mesh-support + autonomy responsibility)
--    Measurement: delivery latency, proposal status transitions, mesh activity volume
--
-- 2. ser_coordination — SER lifecycle tracking (autonomy responsibility)
--    Measurement: escalation frequency, participant ack rate, coordination latency
--
-- 3. blocker_routing — Tactical blocker queue (mesh-support responsibility)
--    Measurement: blocker acknowledge time, resolution time, practice labor allocation
--
-- Views provided for immediate analysis:
--   - v_proposal_latency_summary: delivery latency by source practice
--   - v_ser_escalation_summary: escalation history & current state
--   - v_blocker_resolution_metrics: blocker lifecycle metrics
--
-- Status: Ready for deployment to analytics practice DB
-- Next step: Wire telemetry pipeline (mesh-support Cortex events, autonomy SER polling)

