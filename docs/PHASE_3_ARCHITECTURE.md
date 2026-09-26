# Phase 3 Architecture — Production-Scale Shared Agent Service

**Status:** Architecture specification v1.0  
**Date:** 2026-07-30  
**Scope:** Multi-practice request routing, prioritization, observability, scalability  

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Requesting Practices                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Autonomy   │  │ Mesh-Support │  │  Outreach    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└──────────────┬──────────────┬──────────────┬────────────────────┘
               │              │              │
               └──────────────┼──────────────┘
                              │
        ┌─────────────────────▼──────────────────────┐
        │    REST API (Request Handler)              │
        │  POST /api/tasks/submit                    │
        │  GET  /api/tasks/{task_id}                 │
        │  POST /api/tasks/batch (optional)          │
        └──────────────────────┬──────────────────────┘
                               │
        ┌──────────────────────▼──────────────────────┐
        │       Task Persistence Layer                │
        │    SQLite/PostgreSQL with indexing          │
        │    Status: queued|processing|completed      │
        └──────────────────────┬──────────────────────┘
                               │
        ┌──────────────────────▼──────────────────────┐
        │     Priority Queue Service                  │
        │  - Priority tiers (critical/high/normal)    │
        │  - Deadline-aware aging                     │
        │  - Fair scheduling (no starvation)          │
        └──────────────────────┬──────────────────────┘
                               │
        ┌──────────────────────▼──────────────────────┐
        │   Worker Pool (N concurrent workers)        │
        │  - Poll queue                               │
        │  - Execute Agent v3                         │
        │  - Store results + status                   │
        └──────────────────────┬──────────────────────┘
                               │
        ┌──────────────────────▼──────────────────────┐
        │         Agent Core (v3)                     │
        │  ReAct loop: Understanding → Planning →     │
        │  Execution → Reflection                     │
        │  Bifrost gateway + OpenRouter models        │
        └──────────────────────┬──────────────────────┘
                               │
        ┌──────────────────────▼──────────────────────┐
        │    Empirica Artifact Integration            │
        │  - Log findings (agent reasoning)           │
        │  - Log decisions (approach chosen)          │
        │  - Full transparency to requesting practice │
        └──────────────────────────────────────────────┘

        ┌──────────────────────────────────────────────┐
        │    Observability (Cross-cutting)            │
        │  - Prometheus metrics                       │
        │  - OpenTelemetry distributed tracing        │
        │  - Alerting rules (Slack webhooks)          │
        │  - Grafana dashboard                        │
        └──────────────────────────────────────────────┘
```

---

## Component Specifications

### 1. REST API & Request Handler

**Endpoint: `POST /api/tasks/submit`**

Request body:
```json
{
  "requesting_practice": "empirica-foundation.carly.empirica-autonomy",
  "title": "Design state machine for gates feature A.0.1",
  "description": "Full task description here...",
  "priority": 2,
  "deadline": "2026-07-31T23:59:59Z",
  "context": {
    "existing_patterns": ["state machine in routes"],
    "constraints": ["must integrate with existing auth"]
  }
}
```

Response:
```json
{
  "task_id": "task_abc123def456",
  "status": "queued",
  "created_at": "2026-07-30T18:00:00Z",
  "estimated_wait_time_seconds": 45
}
```

**Endpoint: `GET /api/tasks/{task_id}`**

Response (in-progress):
```json
{
  "task_id": "task_abc123def456",
  "status": "processing",
  "requesting_practice": "empirica-foundation.carly.empirica-autonomy",
  "title": "Design state machine for gates feature A.0.1",
  "started_at": "2026-07-30T18:01:30Z",
  "progress": "executing_phase_3_of_4"
}
```

Response (completed):
```json
{
  "task_id": "task_abc123def456",
  "status": "completed",
  "requesting_practice": "empirica-foundation.carly.empirica-autonomy",
  "title": "Design state machine for gates feature A.0.1",
  "created_at": "2026-07-30T18:00:00Z",
  "started_at": "2026-07-30T18:01:30Z",
  "completed_at": "2026-07-30T18:08:45Z",
  "output": {
    "understanding": "1756 chars...",
    "planning": "574 chars...",
    "execution": "7420 chars...",
    "reflection": "4704 chars..."
  },
  "artifacts_logged": 5,
  "total_reasoning_chars": 14454
}
```

**Error responses:**
- 400: Malformed request (missing fields, invalid practice ID)
- 429: Rate limit exceeded (max 100 requests/minute per practice)
- 503: Service overloaded (queue depth > 2000)

---

### 2. Task Persistence Layer

**Database schema:**

```sql
CREATE TABLE tasks (
  id TEXT PRIMARY KEY,
  requesting_practice TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  priority INTEGER NOT NULL,  -- 0-3
  deadline TIMESTAMP,
  context JSONB,
  status TEXT NOT NULL,  -- queued|processing|completed|failed
  created_at TIMESTAMP NOT NULL,
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  output JSONB,
  error_message TEXT,
  artifacts_logged INTEGER DEFAULT 0,
  INDEX (requesting_practice, created_at),
  INDEX (status, priority, deadline),
  INDEX (created_at DESC)
);

