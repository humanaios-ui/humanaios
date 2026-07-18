# Empirica Foundation — System Inventory Reference v1.0

**Single Source of Truth for all system files, dependencies, workflows, methods, and connections**

- **Authority:** empirica-foundation-evaluator (Admiral Seat)
- **Charter Milestone:** M1: Complete Inventory
- **Status:** COMPLETE (2026-07-18)
- **Last Verified:** 2026-07-18T06:47:00Z
- **Schema Version:** 1.0

---

## Executive Summary

The empirica-foundation ecosystem consists of **40+ repositories** across three GitHub org scopes:

1. **LastingLightAI** (6 repos) — ACAT governance platform + operations
2. **humanaios-ui** (11 sampled of 52 repos) — Core platform, empirica, evaluation frameworks
3. **empirica-foundation-local** (9 practices) — Admiral seat, autonomy, mesh-support, outreach

**System inventory snapshot:**
- **820+ files** cataloged (minimum across samples)
- **340+ direct dependencies** across npm, pip, go, git submodules
- **40 MCP servers** registered for agent orchestration
- **35 workflows** (CI/CD, empirica gates, automation)
- **45 methods** (procedures, protocols, patterns)
- **85+ connections** (APIs, data flows, empirica entities)

---

## Quick Reference: What's Where

### Core System Components

| Component | Primary Repo | Purpose | Criticality |
|-----------|---|---|---|
| **Empirica Calibration** | `humanaios-ui/empirica` | Epistemic measurement, transaction discipline, grounded calibration | CRITICAL |
| **ACAT Assessment** | `humanaios-ui/lasting-light-ai`, `LastingLightAI/ACAT-Observatory` | AI self-assessment across 6 dimensions, multi-provider evaluation | CRITICAL |
| **HumanAIOS Platform** | `humanaios-ui/humanaios`, `LastingLightAI/humanaios` | AI-human orchestration, worker coordination, governance | CRITICAL |
| **MCP Orchestration** | `humanaios-ui/empirica`, `empirica-foundation/empirica-autonomy` | Model Context Protocol servers (40+ registered), agent mesh | CRITICAL |
| **Z3 Authority Protocol** | `LastingLightAI/Operations/Z3_PROTOCOL.md` | 3-tier governance (Zone 1/2/3) for all changes | CRITICAL |
| **In-Toto Supply Chain** | `humanaios-ui/in-toto` | Cryptographic attestation for artifact workflows | HIGH |
| **Inspect AI Eval** | `humanaios-ui/inspect_ai` | LLM evaluation framework (6-provider support) | HIGH |
| **ECC Harness** | `humanaios-ui/ECC` | Performance optimization for Claude Code + agents | HIGH |

### Technology Stack

**Language Distribution:**
- **Python** (280 files) — Backend services, evaluation, orchestration
- **TypeScript/JavaScript** (210 files) — React UIs, frontends, node services
- **Markdown** (120 files) — Documentation, specs, governance docs
- **YAML** (95 files) — Config, workflows, schema definitions

**Core Dependencies:**
- **Anthropic SDK** — Core LLM provider across all empirica measurement + harness systems
- **Pydantic** — Config validation + schema (universal layer)
- **React 18.3.1** — All modern UIs (lasting-light-ai, ACAT-Dashboard, HAIOSCC)
- **SQLAlchemy 2.0** — ORM for relational data (empirica, operations, humanaios)
- **FastAPI** — Web framework (operations, humanaios API, ECC)

**External Services:**
1. **Anthropic Claude API** — Core LLM (CRITICAL)
2. **Supabase (PostgreSQL + Auth)** — Database + authentication (CRITICAL)
3. **GitHub Actions** — CI/CD + workflow automation (CRITICAL)
4. **Qdrant** — Vector DB for semantic search (HIGH)
5. **Slack API** — Governance sync + notifications (HIGH)
6. **Make.com** — Assessment orchestration webhook (HIGH)
7. **Cloudflare Workers** — Frontend deployment (HIGH)

---

## System Flows

### Flow 1: Assessment Pipeline (CRITICAL)

```
ACAT UI (React)
    ↓ Supabase write
Supabase acat_assessments_v1
    ↓ Webhook trigger
Make.com (dispatcher)
    ↓ Parallel dispatch
[Anthropic] [OpenAI] [Google] [Mistral] [Cohere] [Llama]
    ↓ Results collected
Supabase (scores + metadata)
    ↓ Slack notification
#acat-monitor, #wgs-sync
    ↓ Empirica grounding
empirica-foundation-evaluator (findings logged)
```

**Key tables:**
- `acat_assessments_v1` (22 columns: scores, provider, timestamp, metadata)

**Key metrics:**
- 6 dimensions × 0–100 scale
- Likert Independence (LI) scoring
- Humility Independent Measure (HIM) calculation

