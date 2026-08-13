# Capacity Planning Guide — HumanAIOS ACAT Assessment API

Production capacity limits, deployment sizing, and scaling guidelines.

## System Capacity

### Current Configuration (After Connection Pool Fix)

| Setting | Value | Notes |
|---------|-------|-------|
| **DB Connection Pool** | 40 connections | Supports 100+ concurrent users |
| **Assessment Timeout** | 30 minutes | Per-job execution window |
| **Job Recovery** | Automatic on startup | Incomplete jobs re-queued |
| **DB Persistence** | PostgreSQL | All job state durable |

---

## Capacity Limits

### Concurrent Users

| Level | Concurrent Users | Avg Latency | P99 Latency | Error Rate | Status |
|-------|------------------|-------------|------------|-----------|--------|
| **Baseline** | 1 | 1.25s | 4.1s | 0.0% | ✅ Optimal |
| **Light** | 10 | 1.42s | 4.5s | 0.0% | ✅ Good |
| **Moderate** | 50 | 1.68s | 4.9s | 0.3% | ✅ Good |
| **Heavy** | 100 | 2.45s | 7.8s | 0.5%* | ✅ Acceptable |
| **Max** | 150+ | Degraded | TBD | TBD | ⚠️ Untested |

*Error rate after connection pool fix (40 connections)

### Throughput

| Metric | Value | Constraint |
|--------|-------|-----------|
| **Max Assessments/min** | 53 | Limited by ACAT execution time (30 min) |
| **Max Submissions/sec** | ~9 | API layer (load testing shows 8-9 req/s at 100 users) |
| **Max Job Queue Depth** | 100+ | With 40 connection pool |

**Limiting Factor:** ACAT protocol execution (~30 minutes per assessment) is the bottleneck, not the API layer.

---

## Deployment Sizing

### Single Instance (Development/Testing)

- **Concurrency:** Up to 50 users
- **Throughput:** ~30 assessments/min
- **Resources:** 2 CPU, 4GB RAM, 20GB disk
- **Database:** Shared or local PostgreSQL
- **Use Case:** Development, staging, small pilot

**Configuration:**
```env
DATABASE_POOL_MAX=40
DATABASE_URL=postgresql://user:pass@localhost:5432/humanaios
REDIS_URL=redis://localhost:6379
```

---

### High-Availability Deployment (Production)

**Recommended Architecture:** 2-3 API instances + shared database

#### Instance Configuration

| Component | Spec | Notes |
|-----------|------|-------|
| **API Instances** | 3x | For failover + rolling updates |
| **Each Instance** | 4 CPU, 8GB RAM | Supports ~40 concurrent users per instance |
| **Load Balancer** | Round-robin or least-conn | Distributes traffic evenly |
| **Database** | PostgreSQL HA (2+ replicas) | Replication for durability |
| **Cache** | Redis cluster (3 nodes) | For session state |

#### Capacity

- **Total Concurrency:** 100+ users (40 per instance × 3)
- **Total Throughput:** ~50 assessments/min across fleet
- **Failover Time:** < 5 seconds (health check interval)
- **Recovery Time:** < 30 seconds (job recovery on restart)

#### Configuration

```env
# Environment variables for each instance
DATABASE_POOL_MAX=40
DATABASE_URL=postgresql://user:pass@db-primary:5432/humanaios
REDIS_URL=redis://redis-cluster:6379

# Load balancer configuration
UPSTREAM api {
  server api-1:3000 max_fails=3 fail_timeout=30s;
  server api-2:3000 max_fails=3 fail_timeout=30s;
  server api-3:3000 max_fails=3 fail_timeout=30s;
}
```

---

## Scaling Strategy

### Horizontal Scaling (Add Instances)

**When to scale out:**
- Concurrent users exceed 40 per instance
- P99 latency approaches 10 seconds
- Error rate exceeds 1%

**How to scale:**
1. Launch new API instance with same config
2. Add to load balancer upstream pool
3. Load balancer automatically routes new traffic
4. Old instances continue serving existing connections
5. Monitor recovery: "Recovering N jobs" in logs

**Rolling Update Procedure:**
```bash
# For each instance (one at a time):
1. Mark unhealthy in load balancer
2. Wait for connections to drain (~2 min)
3. Stop instance (jobs persist in DB)
4. Deploy new version
5. Start instance
6. Monitor: Jobs auto-recovered from DB
7. Mark healthy in load balancer
8. Repeat for next instance
```

### Vertical Scaling (Larger Instances)

**When to scale up:**
- Single instance approaching 40 CPU usage
- High memory usage (approaching 8GB)
- Database query latency > 100ms

**How to scale:**
1. Launch new instance with larger spec (8 CPU, 16GB)
2. Migrate traffic from old instance (rolling update)
3. Terminate old instance once drained

---

## Bottleneck Analysis

### Primary Bottleneck: ACAT Protocol Execution

- **Duration:** ~30 minutes per assessment
- **Impact:** Limits throughput to 53 assessments/min
- **Mitigation:** Parallelize assessment execution (requires architecture change)
- **Status:** Already optimized in Task 2, further optimization is complex

### Secondary Bottleneck: Database Connections

- **Current:** 40 connections per instance
- **At 100 users:** ~33% utilization (plenty of headroom)
- **At 200 users:** ~65% utilization (still acceptable)
- **At 300 users:** Would exceed pool, increase to 60-80

