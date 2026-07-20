#!/usr/bin/env python3
"""
Consciousness-Aligned Guidance System v1.0

Core engine for matching a person's consciousness level to appropriate wisdom teachings
and showing cross-tradition parallels.

Architecture:
- WisdomDatabase: Loads v0.2 JSON schema
- ConsciousnessLevel: Represents 0-1000 Hawkins scale with tier classification
- GuidanceQuery: Takes level + optional constraint (tradition, obstacle, theme)
- GuidanceResponse: Returns teaching + parallels + next-level pathway

Usage:
  guidance = ConsciousnessGuidanceEngine(wisdom_db_path)
  response = guidance.query(level=50, tradition=None, obstacle="powerlessness")
  print(response.formatted())
"""

import json
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
from enum import Enum


class ConsciousnessZone(Enum):
    """Hawkins consciousness level zones"""
    POWER_LOSS = (0, 50)  # Shame, guilt, apathy
    LOWER_POWER = (50, 200)  # Fear, desire, anger, pride
    POWER = (200, 350)  # Courage, neutrality
    HIGHER_POWER = (350, 600)  # Willingness, acceptance, love, joy
    TRUTH_REVEALING = (600, 700)  # Peace, enlightenment
    TRANSCENDENT = (700, 1000)  # Beyond calibration

    @classmethod
    def from_level(cls, level: int):
        """Get zone for a consciousness level"""
        for zone in cls:
            if zone.value[0] <= level < zone.value[1]:
                return zone
        return cls.TRANSCENDENT


@dataclass
class TeachingMatch:
    """A matched teaching with metadata"""
    system: str
    unit_id: str
    title: str
    sequence: int
    zone: str
    key_concepts: List[str]
    calibration_level: Tuple[int, int]
    application_practice: str
    parallels: List[Dict]  # Cross-tradition parallels

    def to_dict(self):
        return {
            "system": self.system,
            "unit_id": self.unit_id,
            "title": self.title,
            "sequence": self.sequence,
            "zone": self.zone,
            "key_concepts": self.key_concepts,
            "calibration_level": self.calibration_level,
            "application_practice": self.application_practice,
            "parallels": self.parallels,
        }


@dataclass
class GuidanceResponse:
    """Response from guidance query"""
    user_level: int
    user_zone: str
    primary_teaching: TeachingMatch
    next_level_pathway: Optional[TeachingMatch]
    supporting_teachings: List[TeachingMatch]
    zone_interpretation: str

    def formatted(self) -> str:
        """Format as readable guidance"""
        output = []
        output.append("=" * 70)
        output.append(f"CONSCIOUSNESS-ALIGNED GUIDANCE | Level {self.user_level} ({self.user_zone})")
        output.append("=" * 70)
        output.append("")

        output.append("YOUR CURRENT TEACHING:")
        output.append(f"  System: {self.primary_teaching.system}")
        output.append(f"  Teaching: {self.primary_teaching.title}")
        output.append(f"  Concepts: {', '.join(self.primary_teaching.key_concepts)}")
        output.append(f"  Practice: {self.primary_teaching.application_practice}")
        output.append("")

        output.append("HOW OTHER TRADITIONS ADDRESS THIS LEVEL:")
        for parallel in self.primary_teaching.parallels:
            output.append(f"  • {parallel['system']}: {parallel['concept']}")
            output.append(f"    └─ {parallel['reason']}")
        output.append("")

        if self.next_level_pathway:
            output.append("WHEN YOU'RE READY FOR THE NEXT STEP:")
            output.append(f"  Level: {self.next_level_pathway.calibration_level[0]}-{self.next_level_pathway.calibration_level[1]}")
            output.append(f"  Teaching: {self.next_level_pathway.title} ({self.next_level_pathway.system})")
            output.append("")

        output.append("ZONE INTERPRETATION:")
        output.append(f"  {self.zone_interpretation}")
        output.append("")
        output.append("=" * 70)

        return "\n".join(output)

    def to_dict(self):
        return {
            "user_level": self.user_level,
            "user_zone": self.user_zone,
            "primary_teaching": self.primary_teaching.to_dict(),
            "next_level_pathway": self.next_level_pathway.to_dict() if self.next_level_pathway else None,
            "supporting_teachings": [t.to_dict() for t in self.supporting_teachings],
            "zone_interpretation": self.zone_interpretation,
        }


