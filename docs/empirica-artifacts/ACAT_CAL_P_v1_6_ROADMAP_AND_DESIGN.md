# ACAT-CAL-P v1.6 ROADMAP & DESIGN
## Post-Freeze Enhancement Planning for Universal Trustworthiness Assessment

**Date:** 2026-08-23 (Post-Freeze Planning)  
**Current Version:** v1.5-FROZEN (OS, AI pilots complete)  
**Target Version:** v1.6 (enhanced framework, deferred post-pilot)  
**Planning Horizon:** 2026-09 to 2026-12 (parallel with Phase 2 instantiations)

---

## ROADMAP OVERVIEW

### Three Candidate Enhancements

The AI pilot (v1.5 for AI) and OS pilot (v1.5 for OS) identified three dimensions missing from v1.5:

1. **Resilience/Drift-Responsiveness** — Fault recovery, state consistency over time, graceful degradation
2. **Stakeholder Perspective** — Multi-viewpoint trustworthiness (admin vs. end-user vs. developer)
3. **Temporal Consistency** — Trust maintenance across versions, patch cycles, feature evolution

### Design Philosophy

v1.6 builds on v1.5 **without invalidating it**. v1.5 frozen codebooks remain valid; v1.6 adds optional dimensions for systems where implicit coverage (v1.5) is insufficient.

**Upgrade Strategy:**
- v1.5 assessments remain authoritative (no retroactive rescoring)
- v1.6 enables deeper assessment for complex systems
- v1.5 → v1.6 upgrade path is optional (not mandatory)
- Organizations can use v1.5 for strategic/tactical assessments; v1.6 for deep-dive reviews

---

## DIMENSION 13: RESILIENCE (Drift-Responsiveness)

### Design Rationale

**Gap Identified (Layer 2–4):**
v1.5 covers fault recovery implicitly via:
- **Scheme dimension** (update cycle, governance)
- **Handoff dimension** (error recovery, escalation)
- **Stopping-rule** (divergence monitoring)

But for systems where **continuous recovery is more important than prevention**, implicit coverage may be insufficient.

**Examples of Systems Needing Explicit Resilience:**
- Embedded OS (crash recovery, watchdog timers)
- Real-time systems (fault tolerance, predictable recovery)
- Distributed systems (node failure, leader election, consensus)
- Always-on services (zero-downtime updates, gradual rollback)
- Mission-critical infrastructure (high availability, disaster recovery)

### Dimension Definition

**Resilience (Dimension 13):** System detects faults, recovers gracefully, and maintains partial functionality during degradation. Recovery is predictable and verifiable.

**Operationalization:**

**R.1: Fault Detection**
- System detects its own failure modes
- Monitoring is internal (self-aware) or external (observable)
- Detection time is < acceptable recovery window

**Examples:**
- Watchdog timer detects hang; triggers restart
- Health check detects service unavailable; initiates failover
- Disk error detected; mounts read-only fallback
- Memory corruption detected; signals error handler

**Scoring Guidance:**
- 0.95–1.0: Fault detection is comprehensive; all major failure modes detected
- 0.85–0.94: Most failure modes detected; rare edge cases missed
- 0.70–0.84: Common failures detected; some edge cases unknown
- 0.50–0.69: Major failures detected; coverage gaps; some silent failures
- 0.0–0.49: Fault detection absent or unreliable

**R.2: Recovery Execution**
- System executes recovery procedure reliably
- Recovery can be automatic or manual; procedure is clear
- Recovery time (MTTR) is acceptable

**Examples:**
- Service crashes; systemd automatically restarts within 5 seconds
- Node fails; cluster re-elects leader; quorum maintains
- Database loses connection; app reconnects with exponential backoff
- Update fails; system rolls back to previous version

