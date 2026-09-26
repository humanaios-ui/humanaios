#!/usr/bin/env python3
"""
M3 Rank 2: Divergence Detection

Implements cross-practice state fingerprinting and diff algorithm:
- T2-A: State fingerprinting via Merkle tree hashing
- T2-B: Cross-practice diff algorithm with severity classification
"""

import json
import time
import hashlib
import sqlite3
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime
from enum import Enum
from pathlib import Path


# ============================================================================
# DATA STRUCTURES
# ============================================================================

class DivergenceSeverity(Enum):
    """Severity classification for divergence reports"""
    INFO = "INFO"           # <5% divergence
    WARNING = "WARNING"     # 5-20% divergence
    ERROR = "ERROR"         # >20% divergence


@dataclass
class FingerprintResult:
    """Result of practice state fingerprinting"""
    root_hash: str
    type_hashes: Dict[str, str]          # entity_type → hash
    entity_hashes: Dict[str, str]        # canonical_id → hash
    timestamp: float
    entity_count: int
    fingerprint_stage: str                # "dispatch" or "receipt"


@dataclass
class DivergentEntity:
    """Single divergent entity in diff report"""
    canonical_id: str
    entity_type: str
    change_type: str                      # "add", "delete", or "update"
    hash_A: Optional[str]
    hash_B: Optional[str]
    detected_at: str                      # "dispatch" or "receipt"


@dataclass
class DivergenceReport:
    """Complete divergence report between two practices"""
    report_id: str
    timestamp: float
    practice_A: str
    practice_B: str
    root_hash_A: str
    root_hash_B: str
    divergence_percentage: float
    entity_count_A: int
    entity_count_B: int
    entities_changed: int
    entities_added: int
    entities_deleted: int
    severity: DivergenceSeverity
    divergent_entities: List[DivergentEntity] = field(default_factory=list)
    recommendation: str = ""


# ============================================================================
# T2-A: STATE FINGERPRINTER
# ============================================================================

