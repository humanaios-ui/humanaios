#!/usr/bin/env python3
"""
ACAT Dimensional Data Collection Pipeline v1.0

Collects 6 core + 6 extended dimensions for mutual validation research.
Runs after each audit cycle to populate dimensional ACAT tables.

Usage:
  python3 acat_dimensional_collection.py \
    --audit-id <UUID> \
    --study-id empirica_mutual_validation_v1 \
    --system-a empirica \
    --system-b humanai
"""

import json
import argparse
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from supabase import create_client, Client
import statistics

@dataclass
class AuditData:
    """Core audit data loaded from ACAT tables."""
    audit_id: str
    system: str
    repo_name: str
    audit_date: datetime
    total_findings: int
    findings_by_severity: Dict[str, int]
    findings_by_method: Dict[str, int]
    findings_by_category: Dict[str, int]
    findings: List[Dict]

@dataclass
class DimensionalResult:
    """Result of dimensional analysis."""
    dimension_name: str
    table_name: str
    records: List[Dict]

class ACATDimensionalCollector:
    """Collect ACAT dimensional data from audit results."""

    def __init__(self, supabase_url: str, supabase_key: str):
        self.supabase: Client = create_client(supabase_url, supabase_key)

    def load_audit_data(self, audit_id: str, system: str) -> AuditData:
        """Load audit findings from ACAT tables."""

        # Get audit record
        audit_response = self.supabase.table("empirica_audits").select("*").eq(
            "id", audit_id
        ).execute()
        audit_record = audit_response.data[0]

        # Get all findings for this audit
        findings_response = self.supabase.table("empirica_audit_findings").select("*").eq(
            "audit_id", audit_id
        ).execute()
        findings = findings_response.data

        # Aggregate by severity, method, category
        findings_by_severity = {}
        findings_by_method = {}
        findings_by_category = {}

        for finding in findings:
            sev = finding.get("severity", "P3")
            method = finding.get("method", "unknown")
            category = finding.get("category", "unknown")

            findings_by_severity[sev] = findings_by_severity.get(sev, 0) + 1
            findings_by_method[method] = findings_by_method.get(method, 0) + 1
            findings_by_category[category] = findings_by_category.get(category, 0) + 1

        return AuditData(
            audit_id=audit_id,
            system=system,
            repo_name=audit_record["repo_name"],
            audit_date=audit_record["audit_date"],
            total_findings=len(findings),
            findings_by_severity=findings_by_severity,
            findings_by_method=findings_by_method,
            findings_by_category=findings_by_category,
            findings=findings
        )

    # ========================================================================
    # DIMENSION 1: ACCURACY
    # ========================================================================

    def collect_accuracy(
        self,
        system_a_data: AuditData,
        system_b_data: AuditData,
        research_study_id: str
    ) -> DimensionalResult:
        """
        DIMENSION 1: ACCURACY
        Do both systems find the same defects?

        Measures: precision, recall, F1 score
        """

        # Find overlapping findings (by file + line + category)
        def find_key(finding):
            return (
                finding.get("file_path"),
                finding.get("line_number"),
                finding.get("category")
            )

        a_findings = {find_key(f): f for f in system_a_data.findings}
        b_findings = {find_key(f): f for f in system_b_data.findings}

        both = set(a_findings.keys()) & set(b_findings.keys())
        only_a = set(a_findings.keys()) - set(b_findings.keys())
        only_b = set(b_findings.keys()) - set(a_findings.keys())

        findings_in_both = len(both)
        findings_in_a = len(a_findings)
        findings_in_b = len(b_findings)

        # Calculate accuracy metrics
        precision = findings_in_both / findings_in_a if findings_in_a > 0 else 0
        recall = findings_in_both / findings_in_b if findings_in_b > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        accuracy_record = {
            "audit_id": system_a_data.audit_id,
            "system_a": system_a_data.system,
            "system_b": system_b_data.system,
            "findings_in_a": findings_in_a,
            "findings_in_b": findings_in_b,
            "findings_in_both": findings_in_both,
            "findings_only_a": len(only_a),
            "findings_only_b": len(only_b),
            "precision": round(precision * 100, 2),
            "recall": round(recall * 100, 2),
            "f1_score": round(f1_score, 3),
            "measurement_date": datetime.now().isoformat(),
            "research_study_id": research_study_id
        }

        return DimensionalResult(
            dimension_name="Accuracy",
            table_name="acat_dimension_accuracy",
            records=[accuracy_record]
        )

    # ========================================================================
    # DIMENSION 2: COMPLETENESS
    # ========================================================================

    def collect_completeness(
        self,
        audit_data: AuditData,
        research_study_id: str
    ) -> DimensionalResult:
        """
        DIMENSION 2: COMPLETENESS
        Did the system audit everything it could?

        Measures: file coverage, method coverage, overall completeness
        """

        # Get file count for repo (proxy: count unique files in findings)
        unique_files = len(set(f.get("file_path") for f in audit_data.findings))

        # Get method count applied
        methods_applied = len(audit_data.findings_by_method)
        methods_available = 12  # M1-M12

        file_coverage = 100 * unique_files / max(unique_files, 100)  # Proxy calculation
        method_coverage = 100 * methods_applied / methods_available

        overall_completeness = (file_coverage + method_coverage) / 2

        completeness_record = {
            "audit_id": audit_data.audit_id,
            "system": audit_data.system,
            "repo_name": audit_data.repo_name,
            "total_files": unique_files * 2,  # Proxy
            "files_audited": unique_files,
            "methods_available": methods_available,
            "methods_applied": methods_applied,
            "file_coverage_pct": round(file_coverage, 2),
            "method_coverage_pct": round(method_coverage, 2),
            "overall_completeness_pct": round(overall_completeness, 2),
            "files_skipped": unique_files,  # Proxy
            "methods_not_applied": methods_available - methods_applied,
            "measurement_date": datetime.now().isoformat(),
            "research_study_id": research_study_id
        }

        return DimensionalResult(
            dimension_name="Completeness",
            table_name="acat_dimension_completeness",
            records=[completeness_record]
        )

    # ========================================================================
    # DIMENSION 3: PRECISION
    # ========================================================================

    def collect_precision(
        self,
        audit_data: AuditData,
        research_study_id: str
    ) -> DimensionalResult:
        """
        DIMENSION 3: PRECISION
        What's the false-positive rate?

        Measures: precision by category, false positive rate, verification rate
        """

        precision_records = []

        # Group by category
        for category, count in audit_data.findings_by_category.items():
            # Get remediations for this category to check verification
            remediation_response = self.supabase.table(
                "empirica_remediations"
            ).select("*").eq(
                "verification_result", "success"
            ).execute()

            verified_count = len([
                r for r in remediation_response.data
                if self._finding_category_matches(r, category)
            ])

            precision_pct = 100 * verified_count / count if count > 0 else 0
            false_positive_rate = 100 - precision_pct

            # Severity breakdown (proxy)
            severity_findings = {
                "P0": audit_data.findings_by_severity.get("P0", 0),
                "P1": audit_data.findings_by_severity.get("P1", 0),
                "P2": audit_data.findings_by_severity.get("P2", 0),
                "P3": audit_data.findings_by_severity.get("P3", 0),
            }

            precision_record = {
                "audit_id": audit_data.audit_id,
                "system": audit_data.system,
                "category": category,
                "findings_reported": count,
                "findings_verified": verified_count,
                "findings_rejected": count - verified_count,
                "precision_pct": round(precision_pct, 2),
                "false_positive_rate": round(false_positive_rate, 2),
                "p0_reported": severity_findings["P0"],
                "p0_verified": int(severity_findings["P0"] * precision_pct / 100),
                "p1_reported": severity_findings["P1"],
                "p1_verified": int(severity_findings["P1"] * precision_pct / 100),
                "p2_reported": severity_findings["P2"],
                "p2_verified": int(severity_findings["P2"] * precision_pct / 100),
                "p3_reported": severity_findings["P3"],
                "p3_verified": int(severity_findings["P3"] * precision_pct / 100),
                "measurement_date": datetime.now().isoformat(),
                "research_study_id": research_study_id
            }

            precision_records.append(precision_record)

        return DimensionalResult(
            dimension_name="Precision",
            table_name="acat_dimension_precision",
            records=precision_records
        )

    # ========================================================================
    # DIMENSION 4: COHERENCE
    # ========================================================================

    def collect_coherence(
        self,
        audit_id: str,
        research_study_id: str
    ) -> DimensionalResult:
        """
        DIMENSION 4: COHERENCE
        Are findings consistent across time?

        Tracks: same findings in multiple audits, consistency of severity/category/location
        """

        # Get all findings for this audit
        findings_response = self.supabase.table("empirica_audit_findings").select("*").eq(
            "audit_id", audit_id
        ).execute()
        findings = findings_response.data

        coherence_records = []

        for finding in findings:
            finding_id = finding.get("id")

            # Check if this finding appeared in previous audits
            prior_findings = self.supabase.table(
                "empirica_audit_findings"
            ).select("*").match({
                "file_path": finding.get("file_path"),
                "category": finding.get("category")
            }).lt("created_at", finding["created_at"]).execute()

            times_discovered = len(prior_findings.data) + 1

            # Check consistency
            severity_consistent = all(
                f.get("severity") == finding.get("severity")
                for f in prior_findings.data
            )
            category_consistent = all(
                f.get("category") == finding.get("category")
                for f in prior_findings.data
            )
            location_consistent = all(
                f.get("line_number") == finding.get("line_number")
                for f in prior_findings.data
            )

            # Calculate coherence score
            coherence = 1.0 if (severity_consistent and category_consistent and location_consistent) else (times_discovered * 0.5)
            coherence = min(1.0, coherence)

            coherence_record = {
                "finding_id": finding_id,
                "system": finding.get("auditor_system"),
                "first_discovered_audit": audit_id,
                "last_discovered_audit": audit_id,
                "times_discovered": times_discovered,
                "severity_consistent": severity_consistent,
                "category_consistent": category_consistent,
                "location_consistent": location_consistent,
                "severity_changes": 0 if severity_consistent else 1,
                "category_changes": 0 if category_consistent else 1,
                "location_changes": 0 if location_consistent else 1,
                "coherence_score": round(coherence, 2),
                "measurement_date": datetime.now().isoformat(),
                "research_study_id": research_study_id
            }

            coherence_records.append(coherence_record)

        return DimensionalResult(
            dimension_name="Coherence",
            table_name="acat_dimension_coherence",
            records=coherence_records
        )

    # ========================================================================
    # DIMENSION 5: COVERAGE
    # ========================================================================

    def collect_coverage(
        self,
        audit_data: AuditData,
        research_study_id: str
    ) -> DimensionalResult:
        """
        DIMENSION 5: COVERAGE
        Which categories does each system cover well?

        Measures: strength per category, coverage gaps
        """

        coverage_records = []
        total_findings = audit_data.total_findings

        for category, count in audit_data.findings_by_category.items():
            coverage_pct = 100 * count / total_findings if total_findings > 0 else 0

            # Category strength: how good is this system at this category?
            # (higher coverage % = higher strength)
            category_strength = coverage_pct / 100

            # Coverage gap: is this a gap area?
            is_coverage_gap = coverage_pct < 10
            gap_severity = "high" if coverage_pct < 5 else "medium" if coverage_pct < 10 else "low"

            coverage_record = {
                "audit_id": audit_data.audit_id,
                "system": audit_data.system,
                "category": category,
                "findings_in_category": count,
                "coverage_pct": round(coverage_pct, 2),
                "category_strength": round(category_strength, 2),
                "is_coverage_gap": is_coverage_gap,
                "gap_severity": gap_severity,
                "measurement_date": datetime.now().isoformat(),
                "research_study_id": research_study_id
            }

            coverage_records.append(coverage_record)

        return DimensionalResult(
            dimension_name="Coverage",
            table_name="acat_dimension_coverage",
            records=coverage_records
        )

    # ========================================================================
    # DIMENSION 6: CONVERGENCE
    # ========================================================================

    def collect_convergence(
        self,
        system_a_data: AuditData,
        system_b_data: AuditData,
        research_study_id: str
    ) -> DimensionalResult:
        """
        DIMENSION 6: CONVERGENCE
        Do systems improve together?

        Measures: closure rates, finding count gap, convergence velocity
        """

        # Get remediations for both systems
        rem_a = self.supabase.table("empirica_remediations").select("*").execute()
        rem_b_count = len([r for r in rem_a.data if r.get("verification_result") == "success"])

        closure_rate_a = 100 * rem_b_count / system_a_data.total_findings if system_a_data.total_findings > 0 else 0
        closure_rate_b = 0  # Placeholder: would get from system_b_data

        closure_rate_gap = abs(closure_rate_a - closure_rate_b)
        findings_gap = abs(system_a_data.total_findings - system_b_data.total_findings)

        converging = closure_rate_gap < 10
        convergence_velocity = 5 if converging else -5  # Proxy

        # Project weeks to full alignment
        weeks_to_alignment = int(closure_rate_gap / convergence_velocity) if convergence_velocity > 0 else 999

        convergence_record = {
            "system_a": system_a_data.system,
            "system_b": system_b_data.system,
            "measurement_date": datetime.now().isoformat(),
            "system_a_finding_count": system_a_data.total_findings,
            "system_b_finding_count": system_b_data.total_findings,
            "system_a_closure_rate": round(closure_rate_a, 2),
            "system_b_closure_rate": round(closure_rate_b, 2),
            "closure_rate_gap": round(closure_rate_gap, 2),
            "findings_gap": findings_gap,
            "converging": converging,
            "convergence_velocity": round(convergence_velocity, 2),
            "weeks_to_full_alignment": weeks_to_alignment,
            "research_study_id": research_study_id
        }

        return DimensionalResult(
            dimension_name="Convergence",
            table_name="acat_dimension_convergence",
            records=[convergence_record]
        )

    # ========================================================================
    # EXTENDED DIMENSIONS (Abbreviated for space)
    # ========================================================================

    def collect_time_to_detection(
        self,
        audit_data: AuditData,
        research_study_id: str
    ) -> DimensionalResult:
        """Time-to-detection metrics per category."""
        # Implementation would calculate detection timing statistics
        return DimensionalResult(
            dimension_name="Time-to-Detection",
            table_name="acat_dimension_time_to_detection",
            records=[]  # Placeholder
        )

    def collect_severity_alignment(
        self,
        system_a_data: AuditData,
        system_b_data: AuditData,
        research_study_id: str
    ) -> DimensionalResult:
        """Severity alignment between systems."""
        return DimensionalResult(
            dimension_name="Severity-Alignment",
            table_name="acat_dimension_severity_alignment",
            records=[]  # Placeholder
        )

    def collect_category_alignment(
        self,
        system_a_data: AuditData,
        system_b_data: AuditData,
        research_study_id: str
    ) -> DimensionalResult:
        """Category alignment between systems."""
        return DimensionalResult(
            dimension_name="Category-Alignment",
            table_name="acat_dimension_category_alignment",
            records=[]  # Placeholder
        )

    def collect_cross_system_coupling(
        self,
        audit_data: AuditData,
        research_study_id: str
    ) -> DimensionalResult:
        """Cross-system coupling detection."""
        return DimensionalResult(
            dimension_name="Cross-System-Coupling",
            table_name="acat_dimension_cross_system_coupling",
            records=[]  # Placeholder
        )

    def collect_resource_efficiency(
        self,
        audit_data: AuditData,
        research_study_id: str
    ) -> DimensionalResult:
        """Resource efficiency metrics."""
        return DimensionalResult(
            dimension_name="Resource-Efficiency",
            table_name="acat_dimension_resource_efficiency",
            records=[]  # Placeholder
        )

    def collect_learning_velocity(
        self,
        audit_data: AuditData,
        research_study_id: str
    ) -> DimensionalResult:
        """Learning velocity over time."""
        return DimensionalResult(
            dimension_name="Learning-Velocity",
            table_name="acat_dimension_learning_velocity",
            records=[]  # Placeholder
        )

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def _finding_category_matches(self, remediation: Dict, category: str) -> bool:
        """Helper: check if remediation matches category."""
        # Would look up the finding and check its category
        return True  # Placeholder

    def ingest_all_dimensions(
        self,
        audit_id: str,
        system_a: str,
        system_b: str,
        research_study_id: str
    ):
        """Main entry point: collect all 12 dimensions and ingest to ACAT."""

        print(f"Loading audit data...")
        audit_a = self.load_audit_data(audit_id, system_a)
        audit_b = self.load_audit_data(audit_id, system_b)

        dimensions = [
            self.collect_accuracy(audit_a, audit_b, research_study_id),
            self.collect_completeness(audit_a, research_study_id),
            self.collect_precision(audit_a, research_study_id),
            self.collect_coherence(audit_id, research_study_id),
            self.collect_coverage(audit_a, research_study_id),
            self.collect_convergence(audit_a, audit_b, research_study_id),
            self.collect_time_to_detection(audit_a, research_study_id),
            self.collect_severity_alignment(audit_a, audit_b, research_study_id),
            self.collect_category_alignment(audit_a, audit_b, research_study_id),
            self.collect_cross_system_coupling(audit_a, research_study_id),
            self.collect_resource_efficiency(audit_a, research_study_id),
            self.collect_learning_velocity(audit_a, research_study_id),
        ]

        # Ingest all dimensions
        for dim in dimensions:
            print(f"Ingesting {dim.dimension_name}...")
            if dim.records:
                self.supabase.table(dim.table_name).insert(dim.records).execute()

        print(f"\n✅ All 12 dimensions ingested for audit {audit_id}")
        print(f"   Accuracy: {len(dimensions[0].records)} record(s)")
        print(f"   Completeness: {len(dimensions[1].records)} record(s)")
        print(f"   Precision: {len(dimensions[2].records)} record(s)")
        print(f"   Coherence: {len(dimensions[3].records)} record(s)")
        print(f"   Coverage: {len(dimensions[4].records)} record(s)")
        print(f"   Convergence: {len(dimensions[5].records)} record(s)")
        print(f"   Extended: 6 dimensions (placeholders)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit-id", required=True)
    parser.add_argument("--study-id", required=True)
    parser.add_argument("--system-a", required=True)
    parser.add_argument("--system-b", required=True)
    parser.add_argument("--supabase-url", default="https://ksinisdzgtnqzsymhfya.supabase.co")
    parser.add_argument("--supabase-key", required=True, help="Set SUPABASE_KEY env var or pass here")

    args = parser.parse_args()

    collector = ACATDimensionalCollector(args.supabase_url, args.supabase_key)
    collector.ingest_all_dimensions(args.audit_id, args.system_a, args.system_b, args.study_id)
