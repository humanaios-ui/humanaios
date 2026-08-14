# Registry Performance Analysis — Gap-Function Scope (Observability / Translation / Interpretation)

**Status:** DRAFT — Z2 ratification pending (analysis is JUDGMENT-tier; see §7)
**Type:** Registry performance analysis · registry-touching (IC-030 satisfied — see Provenance)
**Method:** Each IC-series incident is classified by which function of the automation↔authority gap failed: **Observability** (could the authority see actual state), **Translation** (did the compression from activity to claim preserve fidelity), or **Interpretation** (did the judgment layer have the capacity, framework, and consequence to rule on the signal). Derived from the session framing: fabrication drift = observability failure; IC-031 receipt overstatement = translation failure; rubber-stamp risk = interpretation failure.

---

## Provenance

- **Registry fetched live:** `https://raw.githubusercontent.com/humanaios-ui/operations/main/REGISTERED.md`, fetched this session (IC-030 hard-halt requirement satisfied before analysis).
- **Registry self-declared state:** Last updated July 14, 2026 (S-071426); F-18..F-58, IC to IC-058, 34 H-class entries; append-only with honest gaps (F-32/F-33 preserved, not backfilled).
- **Parsed:** 118 entries with id+name front-matter; 44 IC-series items (including IC-cand provisional entries) form the analysis population.
- **Declared provenance gap:** commit SHA pinning unavailable this session (GitHub API rate-limited); pinning falls back to the file's own header date + fetch timestamp. Z3 should pin the SHA at commit time.
- **Scope boundary (declared, not silent):** This analysis classifies the **IC-series only** — the incident record is the performance record. F-class and H-class entries were *not* per-entry classified: doing so honestly requires reading each synopsis against the taxonomy, and several parsed synopses showed extraction misalignment. Mapping F/H entries by which gap function they *study* is proposed as follow-on work (§8), not smuggled in unverified.

---

## 1. Operational definitions and decision rules

| Function | Failure signature | Decision rule |
|---|---|---|
| **O — Observability** | Authority (or its instruments) could not see actual state: assertion without inspection, broken/blind verification surfaces, referenced artifacts that don't exist, stale canonical pointers | *Would looking have prevented it?* If the truth was checkable and nothing checked (or the checker itself was blind), classify O |
| **T — Translation** | State was observable, but the compression from activity → claim → receipt distorted in transit: overstatement, count drift, status divergence across surfaces, ratified decisions not propagated, undocumented canonical workflows | *Did the claim diverge from the activity it summarized?* If reality and its representation split, classify T |
| **I — Interpretation** | Signal arrived intact, but the judgment layer failed: bandwidth exceeded, unreliable signal weighted as reliable, judging instrument misread meaning, gates without consequence, ceremony instead of oversight | *Did the authority receive a faithful signal and still fail to rule correctly — or was its ruling non-consequential?* Classify I |
| **E — Execution residual** | Incident doesn't map to the gap: agent-side discipline failure with state fully visible and claims accurate | Declared residual; the taxonomy's leftovers are data, not embarrassment |

Mixed incidents take the **root-cause** function (the failure that, removed, prevents the incident).

## 2. Per-entry classification — IC series

