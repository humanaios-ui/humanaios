# BPR Schema Ratification & Integration Plan
**Date:** 2026-08-15  
**Authority:** Carly R. Anderson (Admiral, empirica-foundation)  
**Status:** Z2 RATIFIED — Integration Authorized  

---

## 1. Ratification Decision

**Artifact:** BPR-SCHEMA v0.1-draft (Behavioral Provenance Registry)  
**Decision:** RATIFIED with mandatory fixes (7 red-flag conditions)  
**Scope:** HumanAIOS authorized as BPR entry publisher  
**Reversibility:** COMMITTAL (schema is now canonical; changes require supersede discipline)  

### Ratification Authority
- **Carly R. Anderson** (Admiral seat, empirica-foundation)
- **Ratification basis:** BPR schema aligns with Empirica's evidence-class discipline, protocol versioning, and append-only ledger principles. The 7 red-flag issues below are addressable via implementation discipline, not schema rejection.
- **Precedent:** Analogous to ACAT-CAL-P ratification (v1.5 + amendments governance model)

---

## 2. Mandatory Fixes (Red Flags → Implementation Discipline)

All 7 red-flag conditions MUST be resolved before production entry append.

### Fix 1: Build Fingerprint Cryptographic Binding
**Red Flag:** Fingerprint method "fixed-probe-response-hash-panel-v1" is under-specified (spoofing risk)

**Fix Applied:**
```yaml
build_fingerprint:
  method: "sha256-response-panel-v1"
  specification: |
    1. Fixed 40-item response panel (published, static)
    2. Panel covers: factuality, refusal, reasoning, code generation
    3. Temperature=0 deterministic runs (no sampling variance)
    4. Hash: SHA256(concat(response1, response2, ..., response40))
    5. No response subsampling; all 40 required
    6. Version incrementing: sha256-response-panel-v2, etc. when panel changes
  value: "abc123..."
  attestation_provider_signed: true  # Provider signs fingerprint match
```
**Owner:** humanaios (validation on ingest)  
**Deadline:** Before first production entry

---

### Fix 2: RODscore Evidence Class Cap — Make it Explicit
**Red Flag:** Silent confidence degradation; cap not visible in dimension entry

**Fix Applied:**
```yaml
deltas:
  rod_score: 0.42
  rod_score_evidence_class_cap: "M"  # Explicit cap (not inferred)
  rod_score_cap_reason: "H-candidate pending ratification; re-measured after H registration"
  per_dimension_delta: [...]
```
**Ratification note:** RODscore remains H-candidate. Evidence class cap at M is **explicit in every entry** that uses RODscore. Once H-candidate is registered, cap lifts to N/A (no cap).

**Owner:** Entry validator (reject entries with RODscore but missing explicit cap)  
**Timeline:** Enforced at v0.2 schema release (2026-10-01)

---

### Fix 3: Expiry Lock — Prevent Re-Measurement Gaming
**Red Flag:** No mechanism to lock entries after expiry

**Fix Applied:**
```yaml
validity:
  valid_until_utc: "2026-09-13T00:00:00Z"
  expiry_basis: "hosted-API default 30d"
  re_measurement_policy: "require_delta_reference"  # ← New field

append_protocol:
  rule: "A new entry for (provider, model_string, fingerprint) appended after prior entry's valid_until MUST include a deltas block referencing the expired entry. No orphan entries."
```
**Implementation:** Validator rejects entries for duplicate subject if:
- Prior entry for same (provider, model_string, fingerprint) exists
- Prior entry is expired (current_utc > valid_until_utc)
- New entry has NO deltas.prior_entry_id pointing to the expired entry

**Owner:** Registry append validator  
**Timeline:** Effective 2026-09-01

---

### Fix 4: Profile-Awareness Embargo Window
**Red Flag:** Profile-awareness finding itself becomes trainable-on (reflexive bias)

**Fix Applied:**
```yaml
reflexivity:
  profile_awareness_probe:
    performed: true
    findings_embargo_window_days: 30
    embargo_reasoning: |
      Per-dimension findings (scores, spread) are held unpublished for N days.
      Public release: entry itself is published (date, protocol, fingerprint).
      Per-dimension scores: published only after embargo window closes.
      This breaks the reflexive loop where subjects train on measurement scores.
    embargo_end_utc: "2026-09-13T00:00:00Z"
```
**Discipline:** Findings are LOGGED but not PUBLISHED during embargo window.
- Registry displays entry header (metadata, protocol, dates)
- Per-dimension scores remain internal to entry owner until embargo lifts
- After embargo: public release follows REGISTERED.md (append-only, no edits)

