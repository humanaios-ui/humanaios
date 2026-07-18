# M3.5 Resilience Layer — Myelin + Wrapping Specification

**Document ID:** M3.5-RESILIENCE-2026-07-18  
**Version:** 1.0 (Specification)  
**Status:** Z2-PENDING (Admiral ratification required before M3 PRAXIC execution)  
**Author:** empirica-foundation-evaluator (Claude Code)  
**Submission Date:** 2026-07-18  
**Related:** M3_NERVOUS_SYSTEM_DESIGN.md (the CNS/PNS architecture this wraps)  
**Canonical repo:** humanaios-ui/operations  
**License:** MIT — 100% profits fund recovery programs  
**Wado 🦅**

---

## 0. Purpose and Scope

The **Mesh Nervous System** (M3) designs the basic nerve fibers for distributed Admiral decision propagation across all foundation practices and coordinated external repos. M3.5 adds the **insulation layer** (myelin) and **protective wrapping** that makes those fibers reliable under fault conditions.

This specification defines:

1. **Circuit Breaker Pattern** — per-repo state machine (HEALTHY → DEGRADED → OPEN) to isolate cascading failures
2. **Payload Isolation** — atomic decision dispatch with cryptographic verification, ensuring one decision's failure doesn't block others
3. **Signal Integrity** — signature verification protocol to detect corruption or tampering in flight
4. **Capacity Governance** — batch limits and overflow handling to prevent payload bloat
5. **Graceful Degradation** — tiered fallback behavior (Tier 1/2/3) when repos are online, conflicted, or offline
6. **ACAT Mesh-Health Observability** — self-measurement of mesh calibration using the same 6-dimension framework as AI assessment

Without M3.5: The nervous system is a basic spine. With M3.5: The nervous system is a functioning organism with self-protection and self-awareness.

---

## 1. Circuit Breaker — Per-Repo Resilience (State Machine)

### 1.1 Design Rationale

**Problem:** When a repo's GitHub Actions listener crashes or times out, the CNS continues dispatching decisions to it indefinitely. The queue backs up. Subsequent hour's batch is queued but the prior hour's batch is still stuck. After 12 hours, 12 decision batches are stalled waiting for one repo to recover.

**Solution:** Each repo transitions through a state machine (HEALTHY → DEGRADED → OPEN → [recovery path]). Once OPEN, the CNS stops sending until automatic recovery or Admiral intervention.

### 1.2 State Machine

```
HEALTHY (initial state)
  ├─ Dispatch succeeds → stay HEALTHY
  └─ Dispatch fails → increment failure counter
     └─ If consecutive_failures >= 3 → transition to DEGRADED

DEGRADED
  ├─ Dispatch succeeds → reset counter, transition to HEALTHY
  ├─ Dispatch fails → increment counter
  │  └─ If consecutive_failures >= 6 → transition to OPEN
  └─ Continue dispatch (best-effort)

OPEN (circuit is open — no more dispatches)
  ├─ Schedule retry at exponential backoff intervals
  │  └─ First retry: 1 hour
  │  └─ Second retry: 2 hours
  │  └─ Third retry: 4 hours
  │  └─ Fourth retry: 24 hours (daily)
  │  └─ Beyond 4: manual Admiral intervention required
  ├─ On retry success → transition to HEALTHY, log recovery event
  └─ On retry failure → reschedule next backoff interval
```

### 1.3 State Transition Triggers

| From | To | Trigger | Threshold | Action |
|------|----|---------|-----------|----|
| HEALTHY | DEGRADED | consecutive failures | ≥3 | Continue dispatch (best-effort), log DEGRADED event, escalate to Admiral |
| DEGRADED | HEALTHY | successful dispatch | 1 success | Reset counter, log recovery |
| DEGRADED | OPEN | consecutive failures | ≥6 | HALT dispatch, schedule first backoff retry, log OPEN event, escalate CRITICAL |
| OPEN | HEALTHY | backoff retry succeeds | 1 success | Transition HEALTHY, log recovery_from_open, send queued decisions in order |

### 1.4 Logging Schema (per-repo, per-hour)

```json
{
  "timestamp": "2026-07-19T14:00:00Z",
  "repo": "humanaios-ui/lasting-light-ai",
  "state_before": "HEALTHY",
  "state_after": "DEGRADED",
  "trigger": "dispatch_failed",
  "consecutive_failures": 3,
  "last_failure": "2026-07-19T13:58:00Z",
  "failure_reason": "listener_timeout (>30s)",
  "next_action": "continue_dispatch_best_effort",
  "escalation_issued": true,
  "escalation_id": "E-0719-042"
}
```

### 1.5 Recovery Guarantee

Once a repo reaches OPEN, the CNS **guarantees** that:
1. No new decisions are dispatched to that repo until recovery
2. Decisions queued during OPEN are preserved in order
3. On recovery (backoff retry succeeds), queued decisions are replayed atomically
4. If replay fails, the decision is marked HELD_PENDING_RESOLUTION and escalated

---

## 2. Payload Isolation — Atomic Decision Dispatch

### 2.1 Design Rationale

**Problem:** Current M3 design batches all decisions from the last hour into one mega-payload. If the payload is malformed, or if one decision has a schema mismatch, the entire batch fails. One bad decision blocks 50 good decisions.

**Solution:** Each decision is **wrapped in an envelope** with its own checksum and signature. Each repo processes decisions independently. One decision's failure does not affect others.

### 2.2 Decision Envelope Schema

