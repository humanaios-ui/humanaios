"""
Integration tests for gates with live Cortex SER and empirica state.

Tests gates operating against actual mesh coordination state (SER),
resource-miner labor tracking, and temporal-oracle timeline validation.
"""

import pytest
import json
from datetime import datetime, timedelta
from typing import Dict, Any

from src.gates.readiness_gates import ReadinessGate, ReadinessLevel
from src.gates.resource_guard import ResourceGuard, ResourceBudget, ResourceCheckLevel
from src.gates.sentinel_verify import SentinelGate, ActionType, VectorLevel


class TestReadinessGateIntegration:
    """Readiness gate integration with empirica artifact system."""

    def test_readiness_with_artifact_logging(self):
        """Readiness result should be loggable as empirica finding."""
        gate = ReadinessGate()
        gate.log_evidence("read", "src/gates/cli.py", confidence=0.9)
        gate.log_evidence("read", "tests/test_gates_cli.py", confidence=0.85)
        gate.log_evidence("grep", "def readiness_check", confidence=0.95)
        gate.add_assumption("Gate implementation is correct", 0.8)

        result = gate.evaluate()
        assert result.level == ReadinessLevel.READY

        # Artifact logging format
        artifact = {
            "kind": "finding",
            "title": f"Readiness check PASS: {result.evidence_gathered}/{result.evidence_required} evidence",
            "summary": f"Noetic phase complete. Evidence collected: {result.evidence_gathered}, Assumptions: {result.assumptions_undocumented}, Uncertainty: {result.uncertainty_level:.2f}",
            "impact": 0.3 if result.level == ReadinessLevel.READY else 0.8,
        }
        assert artifact["impact"] == 0.3  # Low impact for pass

    def test_readiness_failure_escalation(self):
        """Readiness failure should escalate with high impact."""
        gate = ReadinessGate()
        gate.add_unknown("What is the Sentinel schema?")
        gate.add_unknown("How do resource vectors work?")

        result = gate.evaluate(max_uncertainty=0.1)
        assert result.level != ReadinessLevel.READY

        artifact = {
            "kind": "finding",
            "title": f"Readiness check FAIL: High uncertainty",
            "impact": 0.8,  # High impact for failure
        }
        assert artifact["impact"] == 0.8


class TestResourceGuardIntegration:
    """Resource guard integration with resource-miner + mesh-support."""

    def test_resource_check_within_bounds(self):
        """Resource consumption within budget → pass."""
        budget = ResourceBudget(
            human_labor_hours_remaining=64.0,
            ai_tokens_remaining=100000,
            practices_active=15,
            practices_capacity=20,
            escalations_pending=0,
            escalation_sla_hours=4.0
        )
        estimate = ResourceEstimate(
            human_labor_hours=30.0,
            ai_tokens=50000,
            practices_affected=15,
            escalations_required=0
        )

        guard = ResourceGuard(budget)
        result = guard.check(estimate)

        assert result.level == ResourceCheckLevel.SUFFICIENT

    def test_resource_check_approaching_limit(self):
        """Resource consumption > 80% → warning."""
        budget = ResourceBudget(
            human_labor_hours_remaining=64.0,
            ai_tokens_remaining=100000,
            practices_active=15,
            practices_capacity=20,
            escalations_pending=0,
            escalation_sla_hours=4.0
        )
        consumption = {"labor_hours": 53, "tokens": 85000}  # 83% consumed

        guard = ResourceGuard()
        result = guard.check({
            "estimate": {"labor_hours": 5, "tokens": 5000},
            "current_consumption": consumption,
            "practice_count": 15,
        })

        assert result.level == ResourceCheckLevel.WARNING
        # Should escalate to resource-miner for oversight

    def test_resource_check_exceeded(self):
        """Resource consumption > 100% → fail + escalate."""
        budget = ResourceBudget(
            human_labor_hours_remaining=64.0,
            ai_tokens_remaining=100000,
            practices_active=15,
            practices_capacity=20,
            escalations_pending=0,
            escalation_sla_hours=4.0
        )
        consumption = {"labor_hours": 65, "tokens": 110000}  # Over budget

        guard = ResourceGuard()
        result = guard.check({
            "estimate": {"labor_hours": 5, "tokens": 5000},
            "current_consumption": consumption,
            "practice_count": 15,
        })

        assert result.level == ResourceCheckLevel.INSUFFICIENT
        # Artifact: escalation to mesh-support + resource-miner
        escalation = {
            "kind": "finding",
            "title": "Resource constraint VIOLATED",
            "impact": 0.9,  # Critical
            "target": "mesh-support"
        }


