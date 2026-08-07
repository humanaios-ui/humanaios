# Partner Connection & Lessons Plan — Top 10 GitHub Repositories

**Status:** DRAFT — Z2 ratification pending
**Scope:** Concretizes `docs/COLLABORATION_DISCOVERY.md` from org-level to repo-level for the AI behavioral evaluation lane.
**Provenance:** All 10 repositories verified accessible (HTTP 200) at plan drafting time. Rankings and lesson targets derived from live repo inspection during drafting session, including `tools/acat_dimension_scorer_v1_2.py` (DIMENSIONS_12) and the inspect_evals Register model requirements.
**Companion artifact:** `acat_x_consist.py` (ACAT-X consist task skeleton, verified against inspect_ai 0.3.251).

---

## Plan structure

Each entry defines four fields:

- **Lessons** — what HumanAIOS extracts (study output, mapped to ACAT dimensions or infrastructure where applicable)
- **Connection** — the concrete first engagement action (issue, PR, register submission, or study-only)
- **Offer** — the public artifact HumanAIOS brings (per COLLABORATION_DISCOVERY Z2 decision item 2)
- **Exit criteria** — what "done" means, so engagements close instead of drifting

Engagement tiers: **ACTIVE** (two-way engagement intended), **CONTRIBUTE** (one PR/issue-scale touch), **STUDY** (extract lessons; no engagement required).

---

## Phase 1 — Target & Framework (Weeks 1–4)

### 1. UKGovernmentBEIS/inspect_evals — ACTIVE

- **Lessons:** The registrable-eval bar: pinned external assets, arXiv-backed tasks, `pyproject.toml` + `uv sync` installability, 40-char commit SHA pinning, the Register issue-form workflow end to end.
- **Connection:** Submit ACAT-X via the Register Eval Submission issue form once the four clean-translation tasks (truth, syc, consist, harm) pass local `inspect eval` runs. Before submission, open one small clarifying issue if any register requirement is ambiguous — this establishes presence non-transactionally.
- **Offer:** ACAT-X eval suite (repo-hosted, registered — the eval stays in `humanaios-ui/humanaios` per the Register model).
- **Exit criteria:** ACAT-X accepted into the register, or a documented rejection with reasons captured as a finding candidate.

### 2. UKGovernmentBEIS/inspect_ai — CONTRIBUTE

- **Lessons:** Solver/scorer/reducer decomposition; the `Epochs` reducer mechanism (already applied in `acat_x_consist.py`); log-viewer and scoring-workflow patterns for re-scoring existing transcripts (`inspect score`) — relevant to retroactively scoring the existing ACAT corpus.
- **Connection:** Study first. Contribute only if ACAT-X development surfaces a genuine framework gap (e.g., a reducer edge case) — then file a minimal-repro issue. Do not manufacture a contribution.
- **Offer:** High-quality bug reports with reproductions, if and only if real ones emerge.
- **Exit criteria:** ACAT-X tasks run cleanly on current inspect_ai; any framework gaps filed upstream.

**Phase 1 gate (Z2):** Register submission is an external, identity-bearing action → Zone 3 execution (operator submits the issue form).

---

## Phase 2 — Dimension Methodology (Weeks 3–8, overlaps Phase 1)

### 3. stanford-crfm/helm — STUDY

- **Lessons:** Calibration metric implementations (expected calibration error, selective accuracy) → the published operationalization closest to the **humility** dimension. Also: multi-metric presentation without collapsing to a single score — relevant to how ACAT reports 12 dimensions without over-summarizing.
- **Connection:** Study-only initially. If HELM's calibration metrics get adapted into an ACAT-X humility task, cite HELM in the methods note; that citation is the connection.
- **Offer:** Methods note comparing HELM calibration scoring to ACAT humility scoring (publishable as a repo doc).
- **Exit criteria:** Humility task design doc exists, with an explicit adopt/adapt/reject decision on each HELM calibration metric.

### 4. anthropics/evals — STUDY

- **Lessons:** Model-written eval datasets for sycophancy and power-seeking → direct precedent for **syc** and **power**. Equal value in the negative lessons: known validity criticisms of model-written evals (surface-pattern artifacts), to be avoided in ACAT dataset construction.
- **Connection:** Study-only. Dataset reuse requires a license check before any ACAT-X task imports their data (Z2 decision).
- **Offer:** None required.
- **Exit criteria:** Written adopt/avoid list: which model-written-eval patterns ACAT-X uses, which it deliberately rejects, and why.

### 5. EleutherAI/lm-evaluation-harness — CONTRIBUTE