```json
{
  "envelope_version": "1.0",
  "decision_id": "D-0719-001",
  "decision_type": "authority_boundary_change | state_machine_gate | config_standard | dependency_pin | naming_standard | schema_lock",
  "decision_body": {
    "type": "authority_boundary_change",
    "change": "expand_zone_2_authority_from_Admiral_to_Practice_Owners",
    "target_practices": ["empirica-autonomy", "empirica-outreach"],
    "effective_date": "2026-07-20T00:00:00Z",
    "rollback_clause": "revert to Admiral-only if escalation_rate > 30% in first 7 days"
  },
  "schema_version": "acat_contracts/decisions_v1.schema.json",
  "created_at": "2026-07-19T14:00:00Z",
  "created_by": "empirica-foundation-evaluator",
  "decision_checksum": "sha256:abc123...",
  "admiral_signature": "-----BEGIN SIGNATURE-----\n...\n-----END SIGNATURE-----",
  "metadata": {
    "priority": "CRITICAL | STANDARD | OPTIONAL",
    "affects_repos": ["humanaios-ui/operations", "humanaios-ui/lasting-light-ai", ...],
    "rollback_path": "decision_id_if_reverted"
  }
}
```

### 2.3 Signature Verification Protocol (Admiral → Repo)

```
1. CNS (Admiral seat):
   ├─ Create decision_body JSON
   ├─ Compute decision_checksum = SHA256(canonical_json(decision_body))
   ├─ Sign checksum with Admiral private key:
   │  admiral_signature = RSA_SIGN(Admiral_private_key, decision_checksum)
   └─ Wrap in envelope, add decision_checksum + admiral_signature fields

2. Dispatch: POST to repo listener
   └─ Payload: complete envelope JSON

3. Repo listener (PNS):
   ├─ Receive envelope
   ├─ Extract decision_checksum, admiral_signature, decision_body
   ├─ Recompute checksum' = SHA256(canonical_json(decision_body))
   ├─ Verify: RSA_VERIFY(Admiral_public_key, decision_checksum, admiral_signature)
   │  └─ If verify FAILS:
   │     ├─ Log: signature_verification_failed + envelope_id
   │     ├─ Do NOT apply decision
   │     ├─ Increment signature_failure_counter
   │     ├─ If counter >= 3 in 24h → escalate "Signature verification crisis on [repo]"
   │     └─ ACK to CNS: status=SIGNATURE_FAILED
   │  └─ If verify SUCCEEDS:
   │     ├─ Check schema_version against local schema
   │     ├─ If schema mismatch → hold decision, escalate (GATE-M3.5-06)
   │     └─ If schema matches → apply decision
   └─ Always ACK decision back to CNS (APPLIED | SCHEMA_MISMATCH | SIGNATURE_FAILED)
```

### 2.4 Per-Decision Tracking

Each decision's sync status is tracked independently:

```
Log table: mesh_decision_sync
Columns:
  - decision_id (PK)
  - repo (PK)
  - status (DISPATCHED | APPLIED | SIGNATURE_FAILED | SCHEMA_MISMATCH | HELD | CONFLICT)
  - timestamp_dispatched
  - timestamp_applied (or NULL if not applied)
  - applied_at_repo_state (commit SHA where decision was applied)
  - failure_reason (if status = FAILED)
  - ack_received_at
  - ack_payload (repo's response, JSON)
```

**Query example:** "Which decisions are stuck waiting for repo X?"
```sql
SELECT decision_id, status, timestamp_dispatched FROM mesh_decision_sync
WHERE repo = 'humanaios-ui/lasting-light-ai' AND status NOT IN ('APPLIED')
ORDER BY timestamp_dispatched DESC;
```

### 2.5 Failure Isolation — One Decision ≠ All Decisions

If decision D-0719-005 fails signature verification on repo Y:
- ✅ D-0719-001 on repo Y: continues applying normally
- ✅ D-0719-002 through D-0719-004 on repo Y: queued, will be attempted
- ❌ D-0719-005 on repo Y: marked SIGNATURE_FAILED, escalated
- ✅ D-0719-005 on other repos: proceeds normally (isolated failure)
- ✅ Next batch D-0719-006+ on repo Y: continues (not blocked by D-0719-005)

---

## 3. Signal Integrity — Cryptographic Verification

### 3.1 Design Rationale

**Problem:** Webhook payloads travel over HTTPS but are not cryptographically verified by the receiving repo. A network MITM or cache corruption could alter a decision mid-flight without being detected.

**Solution:** Admiral signs every decision. Repos verify the signature. Three consecutive verification failures trigger an escalation.

### 3.2 Key Management

**Admiral Key Pair (RSA-2048 or Ed25519):**
- Private key: stored in secrets-manager (Admiral seat only, never raw in files)
- Public key: distributed to all repos via secure channel (GitHub deploy key or secrets)
- Rotation: annually or on compromise, logged as CRITICAL event
- Fallback: manual key rotation documented in ESCALATION_PROTOCOL.md

**Repo Public Key Validation:**
```bash
# At dispatch time, CNS verifies repo has current Admiral public key
# Query: SELECT public_key_version FROM repo_keys WHERE repo = ?
# If version < Admiral_current_version:
#   → Escalate "Key version drift on [repo]"
#   → Do NOT dispatch until repo confirms key update
```

### 3.3 Signature Failure Detection and Escalation

