#!/usr/bin/env python3
"""
Frontmatter validator for HAIOS controlled documents.
Validates YAML frontmatter against schema per DOCUMENT_CONTROL_PLAN.md §4.
Usage:
  python validate_frontmatter.py <file.md>
  python validate_frontmatter.py <directory>  # batch mode
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, Tuple, List

try:
    import yaml
    import jsonschema
except ImportError:
    print("ERROR: Install required packages: pip install pyyaml jsonschema")
    sys.exit(1)


class FrontmatterValidator:
    """Validate YAML frontmatter against the HAIOS controlled document schema."""

    SCHEMA_PATH = Path(__file__).parent / "frontmatter.schema.json"

    def __init__(self):
        with open(self.SCHEMA_PATH) as f:
            self.schema = json.load(f)

    def extract_frontmatter(self, content: str) -> Tuple[Dict, str, int]:
        """Extract YAML frontmatter from markdown. Return (dict, body, line_offset)."""
        if not content.startswith("---"):
            return {}, content, 0

        lines = content.split("\n")
        end_idx = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                end_idx = i
                break

        if end_idx is None:
            return {}, content, 0

        fm_text = "\n".join(lines[1:end_idx])
        body = "\n".join(lines[end_idx + 1:])

        try:
            data = yaml.safe_load(fm_text) or {}
        except yaml.YAMLError as e:
            return None, None, e

        return data, body, end_idx + 1

    def validate(self, file_path: Path) -> Tuple[bool, List[str]]:
        """Validate a single markdown file. Return (is_valid, errors)."""
        if not file_path.exists():
            return False, [f"File not found: {file_path}"]

        if not file_path.suffix == ".md":
            return False, [f"Not a markdown file: {file_path}"]

        content = file_path.read_text(encoding="utf-8")
        fm, body, offset = self.extract_frontmatter(content)

        errors = []

        if fm is None:
            errors.append(f"Line {offset}: Invalid YAML frontmatter — {body}")
            return False, errors

        if not fm:
            errors.append("Missing YAML frontmatter (---...---)")
            return False, errors

        # Convert date objects back to ISO format strings for schema validation
        for date_field in ['created_date', 'review_due', 'approved_date']:
            if date_field in fm and isinstance(fm[date_field], __import__('datetime').date):
                fm[date_field] = fm[date_field].isoformat()

        # Validate against schema
        try:
            jsonschema.validate(instance=fm, schema=self.schema)
        except jsonschema.ValidationError as e:
            errors.append(f"Schema validation failed: {e.message}")
            if e.path:
                errors.append(f"  Field: {'.'.join(str(p) for p in e.path)}")
            return False, errors

        # Additional business logic validation
        status = fm.get("status")
        if status == "approved" and not fm.get("approved_by"):
            errors.append("status=approved requires approved_by field")

        if status == "approved" and not fm.get("approved_date"):
            errors.append("status=approved requires approved_date field")

        if fm.get("canonical") is not True:
            errors.append("canonical must be explicitly set to true")

        return len(errors) == 0, errors

    def validate_batch(self, directory: Path) -> Dict[str, Tuple[bool, List[str]]]:
        """Validate all .md files in directory. Return {file: (valid, errors)}."""
        results = {}
        for md_file in directory.rglob("*.md"):
            valid, errors = self.validate(md_file)
            results[str(md_file)] = (valid, errors)
        return results

    def validate_registry_uniqueness(self, registry_path: Path) -> Tuple[bool, List[str]]:
        """Validate that document-registry.yaml has unique doc_ids and only one canonical per id."""
        if not registry_path.exists():
            return True, []  # No registry yet

        with open(registry_path) as f:
            registry = yaml.safe_load(f) or {}

        errors = []
        doc_ids = {}

        for doc in registry.get("documents", []):
            doc_id = doc.get("doc_id")
            if not doc_id:
                errors.append("Registry entry missing doc_id")
                continue

            if doc_id in doc_ids:
                errors.append(f"Duplicate doc_id: {doc_id} at paths: {doc_ids[doc_id]['path']}, {doc['path']}")

            if doc.get("canonical"):
                if doc_id in doc_ids and doc_ids[doc_id].get("canonical"):
                    errors.append(f"Multiple canonical entries for doc_id {doc_id}")
                doc_ids[doc_id] = doc

        return len(errors) == 0, errors


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_frontmatter.py <file.md> | <directory>")
        sys.exit(1)

    target = Path(sys.argv[1])
    validator = FrontmatterValidator()

    if target.is_file():
        valid, errors = validator.validate(target)
        if valid:
            print(f"✓ {target}: frontmatter valid")
            return 0
        else:
            print(f"✗ {target}: frontmatter invalid")
            for error in errors:
                print(f"  {error}")
            return 1

    elif target.is_dir():
        results = validator.validate_batch(target)
        valid_count = sum(1 for v, _ in results.values() if v)
        total_count = len(results)

        print(f"Batch validation: {valid_count}/{total_count} files valid\n")

        for file, (valid, errors) in sorted(results.items()):
            if not valid:
                print(f"✗ {file}")
                for error in errors:
                    print(f"  {error}")

        return 0 if valid_count == total_count else 1

    else:
        print(f"Path not found: {target}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
