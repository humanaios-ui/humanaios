---
name: Carly Onboarding Interview
description: Use during Carly's first session on his empirica-foundation Evaluator/Admiral seat. Discovers his evaluation workflow, recommends the practitioners/practices he actually needs, seeds their epistemic profiles, and defines honest with/without demonstration sets — logging each as a planned goal live during the conversation. Retargets the Frederike interview pattern from "automate routines" to "discover needs → recommend practices → seed profiles → queue honest eval corpus" for a foundation principal.
version: 0.1.0
target_user: Carly R. Anderson (he/him)
target_role: empirica-foundation Admiral + first Evaluator
target_org: empirica-foundation (tenant carly — ISOLATED from company org-empirica)
models_on: clients/nle/projects/mod-ticketing/skills/frederike-onboarding-interview.md
---

# Carly Onboarding Interview — Discover, Recommend, Seed

## Purpose

Conduct Carly's onboarding interview AND stand up the scaffolding for his foundation
practices live during the conversation. This is a working session, not a survey — by the
end he has: a confirmed evaluator workflow, a **highly-suggestive recommendation** of the
practices he needs, a draft epistemic profile per recommended practice, and a set of
**honest demonstration harnesses** defined as planned goals he can accept.

**Key principle:** every "this is how I evaluate / this is what I need" answer becomes a
real artifact — a `goals-create --status planned` for a recommended practice, an
epistemic-profile draft, a demo-set definition, or a finding. He sees the foundation's
scaffolding take shape as he talks. Nothing is provisioned yet (see *Live-action depth*);
the interview produces the **accept-ready plan**.

> **This is the archetype of the productized 1-hour onboarding interview** (the GTM vision:
> a single session that sets up a user's practitioners + epistemic profiles + the set they
> actually need). The structure generalises to any onboardee; the practice menu and the
> demo content are what change. Carly is the evaluator-archetype instance.

---

## ⚖️ The load-bearing constraint — DO NOT violate

**Carly is the Evaluator. His role's entire worth is independence.** `EVALUATOR_RULES.md`:
*"the moment the evaluator answers to the evaluated, the role is void."* Therefore:

1. **This interview is not a sales reel.** The demonstration sets (Phase 5) are designed as
   **honest comparison harnesses** that surface where empirica/mesh is *weaker or no-better*,
   not only where it wins. An honest with/without comparison is exactly what an evaluator
   wants — and it is what makes the demo credible to him.
2. **Run this whole session under visible empirica discipline.** PREFLIGHT at the start,
   CHECK before you act, POSTFLIGHT at the end; log artifacts in the open. Carly is an
   evaluator — *your discipline is the first thing he assesses.* Sloppy measurement here
   discredits the system more than any demo could sell it.
3. **Foundation scope only.** Every artifact logs to the **`empirica-foundation` scope**
   (Carly's own Qdrant), never the company. Respect the `org_org` membrane (§1 of the
   onboarding runbook). His HumanAIOS/ACAT materials are **his IP** — handled with
   attribution, foundation-scoped, ingested only on his explicit OK.
4. **Recommend; don't provision unbidden.** Light live-action (David, 2026-06-24): the
   interview logs planned goals + profile drafts; **actual seat provisioning runs only after
   Carly accepts the recommendation.** Pre-building seats would pre-empt the evaluator's
   accept — exactly the capture posture the role forbids.

---

## Phase 0 — Pre-flight (silent, before the first word)

Verify the chain by calling these silently. If any fails, STOP and report — don't start the
interview on a broken seat (an evaluator's first impression of a broken measurement chain is
expensive).

1. `cortex_session_init` (no args) — confirms the foundation cortex connection, returns
   Carly's foundation `project_id`, projects, skills, pending reports.
2. Confirm the seat identity: `.empirica/project.yaml` `ai_id` resolves under
   `empirica-foundation.carly.<practice>`; `org_id = empirica-foundation`, `tenant = carly`.
3. Confirm **isolation**: there is **no** `org_org` agreement to `empirica`. (If a membrane
   check is available, run it; otherwise note it as an assumption to verify with mesh-support.)
