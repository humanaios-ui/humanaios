"""
Test suite for Sentinel verification gates.
"""

import pytest
from src.gates.sentinel_verify import (
    SentinelGate,
    ActionType,
    EpistemicVectors,
    VectorLevel,
)


@pytest.fixture
def gate():
    """Create a Sentinel verification gate."""
    return SentinelGate()


@pytest.fixture
def strong_vectors():
    """Strong epistemic state suitable for deployment."""
    return EpistemicVectors(
        know=0.95,
        uncertainty=0.05,
        context=0.95,
        engagement=0.98,
        clarity=0.95,
        coherence=0.90,
    )


@pytest.fixture
def weak_vectors():
    """Weak epistemic state suitable only for investigation."""
    return EpistemicVectors(
        know=0.3,
        uncertainty=0.7,
        context=0.2,
        engagement=0.3,
        clarity=0.2,
        coherence=0.1,
    )


@pytest.fixture
def moderate_vectors():
    """Moderate epistemic state suitable for implementation."""
    return EpistemicVectors(
        know=0.78,
        uncertainty=0.22,
        context=0.82,
        engagement=0.87,
        clarity=0.81,
        coherence=0.72,
    )


class TestInvestigateThresholds:
    """Test INVESTIGATE action thresholds (most permissive)."""

    def test_investigate_weak_vectors(self, gate, weak_vectors):
        """Investigate succeeds with weak vectors."""
        result = gate.verify(weak_vectors, ActionType.INVESTIGATE)
        # Investigate has lowest thresholds
        assert result.level in [VectorLevel.PASS, VectorLevel.MARGINAL]

    def test_investigate_strong_vectors(self, gate, strong_vectors):
        """Investigate succeeds with strong vectors."""
        result = gate.verify(strong_vectors, ActionType.INVESTIGATE)
        assert result.level == VectorLevel.PASS
        assert len(result.passed_checks) > 0


class TestImplementThresholds:
    """Test IMPLEMENT action thresholds."""

    def test_implement_moderate_vectors(self, gate, moderate_vectors):
        """Implement succeeds with moderate vectors."""
        result = gate.verify(moderate_vectors, ActionType.IMPLEMENT)
        assert result.level in [VectorLevel.PASS, VectorLevel.MARGINAL]

    def test_implement_weak_vectors(self, gate, weak_vectors):
        """Implement fails with weak vectors."""
        result = gate.verify(weak_vectors, ActionType.IMPLEMENT)
        assert result.level == VectorLevel.FAIL
        assert len(result.failed_checks) > 0

    def test_implement_strong_vectors(self, gate, strong_vectors):
        """Implement succeeds with strong vectors."""
        result = gate.verify(strong_vectors, ActionType.IMPLEMENT)
        assert result.level == VectorLevel.PASS


class TestDeployThresholds:
    """Test DEPLOY action thresholds (most stringent)."""

    def test_deploy_strong_vectors(self, gate, strong_vectors):
        """Deploy succeeds with strong vectors."""
        result = gate.verify(strong_vectors, ActionType.DEPLOY)
        assert result.level == VectorLevel.PASS

    def test_deploy_moderate_vectors(self, gate, moderate_vectors):
        """Deploy fails with moderate vectors."""
        result = gate.verify(moderate_vectors, ActionType.DEPLOY)
        assert result.level == VectorLevel.FAIL

    def test_deploy_weak_vectors(self, gate, weak_vectors):
        """Deploy fails with weak vectors."""
        result = gate.verify(weak_vectors, ActionType.DEPLOY)
        assert result.level == VectorLevel.FAIL
        assert any("high" in r.lower() or "cannot" in r.lower() for r in result.recommendations)


class TestPublishThresholds:
    """Test PUBLISH action thresholds."""

    def test_publish_strong_vectors(self, gate, strong_vectors):
        """Publish succeeds with strong vectors."""
        result = gate.verify(strong_vectors, ActionType.PUBLISH)
        assert result.level == VectorLevel.PASS

    def test_publish_weak_coherence(self, gate):
        """Publish fails if coherence is low despite other vectors."""
        vectors = EpistemicVectors(
            know=0.90,
            uncertainty=0.10,
            context=0.90,
            engagement=0.92,
            clarity=0.90,
            coherence=0.60,  # Too low for publish
        )
        result = gate.verify(vectors, ActionType.PUBLISH)
        assert result.level == VectorLevel.FAIL
        assert any("coherence" in check.lower() for check in result.failed_checks)


