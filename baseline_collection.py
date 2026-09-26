"""
Measurement Baseline Collection — Phase 3.4
Cold-start and warm-start baseline establishment for Phase 3.5 convergence analysis
"""

import json
import time
from datetime import datetime
from typing import List, Dict
import statistics

class BaselineCollector:
    """Collects and analyzes Phase 3.4 baseline metrics."""
    
    def __init__(self, baseline_file: str = "baseline_metrics.json"):
        self.baseline_file = baseline_file
        self.samples = []
    
    def record_transaction(self, transaction: Dict) -> None:
        """Record a single transaction baseline."""
        sample = {
            "timestamp": datetime.utcnow().isoformat(),
            "transaction_id": transaction.get("transaction_id"),
            "session_id": transaction.get("session_id"),
            "work_type": transaction.get("work_type", "code"),
            
            # Latency metrics (seconds)
            "latency_preflight_to_postflight": transaction.get("latency_seconds"),
            "latency_p_value": None,  # Computed from trace
            
            # Vector metrics
            "preflight_vectors": transaction.get("preflight_vectors", {}),
            "postflight_vectors": transaction.get("postflight_vectors", {}),
            "vector_deltas": self._compute_deltas(
                transaction.get("preflight_vectors", {}),
                transaction.get("postflight_vectors", {})
            ),
            
            # Artifact metrics
            "artifacts_logged": transaction.get("artifacts_logged", 0),
            "findings": transaction.get("artifact_count", {}).get("findings", 0),
            "unknowns": transaction.get("artifact_count", {}).get("unknowns", 0),
            "decisions": transaction.get("artifact_count", {}).get("decisions", 0),
            
            # Calibration metrics
            "postflight_confidence": transaction.get("postflight_confidence"),
            "claims_declared": transaction.get("claims_declared"),
            "claims_grounded": transaction.get("claims_grounded"),
        }
        self.samples.append(sample)
    
    @staticmethod
    def _compute_deltas(preflight: Dict, postflight: Dict) -> Dict:
        """Compute vector deltas."""
        deltas = {}
        for key in preflight.keys():
            if key in postflight:
                deltas[key] = postflight[key] - preflight[key]
        return deltas
    
    def generate_report(self) -> Dict:
        """Generate baseline analysis report."""
        if not self.samples:
            return {"error": "No samples collected"}
        
        # Latency analysis
        latencies = [s["latency_preflight_to_postflight"] for s in self.samples if s["latency_preflight_to_postflight"]]
        
        # Artifact distribution
        all_artifacts = [s["artifacts_logged"] for s in self.samples]
        
        # Confidence distribution
        confidences = [s["postflight_confidence"] for s in self.samples if s["postflight_confidence"]]
        
        # Vector delta means
        all_deltas = {}
        for sample in self.samples:
            for key, value in sample["vector_deltas"].items():
                if key not in all_deltas:
                    all_deltas[key] = []
                all_deltas[key].append(value)
        
        delta_means = {k: statistics.mean(v) for k, v in all_deltas.items()}
        
        report = {
            "baseline_meta": {
                "sample_count": len(self.samples),
                "collection_period": f"{self.samples[0]['timestamp']} to {self.samples[-1]['timestamp']}",
                "baseline_type": "cold_start" if len(self.samples) < 15 else "warm_start",
            },
            "latency_metrics": {
                "p0": min(latencies) if latencies else None,
                "p50": statistics.median(latencies) if latencies else None,
                "p99": sorted(latencies)[int(len(latencies) * 0.99)] if len(latencies) > 0.99 else max(latencies),
                "mean": statistics.mean(latencies) if latencies else None,
                "stdev": statistics.stdev(latencies) if len(latencies) > 1 else None,
            },
            "artifact_metrics": {
                "median_per_transaction": statistics.median(all_artifacts),
                "mean_per_transaction": statistics.mean(all_artifacts),
                "iqr_lower": sorted(all_artifacts)[len(all_artifacts)//4],
                "iqr_upper": sorted(all_artifacts)[3*len(all_artifacts)//4],
            },
            "confidence_metrics": {
                "mean": statistics.mean(confidences),
                "min": min(confidences),
                "max": max(confidences),
                "stdev": statistics.stdev(confidences) if len(confidences) > 1 else None,
            },
            "vector_delta_means": delta_means,
            "success_criteria": {
                "sample_count_threshold_30": len(self.samples) >= 30,
                "latency_p99_under_5min": (sorted(latencies)[int(len(latencies) * 0.99)] < 300) if latencies else False,
                "confidence_mean_over_0_85": statistics.mean(confidences) > 0.85 if confidences else False,
            }
        }
        return report
    
    def save_baseline(self) -> None:
        """Save baseline to JSON file."""
        report = self.generate_report()
        with open(self.baseline_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"✅ Baseline saved to {self.baseline_file}")
    
    def load_baseline(self) -> Dict:
        """Load baseline from JSON file."""
        with open(self.baseline_file, 'r') as f:
            return json.load(f)


# Usage:
if __name__ == "__main__":
    collector = BaselineCollector()
    
    # Simulate collection of 30 transactions
    for i in range(30):
        sample_txn = {
            "transaction_id": f"txn_{i:03d}",
            "session_id": "s_baseline",
            "work_type": "code",
            "latency_seconds": 120 + (i % 60),  # Varied latency
            "preflight_vectors": {
                "know": 0.82, "do": 0.85, "context": 0.83,
                "clarity": 0.78, "coherence": 0.80, "signal": 0.79,
                "density": 0.77, "state": 0.81, "change": 0.40,
                "completion": 0.20, "impact": 0.88, "engagement": 0.92,
                "uncertainty": 0.20,
            },
            "postflight_vectors": {
                "know": 0.85, "do": 0.87, "context": 0.85,
                "clarity": 0.83, "coherence": 0.84, "signal": 0.84,
                "density": 0.82, "state": 0.84, "change": 0.65,
                "completion": 0.75, "impact": 0.87, "engagement": 0.93,
                "uncertainty": 0.15,
            },
            "artifacts_logged": 5,
            "artifact_count": {"findings": 2, "unknowns": 1, "decisions": 1},
            "postflight_confidence": 0.88,
            "claims_declared": 3,
            "claims_grounded": 3,
        }
        collector.record_transaction(sample_txn)
    
    # Generate and save report
    report = collector.generate_report()
    print("\n=== BASELINE REPORT ===")
    print(json.dumps(report, indent=2))
    collector.save_baseline()

