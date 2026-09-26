#!/usr/bin/env python3
"""
Integration tests for Phase 3.1: Multi-practice request routing
"""

import json
import pytest
import tempfile
import os
from task_service import TaskService, TaskRequest, TaskStatus, TaskDatabase


@pytest.fixture
def temp_db():
    """Create temporary database for testing"""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture
def service(temp_db):
    """Create task service with temporary database"""
    svc = TaskService(db_path=temp_db)
    return svc


@pytest.fixture
def client(service):
    """Flask test client"""
    return service.app.test_client()


class TestTaskSubmission:
    """Tests for POST /api/tasks/submit"""

    def test_submit_task_autonomy_practice(self, client):
        """Test submitting task from autonomy practice"""
        response = client.post("/api/tasks/submit", json={
            "requesting_practice": "empirica-foundation.carly.empirica-autonomy",
            "title": "Design state machine for gates",
            "description": "Full description of the task...",
            "priority": 2,
            "deadline": "2026-07-31T23:59:59Z",
            "context": {"key": "value"}
        })

        assert response.status_code == 202
        data = response.get_json()
        assert "task_id" in data
        assert data["status"] == "queued"
        assert "created_at" in data

    def test_submit_task_mesh_support_practice(self, client):
        """Test submitting task from mesh-support practice"""
        response = client.post("/api/tasks/submit", json={
            "requesting_practice": "empirica-foundation.carly.empirica-mesh-support",
            "title": "Infrastructure assessment",
            "description": "Evaluate current deployment...",
            "priority": 1
        })

        assert response.status_code == 202
        data = response.get_json()
        assert data["status"] == "queued"

    def test_submit_task_outreach_practice(self, client):
        """Test submitting task from outreach practice"""
        response = client.post("/api/tasks/submit", json={
            "requesting_practice": "empirica-foundation.carly.empirica-outreach",
            "title": "Community engagement strategy",
            "description": "Plan Q3 outreach initiatives...",
            "priority": 0
        })

        assert response.status_code == 202
        data = response.get_json()
        assert data["status"] == "queued"

    def test_submit_with_defaults(self, client):
        """Test task submission with default priority"""
        response = client.post("/api/tasks/submit", json={
            "requesting_practice": "empirica-foundation.carly.empirica-autonomy",
            "title": "Test task",
            "description": "Test description"
        })

        assert response.status_code == 202
        data = response.get_json()
        # Should use default priority=1 (normal)

    def test_invalid_practice(self, client):
        """Test rejection of invalid practice"""
        response = client.post("/api/tasks/submit", json={
            "requesting_practice": "invalid-practice",
            "title": "Test",
            "description": "Test"
        })

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_missing_required_fields(self, client):
        """Test rejection of missing required fields"""
        # Missing title
        response = client.post("/api/tasks/submit", json={
            "requesting_practice": "empirica-foundation.carly.empirica-autonomy",
            "description": "Test"
        })
        assert response.status_code == 400

        # Missing description
        response = client.post("/api/tasks/submit", json={
            "requesting_practice": "empirica-foundation.carly.empirica-autonomy",
            "title": "Test"
        })
        assert response.status_code == 400

    def test_invalid_priority(self, client):
        """Test rejection of invalid priority"""
        response = client.post("/api/tasks/submit", json={
            "requesting_practice": "empirica-foundation.carly.empirica-autonomy",
            "title": "Test",
            "description": "Test",
            "priority": 5
        })

        assert response.status_code == 400

    def test_empty_request_body(self, client):
        """Test rejection of empty request body"""
        response = client.post("/api/tasks/submit", data="", content_type="application/json")
        assert response.status_code == 400


class TestTaskStatusTracking:
    """Tests for GET /api/tasks/{task_id}"""

    def test_get_queued_task(self, client):
        """Test retrieving queued task"""
        # First submit a task
        submit_response = client.post("/api/tasks/submit", json={
            "requesting_practice": "empirica-foundation.carly.empirica-autonomy",
            "title": "Test task",
            "description": "Test description",
            "priority": 2
        })
        task_id = submit_response.get_json()["task_id"]

        # Retrieve the task
        get_response = client.get(f"/api/tasks/{task_id}")

        assert get_response.status_code == 200
        data = get_response.get_json()
        assert data["task_id"] == task_id
        assert data["status"] == "queued"
        assert data["requesting_practice"] == "empirica-foundation.carly.empirica-autonomy"
        assert data["title"] == "Test task"
        assert "created_at" in data

    def test_get_completed_task(self, service, client):
        """Test retrieving completed task with output"""
        # Submit task
        submit_response = client.post("/api/tasks/submit", json={
            "requesting_practice": "empirica-foundation.carly.empirica-autonomy",
            "title": "Test task",
            "description": "Test description"
        })
        task_id = submit_response.get_json()["task_id"]

        # Simulate completion
        output = {
            "understanding": "Analysis text (1000 chars)..." + "x" * 1000,
            "planning": "Plan text (500 chars)..." + "x" * 500,
            "execution": "Execution text (5000 chars)..." + "x" * 5000,
            "reflection": "Reflection text (2000 chars)..." + "x" * 2000
        }
        service.db.update_status(task_id, "completed", output=output, error_message=None)

        # Retrieve
        get_response = client.get(f"/api/tasks/{task_id}")

        assert get_response.status_code == 200
        data = get_response.get_json()
        assert data["status"] == "completed"
        assert "output" in data
        assert "total_reasoning_chars" in data
        assert data["total_reasoning_chars"] == sum(len(v) for v in output.values())

    def test_get_failed_task(self, service, client):
        """Test retrieving failed task with error message"""
        # Submit task
        submit_response = client.post("/api/tasks/submit", json={
            "requesting_practice": "empirica-foundation.carly.empirica-autonomy",
            "title": "Test task",
            "description": "Test description"
        })
        task_id = submit_response.get_json()["task_id"]

        # Simulate failure
        service.db.update_status(task_id, "failed", error_message="Model timeout after 300s")

        # Retrieve
        get_response = client.get(f"/api/tasks/{task_id}")

        assert get_response.status_code == 200
        data = get_response.get_json()
        assert data["status"] == "failed"
        assert "error_message" in data
        assert data["error_message"] == "Model timeout after 300s"

    def test_get_nonexistent_task(self, client):
        """Test retrieving non-existent task"""
        response = client.get("/api/tasks/task_nonexistent")
        assert response.status_code == 404


