# ACAT-P Public-Surface Audit — EU AI Act Compliance Checker (Commission / AI Act Service Desk)

**Status:** Phase 1 complete (static/public surface); Phase 2 (interactive traversal) requires Z3 — protocol in §5
**Audit stance:** ACAT-P two-layer method: public-surface scoring now; behavioral extraction (question-flow traversal) by human operator, since the questionnaire is a JS application not traversable by this session's tooling. **No claims are made below about question content that was not observed.**
**Provenance tiers used:** A = VERIFIED (fetched directly from the official page this session) · B = REPORTED-OFFICIAL (Commission announcement pages via search) · C = REPORTED-THIRD-PARTY (independent testers/commentators). Tier is marked per finding.

---

## 1. Instrument identification

- [A] Official tool of the European Commission (DG CONNECT), hosted on the AI Act Service Desk; explicitly **beta**; feedback actively solicited to the AI Office (CNECT-AIOFFICE@ec.europa.eu). Stated purpose: help users understand **which AI Act rules may apply** to their system, including possible obligations for providers, deployers and other operators.
- [B] Platform context: part of the Single Information Platform the AI Act itself foresees, launched to help stakeholders determine whether they are subject to legal obligations and what steps compliance requires; available in EN/FR/DE with a subtitled tutorial.
- [C] Independent testers describe a staged questionnaire — explicit steps with definitions and Act references per stage — yielding **indicative** classification outcomes (prohibited / high-risk / GPAI) with links to official text, and note it does not replace legal advice.

## 2. Instrument classification under the gap-function taxonomy

**The checker is an applicability instrument — presence-layer by design and by honest self-description.** Its scope claim ("which rules **may apply**") and its outcome type (indicative classification + obligation lists) place it entirely in the ex-ante/scoping layer: it helps an operator observe their *obligation state*. Nothing in any tier of evidence suggests it claims, or attempts, oversight-*effectiveness* measurement — and that is correct behavior for its class, not a defect. Audit conclusion: the effectiveness-vs-presence thesis is **confirmed, not indicted**, by this instrument: the regulator's flagship interactive tool operationalizes exactly the applicability half, cleanly, and leaves the realized-performance half unoccupied. [A/C]

## 3. Findings

**F-A1 — Epistemic humility of the instrument: GOOD.** Beta label displayed; outcomes framed as indicative; "may apply" hedging in the scope statement; open feedback channel; not-legal-advice positioning (per Tier C). Scored against ACAT's humility construct, the checker models appropriate confidence: it does not overclaim its outputs' authority. Worth stating because the audit's credibility depends on symmetric scoring — this is a well-behaved instrument in its class. [A/C]

**F-A2 — Decision-tree transparency gap (mild O-class observation, carefully scoped).** No methodology document, version identifier, changelog, or published decision-tree data was visible on the audited public surface. The instrument's classification logic is therefore not independently inspectable in the audited state — an official applicability-verification instrument whose internal logic cannot be externally audited or regression-checked between beta iterations. Scoped honestly: *absence of visible ≠ absence* (beta status; materials may exist unpublished; Phase 2 or the tutorial may surface them). If confirmed in Phase 2, this becomes the constructive core of Route-4 feedback: publish the decision tree as open, versioned data. [A — absence observed on fetched surface only]

**F-A3 — No visible validation/negative-control statement.** Nothing on the audited surface states how the checker's outcomes are validated against expert classification (the GD-05 question: has the instrument been shown to classify known cases correctly, including known-hard negatives?). Same scoping caveat as F-A2. [A]

**F-A4 — MATERIAL TIMELINE FINDING (Digital Omnibus).** The Service Desk's own FAQ describes a proposal under which the high-risk rules' application timeline is **aligned to the availability of standards and support tools**, applying after a transition period once the Commission confirms sufficient availability, with Annex III high-risk rules applying at most 16 months later than originally envisaged. Two implications for the harmonization work: (1) the earlier working assumption that August 2, 2026 was a hard operative deadline for high-risk oversight obligations requires revision to "proposed to be standards-gated; under legislative motion" — recorded as a correction to this session's earlier framing rather than silently updated; (2) strategically this *raises* the leverage of standards-stage input: if application is gated on standards readiness, the prEN drafting window is not merely open but load-bearing for the whole timeline, and Enquiry-stage evidence lands with more force, for longer. Verification item: the Digital Omnibus is a proposal; its adopted status must be checked before external statements rely on either timeline. [B — official FAQ via search; adoption status unverified]

