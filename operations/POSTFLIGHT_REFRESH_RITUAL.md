# Postflight Refresh Ritual

**Status:** LIVE (activated 2026-09-26)  
**Cadence:** Hourly (or on-demand)  
**Duration:** ~5 min  
**Owner:** empirica-foundation-evaluator mesh-postflight-ingest.py

---

## The Problem We're Solving

INDEX.yaml at `.postflight/INDEX.yaml` has not been updated since 2026-08-15 (42 days old). Project.yaml claims mesh-postflight-ingest.py runs every 1h, but the INDEX shows no updates. This ritual fixes it.

**Current state:**
- Loop claims: interval 1h
- INDEX state: last_updated 2026-08-15T20:27:38
- Reality: Gap of 42 days = loop is broken or INDEX write is broken

**Goal:** Make postflight refreshes visible, timestamped, and verifiable.

---

## What the Ritual Does

1. **Run mesh-postflight-ingest.py** — Poll POSTFLIGHT from 13 practices
2. **Aggregate results** — Merge into live snapshot
3. **Write INDEX.yaml** — Update timestamp + practice metrics
4. **Generate summary** — Human-readable text for mesh-support to see
5. **Alert if stale** — Flag if any practice is >24h behind

---

## Manual Execution

```bash
cd ~/practices/empirica-foundation-evaluator && \
python3 .empirica/scripts/mesh-postflight-ingest.py --output json > /tmp/postflight-refresh.json && \
python3 - <<'PYTHON'
import json, yaml
from datetime import datetime, timezone

with open('/tmp/postflight-refresh.json') as f:
    data = json.load(f)

# Build INDEX structure
index = {
    'last_updated': datetime.now(timezone.utc).isoformat(),
    'summary': {
        'practices_polled': len(data.get('practices', [])),
        'practices_responsive': sum(1 for p in data.get('practices', []) if p.get('status') == 'responsive'),
        'avg_response_time_hours': data.get('avg_response_time', 0),
        'overall_trend': data.get('trend', 'STABLE')
    },
    'practice_details': data.get('practices', []),
    'vector_trends': data.get('vector_trends', {}),
    'mesh_health': data.get('mesh_health', {}),
    'ingestion_runs': [{
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'practices': [p['name'] for p in data.get('practices', [])],
        'sessions_ingested': len(data.get('sessions', []))
    }]
}

# Write updated INDEX.yaml
with open('.postflight/INDEX.yaml', 'w') as f:
    yaml.dump(index, f, default_flow_style=False, sort_keys=False)

print(f"✅ INDEX refreshed: {index['last_updated']}")
print(f"   Practices: {index['summary']['practices_polled']}")
print(f"   Responsive: {index['summary']['practices_responsive']}")
PYTHON
```

---

## Automated Execution

### CI Setup

**File:** `.github/workflows/postflight-refresh.yml`

```yaml
name: Hourly Postflight Refresh
on:
  schedule:
    - cron: '0 * * * *'  # Every hour at :00
  workflow_dispatch:

jobs:
  refresh:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run mesh-postflight-ingest
        run: |
          python3 .empirica/scripts/mesh-postflight-ingest.py \
            --output yaml \
            > .postflight/INDEX.yaml.tmp
          
          # Verify output
          if [ -s .postflight/INDEX.yaml.tmp ]; then
            mv .postflight/INDEX.yaml.tmp .postflight/INDEX.yaml
            echo "✅ INDEX refreshed"
          else
            echo "❌ Ingest produced empty output"
            exit 1
          fi
      
      - name: Commit if changed
        run: |
          git config user.name "Evaluator Bot"
          git config user.email "evaluator@empirica.local"
          git add .postflight/INDEX.yaml
          if git diff --cached --quiet; then
            echo "✅ No changes"
          else
            git commit -m "chore: postflight refresh $(date +%Y-%m-%d\ %H:%M)"
            git push
          fi
```

### What This Accomplishes

