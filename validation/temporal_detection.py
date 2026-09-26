"""
T1.2: Temporal Language Detection Patterns

Define regex patterns for 8 temporal language categories.
These patterns power all 4 validation checkpoints (PREFLIGHT, CHECK, POSTFLIGHT, output).

Categories:
1. absolute_time — specific times (9am CST, 3:30 PM)
2. dates — calendar dates (2026-08-22, Sep 15, Friday)
3. relative_day — day names and relative references (Monday, today, tomorrow)
4. relative_time — relative temporal phrases (next week, in 3 days, by Thursday)
5. duration — explicit time durations (2 hours, 3 days, 77 days)
6. deadline_words — deadline-oriented language (deadline, by date, schedule, ETA)
7. calendar_words — recurring/scheduled language (weekly, monthly, quarterly, annual)
8. temporal_sequence — ordering by time (first, then, later, before, after, during)
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class TemporalMatch:
    """Result of finding temporal language."""
    pattern_name: str
    matched_text: str
    position: int
    context: str  # Surrounding text for clarity


class TemporalDetector:
    """Detect temporal language patterns in text."""

    # ========================================================================
    # PATTERN DEFINITIONS
    # ========================================================================

    PATTERNS = {
        "absolute_time": {
            "pattern": r"\b\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM|a\.m\.|p\.m\.)\b|(?:CST|EST|PST|UTC|GMT|Z)(?:\s|$)",
            "examples": ["9am CST", "3:30 PM", "12:00 UTC"],
            "description": "Specific times of day (with or without AM/PM)"
        },

        "dates": {
            "pattern": r"\d{4}-\d{2}-\d{2}|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\b|\b\d{1,2}(?:st|nd|rd|th)?\b",
            "examples": ["2026-08-22", "August 15", "Sep 15"],
            "description": "Calendar dates in various formats"
        },

        "relative_day": {
            "pattern": r"\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b|\b(?:today|tomorrow|yesterday)\b",
            "examples": ["Monday", "Friday", "today", "tomorrow"],
            "description": "Day names or relative references"
        },

        "relative_time": {
            "pattern": r"\bthis\s+(?:week|month|quarter|year)\b|\bnext\s+(?:week|month|quarter|year)\b|\blast\s+(?:week|month|quarter|year)\b|\bin\s+\d+\s+(?:days?|weeks?|months?|hours?|minutes?)\b|\b(?:within|by)\s+\d+\s+(?:days?|weeks?|months?|hours?)\b",
            "examples": ["this week", "next month", "in 3 days", "within 2 weeks"],
            "description": "Relative temporal phrases"
        },

        "duration": {
            "pattern": r"\btakes?\s+\d+(?:\.\d+)?\s+(?:hours?|days?|weeks?|minutes?|seconds?)|(?:for\s+)?\d+(?:\.\d+)?-?(?:hour|day|week|minute|second)(?:\s|[sd]|$)|\b\d+(?:\.\d+)?[hd]\b(?:\s|$)",
            "examples": ["takes 2 hours", "3-day task", "2h", "5 days"],
            "description": "Explicit time durations"
        },

        "deadline_words": {
            "pattern": r"\bdeadline\b|\bby\s+(?:end of|the end of|(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)|\d{1,2})\b|\bschedule\b|\bwhen\s+done\b|\bETA\b|\bdue\b",
            "examples": ["deadline", "by Friday", "schedule", "ETA"],
            "description": "Deadline-oriented language"
        },

        "calendar_words": {
            "pattern": r"\b(?:weekly|biweekly|fortnightly|monthly|quarterly|annually?|yearly|daily|hourly|recurring|recurrence|repeat|sprint|standup|sync)\b",
            "examples": ["weekly", "monthly", "quarterly", "recurring"],
            "description": "Recurring/scheduled language"
        },

        "temporal_sequence": {
            "pattern": r"\b(?:first|second|third|then|next|after|before|during|meanwhile|later|earlier|when|once|until)\s+(?:we|I|it|this|that|the)",
            "examples": ["first we", "then we", "after that", "before starting"],
            "description": "Temporal sequencing (typically at start of sentence)"
        }
    }

    # ========================================================================
    # DETECTION METHODS
    # ========================================================================

    @classmethod
    def find_all_matches(cls, text: str) -> List[TemporalMatch]:
        """Find all temporal language in text."""
        matches = []

        for pattern_name, pattern_info in cls.PATTERNS.items():
            pattern = pattern_info["pattern"]
            regex = re.compile(pattern, re.IGNORECASE)

            for match in regex.finditer(text):
                start, end = match.span()
                # Get context (50 chars before/after)
                context_start = max(0, start - 50)
                context_end = min(len(text), end + 50)
                context = text[context_start:context_end]

                matches.append(TemporalMatch(
                    pattern_name=pattern_name,
                    matched_text=match.group(),
                    position=start,
                    context=context.strip()
                ))

        # Sort by position
        matches.sort(key=lambda m: m.position)
        return matches

    @classmethod
    def has_temporal_language(cls, text: str) -> bool:
        """Quick check: does text contain temporal language?"""
        return len(cls.find_all_matches(text)) > 0

    @classmethod
    def get_violations(cls, text: str) -> List[str]:
        """Get formatted list of temporal language violations."""
        matches = cls.find_all_matches(text)
        violations = []

        for match in matches:
            violation = (
                f"Temporal language in {match.pattern_name}: '{match.matched_text}' "
                f"(context: ...{match.context}...)"
            )
            violations.append(violation)

        return violations

    @classmethod
    def scan_field(cls, field_name: str, field_value: str) -> Tuple[bool, List[str]]:
        """
        Scan a single field for temporal language.

        Returns: (is_clean, violations)
        """
        violations = cls.get_violations(field_value)
        return len(violations) == 0, violations


# ============================================================================
# HELPER FUNCTIONS FOR VALIDATION CHECKPOINTS
# ============================================================================

def validate_resource_field_for_temporal(field_name: str, field_value: str) -> Tuple[bool, str]:
    """
    Validate that a resource field (resource_anchor, resource_scope, etc.)
    does NOT contain temporal language.

    Returns: (is_valid, error_message)
    """
    if not field_value:
        return True, ""

    # Convert to string if needed (could be dict/list)
    field_str = str(field_value)

    is_clean, violations = TemporalDetector.scan_field(field_name, field_str)

    if not is_clean:
        error = (
            f"Temporal language in {field_name}:\n" +
            "\n".join(f"  - {v}" for v in violations[:3]) +  # First 3 violations
            (f"\n  ... and {len(violations)-3} more" if len(violations) > 3 else "")
        )
        return False, error

    return True, ""


def validate_claim_grounding_for_temporal(grounding_text: str) -> Tuple[bool, str]:
    """
    Validate that claim grounding (evidence) does NOT use time as the basis.

    Returns: (is_valid, error_message)
    """
    # Grounding should be: 'read', 'ran', 'retrieved', 'assumed'
    # If grounding text refers to time/duration/schedule, it's weak grounding

    is_clean, violations = TemporalDetector.scan_field("grounding", grounding_text)

    if not is_clean:
        error = (
            f"Claim grounding uses temporal reference (should use: read|ran|retrieved|assumed):\n" +
            "\n".join(f"  - {v}" for v in violations)
        )
        return False, error

    return True, ""


def validate_verdict_for_temporal(verdict_text: str) -> Tuple[bool, str]:
    """
    Validate that a verdict (held|refuted|untested) does NOT use time.

    Returns: (is_valid, error_message)
    """
    is_clean, violations = TemporalDetector.scan_field("verdict", verdict_text)

    if not is_clean:
        error = (
            f"Verdict contains temporal language (should be: held|refuted|untested):\n" +
            "\n".join(f"  - {v}" for v in violations)
        )
        return False, error

    return True, ""


# ============================================================================
# UTILITY: Print all patterns for documentation
# ============================================================================

def print_pattern_guide():
    """Print pattern guide for reference."""
    print("=" * 80)
    print("TEMPORAL LANGUAGE DETECTION PATTERNS")
    print("=" * 80)

    for i, (name, info) in enumerate(TemporalDetector.PATTERNS.items(), 1):
        print(f"\n{i}. {name.upper()}")
        print(f"   Description: {info['description']}")
        print(f"   Examples: {', '.join(info['examples'])}")
        print(f"   Pattern: {info['pattern'][:80]}{'...' if len(info['pattern']) > 80 else ''}")


if __name__ == "__main__":
    # Demo: run pattern guide and test on sample text
    print_pattern_guide()

    # Test on sample text
    print("\n\n" + "=" * 80)
    print("TEST: Scanning sample text")
    print("=" * 80)

    sample_text = """
    We need to finish this task by Friday. It should take about 2 hours.
    Schedule a weekly standup meeting for next month.
    First we'll review, then we'll implement, later we'll test.
    """

    print(f"\nSample text:\n{sample_text}")

    matches = TemporalDetector.find_all_matches(sample_text)
    print(f"\nMatches found: {len(matches)}")
    for match in matches:
        print(f"  - {match.pattern_name}: '{match.matched_text}'")
