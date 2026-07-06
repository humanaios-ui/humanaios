# HumanAIOS — Document Control Method: Implementation Plan

> **Status:** ratified draft (2026-07-02). Authored by the autonomy practice at Carly's request.
> **Scope (CONFIRMED):** the **humanaios multi-repo ecosystem — all 5 repos** (the doc sprawl the S070126 audit exposed), method reusable for the empirica-foundation practice docs. Approach: **git-native controlled-documents**, informed by the open-source landscape below. Activation method resolved in §10.

---

## 0. Why — the problem this controls

The S070126 audit already did the hard forensic work and quantified the failure mode:

| Audit step | Finding | What it tells us |
|---|---|---|
| T0 freeze | known-state checkpoint | no baseline existed before |
| T1 inbox triage | **1653 files** bucketed | uncontrolled intake |
| T2 reconciliation | **71 diverged pairs** | no single source of truth |
| T3 scope/alignment | **5 repos** audited | control must be multi-repo |

**Diagnosis:** the problem is **multi-repo git divergence + uncontrolled intake**, *not* scanned-document archival. That rules the solution in and out (see §2). The audit was the one-time cleanup; **this plan is the standing discipline that stops it recurring.**

---

## 1. Design principles

1. **Single source of truth (SSOT).** Every controlled document has exactly one canonical location; all other references *link*, never *copy*. Divergence becomes structurally impossible, not just discouraged.
2. **Git-native, docs-as-code.** Control rides the workflow that already exists (repos, branches, PRs) — no parallel system, no second source of truth.
3. **Earned from ISO 9001 §7.5.** Adopt the *discipline* (identification, review/approval, availability, retention) without the certification overhead — it's the battle-tested controlled-document rubric.
4. **Automate the gate, not the judgment.** CI enforces the mechanical rules (metadata present, links valid, no duplicates); humans own approval.
5. **Monitor for drift continuously.** Control that's only checked at the audit is control that has already failed. Detection is scheduled and ongoing (§5).
6. **Turtle-consistent with empirica.** This mirrors the ecosystem's own artifact/provenance model — controlled docs get IDs, owners, and revision history the same way findings/decisions do.

---

## 2. Open-source resources — to adopt & learn from

Researched 2026-07-02. Classified by whether we **adopt** (use directly) or **learn from** (borrow the model).

