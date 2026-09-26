# M2 Rank 3: Phase 1 Entity Inventory

**Document ID:** M2R3-PHASE1-INVENTORY-2026-07-23  
**Status:** COMPLETE  
**Discovered:** 2026-07-23  
**Entities Catalogued:** 11 projects, 5 contacts, 2 organizations, 3 engagements, 3+ users

---

## PROJECTS (Discovered: 11)

| Project | Directory | Status | Registered | Notes |
|---------|-----------|--------|------------|-------|
| empirica-foundation-evaluator | empirica-foundation-evaluator | ✓ Active | ❌ No | Admiral seat, Evaluator practice |
| empirica-autonomy | empirica-autonomy | ✓ Active | ❌ No | Autonomy/ECO gates |
| empirica-mesh-support | empirica-mesh-support | ✓ Active | ❌ No | Cross-org coordination |
| empirica-outreach | empirica-outreach | ✓ Active | ❌ No | Research/proposals |
| humanaios | humanaios | ✓ Active | ❌ No | HumanAIOS platform |
| humanaios-internal | humanaios-internal | ✓ Active | ❌ No | Internal research |
| website | website | ✓ Active | ❌ No | Foundation website |
| flta-app-empirica | flta-app-empirica | ✓ Active | ❌ No | FLTA engagement |
| collaborator-ops | collaborator-ops | ✓ Active | ❌ No | Operations practice |
| grok-crossref | grok-crossref | ✓ Active | ❌ No | Knowledge integration |
| opportunity-aggregator | opportunity-aggregator | ✓ Active | ❌ No | Opportunity tracking |

**Summary:** 11 projects discovered (expected 9). All in `/practices` directory. None currently registered in entity_registry.

---

## CONTACTS (Discovered: 5)

| Contact | Email | Role | Registered | Notes |
|---------|-------|------|------------|-------|
| Carly R. Anderson | carly.r.anderson@gmail.com | Admiral | ✓ Yes (partial) | Foundation BDFL, Evaluator owner |
| GitHub Copilot | 198982749+Copilot@users.noreply.github.com | Bot | ❌ No | GitHub automation |
| Dependabot | 49699333+dependabot[bot]@users.noreply.github.com | Bot | ❌ No | Dependency automation |
| AI OS Human | aioshuman@gmail.com | ? | ❌ No | Possible contributor (unclear) |
| Local User | andersonfamily@Carlys-MacBook-Pro.local | Developer | ❌ No | Local machine contributor |

**Summary:** 5 contacts identified (Carly confirmed, others partial/bot). Only Carly partially registered. Need to establish canonical contact registry.

---

## ORGANIZATIONS (Discovered: 2)

| Organization | Slug | Practices | Registered | Notes |
|--------------|------|-----------|------------|-------|
| empirica-foundation | empirica-foundation | 9 practices | ✓ Yes | Foundation org |
| empirica (company) | empirica | mesh-support via cross-org agreement | ✓ Yes (partial) | Company org, support channel to mesh-support |

**Summary:** 2 organizations as expected. Both partially registered. Cross-org relationship needs verification.

---

## ENGAGEMENTS (Discovered: 3)

| Engagement | Name | Projects | Status | Notes |
|-----------|------|----------|--------|-------|
| ACAT Pilot | ACAT Assessment & Calibration | empirica-foundation-evaluator | ❌ Unregistered | Calibration instrument |
| HumanAIOS Initiative | HumanAIOS Platform | humanaios, humanaios-internal | ❌ Unregistered | Core platform initiative |
| FLTA | FLTA Integration | flta-app-empirica | ❌ Unregistered | FLTA engagement |

**Summary:** 3 engagements confirmed (expected 3). None currently registered. Need to establish engagement entity type.

---

## USERS (Discovered: 3+)

From `git log --format="%aE"` analysis:

| User | Email | Contribution Type | Count |
|------|-------|-------------------|-------|
| Carly R. Anderson | carly.r.anderson@gmail.com | Code, docs, commits | 50+ |
| Local Developer | andersonfamily@Carlys-MacBook-Pro.local | Code, commits | 20+ |
| GitHub Bots | github bots | CI/automation | Various |

**Summary:** 2-3 human users identified from git log. Bots excluded from user registry (separate tracking). Need to establish user entity type and canonical tracking.

---

## CURRENT REGISTRY STATE

**entity_registry SQLite table:**
- Entries: ~3 (partial)
- Fully registered: empirica-foundation-evaluator (partial), empirica-foundation (org), empirica (org)
- Missing projects: 8/11
- Missing contacts: 4/5 (only Carly partial)
- Missing engagements: 3/3
- Missing users: 3/3

**entity_memberships:**
- Registered relationships: 0
- Expected relationships: 8+ (member-of, owns, serves, uses, contributor_to)

---

## SCHEMA GAPS IDENTIFIED

**Current fields available:**
- entity_type, entity_id, display_name, description, source_db, source_table, emoji_state, status, created_at, updated_at, metadata

**Missing fields (blocking full registry):**
- `canonical_identifier` — 3-form (org.tenant.project) for routing
- `authority_tier` — (Admiral, Owner, Member, Observer)
- `contact_info_encrypted` — email, Slack handle
- `last_verified_at` — verification timestamp
- `verification_status` — (synced, stale, conflict)
- `verification_hash` — source file hash for change detection

---

## NEXT PHASES (Phases 2-6)

| Phase | Task | Dependencies | Timeline |
|-------|------|--------------|----------|
| **Phase 2** | Schema Update | Phase 1 ✓ | Day 1 |
| **Phase 3** | Entity Registration | Phase 2 | Day 2-3 |
| **Phase 4** | Relationship Validation | Phase 3 | Day 3-4 |
| **Phase 5** | Sync Pipeline | Phase 4 | Day 4-5 |
| **Phase 6** | Verification & Testing | Phase 5 | Day 5-6 |

**Total Timeline:** 6 days (can be parallelized after Phase 2)

---

## RECOMMENDATIONS

1. ✅ **Start Phase 2 immediately** — schema update is independent and unblocking
2. ✅ **Parallelize Phases 3-4** — entity registration and relationship validation can overlap
3. ✅ **Phase 5** — sync pipeline implementation (requires stable schema + entities)
4. ✅ **Phase 6** — verification & testing (final checkpoint)

---

**Status: Phase 1 complete. Ready to launch Phase 2-6 work.**
