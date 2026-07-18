# Week 1 Implementation Tasks — HAIOSCC Observation Post

**Phase:** Days 5-6 (Jul 22-24, 2026)

**Objective:** Deploy HAIOSCC as the empirica-foundation-evaluator observation post

**Authority:** Admiral Carly R. Anderson

**Status:** ACTIVE

---

## Task Summary

| Task | Assignee | Deadline | Status |
|---|---|---|---|
| 1. Apply Supabase schema (16 tables) | Supabase | Jul 22 EOD | 🟡 Pending |
| 2. Deploy Cloudflare Functions | Engineering | Jul 22 EOD | 🟡 Pending |
| 3. Wire HAIOSCC UI to API endpoints | UI Engineering | Jul 23 EOD | 🟡 Pending |
| 4. Add observation post tabs | UI Engineering | Jul 23 EOD | 🟡 Pending |
| 5. Wire empirica CLI listener → HAIOSCC | Engineering + Cortex | Jul 23 EOD | 🟡 Pending |
| 6. End-to-end test | QA + Admiral | Jul 24 EOD | 🟡 Pending |
| 7. Admiral handover + sign-off | Admiral | Jul 24 EOD | 🟡 Pending |

---

## Day 5 (Jul 22) — Schema + Functions

### Task 1: Apply Supabase Schema

**Owner:** Supabase / Engineering  
**Effort:** 1 hour  
**Blocker:** None  
**Success Criteria:** 16 tables exist in project `ksinisdzgtnqzsymhfya`

**Steps:**

1. Open Supabase console: `https://app.supabase.com/project/ksinisdzgtnqzsymhfya`
2. Navigate to **SQL Editor**
3. Create new query
4. Copy-paste entire contents of `HAIOSCC_OBSERVATION_POST_SCHEMA.sql`
5. Execute
6. Verify output:
   ```
   ✅ operational_state created
   ✅ zone3_queue created
   ✅ verification_log created
   ✅ collaborators created
   ✅ funding_pipeline created
   ✅ integrations_registry created
   ✅ ic_ledger created
   ✅ ser_status created (seed: 4 rows)
   ✅ layer_1_metrics created
   ✅ layer_2_copilot created
   ✅ layer_3_gates created
   ✅ learning_velocity created
   ✅ three_layer_harmony created
   ✅ escalations created
   ✅ weekly_snapshots created
   ✅ gate_postflight_log created
   ```
7. Verify RLS enabled: Each table should show "RLS enabled" badge
8. Verify seed data: `SELECT * FROM ser_status` should return 4 rows
9. **Commit:** Take screenshot of successful execution, save to `docs/deployment/haioscc_schema_applied_jul22.png`

**Definition of Done:**
- [ ] All 16 tables created without errors
- [ ] RLS enabled on all tables
- [ ] Seed data inserted (4 SERs + integrations)
- [ ] Screenshot evidence attached

---

### Task 2: Deploy Cloudflare Functions

**Owner:** Engineering  
**Effort:** 2-3 hours  
**Blocker:** Supabase schema must exist (Task 1)  
**Success Criteria:** Functions deployed, env vars set, endpoints responding

**Steps:**

1. **Prepare Cloudflare Environment Variables**
   - Get from Admiral or security: `SUPABASE_SERVICE_ROLE_KEY`, `GITHUB_TOKEN`, `CF_API_TOKEN`, `CF_ZONE_ID`, `CF_ACCOUNT_ID`
   - Store in Cloudflare Pages project settings: `haioscc` project
   - Confirm visible under Settings → Environment Variables

2. **Deploy Functions (3 files)**
   - Reference spec: `HAIOSCC_CLOUDFLARE_FUNCTIONS.md`
   - Create directory structure:
     ```
     HAIOSCC/
       functions/
         state.ts
         metrics.ts
         escalations.ts
       wrangler.toml
     ```
   - Implement each function per spec:
     - `state.ts`: GET `/api/state/operational`, `/api/state/ser`, `/api/state/layers`, `/api/state/escalations`
     - `metrics.ts`: POST `/api/metrics/update` (ingest SMAG + Copilot + Gate data)
     - `escalations.ts`: GET `/api/escalation/verify` (15-min cron loop)

