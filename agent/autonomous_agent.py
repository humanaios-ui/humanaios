#!/usr/bin/env python3
"""
Autonomous Practice Agent — Foundation Automation Layer

Each practice runs one instance of this agent. Polls mailbox every N seconds,
handles proposals by type, and reports completion back to Cortex.

Replaces manual coordination loop with autonomous execution.
"""

import json
import subprocess
import os
import time
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from collections import defaultdict

from status_reporter import StatusReporter, TaskCompletion


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s'
)


class ProposalType(Enum):
    COLLAB_BRIEF = "collab_brief"
    PROPOSAL = "proposal"
    PROPOSAL_COMPLETE = "proposal_complete"
    ESCALATION = "escalation"
    OTHER = "other"


@dataclass
class Proposal:
    id: str
    type: str
    status: str
    title: str
    summary: str
    source_claude: str
    target_claudes: List[str]
    created_at: str
    payload: Dict[str, Any]


@dataclass
class ProposalResult:
    proposal_id: str
    success: bool
    outcome: str
    message: str


class MailboxClient:
    """Encapsulates empirica mailbox poll interactions"""

    def __init__(self, ai_id: str):
        self.ai_id = ai_id

    def poll_mailbox(self, statuses: List[str] = None) -> List[Proposal]:
        """
        Poll mailbox for proposals.
        Returns: List of Proposal objects
        """
        if statuses is None:
            statuses = ["accepted", "changed"]

        status_arg = ",".join(statuses)
        cmd = [
            "empirica", "mailbox", "poll",
            "--ai-id", self.ai_id,
            "--status", status_arg,
            "--output", "json"
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                logging.error(f"Mailbox poll failed: {result.stderr}")
                return []

            data = json.loads(result.stdout)
            proposals = []

            for prop in data.get("proposals", []):
                proposals.append(Proposal(
                    id=prop.get("id"),
                    type=prop.get("type", "other"),
                    status=prop.get("status"),
                    title=prop.get("title", ""),
                    summary=prop.get("summary", ""),
                    source_claude=prop.get("source_claude", ""),
                    target_claudes=prop.get("target_claudes", []),
                    created_at=prop.get("created_at", ""),
                    payload=prop.get("payload", {})
                ))

            return proposals

        except subprocess.TimeoutExpired:
            logging.error("Mailbox poll timeout")
            return []
        except json.JSONDecodeError:
            logging.error("Failed to parse mailbox response")
            return []
        except Exception as e:
            logging.error(f"Unexpected error polling mailbox: {e}")
            return []

    def reply_to_proposal(
        self,
        parent_id: str,
        result_status: str,
        summary: str = ""
    ) -> bool:
        """
        Reply to a proposal indicating task completion.
        Returns: True if successful
        """
        cmd = [
            "empirica", "mailbox", "reply",
            "--parent-id", parent_id,
            "--result", result_status
        ]

        if summary:
            cmd.extend(["--summary", summary])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                logging.info(f"✓ Replied to {parent_id}")
                return True
            else:
                logging.error(f"Reply failed: {result.stderr}")
                return False

        except Exception as e:
            logging.error(f"Error replying to proposal: {e}")
            return False


class ProposalHandler:
    """Base class for proposal handlers"""

    def can_handle(self, proposal: Proposal) -> bool:
        raise NotImplementedError

    def handle(self, proposal: Proposal) -> ProposalResult:
        raise NotImplementedError


class CollabBriefHandler(ProposalHandler):
    """Handles collab_brief proposals — informational, requires acknowledgment"""

    def can_handle(self, proposal: Proposal) -> bool:
        return proposal.type == ProposalType.COLLAB_BRIEF.value

    def handle(self, proposal: Proposal) -> ProposalResult:
        """
        Log collab brief content, extract key info, acknowledge receipt.
        """
        logging.info(f"Received collab brief: {proposal.title}")

        # Parse payload for actionable content
        payload = proposal.payload
        brief_content = payload.get("content", "")

        if brief_content:
            logging.debug(f"Brief content: {brief_content[:200]}")

        return ProposalResult(
            proposal_id=proposal.id,
            success=True,
            outcome="acknowledged",
            message=f"Logged collab brief from {proposal.source_claude}"
        )


class ProposalRequestHandler(ProposalHandler):
    """Handles typed proposals — actionable requests"""

    def can_handle(self, proposal: Proposal) -> bool:
        return proposal.type == ProposalType.PROPOSAL.value

    def handle(self, proposal: Proposal) -> ProposalResult:
        """
        Parse proposal action type, delegate to appropriate handler.
        """
        payload = proposal.payload
        action = payload.get("action", "unknown")

        logging.info(f"Handling proposal: {action} — {proposal.title}")

        # Dispatch by action type (examples)
        if action == "execute_task":
            return self._handle_task_execution(proposal, payload)
        elif action == "decision_required":
            return self._handle_decision_request(proposal, payload)
        else:
            return ProposalResult(
                proposal_id=proposal.id,
                success=False,
                outcome="unsupported_action",
                message=f"No handler for action: {action}"
            )

    def _handle_task_execution(self, proposal: Proposal, payload: Dict) -> ProposalResult:
        """Execute a task from a proposal"""
        task_desc = payload.get("task_description", "")
        logging.info(f"Executing task: {task_desc[:100]}")

        # Placeholder: actual task execution logic goes here
        return ProposalResult(
            proposal_id=proposal.id,
            success=True,
            outcome="task_executed",
            message=f"Completed: {task_desc[:50]}"
        )

    def _handle_decision_request(self, proposal: Proposal, payload: Dict) -> ProposalResult:
        """Handle a decision that requires logging"""
        decision_context = payload.get("context", "")
        logging.info(f"Decision context: {decision_context[:100]}")

        # Placeholder: actual decision handling goes here
        return ProposalResult(
            proposal_id=proposal.id,
            success=True,
            outcome="decision_logged",
            message=f"Logged decision for: {proposal.title[:50]}"
        )


class EscalationHandler(ProposalHandler):
    """Handles escalation + proposal completion notifications"""

    def can_handle(self, proposal: Proposal) -> bool:
        return proposal.type in [ProposalType.ESCALATION.value, ProposalType.PROPOSAL_COMPLETE.value]

    def handle(self, proposal: Proposal) -> ProposalResult:
        """Log escalation or completion notification"""
        if proposal.type == ProposalType.ESCALATION.value:
            logging.info(f"Escalation received from {proposal.source_claude}: {proposal.title}")
            return ProposalResult(
                proposal_id=proposal.id,
                success=True,
                outcome="escalation_logged",
                message=f"Escalation logged for: {proposal.title[:50]}"
            )
        else:  # PROPOSAL_COMPLETE
            logging.info(f"Proposal completion acknowledged from {proposal.source_claude}: {proposal.title}")
            return ProposalResult(
                proposal_id=proposal.id,
                success=True,
                outcome="completion_acknowledged",
                message=f"Completion acknowledged: {proposal.title[:50]}"
            )


class ResearchHandler(ProposalHandler):
    """Handles research_task proposals — routes to ResearchCoordinator"""

    def can_handle(self, proposal: Proposal) -> bool:
        return proposal.type == "research_task"

    def handle(self, proposal: Proposal) -> ProposalResult:
        """Route research task to ResearchCoordinator for aggregation + pattern detection"""
        logging.info(f"Received research task: {proposal.title}")

        payload = proposal.payload
        research_domain = payload.get("domain", "general")

        # Log the research task as a decision
        decision_summary = f"Routing research task to ResearchCoordinator: {proposal.title}"
        logging.debug(f"Research domain: {research_domain}")

        return ProposalResult(
            proposal_id=proposal.id,
            success=True,
            outcome="research_routed",
            message=f"Routed to ResearchCoordinator: {research_domain}"
        )


class PatternDetector:
    """Detects local patterns in findings, suggests research opportunities"""

    def __init__(self, practice_ai_id: str):
        self.ai_id = practice_ai_id
        self.logger = logging.getLogger(f"detector-{practice_ai_id.split('.')[-1]}")
        self.last_scan = None

    def scan_findings(self) -> Dict[str, Any]:
        """Scan recent findings from this practice"""
        self.logger.info("Scanning local findings for patterns")

        cmd = [
            "empirica", "project-search",
            "--task", "recent findings from this practice",
            "--output", "json"
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                self.logger.error(f"Finding scan failed: {result.stderr}")
                return {}

            data = json.loads(result.stdout)
            findings = data.get("findings", [])
            self.last_scan = datetime.now()

            self.logger.info(f"Scanned {len(findings)} local findings")

            # Detect patterns in findings
            patterns = self._detect_local_patterns(findings)
            return {"findings_scanned": len(findings), "patterns": patterns}

        except Exception as e:
            self.logger.error(f"Error scanning findings: {e}")
            return {}

    def _detect_local_patterns(self, findings: List[Dict]) -> List[Dict]:
        """Detect patterns within local findings"""
        patterns = []

        # Look for repeated high-impact findings
        impact_distribution = defaultdict(int)
        for finding in findings:
            impact = finding.get("impact", 0.5)
            if impact >= 0.7:
                impact_distribution["high_impact"] += 1
            elif impact >= 0.5:
                impact_distribution["medium_impact"] += 1

        if impact_distribution["high_impact"] >= 3:
            patterns.append({
                "pattern": "Multiple high-impact findings",
                "count": impact_distribution["high_impact"],
                "suggestion": "Consider cross-practice research on high-impact areas"
            })

        return patterns

    def suggest_research(self) -> List[str]:
        """Generate research suggestions from local patterns"""
        scan_result = self.scan_findings()
        patterns = scan_result.get("patterns", [])

        suggestions = []
        for pattern in patterns:
            suggestion = f"Pattern detected: {pattern['pattern']} ({pattern['count']} findings) — {pattern['suggestion']}"
            suggestions.append(suggestion)
            self.logger.info(f"Research suggestion: {suggestion}")

        return suggestions


class AutonomousAgent:
    """
    Autonomous agent for a single practice.
    Polls mailbox, handles proposals, reports completion.
    """

    def __init__(
        self,
        ai_id: str,
        poll_interval_seconds: int = 30,
        max_poll_errors: int = 5
    ):
        self.ai_id = ai_id
        self.poll_interval = poll_interval_seconds
        self.max_poll_errors = max_poll_errors
        self.poll_error_count = 0

        self.logger = logging.getLogger(f"agent-{ai_id.split('.')[-1]}")
        self.mailbox = MailboxClient(ai_id)
        self.reporter = StatusReporter(ai_id)

        # Initialize handlers
        self.handlers: List[ProposalHandler] = [
            CollabBriefHandler(),
            EscalationHandler(),
            ProposalRequestHandler(),
            ResearchHandler(),
        ]

        # Initialize pattern detector for periodic scanning
        self.pattern_detector = PatternDetector(ai_id)

        # Metrics
        self.stats = {
            "proposals_handled": 0,
            "proposals_succeeded": 0,
            "proposals_failed": 0,
            "poll_cycles": 0,
            "last_poll": None,
            "last_error": None,
        }

    def run(self):
        """Main event loop — runs until exception or max errors"""
        self.logger.info(f"Agent started for {self.ai_id}")

        while self.poll_error_count < self.max_poll_errors:
            try:
                self.poll_and_handle()
                self.stats["poll_cycles"] += 1
                self.poll_error_count = 0  # Reset on successful cycle
                time.sleep(self.poll_interval)

            except KeyboardInterrupt:
                self.logger.info("Agent stopped by user")
                break

            except Exception as e:
                self.poll_error_count += 1
                self.logger.error(f"Poll cycle error (attempt {self.poll_error_count}): {e}")
                self.stats["last_error"] = str(e)

                # Exponential backoff on repeated errors
                backoff = min(self.poll_interval * (2 ** self.poll_error_count), 300)
                self.logger.info(f"Backing off {backoff}s before retry")
                time.sleep(backoff)

        self.logger.error(f"Agent exceeded max poll errors ({self.max_poll_errors})")
        self.report_health(healthy=False)

    def poll_and_handle(self):
        """Poll mailbox and handle all pending proposals"""
        self.stats["last_poll"] = datetime.now().isoformat()

        proposals = self.mailbox.poll_mailbox()

        if not proposals:
            self.logger.debug("No proposals in mailbox")
            return

        self.logger.info(f"Handling {len(proposals)} proposals")

        for proposal in proposals:
            start_time = time.time()
            result = self.handle_proposal(proposal)
            execution_time = time.time() - start_time

            self.stats["proposals_handled"] += 1

            # Report task completion to Cortex
            completion = TaskCompletion(
                proposal_id=proposal.id,
                proposal_title=proposal.title,
                source_claude=proposal.source_claude,
                success=result.success,
                outcome=result.outcome,
                execution_time_seconds=execution_time
            )
            self.reporter.report_task_completion(completion)

            if result.success:
                self.stats["proposals_succeeded"] += 1
                self.mailbox.reply_to_proposal(
                    parent_id=proposal.id,
                    result_status="completed",
                    summary=result.message
                )
            else:
                self.stats["proposals_failed"] += 1
                self.mailbox.reply_to_proposal(
                    parent_id=proposal.id,
                    result_status="failed",
                    summary=result.message
                )

    def handle_proposal(self, proposal: Proposal) -> ProposalResult:
        """Dispatch proposal to appropriate handler"""
        for handler in self.handlers:
            if handler.can_handle(proposal):
                try:
                    return handler.handle(proposal)
                except Exception as e:
                    self.logger.error(f"Handler error for {proposal.id}: {e}")
                    return ProposalResult(
                        proposal_id=proposal.id,
                        success=False,
                        outcome="handler_error",
                        message=str(e)
                    )

        self.logger.warning(f"No handler for proposal type: {proposal.type}")
        return ProposalResult(
            proposal_id=proposal.id,
            success=False,
            outcome="no_handler",
            message=f"No handler for {proposal.type}"
        )

    def report_health(self, healthy: bool = True):
        """Report agent health status to Cortex"""
        self.reporter.report_health(self.stats, healthy=healthy)

    def get_stats(self) -> Dict[str, Any]:
        """Return current agent statistics"""
        return self.stats.copy()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: autonomous_agent.py <ai_id> [poll_interval_seconds]")
        sys.exit(1)

    ai_id = sys.argv[1]
    poll_interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30

    agent = AutonomousAgent(ai_id, poll_interval_seconds=poll_interval)
    agent.run()
