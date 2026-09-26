"""
Test suite for readiness gates.
"""

import pytest
from src.gates.readiness_gates import (
    ReadinessGate,
    ReadinessLevel,
    EvidenceRequirement,
)


@pytest.fixture
def gate():
    """Create a fresh readiness gate for each test."""
    return ReadinessGate()


class TestEvidenceLogging:
    """Test evidence collection and logging."""

    def test_log_single_evidence(self, gate):
        """Record one piece of evidence."""
        gate.log_evidence(
            kind="read",
            source="empirica-system-prompt.md",
            confidence=0.95,
            notes="TRANSACTION DISCIPLINE section"
        )
        assert len(gate.evidence_log) == 1
        assert gate.evidence_log[0]["kind"] == "read"
        assert gate.evidence_log[0]["confidence"] == 0.95

    def test_log_multiple_evidence(self, gate):
        """Record multiple pieces of evidence from different sources."""
        gate.log_evidence("read", "source1.py", 0.9)
        gate.log_evidence("grep", "codebase", 0.7, "found 5 matches")
        gate.log_evidence("query", "empirica db", 0.85)

        assert len(gate.evidence_log) == 3
        assert gate.evidence_log[1]["kind"] == "grep"

    def test_average_confidence(self, gate):
        """Compute average confidence across evidence."""
        gate.log_evidence("read", "s1", 1.0)
        gate.log_evidence("read", "s2", 0.8)
        gate.log_evidence("read", "s3", 0.6)

        avg = gate._avg_confidence()
        assert abs(avg - 0.8) < 0.01  # (1.0 + 0.8 + 0.6) / 3


class TestAssumptionTracking:
    """Test assumption documentation."""

    def test_add_assumption(self, gate):
        """Record an assumption."""
        gate.add_assumption("API will accept JSON payloads", 0.8)
        assert len(gate.assumptions) == 1
        assert "API will accept" in gate.assumptions[0]

    def test_multiple_assumptions(self, gate):
        """Track multiple assumptions."""
        gate.add_assumption("Assumption 1", 0.7)
        gate.add_assumption("Assumption 2", 0.5)
        gate.add_assumption("Assumption 3", 0.9)

        assert len(gate.assumptions) == 3


class TestUnknownTracking:
    """Test unknown recording."""

    def test_add_unknown(self, gate):
        """Record something unknown."""
        gate.add_unknown("Sentinel vector update frequency")
        assert len(gate.unknowns) == 1
        assert "Sentinel vector" in gate.unknowns[0]


class TestReadinessEvaluation:
    """Test readiness assessment logic."""

    def test_insufficient_evidence(self, gate):
        """Readiness fails with insufficient evidence."""
        gate.log_evidence("read", "file1.py", 0.8)
        result = gate.evaluate(min_evidence_items=3)

        assert result.level == ReadinessLevel.NOT_READY
        assert any("Insufficient evidence" in b for b in result.blockers)

    def test_sufficient_evidence(self, gate):
        """Readiness passes with enough evidence."""
        for i in range(3):
            gate.log_evidence("read", f"file{i}.py", 0.8)

        result = gate.evaluate(min_evidence_items=3)
        assert result.level == ReadinessLevel.READY

    def test_too_many_assumptions(self, gate):
        """Readiness blocked by excessive undocumented assumptions."""
        gate.log_evidence("read", "f1", 0.9)
        gate.log_evidence("read", "f2", 0.9)
        gate.log_evidence("read", "f3", 0.9)

        gate.add_assumption("A1", 0.6)
        gate.add_assumption("A2", 0.6)
        gate.add_assumption("A3", 0.6)

        result = gate.evaluate(max_undocumented_assumptions=2)
        assert result.level == ReadinessLevel.NOT_READY
        assert any("Too many undocumented" in b for b in result.blockers)

    def test_high_uncertainty(self, gate):
        """Readiness blocked by excessive uncertainty."""
        # Add low-confidence evidence
        gate.log_evidence("read", "f1", 0.4)
        gate.log_evidence("grep", "g1", 0.3)
        gate.log_evidence("query", "q1", 0.2)

        result = gate.evaluate(max_uncertainty=0.1)
        assert result.level == ReadinessLevel.NOT_READY

    def test_partially_ready(self, gate):
        """Readiness marked as partially when recommendations exist but no blockers."""
        gate.log_evidence("read", "f1", 0.85)
        gate.log_evidence("read", "f2", 0.85)
        gate.log_evidence("read", "f3", 0.85)

        # Add some unknowns (not enough to block, just to trigger recommendation)
        for i in range(4):
            gate.add_unknown(f"Unknown {i}")

        result = gate.evaluate(max_undocumented_assumptions=5, max_uncertainty=0.4)
        # With 4 unknowns: 0.15 base + 0.2 unknown_risk = 0.35 uncertainty (within threshold)
        # Should pass or be partially ready
        assert result.level in [ReadinessLevel.READY, ReadinessLevel.PARTIALLY_READY]

    def test_uncertainty_computation(self, gate):
        """Uncertainty combines confidence, unknowns, and assumptions."""
        gate.log_evidence("read", "f1", 0.8)  # 0.2 base uncertainty
        gate.add_unknown("U1")  # +0.05
        gate.add_unknown("U2")  # +0.05
        gate.add_assumption("A1", 0.7)  # +0.03

        uncertainty = gate._compute_uncertainty()
        # Expected: 0.2 + 0.1 + 0.03 = 0.33
        assert abs(uncertainty - 0.33) < 0.01


class TestSerialization:
    """Test JSON serialization."""

    def test_to_json(self, gate):
        """Serialize gate state to JSON."""
        gate.log_evidence("read", "file.py", 0.85)
        gate.add_assumption("Test assumption", 0.7)
        gate.add_unknown("Test unknown")

        json_str = gate.to_json()
        assert "evidence_log" in json_str
        assert "file.py" in json_str
        assert "Test assumption" in json_str

    def test_result_to_dict(self, gate):
        """Serialize result to dictionary."""
        gate.log_evidence("read", "f1", 0.9)
        gate.log_evidence("read", "f2", 0.9)
        gate.log_evidence("read", "f3", 0.9)

        result = gate.evaluate()
        result_dict = result.to_dict()

        assert result_dict["level"] == "ready"
        assert result_dict["evidence_gathered"] == 3
        assert isinstance(result_dict["blockers"], list)
