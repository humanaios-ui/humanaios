-- ============================================================================
-- Schema.sql Extension: Registry Submission Persistence
-- Bridges API Bridge ↔ Database Layer
-- Purpose: Store registry gate submissions, outcomes, scores, and pipeline state
-- ============================================================================

-- ============================================================================
-- CORE REGISTRY TABLES
-- ============================================================================

-- Registry submissions (intake from API bridge)
CREATE TABLE registry_submissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,

    -- Submission metadata
    record JSONB NOT NULL,  -- Full submission: {title, company, location, salary, desc, source_id, attest_hash, source_license, ...}
    source_id VARCHAR(255),  -- Reference to attested_sources registry
    attest_hash VARCHAR(255),  -- Cryptographic attestation
    source_license VARCHAR(100),

    -- Gate outcome
    outcome VARCHAR(50) NOT NULL,  -- ACCEPT | QUARANTINE | CANDIDATE
    outcome_reason TEXT,  -- Detailed reason for outcome

    -- Scoring (for ACCEPT outcomes)
    score JSONB,  -- {score: INT, adversarial_signatures_at_input: [], ...}

    -- Pipeline state
    pipeline_status VARCHAR(50) NOT NULL DEFAULT 'proposed',  -- proposed | ratified | landed | rejected

    -- Timestamps
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    decided_at TIMESTAMP WITH TIME ZONE,
    landed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CONSTRAINT valid_outcome CHECK (outcome IN ('ACCEPT', 'QUARANTINE', 'CANDIDATE')),
    CONSTRAINT valid_pipeline_status CHECK (pipeline_status IN ('proposed', 'ratified', 'landed', 'rejected'))
);

CREATE INDEX idx_registry_org ON registry_submissions(org_id);
CREATE INDEX idx_registry_outcome ON registry_submissions(outcome);
CREATE INDEX idx_registry_status ON registry_submissions(pipeline_status);
CREATE INDEX idx_registry_source_id ON registry_submissions(source_id);
CREATE INDEX idx_registry_submitted_at ON registry_submissions(submitted_at DESC);

-- Registry feedback (issues, security rejections)
CREATE TABLE registry_feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    submission_id UUID REFERENCES registry_submissions(id) ON DELETE SET NULL,

    -- Feedback type
    source VARCHAR(50) NOT NULL,  -- user | machine
    type VARCHAR(100) NOT NULL,  -- security_reject | validation_error | user_report | etc.
    severity VARCHAR(50) DEFAULT 'medium',  -- low | medium | high | critical
    message TEXT NOT NULL,

    -- Resolution tracking
    status VARCHAR(50) DEFAULT 'open',  -- open | acknowledged | resolved
    resolved_at TIMESTAMP WITH TIME ZONE,

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CONSTRAINT valid_source CHECK (source IN ('user', 'machine')),
    CONSTRAINT valid_severity CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    CONSTRAINT valid_status CHECK (status IN ('open', 'acknowledged', 'resolved'))
);

CREATE INDEX idx_feedback_org ON registry_feedback(org_id);
CREATE INDEX idx_feedback_submission ON registry_feedback(submission_id);
CREATE INDEX idx_feedback_type ON registry_feedback(type);
CREATE INDEX idx_feedback_severity ON registry_feedback(severity);
CREATE INDEX idx_feedback_status ON registry_feedback(status);

-- Harness configuration (resource allocation modes)
CREATE TABLE harness_modes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,

    -- Mode configuration
    mode VARCHAR(50) NOT NULL,  -- balanced | ai-led | human-led | capital-injection | custom
    human_allocation DECIMAL(3,2) NOT NULL,  -- 0.0 - 1.0
    machine_allocation DECIMAL(3,2) NOT NULL,  -- 0.0 - 1.0
    capital_allocation DECIMAL(3,2) NOT NULL,  -- 0.0 - 1.0

    -- Validation
    created_by UUID REFERENCES users(id),
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CONSTRAINT valid_mode CHECK (mode IN ('balanced', 'ai-led', 'human-led', 'capital-injection', 'custom')),
    CONSTRAINT allocations_sum CHECK (human_allocation + machine_allocation + capital_allocation = 1.0)
);

CREATE INDEX idx_harness_org ON harness_modes(org_id);
CREATE INDEX idx_harness_active ON harness_modes(active);

-- Intent tracking (stated vs revealed)
CREATE TABLE intent_reconciliation (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,

    -- Intent lifecycle
    stated_intent TEXT,  -- What the system claims to be doing
    revealed_intent TEXT,  -- What it actually does (from actions)
    gap_analysis TEXT,  -- Identified discrepancies

    -- Measurement
    measurement_date TIMESTAMP WITH TIME ZONE NOT NULL,
    gap_score DECIMAL(3,2),  -- 0.0 = perfect alignment, 1.0 = complete divergence

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CONSTRAINT gap_score_range CHECK (gap_score >= 0.0 AND gap_score <= 1.0)
);