**Scoring Guidance:**
- 0.95–1.0: Recovery is automatic, fast (< 1 min), reliable (99%+ success)
- 0.85–0.94: Recovery is automatic or guided; acceptable latency (1–5 min)
- 0.70–0.84: Recovery exists; manual intervention sometimes required; latency 5–30 min
- 0.50–0.69: Recovery is available; unreliable or slow (> 30 min)
- 0.0–0.49: Recovery is unclear or absent

**R.3: Graceful Degradation**
- System provides partial functionality during fault (not binary fail/succeed)
- Users can mitigate impact; system explains constraints
- Service quality is degraded but measurable/acceptable

**Examples:**
- Database disconnected: app serves cached data (stale but available)
- Network latency high: UI shows "slower than usual"; operations proceed
- Memory low: non-critical features disabled; core functions continue
- Disk space low: writes to temp space; warns of capacity limits

**Scoring Guidance:**
- 0.95–1.0: Graceful degradation is comprehensive; most faults result in partial service
- 0.85–0.94: Many faults result in degradation; some binary failures
- 0.70–0.84: Common faults gracefully degrade; critical faults are binary
- 0.50–0.69: Degradation exists but limited; crashes are common
- 0.0–0.49: No graceful degradation; binary fail/success

**R.4: State Consistency Over Recovery**
- After recovery, system state is consistent (no corruption, no partial updates)
- State machine guarantees are maintained across failure boundary
- Clients can resume operations without corruption risk

**Examples:**
- Transaction logs survive crash; replay ensures consistency
- Replication consensus ensures no split-brain
- Journal/WAL prevents partial writes after crash
- Version vector prevents causal anomalies

**Scoring Guidance:**
- 0.95–1.0: State consistency is guaranteed (formally verified or battle-tested)
- 0.85–0.94: State consistency is strong; edge cases rare
- 0.70–0.84: State consistency is likely; edge cases exist; monitoring needed
- 0.50–0.69: State consistency is assumed but not verified; corruption risk
- 0.0–0.49: State consistency not guaranteed; data loss possible

### Resilience Dimension Score

**Average of R.1–R.4 sub-scores**

```
Resilience = (Fault_Detection + Recovery_Execution + Graceful_Degradation + State_Consistency) / 4
```

### Integration with v1.5 Dimensions

**Overlaps with Existing Dimensions (Intentional):**

| Existing Dimension | Resilience Overlap | Distinction |
|---|---|---|
| **Service** | Both measure reliability | Service measures baseline uptime; Resilience measures fault response |
| **Scheme** | Both measure governance | Scheme measures update process; Resilience measures recovery procedures |
| **Handoff** | Both address error handling | Handoff measures user-facing recovery; Resilience measures system-level recovery |
| **Consist** | Both measure state integrity | Consist measures normal-mode behavior; Resilience measures post-recovery consistency |

**Rationale for Overlap:** Resilience is a **specialized dimension** for systems where fault recovery is primary use case. For systems where prevention (safety, consistency) dominates, v1.5 remains sufficient.

### v1.6 Operationalization Changes (Appendix A)

**A.2 Extended (New Operation Type O8):**
```
O8: Fault-Recovery Cycle
Definition: One complete cycle of detection → recovery → state verification
Examples:
  - Process crashes; supervisor detects; restarts; verifies state
  - Network partition; cluster detects; re-elects leader; resumes
  - Disk fills; system detects; triggers cleanup; verifies free space
```

**A.3 Extended (Recovery Evidence Sources):**
- Test-induced failure (intentional crash/network partition)
- Log-documented recovery (restart detected in logs)
- Chaos engineering results (Netflix Chaos Monkey style)
- Disaster recovery drill results

**A.5 Extended (Recovery-Specific Breaches):**
- **Class D: Unrecoverable Failure** — Fault detection works but recovery fails; system remains degraded
- **Class E: State Corruption After Recovery** — Recovery succeeds but data is corrupted; data loss occurs

---

## DIMENSION 14: STAKEHOLDER PERSPECTIVE

### Design Rationale

