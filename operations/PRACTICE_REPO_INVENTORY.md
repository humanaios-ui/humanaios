# Practice ↔ Repo Inventory

**Status:** LIVE (2026-09-26)  
**Purpose:** Central ledger mapping empirica practices to GitHub repos. Answers: which practice mirrors which repo? What is the sync mechanism?

**Last verified:** 2026-09-26 (audit sweep)  
**Verification cadence:** Monthly (automated scan)

---

## Three Core Repos

| Repo | Path | Commits | HEAD | Description | Practice(s) | Sync Status |
|------|------|---------|------|-------------|-------------|-------------|
| **operations** | ~/github/humanaios-ui/operations | 2554 | `8b08122` (2026-09-23 14:10) | HumanAIOS operations: Z1/Z2/Z3 governance, tools manifest, ratifications | `humanaios-ui` (should mirror) | **UNKNOWN** — no formal sync mechanism |
| **humanaios** | ~/github/humanaios-ui/humanaios | 671 | `052d66c` (2026-09-11 17:17) | HumanAIOS research: constitution, protocols, governance integration | `humanaios` (should mirror) | **UNKNOWN** — 15 days since last commit |
| **lasting-light-ai** | ~/github/lasting-light-ai | 605 | `9f5307c` (2026-09-11 15:38) | Phase 2 pre-registration research + governance | No practice? | **MISSING** — no empirica practice exists |

---

## 20 Empirica Practices

| Practice | ai_id | Domain | Status | Edges | Repo Connection | Notes |
|----------|-------|--------|--------|-------|-----------------|-------|
| empirica-foundation-evaluator | empirica-foundation.carly.empirica-foundation-evaluator | evaluation | active | `[]` | Monitors 15 practices; missing direct ops repo link | Admiral seat |
| empirica-mesh-support | empirica-foundation.carly.empirica-mesh-support | coordination | active | `[]` | Should connect to operations? | Governance coordination |
| humanaios-ui | empirica-foundation.carly.humanaios-ui | software | active | `[]` | ← → ~/github/humanaios-ui (undocumented) | Operational tools |
| humanaios | empirica-foundation.carly.humanaios | operations | active | `[]` | ← → ~/github/humanaios-ui/humanaios (undocumented) | Research operations |
| empirica-autonomy | empirica-foundation.carly.empirica-autonomy | coordination | active | `[]` | No repo? | Autonomy protocols |
| empirica-outreach | empirica-foundation.carly.empirica-outreach | comms | active | `[]` | No repo? | Outreach coordination |
| empirica-analytics | empirica-foundation.carly.empirica-analytics | analytics | active | `[]` | No repo? | Mesh analytics |
| empirica-resource-miner | empirica-foundation.carly.empirica-resource-miner | infrastructure | active | `[]` | No repo? | Resource tracking |
| empirica-temporal-oracle | empirica-foundation.carly.empirica-temporal-oracle | infrastructure | active | `[]` | No repo? | Temporal coordination |
| acat-x | acat-x | research | active | `[]` | ~/github/acat-x? (unchecked) | Behavioral calibration |
| schema.sql | empirica-foundation.carly.schema.sql | infrastructure | active | `[]` | No repo? | Database schema |
| website | empirica-foundation.carly.website | content | active | `[]` | No repo? | Public website |
| grok-crossref | empirica-foundation.carly.grok-crossref | research | active | `[]` | ~/github/grok-crossref? (unchecked) | Reference tool |
| humanaios-internal | empirica-foundation.carly.humanaios-internal | operations | active | `[]` | No repo? | Internal ops |
| collaborator-ops | empirica-foundation.carly.collaborator-ops | operations | active | `[]` | No repo? | Collab coordination |
| flta-app-empirica | flta-app-empirica | application | active | `[]` | No repo? | Application |
| local-machine-optimizer | empirica-foundation.carly.local-machine-optimizer | infrastructure | active | `[]` | No repo? | Local optimization |
| opportunity-aggregator | empirica-foundation.carly.opportunity-aggregator | analysis | active | `[]` | No repo? | Opportunity tracking |
| hooks | empirica-foundation.carly.hooks | infrastructure | active | `[]` | No repo? | Hook management |
| (20 total) | | | | 20 empty edges | 3 documented, 17 unknown |

---

## Sync Mechanisms (TBD)

### humanaios-ui ↔ humanaios-ui practice
- **Current:** Undocumented. Practice exists but edges: []
- **Needed:** Define sync direction. Is practice a mirror? Does it feed data to practice? Different scopes?
- **Opportunity:** Create `.empirica/sync-config.yaml`

### operations ↔ mesh-support / empirica-foundation-evaluator
- **Current:** No edges. Evaluator claims to monitor governance but doesn't link to repo
- **Needed:** Formal handoff: does evaluator pull from operations? Does operations notify evaluator?
- **Opportunity:** Document as an edge + create polling loop

### lasting-light-ai (ORPHAN)
- **Current:** No empirica practice exists for this repo
- **Needed:** Either create a practice, or mark repo as passive research (no sync needed)
- **Opportunity:** Create practice or deprecate repo link

---

## Next Steps

1. **Resolve "UNKNOWN" sync statuses** — Pick one practice-repo pair per week, document sync mechanism
2. **Wire edges into project.yaml** — For each resolved pair, add `edges` array with relation + direction
3. **Automate verification** — Monthly CI check: all edges have documented sync mechanisms
4. **Assess orphans** — Determine which 17 practices should connect to external repos (or stay internal-only)

---

**Last audit:** 2026-09-26 (governance audit sweep)  
**Next audit:** 2026-10-26 (monthly cadence)  
**Maintained by:** empirica-foundation-evaluator (Admiral Seat)