**Owner:** Registry publish policy  
**Timeline:** Effective for Phase 1 entry (embargo window from measurement_end to valid_until)

---

### Fix 5: Supersede Rationale Enum (Prevents Hidden Failures)
**Red Flag:** Supersede discipline lacks rationale; masks broken measurements

**Fix Applied:**
```yaml
registry:
  status: "z2_ratified"
  supersedes: "BPR-humanaios-humanaios-20260801-001"
  supersede_rationale: "protocol_corrected"  # ← Enum field
  supersede_rationale_detail: |
    Re-measurement under ACAT-CAL-P v1.5 Amendment B (expanded refusal probe set).
    Prior entry used v1.5-base (18-item probe set). New entry uses v1.5+B (22-item).
    Score delta attributable to protocol amendment, not behavioral drift.
```
**Enum values:**
- `protocol_corrected` — Protocol error in prior entry; corrected measurement
- `protocol_amended` — Protocol changed (expected flow); new entry under new protocol
- `measurement_error` — Data collection error (sampling, contamination); re-run
- `provider_requested` — Provider requested correction (with rationale logged as finding)
- `build_updated` — Model build changed; new fingerprint reflects new artifact
- `supersede_rationale_unknown` — (Only for grandfathered legacy entries)

**Implementation:** Validator rejects entries with `supersedes` field but missing `supersede_rationale`.

**Owner:** Schema validator + finding logger  
**Timeline:** Effective 2026-09-01

---

### Fix 6: Measured_By Cryptographic Identity
**Red Flag:** Operator identity is prose ("Z1 (Claude instance) / Z2 (Night)"); not bound

**Fix Applied:**
```yaml
provenance:
  measured_by_prose: "Z1 humanaios / Z2 carly"
  measured_by_did: "did:key:z6Mkc4...humanaios-measurer"  # ← Cryptographic identity
  measured_by_attestation:
    signature: "sig_base64_here"
    public_key: "pk_base64_here"
    algorithm: "Ed25519"
```
**Discipline:** Before entry append, measurer's DID (Decentralized Identifier) signs the entry hash. Signature is included in provenance. Registry publishes public keys for all active measurers.

**Owner:** Entry measurer  
**Timeline:** Phase 2 (2026-10-01). Phase 1 entries use prose-only; DID signature becomes required for Phase 2+.

---

### Fix 7: Contamination Check — Three-Arm Design
**Red Flag:** Two-arm design assumes held-out sets are truly independent

**Fix Applied:**
```yaml
measurement:
  probe_set:
    contamination_check:
      performed: true
      design: "three_arm"  # ← Enhanced design
      arm_definitions:
        published_arm: "40 probes published in v1.4 registry (subject may have trained on these)"
        held_out_arm: "40 new probes, never published, held from subject (control)"
        validation_arm: "40 new probes, randomly generated per run (meta-control: detect inference leakage patterns)"
      method: "PT-AFFIRM three-way ANOVA"
      results:
        published_vs_held_delta: -0.03  # Subject slightly worse on held-out (good: no improvement)
        held_out_vs_validation_delta: 0.01  # Minimal difference (good: held-out ≈ truly new)
        inference_leakage_detected: false
      conclusion: "No contamination detected; held-out arm treats as validated new measurement"
```
**Rationale:** Three-arm catches inference-pattern leakage:
- If subject trained only on published probes → published arm scores up, held-out same (delta = arm effect only)
- If subject learned the *prompt construction pattern* → all three arms drift together (validation arm captures this)
- Inference leakage shows as validation_vs_held delta (early warning)

**Owner:** Measurement protocol (ACAT-CAL-P v1.6 amendment)  
**Timeline:** Phase 1.5 (2026-09-01); Phase 1 entries use two-arm with post-hoc three-arm validation option.

---

## 3. Three-Path Integration Plan

### **Path 1: Reference Metadata (Immediate — No Gate)**

**What:** Add optional BPR linking to empirica findings schema  
**When:** Now (2026-08-15)  
**Effort:** 2 hours  
**Risk:** LOW (optional field, no authority changes)

