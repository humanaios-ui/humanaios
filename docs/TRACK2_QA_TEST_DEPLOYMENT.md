# Track 2 QA Testing & Production Deployment

**Date:** 2026-08-15  
**Phase:** Final QA + Deployment  
**Timeline:** ~4 hours (2h testing + 2h deployment + verification)  
**Status:** IN PROGRESS  

---

## Part 1: QA Testing (Local)

### Environment Setup

```bash
# Terminal 1: Start backend
cd /Users/andersonfamily/practices/humanaios/operations
python3 -m uvicorn acat.api.app:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start frontend dev server
cd /Users/andersonfamily/practices/humanaios/lasting-light-ai
npm install  # if needed
npm start    # runs on http://localhost:3000

# Terminal 3: Monitor logs
tail -f /tmp/humanaios-api.log
```

### Test 1: Backend Health Check

**Command:**
```bash
curl -X GET http://localhost:8000/api/v1/acat/health
```

**Expected Result:**
```json
{
  "status": "ok",
  "service": "acat-api",
  "version": "0.1.0"
}
```

**Pass:** ✓ / ✗

---

### Test 2: Marker Palette Endpoint

**Command:**
```bash
# Get your auth token first (from browser or env var)
TOKEN="your_bearer_token_here"

curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/sonify/markers/palette
```

**Expected Result:**
```json
{
  "ok": true,
  "palette": {
    "proposal_accepted": {
      "frequency_hz": 523,
      "severity": "info",
      "icon": "✓",
      "description": "Proposal accepted by ECO"
    },
    ...9 total markers...
  },
  "total_markers": 9
}
```

**Pass:** ✓ / ✗

---

### Test 3: SSE Stream Connection