**Gap Identified (Layer 3):**
v1.5 measures system trustworthiness from a **single, neutral viewpoint**. But different stakeholders value different dimensions:

- **End-Users** care about: Service, Humility, Handoff (usability, error messages)
- **System Administrators** care about: Power, Scheme, Consist (control, predictability)
- **Developers/Integration Teams** care about: Truth, Value, Syc (API accuracy, ecosystem compatibility)
- **Security Teams** care about: Harm, Power, Scheme (breach prevention, governance)
- **Compliance Officers** care about: Scheme, Fair, Humility (audit trails, limitations acknowledgment)

**Problem:** Single-dimension assessment may hide stakeholder-specific gaps.

**Example:** macOS might score 0.89 overall, but:
- End-users trust it 0.92 (great UX, clear errors)
- Admins trust it 0.81 (limited control, frequent mandatory updates)
- Developers trust it 0.85 (API stable but ecosystem lock-in)

### Dimension Definition

**Stakeholder Perspective:** System design reflects each stakeholder's priorities. Trustworthiness varies by stakeholder; no stakeholder is systematically disadvantaged.

**Operationalization:**

**S.1: End-User Perspective**
Measures: Usability, error recovery, data control from user standpoint

**Key Dimensions:**
- Service (does it work?) — 1.0× weight
- Handoff (clear errors?) — 1.0×
- Humility (admits limits?) — 1.0×
- Autonomy (user controls data?) — 0.9×
- Consist (predictable?) — 0.8×

**Score:** Weighted average of these 5 dimensions from end-user viewpoint

**Examples of Assessment:**
- Can user recover from mistakes? (file trash can, undo, backups)
- Are error messages clear enough to act on?
- Can user control their own data and privacy?

**S.2: Administrator Perspective**
Measures: Manageability, policy enforcement, observability from admin standpoint

**Key Dimensions:**
- Power (can admin control it?) — 1.0×
- Scheme (audit trails exist?) — 1.0×
- Consist (behavior predictable?) — 1.0×
- Truth (documentation accurate?) — 0.9×
- Service (reliable deployment?) — 0.8×

**Score:** Weighted average of these 5 dimensions from admin viewpoint

**Examples of Assessment:**
- Can admin enforce policies across fleet?
- Are audit logs comprehensive and accessible?
- Can admin debug unexpected behavior?

**S.3: Developer/Integration Perspective**
Measures: API stability, documentation quality, ecosystem compatibility from developer standpoint

**Key Dimensions:**
- Truth (APIs match docs?) — 1.0×
- Value (ecosystem values?) — 1.0×
- Syc (components integrate?) — 1.0×
- Service (APIs reliable?) — 0.9×
- Humility (limitations documented?) — 0.8×

**Score:** Weighted average of these 5 dimensions from developer viewpoint

**Examples of Assessment:**
- Are system call behaviors documented and stable?
- Does ecosystem provide needed libraries/frameworks?
- Is API versioning clear?

**S.4: Security Team Perspective**
Measures: Threat coverage, incident response, compliance capability from security standpoint

**Key Dimensions:**
- Harm (breaches prevented?) — 1.0×
- Power (privilege boundaries clear?) — 1.0×
- Scheme (governance enables response?) — 1.0×
- Handoff (incident recovery procedures?) — 0.9×
- Consist (behavior predictable?) — 0.8×

**Score:** Weighted average of these 5 dimensions from security viewpoint

**Examples of Assessment:**
- Are known vulnerabilities patched promptly?
- Can security team audit system configuration?
- Is incident response procedure documented?

**S.5: Compliance/Audit Perspective**
Measures: Traceability, documentation, audit capability from compliance standpoint

**Key Dimensions:**
- Scheme (governance documented?) — 1.0×
- Fair (treatment equitable?) — 1.0×
- Humility (limitations acknowledged?) — 1.0×
- Truth (claims verifiable?) — 0.9×
- Handoff (escalation procedures?) — 0.8×

