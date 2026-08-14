#!/usr/bin/env python3
"""
Cross-File Dependency Scanner — v1.0 (SKELETON)
Builder v1.7 compliant · diagnostic_tool

STATUS: Z1 DRAFT. Proposed in Leverage-Point Tooling Spec (entry #5),
NOT registered, NOT ratified. Requires Zone 2 review before build-out
or use against live governance files. This file is a structural
skeleton, not a finished tool -- the CANONICAL_FILES set and the
per-file rule functions below are placeholders and must be reviewed
against the actual current content of CURRENT.md, SESSION_RITUALS.md,
README, and OPERATOR_RUNBOOK before this is trusted for real use.

ARCHITECTURE NOTE (why this shape): this skeleton reuses a pattern
validated in a throwaway test fixture earlier in this session (a
Fibonacci sequence run through three unrelated "constrained generator"
formats, each paired with a causal-chain manifest). The fixture had
zero domain relevance to HumanAIOS -- what carried over is the control
flow only:

    root_event -> [ generator(constraint) for each downstream file ] -> (report, manifest)

Here:
  - root_event    = a newly registered principle or finding
  - generators    = one per canonical file, each encoding that file's
                     OWN update rule (not a shared rule -- this is the
                     part the fixture got right: each downstream
                     consumer has its own constraint grammar)
  - artifact      = human-readable checklist of stale/missing refs
  - manifest      = structured JSON trace of root -> which file ->
                     which rule -> why flagged, for Zone 2 review

This tool is detection/checklist only per the spec's stated boundary:
it greps and flags, it does NOT edit any canonical file. A human
still makes every edit.
"""
import json
import sys
import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

TOOL_NAME = "cross_file_dependency_scanner"
TOOL_VERSION = "1.0.0-skeleton"

# PLACEHOLDER: confirm this is still the correct canonical set and
# correct live paths before real use (Session-Open Fetch-and-Diff,
# entry #1 of the same spec, is the intended upstream check for this).
CANONICAL_FILES = {
    "CURRENT.md": "raw_github",
    "SESSION_RITUALS.md": "raw_github",
    "README.md": "raw_github",
    "OPERATOR_RUNBOOK.md": "local_only",  # humanaios-internal, per memory: never public GitHub
}


class SpecLoadFailed(Exception):
    pass


def load_file_text(path: str, source_hint: str) -> str:
    """
    Loads a canonical file's current text for scanning.
    PLACEHOLDER: real implementation must live-fetch raw_github paths
    (raw.githubusercontent.com/humanaios-ui/operations/main/[FILE])
    per the standing "never trust cached copies" rule, and read
    local_only paths from the humanaios-internal clone. This skeleton
    accepts pre-fetched text so the control flow can be tested without
    a live network dependency.
    """
    p = Path(path)
    if not p.exists():
        raise SpecLoadFailed(f"{path}: not found -- fetch live before scanning, do not skip")
    return p.read_text(encoding="utf-8")


# --- Per-file "generators": each canonical file gets its own rule set,
# mirroring the fixture's one-generator-per-constraint-grammar design.

def check_current_md(finding_id: str, finding_summary: str, text: str) -> dict:
    """CURRENT.md's rule: any new P-number or F-/H- ID referenced
    elsewhere in the doc set should appear in the current state summary."""
    hit = finding_id in text
    return {
        "file": "CURRENT.md",
        "rule": "new finding/principle ID should appear in current-state summary",
        "flagged": not hit,
        "detail": f"'{finding_id}' {'found' if hit else 'NOT found'} in CURRENT.md",
    }


def check_session_rituals_md(finding_id: str, finding_summary: str, text: str) -> dict:
    """SESSION_RITUALS.md's rule: if a finding changes a session-open
    or session-close STEP (vs. being purely descriptive), the ritual
    text should reference it."""
    ritual_keywords = ("session-open", "session close", "B.0", "B.6", "Phase 1", "Phase 3")
    plausibly_ritual_relevant = any(k.lower() in finding_summary.lower() for k in ritual_keywords)
    hit = finding_id in text
    return {
        "file": "SESSION_RITUALS.md",
        "rule": "finding affecting a ritual step should be referenced in ritual text",
        "flagged": plausibly_ritual_relevant and not hit,
        "detail": (
            f"finding summary suggests ritual relevance={plausibly_ritual_relevant}; "
            f"'{finding_id}' {'found' if hit else 'NOT found'} in SESSION_RITUALS.md"
        ),
    }


def check_readme_md(finding_id: str, finding_summary: str, text: str) -> dict:
    """README.md's rule: a NEW FILE (not a finding) should appear in
    the README index. For a finding/principle, README relevance is
    rare -- only flag if summary explicitly says 'new file' or 'new tool'."""
    is_new_artifact = any(k in finding_summary.lower() for k in ("new file", "new tool", "new skill"))
    hit = finding_id in text
    return {
        "file": "README.md",
        "rule": "new file/tool/skill should appear in README index",
        "flagged": is_new_artifact and not hit,
        "detail": f"new-artifact signal={is_new_artifact}; '{finding_id}' {'found' if hit else 'NOT found'} in README.md",
    }


