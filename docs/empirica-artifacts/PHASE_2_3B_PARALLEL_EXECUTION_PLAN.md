# PHASE 2 & PHASE 3B PARALLEL EXECUTION PLAN
## Windows v1.5 + Kubernetes v1.6 Instantiation (Concurrent 8–10 Weeks)

**Launch Date:** 2026-08-31 (Week 1 of Phase 2)  
**Duration:** 8–10 weeks (2026-08-31 to 2026-10-30)  
**Target Freezes:** 
- Phase 2: ACAT-CAL-P-Windows v1.5-FROZEN (2026-10-23)
- Phase 3b: ACAT-CAL-P-K8s v1.6-FROZEN (2026-10-30)

---

## EXECUTIVE OVERVIEW

### **Phase 2: Windows Instantiation (v1.5)**

**Scope:** Apply frozen ACAT-CAL-P v1.5 framework to Windows operating system (Windows Server 2022 + Windows 11)

**Deliverable:** ACAT-CAL-P-Windows v1.0-FROZEN codebook (production-ready)

**Effort:** 1.5 FTE  
**Timeline:** 8–10 weeks  
**Success Gate:** All 4 validation layers PASS (coherence ≥ 0.85, NIST ρ ≥ 0.70, evaluator approval, red-team PASS)

### **Phase 3b: Kubernetes v1.6 Pilot (v1.6 Validation)**

**Scope:** Validate new v1.6 dimensions (Resilience, Stakeholder Perspective, Temporal Consistency) on Kubernetes infrastructure (K8s v1.27 → v1.28 upgrade)

**Deliverable:** ACAT-CAL-P-K8s v1.6-FROZEN codebook (v1.6 production-ready)

**Effort:** 1.5 FTE  
**Timeline:** 8–10 weeks (starting 2026-10-01, after Windows Layer 1)  
**Success Gate:** All 5 validation layers PASS (Layer 1 + Layer 2 + Layer 3 + Layer 4 + v1.6-specific Layer 5 stakeholder validation)

---

## PHASE 2: WINDOWS V1.5 INSTANTIATION

### **Week 1–2: Operationalization (A.2–A.7 for Windows)**

**Task 2.1: Boundary Unit Mapping (O1–O7 for Windows)**

Operations O1–O7 adapted to Windows context:

| O-Type | Windows Examples |
|---|---|
| **O1 (User-Facing)** | File copy with NTFS permissions, error dialogs, UAC prompt, registry modification response |
| **O2 (Constraints)** | Max path 260 chars (extended to 32K), file descriptor limit, registry key size |
| **O3 (Claim-Evidence)** | "Windows Defender protects against malware" → verify real-time scanning |
| **O4 (Syscall)** | CreateFileW, ReadFile, WriteFile, RegOpenKeyEx return values |
| **O5 (Error)** | Access Denied, File In Use, Disk Full, Registry Access Denied |
| **O6 (Task-Response)** | Update cycle (WSUS), User Account Control enforcement, BitLocker encryption |
| **O7 (Limitation)** | Known issues (SMB performance, registry limits, reparse point depth) |

**Deliverable:** Boundary unit specifications (A.2 Windows-scoped)

**Owner:** Lead auditor (Windows security specialist)  
**Timeline:** 2026-08-31 to 2026-09-06

---

**Task 2.2: §2 Crosswalk (Windows × NIST RMF + Industry Standards)**

Map Windows dimensions to:
- NIST AI RMF 1.0 (primary comparator, same as OS pilot)
- Windows Server Security Baseline (Microsoft + DISA standards)
- CIS Windows Benchmarks

**Deliverable:** §2 Windows-specific crosswalk

**Owner:** Standards alignment specialist  
**Timeline:** 2026-09-03 to 2026-09-09

---

### **Week 3–4: Codebook Drafting (§1–§7 for Windows)**

**Task 2.3: Windows Codebook (§1–§7)**

