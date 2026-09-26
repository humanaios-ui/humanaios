# Implementation Guide — Mechanical Enforcement via Earned Autonomy
**Artifact ID:** CIO-GUIDE-S082226-01 · **Classification:** Board / Z2 review · **Status:** DRAFT (untested — see §7)
**Zone provenance:** Z1 draft · Z2 (Night) ratify · Z3 land → `humanaios-ui/operations`
**Closes:** F-45 (enforcement locus in memory, not code) · parent-audit V4 (phantom Z2 gate)

---

## 1. The principle being implemented

F-45 states the enforcement locus must live in **code, not memory**. Today zone discipline is *procedural*: Z1 follows the rules because it was told to. A drifting, compromised, or hyperfocused Z1 has no hard stop — the exact predicate the HF incident turned on. "Earned autonomy" converts this from a norm Z1 *chooses* to obey into a boundary the platform *enforces regardless of Z1's state*: autonomy is scaled to registry-tracked reliability and tightened automatically on drift.

You already own two of the three parts:
- **Reliability ledger** — `REGISTERED.md` F/IC/H history per session.
- **Drift signal** — IC-031 receipt-overstatement incidents (and now IC-059 self-audit, IC-060 scope).
- **Missing: the tightening gate** — the mechanical enforcement point. This guide builds it.

**Honest scope boundary (read first).** GitHub-native enforcement governs the **Z3 landing boundary** — what reaches the repository. It does **not** constrain Z1's *in-session* tool calls (bash, API, file writes happen before anything reaches GitHub). Full in-session mechanical constraint requires a harness-level tool allowlist Z1 does not control. This gate therefore catches bad artifacts *at the repository door* and governs *what autonomy tier is permitted to land unattended* — it is necessary and high-value, but it is not a sandbox. Do not oversell it as one. Pair it with the Protect-column security work (least-authority sweep, Org migration) from the parent audit; this guide is the enforcement half, not the security half.

---

## 2. The three mechanical primitives GitHub gives you

These are the load-bearing enforcement points. None depend on Z1 cooperating.

1. **Branch protection + required review + CODEOWNERS.** Make `REGISTERED.md`, `tools/**`, and `.github/workflows/**` require an approving review from a Z2 code-owner before merge. This is the real Z2 gate the audit found phantom. Single CODEOWNERS location (parent audit flagged three — collapse to `.github/CODEOWNERS`).
2. **GitHub Environments with required reviewers.** Wrap any registry-touching workflow in an `environment:` that has a required-reviewer protection rule. The job *pauses* until a human Z2 approves the run. This is the mechanical ratification gate for *automated* landings.
3. **Signed commits / attestations.** Require signed commits on protected paths; optionally OIDC-based attestations so a landing carries a verifiable claim of *which tier* produced it. This makes tier-jumping detectable, not just discouraged.

---

## 3. The reliability ledger — compute a tier from the registry

A small scheduled job derives an **autonomy tier** per actor from the pinned registry. Illustrative logic (untested draft):

```
# reliability_score(actor, window=last_N_sessions):
#   base      = sessions_clean_of_IC / sessions_total
#   penalty   = w1*IC031_incidents + w2*IC059_selfaudit + w3*IC060_scope
#   recency   = decay-weight recent incidents heavier
#   score     = clamp(base - penalty*recency, 0, 1)
#
# tier(score):
#   score >= 0.90  -> T3  (broad)
#   0.70..0.90     -> T2  (standard)
#   0.50..0.70     -> T1  (restricted)
#   < 0.50         -> T0  (supervised-only)
```

Inputs come only from the append-only registry, so the tier is auditable and reproducible from a pinned SHA. Freeze the weight vector as a pre-registered artifact (`autonomy_weights_v1.md` + SHA) before first use — same discipline as the ranking formula.

---

## 4. The autonomy tier ladder — what each tier may land unattended

