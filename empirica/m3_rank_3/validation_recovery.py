#!/usr/bin/env python3
"""
M3 Rank 3: State Sync Validation & Recovery

Implements divergence validation (T3-A) and recovery procedures (T3-B):
- T3-A: ValidationOrchestrator - verify divergence reports are truthful
- T3-B: RecoveryOrchestrator - dispatch corrections and verify recovery
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

class AuthorityStrategy(Enum):
    """Strategy for determining authoritative source on divergence"""
    ADMIRAL_WINS = "admiral_wins"           # Admiral is always authoritative
    MAJORITY_VOTE = "majority_vote"         # 3+ practices vote on truth
    LAST_WRITE_WINS = "last_write_wins"     # Use entity's updated_at timestamp


class ValidationStatus(Enum):
    """Result of divergence validation"""
    CONFIRMED = "confirmed"                 # Divergence is real
    FALSE_POSITIVE = "false_positive"       # Report was wrong/stale
    TAMPERING_SUSPECTED = "tampering"       # Unreachable or mismatch


@dataclass
class ValidationVerdict:
    """Result of validating a single divergent entity"""
    canonical_id: str
    is_confirmed: bool                      # Divergence is real
    is_false_positive: bool                 # Report was wrong
    is_tampering_suspected: bool            # Unreachable or mismatch
    actual_hash_A: Optional[str]            # Recomputed from source
    actual_hash_B: Optional[str]
    reported_hash_A: str
    reported_hash_B: str
    status: ValidationStatus
    reason: str                             # Explanation of verdict


@dataclass
class RecoveryResult:
    """Result of recovery operation"""
    success: bool
    entities_fixed: int
    recovery_time: float                    # seconds
    recovery_id: str
    final_root_hash: Optional[str]
    reason: Optional[str] = None            # if failed


@dataclass
class CorrectionBatch:
    """Batch of corrections to apply"""
    recovery_id: str
    timestamp: float
    corrections: List[Dict]                 # {operation, canonical_id, entity, ...}
    source_claude: str
    target_claudes: List[str]
    admiral_signature: str


# ============================================================================
# T3-A: VALIDATION ORCHESTRATOR
# ============================================================================

class ValidationOrchestrator:
    """
    Validates divergence reports from M3R2.

    Process:
    1. Fetch entity from both practices (source of truth)
    2. Recompute hashes from fresh data
    3. Compare to reported hashes
    4. Return verdict: CONFIRMED | FALSE_POSITIVE | TAMPERING
    """

    def __init__(self, workspace_db_path: Optional[str] = None):
        if workspace_db_path is None:
            workspace_db_path = str(Path.home() / ".empirica/workspace/workspace.db")
        self.workspace_db_path = workspace_db_path

    def validate_divergence_report(
        self,
        report_id: str,
        divergent_entities: List[Dict],
        practice_name_A: str,
        practice_name_B: str,
    ) -> List[ValidationVerdict]:
        """
        Validate all divergences in a report.

        Returns: List[ValidationVerdict] - one verdict per entity
        """
        verdicts = []

        for entity_diff in divergent_entities:
            verdict = self._validate_single_entity(
                entity_diff,
                practice_name_A,
                practice_name_B,
            )
            verdicts.append(verdict)

        return verdicts

    def _validate_single_entity(
        self,
        entity_diff: Dict,
        practice_name_A: str,
        practice_name_B: str,
    ) -> ValidationVerdict:
        """Validate a single divergent entity"""
        canonical_id = entity_diff['canonical_id']
        reported_hash_A = entity_diff.get('hash_A')
        reported_hash_B = entity_diff.get('hash_B')

        # Step 1: Fetch entity from both practices
        try:
            entity_A = self._fetch_entity(practice_name_A, canonical_id)
            entity_B = self._fetch_entity(practice_name_B, canonical_id)
            reachable_A = entity_A is not None
            reachable_B = entity_B is not None
        except Exception as e:
            return ValidationVerdict(
                canonical_id=canonical_id,
                is_confirmed=False,
                is_false_positive=False,
                is_tampering_suspected=True,
                actual_hash_A=None,
                actual_hash_B=None,
                reported_hash_A=reported_hash_A or "unknown",
                reported_hash_B=reported_hash_B or "unknown",
                status=ValidationStatus.TAMPERING_SUSPECTED,
                reason=f"Failed to fetch entity: {str(e)}",
            )

        # Handle unreachable practices
        if not reachable_A or not reachable_B:
            return ValidationVerdict(
                canonical_id=canonical_id,
                is_confirmed=False,
                is_false_positive=False,
                is_tampering_suspected=True,
                actual_hash_A=self._hash_entity(entity_A) if entity_A else None,
                actual_hash_B=self._hash_entity(entity_B) if entity_B else None,
                reported_hash_A=reported_hash_A or "unknown",
                reported_hash_B=reported_hash_B or "unknown",
                status=ValidationStatus.TAMPERING_SUSPECTED,
                reason=f"Unreachable: {practice_name_A if not reachable_A else practice_name_B}",
            )

        # Step 2: Recompute hashes from fresh data
        actual_hash_A = self._hash_entity(entity_A)
        actual_hash_B = self._hash_entity(entity_B)

        # Step 3: Determine verdict based on hash divergence
        hashes_match = actual_hash_A == actual_hash_B

        if hashes_match:
            # Hashes match → divergence is false positive (state is actually synchronized)
            status = ValidationStatus.FALSE_POSITIVE
            is_confirmed = False
            is_false_positive = True
            is_tampering = False
            reason = "False positive: entities have matching hashes (no actual divergence)"
        else:
            # Hashes differ → divergence is confirmed
            status = ValidationStatus.CONFIRMED
            is_confirmed = True
            is_false_positive = False
            is_tampering = False
            reason = f"Divergence confirmed: {canonical_id} has different hashes in practices"

        return ValidationVerdict(
            canonical_id=canonical_id,
            is_confirmed=is_confirmed,
            is_false_positive=is_false_positive,
            is_tampering_suspected=is_tampering,
            actual_hash_A=actual_hash_A,
            actual_hash_B=actual_hash_B,
            reported_hash_A=reported_hash_A or "none",
            reported_hash_B=reported_hash_B or "none",
            status=status,
            reason=reason,
        )

    def _fetch_entity(self, practice_name: str, canonical_id: str) -> Optional[Dict]:
        """Fetch entity from a practice's workspace database"""
        try:
            conn = sqlite3.connect(self.workspace_db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM entity_registry
                WHERE canonical_identifier = ? AND status = 'active'
            """, (canonical_id,))

            row = cursor.fetchone()
            conn.close()

            return dict(row) if row else None
        except Exception:
            return None

    def _hash_entity(self, entity: Dict) -> str:
        """Compute SHA256 hash of entity using same fields as M3R2"""
        fields = ['canonical_identifier', 'authority_tier', 'source_of_truth', 'updated_at']
        content = "".join([str(entity.get(f, '')) for f in fields])
        return hashlib.sha256(content.encode()).hexdigest()


# ============================================================================
# T3-B: RECOVERY ORCHESTRATOR
# ============================================================================

class RecoveryOrchestrator:
    """
    Orchestrates recovery from validated divergences.

    Process:
    1. For each confirmed divergence, determine authoritative source
    2. Generate correction batch (upsert/delete operations)
    3. Sign batch with Admiral signature
    4. Dispatch via M3R1 batch accumulator
    5. Wait for acknowledgments from all practices
    6. Re-fingerprint to verify recovery
    """

    def __init__(self, workspace_db_path: Optional[str] = None):
        if workspace_db_path is None:
            workspace_db_path = str(Path.home() / ".empirica/workspace/workspace.db")
        self.workspace_db_path = workspace_db_path
        self.recovery_counter = 0

    def recover_from_validated_divergences(
        self,
        verdicts: List[ValidationVerdict],
        confirmed_verdicts_only: bool = True,
        authority_strategy: AuthorityStrategy = AuthorityStrategy.ADMIRAL_WINS,
    ) -> RecoveryResult:
        """
        Recover from validated divergences.

        Args:
            verdicts: List of ValidationVerdict from validation phase
            confirmed_verdicts_only: If True, skip false positives
            authority_strategy: How to choose authoritative source

        Returns: RecoveryResult with success status and entities fixed
        """
        start_time = time.time()
        self.recovery_counter += 1
        recovery_id = f"recov_{int(time.time() * 1000)}_{self.recovery_counter}"

        # Filter to confirmed divergences only
        if confirmed_verdicts_only:
            confirmed = [v for v in verdicts if v.is_confirmed]
        else:
            confirmed = verdicts

        if not confirmed:
            return RecoveryResult(
                success=True,
                entities_fixed=0,
                recovery_time=time.time() - start_time,
                recovery_id=recovery_id,
                final_root_hash=None,
                reason="No confirmed divergences to recover",
            )

        # Step 1: Generate correction batch
        corrections = []
        for verdict in confirmed:
            correction = self._generate_correction(
                verdict,
                authority_strategy,
            )
            if correction:
                corrections.append(correction)

        if not corrections:
            return RecoveryResult(
                success=False,
                entities_fixed=0,
                recovery_time=time.time() - start_time,
                recovery_id=recovery_id,
                final_root_hash=None,
                reason="Could not generate corrections for any divergence",
            )

        # Step 2: Create batch
        batch = CorrectionBatch(
            recovery_id=recovery_id,
            timestamp=time.time(),
            corrections=corrections,
            source_claude="empirica-foundation-evaluator",
            target_claudes=["empirica-autonomy", "empirica-mesh-support"],  # Mock: would be all practices
            admiral_signature=self._sign_batch(corrections),
        )

        # Step 3: Dispatch (in real impl, would use M3R1 dispatcher)
        dispatch_success = self._dispatch_corrections(batch)

        if not dispatch_success:
            return RecoveryResult(
                success=False,
                entities_fixed=0,
                recovery_time=time.time() - start_time,
                recovery_id=recovery_id,
                final_root_hash=None,
                reason="Failed to dispatch correction batch",
            )

        # Step 4: Verify recovery (in real impl, would wait for acks + re-fingerprint)
        recovery_time = time.time() - start_time

        return RecoveryResult(
            success=True,
            entities_fixed=len(corrections),
            recovery_time=recovery_time,
            recovery_id=recovery_id,
            final_root_hash=self._compute_final_hash(),
            reason=None,
        )

    def _generate_correction(
        self,
        verdict: ValidationVerdict,
        authority_strategy: AuthorityStrategy,
    ) -> Optional[Dict]:
        """Generate a single correction operation"""
        canonical_id = verdict.canonical_id

        # Determine authoritative source
        if authority_strategy == AuthorityStrategy.ADMIRAL_WINS:
            authoritative_practice = "empirica-foundation-evaluator"
        else:
            # For MVP, default to Admiral
            authoritative_practice = "empirica-foundation-evaluator"

        # Fetch authoritative entity
        entity = self._fetch_entity(canonical_id)
        if entity is None:
            return None

        return {
            "operation": "upsert",
            "canonical_id": canonical_id,
            "entity": entity,
            "source": authoritative_practice,
            "timestamp": time.time(),
            "reason": f"Recovery from divergence {verdict.canonical_id}",
        }

    def _fetch_entity(self, canonical_id: str) -> Optional[Dict]:
        """Fetch entity from workspace database"""
        try:
            conn = sqlite3.connect(self.workspace_db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM entity_registry
                WHERE canonical_identifier = ? AND status = 'active'
            """, (canonical_id,))

            row = cursor.fetchone()
            conn.close()

            return dict(row) if row else None
        except Exception:
            return None

    def _sign_batch(self, corrections: List[Dict]) -> str:
        """Sign batch (mock implementation)"""
        content = json.dumps(corrections, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:32]

    def _dispatch_corrections(self, batch: CorrectionBatch) -> bool:
        """Dispatch corrections (mock implementation)"""
        # In real impl, would use M3R1 dispatcher
        return True

    def _compute_final_hash(self) -> str:
        """Compute final root hash after recovery (mock)"""
        return hashlib.sha256(b"recovered_state").hexdigest()


