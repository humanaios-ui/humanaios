"""
CLI commands for Sentinel validation gates.

Three commands available:
  - readiness-check: Verify noetic phase completion
  - resource-check: Validate resource allocation
  - sentinel-verify: Check epistemic vectors for action
  - system-stance: Summarize opportunities and pre-action requirements
"""

import json
import sys
from typing import Optional, Dict, Any
from argparse import ArgumentParser, Namespace

from .readiness_gates import ReadinessGate, ReadinessLevel
from .resource_guard import ResourceGuard, ResourceBudget, ResourceEstimate, ResourceCheckLevel
from .sentinel_verify import SentinelGate, ActionType, EpistemicVectors, VectorLevel
from .system_stance import assess_system_stance


def readiness_check(args: Namespace) -> Dict[str, Any]:
    """
    CLI: readiness-check

    Verify that noetic work is complete before moving to praxic.
    Reads from session state or accepts JSON config.
    """
    gate = ReadinessGate()

    # Load evidence from input or stdin
    if args.input_file:
        with open(args.input_file, "r") as f:
            config = json.load(f)
    elif args.config:
        config = json.loads(args.config)
    else:
        # Read from stdin
        config = json.load(sys.stdin)

    # Populate gate from config
    for ev in config.get("evidence", []):
        gate.log_evidence(
            kind=ev["kind"],
            source=ev["source"],
            confidence=ev.get("confidence", 0.7),
            notes=ev.get("notes", "")
        )

    for assumption in config.get("assumptions", []):
        gate.add_assumption(assumption["text"], assumption.get("confidence", 0.5))

    for unknown in config.get("unknowns", []):
        gate.add_unknown(unknown)

    # Evaluate
    result = gate.evaluate(
        min_evidence_items=config.get("min_evidence", 3),
        max_undocumented_assumptions=config.get("max_assumptions", 2),
        max_uncertainty=config.get("max_uncertainty", 0.25)
    )

    output = {
        "command": "readiness-check",
        "status": "pass" if result.level == ReadinessLevel.READY else "fail",
        "level": result.level.value,
        "result": result.to_dict(),
    }

    if args.output == "json":
        print(json.dumps(output, indent=2))
    else:
        print(f"Readiness: {result.level.value}")
        print(f"  Evidence: {result.evidence_gathered}/{result.evidence_required}")
        print(f"  Assumptions: {result.assumptions_undocumented}")
        print(f"  Uncertainty: {result.uncertainty_level:.2f}")
        if result.blockers:
            print(f"  Blockers: {'; '.join(result.blockers)}")
        if result.recommendations:
            print(f"  Recommendations: {'; '.join(result.recommendations)}")

    return output


def resource_check(args: Namespace) -> Dict[str, Any]:
    """
    CLI: resource-check

    Validate that proposed work fits within resource constraints.
    Reads budget and estimate from JSON config.
    """
    if args.input_file:
        with open(args.input_file, "r") as f:
            config = json.load(f)
    elif args.config:
        config = json.loads(args.config)
    else:
        config = json.load(sys.stdin)

    # Build budget
    budget_cfg = config.get("budget", {})
    budget = ResourceBudget(
        human_labor_hours_remaining=budget_cfg.get("human_labor_hours_remaining", 100.0),
        ai_tokens_remaining=budget_cfg.get("ai_tokens_remaining", 500000),
        practices_active=budget_cfg.get("practices_active", 5),
        practices_capacity=budget_cfg.get("practices_capacity", 15),
        escalations_pending=budget_cfg.get("escalations_pending", 2),
        escalation_sla_hours=budget_cfg.get("escalation_sla_hours", 4.0),
    )

    # Build estimate
    estimate_cfg = config.get("estimate", {})
    estimate = ResourceEstimate(
        human_labor_hours=estimate_cfg.get("human_labor_hours", 5.0),
        ai_tokens=estimate_cfg.get("ai_tokens", 50000),
        practices_affected=estimate_cfg.get("practices_affected", 1),
        escalations_required=estimate_cfg.get("escalations_required", 0),
    )

    # Check
    guard = ResourceGuard(budget)
    result = guard.check(estimate)

    output = {
        "command": "resource-check",
        "status": "pass" if result.level == ResourceCheckLevel.SUFFICIENT else
                  "warning" if result.level == ResourceCheckLevel.WARNING else "fail",
        "level": result.level.value,
        "result": result.to_dict(),
    }

    if args.output == "json":
        print(json.dumps(output, indent=2))
    else:
        print(f"Resource Check: {result.level.value}")
        print(f"  Labor: {estimate.human_labor_hours:.1f}h / {budget.human_labor_hours_remaining:.1f}h")
        print(f"  Tokens: {estimate.ai_tokens} / {budget.ai_tokens_remaining}")
        print(f"  Practices: {budget.practices_active} + {estimate.practices_affected} / {budget.practices_capacity}")
        if result.blockers:
            print(f"  BLOCKERS: {'; '.join(result.blockers)}")
        if result.warnings:
            print(f"  Warnings: {'; '.join(result.warnings)}")

    return output


