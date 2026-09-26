# Phase 4 API Contracts: humanaios ↔ empirica ↔ cortex

**Document**: Phase 4 Integration Specification  
**Scope**: All API contracts between three systems  
**Owner**: empirica-foundation-evaluator  
**Status**: LIVE (Phase 4 execution)

---

## System Overview

```
┌──────────────┐         ┌─────────────────┐         ┌──────────────┐
│  humanaios   │◄─────►  │    empirica     │◄─────►  │   cortex     │
│ (user-facing)│         │   (evaluation)  │         │  (mesh/collab)│
└──────────────┘         └─────────────────┘         └──────────────┘
   13 endpoints              8 async endpoints        4 MCP servers
```

---

## 1. humanaios → empirica API Surface

**System**: humanaios (self-hosted, REST/JSON)  
**Auth**: GitHub PAT (empirica-foundation scope)  
**Base URL**: `https://humanaios.empirica.local/api/v1`

### 1.1 Health & Status

```
GET /health
  Response: { status: "healthy", version: "2.1.0", uptime_ms: <int> }
  SLA: <100ms
  Timeout: 5s
  Used by: Phase 3.9 smoke test, orchestration monitoring
```

### 1.2 Session & Auth

```
POST /auth/token
  Payload: { credentials: "GitHub PAT" }
  Response: { token: "<JWT>", expires_in: 3600 }
  SLA: <200ms
  Timeout: 10s

POST /sessions
  Payload: { practice_id: "empirica-evaluator", user_id: "<UUID>" }
  Response: { session_id: "<ID>", created_at: "<ISO>" }
  SLA: <500ms
  Timeout: 15s
```

### 1.3 Findings & Artifacts (Ingest)

```
POST /artifacts/findings
  Payload: { finding: "...", impact: <0-1>, visibility: "local|shared|public" }
  Response: { artifact_id: "<UUID>", indexed_at: "<ISO>" }
  SLA: <300ms
  Timeout: 10s
  Rate limit: 100/min per practice

POST /artifacts/goals
  Payload: { objective: "...", description: "...", status: "planned|in_progress|complete" }
  Response: { goal_id: "<UUID>", created_at: "<ISO>" }
  SLA: <300ms
  Timeout: 10s

POST /artifacts/unknowns
  Payload: { unknown: "...", impact: <0-1> }
  Response: { unknown_id: "<UUID>" }
  SLA: <300ms
  Timeout: 10s
```

### 1.4 Search & Query

```
GET /search?query=<term>&limit=<int>
  Response: { results: [...], total: <int> }
  SLA: <500ms for 100 results
  Timeout: 30s

GET /artifacts/<type>/<id>
  Response: { artifact: {...}, related: [...] }
  SLA: <200ms
  Timeout: 5s
```

### 1.5 Webhook (async push)

```
POST /webhooks/subscribe
  Payload: { event_type: "finding.created|goal.updated", url: "<external>" }
  Response: { subscription_id: "<UUID>" }
  SLA: <100ms
  Timeout: 5s

Webhook delivery: empirica → humanaios
  Event: { type: "finding.created", artifact_id: "<UUID>", timestamp: "<ISO>" }
  Retry: exponential backoff, max 5 attempts
  Timeout: 10s per delivery
```

---

## 2. empirica → cortex API Surface

**System**: cortex (mesh orchestration, async gRPC/HTTP)  
**Auth**: Empirica bearer token + x-api-key header  
**Base URL**: `https://cortex.empirica.internal/api/v1`

### 2.1 Session & Initialization

```
POST /sessions/create
  Payload: { ai_id: "empirica-foundation-evaluator", tenant: "carly" }
  Response: { session_id: "<UUID>", ntfy_topic: "empirica-foundation-...", auth: "bearer" }
  SLA: <500ms
  Timeout: 15s
  Async: creates listener subscription
```

### 2.2 Collaboration (noetic, ungated)

```
POST /collab/send
  Payload: { target_ai: "empirica.david.empirica-mesh-support", message: "...", brief: true }
  Response: { proposal_id: "<UUID>", status: "queued" }
  SLA: <200ms
  Timeout: 10s
  Gate: none (noetic flow)
```

### 2.3 Proposals (praxic, ECO-gated)

