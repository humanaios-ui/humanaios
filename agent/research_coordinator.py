#!/usr/bin/env python3
"""
Research Coordinator Practice — Aggregation + Pattern Detection

Runs in the empirica-research-coordinator practice (evaluator seat).
Polls evaluator inbox for research proposals, aggregates findings from all 15 practices,
detects cross-practice patterns, routes research tasks to specialized research practices.
"""

import json
import subprocess
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s'
)


@dataclass
class ResearchProposal:
    id: str
    source_claude: str
    title: str
    research_domain: str
    priority: int
    payload: Dict[str, Any]


@dataclass
class Finding:
    practice_ai_id: str
    finding_id: str
    content: str
    impact: float
    timestamp: str


@dataclass
class Pattern:
    pattern_name: str
    affected_practices: List[str]
    frequency: int
    severity: float
    recommendation: str


class FindingAggregator:
    """Collects findings from all 15 practices"""

    def __init__(self):
        self.findings_by_practice: Dict[str, List[Finding]] = defaultdict(list)
        self.logger = logging.getLogger("aggregator")
        self.last_sync = None

    def aggregate_findings(self) -> Dict[str, List[Finding]]:
        """Query Cortex for recent findings from all practices"""
        self.logger.info("Aggregating findings from all 15 practices")

        cmd = [
            "empirica", "project-search",
            "--task", "recent findings across all practices",
            "--global",
            "--output", "json"
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                self.logger.error(f"Finding aggregation failed: {result.stderr}")
                return {}

            data = json.loads(result.stdout)
            findings = data.get("findings", [])

            for finding in findings:
                practice = finding.get("source_practice", "unknown")
                f = Finding(
                    practice_ai_id=practice,
                    finding_id=finding.get("id", ""),
                    content=finding.get("content", ""),
                    impact=float(finding.get("impact", 0.5)),
                    timestamp=finding.get("created_at", "")
                )
                self.findings_by_practice[practice].append(f)

            self.last_sync = datetime.now()
            self.logger.info(f"Aggregated {len(findings)} findings from {len(self.findings_by_practice)} practices")
            return self.findings_by_practice

        except Exception as e:
            self.logger.error(f"Error aggregating findings: {e}")
            return {}


class PatternDetector:
    """Detects cross-practice patterns in findings"""

    def __init__(self):
        self.logger = logging.getLogger("detector")
        self.known_patterns: Dict[str, Pattern] = {}

    def detect_patterns(self, findings_by_practice: Dict[str, List[Finding]]) -> List[Pattern]:
        """Analyze findings for cross-practice patterns"""
        self.logger.info("Detecting patterns across practices")

        patterns = []

        # Pattern 1: High-impact findings affecting multiple practices
        high_impact_by_content = defaultdict(list)
        for practice, findings in findings_by_practice.items():
            for finding in findings:
                if finding.impact >= 0.7:
                    high_impact_by_content[finding.content[:100]].append(practice)

        for content_key, practices in high_impact_by_content.items():
            if len(practices) >= 3:  # Affects 3+ practices
                pattern = Pattern(
                    pattern_name=f"High-impact finding (>{len(practices)} practices)",
                    affected_practices=practices,
                    frequency=len(practices),
                    severity=0.8,
                    recommendation=f"Research: Why does {content_key} affect {len(practices)} practices?"
                )
                patterns.append(pattern)

        # Pattern 2: Temporal clustering (many findings at same time)
        findings_by_time = defaultdict(list)
        for practice, findings in findings_by_practice.items():
            for finding in findings:
                # Bucket by hour
                dt = datetime.fromisoformat(finding.timestamp.replace('Z', '+00:00'))
                hour_key = dt.strftime("%Y-%m-%d %H:00")
                findings_by_time[hour_key].append(finding)

        for time_key, findings in findings_by_time.items():
            if len(findings) >= 10:  # 10+ findings in one hour
                practices = set(f.practice_ai_id for f in findings)
                pattern = Pattern(
                    pattern_name=f"Temporal spike ({len(findings)} findings in {time_key})",
                    affected_practices=list(practices),
                    frequency=len(findings),
                    severity=0.6,
                    recommendation=f"Research: Why the spike at {time_key}?"
                )
                patterns.append(pattern)

        self.logger.info(f"Detected {len(patterns)} patterns")
        return patterns

    def suggest_research(self, patterns: List[Pattern]) -> List[str]:
        """Generate research suggestions from patterns"""
        suggestions = []
        for pattern in patterns:
            suggestions.append(f"Pattern '{pattern.pattern_name}' affecting {len(pattern.affected_practices)} practices: {pattern.recommendation}")
        return suggestions


class ResearchRouter:
    """Routes research tasks to specialized research practices"""

    # Map research domains to research practices
    RESEARCH_PRACTICE_MAP = {
        "resources": "empirica-foundation.carly.empirica-resource-miner",
        "temporal": "empirica-foundation.carly.empirica-temporal-oracle",
        "analytics": "empirica-foundation.carly.empirica-analytics",
        "opportunities": "empirica-foundation.carly.opportunity-aggregator",
        "optimization": "empirica-foundation.carly.local-machine-optimizer"
    }

    def __init__(self):
        self.logger = logging.getLogger("router")

    def route_research_task(self, proposal: ResearchProposal) -> bool:
        """Route a research proposal to the appropriate practice"""
        domain = proposal.research_domain.lower()
        target_practice = self.RESEARCH_PRACTICE_MAP.get(domain)

        if not target_practice:
            self.logger.warning(f"Unknown research domain: {domain}")
            return False

        self.logger.info(f"Routing research to {target_practice}: {proposal.title}")

        # In a full implementation, would send via cortex_propose
        # For now, log the routing decision
        self.logger.debug(f"Would send proposal {proposal.id} to {target_practice}")
        return True


class CortexPublisher:
    """Publishes research findings + patterns back to Cortex"""

    def __init__(self, practice_ai_id: str):
        self.ai_id = practice_ai_id
        self.logger = logging.getLogger("publisher")

    def publish_pattern_finding(self, pattern: Pattern) -> bool:
        """Log a detected pattern as a shared Cortex finding"""
        description = f"""
## Cross-Practice Pattern Detected

**Pattern:** {pattern.pattern_name}

**Affected Practices ({len(pattern.affected_practices)}):**
{', '.join(pattern.affected_practices)}

**Frequency:** {pattern.frequency} occurrences
**Severity:** {pattern.severity:.1%}

**Recommendation:**
{pattern.recommendation}

---
*Detected by ResearchCoordinator at {datetime.now().isoformat()}*
"""

        cmd = [
            "empirica", "finding-log",
            "--finding", f"Research Pattern: {pattern.pattern_name}",
            "--description", description,
            "--impact", str(pattern.severity),
            "--visibility", "shared",
            "--epistemic-source", "search"
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.logger.info(f"✓ Published pattern: {pattern.pattern_name}")
                return True
            else:
                self.logger.error(f"Failed to publish pattern: {result.stderr}")
                return False
        except Exception as e:
            self.logger.error(f"Error publishing pattern: {e}")
            return False

    def publish_research_suggestion(self, suggestion: str) -> bool:
        """Log a research suggestion as an unknown"""
        cmd = [
            "empirica", "unknown-log",
            "--unknown", suggestion,
            "--description", f"Auto-detected research opportunity from pattern analysis",
            "--epistemic-source", "search"
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.logger.info(f"✓ Logged research suggestion")
                return True
            else:
                self.logger.error(f"Failed to log suggestion: {result.stderr}")
                return False
        except Exception as e:
            self.logger.error(f"Error logging suggestion: {e}")
            return False


class ResearchCoordinator:
    """Main coordinator loop for research orchestration"""

    def __init__(
        self,
        ai_id: str,
        poll_interval_seconds: int = 300  # 5 minutes for research cycle
    ):
        self.ai_id = ai_id
        self.poll_interval = poll_interval_seconds

        self.logger = logging.getLogger("coordinator")
        self.aggregator = FindingAggregator()
        self.detector = PatternDetector()
        self.router = ResearchRouter()
        self.publisher = CortexPublisher(ai_id)

        self.stats = {
            "research_proposals_received": 0,
            "research_proposals_routed": 0,
            "patterns_detected": 0,
            "patterns_published": 0,
            "poll_cycles": 0,
            "last_poll": None
        }

    def poll_research_inbox(self) -> List[ResearchProposal]:
        """Poll evaluator inbox for research proposals"""
        cmd = [
            "empirica", "mailbox", "poll",
            "--ai-id", self.ai_id,
            "--status", "accepted",
            "--output", "json"
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                self.logger.error(f"Mailbox poll failed: {result.stderr}")
                return []

            data = json.loads(result.stdout)
            proposals = []

            for prop in data.get("proposals", []):
                if prop.get("type") == "research_task":
                    proposals.append(ResearchProposal(
                        id=prop.get("id"),
                        source_claude=prop.get("source_claude", ""),
                        title=prop.get("title", ""),
                        research_domain=prop.get("payload", {}).get("domain", "general"),
                        priority=int(prop.get("payload", {}).get("priority", 5)),
                        payload=prop.get("payload", {})
                    ))

            return proposals

        except Exception as e:
            self.logger.error(f"Error polling research inbox: {e}")
            return []

    def execute_research_cycle(self):
        """Execute one full research coordination cycle"""
        self.stats["poll_cycles"] += 1
        self.stats["last_poll"] = datetime.now().isoformat()

        self.logger.info(f"=== Research Cycle {self.stats['poll_cycles']} ===")

        # Phase 1: Poll for research proposals
        proposals = self.poll_research_inbox()
        self.stats["research_proposals_received"] += len(proposals)
        self.logger.info(f"Received {len(proposals)} research proposals")

        # Phase 2: Route research tasks
        for proposal in proposals:
            if self.router.route_research_task(proposal):
                self.stats["research_proposals_routed"] += 1

        # Phase 3: Aggregate findings from all practices
        findings_by_practice = self.aggregator.aggregate_findings()

        # Phase 4: Detect patterns
        patterns = self.detector.detect_patterns(findings_by_practice)
        self.stats["patterns_detected"] += len(patterns)

        # Phase 5: Publish patterns + suggestions
        for pattern in patterns:
            if self.publisher.publish_pattern_finding(pattern):
                self.stats["patterns_published"] += 1

        # Phase 6: Publish research suggestions
        suggestions = self.detector.suggest_research(patterns)
        for suggestion in suggestions:
            self.publisher.publish_research_suggestion(suggestion)

        self.logger.info(f"Cycle complete: {len(proposals)} proposals, {len(patterns)} patterns, {len(suggestions)} suggestions")

    def run(self, max_cycles: Optional[int] = None):
        """Run the coordinator loop"""
        self.logger.info(f"ResearchCoordinator started for {self.ai_id}")

        cycle_count = 0
        while max_cycles is None or cycle_count < max_cycles:
            try:
                self.execute_research_cycle()
                cycle_count += 1
                self.logger.debug(f"Sleeping for {self.poll_interval}s until next cycle")
                import time
                time.sleep(self.poll_interval)

            except KeyboardInterrupt:
                self.logger.info("Coordinator stopped by user")
                break

            except Exception as e:
                self.logger.error(f"Cycle error: {e}")
                import time
                time.sleep(min(self.poll_interval * 2, 600))

    def get_stats(self) -> Dict[str, Any]:
        """Return current coordinator statistics"""
        return self.stats.copy()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: research_coordinator.py <ai_id> [poll_interval_seconds]")
        sys.exit(1)

    ai_id = sys.argv[1]
    poll_interval = int(sys.argv[2]) if len(sys.argv) > 2 else 300

    coordinator = ResearchCoordinator(ai_id, poll_interval_seconds=poll_interval)
    coordinator.run()
