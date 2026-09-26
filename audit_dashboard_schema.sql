-- Audit Dashboard Schema v1.0
--
-- Live SQL layer for human operators.
-- Provides real-time view of: findings + files + goals + decisions + practices.
-- Enables orchestration of audit findings into Week 1-4 execution plan.
--
-- This schema lives in .empirica/sessions/sessions.db (Empirica database)
-- and syncs findings from empirica artifacts + YAML registry.

-- Main findings view (read from empirica log-artifacts)
CREATE VIEW v_audit_findings AS
SELECT
    artifacts.id AS finding_uuid,
    artifacts.data ->> 'method' AS audit_method,
    artifacts.data ->> 'severity' AS severity,
    artifacts.data ->> 'category' AS category,
    artifacts.data ->> 'file_path' AS file_path,
    (artifacts.data ->> 'line')::INTEGER AS line_number,
    artifacts.data ->> 'finding' AS message,
    artifacts.data ->> 'impact' AS impact,
    artifacts.created_at AS discovered_at,
    projects.name AS project_name
FROM artifacts
JOIN projects ON artifacts.project_id = projects.id
WHERE artifacts.type = 'finding'
    AND artifacts.data ->> 'category' IN ('claim_lint', 'duplicate_file', 'link_broken', 'anchor_missing', etc.)
ORDER BY severity DESC, audit_method ASC;

-- File inventory with audit coverage
CREATE VIEW v_audit_file_coverage AS
SELECT
    file_path,
    COUNT(DISTINCT audit_method) AS methods_applied,
    COUNT(*) AS finding_count,
    MAX(severity) AS max_severity,
    CASE
        WHEN COUNT(DISTINCT audit_method) >= 8 THEN 'FULL'
        WHEN COUNT(DISTINCT audit_method) >= 4 THEN 'PARTIAL'
        ELSE 'MINIMAL'
    END AS coverage_status,
    STRING_AGG(DISTINCT audit_method, ', ' ORDER BY audit_method) AS methods_list
FROM v_audit_findings
GROUP BY file_path
ORDER BY finding_count DESC;

-- Severity summary with action mapping
CREATE VIEW v_audit_severity_summary AS
SELECT
    severity,
    COUNT(*) AS finding_count,
    CASE
        WHEN severity = 'P0' THEN 'ESCALATE_IMMEDIATELY'
        WHEN severity = 'P1' THEN 'IMPLEMENT_FIX (Week 1)'
        WHEN severity = 'P2' THEN 'SCHEDULE_FIX (Week 2-3)'
        WHEN severity = 'P3' THEN 'QUEUE_IMPROVEMENT'
    END AS action_category,
    STRING_AGG(DISTINCT category, ', ') AS categories
FROM v_audit_findings
GROUP BY severity
ORDER BY severity ASC;

-- Method effectiveness (how many findings per method)
CREATE VIEW v_audit_method_impact AS
SELECT
    audit_method,
    COUNT(*) AS finding_count,
    COUNT(DISTINCT file_path) AS affected_files,
    STRING_AGG(DISTINCT category, ', ') AS categories,
    STRING_AGG(DISTINCT severity, ', ') AS severities,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM v_audit_findings), 2) AS percent_of_total
FROM v_audit_findings
GROUP BY audit_method
ORDER BY finding_count DESC;

-- Ground truth linkage (findings ← method ← published sources)
CREATE VIEW v_audit_ground_truth_linkage AS
SELECT
    af.audit_method,
    af.finding_count,
    gt.external_source_url,
    gt.standard_body,
    gt.validation_mechanism,
    gt.severity_mapping
FROM (SELECT DISTINCT audit_method, COUNT(*) as finding_count
      FROM v_audit_findings
      GROUP BY audit_method) af
CROSS JOIN ground_truth_mapping gt
WHERE af.audit_method = gt.method_id
ORDER BY af.audit_method;