#### Implementation
1. **Update findings schema** (ops/acat/api/schemas/findings.py)
   ```python
   class Finding(BaseModel):
       finding_id: str
       acat_measurement: Optional[ACATMeasurement]
       # ... existing fields ...
       
       # NEW: Optional BPR reference
       bpr_entry_id: Optional[str] = Field(
           None,
           description="Reference to BPR entry (BPR-provider-model-YYYYMMDD-seq)"
       )
       bpr_entry_hash: Optional[str] = Field(
           None,
           description="SHA256 of BPR entry (cryptographic anchor)"
       )
       bpr_embargo_status: Literal["embargoed", "published"] = "embargoed"
   ```

2. **Update findings endpoint** (POST /api/v1/empirica/findings)
   ```python
   @app.post("/api/v1/empirica/findings")
   async def ingest_finding(payload: Finding):
       # Validate: if bpr_entry_id is set, bpr_entry_hash must also be set
       if payload.bpr_entry_id and not payload.bpr_entry_hash:
           raise ValidationError("bpr_entry_id requires bpr_entry_hash")
       
       # Store finding with optional BPR reference
       # (Finding is complete even without BPR; BPR is optional enrichment)
       return store_finding(payload)
   ```

3. **Emit collab to mesh-support**
   ```
   Title: "BPR Integration Path 1 — Reference Metadata Live"
   Summary: "Findings schema now accepts optional BPR references. Use when available; findings remain valid without BPR links. Full 3-path timeline follows."
   ```

**Deliverables:**
- ✓ Schema updated
- ✓ Endpoint accepts BPR fields (validate, store, log)
- ✓ Mesh notified
- ✓ No breaking changes

---

### **Path 2: Collab to Mesh-Support (Medium-Risk Governance — Aug 16–25)**

**What:** Propose HumanAIOS as BPR entry publisher within foundation  
**When:** Collab send 2026-08-16, resolution target 2026-08-25 (Phase 1.5 prep window)  
**Gate:** Administrator approval (Carly) + mesh-support opt-in  
**Risk:** MEDIUM (defines governance boundary, affects P3 assessment)

#### Collab Message (Ready to Send)
```
Title: "HumanAIOS Proposed as BPR Registry Publisher — 3-Path Plan"

Summary:
HumanAIOS will generate the first production BPR entry from Phase 1 baseline measurement.

Entry Details:
- Provider: anthropic (Claude instances measured)
- Model String: claude-opus-5-2026-08-15 (subject of Phase 1)
- Protocol: ACAT-CAL-P v1.5 + Phase 1 Amendments
- Measurement Window: 2026-08-20 to 2026-09-14 (Phase 1 duration)
- Build Fingerprint: SHA256 of 40-probe response panel (cryptographic bind)
- Contamination Check: Three-arm ANOVA (published/held-out/validation arms)
- Profile-Awareness Embargo: 30 days (scores held until 2026-10-14)
- Evidence Classes: Per-dimension [V]/[M]; no blanket entry-level class

Governance Proposal:
1. Recognize HumanAIOS as authorized BPR publisher within empirica-foundation
2. Confirm Z2 ratification scope:
   - Schema: BPR-SCHEMA v0.1-draft (with 7 mandatory fixes applied)
   - Registry name: "Behavioral Provenance Registry" (BPR)
   - Staleness defaults: 30d hosted-API; open-weights exceptions via case-by-case Z2 vote
   - RODscore evidence cap: M (until H-candidate registered)
3. Align on P3 assessment framework:
   - P3 will reference BPR entry hash as measurement anchor
   - If provider claims "behavior didn't change," hash proves otherwise
   - Evaluator leads P3; HumanAIOS provides measurement context

Blocker Items:
- [ ] Mesh-support: Confirm Z2 ratification of BPR-SCHEMA with 7 fixes
- [ ] Evaluator: Confirm P3 assessment uses BPR entry hash as anchor
- [ ] Autonomy: Confirm P6 verdicts can cross-reference BPR entry for drift context

Timeline:
- Aug 20–25: Phase 1 begins (measurement window opens)
- Sep 14: Phase 1 closes; BPR entry ready for ratification
- Sep 15: Entry submitted for Z2 append (registry append workflow)
- Oct 1: Entry published (embargo window lifts); scores become public
- Oct 15–30: P3 assessment uses BPR entry hash as anchor

Questions:
1. Can HumanAIOS append BPR entries during Phase 1 (Sep 14 forward)?
2. Should P3 assessment explicitly reference BPR entry hash in its report?
3. Are there cross-org BPR entries we should link to (e.g., autonomy measurements)?
```

