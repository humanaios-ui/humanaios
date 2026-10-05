"""Assess opportunities, claims, evidence, and verification before action."""

from typing import Any, Dict, List


def _text_list(value: Any, field: str) -> List[str]:
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        raise ValueError(f"{field} must be a list of non-empty strings")
    return [item.strip() for item in value]


def assess_system_stance(config: Dict[str, Any]) -> Dict[str, Any]:
    """Summarize opportunity claims and whether consequential action is ready."""
    if not isinstance(config, dict):
        raise ValueError("config must be an object")

    opportunities = config.get("opportunities", [])
    if not isinstance(opportunities, list):
        raise ValueError("opportunities must be a list")

    consequential_action = config.get("consequential_action", True)
    if not isinstance(consequential_action, bool):
        raise ValueError("consequential_action must be a boolean")

    minimum_confidence = config.get("minimum_confidence", 0.8)
    if (
        isinstance(minimum_confidence, bool)
        or not isinstance(minimum_confidence, (int, float))
        or not 0 <= minimum_confidence <= 1
    ):
        raise ValueError("minimum_confidence must be a number between 0 and 1")

    assessed_opportunities = []
    all_requirements = []
    confidences = []

    for index, opportunity in enumerate(opportunities):
        if not isinstance(opportunity, dict):
            raise ValueError(f"opportunities[{index}] must be an object")
        title = opportunity.get("title")
        if not isinstance(title, str) or not title.strip():
            raise ValueError(f"opportunities[{index}].title must be a non-empty string")
        description = opportunity.get("description", "")
        if not isinstance(description, str):
            raise ValueError(f"opportunities[{index}].description must be a string")
        propositions = opportunity.get("propositions", [])
        if not isinstance(propositions, list):
            raise ValueError(f"opportunities[{index}].propositions must be a list")

        opportunity_requirements = _text_list(
            opportunity.get("verification_requirements", []),
            f"opportunities[{index}].verification_requirements",
        )
        assessed_propositions = []
        if not propositions:
            opportunity_requirements.append(
                "State and assess at least one proposition about this opportunity."
            )

        for proposition_index, proposition in enumerate(propositions):
            field = f"opportunities[{index}].propositions[{proposition_index}]"
            if not isinstance(proposition, dict):
                raise ValueError(f"{field} must be an object")
            statement = proposition.get("statement")
            if not isinstance(statement, str) or not statement.strip():
                raise ValueError(f"{field}.statement must be a non-empty string")
            confidence = proposition.get("confidence", 0.5)
            if (
                isinstance(confidence, bool)
                or not isinstance(confidence, (int, float))
                or not 0 <= confidence <= 1
            ):
                raise ValueError(f"{field}.confidence must be a number between 0 and 1")

            supporting = _text_list(
                proposition.get("supporting_evidence", []),
                f"{field}.supporting_evidence",
            )
            contradicting = _text_list(
                proposition.get("contradicting_evidence", []),
                f"{field}.contradicting_evidence",
            )
            requirements = _text_list(
                proposition.get("verification_requirements", []),
                f"{field}.verification_requirements",
            )
            confidence = float(confidence)
            confidences.append(confidence)

            if not supporting:
                requirements.append(
                    f"Gather supporting evidence for: {statement.strip()}"
                )
            if contradicting:
                requirements.append(
                    f"Assess and resolve contradictory evidence for: {statement.strip()}"
                )
            if confidence < minimum_confidence:
                requirements.append(
                    f"Verify the confidence of this proposition reaches "
                    f"{minimum_confidence:.2f}: {statement.strip()}"
                )

            if supporting and contradicting:
                evidence_status = "contested"
            elif supporting:
                evidence_status = "supported"
            elif contradicting:
                evidence_status = "contradicted"
            else:
                evidence_status = "unverified"

            assessed_propositions.append({
                "statement": statement.strip(),
                "confidence": confidence,
                "evidence_status": evidence_status,
                "supporting_evidence": supporting,
                "contradicting_evidence": contradicting,
                "verification_requirements": requirements,
            })
            opportunity_requirements.extend(requirements)

        opportunity_requirements = list(dict.fromkeys(opportunity_requirements))
        all_requirements.extend(opportunity_requirements)
        assessed_opportunities.append({
            "title": title.strip(),
            "description": description.strip(),
            "propositions": assessed_propositions,
            "pre_action_requirements": opportunity_requirements,
        })

    if not opportunities:
        all_requirements.append("Identify and assess an opportunity before taking action.")

    all_requirements = list(dict.fromkeys(all_requirements))
    action_ready = bool(assessed_opportunities) and (
        not consequential_action or not all_requirements
    )
    return {
        "status": "pass" if action_ready else "fail",
        "consequential_action": consequential_action,
        "action_ready": action_ready,
        "overall_confidence": (
            sum(confidences) / len(confidences) if confidences else None
        ),
        "confidence_basis": (
            "reported per proposition; overall confidence is their unweighted mean"
        ),
        "opportunities": assessed_opportunities,
        "pre_action_requirements": all_requirements,
    }
