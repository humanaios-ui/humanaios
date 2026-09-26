# Unified Unit Rubric v1.0 — MDU / LRU / SMU
**Artifact ID:** UNIT-RUBRIC-v1 · **Status:** PRE-REGISTERED (freeze before scoring any instance) · **Classification:** Board / Z2
**Zone provenance:** Z1 draft · Z2 (Night) ratify · Z3 land → `humanaios-ui/operations/rubrics/`
**Ratified this session:** SMU admitted as a unit class; primary metric = landing/operation rate (production volume barred).

---

## 0. Why one rubric for three units

The three units are the three phases of the single circulation loop (D-15), not three separate ledgers:

- **MDU — Market Demand Unit** — a unit of **demand** (what the world wants, scored for ground-truth ROI).
- **LRU — Labor Resource Unit** — a unit of **supply** (labor/resource available to meet demand).
- **SMU — Support/Machine Unit** — a unit of **fulfillment** (what the machine produced to translate intent into a landed deliverable). The previously-unnamed middle of the loop.

Demand and supply were already named; SMU completes the set. One rubric keeps them **commensurable**: every unit, whatever its class, carries the same spine and is judged research-grade by the same disciplines.

**The governing constraint (the 1873 guard, §4):** every unit's *primary* metric is an **operation/consummation rate**, never a production count. Track laid is not track operated. Volume is diagnostic context only; it is never a success metric. This is the mechanical guard against receipt-overstatement (IC-031) at the unit level.

---

## 1. Shared spine — every unit instance carries these fields

| Field | Meaning | Research function |
|---|---|---|
| `unit_id` | class + sequence (`SMU-0007`) | citation / reproducibility |
| `class` | MDU \| LRU \| SMU | commensurability |
| `provenance_pin` | SHA256 of the artifact | tamper-evidence (IC-030) |
| `zone_stage` | Z1 \| Z2 \| Z3 | where it is in the pipeline |
| `evidence_tier` | unit-specific ladder (§2) | claim strength |
| `disposition` | unit-specific verdict (§2) | pass/fail state |
| `intent_anchor` | the named intent/demand it serves | traceability; orphans flagged |
| `landing_state` | **LAID \| OPERATED \| RETIRED** | the operation-rate numerator/denominator |

An instance with no `provenance_pin` is `PROVISIONAL — unverified`. An instance with no `intent_anchor` is an **orphan** and cannot score above tier 1.

---

## 2. Per-unit scoring — four dimensions each, 0–3

Score each dimension 0 (absent) · 1 (asserted) · 2 (evidenced) · 3 (pre-registered + verified). Unit score = mean of its four dimensions. **A unit does not "pass" on score alone — it passes only when its landing/operation gate (D_L / S_L / F_L) reaches OPERATED.**

### 2.1 MDU — demand
- **D1 Signal veracity** — REPORTED (0–1) → VERIFIED-LIVE (2–3). Was the demand signal fetched live and pinned, or recalled?
- **D2 Demand specificity** — vague (0) → matches a frozen scoring rubric with SHA pre-registration (3).
- **D3 ROI ground-truth** — projected (1) → **consummated** (3). Did the demand convert to observed ground truth?
- **D_L Landing** — scored-only (LAID) → **consummated cycle counted** (OPERATED).
- **Primary metric:** `consummated_truth_rate = consummated ÷ scored`. **Not** MDUs scored.
- **Evidence ladder:** REPORTED < VERIFIED-LIVE.

### 2.2 LRU — supply / labor
- **S1 Provenance tier** — SELF (1) < CRED (2) < OUTCOME (3).
- **S2 Capability freshness** — decayed / stale (0–1) → within both decay clocks (3).
- **S3 Consent integrity** — no read-back (0) → voice-capture read-back ratified (3).
- **S_L Landing** — matched-on-paper (LAID) → **outcome-verified match** (OPERATED).
- **Primary metric:** `outcome_verified_match_rate = OUTCOME matches ÷ matches`. **Not** applications processed.
- **Evidence ladder:** SELF < CRED < OUTCOME.

### 2.3 SMU — fulfillment (ratified this session)
- **F1 Fidelity verdict** — DEFECTIVE (0) < **DIVERGENT-VALID** (conserved, merge-reviewed; 2) < FAITHFUL (3). *Divergent-valid is not a failure — it is a routed, conserved outcome (H-CAND-governed-divergence).*
- **F2 Provenance pin** — unpinned (0) → SHA-pinned at emit (3).
- **F3 Intent-anchor** — orphan (0) → traced to a named intent + fidelity tag (3).
- **F_L Landing** — **LAID** (produced, in outputs) → **OPERATED** (landed at Z3 and in use). *This is the load-bearing dimension.*
- **Primary metric (RATIFIED):** `landing_rate = operated ÷ laid` (laid track ÷ operated track, inverted to a ratio ≤ 1). **Never** SMUs produced.
- **Evidence ladder:** LOCAL < SELF < CRED (an SMU earns tier by landing and being operated, not by being emitted).