### Tertiary Bottleneck: Network I/O

- **Assessment Polling:** Clients poll GET /assessments/:id every 2 seconds
- **At 100 users:** ~50 poll requests/sec
- **Optimization:** Implement server-sent events (SSE) instead of polling
- **Impact:** Would reduce query load by 80%

---

## Monitoring & Alerting

### Key Metrics to Monitor

```
# Database Connection Pool
- pg_connection_pool_utilization: Current / Max connections
- pg_connection_pool_waiting: Queued connection requests
- pg_slow_queries: Queries taking > 100ms

# Assessment Job Queue
- assessment_jobs_queued: Jobs waiting to execute
- assessment_jobs_running: Jobs currently executing
- assessment_jobs_failed: Failed assessments (error rate)

# API Performance
- api_request_latency_p50, p95, p99: Response times
- api_error_rate: Percentage of failed requests
- api_timeout_errors: Jobs exceeding 30-min timeout

# System Resources
- api_cpu_usage: CPU utilization per instance
- api_memory_usage: Memory usage per instance
- api_disk_usage: Disk space (job results, logs)
```

### Alerting Rules

```
# Critical (page on-call)
- Database connection pool at 80%+ utilization
- Error rate > 5%
- P99 latency > 30 seconds
- Jobs failed > 10% (cascading failures)

# Warning (log and monitor)
- Database connection pool at 60%+ utilization
- Error rate > 1%
- P99 latency > 15 seconds
- Job queue depth > 50 (backlog growing)
- Job timeout errors > 3 in 5 min window
```

### Dashboards

Recommended Prometheus + Grafana setup:

```
Database:
  - Connection pool utilization (gauge)
  - Query latency distribution (heatmap)
  - Slow query log (table)

Jobs:
  - Queue depth over time (line chart)
  - Success/failure rate (stacked bar)
  - Execution time distribution (histogram)

API:
  - Request latency P50/P95/P99 (line chart)
  - Error rate (line chart)
  - Throughput (requests/sec)

Infrastructure:
  - CPU usage per instance (stacked bar)
  - Memory usage per instance (stacked bar)
  - Disk usage (gauge)
```

---

## Disaster Recovery

### Failure Scenarios

#### Scenario 1: Single API Instance Fails

**What happens:**
1. Load balancer detects health check failure
2. Stops routing traffic to failed instance (< 30s)
3. Traffic redistributed to healthy instances
4. Failed instance: jobs remain in DB

**Recovery:**
1. Restart instance (manual or auto-restart)
2. AssessmentsService calls `recoverJobsOnStartup()`
3. Incomplete jobs re-queued and resume
4. No data loss, no duplicate executions

**Time to recovery:** ~2 minutes (instance restart + recovery)

#### Scenario 2: Database Connection Pool Exhaustion

**What happens:**
1. All connections in use, new requests queue
2. Queued requests timeout after 2 seconds
3. Error rate spikes to 5%+
4. Clients see 503 Service Unavailable

**Prevention:**
1. Monitor connection pool utilization (current: 40 max)
2. Alert when > 60% (24 connections in use)
3. Scale horizontally or increase pool size

**Recovery (immediate):**
1. Kill long-running connections: `SELECT pg_terminate_backend(...)`
2. Restart affected API instances
3. Jobs auto-recover from DB

#### Scenario 3: Database Crashes

**What happens:**
1. All API instances lose database connection
2. No new jobs can be submitted (201 errors)
3. Job status checks fail (500 errors)
4. Jobs not lost (persisted to DB)

**Prevention:**
1. Use PostgreSQL HA (streaming replication)
2. Automated failover to replica
3. Recovery time: < 30 seconds

**Manual recovery:**
1. Restore from latest backup
2. Replay transaction log to recover in-flight jobs
3. Restart API instances
4. Jobs auto-recover

---

## Cost Estimation

### AWS Example (Production 3-Instance HA Setup)

| Component | Spec | Cost/month |
|-----------|------|-----------|
| **EC2 Instances** | 3x t3.large (4 CPU, 8GB) | $270 |
| **RDS PostgreSQL** | Multi-AZ, 100GB | $180 |
| **ElastiCache Redis** | 3-node cluster | $60 |
| **Load Balancer** | ALB | $40 |
| **Data Transfer** | Estimate 100GB/month | $25 |
| **Backups** | Automated snapshots | $20 |
| **Total** | | **~$595/month** |

**Scaling costs:**
- Add 1 API instance: +$90/month
- Increase DB storage 100GB: +$18/month
- 10x scaling (3→30 instances): +$2,700/month

---

## Capacity Planning Checklist

Before production deployment, verify:

- [ ] Database connection pool: 40+ connections
- [ ] Load balancer configured (health checks, routing)
- [ ] Auto-restart enabled on API instances
- [ ] Database HA/replication configured
- [ ] Backups automated (daily snapshots)
- [ ] Monitoring/alerting set up (Prometheus + Grafana)
- [ ] Log aggregation (ELK or CloudWatch)
- [ ] On-call rotation established
- [ ] Runbook documented (see OPERATIONS_RUNBOOK.md)
- [ ] Disaster recovery tested (failover drills)

---

## References

- Task 7.3 Results: `SAMPLE_RESULTS_SCALING.md`
- Operations Runbook: `OPERATIONS_RUNBOOK.md`
- Load Testing: `README.md`
- Durability Testing: `DURABILITY_TEST_GUIDE.md`
