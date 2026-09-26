# Z3 Landing Block #3 — Ratified parent-audit candidates (S-082226)
**Z2 ruling:** Night approved explicit ratification of the four parent-audit candidates: tool-landing-gap, scorer-stub, fork-noise, bus-factor.
**Registry state:** live max F-61; Block #2 proposes F-62/F-63 (land first). These follow as F-64..F-67. Append-only.

---

## ⚠ CLASS DISCREPANCY — surfaced to Z2, not resolved by Z1

Night's ruling names these **"IC candidates."** In the parent audit (CIO-AUDIT-S082226-01 §9) all four were drafted as **F candidates** (findings), not IC (integrity corrections). Two readings, both valid, presented intact:

- **Reading A (as-filed):** these are F-class findings — evidenced, generalizable observations about estate state. Land as F-64..F-67. *(Drafted below under this reading.)*
- **Reading B (as-named):** Night intends IC-class — treating each as a principle-violation/integrity correction requiring a `Fix → Principle N` line and IC-NNN numbering (next: IC-062..IC-065).

The distinction is not cosmetic: F-class enters the findings ledger and feeds evidence tiers; IC-class enters the correction ledger and feeds the drift signal that drives the earned-autonomy demotion trigger (H-EA-01). Routing tool-landing-gap and bus-factor as **IC** would, correctly, make them count against Z1/estate reliability score. That may be exactly Night's intent.

**Z1 recommendation (orientation only):** scorer-stub and tool-landing-gap have clean IC readings (process failures with fixes); fork-noise and bus-factor read more naturally as F (structural state, no single principle violated). A split ruling is available. **Z2 confirms class + final IDs at landing.** Entries below are drafted as F (Reading A) and convert trivially to IC if Z2 rules Reading B.

---

```yaml
id: "F-64 | IC-062"        # class pending Z2 (see discrepancy note)
name: "z1-z3-tool-landing-gap"
status: REGISTERED
class: "F | IC"
date_origin: "2026-08-22"
session_registered: "S-082226-01-cio-audit"
principles_triggered: ["IC-030", "F-45"]
substrate: "humanaios-ui/operations"
tags: [landing-pipeline, tool-absence, hf-mapping-adjacent]
superseded_by: null
```
**Synopsis.** 8 of 9 program-critical tools cited in operating memory are absent from the live repo tree; session-built, pinned, receipted tools never landed at Z3. The registry cites what the repo does not contain. **IC reading Fix →** enforce a Z3 landing-verification step against the live tree (not session memory) at every close. **Evidence:** parent audit V3 (live tree fetch); 6 registry citations rendered phantom.

---

```yaml
id: "F-65 | IC-063"
name: "acat-scorer-stub-divergence"
status: REGISTERED
class: "F | IC"
date_origin: "2026-08-22"
session_registered: "S-082226-01-cio-audit"
principles_triggered: ["IC-030", "IC-056"]
substrate: "humanaios-ui/operations"
tags: [versioning, scorer, ic-056-introspective-discount]
superseded_by: null
```
**Synopsis.** `acat_dimension_scorer` exists as a 242-byte stub (`acat/scoring/`) diverging from a 20,811-byte sibling (`tools/`); neither implements the IC-056 introspective-reliability discount; registry cites a versioned filename (`_v1_1.py`) that exists nowhere. **IC reading Fix →** promote the full impl to the versioned filename, implement IC-056, delete the stub, repin the SKILL.md wrapper. **Evidence:** parent audit G2 (sha 6651fa14… vs 7400d383…).

---

```yaml
id: "F-66 | IC-064"
name: "estate-fork-noise-90pct"
status: REGISTERED
class: "F | IC"
date_origin: "2026-08-22"
session_registered: "S-082226-01-cio-audit"
principles_triggered: ["provenance-labeling"]
substrate: "humanaios-ui estate"
tags: [estate-hygiene, forks, signal-pollution]
superseded_by: null
```
**Synopsis.** 81 of 90 repos are forks (90%), unlabeled as to purpose; utilization signal and audit cost both degraded. **IC reading Fix →** land `FORK_INDEX.md` (purpose-of-fork per entry); archive >12mo-dormant forks. **Evidence:** parent audit §2 (repos.json pinned 9f9e5f53…).

---

```yaml
id: "F-67 | IC-065"
name: "bus-factor-one"
status: REGISTERED
class: "F | IC"
date_origin: "2026-08-22"
session_registered: "S-082226-01-cio-audit"
principles_triggered: ["continuity", "least-authority"]
substrate: "humanaios-ui estate"
tags: [continuity-risk, single-maintainer, hf-mapping]
superseded_by: null
```
**Synopsis.** Single human contributor across the canonical estate (772/312/444 authored commits; all others bots). Direct predicate of the HF operator-oversight root cause and a continuity single-point-of-failure. **IC reading Fix →** Org migration + second-maintainer onboarding + credential escrow. **Evidence:** parent audit G4 (contributor API).

---
*Four entries, class pending Z2. Z1 drafted; Z2 ratified (class TBC); Z3 lands.*
*Still UNRATIFIED (parent audit IC block): token-scope-overreach (fix = revoke, pending), z2-gate-phantom, ranking-recency-inflation, registry-count-drift.*