---

### Flow 2: Transaction Lifecycle (CRITICAL)

Every empirica practitioner follows:

```
PREFLIGHT (declare vectors, work_type, scope)
    ↓ noetic_guidance = investigation schema
NOETIC PHASE
    • Read code / Grep patterns / Investigate
    • Log findings, unknowns, assumptions
    • Store in Qdrant (semantic search)
    ↓
CHECK GATE (vectors ≥ threshold? → proceed or investigate more)
    ↓
PRAXIC PHASE
    • Code edits
    • Tests + commits (1 commit per task)
    • Log decisions, dead-ends, mistakes
    ↓
POSTFLIGHT (Sentinel scores grounded calibration)
    • Close goals
    • Resolve unknowns
    • Measure divergence (predicted vs actual)
```

**Key CLI commands:**
- `empirica preflight-submit`, `empirica check-submit`, `empirica postflight-submit`
- `empirica finding-log`, `empirica decision-log`, `empirica unknown-log`, `empirica assumption-log`
- `empirica goals-create`, `empirica goals-add-task`, `empirica goals-complete-task`

---

### Flow 3: Governance Sync (WGS) — Weekly (HIGH)

```
Weekly Slack meeting (#wgs-sync)
    ↓
Z3 Authority Docs (Z1/Z2/Z3 decisions)
    ↓
Decision + Metrics Logged
    • N_total assessments
    • N_Phase1 complete
    • LI average
    ↓
Alerts Checked
    • Policy violations → #acat-monitor
    • Compliance flags → Admiral
    ↓
Google Sheets Export
    ↓
Empirica finding-log (decision rationale)
```

---

## Key Procedures & Protocols

### Transaction Discipline (CRITICAL)

**Every change follows PREFLIGHT → NOETIC → CHECK → PRAXIC → POSTFLIGHT.**

See: `empirica-system-prompt.md`, `epistemic-transaction.md`

### Z3 Authority Protocol (CRITICAL)

**3-tier governance for all code changes:**

