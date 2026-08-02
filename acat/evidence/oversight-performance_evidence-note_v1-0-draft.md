# Measuring Realized Oversight Performance: A Gap-Function Incident Taxonomy from a Governed AI Deployment

**HumanAIOS LLC — Public Evidence Note (v1.0 draft for Z3 publication)**
**Date:** August 2026 · **Contact:** [Z3 to complete] · **Dataset lineage:** HumanAIOS ACAT research platform; related dataset `humanaios/acat-assessments` (Hugging Face); arXiv preprint [Z3: insert ID]

## Summary

Standards and regulation for AI human oversight primarily establish *capability and process conformance*: that oversight roles are named, intervention is designed for, logs are kept, and reaction timeframes are computed. Operational *effectiveness* — whether the human layer actually catches automation's failures in deployment — typically requires post-deployment measurement, for which no explicit counterpart was identified in the standards and regulatory sources we reviewed. This note publishes the method and headline results of one working instrument for that measurement layer, from a small, fully provenance-tracked deployment, as evidence that the layer is implementable — including by a very small operator — and as input to standards drafters while the relevant texts (prEN 18229 series) remain in draft.

## Method

Every incident in our governance registry is classified by **which function of the automation↔authority gap failed**:

- **Observability (O):** the authority or its instruments could not see actual state — assertion without inspection, or verification surfaces that were blind (returning PASS regardless of reality).
- **Translation (T):** state was observable, but the compression from activity to claim distorted in transit — overstated receipts, count drift, status divergence across surfaces, ratified decisions not propagated.
- **Interpretation (I):** a faithful signal arrived and the judgment layer still failed — bandwidth saturation, unreliable signals weighted as reliable, gates that warn without consequence.
- **Execution residual (E):** discipline failures outside the gap (state visible, claims accurate).

Assignment is rule-driven at registration, append-only, and second-coded across independent reviewers; near-misses are captured in a separate low-friction class; incident severities are recorded in dollar terms where incurred.

## Headline results (observational; exploratory; single-organization longitudinal dataset)

Across N=44 registered incidents on one production platform: **Translation 43% · Observability 36% · Interpretation 18% · Execution residual 2%.**

Three findings we believe are useful to drafters and researchers:

1. **The claim layer fails most.** The modal failure is not the model and not the human — it is the compression between what automation did and what it reported. The layer that oversight decisions are actually made *from* was, in our record, the least faithful.
2. **Blind instruments are a distinct observability sub-mode.** Several incidents involved verification surfaces that passed by construction (e.g., a CI audit targeting a nonexistent path, printing PASS on every run). Functional-safety regimes address this class through mandatory proof testing of safety functions (IEC 61508-family practice); we found no equivalent requirement in the AI oversight stack reviewed, and we now require class-matched negative controls for every PASS-emitting instrument internally.
3. **Failure gravity and instrumentation were inverted.** Interpretation failures were rarest and gravest in our record — including oversight rituals performing vigilance without exercising it — and were the least instrumented class, each caught ad hoc. Our remediations (tiered ratification to ration reviewer bandwidth; trigger-based depth re-sampling of batch approvals; evidence-based revocability of automation components) target precisely this class.

## Correspondence to existing frameworks (conceptual, clause verification pending)

The taxonomy shows conceptual correspondence with EU AI Act Article 14(4): O with 14(4)(a) monitoring/anomaly detection; T with 14(4)(c) correct interpretation of output; I with 14(4)(b) automation bias and 14(4)(d) override; and with the automation dimensions of recent deployment-risk research (detection speed, decision authority, override capability — the P(H|F,A) decomposition). Our incident records carry the field that research agenda notes is absent from most AI incident taxonomies: the automation/oversight configuration in force at the time of failure.

## Limitations, stated plainly

Single organization; small N; observational and exploratory, not statistically general. Classification is judgment-tier, mitigated by rule-driven assignment and independent second-coding, with inter-rater reliability reporting planned. Absence claims ("no counterpart identified") are scoped to sources reviewed and are maintained as falsifiable: production of a covering regulatory or standards text demotes them, and we will publish such demotions. The registry records failures and captured near-misses; silent successes and false positives are not yet systematically measured (a confusion-matrix treatment is future work).

## What we offer

To standards drafters: a documented, citable failure class (false-green verification) with an established engineering remedy (proof-test/negative-control requirements) available for migration into the oversight and logging texts while they remain in draft. To researchers: an aggregated, provenance-governed longitudinal incident dataset structured around the fields the empirical validation agenda requests — automation context, expert-coded classification with measurable agreement, near-miss logging, denominators, and quantified severities. Aggregate data as published here; inquiries regarding methodology or collaboration welcome.

*Published under HumanAIOS's own disclosure discipline: this note asserts only what its registry evidences, scopes every absence claim, and was reviewed adversarially across independent AI substrates and ratified by its human operator prior to release.*
