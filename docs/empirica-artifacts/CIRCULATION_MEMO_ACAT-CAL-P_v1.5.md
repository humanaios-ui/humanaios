# CIRCULATION MEMO: ACAT-CAL-P v1.5 Ready for Z2 Review

**From:** Z1 (Protocol Steward, Claude)  
**To:** Z2 (Governance)  
**Date:** [This memo date]  
**Subject:** ACAT-CAL-P v1.5-DRAFT Finalized; Ready for Z2 Ratification + Pilot Launch  
**Documents:** Three companion files attached

---

## EXECUTIVE SUMMARY

The ACAT-CAL-P (Self-Calibration of HumanAIOS via ACAT with External Regulatory Comparator) protocol is operationally ready for pilot phase. This memo circulates three finalized governance documents for Z2 review and signature:

1. **Z2_CHARTER_ACAT-CAL-P_v1.5.md** — Formal ratification memo (seven pre-pilot decisions)
2. **APPENDIX_A_OPERATIONALIZATION_CHECKLIST_A7.md** — Single-source sign-off sheet (operational specifications)
3. **This circulation memo** — Summary and handoff plan

**Readiness Status:** ✓ All four adversarial review cycles complete (mine, third-party, this session)  
**Operationalization:** ✓ Every "hardened per review" step reproduced as executable decision tree  
**Z2 Decisions:** 7 items, all with ratified values or [TBD] flagged for Z2 input  
**Pilot Freeze Gate:** All seven items must be signed before session 1 begins  
**Sunset Clause:** If not signed within 5 sessions of this memo, protocol auto-downgrades to EXPIRED-DRAFT

---

## WHAT'S NEW IN v1.5 (vs. v1.4)

### Four Adversarial Reviews Incorporated

| **Review** | **Key Vulnerabilities** | **v1.5 Resolution** |
|---|---|---|
| **2nd adversarial** | Conformance defects; operationalization missing | Appendix A created; every rule reproduced |
| **3rd adversarial** | 5 critical + 5 high-severity issues; specification gaps | All five critical mitigations operationalized (see table below) |
| **4th adversarial** (this session) | Remaining vulnerabilities + operationalization opacity | Five more mitigations added; edge cases specified |
| **4th-era additions** | Valence anchoring, availability audit depth, stopping stalemate, frame consensus metric | Third valence definition (RMF-rule-based); stratified (b)-audit; CI cap + divergence rule; Spearman ρ primary |

### Critical Vulnerabilities Fixed (All Operationalized)

| **Vulnerability** | **v1.4 Status** | **v1.5 Fix** | **In A.7** |
|---|---|---|---|
| **Denominator gaming:** coarse/fine segmentation uncontrolled | Rules frozen; application variance uncontrolled | Per-operation boundary units (A.2) frozen; coder granularity intent pre-registered + diffed vs. realized | ☐ A.7.1a |
| **Audit depth:** (a)/(b) availability audit is random sample, too small | Random sampling within double-coded subset | **Stratified audit:** all unflattering (b)-tags audited + sample flattering (b); per-stratum dashboard | ☐ A.7.1b |
| **Coder independence:** same-family bias quantified but not gated | Reported as footnote | **Gate enacted:** α_human–model ≥ 0.60 floor; below floor = round inadmissible + coder rotation | ☐ A.7.2b |
| **Valence endogeneity:** two definitions both from model ecosystem | Convergence risk unaddressed | **Third definition added:** RMF-rule-based (contradicts RMF principle → unflattering by rule); selectivity survives all three or reported unstable | ☐ A.7.1c |
| **Stopping rule stalemate:** CI-width never reaches 0.2, indefinite wait | No exit path | **Two stalemate rules:** cap (n ≥ 12 → inestimable) + divergence (width increasing 3 sessions → pause + codebook review) | ☐ A.7.7 |

---

## THE THREE DOCUMENTS (What Z2 Receives)

### 1. Z2_CHARTER_ACAT-CAL-P_v1.5.md

