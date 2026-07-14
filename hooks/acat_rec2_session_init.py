#!/usr/bin/env python3
"""
ACAT Integration Recommendation 2: Auto-create `acat_current_session.json` at session-create time

Trigger: SessionStart hook (startup|resume)
Zone: 1 (draft) → requires autonomy integration
Implementation: empirica hook or Claude Code settings.json

When: Every new session starts, automatically create a blank ACAT state file
Why: Enables ACAT tracking from session start without manual setup
Flow: session-init → creates .empirica/acat_current_session.json with empty state
"""

import json
import os
import uuid
from pathlib import Path
from datetime import datetime


BLANK_ACAT_STATE = {
    "acat_session_id": str(uuid.uuid4()),
    "empirica_session_id": "",  # Will be populated by empirica runtime
    "agent_name": "",  # Will be populated if known
    "submission_purity": "two_stage_verified",
    "corpus_source": "empirica_session",
    "exercise_id": "",
    "exercise_path": "",
    "exercise_category": "",
    "dimension_focus": [],
    "student_persona": {},
    "p1_submitted": False,
    "p1_scores": {},
    "p2_submitted": False,
    "p2_observability_log": "",
    "p3_submitted": False,
    "p3_scores": {},
    "p3_delta_per_dimension": {},
    "verifier_submitted": False,
    "verifier_scores": {},
    "session_transcript_ref": "",
    "created_at": datetime.utcnow().isoformat() + "Z",
    "observability_summary": {},
}


def create_acat_session_state(project_root: Path = None) -> dict:
    """
    Create a new ACAT session state file at project root.

    Args:
        project_root: Path to project root. Defaults to current directory.

    Returns:
        Dict with creation status + path
    """
    if project_root is None:
        project_root = Path.cwd()
    else:
        project_root = Path(project_root)

    acat_dir = project_root / ".empirica"
    acat_dir.mkdir(parents=True, exist_ok=True)

    state_file = acat_dir / "acat_current_session.json"

    # Check if file already exists (don't overwrite)
    if state_file.exists():
        try:
            with open(state_file, "r") as f:
                existing = json.load(f)
            # If it has p1/p3 scores, it's an active session — don't reset
            if existing.get("p1_submitted") or existing.get("p3_submitted"):
                return {
                    "ok": True,
                    "action": "skipped",
                    "reason": "Active ACAT session detected (p1/p3 scores present)",
                    "path": str(state_file),
                }
        except (json.JSONDecodeError, IOError):
            pass  # File is corrupted or unreadable — overwrite below

    # Write new state
    try:
        with open(state_file, "w") as f:
            json.dump(BLANK_ACAT_STATE, f, indent=2)
        return {
            "ok": True,
            "action": "created",
            "path": str(state_file),
            "acat_session_id": BLANK_ACAT_STATE["acat_session_id"],
        }
    except IOError as e:
        return {
            "ok": False,
            "action": "failed",
            "error": str(e),
        }


def hook_handler(event_data: dict) -> dict:
    """
    Hook handler for SessionStart:startup|resume events.

    Expected event_data:
    {
        "event": "SessionStart",
        "trigger": "startup" | "resume",
        "project_root": "/path/to/project"
    }
    """
    project_root = event_data.get("project_root")
    trigger = event_data.get("trigger", "startup")

    result = create_acat_session_state(project_root)

    if result["ok"]:
        action_desc = "created" if result["action"] == "created" else "skipped"
        print(f"[ACAT REC 2] Session state {action_desc}: {result.get('path')}")
    else:
        print(f"[ACAT REC 2] ERROR: {result.get('error')}")

    return result


if __name__ == "__main__":
    # Test: create session state in current directory
    result = create_acat_session_state()
    print(json.dumps(result, indent=2))
