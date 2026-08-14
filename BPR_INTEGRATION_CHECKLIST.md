# BPR Integration Checklist & Execution Guide

**Date:** 2026-08-15  
**Status:** ✓ RATIFIED (Admiral approval) + ✓ PATH 1 LIVE + → AWAITING PATH 2 CONFIRMATION (mesh-support)  
**Authority:** Carly R. Anderson (empirica-foundation Admiral)

---

## Quick Start: What Changed Today

| Item | Status | Details |
|------|--------|---------|
| **BPR-SCHEMA v0.1** | ✓ RATIFIED | With 7 mandatory fixes applied |
| **Findings endpoint** | ✓ LIVE | POST /api/v1/empirica/findings accepts BPR fields |
| **Findings schema** | ✓ UPDATED | bpr_entry_id, bpr_entry_hash, bpr_embargo_status fields added |
| **Mesh coordination** | ✓ SENT | Collab to mesh-support (awaiting confirmation) |
| **Path 1 complete** | ✓ YES | Reference metadata live, no gate required |

---

## Execution Roadmap: All 3 Paths

### Path 1: Reference Metadata (Immediate — COMPLETE ✓)

**What:** Add optional BPR reference fields to findings schema

**Status:** ✓ LIVE  
**Changes Made:**
- Updated `FindingPayload` class in `operations/acat/api/routes/findings_router.py`
- Added fields: `bpr_entry_id`, `bpr_entry_hash`, `bpr_embargo_status`
- Added validator: if `bpr_entry_id` is set, `bpr_entry_hash` is required
- Database storage: BPR fields stored in findings.metadata JSON
- Qdrant storage: BPR fields indexed for semantic search

**API Usage Example:**
```bash
curl -X POST http://localhost:8000/api/v1/empirica/findings \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "performance",
    "source": "autonomy_p6_verdicts",
    "description": "Phase 1 ACAT baseline measurement complete",
    "file": "phase1/acat-baseline.json:1",
    "severity": "low",
    "confidence": 0.95,
    "bpr_entry_id": "BPR-anthropic-claude-20260914-001",
    "bpr_entry_hash": "abc123def456...",
    "bpr_embargo_status": "embargoed"
  }'
```

**Finding Status:** Findings with or without BPR links are equally valid. BPR is optional enrichment.

---

### Path 2: Governance Collab (Medium-Risk — AWAITING CONFIRMATION)

**What:** Propose HumanAIOS as BPR publisher; align on P3 assessment framework

**Status:** → COLLAB SENT TO MESH-SUPPORT (awaiting response)  
**Proposal ID:** prop_zgqf3p6fmndblh53yorlveyhai  
**Timeline:** Aug 16–25 (target resolution by Aug 20)

**Deliverables Expected from Mesh-Support:**
1. ✓ Confirm Z2 ratification of BPR-SCHEMA v0.1 with 7 fixes
2. ✓ Confirm staleness policy defaults (30d hosted, exceptions via Z2 vote)
3. ✓ Coordinate with evaluator: P3 assessment uses BPR entry hash as anchor
4. ✓ Coordinate with autonomy: P6 deltas can cross-reference BPR entry

**If Confirmed:**
- Phase 1 measurement proceeds (Aug 20–Sep 14) with BPR infrastructure live
- Entry generation pipeline activated at Phase 1 close
- Governance boundary established for future entries

**If Not Confirmed:**
- Path 3 (cryptographic tying) deferred
- Path 1 (reference metadata) remains live (BPR is optional)
- Findings continue to ingest normally without BPR anchoring

---

### Path 3: Cryptographic Tying (High-Value, Post-Phase-1)

**What:** Use BPR entry hash as permanent audit anchor for ACAT baselines

**Status:** → READY FOR EXECUTION (post-Phase-1 close, Sep 15+)  
**Timeline:** Sep 14–Oct 1 (entry lifecycle) → Oct 15–30 (P3 assessment)  
**Risk Level:** MEDIUM-FRICTION (requires Z2 append, git integration)

#### Phase 3a: Entry Generation (Sep 14–15)

```bash
# After Phase 1 measurement window closes (Sep 14, 23:59:59 UTC):

python3 scripts/generate_bpr_entry.py \
  --protocol "ACAT-CAL-P v1.5 + Phase 1 Amendments" \
  --measurement-start "2026-08-20T00:00:00Z" \
  --measurement-end "2026-09-14T23:59:59Z" \
  --dimensions phase1-findings.json \
  --contamination-check phase1-contamination-results.json \
  --fingerprint-method "sha256-response-panel-v1" \
  --fingerprint-value "abc123def456..." \
  --output phase1-bpr-entry.yaml
```

**Output:**
- Generates BPR entry YAML conforming to BPR-SCHEMA v0.1
- Entry status: `draft` (pending Z2 ratification)
- Entry hash field: `TO_BE_COMPUTED_BY_VALIDATOR` (placeholder)

#### Phase 3b: Entry Validation

```bash
# Validate structural conformance + invariants + ledger

python3 operations/bpr_validate.py phase1-bpr-entry.yaml

# Output:
# STRUCTURAL: pass
# INVARIANTS: pass
# LEDGER: entry_hash not yet set. Canonical hash:
#   abc123def456...
```