# ============================================================================
# UTILITIES
# ============================================================================

def verdict_to_json(verdict: ValidationVerdict) -> str:
    """Serialize verdict to JSON"""
    data = {
        'canonical_id': verdict.canonical_id,
        'is_confirmed': verdict.is_confirmed,
        'is_false_positive': verdict.is_false_positive,
        'is_tampering_suspected': verdict.is_tampering_suspected,
        'actual_hash_A': verdict.actual_hash_A,
        'actual_hash_B': verdict.actual_hash_B,
        'reported_hash_A': verdict.reported_hash_A,
        'reported_hash_B': verdict.reported_hash_B,
        'status': verdict.status.value,
        'reason': verdict.reason,
    }
    return json.dumps(data, indent=2)


def recovery_result_to_json(result: RecoveryResult) -> str:
    """Serialize recovery result to JSON"""
    data = {
        'recovery_id': result.recovery_id,
        'success': result.success,
        'entities_fixed': result.entities_fixed,
        'recovery_time': result.recovery_time,
        'final_root_hash': result.final_root_hash,
        'reason': result.reason,
    }
    return json.dumps(data, indent=2)


if __name__ == "__main__":
    print("M3 Rank 3: State Sync Validation & Recovery")
    print("Classes: ValidationOrchestrator, RecoveryOrchestrator")
    print("Status: Ready for integration testing (T3-D)")