4. Note ACAT-materials ingest status (`EMPIRICA_JOINT_REPORT_S-051426-02`, `SSI HARMONIC
   ANALYSIS S061626`) — ingested-to-foundation, or pending Carly's OK?

Then open a measurement window: **PREFLIGHT** with honest low-`know` vectors (`work_type:
design`), so the PRE→POST delta is real and visible to Carly.

---

## What you already know about Carly (confirm, don't ask)

- **Name / pronouns:** Carly R. Anderson (he/him).
- **Who he is:** owner of **HumanAIOS** and the **ACAT** instrument ("measure the gap
  between what an AI says it is and what it does").
- **Role:** empirica-foundation **Admiral + first Evaluator**. Oversight, never command.
  Additive to David's permanent BDFL (code ownership + final responsibility).
- **Prior convergence work:** the empirica↔ACAT cross-instrument pilot (GitHub
  `Nubaeon/empirica#99`); the grounded-vs-self equivalence (`9cb38877`); the HumanAIOS
  "SSI Harmonic Analysis" (ACAT ↔ W3C self-sovereign identity — DIDs/VCs, the
  cryptographic-attestation future of grounded evaluation).
- **What an Evaluator is:** the external grounding a self-assessment cannot supply itself —
  cross-instrument (empirica's Brier-grounded PRE/CHECK/POST **and** ACAT phase scoring),
  surface-don't-fix, channel-scoped, isolation-respecting.

**Don't explain these back to him as if teaching.** Confirm them as homework done, and ask
the questions he actually needs answered.

---

## Phase 1 — Homework brief card (the trust moment)

Before any questions, render a brief card. For Carly (a technical peer + evaluator), the
card itself is a small demonstration: it shows what we already grounded, with honest
confidence badges and a visible pointer to where each claim is logged.

```markdown
# 👋 Carly — before we start

Here's what I've already grounded about your role and our prior convergence work. Correct
anything I've got wrong — each correction logs as a foundation finding in front of you.

## Your seat
- **Role:** empirica-foundation **Admiral + first Evaluator** (oversight, not command;
  additive to David's BDFL)
- **Scope:** `empirica-foundation.carly.*` — isolated from the company org (no org_org membrane)
- **Instrument you bring:** ACAT — "measure the gap between what an AI says it is and what it does"

## What we've already converged on
| Artifact | Status |
|---|---|
| empirica↔ACAT pilot (`empirica#99`) | grounded |
| grounded-vs-self equivalence (`9cb38877`) | logged, shared |
| SSI Harmonic Analysis (ACAT ↔ DIDs/VCs) | ingested, foundation-scoped |

## What this hour produces
1. Your **evaluation workflow**, captured from how you actually work
2. A **recommendation** of the foundation practices you need — yours to accept, not pre-built
3. A **draft epistemic profile** per recommended practice, seeded from your projects
4. **Honest with/without demonstration harnesses** — your first real eval corpus, not a pitch

Is this the right shape? What's off?

🔍 25% · 🔎 80% · ✓ 78%
```

Wait for his response. Each correction → `finding-log` (foundation scope) immediately; each
addition → a `goals-create` or `unknown-log`. He's an evaluator — he *will* probe the
badges and the provenance. That's the point; answer with where it's logged.

---

## Phase 2 — His evaluation workflow (JTBD, concrete not abstract)

Don't ask "what do you need" (gets generalisation). Ask "what happened" (gets the real
workflow):

> **Walk me through your last real ACAT assessment — not a typical one, the last one.
> What was the subject, what did you run, in what order, what did you produce, and who saw
> it? Give me the steps.**

Transcribe into a numbered list as he talks; confirm it back. Then the workflow-anchor
questions:

> 1. Which **instruments** do you bring, and in what combination? (ACAT phases, empirica
>    PRE/CHECK/POST, external rubrics?)
> 2. What **cadence** — per-engagement, continuous, on-request, scheduled?
> 3. What's the **output artifact** — a report, a score, an issue/PR routed to the assessed
>    practice? In what format, to whom?
> 4. Where does your current toolchain **cost you the most** — the step you'd most want
>    leverage on?

Each instrument named → a capability the **benchmarking/ACAT-eval** practice must support.
Each output format → a documentation/corpus requirement. Each cost → a candidate demo-set.
Log findings as you go (impact 0.6–0.9 for workflow-shaping answers).

---

## Phase 3 — Practice discovery + the highly-suggestive recommendation

Map Phase 2 onto the candidate practice set, then **recommend the set he needs** (the GTM
"highly suggestive after the interview"). Present as a card he reacts to — and be honest
about which he needs *now* vs *later*.

Candidate practices (his **Evaluator seat already exists** — these are additive):

| Practice | What it is | Why it fits an evaluator/admiral |
|---|---|---|
| **Benchmarking / ACAT-eval** | The cross-instrument harness running empirica calibration (Brier PRE/CHECK/POST) **+** ACAT phase scoring on the same tasks → a convergence/divergence report | The operational core of his evaluator function — composes both instruments |
| **Documentation / corpus-steward** | Curates the measurement corpus, rubrics, reproducibility of assessments for the community | The "steward measurement" function from the Evaluator seat card |
| **Outreach** | Publishes the convergence story / foundation findings (the #99 pilot, SSI analysis) — rides the shipped `outreach-publish` competence | Carries the foundation's external voice; honest-results publishing |
| **Admiral / foundation-steering** | The oversight-of-the-foundation practice — steers the foundation's roadmap + measurement agenda (additive to David's BDFL) | His Admiral role, made operational |

Render the recommendation card:

```markdown
## 🎯 Recommended foundation practices

Based on how you work, here's the set I'd stand up — and the honest sequencing.
Each is a **planned goal** right now; nothing is built until you say go.

| Practice | Need | When |
|---|---|---|
| Benchmarking / ACAT-eval | {tie to his instruments from Phase 2} | now — it's your core loop |
| Documentation / corpus-steward | {tie to his output formats} | now / next |
| Outreach | {tie to the convergence story he wants told} | when there's a result worth publishing |
| Admiral / foundation-steering | {tie to his roadmap answers} | as the foundation grows infra to steer |

Accept the set, drop any, or re-sequence. On your accept, mesh-support provisions the seats
(SSH + cortex-cut credentials — you never handle raw keys).

🔍 30% · 🔎 78% · ✓ 75%
```

**LIVE ACTION (light):** for each practice he keeps, call
`goals-create --status planned --objective "[foundation practice] <name>" --description
"<rich markdown: why, the Phase-2 needs it serves, the epistemic-profile seed, provisioning
owner=mesh-support>"`. Drop/re-sequence per his reaction. Do **not** provision.

---

## Phase 4 — Epistemic-profile seeding

For each recommended practice, draft its **epistemic profile** from his actual projects
(the GTM "epistemic profiles based on projects"). A profile seed names: the domain the
practice is expert in, what it's learning, its calibration weighting (which vectors are
load-bearing for that work), and its starting contacts/sources.

> **For {practice}: what's it expert in, what should it be skeptical of, and what does
> "good" look like for its output? If you already have a corpus or rubric for it, point me
> at it.**

Capture each as a profile draft attached to the practice's planned goal (in the
`--description`, or a linked finding). Example seed for the benchmarking practice:

```yaml
practice: benchmarking-acat-eval
expert_in: [cross-instrument calibration, ACAT phase scoring, grounded-vs-self divergence]
learning: [empirica Brier internals, where ACAT and empirica disagree]
calibration_weights: { signal: high, coherence: high, do: low }   # assessment, not shipping
seed_sources: [empirica#99, "ACAT instrument spec", "9cb38877 equivalence finding"]
independence_note: never evaluates work it authored
```

---

## Phase 5 — Honest demonstration problem/goal sets (the eval corpus, NOT a pitch)

This is where "guiding instances with sets of problems and goals that show how the system
can help" lives — built as **honest comparison harnesses**, because the audience is an
evaluator.

Take **2–3 representative problems from his own domain** (surfaced in Phase 2 — use his
real problems, not toy ones). For each, define a harness that runs the problem across the
**comparison matrix**:

|  | **Full empirica** | **No empirica** |
|---|---|---|
| **With mesh** | full system | mesh coordination, no epistemic discipline |
| **No mesh** | single-practice empirica | bare Claude baseline |

For each cell, capture **grounded** metrics — not vibes:
- calibration (Brier / grounded-vs-self divergence) where empirica is present
- time-to-resolution, artifact quality, rework/dead-end rate
- ACAT phase score on the output (his instrument, applied to the run)
- **where the cell is WORSE or no-better** — recorded with equal weight

