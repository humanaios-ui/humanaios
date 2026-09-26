#!/usr/bin/env python3
"""
Empirica Observability Instrumentation
Wires empirica-sessions logs, practice stdout, and ACAT metrics into Loki/Jaeger.
"""

import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Configure logging for empirica sessions
LOGS_DIR = Path.home() / ".empirica" / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

SESSION_LOG_FILE = LOGS_DIR / "empirica-instrumentation.log"

# Root logger for empirica
logger = logging.getLogger("empirica.instrumentation")
logger.setLevel(logging.INFO)

# File handler for empirica logs
fh = logging.FileHandler(SESSION_LOG_FILE)
fh.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S'
)
fh.setFormatter(formatter)
logger.addHandler(fh)


class PracticeStdoutCapture:
    """Capture practice stdout to log file for Loki ingestion."""

    def __init__(self, practice_id: str):
        self.practice_id = practice_id
        self.log_dir = Path("/tmp/autonomous-agents")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / f"{practice_id}.log"
        self.logger = logging.getLogger(f"practice.{practice_id}")

        # Configure practice logger
        fh = logging.FileHandler(self.log_file)
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(name)s: %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S'
        )
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.setLevel(logging.INFO)

    def log(self, level: str, message: str):
        """Log message with level (DEBUG, INFO, WARNING, ERROR)."""
        getattr(self.logger, level.lower())(message)

    def log_execution(self, task: str, status: str, duration_s: float = None):
        """Log task execution event."""
        msg = f"Task: {task} | Status: {status}"
        if duration_s:
            msg += f" | Duration: {duration_s:.2f}s"
        self.logger.info(msg)


class ACATMetricsCollector:
    """Collect ACAT (Auto-Calibrating Assessment Tool) metrics for Loki/Jaeger."""

    def __init__(self):
        self.metrics_dir = Path("/tmp/acat-metrics")
        self.metrics_dir.mkdir(parents=True, exist_ok=True)

    def record_vector_metric(self, practice_id: str, vector_name: str, value: float, metadata: dict = None):
        """Record a calibration vector metric."""
        timestamp = datetime.now(timezone.utc).isoformat()
        metric = {
            "timestamp": timestamp,
            "metric_type": "vector",
            "practice_id": practice_id,
            "vector_name": vector_name,
            "value": value,
            "metadata": metadata or {}
        }

        # Write to JSONL file for Loki ingestion
        metrics_file = self.metrics_dir / f"{practice_id}-metrics.jsonl"
        with open(metrics_file, "a") as f:
            f.write(json.dumps(metric) + "\n")

    def record_transaction_metric(self, practice_id: str, transaction_id: str, metrics: dict):
        """Record transaction-level metrics."""
        timestamp = datetime.now(timezone.utc).isoformat()
        metric = {
            "timestamp": timestamp,
            "metric_type": "transaction",
            "practice_id": practice_id,
            "transaction_id": transaction_id,
            "metrics": metrics
        }

        metrics_file = self.metrics_dir / f"{practice_id}-metrics.jsonl"
        with open(metrics_file, "a") as f:
            f.write(json.dumps(metric) + "\n")


def initialize_instrumentation(practice_id: str = None):
    """Initialize instrumentation for a practice."""
    logger.info(f"Initializing instrumentation for practice: {practice_id or 'evaluator'}")

    # Set up practice stdout capture
    if practice_id:
        stdout_capture = PracticeStdoutCapture(practice_id)
        logger.info(f"Practice stdout capture initialized: {stdout_capture.log_file}")
        return stdout_capture

    # Set up ACAT metrics collector
    metrics_collector = ACATMetricsCollector()
    logger.info(f"ACAT metrics collector initialized: {metrics_collector.metrics_dir}")
    return metrics_collector


def validate_log_ingestion(loki_url: str = "http://localhost:3100", timeout_s: int = 30):
    """Validate that logs are flowing into Loki at <5s latency."""
    import requests

    start_time = time.time()
    while time.time() - start_time < timeout_s:
        try:
            # Query Loki for recent logs
            response = requests.get(
                f"{loki_url}/loki/api/v1/query",
                params={
                    "query": '{job=~"empirica_sessions|practice_stdout|acat_metrics"}',
                    "limit": 10
                },
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                streams = data.get("data", {}).get("result", [])

                if streams:
                    logger.info(f"✓ Log ingestion validated: {len(streams)} streams flowing to Loki")

                    # Check ingestion latency
                    latest_log_time = None
                    for stream in streams:
                        if stream.get("values"):
                            latest_ts_ns = int(stream["values"][-1][0])
                            latest_ts = latest_ts_ns / 1e9
                            if not latest_log_time or latest_ts > latest_log_time:
                                latest_log_time = latest_ts

                    if latest_log_time:
                        ingestion_latency = time.time() - latest_log_time
                        logger.info(f"✓ Ingestion latency: {ingestion_latency:.2f}s (target: <5s)")
                        return ingestion_latency < 5.0

        except Exception as e:
            logger.debug(f"Loki health check: {e}")

        time.sleep(1)

    logger.warning(f"Log ingestion validation timeout after {timeout_s}s")
    return False


if __name__ == "__main__":
    # Initialize instrumentation
    if len(sys.argv) > 1:
        practice_id = sys.argv[1]
        capture = initialize_instrumentation(practice_id)
        capture.log("INFO", "Instrumentation initialized for practice execution")
    else:
        collector = initialize_instrumentation()
        logger.info("Instrumentation ready for empirica sessions")