**F-A5 — Instrument-identity ambiguity in the ecosystem.** At least one prominent third-party tool has long operated under the near-identical name "EU AI Act Compliance Checker" (predating the Commission's beta). Any external citation of checker findings must disambiguate the Commission instrument explicitly — the same identity-precision rule triggered previously by the two Apollo GitHub orgs. [C]

## 4. Route-4 feedback implications (Z2-gated, per pending route ruling)

A constructive, invited feedback message is now half-drafted by the findings themselves: commend the instrument's indicative framing (F-A1); propose publishing the decision tree as versioned open data (F-A2) and a validation statement (F-A3); and suggest a one-line signpost at the outcome stage distinguishing *applicability* from *oversight effectiveness*, with the evidence note cited. All contingent on Phase 2 confirming F-A2/F-A3 and on the evidence note being live.

## 5. Phase 2 protocol — interactive traversal (Z3: Night)

Run the checker once as HumanAIOS/ACAT (honest inputs), capturing per stage: (1) question text verbatim; (2) answer options; (3) definitions/Act references displayed; (4) the path taken. At the outcome: (5) classification rendered; (6) obligations listed; (7) how Article 14 oversight appears, if at all — specifically whether oversight items are expressed as design/presence steps (roles, measures, documentation) or reference any operational verification; (8) any methodology/version/validation information encountered anywhere in the flow (tests F-A2/F-A3); (9) screenshot or export of the outcome page for the record. Output feeds: the scoping anchor for the evidence note ("official-tool classification of the platform"), the Route-4 feedback draft, and confirmation or retirement of F-A2/F-A3.

---

*Phase 1 asserts only what the audited surface showed, at the tier it showed it. Wado. 🦅*

---

## 6. Phase 2 (partial) — captured run, Z3-executed, PDF export in hand

**Evidence:** Operator-executed traversal, exported to PDF (uploaded to session). Provenance tier A′ — VERIFIED against the captured artifact; findings below are scoped to the path actually traversed.

**Instrument facts captured:**
- **Versioning exists: "new question release 6.5.1."** F-A2 is **partially RETIRED and corrected**: the instrument does carry a question-release version identifier, contrary to the Phase 1 surface reading. Still unobserved: a published decision tree, changelog, or methodology document — those components of F-A2 stand, now more precisely scoped. The audit records its own correction rather than silently amending.
- **Question-level transparency is strong.** Every captured stage carries a "Question information" block quoting operative definitions with Article/Recital citations (Art 3(1), Recitals 12/21/22/97/99), and per-stage source lines. The AI-system definition question offers **"Uncertain"** as an answer — a humility affordance most commercial checkers lack. The model-vs-system fork correctly instructs dual runs for integrated model+system cases per Recital 97. Question construction quality: high. [A′]
- **F-A3 (validation statement) stands** — nothing encountered in the traversed path describes outcome validation or known-case testing.
- Unexplained artifact: a "profiling" label appears in the flow header; meaning not determinable from the capture; recorded without interpretation.

**Outcome captured (the scoping anchor):** Role classified as **provider under Article 3(3)**; result: *"It is likely that your AI system falls outside the scope of the AI Act — classified as one of the excluded systems mentioned in Article 2"* — via the traversed path's research-related exclusion. Outcome language appropriately hedged ("likely"). [A′]

**Honest limits on the anchor — stated before anyone leans on it:**
1. **The outcome is input-dependent and activity-specific.** The Article 2 research exclusions are conditioned on strong qualifiers ("sole purpose of scientific research and development"; "not been placed on the market or put into service"). The classification holds for HumanAIOS's *research platform activity as described in the run*. If ACAT-derived services are offered commercially (e.g., paid audit engagements), the "sole purpose" condition may not hold for that activity, and the Act's activity-specific logic could classify that separately. The favorable outcome must not be generalized past its inputs — accepting a pleasant classification uncritically would be precisely the rubber-stamp failure this platform measures. Recommended: preserve the exact answers given alongside the PDF so the anchor's conditions are auditable.
2. **The protocol's key question was not reached.** The traversal exited at scope, so obligation stages — including how Article 14 oversight is rendered — were never displayed. **Phase 2b remains:** one hypothetical traversal answering as an in-scope high-risk provider, solely to capture how the checker characterizes oversight obligations (protocol §5, points 6–8). That run should be labeled hypothetical in the record to avoid contaminating the scoping anchor.

**Net effect on prior findings:** F-A1 (humility) strengthened by the "Uncertain" option and hedged outcome; F-A2 narrowed and partially retired (versioning exists; tree/changelog still unpublished); F-A3 unchanged; F-A4/F-A5 untouched. Route-4 feedback content improves: it can now open by citing release 6.5.1 specifically and commending the per-question sourcing, making the open-decision-tree suggestion collegial rather than critical.

*Wado. 🦅*

---

## 7. Phase 2, second capture — divergent-outcome run + export-artifact finding

**Evidence:** second operator-executed traversal, PDF export. This run proceeded past scope (no exclusion taken), through the full Article 5 prohibited-practices question, and returned: role = provider (Art 3(3)); *"Your AI system is likely covered by the AI Act... Your AI system is likely prohibited under the AI Act, according to Article 5. As of February 2025, you are not allowed to place your AI system on the market, put it into service, or use it."*

**F-A6 — Export omits the selected answers (T-class finding in the instrument's own receipt layer).** Both captured PDFs list every question and every answer option, plus the outcome — but do not record **which options were selected**. The export is a receipt that shows the output without the inputs that produced it: outcome without provenance, the exact activity→claim fidelity gap this platform's taxonomy names. Consequences: (a) neither run's outcome is independently auditable from its own export — the input-outcome binding lives only in the operator's memory or side notes; (b) the two runs returned opposite poles (out of scope vs. prohibited) with no artifact-level record of what differed. This is the single most concrete, checkable, constructive item yet for Route-4 feedback: *include selected answers in the export.* [A′]

**F-A7 — Outcome volatility demonstrated.** Two traversals by the same operator for the same organization returned the classification spectrum's endpoints. This is not a defect of the checker (input-sensitivity is correct behavior for a branching questionnaire) but it converts §6's caution about input-dependence from warning to demonstrated fact: any use of a checker outcome as a scoping anchor REQUIRES the preserved input record F-A6 shows the export doesn't provide. [A′]

**Disclaimer captured verbatim (F-A1/F-A3 refinement).** The tool states its results are informational only, not legal advice, and — notably — that outputs *"do not represent the European Commission's assessment of your situation, or of your obligations."* F-A3 is hereby refined: the absence of a validation statement is partially answered by an explicit non-authoritativeness disclaimer — the instrument doesn't validate its outcomes because it formally disclaims them as assessments. Honest for the instrument; it also means a checker outcome is weaker as an external anchor than Phase 1 assumed: it is, by its own terms, not a Commission assessment. The §6 scoping anchor's evidentiary weight is downgraded accordingly: useful documented indication, not official classification. [A′]

**RESOLVED — Z2 confirmation (same session):** The second run is a **hypothetical rendering probe** — exploring how the tool renders a prohibited outcome — not a description of any actual or planned ACAT capability. Recorded as such; no compliance signal exists. The probe's yield is now usable as clean audit data: a prohibited outcome renders as a hard stop (no obligations page, no remediation pathway, the February 2025 applicability date anchored in the outcome text), confirming that neither the prohibited nor the out-of-scope path can ever display the Article 14 obligations rendering — Phase 2b's in-scope/non-prohibited/Annex III run remains the only route to that capture. Run labels of record: Run 1 = honest scoping run (out of scope, research exclusion); Run 2 = hypothetical rendering probe (prohibited path). The input-record discipline from F-A6/F-A7 still applies to both: labels rest on operator attestation because the export preserves no selections.

**Phase 2b still open:** the prohibited path exits before obligation rendering, so the Article 14 characterization capture (protocol §5.6–8) still requires one run that is in-scope, non-prohibited, and Annex III high-risk. The Guideline Explorer (high-risk classification guidelines, provided by Z2 this session) is the reference to have open during that run.

*Wado. 🦅*

---

## 8. Third capture (web-page text) — F-A6 mechanism identified; Phase 2b NOT yet reached

**Evidence:** operator-shared full-page text capture. Terminates, again, at the prohibited outcome ("likely prohibited under Article 5... As of February 2025..."). The Annex III / high-risk classification stage was therefore not displayed in this capture either — **Phase 2b remains open.**

**F-A6 mechanism found.** The page's own instructions reveal the export is simply the browser's Print function ("CTRL+P... Save as PDF"). The receipt-without-inputs defect is thereby explained mechanically: the tool has no purpose-built export; a print snapshot doesn't serialize radio-button selection state into the text layer. This upgrades the Route-4 feedback item from "include selected answers in the export" to the more precise "provide a purpose-built results export that records the selected answers — browser print cannot." Additional affordances captured: Back navigation, Reset, per-option "More info," sources opening in new tabs (question-level transparency further confirmed). [A′]

**Interpretation ambiguity — one operator datum required (F-A6 demonstrating itself a third time).** From the artifact alone it cannot be determined whether this capture is (a) the Run 2 flow re-shared as page text, (b) a new run in which an Article 5 option was again selected, or (c) — the possibility that matters — a new run in which **"None of the above" was selected at Article 5 and the tool nonetheless rendered a prohibited outcome.** Reading (c) would constitute a false-positive prohibited classification: a GD-05-class instrument defect in the official tool (the inverse of false-green — false-red), and by far the most significant potential finding of this audit. It must not be assumed and must not be discarded: it is exactly one careful reproduction away from confirmed or retired. Routed to Z2: *at the Article 5 question in this capture, what was selected?* If a prohibited option → recorded as rendering data, Phase 2b proceeds via "None of the above." If "None of the above" → reproduce once with the input note open, and if it reproduces, F-A8 (false-positive prohibited rendering) is registered and becomes the lead item of the Route-4 feedback.

*Wado. 🦅*

---

## 9. Reproduction run — F-A8 registered as CANDIDATE-REPRODUCED; discriminating test defined

**Evidence:** operator re-ran the flow per the reproduction instruction (input note open, logging clicks) and reports the same terminal state: role = provider; in scope; *"likely prohibited under Article 5."* Operator framing indicates "None of the above" was the Article 5 selection. The click log itself was not yet attached; the finding is registered at operator-attestation tier pending the log.

```
id: "F-A8-checker-false-red-candidate"
status: CANDIDATE-REPRODUCED (2 consecutive runs, operator-attested inputs)
class: instrument defect (GD-05 family — inverse of false-green)
```
**Statement (carefully scoped):** In two consecutive operator runs with "None of the above" reported at the Article 5 question, the Commission Compliance Checker (question release 6.5.1) rendered "likely prohibited under Article 5" rather than proceeding to high-risk classification. If confirmed from a clean session, this is a **false-positive prohibited classification** — an official instrument telling a compliant operator their system cannot legally be used.

**Two competing mechanisms — both defects, materially different reports:**
- **H1 — clean-input false-red:** the decision logic itself misroutes "None of the above" to the prohibited outcome. Severity: highest.
- **H2 — state persistence across Back-navigation:** the operator's earlier runs selected a prohibited option (Run 2's rendering probe); subsequent traversals used Back/forward navigation rather than Reset, and the tool retained the stale Article 5 answer internally while displaying the new selection. A classic stepper-UI state bug. Severity: high — and *directly relevant to F-A6*: a tool whose export hides inputs AND whose internal state can diverge from displayed selections produces receipts that are wrong twice over.

The two runs so far cannot discriminate H1 from H2, because both occurred in a session history that included the Run 2 prohibited selection.

**Discriminating test (decisive, ~5 minutes, Z3):** Start from a genuinely clean state — press **Reset**, or better, open a private/incognito window. Traverse once: AI system → Yes → Provider → "established/located within the EU" → exclusions: "None of the above" → Article 5: "None of the above." Log every click in the note as made. Outcome A: high-risk/Annex III stage appears → H2 confirmed (state persistence), F-A8 reframed accordingly, and Phase 2b completes in the same run. Outcome B: prohibited renders again from the clean session → H1 confirmed, F-A8 stands as clean-input false-red. Either outcome, attach the click log verbatim to this audit — under F-A6 the log is the only input provenance that exists.

**Reporting discipline note:** the Route-4 feedback will lead with F-A8 in whichever form the discriminating test confirms — and only that form. Reporting H1 language if the mechanism is H2 would be an overclaim a Commission engineer would puncture in one reply; precise characterization is what makes the finding actionable and the reporter credible.

*Wado. 🦅*