class ConsciousnessGuidanceEngine:
    """Core guidance engine"""

    ZONE_INTERPRETATIONS = {
        "POWER_LOSS": (
            "You're at the recognition phase. The good news: you've acknowledged "
            "where you are. This is the only place real change can begin. "
            "The teaching at this level helps you see that powerlessness is NOT "
            "permanent—it's the starting point for awakening."
        ),
        "LOWER_POWER": (
            "You're in active transformation. Fear, desire, and anger are signs "
            "that energy is moving upward. These emotions have intelligence; "
            "use them as fuel. The teaching at this level helps you channel "
            "that energy toward growth rather than destruction."
        ),
        "POWER": (
            "You're developing self-direction. Courage and neutrality mean you "
            "can see clearly and act decisively. The teaching at this level "
            "teaches you to master your own mind and life."
        ),
        "HIGHER_POWER": (
            "You're integrating wisdom. Willingness and love mean you're opening "
            "to something larger than yourself. The teaching at this level teaches "
            "you to serve and transmit what you've learned."
        ),
        "TRUTH_REVEALING": (
            "You're touching ultimate reality. Peace and enlightenment mean the "
            "boundaries between self and world are dissolving. The teaching at "
            "this level points to what cannot be spoken."
        ),
        "TRANSCENDENT": (
            "You're beyond the scale. This is the realm of saints, enlightened "
            "masters, avatars. The teaching here is lived, not spoken."
        ),
    }

    def __init__(self, wisdom_db_path: str):
        """Load wisdom database"""
        with open(wisdom_db_path, 'r') as f:
            self.db = json.load(f)
        self._build_indices()

    def _build_indices(self):
        """Build searchable indices of teachings"""
        self.teachings_by_level = {}
        self.teachings_by_system = {}
        self.teachings_by_zone = {}

        for system_name, system_data in self.db["systems"].items():
            if "units" not in system_data:
                continue

            self.teachings_by_system[system_name] = []

            for unit_id, unit_data in system_data["units"].items():
                calibration = unit_data.get("metadata", {}).get("calibration_level", None) or \
                              self._infer_calibration(system_name, unit_data.get("sequence", 0))

                zone = unit_data.get("metadata", {}).get("zone", "unknown")

                if zone not in self.teachings_by_zone:
                    self.teachings_by_zone[zone] = []

                teaching = {
                    "system": system_name,
                    "unit_id": unit_id,
                    "data": unit_data,
                    "calibration_level": calibration,
                    "zone": zone,
                }

                self.teachings_by_system[system_name].append(teaching)
                self.teachings_by_zone[zone].append(teaching)

                # Index by level range
                if isinstance(calibration, tuple):
                    for level in range(calibration[0], calibration[1] + 1, 50):
                        if level not in self.teachings_by_level:
                            self.teachings_by_level[level] = []
                        self.teachings_by_level[level].append(teaching)

    def _infer_calibration(self, system: str, sequence: int) -> Tuple[int, int]:
        """Infer calibration level based on system and sequence"""
        calibrations = {
            "aa_12_steps": [(0, 100), (100, 200), (200, 300), (300, 400), (400, 500),
                           (500, 600), (600, 700), (700, 800), (800, 900), (900, 950), (950, 975), (975, 1000)],
            "aa_12_traditions": [(350, 400)] * 12,
            "hawkins_map": [(i * 60, (i + 1) * 60) for i in range(17)],
            "words_of_jesus": [(200, 300)] * 12 + [(300, 400)] * 8 + [(400, 500)] * 6 + [(500, 600)] * 3,
            "buddhist_core_teachings": [(200, 300)] * 6 + [(300, 400)] * 8 + [(400, 500)] * 8 + [(500, 600)] * 4,
            "freemasonry_degrees": [(200, 300)] * 10 + [(300, 400)] * 10 + [(400, 500)] * 10,
        }
        if system in calibrations and sequence - 1 < len(calibrations[system]):
            return calibrations[system][sequence - 1]
        return (300, 500)  # Default

    def query(self, level: int, tradition: Optional[str] = None, obstacle: Optional[str] = None) -> GuidanceResponse:
        """
        Query the guidance system.

        Args:
            level: Consciousness level 0-1000
            tradition: Optional specific tradition to focus on (aa_12_steps, hawkins_map, etc.)
            obstacle: Optional obstacle/challenge to address (powerlessness, anger, etc.)

        Returns:
            GuidanceResponse with primary teaching and parallels
        """
        # Clamp level to valid range
        level = max(0, min(1000, level))

        # Find closest zone
        zone = ConsciousnessZone.from_level(level)

        # Find primary teaching
        primary = self._find_best_teaching(level, tradition, zone)

        # Find next-level teaching
        next_level = self._find_next_level_teaching(level, zone)

        # Find supporting teachings from other traditions
        supporting = self._find_supporting_teachings(level, zone, exclude_system=primary["system"])

        # Build response
        response = GuidanceResponse(
            user_level=level,
            user_zone=zone.name,
            primary_teaching=self._teaching_to_match(primary),
            next_level_pathway=self._teaching_to_match(next_level) if next_level else None,
            supporting_teachings=[self._teaching_to_match(t) for t in supporting[:3]],
            zone_interpretation=self.ZONE_INTERPRETATIONS.get(zone.name, ""),
        )

        return response

    def _find_best_teaching(self, level: int, tradition: Optional[str], zone: ConsciousnessZone):
        """Find the most appropriate teaching for this level"""
        candidates = []

        if tradition:
            if tradition in self.teachings_by_system:
                candidates = self.teachings_by_system[tradition]
        else:
            # Search across all systems
            for system_teachings in self.teachings_by_system.values():
                candidates.extend(system_teachings)

        # Filter by zone
        candidates = [t for t in candidates if t["zone"] == zone.name]

        if not candidates:
            # Fallback: get closest by calibration
            candidates = [t for t in [item for items in self.teachings_by_system.values() for item in items]
                         if isinstance(t["calibration_level"], tuple) and
                         t["calibration_level"][0] <= level <= t["calibration_level"][1]]

        if not candidates:
            # Ultimate fallback
            return self.teachings_by_system[list(self.teachings_by_system.keys())[0]][0]

        # Return first candidate (could be randomized or scored)
        return candidates[0]

    def _find_next_level_teaching(self, level: int, zone: ConsciousnessZone):
        """Find the teaching for the next consciousness level"""
        zones = list(ConsciousnessZone)
        current_idx = zones.index(zone)

        if current_idx >= len(zones) - 1:
            return None  # Already at top

        next_zone = zones[current_idx + 1]
        candidates = self.teachings_by_zone.get(next_zone.name, [])

        return candidates[0] if candidates else None

    def _find_supporting_teachings(self, level: int, zone: ConsciousnessZone, exclude_system: str = None):
        """Find 2-3 teachings from other traditions at same level"""
        candidates = self.teachings_by_zone.get(zone.name, [])

        if exclude_system:
            candidates = [t for t in candidates if t["system"] != exclude_system]

        # Prefer diversity (one from each tradition)
        by_system = {}
        for teaching in candidates:
            if teaching["system"] not in by_system:
                by_system[teaching["system"]] = teaching

        return list(by_system.values())

    def _teaching_to_match(self, teaching: Dict) -> TeachingMatch:
        """Convert teaching dict to TeachingMatch"""
        unit_data = teaching["data"]
        relationships = unit_data.get("relationships", {})
        parallels_raw = relationships.get("parallels_in_other_systems", [])

        # Normalize parallels to expected format
        parallels = []
        for p in parallels_raw:
            if isinstance(p, dict):
                # Extract concept or use defaults
                concept = p.get("concept", p.get("system", "Unknown concept"))
                reason = p.get("reason", "Related teaching")
                system = p.get("system", "Unknown system")
                parallels.append({
                    "system": system,
                    "concept": concept,
                    "reason": reason
                })

        return TeachingMatch(
            system=teaching["system"],
            unit_id=teaching["unit_id"],
            title=unit_data.get("title", "Unknown"),
            sequence=unit_data.get("sequence", 0),
            zone=teaching["zone"],
            key_concepts=unit_data.get("metadata", {}).get("key_concepts", []),
            calibration_level=teaching["calibration_level"],
            application_practice=unit_data.get("application", {}).get("practice", "Contemplative practice"),
            parallels=parallels[:3] if parallels else [{"system": "Cross-tradition", "concept": "Related wisdom", "reason": "Addresses same consciousness level"}],
        )