CREATE TABLE task_events (
  id TEXT PRIMARY KEY,
  task_id TEXT NOT NULL,
  event_type TEXT NOT NULL,  -- submitted|started|completed|failed
  timestamp TIMESTAMP NOT NULL,
  metadata JSONB,
  FOREIGN KEY (task_id) REFERENCES tasks(id),
  INDEX (task_id, timestamp)
);
```

---

### 3. Priority Queue Service

**Priority semantics:**

| Priority | Tier | Base Weight | Aging Boost |
|----------|------|-------------|-------------|
| 3 | Critical | 1000 | +100/min |
| 2 | High | 100 | +10/min |
| 1 | Normal | 10 | +1/min |
| 0 | Low | 1 | +0.1/min |

**Algorithm:**
```
effective_priority = base_weight + (age_minutes * aging_boost)
```

**Fair scheduling rule:**
- Task with lowest priority tier cannot be starved for > 10 minutes
- After 10 minutes, boost low-priority task to effective priority of critical

**Implementation:** Python `heapq` with thread-safe wrapper
- Enqueue: O(log n)
- Dequeue: O(log n)
- Deadline tracking: separate min-heap for deadline-based preemption

---

### 4. Background Worker Pool

**Worker lifecycle:**

1. Start: N workers (default 3, configurable)
2. Poll: Query queue, acquire task (atomic)
3. Execute: Run agent v3 on task, handle errors
4. Store: Save output + status to database
5. Notify: Optional webhook callback to requesting practice
6. Repeat

**Concurrency model:**
- Thread pool with `concurrent.futures.ThreadPoolExecutor`
- Shared queue protected by `threading.Lock`
- Database connection pooling (SQLAlchemy)

**Error handling:**
- Model timeout: retry up to 3 times with backoff
- Database error: mark task as failed, log to observability
- Agent crash: capture stack trace, log to observability, mark failed

**Graceful shutdown:**
- Signal handler on SIGTERM
- Wait for current tasks to complete (timeout: 30s)
- Drain queue (no new tasks accepted)
- Close database connections

---

### 5. Observability Stack

**Prometheus metrics:**

```
# Counters
requests_total{practice="autonomy",status="success"}
requests_total{practice="autonomy",status="error"}

# Gauges
queue_depth{worker_id="worker_1"}
active_workers

# Histograms
task_latency_seconds{quantile="0.5"}
task_latency_seconds{quantile="0.95"}
task_latency_seconds{quantile="0.99"}

# Rates
error_rate (derived from errors_total / requests_total)
completion_rate (derived from completed_tasks_total / requests_total)
```

**OpenTelemetry tracing:**

Instrument spans:
- `http.request.submit` → Request handler
- `queue.enqueue` → Task queued
- `queue.dequeue` → Task acquired by worker
- `agent.execute` → Agent v3 execution
  - `agent.phase.understanding`
  - `agent.phase.planning`
  - `agent.phase.execution`
  - `agent.phase.reflection`
- `db.insert` → Result storage

**Alerting rules:**

```promql
# Error rate alert
(errors_total / requests_total) > 0.05 for 5m

# Queue depth alert
queue_depth > 1000 for 1m

# Task latency alert
histogram_quantile(0.99, task_latency_seconds) > 300 for 5m

