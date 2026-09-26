#!/usr/bin/env python3
"""
Alert Manager - Orchestrates anomaly detection, routing, and escalation
"""

import json
import subprocess
from typing import List, Dict, Any
from datetime import datetime
import logging

from anomaly_detection import AnomalyDetector, AnomalyAlert

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("alert_manager")


class AlertManager:
    """Manages alert detection, routing, and escalation"""

    def __init__(self, rules_file: str = "alert_rules.json"):
        self.rules_file = rules_file
        self.rules = self._load_rules()
        self.detector = AnomalyDetector()
        self.pending_alerts: List[Dict[str, Any]] = []

    def _load_rules(self) -> Dict[str, Any]:
        """Load alert rules from JSON"""
        try:
            with open(self.rules_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Alert rules file not found: {self.rules_file}")
            return {}

    def evaluate_alerts(self, anomalies: List[AnomalyAlert]) -> List[Dict[str, Any]]:
        """Evaluate anomalies against alert rules"""
        alerts = []

        for anomaly in anomalies:
            # Find matching rule
            matching_rule = None
            for rule in self.rules.get("alert_rules", []):
                if rule["type"] == anomaly.anomaly_type and rule["severity"] == anomaly.severity:
                    matching_rule = rule
                    break

            if matching_rule:
                alert = {
                    "rule_id": matching_rule["id"],
                    "rule_name": matching_rule["name"],
                    "severity": anomaly.severity,
                    "practice": anomaly.practice,
                    "metric": anomaly.metric,
                    "message": anomaly.message,
                    "timestamp": anomaly.timestamp,
                    "routing": matching_rule["routing"],
                    "scope": matching_rule["scope"],
                    "current_value": anomaly.current_value,
                    "threshold": anomaly.threshold,
                }
                alerts.append(alert)

        return alerts

    def route_alerts(self, alerts: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Route alerts to appropriate handlers based on rules"""
        routing_rules = self.rules.get("routing_rules", {})
        routed = {"escalation": [], "alert": [], "info": []}

        for alert in alerts:
            routing_type = alert["routing"]

            if routing_type in routed:
                routed[routing_type].append(alert)
                logger.info(f"Routed '{alert['rule_name']}' to {routing_type}")

        return routed

    def send_to_mailbox(self, alerts: List[Dict[str, Any]]):
        """Send alerts to Empirica mailbox"""
        if not alerts:
            return

        for alert in alerts:
            # Create mailbox entry
            mailbox_content = {
                "type": f"alert/{alert['severity']}",
                "title": alert["rule_name"],
                "practice": alert["practice"],
                "message": alert["message"],
                "metric": alert["metric"],
                "current_value": alert["current_value"],
                "threshold": alert["threshold"],
                "timestamp": alert["timestamp"],
            }

            try:
                # This would integrate with empirica mailbox system
                logger.info(f"Alert sent to mailbox: {alert['rule_name']} for {alert['practice']}")
                self.pending_alerts.append({
                    "alert": alert,
                    "status": "sent",
                    "sent_at": datetime.now().isoformat(),
                })
            except Exception as e:
                logger.error(f"Failed to send alert to mailbox: {str(e)}")

    def create_escalation(self, alerts: List[Dict[str, Any]]):
        """Create escalation incidents for critical alerts"""
        if not alerts:
            return

        for alert in alerts:
            escalation = {
                "type": "escalation",
                "severity": "critical",
                "source": "analytics_alert_manager",
                "alert_rule": alert["rule_id"],
                "practice": alert["practice"],
                "description": alert["message"],
                "required_action": self._generate_recommendation(alert),
                "timestamp": datetime.now().isoformat(),
            }

            try:
                logger.info(f"Escalation created for: {alert['rule_name']}")
                self.pending_alerts.append({
                    "escalation": escalation,
                    "status": "created",
                    "created_at": datetime.now().isoformat(),
                })
            except Exception as e:
                logger.error(f"Failed to create escalation: {str(e)}")

    def _generate_recommendation(self, alert: Dict[str, Any]) -> str:
        """Generate actionable recommendation based on alert"""
        recommendations = {
            "query_latency": "Optimize queries, check resource utilization, consider increasing Loki retention",
            "ingestion_rate": "Check log producer health, verify network connectivity, inspect Loki ingester logs",
            "coordination_delay": "Investigate SER participant responsiveness, check network latency, verify proposal queue",
            "vector_drift": "Run recalibration on practice vectors, investigate measurement discrepancies",
            "health_degradation": "Perform health diagnosis, check all component statuses, consider rolling restart",
            "trace_correlation": "Verify trace ID propagation, check Jaeger configuration, inspect trace ingestion",
        }

        for key, rec in recommendations.items():
            if key in alert.get("metric", "").lower():
                return rec

        return "Investigate alert and consult observability documentation"

    def get_alert_summary(self) -> Dict[str, Any]:
        """Get summary of all alerts"""
        by_severity = {"critical": 0, "warning": 0, "info": 0}
        by_type = {}
        by_practice = {}

        for alert_entry in self.pending_alerts:
            alert = alert_entry.get("alert") or alert_entry.get("escalation")

            if alert:
                by_severity[alert.get("severity", "info")] += 1

                atype = alert.get("metric", "unknown")
                by_type[atype] = by_type.get(atype, 0) + 1

                practice = alert.get("practice", "unknown")
                by_practice[practice] = by_practice.get(practice, 0) + 1

        return {
            "total_alerts": len(self.pending_alerts),
            "by_severity": by_severity,
            "by_type": by_type,
            "by_practice": by_practice,
            "timestamp": datetime.now().isoformat(),
        }

    def export_alerts(self, filepath: str = "alerts_processed.json"):
        """Export processed alerts to JSON"""
        output = {
            "export_time": datetime.now().isoformat(),
            "alerts": self.pending_alerts,
            "summary": self.get_alert_summary(),
        }

        with open(filepath, 'w') as f:
            json.dump(output, f, indent=2, default=str)

        logger.info(f"Alerts exported to {filepath}")

    def run_alert_cycle(self):
        """Execute complete alert detection -> routing -> escalation cycle"""
        logger.info("Starting alert detection cycle...")

        # Run anomaly detection
        anomalies = self.detector.run_detection()
        logger.info(f"Detected {len(anomalies)} anomalies")

        # Evaluate against alert rules
        alerts = self.evaluate_alerts(anomalies)
        logger.info(f"Generated {len(alerts)} alerts")

        # Route alerts
        routed = self.route_alerts(alerts)

        # Send to mailbox
        self.send_to_mailbox(routed.get("alert", []))
        self.send_to_mailbox(routed.get("info", []))

        # Create escalations for critical
        self.create_escalation(routed.get("escalation", []))

        # Export results
        self.export_alerts()

        # Print summary
        summary = self.get_alert_summary()
        logger.info(f"Alert cycle complete:")
        logger.info(f"  Total alerts: {summary['total_alerts']}")
        logger.info(f"  Critical: {summary['by_severity']['critical']}")
        logger.info(f"  Warning: {summary['by_severity']['warning']}")
        logger.info(f"  Info: {summary['by_severity']['info']}")

        return summary


def main():
    manager = AlertManager()
    summary = manager.run_alert_cycle()

    print("\n" + "=" * 60)
    print("Alert Management Cycle Complete")
    print("=" * 60)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
