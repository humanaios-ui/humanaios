# Operations Runbook — HumanAIOS ACAT Assessment API

Production deployment, monitoring, troubleshooting, and scaling guide.

## Table of Contents

1. [Deployment](#deployment)
2. [Monitoring](#monitoring)
3. [Troubleshooting](#troubleshooting)
4. [Scaling](#scaling)
5. [Maintenance](#maintenance)
6. [Incident Response](#incident-response)

---

## Deployment

### Prerequisites

- PostgreSQL 12+ with HA setup (primary + replica)
- Redis cluster (3+ nodes)
- 3x API instances (t3.large or equivalent: 4 CPU, 8GB RAM)
- Load balancer (ALB, nginx, HAProxy, or equivalent)
- Monitoring stack (Prometheus + Grafana, CloudWatch, or equivalent)

### Initial Deployment

#### 1. Database Setup

```bash
# Create database
createdb humanaios -U postgres

# Run migrations
cd apps/api
npm run migration:run

# Verify tables created
psql $DATABASE_URL -c "\dt"

# Check assessment_jobs table exists
psql $DATABASE_URL -c "\d assessment_jobs"
```

#### 2. Configure Connection Pool

Update `database.module.ts`:
```typescript
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 40,  // Connection pool size (adjust based on load)
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

#### 3. Environment Variables

Create `.env.production`:
```env
NODE_ENV=production
PORT=3000
LOG_LEVEL=info

# Database
DATABASE_URL=postgresql://user:pass@db-primary:5432/humanaios

# Redis
REDIS_URL=redis://redis-cluster:6379

# Assessment config
ASSESSMENT_TIMEOUT_MS=1800000  # 30 minutes
ASSESSMENT_PHASE_COUNT=3

# Monitoring
METRICS_PORT=9090
```

#### 4. Deploy to Instances

```bash
# On each instance:
1. Clone repository
2. Install dependencies: npm install
3. Build: npm run build
4. Set environment variables
5. Start service: npm run start

# Verify startup
curl http://localhost:3000/health

# Watch logs
tail -f logs/assessment-api.log | grep -E "started|Recovering"
```

#### 5. Configure Load Balancer

**Nginx example:**
```nginx
upstream api_backend {
  least_conn;  # Load balancing algorithm
  server api-1:3000 max_fails=3 fail_timeout=30s;
  server api-2:3000 max_fails=3 fail_timeout=30s;
  server api-3:3000 max_fails=3 fail_timeout=30s;
}

server {
  listen 80;
  server_name api.humanaios.ai;

  location / {
    proxy_pass http://api_backend;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_connect_timeout 5s;
    proxy_read_timeout 35s;  # Slightly > 30s job timeout
    proxy_send_timeout 5s;
  }

  location /health {
    access_log off;
    proxy_pass http://api_backend;
  }
}
```

#### 6. Setup Monitoring

```bash
# Install Prometheus Node Exporter on each instance
wget https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz
tar xvfz node_exporter-1.3.1.linux-amd64.tar.gz
./node_exporter-1.3.1.linux-amd64/node_exporter --web.listen-address=:9100 &

# Add to Prometheus scrape config
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'api-instances'
    static_configs:
      - targets: ['api-1:9090', 'api-2:9090', 'api-3:9090']
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['api-1:9100', 'api-2:9100', 'api-3:9100']
```

---

## Monitoring

### Essential Metrics

#### Database Connection Pool

```sql
-- Check current connection usage
SELECT count(*) as total_connections FROM pg_stat_activity;
SELECT usename, count(*) FROM pg_stat_activity GROUP BY usename;

-- Monitor pool utilization
SELECT (SELECT count(*) FROM pg_stat_activity) / 40.0 as pool_utilization;
```

**Alert:** Utilization > 80% (32+ connections)

#### Assessment Job Queue

```sql
-- Queue depth
SELECT status, COUNT(*) FROM assessment_jobs 
WHERE created_at > NOW() - INTERVAL '1 hour'
GROUP BY status;

-- Error rate (last hour)
SELECT 
  (SELECT COUNT(*) FROM assessment_jobs 
   WHERE status = 'failed' AND created_at > NOW() - INTERVAL '1 hour') 
  / NULLIF(COUNT(*), 0) * 100 as error_rate_percent
FROM assessment_jobs
WHERE created_at > NOW() - INTERVAL '1 hour';

-- Job age (how long queued)
SELECT 
  status,
  MIN(created_at) as oldest,
  MAX(created_at) as newest,
  COUNT(*) as count
FROM assessment_jobs
WHERE status IN ('queued', 'running')
GROUP BY status;
```

**Alert:** Error rate > 1%, Queue depth > 50

#### API Performance

```bash
# From logs (grep for metrics)
tail -f logs/assessment-api.log | grep -E "latency|error"

# Example log format
[2026-08-08 14:30:45] POST /api/v1/assessments - latency: 85ms, status: 201
[2026-08-08 14:30:46] GET /api/v1/assessments/:id - latency: 52ms, status: 200
```

**Alert:** P99 latency > 15 seconds, Error rate > 1%

### Dashboard Queries (Prometheus)

```
# Connection pool utilization
rate(pg_connections_used[5m]) / 40

# Assessment error rate
rate(assessment_jobs_failed[5m]) / rate(assessment_jobs_total[5m])

# API request latency P99
histogram_quantile(0.99, rate(api_request_duration_seconds_bucket[5m]))

# Job queue depth
assessment_jobs_queued
```

---

## Troubleshooting

### Issue: High Error Rate (5%+)

**Symptom:** Spike in 500/503 errors

**Investigation:**
```bash
# Check API logs
tail -100 logs/assessment-api.log | grep -i error

# Check database connectivity
psql $DATABASE_URL -c "SELECT 1"

# Check connection pool
psql $DATABASE_URL -c "SELECT count(*) FROM pg_stat_activity"

# Check Redis
redis-cli PING
```

**Likely Causes:**
1. Database connection pool exhausted → Check pool utilization
2. Database unreachable → Check connectivity, restart replica
3. Redis connection issues → Restart Redis
4. High load → Scale horizontally (add instances)

**Resolution:**
```bash
# Restart affected instance
sudo systemctl restart humanaios-api

# Watch recovery logs
tail -f logs/assessment-api.log | grep "Recovering"
```

### Issue: Slow Response Times (P99 > 15s)

**Symptom:** API responses taking 15+ seconds

**Investigation:**
```bash
# Check slow queries (PostgreSQL)
psql $DATABASE_URL -c "
SELECT query, mean_time, calls
FROM pg_stat_statements
WHERE mean_time > 100
ORDER BY mean_time DESC
LIMIT 10;"

# Check CPU/memory on instances
top -b -n 1 | head -20

# Check job execution times
psql $DATABASE_URL -c "
SELECT 
  COUNT(*) as jobs,
  EXTRACT(EPOCH FROM (MAX(completed_at) - MIN(started_at))) as total_time_sec
FROM assessment_jobs
WHERE status = 'completed'
  AND completed_at > NOW() - INTERVAL '1 hour';"
```

**Likely Causes:**
1. Slow ACAT protocol execution (expected, takes ~30 min per job)
2. Database query slow → Check slow query log
3. High concurrent load → Scale horizontally
4. Memory pressure → Increase instance size

**Resolution:**
```bash
# Scale horizontally (add instance)
# Or increase instance size and rolling-restart
```

### Issue: Jobs Stuck in "queued" or "running"

**Symptom:** Jobs never complete (stuck for > 35 min)

**Investigation:**
```sql
-- Check stuck jobs
SELECT job_id, assessment_id, status, created_at, started_at
FROM assessment_jobs
WHERE status IN ('queued', 'running')
  AND created_at < NOW() - INTERVAL '35 minutes'
ORDER BY created_at ASC;

-- Check if assessment has result
SELECT a.id, a.status, a.result_summary
FROM assessments a
LEFT JOIN assessment_jobs j ON a.id = j.assessment_id
WHERE j.status IN ('queued', 'running')
  AND j.created_at < NOW() - INTERVAL '35 minutes'
ORDER BY a.created_at ASC;
```

**Likely Causes:**
1. API instance crashed mid-execution → Recovery failed
2. ACAT protocol hung → Timeout should have fired (30 min)
3. Database error → Check error_message column

**Resolution:**
```bash
# Check if timeout was enforced
SELECT error_message FROM assessment_jobs
WHERE status = 'failed'
  AND error_message LIKE '%timeout%'
ORDER BY updated_at DESC
LIMIT 10;

# If not timed out, manually mark as failed
UPDATE assessment_jobs
SET status = 'failed', 
    error_message = 'Manual intervention: job exceeded 35 min',
    completed_at = NOW()
WHERE job_id = '<job_id>';

# Update assessment
UPDATE assessments
SET status = 'failed'
WHERE id = '<assessment_id>';
```

### Issue: Database Connection Pool Exhausted

**Symptom:** 
- `Error: connect timeout`
- Queue of pending connections
- New requests fail immediately

**Investigation:**
```bash
# Check pool utilization
psql $DATABASE_URL -c "
SELECT 
  count(*) as active_connections,
  40 as pool_max,
  count(*) / 40.0 * 100 as utilization_percent
FROM pg_stat_activity;"

# Which queries are hogging connections?
psql $DATABASE_URL -c "
SELECT 
  usename, state, COUNT(*) as connection_count, 
  MIN(query_start) as oldest_query_start
FROM pg_stat_activity
GROUP BY usename, state
ORDER BY connection_count DESC;"
```

**Resolution:**

Option 1: Kill long-running connections
```bash
psql $DATABASE_URL -c "
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
  AND query_start < NOW() - INTERVAL '5 minutes';"
```

Option 2: Increase pool size
```typescript
// database.module.ts
max: 60,  // Increase from 40 to 60
```

Option 3: Scale API instances (more instances = more requests spread across more pools)

---

## Scaling

### Horizontal Scaling (Add Instance)

**Trigger:** Utilization > 60% (24 of 40 connections)

**Steps:**
```bash
# 1. Launch new instance with production config
#    (same database.module.ts, environment variables)

# 2. Wait for startup
sleep 10
curl http://new-api-instance:3000/health

# 3. Watch recovery logs (should show "Recovering N jobs")
ssh new-api-instance
tail -f logs/assessment-api.log

# 4. Add to load balancer
#    Update nginx upstream config or ALB target group

# 5. Verify traffic is routing
curl http://load-balancer/health  # Should succeed
```

### Vertical Scaling (Larger Instance)

**Trigger:** CPU sustained > 70% or Memory > 80%

**Steps:**
```bash
# 1. Create new larger instance (e.g., t3.xlarge: 4 CPU, 16GB)
# 2. Deploy code to new instance
# 3. Add to load balancer
# 4. Remove old instance from load balancer
# 5. Wait for connections to drain (~2 min)
# 6. Terminate old instance
```

### Connection Pool Scaling

**Current:** 40 connections
**For 100 users:** ~33% utilization (OK)
**For 200 users:** ~66% utilization (increase to 60)
**For 300+ users:** Increase to 80-100

```typescript
// database.module.ts
max: 60,  // Adjust based on expected load
```

---

## Maintenance

### Database Backups

```bash
# Manual backup
pg_dump $DATABASE_URL > humanaios_backup_$(date +%Y%m%d_%H%M%S).sql

# Restore from backup
psql $DATABASE_URL < humanaios_backup_20260808_143000.sql

# Automated backups (recommended)
# Configure in RDS/managed PostgreSQL: daily snapshots
```

### Log Rotation

```bash
# Setup logrotate for API logs
cat > /etc/logrotate.d/humanaios-api << EOF
/var/log/humanaios-api/*.log {
  daily
  rotate 7
  compress
  delaycompress
  notifempty
  create 0640 humanaios humanaios
  postrotate
    systemctl reload humanaios-api > /dev/null 2>&1 || true
  endscript
}
EOF
```

### Connection Pool Health Check

```bash
# Monthly: verify pool is healthy
psql $DATABASE_URL -c "
-- Should return 40 (pool max)
SHOW max_connections;

-- Should return < 40 (pool not exhausted)
SELECT count(*) FROM pg_stat_activity;

-- Should return > 0 (pool is being used)
SELECT count(*) FROM assessment_jobs WHERE status IN ('queued', 'running');
"
```

---

## Incident Response

### Incident Severity Classification

| Severity | Error Rate | P99 Latency | Response Time |
|----------|-----------|------------|----------------|
| **P1 Critical** | > 10% | N/A | Immediate (page on-call) |
| **P2 High** | 5-10% | > 30s | 5 minutes |
| **P3 Medium** | 1-5% | > 15s | 15 minutes |
| **P4 Low** | < 1% | < 15s | Next business day |

### P1 Incident: Complete Outage (All Instances Down)

**Detection:** No instances respond to health checks

**Response (On-Call):**
```
1. [0-2 min] Page on-call team
2. [2-5 min] Check API instance status
   - SSH to instance
   - systemctl status humanaios-api
   - tail -100 logs/assessment-api.log
3. [5-10 min] Determine root cause
   - Check database connectivity
   - Check Redis connectivity
   - Check disk space
   - Check memory/CPU
4. [10-15 min] Apply fix
   - Restart instances if hung
   - Restore database from backup if corrupted
   - Increase resources if maxed out
5. [15-20 min] Verify recovery
   - curl http://localhost:3000/health
   - Monitor error rate (should drop to < 1%)
   - Watch recovery logs
6. [20+ min] Post-incident review
   - Document what happened
   - Update runbook if needed
   - Notify stakeholders
```

### P2 Incident: High Error Rate (5%+)

**Detection:** Monitoring alert triggered

**Response (Escalation):**
```
1. [0-1 min] Acknowledge alert
2. [1-5 min] Investigate root cause
   - Check connection pool utilization
   - Check database slow query log
   - Check instance resources (CPU/memory)
   - Check job queue depth
3. [5-10 min] Apply immediate fix
   - Scale horizontally (add instance)
   - Or kill stuck connections
   - Or restart affected instance
4. [10-15 min] Verify
   - Error rate should drop
   - P99 latency should improve
5. [15+ min] Long-term fix
   - Increase pool size?
   - Add caching?
   - Optimize query?
```

### P3 Incident: Elevated Latency (P99 > 15s)

**Detection:** Monitoring alert or customer report

**Response (Monitoring):**
```
1. [0-5 min] Confirm issue
   - Run load test to reproduce
   - Check if issue is consistent
2. [5-15 min] Investigate
   - Check slow query log
   - Profile ACAT protocol
   - Check resource utilization
3. [15-30 min] Apply fix
   - Scale instance size
   - Optimize database queries
   - Add caching
4. [30+ min] Validate
   - Rerun load test
   - Verify P99 latency improved
```

---

## Contact Information

**On-Call Rotation:**
- Primary: [team lead]
- Secondary: [senior engineer]
- Manager: [engineering manager]

**Escalation Path:**
- Unresolved P1 > 30 min: Escalate to VP Engineering
- Unresolved P2 > 1 hour: Escalate to Engineering Manager
- Unresolved P3 > 4 hours: Create ticket for planning

**References:**
- Capacity Planning: `CAPACITY_PLANNING.md`
- Load Testing: `README.md`
- Durability Testing: `DURABILITY_TEST_GUIDE.md`
- Database Schema: `alembic/versions/`
