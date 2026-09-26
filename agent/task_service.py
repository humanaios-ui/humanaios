#!/usr/bin/env python3
"""
Phase 3: Multi-practice Task Service
REST API for task submission and status tracking.
"""

import json
import uuid
import time
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3
import threading
import logging

from flask import Flask, request, jsonify, g
from werkzeug.exceptions import BadRequest, TooManyRequests, ServiceUnavailable
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
from observability import get_tracer
from opentelemetry import trace as trace_api

tracer = get_tracer(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger('task-service')

# Prometheus metrics
requests_total = Counter(
    'requests_total',
    'Total task requests received',
    ['practice', 'status']
)

requests_latency = Histogram(
    'requests_latency_seconds',
    'HTTP request latency',
    ['endpoint']
)

task_latency = Histogram(
    'task_latency_seconds',
    'Task processing latency',
    ['practice', 'priority', 'phase']
)

queue_depth = Gauge(
    'queue_depth',
    'Current queue depth'
)

active_tasks = Gauge(
    'active_tasks',
    'Currently active tasks'
)


class TaskStatus(Enum):
    """Task lifecycle states"""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Priority(Enum):
    """Priority levels for task scheduling"""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


@dataclass
class TaskRequest:
    """Task submission request"""
    requesting_practice: str
    title: str
    description: str
    priority: int = 1
    deadline: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

    def validate(self) -> None:
        """Validate request fields"""
        if not self.requesting_practice or not self.requesting_practice.startswith("empirica-foundation"):
            raise BadRequest("Invalid requesting_practice")
        if not self.title or len(self.title) > 256:
            raise BadRequest("Title must be 1-256 characters")
        if not self.description or len(self.description) > 8000:
            raise BadRequest("Description must be 1-8000 characters")
        if self.priority not in [0, 1, 2, 3]:
            raise BadRequest("Priority must be 0 (low), 1 (normal), 2 (high), or 3 (critical)")


@dataclass
class Task:
    """Task state"""
    id: str
    requesting_practice: str
    title: str
    description: str
    priority: int
    deadline: Optional[str]
    context: Optional[Dict[str, Any]]
    status: str
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    output: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    artifacts_logged: int = 0


class TaskDatabase:
    """SQLite task persistence"""

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.lock = threading.RLock()
        self._init_schema()

    def _init_schema(self) -> None:
        """Create database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                requesting_practice TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                priority INTEGER NOT NULL,
                deadline TEXT,
                context TEXT,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                started_at TEXT,
                completed_at TEXT,
                output TEXT,
                error_message TEXT,
                artifacts_logged INTEGER DEFAULT 0
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tasks_practice_created
            ON tasks (requesting_practice, created_at DESC)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tasks_status_priority
            ON tasks (status, priority DESC, deadline)
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS task_events (
                id TEXT PRIMARY KEY,
                task_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                metadata TEXT,
                FOREIGN KEY (task_id) REFERENCES tasks(id)
            )
        """)

        conn.commit()
        conn.close()
        logger.info("Database schema initialized")

    def create_task(self, req: TaskRequest) -> Task:
        """Create and persist a new task"""
        task_id = f"task_{uuid.uuid4().hex[:16]}"
        now = datetime.now(timezone.utc).isoformat()

        task = Task(
            id=task_id,
            requesting_practice=req.requesting_practice,
            title=req.title,
            description=req.description,
            priority=req.priority,
            deadline=req.deadline,
            context=req.context,
            status=TaskStatus.QUEUED.value,
            created_at=now
        )

        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO tasks
                (id, requesting_practice, title, description, priority, deadline, context, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task.id,
                task.requesting_practice,
                task.title,
                task.description,
                task.priority,
                task.deadline,
                json.dumps(task.context) if task.context else None,
                task.status,
                task.created_at
            ))

            # Log event
            event_id = f"event_{uuid.uuid4().hex[:16]}"
            cursor.execute("""
                INSERT INTO task_events
                (id, task_id, event_type, timestamp, metadata)
                VALUES (?, ?, ?, ?, ?)
            """, (
                event_id,
                task.id,
                "submitted",
                now,
                json.dumps({"requesting_practice": req.requesting_practice})
            ))

            conn.commit()
            conn.close()

        logger.info(f"Task created: {task.id}")
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieve task by ID"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, requesting_practice, title, description, priority, deadline, context,
                       status, created_at, started_at, completed_at, output, error_message, artifacts_logged
                FROM tasks WHERE id = ?
            """, (task_id,))

            row = cursor.fetchone()
            conn.close()

            if not row:
                return None

            (task_id, practice, title, desc, priority, deadline, context, status, created_at,
             started_at, completed_at, output, error_msg, artifacts) = row

            return Task(
                id=task_id,
                requesting_practice=practice,
                title=title,
                description=desc,
                priority=priority,
                deadline=deadline,
                context=json.loads(context) if context else None,
                status=status,
                created_at=created_at,
                started_at=started_at,
                completed_at=completed_at,
                output=json.loads(output) if output else None,
                error_message=error_msg,
                artifacts_logged=artifacts
            )

    def update_status(self, task_id: str, status: str,
                     output: Optional[Dict] = None,
                     error_message: Optional[str] = None) -> None:
        """Update task status"""
        now = datetime.now(timezone.utc).isoformat()

        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            if status == TaskStatus.PROCESSING.value:
                cursor.execute("""
                    UPDATE tasks SET status = ?, started_at = ? WHERE id = ?
                """, (status, now, task_id))
            elif status == TaskStatus.COMPLETED.value:
                cursor.execute("""
                    UPDATE tasks SET status = ?, completed_at = ?, output = ? WHERE id = ?
                """, (status, now, json.dumps(output) if output else None, task_id))
            elif status == TaskStatus.FAILED.value:
                cursor.execute("""
                    UPDATE tasks SET status = ?, completed_at = ?, error_message = ? WHERE id = ?
                """, (status, now, error_message, task_id))

            # Log event
            event_id = f"event_{uuid.uuid4().hex[:16]}"
            cursor.execute("""
                INSERT INTO task_events
                (id, task_id, event_type, timestamp, metadata)
                VALUES (?, ?, ?, ?, ?)
            """, (
                event_id,
                task_id,
                status,
                now,
                json.dumps({
                    "has_output": output is not None,
                    "has_error": error_message is not None
                })
            ))

            conn.commit()
            conn.close()

        logger.info(f"Task {task_id} → {status}")

    def list_tasks_by_practice(self, practice: str, limit: int = 10) -> List[Task]:
        """List recent tasks for a practice"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, requesting_practice, title, description, priority, deadline, context,
                       status, created_at, started_at, completed_at, output, error_message, artifacts_logged
                FROM tasks WHERE requesting_practice = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (practice, limit))

            rows = cursor.fetchall()
            conn.close()

            tasks = []
            for row in rows:
                (task_id, practice, title, desc, priority, deadline, context, status, created_at,
                 started_at, completed_at, output, error_msg, artifacts) = row

                tasks.append(Task(
                    id=task_id,
                    requesting_practice=practice,
                    title=title,
                    description=desc,
                    priority=priority,
                    deadline=deadline,
                    context=json.loads(context) if context else None,
                    status=status,
                    created_at=created_at,
                    started_at=started_at,
                    completed_at=completed_at,
                    output=json.loads(output) if output else None,
                    error_message=error_msg,
                    artifacts_logged=artifacts
                ))

            return tasks


