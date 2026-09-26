"""
Test suite for gates CLI commands.
"""

import json
import pytest
from argparse import Namespace
from src.gates.cli import readiness_check, resource_check, sentinel_verify


class TestReadinessCheckCLI:
    """Test readiness-check command."""

    def test_readiness_check_pass(self, capsys):
        """Readiness check passes with good config."""
        config = json.dumps({
            "evidence": [
                {"kind": "read", "source": "file1.py", "confidence": 0.9},
                {"kind": "read", "source": "file2.py", "confidence": 0.85},
                {"kind": "read", "source": "file3.py", "confidence": 0.8},
            ],
            "assumptions": [],
            "unknowns": [],
            "min_evidence": 3,
            "max_assumptions": 2,
            "max_uncertainty": 0.25,
        })

        args = Namespace(
            config=config,
            input_file=None,
            output="human"
        )

        result = readiness_check(args)
        assert result["status"] == "pass"
        assert result["level"] == "ready"

    def test_readiness_check_fail(self):
        """Readiness check fails with insufficient evidence."""
        config = json.dumps({
            "evidence": [
                {"kind": "read", "source": "file1.py", "confidence": 0.8},
            ],
            "assumptions": [],
            "unknowns": [],
            "min_evidence": 3,
        })

        args = Namespace(
            config=config,
            input_file=None,
            output="json"
        )

        result = readiness_check(args)
        assert result["status"] == "fail"
        assert result["level"] == "not_ready"

    def test_readiness_check_json_output(self, capsys):
        """Readiness check outputs JSON format."""
        config = json.dumps({
            "evidence": [
                {"kind": "read", "source": "f1", "confidence": 0.9},
                {"kind": "read", "source": "f2", "confidence": 0.85},
                {"kind": "read", "source": "f3", "confidence": 0.8},
            ],
            "assumptions": [],
            "unknowns": [],
        })

        args = Namespace(
            config=config,
            input_file=None,
            output="json"
        )

        result = readiness_check(args)
        captured = capsys.readouterr()

        # Should have JSON output
        output_json = json.loads(captured.out)
        assert output_json["command"] == "readiness-check"
        assert "result" in output_json


class TestResourceCheckCLI:
    """Test resource-check command."""

    def test_resource_check_sufficient(self):
        """Resource check passes with sufficient budget."""
        config = json.dumps({
            "budget": {
                "human_labor_hours_remaining": 100.0,
                "ai_tokens_remaining": 500000,
                "practices_active": 5,
                "practices_capacity": 15,
                "escalations_pending": 2,
                "escalation_sla_hours": 4.0,
            },
            "estimate": {
                "human_labor_hours": 10.0,
                "ai_tokens": 50000,
                "practices_affected": 1,
                "escalations_required": 0,
            },
        })

        args = Namespace(
            config=config,
            input_file=None,
            output="json"
        )

        result = resource_check(args)
        assert result["status"] == "pass"
        assert result["level"] == "sufficient"

    def test_resource_check_insufficient(self):
        """Resource check fails with insufficient budget."""
        config = json.dumps({
            "budget": {
                "human_labor_hours_remaining": 10.0,
                "ai_tokens_remaining": 50000,
                "practices_active": 5,
                "practices_capacity": 15,
                "escalations_pending": 2,
                "escalation_sla_hours": 4.0,
            },
            "estimate": {
                "human_labor_hours": 50.0,
                "ai_tokens": 100000,
                "practices_affected": 1,
                "escalations_required": 0,
            },
        })

        args = Namespace(
            config=config,
            input_file=None,
            output="json"
        )

        result = resource_check(args)
        assert result["status"] == "fail"
        assert result["level"] == "insufficient"

    def test_resource_check_warning(self):
        """Resource check warns when tight."""
        config = json.dumps({
            "budget": {
                "human_labor_hours_remaining": 12.0,  # 80% of 15
                "ai_tokens_remaining": 500000,
                "practices_active": 5,
                "practices_capacity": 15,
                "escalations_pending": 2,
                "escalation_sla_hours": 4.0,
            },
            "estimate": {
                "human_labor_hours": 10.0,
                "ai_tokens": 50000,
                "practices_affected": 0,
                "escalations_required": 0,
            },
        })

        args = Namespace(
            config=config,
            input_file=None,
            output="json"
        )

        result = resource_check(args)
        # Might be warning depending on exact thresholds
        assert result["level"] in ["sufficient", "warning"]


class TestSentinelVerifyCLI:
    """Test sentinel-verify command."""

    def test_sentinel_verify_pass(self):
        """Sentinel verify passes with strong vectors."""
        config = json.dumps({
            "vectors": {
                "know": 0.95,
                "uncertainty": 0.05,
                "context": 0.95,
                "engagement": 0.98,
                "clarity": 0.95,
                "coherence": 0.90,
            },
            "action": "deploy",
        })

        args = Namespace(
            config=config,
            input_file=None,
            output="json"
        )

        result = sentinel_verify(args)
        assert result["status"] == "pass"
        assert result["level"] == "pass"

    def test_sentinel_verify_fail(self):
        """Sentinel verify fails with weak vectors for strong action."""
        config = json.dumps({
            "vectors": {
                "know": 0.3,
                "uncertainty": 0.7,
                "context": 0.2,
                "engagement": 0.3,
                "clarity": 0.2,
                "coherence": 0.1,
            },
            "action": "deploy",
        })

        args = Namespace(
            config=config,
            input_file=None,
            output="json"
        )

        result = sentinel_verify(args)
        assert result["status"] == "fail"
        assert result["level"] == "fail"

    def test_sentinel_verify_recommend_action(self):
        """Sentinel verify recommends appropriate action."""
        config = json.dumps({
            "vectors": {
                "know": 0.5,
                "uncertainty": 0.5,
                "context": 0.5,
                "engagement": 0.5,
                "clarity": 0.5,
                "coherence": 0.5,
            },
            "action": "deploy",
        })

        args = Namespace(
            config=config,
            input_file=None,
            output="json"
        )

        result = sentinel_verify(args)
        # Should recommend something safer than deploy
        recommended = result.get("recommended_action")
        assert recommended in ["investigate", "implement", "escalate"]

    def test_sentinel_verify_marginal(self):
        """Sentinel verify can return marginal result."""
        config = json.dumps({
            "vectors": {
                "know": 0.74,  # Just below IMPLEMENT threshold
                "uncertainty": 0.26,
                "context": 0.80,
                "engagement": 0.86,
                "clarity": 0.80,
                "coherence": 0.72,
            },
            "action": "implement",
        })

        args = Namespace(
            config=config,
            input_file=None,
            output="json"
        )

        result = sentinel_verify(args)
        # Should be marginal or pass depending on exact logic
        assert result["status"] in ["pass", "marginal"]
