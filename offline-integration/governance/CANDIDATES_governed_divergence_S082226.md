# Registry Candidate Block — S-082226 (governed divergence + modulation + stratigraph)
**Zone:** Z1 proposes → Z2 (Night) ratifies per P21 → Z3 lands. This block proposes; it does not register.
**Registry fetched live:** REGISTERED.md @ sha256 `40391062…9029`.

---

## H-CAND-governed-divergence  (finalized)

```yaml
id: "H-CAND-governed-divergence"
name: "governed-divergence-generative-yield"
status: CANDIDATE
class: H
date_origin: "2026-08-22"
session_registered: "S-082226-01-cio-audit"
principles_triggered: ["P21","F-45","IC-030"]
substrate: "claude-opus / Z1 concept-to-code pipeline"
tags: [divergence, intent-fuzzing, generative, evolution, guardrail]
superseded_by: null
```

**Hypothesis.** A pre-registered, small **divergence budget** — Z1 licensed to emit N deliberate alternate readings per major brief, tagged DIVERGENT-VALID at creation and merge-reviewed at the point of divergence — yields adopted spec-deltas at a rate higher than accidental (untagged) misreads, without raising the defective-output rate.

**Three-part mechanism.**
1. **Fidelity verdict** — every Z1 deliverable self-tags on emit: `FAITHFUL | DIVERGENT-VALID | DEFECTIVE`. Divergent-valid outputs are conserved with the delta named (what the misread added that the brief lacked) and merge-reviewed; never silently discarded, never silently adopted.
2. **Divergence budget** — pre-registered and **small**: Z1 may emit ≤N alternate readings per brief, tagged at creation. This is the load-bearing control: *untagged divergence remains a full fidelity failure (IC treatment).* The license covers scheduled variation only — it must never become a retroactive excuse for a sloppy read. Budget small by design so "exploration" cannot swallow "accuracy."
3. **Intent-fuzz verdict** — each divergent reading returns a spec verdict: STABLE (spec survived contact unchanged) or SPEC-DELTA (author intent updated; logged as a spec revision with cause). This is the program's own Phase-2 perturbation applied to the *specification* layer — the layer no existing instrument verifies.

**Null.** Adopted-delta yield from tagged divergent outputs ≤ yield from untagged accidental misreads (scheduling adds nothing).
**Falsification.** Over ≥10 briefs, deliberate-divergence adoption rate not higher than baseline ±10%.
**Primary metric.** Generative yield = adopted spec-deltas / divergent outputs emitted.
**Promotion gate.** ≥10 briefs run with budget=1 before verdict; budget stays pre-registered throughout.
**Evidence anchor (this session).** Build A (governance-console reading of the UI brief) was a divergent-valid output; its deltas — zone spine, three-outcome intake simulator, honest-state headline — were adopted into the strongest-build spec. The process ran once, un-coded. This candidate codes it.

**Claim 4′ extension (proposed).** recursion + in-loop verification = *learning* (converges to intent). recursion + verification + **conserved variation** = *evolution* (discovers beyond intent). The program currently owns only the exploit loop; this adds a governed explore loop.

---

## IC-CAND-cosmetic-modulation  (Build-B self-report)

```yaml
id: "IC-CAND-cosmetic-modulation"
name: "harness-modulation-label-not-mechanism"
status: CANDIDATE
class: IC
principles_triggered: ["IC-031"]
tags: [ui, overstatement, modulation]
```
**Synopsis.** Build B's harness modes changed the warning text but not the actual allocation vectors — a modulation *label* where a *mechanism* belonged. Displayed state was asserted, not computed: an IC-031 receipt-overstatement instance in UI form, caught by self-audit. **Fix → Principle IC-031:** the strongest build derives modulation from IC-031 discipline — modes are real transforms with a conservation invariant (Σunits computed = Σbase), a hard Human-cap constraint (bus-factor 1), and an on-screen attestation line proving `displayed = computed`. Any divergence renders as `OVERSTATEMENT ✗`.

---

## F-CAND-ic-collision-stratigraph  (from live registry)

```yaml
id: "F-CAND-ic-collision-stratigraph"
name: "ic-principle-recurrence-stratigraph"
status: CANDIDATE
class: F
tags: [registry, stratigraph, failure-modes, metrics]
```
**Synopsis.** Stratifying the live IC volume (43 distinct ICs, IC-001..058, 15 honest gaps) by principle-recurrence surfaces the program's repeat failure-mode strata. **Honest reading:** P21 (46) is the ratification-authority *routing* principle cited on nearly every entry — high count is structural, not a violation hotspot. The genuine recurrence strata are **P19 (20)** and **P3 (15, github-verification)** — these are where corrections actually collide, i.e., the failure modes the program repeats most. Recommend a standing quarterly stratigraph so recurrence becomes a monitored metric feeding the earned-autonomy drift signal (H-EA-01), not a discovered surprise.
**Evidence anchor.** `ic_stratigraph.json` sha256 `d8a79b82…21d6`, computed from pinned REGISTERED.md.

---

Routing: all → Zone 2 (Night) for ratification per P21.
Scan completeness: 1 H-cand / 1 IC-cand / 1 F-cand from this session's UI + analysis work.