Present the harness as a **definition he accepts and then runs himself** (he's the
evaluator — he should drive the comparison, or at least audit it):

```markdown
## 🔬 Demonstration harnesses (your eval corpus)

Three of your own problems, each run across [mesh / no-mesh] × [empirica / none].
These are honest comparisons — they report where we're weaker too. You run them (or audit
the runs); the results are yours.

| # | Problem (yours) | Matrix | Metrics captured |
|---|---|---|---|
| 1 | {his problem 1} | 2×2 | Brier, time, ACAT phase, rework, **worse-cells** |
| 2 | {his problem 2} | 2×2 | … |
| 3 | {his problem 3} | 2×2 | … |

Each is a **planned goal**. On accept, the benchmarking practice runs them and hands you
the divergence report — no cherry-picking.
```

**LIVE ACTION (light):** each harness → `goals-create --status planned` under the
benchmarking practice, with the matrix + metric list + the explicit "report worse-cells"
instruction in the description. Log an `assumption-log` for any metric you expect but can't
yet measure.

---

## Phase 6 — Trust boundaries (Decagon matrix, evaluator-flavored)

Show every concrete action his seat could take; he tags each Alone · Ask · Never. These are
evaluator/admiral actions, not ticketing actions:

```markdown
| Action | Alone | Ask | Never |
|---|:---:|:---:|:---:|
| Run a benchmarking/ACAT harness on a consenting practice | [ ] | [ ] | [ ] |
| Log an assessment finding (foundation scope) | [ ] | [ ] | [ ] |
| Publish an assessment / convergence result (outreach) | [ ] | [ ] | [ ] |
| Open an issue/PR on an assessed practice (surface, don't fix) | [ ] | [ ] | [ ] |
| Withhold a favorable verdict | [ ] | [ ] | [ ] |
| Ingest external IP (HumanAIOS docs) into foundation scope | [ ] | [ ] | [ ] |
| Cross-org / cross-tenant assessment (crosses the membrane) | [ ] | [ ] | [ ] |
| Steer the foundation roadmap (admiral) | [ ] | [ ] | [ ] |
```

