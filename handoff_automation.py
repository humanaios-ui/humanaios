#!/usr/bin/env python3
"""
Resource-Miner Integration Handoff Automation

Implements automatic triggers for the 5-part pipeline protocol:
1. Miner → Aggregator (Resource Batch)
2. Aggregator → Miner (Ranking Feedback)
3. Optimizer → Miner (Deployment Results)
4. Miner → Evaluator (System Metrics)
5. Evaluator → Miner (Orchestration Guidance)

Usage:
  from handoff_automation import HandoffTrigger, validate_resource_batch

  # Miner sends resource batch to aggregator
  batch = load_json('RESOURCE_CATALOG.json')
  if validate_resource_batch(batch):
    HandoffTrigger.send_batch_to_aggregator(batch)
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class HandoffMessage:
    """Represents a handoff message between practices"""
    source: str  # canonical AI ID
    target: str  # canonical AI ID
    message_type: str  # batch|feedback|results|metrics|guidance
    timestamp: str
    content: Dict

    def to_json(self) -> str:
        return json.dumps({
            'source': self.source,
            'target': self.target,
            'type': self.message_type,
            'timestamp': self.timestamp,
            'content': self.content
        }, indent=2)


class HandoffValidator:
    """Validates messages against specification schemas"""

    @staticmethod
    def validate_resource_batch(batch: Dict) -> bool:
        """Validate miner resource batch before sending to aggregator"""
        required_fields = [
            'resources',  # Array of resource objects
            'metadata'    # Includes discovery_date, total_resources, tiers
        ]

        # Check top-level structure
        if not all(field in batch for field in required_fields):
            print(f"✗ Missing required fields: {required_fields}")
            return False

        # Check each resource has required properties
        required_resource_props = [
            'id', 'name', 'type', 'impact', 'feasibility',
            'strategic_fit', 'cost_tokens', 'tier', 'verification_status'
        ]

        for resource in batch.get('resources', []):
            if not all(prop in resource for prop in required_resource_props):
                print(f"✗ Resource {resource.get('id')} missing properties")
                return False

        print(f"✓ Resource batch valid: {len(batch['resources'])} resources")
        return True

    @staticmethod
    def validate_ranked_opportunities(ranked: Dict) -> bool:
        """Validate aggregator ranking feedback"""
        required = [
            'ranking_batch_id',
            'timestamp',
            'resources_received',
            'opportunities_ranked',
            'ranking_method',
            'top_5_opportunities'  # At least top 5 listed
        ]

        if not all(field in ranked for field in required):
            print(f"✗ Ranking feedback missing required fields")
            return False

        if len(ranked['top_5_opportunities']) < 5:
            print(f"✗ Must include top 5 opportunities (got {len(ranked['top_5_opportunities'])})")
            return False

        print(f"✓ Ranked opportunities valid: {ranked['opportunities_ranked']} ranked")
        return True

    @staticmethod
    def validate_deployment_results(results: Dict) -> bool:
        """Validate optimizer deployment results"""
        required = [
            'deployment_batch_id',
            'timestamp',
            'opportunities_deployed',
            'opportunities_successful',
            'opportunities_failed',
            'results'  # Per-opportunity status
        ]

        if not all(field in results for field in required):
            print(f"✗ Deployment results missing required fields")
            return False

        # Check results structure
        for opp_id, result in results['results'].items():
            if 'status' not in result or 'outcome' not in result:
                print(f"✗ Opportunity {opp_id} missing status/outcome")
                return False

        print(f"✓ Deployment results valid: {results['opportunities_deployed']} deployed")
        return True

    @staticmethod
    def validate_metrics_report(metrics: Dict) -> bool:
        """Validate miner system metrics report to evaluator"""
        required_phases = [
            'extraction',
            'conversion',
            'utilization',
            'realization'
        ]

        if not all(phase in metrics for phase in required_phases):
            print(f"✗ Metrics missing phases: {required_phases}")
            return False

        print(f"✓ Metrics report valid: {len(metrics.get('next_priorities', []))} priorities")
        return True


class HandoffTrigger:
    """Implements automatic handoff sending between practices"""

    CANONICAL_SEATS = {
        'miner': 'empirica-foundation.carly.empirica-resource-miner',
        'aggregator': 'empirica-foundation.carly.opportunity-aggregator',
        'optimizer': 'empirica-foundation.carly.local-machine-optimizer',
        'evaluator': 'empirica-foundation.carly.empirica-foundation-evaluator'
    }

    @staticmethod
    def send_batch_to_aggregator(batch: Dict) -> bool:
        """
        Handoff 1: Miner → Aggregator
        Send discovered resources for ranking
        """
        if not HandoffValidator.validate_resource_batch(batch):
            return False

        message = HandoffMessage(
            source=HandoffTrigger.CANONICAL_SEATS['miner'],
            target=HandoffTrigger.CANONICAL_SEATS['aggregator'],
            message_type='batch',
            timestamp=datetime.now().isoformat(),
            content={
                'batch_id': f"MINER_{datetime.now().strftime('%Y%m%d_%H%M')}",
                'resources_discovered': len(batch['resources']),
                'ledger_path': 'RESOURCE_CATALOG.json',
                'ready_for_ranking': True
            }
        )

        # Send via cortex_collab
        cmd = f"""empirica mailbox reply \\
          --parent-id "prop_miner_batch_notification" \\
          --summary "{message.to_json()}" \\
          --result "shipped"
        """

        print(f"→ Sending resource batch to aggregator ({len(batch['resources'])} resources)")
        return _execute_handoff(cmd)

    @staticmethod
    def send_ranking_feedback_to_miner(ranked: Dict) -> bool:
        """
        Handoff 2: Aggregator → Miner
        Send ranked opportunities feedback
        """
        if not HandoffValidator.validate_ranked_opportunities(ranked):
            return False

        message = HandoffMessage(
            source=HandoffTrigger.CANONICAL_SEATS['aggregator'],
            target=HandoffTrigger.CANONICAL_SEATS['miner'],
            message_type='feedback',
            timestamp=datetime.now().isoformat(),
            content={
                'ranking_batch_id': ranked['ranking_batch_id'],
                'opportunities_ranked': ranked['opportunities_ranked'],
                'top_opportunities': ranked['top_5_opportunities'],
                'quality_feedback': 'valid'
            }
        )

        print(f"→ Sending ranking feedback to miner ({ranked['opportunities_ranked']} opportunities)")
        return _execute_handoff(f"cortex_collab '{message.to_json()}'")

    @staticmethod
    def send_deployment_results_to_miner(results: Dict) -> bool:
        """
        Handoff 3: Optimizer → Miner
        Send deployment results and feedback
        """
        if not HandoffValidator.validate_deployment_results(results):
            return False

        message = HandoffMessage(
            source=HandoffTrigger.CANONICAL_SEATS['optimizer'],
            target=HandoffTrigger.CANONICAL_SEATS['miner'],
            message_type='results',
            timestamp=datetime.now().isoformat(),
            content={
                'deployment_batch_id': results['deployment_batch_id'],
                'successful': results['opportunities_successful'],
                'failed': results['opportunities_failed'],
                'success_rate': f"{100 * results['opportunities_successful'] / results['opportunities_deployed']:.0f}%"
            }
        )

        print(f"→ Sending deployment results to miner ({results['opportunities_successful']}/{results['opportunities_deployed']} successful)")
        return _execute_handoff(f"cortex_propose '{message.to_json()}'")

    @staticmethod
    def send_metrics_to_evaluator(metrics: Dict) -> bool:
        """
        Handoff 4: Miner → Evaluator
        Send system metrics report
        """
        if not HandoffValidator.validate_metrics_report(metrics):
            return False

        message = HandoffMessage(
            source=HandoffTrigger.CANONICAL_SEATS['miner'],
            target=HandoffTrigger.CANONICAL_SEATS['evaluator'],
            message_type='metrics',
            timestamp=datetime.now().isoformat(),
            content={
                'extraction_rate': metrics.get('extraction', {}).get('efficiency'),
                'conversion_rate': metrics.get('conversion', {}).get('conversion_rate'),
                'utilization_rate': metrics.get('utilization', {}).get('success_rate'),
                'estimated_roi': metrics.get('realization', {}).get('estimated_roi')
            }
        )

        print(f"→ Sending metrics to evaluator (estimated ROI: {metrics.get('realization', {}).get('estimated_roi')})")
        return _execute_handoff(f"cortex_propose '{message.to_json()}'")

    @staticmethod
    def send_guidance_to_miner(guidance: Dict) -> bool:
        """
        Handoff 5: Evaluator → Miner
        Send orchestration guidance for next cycle
        """
        message = HandoffMessage(
            source=HandoffTrigger.CANONICAL_SEATS['evaluator'],
            target=HandoffTrigger.CANONICAL_SEATS['miner'],
            message_type='guidance',
            timestamp=datetime.now().isoformat(),
            content={
                'next_cycle_priorities': guidance.get('next_cycle_focus', {}),
                'strategic_adjustments': guidance.get('strategic_adjustments', {})
            }
        )

        print(f"→ Sending guidance to miner ({len(guidance.get('next_cycle_focus', {}))} priorities)")
        return _execute_handoff(f"cortex_collab '{message.to_json()}'")


class HandoffMonitor:
    """Monitors handoff pipeline for delays and issues"""

    @staticmethod
    def check_handoff_health() -> Dict:
        """Check status of all handoffs in pipeline"""
        return {
            'timestamp': datetime.now().isoformat(),
            'handoffs': {
                'miner_to_aggregator': {'status': 'unknown', 'last_seen': None},
                'aggregator_to_miner': {'status': 'unknown', 'last_seen': None},
                'optimizer_to_miner': {'status': 'unknown', 'last_seen': None},
                'miner_to_evaluator': {'status': 'unknown', 'last_seen': None},
                'evaluator_to_miner': {'status': 'unknown', 'last_seen': None}
            }
        }

    @staticmethod
    def alert_on_delay(handoff_id: str, max_wait_seconds: int = 3600) -> bool:
        """Alert if handoff takes too long"""
        health = HandoffMonitor.check_handoff_health()
        # Implementation: check cortex mailbox for stalled handoffs
        # If delay > max_wait_seconds, trigger alert
        return True


def _execute_handoff(cmd: str) -> bool:
    """Execute cortex command for sending handoff"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except Exception as e:
        print(f"✗ Handoff execution failed: {e}")
        return False


# ============================================================================
# Example usage (for testing)
# ============================================================================

if __name__ == '__main__':
    print("Resource-Miner Integration Handoff Automation")
    print("=" * 60)
    print("")
    print("Example: Validate and send resource batch")
    print("")

    # Load example resource catalog
    try:
        batch = json.loads("""
        {
            "resources": [
                {
                    "id": "cicd_builder_lint",
                    "name": "Builder Lint",
                    "type": "cicd",
                    "impact": 0.9,
                    "feasibility": 0.95,
                    "strategic_fit": 0.9,
                    "cost_tokens": 200,
                    "tier": "critical",
                    "verification_status": "verified"
                }
            ],
            "metadata": {
                "discovery_date": "2026-08-18",
                "total_resources": 1,
                "tiers": {"critical": 1, "high": 0, "medium": 0, "low": 0}
            }
        }
        """)

        # Validate
        if HandoffValidator.validate_resource_batch(batch):
            print("✓ Batch validation passed")
            # Would send: HandoffTrigger.send_batch_to_aggregator(batch)

    except Exception as e:
        print(f"Error: {e}")

    print("")
    print("Handoff automation ready for integration into practices")