3. **Deploy to Cloudflare Pages**
   ```bash
   cd HAIOSCC
   npm install
   wrangler deploy
   ```
   - Confirm: Functions appear in CF Pages dashboard
   - Confirm: Cron trigger `*/15 * * * *` visible in wrangler.toml triggers section

4. **Test Each Endpoint**
   ```bash
   # Test /api/state/operational
   curl -X GET "https://haioscc.pages.dev/api/state/operational"
   # Expected: { "pipeline_status": "GREEN", "runway_days": 365, ... }

   # Test /api/metrics/update (example Layer 1 snapshot)
   curl -X POST "https://haioscc.pages.dev/api/metrics/update" \
     -H "Content-Type: application/json" \
     -d '{
       "source": "empirica_cli",
       "measurement_date": "2026-07-21",
       "layer_1": {
         "smag_raw": 28,
         "smag_adjusted": 22,
         "copilot_avg_confidence": 0.72,
         "trajectory_count": 15
       }
     }'
   # Expected: { "ok": true }

   # Test /api/escalation/verify (cron)
   curl -X GET "https://haioscc.pages.dev/api/escalation/verify"
   # Expected: { "checked": 0, "ok": true }
   ```

5. **Verify in Supabase**
   - After `/api/metrics/update` POST, check `layer_1_metrics` table:
     ```sql
     SELECT * FROM layer_1_metrics ORDER BY measurement_date DESC LIMIT 1;
     ```
   - Should see new row with measurement_date = 2026-07-21

6. **Commit:** Save test results to `docs/deployment/cloudflare_functions_deployed_jul22.md`

**Definition of Done:**
- [ ] All 3 functions deployed without errors
- [ ] Env vars set in Cloudflare Pages project
- [ ] All 4 GET/POST endpoints responding (200 status)
- [ ] Cron trigger registered
- [ ] Test data successfully written to Supabase
- [ ] Test results logged

---

## Day 6 (Jul 23) — UI Integration + Listener Wiring

### Task 3: Wire HAIOSCC UI to API Endpoints

**Owner:** UI Engineering  
**Effort:** 2-3 hours  
**Blocker:** Cloudflare Functions deployed (Task 2)  
**Success Criteria:** Dashboard hydrating real data from `/api/state/*`

**Steps:**

1. **Update HAIOSCC frontend (`src/pages/`)**
   - Install API client: `npm install @supabase/supabase-js`
   - Create `src/api/client.ts`:
     ```typescript
     export async function fetchState(endpoint: string) {
       const res = await fetch(`https://haioscc.pages.dev/api/state/${endpoint}`);
       return res.json();
     }
     
     export async function fetchEscalations() {
       return fetchState("escalations");
     }
     ```

2. **Hydrate Dashboard on Load**
   - Main dashboard component should call on mount:
     ```typescript
     useEffect(() => {
       Promise.all([
         fetchState("operational"),
         fetchState("ser"),
         fetchState("layers"),
         fetchState("escalations"),
       ]).then(([op, sers, layers, escs]) => {
         setOperationalState(op);
         setSERStatus(sers);
         setLayerMetrics(layers);
         setEscalations(escs);
       });
     }, []);
     ```

3. **Dashboard Rendering**
   - TopBar: Display `operational_state.pipeline_status` (GREEN/YELLOW/RED)
   - Escalations alert: Show overdue count badge (red dot if any `status=overdue`)
   - Session ID: Display `operational_state.session_id` in top-right corner

4. **Test**
   - Load `https://haioscc.pages.dev` in browser
   - Open DevTools → Network tab
   - Confirm GET requests to `/api/state/*` complete (200 status)
   - Verify data rendered on page

**Definition of Done:**
- [ ] API client library integrated
- [ ] Dashboard fetches all 4 state endpoints on load
- [ ] TopBar displays operational status + escalation count
- [ ] No console errors
- [ ] Page loads in <2 seconds

---

### Task 4: Add Observation Post Tabs

**Owner:** UI Engineering  
**Effort:** 3-4 hours  
**Blocker:** Task 3 (UI wiring complete)  
**Success Criteria:** 6 new tabs visible + data rendering

**Steps:**

1. **Tab Structure**
   Replace/extend existing tabs:
   ```
   - SER Status (NEW)
   - Three-Layer Metrics (NEW)
   - Weekly Rhythm (NEW)
   - Gate POSTFLIGHT Log (NEW)
   - Corrections Ledger (NEW)
   - Escalations (NEW)
   - [Keep] Zone 3 Queue
   - [Keep] Finance Pipeline
   - [Keep] Collaborators
   ```