CREATE INDEX idx_intent_org ON intent_reconciliation(org_id);
CREATE INDEX idx_intent_date ON intent_reconciliation(measurement_date DESC);

-- ============================================================================
-- PIPELINE STATE VIEW (for sync/state endpoint)
-- ============================================================================

CREATE VIEW registry_pipeline_state AS
SELECT
    org_id,
    COUNT(*) FILTER (WHERE pipeline_status = 'proposed') as pipeline_propose_count,
    COUNT(*) FILTER (WHERE pipeline_status = 'ratified') as pipeline_ratify_count,
    COUNT(*) FILTER (WHERE pipeline_status = 'landed') as pipeline_land_count,
    COUNT(*) FILTER (WHERE outcome = 'QUARANTINE') as feedback_count,
    COUNT(*) as total_submissions,
    MAX(submitted_at) as last_submission
FROM registry_submissions
GROUP BY org_id;

-- ============================================================================
-- TRIGGERS & MAINTENANCE
-- ============================================================================

-- Update updated_at on registry submissions
CREATE TRIGGER update_registry_submissions_updated_at BEFORE UPDATE ON registry_submissions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Update updated_at on registry feedback
CREATE TRIGGER update_registry_feedback_updated_at BEFORE UPDATE ON registry_feedback
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Update updated_at on intent reconciliation
CREATE TRIGGER update_intent_reconciliation_updated_at BEFORE UPDATE ON intent_reconciliation
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- ROW-LEVEL SECURITY
-- ============================================================================

-- Enable RLS on registry tables
ALTER TABLE registry_submissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE registry_feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE harness_modes ENABLE ROW LEVEL SECURITY;
ALTER TABLE intent_reconciliation ENABLE ROW LEVEL SECURITY;

-- Org isolation policies
CREATE POLICY org_isolation_registry_submissions ON registry_submissions
    FOR ALL
    USING (org_id IN (
        SELECT org_id FROM users WHERE id = current_setting('app.current_user_id')::uuid
    ));

CREATE POLICY org_isolation_registry_feedback ON registry_feedback
    FOR ALL
    USING (org_id IN (
        SELECT org_id FROM users WHERE id = current_setting('app.current_user_id')::uuid
    ));

CREATE POLICY org_isolation_harness_modes ON harness_modes
    FOR ALL
    USING (org_id IN (
        SELECT org_id FROM users WHERE id = current_setting('app.current_user_id')::uuid
    ));

CREATE POLICY org_isolation_intent_reconciliation ON intent_reconciliation
    FOR ALL
    USING (org_id IN (
        SELECT org_id FROM users WHERE id = current_setting('app.current_user_id')::uuid
    ));

-- ============================================================================
-- COMMENTS & DOCUMENTATION
-- ============================================================================

COMMENT ON TABLE registry_submissions IS 'API bridge registry gate submissions with outcomes, scores, and pipeline state';
COMMENT ON TABLE registry_feedback IS 'Issues, errors, and rejections from gate processing';
COMMENT ON TABLE harness_modes IS 'Resource allocation configurations (human/machine/capital ratios)';
COMMENT ON TABLE intent_reconciliation IS 'Tracking alignment between stated and revealed intent';
COMMENT ON COLUMN registry_submissions.record IS 'Full submission payload: {title, company, location, salary, desc, source_id, attest_hash, source_license}';
COMMENT ON COLUMN registry_submissions.score IS 'Gate scoring output: {score: INT, adversarial_signatures_at_input: []}';
COMMENT ON COLUMN harness_modes.human_allocation IS 'Weight of human decision-making (0.0-1.0)';
COMMENT ON COLUMN harness_modes.machine_allocation IS 'Weight of automated AI decisions (0.0-1.0)';
COMMENT ON COLUMN harness_modes.capital_allocation IS 'Weight of capital/resource injection (0.0-1.0)';

-- ============================================================================
-- INTEGRATION NOTES
-- ============================================================================
-- This extension integrates the API bridge with persistent storage:
-- 1. registry_submissions stores all incoming records + outcomes
-- 2. registry_feedback captures quarantines/rejections
-- 3. harness_modes stores resource allocation configurations
-- 4. intent_reconciliation tracks stated vs revealed intent gaps
--
-- API bridge modifications needed:
-- - Add SQLAlchemy ORM models for these tables
-- - Modify APIBridge.process_registry_submission() to write to DB
-- - Modify APIBridge.get_feedback_report() to write to DB
-- - Modify APIBridge.sync_state() to query DB + return registry_pipeline_state
-- - Modify APIBridge.set_harness_mode() to write to DB + update active mode
-- ============================================================================