# Worker down alert
up{job="agent_workers"} == 0 for 2m
```

**Grafana dashboard:**
- Queue depth (time series, refresh 10s)
- Requests/second (time series)
- Error rate (time series, threshold line at 5%)
- Latency percentiles (p50/p95/p99, stacked area)
- Practice breakdown (pie chart: autonomy/mesh-support/outreach)
- Worker status (gauge: 3/3 healthy)

---

### 6. Scalability Tuning

**Bottleneck mitigation:**

| Bottleneck | Detection | Solution |
|------------|-----------|----------|
| Queue contention | Lock wait time > 100ms | Use lock-free queue (atomic operations) |
| Database I/O | INSERT latency > 500ms | Connection pooling (size 20) + async writes |
| Model latency | p99 > 300s | Cache responses (1h TTL), prioritize cached hits |
| Memory | Resident set > 500MB | Streaming responses, batch cleanup |
| CPU | Utilization > 80% | Scale horizontally (more workers/instances) |

**Optimizations:**

1. **Database:** Connection pooling (SQLAlchemy), async writes to write-ahead log
2. **Caching:** Redis or in-memory LRU (task_hash → result) with 1h TTL
3. **Batching:** POST /api/tasks/batch endpoint (accept up to 100 tasks in one call)
4. **Async model:** Bifrost model calls return fast (streaming support), non-blocking queue polling

**Stress test target:**
- 500 concurrent requests
- Mixed priorities (30% critical, 40% high, 30% normal)
- 3 worker pool
- Measure:
  - p50 latency < 60s
  - p95 latency < 120s
  - p99 latency < 180s
  - Queue depth stays < 100

---

## Implementation Order

### Phase 3.1: Multi-practice request routing
1. Design request schema
2. Implement REST API (POST /submit, GET /{task_id})
3. Implement task persistence (database schema + ORM)
4. Write integration tests
5. **Commit:** `feat(api): multi-practice request handler`

### Phase 3.2: Task prioritization & queue management
6. Design priority queue semantics
7. Implement PriorityQueue class (thread-safe)
8. Implement background worker loop
9. Implement worker pool (concurrent.futures)
10. Load test (100 concurrent)
11. **Commit:** `feat(queue): priority queue + worker pool`

### Phase 3.3: Production observability
12. Instrument Prometheus metrics
13. Instrument OpenTelemetry tracing
14. Configure alerting rules
15. Create Grafana dashboard
16. Write observability tests
17. **Commit:** `feat(observability): metrics + tracing + alerts`

### Phase 3.4: Scalability tuning
18. Profile bottlenecks (100 concurrent load test)
19. Implement connection pooling
20. Implement result caching
21. Implement batch request handler
22. Stress test (500 concurrent)
23. **Commit:** `feat(scale): optimizations for 500+ concurrent`

---

## Production Readiness Checklist

- [ ] All 4 components (routing, queue, observability, scalability) deployed
- [ ] Integration test suite passes (100% coverage of happy path)
- [ ] Load test passes (100 concurrent, p99 < 120s)
- [ ] Stress test passes (500 concurrent, queue depth < 100)
- [ ] Alerting validated (test alerts fire correctly)
- [ ] Runbook written (how to scale, troubleshoot, deploy)
- [ ] Documentation complete (API spec, architecture, operations)
- [ ] Three practices (autonomy, mesh-support, outreach) onboarded
- [ ] Monitoring dashboard live and tracking metrics
- [ ] Graceful degradation verified (queue full → 503, worker down → alert)

---

## Configuration

**Environment variables:**

```bash
# Queue configuration
QUEUE_WORKER_COUNT=3
QUEUE_MAX_DEPTH=2000
QUEUE_POLLING_INTERVAL_MS=500

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/agent_service
DB_POOL_SIZE=20
DB_POOL_RECYCLE=300

# Caching (optional)
CACHE_TYPE=redis
CACHE_REDIS_URL=redis://localhost:6379
CACHE_TTL_SECONDS=3600

# Observability
PROMETHEUS_PORT=9090
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...

# Rate limiting
RATE_LIMIT_PER_PRACTICE=100/minute

# Model configuration
BIFROST_URL=http://localhost:8080
OPENROUTER_API_KEY=sk-or-v1-...
```

---

## Next Steps

1. Implement Phase 3.1 (request routing)
2. Implement Phase 3.2 (queue + workers)
3. Implement Phase 3.3 (observability)
4. Implement Phase 3.4 (scalability)
5. Run integration + load + stress tests
6. Deploy to staging
7. Onboard three practices
8. Monitor production metrics
9. Iterate based on real-world load