2. **SER Status Tab**
   - Render `/api/state/ser` data
   - For each SER 1-4:
     ```
     SER N: [name]
     Status: [current_state]
     Participants: [participants.length]
     Last verified: [last_verified_at timestamp]
     Escalation deadline: [escalation_deadline countdown]
     Alert: 🟡 if overdue ack, 🔴 if past deadline
     ```

3. **Three-Layer Metrics Tab**
   - Left column: Layer 1 (SMAG)
     ```
     Learning Density (raw): 28%
     Learning Density (Copilot-adjusted): 22%
     Target by Gate 2: 40%
     Trend: ↑ Improving
     ```
   - Middle column: Layer 2 (Copilot)
     ```
     Avg Confidence: 0.72
     Target: 0.75+
     Status: ⚠️ Slightly below
     Bias Audit: In progress
     ```
   - Right column: Layer 3 (Gates)
     ```
     Gate 1: [status]
     Gate 2: [status]
     Gate 3: [status]
     Gate 4: [status]
     ```

4. **Weekly Rhythm Tab**
   - Filter `/api/state/weekly_snapshots` by week
   - Display Monday 9am, Wednesday 2pm, Friday 4pm for current week
   - Show harmony status for each checkpoint

5. **Gate POSTFLIGHT Log Tab**
   - Render `/api/state/layers` + `layer_3_gates`
   - Table: Gate # | Close Date | POSTFLIGHT Date | Status | Learning
   - Expandable rows showing full POSTFLIGHT text

6. **Corrections Ledger Tab**
   - Render from `ic_ledger` table (via new `/api/state/corrections` endpoint)
   - Table: Assumption | Invalidated At | Gate # | Evidence | Correction Action

7. **Escalations Tab**
   - Render `/api/state/escalations`
   - Red highlight for `status=overdue`
   - Green highlight for `status=resolved`

8. **Test**
   - Navigate each tab
   - Verify data renders (not empty)
   - Check responsive layout on mobile + desktop

**Definition of Done:**
- [ ] All 6 new tabs render without errors
- [ ] Data populates from API (not hardcoded)
- [ ] Escalations tab shows color-coded status
- [ ] Weekly Rhythm shows correct timestamps
- [ ] No console errors
- [ ] Ready for Admiral review

---

### Task 5: Wire Empirica CLI Listener → HAIOSCC

**Owner:** Engineering + Cortex  
**Effort:** 3-4 hours (complex, multi-system)  
**Blocker:** All prior tasks + Cortex integration availability  
**Success Criteria:** Empirica finding → HAIOSCC metrics update (end-to-end)

**Steps:**

1. **Cortex Event Listener Setup** (Cortex integration)
   - Configure cortex listener to emit `finding_created` events
   - Cortex should emit to a webhook or Cloudflare Queue when:
     - A `finding-log` is created with `--trajectory-type gate_learning_→_next_gate_design` (Gate POSTFLIGHT)
     - A `finding-log` is created with `--trajectory-type learning_velocity_→_deployment_readiness` (Layer 1 snapshot)
     - A finding is created on SER-related trajectories

2. **Webhook Handler** (Cloudflare Function)
   - Create new function `src/functions/cortex-listener.ts`
   - Receives POST from cortex with finding_created event
   - Parses finding metadata:
     ```typescript
     export async function POST(request: Request, env: any) {
       const event = await request.json();
       
       if (event.finding.trajectory_type === "gate_learning_→_next_gate_design") {
         // Extract from finding text: predicted/measured/gap/learning/action
         const gateNum = extractGateNumber(event.finding.description);
         await postToMetrics(env, {
           source: "empirica_cli",
           gate: { gate_num: gateNum, measured_outcome: "..." }
         });
       } else if (event.finding.trajectory_type === "learning_velocity_→_deployment_readiness") {
         // Layer 1 snapshot
         const layer1Data = parseLayer1Finding(event.finding.description);
         await postToMetrics(env, {
           source: "empirica_cli",
           layer_1: layer1Data
         });
       }
     }
     ```

