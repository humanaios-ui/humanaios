# Document-intelligence source audit: initial census

## Pinned inventory

The inventory in [`tracked-files.json`](tracked-files.json) enumerates the complete Git tree of default-branch `main` at commit
`ebe164d2d2170c154a7710d97c4590dbddf31f70`. It contains **976 tracked paths**.
The immutable tree is the census baseline; this is not a census of later PR
changes.

Every path has its Git mode, object type and object ID. Git tree membership does not prove that the referenced blob is locally readable. The census script uses
NUL-delimited `git ls-tree` output and does not follow symlinks. It labels
obvious compiled/binary types from mode, path, or suffix metadata only. This
classification is a triage hint, not content inspection.

| Item state | Count | Meaning |
|---|---:|---|
| Inspected/evidence-linked | 0 | No path has completed the requested per-file claim/dependency audit |
| Pending | 928 | 921 text/source candidates and 7 unclassified files not inspected or linked to an owner/control document |
| Metadata-only / excluded from content review | 48 | 45 `.pyc` compiled files and 3 binary/media files; exclusions have per-path reasons |
| Blocked within the pinned Git tree | 0 | No blocked objects are established by this metadata-only inventory; local blob accessibility has not been verified |

All records have `controlling_doc_id: PENDING` and `owner: PENDING`; no path is represented as source-linked or fully audited. Sensitivity is unassessed except for 81 path-name heuristic candidates, which still require content review. The path heuristic does not establish that a file is private or contains sensitive data.

The pinned tree listing contains only blob references with regular file modes (937
`100644`, 39 `100755`); no symlink or submodule entries were present.

To resume or create a new snapshot:

```sh
python3 scripts/document_intelligence_census.py \
  --commit <full-git-commit> \
  --output /tmp/tracked-files.json
```

The committed JSON remains the pinned baseline and is not silently refreshed
when the branch changes. A resumed audit must record a new checkpoint and
preserve reviewed, pending, excluded, and blocked states per path.

## Existing capabilities and source audit findings

Evidence below is limited to the named files and spans. It does not assert
deployment/runtime behavior or independent corroboration.