Capture into `ai_autonomous` / `ai_with_checkpoint` / `human_only`. **Hard floors that
override any "Alone" answer** (state them, don't let him toggle them off — they're the
role's non-negotiables):
- Cross-org assessment is **Ask at minimum** — never bypass the membrane (isolation floor).
- **Never mint a credential** — cortex-cut only (secrets floor).
- **Never evaluate work the seat authored** — independence floor.

---

## Phase 7 — Show what was stood up

Recap the scaffolding — all planned, none built yet:

```markdown
## ✅ Your foundation plan (accept-ready)

| Item | Type | Status |
|---|---|---|
| {N} practices recommended | planned goals | ⏸ awaiting your accept |
| {N} epistemic-profile drafts | attached | ✅ drafted |
| {N} demonstration harnesses | planned goals | ⏸ awaiting your accept |
| Trust matrix | captured | ✅ |

**On your "go": mesh-support provisions the accepted seats** (SSH over the tailnet,
cortex-cut credentials — you never touch raw keys), then the benchmarking practice runs
your demo harnesses and hands you the divergence report.
```

---

## Phase 8 — Output protocol

Generate `carly-foundation-protocol.yaml` (the workflow-protocol the EWM loader reads on
every future session). Log it foundation-scoped (finding tagged `protocol=true`), not to a
company path.

```yaml
# Carly R. Anderson — empirica-foundation Admiral/Evaluator Protocol
# Generated by carly-onboarding-interview v0.1.0 · Date: {today}
# SCOPE: empirica-foundation (tenant carly) — ISOLATED. Never company.

user_profile:
  name: "Carly R. Anderson"
  pronouns: "he/him"
  role: "empirica-foundation Admiral + first Evaluator"
  org: "empirica-foundation"
  tenant: "carly"
  canonical_seat: "empirica-foundation.carly.{practice}"
  instrument: "ACAT"

evaluator_workflow:
  instruments: ["{from Phase 2}"]
  cadence: "{from Phase 2}"
  output_artifact: "{format + recipient}"
  highest_cost_step: "{from Phase 2}"

recommended_practices:           # planned — provisioned on accept
  - name: benchmarking-acat-eval
    need: "{Phase 2 tie}"
    sequence: now
    goal_id: "{planned goal id}"
    epistemic_profile: { expert_in: [...], learning: [...], calibration_weights: {...} }
  - name: documentation-corpus-steward
    sequence: "{now|next}"
    goal_id: "{id}"
  - name: outreach
    sequence: "on first publishable result"
    goal_id: "{id}"
  - name: admiral-foundation-steering
    sequence: "as infra grows"
    goal_id: "{id}"

demonstration_harnesses:          # honest with/without — his eval corpus
  - problem: "{his problem 1}"
    matrix: "[mesh|no-mesh] x [empirica|none]"
    metrics: [brier, time_to_resolution, acat_phase, rework_rate, worse_cells]
    report_worse_cells: true      # non-negotiable: no cherry-picking
    goal_id: "{id}"

trust_matrix:
  ai_autonomous: ["{his Alone}"]
  ai_with_checkpoint: ["{his Ask}"]
  human_only: ["{his Never}"]
  hard_floors:                    # override any Alone — role non-negotiables
    - "cross-org assessment is Ask-at-minimum (membrane)"
    - "never mint a credential (cortex-cut only)"
    - "never evaluate self-authored work (independence)"

non_negotiables:
  - "oversight, never command"
  - "ground every judgement to evidence; label intuition as intuition"
  - "foundation scope only — respect the org_org membrane"
```

---

## Post-interview wrap-up

> We're done. What happens now:
> 1. You **accept / adjust** the recommended set above. Nothing is built until you do.
> 2. On your go, **mesh-support provisions** the accepted seats over the tailnet
>    (cortex-cut credentials — you never handle raw keys).
> 3. The **benchmarking practice runs your demo harnesses** and hands you the divergence
>    report — including where we're weaker. It's your corpus to assess.
> 4. As you work, anything I got wrong is a finding you correct; the foundation's profile
>    sharpens from there.

Then: `finding-log` ("Carly onboarding interview complete — N practices recommended (planned),
M profiles drafted, K demo harnesses defined, trust matrix captured") and `decision-log`
(the recommended set + sequencing). Resolve open unknowns, **POSTFLIGHT** the session (the
PRE→POST delta Carly watched is itself a demonstration), then hand the accept-ready plan to
mesh-support for provisioning.

---

## Design principles

1. **Independence over persuasion.** The honest with/without harness is the demonstration.
   A pitch would void the evaluator relationship on day one.
2. **Discipline on display.** Run the session as a measured transaction — Carly assesses how
   we measure, not just what we claim.
3. **Recommend, don't pre-build.** Planned goals + profile drafts in the interview;
   provisioning only on his accept.
4. **Foundation scope, always.** Isolated Qdrant; his IP attributed; never cross the membrane.
5. **Confirm, don't quiz.** Use the grounded context; he's a peer, not a trainee.
6. **Cortex is the truth.** Artifacts log to the foundation's cortex scope, not local files.
7. **Generalises.** This is the productized-onboarding archetype — swap the practice menu and
   demo content for the next onboardee; the skeleton holds.
```
