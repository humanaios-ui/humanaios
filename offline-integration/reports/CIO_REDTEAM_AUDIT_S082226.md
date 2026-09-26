# CIO Red-Team Critical Audit — GitHub Estate, humanaios-ui
**Artifact ID:** CIO-AUDIT-S082226-01 · **Classification:** Board of Trustees / Z2 review
**Zone provenance:** Drafted Z1 · Ratification Z2 (Night) · Landing Z3 → `humanaios-ui/operations`
**Session date:** 2026-08-22 · **Method:** GET-only authenticated API sweep, live-fetch + SHA256 pin (IC-030), pre-registered composite ranking
**Counted cycle:** YES — includes folded `skill_scan --remote` arm (ruling recorded §0.3)

---

## 0. Governance preamble

### 0.1 Token disposition — ACTION REQUIRED
The PAT used for this audit was transmitted in conversation plaintext and is **burned**. Granted scope was `public_repo`, which confers **read AND write** on public repositories — broader than the declared read-only intent. This audit self-imposed a GET-only discipline (zero mutating calls; verifiable against the GitHub audit log). **Board action: revoke the token immediately post-review.** Filed as IC-CAND-token-scope-overreach (§9).

### 0.2 Pre-registration receipts
| Artifact | SHA256 |
|---|---|
| `ranking_formula_v1.md` (locked before scoring) | `00a3b53ddececebf52b62ffc9ca633e0ad6ee973853cbca6c4850208f4616bd5` |
| `REGISTERED.md` (live fetch, Aug 15 state) | `40391062966c6d6f9e29819a56ba1b87a035146e9d962a331d33de0aa8069029` |
| `repos.json` (90-repo listing) | `9f9e5f53d27b1b2b45bff693281a5a50f20c69f07c223638cc11aaa7eb29ce7b` |
| `ranking.json` (composite scores) | `e993a57b74dcace2b76bb18f6a114602488755ef1e0ce59b5a11764f6eb4296f` |
| `skill_scan_remote.json` | `bac5f30e5be3ed61ba126abcf54915c583e65c0c3190d9c4146ef6342c35c37c` |

### 0.3 Scope-coupling ruling (Z1, delegated by Z2)
The pending `skill_scan_v1_0.py --remote` arm was **folded into this cycle**. Rationale: one token lifetime, one exposure window, one counted cycle. Note the recursion: the scan could not run *via* `skill_scan_v1_0.py` because that tool is absent from the repo (§6, V3) — the remote arm was executed as an equivalent authenticated code-search sweep. The tool-absence is itself a top finding.

---

## 1. Executive summary (board-facing)

The `humanaios-ui` GitHub estate is a **90-repository personal account** (not an organization) operated by a **single human contributor**, exhibiting simultaneously: (a) an unusually sophisticated governance-and-verification methodology, and (b) a live enforcement layer that **does not match its own documented claims**. The audit's central finding is a **claims-vs-artifacts gap**: 8 of 9 program-critical tools cited in operating memory are absent from the canonical repo; the claimed Z2 ratification CI gate does not exist; the flagship scoring tool exists as a 242-byte stub diverging from a 20.8KB unversioned sibling; and all 4 methodology documents linked from the register-submission roadmap are phantoms. This is precisely the failure mode the program's own Claim 4′ predicts: *recursion without the in-loop verification read equals drift*. The verification read has now been performed; the drift is quantified below.

Countervailing strengths are real: append-only registry discipline is live and CI-validated, 36 workflows run in `operations`, licensing hygiene is strong (Apache-2.0 / MIT / CC-BY-4.0 across the estate), a secret-scan workflow exists on the product repo, and 88 SKILL.md agent-skill files represent a genuine, unusual asset. The organization's niche claim (standing public first-person evaluator process-failure register) remains supported.

**Top-line risks, ranked:** (R1) bus factor = 1; (R2) tool-landing pipeline failure — session artifacts never reach Z3; (R3) governance enforcement is procedural, not mechanical (F-45 confirmed live, worse than recorded); (R4) 90% fork noise obscuring the 9-repo real estate; (R5) "Empirica" naming collision exposure for getempirica.com.