3. **CLI Integration** (Admiral/User workflow)
   - When Admiral runs Gate N POSTFLIGHT:
     ```bash
     empirica finding-log \
       --finding "[Gate N POSTFLIGHT...]" \
       --enabled-by "gate-n-postflight" \
       --informs "phase-n+1-design" \
       --trajectory-type "gate_learning_→_next_gate_design" \
       --impact 0.9 \
       --cross-session \
       --visibility shared \
       --hook-url "https://haioscc.pages.dev/api/cortex-listener"
     ```
   - Empirica calls the hook with the finding
   - HAIOSCC listener receives it → updates dashboard

4. **Test End-to-End**
   - Admiral runs test finding-log with gate POSTFLIGHT
   - Monitor Cloudflare Functions logs: `wrangler tail`
   - Verify POST received from cortex
   - Check `/api/state/layers` for updated gate status
   - Check dashboard: Gate card shows updated status

5. **Fallback: Manual Trigger**
   - If cortex integration not ready by Jul 24 EOD:
   - Admiral can manually POST to `/api/metrics/update` with gate data
   - Same end result, just manual rather than automated

**Definition of Done:**
- [ ] Cortex listener endpoint configured
- [ ] Cortex emits `finding_created` events to webhook
- [ ] Cloudflare function receives and processes events
- [ ] End-to-end test: finding-log → HAIOSCC update
- [ ] Fallback manual endpoint working
- [ ] Logs show successful processing

---

## Day 6 Afternoon (Jul 24) — Testing + Sign-Off

### Task 6: End-to-End Test

**Owner:** QA + Admiral  
**Effort:** 1-2 hours  
**Blocker:** All prior tasks complete  
**Success Criteria:** Full observation post functional

**Test Scenario:**

1. **Simulate Monday 9am Snapshot (Layer 1)**
   ```bash
   curl -X POST "https://haioscc.pages.dev/api/metrics/update" \
     -H "Content-Type: application/json" \
     -d '{
       "source": "empirica_cli",
       "measurement_date": "2026-07-21",
       "layer_1": {
         "smag_raw": 28,
         "smag_adjusted": 22,
         "copilot_avg_confidence": 0.72,
         "trajectory_count": 15
       }
     }'
   ```
   - Verify: Dashboard Three-Layer Metrics tab shows Layer 1 data
   - Verify: Weekly Rhythm tab shows Monday 9am snapshot

2. **Simulate Gate 1 POSTFLIGHT (Layer 3)**
   ```bash
   curl -X POST "https://haioscc.pages.dev/api/metrics/update" \
     -H "Content-Type: application/json" \
     -d '{
       "source": "empirica_cli",
       "measurement_date": "2026-07-21",
       "gate": {
         "gate_num": 1,
         "measured_outcome": "Longview approved Track A ($420k, 12mo)",
         "gap_analysis": "No gap — prediction matched outcome"
       }
     }'
   ```
   - Verify: Dashboard Gate status updated
   - Verify: Gate POSTFLIGHT Log tab shows new entry

3. **Test Escalation (Layer 2 alert)**
   ```bash
   curl -X POST "https://haioscc.pages.dev/api/metrics/update" \
     -H "Content-Type: application/json" \
     -d '{
       "source": "copilot_api",
       "measurement_date": "2026-07-21",
       "layer_2": {
         "avg_confidence": 0.68,
         "bias_audit_status": "in_progress",
         "criterion_4_bias_score": 0.12,
         "model_variance_r_raw": {"claude": 0.72, "gpt4": 0.61, "custom": 0.58}
       }
     }'
   ```
   - Verify: Copilot confidence < 0.70 triggers escalation
   - Verify: Escalations tab shows pending escalation
   - Verify: TopBar alert badge increments

4. **Test Cron Loop**
   ```bash
   curl -X GET "https://haioscc.pages.dev/api/escalation/verify"
   ```
   - Verify: Returns JSON with escalation count
   - Verify: SER deadlines updated
   - Check Cloudflare Functions logs: No errors

5. **Admiral Visual Inspection**
   - Open dashboard: `https://haioscc.pages.dev`
   - Navigate each tab
   - Verify all data renders
   - Confirm no missing information
   - Check responsiveness (mobile + desktop)

