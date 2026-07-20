# Consciousness-Aligned Guidance System v1.0
## API Documentation & Usage Guide

---

## Overview

The **Consciousness-Aligned Guidance System** matches a person's consciousness level (Hawkins 0-1000 scale) to appropriate wisdom teachings from 6 major traditions:
- AA 12 Steps & 12 Traditions
- Hawkins Map of Consciousness
- Words of Jesus
- Buddhist Core Teachings
- Freemasonry Degrees

The system:
1. **Identifies current level** (0-1000 Hawkins scale)
2. **Maps to consciousness zone** (PowerLoss, LowerPower, Power, HigherPower, TruthRevealing, Transcendent)
3. **Returns primary teaching** (most appropriate tradition for this level)
4. **Shows parallels** (how 2-3 other traditions address the same level)
5. **Suggests next level** (what comes after current teaching)

---

## Core Concepts

### Consciousness Zones

```
Zone               Level Range    Key Characteristics
────────────────────────────────────────────────────────
POWER_LOSS         0-50           Shame, guilt, apathy
LOWER_POWER        50-200         Fear, desire, anger, pride
POWER              200-350        Courage, neutrality
HIGHER_POWER       350-600        Willingness, acceptance, love, joy
TRUTH_REVEALING    600-700        Peace, enlightenment
TRANSCENDENT       700-1000       Beyond calibration
```

### Three-Level Understanding

Each teaching is understood at three levels:
1. **Exoteric** (outer, literal) — The visible teaching, ethics, rules
2. **Mesoteric** (middle, allegorical) — Hidden meanings, psychological applications
3. **Esoteric** (inner, ultimate) — Highest truth; what cannot be spoken

---

## Usage

### Basic Query

```python
from guidance_system_v1.0 import ConsciousnessGuidanceEngine

# Initialize with wisdom database
engine = ConsciousnessGuidanceEngine("wisdom_database_v0.2.json")

# Query for consciousness level 75 (Fear; beginning upward movement)
response = engine.query(level=75)

# Display formatted guidance
print(response.formatted())
```

### Query with Tradition Filter

```python
# Get guidance specifically from Buddhist teachings
response = engine.query(level=150, tradition="buddhist_core_teachings")

# Get guidance from AA path
response = engine.query(level=300, tradition="aa_12_steps")
```

### Access Structured Response

```python
response = engine.query(level=450)

# Access components programmatically
print(f"Level: {response.user_level}")
print(f"Zone: {response.user_zone}")
print(f"Teaching: {response.primary_teaching.title}")
print(f"System: {response.primary_teaching.system}")

# Cross-tradition parallels
for parallel in response.primary_teaching.parallels:
    print(f"  {parallel['system']}: {parallel['concept']}")

# Convert to JSON
import json
data = response.to_dict()
json_str = json.dumps(data, indent=2)
```

---

## Output Format

### Formatted Output Example

```
======================================================================
CONSCIOUSNESS-ALIGNED GUIDANCE | Level 75 (LOWER_POWER)
======================================================================

YOUR CURRENT TEACHING:
  System: buddhist_core_teachings
  Teaching: The Eightfold Path
  Concepts: eightfold-path, right-living, ethics, meditation, wisdom
  Practice: Structured daily practice; study one aspect per month

HOW OTHER TRADITIONS ADDRESS THIS LEVEL:
  • Stoic: suffering-and-adversity
    └─ Reality-facing; acceptance of difficulty
  • Hawkins: level 5
    └─ Anger as first sign of upward momentum

WHEN YOU'RE READY FOR THE NEXT STEP:
  Level: 200-350
  Teaching: Courage and Neutrality (Hawkins Map)

ZONE INTERPRETATION:
  You're in active transformation. Fear, desire, and anger are signs
  that energy is moving upward. These emotions have intelligence; use
  them as fuel. The teaching at this level helps you channel that
  energy toward growth rather than destruction.

======================================================================
```