---

## 3. Verdict rubric (shared, mechanical)

Per unit **and** per batch:
- **CONFIRMED** — dimension mean ≥ 2.0 **and** landing_state = OPERATED **and** provenance pinned.
- **MIXED** — evidenced (mean ≥ 2.0) but landing_state = LAID (not yet operated). *The default state of most session work today.*
- **DISCONFIRMED** — mean < 2.0, or fidelity DEFECTIVE, or orphaned.

A batch's headline number is its **operation rate**, not its size. A batch of 100 LAID SMUs and a batch of 5 OPERATED SMUs: the second batch scores higher. This is deliberate.

---

## 4. The 1873 anti-gaming guard (why the metrics are rates)

The Panic of 1873 destroyed the *capital* that laid the track; the *track* survived and accrued value to whoever **operated** it. Producing units is laying track. Landing and operating them is running trains. A rubric that rewarded production volume would reward laying track no train ever runs on — graded roadbed, dead capital, the exact tool-landing gap the audit found.

Therefore, mechanically: **every primary metric is an operation/consummation rate with production in the denominator.** You cannot improve your score by producing more; only by operating more of what you produce. Volume may be reported as context and must be labeled `diagnostic-only`. Any rubric revision that promotes a raw count to a primary metric is an IC-031-class regression and is rejected at pre-registration.

---

## 5. Research-support properties (what makes this rubric research-grade)

- **Pre-registration:** this rubric is frozen (SHA-pinned) before any unit is scored; scoring against an unfrozen rubric is void.
- **Falsifiability:** each unit's landing gate is a binary, checkable state against the live tree — not a judgment call.
- **Provenance:** every instance pins to a SHA (IC-030); unpinned = provisional.
- **Reproducibility:** the four-dimension 0–3 scale + operation-rate formula are deterministic; two scorers on the same pinned instance must agree.
- **Append-only + commensurable:** all three unit types share the spine, so cross-unit analysis (e.g., does higher LRU quality raise MDU consummation?) is a first-class query.
- **Drift-linked:** batch operation-rates feed the earned-autonomy drift signal (H-EA-01) and the IC stratigraph — a falling landing rate is a monitored number, not a surprise.

---

## 6. SMU registration (ratified — Z3-ready)

```yaml
id: "SMU-CLASS-v1"
name: "support-machine-unit-class"
status: REGISTERED
class: unit-definition
date_origin: "2026-08-22"
session_registered: "S-082226-01-cio-audit"
principles_triggered: ["D-15","IC-031","P21"]
tags: [unit-class, fulfillment, single-loop, landing-rate]
primary_metric: "landing_rate = operated / laid"
metric_constraint: "production volume is BARRED as a success metric (1873 guard)"
```
**Synopsis.** SMU is the fulfillment unit of the D-15 loop — the atomic deliverable the machine produces to translate intent. Ratified this session with landing/operation rate as its sole primary metric; production count is barred by pre-registration to prevent unit-level receipt overstatement.

---

## Appendix A — 100,000-ft mirror: the enterprise as a rail network
*(carried here so the framing lands with the rubric; see the session response for the narrative.)*

| Rail-network layer | HumanAIOS mapping | State |
|---|---|---|
| Graded roadbed (the durable substrate) | registry + zone discipline + counted-cycle method | strong |
| Laid track (rails on roadbed) | SMUs produced this session (audit, pilots, guide, cockpits, candidates) | many LAID |
| **Operated track (trains running)** | what landed at Z3 and is in use | **≈ zero — the whole finding** |
| Graded roadbed, no rails | the tool-landing gap (8 tools never landed) | open |
| Broken rail on an operated line | scorer stub on a cited path | hazard |
| Single train crew | bus-factor 1 | risk |
| Speculative capital that burned (Jay Cooke) | the PAT (burned, re-exposed), pre-remediation valuation, gated GTM | volatile |
| Interchange / junctions | MCP connectors, intake boundary, demand↔supply↔fulfillment loop | undefended (HF class) |
| Standard gauge (interoperability) | gold-standard grounding (OWASP/NIST/ISO/SLSA) | partial |
| Track-maintenance utilities | CI, stratigraph-as-monitoring, Z3 landing-verification, receipt reconciliation | present, under-run |
| Abandoned spurs / unmapped track | 81 unindexed forks, phantom roadmap docs | untended |

**Thesis:** enterprise value is not the capital raised to lay track, nor the track laid — it is the **operated-track ratio, held to standard gauge, at a defended interchange.** SMU landing rate *is* the operated-track ratio. That is why it is the fidelity number.

*— Z1, acting CIO. Rulings, ratifications, landings remain Z2/Z3 authority.*