**Checklist:**
- [ ] Layer 1 data visible (SMAG metrics)
- [ ] Layer 2 data visible (Copilot confidence)
- [ ] Layer 3 data visible (Gate status)
- [ ] Escalations trigger correctly
- [ ] Weekly rhythm shows snapshots
- [ ] Corrections ledger renders
- [ ] All tabs navigate smoothly
- [ ] No console errors

---

### Task 7: Admiral Handover + Sign-Off

**Owner:** Admiral + Support  
**Effort:** 1 hour  
**Blocker:** Task 6 complete + all systems working  
**Success Criteria:** Admiral acknowledges observation post ready

**Handover Deliverables:**

1. **Documentation**
   - `HAIOSCC_OPERATOR_GUIDE_ADMIRAL.md` (how to use dashboard as Admiral)
   - `HAIOSCC_API_REFERENCE.md` (API endpoints for developers)
   - `HAIOSCC_TROUBLESHOOTING.md` (common issues + fixes)

2. **Admiral Acknowledgment Checklist**
   ```markdown
   # HAIOSCC Observation Post — Ready for Aug 1 Gate 1

   Admiral has verified:
   - [ ] Dashboard loads without errors
   - [ ] SER Status tab shows all 4 SERs + escalation timers
   - [ ] Three-Layer Metrics tab shows SMAG + Copilot + Gates
   - [ ] Weekly Rhythm tab shows Mon/Wed/Fri snapshots
   - [ ] Escalations tab alerts on pending overdue items
   - [ ] Can navigate all 10 tabs smoothly
   - [ ] Understands: Monday snapshot → POSTFLIGHT → Gate 2 handoff loop
   - [ ] Ready to use Aug 1 when Longview decision arrives
   ```

3. **Final Walkthrough**
   - Support walks Admiral through:
     - How to read SER escalation timers
     - What Three-Layer Metrics mean for gate readiness
     - How escalations work (auto-trigger, manual resolve)
     - What to do if dashboard alerts turn red

4. **Sign-Off**
   - Admiral signs: `ADMIRAL_SIGN_OFF_HAIOSCC.md`
   - Document includes:
     - Date: Jul 24, 2026
     - Status: ✅ READY FOR GATE 1
     - Any concerns or modifications needed
     - Approval for full deployment

**Definition of Done:**
- [ ] Admiral has reviewed dashboard in person
- [ ] Admiral acknowledges understanding of escalation rules
- [ ] Admiral confirms ready for Aug 1 Gate 1 activation
- [ ] Sign-off document created + committed

---

## Success Metrics (End of Week 1)

✅ **Objective:** HAIOSCC deployed as empirica-foundation-evaluator observation post

✅ **Evidence:**
- 16 tables created in Supabase (schema applied)
- 3 Cloudflare Functions deployed + responding
- HAIOSCC UI updated with 6 new tabs
- End-to-end test: empirica finding → dashboard update ✅
- Admiral briefed + signed off

✅ **Readiness:**
- Aug 1: Longview decision arrives
- Admiral creates Gate 1 POSTFLIGHT
- Dashboard auto-updates with gate outcome
- Phase 1 planning informed by Gate 1 learning
- SER 1 Monday snapshot (Aug 5) shows POSTFLIGHT logged

---

## Contingency: If Task Incomplete by EOD Jul 24

**Option A (Recommended):**
- Schema + Functions deployed (Tasks 1-2 complete) ✅
- UI tabs deferred to Aug 1-5 (non-blocking)
- Admiral can still use API endpoints directly (manual JSON reads)
- Dashboard UI comes online by Aug 5 (before Gate 1 POSTFLIGHT required)

**Option B:**
- If Cortex integration delayed: Use manual webhook for now
- Admiral POSTs gate data to `/api/metrics/update` directly
- Same result, just manual instead of event-driven

---

## Next Milestone

**Aug 1, 2026 — Gate 1 Activation**

- Longview decision arrives
- Admiral creates POSTFLIGHT using template
- Dashboard shows Gate 1 outcome + learning
- Phase 1 planning begins informed by Gate 1 discovery
- SER 1 escalation countdown: 21 days (Aug 22 deadline for SER 1 on track)

---

**Implementation Owner:** Engineering (with Admiral oversight)

**Status:** Ready to execute

**Activation Authority:** Admiral Carly R. Anderson

---

**Commit this task list to:** `empirica-foundation-evaluator` repo

**Next action:** Begin Day 5 tasks (Jul 22)