class TaskService:
    """REST API service for task management"""

    def __init__(self, db_path: str = "/tmp/tasks.db"):
        self.db = TaskDatabase(db_path)
        self.app = Flask(__name__)
        self.rate_limits = {}  # practice → (count, window_start)
        self.setup_routes()

    def setup_routes(self) -> None:
        """Configure REST endpoints"""

        @self.app.route("/api/tasks/submit", methods=["POST"])
        def submit_task():
            start_time = time.time()
            status_code = 500

            with tracer.start_as_current_span("http.request.submit") as span:
                try:
                    data = request.get_json()
                    if not data:
                        raise BadRequest("Request body must be JSON")

                    # Parse and validate request
                    req = TaskRequest(
                        requesting_practice=data.get("requesting_practice"),
                        title=data.get("title"),
                        description=data.get("description"),
                        priority=data.get("priority", 1),
                        deadline=data.get("deadline"),
                        context=data.get("context")
                    )
                    req.validate()

                    # Add span attributes
                    span.set_attribute("http.method", "POST")
                    span.set_attribute("http.url", "/api/tasks/submit")
                    span.set_attribute("task.practice", req.requesting_practice)
                    span.set_attribute("task.priority", req.priority)

                    # Check rate limit (100 requests/minute per practice)
                    self._check_rate_limit(req.requesting_practice)

                    # Create and persist task
                    task = self.db.create_task(req)
                    status_code = 202

                    # Add trace_id to task context for distributed tracing
                    span_context = trace_api.get_current_span().get_span_context()
                    if task.context is None:
                        task.context = {}
                    task.context['trace_id'] = format(span_context.trace_id, '032x')
                    task.context['span_id'] = format(span_context.span_id, '016x')

                    # Record metrics
                    requests_total.labels(practice=req.requesting_practice, status='success').inc()
                    requests_latency.labels(endpoint='submit_task').observe(time.time() - start_time)

                    span.set_attribute("http.status_code", 202)
                    span.set_attribute("task.id", task.id)

                    return jsonify({
                        "task_id": task.id,
                        "status": task.status,
                        "created_at": task.created_at,
                        "estimated_wait_time_seconds": 60
                    }), 202

                except BadRequest as e:
                    status_code = 400
                    logger.warning(f"Bad request: {e}")
                    requests_total.labels(practice='unknown', status='bad_request').inc()
                    requests_latency.labels(endpoint='submit_task').observe(time.time() - start_time)
                    span.set_attribute("http.status_code", 400)
                    span.record_exception(e)
                    return jsonify({"error": str(e)}), 400
                except TooManyRequests as e:
                    status_code = 429
                    logger.warning(f"Rate limit: {e}")
                    requests_total.labels(practice='unknown', status='rate_limited').inc()
                    requests_latency.labels(endpoint='submit_task').observe(time.time() - start_time)
                    span.set_attribute("http.status_code", 429)
                    span.record_exception(e)
                    return jsonify({"error": str(e)}), 429
                except Exception as e:
                    status_code = 500
                    logger.error(f"Error submitting task: {e}")
                    requests_total.labels(practice='unknown', status='error').inc()
                    requests_latency.labels(endpoint='submit_task').observe(time.time() - start_time)
                    span.set_attribute("http.status_code", 500)
                    span.record_exception(e)
                    return jsonify({"error": "Internal server error"}), 500

        @self.app.route("/api/tasks/<task_id>", methods=["GET"])
        def get_task(task_id):
            start_time = time.time()
            try:
                task = self.db.get_task(task_id)
                if not task:
                    requests_latency.labels(endpoint='get_task').observe(time.time() - start_time)
                    return jsonify({"error": "Task not found"}), 404

                response = {
                    "task_id": task.id,
                    "status": task.status,
                    "requesting_practice": task.requesting_practice,
                    "title": task.title,
                    "created_at": task.created_at,
                    "started_at": task.started_at,
                    "completed_at": task.completed_at
                }

                if task.status == TaskStatus.COMPLETED.value:
                    response["output"] = task.output
                    response["artifacts_logged"] = task.artifacts_logged
                    if task.output:
                        response["total_reasoning_chars"] = sum(
                            len(v) for v in task.output.values() if isinstance(v, str)
                        )

                elif task.status == TaskStatus.FAILED.value:
                    response["error_message"] = task.error_message

                requests_latency.labels(endpoint='get_task').observe(time.time() - start_time)
                return jsonify(response), 200

            except Exception as e:
                logger.error(f"Error getting task: {e}")
                requests_latency.labels(endpoint='get_task').observe(time.time() - start_time)
                return jsonify({"error": "Internal server error"}), 500

        @self.app.route("/api/health", methods=["GET"])
        def health():
            return jsonify({"status": "healthy"}), 200

        @self.app.route("/metrics", methods=["GET"])
        def metrics():
            return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

        @self.app.errorhandler(500)
        def handle_error(error):
            logger.error(f"Internal error: {error}")
            return jsonify({"error": "Internal server error"}), 500

    def _check_rate_limit(self, practice: str) -> None:
        """Check rate limit (100 requests/minute per practice)"""
        now = datetime.now(timezone.utc).timestamp()

        if practice not in self.rate_limits:
            self.rate_limits[practice] = (1, now)
            return

        count, window_start = self.rate_limits[practice]
        elapsed = now - window_start

        if elapsed < 60:  # Within 1-minute window
            if count >= 100:
                raise TooManyRequests("Rate limit exceeded: 100 requests/minute per practice")
            self.rate_limits[practice] = (count + 1, window_start)
        else:
            # New window
            self.rate_limits[practice] = (1, now)

    def run(self, host: str = "0.0.0.0", port: int = 5000, debug: bool = False) -> None:
        """Start the service"""
        logger.info(f"Starting Task Service on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug, threaded=True)


if __name__ == "__main__":
    service = TaskService(db_path="/tmp/tasks.db")
    service.run(debug=True)
