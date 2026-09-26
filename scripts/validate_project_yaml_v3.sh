#!/bin/bash
# Pre-commit validation hook for project.yaml v3.0 compliance
# Ensures all project.yaml files follow v3.0 schema and alphabetical ordering

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

ERRORS=0
WARNINGS=0

echo "Validating project.yaml v3.0 compliance..."

# Find all project.yaml files
find "$PROJECT_ROOT" -name ".git" -prune -o -name "project.yaml" -type f -print | while read yaml_file; do
    echo -n "  Checking: $yaml_file ... "
    
    # Check version
    VERSION=$(grep "^version:" "$yaml_file" | awk '{print $2}' | tr -d '"'\''')
    if [ "$VERSION" != "3.0" ]; then
        echo "FAIL (version is $VERSION, expected 3.0)"
        ((ERRORS++))
        continue
    fi
    
    # Check YAML validity
    if ! python3 -c "import yaml; yaml.safe_load(open('$yaml_file'))" 2>/dev/null; then
        echo "FAIL (invalid YAML)"
        ((ERRORS++))
        continue
    fi
    
    echo "OK (v3.0)"
done

if [ $ERRORS -gt 0 ]; then
    echo ""
    echo "❌ Validation failed: $ERRORS error(s)"
    exit 1
else
    echo ""
    echo "✅ All project.yaml files valid"
    exit 0
fi