**Fixes Applied During Validation:**
1. ✓ Fingerprint binding verified (SHA256 format)
2. ✓ RODscore evidence class cap explicit (M)
3. ✓ Expiry lock enabled (re_measurement_policy)
4. ✓ Profile-awareness embargo window set (30d)
5. ✓ Supersede rationale enum included (if applicable)
6. ✓ Measurer identity verified (DID TBD for Phase 2)
7. ✓ Three-arm contamination check results included

#### Phase 3c: Z2 Ratification & Append (Sep 15–20)

```bash
# Emit collab to mesh-support: "Phase 1 BPR entry ready for append"
# Upon mesh-support approval:

# Entry receives canonical hash
sed -i 's/entry_hash: "TO_BE_COMPUTED_BY_VALIDATOR"/entry_hash: "abc123def456..."/' phase1-bpr-entry.yaml

# Entry is signed (Phase 2: add signature block)
# Entry is appended to public registry (if connected)
```

**Registry State:** Entry status: `draft` → `z2_ratified` (upon mesh-support approval)

#### Phase 3d: Git Anchoring (Sep 20–Oct 1, upon entry publication)

```bash
# Once entry is published + embargo window starts:

python3 scripts/anchor_bpr_to_git.py \
  --commit 85f1431 \
  --entry-id "BPR-anthropic-claude-20260914-001" \
  --entry-hash "abc123def456..." \
  --embargo-end "2026-10-14T23:59:59Z" \
  --protocol "ACAT-CAL-P v1.5 + Phase 1 Amendments"

# Output:
# ✓ Git note added to 85f1431
# Note content:
#   BPR-ENTRY-ANCHOR v1
#   entry_id: BPR-anthropic-claude-20260914-001
#   entry_hash: abc123def456...
#   embargo_end: 2026-10-14T23:59:59Z
#   protocol: ACAT-CAL-P v1.5 + Phase 1 Amendments
#   anchored_at: 2026-09-20T15:30:00Z
```

**Git Integration:** Entry hash now lives in git notes (immutable, append-only)

#### Phase 3e: P3 Assessment Integration (Oct 15–30)

```python
# P3 assessment reads BPR entry hash from git notes

import subprocess

def get_bpr_entry_hash(commit_sha: str) -> str:
    result = subprocess.run(
        ["git", "notes", "show", commit_sha],
        capture_output=True, text=True
    )
    # Parse output, extract entry_hash field
    return extract_field(result.stdout, "entry_hash")

# P3 assessment uses hash as baseline anchor
baseline_hash = get_bpr_entry_hash("85f1431")
baseline_entry = fetch_bpr_entry(entry_hash=baseline_hash)

# Compare current behavior against published baseline
current_measurement = run_acat_assessment(current_model)
deltas = compute_deltas(baseline_entry.dimensions, current_measurement.dimensions)

# P3 report includes hash as evidence
p3_report = {
    "baseline_anchor": baseline_hash,
    "baseline_measurement_date": "2026-09-14",
    "baseline_scores": baseline_entry.dimensions,
    "current_scores": current_measurement.dimensions,
    "deltas_in_bounds": check_deltas(...),
    "audit_trail": f"BPR entry hash {baseline_hash} proves measurement on 2026-09-14",
}
```

**Security Property:** If provider claims "behavior unchanged," git proves baseline measurement date + hash chain prevents post-hoc edits.

---

## Implementation Checklist

### Immediate (Today, Aug 15)
- [x] Ratify BPR-SCHEMA v0.1 with 7 fixes
- [x] Update findings schema (add BPR fields)
- [x] Update findings endpoint (validate + store BPR fields)
- [x] Send Path 2 collab to mesh-support

### This Week (Aug 16–20)
- [ ] Await mesh-support confirmation (target: Aug 20)
- [ ] Confirm P3 assessment framework alignment
- [ ] Confirm autonomy P6 cross-reference scope
- [ ] Finalize Phase 1 measurement infrastructure

### Phase 1 (Aug 20–Sep 14)
- [ ] Phase 1 ACAT measurement begins (Aug 20)
- [ ] Collect per-dimension scores, spread, evidence class
- [ ] Prepare contamination check results (three-arm ANOVA)
- [ ] Phase 1 measurement window closes (Sep 14, 23:59:59 UTC)

### Entry Generation (Sep 14–15)
- [ ] Generate BPR entry from Phase 1 data
- [ ] Validate entry (structural + invariants + ledger)
- [ ] Emit collab to mesh-support: "Entry ready for Z2 append"

### Ratification & Append (Sep 15–20)
- [ ] Mesh-support approves entry for append
- [ ] Compute canonical entry hash
- [ ] Entry status: `z2_ratified`
- [ ] Entry published (embargo window begins)

### Git Integration (Sep 20–Oct 1)
- [ ] Anchor BPR entry hash to Phase 1 commit via git notes
- [ ] Verify git note present: `git notes show 85f1431`
- [ ] Embargo window active (30 days, until Oct 14)