```
POST /proposals/create
  Payload: { 
    type: "work_request",
    target_ai: "empirica.david.empirica-autonomy",
    action: "execute_phase_3_validation",
    payload: {...},
    metadata: { clauses: [...], epistemic_state: {...} }
  }
  Response: { proposal_id: "<UUID>", status: "submitted" }
  SLA: <300ms
  Timeout: 15s
  Gate: Sentinel CHECK gate required (praxic only)
  
Wait for resolution:
POST /proposals/<id>/poll
  Response: { status: "accepted|declined|pending", resolution: "..." }
  Polling: 30s interval, 24h timeout
```

### 2.4 Mailbox (inbox/outbox)

```
GET /mailbox/inbox?status=pending|accepted|declined
  Response: { items: [...], cursor: "..." }
  SLA: <300ms
  Timeout: 10s

POST /mailbox/reply
  Payload: { parent_id: "<UUID>", summary: "...", status: "accepted|completed|declined" }
  Response: { reply_id: "<UUID>" }
  SLA: <200ms
  Timeout: 10s
```

### 2.5 Publishing & Visibility

```
POST /artifacts/publish
  Payload: { artifact_id: "<UUID>", visibility: "local|shared|public" }
  Response: { published_at: "<ISO>", qdrant_indexed: true }
  SLA: <500ms
  Timeout: 20s
  
Search (Qdrant async):
GET /knowledge/search?query=&scope=session|project|global
  Response: { results: [...], cursor: "..." }
  SLA: <1000ms
  Timeout: 30s
```

---

## 3. cortex → External MCPs

**System**: MCP servers (managed by cortex router)  
**Auth**: Cortex bearer token (auto-routed)  
**Protocol**: MCP stdio + HTTP

### 3.1 claude-in-chrome

```
Browser automation & screenshots
  Methods: navigate, click, read_page, screenshot, gif_creator
  SLA: <5s per action
  Timeout: 30s
  Used by: Phase 4.3 browser-based API inspection, demo capture
```

### 3.2 Railway

```
Infrastructure operations (deploy, logs, metrics)
  Methods: create-service, get-logs, set-variables, list-deployments
  SLA: <1000ms for reads, <5s for deploys
  Timeout: 60s for deploys
  Used by: Phase 4+ infra ops, resource audit
```

### 3.3 Supabase

```
Database & edge functions
  Methods: apply_migration, execute_sql, deploy_edge_function
  SLA: <500ms for reads, <5s for migrations
  Timeout: 30s
  Used by: measurement gates, data layer for Phase 4+
```

### 3.4 Slack

```
Communication & notifications
  Methods: send_message, create_canvas, update_canvas
  SLA: <500ms
  Timeout: 10s
  Used by: Phase 3.9 deployment notifications, escalation alerts
```

---

## 4. Integration Patterns

### 4.1 Artifact Flow

```
humanaios (user action)
  → POST /artifacts/findings
  → empirica ingests
  → empirica logs to cortex (via POST /artifacts/publish)
  → cortex indexes in Qdrant
  → cortex notifies subscribers (via Slack MCP if visibility=shared)
```

### 4.2 Proposal Flow (Work Request)

```
empirica (praxic decision)
  → CHECK gate required
  → cortex_propose (POST /proposals/create)
  → target_ai receives (mailbox inbox)
  → target_ai executes & replies (POST /mailbox/reply)
  → empirica polls (GET /mailbox/inbox)
  → proposal closes
```

### 4.3 Monitoring Flow

```
Phase 3.9 deployment live
  → humanaios /health (100ms polling)
  → empirica observes metrics
  → escalation triggered if latency > 1200ms
  → cortex_propose to escalation SER
  → mesh-support responds
```

---

## 5. Error Handling & Fallbacks

| Error | SLA | Action |
|-------|-----|--------|
| humanaios /health timeout | 5s | escalate to mesh-support (SER) |
| cortex unreachable | 15s | fall back to local empirica recording |
| proposal declined | immediate | log dead-end, notify source AI |
| Qdrant index lag | 30s+ | deliver findings locally first, async index |
| MCP timeout | per-MCP SLA | retry 3x, then escalate |

---

## 6. Phase 4+ Evolution

**Phase 4b (Sep 20-22)**: Integration testing. Verify all 25 endpoints, rate limits, error paths.

**Phase 5**: Schema validation (JSON Schema for all payloads). OpenAPI/gRPC definitions.

**Phase 6+**: Auto-discovery via MCP introspection. Semantic versioning & backward compatibility.

---

**Document Owner**: empirica-foundation-evaluator  
**Last Updated**: 2026-09-17  
**Version**: Phase 4.0 (live)
