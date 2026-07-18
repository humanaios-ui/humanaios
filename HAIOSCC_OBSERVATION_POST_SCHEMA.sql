-- HAIOSCC Observation Post Schema
-- Empirica Foundation Evaluator + Three-Layer Monitoring
--
-- This schema combines Zone-3 operations (original) + observation post extensions
-- Status: Ready for application to Supabase project ksinisdzgtnqzsymhfya
-- Date: 2026-07-18

-- ============================================================================
-- PART 1: FOUNDATIONAL TABLES (Zone-3 Operations)
-- ============================================================================

-- operational_state: Single-row system heartbeat
CREATE TABLE IF NOT EXISTS operational_state (
    id BIGSERIAL PRIMARY KEY,
    pipeline_status TEXT NOT NULL DEFAULT 'GREEN', -- GREEN/YELLOW/RED
    runway_days INTEGER NOT NULL DEFAULT 365,
    critical_count INTEGER NOT NULL DEFAULT 0,
    session_id UUID NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT operational_state_single_row CHECK (id = 1)
);

-- zone3_queue: Execution items for Night operator
CREATE TABLE IF NOT EXISTS zone3_queue (
    id BIGSERIAL PRIMARY KEY,
    item_key TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    severity TEXT NOT NULL, -- CRITICAL/WARN/INFO
    zone TEXT NOT NULL DEFAULT 'zone3', -- zone1/zone2/zone3
    owner TEXT,
    verification_kind TEXT NOT NULL, -- github_pr/cf_cache/manual_confirm/workflow_run/etc
    verification_target TEXT, -- PR#, cache key, manual description, workflow id, etc
    resolved_at TIMESTAMPTZ,
    resolution_evidence JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT zone3_queue_unique_unresolved UNIQUE NULLS NOT DISTINCT (item_key, resolved_at)
);

