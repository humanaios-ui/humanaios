#!/usr/bin/env python3
"""
Phase 3.6: Cortex Escalation Proposer
Generates typed cortex proposals for alert escalations
Routes escalations to practices and Admiral
"""

import json
import uuid
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

@dataclass
class CortexProposal:
    """Typed cortex proposal for escalation"""
    proposal_id: str
    source_claude: str  # empirica-foundation.carly.empirica-foundation-evaluator
    target_claudes: List[str]  # practices or Admiral
    proposal_type: str  # "escalation_request", "incident_notification", "ser_decision"
    payload: Dict[str, Any]
    priority: str  # "critical", "high", "normal"
    created_at: float
    expires_at: float

    def to_dict(self):
        return {
            "proposal_id": self.proposal_id,
            "source_claude": self.source_claude,
            "target_claudes": self.target_claudes,
            "proposal_type": self.proposal_type,
            "payload": self.payload,
            "priority": self.priority,
            "created_at": self.created_at,
            "expires_at": self.expires_at
        }

class CortexEscalationProposer:
    """Generates proposals for alert escalations"""

    def __init__(self):
        self.source_claude = "empirica-foundation.carly.empirica-foundation-evaluator"
        self.proposals_log = Path("analytics/escalation_proposals.json")
        self.mesh_outbox = Path("analytics/mesh_outbox.json")

        # Practice roster
        self.practices = {
            "empirica-autonomy": "empirica-foundation.carly.empirica-autonomy",
            "empirica-mesh-support": "empirica-foundation.carly.empirica-mesh-support",
            "empirica-outreach": "empirica-foundation.carly.empirica-outreach",
            "humanaios": "empirica-foundation.carly.humanaios",
        }

        self.admiral = "empirica-foundation.carly.empirica-foundation-evaluator"  # Admiral is evaluator seat

    def create_escalation_proposal(
        self,
        alert_dict: Dict[str, Any],
        decision_dict: Dict[str, Any],
        ser_id: Optional[str] = None
    ) -> CortexProposal:
        """Create proposal for alert escalation"""

        alert = alert_dict
        decision = decision_dict
        severity = alert.get("severity", "warning")
        practice_name = alert.get("practice", "unknown")

        # Determine targets
        targets = []
        if decision.get("target_practice"):
            targets.append(decision["target_practice"])

        if decision.get("admiral_escalate"):
            targets.append(self.admiral)

        # Create proposal payload
        payload = {
            "alert": alert,
            "decision": decision,
            "escalation_type": "critical" if severity == "critical" else "warning",
            "ser_id": ser_id,
            "action_required": decision.get("admiral_escalate", False),
            "response_deadline": (time.time() + 300) if severity == "critical" else (time.time() + 900),
        }

        # Create proposal
        proposal = CortexProposal(
            proposal_id=f"prop_{uuid.uuid4().hex[:12]}",
            source_claude=self.source_claude,
            target_claudes=targets,
            proposal_type="escalation_request" if severity == "critical" else "incident_notification",
            payload=payload,
            priority="critical" if severity == "critical" else "high",
            created_at=time.time(),
            expires_at=time.time() + (3600 if severity == "critical" else 7200)
        )

        return proposal

    def send_proposal(self, proposal: CortexProposal):
        """Send proposal to mesh (log to outbox)"""

        outbox = []
        if self.mesh_outbox.exists():
            with open(self.mesh_outbox) as f:
                try:
                    data = json.load(f)
                    outbox = data.get("pending", [])
                except json.JSONDecodeError:
                    outbox = []

        outbox.append({
            "event_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "status": "pending",
            **proposal.to_dict()
        })

        # Keep last 500 proposals
        if len(outbox) > 500:
            outbox = outbox[-500:]

        with open(self.mesh_outbox, "w") as f:
            json.dump({
                "mesh_outbox": "empirica-foundation.carly.empirica-foundation-evaluator",
                "last_updated": datetime.now().isoformat(),
                "pending_count": len(outbox),
                "pending": outbox
            }, f, indent=2)

        # Log proposal for audit
        self._log_proposal(proposal)

    def _log_proposal(self, proposal: CortexProposal):
        """Log proposal for audit trail"""
        proposals = []

        if self.proposals_log.exists():
            with open(self.proposals_log) as f:
                try:
                    data = json.load(f)
                    proposals = data.get("proposals", [])
                except json.JSONDecodeError:
                    proposals = []

        proposals.append({
            "logged_at": datetime.now().isoformat(),
            **proposal.to_dict()
        })

        # Keep last 1000 proposals
        if len(proposals) > 1000:
            proposals = proposals[-1000:]

        with open(self.proposals_log, "w") as f:
            json.dump({
                "source_claude": self.source_claude,
                "export_time": datetime.now().isoformat(),
                "total_proposals": len(proposals),
                "proposals": proposals,
                "summary": {
                    "critical": sum(1 for p in proposals if p.get("priority") == "critical"),
                    "high": sum(1 for p in proposals if p.get("priority") == "high"),
                    "escalation_requests": sum(1 for p in proposals if p.get("proposal_type") == "escalation_request"),
                    "incident_notifications": sum(1 for p in proposals if p.get("proposal_type") == "incident_notification"),
                }
            }, f, indent=2)

    def process_escalation(
        self,
        alert_dict: Dict[str, Any],
        decision_dict: Dict[str, Any]
    ) -> CortexProposal:
        """Process alert escalation: create and send proposal"""

        ser_id = decision_dict.get("ser_id")
        proposal = self.create_escalation_proposal(alert_dict, decision_dict, ser_id)
        self.send_proposal(proposal)

        return proposal

def main():
    """Demo: Send escalation proposals"""
    proposer = CortexEscalationProposer()

    # Sample alert and decision
    alert = {
        "alert_id": "alert_test_001",
        "severity": "critical",
        "rule_name": "Query Latency Critical",
        "practice": "empirica-autonomy",
        "message": "Query latency p95 exceeds SLA"
    }

    decision = {
        "alert_id": "alert_test_001",
        "target_practice": "empirica-foundation.carly.empirica-autonomy",
        "admiral_escalate": True,
        "ser_id": "ser_abc123",
        "reasoning": "Critical latency spike requires Admiral attention"
    }

    # Process escalation
    proposal = proposer.process_escalation(alert, decision)
    print(f"✓ Proposal created: {proposal.proposal_id}")
    print(f"  Type: {proposal.proposal_type}")
    print(f"  Priority: {proposal.priority}")
    print(f"  Targets: {proposal.target_claudes}")

if __name__ == "__main__":
    main()