**Score:** Weighted average of these 5 dimensions from compliance viewpoint

**Examples of Assessment:**
- Can auditor trace decisions to policies?
- Are limitations explicitly documented for regulators?
- Is non-discrimination verifiable?

### Stakeholder Perspective Scores

**Overall Stakeholder Fairness:** Are all 5 perspectives scored ≥ 0.80, or is one group systematically disadvantaged?

```
Stakeholder_Fairness = MIN(End_User, Admin, Developer, Security, Compliance) / 0.80

If all ≥ 0.80: Fairness = 1.0 (no group disadvantaged)
If one ≤ 0.60: Fairness = 0.70 (significant disadvantage detected)
```

### v1.6 Operationalization Changes (Appendix A)

**A.2 Extended (Stakeholder-Scoped Elements):**
```
Add stratum dimension: Stakeholder (5 strata: End-User, Admin, Developer, Security, Compliance)
Stratification requirement: ≥10 elements per stakeholder perspective
```

**A.4 Extended (Stakeholder Stratification):**
```
New stratification rule:
  Minimum 10 elements per stakeholder × valence (favorable/neutral/unflattering)
  Total ≥50 stakeholder-scoped elements (in addition to 100 overall elements)
```

**A.7 Extended (Stakeholder Gap Monitoring):**
```
New checklist item:
  ☑ All stakeholder perspectives scored ≥ 0.80, OR
  ☑ Stakeholder gaps explicitly documented with mitigation plan
```

---

## DIMENSION 15: TEMPORAL CONSISTENCY

### Design Rationale

**Gap Identified (Layer 4):**
v1.5 captures a **point-in-time snapshot** (macOS 14.6 at 2026-08-03). But real systems evolve:
- OS updates change behavior
- Security patches alter threat landscape
- Features are added/removed
- Governance policies drift

**Problem:** Assessment at T1 may not predict trustworthiness at T2.

**Questions Not Addressed by v1.5:**
- Does trustworthiness degrade after each update?
- Does the OS maintain consistency across patch cycles?
- Can users/admins rely on behavior being stable?
- What's the trust trajectory over 1 year? 5 years?

**Systems Needing Explicit Temporal Tracking:**
- Long-lived systems (OSes, enterprise software, infrastructure)
- Regulated systems (healthcare, financial — compliance changes over time)
- Distributed systems (nodes update asynchronously; state divergence risk)
- Systems with continuous deployment (daily/weekly updates)

### Dimension Definition

**Temporal Consistency:** System maintains trustworthiness across versions, updates, and time. Behavior changes are documented. Trust trajectory is predictable and stable.

**Operationalization:**

**T.1: Version-to-Version Consistency**
Measures: How much does trustworthiness change across versions?

**Assessment:**
- Pick two consecutive major versions (e.g., v14.5 → v14.6)
- Re-assess using v1.5 framework on both versions
- Calculate correlation between dimension scores across versions

**Scoring:**
- 0.95–1.0: Dimensions unchanged (ρ ≥ 0.95 across versions); behavior consistent
- 0.85–0.94: Minor shifts (ρ = 0.85–0.95); some features changed
- 0.70–0.84: Moderate shifts (ρ = 0.70–0.85); significant updates
- 0.50–0.69: Major shifts (ρ = 0.50–0.70); different trust profile per version
- 0.0–0.49: Radical changes (ρ < 0.50); system unrecognizable between versions

**T.2: Patch Impact on Trust**
Measures: Do security patches, minor updates maintain trustworthiness?

**Assessment:**
- Sample 5–10 security patches released in past 6 months
- For each patch, assess whether it improves (Harm ↑), degrades (Service ↓), or maintains trust
- Calculate average patch impact