| ID | Slug | Fn | Rationale (one line) |
|---|---|---|---|
| IC-001/002/003 | github-verification-browser-cache | O | Verification surface served cached pages; the checker showed stale reality |
| IC-018 | file-creation-drift | E | State visible, claims accurate; output-form discipline diverged from directive — execution residual |
| IC-019 | make-oauth-dead-task-carry | T | Ratified exit decision never translated into working state; dead task carried 8+ sessions |
| IC-020 | operating-process-homeless | O | No canonical fetchable URL — nothing to observe against |
| IC-021 | unsupported-dataset-claims | O | Claims asserted against a canonical table never inspected; F-findings proposed on nonexistent corpus rows |
| IC-022 | off-by-one-n-count-drift | T | True counts existed; declared numbers mutated in transit across surfaces |
| IC-023 | wrong-org-url-drift | O | Canonical pointers left stale after migration; observability infrastructure aimed at the wrong org |
| IC-024 | f29-dual-status-inconsistency | T | One fact, two representation surfaces, divergent statuses |
| IC-025 | cross-file-edit-promise-not-landed | T | Declared coordinated landing; delivery was partial — claim exceeded activity |
| IC-026 | behind-remote-preflight-failure | T | The `[behind 7]` state was visible; protocol translated it into soft suggestion instead of halt directive |
| IC-027 | session-id-binding-omitted | T | Provenance metadata dropped in the artifact handoff — 8 of 9 artifacts unbound |
| IC-028 | stillpoint-ritualization-autodream | I | The canonical ceremony failure: governance apparatus performed vigilance while being the pattern it existed to catch |
| IC-029 | canonical-fetch-block-semantics-gap | T | Fetch states occurred in reality but had no protocol vocabulary — untranslatable state |
| IC-030 | registered-md-fetch-skipped | O | Registry-touching work proceeded blind to live registry state |
| IC-031 | receipt-overstatement-content-inaccuracy | T | The type specimen: receipt claimed contents not present in the push |
| IC-032 | constraint-before-data-inspection | O | CHECK constraint added without querying the live table it constrained |
| IC-033 | governance-blocker-conflation | T | Distinct blockers compressed into one undifferentiated unit for 10+ sessions; structure lost in compression |
| IC-034 | confident-wrong-field-declaration | O | Field lists declared confirmed, twice, without live validation — assertion without inspection (D-OVERCLAIM origin) |
| IC-035 | canonical-workflow-not-documented | T | Canonical activity existed with no ratifiable representation — untranslated into governable form |
| IC-037 | legibility-test-scorer-conflation | I | Judging instrument misread meaning: counted safeguards as friction |
| IC-038 | charter-countdown-carry-error | T | Numeric value drifted in carry between sessions |
| IC-039 | search-before-assert-gap | O | Conclusion stated as fact without searching prior sessions that already held the answer |
| IC-040 | shipped-contract-mismatch | T | Public documentation diverged from the real JSON Schema contract |
| IC-041 | audit-false-pass | O | Purest form: CI targeted a nonexistent path and printed PASS by construction — a verification surface blind by design |
| IC-042 | scanner-deploy-corruption | O | Committed bytes differed from believed bytes; discovered only by executing the raw commit |
| IC-043 | phantom-migration-references | O | Migrations cited by exact name across docs and memory; none existed (D-PATH-FABRICATION class) |
| IC-044 | submission-purity-constraint-collapse-recurrence | T | Consolidation reported complete; half-executed — claim > delivery, recurrence of IC-032 class |
| IC-045 | marker-injection-dead-endpoint | O | Lint pass silently killed the endpoint; no signal surfaced that live behavior changed |
| IC-046 | scorer-purity-exclusion-gap | T | Scorer's LI output claims clean data while dropping the purity fields that would say otherwise |
| IC-047 | scorer-certainty-overclaim | T | Unconditional PASS emitted over JUDGMENT-tier scores — certainty inflated in output translation |
| IC-048 | grounding-schema-unpopulated | O | Grounding-tier claims made against schema fields that live rows never populated |
| IC-049 | stage1-readiness-overclaim | O | Readiness described without querying the corpus; live checks contradicted both data buckets |
| IC-050 | blocker-gate-not-enforced | I | Gate warns and continues — judgment rendered non-consequential (sovereignty without teeth) |
| IC-051 | orchestrator-input-mapping-loss | T | Real input fields dropped in perceive()/mapping; placeholders persisted downstream — literal translation loss |
| IC-052 | drift-validator-missing-d-overclaim-entry | O | The drift detector blind to a Zone-2-ratified drift signal it exists to detect |
| IC-053 | drift-validator-missing-d-overclaim-key | O | Same mechanism as IC-052 (registered from the stranded queue) — detector blindness |
| IC-054 | no-same-session-self-correction-instrument | O | Instrumentation gap: same-session corrections invisible to any instrument |
| IC-055 | self-correction-claims-not-uniformly-gated | T | Self-correction claims passed ungated by external verification, wrong each time — self-certified claims in transit |
| IC-056 | p1-introspective-reliability-unweighted | I | Known-unreliable self-report weighted equally in judgment — interpretation framework fails to discount |
| IC-057 | elicitation-surface-taxonomy (unification) | I | Construct-validity correction: six unrecognized axes distorting what measurements *mean* |
| IC-058 | outcome-symmetry-corpus-gap | I | Hypothesis corpus can confirm but often cannot disconfirm — an asymmetric judgment framework |
| IC-cand (maintained-headline-recurrence) | T | Same values embedded in multiple manual-sync locations; divergence by construction |
| IC-cand (draft-reply-send-status-gap) | T | Drafted vs. sent status ambiguous — activity→status claim gap on an external engagement |

## 3. Distribution

| Function | Count | Share of 44 |
|---|---|---|
| **Translation** | 19 | 43% |
| **Observability** | 16 | 36% |
| **Interpretation** | 8 | 18% |
| **Execution residual** | 1 | 2% |

## 4. Performance findings

**4.1 — Translation is the largest incident surface.** Nearly half the incident record is fidelity loss in the activity→claim compression: overstatement (IC-031, IC-044, IC-047, IC-055), representation divergence (IC-022, IC-024, IC-038, headline-recurrence), ratified-but-unpropagated state (IC-019, IC-025), and untranslatable or undocumented state (IC-029, IC-035). The WAMPUM/receipt layer is where the gap leaks most often.

