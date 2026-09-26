# Z2 Ratification Record — MCP Grounding Rulings
**Artifact ID:** Z2-RAT-S082226-02 · **Classification:** Board / Z2 record
**Zone provenance:** Z1 proposed (gauge/signaling grounding analysis) · **Z2 (Night) RATIFIED 2026-08-22** · Z3 landing pending
**Session:** S-082226-01 · **Authority:** P21 (Z2 ratification authority). This record registers the ruling; landing remains Z3.

---

## Ratified items (Z2 language of record)

**R1 — RAI as interchange control on the tool-call.**
> "RAI should be specified as an interchange control on the tool-call itself: every coupling event resolves provenance against the attested registry, with in-toto/OpenTimestamps as the manifest format."

Effect: Registry-Attested Intake (P2) is re-specified from a general intake filter to an **MCP-native interchange control**. The unit of enforcement is the coupling event (the MCP tool-call). The mock attested-source fixture (cycle-2, sha `5e6da699…ab1a`) is superseded as a *target*: the promotion gate for F-CAND-three-outcome-discovery-pathway already requires a live in-toto/OpenTimestamps binding; this ruling makes that binding the product specification, not just the pilot's next step. The forked estate assets (`in-toto`, `python-opentimestamps`, `opentimestamps-server`) are the designated manifest substrate.

**R2 — Z2 ratification implemented as MCP elicitation.**
> "Implementing Z2 ratification as MCP elicitation rather than as a bespoke GitHub workflow."

Effect: the earned-autonomy / ratify-before-act gate (G3, P3) is implemented against MCP's enterprise-managed authorization + elicitation-for-approvals primitives (2026 stateless spec), making the Z2 gate **protocol-native** rather than platform-bespoke. Scope note recorded at ratification: the GitHub branch ruleset + CODEOWNERS + protected environment remain as the **repo-write mechanical backstop** — R2 governs the *ratification interaction layer* (how Z2 approval is elicited and recorded for agent actions), not the removal of repository-layer protection. Registry-touching agent actions pause on an MCP elicitation to Night; the repo ruleset independently blocks unratified writes.

**R3 — Evidence-level crosswalk keying.**
> "Crosswalk is keyed at the evidence level: each register entry, attestation, and counted cycle mapped to the specific EU AI Act logging article, ISO 42001 clause, or relevant regulatory modules it satisfies."

Effect: HARMONIZATION_CROSSWALK and the P-CAND-gold-standard-grounding commitment are upgraded from framework-level mapping (product ↔ standard) to **evidence-level keying** (artifact ↔ clause). Each REGISTERED.md entry, each attestation, and each counted-cycle report carries the specific regulatory module it satisfies (e.g., EU AI Act Art. 12 record-keeping / Art. 14 human oversight; ISO/IEC 42001 clause-level; NIST AI RMF function/category). The register moves from *honest* to *admissible*.

---

## Landing instructions (Z3)

1. **CROSSWALK_v2 schema** — add `evidence_key` field(s) to crosswalk entries; backfill existing register entries and the two counted-cycle reports. (R3)
2. **RAI spec revision** — author `RAI_SPEC_v0.2` specifying the gate at the MCP tool-call boundary with in-toto attestation + OpenTimestamps as the manifest format; cycle-3 pilot pre-registration binds to live attestations, not the mock. (R1)
3. **G3 gate build** — implement the Z2 elicitation flow per revised runbook G3; retain branch ruleset/environment as backstop. (R2)
4. All three land under the standing disciplines: SHA-pinned at emit, runtime-verified where interactive (IC-066 parse-not-runtime), verified against the live tree.

## Landing state

Per UNIT-RUBRIC-v1: this ratification changes `zone_stage` (Z2 passed) on the affected items; it does **not** change `landing_state`. All three remain **LAID** until Z3 lands them. Session landing rate is unaffected by ratification alone — ratified-unlanded is still operated = 0.

## Registry routing

```
Ruling record → land at humanaios-ui/operations/rulings/ (append-only)
Touches: P2 (RAI), P3 (Earned-Autonomy Gate), G3, §3.5 crosswalk,
         F-CAND-three-outcome-discovery-pathway (promotion gate now = product spec),
         P-CAND-gold-standard-grounding (upgraded to evidence-level keying)
Frozen artifacts NOT modified: PREREGISTER_intake_pilot_v2.md (sha 3ca66713…bf40),
         CIO-PILOT-S082226-02, UNIT-RUBRIC-v1, PREREG_convergence_v1.md — pre-registered
         /pinned artifacts are superseded by new versions, never edited in place.
```

*— Z2 ruling recorded by Z1. Landing remains Z3 authority.*
