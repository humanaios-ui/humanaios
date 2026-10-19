#!/usr/bin/env python3
"""Create a metadata-only inventory of every path in an immutable Git tree."""

import argparse
import json
import os
import re
import subprocess
from collections import Counter
from pathlib import Path


TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".jsonl",
    ".md",
    ".py",
    ".sh",
    ".sql",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
BINARY_SUFFIXES = {".db", ".docx", ".jpg", ".jpeg", ".png", ".pdf", ".pyc"}
SENSITIVE_PATH_MARKERS = (".empirica", ".env", "mailbox_state", "secret", "credential")


def parse_tree(output):
    """Parse `git ls-tree -rz` records without treating path bytes as delimiters."""
    entries = []
    for record in output.split(b"\0"):
        if not record:
            continue
        metadata, path = record.split(b"\t", 1)
        mode, object_type, object_id = metadata.decode("ascii").split(" ", 2)
        entries.append(
            {
                "path": path.decode("utf-8", "surrogateescape"),
                "mode": mode,
                "object_type": object_type,
                "object_id": object_id,
            }
        )
    return entries


def classify(entry):
    path = entry["path"]
    mode = entry["mode"]
    object_type = entry["object_type"]
    suffix = Path(path).suffix.lower()

    if mode == "160000" or object_type == "commit":
        source_kind = "submodule"
        object_access = "submodule-pointer-only; contents not in the parent tree"
        review_state = "metadata-only"
        disposition = "excluded-from-content-review; submodule contents not enumerated"
    elif mode == "120000":
        source_kind = "symlink"
        object_access = "symlink-object-only; target not followed"
        review_state = "metadata-only"
        disposition = "excluded-from-following; symlink target not followed"
    elif suffix == ".pyc":
        source_kind = "generated"
        object_access = "git-blob-unverified; tree listing does not confirm local content accessibility"
        review_state = "metadata-only"
        disposition = "excluded-from-text-review; compiled artifact identified by suffix"
    elif suffix in BINARY_SUFFIXES:
        source_kind = "binary-or-media"
        object_access = "git-blob-unverified; tree listing does not confirm local content accessibility"
        review_state = "metadata-only"
        disposition = "excluded-from-text-review; binary/media type inferred from suffix"
    elif suffix in TEXT_SUFFIXES or path.rsplit("/", 1)[-1] in {
        ".gitignore",
        ".prettierrc",
        "CODEOWNERS",
        "LICENSE",
    }:
        source_kind = "text-or-source-candidate"
        object_access = "git-blob-unverified; tree listing does not confirm local content accessibility"
        review_state = "pending"
        disposition = "pending-content, owner, and controlling-document review"
    else:
        source_kind = "unclassified"
        object_access = "git-blob-unverified; tree listing does not confirm local content accessibility"
        review_state = "pending"
        disposition = "pending-type, content, owner, and controlling-document review"

    lower_path = path.lower()
    sensitive_candidate = any(marker in lower_path for marker in SENSITIVE_PATH_MARKERS)
    return {
        **entry,
        "source_kind": source_kind,
        "object_access": object_access,
        "sensitivity": "candidate" if sensitive_candidate else "unassessed",
        "sensitivity_basis": (
            "path-name heuristic only; contents not inspected"
            if sensitive_candidate
            else "not assessed; contents not inspected"
        ),
        "review_state": review_state,
        "controlling_doc_id": "PENDING",
        "owner": "PENDING",
        "disposition": disposition,
    }


def inventory(commit):
    # Accept only an immutable object ID; never let a moving ref choose the audit baseline.
    if not re.fullmatch(r"[0-9a-fA-F]{40}", commit):
        raise ValueError("Expected a full 40-character commit SHA")
    # Git hooks can set GIT_DIR/GIT_WORK_TREE for an unrelated repository.
    clean_env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    resolved = subprocess.run(
        ["git", "rev-parse", "--verify", f"{commit}^{{commit}}"],
        check=True,
        capture_output=True,
        timeout=120,
        env=clean_env,
        text=True,
    ).stdout.strip()
    tree = subprocess.run(
        ["git", "ls-tree", "-r", "-z", "--full-tree", resolved],
        check=True,
        capture_output=True,
        timeout=120,
        env=clean_env,
    ).stdout
    items = [classify(entry) for entry in parse_tree(tree)]
    return {
        "format": "humanaios-document-intelligence-census-v1",
        "commit": resolved,
        "tracked_path_count": len(items),
        "counts_by_source_kind": dict(sorted(Counter(i["source_kind"] for i in items).items())),
        "counts_by_review_state": dict(sorted(Counter(i["review_state"] for i in items).items())),
        "items": items,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", required=True, help="Git commit to inventory")
    parser.add_argument("--output", required=True, type=Path, help="JSON output path")
    args = parser.parse_args()

    result = inventory(args.commit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Inventoried {result['tracked_path_count']} paths at {result['commit']}; "
        f"review states: {result['counts_by_review_state']}"
    )


if __name__ == "__main__":
    main()