def sentinel_verify(args: Namespace) -> Dict[str, Any]:
    """
    CLI: sentinel-verify

    Verify epistemic vector state is sufficient for the proposed action.
    Reads vectors and action type from JSON config.
    """
    if args.input_file:
        with open(args.input_file, "r") as f:
            config = json.load(f)
    elif args.config:
        config = json.loads(args.config)
    else:
        config = json.load(sys.stdin)

    # Build vectors
    vectors_cfg = config.get("vectors", {})
    vectors = EpistemicVectors(
        know=vectors_cfg.get("know", 0.5),
        uncertainty=vectors_cfg.get("uncertainty", 0.5),
        context=vectors_cfg.get("context", 0.5),
        engagement=vectors_cfg.get("engagement", 0.5),
        clarity=vectors_cfg.get("clarity", 0.5),
        coherence=vectors_cfg.get("coherence", 0.5),
    )

    # Get action type
    action_str = config.get("action", "investigate")
    action = ActionType(action_str)

    # Verify
    gate = SentinelGate()
    result = gate.verify(vectors, action)

    output = {
        "command": "sentinel-verify",
        "status": "pass" if result.level == VectorLevel.PASS else
                  "marginal" if result.level == VectorLevel.MARGINAL else "fail",
        "level": result.level.value,
        "recommended_action": gate.recommend_action(vectors).value,
        "result": result.to_dict(),
    }

    if args.output == "json":
        print(json.dumps(output, indent=2))
    else:
        print(f"Sentinel Verify ({action.value}): {result.level.value}")
        print(f"  Vectors: know={vectors.know:.2f}, uncertainty={vectors.uncertainty:.2f}, "
              f"context={vectors.context:.2f}, engagement={vectors.engagement:.2f}")
        print(f"  Recommended action: {gate.recommend_action(vectors).value}")
        if result.passed_checks:
            print(f"  ✓ {len(result.passed_checks)} checks passed")
        if result.marginal_checks:
            print(f"  ⚠ {len(result.marginal_checks)} checks marginal")
        if result.failed_checks:
            print(f"  ✗ {len(result.failed_checks)} checks FAILED")
            for check in result.failed_checks[:3]:
                print(f"     - {check}")

    return output


def system_stance(args: Namespace) -> Dict[str, Any]:
    """CLI: summarize opportunities, evidence, confidence, and pre-action checks."""
    if args.input_file:
        with open(args.input_file, "r") as f:
            config = json.load(f)
    elif args.config:
        config = json.loads(args.config)
    else:
        config = json.load(sys.stdin)

    result = assess_system_stance(config)
    output = {"command": "system-stance", **result}
    if args.output == "json":
        print(json.dumps(output, indent=2))
    else:
        print(f"System stance: {'ready' if result['action_ready'] else 'not ready'}")
        for opportunity in result["opportunities"]:
            print(f"  Opportunity: {opportunity['title']}")
            if opportunity["description"]:
                print(f"    {opportunity['description']}")
            for proposition in opportunity["propositions"]:
                print(
                    f"    Proposition ({proposition['evidence_status']}, "
                    f"confidence {proposition['confidence']:.2f}): "
                    f"{proposition['statement']}"
                )
                for evidence in proposition["supporting_evidence"]:
                    print(f"      Supports: {evidence}")
                for evidence in proposition["contradicting_evidence"]:
                    print(f"      Contradicts: {evidence}")
        if result["pre_action_requirements"]:
            print("  Verify before consequential action:")
            for requirement in result["pre_action_requirements"]:
                print(f"    - {requirement}")
    return output


def main():
    """Main CLI entry point."""
    parser = ArgumentParser(description="Sentinel validation gates for transaction discipline")
    subparsers = parser.add_subparsers(dest="command", help="Gate command to run")

    # readiness-check
    readiness_parser = subparsers.add_parser("readiness-check", help="Verify noetic phase complete")
    readiness_parser.add_argument("--config", help="JSON config string")
    readiness_parser.add_argument("--input-file", "-i", help="Input JSON file")
    readiness_parser.add_argument("--output", "-o", choices=["json", "human"], default="human")
    readiness_parser.set_defaults(func=readiness_check)

    # resource-check
    resource_parser = subparsers.add_parser("resource-check", help="Validate resource allocation")
    resource_parser.add_argument("--config", help="JSON config string")
    resource_parser.add_argument("--input-file", "-i", help="Input JSON file")
    resource_parser.add_argument("--output", "-o", choices=["json", "human"], default="human")
    resource_parser.set_defaults(func=resource_check)

    # sentinel-verify
    sentinel_parser = subparsers.add_parser("sentinel-verify", help="Check epistemic vectors")
    sentinel_parser.add_argument("--config", help="JSON config string")
    sentinel_parser.add_argument("--input-file", "-i", help="Input JSON file")
    sentinel_parser.add_argument("--output", "-o", choices=["json", "human"], default="human")
    sentinel_parser.set_defaults(func=sentinel_verify)

    # system-stance
    stance_parser = subparsers.add_parser(
        "system-stance",
        help="Assess opportunities, propositions, evidence, and pre-action requirements",
    )
    stance_parser.add_argument("--config", help="JSON config string")
    stance_parser.add_argument("--input-file", "-i", help="Input JSON file")
    stance_parser.add_argument("--output", "-o", choices=["json", "human"], default="human")
    stance_parser.set_defaults(func=system_stance)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        result = args.func(args)
        # Exit with appropriate code
        status = result.get("status", "fail")
        if status == "pass":
            sys.exit(0)
        elif status == "warning":
            sys.exit(1)  # Warning treated as failure for gate purposes
        else:
            sys.exit(2)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
