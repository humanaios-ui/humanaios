-- Blocker Spec Field Integration — Step 3 (F-34)
-- Added: 2026-09-11
-- Purpose: Implement score_source field for blocker routing and scoring/classification
-- Scope: blocker_routing table enhancement for outreach workflow coordination

-- ============================================
-- MIGRATION: Add score_source field to blocker_routing
-- ============================================
-- This field tracks the source of a blocker's score/confidence
-- Enables outreach team to validate blocker classification and routing

ALTER TABLE blocker_routing ADD COLUMN IF NOT EXISTS score_source VARCHAR(50);
-- score_source: 'empirica' (auto-detected), 'cortex' (from mesh), 'heuristic' (pattern-based), 'manual' (human-classified)

ALTER TABLE blocker_routing ADD COLUMN IF NOT EXISTS confidence_score DECIMAL(3, 2);
-- confidence_score: 0.0-1.0, credibility of the blocker's classification and priority

ALTER TABLE blocker_routing ADD COLUMN IF NOT EXISTS scored_at TIMESTAMP WITH TIME ZONE;
-- scored_at: when the blocker was last scored/classified

-- Add index for score_source filtering (outreach workflow optimization)
CREATE INDEX IF NOT EXISTS idx_blocker_routing_score_source ON blocker_routing(score_source);
CREATE INDEX IF NOT EXISTS idx_blocker_routing_confidence ON blocker_routing(confidence_score DESC);

-- ============================================
-- OUTREACH BLOCKER WORKFLOW
-- ============================================
-- Supports outreach team's 8-blocker coordination:
-- 1. empirica (auto-detected): default score_source
-- 2-8. Escalation tracking with confidence scoring

-- View: Blockers ready for outreach action
-- (scored, prioritized, with routing clarity)
CREATE OR REPLACE VIEW v_blocker_outreach_queue AS
SELECT
    blocker_id,
    blocker_title,
    priority,
    score_source,
    confidence_score,
    status,
    affected_practices,
    assigned_to,
    practices_labor_hours,
    scored_at,
    CASE
        WHEN score_source = 'empirica' AND confidence_score >= 0.75 THEN 'ready_for_routing'
        WHEN score_source = 'cortex' AND confidence_score >= 0.80 THEN 'ready_for_routing'
        WHEN score_source IN ('heuristic', 'manual') THEN 'needs_validation'
        ELSE 'pending_scoring'
    END AS outreach_status
FROM blocker_routing
WHERE status IN ('open', 'acknowledged')
ORDER BY priority DESC, confidence_score DESC, created_at ASC;

-- ============================================
-- RESOURCE-BASED COORDINATION TRACKING
-- ============================================
-- Outreach coordination: 3h + Mesh-support 2h + Admiral 0.5h
-- (EU AI Act decision pending for reclassification)

CREATE OR REPLACE VIEW v_blocker_resource_allocation AS
SELECT
    COUNT(*) as total_blockers,
    COUNT(CASE WHEN status = 'open' THEN 1 END) as open_blockers,
    COUNT(CASE WHEN score_source = 'empirica' THEN 1 END) as auto_scored,
    COUNT(CASE WHEN confidence_score >= 0.8 THEN 1 END) as high_confidence,
    SUM(practices_labor_hours) as total_labor_hours,
    AVG(confidence_score) as avg_confidence
FROM blocker_routing;

-- ============================================
-- DEPLOYMENT NOTES
-- ============================================
-- Step 3: Blocker Spec Field Integration (F-34)
--
-- This migration adds three fields to blocker_routing:
-- 1. score_source: Origin of blocker's score ('empirica', 'cortex', 'heuristic', 'manual')
-- 2. confidence_score: Classification credibility (0.0-1.0)
-- 3. scored_at: Timestamp of last scoring
--
-- Supports outreach workflow:
-- - Prioritizes blockers by confidence score
-- - Tracks scoring source for auditing
-- - Enables resource-based coordination (3h outreach + 2h mesh + 0.5h Admiral escalation)
--
-- Views:
-- - v_blocker_outreach_queue: Blockers ready for outreach action/validation
-- - v_blocker_resource_allocation: Resource impact summary for coordination
--
-- Status: Ready for deployment to analytics practice database
-- Delivery: Sep 16 (F-34)
-- Team: Outreach (primary), Mesh-support (escalation), Admiral (EU AI Act decision)
