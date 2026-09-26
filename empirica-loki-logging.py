#!/usr/bin/env python3
"""
Empirica → Loki Logging Integration
Forwards empirica session logs to Loki via HTTP API
"""

import json
import logging
import time
from datetime import datetime
from typing import Optional, Dict, Any
import requests
from pathlib import Path

class EmpirikaLokiHandler(logging.Handler):
    """Python logging handler that sends logs to Loki"""

    def __init__(self, loki_url: str = "http://localhost:3100", batch_size: int = 10):
        super().__init__()
        self.loki_url = loki_url.rstrip('/')
        self.batch_size = batch_size
        self.logs_buffer = []
        self.session_id = None
        self.practice = None
        self.phase = None

    def set_context(self, session_id: str, practice: str, phase: str):
        """Set the context labels for log entries"""
        self.session_id = session_id
        self.practice = practice
        self.phase = phase

    def emit(self, record: logging.LogRecord):
        """Send log record to Loki"""
        try:
            # Format log entry
            log_entry = {
                "timestamp": int(record.created * 1e9),  # nanoseconds
                "level": record.levelname,
                "logger": record.name,
                "message": self.format(record),
                "session_id": self.session_id,
                "practice": self.practice,
                "phase": self.phase,
            }

            # Add extra fields from LogRecord
            if hasattr(record, 'task_id'):
                log_entry['task_id'] = record.task_id
            if hasattr(record, 'goal_id'):
                log_entry['goal_id'] = record.goal_id
            if hasattr(record, 'vector_name'):
                log_entry['vector_name'] = record.vector_name

            self.logs_buffer.append((int(record.created * 1e9), json.dumps(log_entry)))

            # Flush if buffer is full
            if len(self.logs_buffer) >= self.batch_size:
                self.flush()

        except Exception as e:
            self.handleError(record)

    def flush(self):
        """Send buffered logs to Loki"""
        if not self.logs_buffer:
            return

        try:
            # Sort by timestamp
            self.logs_buffer.sort(key=lambda x: x[0])

            # Build Loki push request
            payload = {
                "streams": [
                    {
                        "stream": {
                            "job": "empirica-sessions",
                            "practice": self.practice or "unknown",
                            "phase": self.phase or "unknown",
                            "session_id": self.session_id or "unknown"
                        },
                        "values": [
                            [str(ts), msg] for ts, msg in self.logs_buffer
                        ]
                    }
                ]
            }

            # POST to Loki
            response = requests.post(
                f"{self.loki_url}/loki/api/v1/push",
                json=payload,
                timeout=5
            )

            if response.status_code in (200, 204):
                self.logs_buffer = []
            else:
                logging.warning(f"Loki push failed: {response.status_code}")

        except Exception as e:
            logging.error(f"Failed to flush logs to Loki: {e}")


class AcatMetricsLokiHandler(logging.Handler):
    """Handler for ACAT grounding metrics → Loki"""

    def __init__(self, loki_url: str = "http://localhost:3100"):
        super().__init__()
        self.loki_url = loki_url.rstrip('/')
        self.metrics_buffer = []

    def emit(self, record: logging.LogRecord):
        """Send ACAT metric to Loki"""
        try:
            # Extract ACAT-specific fields
            metric_entry = {
                "timestamp": int(record.created * 1e9),
                "ai_id": getattr(record, 'ai_id', 'unknown'),
                "vector_name": getattr(record, 'vector_name', ''),
                "predicted": getattr(record, 'predicted', 0.0),
                "actual": getattr(record, 'actual', 0.0),
                "brier_error": getattr(record, 'brier_error', 0.0),
                "phase": getattr(record, 'phase', 'unknown'),
                "session_id": getattr(record, 'session_id', ''),
                "message": self.format(record)
            }

            self.metrics_buffer.append((int(record.created * 1e9), json.dumps(metric_entry)))

            # Flush every 10 entries or every 30 seconds (handled by TimedRotatingFileHandler upstream)
            if len(self.metrics_buffer) >= 10:
                self.flush()

        except Exception as e:
            self.handleError(record)

    def flush(self):
        """Send buffered ACAT metrics to Loki"""
        if not self.metrics_buffer:
            return

        try:
            self.metrics_buffer.sort(key=lambda x: x[0])

            payload = {
                "streams": [
                    {
                        "stream": {
                            "job": "acat-grounding",
                            "source": "empirica"
                        },
                        "values": [
                            [str(ts), msg] for ts, msg in self.metrics_buffer
                        ]
                    }
                ]
            }

            response = requests.post(
                f"{self.loki_url}/loki/api/v1/push",
                json=payload,
                timeout=5
            )

            if response.status_code in (200, 204):
                self.metrics_buffer = []
            else:
                logging.warning(f"ACAT metrics push failed: {response.status_code}")

        except Exception as e:
            logging.error(f"Failed to push ACAT metrics to Loki: {e}")


def setup_empirica_loki_logging(
    session_id: str,
    practice: str,
    phase: str,
    loki_url: str = "http://localhost:3100"
) -> logging.Logger:
    """
    Configure empirica logger with Loki handler

    Usage:
        logger = setup_empirica_loki_logging(
            session_id="sess_abc123",
            practice="autonomy",
            phase="PREFLIGHT",
            loki_url="http://loki:3100"
        )
        logger.info("Starting PREFLIGHT phase")
    """

    logger = logging.getLogger("empirica.sessions")
    logger.setLevel(logging.DEBUG)

    # Create Loki handler
    loki_handler = EmpirikaLokiHandler(loki_url=loki_url)
    loki_handler.set_context(session_id, practice, phase)
    loki_handler.setFormatter(logging.Formatter(
        '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
    ))

    logger.addHandler(loki_handler)

    return logger


def setup_acat_metrics_logging(
    loki_url: str = "http://localhost:3100"
) -> logging.Logger:
    """
    Configure ACAT metrics logger for Loki

    Usage:
        acat_logger = setup_acat_metrics_logging(loki_url="http://loki:3100")
        acat_logger.info("Calibration check", extra={
            'ai_id': 'autonomy',
            'vector_name': 'know',
            'predicted': 0.75,
            'actual': 0.68,
            'brier_error': 0.0049
        })
    """

    logger = logging.getLogger("empirica.acat")
    logger.setLevel(logging.INFO)

    # Create ACAT handler
    acat_handler = AcatMetricsLokiHandler(loki_url=loki_url)
    acat_handler.setFormatter(logging.Formatter(
        '{"timestamp": "%(asctime)s", "message": "%(message)s"}'
    ))

    logger.addHandler(acat_handler)

    return logger


# Example integration
if __name__ == "__main__":
    import sys

    # Configure loggers
    session_logger = setup_empirica_loki_logging(
        session_id="sess_demo_001",
        practice="autonomy",
        phase="PREFLIGHT"
    )

    acat_logger = setup_acat_metrics_logging()

    # Test logging
    session_logger.info("PREFLIGHT submitted")
    session_logger.debug("Vectors: know=0.8, do=0.9, context=0.75")

    acat_logger.info("ACAT calibration check", extra={
        'ai_id': 'autonomy',
        'vector_name': 'know',
        'predicted': 0.80,
        'actual': 0.78,
        'brier_error': 0.0004,
        'phase': 'POSTFLIGHT',
        'session_id': 'sess_demo_001'
    })

    session_logger.info("Logs flushed to Loki")

    # Flush handlers before exit
    for handler in session_logger.handlers:
        if isinstance(handler, EmpirikaLokiHandler):
            handler.flush()

    for handler in acat_logger.handlers:
        if isinstance(handler, AcatMetricsLokiHandler):
            handler.flush()
