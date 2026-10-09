# REVIEW: Items D & E — Blocking Pilot Freeze

**Context:** D and E are the two categories holding up pilot launch. D has a hard 5-session sunset clock. E is a procedural blocker (red-team must complete before codebook freeze).

---

## ITEM D: Pending Z2 Supply (4 Items, 5-Session Sunset)

### The Clock

**Sunset Rule (§9, Charter):**
- If all 4 items are not supplied within 5 sessions of 2026-07-30, protocol auto-downgrades to EXPIRED-DRAFT
- Protocol becomes **non-citable** in deliverables
- Must be renewed with new charter memo if extended

**Current Status:** 2/4 items supplied (D-1 ✓, D-2 ✓); Clock started 2026-07-30

**Sessions before expiry:** 5 sessions from now (Current: S1 baseline; Sessions 2–5; then EXPIRY at S6)

---

### The 4 Items (Prioritized by Criticality)

#### **1. ✓ RESOLVED: Extended-Dimension Names (6 existing dimensions)**

**What it is:** The canonical names for the 6 extended ACAT dimensions that complement the 6 core ones.

**Why critical:** §2 (ACAT↔NIST crosswalk) and §3 (Operation×Dimension loading) **cannot be completed** without these names. The protocol's measurement framework is incomplete until these are named.

**Z2 Decision (2026-07-30):**
```
✓ CONFIRMED: Use the six existing dimensions already in humanaios ACAT:
  1. scheme
  2. power
  3. syc
  4. consist
  5. fair
  6. handoff
```

**Impact:** §2 and §3 now unblocked; 12-dimensional assessment framework (core 6 + extended 6) locked for protocol operationalization.

**Status:** CLOSED ✓

---

#### **2. ✓ RESOLVED: Harm-Rule Standard Designation (A.5 breach definition)**

**What it is:** Which standard governs Class C (harm-rule) breaches?

**Z2 Decision (2026-07-30):**
```
✓ DESIGNATED: A+B (Dual Validation)
  A = HumanAIOS validated ratified findings (empirical grounding)
  B = NIST Safe scope appropriate for general implementation (external standardization)

Rationale: Triangulation via two independent standards mitigates bias
  - Empirical grounding (A) prevents decontextualization
  - External standardization (B) prevents organization-specific drift
  - Both must validate Class C breach; divergence flags edge cases
```

**Impact:** A.5 breach definitions now unblocked; red-team §11.1–3 can audit Class C breaches against both standards.

**Status:** CLOSED ✓

---

#### **3. MEDIUM: Session ID**

**What it is:** The formal session identifier for this governance-close session (placeholder: S-073026-NN).

**Why needed:** WGS (Session-wide governance) close-log needs a canonical session ID for the audit trail.

**Current status:** Placeholder assigned; awaiting Z2's formal descriptor.

**Decision needed from Z2:**
```
What is the canonical session ID for this session?
Example format: S-073030-GOVERNANCE or similar
```

**Blocker consequence:** Low — can be assigned retroactively at any point. Mainly affects WGS record cleanliness.

---

#### **4. MEDIUM: Charter Day**

**What it is:** The formal date when the protocol charter (Z2_CHARTER_ACAT-CAL-P_v1.5.md) was issued.

**Current status:** Issued 2026-07-30; awaiting Z2 formal confirmation.

**Decision needed from Z2:**
```
Charter day (confirm 2026-07-30 or assign alternate)?
```

**Blocker consequence:** Low — protocol ratification is already complete; charter day is a ceremonial/audit anchor.

---

### D Summary: Decision Status

| Item | Criticality | Z2 Action | Status | Impact |
|---|---|---|---|---|
| Extended-dimension names | **CRITICAL** | Confirm the 6 existing dimensions | ✓ RESOLVED | §2/§3 unblocked; 12-dim framework locked |
| Harm-rule standard | **HIGH** | Designate A+B dual validation | ✓ RESOLVED | A.5 unblocked; red-team §11 can proceed |
| Session ID | MEDIUM | Assign descriptor | ⧗ PENDING | WGS record cleanliness (hygiene) |
| Charter day | MEDIUM | Confirm 2026-07-30 | ⧗ PENDING | Audit trail completeness (hygiene) |

**Shortest path:** Items 1–2 now closed; items 3–4 hygiene (can follow anytime before Session 5 expires).

---

## ITEM E: Pending Z2 Sign-Off (Red-Team Blocking Pilot Freeze)

### What Must Happen

**Pilot freeze is blocked until:**
1. ✓ §11.1–3 red-team results reported (three stress tests)
2. ✓ Appendix A checklist fully signed off (A.7.10)
3. ✓ All procedural gates satisfied

**Current status:** 
- Red-team materials staged and ready
- Red-team execution happens in parallel with Sessions 1–2
- Results expected by end of Session 5