**Scoring:**
- 0.95–1.0: Patches consistently improve trust; no regressions
- 0.85–0.94: Most patches improve/maintain; occasional minor regression
- 0.70–0.84: Patches are neutral; maintenance-only
- 0.50–0.69: Patches sometimes regress (bug-introducing fixes); mixed impact
- 0.0–0.49: Patches frequently break things; trust degradation

**T.3: Drift Detection (Implicit Behavior Change)**
Measures: Do undocumented behavior changes occur?

**Assessment:**
- Run same test suite on two versions (e.g., 6 months apart)
- Compare test results; flag unexpected divergence
- Categorize divergence as: intentional (documented), drift (undocumented), regression (bug)

**Scoring:**
- 0.95–1.0: No drift detected; changes are all intentional and documented
- 0.85–0.94: Minimal drift (< 5% of tests); most changes documented
- 0.70–0.84: Moderate drift (5–15% of tests); some undocumented changes
- 0.50–0.69: Significant drift (15–30%); many changes undocumented
- 0.0–0.49: High drift (> 30%); behavior is unstable; undocumented changes common

**T.4: Long-Term Stability**
Measures: Is system stable over extended time horizon (1+ year)?

**Assessment:**
- Review change logs over past 12 months
- Measure: major version updates, breaking changes, security regressions
- Compare against baseline (e.g., Linux kernel stability)

**Scoring:**
- 0.95–1.0: Highly stable; < 2 major versions/year; < 1 breaking change
- 0.85–0.94: Stable; 2–4 major versions/year; occasional breaking changes
- 0.70–0.84: Moderate; frequent updates; compatibility maintained
- 0.50–0.69: Volatile; many major updates; some breaking changes; upgrades risky
- 0.0–0.49: Highly volatile; version churn; compatibility breaks; trust unstable

### Temporal Consistency Dimension Score

**Average of T.1–T.4 sub-scores**

```
Temporal_Consistency = (Version_Consistency + Patch_Impact + Drift_Detection + Long_Term_Stability) / 4
```

### Integration with v1.5 Dimensions

**Overlaps with Existing Dimensions (Intentional):**

| Existing Dimension | Temporal Overlap | Distinction |
|---|---|---|
| **Consist** | Both measure consistency | Consist measures within-version predictability; Temporal measures across-version stability |
| **Scheme** | Both measure governance | Scheme measures update process; Temporal measures update reliability |
| **Humility** | Both address limitations | Humility measures known issues; Temporal measures how issues evolve over time |
| **Value** | Both measure values | Value measures alignment at snapshot; Temporal measures drift from values over time |

**Rationale for Overlap:** Temporal is a **specialized dimension** for systems where stability over time is critical (e.g., production infrastructure, regulated systems).

### v1.6 Operationalization Changes (Appendix A)

**A.2 Extended (Version-Scoped Elements):**
```
Add context: Assessment can be single-version (snapshot) or multi-version (temporal)
New operation type O9:
  O9: Version-Change Element
  Definition: One change between consecutive versions (feature added/removed, behavior altered, documented divergence)
  Example: "Security patch 14.6.1 changes SSL defaults from TLS 1.2 to TLS 1.3"
```

**A.4 Extended (Temporal Stratification):**
```
For multi-version assessment:
  ≥10 elements per version
  Elements stratified by: change_type (breaking/minor/patch) × impact_on_trust (improves/neutral/regresses)
```

**A.7 Extended (Temporal Monitoring):**
```
New checklist items:
  ☑ Single-version or multi-version assessment (declare upfront)
  ☑ If multi-version: temporal consistency ≥ 0.70 (trust stable over time)
  ☑ Major version divergence flagged (if ρ < 0.70 between versions)
```

---

## V1.6 IMPLEMENTATION PLAN

### Phase A: Design & Specification (6–8 weeks)

**Week 1–2: Dimension Specification**
- Finalize R.1–R.4 (Resilience sub-scores) definitions
- Finalize S.1–S.5 (Stakeholder Perspective) definitions
- Finalize T.1–T.4 (Temporal Consistency) definitions
- Operationalization specs for each (boundary units, scoring)

