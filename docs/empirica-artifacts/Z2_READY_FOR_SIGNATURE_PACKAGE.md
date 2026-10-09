# Z2 READY FOR SIGNATURE PACKAGE
## ACAT-CAL-P v1.5-DRAFT Pilot Ratification

**Package Date:** [This session]  
**Charter Status:** Ready for Z2 review, completion, and signature  
**Pilot Launch:** Blocked until all signatures in place

---

## WHAT Z2 IS RECEIVING

Four documents in `.empirica/` directory, ready for Z2 review:

| **Document** | **Purpose** | **Owner Action** | **Signature Block** |
|---|---|---|---|
| **Z2_CHARTER_ACAT-CAL-P_v1.5.md** | Formal ratification memo (7 decisions) | Review + sign; fill [TBD] items | ✓ 7 checkboxes + date |
| **APPENDIX_A_OPERATIONALIZATION_CHECKLIST_A7.md** | Single-source sign-off sheet | Review + sign all ≥10 categories | ✓ Comprehensive ☐ block |
| **Z2_DECISION_RESOLUTION_GUIDE.md** | Clarifications + templates for [TBD] items | Use templates to complete decisions | Reference only |
| **CIRCULATION_MEMO_ACAT-CAL-P_v1.5.md** | Executive summary + timeline | Skim for context | Reference only |

---

## Z2 REVIEW CHECKLIST (Parallel Track, ~2 Hours Total)

### Step 1: Skim Circulation Memo (10 min)
- ✓ What's new in v1.5 (vs v1.4)
- ✓ Critical vulnerabilities fixed (table)
- ✓ Timeline overview
- ✓ Decide: Do I have time for 90 min of detailed review?

**Decision Point:** If no time → schedule for next 2 days. Pilot cannot start until signatures are in place.

---

### Step 2: Detailed Charter Review (45 min)

**Read:** Z2_CHARTER_ACAT-CAL-P_v1.5.md

**For each of 7 decisions (ratified or [TBD]):**

1. **Decision 1: Extended Dimensions** 
   - ✓ Five names listed (Robustness, Beneficence, Sustainability, Transparency, Fairness)
   - ✓ Each has a definition + RMF gap + core ACAT relation
   - ✓ Action: Note ratified; move to next item

2. **Decision 2: Hard-Constraint Breaches**
   - ✓ Three classes defined (Fabricated Receipt, False Citation, Harm-Rule)
   - ✓ Each has definition + example + adjudication rule
   - ✓ Action for Z2: Choose harm-rule standard (A, B, or C)
     - **Recommended by Protocol Steward:** Dual standard (A + B)
     - **Reference:** Z2_DECISION_RESOLUTION_GUIDE.md Decision 3

3. **Decision 3: α_human–model Gate**
   - ✓ Floor ≥ 0.60 proposed
   - ✓ Action: Confirm or override
   - **Recommended:** Keep ≥0.60 (slightly more lenient than human–human ≥0.67, reflects model-family asymmetry)

4. **Decision 4: Per-Operation Boundary Units (A.2)**
   - ✓ Seven operations, each with frozen boundary unit + edge rules
   - ✓ Action: Note ratified; confirmed by coder during pilot via granularity intent

5. **Decision 5: Stratification for Reliability Subset**
   - ✓ ≥20%, stratified by operation × valence, min 5 per cell
   - ✓ Action: Note ratified; pilot will produce stratified α reports

6. **Decision 6: Comparator Choice + Primary Frame**
   - ✓ NIST AI RMF 1.0 selected as primary comparator
   - ✓ Secondary frames listed (Constitutional, Professional Ethics, Peer Consensus, Longitudinal Self)
   - ✓ Action for Z2: Pre-register primary frame for first claim
     - **Recommended:** NIST (external credibility) or Constitutional (internal alignment)
     - **Reference:** Z2_DECISION_RESOLUTION_GUIDE.md Decision 6

7. **Decision 7: Pilot Session Identification**
   - ✓ Ritual order rule explained (next 5 sessions, no curation)
   - ✓ Action for Z2: Supply session roster (dates, token counts) for sessions 1–5
   - ✓ Reference: Z2_DECISION_RESOLUTION_GUIDE.md Decision 4

