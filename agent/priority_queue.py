#!/usr/bin/env python3
"""
Phase 3.2: Priority Queue and Worker Pool for task scheduling
"""

import heapq
import threading
import time
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from prometheus_client import Counter, Gauge, Histogram
from task_service import TaskDatabase, TaskStatus
from observability import get_tracer

logger = logging.getLogger('priority-queue')
tracer = get_tracer(__name__)

# Prometheus metrics for queue and workers
tasks_enqueued = Counter(
    'tasks_enqueued_total',
    'Total tasks enqueued',
    ['priority']
)

tasks_dequeued = Counter(
    'tasks_dequeued_total',
    'Total tasks dequeued',
    ['priority']
)

tasks_processed_total = Counter(
    'tasks_processed_total',
    'Total tasks processed',
    ['status']
)

queue_wait_time = Histogram(
    'queue_wait_time_seconds',
    'Time tasks spend in queue',
    ['priority']
)

active_workers = Gauge(
    'active_workers',
    'Number of active workers'
)

current_queue_depth = Gauge(
    'current_queue_depth',
    'Current queue depth'
)

worker_tasks_processed = Counter(
    'worker_tasks_processed_total',
    'Total tasks processed by workers',
    ['worker_id', 'status']
)


@dataclass
class PriorityItem:
    """Item in priority queue"""
    effective_priority: float
    task_id: str
    original_priority: int
    created_at: float
    deadline: Optional[str] = None

    def __lt__(self, other):
        """Comparison for min-heap (lower priority_value = higher priority)"""
        # Sort by effective_priority DESC (negate for min-heap), then by creation time ASC
        if self.effective_priority != other.effective_priority:
            return self.effective_priority > other.effective_priority
        return self.created_at < other.created_at


class PriorityQueue:
    """Thread-safe priority queue with aging and deadline support"""

    def __init__(self):
        self.heap = []
        self.lock = threading.RLock()
        self.task_create_times = {}
        self.aging_boost_per_minute = {
            3: 100,  # Critical: +100/min
            2: 10,   # High: +10/min
            1: 1,    # Normal: +1/min
            0: 0.1   # Low: +0.1/min
        }

    def enqueue(self, task_id: str, priority: int, deadline: Optional[str] = None) -> None:
        """Add task to queue with priority"""
        with tracer.start_as_current_span("queue.enqueue") as span:
            now = time.time()
            self.task_create_times[task_id] = now
            effective_priority = self._calculate_priority(priority, now)

            span.set_attribute("queue.task_id", task_id)
            span.set_attribute("queue.priority", priority)
            span.set_attribute("queue.deadline", deadline or "none")

            with self.lock:
                item = PriorityItem(
                    effective_priority=effective_priority,
                    task_id=task_id,
                    original_priority=priority,
                    created_at=now,
                    deadline=deadline
                )
                heapq.heappush(self.heap, item)

                # Record metrics
                tasks_enqueued.labels(priority=priority).inc()
                current_queue_depth.set(len(self.heap))
                span.set_attribute("queue.depth", len(self.heap))

            logger.info(f"Enqueued {task_id} (priority={priority}, effective={effective_priority:.1f})")

    def dequeue(self) -> Optional[str]:
        """Get highest-priority task from queue"""
        with tracer.start_as_current_span("queue.dequeue") as span:
            with self.lock:
                if not self.heap:
                    span.set_attribute("queue.empty", True)
                    return None

                # Re-calculate priorities in case items have aged
                now = time.time()
                refreshed_heap = []
                for item in self.heap:
                    item.effective_priority = self._calculate_priority(
                        item.original_priority,
                        item.created_at
                    )
                    refreshed_heap.append(item)

                heapq.heapify(refreshed_heap)
                self.heap = refreshed_heap

                if not self.heap:
                    span.set_attribute("queue.empty", True)
                    return None

                item = heapq.heappop(self.heap)
                wait_time = now - item.created_at

                # Record metrics
                tasks_dequeued.labels(priority=item.original_priority).inc()
                queue_wait_time.labels(priority=item.original_priority).observe(wait_time)
                current_queue_depth.set(len(self.heap))

                # Record span attributes
                span.set_attribute("queue.task_id", item.task_id)
                span.set_attribute("queue.priority", item.original_priority)
                span.set_attribute("queue.wait_time_seconds", wait_time)
                span.set_attribute("queue.depth", len(self.heap))

                logger.info(f"Dequeued {item.task_id} (priority={item.original_priority}, age={wait_time:.1f}s)")
                return item.task_id

    def size(self) -> int:
        """Get queue depth"""
        with self.lock:
            return len(self.heap)

    def _calculate_priority(self, base_priority: int, created_at: float) -> float:
        """Calculate effective priority with aging"""
        now = time.time()
        age_minutes = (now - created_at) / 60.0
        base_weight = [1, 10, 100, 1000][base_priority]
        aging_boost = self.aging_boost_per_minute[base_priority]

        effective = base_weight + (age_minutes * aging_boost)

        # Fair scheduling: after 10 minutes, boost low-priority to critical level
        if base_priority == 0 and age_minutes >= 10:
            effective = 1000 + (age_minutes - 10) * 100

        return effective


