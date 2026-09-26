-- ============================================================================
-- ACAT Schema v1.0
-- Mutual Validation Framework - Empirica + Human-AI Systems
-- ============================================================================

-- Core audit tracking
CREATE TABLE empirica_audits (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  audit_name VARCHAR NOT NULL,
  repo_name VARCHAR NOT NULL,
  audit_date TIMESTAMP NOT NULL DEFAULT NOW(),
  method_version VARCHAR,
  audit_methods_used TEXT[],
  total_findings INT,
  research_study_id VARCHAR NOT NULL,
  auditor_system VARCHAR NOT NULL,
  auditor_ai_id VARCHAR NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(audit_name, repo_name, audit_date)
);

CREATE INDEX idx_empirica_audits_repo ON empirica_audits(repo_name);
CREATE INDEX idx_empirica_audits_date ON empirica_audits(audit_date);
CREATE INDEX idx_empirica_audits_study ON empirica_audits(research_study_id);

-- Individual findings from audits
CREATE TABLE empirica_audit_findings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  audit_id UUID NOT NULL REFERENCES empirica_audits(id),
  finding_id VARCHAR UNIQUE NOT NULL,
  repo_name VARCHAR NOT NULL,
  method VARCHAR NOT NULL,
  severity VARCHAR NOT NULL,
  category VARCHAR NOT NULL,
  file_path VARCHAR NOT NULL,
  line_number INT,
  message TEXT,
  details JSONB,
  research_study_id VARCHAR NOT NULL,
  auditor_system VARCHAR NOT NULL,
  auditor_ai_id VARCHAR NOT NULL,
  discovered_at TIMESTAMP NOT NULL DEFAULT NOW(),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_findings_audit ON empirica_audit_findings(audit_id);
CREATE INDEX idx_findings_repo ON empirica_audit_findings(repo_name);
CREATE INDEX idx_findings_method ON empirica_audit_findings(method);
CREATE INDEX idx_findings_severity ON empirica_audit_findings(severity);
CREATE INDEX idx_findings_study ON empirica_audit_findings(research_study_id);

-- Remediation tracking (application layer)
CREATE TABLE empirica_remediations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  finding_id UUID NOT NULL REFERENCES empirica_audit_findings(id),
  fix_type VARCHAR NOT NULL,
  fix_status VARCHAR NOT NULL DEFAULT 'pending',
  assigned_to VARCHAR,
  assigned_date TIMESTAMP,
  fix_commit_sha VARCHAR,
  fix_commit_message TEXT,
  fix_applied_at TIMESTAMP,
  time_to_fix_minutes INT,
  verified_commit_sha VARCHAR,
  verification_method VARCHAR,
  verified_at TIMESTAMP,
  verification_result VARCHAR,
  research_study_id VARCHAR NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_remediations_finding ON empirica_remediations(finding_id);
CREATE INDEX idx_remediations_status ON empirica_remediations(fix_status);
CREATE INDEX idx_remediations_study ON empirica_remediations(research_study_id);

-- Convergence measurements (weekly tracking)
CREATE TABLE empirica_convergence_measurements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  audit_id UUID NOT NULL REFERENCES empirica_audits(id),
  measurement_date TIMESTAMP NOT NULL,
  measurement_type VARCHAR NOT NULL,
  total_findings INT NOT NULL,
  p0_count INT DEFAULT 0,
  p1_count INT DEFAULT 0,
  p2_count INT DEFAULT 0,
  p3_count INT DEFAULT 0,
  findings_fixed INT DEFAULT 0,
  findings_verified INT DEFAULT 0,
  closure_rate DECIMAL(5,2),
  avg_time_to_fix_minutes DECIMAL(10,2),
  time_to_first_fix_minutes INT,
  effectiveness_score DECIMAL(3,2),
  signal_score DECIMAL(3,2),
  consistency_score DECIMAL(3,2),
  resonance_score DECIMAL(3,2),
  adherence_score DECIMAL(3,2),
  latency_score DECIMAL(3,2),
  research_study_id VARCHAR NOT NULL,
  measured_by VARCHAR NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_convergence_audit ON empirica_convergence_measurements(audit_id);
