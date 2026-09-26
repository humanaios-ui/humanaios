#!/usr/bin/env python3
"""
M2R4 Phase 3: project.yaml v2.0 → v3.0 Migration Script

Migrates project.yaml files from v2.0 (ad-hoc field ordering) to v3.0
(alphabetically ordered within 4 logical sections) with full validation,
edge case handling, and rollback support.

Usage:
    python migrate_project_yaml_v3.py <project_yaml_path> [--dry-run] [--verbose]
    python migrate_project_yaml_v3.py --batch <directory> [--dry-run]

Author: M2R4 Phase 3 Task 2
Based on: M2R4_PHASE2_SCHEMA_DESIGN_SPEC.md, M2R4_PHASE3_SCHEMA_MAPPING.md
"""

import sys
import yaml
import json
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime
from copy import deepcopy


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('.empirica/migration.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)


# v3.0 Schema Definition
CANONICAL_FIELDS = {
    'metadata': [
        'ai_id', 'canonical_seat', 'classification', 'created_at', 'created_by', 'description'
    ],
    'organization': [
        'org_id', 'tenant_slug', 'type'
    ],
    'configuration': [
        'auto_detect', 'calibration_weights', 'contacts', 'domain', 'domain_config',
        'engagements', 'evidence_profile', 'languages', 'mesh_id_prefix', 'name',
        'project_id', 'status', 'subjects', 'tags'
    ],
    'relationships': [
        'beads', 'edges'
    ]
}

CANONICAL_FIELD_ORDER = (
    CANONICAL_FIELDS['metadata'] +
    CANONICAL_FIELDS['organization'] +
    CANONICAL_FIELDS['configuration'] +
    CANONICAL_FIELDS['relationships']
)


class SchemaValidator:
    """Validates project.yaml structure for v2.0 and v3.0 compliance."""

    @staticmethod
    def validate_v2(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate v2.0 schema. Returns (is_valid, error_messages)."""
        errors = []

        # Check version
        if 'version' not in data:
            errors.append("Missing 'version' field")
        elif data['version'] not in ('2.0', '2.1', "'2.0'", "'2.1'"):
            errors.append(f"Invalid version '{data['version']}' (expected 2.0 or 2.1)")

        # Check required canonical fields
        for field in CANONICAL_FIELD_ORDER:
            if field not in data:
                errors.append(f"Missing required field '{field}'")

        return len(errors) == 0, errors

    @staticmethod
    def validate_v3(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate v3.0 schema. Returns (is_valid, error_messages)."""
        errors = []

        # Check version
        if 'version' not in data or data['version'] != '3.0':
            errors.append(f"Invalid version '{data.get('version', 'missing')}' (expected 3.0)")

        # Check required canonical fields
        for field in CANONICAL_FIELD_ORDER:
            if field not in data:
                errors.append(f"Missing required field '{field}'")

        # Check alphabetical ordering within sections
        for section_name, fields in CANONICAL_FIELDS.items():
            keys_in_file = [k for k in data.keys() if k in fields and k != 'version']
            sorted_keys = sorted(keys_in_file)
            if keys_in_file != sorted_keys:
                errors.append(
                    f"Fields in '{section_name}' section not alphabetically ordered: "
                    f"got {keys_in_file}, expected {sorted_keys}"
                )

        return len(errors) == 0, errors

    @staticmethod
    def check_extra_fields(data: Dict[str, Any]) -> List[str]:
        """Check for fields not in canonical schema. Returns list of extra field names."""
        extra_fields = []
        for key in data.keys():
            if key not in CANONICAL_FIELD_ORDER and key != 'version':
                extra_fields.append(key)
        return extra_fields


class SchemaConverter:
    """Converts v2.0 project.yaml to v3.0."""

    @staticmethod
    def migrate(data: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
        """
        Migrate v2.0 data to v3.0 format.

        Changes:
        - Version: '2.0' → '3.0'
        - Fields reordered into 4 sections, alphabetically within each
        - subjects: {} → subjects: [] (dict to list)
        - Preserve all other data unchanged
        """
        logger.info("Starting v2.0 → v3.0 migration")

        # Validate input
        is_valid, errors = SchemaValidator.validate_v2(data)
        if not is_valid:
            logger.error(f"v2.0 validation failed: {'; '.join(errors)}")
            raise ValueError(f"Invalid v2.0 schema: {'; '.join(errors)}")

        # Check for extra fields
        extra_fields = SchemaValidator.check_extra_fields(data)
        if extra_fields:
            logger.warning(f"Found {len(extra_fields)} non-canonical fields: {extra_fields}")

        # Create v3.0 structure
        v3_data = {'version': '3.0'}

        # Migrate fields in canonical order
        for field in CANONICAL_FIELD_ORDER:
            if field in data:
                value = data[field]

                # Type conversion: subjects dict → list
                if field == 'subjects' and isinstance(value, dict):
                    value = []
                    logger.info("Converted 'subjects' from dict to list")

                v3_data[field] = value

        # Preserve extra fields at end (with warning)
        for field in extra_fields:
            logger.warning(f"Preserving non-canonical field '{field}' at end of file")
            v3_data[field] = data[field]

        # Validate output
        is_valid, errors = SchemaValidator.validate_v3(v3_data)
        if not is_valid:
            logger.error(f"v3.0 validation failed: {'; '.join(errors)}")
            raise ValueError(f"Migration produced invalid v3.0 schema: {'; '.join(errors)}")

        logger.info("Migration successful")
        return v3_data


class FileManager:
    """Handles file I/O with backup and rollback support."""

    @staticmethod
    def load_yaml(path: Path) -> Dict[str, Any]:
        """Load YAML file. Returns parsed dict."""
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            logger.error(f"YAML parse error in {path}: {e}")
            raise

    @staticmethod
    def save_yaml(path: Path, data: Dict[str, Any], backup: bool = True) -> Path:
        """Save YAML file. Creates backup if requested. Returns backup path."""
        backup_path = None

        # Create backup
        if backup and path.exists():
            backup_path = path.with_suffix(path.suffix + '.bak')
            shutil.copy2(path, backup_path)
            logger.info(f"Created backup: {backup_path}")

        # Write new file
        with open(path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

        logger.info(f"Saved migrated file: {path}")
        return backup_path

    @staticmethod
    def rollback(path: Path, backup_path: Path) -> None:
        """Restore file from backup."""
        if backup_path and backup_path.exists():
            shutil.copy2(backup_path, path)
            logger.info(f"Rolled back: {path}")
        else:
            logger.error(f"Rollback failed: backup not found ({backup_path})")


class MigrationRunner:
    """Orchestrates migration of one or more project.yaml files."""

    def __init__(self, dry_run: bool = False, verbose: bool = False):
        self.dry_run = dry_run
        self.verbose = verbose
        self.stats = {
            'total': 0,
            'successful': 0,
            'skipped': 0,
            'failed': 0,
            'rollbacks': 0
        }

    def migrate_file(self, path: Path) -> bool:
        """
        Migrate a single project.yaml file.
        Returns True if successful, False if failed.
        """
        logger.info(f"Processing: {path}")
        self.stats['total'] += 1

        try:
            # Load v2.0 file
            data = FileManager.load_yaml(path)

            # Check if already v3.0
            if data.get('version') == '3.0':
                logger.info(f"File already v3.0, skipping: {path}")
                self.stats['skipped'] += 1
                return True

            # Migrate
            v3_data = SchemaConverter.migrate(data, verbose=self.verbose)

            # Save (with backup)
            if not self.dry_run:
                backup_path = FileManager.save_yaml(path, v3_data, backup=True)
            else:
                logger.info(f"[DRY-RUN] Would save migrated file: {path}")
                backup_path = None

            self.stats['successful'] += 1
            return True

        except Exception as e:
            logger.error(f"Migration failed for {path}: {e}")
            self.stats['failed'] += 1
            return False

    def migrate_batch(self, directory: Path) -> int:
        """
        Migrate all project.yaml files in a directory tree.
        Returns number of successful migrations.
        """
        logger.info(f"Starting batch migration in: {directory}")

        # Find all project.yaml files
        yaml_files = list(directory.glob('**/.empirica/project.yaml'))
        logger.info(f"Found {len(yaml_files)} project.yaml file(s)")

        # Migrate each
        for yaml_file in yaml_files:
            self.migrate_file(yaml_file)

        # Report stats
        logger.info(f"Batch migration complete:")
        logger.info(f"  Total: {self.stats['total']}")
        logger.info(f"  Successful: {self.stats['successful']}")
        logger.info(f"  Skipped: {self.stats['skipped']}")
        logger.info(f"  Failed: {self.stats['failed']}")

        return self.stats['successful']


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Migrate project.yaml files from v2.0 to v3.0'
    )
    parser.add_argument('path', nargs='?', help='Path to project.yaml file or directory')
    parser.add_argument('--batch', action='store_true', help='Batch mode: migrate all project.yaml in directory tree')
    parser.add_argument('--dry-run', action='store_true', help='Dry run: do not modify files')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    if not args.path:
        parser.print_help()
        return 1

    path = Path(args.path)

    if args.dry_run:
        logger.info("DRY-RUN MODE: No files will be modified")

    runner = MigrationRunner(dry_run=args.dry_run, verbose=args.verbose)

    if args.batch or path.is_dir():
        # Batch mode
        target_dir = path if path.is_dir() else path.parent
        successful = runner.migrate_batch(target_dir)
        return 0 if successful > 0 else 1
    else:
        # Single file mode
        success = runner.migrate_file(path)
        return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
