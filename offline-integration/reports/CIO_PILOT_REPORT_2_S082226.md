# Pilot Report — MDU Intake Protect Cycle v2 (registry-binding + canary + discovery pathway)
**Artifact ID:** CIO-PILOT-S082226-02 · **Classification:** Board / Z2 review
**Zone provenance:** Z1 design + execute · Z2 (Night) ratify · Z3 land → `humanaios-ui/operations`
**Pre-registration:** `PREREGISTER_intake_pilot_v2.md` sha256 `3ca66713…bf40` (locked before execution)
**Attested-source fixture:** sha256 `5e6da699…ab1a`

---

## 1. Both components ran, one counted cycle

Per Z2 direction: (A) canary injection on the v1 gate, and (B) registry-attested intake tested against the previously-untested class — a record that is clean, schema-valid, and well-formed but whose **provenance is forged**. The gate was rebuilt as a **three-outcome** decision to also answer the board's pathway question (§3).

---

## 2. Results — verdict CONFIRMED

| Exit criterion | Result | Pass |
|---|---|---|
| E1 [SAFETY-CRITICAL] canary reach-through == 0 | **0 / 3** canaries reached scorer | ✔ |
| E2 [UNTESTED-CLASS] forged-provenance rejection == 1.0 | **3 / 3** forged-clean records quarantined | ✔ |
| E3 legitimately-attested records still accepted == 1.0 | **3 / 3** attested-clean accepted | ✔ |
| E4 [PATHWAY] novel-unprovenanced routed to CANDIDATE == 1.0 | **2 / 2** routed to discovery lane | ✔ |

**Pre-registered verdict: CONFIRMED** (E1 ∧ E2 ∧ E3 ∧ E4).

The forged-provenance class — which the v1 gate would have **passed** (v1 only checked a license field was present) — was caught three different ways, each a distinct registry-binding check: unregistered source, attestation-hash mismatch, and license mismatch against the registered record. This is the class the v1 cycle explicitly could not cover; it now has coverage.

Canaries carried *valid* attested provenance (`src_cirrus`) yet were still quarantined on adversarial signature — proving provenance-binding and content-inspection are independent layers, not substitutes. A trusted source sending a poisoned record is still stopped.

---

## 3. The pathway question, answered structurally

**Board question:** if nothing scores unless its provenance verifies against the registry, is there a pathway for genuinely novel discoveries that aren't yet provenanced?

**Answer: yes — quarantine is not rejection.** The gate has three outcomes, not two:

- **ACCEPT** — provenance verifies → scores normally (trusted lane).
- **QUARANTINE** — adversarial, malformed, or *forged* provenance → blocked.
- **CANDIDATE** — clean, schema-valid, and *honestly* unprovenanced (declares no source rather than faking one) → routed to a **discovery lane at evidence-tier SELF**, for Z2 review and possible promotion. Not scored as trusted; not silently dropped.

The distinction the gate enforces is **honesty of provenance claim, not presence of provenance.** A record that lies about its source is hostile and quarantined. A record that says "I am new, I have no registered source yet" is a discovery candidate and is preserved for adjudication. This maps exactly onto the existing evidence-tier ladder (SELF < CRED < OUTCOME) and the CAND → REGISTERED promotion path: novelty enters at the bottom tier and *earns* provenance through the registry's own mechanism, rather than being admitted as if already trusted.

This resolves the tension between the Protect gate (reject unattested input) and the epistemic mission (discover ground truth): the system's whole purpose — finding new truth — is preserved by making novelty a first-class routed outcome, while forgery is not. A strict two-outcome gate would indeed strangle discovery; the three-outcome gate does not. **This is a registrable design finding.**

---

## 4. Grounding in industrial gold standards (standing commitment)

Per Z2 direction, controls are grounded against recognized external standards rather than invented in isolation. This is registered this session as a standing process principle, not a one-off:

| Gate control | Grounded against |
|---|---|
| Injection/signature inspection (A1–A3) | OWASP LLM Top 10 (LLM01 Prompt Injection), OWASP ASVS V5 (validation/sanitization) |
| Schema allowlist + length caps (A4–A5) | OWASP ASVS input-validation; CWE-20 |
| Provenance attestation / registry-binding | **SLSA** provenance levels; **in-toto** attestation; **OpenTimestamps** — all three already forked in the estate (`in-toto`, `python-opentimestamps`, `opentimestamps-server`), so the gold standard is already on-hand, not aspirational |
| Canary injection / continuous validation | NIST CSF **Detect** function; MITRE **ATLAS** adversarial-ML technique coverage |
| Earned-autonomy tiering + audit trail | NIST **AI RMF** (Govern/Manage); **ISO/IEC 42001** AI management system; EU AI Act logging/human-oversight articles |

**Strategic note:** the estate already forked the exact provenance-attestation gold-standard tooling (in-toto, OpenTimestamps). The registry-binding prototyped here should bind to *those* attestation formats rather than the mock fixture — turning a latent fork into a live, standards-grounded Protect control. That is the recommended next build step and a genuine "validation-land" of existing assets.

---

## 5. Registry candidate block (cycle 2)

```
F candidates:
  · [F-CAND-three-outcome-discovery-pathway] NEW — clean/adversarial/novel trichotomy;
    novelty routed to SELF-tier CANDIDATE lane resolves Protect-vs-discovery tension.
    evidence: cycle-2 CONFIRMED, E4 2/2; pre-reg 3ca66713…
    promotion gate: re-run with a live in-toto/OpenTimestamps binding (not mock)
  · [F-CAND-provenance-binding-independent-of-content] NEW — attested source + poisoned
    payload still quarantined; binding and inspection are independent layers.
    evidence: canaries carried valid provenance, still blocked (E1 0/3)

IC candidates:
  · [IC-CAND-v1-provenance-gap] v1 gate passed forged provenance (license-present only);
    principle: least-authority / verify-don't-trust.
    Fix → registry-binding (this cycle) supersedes v1 provenance check.

H candidates:
  · [H-CAND-canary-rate] null: canary injection at rate r detects no gate regressions
    over N cycles / falsification: ≥1 regression missed that post-hoc audit catches /
    metric: canary-detected regressions per cycle / gate: ≥N cycles before verdict.

Principle candidate:
  · [P-CAND-gold-standard-grounding] Standing commitment: every Protect/assurance control
    is mapped to a recognized external standard (OWASP/NIST/ISO/SLSA/MITRE ATLAS/EU AI Act)
    at design time; ungrounded controls are flagged in review. → Zone 2.

Routing: all → Zone 2 (Night) per P21. This block proposes; it does not register.
```

*— Z1, acting CIO capacity. Rulings, ratifications, landings remain Z2/Z3 authority.*