CREATE INDEX idx_convergence_date ON empirica_convergence_measurements(measurement_date);
CREATE INDEX idx_convergence_study ON empirica_convergence_measurements(research_study_id);

-- ============================================================================
-- DIMENSIONAL ACAT TABLES (6 Core + Extended)
-- ============================================================================

-- DIMENSION 1: ACCURACY (Do both systems find the same defects?)
CREATE TABLE acat_dimension_accuracy (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  audit_id UUID NOT NULL REFERENCES empirica_audits(id),
  system_a VARCHAR NOT NULL,  -- empirica, humanai, etc.
  system_b VARCHAR NOT NULL,

  -- Overlap metrics
  findings_in_a INT NOT NULL,
  findings_in_b INT NOT NULL,
  findings_in_both INT NOT NULL,
  findings_only_a INT,
  findings_only_b INT,

  -- Accuracy scores
  precision DECIMAL(5,2),  -- findings_in_both / findings_in_a
  recall DECIMAL(5,2),     -- findings_in_both / findings_in_b
  f1_score DECIMAL(5,2),   -- harmonic mean of precision + recall

  measurement_date TIMESTAMP NOT NULL DEFAULT NOW(),
  research_study_id VARCHAR NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_accuracy_audit ON acat_dimension_accuracy(audit_id);
CREATE INDEX idx_accuracy_systems ON acat_dimension_accuracy(system_a, system_b);
CREATE INDEX idx_accuracy_study ON acat_dimension_accuracy(research_study_id);

-- DIMENSION 2: COMPLETENESS (Do both systems catch all defects?)
CREATE TABLE acat_dimension_completeness (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  audit_id UUID NOT NULL REFERENCES empirica_audits(id),
  system VARCHAR NOT NULL,

  -- Coverage metrics
  repo_name VARCHAR NOT NULL,
  total_files INT NOT NULL,
  files_audited INT NOT NULL,
  methods_available INT NOT NULL,
  methods_applied INT NOT NULL,

  -- Completeness scores
  file_coverage_pct DECIMAL(5,2),    -- files_audited / total_files
  method_coverage_pct DECIMAL(5,2),  -- methods_applied / methods_available
  overall_completeness_pct DECIMAL(5,2),

  -- Gaps
  files_skipped INT,
  methods_not_applied INT,

  measurement_date TIMESTAMP NOT NULL DEFAULT NOW(),
  research_study_id VARCHAR NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_completeness_audit ON acat_dimension_completeness(audit_id);
CREATE INDEX idx_completeness_system ON acat_dimension_completeness(system);

-- DIMENSION 3: PRECISION (What's the false-positive rate?)
CREATE TABLE acat_dimension_precision (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  audit_id UUID NOT NULL REFERENCES empirica_audits(id),
  system VARCHAR NOT NULL,
  category VARCHAR NOT NULL,  -- claim_lint, link_broken, etc.

  -- Precision breakdown
  findings_reported INT NOT NULL,
  findings_verified INT NOT NULL,
  findings_rejected INT NOT NULL,

  -- Precision scores
  precision_pct DECIMAL(5,2),  -- verified / reported
  false_positive_rate DECIMAL(5,2),  -- rejected / reported

  -- By severity
  p0_reported INT,
  p0_verified INT,
  p1_reported INT,
  p1_verified INT,
  p2_reported INT,
  p2_verified INT,
  p3_reported INT,
  p3_verified INT,

  measurement_date TIMESTAMP NOT NULL DEFAULT NOW(),
  research_study_id VARCHAR NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_precision_audit ON acat_dimension_precision(audit_id);
CREATE INDEX idx_precision_system ON acat_dimension_precision(system);

-- DIMENSION 4: COHERENCE (Are findings consistent across time?)
CREATE TABLE acat_dimension_coherence (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  finding_id UUID NOT NULL REFERENCES empirica_audit_findings(id),
  system VARCHAR NOT NULL,

  -- Coherence tracking
  first_discovered_audit UUID REFERENCES empirica_audits(id),
  last_discovered_audit UUID REFERENCES empirica_audits(id),
  times_discovered INT NOT NULL DEFAULT 1,

  -- Consistency metrics
  severity_consistent BOOLEAN,  -- Does severity stay the same?
  category_consistent BOOLEAN,  -- Does category stay the same?
  location_consistent BOOLEAN,  -- Does file/line stay the same?

  -- Change tracking
  severity_changes INT DEFAULT 0,
  category_changes INT DEFAULT 0,
  location_changes INT DEFAULT 0,

  -- Coherence score
  coherence_score DECIMAL(3,2),  -- 1.0 = perfectly consistent, 0.0 = always changes

  measurement_date TIMESTAMP NOT NULL DEFAULT NOW(),
  research_study_id VARCHAR NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_coherence_finding ON acat_dimension_coherence(finding_id);
CREATE INDEX idx_coherence_system ON acat_dimension_coherence(system);

-- DIMENSION 5: COVERAGE (Which areas does each system cover?)
CREATE TABLE acat_dimension_coverage (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  audit_id UUID NOT NULL REFERENCES empirica_audits(id),
  system VARCHAR NOT NULL,

  -- Coverage by category
  category VARCHAR NOT NULL,
  findings_in_category INT NOT NULL,
  coverage_pct DECIMAL(5,2),  -- findings in this category / total findings

  -- Strength scoring per category
  category_strength DECIMAL(3,2),  -- how good is this system at this category?

  -- Risk areas (categories with low coverage)
  is_coverage_gap BOOLEAN,
  gap_severity VARCHAR,  -- low, medium, high

  measurement_date TIMESTAMP NOT NULL DEFAULT NOW(),
  research_study_id VARCHAR NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_coverage_audit ON acat_dimension_coverage(audit_id);
CREATE INDEX idx_coverage_system ON acat_dimension_coverage(system);
CREATE INDEX idx_coverage_category ON acat_dimension_coverage(category);

-- DIMENSION 6: CONVERGENCE (Do systems improve together?)
CREATE TABLE acat_dimension_convergence (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  system_a VARCHAR NOT NULL,
  system_b VARCHAR NOT NULL,

  -- Convergence over time
  measurement_date TIMESTAMP NOT NULL,
  system_a_finding_count INT NOT NULL,
  system_b_finding_count INT NOT NULL,

  -- Improvement tracking
  system_a_closure_rate DECIMAL(5,2),  -- % fixed since last measurement
  system_b_closure_rate DECIMAL(5,2),

  -- Alignment metrics
  closure_rate_gap DECIMAL(5,2),  -- |system_a - system_b|
  findings_gap INT,  -- |system_a_count - system_b_count|

  -- Convergence trend
  converging BOOLEAN,  -- gap getting smaller?
  convergence_velocity DECIMAL(5,2),  -- rate of convergence (gap reduction per week)

  -- Time to alignment
  weeks_to_full_alignment INT,  -- projected weeks until gap < 5%

  research_study_id VARCHAR NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_convergence_systems ON acat_dimension_convergence(system_a, system_b);
CREATE INDEX idx_convergence_date ON acat_dimension_convergence(measurement_date);

-- ============================================================================
-- EXTENDED DIMENSIONS
-- ============================================================================

-- EXTENDED: TIME-TO-DETECTION (How fast does each system find defects?)
CREATE TABLE acat_dimension_time_to_detection (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  audit_id UUID NOT NULL REFERENCES empirica_audits(id),
  system VARCHAR NOT NULL,
  category VARCHAR NOT NULL,

  -- Detection timing
  median_time_to_detection_minutes INT,
  p95_time_to_detection_minutes INT,
  slowest_detection_minutes INT,
  fastest_detection_minutes INT,

  -- Detection velocity (findings per minute of audit time)
  audit_time_minutes INT,
  findings_per_audit_minute DECIMAL(10,2),

  measurement_date TIMESTAMP NOT NULL DEFAULT NOW(),
  research_study_id VARCHAR NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- EXTENDED: SEVERITY ALIGNMENT (Do they agree on severity?)
CREATE TABLE acat_dimension_severity_alignment (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  finding_id UUID NOT NULL REFERENCES empirica_audit_findings(id),
  system_a VARCHAR NOT NULL,
  system_b VARCHAR NOT NULL,

  -- Severity assessment
  system_a_severity VARCHAR,
  system_b_severity VARCHAR,
  severity_match BOOLEAN,

  -- Mismatch analysis
  severity_gap INT,  -- |priority_score_a - priority_score_b|
  causes_different_action BOOLEAN,  -- Does mismatch change handling?

  measurement_date TIMESTAMP NOT NULL DEFAULT NOW(),
  research_study_id VARCHAR NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- EXTENDED: CATEGORY ALIGNMENT (Do they find the same types?)
CREATE TABLE acat_dimension_category_alignment (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  audit_id UUID NOT NULL REFERENCES empirica_audits(id),
  system_a VARCHAR NOT NULL,
  system_b VARCHAR NOT NULL,

  -- Category breakdown
  category VARCHAR NOT NULL,
  system_a_count INT NOT NULL,
  system_b_count INT NOT NULL,
  both_found INT NOT NULL,

  -- Category alignment scores
  category_precision DECIMAL(5,2),  -- both_found / system_a_count
  category_recall DECIMAL(5,2),     -- both_found / system_b_count

  -- Category strength differential
  system_a_stronger BOOLEAN,  -- System A finds more in this category
  category_gap INT,  -- |system_a_count - system_b_count|

  measurement_date TIMESTAMP NOT NULL DEFAULT NOW(),
  research_study_id VARCHAR NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- EXTENDED: CROSS-SYSTEM COUPLING (Do findings in one predict failures in other?)
CREATE TABLE acat_dimension_cross_system_coupling (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  audit_id UUID NOT NULL REFERENCES empirica_audits(id),

  -- Coupling mapping
  source_system VARCHAR NOT NULL,  -- empirica
  source_category VARCHAR NOT NULL,  -- M2, M4, etc.
  target_system VARCHAR NOT NULL,  -- humanai
  target_category VARCHAR NOT NULL,

  -- Coupling strength
  source_findings INT NOT NULL,
  target_findings_predicted INT,
  target_findings_actual INT,
  coupling_accuracy DECIMAL(5,2),  -- % of predicted findings that occur

  -- Harmonic resonance
  resonance_strength DECIMAL(3,2),  -- 0-1: how tightly coupled?
  resonance_lag_hours INT,  -- how many hours between source and target manifestation?

  measurement_date TIMESTAMP NOT NULL DEFAULT NOW(),
  research_study_id VARCHAR NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- EXTENDED: RESOURCE EFFICIENCY (Effort-per-finding)
CREATE TABLE acat_dimension_resource_efficiency (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  audit_id UUID NOT NULL REFERENCES empirica_audits(id),
  system VARCHAR NOT NULL,

  -- Resource metrics
  total_audit_time_hours DECIMAL(10,2),
  total_findings INT NOT NULL,
  findings_per_hour DECIMAL(10,2),

  -- Cost-benefit by category
  category VARCHAR NOT NULL,
  category_audit_time_minutes INT,
  category_findings INT,
  category_efficiency DECIMAL(10,2),  -- findings per minute for this category

  -- Cost to fix
  avg_fix_time_minutes DECIMAL(10,2),
  total_fix_time_hours DECIMAL(10,2),
  total_remediations INT,

  -- Overall efficiency score
  efficiency_score DECIMAL(3,2),  -- 0-1: findings + fixes per resource hour

  measurement_date TIMESTAMP NOT NULL DEFAULT NOW(),
  research_study_id VARCHAR NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- EXTENDED: LEARNING VELOCITY (Improvement rate over time)
CREATE TABLE acat_dimension_learning_velocity (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  system VARCHAR NOT NULL,
  repo_name VARCHAR NOT NULL,

  -- Learning trajectory
  measurement_date TIMESTAMP NOT NULL,
  audit_sequence INT NOT NULL,  -- 1st audit, 2nd audit, 3rd audit, etc.

  -- Metrics improving?
  closure_rate DECIMAL(5,2),
  closure_rate_change DECIMAL(5,2),  -- vs. previous audit

  findings_count INT,
  findings_reduction DECIMAL(5,2),  -- % reduction vs. previous

  avg_fix_time_minutes DECIMAL(10,2),
  fix_time_improvement DECIMAL(5,2),  -- % improvement

  -- Learning velocity score
  velocity_score DECIMAL(3,2),  -- 0-1: how fast is system improving?
  direction BOOLEAN,  -- true = improving, false = degrading

  research_study_id VARCHAR NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- DIMENSIONAL DATA COLLECTION SUMMARY
-- ============================================================================

CREATE TABLE acat_collection_manifest (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  collection_date TIMESTAMP NOT NULL DEFAULT NOW(),
  research_study_id VARCHAR NOT NULL,

  -- What was collected
  audits_tracked INT,
  findings_tracked INT,
  dimensions_populated INT,

  -- Dimension status
  accuracy_collected BOOLEAN,
  completeness_collected BOOLEAN,
  precision_collected BOOLEAN,
  coherence_collected BOOLEAN,
  coverage_collected BOOLEAN,
  convergence_collected BOOLEAN,

  -- Extended dimensions
  time_to_detection_collected BOOLEAN,
  severity_alignment_collected BOOLEAN,
  category_alignment_collected BOOLEAN,
  cross_system_coupling_collected BOOLEAN,
  resource_efficiency_collected BOOLEAN,
  learning_velocity_collected BOOLEAN,

  -- Collection health
  collection_status VARCHAR,  -- in_progress, complete, partial, failed
  next_collection_date TIMESTAMP,

  created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- QUERIES FOR DIMENSIONAL ANALYSIS
-- ============================================================================

-- View: Dimensional Health Dashboard
CREATE VIEW acat_dimensional_health AS
SELECT
  'Accuracy' as dimension,
  COUNT(*) as measurements,
  ROUND(AVG(f1_score), 3) as avg_score,
  ROUND(MIN(f1_score), 3) as min_score,
  MAX(measurement_date) as last_measured
FROM acat_dimension_accuracy
GROUP BY 'Accuracy'

UNION ALL

SELECT
  'Completeness',
  COUNT(*),
  ROUND(AVG(overall_completeness_pct), 3),
  ROUND(MIN(overall_completeness_pct), 3),
  MAX(measurement_date)
FROM acat_dimension_completeness
GROUP BY 'Completeness'

UNION ALL

SELECT
  'Precision',
  COUNT(*),
  ROUND(AVG(precision_pct), 3),
  ROUND(MIN(precision_pct), 3),
  MAX(measurement_date)
FROM acat_dimension_precision
GROUP BY 'Precision'

UNION ALL

SELECT
  'Coherence',
  COUNT(*),
  ROUND(AVG(coherence_score), 3),
  ROUND(MIN(coherence_score), 3),
  MAX(measurement_date)
FROM acat_dimension_coherence
GROUP BY 'Coherence'

UNION ALL

SELECT
  'Coverage',
  COUNT(*),
  ROUND(AVG(coverage_pct), 3),
  ROUND(MIN(coverage_pct), 3),
  MAX(measurement_date)
FROM acat_dimension_coverage
GROUP BY 'Coverage'

UNION ALL

SELECT
  'Convergence',
  COUNT(*),
  ROUND(AVG(closure_rate_gap), 3),
  ROUND(MIN(closure_rate_gap), 3),
  MAX(measurement_date)
FROM acat_dimension_convergence
GROUP BY 'Convergence'
ORDER BY dimension;

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

CREATE INDEX idx_findings_created ON empirica_audit_findings(created_at);
CREATE INDEX idx_remediations_created ON empirica_remediations(created_at);
CREATE INDEX idx_convergence_created ON empirica_convergence_measurements(created_at);

-- Dimensional indexes for fast dimensional queries
CREATE INDEX idx_accuracy_study ON acat_dimension_accuracy(research_study_id);
CREATE INDEX idx_completeness_study ON acat_dimension_completeness(research_study_id);
CREATE INDEX idx_precision_study ON acat_dimension_precision(research_study_id);
CREATE INDEX idx_coherence_study ON acat_dimension_coherence(research_study_id);
CREATE INDEX idx_coverage_study ON acat_dimension_coverage(research_study_id);
CREATE INDEX idx_convergence_study ON acat_dimension_convergence(research_study_id);

-- Extended dimension indexes
CREATE INDEX idx_time_to_detection_study ON acat_dimension_time_to_detection(research_study_id);
CREATE INDEX idx_severity_alignment_study ON acat_dimension_severity_alignment(research_study_id);
CREATE INDEX idx_category_alignment_study ON acat_dimension_category_alignment(research_study_id);
CREATE INDEX idx_cross_system_coupling_study ON acat_dimension_cross_system_coupling(research_study_id);
CREATE INDEX idx_resource_efficiency_study ON acat_dimension_resource_efficiency(research_study_id);
CREATE INDEX idx_learning_velocity_study ON acat_dimension_learning_velocity(research_study_id);

-- ============================================================================
-- V1.1 PERFORMANCE IMPROVEMENTS (2026-08-22)
-- ============================================================================
-- Added composite indexes to support:
-- - Time-series queries (measurement_date DESC + system/category)
-- - Dimensional comparisons (audit_id + system pairs)
-- - Category-based analysis
-- - Dashboard aggregations (GROUP BY support)

-- Core dimension improvements
CREATE INDEX idx_accuracy_date_audit ON acat_dimension_accuracy(measurement_date DESC, audit_id);

CREATE INDEX idx_completeness_date_system ON acat_dimension_completeness(measurement_date DESC, system);
CREATE INDEX idx_completeness_audit_date ON acat_dimension_completeness(audit_id, measurement_date DESC);

CREATE INDEX idx_precision_date_system ON acat_dimension_precision(measurement_date DESC, system);
CREATE INDEX idx_precision_category ON acat_dimension_precision(category, system);

CREATE INDEX idx_coherence_date_system ON acat_dimension_coherence(measurement_date DESC, system);

CREATE INDEX idx_coverage_date_system ON acat_dimension_coverage(measurement_date DESC, system);
CREATE INDEX idx_coverage_category_system ON acat_dimension_coverage(category, system);
CREATE INDEX idx_coverage_gap ON acat_dimension_coverage(is_coverage_gap, gap_severity);

CREATE INDEX idx_convergence_systems_date ON acat_dimension_convergence(system_a, system_b, measurement_date DESC);

-- Extended dimension improvements
CREATE INDEX idx_time_detection_audit_system ON acat_dimension_time_to_detection(audit_id, system);
CREATE INDEX idx_time_detection_category_system ON acat_dimension_time_to_detection(category, system);

CREATE INDEX idx_severity_finding_systems ON acat_dimension_severity_alignment(finding_id, system_a, system_b);

CREATE INDEX idx_category_alignment_date ON acat_dimension_category_alignment(measurement_date DESC, category);
CREATE INDEX idx_category_alignment_systems ON acat_dimension_category_alignment(system_a, system_b, category);

CREATE INDEX idx_coupling_source ON acat_dimension_cross_system_coupling(source_system, source_category);
CREATE INDEX idx_coupling_target ON acat_dimension_cross_system_coupling(target_system, target_category);

CREATE INDEX idx_efficiency_category_system ON acat_dimension_resource_efficiency(category, system);

CREATE INDEX idx_velocity_system_repo_date ON acat_dimension_learning_velocity(system, repo_name, measurement_date DESC);
CREATE INDEX idx_velocity_direction ON acat_dimension_learning_velocity(direction, measurement_date DESC);

-- Core table improvements
CREATE INDEX idx_findings_audit_created ON empirica_audit_findings(audit_id, created_at DESC);

CREATE INDEX idx_remediations_verified_at ON empirica_remediations(verified_at DESC) WHERE verified_at IS NOT NULL;
CREATE INDEX idx_remediations_assigned_date ON empirica_remediations(assigned_date DESC) WHERE assigned_date IS NOT NULL;

CREATE INDEX idx_convergence_date_study ON empirica_convergence_measurements(measurement_date DESC, research_study_id);

-- Materialized view support (dashboard queries)
CREATE INDEX idx_accuracy_f1_score ON acat_dimension_accuracy(f1_score);
CREATE INDEX idx_completeness_pct ON acat_dimension_completeness(overall_completeness_pct);
CREATE INDEX idx_precision_pct ON acat_dimension_precision(precision_pct);
CREATE INDEX idx_coherence_score ON acat_dimension_coherence(coherence_score);
CREATE INDEX idx_coverage_pct ON acat_dimension_coverage(coverage_pct);
CREATE INDEX idx_convergence_gap ON acat_dimension_convergence(closure_rate_gap);

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