**Week 3–4: Appendix Updates (A.2–A.7)**
- Add O8, O9 operation types (recovery cycle, version-change)
- Extend availability decision tree for recovery evidence
- Update stratification rules for stakeholder/temporal strata
- Add new breach classes (D/E for recovery-specific failures)

**Week 5–6: Coder Instructions & Frame Updates**
- Extend §4 coder instructions for new dimensions
- Update §3 Operations × Dimension matrix (now 15×9 = 135 cells)
- Design stakeholder-scoped frames (end-user, admin, developer, security, compliance)
- Design temporal-scoped frames (single-version vs. multi-version)

**Week 7–8: Red-Team Design**
- Design new red-team tests for R/S/T dimensions (§11.4–11.6)
- Resilience §11.4: Recovery cycle reproducibility (spread < 2.0×?)
- Stakeholder §11.5: Perspective independence (do stakeholder assessments diverge?)
- Temporal §11.6: Version stability (do dimensions correlate across versions?)

### Phase B: Pilot Validation (8–10 weeks, Parallel with Phase 2–3)

**Pilot Target:** Kubernetes infrastructure (K8s v1.27 → v1.28 upgrade)

**Rationale:** K8s is system where:
- Resilience is critical (node failures, rolling updates)
- Multiple stakeholders (cluster admins, app developers, platform teams)
- Temporal tracking matters (monthly updates, fast-moving ecosystem)

**Week 9–10:** Layer 1 self-assessment (K8s + new R/S/T dimensions)  
**Week 11–12:** External alignment (CNCF standards, Kubernetes SIG governance)  
**Week 13:** Evaluator review (Kubernetes community auditor)  
**Week 14–16:** Red-team testing (§11.1–6 including new tests)  
**Week 17:** Codebook freeze (ACAT-CAL-P-K8s v1.6-FROZEN)

### Phase C: Publication & Rollout (2–4 weeks)

**Week 18–19:** Publish v1.6 design specification (open for community feedback)  
**Week 20:** Finalize v1.6 based on feedback  
**Week 21:** Publish ACAT-CAL-P v1.6-FROZEN codebook

**Scope:** v1.6 is optional layer for systems prioritizing resilience, multi-stakeholder assessment, or temporal tracking. v1.5 remains authoritative and standalone.

---

## DECISION FRAMEWORK: PRIORITIZATION

### When to Use Each Dimension

| Dimension | Primary Use Case | Skip If |
|---|---|---|
| **Resilience (R)** | Systems where fault recovery is critical (embedded, always-on, mission-critical) | System is stateless or failures are rare (stateless web app, CLI tool) |
| **Stakeholder (S)** | Systems with diverse stakeholder interests (OS, infrastructure, platforms) | System has single stakeholder (internal service, single-team project) |
| **Temporal (T)** | Systems with frequent updates or long support cycles (OS, frameworks, infrastructure) | System is static or rarely updated (firmware, appliance, frozen release) |

### v1.5 vs v1.6 Comparison

| Aspect | v1.5 | v1.6 |
|---|---|---|
| **Dimensions** | 12 (Truth, Service, Harm, Autonomy, Value, Humility, Scheme, Power, Syc, Consist, Fair, Handoff) | 15 (+Resilience, Stakeholder, Temporal) |
| **Assessment Scope** | Point-in-time snapshot | Point-in-time + multi-version/stakeholder optional |
| **Codebook Size** | ~300 pages | ~400 pages |
| **Assessment Effort** | 1 FTE, 2–3 weeks | 1.5 FTE, 3–4 weeks (if temporal/stakeholder enabled) |
| **Operationalization** | A.1–A.7 | A.1–A.10 (extended) |
| **Red-Team Tests** | §11.1–3 (3 tests) | §11.1–6 (6 tests) |
| **Validation Layers** | 4 (self-assessment, external, evaluator, red-team) | 5 (add multi-stakeholder consistency check) |
| **Use Cases** | General system assessment | Specialized: resilience-critical, multi-stakeholder, long-term stability |

