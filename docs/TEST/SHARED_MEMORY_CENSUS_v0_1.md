---
doc_id: HAIOS-TEST-010
title: Shared Memory Census V0.1
revision: 1
status: draft
owner: "@carly"
created_date: 2026-09-02
review_due: 2026-12-01
canonical: true
retention: permanent
---
# SHARED_MEMORY_CENSUS_v0_1 (method) + docs/ application + system plan
Read: operations/main, 2026-08-31 (VERIFIED-LIVE). Evidence: docs_context_map.json. Z2 record: findings 1–5 of TOOLS_MEMORY_COMPRESSION_MODEL_v0_1 ratified as candidates 2026-08-31; falsification pass (20-tool human read) reserved to Z2.

## 1. The method, named: Shared-Memory Census (SMC)
Seven mechanical steps; author judgment enters only at step 6, and step 7 bounds the method's own blindness.
1. **UNITS** — enumerate the population (tools, docs, workflows, skills…).
2. **EXTRACT** — grep quoted/inline artifact references per unit. Mechanical, no interpretation.
3. **GRAPH** — bipartite map: units ↔ stores. An edge is shared context; a store with ≥2 units is shared memory.
4. **TIER** — classify each store: L0 working (session/context), L1 short-term (per-unit outputs), L2 long-term (governance docs, REGISTERED.md), L3 commitments (roots, anchors).
5. **METRICS** — isolation rate (units with no shared store), consolidation paths (L1→L2), chain coverage (prev-hash / Merkle), dangling rate (references to absent files).
6. **FINDINGS** — read the metrics through the compression lens: every unit is a compressor; a finding exists only in a store another process reads.
7. **FALSIFIER** — the census sees paths, not consumption; a human read of a sample bounds the grep blindness before anything is built on the numbers.

## 2. Applied to docs/ (103 files, 96 md/html units)
| metric | tools/ (prior run) | docs/ (this run) |
|---|---|---|
| isolation rate | 52% reference nothing shared | 27% reference nothing |
| spine attachment | 14/109 touch REGISTERED.md | **33/96 reference REGISTERED.md**; 12 GOVERNANCE; 11 SESSION_RITUALS; 11 CURRENT |
| unit → executable | n/a | 16/96 reference a live tool/workflow |
| dangling references | 31 root docs (prior index) | **top dangling: assess.html (7 docs), acat_dimension_scorer_v1_1.py (5), PRINCIPLES_SEED.md (5), vc_signer.py / did_generator.py / human_score_vc_route.py (3 each)** |
| session-stamped filenames | — | 18/96 carry S-###### stamps (session exhaust filed as durable memory) |

**Finding D1 (F/IC candidate).** The failure modes are inverse and complementary: tools are *orphaned writers* (compress into stores nobody reads); docs are *dangling pointers* (index entries to memory that was never allocated or was freed). Same root cause as the phantom-tools IC — the durable layer and the working layer diverge without a resolver.
**Finding D2.** The docs layer is the system's real associative memory: it attaches to the registry spine 2.3× better than the tools layer does. The prose remembers; the code forgets.
**Finding D3.** A verifiable-credentials subsystem (vc_signer, did_generator, human_score_vc_route, human_score.schema.json) exists in documentation at ≥3-doc density with no corresponding executables on main — a coherent LAID-on-paper subsystem never landed. Registrable as its own gap.
**Finding D4.** 18 session-stamped files in docs/ are L0 material stored at L2. Memory tiers are being mixed by filing location.
Falsifier for D1–D4: a 15-doc human sample showing the dangling targets live in another repo or branch (the census is single-repo) collapses D1/D3 to a cross-repo indexing gap.

## 3. Verdict on the method
Beneficial: yes. Two runs produced four ratified-candidate findings plus three new ones, each with a number attached and a bounded falsifier, at ~1 founder-hour per run. Its value is that it finds *structural* memory failures (orphans, dangles, tier-mixing) that no amount of per-file review would surface. Its limit is consumption-blindness (step 7) and single-repo scope.

## 4. System-wide application plan (awaiting Z2 hash)
| pass | population | expected failure class | est. hours | order rationale |
|---|---|---|---|---|
| P1 | .github/workflows (36) | orphaned crons: scheduled compressors whose outputs land in stores nothing reads | 1 | code-woken layer; runs unattended, so orphans cost silently |
| P2 | skills (.agents/skills, both repos) | skills referencing rituals/files that moved | 1 | skills are the session-woken instruction memory |
| P3 | humanaios repo (573 files) + **cross-repo edge pass** | dangling refs that actually resolve across repos (tests D1/D3 falsifier mechanically) | 2 | closes the census's biggest blindness |
| P4 | acat/, h-acat/, instruments/, autonomy/gates/ | duplicate stores (scorer copies), tier-mixing | 1.5 | highest duplication risk observed |
| P5 | REGISTERED.md itself as a store | entries pointing at absent evidence files (evidence-dangling) | 1 | joins SMC to claim_reach_lint: reach tier × dangling evidence |
| P6 | consolidation build | one hash-chained events file per domain; Merkle coverage extended; census re-run as the measure | 4 | only after P1–P5 fix the map; census before/after is the KEEP/REVERT metric |
Standing form: `smc_census_v0_1.py` (steps 1–5 as code, emits metrics JSON), run by a scheduled workflow monthly; deltas route to Findings Scan. The census then becomes a compressor whose output *is* consolidated — it must pass its own test.
prior_P that P1–P5 surface ≥3 further registrable findings: 0.8. prior_P that P6's after-census shows orphan rate <10%: 0.6.

## Open for Z2
- Number D1–D4 alongside the ratified tools findings, or hold pending the two falsification passes (Z2's 20-tool read; P3 cross-repo pass).
- Ratify the SMC name and seven steps as the method of record.
- Ratify plan order P1→P6 or reorder; P3 can run first if closing the blindness matters more than the silent-cost layer.
