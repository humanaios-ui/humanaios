#!/usr/bin/env python3
"""
Status Reporter — Logs agent completion events to Cortex

Handles:
1. Task completion via cortex_collab (informational)
2. Health metrics via cortex finding-log
3. Success/failure rate tracking
4. Alert escalation for stalled proposals
"""

import json
import subprocess
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class TaskCompletion:
    proposal_id: str
    proposal_title: str
    source_claude: str
    success: bool
    outcome: str
    execution_time_seconds: float


class StatusReporter:
    """Reports agent execution status and health to Cortex"""

    def __init__(self, practice_ai_id: str):
        self.ai_id = practice_ai_id
        self.logger = logging.getLogger(f"reporter-{practice_ai_id.split('.')[-1]}")

        # Track completion events
        self.completed_tasks: List[TaskCompletion] = []
        self.last_health_report = None

    def report_task_completion(
        self,
        completion: TaskCompletion,
        send_to_source: bool = True
    ) -> bool:
        """
        Report a task completion event to Cortex.
        Optionally sends notification to source Claude via cortex_collab.
        """
        self.completed_tasks.append(completion)

        # Log as decision (what we executed)
        log_cmd = [
            "empirica", "decision-log",
            "--choice", f"Executed: {completion.proposal_title}",
            "--rationale", (
                f"Source: {completion.source_claude}\n"
                f"Outcome: {completion.outcome}\n"
                f"Execution time: {completion.execution_time_seconds:.2f}s"
            ),
            "--reversibility", "committal",
            "--epistemic-source", "ran"
        ]

        try:
            result = subprocess.run(
                log_cmd,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                self.logger.error(f"Failed to log decision: {result.stderr}")
                return False

            self.logger.info(f"✓ Logged task completion: {completion.proposal_id}")

            # Optionally notify source practice
            if send_to_source:
                self._notify_source(completion)

            return True

        except Exception as e:
            self.logger.error(f"Error reporting task completion: {e}")
            return False

    def _notify_source(self, completion: TaskCompletion):
        """Send mailbox reply notification to source practice"""
        notification_summary = f"Task completed: {completion.proposal_title} (outcome: {completion.outcome}, time: {completion.execution_time_seconds:.2f}s)"

        reply_cmd = [
            "empirica", "mailbox", "reply",
            "--parent-id", completion.proposal_id,
            "--result", "completed" if completion.success else "failed",
            "--summary", notification_summary
        ]

        try:
            result = subprocess.run(
                reply_cmd,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                self.logger.info(f"✓ Sent completion notification to {completion.source_claude}")
            else:
                self.logger.error(f"Failed to notify source: {result.stderr}")

        except Exception as e:
            self.logger.error(f"Error notifying source practice: {e}")

    def report_health(
        self,
        stats: Dict[str, Any],
        healthy: bool = True
    ) -> bool:
        """
        Report agent health metrics to Cortex.
        Includes proposal throughput, success rate, error metrics.
        """
        self.last_health_report = datetime.now()

        # Calculate derived metrics
        total_handled = stats.get("proposals_handled", 0)
        succeeded = stats.get("proposals_succeeded", 0)
        failed = stats.get("proposals_failed", 0)

        success_rate = (succeeded / total_handled * 100) if total_handled > 0 else 0
        poll_cycles = stats.get("poll_cycles", 0)

        avg_proposals_per_cycle = (
            total_handled / poll_cycles if poll_cycles > 0 else 0
        )

        health_description = f"""
## Agent Health Report: {self.ai_id.split('.')[-1]}

**Status:** {'✓ HEALTHY' if healthy else '✗ UNHEALTHY'}

### Throughput
- Proposals handled: {total_handled}
- Poll cycles: {poll_cycles}
- Avg proposals per cycle: {avg_proposals_per_cycle:.2f}

### Success Rate
- Succeeded: {succeeded}
- Failed: {failed}
- Success rate: {success_rate:.1f}%

### Timing
- Last poll: {stats.get('last_poll', 'never')}
- Last error: {stats.get('last_error', 'none')}

### Timestamp
- Report generated: {datetime.now().isoformat()}
"""

        finding_cmd = [
            "empirica", "finding-log",
            "--finding", f"Agent health: {self.ai_id.split('.')[-1]} — {success_rate:.0f}% success rate",
            "--description", health_description,
            "--impact", "0.5",
            "--epistemic-source", "ran"
        ]

        try:
            result = subprocess.run(
                finding_cmd,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                self.logger.info(f"✓ Health report logged: {success_rate:.1f}% success")
                return True
            else:
                self.logger.error(f"Failed to log health: {result.stderr}")
                return False

        except Exception as e:
            self.logger.error(f"Error reporting health: {e}")
            return False

    def check_stalled_proposals(
        self,
        stalled_threshold_minutes: int = 60
    ) -> List[str]:
        """
        Check for proposals that haven't been processed in stalled_threshold_minutes.
        Returns list of proposal IDs that may need escalation.
        """
        # In full implementation, would query cortex SER for stuck proposals
        # For now, return empty list as placeholder
        return []

    def alert_on_stall(self, proposal_id: str, reason: str):
        """Alert if a proposal execution stalls"""
        alert_cmd = [
            "empirica", "unknown-log",
            "--unknown", f"Proposal {proposal_id} stalled: {reason}",
            "--description", f"Execution of proposal {proposal_id} exceeded stall threshold"
        ]

        try:
            subprocess.run(
                alert_cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            self.logger.warning(f"Stall alert logged for {proposal_id}")

        except Exception as e:
            self.logger.error(f"Error logging stall alert: {e}")

    def report_research_finding(
        self,
        finding_title: str,
        finding_description: str,
        impact: float = 0.5,
        is_pattern: bool = False
    ) -> bool:
        """Log research findings to Cortex as shared artifacts"""
        find_type = "pattern" if is_pattern else "research finding"

        log_cmd = [
            "empirica", "finding-log",
            "--finding", finding_title,
            "--description", finding_description,
            "--impact", str(impact),
            "--visibility", "shared",
            "--epistemic-source", "search"
        ]

        try:
            result = subprocess.run(
                log_cmd,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                self.logger.info(f"✓ Logged research {find_type}: {finding_title}")
                return True
            else:
                self.logger.error(f"Failed to log research {find_type}: {result.stderr}")
                return False

        except Exception as e:
            self.logger.error(f"Error reporting research finding: {e}")
            return False

    def get_completion_summary(self) -> Dict[str, Any]:
        """Return summary of completed tasks"""
        if not self.completed_tasks:
            return {"total": 0, "completed": []}

        return {
            "total": len(self.completed_tasks),
            "succeeded": len([t for t in self.completed_tasks if t.success]),
            "failed": len([t for t in self.completed_tasks if not t.success]),
            "completed": [
                {
                    "proposal_id": t.proposal_id,
                    "title": t.proposal_title,
                    "outcome": t.outcome,
                    "time_seconds": t.execution_time_seconds
                }
                for t in self.completed_tasks
            ]
        }


class AggregateHealthMonitor:
    """
    Monitors health across all 15 practice agents.
    Aggregates metrics and alerts on fleet-wide issues.
    """

    def __init__(self):
        self.reporters: Dict[str, StatusReporter] = {}
        self.logger = logging.getLogger("fleet-monitor")

    def register_agent(self, ai_id: str) -> StatusReporter:
        """Register a new agent reporter"""
        reporter = StatusReporter(ai_id)
        self.reporters[ai_id] = reporter
        return reporter

    def aggregate_health(self) -> Dict[str, Any]:
        """Aggregate health across all agents"""
        total_proposals = 0
        total_succeeded = 0
        total_failed = 0
        agent_health = {}

        for ai_id, reporter in self.reporters.items():
            summary = reporter.get_completion_summary()
            total_proposals += summary.get("total", 0)
            total_succeeded += summary.get("succeeded", 0)
            total_failed += summary.get("failed", 0)

            agent_health[ai_id] = {
                "succeeded": summary.get("succeeded", 0),
                "failed": summary.get("failed", 0),
                "last_report": reporter.last_health_report
            }

        fleet_success_rate = (
            (total_succeeded / total_proposals * 100)
            if total_proposals > 0
            else 0
        )

        return {
            "timestamp": datetime.now().isoformat(),
            "total_proposals_handled": total_proposals,
            "total_succeeded": total_succeeded,
            "total_failed": total_failed,
            "fleet_success_rate": fleet_success_rate,
            "agents": len(self.reporters),
            "agent_health": agent_health
        }

    def report_fleet_status(self) -> bool:
        """Log aggregate fleet health to Cortex"""
        aggregate = self.aggregate_health()

        description = f"""
## Autonomous Agent Fleet Health Report

**Report Time:** {aggregate['timestamp']}

### Fleet Summary
- Agents active: {aggregate['agents']}
- Total proposals handled: {aggregate['total_proposals_handled']}
- Succeeded: {aggregate['total_succeeded']}
- Failed: {aggregate['total_failed']}
- **Fleet success rate: {aggregate['fleet_success_rate']:.1f}%**

### Agent Breakdown
{self._format_agent_breakdown(aggregate['agent_health'])}
"""

        cmd = [
            "empirica", "finding-log",
            "--finding", f"Agent fleet health: {aggregate['fleet_success_rate']:.0f}% across {aggregate['agents']} agents",
            "--description", description,
            "--impact", "0.8" if aggregate['fleet_success_rate'] >= 80 else "0.9",
            "--epistemic-source", "ran"
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                self.logger.info(f"✓ Fleet status reported: {aggregate['fleet_success_rate']:.1f}%")
                return True
            else:
                self.logger.error(f"Failed to report fleet status: {result.stderr}")
                return False

        except Exception as e:
            self.logger.error(f"Error reporting fleet status: {e}")
            return False

    def _format_agent_breakdown(self, agent_health: Dict) -> str:
        """Format agent health data for markdown"""
        lines = []
        for ai_id, health in agent_health.items():
            practice_name = ai_id.split('.')[-1]
            succeeded = health.get('succeeded', 0)
            failed = health.get('failed', 0)
            total = succeeded + failed
            rate = (succeeded / total * 100) if total > 0 else 0
            lines.append(f"- **{practice_name}**: {rate:.0f}% ({succeeded}/{total})")
        return "\n".join(lines)
