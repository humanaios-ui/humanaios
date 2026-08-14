#!/bin/bash

# Load Testing Execution Script
# Runs all test scenarios sequentially and collects results
# Usage: ./run-all-tests.sh [--api-url http://localhost:3000]

set -e

# Configuration
API_URL="${1:-http://localhost:3000}"
RESULTS_DIR="./results"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_FILE="${RESULTS_DIR}/load-test-report-${TIMESTAMP}.md"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Ensure results directory exists
mkdir -p "${RESULTS_DIR}"

echo -e "${YELLOW}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${YELLOW}║  HumanAIOS Assessment API — Load Testing Suite        ║${NC}"
echo -e "${YELLOW}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "API URL: ${API_URL}"
echo "Results Directory: ${RESULTS_DIR}"
echo "Report: ${REPORT_FILE}"
echo ""

# Function to check API health
check_api_health() {
  echo -e "${YELLOW}[CHECK] Verifying API is running...${NC}"
  if curl -s -f "${API_URL}/health" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ API is healthy${NC}"
    return 0
  else
    echo -e "${RED}✗ API is not responding at ${API_URL}${NC}"
    echo "  Start the API with: npm run start"
    exit 1
  fi
}

# Function to run a test scenario
run_test() {
  local scenario_name=$1
  local config_file=$2
  local duration=$3

  echo ""
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${YELLOW}[TEST] ${scenario_name}${NC}"
  echo -e "${YELLOW}Config: ${config_file}${NC}"
  echo -e "${YELLOW}Duration: ${duration}${NC}"
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

  # Run test and capture output
  local json_report="${RESULTS_DIR}/${scenario_name// /_}-${TIMESTAMP}.json"

  artillery run \
    --target "${API_URL}" \
    "${config_file}" \
    --output "${json_report}" \
    2>&1 | tee "${RESULTS_DIR}/${scenario_name// /_}-${TIMESTAMP}.log"

  echo -e "${GREEN}✓ Test complete: ${json_report}${NC}"
  echo ""
}

# Main test execution
check_api_health

echo -e "${YELLOW}Starting load test suite...${NC}"
echo ""

# Track start time
START_TIME=$(date +%s)

# Run tests in order of increasing load
run_test "Baseline (1 user)" "assessment-submission.yml" "2 minutes"
run_test "Light Load (10 users)" "load-config-light.yml" "2 minutes"
run_test "Moderate Load (50 users)" "load-config-moderate.yml" "2 minutes"
run_test "Heavy Load (100 users)" "load-config-heavy.yml" "2 minutes"

echo ""
echo -e "${YELLOW}Note: Sustained load test takes 10 minutes${NC}"
echo -e "${YELLOW}Would you like to run sustained test now? (y/n)${NC}"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
  run_test "Sustained Load (50 users, 10 min)" "load-config-sustained.yml" "10 minutes"
fi

# Calculate total time
END_TIME=$(date +%s)
TOTAL_TIME=$((END_TIME - START_TIME))
TOTAL_MIN=$((TOTAL_TIME / 60))

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  Load Testing Suite Complete                          ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Total execution time: ${TOTAL_MIN} minutes"
echo "Results saved to: ${RESULTS_DIR}"
echo ""

# Generate summary report
echo "Generating summary report..."
cat > "${REPORT_FILE}" << REPORT_EOF
# Load Testing Results — ${TIMESTAMP}

## Test Execution Summary

- **API URL:** ${API_URL}
- **Test Date:** $(date)
- **Total Duration:** ${TOTAL_MIN} minutes
- **Test Suite:** Baseline, Light, Moderate, Heavy (+ Sustained if run)

## Test Results

### Raw Data
Results JSON files are available in \`results/\` directory:
- baseline-1_user-${TIMESTAMP}.json
- light_load_10_users-${TIMESTAMP}.json
- moderate_load_50_users-${TIMESTAMP}.json
- heavy_load_100_users-${TIMESTAMP}.json
- sustained_load_50_users_10_min-${TIMESTAMP}.json (if run)

### Analysis

Use the \`RESULTS_ANALYSIS_TEMPLATE.md\` to analyze each test:
1. Extract metrics from Artillery JSON output
2. Fill in the template for each scenario
3. Compare across concurrency levels
4. Identify bottlenecks

### Next Steps

1. **Review Metrics:** Check response times, error rates, throughput per test level
2. **Identify Bottleneck:** CPU? DB? Memory?
3. **Document Capacity:** Max concurrent users, throughput limits
4. **Optimization:** If needed, apply fixes and re-run tests

See \`README.md\` for detailed interpretation guide.

REPORT_EOF

echo -e "${GREEN}✓ Report generated: ${REPORT_FILE}${NC}"
echo ""
echo "Next steps:"
echo "1. Review JSON results in ${RESULTS_DIR}/"
echo "2. Fill out RESULTS_ANALYSIS_TEMPLATE.md for each test"
echo "3. Check for bottlenecks and optimization opportunities"
echo "4. See README.md for troubleshooting"