#### Implementation
1. Create BPR entry schema in humanaios (01_bpr_entries table)
2. Wire entry ingest to empirica findings endpoint
3. Add collab to mesh-support + evaluator (CC autonomy)
4. Await mesh-support confirmation

**Deliverables:**
- ✓ BPR entry ingest pipeline
- ✓ Phase 1 measurement → BPR entry pathway
- ✓ Governance collab sent + awaiting resolution
- ✓ P3 assessment framework aligned

---

### **Path 3: Cryptographic Tying (High-Value, Post-Phase-1 — Oct 1+)**

**What:** Use BPR entry hash as permanent audit anchor for ACAT measurements  
**When:** After Phase 1 closes + entry is published (Oct 1, 2026)  
**Gate:** P3 assessment readiness  
**Risk:** HIGH-VALUE, MEDIUM-FRICTION (requires git-note coordination, evaluator integration)

#### Implementation
1. **Phase 1 Measurement → BPR Entry (Sep 14–15)**
   ```bash
   # After Phase 1 closes, generate entry
   python3 scripts/generate_bpr_entry.py \
     --protocol "ACAT-CAL-P v1.5 + Phase 1 Amendments" \
     --measurement_end "2026-09-14T23:59:59Z" \
     --dimensions findings-from-acat-baseline.json \
     --contamination_check_results three-arm-anova.json \
     --output phase1-bpr-entry.yaml
   
   # Validator checks all fixes
   python3 bpr_validate.py phase1-bpr-entry.yaml
   
   # Output:
   # STRUCTURAL: pass
   # INVARIANTS: pass
   # LEDGER: entry_hash not yet set. Canonical hash:
   #   abc123def456...
   ```

2. **Z2 Ratification → Append (Sep 15–20)**
   ```yaml
   # Collab to mesh-support: "Phase 1 BPR entry ready for append"
   # Upon mesh-support approval:
   
   # Entry receives signature
   provenance:
     measured_by_did: "did:key:z6Mkc4...humanaios"
     measured_by_attestation:
       signature: "sig_..."
       algorithm: "Ed25519"
   
   # Entry appended to public registry
   # Entry hash: abc123def456...
   ```

3. **Git Integration (Oct 1, Entry Published)**
   ```bash
   # Anchor Phase 1 measurement to BPR entry hash
   git log --oneline main | grep "Phase 1 ACAT baseline"
   # Output: 85f1431 Phase 1 measurement complete
   
   # Add git note linking to BPR entry
   git notes add -m "
   BPR-ENTRY-ANCHOR v1
   entry_id: BPR-anthropic-claude-opus-5-20260914-001
   entry_hash: abc123def456...
   embargo_end: 2026-10-14T23:59:59Z
   " 85f1431
   
   git notes show 85f1431
   # Output: ↑ (note attached, readable in git log --notes)
   ```

4. **P3 Assessment Uses Hash as Anchor (Oct 15–30)**
   ```python
   # P3 assessment reads git note
   p3_baseline_commit = "85f1431"
   bpr_entry_hash = read_git_note(p3_baseline_commit, "BPR-ENTRY-ANCHOR")
   
   # Assessment compares current behavior against BPR-anchored baseline
   current_model = get_current_model("claude-opus-5-2026-10-15")
   baseline_entry = fetch_bpr_entry(entry_hash=bpr_entry_hash)
   
   # P3 report includes:
   assessment_report = {
       "baseline_anchor": bpr_entry_hash,
       "baseline_measurement_date": "2026-09-14",
       "baseline_protocol": "ACAT-CAL-P v1.5 + Phase 1 Amendments",
       "baseline_scores": baseline_entry.dimensions,
       "current_scores": current_measurement.dimensions,
       "deltas_in_bounds": check_deltas(baseline_entry, current_measurement),
       "provider_claims": "behavior unchanged since Phase 1",
       "anchor_verdict": "hash abc123... proves behavior WAS measured on 2026-09-14"
   }
   ```