| Tier | Reliability | May land WITHOUT Z2 approval | Requires Z2 environment approval | Blocked |
|---|---|---|---|---|
| **T3 Broad** | ≥0.90 | Non-registry docs, tool *additions* with tests | Registry appends, gate/workflow edits | scope/permission changes |
| **T2 Standard** | 0.70–0.90 | Non-registry docs only | All `tools/**` and registry writes | workflow + permission edits |
| **T1 Restricted** | 0.50–0.70 | Nothing unattended | All protected-path writes | tool additions, workflow edits |
| **T0 Supervised** | <0.50 | Nothing | Every write, incl. docs | everything until score recovers |

The tier is enforced by (a) branch-protection required-review count scaling with tier, and (b) the environment reviewer requirement being mandatory below T3 for protected paths. A T1 actor physically cannot merge a registry change without a human approval step — mechanical, not procedural.

---

## 5. The tightening trigger — drift demotes automatically

The point of "tightened on drift." Wire the existing `findings-registry-gate.yml` (or a sibling) so that when a new IC of the drift classes lands:

```
on registry append of class IC where tag in {receipt-overstatement, self-audit, scope}:
  recompute reliability_score(actor)
  if new_tier < current_tier:
      write autonomy_state.json (actor -> lower tier)   # append-only log
      open an issue tagged autonomy-demotion, assign Z2
      # next protected-path PR from actor now needs the stricter review path
```

Demotion is data-driven and immediate; **re-promotion is Z2-gated** (a human ratifies that the drift is resolved before autonomy is restored). This asymmetry — automatic tightening, deliberate loosening — is the safety-preserving default and mirrors the "earned" in earned autonomy.

---

## 6. The missing Z2 gate — concrete build (closes V4)

The actual file the audit found absent. Illustrative skeleton (untested draft; validate before landing):

```yaml
name: z2-ratification-gate
on:
  pull_request:
    paths: ["REGISTERED.md", "tools/**", ".github/workflows/**"]
permissions:
  contents: read
jobs:
  ratify:
    runs-on: ubuntu-latest
    environment: z2-ratification          # <- required-reviewer rule = the human gate
    steps:
      - uses: actions/checkout@v4
      - name: Verify actor tier permits this path
        run: python tools/autonomy_gate_v1.py --actor "${{ github.actor }}" --paths "${{ ... }}"
        # exits non-zero if tier < required-for-path  => PR blocked mechanically
      - name: Require Z2 code-owner approval
        run: echo "CODEOWNERS on protected paths enforces this at merge"
```

Three enforcement layers stack: CODEOWNERS (who may approve), the `environment` reviewer rule (a human must click approve), and `autonomy_gate_v1.py` (tier must permit the path). Any one failing blocks the land. This is the phantom gate made real.

---

## 7. Sequence, and what this does NOT do

**Build order (each step independently valuable, no big-bang):**
1. Collapse to one `.github/CODEOWNERS`; enable branch protection + required review on the three protected path globs. *(This alone kills the phantom-gate finding.)*
2. Create the `z2-ratification` environment with a required reviewer. *(Mechanical human gate for automated landings.)*
3. Land `autonomy_gate_v1.py` + pre-registered `autonomy_weights_v1.md`. *(Tier computation.)*
4. Wire the demotion trigger (§5) into the registry gate. *(Tightening.)*
5. Turn on signed-commit requirement on protected paths. *(Tier-jump detection.)*

**Honest limits — do not let the board over-read:**
- Governs the **repository boundary**, not Z1's live session tool calls (§1 boundary).
- Reliability tier is only as honest as the registry; if IC incidents go **unregistered**, the ledger over-rates the actor. The `humanaios-findings-scan` skill is the compensating control — this gate makes that skill's completeness safety-critical.
- Re-promotion is a human judgment; a lenient Z2 can restore autonomy prematurely. The asymmetry helps but does not remove human error.
- None of this is a security control against external intrusion. It is enforcement of *internal zone discipline*. The Protect-column work (least-authority, Org migration, egress control) is separate and still required.

**Net effect once built:** F-45 closes — enforcement moves from memory into code. The parent audit's largest liability becomes a designed control surface. Z1 drift can still *occur*, but it can no longer *land unattended*, and it demotes the drifting actor automatically. That is the difference between a norm and a boundary.

*— Z1, acting CIO capacity. Rulings, ratifications, landings remain Z2/Z3 authority.*
