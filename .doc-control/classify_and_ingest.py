#!/usr/bin/env python3
"""
File classification and intake orchestrator for humanaios document control.
Implements FILE_INTAKE_PIPELINE.md stages 1–2 (CLASSIFY + INGEST).

Usage:
  python classify_and_ingest.py --source /Users/andersonfamily/Downloads --mode classify-only
  python classify_and_ingest.py --source /Users/andersonfamily/Downloads --mode full --dry-run
  python classify_and_ingest.py --source /Users/andersonfamily/Downloads --mode full
"""

import json
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
import subprocess

try:
    import yaml
except ImportError:
    print("ERROR: Install required package: pip install pyyaml")
    sys.exit(1)


@dataclass
class Classification:
    """Result of classifying a single file."""
    filename: str
    path: str
    controlled: bool
    area: Optional[str]  # GOV, PROC, SPEC, TEST, VIS, OPS
    inferred_doc_id: Optional[str]
    confidence: float  # 0.0–1.0
    reason: str
    status: str  # draft, review, approved, reference, quarantine
    owner_inferred: str
    error: Optional[str] = None


class FileClassifier:
    """Classify files based on content, metadata, and heuristics."""

    # Area keywords and patterns
    AREA_KEYWORDS = {
        "GOV": [
            "governance", "policy", "charter", "decision", "framework",
            "authority", "approval", "ratified", "compliance"
        ],
        "PROC": [
            "procedure", "process", "runbook", "guide", "manual", "workflow",
            "implementation", "deploy", "installation", "setup"
        ],
        "SPEC": [
            "spec", "specification", "standard", "format", "schema",
            "interface", "protocol", "definition", "instrument"
        ],
        "TEST": [
            "test", "experiment", "research", "validation", "verification",
            "protocol", "findings", "testimony", "audit", "assessment"
        ],
        "VIS": [
            "vision", "strategy", "roadmap", "plan", "objectives", "goals"
        ],
        "OPS": [
            "operations", "operational", "incident", "deployment", "monitoring",
            "infrastructure", "system", "issue", "emergency"
        ]
    }

    CONTROLLED_KEYWORDS = [
        "governance", "policy", "protocol", "spec", "specification",
        "standard", "procedure", "process", "charter", "ratified",
        "approved", "compliance", "audit", "framework"
    ]

    REFERENCE_PATTERNS = [
        r"\.py$", r"\.sh$", r"\.js$",  # Code files
        r"\.json$", r"\.csv$", r"\.log$",  # Data/logs
        r"(example|draft|scratch|temp|test)", # Drafty
        r"raw|export|snapshot|dump"  # Ephemeral data
    ]

    def __init__(self):
        self.confidence_threshold = 0.80

    def extract_text(self, file_path: Path) -> str:
        """Extract text from file (first 2KB for speed)."""
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            return content[:2000].lower()
        except Exception:
            return ""

    def extract_frontmatter(self, file_path: Path) -> Optional[Dict]:
        """Extract and parse YAML frontmatter if present."""
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            if not content.startswith("---"):
                return None
            lines = content.split("\n")
            end_idx = None
            for i in range(1, len(lines)):
                if lines[i].strip() == "---":
                    end_idx = i
                    break
            if end_idx:
                fm_text = "\n".join(lines[1:end_idx])
                return yaml.safe_load(fm_text)
        except Exception:
            return None

    def classify_file(self, file_path: Path) -> Classification:
        """Classify a single file."""
        filename = file_path.name
        path = str(file_path)

        # Check if already controlled (has frontmatter with doc_id)
        fm = self.extract_frontmatter(file_path)
        if fm and fm.get("doc_id"):
            return Classification(
                filename=filename,
                path=path,
                controlled=True,
                area=None,
                inferred_doc_id=fm.get("doc_id"),
                confidence=1.0,
                reason="Already has valid frontmatter with doc_id",
                status="existing",
                owner_inferred="(existing)"
            )

        # Check file type: is it code or data?
        if self._is_reference_file(filename):
            return Classification(
                filename=filename,
                path=path,
                controlled=False,
                area=None,
                inferred_doc_id=None,
                confidence=0.95,
                reason=f"File type '{file_path.suffix}' or pattern indicates reference material",
                status="reference",
                owner_inferred="@humanaios-foundation/operations"
            )

        # Extract text and check for governance intent
        text = self.extract_text(file_path)
        size_kb = file_path.stat().st_size / 1024

        controlled_score = self._score_controlled_intent(text)
        if controlled_score < 0.3:
            return Classification(
                filename=filename,
                path=path,
                controlled=False,
                area=None,
                inferred_doc_id=None,
                confidence=0.85,
                reason="No governance intent detected",
                status="reference",
                owner_inferred="@humanaios-foundation/operations"
            )

        # Infer area
        area, area_confidence = self._infer_area(text, filename)
        if not area:
            return Classification(
                filename=filename,
                path=path,
                controlled=True,
                area=None,
                inferred_doc_id=None,
                confidence=0.50,
                reason="Governance intent detected but area unclear",
                status="quarantine",
                owner_inferred="@humanaios-foundation/operations"
            )

        # Generate doc_id
        doc_id = self._generate_doc_id(area)
        confidence = controlled_score * area_confidence * (1.0 if size_kb > 2 else 0.8)
        confidence = min(confidence, 0.95)

        status = "review" if size_kb > 5 else "draft"

        reason = f"Governed doc detected. Area: {area} (conf {area_confidence:.2f}). " \
                 f"Size: {size_kb:.1f}KB. Governance intent: {controlled_score:.2f}."

        return Classification(
            filename=filename,
            path=path,
            controlled=True,
            area=area,
            inferred_doc_id=doc_id,
            confidence=confidence,
            reason=reason,
            status=status,
            owner_inferred="@humanaios-foundation/carly"
        )

    def _is_reference_file(self, filename: str) -> bool:
        """Check if file matches reference patterns."""
        for pattern in self.REFERENCE_PATTERNS:
            if re.search(pattern, filename, re.IGNORECASE):
                return True
        return False

    def _score_controlled_intent(self, text: str) -> float:
        """Score likelihood that text is governance (0.0–1.0)."""
        score = 0.0
        for keyword in self.CONTROLLED_KEYWORDS:
            if keyword in text:
                score += 0.15
        return min(score, 1.0)

    def _infer_area(self, text: str, filename: str) -> Tuple[Optional[str], float]:
        """Infer the document area (GOV/PROC/SPEC/etc.). Return (area, confidence)."""
        scores = {}
        for area, keywords in self.AREA_KEYWORDS.items():
            matches = sum(1 for kw in keywords if kw in text)
            scores[area] = matches

        if not scores or max(scores.values()) == 0:
            return None, 0.0

        top_area = max(scores, key=scores.get)
        top_score = scores[top_area]
        confidence = min(top_score / 3.0, 1.0)  # Normalize to 0–1

        return top_area, confidence

    def _generate_doc_id(self, area: str) -> str:
        """Generate a new doc_id for the area. Return HAIOS-<AREA>-NNN."""
        # Placeholder: in production, query registry for next available NNN
        nnn = "999"  # This will be incremented per actual registry state
        return f"HAIOS-{area}-{nnn}"