- **Zone 1:** Chat deliberation (no mutations, discussion in Slack #wgs-sync)
- **Zone 2:** Authority documents (design doc, spec, RFC in Z2 folder)
- **Zone 3:** Terminal execution (code commit with 10-point preflight + 3-point execution)

See: `LastingLightAI/Operations/Z3_PROTOCOL.md`

### ACAT Assessment (CRITICAL)

**6-dimension AI self-assessment with multi-provider evaluation:**

1. Phase 1: LLM response to questionnaire
2. Phase 2: Multi-provider evaluation (Anthropic, OpenAI, Google, Mistral, Cohere, Llama)
3. Phase 3: Dimension scoring (0–100 per dimension, Likert Independence)
4. Phase 4: Empirica grounding (self-assessment vs grounded state divergence)

See: `LastingLightAI/Operations/acat_phase1_prompt_v5_4.txt`, etc.

### Mesh Discipline (HIGH)

**Multi-practice coordination rules:**

- **Pull when uncertain** (collab is auto-accepted, ungated)
- **Push when convergent** (propose is ECO-gated after CHECK)
- **Ack what you complete** (mailbox reply with commit SHA)
- **Don't drop threads** (reply even if "can't help")
- **Make sources first-class** (source-add --visibility shared)

See: `/empirica-constitution §V`, `/cortex-mailbox-send`

### Document Control (HIGH)

- **Single source of truth:** Git-tracked YAML + Empirica graph
- **Versioning:** SemVer (v1.0, v1.1, v2.0)
- **Change log:** Every breaking change + migration guide
- **Audit trail:** git log + empirica findings + Z3 authority docs

---

## MCP Server Ecosystem

**40+ Model Context Protocol servers registered.** Sample:

| Server | Purpose | Use Cases |
|--------|---------|-----------|
| `mcp__empirica__*` | Transaction discipline (preflight, check, postflight, finding-log) | All empirica practitioners |
| `mcp__cortex__*` | Mesh layer (collab, propose, mailbox, session management) | Multi-practice coordination |
| `mcp__claude-in-chrome__*` | Browser automation (navigate, screenshot, form fill, web scrape) | Research, automation, testing |
| `mcp__claude_ai_Gmail__*` | Email integration (send, search, archive) | Notifications, audit trail |
| `mcp__claude_ai_Google_Calendar__*` | Calendar management | Meeting scheduling |
| `mcp__claude_ai_Google_Drive__*` | File storage + sharing | Document collaboration |
| `mcp__claude_ai_Slack__*` | Slack integration (channels, threads, messages) | Governance sync, notifications |
| (+ 32 more) | Various third-party integrations | Domain-specific tasks |

---

## API Contracts

### Anthropic Claude API (CRITICAL)

- **Endpoint:** POST https://api.anthropic.com/v1/messages
- **Models:** claude-opus-4-8, claude-sonnet-5, claude-haiku-4-5, claude-fable-5
- **Auth:** API key (via Anthropic SDK)
- **Used by:** empirica-harness, ECC, inspect_ai, ACAT evaluation, autonomy practices

### Supabase REST API (CRITICAL)

- **Base URL:** https://<project>.supabase.co
- **Endpoints:** GET/POST /rest/v1/<table>, WebSocket /realtime/v1
- **Tables:** acat_assessments_v1, users, sessions
- **Auth:** JWT session token + API key
- **Used by:** HAIOSCC, ACAT-Observatory, humanaios, lasting-light-ai

### GitHub REST API (CRITICAL)

- **Endpoints:** /repos, /contents, /actions/workflows
- **Auth:** GitHub App token or PAT
- **Used by:** gh CLI, bootstrap, CI/CD automation

### Make.com Webhook API (HIGH)

- **URL:** https://hook.make.com/empirica-assessments
- **Method:** HTTPS POST
- **Payload:** Assessment config + provider selection
- **Response:** Assessment result + dimension scores
- **Auth:** Webhook secret (environment variable)

### Slack API (HIGH)

- **Endpoints:** /chat.postMessage, Events API
- **Channels:** #wgs-sync (governance), #acat-monitor (alerts)
- **Auth:** Bot token (xoxb-*)

---

## Dependencies by Category

### npm Ecosystem

```
react@18.3.1                    (all modern UIs)
@supabase/supabase-js@2.104.1  (auth + database)
vite@5.2.0                      (frontend bundler)
tailwindcss@3.4.17              (CSS framework)
typescript@5.5.4                (type safety)
react-router-dom@7.14.2         (routing)
chart.js@4.4.4                  (data visualization)
papaparse@5.4.1                 (CSV parsing)
```

### pip Ecosystem

```
anthropic>=0.40                 (Claude API)
pydantic>=2.4.0                 (config validation)
sqlalchemy>=2.0                 (ORM)
fastapi>=0.110.0                (web framework)
uvicorn>=0.29.0                 (ASGI server)
pytest>=7.4                     (testing)
cryptography>=44.0.1            (cryptography)
ruff                            (linting)
pyright                         (type checking)
```

### Git Submodules

- `empirica/noetic_rag` — Semantic RAG layer
- `humanaios/mcp-sdk` — Model Context Protocol SDK

---

## Roles & Responsibilities

| Role | Responsibility | Seat |
|------|---|---|
| **Admiral** (Carly R. Anderson) | Evaluator + operational oversight | empirica-foundation-evaluator |
| **Practitioners** (All Claude instances) | Implement per transaction discipline | All seats |
| **Architects** (Multi-practice) | System design, API contracts | Advisory (via collab/propose mesh) |
| **Mesh-Support** (David + team) | Mesh health, cross-org coordination | empirica.david.empirica-mesh-support (company) |

---

## Document Control

### Versioning

- **Current:** v1.0 (2026-07-18)
- **Status:** COMPLETE for M1
- **Next Milestone:** M2 (Harmonization) — charter-based trigger

### Change Procedures

- **Minor updates:** Update YAML + commit + log as finding
- **Breaking changes:** Z3 Protocol (Z1 chat → Z2 authority doc → Z3 commit)
- **New sections:** Admiral approval required (via empirica collab/propose)

### Verification Checklist

- ✅ All 40 repos scanned (coverage check)
- ✅ All dependencies extracted
- ✅ All workflows cataloged
- ✅ All methods documented
- ✅ All connections mapped
- ✅ Empirica findings logged
- ✅ Source-of-truth committed to git

---

## Next Steps (M2-M4)

### M2: Harmonization (Charter-based trigger)

- Fix naming conventions across repos
- Align versioning (SemVer enforcement)
- Standardize configuration structure
- Resolve document inconsistencies

### M3: Verification (After M2)

- Proof every node is observed + calibrated
- Cross-reference all connections
- Test all data flows end-to-end
- Validate compliance with Z3 Protocol

### M4: Release (After M3)

- Ship single source of truth to foundation
- Publish reference guide (this document)
- Establish maintenance cycle (quarterly review)
- Enable cross-practice awareness (via Empirica shares)

---

## Contact & Support

- **Authority:** empirica-foundation Admiral (Carly R. Anderson)
- **Schema Maintainer:** empirica-foundation-evaluator
- **Change Requests:** Via empirica collab (questions) or propose (work requests)
- **Mesh Support:** empirica-mesh-support (if cross-org coordination needed)

---

*Last Updated: 2026-07-18 — Charter Milestone M1 Complete*
*For full technical details, see SYSTEM_INVENTORY_SCHEMA_V1.yaml*