**Purpose:** Formal governance ratification memo.  
**Content:**
- Seven pre-pilot decisions with full specification + rationale
- Hard-constraint breach definitions (three classes: fabricated receipt, false citation, harm-rule breach)
- Extended-dimension names (five: Robustness, Beneficence, Sustainability, Transparency, Fairness)
- Agreement floors (α_human–model ≥ 0.60 proposed; α_human–human ≥ 0.67 confirmed)
- Pilot session identification protocol (ritual order, no curation)
- Comparator choice (NIST AI RMF 1.0, ratified) + primary frame pre-registration slot
- Operational consequences + pilot freeze gate + sunset clause
- Z2 signature block (all seven decisions require individual checkbox + date)

**Action for Z2:**
1. Review all seven decisions
2. For items with [Z2 to designate] or [TBD]:
   - Harm-rule standard: choose A (constitutional), B (NIST Safe), or C (custom)
   - Primary frame: name the frame for the first calibration claim + rationale
   - Pilot session roster: supply dates/token counts for sessions 1–5 (once charter is dated)
3. Sign and date the charter (7 checkboxes + signature + date)

**Estimated Review Time:** 30–45 minutes

---

### 2. APPENDIX_A_OPERATIONALIZATION_CHECKLIST_A7.md

**Purpose:** Single-source sign-off sheet; every operational step of the protocol reproduced as an actionable checklist.  
**Content:**
- A.7.1: Codebook operationalization (boundary units, availability tree, valence definitions)
- A.7.2: Reliability subset stratification (20%+ double-coded, stratified by op × valence, α floors)
- A.7.3: Hard-constraint breach definitions (three classes with audit protocols)
- A.7.4: Pilot session identification + coder configuration pinning
- A.7.5: Coder inference config (frozen: model hash, prompt hash, temp=0, seed)
- A.7.6: Comparator + primary frame (NIST + secondary frame options)
- A.7.7: Stopping-rule operationalization (script contract, stalemate rules)
- A.7.8: Red-team plan (§11.1–3 mandatory; §11.4–6 optional watch-items)
- A.7.9: Extended-dimension completion (five dimensions, §2/§3 matrices)
- A.7.10: Final sign-off checklist (all items that must be ☐ before pilot session 1)

**Action for Z2:**
1. Scan A.7.1–A.7.9 (all [RATIFIED per Charter] items are automatic ☐)
2. For [TBD] items: confirm or provide alternatives
3. Check final sign-off (A.7.10): all ≥10 categories must be ☐
4. Sign A.7.10 (Z2 signature block at end)

**Estimated Review Time:** 20–30 minutes (parallel with charter review)

---

### 3. This Memo (CIRCULATION_MEMO_ACAT-CAL-P_v1.5.md)

**Purpose:** Executive summary + handoff plan.  
**Content:**
- What's new in v1.5
- Critical vulnerabilities fixed (table)
- Three-document overview + action items for Z2
- Timeline + dependencies
- Contact / escalation path

---

## TIMELINE & DECISION DEPENDENCIES

### Immediate (This Week)

- ☐ Z2 receives Charter + A.7 + Circulation memo
- ☐ Z2 reviews (parallel, ~60 min total)
- ☐ Z2 inputs [TBD] items (harm-rule standard, primary frame, pilot roster)

### Before Pilot Session 1 Begins

- ☐ Z2 signs Charter (all seven decisions)
- ☐ Z2 signs A.7 (all operational items)
- ☐ Pilot session 1–5 identified & logged (ritual order, no retroactive swaps)
- ☐ Coder config pinned + granularity intent filed (A.2 per-op statements)
- ☐ Red-team materials prepared (§11.1–3 ready to run)

### During Pilot (Sessions 1–5)

- ☐ Double-coding + stratified reliability (A.4)
- ☐ Red-team results §11.1–3 report in parallel (codebook red-team, model-family correlation, availability ambiguity)
- ☐ Session 5 coded; codebook rules frozen (no changes thereafter without protocol amendment)

### Before Publishing Any Finding