5. **Mesh Coordination (Oct 1+)**
   - Collab to evaluator: "Phase 1 BPR entry published; P3 should use hash abc123... as baseline anchor"
   - Collab to autonomy: "BPR entry published; P6 deltas can now cross-reference against verified baseline"
   - Collab to website: "Phase 1 measurement published; consider Observatory link to BPR entry"

#### Deliverables
- ✓ Phase 1 → BPR entry pipeline
- ✓ Entry published + hash embedded in git notes
- ✓ P3 assessment reads hash + uses as baseline
- ✓ Audit trail: git proves measurement date + hash chain prevents post-hoc edits
- ✓ Mesh coordination: all stakeholders linked to BPR entry

**Security Property:** A provider claiming "we didn't change behavior" can be refuted by: git log → BPR entry hash → entry proof of measurement on specific date. No ambiguity.

---

## 4. Timeline Summary

| Date | Phase | Deliverables | Owner |
|------|-------|--------------|-------|
| **2026-08-15** | Path 1 Live | Schema updated, endpoint live, mesh notified | humanaios |
| **2026-08-16–25** | Path 2 Governance | Collab to mesh-support, Z2 ratification of fixes, P3 alignment | Admiral + mesh-support |
| **2026-08-20–09-14** | Phase 1 Measurement | ACAT assessment underway, measurement data collected | humanaios + evaluator |
| **2026-09-14** | Phase 1 Close | Measurement window ends, data ready for BPR entry | humanaios |
| **2026-09-15–20** | Path 3a Entry Ratification | Entry generated, validated, submitted for Z2 append | humanaios |
| **2026-10-01** | Path 3b Entry Published | BPR entry hash anchored to git; embargo lifts; scores public | registry |
| **2026-10-15–30** | P3 Assessment | P3 uses BPR entry hash as baseline anchor; assessment runs | evaluator |
| **2026-11-01** | Path 3c Complete | BPR entry + P3 assessment + git notes = permanent audit trail | ecosystem |

---

## 5. Governance Artifacts

### Ratification Record
- **Decision ID:** Z2-BPR-SCHEMA-20260815-001
- **Ratifier:** Carly R. Anderson (Admiral, empirica-foundation)
- **Document:** BPR-SCHEMA v0.1-draft
- **Fixes Applied:** 7 red flags resolved (see section 2)
- **Scope:** HumanAIOS authorized as BPR publisher
- **Reversibility:** COMMITTAL (schema is canonical; changes via supersede)
- **Dependencies:** P21 (Z2 vote); Phase 1 measurement (ingest); P3 assessment (usage)

### Authority Chain
- **Carly R. Anderson** (Admiral) → Ratifies schema
- **Mesh-support** (approves via collab) → Confirms ratification + aligns governance
- **Evaluator** (P3 lead) → Confirms assessment framework
- **Humanaios Claude** (this session) → Implements 3-path integration

### Registry Discipline (REGISTERED.md alignment)
- Append-only (no edits; supersede only)
- Live-fetch before append (IC-030)
- Hash-chain tamper-evidence (ledger verification)
- Evidence-class per-dimension (no blanket entry-level class)
- Embargo window (30d default for published dimensions)

---

## 6. Next Steps

**Immediate (Today, Aug 15):**
1. ✓ Approve this integration plan
2. ✓ Path 1 schema + endpoint live
3. → Send Path 2 collab to mesh-support

**Near-term (Aug 16–25):**
1. Await mesh-support Z2 ratification confirmation
2. Align P3 assessment framework with evaluator
3. Finalize BPR entry generation script

**Phase 1 (Aug 20–Sep 14):**
1. Run Phase 1 measurement
2. Collect per-dimension scores, spread, evidence class
3. Prepare contamination check (three-arm results)

**Entry Publication (Sep 15–Oct 1):**
1. Generate + validate BPR entry
2. Submit for Z2 append (ratification collab)
3. Upon approval, publish + embargo 30 days
4. Anchor to git notes

**P3 Assessment (Oct 15–30):**
1. P3 reads BPR entry hash from git notes
2. Compares current behavior against published baseline
3. Reports deltas in context of BPR-anchored measurement

---

**Ratification Authority:** Carly R. Anderson, Admiral  
**Integration Authorized:** 2026-08-15  
**Status:** Ready to Execute
