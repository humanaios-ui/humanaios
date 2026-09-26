# HumanAIOS Repair Sequence — Execution Plan

**Reference:** HumanAIOS Repair Sequence (Claude Fable 5.1, 2026-09-11)  
**Status:** Planning & Delegation (PREFLIGHT: eba2513a)  
**Coordinator:** Claude (David-representative role)  
**Phase:** Phase 2.C.2 Live (SER: ser_31f97ce0da3f4239869a09a7)

---

## Authority Mapping

I represent **David** in this coordination, which means:

| Role | Authority | Fixes |
|------|-----------|-------|
| **David** (upstream) | Cortex/Empirica package, listeners, readiness gates | 09, 12, 26 |
| **Carly** (Admiral/ratifier) | Decisions, tokens, configuration, public messaging | 02, 12, 17, 18, 19, 20, 21, 22, 23, 25 |
| **Claude** (me, David-rep) | Mechanical, write code, run science, coordinate mesh | 01, 03-08, 10-11, 13-16, 24 |

**Key principle from constitution §V:** "Push when convergent" → I prepare David's fixes, then propose via mesh with evidence. I don't execute upstream changes myself.

---

## Wave Structure

### Wave 0: Stop the Bleeding (Mechanical, No Decisions)

**Goal:** Make the API operational and remove false public claims.

| Fix | Title | Owner | Status | Blocker |
|-----|-------|-------|--------|---------|
| 01 | Bring public ACAT intake API back | claude | Ready | None |
| 03 | Remove wrong arXiv identifier | claude | Ready | None |
| 04 | Retire marketing README claims | claude | Ready | None (benefits from 20) |
| 05 | Repair frozen corpus file | claude | Ready | None |
| 06 | Reconcile dimension list | claude | Ready | None |
| 08 | Close 77-day stale transaction | claude | Ready | None |
| 13 | Housekeeping (doctor, uncommitted work) | claude | Ready | None |

**Total effort:** ~1 session (fixes 1-7). **Decision gates:** None.

**Verification:** API health check passes, arXiv grep empty, corpus validates, no stuck transaction.

---

### Wave 1: Measurement Setup (Instrumentation + Upstream Fixes)

**Goal:** Make calibration observable and fix foundational defects.

| Fix | Title | Owner | Status | Blocker |
|-----|-------|-------|--------|---------|
| 07 | Fix Evaluator seat identity | claude | Ready | 13 |
| 09 | Stop listener crash loop | David | **Propose via mesh** | None (after 13) |
| 10 | Retrieval-first session ritual | claude | Ready | None |
| 12 | Let honest uncertainty pass readiness gate | David | **Propose via mesh** | None (after 10) |

**Total effort:** 1 session (claude), 1 message (David proposal).

**Verification:** Evaluator identity correct, listeners healthy, session hook blocks empty closes, readiness gates raise threshold.

**David-representative action:** After 10 is written, compose proposal message to David with:
- Fix 09 evidence: listener logs showing 21 restarts/day, probe target returning 502
- Fix 12 evidence: readiness gate blocking honest corrections (+0.25 uncertainty)
- Request: upstream report + gate semantics change (can be together or separate)

---

### Wave 2: Science & Data (Runnable, Grounded)

**Goal:** Produce external-referent measurements, not self-report about self-report.

| Fix | Title | Owner | Status | Blocker |
|-----|-------|-------|--------|---------|
| 14 | Refresh public dataset | claude | Ready | 01, 05 |
| 15 | Run H-INSPECT-01 to minimum N | Carly | **Request keys** | 01, 05 |
| 16 | Write fractal-gap analysis | claude | Ready | None |
| 11 | Graph closure sprint | claude | Ready | 10 |
| 24 | Register canonical sources | claude | Ready | 03, 14, 20 |

**Total effort:** 2 sessions (claude science). **Decision gates:** API keys from Carly (fix 15).

**Verification:** Dataset updated on HF, KS table exists, agent-layer-gap.md published, closure rates improve.

---

### Wave 3: Restructure (Decisions Only)

**Goal:** Align authority, seat count, and mechanism validation.

| Fix | Title | Owner | Status | Blocker |
|-----|-------|-------|--------|---------|
| 17 | Collapse 14 practices to 3 seats | Carly | **Decision** | 13 |
| 18 | Mechanism audit & verdict table | claude | **Draft** | 17 |
| 19 | External referent (independence) | Carly | **Decision** (3 options) | 15 |
| 20 | One canonical STATUS.md | Carly | **Decision** | 03 |
| 21 | Allow calendar time in planning | Carly | **Decision** | None |
| 22 | Gig pivot template | Carly | **Decision** | None |
| 23 | Protect sole ratifier | Carly | **Decision** | None |
| 25 | Rebalance model spend | Carly | **Decision** | 23 |
| 26 | Report upstream defects | David | **Propose via mesh** | 07, 09, 12 |