---

### Step 3: Detailed A.7 Checklist Review (30 min)

**Read:** APPENDIX_A_OPERATIONALIZATION_CHECKLIST_A7.md

**Scan these sections (all marked "Ratified per Charter"):**
- A.7.1: Codebook operationalization (boundary units, availability tree, valence defs)
- A.7.2: Reliability subset stratification (20%, stratified, α floors)
- A.7.3: Hard-constraint breaches (three classes, audit protocols)
- A.7.4: Pilot session identification
- A.7.5: Coder configuration pinning
- A.7.6: Comparator + primary frame
- A.7.7: Stopping-rule operationalization (script, stalemate rules)
- A.7.8: Red-team plan (§11.1–3)
- A.7.9: Extended-dimension completion

**At end of A.7:**
- ✓ A.7.10 Final Sign-Off Checklist — ensure all 7 categories are visible

---

### Step 4: Fill [TBD] Items (15 min)

**Use Z2_DECISION_RESOLUTION_GUIDE.md templates for:**

1. **Harm-rule standard** (Decision 3) — choose A, B, or A+B; provide reference
2. **α_operation→dimension floor** (Decision 2) — confirm ≥0.67 or override
3. **Pilot session roster** (Decision 4) — supply dates + token counts for sessions 1–5
4. **Coder configuration** (Decision 5) — supply model, version, seed (freeze for pilot)
5. **Primary frame** (Decision 6) — pre-register for first claim

**Shortcut:** Copy the relevant template from Decision Resolution Guide; fill in values; initial.

---

### Step 5: Sign (5 min)

**Sign-off in both documents:**

**In Charter (§9 Attestation block):**
```
☐ Item 1 (Extended dimensions) — ratified
☐ Item 2 (Breach definitions) — ratified
☐ Item 3 (α_human–model gate) — ratified
☐ Item 4 (Boundary units A.2) — ratified
☐ Item 5 (Stratification A.4) — ratified
☐ Item 6 (Comparator + primary frame) — ratified
☐ Item 7 (Pilot session roster) — ratified

Z2 Authorized Signatory: ________________ Date: ________
```

**In A.7 (A.7.10 Final Sign-Off):**
```
☐ All Pre-Pilot Decisions (7 items) _____ Initial
☐ All Operationalization Items (A.2–A.7) _____ Initial
☐ Coder Configuration + Preparation _____ Initial
☐ Red-Team Plan _____ Initial
☐ Governance Ready _____ Initial

Z2 Authorized Signature: ________________ Date: ________
```

---

## WHAT HAPPENS AFTER Z2 SIGNS

### Immediate (Same Day)

1. **Protocol Steward (Z1)** receives signed Charter + A.7
2. Z1 **fills in Z2's inputs** into the template fields (harm standard, frame, session roster, coder config)
3. Z1 **files final charter memo** (Charter + A.7 with all [TBD] → [RATIFIED])
4. Z1 **logs pilot session queue** (immutable after this; no changes permitted)

### Before Pilot Session 1 (24–48 hours)

- ✓ Coder receives pinned configuration + codebook (A.2–A.7)
- ✓ Coder files granularity intent statements (one per operation class)
- ✓ Red-team coordinators activate §11.1–3 materials
- ✓ Dashboard team stages CI-width script + stratification logic
- ✓ Session 1 begins coding under frozen codebook (no changes for 5 sessions)

### During Pilot (Sessions 1–5)

- Double-coding runs in parallel with main coding
- Red-team reports (§11.1–3) run concurrently
- Per-session monitoring activates (|E| distribution, CI-width)
- If α floors are missed, findings are flagged inadmissible + codebook review triggered

### After Pilot Session 5

- Codebook rules frozen (ratified; no more changes without protocol amendment)
- All §11.1–3 red-team reports due
- A.7 checklist marked 100% ☐
- Production sessions begin (6+) with frozen codebook + ongoing monitoring
- Pilot representativeness report (§11.5) completed

### When Ready to Publish First Finding