---

## 2. Organization: what the estate actually is

| Dimension | Finding |
|---|---|
| Account type | **User** account (`humanaios-ui`), created 2026-02-07 — not a GitHub Organization. No org-level teams, no org security policies, no SSO, no fine-grained role separation. Zone discipline has no platform substrate to bind to. |
| Repo census | 90 public repos: **9 original, 81 forks (90%)**. Forks span reference material (awesome-lists), evaluation frameworks (inspect_ai, SWE-bench, SYCON-Bench), agent platforms (openhands, autogen, langgraph, dify), and infra (ollama, sonarqube, scorecard). |
| Contributor concentration | `operations`: humanaios-ui 772 commits, Copilot 82, dependabot 18, ecc-tools 11, github-actions 3. **One human.** |
| Velocity | 100+ commits to `operations` in the trailing 30 days — high single-operator throughput. |
| The real estate | `operations` (canonical process, 1,200 files), `humanaios` (product platform, 679 files, NestJS/TypeScript), `lasting-light-ai` (ACAT assessment site, 280 files), `research` (frozen publication snapshots, 27 files, CC-BY-4.0), `docs`, `ACAT-Dashboard`, `acat-inspect`, `acat-x`, `findlocaltattooartists`. |

**Learning opportunity:** the fork corpus is not waste — it is a curated research surface (it fed the six context-mitigation strategies previously ratified). But it is *unlabeled* as such. A `FORK_INDEX.md` declaring purpose-of-fork per entry would convert noise into a documented research asset and cut future audit cost.

---

## 3. Composite ranking — top 5 (pre-registered formula v1.0)

`score = 0.40·N(authored_commits) + 0.35·N(registry_refs) + 0.25·N(recency)`

| Rank | Repo | Score | Authored commits | Registry refs | Last push |
|---|---|---|---|---|---|
| 1 | `operations` | 0.783 | 772 | 16 | 2026-08-20 |
| 2 | `humanaios` | 0.628 | 312 | 36 | 2026-08-19 |
| 3 | `empirica` (fork) | 0.358 | 0 | 42 | 2026-06-24 |
| 4 | `lasting-light-ai` | 0.251 | 444 | 1 | 2026-07-15 |
| 5 | `research` † | 0.230 | 5 | 26 | 2026-07-08 |

† **Edge case routed to Z2 with both readings intact.** Mechanical application of formula v1.0 produces a 6-way tie at rank 5 (score 0.250) among zero-authored-commit forks whose scores derive entirely from fork-sync recency — the pre-registered tie-break (C1 desc, non-fork) cannot separate identical zeros. **Reading A:** rank 5 = unresolvable degenerate tie block. **Reading B (applied provisionally):** rank 5 = `research`, the next repo with nonzero utilization. Z2 ratification of Reading B requested; formula defect filed as IC-CAND-ranking-recency-inflation with a v1.1 fix pre-drafted (§10).

Notable: `empirica` earns rank 3 with **zero authored commits** — purely on 42 registry references. The program's dependency on an unforked-upstream capability it does not author is itself a strategic datum (§8).

---

## 4. Condition of the estate — per-repo audit

### 4.1 `operations` — canonical process repo (rank 1)
**Description (self-declared):** "Canonical operating process for HumanAIOS — class 2/3 source of truth… ai-behavioral-calibration, llm-observability, behavioral-telemetry, hitl-routing, ai-alignment-measurement, rlhf-inflation, eu-ai-act-compliance, learning-index." License Apache-2.0.

**Strengths:** 36 CI workflows including `findings-registry-gate.yml` (BLOCKING validator on `REGISTERED.md`), drift-monitor, scorecard, semgrep-review, sonarqube trio, scheduled audits, no-op-PR guard. CODEOWNERS present. Append-only registry live at 3,909 lines with schema v2.1 addendum discipline visible in the header.