**Total effort:** 1 session (draft 18), 1 hour (Carly decisions), 1 message (David report).

---

## Execution Sequencing

```
Wave 0 (parallel)
├─ 01, 03-08, 13 (1 session)
└─ Verify: API 200, arXiv 0 matches, corpus valid, no stuck transaction

Wave 1 (sequential, then proposal)
├─ 07 (unblock David fixes)
├─ 09 prepare + 12 prepare (gather evidence)
└─ Propose to David (fix 09, 12 with evidence) [ungated, noetic]

Wave 1.5 (wait for 09/12 feedback)
└─ 10 (session ritual hooks)

Wave 2 (parallel, wait for Carly approval on 15)
├─ 14 (dataset refresh)
├─ 15 (request Carly's API keys, run H-INSPECT)
├─ 16 (agent-layer-gap analysis)
├─ 11 (closure sprint across 3 seats)
└─ 24 (register canonical sources)

Wave 3 (wait for decisions)
├─ 18 draft (mechanisms audit table) — provide to Carly
├─ Carly decides: 17, 19, 20, 21, 22, 23, 25
└─ Propose to David: 26 (upstream defects summary)
```

**Critical path:** 01 → 14 → 15 (dataset live, keys provided). **Blocking decision:** 02 (public intake route).

---

## Current State Integration

**Phase 2.C.2 live:** Governance execution + visibility active.  
**SER active:** ser_31f97ce0da3f4239869a09a7 (Foundation Orchestration)  
**Listener:** cortex-mailbox-poll (30s base)  
**Practices:** 15 active (9 foundation + 6 cross-org)

**Integration point:** Each Wave becomes a task in the current SER. David-representative proposals route through empirica-mesh-support (our ratified cross-org channel).

---

## Decisions Awaiting Carly

### Gate 1: Public Intake Route (Fix 02)
- **Option A (recommended):** Tokenless `/intake/public/phase1` + `/intake/public/phase3`, purity-forced server-side, rate-limited per IP
- **Option B:** Remove POST instruction from site copy
- **Decision impact:** Grows corpus (A) vs. keeps it clean (B)

### Gate 2: External Referent (Fix 19)
- **Option 1:** Public replication invitation (cheapest, depends on 15)
- **Option 2:** Partner-V as instrument validator (scoped to ACAT)
- **Option 3:** David as quarterly calibration referent for Record seat
- **Recommendation:** All three, starting with Option 1 after 15 completes

### Gate 3: Readiness Thresholds (Fix 12)
- **Recommended:** max_uncertainty 0.60, min_know 0.55
- **Upstream proposal:** Change gate to compare against grounded correction, not raw self-report
- **Timing:** Can be local + upstream simultaneously

### Gate 4: Seat Mapping (Fix 17)
- **Proposed:** Instrument / Record / Venture (3 seats)
- **Impact:** Absorbs 14 practices into 3, reduces briefing tax

### Gate 5: STATUS.md Wording (Fix 20)
- **Format:** One canonical file in operations/STATUS.md
- **Draft:** I provide, you sign

### Gate 6: Session Budget & Model (Fixes 23, 25)
- **Questions:** Ratification scope? Session budget (N per week)? Model default?
- **Timing:** Together with gig-pivot decision (22)

---

## What I'm Starting Immediately

With your "go" on this plan, I will:

1. **Execute Wave 0** — one session, one commit per repository, all mechanical
2. **Prepare Wave 1 David fixes** — gather evidence for fixes 09, 12 (listener logs, gate behavior)
3. **Create mesh proposal** — send David the evidence when 10 is ready
4. **Wait for decision gates** — then execute Wave 2-3 in sequence

**No code changes without approval. No upstream proposals without evidence. No decisions on your behalf.**

---

## This Plan in the Graph

- **Goal:** `HumanAIOS Repair Sequence Execution`
- **Tasks:** One per wave, linked to fixes via finding-log
- **Edge discipline:** Each fix logged as finding with `sourced_from → HumanAIOS_repair_sequence` + `edge → prior_finding | decision`

---

*Prepared by Claude (David-representative role) under Phase 2.C.2 orchestration. Ready to execute.*
