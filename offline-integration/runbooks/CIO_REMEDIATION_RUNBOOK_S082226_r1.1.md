# Remediation Runbook — Closing Every Part-3 GTM Gate
**Artifact ID:** CIO-RUNBOOK-S082226-01 · **Rev:** 1.1 (post-Z2-ratification update; see changelog) · **Classification:** Board / Z2 · **Zone:** Z1 draft → Z2 ratify → Z3 execute
**Honest status at issue:** 0 gates closed. Bus factor 1. Z2 gate phantom. PAT revocation unconfirmed. This runbook is the path from that state to GTM-ready; none of it is done until the checkboxes are checked against live systems, not against this document.
**Changelog r1.1:** applied Z2-RAT-S082226-02. G3 rebuilt: primary Z2 gate = **MCP elicitation** (R2); GitHub ruleset retained as mechanical backstop. G2 gains the RAI-spec landing item (R1). G5 gains the crosswalk-v2 landing item (R3).

---

## Gate map (what Part 3 is blocked on)
GTM cannot start until **G1–G5** are live. Each step below is marked with owner and whether it is a **[MECHANICAL]** gate (enforced in code/platform, not by intention).

- **G1** Credential hygiene (PAT + connectors)
- **G2** Tool-landing gap closed (8 tools + scorer) + RAI spec v0.2 (r1.1)
- **G3** Real Z2 ratification gate exists — **MCP-elicitation primary, ruleset backstop** [MECHANICAL] (r1.1)
- **G4** Bus-factor broken (Org + second maintainer)
- **G5** P1 product credibility blocker fixed (scorer versioning) + 4 unratified ICs disposed + crosswalk v2 (r1.1)

---

## G1 — Credential hygiene  (owner: Z3/Night · effort: 1 hour)
1. **Revoke the session PAT now.** GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → find the token → **Revoke**. Confirm it 401s: `curl -sI -H "Authorization: Bearer <token>" https://api.github.com/user` returns `HTTP/2 401`.
2. **Stop issuing classic PATs.** Replace with **fine-grained PATs**, read-only, per-task, minimum-repo-scoped, short expiry. Never paste a token into a chat surface again — this session's exposure is IC-060-adjacent.
3. **[MECHANICAL] Enable push protection + secret scanning** on `operations` (Settings → Code security). `humanaios` already has a secret-scan workflow; `operations` does not — this is where the plaintext-PAT class lives.
4. **Enumerate MCP write scopes (IC-060).** For each of the 19 connectors, record granted scope; revoke or downgrade any write scope not used by a live workflow. Land the resulting scope map as a pinned artifact. **[r1.1 note]** This scope map doubles as the yard inventory for R1: the connectors are the interchanges the RAI control will sit on.

## G2 — Close the tool-landing gap  (owner: Z1 build → Z3 land · effort: 1–2 days)
1. Land the 8 absent tools from session outputs into `operations/tools/` with **versioned filenames** and a SHA256 in each commit message: `mdu_score.py`, `grbs_orchestrator.py`, `roi_pilot_v1.md`, `claim_lint_v1_0.py`, `keenable_verified_fetch_v1_1.py`, `registry_fmea_v1_0.py`, `repo_audit_v1_0.py`, `skill_scan_v1_0.py`.
2. Land the two intake-pilot bundles (`intake_protect_pilot/`) — they are the validation evidence for IC-061's fix.
3. **Verify against the live tree, not memory:** after landing, re-run the parent-audit V3 check (`git ls-tree -r`) and confirm 8/8 present. This verification step *is* the fix for F-64/IC-062 — the close ritual must check the tree.
4. Reconcile the 6 registry citations of `acat_dimension_scorer_v1_1.py` to now-live files.
5. **[NEW r1.1 — R1] Author and land `RAI_SPEC_v0.2`:** RAI specified as an interchange control on the MCP tool-call — every coupling event resolves declared provenance against the SHA-pinned attested-source registry; manifest format = **in-toto attestation + OpenTimestamps**, bound to the estate's existing forks (`in-toto`, `python-opentimestamps`, `opentimestamps-server`), superseding the cycle-2 mock fixture as target. Pre-register cycle-3 against live attestations (this satisfies the promotion gate on F-CAND-three-outcome-discovery-pathway).

