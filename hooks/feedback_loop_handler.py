#!/usr/bin/env python3
"""
Feedback Loop Handler for Phase 3.B Test Practice

Receives oracle guidance (via cortex_collab or file-based inbox) and
measures convergence: δ(self_report) → δ(acat_x_observed) over time.

This handler runs at POSTFLIGHT and:
1. Logs received guidance (from oracle Cycle 3)
2. Records self-reported vectors (from PREFLIGHT)
3. Measures delta against prior observables
4. Computes convergence rate (ρ increase per day)
"""

import json
import logging
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List


log_path = Path.home() / ".empirica" / "logs" / "feedback-loop-convergence.log"
log_path.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(log_path), logging.StreamHandler()]
)
logger = logging.getLogger("feedback-loop")


@dataclass
class GuidanceEvent:
    """Oracle guidance received by practice."""
    timestamp: str  # ISO format
    guidance_title: str
    guidance_body: str
    vectors_mentioned: List[str]  # ["do", "change", "state"]
    action_required: str  # e.g. "recalibrate on do vector"


@dataclass
class FeedbackLoopSnapshot:
    """Measurement of feedback loop convergence."""
    transaction_num: int
    timestamp: str
    self_reported_vectors: Dict  # {"do": 0.8, "change": 0.6, "state": 0.85}
    acat_x_observed: Optional[Dict]  # from prior transaction's hook
    delta: Optional[Dict]  # |self - observed| per vector
    guidance_acknowledged: bool
    days_since_guidance: Optional[float]


class FeedbackLoopTracker:
    """Track convergence of practice's self-report toward observed behavior."""

    def __init__(self, practice_name: str = "opportunity-aggregator"):
        self.practice_name = practice_name
        self.data_dir = Path.home() / ".empirica" / "feedback-loops" / practice_name
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.guidance_log = self.data_dir / "guidance_received.jsonl"
        self.convergence_log = self.data_dir / "convergence_snapshots.jsonl"

    def log_guidance_received(self, title: str, body: str, vectors: List[str]):
        """Record that oracle guidance was received."""
        event = GuidanceEvent(
            timestamp=datetime.now().isoformat(),
            guidance_title=title,
            guidance_body=body,
            vectors_mentioned=vectors,
            action_required=self._parse_action(body)
        )
        with open(self.guidance_log, "a") as f:
            f.write(json.dumps(asdict(event)) + "\n")
        logger.info(f"Guidance logged: {title}")

    def record_postflight(
        self,
        transaction_num: int,
        self_vectors: Dict,
        acat_x_observed: Optional[Dict] = None
    ):
        """Record POSTFLIGHT vectors and measure convergence."""
        # Load prior observed vectors if available
        prior_observed = self._load_prior_observed()

        # Compute delta if we have observed vectors
        delta = None
        if acat_x_observed:
            delta = {
                k: abs(self_vectors.get(k, 0) - acat_x_observed.get(k, {}).get("value", 0))
                for k in ["do", "change", "state"]
            }

        # Check if guidance was received since last transaction
        guidance_ack = self._check_guidance_acked()
        days_since = self._days_since_guidance()

        snapshot = FeedbackLoopSnapshot(
            transaction_num=transaction_num,
            timestamp=datetime.now().isoformat(),
            self_reported_vectors=self_vectors,
            acat_x_observed=acat_x_observed,
            delta=delta,
            guidance_acknowledged=guidance_ack,
            days_since_guidance=days_since
        )

        with open(self.convergence_log, "a") as f:
            f.write(json.dumps(asdict(snapshot), default=str) + "\n")

        logger.info(f"Convergence snapshot {transaction_num}: delta={delta}")

        # Compute convergence rate if we have history
        rate = self._compute_convergence_rate()
        if rate is not None:
            logger.info(f"Convergence rate: ρ += {rate:.3f} per day")

        return snapshot

    def _load_prior_observed(self) -> Optional[Dict]:
        """Load ACAT-X observables from prior transaction."""
        # TODO: read from empirica grounding layer
        return None

    def _check_guidance_acked(self) -> bool:
        """Check if practice acknowledged recent guidance."""
        if not self.guidance_log.exists():
            return False
        # Simple heuristic: if guidance exists, assume it was seen
        return self.guidance_log.stat().st_mtime > (datetime.now().timestamp() - 86400)

    def _days_since_guidance(self) -> Optional[float]:
        """Days since last guidance received."""
        if not self.guidance_log.exists():
            return None
        mtime = self.guidance_log.stat().st_mtime
        return (datetime.now().timestamp() - mtime) / 86400

    def _parse_action(self, body: str) -> str:
        """Extract action from guidance body."""
        if "do" in body.lower():
            return "recalibrate:do"
        elif "change" in body.lower():
            return "recalibrate:change"
        elif "state" in body.lower():
            return "recalibrate:state"
        return "review"

    def _compute_convergence_rate(self) -> Optional[float]:
        """Compute ρ improvement per day from convergence log."""
        if not self.convergence_log.exists():
            return None

        snapshots = []
        with open(self.convergence_log) as f:
            for line in f:
                try:
                    snapshots.append(json.loads(line))
                except json.JSONDecodeError:
                    pass

        if len(snapshots) < 2:
            return None

        # Simple rate: (delta_older - delta_newer) / days_elapsed
        # Ideally would compute ρ correlation, but delta is an approximation
        first, last = snapshots[0], snapshots[-1]

        if not (first.get("delta") and last.get("delta")):
            return None

        first_delta = sum(first["delta"].values()) / 3
        last_delta = sum(last["delta"].values()) / 3
        improvement = first_delta - last_delta

        t1 = datetime.fromisoformat(first["timestamp"])
        t2 = datetime.fromisoformat(last["timestamp"])
        days = (t2 - t1).days or 1

        return improvement / days


def main():
    """Test harness."""
    tracker = FeedbackLoopTracker()
    logger.info("Feedback loop tracker initialized for opportunity-aggregator")


if __name__ == "__main__":
    main()