---

## API Reference

### ConsciousnessGuidanceEngine

#### `__init__(wisdom_db_path: str)`
Initialize the engine with a wisdom database path.

**Parameters:**
- `wisdom_db_path` (str): Path to `wisdom_database_v0.2.json`

**Example:**
```python
engine = ConsciousnessGuidanceEngine("wisdom_database_v0.2.json")
```

#### `query(level: int, tradition: Optional[str] = None) -> GuidanceResponse`
Query for guidance at a specific consciousness level.

**Parameters:**
- `level` (int): Consciousness level 0-1000 (Hawkins scale)
- `tradition` (Optional[str]): Specific tradition filter (default: None for all traditions)

**Returns:**
- `GuidanceResponse` object with teaching, parallels, and interpretations

**Consciousness Levels:**
- 0-50: Deep powerlessness/shame
- 50-100: Guilt/apathy
- 100-200: Fear/desire/anger
- 200-300: Courage/beginning self-direction
- 300-400: Neutrality/balance
- 400-500: Willingness/acceptance
- 500-600: Love/joy/service
- 600-700: Peace/enlightenment
- 700-1000: Transcendent states

**Example:**
```python
# Level 25: Recognition of powerlessness
response = engine.query(level=25)

# Level 350: Entering integration phase
response = engine.query(level=350)

# Level 550: Transmission/service mode
response = engine.query(level=550, tradition="aa_12_steps")
```

### GuidanceResponse

#### Properties
- `user_level` (int): The requested consciousness level
- `user_zone` (str): Zone name (POWER_LOSS, LOWER_POWER, etc.)
- `primary_teaching` (TeachingMatch): Best teaching for this level
- `next_level_pathway` (Optional[TeachingMatch]): Teaching for next level
- `supporting_teachings` (List[TeachingMatch]): 2-3 teachings from other traditions
- `zone_interpretation` (str): Context-aware guidance for this zone

#### Methods
- `formatted() -> str`: Return human-readable formatted guidance
- `to_dict() -> Dict`: Convert to JSON-serializable dictionary

### TeachingMatch

#### Properties
- `system` (str): Tradition name (e.g., "aa_12_steps", "buddhist_core_teachings")
- `unit_id` (str): Teaching unit ID
- `title` (str): Teaching title
- `sequence` (int): Position in tradition
- `zone` (str): Consciousness zone
- `key_concepts` (List[str]): Core concepts
- `calibration_level` (Tuple[int, int]): Consciousness level range
- `application_practice` (str): How to practice/apply this teaching
- `parallels` (List[Dict]): Cross-tradition parallels

---

## Integration Examples

### Web API (FastAPI)

```python
from fastapi import FastAPI
from guidance_system_v1_0 import ConsciousnessGuidanceEngine

app = FastAPI()
engine = ConsciounsciousnessGuidanceEngine("wisdom_database_v0.2.json")

@app.get("/guidance/{level}")
async def get_guidance(level: int, tradition: Optional[str] = None):
    response = engine.query(level=level, tradition=tradition)
    return response.to_dict()

# Usage: GET /guidance/75
# Usage: GET /guidance/350?tradition=aa_12_steps
```

### Conversational AI

```python
def guidance_chatbot(user_level: int, user_question: str):
    response = engine.query(level=user_level)
    
    system_prompt = f"""
    You are a wisdom guide. The user is at consciousness level {user_level} ({response.user_zone}).
    
    Current teaching: {response.primary_teaching.title}
    Tradition: {response.primary_teaching.system}
    
    Context: {response.zone_interpretation}
    
    Respond to their question using wisdom from this tradition and related traditions.
    """
    
    # Pass to LLM for conversational response
    return llm_call(system_prompt, user_question)

# Usage:
# guidance_chatbot(level=75, user_question="I'm afraid and don't know what to do")
```

### Therapeutic/Coaching Application