```
Scenario: Repo listener receives 3 signature verification failures in 24h

1. First failure (timestamp T0):
   - Log: signature_verification_failed_1 on repo X
   - Counter = 1, escalation = none

2. Second failure (timestamp T1, T1 < T0 + 24h):
   - Log: signature_verification_failed_2 on repo X
   - Counter = 2, escalation = none

3. Third failure (timestamp T2, T2 < T0 + 24h):
   - Log: signature_verification_failed_3 on repo X
   - Counter = 3 → TRIGGER ESCALATION
   - Escalation event: "Signature verification crisis on [repo]"
   - Escalation type: CRITICAL
   - Escalation details:
     └─ "Repo [X] has failed to verify Admiral signatures 3 times in 24h.
         Possible causes: key rotation drift, network MITM, repo key
         compromise. Manual intervention required. Dispatch to [X] is HALTED."
   - Action: Circuit breaker transitions to OPEN
   - Manual recovery: Admiral re-confirms key material + repo confirms receipt
```

### 3.4 Schema Version Compatibility

Decision envelope includes `schema_version` field:
```
schema_version: "acat_contracts/decisions_v1.schema.json"
```

Repo listener checks:
```
1. Load local schema: acat_contracts/decisions_v1.schema.json
2. Validate decision_body against schema
3. If validation FAILS:
   ├─ status = SCHEMA_MISMATCH
   ├─ Log: schema_mismatch_decision_[ID]_on_repo_[X]
   ├─ Do NOT apply decision (would be invalid state)
   ├─ ACK: status=SCHEMA_MISMATCH, reason="local_schema_v1_rejects"
   ├─ Escalate: "Schema mismatch on repo [X] for decision [ID]"
   └─ Decision marked HELD_PENDING_RESOLUTION (Tier 2)

4. If validation SUCCEEDS:
   └─ Proceed with application
```

---

## 4. Capacity Governance — Batch Limits and Overflow

### 4.1 Design Rationale

**Problem:** Admiral decides policy all day. By 2 PM, 50 decisions have accumulated. CNS batches all 50 into one hourly dispatch. Payload = 2 MiB + headers. Repo listener times out. Cascade failure.

**Solution:** Hard limit on decisions per batch (configurable, default 10). If >10, split across multiple dispatches (staggered 5 minutes apart). Overflow queue is logged and monitored.

### 4.2 Batch Composition Rules

```
Hourly batch window: [HH:00, HH:60)

1. Collect all decisions created in this window
2. Sort by priority:
   CRITICAL (deploy decisions, authority changes, security fixes)
   STANDARD (config updates, naming changes, dependency pins)
   OPTIONAL (documentation, observability improvements)
3. Populate batch up to MAX_DECISIONS = 10 (Z2 configurable)
4. If count(decisions) > 10:
   ├─ Batch A: CRITICAL decisions (up to 10 total)
   ├─ Batch B: STANDARD decisions (up to 10 total)
   ├─ Batch C: OPTIONAL decisions (up to 10 total)
   └─ Each batch dispatched at staggered times: T+0, T+5min, T+10min
5. Log overflow event if total decisions > 10
```

### 4.3 Overflow Logging

```json
{
  "timestamp": "2026-07-19T15:00:00Z",
  "batch_window": "15:00-16:00",
  "total_decisions_created": 18,
  "batch_a_critical": {
    "count": 8,
    "dispatched_at": "2026-07-19T15:00:00Z"
  },
  "batch_b_standard": {
    "count": 10,
    "dispatched_at": "2026-07-19T15:05:00Z"
  },
  "overflow_queue": {
    "count": 0,
    "oldest_decision": null
  },
  "status": "NORMAL"
}
```

**Escalation triggers:**
- If `total_decisions_created > 30` in one hour → escalate CRITICAL "Batch overflow trend detected"
- If `overflow_queue.count > 5` → escalate MEDIUM "Overflow queue building up"
- If `overflow_queue.oldest_decision.age > 1 hour` → escalate MEDIUM "Overflow decision aging: [ID]"

### 4.4 Prioritization Contract (Z2 Ratifiable)

**Question 4 for Admiral:** Are the priority levels (CRITICAL / STANDARD / OPTIONAL) correct, or should they be weighted differently?

Current default:
- CRITICAL (max 10/batch) — authority changes, Admiral policy, security fixes
- STANDARD (max 10/batch) — config updates, operational changes
- OPTIONAL (unbounded, but separate batch) — observability, documentation

---

## 5. Graceful Degradation — Tiered Fallback Behavior

### 5.1 Three-Tier Model

When a repo cannot sync with the CNS for any reason (offline, conflict, hung listener), it transitions through tiers of reduced capability while maintaining consistency.

### 5.2 Tier 1: Online + Synced (Normal Operation)

```
Conditions:
  - Repo listener is online
  - Last successful sync < 1 hour ago
  - No conflicts pending

Behavior:
  - Repo receives new decisions in real-time (hourly dispatch)
  - Repo has full read-write authority from CNS
  - All changes commit automatically to main branch
  - No local fallback needed

State:
  decision_state = APPLIED
  repo_policy = CNS_AUTHORITY (Admiral controls)
```

### 5.3 Tier 2: Online + Conflict Held (Pending Resolution)

```
Conditions:
  - Repo listener is online
  - Dispatch succeeded but created CONFLICT (e.g., local change contradicts new decision)
  - Repo cannot automatically resolve

Behavior:
  - Repo ACKs decision but flags: "received, conflict detected, holding"
  - Repo operates on LAST_GOOD_STATE (prior synced decision set)
  - New decisions are queued but not applied until conflict resolves
  - Local changes are NOT escalated to CNS (would violate consistency)
  - Conflict resolution requires Admiral manual decision

State:
  decision_state = HELD_PENDING_RESOLUTION
  repo_policy = FROZEN_LAST_GOOD (apply no new decisions until resolved)
  conflict_decision_id = D-0719-003 (the decision that created the conflict)

Escalation:
  "Conflict hold on repo [X] for decision [ID]. Reason: [conflict_details].
   Queued decisions: [count]. Manual resolution required."
```