**Defects (verified live):**
- **Root sprawl:** dozens of ALL-CAPS markdown files at repo root; no consistent `docs/` consolidation. Discoverability cost compounds per file.
- **Hygiene:** `.DS_Store`, `Archive.zip`, `Archive 2.zip` committed. Filename typo `ACAT_ASESSEMENT_SEED.md` frozen into history and any inbound links.
- **CODEOWNERS ×3** (root, `.github/`, `tools/org-defaults/`) — GitHub honors one; the others are drift vectors.
- **Tests are prose:** "test" hits are markdown test *plans* (`TESTING_PHASE_COMPLETE.md` etc.), not executable suites. CI validates the registry file format but not tool behavior.
- **36 workflows on a bus-factor-1 account** is itself a risk: maintenance surface exceeds maintainer bandwidth.

### 4.2 `humanaios` — product platform (rank 2)
**Description:** "AI-human orchestration platform. Workers complete real-world tasks delegated by AI agents. Pre-launch R&D phase. Cherokee Nation citizen-founded. Apache 2.0. 100% of profits fund recovery programs." Topics: nestjs, typescript, mcp, monitoring, physical-exchange, recovery.

**Strengths:** clearest product identity in the estate; `secret-scan.yml` present (only repo with one); registry-mirror-sync workflow ties product repo to canonical registry; CHANGELOG maintained; testimony/traditions compliance docs indicate a coherent mission layer (12-Traditions decision filter) rare in early-stage repos.
**Defects:** same root-sprawl and `.DS_Store` pattern as `operations`; integration-test artifacts are again markdown result narratives, not CI-run suites; "Pre-launch" status with 679 files and no visible deploy pipeline in workflows (5 workflows, none deployment).

### 4.3 `empirica` — fork of `EmpiricaAI/empirica` (rank 3)
"Make AI agents and AI workflows measurably reliable. Epistemic measurement, Noetic RAG, Sentinel gating." MIT. Proper engineering shape: Dockerfiles, docker-compose, real `tests/` with pytest files, ci/dependency-scan/release workflows, ARCHITECTURE.md, SECURITY.md. **Zero commits authored by humanaios-ui** — the fork is a consumed dependency, not a contribution surface, despite 42 registry references (highest in the estate). See §8 naming-collision finding.

### 4.4 `lasting-light-ai` — ACAT assessment platform (rank 4)
"AI Governance Awareness Assessment Platform." Apache-2.0, HTML front-end, ACAT schema v5.2, VALIDATION_PLAN.md, PRIVACY.md, SECURITY.md, CODE_OF_CONDUCT — the most complete *policy* file set in the estate. Defects: a binary `.docx` research paper committed to the repo (belongs in `research/` or a release asset); a non-ASCII root entry (`The Witness Stand · NEXUS-φ`) that will break naive tooling and some filesystems; only 2 workflows, one of which is the sole executable-looking test (`acat-bot-test.yml`) in the top 5.

### 4.5 `research` — publication snapshots (rank 5, Reading B)
27 files, CC-BY-4.0, "frozen-at-publication snapshots." Clean, minimal, correctly licensed for academic reuse. Defect: no CI at all — even a checksum-freeze verification workflow would mechanically enforce the "frozen" claim rather than asserting it.

---

## 5. Skill scan — folded `--remote` arm (V5)

**88 SKILL.md files across 4 repos** (all original, none in forks): `operations` 81, `humanaios` 3, `lasting-light-ai` 2, `research` 2. Full inventory pinned in `skill_scan_remote.json`.

Assessment: the skill corpus is a genuine differentiating asset — 81 agent-operable skills co-located with the canonical process is an unusually deep automation substrate. Risks: (a) skills are concentrated in one repo on a bus-factor-1 account; (b) at least one skill directory (`tools/skills/acat_dimension_scorer/`) wraps a tool whose implementations are unversioned and diverging (§6 G2) — a skill pointing at unstable ground; (c) no skill-level version pinning was observed at scan depth, so skill↔tool contract drift is undetectable mechanically.

---

## 6. Verification ledger — claims vs. live artifacts

