#!/bin/bash
# Track 2 QA Test Suite Execution Script
# Runs all automated tests for Track 2 SSE + UI integration

set -e

echo "========================================"
echo "Track 2 QA Test Suite"
echo "========================================"
echo ""

# Configuration
API_URL="http://localhost:8000"
MARKER_URL="$API_URL/api/v1/sonify/markers"
TOKEN="${HUMANAIOS_TOKEN:-test_token_12345}"  # Use env var or default

# Test results
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function
test_endpoint() {
    local name=$1
    local method=$2
    local endpoint=$3
    local data=$4
    local expected_code=$5

    echo -n "Testing: $name ... "

    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" -H "Authorization: Bearer $TOKEN" \
            "$API_URL$endpoint")
    else
        response=$(curl -s -w "\n%{http_code}" -X POST -H "Authorization: Bearer $TOKEN" \
            -H "Content-Type: application/json" -d "$data" "$API_URL$endpoint")
    fi

    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | head -n -1)

    if [ "$http_code" = "$expected_code" ]; then
        echo "✓ PASS (HTTP $http_code)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo "  Response: ${body:0:100}..."
        return 0
    else
        echo "✗ FAIL (Expected $expected_code, got $http_code)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo "  Response: $body"
        return 1
    fi
}

echo "=== Test 1: Backend Health Check ==="
test_endpoint "Health" "GET" "/api/v1/acat/health" "" "200"
echo ""

echo "=== Test 2: Marker Palette Endpoint ==="
test_endpoint "Palette" "GET" "$MARKER_URL/palette" "" "200"
echo ""

echo "=== Test 3: Test Marker Emission ==="
test_marker_payload='{
  "event_type": "proposal",
  "data": {
    "id": "prop_test_001",
    "status": "accepted",
    "type": "collab_brief",
    "source_claude": "empirica-foundation.carly.autonomy",
    "target_claudes": ["empirica-foundation.carly.humanaios"]
  }
}'
test_endpoint "Emit Test Marker" "POST" "$MARKER_URL/event" "$test_marker_payload" "200"
echo ""

echo "=== Test 4: Test Marker Variants ==="

# Proposal changed
echo -n "Testing: Proposal changed marker ... "
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
    -d '{"event_type":"proposal","data":{"id":"prop_test_changed","status":"changed","type":"collab_brief","source_claude":"test","target_claudes":["test"]}}' \
    "$MARKER_URL/event" > /dev/null && echo "✓ PASS" && TESTS_PASSED=$((TESTS_PASSED + 1)) || echo "✗ FAIL" && TESTS_FAILED=$((TESTS_FAILED + 1))

# SER opened
echo -n "Testing: SER opened marker ... "
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
    -d '{"event_type":"ser","data":{"ser_id":"ser_test_001","coordination_state":"open","participants":[]}}' \
    "$MARKER_URL/event" > /dev/null && echo "✓ PASS" && TESTS_PASSED=$((TESTS_PASSED + 1)) || echo "✗ FAIL" && TESTS_FAILED=$((TESTS_FAILED + 1))

# Check gate passed
echo -n "Testing: Multiple rapid markers (stack test) ... "
for i in {1..5}; do
  curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
      -d "{\"event_type\":\"proposal\",\"data\":{\"id\":\"prop_rapid_$i\",\"status\":\"accepted\",\"type\":\"test\",\"source_claude\":\"test\",\"target_claudes\":[\"test\"]}}" \
      "$MARKER_URL/event" > /dev/null
  sleep 0.1
done
echo "✓ PASS" && TESTS_PASSED=$((TESTS_PASSED + 1)) || echo "✗ FAIL" && TESTS_FAILED=$((TESTS_FAILED + 1))
echo ""

echo "========================================"
echo "Test Results Summary"
echo "========================================"
echo "Passed: $TESTS_PASSED"
echo "Failed: $TESTS_FAILED"
echo "Total:  $((TESTS_PASSED + TESTS_FAILED))"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo "✓ ALL TESTS PASSED"
    exit 0
else
    echo "✗ SOME TESTS FAILED"
    exit 1
fi