---

### The Three Red-Team Tests (§11.1–3)

#### **§11.1: Codebook Red-Team**

**What it tests:** Are the frozen boundary units (A.2) robust? Do alternative segmentations produce wildly different results?

**Execution:** 
- Run in parallel with Sessions 1–2
- Independent coders apply alternative rule sets to same sample
- Success criterion: |E| spread < 2× (consistency across interpretations)

**Owner:** Red-team lead (not Z2)  
**Blocker:** If FAIL (spread ≥ 2×), codebook review + amendment before freeze

---

#### **§11.2: Model-Family Correlation Study**

**What it tests:** Do different model families produce independent judgments, or do they converge on shared bias?

**Execution:**
- Same sample coded by same-family + cross-family models + human coders
- Success criterion: Cross-family ρ > intra-family difference

**Owner:** Red-team lead  
**Blocker:** If FAIL, selectivity findings flagged as "ecosystem-internal" (not generalizable)

---

#### **§11.3: Availability Ambiguity Battery**

**What it tests:** Is the (a)/(b) operational test (A.3) clear enough? Do coders agree on edge cases?

**Execution:**
- Deliberately ambiguous cases run through A.3 decision tree
- Success criterion: κ ≥ 0.80 (acceptable agreement)

**Owner:** Red-team lead  
**Blocker:** If FAIL (κ < 0.80), clarify A.3 tree with examples before Sessions 3–5

---

### E Summary: What Blocks Freeze

| Blocker | Status | Owner | Timeline |
|---|---|---|---|
| §11.1–3 red-team PASS | ⧗ In progress | Red-team lead | Due by end of Session 5 |
| Appendix A checklist | ☐ Awaiting red-team results | Z2 sign-off | After red-team reports |
| Pilot representativeness audit | ⧗ Staged for Sessions 1–5 | Protocol Steward | Reports after Session 5 |

**Codebook cannot freeze until:**
1. Red-team §11.1–3 all PASS
2. A.7.10 checklist signed by Z2
3. Pilot sessions 1–5 complete

---

## DECISION MATRIX FOR Z2

### Resolved (2026-07-30):

✓ **D-1: Extended-dimension names** → Use the 6 existing dimensions (scheme, power, syc, consist, fair, handoff)

✓ **D-2: Harm-rule standard** → A+B dual validation (HumanAIOS findings + NIST Safe)

### Before Session 5:

**D-3: Session ID** — Assign descriptor (e.g., S-073030-GOVERNANCE) [optional, hygiene]

**D-4: Charter day** — Confirm 2026-07-30 [optional, hygiene]

### Automated (No Z2 Action Required):

**E-1–3: Red-team tests** — Running in background (Sessions 1–2)  
**E-4: Appendix A checklist** — Z2 signs after red-team reports

---

## RISK SUMMARY

| Risk | Probability | Consequence | Mitigation |
|---|---|---|---|
| **D-1/D-2 not supplied by Session 5** | LOW (5-session window is ample) | Protocol EXPIRED-DRAFT; non-citable | Supply by Session 2 (buffer 3 sessions) |
| **Red-team §11 FAIL** | LOW (materials well-designed) | Codebook amendment + recode | Capture in red-team protocol; escalate to Z2 |
| **Appendix A unreviewed after red-team** | NONE (Z2 can sign immediately after results) | No practical impact | Red-team expected by end Session 5 |

---

## BLOCKER RESOLUTION (Session 1)

### **Completed (2026-07-30):**

✓ **D-1 & D-2 locked.** Both critical blockers resolved; §2/§3/A.5 unblocked; red-team §11 can proceed.

### **Optional (Before Session 5):**

3. **Assign session ID** (formal descriptor) — WGS record hygiene
4. **Confirm charter day** (2026-07-30 or alternate) — Audit trail hygiene

### **Automated (Ongoing):**

- Red-team runs Sessions 1–2 (no Z2 action)
- Appendix A checklist: Z2 signs after §11.1–3 report
- Pilot freeze: Automatic upon red-team PASS + checklist signature

---

## WHAT TO WATCH (Sessions 1–5)

**Yellow flags:**
- Red-team §11.1 reports spread ≥ 2× (codebook ambiguity)
- Red-team §11.2 reports cross-family ρ ≤ intra-family (ecosystem bias)
- Red-team §11.3 reports κ < 0.80 (availability test unclear)

**If any yellow:** Escalate to Z2 immediately; codebook review + amendment cycle triggered

**Green flag:** All §11.1–3 PASS → codebook freeze automatic

---

*Items D and E are linked: D-1/D-2 decisions unblock red-team execution (E). D-3/D-4 are hygiene. E is automated execution with red-team PASS/FAIL gates.*

**Next step:** Z2 decision on D-1 and D-2. Everything else flows from that.
