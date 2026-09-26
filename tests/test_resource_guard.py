"""
Test suite for resource guard gates.
"""

import pytest
from src.gates.resource_guard import (
    ResourceGuard,
    ResourceBudget,
    ResourceEstimate,
    ResourceCheckLevel,
)


@pytest.fixture
def budget():
    """Create a healthy resource budget."""
    return ResourceBudget(
        human_labor_hours_remaining=100.0,
        ai_tokens_remaining=500000,
        practices_active=5,
        practices_capacity=15,
        escalations_pending=2,
        escalation_sla_hours=4.0,
    )


@pytest.fixture
def guard(budget):
    """Create a guard with standard budget."""
    return ResourceGuard(budget)


@pytest.fixture
def small_estimate():
    """Small work estimate."""
    return ResourceEstimate(
        human_labor_hours=5.0,
        ai_tokens=50000,
        practices_affected=1,
        escalations_required=0,
    )


@pytest.fixture
def medium_estimate():
    """Medium work estimate."""
    return ResourceEstimate(
        human_labor_hours=30.0,
        ai_tokens=150000,
        practices_affected=2,
        escalations_required=1,
    )


@pytest.fixture
def large_estimate():
    """Large work estimate exceeding budget."""
    return ResourceEstimate(
        human_labor_hours=150.0,
        ai_tokens=600000,
        practices_affected=5,
        escalations_required=3,
    )


class TestHumanLaborCheck:
    """Test human labor budget verification."""

    def test_sufficient_labor(self, guard, small_estimate):
        """Labor check passes with sufficient budget."""
        result = guard.check(small_estimate)
        assert result.level == ResourceCheckLevel.SUFFICIENT
        assert any("sufficient" in c.lower() for c in result.passed_checks)

    def test_insufficient_labor(self, guard, large_estimate):
        """Labor check fails with overcommit."""
        result = guard.check(large_estimate)
        assert result.level == ResourceCheckLevel.INSUFFICIENT
        assert any("overcommit" in b.lower() for b in result.blockers)

    def test_labor_warning(self, guard, medium_estimate):
        """Labor warning when near 80% threshold."""
        # Create tight budget scenario
        guard.budget.human_labor_hours_remaining = 35.0
        result = guard.check(medium_estimate)

        # Should pass but warn
        if result.level == ResourceCheckLevel.WARNING:
            assert any("warning" in w.lower() for w in result.warnings)


class TestTokenBudgetCheck:
    """Test AI token budget verification."""

    def test_sufficient_tokens(self, guard, small_estimate):
        """Token check passes with sufficient budget."""
        result = guard.check(small_estimate)
        assert result.level == ResourceCheckLevel.SUFFICIENT

    def test_insufficient_tokens(self, guard, large_estimate):
        """Token check fails with overcommit."""
        result = guard.check(large_estimate)
        assert result.level == ResourceCheckLevel.INSUFFICIENT
        assert any("Token budget" in b for b in result.blockers)

    def test_token_warning(self, guard):
        """Token warning when near 75% threshold."""
        guard.budget.ai_tokens_remaining = 160000
        estimate = ResourceEstimate(
            human_labor_hours=5.0,
            ai_tokens=130000,
            practices_affected=0,
            escalations_required=0,
        )
        result = guard.check(estimate)

        if result.level == ResourceCheckLevel.WARNING:
            assert any("warning" in w.lower() for w in result.warnings)


class TestPracticeCapacityCheck:
    """Test practice load verification."""

    def test_within_capacity(self, guard, small_estimate):
        """Check passes when within capacity."""
        result = guard.check(small_estimate)
        # 5 active + 1 new = 6 << 15 capacity
        assert result.level in [
            ResourceCheckLevel.SUFFICIENT,
            ResourceCheckLevel.WARNING,
        ]

    def test_exceeds_capacity(self, guard):
        """Check fails when exceeds capacity."""
        estimate = ResourceEstimate(
            human_labor_hours=10.0,
            ai_tokens=100000,
            practices_affected=11,  # 5 + 11 > 15
            escalations_required=0,
        )
        result = guard.check(estimate)
        assert result.level == ResourceCheckLevel.INSUFFICIENT
        assert any("capacity exceeded" in b.lower() for b in result.blockers)

    def test_capacity_warning(self, guard):
        """Warn when approaching 85% capacity."""
        guard.budget.practices_active = 12  # 12 + 1 = 13 (86.7%)
        estimate = ResourceEstimate(
            human_labor_hours=5.0,
            ai_tokens=50000,
            practices_affected=1,
            escalations_required=0,
        )
        result = guard.check(estimate)
        # Should trigger warning
        if result.level == ResourceCheckLevel.WARNING:
            assert any("capacity warning" in w.lower() for w in result.warnings)


class TestEscalationCheck:
    """Test escalation queue verification."""

    def test_escalation_available(self, guard, small_estimate):
        """Escalations available within SLA."""
        small_estimate.escalations_required = 1
        result = guard.check(small_estimate)
        # Should pass
        assert result.level in [
            ResourceCheckLevel.SUFFICIENT,
            ResourceCheckLevel.WARNING,
        ]

    def test_escalation_queue_warning(self, guard):
        """Warn when escalation queue filling."""
        # 2 pending + 3 new escalations in 4h SLA (capacity ~2)
        guard.budget.escalations_pending = 2
        estimate = ResourceEstimate(
            human_labor_hours=5.0,
            ai_tokens=50000,
            practices_affected=0,
            escalations_required=3,
        )
        result = guard.check(estimate)
        # Should trigger warning
        if result.level == ResourceCheckLevel.WARNING:
            assert any("Escalation queue" in w for w in result.warnings)


class TestBudgetUpdates:
    """Test budget state management."""

    def test_update_budget(self, guard):
        """Update budget after consuming resources."""
        old_labor = guard.budget.human_labor_hours_remaining
        new_budget = ResourceBudget(
            human_labor_hours_remaining=old_labor - 25.0,
            ai_tokens_remaining=400000,
            practices_active=6,
            practices_capacity=15,
            escalations_pending=3,
            escalation_sla_hours=4.0,
        )
        guard.update_budget(new_budget)

        assert guard.budget.human_labor_hours_remaining == old_labor - 25.0
        assert guard.budget.practices_active == 6


class TestSerialization:
    """Test result serialization."""

    def test_result_to_dict(self, guard, small_estimate):
        """Serialize result to dictionary."""
        result = guard.check(small_estimate)
        result_dict = result.to_dict()

        assert "level" in result_dict
        assert "budget" in result_dict
        assert "estimate" in result_dict
        assert "passed_checks" in result_dict
        assert isinstance(result_dict["blockers"], list)

    def test_dict_preserves_values(self, guard, small_estimate):
        """Serialized dict preserves numerical values."""
        result = guard.check(small_estimate)
        result_dict = result.to_dict()

        assert result_dict["budget"]["human_labor_hours_remaining"] == 100.0
        assert result_dict["estimate"]["human_labor_hours"] == 5.0


class TestMultipleConstraints:
    """Test behavior when multiple constraints are tight."""

    def test_multiple_blockers(self, guard):
        """Multiple constraint violations produce multiple blockers."""
        estimate = ResourceEstimate(
            human_labor_hours=200.0,  # Over budget
            ai_tokens=600000,  # Over budget
            practices_affected=12,  # Over capacity
            escalations_required=3,  # Over SLA
        )
        result = guard.check(estimate)

        assert result.level == ResourceCheckLevel.INSUFFICIENT
        assert len(result.blockers) >= 2  # At least labor and tokens