| ID | Claim under test | Live result | Verdict |
|---|---|---|---|
| V1 | Two diverging unversioned `acat_dimension_scorer` copies | **Three** artifacts: `acat/scoring/` copy, `tools/` copy, plus `tools/skills/acat_dimension_scorer/SKILL.md` | CONFIRMED-EXTENDED |
| V2 | `REGISTERED.md` cites nonexistent `acat_dimension_scorer_v1_1.py` (prev. reported: 15 refs) | Live count: **6** citations; file still nonexistent | CONFIRMED core / count drift disclosed (6 ≠ 15) |
| V3 | Program-critical tools present in repo | `mdu_score.py`, `grbs_orchestrator.py`, `roi_pilot_v1.md`, `claim_lint_v1_0.py`, `keenable_verified_fetch_v1_1.py`, `registry_fmea_v1_0.py`, `repo_audit_v1_0.py`, `skill_scan_v1_0.py` — **all ABSENT**. Only `.doc-control/validate.py` present. **8/9 missing** | CRITICAL — worse than prior "5 absent" |
| V4 | `z2_ratification_gate.yml` exists as CI enforcement | **ABSENT.** `findings-registry-gate.yml` exists but is a *format validator* (ID collisions, status violations); it contains no Z2/ratification logic | CRITICAL — phantom gate |
| G2 | Scorer copies diverge | 242 bytes vs 20,811 bytes; **neither** implements IC-056 introspective-reliability discount | CONFIRMED — copy A is a stub |
| G3 | Four phantom methodology docs linked from roadmap | `REGISTER_SUBMISSION_ROADMAP.md` links 4 docs (`METHODOLOGY`, `IMPLEMENTATION`, `CASE_STUDY`, `SCORING_RUBRIC`); **4/4 unresolved** | CONFIRMED exactly |
| G4 | — | Single human contributor; 100+ commits/30d | Bus factor = 1 |

