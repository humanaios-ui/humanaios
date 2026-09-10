#!/bin/bash
##
# empirica-postflight-with-acat
#
# Path B Option 1: Wrapper script for POSTFLIGHT + ACAT enrichment
#
# Usage:
#   empirica-postflight-with-acat < /tmp/postflight_payload.json > /tmp/postflight_result.json
#
# Or integrate into workflow:
#   cat $PAYLOAD | empirica-postflight-with-acat
#
# Installation:
#   sudo cp PATH_B_OPTION1_WRAPPER_SCRIPT.sh /usr/local/bin/empirica-postflight-with-acat
#   sudo chmod +x /usr/local/bin/empirica-postflight-with-acat
#
# Then replace: empirica postflight-submit - <<< "$PAYLOAD"
#         with: empirica-postflight-with-acat <<< "$PAYLOAD"
#
# This wrapper:
# 1. Passes POSTFLIGHT payload to empirica postflight-submit (normal flow)
# 2. Extracts session_id from empirica result
# 3. Calls acat-score to assess the session
# 4. Merges ACAT grounding into empirica result
# 5. Returns enriched result to caller
#

set -e

# Configuration
OPERATIONS_DIR="${OPERATIONS_DIR:-$(pwd)/operations}"
ACAT_SCORE_CLI="$OPERATIONS_DIR/bin/acat-score"
API_KEY="${ACAT_API_KEY:-}"
MODEL="${ACAT_MODEL:-claude-opus-4-8}"

# Temp files
POSTFLIGHT_PAYLOAD=$(mktemp)
EMPIRICA_RESULT=$(mktemp)
ACAT_RESULT=$(mktemp)
FINAL_RESULT=$(mktemp)

# Cleanup on exit
cleanup() {
    rm -f "$POSTFLIGHT_PAYLOAD" "$EMPIRICA_RESULT" "$ACAT_RESULT" "$FINAL_RESULT"
}
trap cleanup EXIT

# Read POSTFLIGHT payload from stdin
cat > "$POSTFLIGHT_PAYLOAD"

# Step 1: Call empirica postflight-submit (normal flow)
echo "[postflight-with-acat] Running empirica postflight-submit..." >&2
cat "$POSTFLIGHT_PAYLOAD" | empirica postflight-submit - > "$EMPIRICA_RESULT" 2>/dev/null || {
    echo "[postflight-with-acat] ERROR: empirica postflight-submit failed" >&2
    cat "$EMPIRICA_RESULT"
    exit 1
}

# Step 2: Extract session_id from empirica result
SESSION_ID=$(jq -r '.session_id // empty' "$EMPIRICA_RESULT")
if [ -z "$SESSION_ID" ]; then
    echo "[postflight-with-acat] Warning: No session_id in empirica result, skipping ACAT enrichment" >&2
    cat "$EMPIRICA_RESULT"
    exit 0
fi

# Extract ai_id from postflight payload (or use default)
AI_ID=$(jq -r '.ai_id // "humanaios"' "$POSTFLIGHT_PAYLOAD")

echo "[postflight-with-acat] session_id: $SESSION_ID, ai_id: $AI_ID" >&2

# Step 3: Check if acat-score CLI exists
if [ ! -f "$ACAT_SCORE_CLI" ]; then
    echo "[postflight-with-acat] Warning: acat-score CLI not found at $ACAT_SCORE_CLI, skipping ACAT enrichment" >&2
    cat "$EMPIRICA_RESULT"
    exit 0
fi

# Step 4: Call acat-score assess
echo "[postflight-with-acat] Running acat-score assess..." >&2

ACAT_CMD=(
    "python3" "$ACAT_SCORE_CLI" "assess"
    "--session-id" "$SESSION_ID"
    "--ai-id" "$AI_ID"
    "--rubric-version" "v1.0"
    "--model" "$MODEL"
    "--output" "json"
)

# Add API key if available
if [ -n "$API_KEY" ]; then
    ACAT_CMD+=("--api-key" "$API_KEY")
fi

# Run ACAT with timeout (150s matches hook timeout in acat_postflight_integration.py)
if timeout 150 "${ACAT_CMD[@]}" > "$ACAT_RESULT" 2>/dev/null; then
    echo "[postflight-with-acat] acat-score completed successfully" >&2

    # Step 5: Merge ACAT result into empirica result
    ACAT_GROUNDING=$(jq '.' "$ACAT_RESULT" 2>/dev/null || echo '{}')

    # Use jq to add acat_grounding section to empirica result
    jq --argjson acat_grounding "$ACAT_GROUNDING" \
        '.acat_grounding = $acat_grounding' \
        "$EMPIRICA_RESULT" > "$FINAL_RESULT"

    # Also add convergence signal if we have both vectors and ACAT phase
    if [ "$(echo "$ACAT_GROUNDING" | jq '.phase_score // empty')" != "" ]; then
        EMPIRICA_KNOW=$(jq -r '.vectors.know // 0.5' "$POSTFLIGHT_PAYLOAD")
        ACAT_PHASE_SCORE=$(echo "$ACAT_GROUNDING" | jq '.phase_score')
        DELTA=$(echo "$EMPIRICA_KNOW - ($ACAT_PHASE_SCORE / 4.0)" | bc -l | xargs printf "%.3f")

        jq --arg delta "$DELTA" \
            '.convergence = {"empirica_know": "'$EMPIRICA_KNOW'", "acat_phase_score": '$ACAT_PHASE_SCORE', "delta": '$DELTA'}' \
            "$FINAL_RESULT" > "$FINAL_RESULT.tmp"
        mv "$FINAL_RESULT.tmp" "$FINAL_RESULT"
    fi

    cat "$FINAL_RESULT"
else
    echo "[postflight-with-acat] Warning: acat-score failed or timed out, returning empirica result without ACAT enrichment" >&2
    cat "$EMPIRICA_RESULT"
fi

exit 0