| Finding | Repository evidence | State |
|---|---|---|
| Document-control plan describes a five-repository ecosystem and names `humanaios-ui/operations` as the registry/control hub. | `DOCUMENT_CONTROL_PLAN.md` at this commit, lines 3–5 and 181–188 | **OBSERVED** as a plan; implementation/ratification not established |
| Two in-repository registries have different declared scope. The root registry calls itself the strategic-document enforcement point; `docs/document-registry.yaml` explicitly identifies `empirica-foundation-evaluator`. The plan instead identifies operations as the cross-repository hub. Do not select authority by filename or status alone. | `document-registry.yaml` lines 1–5; `docs/document-registry.yaml` lines 1–6; `DOCUMENT_CONTROL_PLAN.md` lines 181–188 | **CONFLICT / UNRESOLVED SCOPE** |
| An `approved` status is not sufficient evidence of ratification: the root registry's first entry says `status: approved` while its `approval_mark` says `NOT YET MARKED BY ADMIRAL` and its approval text says ratification is pending. | `document-registry.yaml` lines 6–16 | **CONTRADICTED** approval metadata; no effective ratification claimed |
| A document-control workflow exists, but its trigger only covers `docs/**/*.md` and the docs registry. Its frontmatter script enumerates only immediate files in `docs/`; nested documentation is not included. Its approval check inspects a commit-message `Reviewed-by:` string, not an authenticated owner review receipt. | `.github/workflows/document-control.yml` lines 3–8, 21–24, 74–84 | **OBSERVED** workflow source; successful CI/branch protection not established |
| The platform API controller code contains mock responses: agent listing returns an empty array, agent creation returns a timestamp-derived ID and fixed `test-user-id`, and auth register/login return `test-token-*` and a fixed admin user. `AgentsController` has no guard decorator; its module wires the controller without a guard, and `AppModule` has no global guard provider. A JWT guard class exists but is not wired in those modules. | `apps/api/src/agents/agents.controller.ts` lines 1–24; `apps/api/src/agents/agents.module.ts` lines 12–16; `apps/api/src/app.module.ts` lines 6–10; `apps/api/src/auth/jwt-auth.guard.ts` lines 1–9; `apps/api/src/auth/auth.controller.ts` lines 8–40 | **OBSERVED** source; runtime status **UNVERIFIED** |
| `START_HERE.md` describes the platform as pre-launch R&D with no live API or customers. That statement is consistent with the mock controller evidence above, but no deployment/runtime receipt was collected. | `START_HERE.md` lines 94–100 | **SUPPORTED** by source inspection only; runtime **UNVERIFIED** |
| The audit findings registry identifies `humanaios-ui/operations` and a pinned operations commit, and marks its entries with per-file coverage. It is not a platform-wide inventory or source authority for this repository. | `audit_findings_registry.yaml` lines 12–23, 25–43 | **OBSERVED**, scope limited to operations |
| `audit_findings_integrator.py` transforms findings with file/line metadata into empirica artifact nodes. Its current edges only link P0/P1 findings to one fixed CHECK decision; this is not a general code↔document dependency graph or reverse-impact index. | `audit_findings_integrator.py` lines 5–17, 60–86, 103–117 | Existing adapter **OBSERVED**; requested dependency/impact mapping **PENDING** |
| A registry gate checks allowed fields, signature hits, source IDs, attestation hashes, and licenses, with ACCEPT/QUARANTINE/CANDIDATE outcomes. Its inline synthetic stream is not evidence of a complete, resumable audit or a production integration. | `offline-integration/automation/cycle2_registry_gate.py` lines 9–28, 30–58 | Existing gate source **OBSERVED**; production integration **UNVERIFIED** |
| INTENT-OS has a browser-side export that downloads a JSON spec. A separate offline-integration README describes a dashboard→Flask bridge and calls `api_bridge_db.py` production. Its registry/state/harness routes have no authentication or authorization checks in the route functions; the documented startup script binds `0.0.0.0` and enables Flask debug mode. This is a source-verified access-control risk if the documented startup path is used; actual invocation and host/network controls are not verified. | `intent-os-universal-v2.html` line 203; `offline-integration/automation/README_API_BRIDGE.md` lines 3–18, 21–29; `offline-integration/automation/api_bridge_db.py` lines 283–311, 322–368; `offline-integration/automation/run_api_bridge.sh` lines 89–96 | **OBSERVED security concern**; deployed exposure **UNVERIFIED** |
| A Research Coordinator implementation describes aggregation, cross-practice pattern detection, and research routing. Its existence does not establish source-claim dependencies or reverse document impact. | `agent/research_coordinator.py` lines 3–8, 52–60 | Coordinator source **OBSERVED**; requested audit integration **PENDING** |
| Resource Miner integration is specified as “Ready for Implementation”; its narrative also claims a validated deployment. The specification is not a runtime receipt, and the inspected `apps/api/src` modules contain no Resource Miner controller. | `RESOURCE_MINER_INTEGRATION_SPECIFICATION.md` lines 1–13; `apps/api/src/app.module.ts` lines 1–11 | **CONFLICT / UNVERIFIED** operational claims |
| The repository has evidence-oriented readiness/gate code and tests, but this initial census has not established claim-to-source dependency indexing, document reverse-impact traversal, or integration with operations graph projections. | `src/gates/readiness_gates.py`; `src/gates/system_stance.py`; `tests/test_gates_integration.py` | Existing code/tests **OBSERVED**; requested graph/audit integration **PENDING** |
| A sampled scheduled Mesh-Sync-Batch run failed at output processing: the GitHub Actions log reports `Invalid format` after the workflow writes pretty-printed multiline JSON to `GITHUB_OUTPUT`. The run is on the pinned main commit; no retry or workflow change is included in this read-only first deliverable. | `.github/workflows/mesh-sync-batch.yml` line 103; [Actions run 39166287234](https://github.com/humanaios-ui/humanaios/actions/runs/39166287234) at commit `ebe164d2d2170c154a7710d97c4590dbddf31f70` | **OBSERVED** failed run; remediation **PENDING** |

The external operations Repository Graph (#630), Codebase Atlas (#835), Temporal
Graph (#841), observation schema (#896), Longitudinal/Evidence/INTENT graphs,
and sibling research issue are coordination targets, not inspected sources in
this repository snapshot. No graph agreement is counted as independent
corroboration.

## Coverage and limitations

- **Tracked-path accounting:** 976/976 paths enumerated from the pinned tree.
- **Full per-file content/source audit:** 0/976 paths completed by this
  deliverable. Selected source files were inspected to prepare the limited
  capability map above; every path remains pending full claim/dependency
  review. The 48 metadata-only records have per-path dispositions and are not
  claimed as reviewed.
- **Ownership and control mapping:** pending for all paths; both fields are
  explicitly `PENDING` in the census.
- **Claim-level dependencies, code-to-doc change impact, and protected CI at an
  exact PR head:** pending.
- **Full deployment/workflow claim audit and remediation of the sampled
  Mesh-Sync-Batch failure:** pending.
- **API Bridge auth/access-control remediation and deployment verification:**
  pending human owner/security review; this census does not change runtime code.
- **CodeRabbit:** no independent review receipt or per-file coverage was
  available when this report was prepared; review remains pending.
- **Behavioral/security regression cases, held-out graph-vs-keyword baseline,
  and false-positive/recall metrics:** pending. Initial focused tests cover
  NUL-safe path parsing, conservative metadata classifications, and the
  pinned-tree path denominator/state accounting.
- **External/private sources and runtime receipts:** not inspected; blocked or
  unavailable sources must be recorded explicitly before making claims about
  them.

The inventory is a first, resumable metadata deliverable—not a complete source
audit and not a proposal to replace the operations registry or graph.