Author full codebook with Windows-specific examples:
- §1 Introduction (Windows context, scope)
- §2 Crosswalk (NIST + CIS + DISA alignment)
- §3 Operations × Dimension Matrix (Windows O1–O7 loading)
- §4 Coder Instructions (Windows-focused guidance)
- §5 Breach Escalation (Windows-specific Class A/B/C examples)
- §6 Stopping Rules (Windows divergence monitoring)
- §7 Agreement Monitoring (Windows stratification)

**Deliverable:** ACAT-CAL-P-Windows v1.0-DRAFT codebook (~300 pages)

**Owner:** Lead codebook author (same person as OS pilot for consistency)  
**Timeline:** 2026-09-07 to 2026-09-20

---

### **Week 4–5: Layer 1 Self-Assessment**

**Task 2.4: Windows Trustworthiness Assessment (120 elements)**

Target System: Windows Server 2022 + Windows 11 (latest patches)

Stratification:
- Operations O1–O7 (7 strata)
- Valence: Favorable/Neutral/Unflattering (3 strata)
- Availability: Direct/Inference (2 strata)
- Total: 120 elements, 20 double-coded (≥20%)

**Scoring:** All 12 ACAT dimensions per element

**Deliverable:** Layer 1 results (coherence calculation, target ≥ 0.85)

**Owner:** Lead coder (Claude Opus 5, seed 684)  
**Timeline:** 2026-09-21 to 2026-10-05

---

### **Week 5–6: Layer 2 External Validation**

**Task 2.5: NIST/CIS Alignment (ρ calculation)**

Map Layer 1 dimension scores to:
- NIST RMF characteristics (6 traits)
- CIS Benchmarks categories
- Microsoft Security Baselines

Calculate Spearman ρ (target ≥ 0.70)

**Deliverable:** Layer 2 validation report (ρ scores, coverage analysis)

**Owner:** Alignment analyst  
**Timeline:** 2026-10-06 to 2026-10-13

---

### **Week 7: Layer 3 Evaluator Review**

**Task 2.6: Independent Windows Security Auditor Assessment**