```python
def create_guidance_report(client_level: int) -> str:
    response = engine.query(level=client_level)
    
    report = f"""
    CONSCIOUSNESS ASSESSMENT REPORT
    
    Current Level: {response.user_level} ({response.user_zone})
    
    {response.zone_interpretation}
    
    RECOMMENDED TEACHING:
    - System: {response.primary_teaching.system}
    - Teaching: {response.primary_teaching.title}
    - Practice: {response.primary_teaching.application_practice}
    
    RELATED APPROACHES FROM OTHER TRADITIONS:
    """
    
    for parallel in response.primary_teaching.parallels:
        report += f"\n    • {parallel['system']}: {parallel['concept']}"
    
    if response.next_level_pathway:
        report += f"\n    
    NEXT STEP (when ready):
    - Level: {response.next_level_pathway.calibration_level}
    - Teaching: {response.next_level_pathway.title}"
    
    return report
```

---

## Consciousness Level Mapping

### Practical Applications by Level

| Level | Zone | Condition | Suggested Approach |
|-------|------|-----------|-------------------|
| 0-25 | Loss | Suicidal/despair | Immediate support; AA Step 1 |
| 25-50 | Loss | Shame/numbness | Acceptance; Buddhist suffering recognition |
| 50-75 | Lower | Fear/anxiety | Grounding; Courage building |
| 75-125 | Lower | Desire/craving | Discernment; Eightfold Path |
| 125-200 | Lower | Anger/resentment | Channel energy; AA Steps 6-7 |
| 200-250 | Power | Courage/confidence | Action taking; Fellowcraft labor |
| 250-300 | Power | Neutrality emerging | Self-study; Contemplation |
| 300-350 | Power | Balance/clarity | Ethical mastery; Jesus teachings |
| 350-400 | Higher | Willingness activated | Service beginning; Acceptance |
| 400-450 | Higher | Acceptance deepening | Community engagement |
| 450-500 | Higher | Love emerging | Forgiveness work; Compassion practice |
| 500-550 | Higher | Unconditional love | Teaching/transmission mode |
| 550-600 | Higher | Joy independent of circumstance | Enlightenment approaching |
| 600+ | Revealing/Trans | Peace/enlightenment | Non-dual awareness |

---

## Limitations & Future Enhancements

### Current Limitations
- Database covers 6 traditions; other wisdom systems (Sufi, African, Indigenous) not yet included
- Consciousness level is self-reported (not independently assessed)
- No validation that user actually possesses the capacity for their reported level
- Calibrations are approximate (Hawkins map itself is non-quantitative)

### Future Enhancements
- Consciousness level assessment questionnaire (Hawk scale self-report + validation)
- Adaptive recommendations based on learning style (intellectual, devotional, practical, mystical)
- Obstacle-based querying ("I struggle with anger" → appropriate teaching)
- Teacher/community matching (which organizations/teachers work at this level)
- Progress tracking (show movement from level 50 → 200 → 350 over time)
- Contradiction mapping (where traditions disagree; why; synthesis)

---

## Philosophy

This system is based on the recognition that **all wisdom traditions are solving the same problem**: how to move from unconsciousness to consciousness.

The universal patterns across traditions are:
1. Recognition of limitation
2. Active transformation through discipline
3. Integration and mastery
4. Transmission and service

By mapping to consciousness levels, we unlock the ability to match *any person* to *any teaching* at the *exact right time*.

---

## Support & Contribution

For questions or to contribute teachings from additional traditions, see:
- `WISDOM_DATABASE_ASSESSMENT_v0.2.md` — Full assessment of the database
- `wisdom_database_v0.2.json` — Raw database (126 units across 6 systems)
- `guidance_system_v1.0.py` — Source code

---

*Application 1 of the Wisdom-Based Guidance Suite*  
*Production-ready for integration with conversational AI, therapeutic applications, and educational platforms*