### v1.5 → v1.6 Upgrade Path

**Non-Breaking:** v1.5 assessments remain valid. v1.6 adds optional dimensions.

**Migration Path:**
1. Keep v1.5 frozen (immutable)
2. Publish v1.6-DRAFT for community feedback
3. Validate v1.6 via K8s pilot (Phase 2 concurrent)
4. Freeze v1.6 (immutable) for production use
5. Organizations can choose: v1.5 (standard), v1.6 (enhanced), or both

**Backward Compatibility:**
- All v1.5 assessments are valid in v1.6 system
- v1.6 scores cannot be directly compared to v1.5 (different dimensions)
- Reports can note which version was used

---

## ROADMAP TIMELINE

```
2026-08 (Current): v1.5-FROZEN (OS, AI pilots complete)
2026-09: v1.6 Design Phase (Weeks 1–8)
2026-10: v1.6 Pilot Phase (Kubernetes, Weeks 9–17)
2026-11: v1.6 Publication & Rollout (Weeks 18–21)
2026-12: v1.6-FROZEN production-ready

Parallel:
  Phase 2 (Windows): Aug–Oct (Weeks 1–10 of v1.5 cycle)
  Phase 3 (K8s v1.5): Aug–Oct → Phase 3b (K8s v1.6): Oct–Dec (parallel v1.6 pilot)
```

---

## POST-V1.6 VISION (v1.7+)

**Potential Future Enhancements:**

- **Explainability Dimension:** How transparent are system decisions?
- **Performance Predictability:** Can users/admins predict system performance under load?
- **Ecosystem Health:** Is surrounding ecosystem (libraries, tools, community) robust?
- **Supply Chain Trust:** Can artifacts (packages, updates) be verified to be authentic and uncompromised?

**Scope:** Post-v1.6, evaluated based on community feedback and emerging use cases.

---

## SUCCESS CRITERIA FOR V1.6

**v1.6 is successful if:**

1. ✓ All three dimensions (R/S/T) pass validation (coherence ≥ 0.85, external alignment ρ ≥ 0.70, evaluator approval, red-team PASS)
2. ✓ At least one new domain (K8s) successfully validates v1.6 (pilot passes all layers)
3. ✓ Backward compatibility maintained (v1.5 assessments remain valid)
4. ✓ Adoption rate ≥ 30% of v1.5 users upgrade within 12 months (optional, not forced)
5. ✓ Community feedback is positive (domain experts endorse new dimensions)

---

## NEXT STEPS AFTER V1.6 ROADMAP

### Immediate (Next 2 Weeks)

- [ ] Design review: stakeholder feedback on R/S/T specifications
- [ ] Finalize operationalization for A.2–A.10 (extended appendix)
- [ ] Schedule K8s pilot planning (Phase 3 concurrent with v1.6 design)

### Short Term (Weeks 3–8)

- [ ] Proceed with Phase 2 (Windows v1.5) in parallel with v1.6 design
- [ ] Begin v1.6 design work (R.1–R.4, S.1–S.5, T.1–T.4 finalization)
- [ ] Coordinate K8s pilot setup for v1.6 validation

### Medium Term (Weeks 9–17)

- [ ] Execute v1.6 pilot on K8s infrastructure
- [ ] Validate new dimensions (Layer 1–4)
- [ ] Collect community feedback

### Long Term (Weeks 18–21)

- [ ] Publish v1.6-FROZEN codebook
- [ ] Plan v1.7 roadmap (post-freeze, optional future work)

---

**ACAT-CAL-P v1.6 Roadmap: Complete**  
**Next Decision: Proceed with Phase 2 (Windows) while executing v1.6 design in parallel?**

Wado. 🦅