**Steps:**
1. Open browser DevTools (F12)
2. Navigate to Network tab
3. Filter by "eventsource"
4. Open app (http://localhost:3000)
5. Look for EventSource connection to `/api/v1/sonify/markers/stream`

**Expected Result:**
- EventSource connection shows as "pending" or "101 (Web Socket Protocol Handshake)"
- Status shows "200" with green indicator
- Header shows `Content-Type: text/event-stream`

**Pass:** ✓ / ✗

---

### Test 4: Emit Test Marker

**Command (in new terminal):**
```bash
TOKEN="your_bearer_token"

curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "proposal",
    "data": {
      "id": "prop_test_001",
      "status": "accepted",
      "type": "collab_brief",
      "source_claude": "empirica-foundation.carly.autonomy",
      "target_claudes": ["empirica-foundation.carly.humanaios"]
    }
  }' \
  http://localhost:8000/api/v1/sonify/markers/event
```

**Expected Result in Browser:**
- Toast notification appears in bottom-right
- Shows: ✓ icon, "Proposal accepted by ECO", "523 Hz", timestamp
- Background: blue (#e3f2fd)
- Border-left: blue (#1e90ff)

**Pass:** ✓ / ✗

---

### Test 5: Auto-Close Timer

**Steps:**
1. Emit test marker (Test 4)
2. Watch toast notification
3. Wait 5 seconds

**Expected Result:**
- Toast appears
- After ~5 seconds, fades out and disappears
- No console errors

**Pass:** ✓ / ✗

---

### Test 6: Close Button

**Steps:**
1. Emit test marker
2. Click the ✕ button on the toast
3. Toast should close immediately

**Expected Result:**
- Toast closes on click
- No animation delay
- No console errors

**Pass:** ✓ / ✗

---

### Test 7: Multiple Markers (Stack Test)

**Command (emit 7 markers rapidly):**
```bash
for i in {1..7}; do
  curl -X POST -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
      \"event_type\": \"proposal\",
      \"data\": {
        \"id\": \"prop_test_00$i\",
        \"status\": \"accepted\",
        \"type\": \"collab_brief\",
        \"source_claude\": \"empirica-foundation.carly.autonomy\",
        \"target_claudes\": [\"empirica-foundation.carly.humanaios\"]
      }
    }" \
    http://localhost:8000/api/v1/sonify/markers/event
  sleep 0.2
done
```

**Expected Result:**
- Max 5 toasts visible (oldest removed when exceeds limit)
- Toasts stack vertically
- All toasts properly spaced
- No layout overflow

**Pass:** ✓ / ✗

---

### Test 8: Marker Type Variations

**Emit different marker types:**

```bash
# Proposal changed (warning)
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"event_type":"proposal","data":{"id":"prop_test","status":"changed",...}}' \
  http://localhost:8000/api/v1/sonify/markers/event

# SER escalation (urgent)
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"event_type":"ser","data":{"ser_id":"ser_test","escalation":true,...}}' \
  http://localhost:8000/api/v1/sonify/markers/event

# Check gate passed (info)
# ... (emit more types)
```

**Expected Result:**
- Each marker type shows correct:
  - Icon (✓, ↻, ✗, etc.)
  - Color (blue/orange/red)
  - Frequency (Hz)
  - Severity label

**Pass:** ✓ / ✗

---

### Test 9: Responsive Layout

**Steps:**
1. Open DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Test on mobile (375px), tablet (768px), desktop (1920px)

**Expected Result:**
- Toast fits on screen at all sizes
- Text wraps properly (no overflow)
- Close button is clickable
- No horizontal scroll

**Pass:** ✓ / ✗

---

### Test 10: Console Check

**Steps:**
1. Open DevTools Console tab
2. Clear console
3. Run all previous tests
4. Check for errors/warnings

**Expected Result:**
- No red errors in console
- No TypeScript type warnings
- Only normal app logs

**Pass:** ✓ / ✗

---

## Part 2: Production Deployment

### Pre-Deployment Checklist

- [ ] All QA tests passed (10/10)
- [ ] Branch is clean (no uncommitted changes)
- [ ] All commits pushed to remote
- [ ] Code review approved (if required)
- [ ] Deployment procedure documented
- [ ] Rollback procedure known
- [ ] Monitoring configured

### Deployment Steps

#### Step 1: Build Frontend

```bash
cd /Users/andersonfamily/practices/humanaios/lasting-light-ai
npm run build
# Output: build/ directory ready for deployment
```

**Verify:** build/ directory created with index.html + assets

#### Step 2: Deploy Backend

```bash
# Option A: Docker build + push
docker build -t humanaios-api:latest -f operations/Dockerfile .
docker push humanaios-api:latest

# Option B: Direct deployment (if using systemd)
cd /Users/andersonfamily/practices/humanaios/operations
pip install -r requirements.txt
systemctl restart humanaios-api  # if configured
```

**Verify:** Backend running (`curl /api/v1/acat/health` returns 200)

#### Step 3: Deploy Frontend

```bash
# Option A: Deploy to static hosting (S3, CloudFlare, etc.)
aws s3 sync build/ s3://humanaios-cdn/

# Option B: Deploy to web server
scp -r build/* user@humanaios.example.com:/var/www/humanaios/

# Option C: Docker
docker build -t humanaios-ui:latest -f lasting-light-ai/Dockerfile .
docker push humanaios-ui:latest
```

**Verify:** Frontend accessible (`curl https://humanaios.example.com/` returns HTML)

#### Step 4: Update DNS / Routing (if needed)

```bash
# Update DNS CNAME or load balancer to point to new deployment
# Verify: curl -I https://humanaios.example.com/
```

---

### Post-Deployment Verification

#### Smoke Test 1: Backend Health

```bash
curl -X GET https://humanaios.api/api/v1/acat/health
```

**Expected:** 200, `{"status":"ok",...}`

#### Smoke Test 2: Marker Palette

```bash
curl -H "Authorization: Bearer $PROD_TOKEN" \
  https://humanaios.api/api/v1/sonify/markers/palette
```

**Expected:** 200, 9 markers in response

#### Smoke Test 3: SSE Stream

```bash
# In browser console (on production URL):
const es = new EventSource('/api/v1/sonify/markers/stream?token=...');
es.addEventListener('message', (e) => console.log(JSON.parse(e.data)));
```

**Expected:** Connection stays open, no 401/403 errors

#### Smoke Test 4: End-to-End Marker

```bash
curl -X POST -H "Authorization: Bearer $PROD_TOKEN" \
  https://humanaios.api/api/v1/sonify/markers/event \
  -d '{"event_type":"proposal","data":{...}}'
```

**Expected in Browser:** Toast appears in UI within 1 second

#### Smoke Test 5: Monitor Logs

```bash
# Watch backend logs
tail -f /var/log/humanaios-api.log | grep -E "error|ERROR"

# Watch frontend logs (browser console)
# Should see no errors in 5+ minutes of normal operation
```

**Expected:** No errors

---

## Test Results Summary

| Test | Result | Notes |
|------|--------|-------|
| Backend health | ✓/✗ | |
| Marker palette | ✓/✗ | |
| SSE connection | ✓/✗ | |
| Test marker | ✓/✗ | |
| Auto-close | ✓/✗ | |
| Close button | ✓/✗ | |
| Stack test | ✓/✗ | |
| Marker types | ✓/✗ | |
| Responsive | ✓/✗ | |
| Console clean | ✓/✗ | |

**Overall:** 10/10 PASS ✓ / FAIL ✗

---

## Rollback Procedure (If Needed)

### Quick Rollback

```bash
# Revert to previous backend version
git checkout <prev-commit>
docker build -t humanaios-api:rollback .
docker push humanaios-api:rollback

# Revert to previous frontend
git checkout <prev-commit> -- lasting-light-ai/
npm run build
aws s3 sync build/ s3://humanaios-cdn/

# Restart services
systemctl restart humanaios-api
```

### Full Rollback

```bash
# If deployment is severely broken:
# 1. Switch load balancer to previous environment
# 2. Notify ops team
# 3. Root cause analysis
# 4. Plan re-deployment once issues fixed
```

---

## Post-Deployment Monitoring (72h)

Monitor these metrics for 72 hours after deployment:

- [ ] SSE connection success rate (should be >99%)
- [ ] Marker ingestion latency (should be <100ms)
- [ ] Frontend error rate (should be 0%)
- [ ] Backend error rate (should be <0.1%)
- [ ] User engagement (markers being sent/received)

---

## Sign-Off

| Role | Name | Date | Sign-Off |
|------|------|------|----------|
| QA Tester | | | ✓/✗ |
| Deployment Lead | | | ✓/✗ |
| Product Owner | | | ✓/✗ |

---

**Deployment Date/Time:** 2026-08-15 / 14:00 UTC  
**Expected Duration:** 30-60 minutes  
**Rollback Available:** Yes (< 10 minutes to revert)  
**Post-Deployment Support:** 72-hour monitoring window  