class TestRateLimiting:
    """Tests for rate limiting"""

    def test_rate_limit_100_per_minute(self, client):
        """Test that 101st request is rejected"""
        practice = "empirica-foundation.carly.empirica-autonomy"

        # Submit 100 requests (should succeed)
        for i in range(100):
            response = client.post("/api/tasks/submit", json={
                "requesting_practice": practice,
                "title": f"Task {i}",
                "description": "Test"
            })
            assert response.status_code == 202

        # 101st request should be rejected
        response = client.post("/api/tasks/submit", json={
            "requesting_practice": practice,
            "title": "Task 101",
            "description": "Test"
        })
        assert response.status_code == 429

    def test_rate_limit_per_practice(self, client):
        """Test that rate limit is per-practice, not global"""
        practice_a = "empirica-foundation.carly.empirica-autonomy"
        practice_b = "empirica-foundation.carly.empirica-mesh-support"

        # Submit 100 from practice A (succeed)
        for i in range(100):
            response = client.post("/api/tasks/submit", json={
                "requesting_practice": practice_a,
                "title": f"Task A{i}",
                "description": "Test"
            })
            assert response.status_code == 202

        # Practice A is now rate limited
        response = client.post("/api/tasks/submit", json={
            "requesting_practice": practice_a,
            "title": "Task A101",
            "description": "Test"
        })
        assert response.status_code == 429

        # But practice B should still have quota
        response = client.post("/api/tasks/submit", json={
            "requesting_practice": practice_b,
            "title": "Task B1",
            "description": "Test"
        })
        assert response.status_code == 202


class TestTaskPersistence:
    """Tests for task database persistence"""

    def test_task_persisted_to_database(self, service):
        """Test that task is persisted correctly"""
        req = TaskRequest(
            requesting_practice="empirica-foundation.carly.empirica-autonomy",
            title="Test task",
            description="Test description",
            priority=2,
            deadline="2026-07-31T23:59:59Z",
            context={"key": "value"}
        )
        req.validate()

        task = service.db.create_task(req)
        retrieved = service.db.get_task(task.id)

        assert retrieved is not None
        assert retrieved.id == task.id
        assert retrieved.title == "Test task"
        assert retrieved.priority == 2
        assert retrieved.status == "queued"

    def test_task_status_update(self, service):
        """Test updating task status"""
        req = TaskRequest(
            requesting_practice="empirica-foundation.carly.empirica-autonomy",
            title="Test",
            description="Test"
        )
        req.validate()

        task = service.db.create_task(req)

        # Update to processing
        service.db.update_status(task.id, "processing")
        retrieved = service.db.get_task(task.id)
        assert retrieved.status == "processing"

        # Update to completed
        output = {"result": "success"}
        service.db.update_status(task.id, "completed", output=output)
        retrieved = service.db.get_task(task.id)
        assert retrieved.status == "completed"
        assert retrieved.output == output

    def test_list_tasks_by_practice(self, service):
        """Test listing tasks for a specific practice"""
        practice_a = "empirica-foundation.carly.empirica-autonomy"
        practice_b = "empirica-foundation.carly.empirica-mesh-support"

        # Create tasks from practice A
        for i in range(3):
            req = TaskRequest(
                requesting_practice=practice_a,
                title=f"Task A{i}",
                description="Test"
            )
            req.validate()
            service.db.create_task(req)

        # Create tasks from practice B
        for i in range(2):
            req = TaskRequest(
                requesting_practice=practice_b,
                title=f"Task B{i}",
                description="Test"
            )
            req.validate()
            service.db.create_task(req)

        # List tasks from practice A
        tasks_a = service.db.list_tasks_by_practice(practice_a, limit=10)
        assert len(tasks_a) == 3
        assert all(t.requesting_practice == practice_a for t in tasks_a)

        # List tasks from practice B
        tasks_b = service.db.list_tasks_by_practice(practice_b, limit=10)
        assert len(tasks_b) == 2
        assert all(t.requesting_practice == practice_b for t in tasks_b)


class TestHealth:
    """Tests for health check endpoint"""

    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "healthy"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