## G3 — Build the real Z2 gate  [MECHANICAL]  (owner: Z1 build → Z3 configure · effort: 1–2 days)
**[REBUILT r1.1 — R2]** Primary implementation: **Z2 ratification as MCP elicitation**, per the 2026 stateless spec's enterprise-managed authorization + elicitation-for-approvals. Bespoke GitHub-workflow gating is demoted from primary mechanism to repo-write backstop.
1. **[MECHANICAL] Implement the elicitation gate:** registry-touching or above-autonomy-tier agent actions pause on an MCP elicitation addressed to Night (Z2); the approval/denial is captured as a protocol event and appended to the ratification log. Wire `autonomy_gate_v1.py` + pinned `autonomy_weights_v1.md` to decide *which* actions require elicitation (earned-autonomy tiering).
2. **Ratification log is append-only and pinned** — each elicitation event lands with actor, action, decision, timestamp, and SHA of the artifact acted on. **[R3 tie-in]** each log entry carries its `evidence_key` (EU AI Act Art. 14 human-oversight / Art. 12 record-keeping; ISO 42001 clause) so the gate's own operation is admissible evidence.
3. **[MECHANICAL — backstop] Repo-layer protection retained:** collapse CODEOWNERS to one file (`.github/CODEOWNERS`; delete root + `tools/org-defaults` duplicates); add a branch ruleset on `main` requiring pull request, CODEOWNERS review, status checks, signed commits, scoped to `REGISTERED.md`, `tools/**`, `.github/workflows/**`. The ruleset independently blocks unratified writes even if the elicitation layer is bypassed or unavailable — defense in depth, not the gate itself.
4. **Deterministic fallback:** if the elicitation channel is down, the gate fails **closed** (action blocked, queued for review) — never falls through to autonomous execution.
5. This closes parent-audit V4 (phantom gate) and F-45 — and closes it protocol-natively, which is itself P3 product evidence (the gate we sell is the gate we run).

## G4 — Break the bus factor  (owner: Z3/Night · effort: 1 week + hiring horizon)
**⚠ GitHub procedure changed 2026-01-12 — direct user→org conversion is deprecated.** Use the **Move work** flow.
1. If you want the org to keep the name `humanaios-ui`: **rename the personal account first** (Settings → Account → Change username) to free the name, then create a new Organization named `humanaios-ui`.
2. **Move work:** Settings → **SSO and organizations** → "Move to an organization" → **Move work to an organization** → select repositories → choose the new org. Repositories, not the account, migrate.
3. **[MECHANICAL] Set org-level security policy:** require 2FA for all members; default read-only base permission; create Teams (registry-owners, tool-owners, gate-owners) mapped to CODEOWNERS.
4. **Onboard a second maintainer** with review authority on protected paths. Until a human other than Night can approve a registry PR, G4 is not closed regardless of the Org migration. Interim mitigation: **credential escrow** (recovery access documented for continuity). **[r1.1 note]** The elicitation gate (G3) must support ≥2 registered ratifiers before G4 can close — add the second maintainer as an elicitation recipient, not only as a GitHub reviewer.