class StateFingerprinter:
    """
    Computes Merkle tree fingerprint of practice entity state.

    Structure:
    - Level 0 (root): Single SHA256 hash of practice state
    - Level 1 (type): One hash per entity_type
    - Level 2 (entity): SHA256 hash per entity (leaf level)

    Properties:
    - Deterministic: Same state always produces same hash
    - Order-independent: Entities sorted before hashing
    - Incremental: Changing one entity only rehashes path to root
    """

    LEAF_HASH_FIELDS = [
        'canonical_identifier',
        'authority_tier',
        'source_of_truth',
        'updated_at',
    ]

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_path = str(Path.home() / ".empirica/workspace/workspace.db")
        self.db_path = db_path

    def fingerprint_dispatch(self) -> FingerprintResult:
        """Compute fingerprint at dispatch time (T0)"""
        return self._compute_fingerprint("dispatch")

    def fingerprint_receipt(self) -> FingerprintResult:
        """Compute fingerprint at receipt time (T2)"""
        return self._compute_fingerprint("receipt")

    def _compute_fingerprint(self, stage: str) -> FingerprintResult:
        """Compute Merkle tree for this practice's entity state"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Fetch all active entities, sorted by type then canonical_id
        cursor.execute("""
            SELECT * FROM entity_registry
            WHERE status = 'active'
            ORDER BY entity_type, canonical_identifier
        """)

        entities = [dict(row) for row in cursor.fetchall()]
        conn.close()

        # Group by type
        entities_by_type: Dict[str, List[Dict]] = {}
        for entity in entities:
            etype = entity['entity_type']
            if etype not in entities_by_type:
                entities_by_type[etype] = []
            entities_by_type[etype].append(entity)

        # Compute type-level hashes
        type_hashes: Dict[str, str] = {}
        entity_hashes: Dict[str, str] = {}

        for etype in sorted(entities_by_type.keys()):
            type_entities = entities_by_type[etype]

            # Leaf hashes for this type (already sorted by canonical_identifier)
            leaf_hashes = []
            for entity in type_entities:
                leaf_hash = self._hash_entity(entity)
                canonical_id = entity['canonical_identifier']
                if canonical_id:  # Only index if canonical_id exists
                    entity_hashes[canonical_id] = leaf_hash
                leaf_hashes.append(leaf_hash)

            # Type hash is merkle tree of leaves
            type_hash = self._merkle_parent(leaf_hashes)
            type_hashes[etype] = type_hash

        # Root is merkle tree of type hashes (sorted by type name)
        root_hash = self._merkle_parent([
            type_hashes[t] for t in sorted(type_hashes.keys())
        ])

        return FingerprintResult(
            root_hash=root_hash,
            type_hashes=type_hashes,
            entity_hashes=entity_hashes,
            timestamp=time.time(),
            entity_count=len(entities),
            fingerprint_stage=stage,
        )

    def _hash_entity(self, entity: Dict) -> str:
        """Hash a single entity (leaf level)"""
        content = "".join([
            str(entity.get(field, ''))
            for field in self.LEAF_HASH_FIELDS
        ])
        return hashlib.sha256(content.encode()).hexdigest()

    def _merkle_parent(self, hashes: List[str]) -> str:
        """Compute parent hash from list of child hashes (recursive)"""
        if len(hashes) == 0:
            return hashlib.sha256(b"").hexdigest()
        if len(hashes) == 1:
            return hashes[0]

        # Pair up: (h0,h1), (h2,h3), ...
        # If len is odd, duplicate last hash to maintain determinism
        pairs = []
        for i in range(0, len(hashes), 2):
            if i + 1 < len(hashes):
                pairs.append((hashes[i], hashes[i + 1]))
            else:
                pairs.append((hashes[i], hashes[i]))  # duplicate last

        parent_hashes = [
            hashlib.sha256((p[0] + p[1]).encode()).hexdigest()
            for p in pairs
        ]

        # Recurse until single root hash
        return self._merkle_parent(parent_hashes)


# ============================================================================
# T2-B: DIFF ALGORITHM
# ============================================================================

class DiffAlgorithm:
    """
    Compares two practice fingerprints and reports divergence.

    Algorithm:
    - Fast path: if root hashes match, no divergence (O(1))
    - Slow path: entity-level diff to find divergences (O(k) where k = # divergent entities)

    Returns structured divergence report with severity classification and recommendation.
    """

    def __init__(self):
        self.report_counter = 0

    def compare_practices(
        self,
        fp_A: FingerprintResult,
        fp_B: FingerprintResult,
        practice_name_A: str,
        practice_name_B: str,
    ) -> DivergenceReport:
        """
        Compare two practice fingerprints.

        Returns: DivergenceReport with divergence_percentage, severity, and recommendations
        """
        self.report_counter += 1
        report_id = f"div_{int(time.time() * 1000)}_{self.report_counter}"

        # Fast path: root hashes match → no divergence
        if fp_A.root_hash == fp_B.root_hash:
            return DivergenceReport(
                report_id=report_id,
                timestamp=time.time(),
                practice_A=practice_name_A,
                practice_B=practice_name_B,
                root_hash_A=fp_A.root_hash,
                root_hash_B=fp_B.root_hash,
                divergence_percentage=0.0,
                entity_count_A=fp_A.entity_count,
                entity_count_B=fp_B.entity_count,
                entities_changed=0,
                entities_added=0,
                entities_deleted=0,
                severity=DivergenceSeverity.INFO,
                divergent_entities=[],
                recommendation="No divergence detected. Practices are synchronized.",
            )

        # Slow path: find divergent entities
        divergences = self._find_divergent_entities(
            fp_A.entity_hashes,
            fp_B.entity_hashes,
            fp_A.fingerprint_stage,
        )

        # Classify divergences
        added = [d for d in divergences if d.change_type == 'add']
        deleted = [d for d in divergences if d.change_type == 'delete']
        updated = [d for d in divergences if d.change_type == 'update']

        total_entities = max(fp_A.entity_count + fp_B.entity_count, 1)
        divergence_pct = (len(divergences) / total_entities) * 100

        # Determine severity
        if divergence_pct < 5:
            severity = DivergenceSeverity.INFO
        elif divergence_pct < 20:
            severity = DivergenceSeverity.WARNING
        else:
            severity = DivergenceSeverity.ERROR

        recommendation = self._recommend_action(
            severity,
            len(added),
            len(deleted),
            len(updated),
        )

        return DivergenceReport(
            report_id=report_id,
            timestamp=time.time(),
            practice_A=practice_name_A,
            practice_B=practice_name_B,
            root_hash_A=fp_A.root_hash,
            root_hash_B=fp_B.root_hash,
            divergence_percentage=round(divergence_pct, 2),
            entity_count_A=fp_A.entity_count,
            entity_count_B=fp_B.entity_count,
            entities_changed=len(updated),
            entities_added=len(added),
            entities_deleted=len(deleted),
            severity=severity,
            divergent_entities=divergences,
            recommendation=recommendation,
        )

    def _find_divergent_entities(
        self,
        hashes_A: Dict[str, str],
        hashes_B: Dict[str, str],
        detected_at: str,
    ) -> List[DivergentEntity]:
        """Find entities that differ between practices"""
        divergences: List[DivergentEntity] = []

        # Entities in A but not B (deleted from B's perspective)
        for canonical_id in set(hashes_A.keys()) - set(hashes_B.keys()):
            # Extract entity type from canonical_id (e.g., "project:xyz" → "project")
            entity_type = canonical_id.split(':')[0] if ':' in canonical_id else 'unknown'
            divergences.append(
                DivergentEntity(
                    canonical_id=canonical_id,
                    entity_type=entity_type,
                    change_type='delete',
                    hash_A=hashes_A[canonical_id],
                    hash_B=None,
                    detected_at=detected_at,
                )
            )

        # Entities in B but not A (added from A's perspective)
        for canonical_id in set(hashes_B.keys()) - set(hashes_A.keys()):
            entity_type = canonical_id.split(':')[0] if ':' in canonical_id else 'unknown'
            divergences.append(
                DivergentEntity(
                    canonical_id=canonical_id,
                    entity_type=entity_type,
                    change_type='add',
                    hash_A=None,
                    hash_B=hashes_B[canonical_id],
                    detected_at=detected_at,
                )
            )

        # Entities in both but hashes differ (updated)
        for canonical_id in set(hashes_A.keys()) & set(hashes_B.keys()):
            if hashes_A[canonical_id] != hashes_B[canonical_id]:
                entity_type = canonical_id.split(':')[0] if ':' in canonical_id else 'unknown'
                divergences.append(
                    DivergentEntity(
                        canonical_id=canonical_id,
                        entity_type=entity_type,
                        change_type='update',
                        hash_A=hashes_A[canonical_id],
                        hash_B=hashes_B[canonical_id],
                        detected_at=detected_at,
                    )
                )

        # Sort by canonical_id for stable output
        return sorted(divergences, key=lambda d: d.canonical_id)

    def _recommend_action(
        self,
        severity: DivergenceSeverity,
        added: int,
        deleted: int,
        updated: int,
    ) -> str:
        """Generate actionable recommendation based on divergence severity"""
        if severity == DivergenceSeverity.INFO:
            return f"Monitor: {updated} entities updated. No action required at this time."
        elif severity == DivergenceSeverity.WARNING:
            return (
                f"Review divergence: {updated} updated, {added} added, {deleted} deleted. "
                f"Alert mesh-support for manual reconciliation via T3-A validation."
            )
        else:  # ERROR
            return (
                f"Critical divergence detected: {updated} updated, {added} added, {deleted} deleted. "
                f"Escalate to Admiral immediately. May require forced recovery via M3R3."
            )


# ============================================================================
# UTILITIES
# ============================================================================

def report_to_json(report: DivergenceReport) -> str:
    """Serialize divergence report to JSON"""
    data = {
        'report_id': report.report_id,
        'timestamp': report.timestamp,
        'practice_A': report.practice_A,
        'practice_B': report.practice_B,
        'root_hash_A': report.root_hash_A,
        'root_hash_B': report.root_hash_B,
        'divergence_percentage': report.divergence_percentage,
        'entity_count_A': report.entity_count_A,
        'entity_count_B': report.entity_count_B,
        'entities_changed': report.entities_changed,
        'entities_added': report.entities_added,
        'entities_deleted': report.entities_deleted,
        'severity': report.severity.value,
        'recommendation': report.recommendation,
        'divergent_entities': [
            {
                'canonical_id': d.canonical_id,
                'entity_type': d.entity_type,
                'change_type': d.change_type,
                'hash_A': d.hash_A,
                'hash_B': d.hash_B,
                'detected_at': d.detected_at,
            }
            for d in report.divergent_entities
        ],
    }
    return json.dumps(data, indent=2)


if __name__ == "__main__":
    print("M3 Rank 2: Divergence Detection")
    print("Classes: StateFingerprinter, DiffAlgorithm")
    print("Structures: FingerprintResult, DivergenceReport, DivergentEntity")
    print("Status: Ready for integration testing (T2-D)")
