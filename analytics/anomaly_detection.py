#!/usr/bin/env python3
"""
Anomaly Detection Engine for Observability Stack
Detects anomalies in query latency, ingestion rates, coordination, vector calibration
"""

import json
import subprocess
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("anomaly_detection")


@dataclass
class AnomalyAlert:
    anomaly_type: str
    severity: str  # critical, warning, info
    practice: str
    metric: str
    current_value: float
    threshold: float
    message: str
    timestamp: str


class AnomalyDetector:
    """Detects anomalies in observability metrics"""

    def __init__(self, prometheus_url: str = "http://localhost:9090", loki_url: str = "http://localhost:3100"):
        self.prometheus_url = prometheus_url
        self.loki_url = loki_url
        self.anomalies: List[AnomalyAlert] = []

    def query_prometheus(self, query: str, time_range: str = "5m") -> Dict[str, Any]:
        """Query Prometheus for metrics"""
        cmd = [
            "curl", "-s",
            f"{self.prometheus_url}/api/v1/query",
            "--data-urlencode", f"query={query}",
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                logger.error(f"Prometheus query failed: {result.stderr}")
                return {}
        except Exception as e:
            logger.error(f"Prometheus query error: {str(e)}")
            return {}

    def detect_query_latency_anomalies(self) -> List[AnomalyAlert]:
        """Detect anomalies in query latency (p95 > 1000ms)"""
        alerts = []

        # Query Prometheus for query latency p95
        query = 'histogram_quantile(0.95, rate(loki_query_duration_seconds_bucket[5m]))'
        result = self.query_prometheus(query)

        if result.get("data", {}).get("result"):
            for item in result["data"]["result"]:
                value = float(item["value"][1])
                # Threshold: 1000ms
                if value > 1.0:  # Prometheus time is in seconds
                    practice = item["metric"].get("practice", "unknown")
                    alerts.append(AnomalyAlert(
                        anomaly_type="query_latency",
                        severity="warning" if value < 2.0 else "critical",
                        practice=practice,
                        metric="query_latency_p95",
                        current_value=value * 1000,  # Convert to ms
                        threshold=1000,
                        message=f"Query latency p95: {value*1000:.0f}ms (threshold: 1000ms)",
                        timestamp=datetime.now().isoformat()
                    ))

        return alerts

    def detect_ingestion_rate_anomalies(self) -> List[AnomalyAlert]:
        """Detect anomalies in log ingestion rate (drop below baseline)"""
        alerts = []

        # Query ingestion rate
        query = 'rate(loki_ingester_chunks_flushed_total[5m])'
        result = self.query_prometheus(query)

        # Get baseline (last 1 hour average)
        baseline_query = 'avg_over_time(rate(loki_ingester_chunks_flushed_total[5m])[1h:1m])'
        baseline_result = self.query_prometheus(baseline_query)

        if result.get("data", {}).get("result") and baseline_result.get("data", {}).get("result"):
            current = float(result["data"]["result"][0]["value"][1])
            baseline = float(baseline_result["data"]["result"][0]["value"][1])

            # Alert if current is 30% below baseline
            if current < baseline * 0.7:
                alerts.append(AnomalyAlert(
                    anomaly_type="ingestion_rate",
                    severity="warning",
                    practice="foundation",
                    metric="ingestion_rate",
                    current_value=current,
                    threshold=baseline * 0.7,
                    message=f"Ingestion rate dropped to {current:.2f} (baseline: {baseline:.2f})",
                    timestamp=datetime.now().isoformat()
                ))

        return alerts

    def detect_coordination_delays(self) -> List[AnomalyAlert]:
        """Detect anomalies in SER coordination (decision latency)"""
        alerts = []

        # Query decision latency p95
        query = 'histogram_quantile(0.95, rate(ser_decision_latency_seconds_bucket[5m]))'
        result = self.query_prometheus(query)

        if result.get("data", {}).get("result"):
            for item in result["data"]["result"]:
                value = float(item["value"][1])
                # Threshold: 5 seconds
                if value > 5.0:
                    practice = item["metric"].get("practice", "unknown")
                    alerts.append(AnomalyAlert(
                        anomaly_type="coordination_delay",
                        severity="warning",
                        practice=practice,
                        metric="ser_decision_latency_p95",
                        current_value=value,
                        threshold=5.0,
                        message=f"SER decision latency p95: {value:.2f}s (threshold: 5s)",
                        timestamp=datetime.now().isoformat()
                    ))

        return alerts

    def detect_vector_calibration_drift(self) -> List[AnomalyAlert]:
        """Detect anomalies in vector calibration (large divergence)"""
        alerts = []

        # Query vector divergence from service observations
        query = 'abs(acat_self_report_vector - acat_service_observation_vector)'
        result = self.query_prometheus(query)

        if result.get("data", {}).get("result"):
            for item in result["data"]["result"]:
                value = float(item["value"][1])
                vector_name = item["metric"].get("vector", "unknown")
                practice = item["metric"].get("practice", "unknown")

                # Threshold: 0.15 (15% divergence)
                if value > 0.15:
                    alerts.append(AnomalyAlert(
                        anomaly_type="vector_drift",
                        severity="warning",
                        practice=practice,
                        metric=f"vector_divergence_{vector_name}",
                        current_value=value,
                        threshold=0.15,
                        message=f"Vector {vector_name} divergence: {value:.2f} (threshold: 0.15)",
                        timestamp=datetime.now().isoformat()
                    ))

        return alerts

    def detect_practice_health_degradation(self) -> List[AnomalyAlert]:
        """Detect overall practice health degradation"""
        alerts = []

        # Query practice health score (composite metric)
        query = 'empirica_practice_health_score'
        result = self.query_prometheus(query)

        if result.get("data", {}).get("result"):
            for item in result["data"]["result"]:
                score = float(item["value"][1])
                practice = item["metric"].get("practice", "unknown")

                # Threshold: 0.7 (70% health)
                if score < 0.7:
                    severity = "critical" if score < 0.5 else "warning"
                    alerts.append(AnomalyAlert(
                        anomaly_type="health_degradation",
                        severity=severity,
                        practice=practice,
                        metric="practice_health_score",
                        current_value=score,
                        threshold=0.7,
                        message=f"Practice health score: {score:.2f} (threshold: 0.7)",
                        timestamp=datetime.now().isoformat()
                    ))

        return alerts

    def run_detection(self) -> List[AnomalyAlert]:
        """Run all anomaly detection checks"""
        logger.info("Starting anomaly detection sweep...")

        all_anomalies = []

        # Run all detectors
        detectors = [
            ("Query Latency", self.detect_query_latency_anomalies),
            ("Ingestion Rate", self.detect_ingestion_rate_anomalies),
            ("Coordination Delays", self.detect_coordination_delays),
            ("Vector Drift", self.detect_vector_calibration_drift),
            ("Practice Health", self.detect_practice_health_degradation),
        ]

        for detector_name, detector_func in detectors:
            try:
                logger.info(f"  Running: {detector_name}")
                anomalies = detector_func()
                all_anomalies.extend(anomalies)
                logger.info(f"    Found {len(anomalies)} anomalies")
            except Exception as e:
                logger.error(f"  Error in {detector_name}: {str(e)}")

        self.anomalies = all_anomalies
        logger.info(f"Detection complete: {len(all_anomalies)} total anomalies found")

        return all_anomalies

    def get_anomalies_by_severity(self) -> Dict[str, List[AnomalyAlert]]:
        """Group anomalies by severity"""
        grouped = {"critical": [], "warning": [], "info": []}

        for anomaly in self.anomalies:
            grouped[anomaly.severity].append(anomaly)

        return grouped

    def export_anomalies_json(self, filepath: str = "anomalies.json"):
        """Export detected anomalies to JSON"""
        anomalies_dict = [
            {
                "type": a.anomaly_type,
                "severity": a.severity,
                "practice": a.practice,
                "metric": a.metric,
                "current_value": a.current_value,
                "threshold": a.threshold,
                "message": a.message,
                "timestamp": a.timestamp,
            }
            for a in self.anomalies
        ]

        with open(filepath, "w") as f:
            json.dump({
                "detection_time": datetime.now().isoformat(),
                "total_anomalies": len(self.anomalies),
                "anomalies": anomalies_dict,
                "summary": {
                    "critical": len([a for a in self.anomalies if a.severity == "critical"]),
                    "warning": len([a for a in self.anomalies if a.severity == "warning"]),
                    "info": len([a for a in self.anomalies if a.severity == "info"]),
                }
            }, f, indent=2)

        logger.info(f"Anomalies exported to {filepath}")


def main():
    detector = AnomalyDetector()
    anomalies = detector.run_detection()

    # Print summary
    print("\n" + "=" * 60)
    print("Anomaly Detection Summary")
    print("=" * 60)

    by_severity = detector.get_anomalies_by_severity()
    print(f"🔴 Critical: {len(by_severity['critical'])}")
    print(f"🟡 Warning: {len(by_severity['warning'])}")
    print(f"🔵 Info: {len(by_severity['info'])}")
    print(f"📊 Total: {len(anomalies)}")

    if by_severity['critical']:
        print("\nCRITICAL ANOMALIES:")
        for anomaly in by_severity['critical']:
            print(f"  • {anomaly.practice}: {anomaly.message}")

    if by_severity['warning']:
        print("\nWARNING ANOMALIES:")
        for anomaly in by_severity['warning'][:5]:  # Show first 5
            print(f"  • {anomaly.practice}: {anomaly.message}")
        if len(by_severity['warning']) > 5:
            print(f"  ... and {len(by_severity['warning']) - 5} more")

    print("\n" + "=" * 60)

    # Export results
    detector.export_anomalies_json()


if __name__ == "__main__":
    main()
