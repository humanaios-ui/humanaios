#!/usr/bin/env python3
"""
Add YAML frontmatter to markdown files.
Usage:
  python add_frontmatter.py --file <path> --doc-id HAIOS-GOV-013 --title "My Title" --status review
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta

def add_frontmatter(file_path: Path, doc_id: str, title: str, area: str,
                    status: str = "draft", owner: str = "@carly") -> bool:
    """Add frontmatter to a markdown file."""

    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}")
        return False

    content = file_path.read_text(encoding="utf-8")

    # Check if already has frontmatter
    if content.startswith("---"):
        print(f"WARNING: {file_path.name} already has frontmatter. Skipping.")
        return False

    # Create review_due date (3 months from now)
    today = datetime.now().date()
    review_due = today + timedelta(days=90)

    frontmatter = f"""---
doc_id: {doc_id}
title: {title}
revision: 1
status: {status}
owner: "{owner}"
created_date: {today.isoformat()}
review_due: {review_due.isoformat()}
canonical: true
retention: permanent
---
"""

    # Prepend frontmatter
    new_content = frontmatter + content
    file_path.write_text(new_content, encoding="utf-8")

    print(f"✓ Added frontmatter to {file_path.name}")
    print(f"  doc_id: {doc_id}")
    print(f"  status: {status}")
    print(f"  review_due: {review_due.isoformat()}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Add YAML frontmatter to markdown files")
    parser.add_argument("--file", type=Path, required=True, help="Path to .md file")
    parser.add_argument("--doc-id", required=True, help="doc_id (e.g., HAIOS-GOV-013)")
    parser.add_argument("--title", required=True, help="Document title")
    parser.add_argument("--area", required=True, help="Document area (GOV, PROC, SPEC, TEST, VIS, OPS)")
    parser.add_argument("--status", default="draft", choices=["draft", "review", "approved"],
                        help="Initial status")
    parser.add_argument("--owner", default="@carly", help="Owner identifier")

    args = parser.parse_args()

    if add_frontmatter(args.file, args.doc_id, args.title, args.area, args.status, args.owner):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
