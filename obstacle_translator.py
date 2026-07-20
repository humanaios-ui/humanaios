#!/usr/bin/env python3
"""
Obstacle-to-Opportunity Translator v1.0

ML Problem → Consciousness Level → AA Wisdom Teaching → Actionable ML Technique

Translates supervised learning obstacles into wisdom teachings and concrete code patterns.
"""

import json
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
from enum import Enum


@dataclass
class MLTechnique:
    """An ML technique that addresses an obstacle"""
    name: str
    principle: str
    wisdom_mapping: str
    code_technique: str
    hyperparameter: str
    expected_impact: str


@dataclass
class WisdomTeaching:
    """AA wisdom teaching for a consciousness level"""
    step_number: int
    step_text: str
    translation: str
    secondary_step: Optional[int] = None
    secondary_text: Optional[str] = None
    tradition: Optional[str] = None
    tradition_translation: Optional[str] = None


@dataclass
class ConsciousnessMapping:
    """How an obstacle maps to consciousness level"""
    level: int
    zone: str
    reasoning: str


@dataclass
class ObstacleTranslation:
    """Complete translation of an ML obstacle"""
    obstacle_id: str
    obstacle_name: str
    description: str
    symptoms: List[str]

    # Consciousness mapping
    consciousness_level: int
    consciousness_zone: str
    consciousness_reasoning: str

    # AA Wisdom
    aa_wisdom: WisdomTeaching

    # Hawkins teaching
    hawkins_level: int
    hawkins_name: str
    hawkins_teaching: str
    hawkins_pathway: str

    # ML Techniques
    techniques: List[MLTechnique]

    # Progression
    next_level: int
    next_teaching: str

    def formatted(self) -> str:
        """Format as readable guidance"""
        output = []
        output.append("=" * 80)
        output.append(f"ML OBSTACLE-TO-OPPORTUNITY TRANSLATION | {self.obstacle_name}")
        output.append("=" * 80)
        output.append("")

        output.append("THE PROBLEM:")
        output.append(f"  {self.description}")
        output.append("")
        output.append("SYMPTOMS:")
        for symptom in self.symptoms:
            output.append(f"  • {symptom}")
        output.append("")

        output.append("CONSCIOUSNESS ANALYSIS:")
        output.append(f"  Level: {self.consciousness_level} ({self.consciousness_zone})")
        output.append(f"  Reasoning: {self.consciousness_reasoning}")
        output.append("")

        output.append("AA WISDOM TEACHING:")
        output.append(f"  Step {self.aa_wisdom.step_number}: {self.aa_wisdom.step_text}")
        output.append(f"  Translation: {self.aa_wisdom.translation}")
        if self.aa_wisdom.secondary_step:
            output.append(f"  Step {self.aa_wisdom.secondary_step}: {self.aa_wisdom.secondary_text}")
            output.append(f"  Translation: {self.aa_wisdom.tradition_translation}")
        output.append("")

        output.append("HAWKINS MAP:")
        output.append(f"  Level {self.hawkins_level}: {self.hawkins_name}")
        output.append(f"  Teaching: {self.hawkins_teaching}")
        output.append(f"  Pathway: {self.hawkins_pathway}")
        output.append("")

        output.append("ML TECHNIQUES (How Wisdom Translates to Code):")
        for i, tech in enumerate(self.techniques, 1):
            output.append(f"  {i}. {tech.name}")
            output.append(f"     Principle: {tech.principle}")
            output.append(f"     Wisdom: {tech.wisdom_mapping}")
            output.append(f"     Code: {tech.code_technique}")
            output.append(f"     Tune: {tech.hyperparameter}")
            output.append(f"     Impact: {tech.expected_impact}")
            output.append("")

        output.append("NEXT STEP:")
        output.append(f"  When ready: Level {self.next_level}")
        output.append(f"  Teaching: {self.next_teaching}")
        output.append("")
        output.append("=" * 80)

        return "\n".join(output)

    def to_dict(self):
        """Convert to JSON-serializable dictionary"""
        return {
            "obstacle_id": self.obstacle_id,
            "obstacle_name": self.obstacle_name,
            "description": self.description,
            "symptoms": self.symptoms,
            "consciousness": {
                "level": self.consciousness_level,
                "zone": self.consciousness_zone,
                "reasoning": self.consciousness_reasoning,
            },
            "aa_wisdom": {
                "step": self.aa_wisdom.step_number,
                "text": self.aa_wisdom.step_text,
                "translation": self.aa_wisdom.translation,
                "secondary_step": self.aa_wisdom.secondary_step,
                "secondary_text": self.aa_wisdom.secondary_text,
            },
            "hawkins": {
                "level": self.hawkins_level,
                "name": self.hawkins_name,
                "teaching": self.hawkins_teaching,
                "pathway": self.hawkins_pathway,
            },
            "techniques": [
                {
                    "name": t.name,
                    "principle": t.principle,
                    "wisdom_mapping": t.wisdom_mapping,
                    "code_technique": t.code_technique,
                    "hyperparameter": t.hyperparameter,
                    "expected_impact": t.expected_impact,
                }
                for t in self.techniques
            ],
            "progression": {
                "next_level": self.next_level,
                "next_teaching": self.next_teaching,
            },
        }


