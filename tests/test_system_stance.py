import pytest
from argparse import Namespace

from src.gates.system_stance import assess_system_stance
from src.gates.cli import system_stance


def test_reports_opportunities_evidence_and_confidence():
    result = assess_system_stance({
        "opportunities": [{
            "title": "Pilot a new service",
            "description": "Test demand in one region.",
            "propositions": [{
                "statement": "Customers want the service.",
                "confidence": 0.7,
                "supporting_evidence": ["Three customers requested it."],
                "contradicting_evidence": ["Survey response rate was low."],
            }],
        }],
    })

    proposition = result["opportunities"][0]["propositions"][0]
    assert result["overall_confidence"] == 0.7
    assert proposition["evidence_status"] == "contested"
    assert proposition["supporting_evidence"] == ["Three customers requested it."]
    assert proposition["contradicting_evidence"] == ["Survey response rate was low."]
    assert not result["action_ready"]
    assert any("resolve contradictory evidence" in item for item in result["pre_action_requirements"])
    assert any("reaches 0.80" in item for item in result["pre_action_requirements"])


def test_consequential_action_waits_for_explicit_verification():
    result = assess_system_stance({
        "opportunities": [{
            "title": "Pilot a new service",
            "propositions": [{
                "statement": "The pilot is legally permitted.",
                "confidence": 0.95,
                "supporting_evidence": ["Counsel's written review."],
                "verification_requirements": ["Confirm local permits are current."],
            }],
        }],
    })

    assert result["status"] == "fail"
    assert result["pre_action_requirements"] == ["Confirm local permits are current."]


def test_nonconsequential_action_can_proceed_while_showing_open_checks():
    result = assess_system_stance({
        "consequential_action": False,
        "opportunities": [{
            "title": "Explore a new service",
            "propositions": [{
                "statement": "The service may be useful.",
                "supporting_evidence": ["One exploratory interview."],
            }],
        }],
    })

    assert result["status"] == "pass"
    assert result["action_ready"]
    assert result["pre_action_requirements"]


def test_no_opportunities_does_not_authorize_consequential_action():
    result = assess_system_stance({"opportunities": []})

    assert not result["action_ready"]
    assert result["overall_confidence"] is None
    assert result["pre_action_requirements"] == [
        "Identify and assess an opportunity before taking action."
    ]


def test_cli_emits_json_stance_report(capsys):
    result = system_stance(Namespace(
        config=(
            '{"opportunities":[{"title":"Pilot","propositions":[{'
            '"statement":"Demand exists","confidence":0.9,'
            '"supporting_evidence":["Customer interview"]}]}]}'
        ),
        input_file=None,
        output="json",
    ))

    output = capsys.readouterr().out
    assert '"command": "system-stance"' in output
    assert result["opportunities"][0]["propositions"][0]["statement"] == "Demand exists"


@pytest.mark.parametrize("confidence", [-0.1, 1.1, True])
def test_rejects_invalid_confidence(confidence):
    with pytest.raises(ValueError, match="confidence"):
        assess_system_stance({
            "opportunities": [{
                "title": "Opportunity",
                "propositions": [{
                    "statement": "A claim.",
                    "confidence": confidence,
                }],
            }],
        })