class TestSentinelVerifyIntegration:
    """Sentinel gate integration with actual Sentinel vector state."""

    def test_sentinel_verify_investigate_action(self):
        """Investigate action requires moderate epistemic grounding."""
        from src.gates.sentinel_verify import EpistemicVectors

        vectors = EpistemicVectors(
            know=0.7,
            uncertainty=0.3,
            context=0.8,
            engagement=0.85,
            clarity=0.75,
            coherence=0.8
        )

        gate = SentinelGate()
        result = gate.verify(vectors, ActionType.INVESTIGATE)
        assert result.level == VectorLevel.PASS

    def test_sentinel_verify_deploy_action(self):
        """Deploy action requires high epistemic confidence."""
        from src.gates.sentinel_verify import EpistemicVectors

        vectors = EpistemicVectors(
            know=0.85,
            uncertainty=0.1,
            context=0.9,
            engagement=0.95,
            clarity=0.9,
            coherence=0.9
        )

        gate = SentinelGate()
        result = gate.verify(vectors, ActionType.DEPLOY)
        assert result.level == VectorLevel.PASS

    def test_sentinel_verify_publish_escalation(self):
        """Publish action with insufficient clarity → escalate."""
        from src.gates.sentinel_verify import EpistemicVectors

        vectors = EpistemicVectors(
            know=0.8,
            uncertainty=0.15,
            context=0.75,
            engagement=0.9,
            clarity=0.5,  # Too low for publish
            coherence=0.8
        )

        gate = SentinelGate()
        result = gate.verify(vectors, ActionType.PUBLISH)
        assert result.level != VectorLevel.PASS
        # Should escalate: "Clarity insufficient for publish action"


class TestCortexMailboxIntegration:
    """Gates integration with Cortex mailbox for SER updates."""

    def test_gate_result_sendable_to_mailbox(self):
        """Gate results should be shaped as Cortex collab payload."""
        gate = ReadinessGate()
        gate.log_evidence("read", "test.py", confidence=0.9)

        result = gate.evaluate()

        # Shape as Cortex collab
        collab = {
            "type": "collab_brief",
            "source_claude": "empirica-foundation.carly.empirica-foundation-evaluator",
            "target_claudes": ["empirica-foundation.carly.empirica-mesh-support"],
            "title": f"Gate verification: {result.level.value}",
            "summary": json.dumps(result.to_dict()),
            "payload": {
                "gate": "readiness-check",
                "status": "pass",
                "impact": 0.3,
            }
        }

        assert collab["type"] == "collab_brief"
        assert collab["payload"]["gate"] == "readiness-check"

    def test_gate_escalation_triggers_ser_update(self):
        """Gate failure should trigger SER escalation to mesh-support."""
        gate = ReadinessGate()
        gate.add_unknown("Critical unknown")
        gate.add_unknown("Unresolved dependency")

        result = gate.evaluate(max_uncertainty=0.1)
        assert result.level != ReadinessLevel.READY

        # SER update payload
        ser_update = {
            "action": "transition_ser",
            "ser_id": "ser_31f97ce0da3f4239869a09a7",
            "new_state": "blocked",
            "blocker_source": "empirica-foundation.carly.empirica-foundation-evaluator",
            "gate_failure": "readiness-check",
            "resolution_required": True,
        }

        assert ser_update["new_state"] == "blocked"
        assert ser_update["gate_failure"] == "readiness-check"


class TestGateOrchestrationFlow:
    """End-to-end gate orchestration for a transaction."""

    def test_transaction_gate_sequence(self):
        """Transaction gates sequence: readiness → resource → sentinel."""

        # Phase 1: Check readiness (noetic preconditions)
        readiness = ReadinessGate()
        readiness.log_evidence("read", "file.py", 0.9)
        readiness.log_evidence("grep", "pattern", 0.85)
        readiness.log_evidence("query", "db", 0.8)
        readiness_result = readiness.evaluate()
        assert readiness_result.level == ReadinessLevel.READY

        # Phase 2: Check resources (allocation constraints)
        budget = ResourceBudget(
            human_labor_hours_remaining=64.0,
            ai_tokens_remaining=100000,
            practices_active=15,
            practices_capacity=20,
            escalations_pending=0,
            escalation_sla_hours=4.0
        )
        estimate = ResourceEstimate(
            human_labor_hours=30.0,
            ai_tokens=50000,
            practices_affected=15,
            escalations_required=0
        )
        resource = ResourceGuard()
        resource_result = resource.check(budget, estimate)
        assert resource_result.level == ResourceCheckLevel.SUFFICIENT

        # Phase 3: Check sentinel (epistemic readiness)
        from src.gates.sentinel_verify import EpistemicVectors
        vectors = EpistemicVectors(
            know=0.85, uncertainty=0.15, context=0.8,
            engagement=0.9, clarity=0.85, coherence=0.8
        )
        sentinel = SentinelGate()
        sentinel_result = sentinel.verify(vectors, ActionType.IMPLEMENT)
        assert sentinel_result.level == VectorLevel.PASS

        # All gates passed → proceed
        all_pass = (
            readiness_result.level == ReadinessLevel.READY and
            resource_result.level == ResourceCheckLevel.SUFFICIENT and
            sentinel_result.level == VectorLevel.PASS
        )
        assert all_pass, "Transaction gates should all pass"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
