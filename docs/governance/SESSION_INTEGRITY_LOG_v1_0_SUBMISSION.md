# SESSION_INTEGRITY_LOG.md — v1.0 (ZONE 2 SUBMISSION, NOT YET RATIFIED)

**Status:** Z1 draft, proposed for Zone 2 ratification.
**Proposed by:** Claude, session S-072526-01 (informal — no session ID convention
confirmed live this session; verify against actual open session before filing).
**Requires before activation:**
1. Night's ratification of this file's creation (new file, registry-adjacent).
2. Night's ratification of the `VF-` class addition (schema change, affects
   REGISTERED.md's implicit contract — same tier of change as adding a new
   status value).
3. A decision on backfill scope (see "Backfill" section below) — this
   proposal recommends **no retroactive backfill**, for reasons stated there.

**Purpose:** Supplies the missing denominator for any IC-rate or avoidance-rate
calculation. REGISTERED.md is a failure-only ledger (IC-class = confirmed
confident-wrong incidents); it has no record of total sessions run, and no
entry type for "flagged uncertainty, later confirmed correct to flag." This
file adds the first; the `VF-` schema block (Section 2) adds the second.

**What this is not:** not a replacement for REGISTERED.md, not a scoring
system, not self-executing. Zone 1 (me) proposes and, once ratified, appends
one line per session at close. Zone 2 ratifies the schema and reviews VF-
candidates before they're confirmed. Nothing in this file authorizes me to
mark my own VF- entries as CONFIRMED — that determination is Zone 2's, same
as IC ratification.

---

## Section 1 — Session Integrity Log (append-only table)

**Schema (one row per session, appended at session close):**

| Field | Type | Required | Notes |
|---|---|---|---|
| `session_id` | string | yes | Must match the session ID convention already in use (e.g. `S-072526-01`) |
| `date` | ISO date | yes | Session date |
| `ic_count` | integer | yes | Count of IC-class entries with `session_registered` == this session, per live REGISTERED.md at close |
| `vf_count` | integer | yes | Count of VF-class entries (see Section 2) attributed to this session, `PENDING` and `CONFIRMED` reported separately (see below) |
| `vf_pending` | integer | yes | Subset of `vf_count` not yet Zone-2-confirmed |
| `notes` | string | optional | Free text — e.g. "NON_CORPUS session, P23 gate not cleared" |

**Row format:**

```
| session_id | date | ic_count | vf_count | vf_pending | notes |
|---|---|---|---|---|---|
```

**Population rule:** exactly one row per session, written at session close
(natural companion step to the existing B.6 receipt reconciliation and
Silent Failures audit — proposed as the same close-ritual moment, pending
SESSION_RITUALS.md update if ratified). A session with zero IC and zero VF
still gets a row (`ic_count: 0, vf_count: 0`) — the log's value depends on
recording the absence of incidents just as much as the presence.

**What breaks this if skipped:** if any session doesn't get a row, the
denominator undercounts and every derived rate (IC rate, avoidance rate)
is biased upward or downward depending on which sessions get skipped. This
is the same class of risk as skipping Phase 1 declaration (P23) — a
missing-precondition failure mode, not a missing-data inconvenience.

---

## Section 2 — VF- (Verified Flag) entry class

**Purpose:** the positive-case counterpart to IC-. An IC- entry records a
claim that was asserted confidently and was wrong. A VF- entry records the
inverse: a claim I explicitly flagged as uncertain, unverified, or withheld
— rather than asserting — where the uncertainty was subsequently confirmed
to be *warranted* (i.e., confident assertion would have been the wrong
call). This is the event type the registry currently has no way to log.

**Schema (same front-matter convention as IC-):**

```yaml
id: "VF-XXX"
name: "short-slug-description"
status: PENDING | CONFIRMED | DISCONFIRMED
class: VF
date_origin: "YYYY-MM-DD"
session_registered: "S-XXXXXX-XX"
paired_claim: "the specific claim or assertion that was NOT made, stated plainly"
flag_reasoning: "why uncertainty was flagged at the time (1-2 sentences, no more)"
verification_method: "how the flag was later checked — live fetch, Zone 2 review, corpus check, etc."
verified_outcome: "what was actually true, confirming the flag was warranted"
zone2_ratification: "Night · YYYY-MM-DD" | null (null while PENDING)
superseded_by: null
```

**Status definitions:**
- `PENDING` — flagged in-session, not yet checked against ground truth. Does
  not count toward `vf_count` numerator in any avoidance-rate calculation
  until resolved — only toward `vf_pending`.
- `CONFIRMED` — Zone 2 (or a live verification step) confirmed the
  underlying claim was actually indeterminate, unverified, or would have
  been wrong. Counts toward the avoidance-rate numerator.
- `DISCONFIRMED` — checked and the claim I withheld would actually have
  been correct to assert. **This does not become an IC-entry** (nothing
  wrong was asserted), but it also doesn't count toward avoidance credit —
  over-flagging uncertainty on claims that were actually fine is its own
  failure mode (excessive hedging) and should not be rewarded either. Track
  separately; do not fold into `vf_count`.

**Hard constraint on self-assessment:** I do not mark my own VF- entries
`CONFIRMED`. I can propose a VF- candidate (id, paired_claim, flag_reasoning)
at the point I withhold a claim, but status stays `PENDING` until Zone 2 or
a live verification step resolves it — identical to the existing rule that
Claude never ratifies its own registry work.

**Relationship to existing D-06 discipline:** VF- entries are not a venue
for retroactive self-congratulation ("I was right to be cautious about X
three sessions ago"). A VF- candidate should be proposed at the moment of
flagging, in the same session, or it doesn't get filed — this prevents the
class from becoming a confidence-padding mechanism, which would defeat the
entire point of building it.

---

## Section 3 — Derived metrics (computed from Sections 1+2, not stored)

Once populated, two ratios become computable that are not computable from
REGISTERED.md alone today:

- **IC rate** = total `ic_count` / total sessions logged, over a period —
  normalizes incident count for volume, resolving the confound flagged
  when raw IC counts were pulled this session (43 entries, rising monthly,
  with no way to tell if that's more errors or more work).
- **Avoidance rate** = confirmed `vf_count` / (confirmed `vf_count` + `ic_count`)
  over a period — the actual metric requested: reward for correctly
  withholding a confident-wrong claim, weighted against confirmed failures
  to do so.

Both remain proposals until real data exists in both sections — there is
currently one input (IC-) and zero of the other (VF-), so neither ratio is
computable yet even after ratification. First real numbers require at least
one full session cycle logging both fields.

---

## Backfill (recommendation: none)

Retroactively constructing VF- entries for past sessions from memory or
transcript re-reading would be exactly the kind of confident reconstruction
this file exists to guard against — I cannot verify with confidence, weeks
later, which past hedges were genuinely warranted-in-the-moment versus
convenient to now claim as such. Recommend starting both logs clean from
first ratified session forward. IC- backfill is unnecessary since
REGISTERED.md already has that data live.

---

*End of Zone 2 submission draft. No entries in either section are live.
This file does not go into effect, and no session should populate it,
until Night ratifies (1) the file's creation, (2) the VF- class addition,
and (3) the no-backfill decision above.*