class ObstacleTranslator:
    """Translate ML obstacles to wisdom teachings and code techniques"""

    def __init__(self, mappings_file: str = "ml_obstacle_mappings_database.json"):
        """Load mappings database"""
        with open(mappings_file, 'r') as f:
            self.db = json.load(f)

        # Build index
        self.obstacles_by_id = {}
        for obstacle_id, obstacle_data in self.db.get("obstacles", {}).items():
            self.obstacles_by_id[obstacle_id] = obstacle_data

    def translate(self, obstacle_id: str) -> ObstacleTranslation:
        """
        Translate ML obstacle to wisdom teaching + techniques

        Args:
            obstacle_id: ID of obstacle (e.g., "overfitting", "class_imbalance")

        Returns:
            ObstacleTranslation with full mapping
        """
        if obstacle_id not in self.obstacles_by_id:
            raise ValueError(f"Obstacle '{obstacle_id}' not found in database")

        obstacle = self.obstacles_by_id[obstacle_id]

        # Extract consciousness mapping
        cons_map = obstacle.get("consciousness_mapping", {})
        cons_level = cons_map.get("level", 0)
        cons_zone = cons_map.get("zone", "UNKNOWN")
        cons_reasoning = cons_map.get("reasoning", "")

        # Extract AA wisdom
        aa_data = obstacle.get("aa_wisdom", {})
        aa_wisdom = WisdomTeaching(
            step_number=aa_data.get("primary_step", 0),
            step_text=aa_data.get("step_text", ""),
            translation=aa_data.get("translation", ""),
            secondary_step=aa_data.get("secondary_step"),
            secondary_text=aa_data.get("secondary_text"),
            tradition=aa_data.get("tradition"),
            tradition_translation=aa_data.get("translation_tradition"),
        )

        # Extract Hawkins teaching
        hawkins = obstacle.get("hawkins_teaching", {})
        hawkins_level = hawkins.get("level", 0)
        hawkins_name = hawkins.get("level_name", "")
        hawkins_teaching = hawkins.get("teaching", "")
        hawkins_pathway = hawkins.get("pathway", "")

        # Extract techniques
        techniques = []
        for tech_data in obstacle.get("ml_techniques", []):
            tech = MLTechnique(
                name=tech_data.get("name", ""),
                principle=tech_data.get("principle", ""),
                wisdom_mapping=tech_data.get("wisdom_mapping", ""),
                code_technique=tech_data.get("code_technique", ""),
                hyperparameter=tech_data.get("hyperparameter", ""),
                expected_impact=tech_data.get("expected_impact", ""),
            )
            techniques.append(tech)

        # Extract progression
        progression = obstacle.get("progression", {})
        next_level = progression.get("next_level", cons_level + 50)
        next_teaching = progression.get("next_teaching", "")

        # Build translation
        translation = ObstacleTranslation(
            obstacle_id=obstacle_id,
            obstacle_name=obstacle.get("name", ""),
            description=obstacle.get("description", ""),
            symptoms=obstacle.get("symptoms", []),
            consciousness_level=cons_level,
            consciousness_zone=cons_zone,
            consciousness_reasoning=cons_reasoning,
            aa_wisdom=aa_wisdom,
            hawkins_level=hawkins_level,
            hawkins_name=hawkins_name,
            hawkins_teaching=hawkins_teaching,
            hawkins_pathway=hawkins_pathway,
            techniques=techniques,
            next_level=next_level,
            next_teaching=next_teaching,
        )

        return translation

    def translate_by_name(self, obstacle_name: str) -> ObstacleTranslation:
        """Translate obstacle by name (fuzzy match)"""
        # Exact match first
        for oid, obstacle in self.obstacles_by_id.items():
            if obstacle.get("name", "").lower() == obstacle_name.lower():
                return self.translate(oid)

        # Fuzzy match (contains)
        for oid, obstacle in self.obstacles_by_id.items():
            if obstacle_name.lower() in obstacle.get("name", "").lower():
                return self.translate(oid)

        raise ValueError(f"No obstacle matching '{obstacle_name}'")

    def list_obstacles(self) -> List[Dict]:
        """List all available obstacles"""
        obstacles = []
        for oid, obstacle in self.obstacles_by_id.items():
            obstacles.append({
                "id": oid,
                "name": obstacle.get("name", ""),
                "level": obstacle.get("consciousness_mapping", {}).get("level", 0),
                "techniques_count": len(obstacle.get("ml_techniques", [])),
            })
        return sorted(obstacles, key=lambda x: x["level"])

    def get_obstacles_by_level(self, level: int) -> List[Dict]:
        """Get all obstacles at a specific consciousness level"""
        matching = []
        for oid, obstacle in self.obstacles_by_id.items():
            obs_level = obstacle.get("consciousness_mapping", {}).get("level", 0)
            if obs_level == level:
                matching.append({
                    "id": oid,
                    "name": obstacle.get("name", ""),
                })
        return matching


