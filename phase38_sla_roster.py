#!/usr/bin/env python3
"""
Phase 3.8: SLA Roster Completion
Defines SLAs for all 17 foundation practices
"""

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

@dataclass
class PracticeSLA:
    """SLA definition for a practice"""
    practice_name: str
    query_latency_p95_ms: float
    query_latency_p99_ms: float
    ingestion_rate_min_cps: float
    coordination_latency_p95_s: float
    health_score_min: float
    trace_correlation_min: float
    escalation_response_minutes: int
    critical_response_minutes: int

    def to_dict(self):
        return {
            "practice_name": self.practice_name,
            "query_latency_p95_ms": self.query_latency_p95_ms,
            "query_latency_p99_ms": self.query_latency_p99_ms,
            "ingestion_rate_min_cps": self.ingestion_rate_min_cps,
            "coordination_latency_p95_s": self.coordination_latency_p95_s,
            "health_score_min": self.health_score_min,
            "trace_correlation_min": self.trace_correlation_min,
            "escalation_response_minutes": self.escalation_response_minutes,
            "critical_response_minutes": self.critical_response_minutes
        }

class SLARosterBuilder:
    """Builds complete SLA roster for all practices"""

    PRACTICES = [
        # Core foundation (9)
        "empirica-autonomy",
        "empirica-mesh-support",
        "empirica-outreach",
        "empirica-foundation-evaluator",
        "empirica-analytics",
        "empirica-resource-miner",
        "empirica-temporal-oracle",
        "humanaios",
        "website",
        # Extended foundation (8)
        "acat-x",
        "collaborator-ops",
        "flta-app-empirica",
        "grok-crossref",
        "humanaios-internal",
        "humanaios-ui",
        "local-machine-optimizer",
        "opportunity-aggregator"
    ]

    def __init__(self):
        self.slas: Dict[str, PracticeSLA] = {}
        self.sla_file = Path("analytics/sla_roster_complete.json")
        self._define_slas()

    def _define_slas(self):
        """Define SLAs for all 17 practices"""

        slas = [
            # CORE FOUNDATION (Tier 1) - Strictest SLAs
            PracticeSLA(
                practice_name="empirica-autonomy",
                query_latency_p95_ms=1000,
                query_latency_p99_ms=1500,
                ingestion_rate_min_cps=10,
                coordination_latency_p95_s=5,
                health_score_min=0.75,
                trace_correlation_min=0.95,
                escalation_response_minutes=5,
                critical_response_minutes=2
            ),
            PracticeSLA(
                practice_name="empirica-mesh-support",
                query_latency_p95_ms=1500,
                query_latency_p99_ms=2000,
                ingestion_rate_min_cps=20,
                coordination_latency_p95_s=10,
                health_score_min=0.70,
                trace_correlation_min=0.90,
                escalation_response_minutes=10,
                critical_response_minutes=5
            ),
            PracticeSLA(
                practice_name="empirica-foundation-evaluator",
                query_latency_p95_ms=1200,
                query_latency_p99_ms=1800,
                ingestion_rate_min_cps=15,
                coordination_latency_p95_s=8,
                health_score_min=0.75,
                trace_correlation_min=0.95,
                escalation_response_minutes=5,
                critical_response_minutes=2
            ),
            PracticeSLA(
                practice_name="empirica-outreach",
                query_latency_p95_ms=2000,
                query_latency_p99_ms=3000,
                ingestion_rate_min_cps=5,
                coordination_latency_p95_s=15,
                health_score_min=0.70,
                trace_correlation_min=0.90,
                escalation_response_minutes=15,
                critical_response_minutes=10
            ),

            # ANALYTICS & INFRASTRUCTURE (Tier 2)
            PracticeSLA(
                practice_name="empirica-analytics",
                query_latency_p95_ms=1500,
                query_latency_p99_ms=2500,
                ingestion_rate_min_cps=20,
                coordination_latency_p95_s=10,
                health_score_min=0.70,
                trace_correlation_min=0.90,
                escalation_response_minutes=10,
                critical_response_minutes=5
            ),
            PracticeSLA(
                practice_name="empirica-resource-miner",
                query_latency_p95_ms=2000,
                query_latency_p99_ms=3000,
                ingestion_rate_min_cps=8,
                coordination_latency_p95_s=12,
                health_score_min=0.65,
                trace_correlation_min=0.85,
                escalation_response_minutes=20,
                critical_response_minutes=10
            ),
            PracticeSLA(
                practice_name="empirica-temporal-oracle",
                query_latency_p95_ms=2000,
                query_latency_p99_ms=3000,
                ingestion_rate_min_cps=10,
                coordination_latency_p95_s=15,
                health_score_min=0.65,
                trace_correlation_min=0.85,
                escalation_response_minutes=20,
                critical_response_minutes=10
            ),

            # HUMANAIOS ECOSYSTEM (Tier 2)
            PracticeSLA(
                practice_name="humanaios",
                query_latency_p95_ms=1800,
                query_latency_p99_ms=2500,
                ingestion_rate_min_cps=12,
                coordination_latency_p95_s=10,
                health_score_min=0.70,
                trace_correlation_min=0.90,
                escalation_response_minutes=10,
                critical_response_minutes=5
            ),
            PracticeSLA(
                practice_name="humanaios-internal",
                query_latency_p95_ms=2000,
                query_latency_p99_ms=3000,
                ingestion_rate_min_cps=8,
                coordination_latency_p95_s=12,
                health_score_min=0.65,
                trace_correlation_min=0.85,
                escalation_response_minutes=15,
                critical_response_minutes=10
            ),
            PracticeSLA(
                practice_name="humanaios-ui",
                query_latency_p95_ms=1500,
                query_latency_p99_ms=2000,
                ingestion_rate_min_cps=10,
                coordination_latency_p95_s=8,
                health_score_min=0.70,
                trace_correlation_min=0.90,
                escalation_response_minutes=10,
                critical_response_minutes=5
            ),

            # EXTENDED FOUNDATION (Tier 3) - Relaxed SLAs
            PracticeSLA(
                practice_name="website",
                query_latency_p95_ms=3000,
                query_latency_p99_ms=4000,
                ingestion_rate_min_cps=5,
                coordination_latency_p95_s=20,
                health_score_min=0.60,
                trace_correlation_min=0.80,
                escalation_response_minutes=30,
                critical_response_minutes=15
            ),
            PracticeSLA(
                practice_name="acat-x",
                query_latency_p95_ms=2500,
                query_latency_p99_ms=3500,
                ingestion_rate_min_cps=10,
                coordination_latency_p95_s=15,
                health_score_min=0.65,
                trace_correlation_min=0.85,
                escalation_response_minutes=20,
                critical_response_minutes=10
            ),
            PracticeSLA(
                practice_name="collaborator-ops",
                query_latency_p95_ms=2500,
                query_latency_p99_ms=3500,
                ingestion_rate_min_cps=8,
                coordination_latency_p95_s=15,
                health_score_min=0.65,
                trace_correlation_min=0.85,
                escalation_response_minutes=20,
                critical_response_minutes=10
            ),
            PracticeSLA(
                practice_name="flta-app-empirica",
                query_latency_p95_ms=2500,
                query_latency_p99_ms=3500,
                ingestion_rate_min_cps=10,
                coordination_latency_p95_s=15,
                health_score_min=0.65,
                trace_correlation_min=0.85,
                escalation_response_minutes=20,
                critical_response_minutes=10
            ),
            PracticeSLA(
                practice_name="grok-crossref",
                query_latency_p95_ms=2000,
                query_latency_p99_ms=3000,
                ingestion_rate_min_cps=10,
                coordination_latency_p95_s=15,
                health_score_min=0.70,
                trace_correlation_min=0.90,
                escalation_response_minutes=15,
                critical_response_minutes=10
            ),
            PracticeSLA(
                practice_name="local-machine-optimizer",
                query_latency_p95_ms=3000,
                query_latency_p99_ms=4000,
                ingestion_rate_min_cps=5,
                coordination_latency_p95_s=20,
                health_score_min=0.60,
                trace_correlation_min=0.80,
                escalation_response_minutes=30,
                critical_response_minutes=15
            ),
            PracticeSLA(
                practice_name="opportunity-aggregator",
                query_latency_p95_ms=2500,
                query_latency_p99_ms=3500,
                ingestion_rate_min_cps=8,
                coordination_latency_p95_s=15,
                health_score_min=0.65,
                trace_correlation_min=0.85,
                escalation_response_minutes=20,
                critical_response_minutes=10
            ),
        ]

        for sla in slas:
            self.slas[sla.practice_name] = sla

    def generate_roster(self) -> Dict[str, Any]:
        """Generate complete SLA roster"""

        roster = {
            "timestamp": datetime.now().isoformat(),
            "total_practices": len(self.slas),
            "tier_1_core": 4,
            "tier_2_extended": 5,
            "tier_3_ecosystem": 8,
            "slas": {}
        }

        for practice_name, sla in self.slas.items():
            roster["slas"][practice_name] = sla.to_dict()

        return roster

    def save_roster(self, roster: Dict[str, Any]):
        """Save roster to file"""
        with open(self.sla_file, "w") as f:
            json.dump({
                "phase": "3.8",
                "export_time": datetime.now().isoformat(),
                "roster": roster,
                "summary": {
                    "total_practices": roster["total_practices"],
                    "tier_1_core": roster["tier_1_core"],
                    "tier_2_extended": roster["tier_2_extended"],
                    "tier_3_ecosystem": roster["tier_3_ecosystem"],
                    "all_practices_covered": len(self.slas) == len(self.PRACTICES)
                }
            }, f, indent=2)

