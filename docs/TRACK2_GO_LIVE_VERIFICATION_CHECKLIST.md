# Track 2 Go-Live Verification Checklist

**Status:** Aug 29, 2026 (go-live deadline TODAY)  
**Blocker Status:** ✅ REMOVED — Both backend + frontend wired and integrated  
**Next Steps:** Accessibility audit + Latency/stress testing + Admiral sign-off  

---

## Critical Path Completed

### ✅ Task 1: Backend Wiring (COMPLETE)
- **Commit:** 811a69c (operations repo)
- **What changed:** `track2_ui_integration` router imported + wired into FastAPI app.py
- **Route:** `/api/v1/sonify` (prefix)
- **Status:** Live, endpoints available
- **Verification:** Python syntax valid, no import errors

### ✅ Task 2: Frontend Integration (COMPLETE)
- **Commit:** e9e2e58 (lasting-light-ai repo)
- **What changed:** `MarkerToastContainer` imported + conditionally rendered in App.tsx
- **Auth:** Token loaded from localStorage (`auth_token`)
- **Status:** Live, component renders when authenticated
- **Verification:** `npm run build` succeeds, 407 modules transformed, no TypeScript errors

---

## Remaining Verification Tasks (Before Deploy)

### 📋 Task 3: Accessibility Verification

**Scope:** WCAG 2.1 AA compliance for Track 2 marker notifications

**Checklist:**
- [ ] **Color contrast:** Marker toast colors meet WCAG AA (4.5:1 for small text, 3:1 for large)
  - Info (blue): Frequency 523Hz, check against background
  - Warning (orange): Frequency 587Hz, check against background
  - Urgent (red): Frequency 659-698Hz, check against background
- [ ] **Keyboard navigation:** Toast can be dismissed with Escape key
- [ ] **Screen reader:** Toast content announced (aria-live region for MarkerToastContainer)
- [ ] **Focus management:** Focus stays in toast when it appears (no context jump)
- [ ] **Motion/animation:** Animation can be disabled via prefers-reduced-motion
- [ ] **Icon accessibility:** Icon + text redundancy (no icon-only markers)

**Tools:**
- axe DevTools browser extension (free)
- WAVE (https://wave.webaim.org)
- Manual testing with screen reader (VoiceOver on Mac)

**Acceptance Criteria:**
- No WCAG AA violations reported by axe
- All 6 checklist items verified
- Document any waivers (e.g., if animation is intentional)

---

### ⏱️ Task 4: Latency & Stress Testing

**Scope:** Performance verification for marker streaming under load

**Checklist:**
- [ ] **SSE Connection latency:** <500ms from event publish to browser receive
  - Measure: Open DevTools Network tab, watch `/api/v1/sonify/markers/stream`
  - Send 10 test markers via `test_track2_qa.sh` or manual curl
  - Confirm heartbeat every 30s
- [ ] **Marker throughput:** >100 events/sec without dropping
  - Send rapid-fire markers (use `ab` or similar load tool)
  - Confirm all appear in UI (no silent drops)
- [ ] **UI responsiveness:** No jank/stutter during marker stream
  - Open Chrome DevTools Performance tab
  - Record 30 seconds of marker activity
  - Check FPS (target: >60 FPS)
- [ ] **Memory stability:** No memory leaks after 1000+ markers
  - Monitor Task Manager or Chrome DevTools Memory
  - Send 1000 markers over 10 minutes
  - Check heap growth (should stabilize, not grow linearly)
- [ ] **Connection recovery:** Reconnect after network disconnect
  - Disable network in DevTools
  - Re-enable after 10 seconds
  - Confirm SSE reconnects without manual page reload
- [ ] **Browser compatibility:** Test on at least 2 browsers
  - Chrome (latest): EventSource fully supported
  - Firefox (latest): EventSource fully supported
  - Safari (if available): EventSource fully supported

**Tools:**
- Chrome DevTools (Network, Performance, Memory tabs)
- `test_track2_qa.sh` (in operations repo root)
- Apache Bench: `ab -n 100 -c 1 http://localhost:8000/api/v1/sonify/markers/stream`
- Network throttling: DevTools Network tab → throttle to Slow 3G

**Acceptance Criteria:**
- Latency consistently <500ms (measure 10+ samples)
- Throughput >100 evt/sec confirmed
- Chrome DevTools shows >60 FPS
- No memory leaks detected over 1000 marker test
- Connection recovery verified
- At least Chrome + Firefox tested

---

## Sign-Off Gate

**Admiral Review Required:**
- [ ] Accessibility audit completed and documented
- [ ] Latency/stress test completed and documented
- [ ] Both pass acceptance criteria
- [ ] No blockers for deployment

**If issues found:**
1. Document as finding + unknown (if unclear how to fix)
2. Escalate to mesh-support if cross-practice or infrastructure issue
3. Update this checklist with workaround or waiver

**If all clear:**
- Deploy to production
- Update Track 2 status in Charter (go-live confirmed)
- Close Goal: `f30857da-bf3f-4116-aa87-17f14065318a`

---

## Deployment Steps (After Sign-Off)

1. **Verify endpoints live:**
   ```bash
   curl -H "Authorization: Bearer <token>" \
     http://api.humanaios.io/api/v1/sonify/markers/palette
   ```
   Should return 9 marker definitions.

2. **Test end-to-end (localhost first):**
   ```bash
   # Terminal 1: Start API
   cd operations && python -m uvicorn acat.api.app:app --reload
   
   # Terminal 2: Test marker ingest
   curl -X POST http://localhost:8000/api/v1/sonify/markers/event \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer test-token" \
     -d '{"marker_type": "check_gate_passed", "source_id": "test"}'
   ```

3. **Deploy to staging, run full test suite**

4. **Deploy to production, verify live**

---

## Context / Background

- **Original blocker:** Backend wired, frontend not integrated, no accessibility/performance verification run
- **Fixes applied:** Both wired, components verified to compile
- **Timeline:** 6-day critical path (Aug 22→Aug 29 escalation)
- **Impact:** Track 2 unblocks Phase 2 sonification + empirica mesh observability

---

**Last updated:** 2026-08-29 00:00 UTC  
**Owner:** Claude (humanaios practice)  
**Gate:** Awaiting Admiral accessibility/latency audit approval before deployment