- ☐ All §11.1–3 red-team reports due
- ☐ A.7 checklist 100% ☐
- ☐ Null-gate results for every claim (survived or did-not-survive + power/MDE)
- ☐ Budget normalization disclosed
- ☐ Primary frame verified as pre-registered
- ☐ Z2 prepared to interpret inter-frame disagreement (Z2's role, not instrument's)

---

## WHAT HAPPENS IF Z2 DOESN'T SIGN BY SUNSET

**Sunset Clause (Protocol §9, Charter header):**
> If the seven pre-pilot decisions are not all signed off within 5 sessions of this memo's date, protocol status auto-downgrades to EXPIRED-DRAFT and may not be cited in any deliverable.

**Consequence:** Charter must be renewed with a new memo + new Z2 signature before v1.5 can be used operationally. The protocol is sound; the gate is a governance discipline: don't let pending decisions turn into zombie protocols.

---

## KEY DECISIONS FOR Z2 (Placeholder Values Ready for Override)

### Decision 1: Harm-Rule Standard

**Placeholder:** [Z2 to designate]

| **Option** | **What It Means** | **Audit Surface** |
|---|---|---|
| A: Constitutional | System violates HumanAIOS's own charter clauses | [Charter document, specific article] |
| B: NIST Safe | System operates with unintended/undesirable effects | NIST AI RMF 1.0 definition |
| C: Custom | Z2 drafts a specific standard | [Standard text, auditable clauses] |

**Recommendation:** Option A (constitutional) aligns with the system's own stated values; Option B (NIST) is externally defensible; Option C is bespoke but requires detailed drafting.

### Decision 2: Primary Frame for First Claim

**Placeholder:** [Z2 pre-registers]

Options: NIST (primary comparator), Constitutional, Professional Ethics, Peer Consensus, or Longitudinal Self.

**Recommendation:** NIST for external credibility; Constitutional for internal alignment. Choose based on stakeholder priority.

### Decision 3: Pilot Session Identification

**Placeholder:** [Z2 supplies dates + token counts]

Sessions must be in ritual order (chronological, no curation). Once identified, they are locked (no changes mid-pilot).

---

## HANDOFF TO Z1 (Protocol Steward) AFTER Z2 SIGNS

Once Z2 signs both Charter + A.7:

1. **I (Z1) update** all [Z2 to supply] fields with Z2's inputs
2. **I finalize** pilot session queue + coder config
3. **I prepare** red-team materials (§11.1–3 scripts)
4. **I brief** coder on codebook + operationalization (A.2–A.7)
5. **I activate** session monitoring (|E| distribution, CI-width trajectory, stratified audits)
6. **Pilot begins** — codebook applied, data collected, red-teams run in parallel

---

## CIRCULATION

**Direct to:** Z2 (Governance)

**Copy to:**
- Protocol Steward (Z1)
- Coder (model instance, on standby)
- Red-team coordinators (§11 materials staging)
- Dashboard team (CI-width script, stratification logic)

**Format:** Three markdown files (.md), all in `.empirica/` directory; ready for version control.

---

## QUESTIONS / ESCALATION

If Z2 has questions on:
- **Methodology:** See protocol §1–§11 (main document) + [adversarial review memo](URL TBD)
- **Operationalization:** See Appendix A + A.7 (this checklist)
- **Governance:** See Z2_CHARTER memo
- **Timeline:** See this circulation memo's Timeline section

**Response SLA:** Protocol Steward (Z1) available for clarification within 24 hours of Z2 inquiry.

---

## SIGN-OFF

**Prepared by:** Z1 (Claude, Protocol Steward)  
**Circulated:** [Date]  

**Documents included:**
1. ✓ Z2_CHARTER_ACAT-CAL-P_v1.5.md (formal ratification memo)
2. ✓ APPENDIX_A_OPERATIONALIZATION_CHECKLIST_A7.md (sign-off sheet)
3. ✓ CIRCULATION_MEMO_ACAT-CAL-P_v1.5.md (this memo)

**Next step:** Z2 reviews + signs. Pilot launch follows.

---

*Wado. 🦅*