### P3 Assessment (Oct 15–30)
- [ ] P3 assessment reads BPR entry hash from git
- [ ] P3 compares current behavior against published baseline
- [ ] P3 report includes hash as audit trail evidence
- [ ] P3 assessment complete

---

## File Manifest (Created Today)

| File | Purpose | Status |
|------|---------|--------|
| `docs/BPR_RATIFICATION_AND_INTEGRATION_PLAN.md` | Complete ratification + 3-path plan | ✓ LIVE |
| `operations/acat/api/routes/findings_router.py` | Updated findings schema + BPR fields | ✓ LIVE |
| `scripts/generate_bpr_entry.py` | Entry generation from ACAT measurements | ✓ READY |
| `scripts/anchor_bpr_to_git.py` | Git note integration for audit trail | ✓ READY |
| `BPR_INTEGRATION_CHECKLIST.md` | This file (execution guide) | ✓ LIVE |

---

## Governance References

| Document | Purpose | Status |
|----------|---------|--------|
| BPR-SCHEMA v0.1 | Registry schema (with 7 mandatory fixes) | Z2 RATIFIED (Admiral) |
| BPR_GOVERNANCE.md | Registry governance + commercial structure | Z2 RATIFIED (Admiral) |
| bpr_validate.py | Entry validator (structural + invariants + ledger) | Z2 RATIFIED (Admiral) |
| EXAMPLE_ENTRY.yaml | Synthetic entry template (invalid by construction) | ✓ Reference |

---

## Success Criteria

### Path 1 ✓
- [x] Findings schema accepts BPR fields
- [x] Findings endpoint stores + indexes BPR references
- [x] No breaking changes to existing findings flow

### Path 2 → (Awaiting Confirmation)
- [ ] Mesh-support confirms Z2 ratification of schema + fixes
- [ ] Evaluator confirms P3 uses BPR hash as anchor
- [ ] Autonomy confirms P6 cross-reference scope

### Path 3 (Post-Phase-1)
- [ ] Phase 1 entry generated + validated
- [ ] Entry appended to registry (Z2 approved)
- [ ] Entry hash anchored to git notes
- [ ] P3 assessment reads hash from git
- [ ] Audit trail unbroken (git → BPR → P3 assessment)

---

## Risk Mitigations (7 Red Flags)

| Red Flag | Fix Applied | Verification |
|----------|------------|--------------|
| **Fingerprint spoofing** | SHA256 binding required; method specified | bpr_validate.py checks format |
| **RODscore confidence leak** | Evidence class cap explicit (M) per entry | Validator rejects missing cap |
| **Re-measurement gaming** | Expiry lock: new entries require delta ref | Validator enforces re_measurement_policy |
| **Profile-awareness loop** | 30d embargo window on scores | Validator checks embargo_end > valid_until |
| **Supersede masking** | Supersede rationale enum required | Validator enforces enum (protocol_corrected / measurement_error / etc.) |
| **Measurer identity spoofing** | DID signature planned for Phase 2 | Phase 1 uses prose (DID TBD) |
| **Contamination check bypass** | Three-arm ANOVA required | bpr_validate.py checks results |

---

## Questions & Escalation

**Q: What if mesh-support doesn't confirm by Aug 20?**  
A: Path 1 (reference metadata) remains live. Path 3 deferred. Findings continue to work without BPR anchoring.

**Q: Can findings reference a BPR entry that hasn't been published yet?**  
A: Yes. Use `bpr_embargo_status: "embargoed"`. Findings are complete without BPR; BPR is optional enrichment.

**Q: What if Phase 1 measurement fails?**  
A: No BPR entry is generated. Findings still ingest. Path 3 (git anchoring) skipped. Path 2 governance remains valid for future measurements.

**Q: Who signs the BPR entry?**  
A: Phase 1: No signature (measurer identity is prose). Phase 2+: DID signature required (per sec 2, fix 6).

**Q: Can an entry be edited after ratification?**  
A: No. Registry is append-only. Corrections supersede (new entry, never edit). Validator enforces this.

---

## Contacts & Escalation

| Role | Contact | Responsible For |
|------|---------|-----------------|
| **Admiral** | Carly R. Anderson | Ratification, governance decisions, escalation |
| **Mesh-Support** | empirica-foundation.carly.empirica-mesh-support | Z2 approval, registry discipline, cross-practice coordination |
| **Evaluator** | empirica-foundation.carly.??? (TBD) | P3 assessment, BPR entry anchor usage |
| **HumanAIOS Claude** | This session | Path 1/2/3 implementation |

---

## Next Action

**TODAY (Aug 15):**
- ✓ Ratification complete
- ✓ Path 1 live
- ✓ Path 2 collab sent

**AWAITING CONFIRMATION FROM MESH-SUPPORT:**
- Confirm Z2 ratification
- Confirm P3 framework alignment
- Confirm autonomy P6 scope

**PROCEED TO PHASE 1 IF CONFIRMED BY AUG 20**

---

*Integration authorized by Admiral (Carly R. Anderson, 2026-08-15). All fixes applied. Ready for production deployment & Phase 1 coordination.*