class TaskWorker:
    """Background worker that processes tasks from queue"""

    def __init__(self, worker_id: int, queue: PriorityQueue, db: TaskDatabase):
        self.worker_id = worker_id
        self.queue = queue
        self.db = db
        self.running = False
        self.tasks_processed = 0

    def run(self) -> None:
        """Main worker loop"""
        self.running = True
        logger.info(f"Worker {self.worker_id} started")

        while self.running:
            try:
                # Poll queue
                task_id = self.queue.dequeue()

                if not task_id:
                    time.sleep(0.5)  # Brief sleep if queue is empty
                    continue

                # Mark as processing
                self.db.update_status(task_id, TaskStatus.PROCESSING.value)

                # Execute task (placeholder - would call agent v3)
                logger.info(f"Worker {self.worker_id} executing {task_id}")
                self._execute_task(task_id)

                self.tasks_processed += 1

            except Exception as e:
                logger.error(f"Worker {self.worker_id} error: {e}")

    def stop(self) -> None:
        """Stop the worker"""
        self.running = False
        logger.info(f"Worker {self.worker_id} stopped (processed {self.tasks_processed} tasks)")

    def _execute_task(self, task_id: str) -> None:
        """Execute a task (placeholder for agent v3)"""
        with tracer.start_as_current_span("worker.execute") as span:
            start_time = time.time()
            try:
                span.set_attribute("worker.id", self.worker_id)
                span.set_attribute("task.id", task_id)

                # This is where we'd call agent v3
                # For now, simulate success
                time.sleep(1)  # Simulate work

                output = {
                    "understanding": "Analysis placeholder",
                    "planning": "Plan placeholder",
                    "execution": "Execution placeholder",
                    "reflection": "Reflection placeholder"
                }

                self.db.update_status(
                    task_id,
                    TaskStatus.COMPLETED.value,
                    output=output
                )

                # Record metrics
                elapsed = time.time() - start_time
                tasks_processed_total.labels(status='success').inc()
                worker_tasks_processed.labels(worker_id=self.worker_id, status='success').inc()

                span.set_attribute("task.status", "completed")
                span.set_attribute("task.duration_seconds", elapsed)
                logger.info(f"Task {task_id} completed by worker {self.worker_id} (took {elapsed:.2f}s)")

            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(f"Task {task_id} failed in worker {self.worker_id}: {e}")
                self.db.update_status(task_id, TaskStatus.FAILED.value, error_message=str(e))

                # Record metrics
                tasks_processed_total.labels(status='failed').inc()
                worker_tasks_processed.labels(worker_id=self.worker_id, status='failed').inc()

                span.set_attribute("task.status", "failed")
                span.set_attribute("task.error", str(e))
                span.set_attribute("task.duration_seconds", elapsed)
                span.record_exception(e)


class WorkerPool:
    """Pool of background workers"""

    def __init__(self, queue: PriorityQueue, db: TaskDatabase, worker_count: int = 3):
        self.queue = queue
        self.db = db
        self.worker_count = worker_count
        self.workers = []
        self.executor = ThreadPoolExecutor(max_workers=worker_count)
        self.running = False

    def start(self) -> None:
        """Start worker pool"""
        self.running = True
        logger.info(f"Starting {self.worker_count} workers")

        for i in range(self.worker_count):
            worker = TaskWorker(i, self.queue, self.db)
            self.workers.append(worker)
            self.executor.submit(worker.run)

        # Record metrics
        active_workers.set(self.worker_count)

    def stop(self) -> None:
        """Stop worker pool gracefully"""
        logger.info("Stopping worker pool")
        self.running = False

        # Signal workers to stop
        for worker in self.workers:
            worker.stop()

        # Wait for completion
        self.executor.shutdown(wait=True)

        # Record metrics
        active_workers.set(0)
        logger.info("Worker pool stopped")

    def get_stats(self) -> Dict[str, Any]:
        """Get worker pool statistics"""
        total_processed = sum(w.tasks_processed for w in self.workers)
        return {
            "worker_count": self.worker_count,
            "running": self.running,
            "queue_depth": self.queue.size(),
            "total_tasks_processed": total_processed
        }


def main():
    """Test the priority queue and worker pool"""
    # Setup
    from task_service import TaskService

    service = TaskService(db_path="/tmp/test_queue.db")
    queue = PriorityQueue()
    pool = WorkerPool(queue, service.db, worker_count=2)

    try:
        # Start pool
        pool.start()

        # Enqueue test tasks with different priorities
        for i in range(5):
            req_data = {
                "requesting_practice": f"empirica-foundation.carly.empirica-autonomy",
                "title": f"Test task {i}",
                "description": f"Description {i}",
                "priority": i % 4  # Mix of priorities
            }

            from task_service import TaskRequest
            req = TaskRequest(**req_data)
            req.validate()
            task = service.db.create_task(req)
            queue.enqueue(task.id, req.priority)

        # Let workers process
        time.sleep(5)

        # Print stats
        stats = pool.get_stats()
        logger.info(f"Stats: {stats}")

    finally:
        pool.stop()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s'
    )
    main()