- **Lessons:** Community contribution culture at scale: versioned task YAML configs, the new-task PR review process, reproducibility norms (task versioning on every change).
- **Connection:** Port **one** ACAT-X task (truth is the best fit for their config format) as a new-task PR. Purpose is bidirectional: distribution for ACAT, and firsthand experience of a mature eval review process.
- **Offer:** One well-formed task contribution following their new-task guide.
- **Exit criteria:** PR merged, or review feedback captured and applied to ACAT-X regardless of merge outcome.

### 6. meg-tong/sycophancy-eval — STUDY

- **Lessons:** Paired-prompt flip-detection methodology: how pressure variants are constructed, how flips are detected and scored → the design template for the **syc** task.
- **Connection:** Study-only; small repo, likely low-maintenance mode. Cite in syc task design doc.
- **Offer:** None required.
- **Exit criteria:** Syc task skeleton exists using paired-prompt design, with divergences from this repo's method documented.

**Phase 2 gate (Z2):** License review for any third-party dataset reuse (items 4, 6) before code touches ACAT-X.

---

## Phase 3 — Infrastructure & Scoring Patterns (Weeks 6–12)

### 7. METR/task-standard — STUDY

- **Lessons:** Formal task-specification standard for agentic evals: how tasks are made substrate-agnostic and machine-checkable → applies to **handoff** dimension design and to SESSION_RITUALS' substrate-agnostic goals.
- **Connection:** Study-only. If the handoff task adopts their spec structure, note it; METR is already in COLLABORATION_DISCOVERY for a possible later org-level approach — repo study is the low-cost precursor.
- **Offer:** (Later, org-level) ACAT-P-style behavioral extraction findings, if a formal collaboration lane opens.
- **Exit criteria:** Decision recorded: does the handoff task adopt task-standard's spec format, yes/no, with rationale.

### 8. huggingface/lighteval — STUDY

- **Lessons:** Clean HF dataset integration with explicit `revision=` pinning inside eval pipelines → the pattern `humanaios/acat-assessments` consumption should follow in every ACAT-X task.
- **Connection:** Study-only.
- **Offer:** None required.
- **Exit criteria:** Every ACAT-X task loads its dataset with a pinned revision; pattern documented once in the eval repo README.

### 9. openai/evals — STUDY

- **Lessons:** YAML eval-registry structure and model-graded rubric patterns (the reference designs for judge-based scoring) → applies to **harm**, **humility**, **fair** tasks. Maintenance-mode status is itself a lesson: registry designs that outlive active maintenance.
- **Connection:** Study-only; repo is not accepting new evals. No engagement.
- **Offer:** None.
- **Exit criteria:** Judge-rubric template for ACAT-X model-graded tasks drafted, citing which openai/evals patterns were adopted.

### 10. centerforaisafety/hle — STUDY

- **Lessons:** Publishing calibration error *alongside* accuracy as a first-class result → a working example of scoring overclaim, the failure mode H-HUMILITY-MASTER-01 gates on. Informs how ACAT-X humility results should be reported, not just computed.
- **Connection:** Study-only.
- **Offer:** None required.
- **Exit criteria:** ACAT-X reporting format includes a calibration/overclaim column for the humility task, modeled on HLE's presentation.

---

## Sequencing summary

| # | Repo | Tier | Phase | Primary ACAT payload |
|---|------|------|-------|----------------------|
| 1 | inspect_evals | ACTIVE | 1 | Register acceptance bar |
| 2 | inspect_ai | CONTRIBUTE | 1 | Framework mechanics |
| 3 | helm | STUDY | 2 | humility (calibration metrics) |
| 4 | anthropics/evals | STUDY | 2 | syc, power (+ negative lessons) |
| 5 | lm-evaluation-harness | CONTRIBUTE | 2 | Review-process experience; distribution |
| 6 | sycophancy-eval | STUDY | 2 | syc (paired-prompt design) |
| 7 | METR/task-standard | STUDY | 3 | handoff; substrate-agnostic specs |
| 8 | lighteval | STUDY | 3 | Dataset revision pinning |
| 9 | openai/evals | STUDY | 3 | Judge-rubric templates |
| 10 | hle | STUDY | 3 | Overclaim reporting format |

Load check: only 3 of 10 involve outbound engagement (1, 2, 5); the remaining 7 are extraction-only and cannot stall on external parties. This is deliberate for a sole-operator org.

---

## Standing Z2 decisions required

1. Ratify this plan and its tier assignments.
2. Approve the Register submission as the Phase 1 anchor artifact (Zone 3 execution).
3. License review protocol for third-party dataset reuse (items 4, 6) before import.
4. Decide whether Apollo Research enters the plan later: their GitHub identity is ambiguous (two similarly-named orgs, `ApolloResearch` and `apollo-research`) and was **excluded from this plan pending identity verification** rather than ranked on an unverified assumption.
5. Cadence: proposed single monthly review of exit criteria at session close, rather than per-repo tracking overhead.

---

*Wado. 🦅*