# ============================================================================
# TEST CASES
# ============================================================================

def run_test_translations():
    """Run test translations"""
    print("\n" + "=" * 80)
    print("OBSTACLE-TO-OPPORTUNITY TRANSLATOR - TEST SUITE")
    print("=" * 80 + "\n")

    translator = ObstacleTranslator("ml_obstacle_mappings_database.json")

    # Test 1: List all obstacles
    print("AVAILABLE OBSTACLES:")
    print("-" * 80)
    for obstacle in translator.list_obstacles():
        print(f"  • {obstacle['name']:<35} (Level {obstacle['level']:3d}) - {obstacle['techniques_count']} techniques")
    print("")

    # Test 2: Translate specific obstacles
    test_obstacles = ["overfitting", "class_imbalance", "concept_drift", "adversarial_vulnerability"]

    for obstacle_id in test_obstacles:
        print(f"\n{'—' * 80}")
        print(f"TRANSLATION: {obstacle_id.upper()}")
        print(f"{'—' * 80}\n")

        try:
            translation = translator.translate(obstacle_id)
            print(translation.formatted())

        except Exception as e:
            print(f"ERROR: {e}")

    # Test 3: Get obstacles by level
    print(f"\n{'—' * 80}")
    print("OBSTACLES AT LEVEL 75 (Fear)")
    print(f"{'—' * 80}\n")

    obstacles_at_75 = translator.get_obstacles_by_level(75)
    for obs in obstacles_at_75:
        print(f"  • {obs['name']}")

    # Test 4: Export to JSON
    print(f"\n{'—' * 80}")
    print("JSON EXPORT (Overfitting)")
    print(f"{'—' * 80}\n")

    translation = translator.translate("overfitting")
    import json as json_lib
    print(json_lib.dumps(translation.to_dict(), indent=2)[:500] + "...")


if __name__ == "__main__":
    run_test_translations()
