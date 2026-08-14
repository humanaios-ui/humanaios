#!/usr/bin/env python3
"""
anchor_bpr_to_git.py -- Anchor BPR entry hash to git notes for permanent audit trail.

Usage:
  python3 scripts/anchor_bpr_to_git.py \
    --commit 85f1431 \
    --entry-id "BPR-anthropic-claude-20260914-001" \
    --entry-hash "abc123def456..." \
    --embargo-end "2026-10-14T23:59:59Z" \
    --protocol "ACAT-CAL-P v1.5 + Phase 1 Amendments"

Adds a git note to the specified commit linking it to the BPR entry hash.
This creates an immutable, append-only audit trail.

Requirements:
  - Git repository in current directory
  - Commit SHA exists
  - BPR entry has been published (hash is canonical)
"""

import sys
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

def run_git_command(args: list) -> tuple[int, str, str]:
    """Execute git command and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def verify_git_repo() -> bool:
    """Check if we're in a git repository."""
    code, _, _ = run_git_command(["rev-parse", "--git-dir"])
    return code == 0

def verify_commit_exists(commit: str) -> bool:
    """Verify commit SHA exists in repo."""
    code, _, _ = run_git_command(["cat-file", "-t", commit])
    return code == 0

def add_git_note(commit: str, entry_id: str, entry_hash: str, embargo_end: str, protocol: str) -> bool:
    """
    Add a git note to the commit linking to BPR entry.

    Format:
    ```
    BPR-ENTRY-ANCHOR v1
    entry_id: BPR-anthropic-claude-20260914-001
    entry_hash: abc123def456...
    embargo_end: 2026-10-14T23:59:59Z
    protocol: ACAT-CAL-P v1.5 + Phase 1 Amendments
    anchored_at: 2026-09-20T15:30:00Z
    ```
    """
    note_content = f"""BPR-ENTRY-ANCHOR v1
entry_id: {entry_id}
entry_hash: {entry_hash}
embargo_end: {embargo_end}
protocol: {protocol}
anchored_at: {datetime.utcnow().isoformat()}Z
"""

    code, _, err = run_git_command([
        "notes", "add", "-m", note_content, commit
    ])

    if code != 0:
        print(f"✗ Failed to add git note: {err}", file=sys.stderr)
        return False

    return True

def show_git_note(commit: str) -> tuple[int, str]:
    """Retrieve git note for commit."""
    code, output, _ = run_git_command(["notes", "show", commit])
    return code, output

def main():
    parser = argparse.ArgumentParser(
        description="Anchor BPR entry hash to git commit via notes"
    )
    parser.add_argument("--commit", required=True, help="Git commit SHA (or short SHA)")
    parser.add_argument("--entry-id", required=True, help="BPR entry ID")
    parser.add_argument("--entry-hash", required=True, help="BPR entry SHA256 hash")
    parser.add_argument("--embargo-end", required=True, help="Embargo end timestamp (ISO 8601)")
    parser.add_argument("--protocol", required=True, help="Measurement protocol")
    parser.add_argument("--verify-only", action="store_true", help="Only verify, don't add note")

    args = parser.parse_args()

    # Verify we're in a git repo
    if not verify_git_repo():
        print("✗ Not in a git repository", file=sys.stderr)
        return 1

    # Verify commit exists
    if not verify_commit_exists(args.commit):
        print(f"✗ Commit not found: {args.commit}", file=sys.stderr)
        return 1

    print(f"✓ Git repository verified")
    print(f"✓ Commit verified: {args.commit}")
    print()

    # Validate entry hash format (SHA256 = 64 hex chars)
    if len(args.entry_hash) != 64 or not all(c in '0123456789abcdef' for c in args.entry_hash.lower()):
        print(f"✗ Invalid entry hash (must be 64-char SHA256): {args.entry_hash}", file=sys.stderr)
        return 1

    print(f"Entry Details:")
    print(f"  ID: {args.entry_id}")
    print(f"  Hash: {args.entry_hash}")
    print(f"  Embargo End: {args.embargo_end}")
    print(f"  Protocol: {args.protocol}")
    print()

    if args.verify_only:
        print("--verify-only mode: not adding note")
        return 0

    # Add git note
    if add_git_note(args.commit, args.entry_id, args.entry_hash, args.embargo_end, args.protocol):
        print(f"✓ Git note added to {args.commit}")
        print()

        # Show the note
        code, note = show_git_note(args.commit)
        if code == 0:
            print("Note content:")
            for line in note.split("\n"):
                print(f"  {line}")
        print()
        print("To view this note later:")
        print(f"  git notes show {args.commit}")
        print()
        print("To see notes in git log:")
        print(f"  git log --notes {args.commit}~1..{args.commit}")
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
