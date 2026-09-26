"""
Resource-Accounting-Guard Schema Validation

Enforces upstream validation of PREFLIGHT/POSTFLIGHT payloads:
- Removes temporal fields (no timestamps, deadlines, durations)
- Requires resource_anchor fields (labor_hours, ai_tokens, decisions)
- Makes resource_scope_this_transaction required
- Rejects temporal language in resource fields
"""

from typing import Any, Dict, List, Tuple
from pydantic import BaseModel, Field, validator
import re


# ============================================================================
# RESOURCE ANCHOR: Required fields for all PREFLIGHT/POSTFLIGHT
# ============================================================================

class ResourceAnchor(BaseModel):
    """Resource consumption budget/actual for this transaction."""

    labor_hours_budget_this_transaction: Tuple[float, float] = Field(
        ...,
        description="Labor hours budget: [min, max]"
    )
    ai_tokens_budget_this_transaction: Tuple[int, int] = Field(
        ...,
        description="AI tokens budget: [min, max]"
    )
    decisions_pending_count: int = Field(
        ...,
        description="Number of decisions pending this transaction"
    )
    measurement_gates_active_count: int = Field(
        default=0,
        description="Number of active measurement gates"
    )
    escalations_open_count: int = Field(
        default=0,
        description="Number of open escalations"
    )

    @validator('labor_hours_budget_this_transaction')
    def validate_labor_range(cls, v):
        if not (0 < v[0] < v[1]):
            raise ValueError("labor_hours_budget must be [min > 0, max > min]")
        return v

    @validator('ai_tokens_budget_this_transaction')
    def validate_tokens_range(cls, v):
        if not (0 < v[0] < v[1]):
            raise ValueError("ai_tokens_budget must be [min > 0, max > min]")
        return v


class ResourceScope(BaseModel):
    """What gets consumed and what should change."""

    what_gets_consumed: List[str] = Field(
        ...,
        description="List of resource consumption items with labor/token estimates"
    )
    what_should_change: List[str] = Field(
        ...,
        description="List of expected changes (Y|N|PENDING)"
    )

    @validator('what_gets_consumed')
    def validate_consumed_has_estimates(cls, v):
        """Each item must include labor or token estimate."""
        for item in v:
            if not re.search(r'\b(?:hours?|tokens?|labor)\b', item, re.IGNORECASE):
                raise ValueError(f"Consumption item must include resource estimate: {item}")
        return v


# ============================================================================
# UPDATED PREFLIGHT: Remove temporal fields, require resource fields
# ============================================================================

class PreflightVectors(BaseModel):
    """The 13 epistemic vectors."""
    know: float
    uncertainty: float
    context: float
    clarity: float
    coherence: float
    signal: float
    density: float
    state: float
    change: float
    completion: float
    impact: float
    do: float
    engagement: float

    @validator('*')
    def validate_vector_range(cls, v):
        if not (0.0 <= v <= 1.0):
            raise ValueError(f"Vector must be in [0.0, 1.0], got {v}")
        return v


class Claim(BaseModel):
    """A claim used in grounding."""
    claim: str
    grounding: str = Field(..., description="read|ran|retrieved|assumed")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)

    @validator('grounding')
    def validate_grounding(cls, v):
        valid = ['read', 'ran', 'retrieved', 'assumed']
        if v not in valid:
            raise ValueError(f"Grounding must be one of {valid}, got {v}")
        return v


class PreflightPayload(BaseModel):
    """Updated PREFLIGHT schema - NO TEMPORAL FIELDS."""

    session_id: str
    work_type: str = Field(..., description="code|research|debug|infra|design|release|remote-ops")
    work_context: str = Field(default="iteration", description="greenfield|iteration|investigation|refactor")
    domain: str = Field(default="default")
    criticality: str = Field(default="medium", description="low|medium|high")
    task_context: str = Field(default="")

    # REQUIRED: Resource anchor (upstream validation starts here)
    resource_anchor: ResourceAnchor
    resource_scope_this_transaction: ResourceScope

    # Vectors
    vectors: PreflightVectors
    reasoning: str = Field(..., description="Why you're opening this transaction")

    # Optional: claims for pre-grounded work
    claims: List[Claim] = Field(default_factory=list)

    # NO: timestamp (removed - use session_id for grounding)
    # NO: estimated_duration_hours (removed - use labor_hours_budget)
    # NO: deadline (removed - resource scope has what_should_change)

    class Config:
        extra = "forbid"  # Reject any temporal fields

    def validate_no_temporal_language(self) -> List[str]:
        """Scan all text fields for temporal language patterns."""
        violations = []

        TEMPORAL_PATTERNS = {
            "absolute_time": r"\d{1,2}:\d{2}\s*(am|pm|CST|EST|UTC|Z)",
            "dates": r"\d{4}-\d{2}-\d{2}|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec",
            "relative_day": r"Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|today|tomorrow",
            "relative_time": r"this week|next week|next month|in \d+ (days|hours|weeks)",
            "duration": r"takes? \d+ (minutes|hours|days|weeks)",
            "deadline_words": r"deadline|by.*date|schedule|when.*done|ETA",
            "calendar_words": r"weekly|monthly|quarterly|annual|recurring|sprint"
        }

        text_to_scan = f"{self.task_context} {self.reasoning}"

        for pattern_name, pattern in TEMPORAL_PATTERNS.items():
            matches = re.finditer(pattern, text_to_scan, re.IGNORECASE)
            for match in matches:
                violations.append(
                    f"Temporal language '{match.group()}' in {pattern_name} — use resource metrics instead"
                )

        return violations


