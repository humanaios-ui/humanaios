#!/bin/bash
# Activate enforcement: Link pre-commit hook into git
# This makes the resource-keyed validator mandatory for all commits

set -u

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOOK_SRC="$REPO_ROOT/hooks/pre-commit-resource-keyed"
HOOK_DEST="$REPO_ROOT/.git/hooks/pre-commit"

if [[ ! -f "$HOOK_SRC" ]]; then
    echo "❌ Hook source not found: $HOOK_SRC"
    exit 1
fi

echo "📌 Linking pre-commit hook..."
mkdir -p "$REPO_ROOT/.git/hooks"

if [[ -f "$HOOK_DEST" ]]; then
    echo "   Backing up existing hook to $HOOK_DEST.bak"
    mv "$HOOK_DEST" "$HOOK_DEST.bak"
fi

ln -sf "$HOOK_SRC" "$HOOK_DEST"
chmod +x "$HOOK_DEST"

echo "✅ Resource-keyed enforcement activated"
echo ""
echo "From now on:"
echo "  ✓ All goal/task commits validated before landing in git"
echo "  ✓ Temporal framing rejected at commit time (not after the fact)"
echo "  ✓ This is not optional—it's structural"
echo ""
echo "To test:"
echo "  echo '\"by Friday\"' > test.json && git add test.json && git commit -m 'test'"
echo "  (Should reject)"
echo ""
echo "To verify enforcement is active:"
echo "  cat $HOOK_DEST | grep 'pre-commit-resource-keyed'"
