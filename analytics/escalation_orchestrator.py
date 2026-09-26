#!/usr/bin/env python3
"""
Phase 3.6: Alert Escalation Orchestrator
Routes critical alerts to cortex proposals and practices
"""

import json
import time
import hashlib
import uuid
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any

class AlertSeverity(Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"

class EscalationAction(Enum):
    SEND_TO_PRACTICE = "send_to_practice"
    ADMIRAL_ESCALATION = "admiral_escalation"
    CREATE_SER = "create_ser"
    LOG_INCIDENT = "log_incident"

@dataclass
class Alert:
    """Alert from observability system"""
    alert_id: str
    timestamp: float
    severity: AlertSeverity
    rule_id: str
    rule_name: str
    message: str
    practice: str
    metric: str
    current_value: float
    threshold: float
    metadata: Dict[str, Any]

    def to_dict(self):
        return {
            "alert_id": self.alert_id,
            "timestamp": self.timestamp,
            "severity": self.severity.value,
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "message": self.message,
            "practice": self.practice,
            "metric": self.metric,
            "current_value": self.current_value,
            "threshold": self.threshold,
            "metadata": self.metadata
        }

@dataclass
class EscalationDecision:
    """Decision about how to escalate an alert"""
    alert_id: str
    actions: List[EscalationAction]
    target_practice: Optional[str]
    admiral_escalate: bool
    ser_id: Optional[str]
    reasoning: str
    timestamp: float

    def to_dict(self):
        return {
            "alert_id": self.alert_id,
            "actions": [a.value for a in self.actions],
            "target_practice": self.target_practice,
            "admiral_escalate": self.admiral_escalate,
            "ser_id": self.ser_id,
            "reasoning": self.reasoning,
            "timestamp": self.timestamp
        }

class AlertEscalationOrchestrator:
    """Routes alerts to escalation workflows"""

    def __init__(self, alert_rules_path: str = "analytics/alert_rules.json"):
        self.alert_rules_path = Path(alert_rules_path)
        self.rules = self._load_rules()
        self.decisions_log = Path("analytics/escalation_decisions.json")
        self.metrics_path = Path("analytics/escalation_metrics.json")

    def _load_rules(self) -> Dict[str, Any]:
        """Load alert rules and SLAs"""
        if self.alert_rules_path.exists():
            with open(self.alert_rules_path) as f:
                return json.load(f)
        return {"alert_rules": [], "routing_rules": {}, "practice_slas": {}}

    def process_alert(self, alert: Alert) -> EscalationDecision:
        """Decide how to escalate an alert"""
        actions = []
        target_practice = None
        admiral_escalate = False
        ser_id = None

        routing_rule = self.rules.get("routing_rules", {}).get(
            "escalation" if alert.severity == AlertSeverity.CRITICAL else "alert", {}
        )

        # Determine actions based on alert routing
        if alert.severity == AlertSeverity.CRITICAL:
            actions.extend([
                EscalationAction.CREATE_SER,
                EscalationAction.SEND_TO_PRACTICE,
                EscalationAction.LOG_INCIDENT,
            ])
            admiral_escalate = True
            ser_id = self._create_ser_id(alert)
        else:
            actions.extend([
                EscalationAction.SEND_TO_PRACTICE,
                EscalationAction.LOG_INCIDENT,
            ])

        # Route to practice
        if alert.practice:
            target_practice = alert.practice
        else:
            # Route to mesh-support for unspecified practices
            target_practice = "empirica-foundation.carly.empirica-mesh-support"

        decision = EscalationDecision(
            alert_id=alert.alert_id,
            actions=actions,
            target_practice=target_practice,
            admiral_escalate=admiral_escalate,
            ser_id=ser_id,
            reasoning=self._generate_reasoning(alert, routing_rule),
            timestamp=time.time()
        )

        return decision

    def _create_ser_id(self, alert: Alert) -> str:
        """Generate SER ID for critical alert"""
        content = f"{alert.rule_id}_{alert.practice}_{alert.timestamp}".encode()
        hash_val = hashlib.sha256(content).hexdigest()[:12]
        return f"ser_{hash_val}_{int(time.time())}"

    def _generate_reasoning(self, alert: Alert, routing_rule: Dict) -> str:
        """Generate explanation for escalation decision"""
        if alert.severity == AlertSeverity.CRITICAL:
            return (
                f"CRITICAL alert: {alert.rule_name}. "
                f"Metric {alert.metric} at {alert.current_value:.2f} "
                f"exceeds threshold {alert.threshold:.2f}. "
                f"SER created for sustained tracking. "
                f"Admiral escalation triggered per escalation protocol."
            )
        else:
            return (
                f"WARNING alert: {alert.rule_name}. "
                f"Metric {alert.metric} at {alert.current_value:.2f} "
                f"approaches threshold {alert.threshold:.2f}. "
                f"Routed to practice {alert.practice} for investigation."
            )

    def log_decision(self, decision: EscalationDecision):
        """Log escalation decision"""
        decisions = []

        if self.decisions_log.exists():
            with open(self.decisions_log) as f:
                try:
                    data = json.load(f)
                    decisions = data.get("decisions", [])
                except json.JSONDecodeError:
                    decisions = []

        decisions.append({
            "decision_id": str(uuid.uuid4()),
            **decision.to_dict()
        })

        # Keep last 1000 decisions
        if len(decisions) > 1000:
            decisions = decisions[-1000:]

        with open(self.decisions_log, "w") as f:
            json.dump({
                "export_time": datetime.now().isoformat(),
                "decisions": decisions,
                "summary": {
                    "total_decisions": len(decisions),
                    "critical_count": sum(1 for d in decisions if d.get("admiral_escalate")),
                    "ser_created": sum(1 for d in decisions if d.get("ser_id"))
                }
            }, f, indent=2)

    def generate_metrics(self):
        """Generate escalation metrics for dashboards"""
        decisions = []

        if self.decisions_log.exists():
            with open(self.decisions_log) as f:
                try:
                    data = json.load(f)
                    decisions = data.get("decisions", [])
                except json.JSONDecodeError:
                    decisions = []

        # Calculate metrics
        total = len(decisions)
        critical_count = sum(1 for d in decisions if d.get("admiral_escalate"))
        warning_count = total - critical_count
        ser_created = sum(1 for d in decisions if d.get("ser_id"))

        # Practice routing
        by_practice = {}
        for d in decisions:
            practice = d.get("target_practice", "unknown")
            by_practice[practice] = by_practice.get(practice, 0) + 1

        metrics = {
            "timestamp": datetime.now().isoformat(),
            "escalation_metrics": {
                "total_escalations": total,
                "critical_escalations": critical_count,
                "warning_escalations": warning_count,
                "ser_created": ser_created,
                "critical_rate": critical_count / max(total, 1),
                "by_practice": by_practice
            },
            "slas": {
                "critical_response_target_minutes": 5,
                "warning_response_target_minutes": 15,
                "ser_creation_rate": ser_created / max(total, 1)
            }
        }

        with open(self.metrics_path, "w") as f:
            json.dump(metrics, f, indent=2)

        return metrics

def main():
    """Demo: Process sample alerts"""
    orchestrator = AlertEscalationOrchestrator()

    # Sample critical alert
    critical_alert = Alert(
        alert_id=f"alert_{int(time.time())}_{uuid.uuid4().hex[:8]}",
        timestamp=time.time(),
        severity=AlertSeverity.CRITICAL,
        rule_id="latency_critical",
        rule_name="Query Latency Critical",
        message="Query latency p95 exceeds SLA",
        practice="empirica-autonomy",
        metric="loki_query_duration_seconds",
        current_value=2.5,
        threshold=2.0,
        metadata={"quantile": 0.95, "sla_window": "5m"}
    )

    # Sample warning alert
    warning_alert = Alert(
        alert_id=f"alert_{int(time.time())+1}_{uuid.uuid4().hex[:8]}",
        timestamp=time.time(),
        severity=AlertSeverity.WARNING,
        rule_id="latency_warning",
        rule_name="Query Latency Warning",
        message="Query latency p95 approaching threshold",
        practice="empirica-mesh-support",
        metric="loki_query_duration_seconds",
        current_value=1.2,
        threshold=1.0,
        metadata={"quantile": 0.95, "trend": "increasing"}
    )

    # Process alerts
    for alert in [critical_alert, warning_alert]:
        decision = orchestrator.process_alert(alert)
        orchestrator.log_decision(decision)
        print(f"✓ {alert.rule_name}: {decision.reasoning}")

    # Generate metrics
    metrics = orchestrator.generate_metrics()
    print(f"\n✓ Escalation metrics: {metrics['escalation_metrics']['total_escalations']} total, "
          f"{metrics['escalation_metrics']['critical_escalations']} critical")

if __name__ == "__main__":
    main()