# ============================================================================
# TEST CASES
# ============================================================================

def run_test_queries():
    """Run test queries against the guidance system"""
    print("\n" + "=" * 70)
    print("CONSCIOUSNESS-ALIGNED GUIDANCE SYSTEM - TEST SUITE")
    print("=" * 70 + "\n")

    engine = ConsciousnessGuidanceEngine("wisdom_database_v0.2.json")

    test_cases = [
        {"level": 25, "name": "Deep shame/powerlessness"},
        {"level": 75, "name": "Fear; beginning to move"},
        {"level": 150, "name": "Desire; seeking change"},
        {"level": 250, "name": "Courage; self-directed"},
        {"level": 350, "name": "Neutral; balanced perspective"},
        {"level": 450, "name": "Willingness; opening to service"},
        {"level": 550, "name": "Love; unconditional compassion"},
        {"level": 650, "name": "Peace; approaching enlightenment"},
    ]

    for test in test_cases:
        print(f"\n{'—' * 70}")
        print(f"TEST: {test['name']} (Level {test['level']})")
        print(f"{'—' * 70}\n")

        try:
            response = engine.query(level=test["level"])
            print(response.formatted())
        except Exception as e:
            print(f"ERROR: {e}")


if __name__ == "__main__":
    run_test_queries()