class TestEscalateThresholds:
    """Test ESCALATE action (high urgency, low knowledge OK)."""

    def test_escalate_high_urgency(self, gate):
        """Escalate succeeds if engagement/urgency is high."""
        vectors = EpistemicVectors(
            know=0.4,
            uncertainty=0.6,  # High uncertainty OK for escalation
            context=0.5,
            engagement=0.98,  # High urgency
            clarity=0.5,
            coherence=0.4,
        )
        result = gate.verify(vectors, ActionType.ESCALATE)
        # Should pass or be marginal (high urgency compensates)
        assert result.level in [VectorLevel.PASS, VectorLevel.MARGINAL]

    def test_escalate_low_urgency(self, gate, weak_vectors):
        """Escalate fails without high urgency."""
        # Weak vectors have low engagement
        result = gate.verify(weak_vectors, ActionType.ESCALATE)
        assert result.level == VectorLevel.FAIL


class TestMarginalReadiness:
    """Test MARGINAL readiness (within 10% of threshold)."""

    def test_marginal_just_below_threshold(self, gate):
        """Marginal when just below threshold."""
        vectors = EpistemicVectors(
            know=0.74,  # 0.75 * 0.9 = 0.675, so 0.74 is marginal
            uncertainty=0.26,  # Threshold 0.25, so this is marginal
            context=0.80,
            engagement=0.86,
            clarity=0.80,
            coherence=0.72,
        )
        result = gate.verify(vectors, ActionType.IMPLEMENT)
        assert result.level == VectorLevel.MARGINAL
        assert len(result.marginal_checks) > 0


class TestRecommendedAction:
    """Test action recommendation based on vectors."""

    def test_recommend_deploy_for_strong(self, gate, strong_vectors):
        """Recommend DEPLOY for strong vectors."""
        action = gate.recommend_action(strong_vectors)
        assert action == ActionType.DEPLOY

    def test_recommend_implement_for_moderate(self, gate, moderate_vectors):
        """Recommend IMPLEMENT for moderate vectors."""
        action = gate.recommend_action(moderate_vectors)
        assert action in [ActionType.IMPLEMENT, ActionType.DEPLOY]

    def test_recommend_investigate_for_weak(self, gate, weak_vectors):
        """Recommend INVESTIGATE for weak vectors."""
        action = gate.recommend_action(weak_vectors)
        assert action == ActionType.INVESTIGATE

    def test_always_investigatable(self, gate):
        """Any vectors can at least investigate."""
        # Create extremely weak vectors
        terrible = EpistemicVectors(
            know=0.1, uncertainty=0.9, context=0.1,
            engagement=0.1, clarity=0.1, coherence=0.0
        )
        action = gate.recommend_action(terrible)
        # Should always recommend investigate as fallback
        assert action == ActionType.INVESTIGATE


class TestVectorBalance:
    """Test interaction between vectors."""

    def test_high_know_compensates_uncertainty(self, gate):
        """High 'know' helps offset high 'uncertainty'."""
        vectors = EpistemicVectors(
            know=0.85,
            uncertainty=0.40,  # Higher than threshold for IMPLEMENT
            context=0.80,
            engagement=0.85,
            clarity=0.80,
            coherence=0.75,
        )
        result = gate.verify(vectors, ActionType.IMPLEMENT)
        # High know doesn't fully compensate, should fail
        assert result.level == VectorLevel.FAIL

    def test_low_engagement_blocks_action(self, gate):
        """Low engagement blocks most actions."""
        vectors = EpistemicVectors(
            know=0.90,
            uncertainty=0.05,
            context=0.90,
            engagement=0.60,  # Below IMPLEMENT threshold
            clarity=0.90,
            coherence=0.85,
        )
        result = gate.verify(vectors, ActionType.IMPLEMENT)
        assert result.level == VectorLevel.FAIL


class TestSerialization:
    """Test result serialization."""

    def test_result_to_dict(self, gate, strong_vectors):
        """Serialize result to dictionary."""
        result = gate.verify(strong_vectors, ActionType.DEPLOY)
        result_dict = result.to_dict()

        assert "level" in result_dict
        assert "vectors" in result_dict
        assert "thresholds" in result_dict
        assert "passed_checks" in result_dict
        assert result_dict["level"] == "pass"

    def test_dict_preserves_vector_values(self, gate, strong_vectors):
        """Serialized dict preserves vector values."""
        result = gate.verify(strong_vectors, ActionType.DEPLOY)
        result_dict = result.to_dict()

        assert result_dict["vectors"]["know"] == 0.95
        assert result_dict["vectors"]["engagement"] == 0.98