| Resource | Role | Verdict |
|---|---|---|
| **[markdownlint](https://github.com/davidanson/markdownlint)** | Markdown syntax/structure linting | **Adopt** — CI gate |
| **[Vale](https://www.datadoghq.com/blog/engineering/how-we-use-vale-to-improve-our-documentation-editing-process/)** | Prose style, banned terms, consistent terminology | **Adopt** — CI gate (advisory→error over time) |
| **link-checkers** (e.g. lychee / [mkdocs-linkcheck](https://pypi.org/project/mkdocs-linkcheck/)) | Broken internal/external links | **Adopt** — CI gate |
| **[GitHub CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)** + branch protection | Review ownership + approval enforcement | **Adopt** — the approval mechanism |
| **[Docs-as-Code review workflow](https://www.draftview.app/blog/docs-as-code-review-workflow-complete-guide)** | 4-stage branch→write→review→merge model | **Learn from** — our lifecycle (§3.3) |
| **[ISO 9001 §7.5.3](https://blog.auditortrainingonline.com/blog/explaining-iso-9001-clause-7.5.3-control-of-documented-information)** | Controlled-document requirements | **Learn from** — metadata + retention (§3.1) |
| MkDocs / Docusaurus / Hugo | Static-site publish of the canonical set | **Optional** — Phase 3 "availability at point of use" |
| **[Paperless-ngx](https://www.papermark.com/blog/best-open-source-document-management-software)** / Mayan EDMS | Full DMS (OCR, workflow, RBAC) | **Reject for now** — built for scanned/PDF archival; would create a *second* SSOT and worsen divergence. Revisit only if a binary/scanned-artifact corpus emerges. |

---

## 3. The control model

### 3.1 Controlled-document metadata (ISO §7.5 → YAML frontmatter)

Every controlled `.md` carries a frontmatter block. CI rejects controlled docs missing required keys.

```yaml
---
doc_id: HAIOS-GOV-012          # unique, stable, never reused
title: 12 Traditions Compliance Audit
revision: 3                     # integer, bumps on approved change
status: approved                # draft | review | approved | superseded | retired
owner: "@humanaios-ui/governance"   # CODEOWNERS group, not a person
approved_by: carly              # required when status=approved
approved_date: 2026-06-30
review_due: 2026-12-30          # drives staleness monitor
supersedes: HAIOS-GOV-011       # optional lineage
canonical: true                 # exactly one canonical per doc_id across all repos
retention: permanent            # permanent | 7y | 3y | superseded-only
---
```

### 3.2 The registry (SSOT enforcement)

A single machine-readable `document-registry.yaml` (in a designated control repo) lists every `doc_id`, its canonical path/repo, revision, status, owner. It is the index that:
- **kills divergence** — a `doc_id` with two `canonical: true` copies is a CI failure;
- powers the drift monitor (§5);
- is the human-readable "controlled document list" ISO §7.5 expects.

### 3.3 Lifecycle & states

```
draft ──PR+review──> review ──approval(CODEOWNERS)──> approved ──published
  ▲                                                      │
  └───────────────── new revision (PR) ─────────────────┘
                          approved ──> superseded ──> retired
```

Obsolete versions are marked `superseded`/`retired` (never silently deleted) — satisfying §7.5 "prevent unintended use of obsolete documents" while preserving history in git.

### 3.4 Approval & ownership

- `CODEOWNERS` maps doc paths → owning group; branch protection **requires** owner approval to merge changes to `approved` docs.
- Groups, not individuals (survives role changes).
- `status: approved` + `approved_by`/`approved_date` are set only in an approved PR — the merge *is* the approval record.

### 3.5 Intake pipeline (formalize the audit triage into a repeatable process)

The T1 inbox triage becomes a standing 4-gate pipeline so `_inbox_files*` never accumulates 1653 items again:

```
_inbox/ ──1.classify──> 2.dedup-vs-registry ──> 3.reconcile ──> 4.register+place
         (type, owner)   (is this already a       (if diverged    (assign doc_id,
                          controlled doc?)          copy → merge)    frontmatter, canonical)
```

Run on a cadence (or on inbox-file-add). Anything that can't be classified is quarantined, not merged.

---

## 4. Automated control gates (CI) — "monitor" at merge time

A `document-control` CI workflow on every PR touching docs, **two severity tiers** (per docs-as-code best practice — error blocks merge, warning advises):

| Check | Tool | Tier |
|---|---|---|
| Frontmatter schema valid + required keys | custom validator | **error** |
| Unique `doc_id`, single `canonical` per id | registry check | **error** |
| Markdown syntax/structure | markdownlint | **error** |
| Links resolve (internal + external) | lychee/link-check | **error** (internal) / warning (external) |
| `status: approved` ⇒ `approved_by` present + owner-approved PR | custom + branch protection | **error** |
| Prose style / banned terms / terminology | Vale | warning → error (ratchet up) |
| Registry in sync with filesystem | registry diff | **error** |

---

## 5. Drift monitoring (ongoing — the standing "monitor")

CI catches drift *at merge*; a scheduled monitor catches drift that accrues *between* merges (external link rot, review-due docs, out-of-band edits, cross-repo divergence).

- **Cadence:** scheduled job (biweekly, matching the existing `services-audit` cron pattern in the ecosystem), or wired as an empirica loop.
- **Emits:** a drift report — diverged pairs, docs past `review_due`, broken links, orphaned/unregistered `.md`, `canonical` conflicts.
- **Escalates:** opens an issue / notifies owner only when *novel* drift appears (diff against last scan) — no noise on a clean run.
- This is the recurring analog of the T2/T3 audit steps — the audit becomes a *sensor*, not a one-off.

---

## 6. Phased rollout

| Phase | Deliverable | Exit criteria |
|---|---|---|
| **P0 ✅ done** | S070126 audit (freeze, triage, reconcile, scope) | baseline known |
| **P1 — Standard** | This method ratified; frontmatter schema + `document-registry.yaml` seeded from the 71 reconciled pairs | registry covers all known controlled docs |
| **P2 — Gate** | CI `document-control` workflow (errors only) + CODEOWNERS + branch protection on the control repo | no non-conforming doc can merge |
| **P3 — Intake** | Inbox pipeline (§3.5) automated; `_inbox_files*` drained to zero-or-quarantine | intake is repeatable, bounded |
| **P4 — Monitor** | Scheduled drift monitor (§5) live | drift detected < 1 cycle after it appears |
| **P5 — Availability** | (optional) static-site publish of the `approved` canonical set | docs available at point of use |
| **P6 — Ratchet** | Vale warnings → errors; extend to all 5 repos | uniform control across the ecosystem |

---

## 7. Roles (RACI, lightweight)

| Role | Who | Owns |
|---|---|---|
| Document owner | CODEOWNERS group per area | content accuracy, approval |
| Control maintainer | designated practice (mesh-support?) | registry, CI, monitor |
| Approver | Carly / area lead | `approved` transitions |
| Contributor | anyone | drafts via PR |

## 8. Success metrics

- Diverged pairs: **71 → 0**, held at 0.
- `_inbox` backlog: bounded (no unbounded growth).
- % controlled docs with valid frontmatter: → 100%.
- Mean time-to-detect drift: < 1 monitor cycle.
- Docs past `review_due`: trending to 0.

## 9. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Frontmatter friction slows contributors | validator gives exact fix; templates + a `new-doc` scaffold |
| CODEOWNERS churn | use groups, not individuals |
| Cross-repo canonical conflicts | registry is the single arbiter; CI blocks dual-canonical |
| Over-tooling | start errors-only + registry; add Vale/site later (P5/P6) |
| Scope wrong (not humanaios) | **confirm scope before P1** (see header) |

## 10. Activation — resolved decisions + the constructive first moves

### 10.1 Resolved decisions

| # | Decision | Resolution |
|---|---|---|
| 1 | **Scope** | ✅ **All 5 repos** (multi-repo). Governed centrally, activated per-repo. |
| 2 | **Control hub** | **`humanaios-ui/operations`** — it already hosts the canonical append-only `REGISTERED.md` (it's a de-facto registry). Home the `document-registry.yaml` + the reusable CI here; the other 4 repos *reference* it. |
| 3 | **Maintainer** | **mesh-support practice** — owns cross-practice plumbing; a natural fit for the registry + drift monitor. Area *content* stays with each doc's CODEOWNERS group. |
| 4 | **`doc_id` scheme** | **`HAIOS-<AREA>-<nnn>`** (e.g. `HAIOS-GOV-012`, `HAIOS-PROC-004`). Areas from the existing `docs/` tree: `GOV` (governance), `PROC` (process), `VIS` (vision), `TEST` (testimony), `TL` (timeline), `OPS`. F/H/IC research classes keep their existing IDs, registered as-is. |

### 10.2 Activation principle — *reuse the audit, don't restart*

The most beneficial and constructive activation is **not** a big-bang rollout. It **converts the S070126 audit's outputs into the living control system**, proves it on one repo, then extends. Value lands in the first move; disruption stays near zero.

```
T2 reconciliation map (71 pairs)  ──►  document-registry.yaml   (already-done work becomes the SSOT)
T1 inbox triage (1653 bucketed)   ──►  intake pipeline seed     (the triage becomes repeatable)
T3 scope audit (5 repos)          ──►  per-repo rollout order   (audit tells us where to extend)
```

### 10.3 Constructive activation sequence

| Move | Action | Why it's the highest-leverage first step | Owner |
|---|---|---|---|
| **A1 — Seed** | Script the 71 reconciled pairs into `document-registry.yaml` (canonical resolved from T2); add frontmatter to those canonical copies | Turns a one-off audit report into a **living artifact** on day one — immediate, visible value with zero new content work | mesh-support |
| **A2 — Pilot** | Stand up the errors-only CI + CODEOWNERS + branch protection on **`operations` only** | Prove the gate on the hub repo before touching the other 4; contained blast radius | mesh-support |
| **A3 — Scaffold** | Ship a `new-doc` template + the frontmatter validator + a one-command local pre-check | Removes contributor friction *before* the gate can frustrate anyone — constructive, not punitive | mesh-support |
| **A4 — Intake** | Turn the T1 triage into the standing pipeline (§3.5); drain `_inbox_files*` to zero-or-quarantine | Stops the backlog re-accumulating; closes the loop the audit opened | area owners |
| **A5 — Extend** | Roll the reusable CI to the remaining 4 repos, one per cycle, in audit-scope order | Incremental, each repo learns from the last; never a synchronized cutover | mesh-support |
| **A6 — Monitor** | Enable the scheduled drift monitor (§5) across all registered repos | The audit becomes a **sensor**, not a periodic fire drill | mesh-support |
| **A7 — Ratchet** | Promote Vale warnings→errors; add availability publish (P5) if wanted | Tighten only after adoption is comfortable | maintainer |

### 10.4 First tangible deliverable (the "activate now" kit)

To move from plan → live, the concrete artifacts to create next (all in `operations`):

1. `document-registry.yaml` — seeded from the 71 pairs
2. `.doc-control/frontmatter.schema.json` + `validate.py` (or a tiny CI script)
3. `.github/workflows/document-control.yml` — errors-only to start
4. `CODEOWNERS` — area groups
5. `docs/_templates/controlled-doc.md` — frontmatter scaffold
6. `CONTROLLED_DOCUMENTS.md` — the human-readable index rendered from the registry

> These 6 files *are* Phase 1+2. Say the word and I can generate the starter kit (schema, validator, CI workflow, template, and a registry seeded from the reconciliation map) as the next transaction.

---

### Appendix — mapping to ISO 9001 §7.5 (traceability)

| §7.5 requirement | This plan |
|---|---|
| Identification & description | frontmatter `doc_id/title/revision/owner/date` (§3.1) |
| Review & approval before release | CODEOWNERS + `approved` PR gate (§3.4) |
| Availability at point of use | published canonical set (P5) + registry |
| Prevent obsolete use | `superseded`/`retired` states (§3.3) |
| Protection & retention | git history + `retention` key + branch protection |
| Control of changes | PR + revision bump + approval record (§3.3–3.4) |