**Interpretation (the audit's spine):** the recurring pattern is **session-built artifacts that never landed at Z3**. Tools built, pinned, and receipted in-session exist in conversation transcripts and outputs directories — not in the repository the registry cites. The Z1→Z3 landing pipeline is the broken link. Claim 4′ holds: the recursion (build → cite → build atop) proceeded without the verification read; this audit *is* the read.

---

## 7. Production-grade service candidates

Ranked by distance-to-production, red-team adjusted:

1. **ACAT assessment platform** (`lasting-light-ai` + `ACAT-Dashboard` + `acat-inspect` + `acat-x` + `research`). Nearest to shippable: live HTML assessment flow, schema v5.2, validation plan, published research snapshots, an MCP endpoint already declared (`api.humanaios.ai`). Blockers: scorer versioning chaos (G2) sits at the *core of the product's credibility claim* — an assessment platform whose own scorer is an unversioned stub is a red-team headline. Fix before any external pilot.
2. **HumanAIOS orchestration platform** (`humanaios`). Real framework (NestJS), real mission differentiation, secret scanning, registry sync. Blockers: no deploy pipeline, no executable test suite, pre-launch with no staging evidence in CI. MDU/LRU pipelines (designed to v0.2 parity) have **no landed code** — they exist only as process documents plus absent tools (V3).
3. **Governance-as-a-product** (the `operations` methodology itself). The registry discipline, findings gate, drift monitors, and 81-skill corpus are collectively a sellable compliance/assurance capability (see §8, EU AI Act lane) — *if* the enforcement gap (V4) is closed. Selling governance tooling while your own Z2 gate is phantom is an existential credibility risk; it is also the cheapest fix in this report.
4. **F-51 external replication kit / DASE collaboration** — research-capital products, contingent on OI-1/OI-3 rulings still open.

---

## 8. Market analysis

**Serviceable lanes, from live repo evidence (descriptions, topics, artifacts):**

- **AI assurance & audit / EU AI Act compliance.** `operations` self-tags `eu-ai-act-compliance`, `ai-alignment-measurement`, `llm-observability`. The Act's high-risk-system conformity-assessment regime creates recurring demand for exactly the artifact class this estate produces (pre-registered rubrics, append-only registers, evidence-tier provenance). Strongest product-market fit on paper; gated on §6 remediation.
- **Human-in-the-loop task orchestration.** `humanaios` (workers completing AI-delegated real-world tasks) competes in the lane occupied by RentAHuman — a service this program *already consumes via MCP*. Dual posture (customer + competitor) needs a deliberate strategy ruling: partner-integrate, differentiate on the recovery-economy mission, or both.
- **AI evaluation & behavioral benchmarking.** Fork curation (inspect_ai, SWE-bench, SYCON-Bench, sycophantic-ai-benchmark) plus ACAT positions the org for third-party model-behavior assessment — the buyer being enterprises and model providers needing independent behavioral attestation.
- **Impact-capital / social-enterprise lane.** Cherokee Nation citizen-founded + 100%-of-profits-to-recovery is a durable differentiator for grant funding, Native business programs, and ESG-aligned procurement — a financing channel most competitors cannot access. It appears in the repo description but nowhere as a formalized capital strategy document; that is a gap and an opportunity.
- **Buyer #2 shortlist (OI-5, open):** this audit's evidence supports adding *AI-audit boutiques and EU-market compliance consultancies* to the shortlist — they buy methodology artifacts wholesale.

**Strategic risk — naming collision (new finding).** The Empirica dependency is a fork of `EmpiricaAI/empirica`; a separate, established academic platform also operates under the Empirica name. Branding **getempirica.com** atop a name attached to at least two prior operators is a trademark/SEO/identity-confusion exposure. Route to Z2 alongside OI-6 (licensing scope) as a paired naming-and-licensing ruling before productization.

---

## 9. Registry Candidate Block (humanaios-findings-scan format)

```
REGISTRY CANDIDATE SCAN (humanaios-findings-scan)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Registry fetched live: REGISTERED.md @ sha256 40391062…9029 (Aug 15 2026 state)

F candidates:
  · [F-CAND-tool-landing-gap] Z1→Z3 landing pipeline failure — NEW
      (EXTENSION-relation to prior "five tools absent" finding; supersedes-pointer needed)
    evidence: V3 — 8/9 cited tools absent from live tree; API tree fetch pinned
    promotion gate: independent re-verification after one remediation PR lands
  · [F-CAND-scorer-stub-divergence] 242B stub vs 20.8KB impl, IC-056 absent both — NEW
    evidence: G2 — sha 6651fa14… vs 7400d383…, live raw fetches
    promotion gate: reconciliation PR merged with versioned filename + IC-056
  · [F-CAND-fork-noise-90pct] 81/90 repos are forks; utilization signal polluted — NEW
    evidence: repos.json pinned 9f9e5f53…
    promotion gate: FORK_INDEX.md landed or Z2 declines
  · [F-CAND-bus-factor-one] single human contributor across canonical estate — NEW
    evidence: G4 contributor API
    promotion gate: mitigation ruling (org migration / second maintainer / escrow)

IC candidates:
  · [IC-CAND-token-scope-overreach] PAT scope public_repo (write-capable) vs
      declared read-only intent; token also chat-plaintext — principle: least-authority
    Fix → least-authority credential issuance; fine-grained read-only PATs only;
      revoke current token post-review.
  · [IC-CAND-z2-gate-phantom] claimed z2_ratification_gate.yml nonexistent; only a
      format validator gates the registry — principle: F-45 (enforcement locus in code)
    Fix → Principle F-45: implement actual Z2 approval gate (CODEOWNERS-required
      review on REGISTERED.md path + environment-protection approval), single
      CODEOWNERS location.
  · [IC-CAND-ranking-recency-inflation] formula v1.0 recency term inflates
      zero-authored forks; tie-break underspecified — principle: pre-registration
      completeness
    Fix → pre-register v1.1: gate C3 on C1>0; explicit degenerate-tie rule.
  · [IC-CAND-registry-count-drift] live phantom-file citation count (6) diverges
      from previously reported count (15) — principle: N-reporting fidelity
    Fix → recount methodology pinned; reconcile which count was measured against
      which registry state.

H candidates:
  · [H-CAND-root-consolidation] null: consolidating root-level .md sprawl into
      docs/ does not reduce unresolved-link rate / falsification: unresolved-link
      count unchanged ±10% after consolidation PR / metric: link-resolution rate
      via automated link-check CI / promotion gate: one consolidation PR + one
      scheduled link-check run.

NM low-friction captures (expire after 3 audits → DRIFT_LOG.md):
  · .DS_Store + Archive.zip ×2 committed (operations, humanaios) — hygiene, below IC bar
  · Filename typo ACAT_ASESSEMENT_SEED.md — cosmetic, link-rot vector
  · CODEOWNERS in 3 locations — drift vector, below IC bar pending G-gate fix
  · Non-ASCII root entry in lasting-light-ai — tooling-compat hazard
  · .docx binary committed to lasting-light-ai — belongs in research/ or releases
  · research/ "frozen" claim unenforced (no checksum CI)
  · Markdown test *plans* standing in for executable suites (top-5-wide pattern)

DUPLICATE / already-registered (cited, not proposed):
  · Phantom roadmap docs (4/4 confirmed) → covered by existing d1f b5f0-audit finding
  · Zone discipline procedurally-not-mechanically enforced → covered by F-45/F-45-EXT
    (IC-CAND-z2-gate-phantom filed as the *extension*: claimed gate is phantom)

Scan completeness: 4 F-cand / 4 IC-cand / 1 H-cand / 7 NM from
  21 substantive observations scanned

Routing: all candidates → Zone 2 (Night) for ratification per P21.
This block proposes; it does not register.
```

---

## 10. Remediation plan — CQI sequence (proposed, Z2 to ratify order)

**Wave 1 — credibility-critical (this week):**
1. Revoke the PAT; reissue fine-grained read-only tokens per task.
2. Land the 8 absent tools from session outputs → `tools/` with versioned filenames + SHA receipts in commit messages. This single PR resolves V3 and converts 6 registry citations from phantom to live.
3. Reconcile scorer: promote the 20.8KB copy to `acat_dimension_scorer_v1_1.py`, implement IC-056, delete the 242B stub, update the SKILL.md wrapper pin.
4. Replace phantom Z2 gate with a real one: single CODEOWNERS, required-review branch protection on `REGISTERED.md` and `tools/`, environment approval for registry-touching workflows. (F-45 gap closes mechanically.)

**Wave 2 — structural (this month):**
5. Create the 4 phantom methodology docs or delete the roadmap links (no third state).
6. `FORK_INDEX.md` with purpose-of-fork per entry; archive dormant forks (>12mo untouched: ~15 candidates).
7. Migrate `humanaios-ui` User account → GitHub **Organization**: unlocks teams, org-level security policy, and a platform substrate for zone separation; directly mitigates bus-factor exposure via role-based second-maintainer onboarding.
8. Repo hygiene PR: remove `.DS_Store`/zips, fix typo via redirect stub, relocate `.docx`, rename non-ASCII entry.

**Wave 3 — assurance (next quarter):**
9. Executable test suites replacing markdown test narratives; wire into existing CI.
10. Checksum-freeze CI on `research/` to mechanically enforce "frozen-at-publication."
11. Formula v1.1 pre-registration for the next counted ranking cycle.
12. Naming/licensing paired ruling on Empirica ↔ getempirica.com (with OI-6).

**Standing CQI instrument:** re-run this audit's verification ledger (V1–V5, G1–G4) as a scheduled quarterly workflow — the checks are all scriptable GET calls. Drift between claims and artifacts becomes a monitored metric instead of a discovered surprise.

---

## 11. Closing statement to the Board

The estate's weakness is not capability — it is **consummation**. Nearly every defect found here is a designed control that was documented but never landed, or landed once and never versioned. The program's own doctrine names this exactly (Claim 4′), and the fix is the program's own discipline applied to itself: every session close must include a Z3 landing verification against the live tree, not against session memory. Wave 1 is four PRs. After Wave 1, the gap between what this organization *says* it enforces and what it *mechanically* enforces drops to near zero — and at that point the governance methodology stops being a liability under audit and becomes the product.

*— Z1, acting CIO capacity. All rulings, ratifications, and landings remain Z2/Z3 authority.*
