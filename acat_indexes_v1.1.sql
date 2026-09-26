-- ============================================================================
-- ACAT Schema v1.1 - Index Improvements
-- Purpose: Optimize query performance for dimensional analysis
-- Added: 2026-08-22
-- ============================================================================

-- CORE DIMENSION INDEXES (filling gaps in v1.0)

-- Accuracy dimension: support time-series + system analysis
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_accuracy_date_audit
  ON acat_dimension_accuracy(measurement_date DESC, audit_id);

-- Completeness dimension: support coverage queries by system + date
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_completeness_date_system
  ON acat_dimension_completeness(measurement_date DESC, system);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_completeness_audit_date
  ON acat_dimension_completeness(audit_id, measurement_date DESC);

-- Precision dimension: support accuracy queries by category + date
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_precision_date_system
  ON acat_dimension_precision(measurement_date DESC, system);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_precision_category
  ON acat_dimension_precision(category, system);

-- Coherence dimension: support finding analysis by date + system
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_coherence_date_system
  ON acat_dimension_coherence(measurement_date DESC, system);

-- Coverage dimension: support gap analysis by category
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_coverage_date_system
  ON acat_dimension_coverage(measurement_date DESC, system);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_coverage_category_system
  ON acat_dimension_coverage(category, system);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_coverage_gap
  ON acat_dimension_coverage(is_coverage_gap, gap_severity);

-- Convergence dimension: support time-series analysis
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_convergence_systems_date
  ON acat_dimension_convergence(system_a, system_b, measurement_date DESC);

-- ============================================================================
-- EXTENDED DIMENSION INDEXES (v1.0 had only research_study_id)
-- ============================================================================

-- Time-to-detection: support category + system analysis
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_time_detection_audit_system
  ON acat_dimension_time_to_detection(audit_id, system);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_time_detection_category_system
  ON acat_dimension_time_to_detection(category, system);

-- Severity alignment: support finding + system pair analysis
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_severity_finding_systems
  ON acat_dimension_severity_alignment(finding_id, system_a, system_b);

-- Category alignment: support category comparison + date
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_category_alignment_date
  ON acat_dimension_category_alignment(measurement_date DESC, category);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_category_alignment_systems
  ON acat_dimension_category_alignment(system_a, system_b, category);

-- Cross-system coupling: support source → target mapping
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_coupling_source
  ON acat_dimension_cross_system_coupling(source_system, source_category);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_coupling_target
  ON acat_dimension_cross_system_coupling(target_system, target_category);

-- Resource efficiency: support cost analysis by category
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_efficiency_category_system
  ON acat_dimension_resource_efficiency(category, system);

-- Learning velocity: support improvement tracking by system + repo
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_velocity_system_repo_date
  ON acat_dimension_learning_velocity(system, repo_name, measurement_date DESC);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_velocity_direction
  ON acat_dimension_learning_velocity(direction, measurement_date DESC);

-- ============================================================================
-- CORE TABLE INDEXES (filling audit-level gaps)
-- ============================================================================

-- Audit findings: support batch lookups by audit + created_at
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_findings_audit_created
  ON empirica_audit_findings(audit_id, created_at DESC);

-- Remediations: support verification workflow
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_remediations_verified_at
  ON empirica_remediations(verified_at DESC) WHERE verified_at IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_remediations_assigned_date
  ON empirica_remediations(assigned_date DESC) WHERE assigned_date IS NOT NULL;

-- Convergence measurements: support metric time-series
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_convergence_date_study
  ON empirica_convergence_measurements(measurement_date DESC, research_study_id);

-- ============================================================================
-- MATERIALIZED VIEW SUPPORT (for dashboard queries)
-- ============================================================================

-- Dimensional health view support: indexes on GROUP BY columns
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_accuracy_f1_score
  ON acat_dimension_accuracy(f1_score);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_completeness_pct
  ON acat_dimension_completeness(overall_completeness_pct);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_precision_pct
  ON acat_dimension_precision(precision_pct);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_coherence_score
  ON acat_dimension_coherence(coherence_score);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_coverage_pct
  ON acat_dimension_coverage(coverage_pct);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_convergence_gap
  ON acat_dimension_convergence(closure_rate_gap);

-- ============================================================================
-- SUMMARY
-- ============================================================================
-- Added 33 indexes to support:
-- 1. Time-series queries (measurement_date + system/category)
-- 2. Dimensional comparisons (audit_id + system pairs)
-- 3. Category-based analysis (category + system)
-- 4. Dashboard aggregations (GROUP BY columns)
-- 5. Workflow tracking (verified_at, assigned_date)
--
-- Index count before: 41 (many tables with only research_study_id index)
-- Index count after: 74 (comprehensive coverage of query patterns)
-- ============================================================================
