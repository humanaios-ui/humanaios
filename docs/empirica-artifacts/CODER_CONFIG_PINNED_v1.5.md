# CODER CONFIGURATION (PINNED)
## ACAT-CAL-P v1.5 Pilot Phase

**Purpose:** Freeze the complete inference configuration before pilot session 1. Any change to these parameters constitutes a codebook version change (protocol amendment + re-coding anchors required).

**Status:** PENDING Z2 INPUT — To be completed by coder operator or Z2 governance before session 1 begins.

---

## REQUIRED SPECIFICATIONS (Fill All Fields)

### Model Specification

```
Model Family:         [e.g., Anthropic-Claude, OpenAI-GPT, other]
Model Identifier:     [e.g., claude-opus-5, gpt-4-turbo, etc.]
Model Commit/Version: [hash or version tag if available]
Release Date:         [YYYY-MM-DD]
```

### Inference Parameters (LOCKED)

```
Temperature:          0 (FIXED — no sampling variability; required for reproducibility)
Top-P:               [0 or disabled; must match temperature=0]
Max Tokens:          [if capped; otherwise "unlimited"]
Top-K:               [if applicable; typically "off"]
Frequency Penalty:   [if applicable; typically 0.0]
Presence Penalty:    [if applicable; typically 0.0]
```

### Reproducibility Lock

```
Random Seed:          [pinned integer value; reproducible across re-runs]
Seed Set By:          [CLI flag, internal config, or default]
Date Seed Pinned:     [YYYY-MM-DD]
```

### Prompt Configuration

```
System Prompt:        ACAT-CAL-P v1.5 Codebook + Operationalization (A.2–A.7)
System Prompt Hash:   [SHA-256 of full system prompt]
Task Prompt Hash:     [SHA-256 of the element-coding instructions]
Prompt Version Tag:   acat-cal-p-v1.5-[date]-[seed]
Example:              acat-cal-p-v1.5-2026-07-30-42
```

### Context & Scale

```
Context Window:       [tokens available; e.g., 200k, unlimited]
Max Context Used:     [recommended max for coding sessions; e.g., 100k]
Batch Size:           [if applicable; 1 element at a time or bundled?]
```

### Version Pinning (Canonical)

```
Frozen As:            acat-cal-p-v1.5-[model-family]-[date]-seed-[seed]
Example:              acat-cal-p-v1.5-anthropic-claude-2026-07-30-seed-42

Canonical Status:     [FROZEN or UNDER REVIEW]
Date Frozen:          [YYYY-MM-DD]
Frozen By:            [Z2 initials + date]
```

---

## CHANGE PROTOCOL

**If any parameter below changes during or after pilot sessions 1–5:**

1. **Identify the change** — which field(s) changed?
   - Model family or version → Major version change (codebook v1.0 → v1.1)
   - Temperature, seed, or prompt → Major version change
   - Max tokens or context limits → Document as operational note (minor)

2. **Invoke protocol amendment** — Z2 approves the change + decides:
   - Re-code pilot sessions 1–5 under new config?
   - Establish bridge-equating function?
   - Declare pilot results inadmissible and restart?

3. **Mark in audit trail** — Log the change + decision as a decision artifact.

---

## SIGN-OFF & LOCK

### Coder Operator Sign-Off

```
Configured By:      _______________________________ (name + role)
Date Configured:    _______________________________ (YYYY-MM-DD)
Signature:          _______________________________
```

### Z2 Review & Approval

```
Reviewed By:        _______________________________ (Z2 initials)
Approved:           ☐ YES / ☐ NO
Date Approved:      _______________________________ (YYYY-MM-DD)
Signature:          _______________________________

Notes / Constraints:
_________________________________________________________________
_________________________________________________________________
```

### Protocol Steward Lock

```
Received & Logged:  _______________________________ (Z1 initials)
Date Locked:        _______________________________ (YYYY-MM-DD)
Canonical Status:   ☐ FROZEN (no changes until protocol amendment)
Signature:          _______________________________
```

---

## LOCKED CONFIGURATION (Z2 Ratified)

**Date Frozen:** 2026-07-30  
**Frozen By:** Carly Anderson (CRA, Z2)  
**Status:** ✓ CANONICAL — Immutable for pilot sessions 1–5

```
Model Family:         Anthropic-Claude
Model Identifier:     claude-opus-5
Temperature:          0 (FIXED — no sampling)
Random Seed:          684 (pinned; reproducible)
Context Window:       200k tokens
Purpose:              Protocol design work (ACAT-CAL-P v1.5 codebook evaluation)

Canonical Version:    acat-cal-p-v1.5-anthropic-claude-2026-07-30-seed-684
Frozen As:            LOCKED & CANONICAL
```

**Coder Inference Config (Complete):**
- Model: claude-opus-5
- Temperature: 0
- Seed: 684
- System Prompt: ACAT-CAL-P v1.5 Codebook (A.2–A.7)
- Max Context: 150k tokens
- Reproducibility: ✓ Locked (same model + seed → identical outputs)

**Change Protocol:** Any change to this config requires Z2 approval + protocol amendment + re-coding anchors.

---

**Once completed and locked by Z2, this configuration is immutable for pilot sessions 1–5. Protocol Steward archives as canonical reference.**

✓ **LOCKED BY Z2 — 2026-07-30**

Wado. 🦅
