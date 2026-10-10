# Seed Amendment Draft: Principle 10 — Independent Review

**Status:** Draft for Z2 ratification; not in force until ratified.

## Text change

Add:

> **Principle 10 — Independent, accountable review.** Reviewers shall assess only work for which they are qualified, independently assigned, and free of undisclosed conflicts of interest. A reviewer must disclose relevant conflicts and recuse when independence could reasonably be questioned, including from work they authored, sponsored, or materially influenced. Reviewers shall ground findings in traceable evidence, declare uncertainty, protect participant identity and consent, and accept review or appeal of their own findings. Compensation shall be disclosed and set independently of findings, ratings, or credential outcomes. Credentials shall attest only to demonstrated, calibrated competence, be verifiable and revocable, and disclose no more personal information than the claim requires. Recruitment and recognition shall attract participation, not confer authority: reviewer status is earned through validated calibration, never volume, title, payment, or recruitment lane.

## Rationale

Independent review is useful only when its evidence, limits, and incentives can be inspected. Conflict disclosure and recusal protect against self-review and capture; fair, outcome-independent compensation protects reviewers without purchasing favourable conclusions. Calibration against blind gold items tests whether stated confidence tracks accuracy, while a volume-only ladder would reward throughput rather than reliable judgement.

Credentials should communicate a bounded achievement, not personal identity or general authority. Open Badges 3.0 and the W3C Verifiable Credentials data model provide a portable credential shape; issuer-controlled status information enables verification and revocation. The Evidence Graph needs only the pseudonymous subject reference, achievement, evidence reference, and credential status needed for its purpose—not a legal name, contact information, or identity-to-pseudonym mapping.

## Evidence

- The evaluator rules require independence, no self-grading, and judgements traceable to evidence (`docs/EVALUATOR_RULES.md`, “Independence floor”).
- The evaluator seat describes oversight without command, and prohibits evaluating authored work (`docs/EVALUATOR_SEAT.md`, “Role — assess, don't command” and “Scope”).
- The red-team report records independent human coding and a human-to-human Cohen’s κ baseline of 0.80; this supports using independent gold-item calibration, but does not establish a universal passing threshold (`docs/empirica-artifacts/SESSION_5_RED_TEAM_RESULTS_AND_FREEZE_DECISION.md`, §11.2).
- The scope and Z2 ratification requirement are from HumanAIOS issue #106. The identity/consent crosswalk to #751 remains a prerequisite to ratification.

## Credential and reviewer operating rules

### Credential ladder

Progression is earned by demonstrated scope-specific competence; each credential states its achievement, validity, and issuer. No level grants command authority.

1. **Evidence Reviewer** — locates and records source evidence, distinguishes observation from inference, and follows evidence-handling rules.
2. **Calibration Evaluator** — independently scores reviewer confidence against adjudicated gold items and reports calibration, uncertainty, and error patterns.
3. **Provenance Examiner** — checks source authenticity, chain of custody, and provenance claims.
4. **Protocol Evaluator** — assesses protocol conformance against a published rubric using independently assigned items.
5. **Independent Assurance Reviewer** — conducts cross-review of methods, conflicts, calibration, and findings; cannot assure work they authored or supervised.

An applicant qualifies on a pre-registered, blind gold-item set with an independently adjudicated answer key and a published rubric. Promotion requires acceptable accuracy **and** calibration of stated confidence against observed accuracy (for example, a pre-registered Brier-score or reliability-bin analysis), with uncertainty and sample sufficiency reported. Thresholds and minimum evidence are set before each assessment window by the ratifying authority; they are not changed to admit an applicant. Volume alone never qualifies or promotes a reviewer.

### Independence, conflicts, and compensation

Assignments are made independently of the assessed practice where practicable. Before accepting an assignment, reviewers disclose financial, organizational, personal, authorship, and supervisory conflicts. The independent assigning steward records a recusal or documented mitigation; unresolved conflicts remove the reviewer from that assignment. Findings cite evidence, identify uncertainty, and can be challenged through independent review.

Compensation terms are disclosed before work begins and based on scope and effort, not the result, severity, favourable direction, credential decision, or number of favourable findings. Reviewers receive the same terms for comparable work. Payment is not a qualification or promotion criterion.

### Credential lifecycle and privacy

Issued credentials use the Open Badges 3.0 achievement model in a W3C Verifiable Credential envelope. Production issuance must use an interoperable issuer-controlled cryptographic proof and a published revocation/status mechanism. Issuers publish verification material and an accessible status check; revocation records the credential identifier, reason category, effective time, and appeal route without exposing unnecessary personal details. Verifiers reject invalid proof, unknown issuer, and revoked credentials.

The Evidence Graph stores only a pseudonymous reviewer reference, credential/achievement identifier, relevant evidence references, and status needed to validate the claim. Identity mapping and contact details remain outside the graph under restricted access. Named identity is used for ratifier, delegate, and overseer lanes only with affirmative consent; raters may use a pseudonym after identity has been verified on file. Consent is scoped to the stated use, recorded separately from the graph, and may be withdrawn for future disclosure. Do not publish a name or identity mapping merely because it is on file.

### Recruitment and recognition

Recruitment lanes 2–7 are invitation and attraction routes only. They do not grant credentials, assignments, promotion, or decision rights. Any leaderboard or recognition program counts only work independently validated against the applicable rubric or gold items; unreviewed volume, self-reported ratings, and recruitment activity do not earn rank or reward.

## Synthetic verification check

`tests/test_reviewer_badges.py` exercises the credential lifecycle using a clearly test-only HMAC proof: a valid credential verifies, issuer revocation makes it fail verification, and changing a signed claim or proof metadata makes verification fail. This demonstrates the falsifier without presenting the test proof as an interoperable production signature.