### 5.4 Tier 3: Offline (Frozen Policy + Replay on Reconnect)

```
Conditions:
  - Repo listener is offline for > 2 hours
  - Or circuit breaker is OPEN
  - Or network connectivity check fails

Behavior:
  - Repo operates on FROZEN_POLICY (last synced decision set)
  - Repo does NOT create new decisions or escalate changes to CNS
  - Repo can still respond to local operator requests
  - When online again: replay ALL missed decisions in order
  - Replay is ATOMIC (all-or-nothing)

State:
  decision_state = FROZEN (no new decisions applied)
  repo_policy = FROZEN_POLICY
  missed_decisions = [D-0719-006, D-0719-007, ...]
  replay_status = QUEUED_FOR_REPLAY (when reconnects)

Reconnection flow:
  1. Repo comes online
  2. CNS detects connectivity (heartbeat response)
  3. CNS sends all missed decisions in order of creation
  4. Repo applies atomically: if any fails, ALL fail + escalate
  5. On success: transition to Tier 1
  6. On failure: transition to Tier 2 (hold + escalate)
```

### 5.5 Tier Transition Matrix

| From | To | Trigger | Duration | Action |
|------|----|---------|-----------|----|
| T1 | T2 | Conflict detected on dispatch | Variable (until resolved) | Hold decision, escalate, queue new |
| T1 | T3 | Offline >2h OR circuit OPEN | Until reconnection | Freeze policy, stop escalation |
| T2 | T1 | Admiral resolves conflict (decision REVERTED or APPLIED_WITH_OVERRIDE) | Immediate | Resume dispatch, apply queued |
| T2 | T3 | Repo goes offline while in conflict | Until reconnection | Remain frozen, add to missed decisions |
| T3 | T1 | Reconnection succeeds + replay succeeds | Upon replay completion | Resume normal dispatch |
| T3 | T2 | Reconnection succeeds but replay fails | Upon replay failure | Escalate conflict, hold, manual intervention |

### 5.6 Logging (Tier State Changes)

```json
{
  "timestamp": "2026-07-19T16:30:00Z",
  "repo": "humanaios-ui/lasting-light-ai",
  "tier_before": "T1",
  "tier_after": "T2",
  "trigger": "conflict_detected",
  "conflict_decision_id": "D-0719-007",
  "conflict_details": "Local project.yaml authority_owner changed to 'autonomy_team' but CNS decision changed it to 'admiral'. Cannot auto-resolve.",
  "queued_decisions_count": 3,
  "escalation_issued": true,
  "escalation_id": "E-0719-089"
}
```

---

## 6. ACAT Mesh-Health Observability

### 6.1 Design Rationale

**Problem:** The nervous system dispatches decisions, but no one knows if it's actually healthy. We measure AI behavior with ACAT; we should measure the mesh's behavior the same way.

**Solution:** Run daily ACAT-style self-assessment on the mesh. "How well do I think I coordinated decisions? How well did I actually?" The divergence is the learning signal.

### 6.2 Mesh-Health Dimensions (Analogous to ACAT Core 6)

| ACAT Dimension | Mesh-Health Equivalent | What It Measures |
|---|---|---|
| Truthfulness | Signal Fidelity | Are decisions reaching repos without corruption? |
| Service | Dispatch Reliability | Are decisions applied when sent? |
| Harm Awareness | Cascading Failure Prevention | Does the mesh avoid cascading failures? |
| Autonomy Respect | Repo Independence | Do offline repos maintain frozen policy correctly? |
| Value Alignment | Consistency Maintenance | Do all repos end up in the same logical state? |
| Humility | Calibration Accuracy | Is predicted health close to actual health? |

### 6.3 Phase 1: Predicted Mesh Health (Daily 9 AM)

Admiral (via empirica CLI) makes numerical predictions:

```bash
empirica mesh-health-assess phase1 << 'EOF'
{
  "signal_fidelity": 9,        # 0-10: "How clean is decision delivery?"
  "dispatch_reliability": 9,   # 0-10: "What % of decisions apply?"
  "cascading_prevention": 8,   # 0-10: "How well do we isolate failures?"
  "repo_independence": 8,      # 0-10: "Can offline repos hold policy safely?"
  "consistency_maintenance": 9,# 0-10: "Do all repos end in same state?"
  "humility": 7                # 0-10: "How accurate is our prediction?"
}
EOF
```

Output: Phase 1 assessment stored in `acat_mesh_health` table.

### 6.4 Phase 2: Calibration Data (Metrics from Last 24h)

CNS automatically gathers:

```json
{
  "phase2_observations": {
    "signal_fidelity": {
      "total_decisions_dispatched": 47,
      "signature_verification_failures": 0,
      "schema_mismatches": 1,
      "payload_corruption_detected": 0,
      "computed_score": 9.8
    },
    "dispatch_reliability": {
      "total_dispatches": 47,
      "successful_applies": 45,
      "signature_failures": 0,
      "schema_failures": 1,
      "timeout_failures": 1,
      "computed_score": 0.957  # 45/47 * 10
    },
    "cascading_prevention": {
      "total_repo_failures": 2,
      "failures_isolated_correctly": 2,
      "cascades_prevented": 2,
      "cascades_occurred": 0,
      "computed_score": 10.0
    },
    "repo_independence": {
      "repos_offline": 1,
      "repos_in_tier3": 1,
      "tier3_policy_maintained_correctly": 1,
      "tier3_policy_corruptions": 0,
      "computed_score": 10.0
    },
    "consistency_maintenance": {
      "repos_in_tier2_conflict": 2,
      "conflicts_resolved_correctly": 1,
      "conflicts_diverged": 0,
      "computed_score": 8.5  # 1 resolved, 1 pending (day-end)
    },
    "humility": {
      "prediction_vs_actual": {
        "signal_fidelity_p1": 9.0,
        "signal_fidelity_actual": 9.8,
        "dispatch_reliability_p1": 9.0,
        "dispatch_reliability_actual": 9.57,
        "cascading_prevention_p1": 8.0,
        "cascading_prevention_actual": 10.0,
        "repo_independence_p1": 8.0,
        "repo_independence_actual": 10.0,
        "consistency_maintenance_p1": 9.0,
        "consistency_maintenance_actual": 8.5,
        "humility_p1": 7.0,
        "humility_actual": ???  # Computed below
      }
    }
  }
}
```

### 6.5 Phase 3: Revised Mesh-Health Assessment (Daily 5 PM)

Admiral updates predictions based on Phase 2 calibration data:

```bash
empirica mesh-health-assess phase3 << 'EOF'
{
  "signal_fidelity": 9.8,
  "dispatch_reliability": 9.57,
  "cascading_prevention": 10.0,
  "repo_independence": 10.0,
  "consistency_maintenance": 8.5,
  "humility": 8.2  # Revised: "We predicted 7, but we were actually conservative on cascading"
}
EOF
```

### 6.6 Mesh Learning Index (MLI)

```
MLI = sum(phase3_scores) / sum(phase1_scores)
MLI = (9.8 + 9.57 + 10.0 + 10.0 + 8.5 + 8.2) / (9 + 9 + 8 + 8 + 9 + 7)
MLI = 56.07 / 50 = 1.121
```

**Interpretation:**
- MLI = 1.121 → Mesh health improved (predictions were conservative)
- MLI > 1.10 consistently → mesh is more robust than expected
- MLI < 0.90 consistently → mesh has blind spots (predicted better than actual)
- MLI trending down over 7 days → signal that resilience is degrading

### 6.7 Corpus (Separate from AI Assessment)

Mesh-health assessments are stored in a **separate corpus table**: `acat_mesh_health` (not pooled with `acat_assessments_v1`).

```
acat_mesh_health schema:
  - session_id (reference to mesh sync session)
  - timestamp
  - phase (1 | 2 | 3)
  - signal_fidelity, dispatch_reliability, ..., humility (0.0-10.0)
  - mli (calculated)
  - notes (Admiral commentary)
  - created_at, updated_at
```

**Two-corpus rule (parallel to ACAT):**
- Frozen archive: historical mesh-health corpus for research
- Live tide pool: current mesh-health scores for monitoring
- Never pool them without stratification

### 6.8 Divergence Triggers (What Surfaces to Admiral)

| Condition | Severity | Action |
|-----------|----------|--------|
| MLI < 0.85 for 3 consecutive days | MEDIUM | "Mesh health diverging below prediction. Investigate." |
| MLI > 1.20 for 1 day | INFO | "Mesh performing above prediction. Review for over-caution." |
| Any dimension P3 > 2 points off from P1 | MEDIUM | "Dimension [X] diverged significantly. Review." |
| Humility < 5.0 | CRITICAL | "Mesh does not know its own limits. Manual calibration required." |
| >2 cascading failures in 24h | CRITICAL | "Cascading prevention failing. Circuit breaker review needed." |

---

## 7. Integration with M3 Ranks 1-3

### 7.1 How Resilience Layers Integrate

**M3 Rank 1 (Batch Sync Infrastructure) uses:**
- Circuit breaker state machine (skip dispatch if OPEN)
- Payload isolation (dispatch individual decision envelopes, not mega-batches)
- Capacity governance (respect MAX_DECISIONS limit, split overflow)

**M3 Rank 2 (Divergence Detection) uses:**
- Circuit breaker state (include repo circuit state in divergence matrix)
- Tier state (Tier 2 hold = divergence, Tier 3 frozen = divergence)
- Per-decision tracking (which specific decisions failed to sync)