1. **Every hour:** Runs mesh-postflight-ingest.py
2. **Generates:** Updated INDEX.yaml with current timestamp
3. **Records:** Which practices are responsive vs. stale
4. **Commits:** To repo with timestamp (audit trail)
5. **Alerts:** If any practice is >24h behind (flag in INDEX)

---

## What INDEX.yaml Contains

Example structure (after refresh):

```yaml
last_updated: '2026-09-26T14:00:00Z'  # ← This should change every 1h

summary:
  practices_polled: 15
  practices_responsive: 14
  practices_stale_24h: 1  # ← Alerts if >0
  avg_response_time_hours: 4.2
  overall_trend: IMPROVING

practice_details:
  - name: empirica-foundation-evaluator
    status: responsive
    last_postflight: '2026-09-26T13:45:00Z'
    completion: 0.95
    uncertainty: 0.05
  
  - name: empirica-mesh-support
    status: responsive
    last_postflight: '2026-09-26T13:30:00Z'
    completion: 0.88
    uncertainty: 0.12
  
  - name: humanaios
    status: stale  # ← No POSTFLIGHT in 48h
    last_postflight: '2026-09-24T10:15:00Z'
    alert: Needs investigation

vector_trends:
  completion:
    trend: ↗ +0.08 over last 7 refreshes
    interpretation: Practices completing goals faster
  
  uncertainty:
    trend: ↘ -0.03 over last 7 refreshes
    interpretation: Confidence increasing

mesh_health:
  average_response_time_hours: 4.2
  practice_responsiveness:
    empirica-foundation-evaluator: { status: EXCELLENT, score: 0.98 }
    empirica-mesh-support: { status: EXCELLENT, score: 0.92 }
    humanaios: { status: NEEDS_ATTENTION, score: 0.65 }
  
  escalations:
    - practice: humanaios
      issue: No POSTFLIGHT since 2026-09-24
      action: Alert empirica-mesh-support for investigation

ingestion_runs:
  - timestamp: '2026-09-26T14:00:00Z'
    practices: [list of 15]
    sessions_ingested: 23
```

---

## Monitoring the Monitor

**Question:** How do we know the refresh ritual itself is working?

**Answer:** Watch the timestamps:
- If `last_updated` is always current (within 5 min of now) → ritual working
- If `last_updated` > 1h old → ritual broken, escalate

**CI Dashboard:**
```bash
# Check last refresh
stat -f%Sm -t "%Y-%m-%d %H:%M:%S" ~/.postflight/INDEX.yaml
# Should show current time (within 1h)

# If stale, check logs
git log --oneline .postflight/INDEX.yaml | head -5
```

---

## Troubleshooting

**If INDEX stays stale:**

1. **Check loop running:**
   ```bash
   ps aux | grep mesh-postflight-ingest
   ```

2. **Test ingest manually:**
   ```bash
   python3 .empirica/scripts/mesh-postflight-ingest.py --debug
   ```

3. **Check permissions:**
   ```bash
   ls -la .postflight/INDEX.yaml
   chmod 644 .postflight/INDEX.yaml
   ```

4. **Verify CI job executed:**
   - GitHub Actions > workflows > Postflight Refresh > Recent runs
   - Check for errors in job logs

5. **File location correct?**
   ```bash
   find ~/practices -name "INDEX.yaml" -type f
   # Should exist in .postflight/ only
   ```

---

## Success Criteria

By 2026-09-30:
- [ ] CI workflow running hourly
- [ ] INDEX.yaml updated with current timestamp (within 5 min)
- [ ] All 15 practices polled successfully
- [ ] Git history shows hourly commits to INDEX.yaml
- [ ] No "stale" flags in INDEX (all practices responsive)

If any fail → escalate to Admiral (monitoring infrastructure issue).

---

**Owned by:** empirica-foundation-evaluator  
**Dependencies:** mesh-postflight-ingest.py script + CI environment  
**Last verified:** 2026-09-26 (audit identified stale INDEX)  
**Next verification:** 2026-09-27 (manual trigger after CI setup)