-- verification_log: Audit trail of verification runs
CREATE TABLE IF NOT EXISTS verification_log (
    id BIGSERIAL PRIMARY KEY,
    queue_item_id BIGINT REFERENCES zone3_queue(id),
    verification_kind TEXT NOT NULL,
    verification_target TEXT,
    result JSONB NOT NULL, -- {ok: bool, evidence: string, error?: string}
    triggered_by TEXT NOT NULL, -- manual/scheduler/action_button
    triggered_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- collaborators: Team tracking
CREATE TABLE IF NOT EXISTS collaborators (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL, -- PI/Researcher/Lead/Support
    email TEXT,
    status TEXT NOT NULL DEFAULT 'active', -- active/inactive/on_leave
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- funding_pipeline: Budget tracking
CREATE TABLE IF NOT EXISTS funding_pipeline (
    id BIGSERIAL PRIMARY KEY,
    source TEXT NOT NULL, -- Longview/Mellon/Grant/Fellowship
    status TEXT NOT NULL, -- pending/approved/in_progress/completed
    amount_requested DECIMAL(12,2),
    amount_approved DECIMAL(12,2),
    track TEXT, -- A/B/C for Longview tracks
    decision_date DATE,
    deployment_date DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- integrations_registry: External service status
CREATE TABLE IF NOT EXISTS integrations_registry (
    id BIGSERIAL PRIMARY KEY,
    service_name TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL, -- connected/error/pending
    last_checked_at TIMESTAMPTZ,
    error_message TEXT
);

-- ic_ledger: Correction ledger (assumptions invalidated)
CREATE TABLE IF NOT EXISTS ic_ledger (
    id BIGSERIAL PRIMARY KEY,
    assumption_id TEXT NOT NULL,
    assumption_text TEXT NOT NULL,
    invalidated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    evidence TEXT NOT NULL,
    gate_num INTEGER, -- which gate revealed the invalidation
    correction_action TEXT NOT NULL, -- what changed as a result
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- PART 2: OBSERVATION POST TABLES (Three-Layer Measurement)
-- ============================================================================

-- ser_status: Shared Epistemic Record tracking (SER 1-4)
CREATE TABLE IF NOT EXISTS ser_status (
    id BIGSERIAL PRIMARY KEY,
    ser_num INTEGER NOT NULL UNIQUE CHECK (ser_num >= 1 AND ser_num <= 4),
    name TEXT NOT NULL,
    description TEXT,
    current_state TEXT NOT NULL, -- open/in_progress/blocked/closed
    participants JSONB NOT NULL, -- [{practice_id, role: required/participating}]
    escalation_deadline TIMESTAMPTZ,
    escalation_rule_days INTEGER,
    last_verified_at TIMESTAMPTZ,
    last_ack_from JSONB, -- {practice_id: timestamp}
    evidence JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- layer_1_metrics: HumanAIOS SMAG Learning Density
CREATE TABLE IF NOT EXISTS layer_1_metrics (
    id BIGSERIAL PRIMARY KEY,
    measurement_date DATE NOT NULL UNIQUE,
    smag_learning_density_raw DECIMAL(5,2) NOT NULL, -- percentage
    smag_learning_density_adjusted DECIMAL(5,2) NOT NULL, -- Copilot-confidence weighted
    copilot_confidence_avg DECIMAL(3,2), -- 0.0-1.0
    trajectory_count INTEGER,
    target_density DECIMAL(5,2), -- for this gate
    on_track_for_gate BOOLEAN,
    trend TEXT, -- improving/stable/declining
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- layer_2_copilot: GitHub Copilot AI Signals
CREATE TABLE IF NOT EXISTS layer_2_copilot (
    id BIGSERIAL PRIMARY KEY,
    measurement_date DATE NOT NULL,
    avg_confidence DECIMAL(3,2) NOT NULL, -- 0.0-1.0, target 0.75+
    confidence_trend TEXT, -- improving/stable/declining
    confidence_variance DECIMAL(3,2), -- consistency
    bias_audit_status TEXT, -- pending/in_progress/complete
    criterion_4_bias_score DECIMAL(3,2), -- 0.0-1.0, target <0.15
    model_variance_r_raw JSONB, -- {claude: 0.72, gpt4: 0.61, custom: 0.58}
    model_variance_r_adjusted JSONB, -- after Copilot bias removal
    findings TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT layer_2_unique_date UNIQUE(measurement_date)
);

-- layer_3_gates: Empirica Gate Decisions
CREATE TABLE IF NOT EXISTS layer_3_gates (
    id BIGSERIAL PRIMARY KEY,
    gate_num INTEGER NOT NULL UNIQUE,
    gate_date DATE,
    predicted_outcome TEXT,
    measured_outcome TEXT,
    gap_analysis TEXT,
    learning TEXT,
    action TEXT,
    status TEXT NOT NULL DEFAULT 'pending', -- pending/open/postflight_ready/closed
    postflight_logged_at TIMESTAMPTZ,
    postflight_evidence JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- learning_velocity: Progress toward gate targets
CREATE TABLE IF NOT EXISTS learning_velocity (
    id BIGSERIAL PRIMARY KEY,
    week_starting DATE NOT NULL,
    gate_target INTEGER NOT NULL, -- which gate this is measuring toward
    density_target DECIMAL(5,2),
    density_actual DECIMAL(5,2),
    copilot_confidence_target DECIMAL(3,2),
    copilot_confidence_actual DECIMAL(3,2),
    trend TEXT, -- on_track/at_risk/behind
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT learning_velocity_unique UNIQUE(week_starting, gate_target)
);

-- three_layer_harmony: Cross-layer flow metrics
CREATE TABLE IF NOT EXISTS three_layer_harmony (
    id BIGSERIAL PRIMARY KEY,
    measurement_date DATE NOT NULL UNIQUE,
    -- Directional flows
    layer1_to_layer2_flowing BOOLEAN, -- SMAG → Copilot confidence
    layer3_to_layer2_flowing BOOLEAN, -- Gate discoveries → Copilot context
    layer2_to_layer3_flowing BOOLEAN, -- Copilot bias audit → Criterion validity
    layer1_to_layer3_flowing BOOLEAN, -- Learning velocity → Deployment readiness
    -- Overall status
    overall_status TEXT NOT NULL, -- GOOD/AT_RISK/BLOCKED
    flow_details JSONB,
    last_break_point TEXT, -- which flow last broke
    remediation_action TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- escalations: Automatic escalation tracking (7-day, 10-day, 14-day rules)
CREATE TABLE IF NOT EXISTS escalations (
    id BIGSERIAL PRIMARY KEY,
    ser_id INTEGER REFERENCES ser_status(id),
    trigger_rule TEXT NOT NULL, -- "copilot_confidence<0.70", "bias_audit_incomplete", "empirica_feedback_blocked", etc
    triggered_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    escalation_deadline TIMESTAMPTZ NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending', -- pending/resolved/overdue
    resolved_at TIMESTAMPTZ,
    evidence_of_resolution TEXT,
    escalation_target TEXT, -- "David Van Assche" / "DeMarius Lawson" / "Admiral"
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- weekly_snapshots: SER state + metrics at rhythm checkpoints
CREATE TABLE IF NOT EXISTS weekly_snapshots (
    id BIGSERIAL PRIMARY KEY,
    snapshot_date DATE NOT NULL, -- Monday of the week
    snapshot_type TEXT NOT NULL, -- monday_9am/wednesday_2pm/friday_4pm
    ser_1_state JSONB, -- {status, escalation_days_remaining, last_verified}
    ser_2_state JSONB,
    ser_3_state JSONB,
    ser_4_state JSONB,
    layer_1_snapshot JSONB, -- SMAG metrics
    layer_2_snapshot JSONB, -- Copilot signals
    layer_3_snapshot JSONB, -- Gate status
    harmony_status TEXT, -- GOOD/AT_RISK/BLOCKED
    escalations_pending INTEGER,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT weekly_snapshots_unique UNIQUE(snapshot_date, snapshot_type)
);

-- gate_postflight_log: Complete record of each gate's learning
CREATE TABLE IF NOT EXISTS gate_postflight_log (
    id BIGSERIAL PRIMARY KEY,
    gate_num INTEGER NOT NULL,
    gate_close_date DATE NOT NULL,
    postflight_create_date DATE NOT NULL,
    predicted_outcome TEXT NOT NULL,
    measured_outcome TEXT NOT NULL,
    gap_analysis TEXT NOT NULL,
    learning TEXT NOT NULL,
    action_for_next_gate TEXT NOT NULL,
    impact_score DECIMAL(3,2), -- 0.0-1.0
    trajectory_created BOOLEAN DEFAULT FALSE,
    empirica_finding_id TEXT, -- link to empirica finding-log entry
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- ROW-LEVEL SECURITY (RLS) — Service role only, no anon access
-- ============================================================================

-- Enable RLS on all tables
ALTER TABLE operational_state ENABLE ROW LEVEL SECURITY;
ALTER TABLE zone3_queue ENABLE ROW LEVEL SECURITY;
ALTER TABLE verification_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE collaborators ENABLE ROW LEVEL SECURITY;
ALTER TABLE funding_pipeline ENABLE ROW LEVEL SECURITY;
ALTER TABLE integrations_registry ENABLE ROW LEVEL SECURITY;
ALTER TABLE ic_ledger ENABLE ROW LEVEL SECURITY;
ALTER TABLE ser_status ENABLE ROW LEVEL SECURITY;
ALTER TABLE layer_1_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE layer_2_copilot ENABLE ROW LEVEL SECURITY;
ALTER TABLE layer_3_gates ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_velocity ENABLE ROW LEVEL SECURITY;
ALTER TABLE three_layer_harmony ENABLE ROW LEVEL SECURITY;
ALTER TABLE escalations ENABLE ROW LEVEL SECURITY;
ALTER TABLE weekly_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE gate_postflight_log ENABLE ROW LEVEL SECURITY;

-- Service role (only for Cloudflare Functions) can access all
CREATE POLICY "service_role_all" ON operational_state FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "service_role_all" ON zone3_queue FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "service_role_all" ON verification_log FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "service_role_all" ON collaborators FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "service_role_all" ON funding_pipeline FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "service_role_all" ON integrations_registry FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "service_role_all" ON ic_ledger FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "service_role_all" ON ser_status FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "service_role_all" ON layer_1_metrics FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "service_role_all" ON layer_2_copilot FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "service_role_all" ON layer_3_gates FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "service_role_all" ON learning_velocity FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "service_role_all" ON three_layer_harmony FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "service_role_all" ON escalations FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "service_role_all" ON weekly_snapshots FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "service_role_all" ON gate_postflight_log FOR ALL USING (auth.role() = 'service_role');

-- ============================================================================
-- PART 3: SEED DATA — Initial state
-- ============================================================================

-- Initialize operational state
INSERT INTO operational_state (pipeline_status, runway_days, critical_count, session_id)
VALUES ('GREEN', 365, 0, gen_random_uuid())
ON CONFLICT (id) DO NOTHING;

-- Initialize SER tracking (SER 1-4)
INSERT INTO ser_status (ser_num, name, description, current_state, participants, escalation_rule_days)
VALUES
  (1, 'Research Execution', 'Gate learning trajectory + SMAG measurement', 'open', '[]', 21),
  (2, 'Collaborator Coordination', 'Criterion 4 + Criterion 7 tracking', 'open', '[]', 14),
  (3, 'Deployment Partnerships', 'Trial protocol + model-diverse partners', 'open', '[]', 14),
  (4, 'Copilot Intelligence Coordination', 'Layer 2 signals + bias audit + feedback to empirica', 'open', '[]', 10)
ON CONFLICT (ser_num) DO NOTHING;

-- Initialize integrations registry
INSERT INTO integrations_registry (service_name, status)
VALUES
  ('empirica_cli', 'connected'),
  ('github_actions', 'pending'),
  ('copilot_api', 'pending'),
  ('acat_api', 'pending')
ON CONFLICT (service_name) DO NOTHING;

-- ============================================================================
-- INDEXES — Query optimization
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_zone3_queue_severity ON zone3_queue(severity);
CREATE INDEX IF NOT EXISTS idx_zone3_queue_resolved ON zone3_queue(resolved_at);
CREATE INDEX IF NOT EXISTS idx_verification_log_queue ON verification_log(queue_item_id);
CREATE INDEX IF NOT EXISTS idx_verification_log_triggered ON verification_log(triggered_at DESC);
CREATE INDEX IF NOT EXISTS idx_ser_status_deadline ON ser_status(escalation_deadline);
CREATE INDEX IF NOT EXISTS idx_escalations_deadline ON escalations(escalation_deadline);
CREATE INDEX IF NOT EXISTS idx_escalations_status ON escalations(status);
CREATE INDEX IF NOT EXISTS idx_layer_1_date ON layer_1_metrics(measurement_date DESC);
CREATE INDEX IF NOT EXISTS idx_layer_2_date ON layer_2_copilot(measurement_date DESC);
CREATE INDEX IF NOT EXISTS idx_gate_postflight_gate ON gate_postflight_log(gate_num);
CREATE INDEX IF NOT EXISTS idx_learning_velocity_week ON learning_velocity(week_starting DESC);
CREATE INDEX IF NOT EXISTS idx_weekly_snapshots_date ON weekly_snapshots(snapshot_date DESC);

-- ============================================================================
-- DONE
-- ============================================================================
--
-- Schema Status: READY FOR APPLICATION
-- Supabase Project: ksinisdzgtnqzsymhfya
--
-- Application procedure:
-- 1. Open Supabase SQL Editor for project ksinisdzgtnqzsymhfya
-- 2. Paste this entire file
-- 3. Execute
-- 4. Verify: all 16 tables created, RLS enabled, seed data inserted
-- 5. Proceed to Cloudflare Functions wiring (next stage)
--
