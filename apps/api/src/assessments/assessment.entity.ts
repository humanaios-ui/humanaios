/**
 * HumanAIOS Assessment Entity & Types
 * Core types for ACAT assessment submissions and results
 */

export interface Assessment {
  id: string;
  org_id: string;
  system_id: string;
  system_name: string;
  system_info: Record<string, any>;
  status: AssessmentStatus;
  result_summary?: Record<string, any>;
  created_at: Date;
  updated_at: Date;
  completed_at?: Date;
}

export type AssessmentStatus = 'pending' | 'running' | 'completed' | 'failed';

export interface CreateAssessmentDto {
  system_id: string;
  system_name: string;
  system_info: {
    description?: string;
    model_name?: string;
    version?: string;
    api_endpoint?: string;
    authentication?: Record<string, any>;
    [key: string]: any;
  };
}

export interface AssessmentResultDto {
  id: string;
  status: AssessmentStatus;
  progress_pct: number;
  completed_at?: Date;
  result?: {
    vectors: CalibrationVectors;
    findings: EpistemicArtifact[];
    recommendations: string[];
    total_duration_ms: number;
  };
}

export interface CalibrationVectors {
  know: number;
  do: number;
  context: number;
  clarity: number;
  coherence: number;
  signal: number;
  density: number;
  state: number;
  change: number;
  completion: number;
  impact: number;
  engagement: number;
  uncertainty: number;
}

// ============================================
// ACAT PROTOCOL TYPES
// ============================================

export interface ACATProtocolRun {
  id: string;
  assessment_id: string;
  step_number: number;
  step_name: string;
  status: ProtocolStepStatus;
  step_data: Record<string, any>;
  result_data?: Record<string, any>;
  duration_ms?: number;
  error_message?: string;
  created_at: Date;
  completed_at?: Date;
}

export type ProtocolStepStatus = 'pending' | 'running' | 'completed' | 'failed';

export interface ACATStep {
  number: number;
  name: string;
  description: string;
  dependencies?: number[];
  parallelizable: boolean;
  timeout_ms: number;
  input_schema: Record<string, any>;
  output_schema: Record<string, any>;
}

// ============================================
// EPISTEMIC ARTIFACT TYPES
// ============================================

export type EpistemicArtifactType = 'finding' | 'decision' | 'assumption' | 'unknown' | 'dead_end' | 'mistake';
export type ArtifactStatus = 'open' | 'resolved' | 'archived' | 'superseded';
export type EdgeRelation =
  | 'attached_to'
  | 'caused_by'
  | 'evidence'
  | 'grounded_by'
  | 'invalidates'
  | 'prevents'
  | 'raised_by'
  | 'related'
  | 'resolves'
  | 'sourced_from';

export interface EpistemicArtifact {
  id: string;
  assessment_id: string;
  task_id?: string;
  type: EpistemicArtifactType;
  title: string;
  description?: string;
  data: Record<string, any>;
  confidence?: number;
  impact?: number;
  status: ArtifactStatus;
  created_at: Date;
  resolved_at?: Date;
}

export interface EpistemicEdge {
  id: string;
  source_id: string;
  target_id: string;
  relation: EdgeRelation;
  created_at: Date;
}

// ============================================
// CREATE/UPDATE DTOs FOR EPISTEMIC ARTIFACTS
// ============================================

export interface CreateFindingDto {
  assessment_id: string;
  task_id?: string;
  finding: string;
  description?: string;
  impact?: number;
  source?: 'test-result' | 'measurement' | 'production' | 'user-report' | 'code-review';
  confidence?: number;
}

export interface CreateDecisionDto {
  assessment_id: string;
  task_id?: string;
  choice: string;
  rationale: string;
  alternatives?: string[];
  reversibility?: 'exploratory' | 'committal' | 'forced';
  domains_affected?: string[];
}

export interface CreateAssumptionDto {
  assessment_id: string;
  task_id?: string;
  assumption: string;
  confidence: number;
  domain: string;
  risk_if_wrong?: 'High' | 'Medium' | 'Low';
  resolution_plan?: string;
}

export interface CreateUnknownDto {
  assessment_id: string;
  task_id?: string;
  unknown: string;
  domain?: string;
  resolution_deadline?: Date;
  blocker_for?: string[];
}

export interface CreateDeadEndDto {
  assessment_id: string;
  task_id?: string;
  approach: string;
  why_failed: string;
  attempt_duration?: number;
  permanent_constraint?: boolean;
}

export interface CreateMistakeDto {
  assessment_id: string;
  task_id?: string;
  mistake: string;
  why_it_happened: string;
  impact?: string;
  prevention: string;
}

export interface CreateEdgeDto {
  source_id: string;
  target_id: string;
  relation: EdgeRelation;
}

// ============================================
// QUERY RESPONSE TYPES
// ============================================

export interface AssessmentWithArtifacts {
  assessment: Assessment;
  artifacts: EpistemicArtifact[];
  edges: EpistemicEdge[];
}

export interface EpistemicGraph {
  nodes: EpistemicArtifact[];
  edges: EpistemicEdge[];
  summary: {
    total_artifacts: number;
    by_type: Record<EpistemicArtifactType, number>;
    open_unknowns: number;
    avg_confidence: number;
    avg_impact: number;
  };
}

// ============================================
// BATCH OPERATIONS
// ============================================

export interface LogArtifactsBatchDto {
  nodes: Array<{
    ref: string;
    type: EpistemicArtifactType;
    data: Record<string, any>;
  }>;
  edges: Array<{
    from: string;
    to: string;
    relation: EdgeRelation;
  }>;
}

export interface ArtifactReference {
  [ref: string]: string; // ref => artifact_id mapping
}