def check_operator_runbook_md(finding_id: str, finding_summary: str, text: str) -> dict:
    """OPERATOR_RUNBOOK.md's rule: operator-facing procedure changes
    should be reflected here. Local-only file -- flagged conservatively
    since this tool cannot verify local state without being run
    on-disk in ~/Desktop/HAIOS-Main/."""
    procedural_keywords = ("operator", "runbook", "procedure", "workflow")
    plausibly_relevant = any(k in finding_summary.lower() for k in procedural_keywords)
    hit = finding_id in text
    return {
        "file": "OPERATOR_RUNBOOK.md",
        "rule": "operator-facing procedure change should be reflected in runbook",
        "flagged": plausibly_relevant and not hit,
        "detail": f"procedural signal={plausibly_relevant}; '{finding_id}' {'found' if hit else 'NOT found'} in OPERATOR_RUNBOOK.md",
    }


GENERATORS = {
    "CURRENT.md": check_current_md,
    "SESSION_RITUALS.md": check_session_rituals_md,
    "README.md": check_readme_md,
    "OPERATOR_RUNBOOK.md": check_operator_runbook_md,
}


def scan(finding_id: str, finding_summary: str, file_texts: dict) -> dict:
    """
    root_event -> per-file generator(constraint) -> (checklist, manifest)
    file_texts: {filename: text}, pre-loaded by caller (see load_file_text
    for the live-fetch contract this skeleton stands in for).
    """
    results = []
    for fname, generator in GENERATORS.items():
        text = file_texts.get(fname, "")
        results.append(generator(finding_id, finding_summary, text))

    manifest = {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "root_event": {"finding_id": finding_id, "summary": finding_summary},
        "causal_chain": [
            f"Root: {finding_id} registered ({finding_summary})",
            "Each canonical file checked against its own update rule (not a shared rule)",
            "Flags routed to Zone 2 for human disposition -- no file edited by this tool",
        ],
        "checks": results,
        "any_flagged": any(r["flagged"] for r in results),
    }
    return manifest


def run_smoke_test() -> bool:
    try:
        # Synthetic file_texts stand in for live-fetched content.
        file_texts = {
            "CURRENT.md": "Charter gates open. P31 ratified.",
            "SESSION_RITUALS.md": "B.0 verification block precedes Phase 3.",
            "README.md": "Index: acat_doc_v1.py, corpus_delta_analyzer_v1_0.py",
            "OPERATOR_RUNBOOK.md": "Operator procedure: session close sequence.",
        }

        # Case 1: finding not referenced anywhere, ritual-relevant summary
        # -> should flag CURRENT.md and SESSION_RITUALS.md, not README/runbook.
        result = scan("P32", "changes the Phase 1 session-open ritual step", file_texts)
        flagged_files = {c["file"] for c in result["checks"] if c["flagged"]}
        assert "CURRENT.md" in flagged_files, "expected CURRENT.md flagged when ID absent"
        assert "SESSION_RITUALS.md" in flagged_files, "expected ritual-relevant finding flagged"
        assert "README.md" not in flagged_files, "README should not flag for a non-artifact finding"

        # Case 2: finding already present everywhere relevant -> nothing flagged
        file_texts2 = dict(file_texts)
        file_texts2["CURRENT.md"] += " See F-100."
        file_texts2["SESSION_RITUALS.md"] += " Per F-100, ritual updated."
        result2 = scan("F-100", "documentation-only finding, no ritual/artifact impact", file_texts2)
        assert result2["any_flagged"] is False, "expected no flags when refs already present and no signal words"

        print("Smoke test PASSED")
        return True
    except AssertionError as e:
        print(f"Smoke test FAILED: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Cross-File Dependency Scanner v1.0 (SKELETON) -- Z1 DRAFT, not ratified"
    )
    parser.add_argument("--finding-id")
    parser.add_argument("--finding-summary")
    parser.add_argument(
        "--file",
        action="append",
        nargs=2,
        metavar=("NAME", "PATH"),
        help="canonical file name (must match CANONICAL_FILES keys) and local path to its pre-fetched text",
    )
    parser.add_argument("--smoke-test", action="store_true")
    args = parser.parse_args()

    if args.smoke_test:
        sys.exit(0 if run_smoke_test() else 1)

    if not (args.finding_id and args.finding_summary and args.file):
        parser.print_help()
        sys.exit(1)

    file_texts = {}
    for name, path in args.file:
        if name not in CANONICAL_FILES:
            print(f"WARNING: '{name}' not in CANONICAL_FILES -- skipping", file=sys.stderr)
            continue
        file_texts[name] = load_file_text(path, CANONICAL_FILES[name])

    manifest = scan(args.finding_id, args.finding_summary, file_texts)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
