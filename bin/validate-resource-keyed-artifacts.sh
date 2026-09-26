#!/bin/bash
# Temporal Framing Detector & Rejector
# Validates goal/task artifacts conform to resource-keyed model
# Exit 1 if temporal framing detected; exit 0 if clean

set -u

ARTIFACT_FILE="${1:-.}"
TEMP_LOGFILE="/tmp/temporal-audit-$$.log"
trap "rm -f $TEMP_LOGFILE" EXIT

# ANSI colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Patterns that indicate temporal framing (BANNED)
declare -a BANNED_PATTERNS=(
    "^[^\"]*by [0-9]{4}-[0-9]{2}-[0-9]{2}[^\"]*$"  # by 2026-08-21
    "^[^\"]*by [0-9]{4}/[0-9]{2}/[0-9]{2}[^\"]*$"  # by 2026/08/21
    "^[^\"]*\\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\\b[^\"]*$"  # day names
    "^[^\"]*\\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[^\"]*$"  # month names
    "^[^\"]*\\bdue \\b[^\"]*$"  # due [something]
    "^[^\"]*\\bdeadline[^\"]*$"  # deadline
    "^[^\"]*\\btakes? [0-9]+ (hours?|days?|weeks?|minutes?)[^\"]*$"  # takes 2 hours
    "^[^\"]*\\bschedule[d]?[^\"]*$"  # scheduled/schedule
    "^[^\"]*\\b(EOD|morning|afternoon|evening|end of week|end of day)[^\"]*$"  # time-of-day
    "^[^\"]*\\b[0-9]+[[:space:]]*(hours?|days?|weeks?|minutes?)[[:space:]]*(from now|ago)[^\"]*$"  # 3 days from now
    "^[^\"]*\\b(by|before|after|during|throughout) the week[^\"]*$"  # temporal periods
)

# Patterns that indicate GOOD resource-keyed language (APPROVED)
declare -a APPROVED_PATTERNS=(
    "blocked_by.*resource_state"  # resource state blocking
    "unblocks.*capability"  # capability unblocking
    "resource_budget"  # resource budgeting
    "human_labor_hours"  # labor hours
    "ai_tokens"  # token consumption
    "once.*consumed"  # once [resource] consumed
    "after.*labor"  # after labor consumed
)

# =====================================================================
# CHECK 1: Temporal framing in goal/task descriptions
# =====================================================================
echo -e "${YELLOW}[CHECK 1] Scanning for BANNED temporal framing...${NC}"

VIOLATIONS_FOUND=0

