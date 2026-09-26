#!/usr/bin/env python3
"""
Phase 3.6: Alert Escalation Automation
Complete orchestration loop:
  alerts → escalation decisions → cortex proposals → practice routing → Admiral notification
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import time

# Import orchestration modules
sys.path.insert(0, str(Path(__file__).parent / "analytics"))
from escalation_orchestrator import (
    AlertEscalationOrchestrator,
    Alert,
    AlertSeverity,
)
from cortex_escalation_proposer import CortexEscalationProposer

class Phase36Orchestrator:
    """Complete Phase 3.6 alert escalation automation"""

    def __init__(self, alerts_path=None):
        self.escalation_orchestrator = AlertEscalationOrchestrator()
        self.cortex_proposer = CortexEscalationProposer()
        # Use test alerts if available, otherwise use processed alerts
        self.alerts_path = Path(alerts_path or "analytics/alerts_for_escalation.json")
        if not self.alerts_path.exists():
            self.alerts_path = Path("analytics/alerts_processed.json")
        self.output_log = Path("phase36_execution.json")

    def load_alerts(self) -> list:
        """Load alerts from observability system"""
        if self.alerts_path.exists():
            with open(self.alerts_path) as f:
                try:
                    data = json.load(f)
                    return [self._dict_to_alert(a) for a in data.get("alerts", [])]
                except json.JSONDecodeError:
                    return []
        return []

    def _dict_to_alert(self, alert_dict: dict) -> Alert:
        """Convert dict to Alert object"""
        return Alert(
            alert_id=alert_dict.get("alert_id", f"alert_{int(time.time())}"),
            timestamp=alert_dict.get("timestamp", time.time()),
            severity=AlertSeverity(alert_dict.get("severity", "warning")),
            rule_id=alert_dict.get("rule_id", "unknown"),
            rule_name=alert_dict.get("rule_name", "Unknown Alert"),
            message=alert_dict.get("message", ""),
            practice=alert_dict.get("practice", ""),
            metric=alert_dict.get("metric", ""),
            current_value=float(alert_dict.get("current_value", 0)),
            threshold=float(alert_dict.get("threshold", 0)),
            metadata=alert_dict.get("metadata", {})
        )

    def process_alerts(self):
        """Main Phase 3.6 orchestration loop"""

        execution_start = time.time()
        alerts = self.load_alerts()

        execution = {
            "phase": "3.6",
            "execution_id": f"exec_{int(execution_start)}",
            "timestamp": datetime.now().isoformat(),
            "alerts_processed": 0,
            "escalations_triggered": 0,
            "critical_escalations": 0,
            "proposals_created": 0,
            "ser_created": 0,
            "details": []
        }

        for alert in alerts:
            try:
                # Step 1: Make escalation decision
                decision = self.escalation_orchestrator.process_alert(alert)
                self.escalation_orchestrator.log_decision(decision)

                # Step 2: Create cortex proposal
                proposal = self.cortex_proposer.process_escalation(
                    alert.to_dict(),
                    decision.to_dict()
                )

                # Record execution details
                detail = {
                    "alert_id": alert.alert_id,
                    "rule": alert.rule_name,
                    "severity": alert.severity.value,
                    "decision_id": decision.to_dict(),
                    "proposal_id": proposal.proposal_id,
                    "targets": proposal.target_claudes,
                    "status": "escalated"
                }

                execution["details"].append(detail)
                execution["alerts_processed"] += 1
                execution["escalations_triggered"] += 1

                if alert.severity == AlertSeverity.CRITICAL:
                    execution["critical_escalations"] += 1

                if decision.ser_id:
                    execution["ser_created"] += 1

                execution["proposals_created"] += 1

            except Exception as e:
                execution["details"].append({
                    "alert_id": alert.alert_id,
                    "status": "error",
                    "error": str(e)
                })

        # Step 3: Generate metrics
        metrics = self.escalation_orchestrator.generate_metrics()
        execution["metrics"] = metrics.get("escalation_metrics", {})

        # Log execution
        self._log_execution(execution)

        return execution

    def _log_execution(self, execution: dict):
        """Log Phase 3.6 execution"""
        executions = []

        if self.output_log.exists():
            with open(self.output_log) as f:
                try:
                    data = json.load(f)
                    executions = data.get("executions", [])
                except json.JSONDecodeError:
                    executions = []

        executions.append(execution)

        # Keep last 100 executions
        if len(executions) > 100:
            executions = executions[-100:]

        with open(self.output_log, "w") as f:
            json.dump({
                "phase": "3.6",
                "export_time": datetime.now().isoformat(),
                "total_executions": len(executions),
                "last_execution": execution,
                "summary": {
                    "total_alerts_processed": sum(e.get("alerts_processed", 0) for e in executions),
                    "total_escalations": sum(e.get("escalations_triggered", 0) for e in executions),
                    "total_critical": sum(e.get("critical_escalations", 0) for e in executions),
                    "total_proposals": sum(e.get("proposals_created", 0) for e in executions),
                    "success_rate": (
                        sum(len(e.get("details", [])) for e in executions) /
                        max(sum(e.get("alerts_processed", 0) for e in executions), 1)
                    ) * 100
                },
                "executions": executions
            }, f, indent=2)

def main():
    """Run Phase 3.6 orchestration"""
    print("🚀 Phase 3.6: Alert Escalation Automation")
    print("=" * 50)

    orchestrator = Phase36Orchestrator()
    execution = orchestrator.process_alerts()

    print(f"\n✅ Execution Complete")
    print(f"  Alerts processed: {execution['alerts_processed']}")
    print(f"  Escalations triggered: {execution['escalations_triggered']}")
    print(f"  Critical escalations: {execution['critical_escalations']}")
    print(f"  Proposals created: {execution['proposals_created']}")
    print(f"  SERs created: {execution['ser_created']}")

    if execution['metrics']:
        metrics = execution['metrics']
        print(f"\n📊 Metrics:")
        print(f"  Critical rate: {metrics.get('critical_rate', 0)*100:.1f}%")
        print(f"  By practice: {metrics.get('by_practice', {})}")

if __name__ == "__main__":
    main()