class IntakeOrchestrator:
    """Orchestrate the full intake pipeline."""

    def __init__(self, registry_path: Path, dry_run: bool = False):
        self.registry_path = registry_path
        self.dry_run = dry_run
        self.classifier = FileClassifier()

    def classify_batch(self, source_dir: Path) -> Tuple[List[Classification], Dict]:
        """Classify all .md files in source directory."""
        classified = []
        manifest = {
            "source": str(source_dir),
            "timestamp": subprocess.check_output(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"]).decode().strip(),
            "mode": "classify-only",
            "files_scanned": 0,
            "classified": [],
            "quarantine": [],
            "already_controlled": []
        }

        for md_file in sorted(source_dir.glob("*.md")):
            cls = self.classifier.classify_file(md_file)
            classified.append(cls)
            manifest["files_scanned"] += 1

            if cls.status == "existing":
                manifest["already_controlled"].append(cls.filename)
            elif cls.status == "quarantine":
                manifest["quarantine"].append({
                    "filename": cls.filename,
                    "reason": cls.reason,
                    "confidence": cls.confidence
                })
            else:
                manifest["classified"].append(asdict(cls))

        return classified, manifest

    def print_manifest(self, manifest: Dict):
        """Pretty-print the intake manifest."""
        print("\n" + "="*70)
        print("INTAKE MANIFEST REPORT")
        print("="*70)
        print(f"Source: {manifest['source']}")
        print(f"Timestamp: {manifest['timestamp']}")
        print(f"Files scanned: {manifest['files_scanned']}\n")

        classified = manifest.get("classified", [])
        quarantine = manifest.get("quarantine", [])
        already = manifest.get("already_controlled", [])

        high_conf = sum(1 for c in classified if c["confidence"] > 0.90)
        low_conf = sum(1 for c in classified if 0.70 <= c["confidence"] <= 0.90)

        print(f"📋 Classified (ready to ingest): {len(classified)} files")
        if high_conf > 0:
            print(f"   ✓ High confidence (> 90%): {high_conf} files")
        if low_conf > 0:
            print(f"   ? Medium confidence (70–90%): {low_conf} files (review before ingest)")

        if quarantine:
            print(f"\n📦 Quarantine (needs triage): {len(quarantine)} files")
            for item in quarantine[:5]:  # Show first 5
                print(f"   • {item['filename']} (conf: {item['confidence']:.2f})")
            if len(quarantine) > 5:
                print(f"   ... and {len(quarantine) - 5} more")

        if already:
            print(f"\n✓ Already registered: {len(already)} files")
            for f in already[:3]:
                print(f"   • {f}")
            if len(already) > 3:
                print(f"   ... and {len(already) - 3} more")

        print("\n" + "="*70)
        print("Next: Review low-confidence items, triage quarantine, run intake-confirm")
        print("="*70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Classify and ingest files into humanaios document control"
    )
    parser.add_argument("--source", type=Path, required=True, help="Source directory")
    parser.add_argument(
        "--mode", choices=["classify-only", "full", "archive-only"], default="classify-only",
        help="Pipeline mode"
    )
    parser.add_argument("--registry", type=Path, default=Path("document-registry.yaml"))
    parser.add_argument("--dry-run", action="store_true", help="Don't make changes")

    args = parser.parse_args()

    if not args.source.exists():
        print(f"ERROR: Source directory not found: {args.source}")
        sys.exit(1)

    orchestrator = IntakeOrchestrator(args.registry, dry_run=args.dry_run)

    if args.mode == "classify-only":
        classified, manifest = orchestrator.classify_batch(args.source)
        orchestrator.print_manifest(manifest)
        # Save manifest for later
        manifest_path = args.source.parent / f"intake-manifest-{manifest['timestamp'].replace(':', '')}.json"
        manifest_path.write_text(json.dumps(manifest, indent=2))
        print(f"Manifest saved: {manifest_path}")

    else:
        print(f"Mode '{args.mode}' not yet implemented in Phase 1")
        sys.exit(1)


if __name__ == "__main__":
    main()