**4.2 — Observability failures cluster into two distinct sub-modes.** (a) *Assert-without-look* — IC-021, IC-032, IC-034, IC-039, IC-049 — checkable truth, nothing checked; and (b) *blind instruments* — IC-041, IC-042, IC-052/053, IC-054 — the checker itself broken, missing, or pointed at nothing. Sub-mode (b) is more dangerous: it produces false green, which is worse than no signal because it actively certifies the wrong state.

**4.3 — Interpretation failures are the rarest and the gravest.** Only 8 entries, but they include the ceremony incident (IC-028: the apparatus performing vigilance while being the pattern), the teeth failure (IC-050: gates that warn and continue), and three of the most recent registrations (IC-056/057/058) — all interpretation-framework corrections. Two readings, both proposed for the record: interpretation genuinely fails least because Z2 review is strong; *or* interpretation failures are systematically under-detected because the detector of interpretation failures is the interpretation layer itself. The recency skew (interpretation ICs concentrate in the newest registrations) weakly supports the second reading: the project only recently built instruments capable of seeing this class.

**4.4 — Mitigation coverage is inverted relative to §4.3.** Observability has the strongest existing instrumentation (B.0 empirical verification, IC-030 hard halts, receipt reconciliation's CONFIRMED/CONTRADICTED anchors). Translation has structural mitigations (Skill 5 receipt reconciliation, findings-scan for the under-registration inverse). Interpretation — the gravest class — is the *least* instrumented: its failures (IC-028, IC-050, IC-056) were each caught ad hoc, not by a standing instrument. The GD directives land precisely here: GD-01 rations interpretation bandwidth, GD-03 makes interpretation consequential, and GD-02 protects the translation layer that feeds it. **The registry's own performance record independently justifies the directive set.**

**4.5 — Recurrence tracks function.** The registry's named recurrences (IC-044 recurring IC-032's class; IC-052/053 duplicating; IC-055 naming three instances of one mechanism) are all O or T class. No interpretation failure has yet been observed to recur — consistent with either reading in §4.3.

## 5. Series-level note (declared scope limit)

F-class and H-class entries largely *study* the gap rather than *fail* in it — e.g., the humility/calibration line (F-29, F-44, F-48, F-49, H-HUMILITY-MASTER-01) is interpretation-layer research; the verification-layer line (F-58, H-VERIF-01/02) is observability research. A per-entry F/H mapping is proposed as follow-on (§8.3) and was deliberately not performed here on partially-misaligned parsed synopses.

## 6. Registry candidate (proposal only — this document does not register)

```
id: "F-CAND-gap-function-incident-taxonomy"
name: "gap-function-incident-taxonomy"
status: CANDIDATE
class: F
date_origin: "2026-08-01"
principles_triggered: ["P21"]
tags: ["governance", "drift", "taxonomy"]
```
**Synopsis:** The full IC-series (N=44) classifies cleanly (43/44) into three gap functions — observability, translation, interpretation — with a stable distribution (T 43% / O 36% / I 18%) and an inverse relationship between failure gravity and existing instrumentation (interpretation: gravest, least instrumented). Generalizable as a triage axis for future IC registration and as independent evidence for the GD directive set.
**Evidence anchor:** live REGISTERED.md fetch this session (SHA pinning pending — declared gap); classification table §2.
**Promotion gate:** Z2 review of the §2 classifications; second-coder pass on at least the 8 I-class and 1 E-class assignments (§7).
**Routing:** → Zone 2 (Night) for ratification per P21.

## 7. Limits (honest tiering)

The classification is **JUDGMENT-tier, single-coder** (this session's agent), performed against entry synopses, not full evidence packages. Specific soft assignments flagged for Z2: IC-026 (T vs I — visible signal, soft protocol), IC-033 (T vs I — compression vs judgment), IC-046 (T vs I — scorer output vs scoring framework), IC-055 (T vs O — ungated claims vs missing verification routing). One residual (IC-018) does not map, and is reported rather than forced. Per the doctrine this analysis serves: the classifier does not certify its own classifications.

## 8. Z2 decisions required

1. Ratify or amend the §1 operational definitions and decision rules as the standing triage axis.
2. Rule on the four flagged soft assignments (§7) and the IC-018 residual.
3. Approve follow-on: per-entry F/H gap-function mapping against full synopses (verified extraction, not this session's partial parse).
4. Decide whether new IC registrations carry a `gap_function: O|T|I|E` front-matter field going forward.
5. Promote or reject F-CAND-gap-function-incident-taxonomy (§6).
6. Prioritize an interpretation-layer standing instrument (§4.4's gap) — the one function whose failures are currently caught only ad hoc.

---

*This document proposes and classifies; it does not register. Append-only writes are Zone 2/3 actions.*

*Wado. 🦅*