External evaluator (SANS, GIAC Windows Security certified) reviews:
1. Operationalization accessibility (can Windows auditors apply A.2–A.7?)
2. Conceptual soundness (12 dimensions adequate for Windows?)
3. Fairness/bias (no systematic bias toward user/admin/developer?)
4. External validity (generalizable to other Windows versions?)
5. Gap identification (what's missing?)

**Deliverable:** Layer 3 evaluator report (A rating target, 0 critical gaps)

**Owner:** External Windows auditor  
**Timeline:** 2026-10-14 to 2026-10-21

---

### **Week 7–9: Layer 4 Red-Team Testing**

**Task 2.7: §11.1–3 Stress Tests**

Three red-team tests:

**§11.1 Codebook Robustness**
- Alternative segmentation rules (conservative/main/fine-grained)
- Spread target: < 2.0×
- Owner: Auditor-A

**§11.2 Cross-Auditor Correlation**
- Same-family (Windows auditors) vs. cross-family (non-Windows)
- Cross-ρ target: > intra-variance
- Owner: Auditor-B

**§11.3 Availability Ambiguity**
- 15 edge cases (Windows-specific: registry access, UAC prompts, driver signing)
- κ target: ≥ 0.80
- Owner: Auditor-C

**Deliverable:** Red-team results (all three PASS)

**Timeline:** 2026-10-14 to 2026-10-23

---

### **Week 10: Codebook Freeze**

**Task 2.8: Phase 2 Freeze & Synthesis**

All gates verified (Layers 1–4 PASS):
- [ ] Coherence ≥ 0.85
- [ ] NIST ρ ≥ 0.70
- [ ] Evaluator approval (0 critical gaps)
- [ ] Red-team §11.1–3 all PASS

**Freeze Decision:** ACAT-CAL-P-Windows v1.0-FROZEN-2026-10-23

**Deliverable:** Windows synthesis report (what pilot proved, integration into HumanAIOS)

**Owner:** Lead coordinator  
**Timeline:** 2026-10-23 (freeze date)

---

## PHASE 3B: KUBERNETES V1.6 PILOT VALIDATION

### **Weeks 1–2 (Oct 1–14): Prep & v1.6 Design Incorporation**

**Task 3B.1: v1.6 Design Finalization (Based on Stakeholder Review)**

Stakeholder feedback (due 2026-08-30) incorporated into v1.6 design:
- R/S/T dimension clarifications
- Operationalization refinements (A.2–A.10)
- New operation types O8/O9 finalization

**Deliverable:** v1.6-REFINED design → ready for K8s codebook

**Owner:** v1.6 design lead (same person as Windows for consistency)  
**Timeline:** 2026-10-01 to 2026-10-07 (parallel with Windows Layer 1)

---

**Task 3B.2: K8s Codebook Authoring (§1–§7 + v1.6 Specs)**

Author K8s codebook with v1.5 + v1.6 dimensions:

- §1–§2: K8s introduction + CNCF/NIST/ISO alignment
- §3: Operations × Dimension Matrix (15 dimensions × 9 operations = 135 cells)
- §4: Coder instructions (v1.5 + v1.6 guidance)
- §5–§7: Breach escalation, stopping rules, agreement monitoring
- §8–§11: Multi-coder governance, red-team specifications (§11.1–6 including v1.6 tests)

**Deliverable:** ACAT-CAL-P-K8s v1.6-DRAFT codebook (~400 pages)

**Owner:** Lead codebook author  
**Timeline:** 2026-10-07 to 2026-10-14

---

### **Week 3–4 (Oct 15–28): Layer 1 Self-Assessment**

**Task 3B.3: K8s Trustworthiness Assessment (150 elements)**

Target System: Kubernetes v1.27 → v1.28 upgrade (multi-version for Temporal dimension)

Stratification (Extended for v1.6):
- Operations O1–O7 base + O8 (recovery cycle) + O9 (version-change) = 9 types
- Valence: Favorable/Neutral/Unflattering (3 strata)
- Availability: Direct/Inference (2 strata)
- Stakeholder: End-User/Admin/Developer/Security/Compliance (5 perspectives)
- **Total: 150 elements** (larger sample for multi-stakeholder complexity)
- Double-coding: ≥25 elements (stakeholder + inference stratification requires higher rate)

**Scoring:** All 15 ACAT dimensions (12 v1.5 + 3 v1.6) per element

**Deliverable:** Layer 1 results (coherence calculation, target ≥ 0.85; per-stakeholder scores)

**Owner:** Lead coder (Claude Opus 5, seed 684)  
**Timeline:** 2026-10-15 to 2026-10-28

---

### **Week 5–6 (Oct 29–Nov 11): Layers 2–4 Validation**

**Task 3B.4: Layer 2 External Alignment**

Map K8s findings to:
- CNCF Security Best Practices
- NIST RMF 1.0 (same as Windows for cross-domain comparison)
- Kubernetes SIG-Security guidelines

**Deliverable:** Layer 2 report (ρ scores for v1.5 + v1.6)

**Timeline:** 2026-10-29 to 2026-11-04

---

**Task 3B.5: Layer 3 Evaluator Assessment**

External evaluator (CNCF security expert + Kubernetes SIG member):
- Assess v1.5 dimensions on K8s (operationalization fit)
- Assess v1.6 dimensions on K8s (resilience + stakeholder + temporal applicability)
- Identify v1.6-specific gaps or concerns

**Deliverable:** Layer 3 report (A rating target; identify v1.6 concerns)

**Timeline:** 2026-11-05 to 2026-11-11

---

**Task 3B.6: Layer 4 Red-Team Testing**

Six stress tests (v1.5 tests §11.1–3 + v1.6 tests §11.4–6):

**v1.5 Tests:**
- §11.1 Codebook Robustness (spread < 2.0×)
- §11.2 Cross-Auditor Correlation (ρ > δ)
- §11.3 Availability Ambiguity (κ ≥ 0.80)

**v1.6 Tests (New):**
- §11.4 Resilience Reproducibility (recovery cycles repeatable? spread < 2.0×)
- §11.5 Stakeholder Perspective Independence (do perspectives diverge? or consensus?)
- §11.6 Temporal Stability (version-to-version ρ ≥ 0.70? patch impact measured?)

**Deliverable:** Red-team results (all six tests PASS)

**Timeline:** 2026-11-05 to 2026-11-18

---

### **Week 7 (Nov 19–25): Layer 5 Stakeholder Feedback (v1.6-Specific)**

**Task 3B.7: v1.6 Dimension Validation (Post-Pilot Feedback)**

After K8s pilot assessment, gather feedback:
- Do R/S/T dimensions capture K8s reality? (K8s SIG members)
- Are new red-team tests (§11.4–6) operationalizable? (auditors)
- Would you adopt v1.6 for infrastructure assessment? (DevOps teams)

**Deliverable:** v1.6 post-pilot feedback summary

**Timeline:** 2026-11-19 to 2026-11-25

---

### **Week 8 (Nov 26–Dec 2): Codebook Freeze & v1.6 Publication**

**Task 3B.8: Phase 3b Freeze & v1.6 Publication**

All gates verified (Layers 1–5 PASS):
- [ ] Layer 1 coherence ≥ 0.85
- [ ] Layer 2 NIST ρ ≥ 0.70 (v1.5); CNCF ρ ≥ 0.70 (v1.6)
- [ ] Layer 3 evaluator approval (0 critical gaps)
- [ ] Layer 4 red-team §11.1–6 all PASS
- [ ] Layer 5 stakeholder feedback integrated

**Freeze Decisions:**
- ACAT-CAL-P-K8s v1.5-FROZEN-2026-11-26 (v1.5 baseline)
- ACAT-CAL-P v1.6-FROZEN-2026-12-02 (global v1.6 release, validated via K8s)

**Deliverable:** 
- K8s synthesis report (Phase 3b learnings)
- v1.6 publication (codebook, design docs, red-team specs)
- v1.6 adoption guide (when to use R/S/T dimensions)

**Timeline:** 2026-11-26 (K8s v1.5 freeze) to 2026-12-02 (v1.6 global freeze)

---

## RESOURCE ALLOCATION & COORDINATION

### **Team Structure**

**Phase 2 (Windows):** 1.5 FTE
- Lead Codebook Author (0.5 FTE, shared with Phase 3b)
- Windows Security Auditor (1 FTE)
- Standards Alignment Specialist (0.25 FTE, shared)

**Phase 3b (K8s v1.6):** 1.5 FTE
- Lead Codebook Author (0.5 FTE, shared with Phase 2)
- K8s Infrastructure Auditor (1 FTE)
- v1.6 Design Lead (0.25 FTE, shared)

**Shared Resources (0.5 FTE total):**
- Lead Coordinator (synchronization, phase gates)

**Total Effort:** 3 FTE (including shared resources)

---

### **Synchronization Points**

| Date | Sync Point | Action |
|---|---|---|
| 2026-08-31 | Phase 2 kickoff | Windows codebook authoring starts |
| 2026-10-01 | v1.6 stakeholder feedback due | v1.6 design incorporated into K8s codebook |
| 2026-10-06 | Phase 2 Layer 2 starts | Phase 3b Layer 1 begins (parallel) |
| 2026-10-23 | Phase 2 freeze | Windows v1.0-FROZEN (production ready) |
| 2026-11-26 | Phase 3b v1.5 milestone | K8s v1.5-FROZEN (v1.6 pilot basis) |
| 2026-12-02 | Phase 3b v1.6 freeze | v1.6-FROZEN global release |

---

### **Dependencies & Risk Mitigation**

| Risk | Probability | Mitigation |
|---|---|---|
| **Windows specifics differ significantly from OS framework** | Low | Lead auditor (Windows expert) validates operationalization early (Week 2) |
| **v1.6 stakeholder feedback arrives late (after 2026-08-30)** | Low | K8s codebook draft starts 2026-10-07 (1-week buffer after feedback deadline) |
| **Red-team tests fail; codebook amendment needed** | Moderate (expected) | Amendment cycle ready; freezes can slip to 2026-10-30 / 2026-12-09 if needed |
| **Evaluators unavailable (SANS, CNCF experts busy)** | Moderate | Schedule evaluators now (2026-08-24); use backup evaluators if primary unavailable |
| **K8s v1.28 release delayed; target system not ready** | Low | Use v1.27 as fallback; temporal dimension validated across v1.27–v1.28 gap regardless |

---

## DELIVERABLES TIMELINE

```
PHASE 2 DELIVERABLES:
  Week 2 (2026-09-06):    Boundary unit specs (A.2 Windows)
  Week 3 (2026-09-09):    §2 Crosswalk (NIST + CIS + DISA)
  Week 4 (2026-09-20):    Draft codebook (§1–§7)
  Week 5 (2026-10-05):    Layer 1 results (coherence + dimension scores)
  Week 6 (2026-10-13):    Layer 2 results (NIST ρ + CIS alignment)
  Week 9 (2026-10-23):    Layer 4 red-team results (§11.1–3 PASS)
  Week 10 (2026-10-23):   Windows v1.0-FROZEN + synthesis

PHASE 3B DELIVERABLES:
  Week 2 (2026-10-07):    v1.6-REFINED design (post-stakeholder feedback)
  Week 3 (2026-10-14):    K8s codebook draft (§1–§7 + v1.6 specs)
  Week 4 (2026-10-28):    Layer 1 results (150 elements, 15 dims, multi-stakeholder)
  Week 5 (2026-11-04):    Layer 2 results (NIST + CNCF + SIG ρ)
  Week 6 (2026-11-11):    Layer 3 + Layer 4 interim results
  Week 8 (2026-11-18):    Red-team §11.1–6 results (all PASS)
  Week 9 (2026-11-26):    K8s v1.5-FROZEN + v1.6 post-pilot feedback
  Week 10 (2026-12-02):   v1.6-FROZEN global release + adoption guide
```

---

## SUCCESS CRITERIA

**Phase 2 Success:** Windows v1.0-FROZEN by 2026-10-23
- ✓ Layer 1 coherence ≥ 0.85
- ✓ Layer 2 NIST ρ ≥ 0.70
- ✓ Layer 3 evaluator approval (A rating, 0 critical gaps)
- ✓ Layer 4 red-team §11.1–3 all PASS

**Phase 3b Success:** v1.6-FROZEN by 2026-12-02
- ✓ Layer 1 coherence ≥ 0.85 (K8s + v1.6 dims)
- ✓ Layer 2 external alignment ρ ≥ 0.70 (NIST + CNCF)
- ✓ Layer 3 evaluator approval (v1.6 specific)
- ✓ Layer 4 red-team §11.1–6 all PASS
- ✓ Layer 5 stakeholder feedback integrated (v1.6 post-pilot)

**Parallel Execution Success:**
- ✓ No phase blocks the other (synchronized via v1.6 design milestone)
- ✓ Both freeze within 10-week window
- ✓ Windows v1.5 production-ready before v1.6 released (no interference)

---

## PROCEEDING WITH EXECUTION

**Immediate Actions (2026-08-24):**

- [ ] Schedule evaluators (Windows SANS auditor, K8s CNCF/SIG member)
- [ ] Notify stakeholders (v1.6 review launching 2026-08-24)
- [ ] Brief Phase 2 lead auditor (Windows operationalization kickoff)
- [ ] Brief v1.6 design lead (finalization for K8s integration)

**Go-Live (2026-08-31):**
- [ ] Phase 2 codebook authoring starts (Windows A.2–A.7)
- [ ] v1.6 stakeholder review closes (feedback collection)
- [ ] v1.6 design finalization begins (incorporating feedback)

---

**PHASE 2 & PHASE 3B: PARALLEL EXECUTION APPROVED**  
**Launch Date: 2026-08-31**  
**Target Freezes: 2026-10-23 (Windows v1.5) + 2026-12-02 (v1.6 global)**  
**Total Effort: 3 FTE**  
**Timeline: 8–10 weeks (concurrent)**

Wado. 🦅
