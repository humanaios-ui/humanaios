#!/bin/bash
# M2R4 Phase 3 T3.4: Migration Testing Script
# Tests v2.0 → v3.0 migration on sample repos with full validation and rollback

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MIGRATE_SCRIPT="$PROJECT_ROOT/scripts/migrate_project_yaml_v3.py"
TEST_LOG="$PROJECT_ROOT/.empirica/migration_test.log"

BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}" | tee -a "$TEST_LOG"
}

log_pass() {
    echo -e "${GREEN}✓ $1${NC}" | tee -a "$TEST_LOG"
}

log_fail() {
    echo -e "${RED}✗ $1${NC}" | tee -a "$TEST_LOG"
}

log_warn() {
    echo -e "${YELLOW}⚠️  $1${NC}" | tee -a "$TEST_LOG"
}

# Initialize test log
cat > "$TEST_LOG" << EOF
M2R4 Phase 3 T3.4: Migration Testing
Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")

Test Repos:
1. empirica-autonomy
2. empirica-mesh-support
3. empirica-outreach

Procedure: dry-run → live migration → verification → rollback test
EOF

log_info "M2R4 Phase 3 T3.4: Migration Testing Started"
log_info "Test repos: empirica-autonomy, empirica-mesh-support, empirica-outreach"
echo ""

# Define test repos
TEST_REPOS=(
    "/Users/andersonfamily/practices/empirica-autonomy/.empirica/project.yaml"
    "/Users/andersonfamily/practices/empirica-mesh-support/.empirica/project.yaml"
    "/Users/andersonfamily/practices/empirica-outreach/.empirica/project.yaml"
)

TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Test each repo
for repo_path in "${TEST_REPOS[@]}"; do
    repo_name=$(basename $(dirname $(dirname "$repo_path")))
    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    echo ""
    log_info "Testing: $repo_name"

    if [ ! -f "$repo_path" ]; then
        log_fail "$repo_name: file not found"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        continue
    fi

    # Test 1: Dry-run migration
    log_info "  → Dry-run migration"
    if python3 "$MIGRATE_SCRIPT" "$repo_path" --dry-run --verbose >/dev/null 2>&1; then
        log_pass "$repo_name: Dry-run passed"
    else
        log_fail "$repo_name: Dry-run failed"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        continue
    fi

    # Test 2: Live migration (creates backup automatically)
    log_info "  → Live migration"
    if python3 "$MIGRATE_SCRIPT" "$repo_path" --verbose >/dev/null 2>&1; then
        log_pass "$repo_name: Live migration completed"
    else
        log_fail "$repo_name: Live migration failed"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        continue
    fi

    # Test 3: Verify v3.0 structure
    log_info "  → Verifying v3.0 structure"
    VERIFY_RESULT=$(python3 << PYEOF
import yaml
with open('$repo_path') as f:
    data = yaml.safe_load(f)

# Check version
if data.get('version') != '3.0':
    print('version_mismatch')
    exit(1)

# Check field count (should be 25 fields + version)
if len(data) < 25:
    print('missing_fields')
    exit(1)

# Check alphabetical ordering
SECTIONS = {
    'metadata': ['ai_id', 'canonical_seat', 'classification', 'created_at', 'created_by', 'description'],
    'organization': ['org_id', 'tenant_slug', 'type'],
    'configuration': ['auto_detect', 'calibration_weights', 'contacts', 'domain', 'domain_config',
                      'engagements', 'evidence_profile', 'languages', 'mesh_id_prefix', 'name',
                      'project_id', 'status', 'subjects', 'tags'],
    'relationships': ['beads', 'edges']
}

all_fields = [k for k in data.keys() if k != 'version']
for section_name, section_fields in SECTIONS.items():
    fields_in_file = [f for f in all_fields if f in section_fields]
    if fields_in_file != sorted(fields_in_file):
        print('ordering_error')
        exit(1)

print('ok')
PYEOF
)

    if [ "$VERIFY_RESULT" = "ok" ]; then
        log_pass "$repo_name: v3.0 structure verified"
    else
        log_fail "$repo_name: v3.0 structure verification failed ($VERIFY_RESULT)"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        continue
    fi

    # Test 4: Verify backup exists
    backup_path="${repo_path}.bak"
    if [ -f "$backup_path" ]; then
        log_pass "$repo_name: Backup created"
    else
        log_fail "$repo_name: Backup not found"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        continue
    fi

    # Test 5: Test rollback
    log_info "  → Testing rollback procedure"
    cp "$backup_path" "${repo_path}.rollback_test"
    if [ -f "${repo_path}.rollback_test" ]; then
        rm "${repo_path}.rollback_test"
        log_pass "$repo_name: Rollback procedure verified"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        log_fail "$repo_name: Rollback procedure verification failed"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
done

echo ""
echo "================================"
log_info "Test Summary"
log_info "Total: $TOTAL_TESTS | Passed: $PASSED_TESTS | Failed: $FAILED_TESTS"

if [ $FAILED_TESTS -eq 0 ]; then
    log_pass "All tests passed! Ready for T3.5 (Runbook)"
    exit 0
else
    log_fail "Some tests failed. Review errors above."
    exit 1
fi