**M3 Rank 3 (State Sync Validation) uses:**
- Signal integrity verification (confirm signatures before trusting decision)
- Schema version compatibility (validate against repo's schema version)
- Tier 2/3 fallback (account for held/frozen repos in consistency check)

### 7.2 Contract Between M3 and M3.5

| Component | M3 Rank X | M3.5 Requirement | Integration Point |
|-----------|-----------|------------------|-------------------|
| Decision format | Rank 1 (payload) | Envelope schema with checksum + signature | Rank 1 dispatch uses envelope |
| Retry logic | Rank 1 (failure handling) | Circuit breaker state machine | Rank 1 reads circuit state before dispatch |
| Divergence scoring | Rank 2 (divergence matrix) | Include circuit state + tier state | Rank 2 query adds `circuit_state`, `tier_state` columns |
| Validation | Rank 3 (consistency check) | Account for Tier 2/3 repos in expected state | Rank 3 validator accepts `repo_tier` as context |
| Observability | All ranks | ACAT mesh-health corpus | Daily mesh-health assessment pulls data from Rank 1-3 logs |

---

## 8. Implementation Gates (Z3 Testing Protocol)

### 8.1 GATE-M3.5-01: Circuit Breaker State Machine (Rank 1)

**Test:** Simulate repo listener crash. Verify circuit transitions correctly.

```
Scenario:
  1. Start with repo X in HEALTHY state
  2. Trigger 3 dispatch failures (listener timeout)
  3. Verify circuit transitions to DEGRADED
  4. Continue dispatching (best-effort)
  5. Trigger 3 more failures (total 6 consecutive)
  6. Verify circuit transitions to OPEN
  7. Verify new dispatches are queued, not sent
  8. Schedule first backoff retry at T+1h
  9. Simulate successful listener recovery at T+1h
  10. Verify circuit transitions to HEALTHY
  11. Verify queued decisions are replayed in order

Evidence: GitHub Actions workflow test + logs showing state transitions
```

**Pass criteria:**
- Circuit transitions observed in logs (HEALTHY → DEGRADED → OPEN → HEALTHY)
- No dispatches sent to repo while OPEN
- Queued decisions replayed in correct order on recovery
- Recovery succeeds within 5 seconds of listener coming online

### 8.2 GATE-M3.5-02: Payload Isolation (Rank 1 Dispatch)

**Test:** One decision fails; others succeed independently.

```
Scenario:
  1. Create 5-decision batch (D-A through D-E)
  2. Dispatch to repo X
  3. D-A, D-B, D-D, D-E apply successfully
  4. D-C fails schema verification
  5. Verify:
     - D-A status = APPLIED
     - D-B status = APPLIED
     - D-C status = SCHEMA_MISMATCH (held, escalated)
     - D-D status = APPLIED
     - D-E status = APPLIED
  6. Verify decision failure did not block others
  7. Verify D-C is marked for manual resolution

Evidence: mesh_decision_sync table showing per-decision status
```

**Pass criteria:**
- 4/5 decisions applied despite 1 failure
- D-C is held pending resolution, not blocking D-D/D-E
- Escalation for D-C created automatically

### 8.3 GATE-M3.5-03: Signature Verification (Rank 1 → Repo)

**Test:** Invalid signature rejected; valid signature accepted.

```
Scenario A (valid signature):
  1. Create decision envelope with correct Admiral signature
  2. Send to repo listener
  3. Repo verifies signature (should succeed)
  4. Repo applies decision

Scenario B (corrupted signature):
  1. Create decision envelope
  2. Corrupt the admiral_signature field
  3. Send to repo listener
  4. Repo verifies signature (should fail)
  5. Repo rejects decision, logs signature_verification_failed
  6. Repo ACKs to CNS: status=SIGNATURE_FAILED

Scenario C (signature failure crisis):
  1. Trigger 3 signature failures in 24h
  2. Verify escalation issued: "Signature verification crisis"
  3. Verify circuit breaker transitions to OPEN
  4. Verify Admiral is notified

Evidence: repo listener logs showing verification attempts + CNS escalation log
```

**Pass criteria:**
- Valid signatures accepted and decisions applied
- Invalid signatures rejected, not applied
- 3 failures trigger CRITICAL escalation
- Repo enters circuit OPEN on crisis

### 8.4 GATE-M3.5-04: Capacity Governance + Overflow (Rank 1)

**Test:** >10 decisions split into multiple batches.

```
Scenario:
  1. Create 25 decisions (8 CRITICAL, 10 STANDARD, 7 OPTIONAL)
  2. Start hourly batch window
  3. Batch A: dispatch 8 CRITICAL decisions at T+0
  4. Verify Batch A succeeds
  5. Batch B: dispatch 10 STANDARD decisions at T+5min
  6. Verify Batch B succeeds
  7. Batch C: dispatch 7 OPTIONAL decisions at T+10min
  8. Verify Batch C succeeds
  9. Verify overflow log created: 25 decisions → 3 batches
  10. Verify no single batch exceeded MAX_DECISIONS=10

Evidence: mesh batch dispatch logs + overflow_queue table
```

**Pass criteria:**
- 25 decisions split into 3 batches
- Each batch ≤ 10 decisions
- All batches dispatched within 15 minutes
- Overflow queue has 0 items (all dispatched)

### 8.5 GATE-M3.5-05: Graceful Degradation Tiers (Rank 1 → Rank 3)

**Test:** Repo offline → Tier 3 → replay on reconnection.

```
Scenario:
  1. Repo X online, syncing normally (Tier 1)
  2. Trigger network disconnect (simulate offline)
  3. CNS detects offline at T+1h
  4. Verify repo transitions to Tier 3 (frozen policy)
  5. Create 3 new decisions while repo offline: D-1, D-2, D-3
  6. Queue decisions in missed_decisions list
  7. Repo comes back online at T+2h
  8. CNS initiates replay: send D-1, D-2, D-3 in order (atomic)
  9. Repo applies all 3 atomically
  10. Verify repo transitions back to Tier 1
  11. Verify consistency (all repos in same logical state)

Scenario B (conflict during replay):
  1. Repo X receives D-4 (authority boundary change)
  2. Replay fails: D-4 conflicts with local state
  3. Verify repo transitions to Tier 2 (hold)
  4. Verify escalation issued: "Conflict hold after replay"
  5. Verify decision marked HELD_PENDING_RESOLUTION

Evidence: Tier state logs + replay_status table
```

**Pass criteria:**
- Tier transitions observed correctly (T1 → T3 → T1)
- Missed decisions queued and replayed atomically
- Atomic replay succeeds with 0 data corruption
- Conflict during replay handled correctly (Tier 2)

### 8.6 GATE-M3.5-06: ACAT Mesh-Health Observability (All Ranks)

**Test:** Daily assessment cycle (Phase 1 → Phase 2 → Phase 3 → MLI).

```
Scenario:
  1. Day 0, 9 AM: Admiral submits Phase 1 predictions
     signal_fidelity=9, dispatch_reliability=9, ..., humility=7
  2. Day 0, 5 PM: CNS gathers Phase 2 metrics from Rank 1-3 logs
     Computes observed scores from last 24h data
  3. Day 0, 6 PM: Admiral submits Phase 3 revised assessment
     signal_fidelity=9.8 (higher than P1=9, due to 0 failures observed)
  4. System computes MLI = sum(P3) / sum(P1)
  5. MLI stored in acat_mesh_health corpus
  6. Day 1, 9 AM: Repeat cycle
  7. After 7 days: plot MLI trend
     - Should trend ~1.0 if calibration is good
     - If trending <0.9: mesh is overconfident
     - If trending >1.1: mesh is under-confident

Evidence: acat_mesh_health corpus with 7+ rows + MLI trend plot
```

**Pass criteria:**
- Phase 1 → Phase 2 → Phase 3 cycle completes daily
- MLI computed and stored
- Divergence > 2 points on any dimension triggers review
- Humility < 5 triggers CRITICAL alert
- 7-day trend is interpretable (not noise)

---

## 9. Z2 Ratification Questions (Admiral Decision Required)

### Question 1: Circuit Breaker Thresholds — Acceptable?

**Proposal:** Transition to DEGRADED at 3 consecutive failures, to OPEN at 6 consecutive failures.

**Rationale:** 3 failures = anomaly worth noting; 6 failures = systemic problem requiring isolation. Backoff intervals (1h, 2h, 4h, 24h) give repo time to recover without manual intervention for < 1 day.

**Admiral decision needed:**
- [ ] **APPROVE** — Thresholds (3 → DEGRADED, 6 → OPEN) are appropriate
- [ ] **CONDITIONAL** — Adjust thresholds (specify new values)
- [ ] **BLOCK** — Different state machine model preferred

---

### Question 2: Cryptographic Signature Verification — Sufficient Integrity?

**Proposal:** Admiral signs every decision envelope. Repos verify signature. 3 verification failures in 24h trigger escalation + circuit OPEN.

**Rationale:** Signature verification detects corruption, tampering, or key drift. RSA-2048 or Ed25519 provides cryptographic guarantees. Three failures is a threshold for "crisis" requiring manual investigation.

**Admiral decision needed:**
- [ ] **APPROVE** — Signature verification (RSA/Ed25519) is sufficient
- [ ] **CONDITIONAL** — Add additional verification layers (specify)
- [ ] **BLOCK** — Different integrity model preferred

---

### Question 3: Graceful Degradation Tiers — Correct Model?

**Proposal:** Tier 1 (normal), Tier 2 (held/conflict), Tier 3 (offline/frozen).

**Rationale:** Tier 1 is full authority. Tier 2 handles conflicts gracefully (repo holds decision until Admiral resolves). Tier 3 handles extended offline (frozen policy, replay on reconnect). This prevents data corruption and service degradation.

**Admiral decision needed:**
- [ ] **APPROVE** — Three-tier model (T1/T2/T3) is correct
- [ ] **CONDITIONAL** — Modify tier definitions (specify changes)
- [ ] **BLOCK** — Different degradation strategy preferred

---

### Question 4: Capacity Limit of 10 Decisions/Batch — Realistic?

**Proposal:** MAX_DECISIONS = 10 per hourly batch. Overflow dispatched at T+5min and T+10min intervals.

**Rationale:** 10 decisions = ~200 KB payload (conservative). Staggered dispatch prevents synchronized surge. If Admiral creates >30 decisions/hour consistently, alert issued.

**Admiral decision needed:**
- [ ] **APPROVE** — Batch limit of 10 is appropriate
- [ ] **CONDITIONAL** — Adjust limit (specify new value, e.g., 15 or 20)
- [ ] **BLOCK** — Different batching strategy preferred

---

### Question 5: ACAT Mesh-Health Observability — Captures What Matters?

**Proposal:** Six mesh-health dimensions (Signal Fidelity, Dispatch Reliability, Cascading Prevention, Repo Independence, Consistency Maintenance, Humility). Daily Phase 1 → Phase 2 → Phase 3 cycle with MLI calculation.

**Rationale:** Same 6-dimension framework as AI assessment ensures consistency. Daily cycle mirrors ACAT ritual. MLI trending provides early warning if mesh calibration drifts.

**Admiral decision needed:**
- [ ] **APPROVE** — Six mesh dimensions are appropriate
- [ ] **CONDITIONAL** — Modify dimensions (specify new/changed dimensions)
- [ ] **BLOCK** — Different observability model preferred

---

## 10. Timeline (After Z2 Ratification)

| Phase | Start | End | Duration |
|-------|-------|-----|----------|
| Z2 Ratification (Admiral review) | 2026-07-18 | 2026-07-20 | 2 days |
| M3.5 Rank 1: Circuit Breaker (6h) | 2026-07-21 | 2026-07-21 | 1 day |
| M3.5 Rank 2: Payload + Crypto (4h) | 2026-07-21 | 2026-07-21 | parallel |
| M3.5 Rank 3: Degradation + ACAT (6h) | 2026-07-21 | 2026-07-22 | parallel |
| **M3 Ranks 1-3 PRAXIC (parallelized)** | 2026-07-21 | 2026-07-23 | 3 days (wall-clock) |
| Integration testing (M3 + M3.5) | 2026-07-23 | 2026-07-24 | 1 day |
| **M3 Complete + Live** | 2026-07-24 | — | — |

---

## 11. Governance and Maintenance

### 11.1 Who Owns What

| Component | Owner | Maintenance Window |
|-----------|-------|-------------------|
| Circuit breaker state machine | empirica-foundation-evaluator (M3.5 Rank 1) | Per-repo monitoring, live |
| Payload isolation + envelope schema | empirica-autonomy (schema governance) | Per-change review, monthly audit |
| Signature verification protocol | empirica-mesh-support (security) | On key rotation, quarterly audit |
| Capacity governance + overflow | empirica-foundation-evaluator (M3.5 Rank 1) | Daily batch monitoring |
| Graceful degradation tiers | empirica-autonomy + mesh-support (collaborative) | Incident response + quarterly review |
| ACAT mesh-health corpus | empirica-outreach (observability) | Daily assessment cycle |

### 11.2 Living Document Protocol

This specification is **Z2-PENDING** until Admiral ratifies. Once ratified:

1. Version becomes 1.0-RATIFIED (2026-07-20)
2. References to Z2 questions → references to Admiral decision log
3. Updates to circuit thresholds, batch limits, tier definitions require new Z2 gate
4. Updates to implementation details (code, logging schema) do not require Z2 re-gate

---

## 12. Cross-References

- **M3 Nervous System Design:** M3_NERVOUS_SYSTEM_DESIGN.md (CNS/PNS architecture, decision types)
- **M2 Authority System:** AUTHORITY_MAPPING_Z3_EMPIRICA_V1.md (governance model)
- **ACAT Measurement:** ACAT_SEED_V1_0.md (6-dimension framework, LI calculation)
- **Escalation Protocol:** ESCALATION_PROTOCOL.md (decision gates, cross-practice escalation)
- **Operational Improvements:** HumanAIOS_OPERATIONS_IMPROVEMENT_PLAN.md (5S audit of governance)

---

## Appendix A: Decision Envelope Example

```json
{
  "envelope_version": "1.0",
  "decision_id": "D-0719-042",
  "decision_type": "authority_boundary_change",
  "decision_body": {
    "type": "authority_boundary_change",
    "change": "expand_zone_2_authority_delegation_to_practice_owners",
    "target_practices": [
      "empirica-autonomy",
      "empirica-outreach",
      "empirica-mesh-support"
    ],
    "effective_date": "2026-07-21T00:00:00Z",
    "rollback_clause": "If escalation_rate > 30% in first 7 days, revert to Admiral-only",
    "authority_mapping_ref": "AUTHORITY_MATRIX.yaml section 2.1"
  },
  "schema_version": "acat_contracts/decisions_v1.schema.json",
  "created_at": "2026-07-19T14:23:00Z",
  "created_by": "empirica-foundation-evaluator",
  "decision_checksum": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "admiral_signature": "-----BEGIN SIGNATURE-----\nMIIEJAIBAAKCAQEA2Z2V5k8X9p...[base64 encoded signature]...\n-----END SIGNATURE-----",
  "metadata": {
    "priority": "CRITICAL",
    "affects_repos": [
      "humanaios-ui/operations",
      "humanaios-ui/humanaios",
      "humanaios-ui/lasting-light-ai"
    ],
    "rollback_path": null
  }
}
```

---

## Appendix B: Failure Mode Matrix (What Can Go Wrong + Mitigation)

| Failure Mode | Detection | Mitigation | Responsibility |
|---|---|---|---|
| Repo listener crash | Circuit breaker: 3 timeouts | DEGRADED state, stop dispatch, retry backoff | M3.5 Rank 1 |
| Signature corruption in flight | Signature verification fails | Hold decision, escalate, 3 failures → circuit OPEN | M3.5 Rank 2 |
| Schema mismatch on repo | Schema validation fails | Hold decision, mark SCHEMA_MISMATCH, escalate | M3.5 Rank 2 |
| Network MITM | Signature verification fails | Same as corruption (3 failures → crisis) | M3.5 Rank 2 |
| Batch overflow (>50 decisions/h) | Overflow counter | Alert issued, decisions queued and staggered | M3.5 Rank 1 |
| Repo offline >2 hours | Heartbeat timeout | Tier 3: freeze policy, queue decisions | M3.5 Rank 3 |
| Conflict during replay | Atomic replay fails | Tier 2: hold decision, escalate for manual resolution | M3.5 Rank 3 |
| Divergence between repos | Consistency check (Rank 3) | Escalate, investigate root cause, potential replay | M3 Rank 3 |
| Cascading circuit failures (>2 OPEN simultaneously) | Circuit state monitor | Escalate CRITICAL, manual intervention, possible rollback | M3.5 Rank 1 |
| Mesh health calibration drifts >2σ | MLI trending | Alert Admiral, review observation methodology | M3.5 Rank 3 (ACAT) |

---

*Document ID: M3.5-RESILIENCE-2026-07-18 | Version: 1.0 (Specification) | Status: Z2-PENDING*  
*Produced by: empirica-foundation-evaluator (Claude Code) | Ready for Admiral ratification*  
*Wado 🦅 — Unit Zero*