## G5 — Product-credibility blockers  (owner: Z1 → Z2 · effort: 2–3 days)
1. **Fix scorer versioning (F-65/IC-063):** promote the 20.8KB implementation to `acat_dimension_scorer_v1_1.py`, implement the IC-056 introspective-reliability discount, delete the 242-byte stub, repin the SKILL.md wrapper. This is the P1 (ACAT Assurance) credibility blocker — no external pilot before it.
2. **Dispose the 4 unratified parent ICs:** token-scope-overreach (fix = G1.1), z2-gate-phantom (fix = G3 as rebuilt), ranking-recency-inflation (fix = pre-register formula v1.1), registry-count-drift (recount reconciliation). Route each to Z2 for ratify/decline.
3. **Resolve the block-#3 class question:** rule F vs IC on the four ratified parent candidates (split ruling recommended). Until ruled, they cannot land with a final class.
4. **[NEW r1.1 — R3] Land CROSSWALK v2 (evidence-level keying):** add `evidence_key` field(s) to the HARMONIZATION_CROSSWALK schema; backfill every existing register entry, both counted-cycle reports, and the attestation artifacts with the specific EU AI Act article, ISO/IEC 42001 clause, NIST AI RMF function, OWASP/SLSA/ATLAS item each satisfies. Unkeyed entries are flagged `UNKEYED` and cannot be cited as compliance evidence.

---

## GTM-readiness gate (the single check)
GTM motion (Part 3 §3.2) starts only when **G1 ✓ G2 ✓ G3 ✓ G4 ✓ G5 ✓**, verified against live systems. The B4 impact-capital channel is the one exception — it has no remediation dependency and can open in parallel today.

**Sequencing:** G1 (hours) → G2 + G3 in parallel (days; G3's elicitation build and G2's RAI spec share the MCP substrate — build together) → G5 (days) → G4 (week+, gated on hiring). Realistic earliest GTM-ready: **~2–3 weeks** on the platform/tooling gates, longer on the second-maintainer human gate. State that honestly to the board; do not compress G4.

---

# Appendix — Adversarial audit of `neuroos-prototype.html`

Audited as an attacker and as a red-team assurance reviewer. The prototype is the personal/mission substrate (NeuroOS ↔ the recovery-funded HumanAIOS mission). It has **none of the Protect controls this session built**, which is the through-line finding.

**A1 — Sensitive data at rest in plaintext [HIGH].** Recovery inventory (resentments, fears, harms/sex-conduct) and an LLM API key persist in `localStorage`/`sessionStorage` unencrypted. Any XSS, shared device, or browser-extension read exposes the most sensitive category of personal data in the app. *Fix:* never persist secrets; gate sensitive views behind explicit consent; consider not persisting inventory at all, or encrypting with a session passphrase.

**A2 — Stored-XSS surface [HIGH].** User text (WIP slots, inventory notes, log) rendered into the DOM risks stored-XSS if any path uses `innerHTML` without escaping. *Fix:* escape all user input on render (`textContent`, not `innerHTML`); this is the personal-OS analog of IC-061 intake-untrusted-input — treat user input as untrusted.

**A3 — Untrusted LLM egress [MED].** API base URL is user-supplied and unvalidated; recovery context sent to an arbitrary endpoint is an exfil path. *Fix:* allowlist endpoints; explicitly exclude recovery-inventory fields from any prompt payload (the app warns but does not enforce — procedural, not mechanical).

**A4 — No audit trail [MED].** Ironic for this program: the personal OS has no append-only log of state changes. *Fix:* add a local append-only action log (the P-model Phase-3 "every output" mapping applied to self).

**A5 — Accessibility failures [MED].** `maximum-scale=1.0, user-scalable=no` disables zoom; status conveyed by color-only dots; dense small mono. *Fix:* allow zoom; add text labels beside color; respect `prefers-reduced-motion`; visible focus.

**A6 — Consent gate on sensitive views [MED].** Inventory/amends open with no lock on a shared device. *Fix:* a mechanical consent gate — the earned-autonomy pattern applied to personal data: sensitive lanes require explicit unlock, not just a click.

**Mapping to session work:** every fix above is a Protect/Detect control this session already designed for the platform. The redesigned console (`humanaios-console.html`) embodies them: escaped rendering (A2), no persisted secrets (A1), append-only session log (A4), zoom + reduced-motion + focus + text-plus-color status (A5), and consent-gated sensitive panels (A6).

*— Z1, acting CIO. Rulings, ratifications, landings remain Z2/Z3 authority. GitHub and MCP-spec procedures verified against 2026 docs at drafting; re-check before executing.*
