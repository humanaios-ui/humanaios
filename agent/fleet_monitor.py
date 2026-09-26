#!/usr/bin/env python3
"""
Fleet Monitor — Aggregates Autonomous Agent health across 15 practices

Polls empirica artifact log every interval, extracts agent health findings,
and generates fleet-wide status dashboard + alerts.
"""

import json
import subprocess
import logging
import sys
import time
from typing import Dict, List, Any
from datetime import datetime, timedelta
from dataclasses import dataclass


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger("fleet-monitor")


@dataclass
class AgentHealth:
    practice_name: str
    success_rate: float
    proposals_handled: int
    succeeded: int
    failed: int
    last_report: str
    uptime_hours: float = 0.0


class FleetMonitor:
    """Monitors autonomous agent fleet health"""

    PRACTICES = [
        "empirica-foundation",
        "empirica-autonomy",
        "empirica-mesh-support",
        "empirica-outreach",
        "humanaios",
        "website",
        "empirica-resource-miner",
        "opportunity-aggregator",
        "local-machine-optimizer",
        "acat-x",
        "grok-crossref",
        "integrations-hub",
        "metrics-collector",
        "event-bridge",
        "governance-sync",
    ]

    def __init__(self, poll_interval_seconds: int = 300):
        self.poll_interval = poll_interval_seconds
        self.agent_health: Dict[str, AgentHealth] = {}
        self.deployment_time = datetime.now()

    def poll_agent_health(self) -> Dict[str, AgentHealth]:
        """Poll empirica project-search for agent health findings"""
        cmd = [
            "empirica", "project-search",
            "--task", "Agent health",
            "--scope", "project",
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
                logger.error(f"Project search failed: {result.stderr}")
                return {}

            data = json.loads(result.stdout)
            health_map = {}

            for finding in data.get("findings", []):
                # Parse finding title: "Agent health: empirica-autonomy — 95% success rate"
                title = finding.get("title", "")
                if "Agent health:" in title:
                    parts = title.split(" — ")
                    if len(parts) == 2:
                        practice = parts[0].replace("Agent health: ", "").strip()
                        rate_str = parts[1].replace("% success rate", "").strip()
                        try:
                            success_rate = float(rate_str) / 100
                        except ValueError:
                            continue

                        # Parse description for metrics
                        description = finding.get("description", "")
                        metrics = self._parse_metrics(description)

                        health_map[practice] = AgentHealth(
                            practice_name=practice,
                            success_rate=success_rate,
                            proposals_handled=metrics.get("proposals_handled", 0),
                            succeeded=metrics.get("succeeded", 0),
                            failed=metrics.get("failed", 0),
                            last_report=finding.get("created_at", ""),
                            uptime_hours=self._calculate_uptime()
                        )

            return health_map

        except subprocess.TimeoutExpired:
            logger.error("Project search timeout")
            return {}
        except json.JSONDecodeError:
            logger.error("Failed to parse project search response")
            return {}
        except Exception as e:
            logger.error(f"Error polling agent health: {e}")
            return {}

    def _parse_metrics(self, description: str) -> Dict[str, int]:
        """Extract metrics from agent health description"""
        metrics = {}
        lines = description.split("\n")

        for line in lines:
            if "Proposals handled:" in line:
                try:
                    metrics["proposals_handled"] = int(line.split(":")[1].strip())
                except (ValueError, IndexError):
                    pass
            elif "Succeeded:" in line:
                try:
                    metrics["succeeded"] = int(line.split(":")[1].strip())
                except (ValueError, IndexError):
                    pass
            elif "Failed:" in line:
                try:
                    metrics["failed"] = int(line.split(":")[1].strip())
                except (ValueError, IndexError):
                    pass

        return metrics

    def _calculate_uptime(self) -> float:
        """Calculate uptime since deployment"""
        elapsed = datetime.now() - self.deployment_time
        return elapsed.total_seconds() / 3600  # hours

    def generate_dashboard(self) -> str:
        """Generate fleet-wide status dashboard"""
        self.agent_health = self.poll_agent_health()

        if not self.agent_health:
            return "No agent health data available yet"

        # Calculate fleet metrics
        total_proposals = sum(h.proposals_handled for h in self.agent_health.values())
        total_succeeded = sum(h.succeeded for h in self.agent_health.values())
        total_failed = sum(h.failed for h in self.agent_health.values())

        fleet_success_rate = (
            (total_succeeded / total_proposals * 100)
            if total_proposals > 0
            else 0
        )

        healthy_agents = sum(
            1 for h in self.agent_health.values()
            if h.success_rate >= 0.95
        )

        dashboard = f"""
# Autonomous Agent Fleet Status Dashboard

**Report Time:** {datetime.now().isoformat()}

## Fleet Summary
- **Agents reporting:** {len(self.agent_health)}/{len(self.PRACTICES)}
- **Agents healthy (≥95%):** {healthy_agents}/{len(self.agent_health)}
- **Fleet success rate:** {fleet_success_rate:.1f}%

### Throughput (All Agents Combined)
- Total proposals handled: {total_proposals}
- Total succeeded: {total_succeeded}
- Total failed: {total_failed}

### Uptime
- Deployment started: {self.deployment_time.isoformat()}
- Elapsed: {self._calculate_uptime():.1f}h

---

## Agent Status by Practice

| Practice | Status | Success Rate | Handled | Succeeded | Failed |
|----------|--------|--------------|---------|-----------|--------|
{self._format_agent_table()}

---

## Performance Insights

### Healthy Agents (≥95% success)
{self._format_healthy_agents()}

### Underperforming Agents (<95% success)
{self._format_underperforming_agents()}

### Not Reporting
{self._format_unreporting_agents()}

---

## Alerts

{self._generate_alerts()}

---

**Dashboard generated by:** fleet_monitor.py
**Next update:** {(datetime.now() + timedelta(seconds=self.poll_interval)).isoformat()}
"""
        return dashboard

    def _format_agent_table(self) -> str:
        """Format agent status table"""
        lines = []
        for practice in self.PRACTICES:
            health = self.agent_health.get(practice)
            if health:
                status = "✓" if health.success_rate >= 0.95 else "⚠"
                rate = health.success_rate * 100
                lines.append(
                    f"| {practice:20} | {status:5} | {rate:6.1f}% | {health.proposals_handled:7} | {health.succeeded:9} | {health.failed:6} |"
                )
            else:
                lines.append(
                    f"| {practice:20} | ✗     | N/A    | 0       | 0         | 0      |"
                )
        return "\n".join(lines)

    def _format_healthy_agents(self) -> str:
        """Format list of healthy agents"""
        healthy = [h for h in self.agent_health.values() if h.success_rate >= 0.95]
        if not healthy:
            return "- None yet (still ramping up)"
        return "\n".join([
            f"- **{h.practice_name}**: {h.success_rate*100:.1f}% ({h.succeeded}/{h.proposals_handled})"
            for h in sorted(healthy, key=lambda x: x.success_rate, reverse=True)
        ])

    def _format_underperforming_agents(self) -> str:
        """Format list of underperforming agents"""
        underperforming = [h for h in self.agent_health.values() if h.success_rate < 0.95]
        if not underperforming:
            return "- None (all agents performing well)"
        return "\n".join([
            f"- **{h.practice_name}**: {h.success_rate*100:.1f}% ({h.succeeded}/{h.proposals_handled}) ⚠"
            for h in sorted(underperforming, key=lambda x: x.success_rate)
        ])

    def _format_unreporting_agents(self) -> str:
        """Format list of agents not reporting"""
        reporting = set(self.agent_health.keys())
        not_reporting = set(self.PRACTICES) - reporting
        if not not_reporting:
            return "- None (all agents reporting)"
        return "\n".join([f"- {p}" for p in sorted(not_reporting)])

    def _generate_alerts(self) -> str:
        """Generate alerts for fleet issues"""
        alerts = []

        # Check for high failure rate
        for health in self.agent_health.values():
            if health.success_rate < 0.90:
                alerts.append(
                    f"⚠ **HIGH FAILURE RATE:** {health.practice_name} at {health.success_rate*100:.1f}% (target: ≥95%)"
                )

        # Check for not reporting
        reporting = set(self.agent_health.keys())
        not_reporting = set(self.PRACTICES) - reporting
        if not_reporting:
            practices_list = ", ".join(sorted(not_reporting))
            alerts.append(f"⚠ **NOT REPORTING:** {practices_list}")

        if not alerts:
            return "✓ No alerts — all agents operating nominally"

        return "\n".join([f"- {alert}" for alert in alerts])

    def report_to_cortex(self, dashboard: str) -> bool:
        """Log fleet dashboard as finding to Cortex"""
        cmd = [
            "empirica", "finding-log",
            "--finding", "Autonomous Agent Fleet Health Dashboard",
            "--description", dashboard,
            "--impact", "0.9",
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
                logger.info("✓ Fleet dashboard logged to Cortex")
                return True
            else:
                logger.error(f"Failed to log dashboard: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Error reporting to Cortex: {e}")
            return False

    def run_continuous(self):
        """Run monitoring loop continuously"""
        logger.info(f"Fleet monitor started (poll interval: {self.poll_interval}s)")

        while True:
            try:
                dashboard = self.generate_dashboard()
                print(dashboard)
                print("\n" + "=" * 80 + "\n")

                self.report_to_cortex(dashboard)

                logger.info(f"Waiting {self.poll_interval}s until next poll...")
                time.sleep(self.poll_interval)

            except KeyboardInterrupt:
                logger.info("Fleet monitor stopped")
                break
            except Exception as e:
                logger.error(f"Monitoring loop error: {e}")
                time.sleep(self.poll_interval)


if __name__ == "__main__":
    poll_interval = int(sys.argv[1]) if len(sys.argv) > 1 else 300

    monitor = FleetMonitor(poll_interval_seconds=poll_interval)
    monitor.run_continuous()