# ============================================================================
# UPDATED POSTFLIGHT: Remove temporal fields, require resource accounting
# ============================================================================

class ResourceAccounting(BaseModel):
    """Actual resource consumption."""
    human_labor_hours_consumed: float = Field(..., ge=0.0)
    ai_tokens_consumed: int = Field(..., ge=0)
    practices_labor_consumed: float = Field(default=0.0, ge=0.0)
    decisions_made: int = Field(default=0, ge=0)


class ClaimAdjudication(BaseModel):
    """Adjudicate claims from PREFLIGHT."""
    index: int
    verdict: str = Field(..., description="held|refuted|untested")
    evidence: str = Field(default="")

    @validator('verdict')
    def validate_verdict(cls, v):
        valid = ['held', 'refuted', 'untested']
        if v not in valid:
            raise ValueError(f"Verdict must be one of {valid}, got {v}")
        return v


class PostflightPayload(BaseModel):
    """Updated POSTFLIGHT schema - NO TEMPORAL FIELDS."""

    session_id: str

    # Vectors at end of transaction
    vectors: PreflightVectors
    reasoning: str

    # REQUIRED: Resource accounting (upstream validation)
    resource_accounting_final: ResourceAccounting

    # Claims adjudication
    claims_adjudication: List[ClaimAdjudication] = Field(default_factory=list)

    # NO: timestamp (removed - use session_id for grounding)
    # NO: human_session (removed - session_id covers grounding)
    # NO: phase (removed - payload type makes it obvious)

    class Config:
        extra = "forbid"  # Reject any temporal fields

    def validate_no_temporal_language(self) -> List[str]:
        """Scan all text fields for temporal language patterns."""
        violations = []

        TEMPORAL_PATTERNS = {
            "absolute_time": r"\d{1,2}:\d{2}\s*(am|pm|CST|EST|UTC|Z)",
            "dates": r"\d{4}-\d{2}-\d{2}|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec",
            "relative_day": r"Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|today|tomorrow",
            "relative_time": r"this week|next week|next month|in \d+ (days|hours|weeks)",
            "duration": r"takes? \d+ (minutes|hours|days|weeks)",
            "deadline_words": r"deadline|by.*date|schedule|when.*done|ETA",
            "calendar_words": r"weekly|monthly|quarterly|annual|recurring|sprint"
        }

        text_to_scan = self.reasoning
        for adj in self.claims_adjudication:
            text_to_scan += f" {adj.evidence}"

        for pattern_name, pattern in TEMPORAL_PATTERNS.items():
            matches = re.finditer(pattern, text_to_scan, re.IGNORECASE)
            for match in matches:
                violations.append(
                    f"Temporal language '{match.group()}' in {pattern_name} — use resource metrics instead"
                )

        return violations


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_preflight(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate PREFLIGHT payload.

    Returns: (is_valid, list_of_violations)
    """
    violations = []

    # Check: Schema compliance
    try:
        pf = PreflightPayload(**payload)
    except Exception as e:
        return False, [f"Schema validation failed: {str(e)}"]

    # Check: No temporal language
    temporal_violations = pf.validate_no_temporal_language()
    if temporal_violations:
        violations.extend(temporal_violations)
        return False, violations

    return True, []


def validate_postflight(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate POSTFLIGHT payload.

    Returns: (is_valid, list_of_violations)
    """
    violations = []

    # Check: Schema compliance
    try:
        pf = PostflightPayload(**payload)
    except Exception as e:
        return False, [f"Schema validation failed: {str(e)}"]

    # Check: No temporal language in verdicts
    for adj in pf.claims_adjudication:
        if adj.verdict not in ['held', 'refuted', 'untested']:
            violations.append(f"Invalid verdict: {adj.verdict} (must be held|refuted|untested)")

    # Check: No temporal language
    temporal_violations = pf.validate_no_temporal_language()
    if temporal_violations:
        violations.extend(temporal_violations)
        return False, violations

    return True, []