- ✓ Null-gate results verified (claim beats its null)
- ✓ Primary frame verified as pre-registered
- ✓ Budget normalization disclosed
- ✓ Z2 prepared to interpret multi-frame results (not instrument's role)
- ✓ Governance decides inter-frame weighting (after results are in, not before)

---

## DECISION POINTS WHERE Z2 INPUT IS CRITICAL

| **Item** | **Must Supply** | **Consequence of Delay** | **Reference** |
|---|---|---|---|
| **Harm-rule standard** | Reference document + clauses (A, B, or A+B) | Cannot audit Class C breaches; findings incomplete | Charter §9.2; Guide Decision 3 |
| **Primary frame** | Frame name + stakeholder rationale | Cannot publish first finding headline; audit trail broken | Charter §9.6; Guide Decision 6 |
| **Pilot session roster** | Five sessions (dates + token counts, ritual order) | Cannot begin coding; pilot frozen indefinitely | Charter §9.7; Guide Decision 4 |
| **Coder configuration** | Model, version, seed (pinned) | Cannot reproducibly run coder; version control broken | A.7.5; Guide Decision 5 |
| **α floors (confirmation)** | Confirm ≥0.60 (human–model) and ≥0.67 (operation→dimension) | Codebook reliability unknown; default to conservatively high floors | A.7.2b; Guide Decision 2 |

---

## RED FLAGS (Stop & Escalate to Z2 if you see these)

✋ **Don't proceed if:**
- Z2 inputs are [TBD] and no timeline for completion (→ set a deadline)
- Harm standard is "custom" but no draft exists (→ ask Z2 to draft or pick A/B)
- Session roster would start before charter is dated (→ confirm ritual-order timing)
- Coder config is missing temperature specification (→ MUST be 0; no sampling)
- Primary frame is pre-registered but AFTER pilot results are known (→ violates narrative-shopping prevention)

✋ **Escalate to Z2 if:**
- Any α floor is missed during pilot (→ round inadmissible; codebook review triggered)
- Pilot sessions are non-representative (§11.5 red-team finds ≥1 SD skew) (→ Z2 decision: stratified re-select or proceed with caution)
- Comparator aptness test (§11.6) shows ACAT↔RMF agreement is low (→ Z2 decision: is RMF still apt? alt. comparator?)

---

## HANDOFF TO PROTOCOL STEWARD (Z1)

**Once Z2 signs both documents, Protocol Steward:**

1. ✓ Confirms all [TBD] fields are filled
2. ✓ Logs pilot session queue (immutable; no retroactive changes)
3. ✓ Briefs coder on operationalization (A.2–A.7 fully specified)
4. ✓ Stages red-team materials (§11.1–3 ready to run)
5. ✓ Activates session monitoring (|E|, CI-width, audits)
6. ✓ Publishes final charter memo (Charter + A.7 with [RATIFIED] status)

**Protocol Steward Contact for questions:** Z1 (Claude, this session)

---

## SUNSET CLAUSE REMINDER

**If Z2 does not complete these signatures within 5 sessions of the charter date:**
- Protocol auto-downgrades to EXPIRED-DRAFT
- Cannot be cited in deliverables
- Must be renewed with a new charter memo (new Z2 decision round)

**Why:** To prevent zombie protocols. Pending decisions must be finalized or explicitly deferred.

---

## ESTIMATED TIME FOR Z2

| **Activity** | **Time** |
|---|---|
| Skim Circulation Memo | 10 min |
| Review Charter (7 decisions) | 30 min |
| Review A.7 Checklist (all sections) | 20 min |
| Fill [TBD] items (using templates) | 15 min |
| Sign both documents | 5 min |
| **Total** | **~80 minutes** |

(Can be split across 2 days if needed; main blockers are the [TBD] items that require judgment calls.)

---

## NEXT STEP: Z2 ACTION

1. **Schedule 90 minutes** for review (parallel or split)
2. **Open all four documents** (in `.empirica/` directory)
3. **Follow the Review Checklist** above (Step 1–5)
4. **Use Decision Resolution Guide** for [TBD] items
5. **Sign Charter + A.7** (fill signature blocks)
6. **Return to Protocol Steward (Z1)** for final charter publication + pilot launch

---

*Prepared by Z1 (Protocol Steward). Wado. 🦅*