def main():
    """Build complete SLA roster"""

    print("🚀 Phase 3.8: SLA Roster Completion")
    print("=" * 60)

    builder = SLARosterBuilder()
    roster = builder.generate_roster()
    builder.save_roster(roster)

    print(f"\n✅ Complete SLA Roster Generated")
    print(f"  Total practices: {roster['total_practices']}")
    print(f"  Tier 1 (Core): {roster['tier_1_core']} practices")
    print(f"  Tier 2 (Extended): {roster['tier_2_extended']} practices")
    print(f"  Tier 3 (Ecosystem): {roster['tier_3_ecosystem']} practices")

    print(f"\n📋 Practices by Tier:")

    tier1 = ["empirica-autonomy", "empirica-mesh-support", "empirica-foundation-evaluator", "empirica-outreach"]
    tier2 = ["empirica-analytics", "empirica-resource-miner", "empirica-temporal-oracle", "humanaios", "humanaios-ui"]
    tier3 = [p for p in roster["slas"].keys() if p not in tier1 + tier2]

    print(f"\n  Tier 1 (Strictest SLAs):")
    for p in tier1:
        sla = roster["slas"][p]
        print(f"    {p}: p95={sla['query_latency_p95_ms']}ms, response={sla['critical_response_minutes']}min")

    print(f"\n  Tier 2 (Standard SLAs):")
    for p in tier2:
        sla = roster["slas"][p]
        print(f"    {p}: p95={sla['query_latency_p95_ms']}ms, response={sla['critical_response_minutes']}min")

    print(f"\n  Tier 3 (Relaxed SLAs):")
    for p in tier3:
        sla = roster["slas"][p]
        print(f"    {p}: p95={sla['query_latency_p95_ms']}ms, response={sla['critical_response_minutes']}min")

if __name__ == "__main__":
    main()