if [[ -f "$ARTIFACT_FILE" ]]; then
    # Extract all string values from JSON (descriptions, objectives, etc.)
    FIELDS_TO_CHECK=$(jq -r '
        .. |
        objects |
        select(.description, .objective, .reason) |
        .description, .objective, .reason
    ' "$ARTIFACT_FILE" 2>/dev/null | grep -v '^null$')

    while IFS= read -r line; do
        [[ -z "$line" ]] && continue

        for pattern in "${BANNED_PATTERNS[@]}"; do
            if grep -qE "$pattern" <<< "$line"; then
                echo -e "${RED}  ✗ BANNED PATTERN: '$pattern'${NC}"
                echo -e "    Found in: $line"
                ((VIOLATIONS_FOUND++))
            fi
        done
    done <<< "$FIELDS_TO_CHECK"
fi

if [[ $VIOLATIONS_FOUND -gt 0 ]]; then
    echo -e "${RED}[FAIL] Found $VIOLATIONS_FOUND temporal framing violation(s)${NC}"
    echo ""
    echo "Fix with resource-based language:"
    echo "  'by [date]' → 'once [resource_state] reached'"
    echo "  '[duration]' → '[resource] budget [amount]'"
    echo "  'due [date]' → 'blocked_by [resource_state]'"
    echo "  'schedule' → 'resource allocation'"
    exit 1
fi

echo -e "${GREEN}  ✓ No temporal framing detected${NC}"

# =====================================================================
# CHECK 2: Validate blocked_by entries are resource-state based
# =====================================================================
echo -e "${YELLOW}[CHECK 2] Validating blocked_by entries are resource-state based...${NC}"

BLOCKED_BY_VIOLATIONS=0

# Extract all blocked_by entries that are objects (should have resource_state)
BLOCKED_BY_ENTRIES=$(jq -r '
    [.. | objects | select(.blocked_by != null and (.blocked_by | type) == "array")] |
    .[].blocked_by[] |
    select(type == "object" and .resource_state == null)
' "$ARTIFACT_FILE" 2>/dev/null)

if [[ ! -z "$BLOCKED_BY_ENTRIES" ]]; then
    while IFS= read -r entry; do
        if [[ ! -z "$entry" ]]; then
            echo -e "${RED}  ✗ blocked_by object missing resource_state: $entry${NC}"
            ((BLOCKED_BY_VIOLATIONS++))
        fi
    done <<< "$BLOCKED_BY_ENTRIES"
fi

if [[ $BLOCKED_BY_VIOLATIONS -gt 0 ]]; then
    echo -e "${RED}[FAIL] Found $BLOCKED_BY_VIOLATIONS blocked_by entries without resource_state${NC}"
    echo ""
    echo "Fix with:"
    echo '  "blocked_by": [{"resource_state": "[X] consumed >= [N]", "reason": "..."}]'
    exit 1
fi

echo -e "${GREEN}  ✓ All blocked_by entries have resource_state${NC}"

# =====================================================================
# CHECK 3: Validate unblocks entries reference capabilities
# =====================================================================
echo -e "${YELLOW}[CHECK 3] Validating unblocks entries reference capabilities...${NC}"

UNBLOCKS_VIOLATIONS=0

UNBLOCKS_ENTRIES=$(jq -r '
    .. |
    objects |
    select(.unblocks != null) |
    .unblocks[]? |
    select(.capability == null)
' "$ARTIFACT_FILE" 2>/dev/null)

if [[ ! -z "$UNBLOCKS_ENTRIES" ]]; then
    echo -e "${RED}  ✗ unblocks entries missing capability field:${NC}"
    echo "$UNBLOCKS_ENTRIES"
    ((UNBLOCKS_VIOLATIONS++))
fi

if [[ $UNBLOCKS_VIOLATIONS -gt 0 ]]; then
    echo -e "${RED}[FAIL] Found $UNBLOCKS_VIOLATIONS unblocks entries without capability${NC}"
    echo ""
    echo "Fix with:"
    echo '  "unblocks": [{"capability": "[phase/gate/state]", "reason": "..."}]'
    exit 1
fi

echo -e "${GREEN}  ✓ All unblocks entries have capability field${NC}"

# =====================================================================
# CHECK 4: Validate resource_budget entries exist for all tasks
# =====================================================================
echo -e "${YELLOW}[CHECK 4] Validating resource_budget entries for all tasks...${NC}"

BUDGET_VIOLATIONS=0

TASKS_WITHOUT_BUDGET=$(jq -r '
    .tasks[]? |
    select(.resource_budget == null) |
    .task_id
' "$ARTIFACT_FILE" 2>/dev/null)

if [[ ! -z "$TASKS_WITHOUT_BUDGET" ]]; then
    echo -e "${RED}  ✗ Tasks missing resource_budget:${NC}"
    echo "$TASKS_WITHOUT_BUDGET"
    BUDGET_VIOLATIONS=$(echo "$TASKS_WITHOUT_BUDGET" | wc -l)
fi

if [[ $BUDGET_VIOLATIONS -gt 0 ]]; then
    echo -e "${RED}[FAIL] Found $BUDGET_VIOLATIONS tasks without resource_budget${NC}"
    echo ""
    echo "Every task must have:"
    echo '  "resource_budget": {"human_labor_hours": N, "ai_tokens": N, ...}'
    exit 1
fi

echo -e "${GREEN}  ✓ All tasks have resource_budget entries${NC}"

# =====================================================================
# CHECK 5: Success criteria must be measurable by resource consumption
# =====================================================================
echo -e "${YELLOW}[CHECK 5] Validating success_criteria are resource-measurable...${NC}"

CRITERIA_VIOLATIONS=0

CRITERIA=$(jq -r '
    .success_criteria[]? |
    select(.resource_measure == null) |
    .criterion
' "$ARTIFACT_FILE" 2>/dev/null)

if [[ ! -z "$CRITERIA" ]]; then
    echo -e "${RED}  ✗ Success criteria missing resource_measure:${NC}"
    echo "$CRITERIA"
    CRITERIA_VIOLATIONS=$(echo "$CRITERIA" | wc -l)
fi

if [[ $CRITERIA_VIOLATIONS -gt 0 ]]; then
    echo -e "${RED}[FAIL] Found $CRITERIA_VIOLATIONS criteria without resource_measure${NC}"
    echo ""
    echo "Every criterion must have:"
    echo '  "resource_measure": "[labor hours / tokens / endpoints / etc]"'
    echo '  "validation_method": "[how to verify at POSTFLIGHT]"'
    exit 1
fi

echo -e "${GREEN}  ✓ All success_criteria have resource_measure${NC}"

# =====================================================================
# SUMMARY
# =====================================================================
echo ""
echo -e "${GREEN}════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ ARTIFACT PASSED RESOURCE-KEYED VALIDATION${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════${NC}"
echo ""
echo "Safe to log to empirica."
exit 0
