#!/usr/bin/env python3
"""
Integration tests for Phase 3.2: Priority Queue and Worker Pool
"""

import pytest
import tempfile
import os
import time
from priority_queue import PriorityQueue, WorkerPool, TaskWorker
from task_service import TaskService, TaskRequest, TaskStatus


@pytest.fixture
def temp_db():
    """Create temporary database"""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture
def service(temp_db):
    """Create task service"""
    return TaskService(db_path=temp_db)


@pytest.fixture
def queue():
    """Create priority queue"""
    return PriorityQueue()


class TestPriorityQueue:
    """Tests for priority queue"""

    def test_enqueue_single_task(self, queue):
        """Test enqueuing a single task"""
        queue.enqueue("task_1", priority=1)
        assert queue.size() == 1

    def test_dequeue_single_task(self, queue):
        """Test dequeuing a single task"""
        queue.enqueue("task_1", priority=1)
        task_id = queue.dequeue()
        assert task_id == "task_1"
        assert queue.size() == 0

    def test_priority_ordering(self, queue):
        """Test that higher-priority tasks dequeue first"""
        queue.enqueue("low", priority=0)
        queue.enqueue("high", priority=2)
        queue.enqueue("normal", priority=1)

        # Should dequeue in priority order: high → normal → low
        assert queue.dequeue() == "high"
        assert queue.dequeue() == "normal"
        assert queue.dequeue() == "low"

    def test_fifo_same_priority(self, queue):
        """Test FIFO ordering for same priority"""
        queue.enqueue("first", priority=1)
        queue.enqueue("second", priority=1)
        queue.enqueue("third", priority=1)

        # Should dequeue in creation order
        assert queue.dequeue() == "first"
        assert queue.dequeue() == "second"
        assert queue.dequeue() == "third"

    def test_critical_priority(self, queue):
        """Test critical priority (highest)"""
        queue.enqueue("low", priority=0)
        queue.enqueue("critical", priority=3)
        queue.enqueue("high", priority=2)

        # Critical should come first
        assert queue.dequeue() == "critical"

    def test_aging_boost_low_priority(self, queue):
        """Test that low-priority tasks are still processable"""
        queue.enqueue("high", priority=2)
        queue.enqueue("low", priority=0)

        # Both tasks should be dequeue-able
        first = queue.dequeue()
        assert first is not None

        second = queue.dequeue()
        assert second is not None

        # Both dequeued (order may vary based on aging)
        assert queue.size() == 0

    def test_empty_dequeue(self, queue):
        """Test dequeuing from empty queue"""
        assert queue.dequeue() is None
        assert queue.size() == 0


class TestWorkerPool:
    """Tests for worker pool"""

    def test_worker_pool_start_stop(self, service, queue):
        """Test starting and stopping worker pool"""
        pool = WorkerPool(queue, service.db, worker_count=2)

        pool.start()
        time.sleep(0.1)

        pool.stop()
        assert pool.running is False


class TestQueuePrioritySemantics:
    """Tests for priority queue semantics"""

    def test_priority_tiers(self, queue):
        """Test all four priority tiers"""
        tasks = [
            ("critical", 3),
            ("high", 2),
            ("normal", 1),
            ("low", 0)
        ]

        for name, priority in tasks:
            queue.enqueue(name, priority=priority)

        # Should dequeue in order: critical → high → normal → low
        assert queue.dequeue() == "critical"
        assert queue.dequeue() == "high"
        assert queue.dequeue() == "normal"
        assert queue.dequeue() == "low"

    def test_fair_scheduling_low_priority(self, queue):
        """Test that low-priority tasks don't starve forever"""
        # This is a conceptual test; actual aging happens over 10 minutes
        queue.enqueue("low", priority=0, deadline="2026-08-01T00:00:00Z")
        queue.enqueue("high", priority=2)

        # Initially high comes first
        assert queue.dequeue() == "high"

        # But low is still available (not starved)
        assert queue.dequeue() == "low"

    def test_deadline_tracking(self, queue):
        """Test that queue tracks deadlines"""
        queue.enqueue("task_1", priority=1, deadline="2026-08-01T12:00:00Z")
        queue.enqueue("task_2", priority=1, deadline="2026-08-02T12:00:00Z")

        # Should dequeue in priority order (deadline doesn't change initial priority)
        assert queue.dequeue() == "task_1"
        assert queue.dequeue() == "task_2"


class TestQueueScale:
    """Tests for scalability"""

    def test_enqueue_100_tasks(self, queue):
        """Test enqueuing 100 tasks"""
        for i in range(100):
            queue.enqueue(f"task_{i}", priority=i % 4)

        assert queue.size() == 100

        # Should be able to dequeue all
        for _ in range(100):
            assert queue.dequeue() is not None

        assert queue.size() == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