-- Practice-scoped findings (holographic view)
CREATE VIEW v_audit_findings_by_practice AS
SELECT
    p.ai_id AS practice_id,
    p.name AS practice_name,
    COUNT(f.finding_uuid) AS finding_count,
    STRING_AGG(DISTINCT f.severity, ', ') AS severities,
    STRING_AGG(DISTINCT f.category, ', ') AS categories,
    CASE
        WHEN p.ai_id = 'empirica-foundation.carly.empirica-foundation-evaluator' THEN 'MASTER'
        WHEN REGEXP_MATCH(f.file_path, p.repository_path) IS NOT NULL THEN 'LOCAL'
        ELSE 'RELATED'
    END AS view_scope,
    CASE
        WHEN p.ai_id = 'empirica-foundation.carly.empirica-foundation-evaluator' THEN 'Orchestration, correlation, escalation'
        ELSE 'Local remediation'
    END AS responsibility
FROM practices p
LEFT JOIN v_audit_findings f ON TRUE
GROUP BY p.ai_id, p.name, p.repository_path
ORDER BY finding_count DESC;

-- Findings ← Goals (from Week 1-4 execution plan)
CREATE VIEW v_audit_findings_to_goals AS
SELECT
    af.finding_uuid,
    af.audit_method,
    af.severity,
    af.message,
    g.id AS goal_id,
    g.objective AS goal_title,
    g.status AS goal_status,
    d.description AS decision_description
FROM v_audit_findings af
LEFT JOIN goals g ON (
    af.severity IN ('P0', 'P1')
    AND g.description ILIKE CONCAT('%', af.category, '%')
    AND g.status = 'in_progress'
)
LEFT JOIN decisions d ON (
    d.related_to_goal = g.id
    AND d.artifact_type = 'decision'
)
ORDER BY af.severity DESC, af.audit_method ASC;

-- Measurement tracking (for convergence gates)
CREATE VIEW v_audit_measurement_progress AS
SELECT
    COUNT(*) AS current_finding_total,
    (SELECT COUNT(*) FROM empirica_history WHERE event = 'audit_run' AND date >= DATE_SUB(NOW(), INTERVAL 7 DAY)) AS audits_this_week,
    ROUND(100.0 * (SELECT COUNT(*) FROM empirica_history
                   WHERE event = 'finding_fixed' AND date >= DATE_SUB(NOW(), INTERVAL 7 DAY)) /
          COUNT(*), 2) AS fix_rate_weekly_percent,
    CASE
        WHEN (SELECT COUNT(*) FROM v_audit_findings WHERE severity IN ('P0', 'P1')) > 0 THEN 'RED'
        WHEN (SELECT COUNT(*) FROM v_audit_findings WHERE severity = 'P2') > 3 THEN 'YELLOW'
        ELSE 'GREEN'
    END AS health_status
FROM v_audit_findings;

-- Operational dashboard (top-level for Z2)
CREATE VIEW v_audit_operations_dashboard AS
SELECT
    (SELECT COUNT(*) FROM v_audit_findings) AS total_findings,
    (SELECT COUNT(*) FROM v_audit_findings WHERE severity = 'P0') AS p0_critical,
    (SELECT COUNT(*) FROM v_audit_findings WHERE severity = 'P1') AS p1_high,
    (SELECT COUNT(*) FROM v_audit_findings WHERE severity = 'P2') AS p2_medium,
    (SELECT COUNT(*) FROM v_audit_findings WHERE severity = 'P3') AS p3_low,
    (SELECT COUNT(DISTINCT file_path) FROM v_audit_findings) AS files_audited,
    (SELECT COUNT(DISTINCT audit_method) FROM v_audit_findings) AS methods_applied,
    (SELECT MAX(discovered_at) FROM v_audit_findings) AS last_audit_run,
    (SELECT health_status FROM v_audit_measurement_progress LIMIT 1) AS overall_health
