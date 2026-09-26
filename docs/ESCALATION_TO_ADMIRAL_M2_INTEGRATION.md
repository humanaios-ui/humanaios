# Escalation to Admiral: M2 Audit + HumanAIOS-Empirica Integration Design

**Date:** 2026-07-23  
**From:** empirica-foundation-evaluator  
**To:** Admiral (Carly R. Anderson)  
**CC:** David (empirica.david.empirica-mesh-support for mesh routing)  
**Status:** READY FOR REVIEW

---

## EXECUTIVE SUMMARY

Two completed investigations with strategic implications:

1. **M2 State Audit** — M2R2-R3 complete/stable. M2R4 Phase 1 (Schema Discovery) complete. **BLOCKER:** 3 breaking inconsistencies + 5 unknowns require design decisions before Phase 2 automation can proceed.

2. **HumanAIOS-Empirica Integration Design** — Comprehensive partnership architecture completed across three dimensions (operator/research/organizational). **3 strategic decisions locked.** Needs Admiral approval to proceed with Phase 1 operator implementation.

**Recommendation:** Both efforts are interdependent. M2R4 Phase 2 (schema harmonization) should incorporate findings from integration planning (particularly humanaios practice + HumanAIOS LLC entity model). Parallel execution: escalate M2 decisions + proceed with operator implementation.

---

## PART 1: M2 STATE AUDIT FINDINGS

### M2 Completion Status

| Rank | Phase | Status |
|------|-------|--------|
| **M2R2** | State Harmonization | ✅ COMPLETE |
| **M2R3** | Entity Registry | ✅ COMPLETE (22+ entities, 51+ relationships) |
| **M2R4 Phase 1** | Schema Discovery | ✅ COMPLETE |
| **M2R4 Phase 2** | Schema Design | 🟡 BLOCKED |

### M2R4 Phase 1 Findings (3 Blocking Inconsistencies)

#### **Finding 1: project.yaml Field Ordering** (SEVERITY: HIGH)
- **Issue:** Type A (evaluator, humanaios) places org_id/tenant/mesh/canonical_seat after domain (line 8)
- Type B (autonomy, mesh-support, outreach, website) places at end after calibration_weights
- Both are v2.0 despite structural change — no version increment
- **Impact:** Automation parsing breaks on field ordering assumptions
- **Action Required:** Define canonical field order + create migration script

#### **Finding 2: Governance Document Distribution Gap** (SEVERITY: HIGH)
- **Issue:** 4 foundation practices reference AUTHORITY_MATRIX.yaml, AUTHORITY_MAPPING.md, ESCALATION_PROTOCOL.md that don't exist locally
- References use `@../docs/` assuming non-existent shared parent directory
- **Impact:** Path resolution fails; 4 practices can't import governance docs
- **Action Required:** Centralize docs + establish @-include mechanism + validate references

#### **Finding 3: CLAUDE.md Authority Section Variants** (SEVERITY: HIGH)
- **Issue:** Variant 1 (evaluator, humanaios) uses @docs/ absolute paths + managed block + Z3_PROTOCOL upstream
- Variant 2 (4 practices) uses @../docs/ relative paths + different auto-approval logic
- **Impact:** Inconsistent governance interpretation across practices
- **Action Required:** Standardize Authority section template + field definitions + path convention

### M2R4 Phase 1 Unknowns (5 Decisions Needed)

1. **Governance document centralization strategy**
   - Should docs live in evaluator/docs with @-include imports from others?
   - Or move to shared foundation location?
   - How to prevent stale copies in humanaios?

2. **Z3_PROTOCOL location and ownership**
   - Is it local (empirica-outreach root, humanaios/operations) or upstream?
   - Why inconsistent placement?
   - Should evaluator reference it as upstream or local?

3. **Path reference convention**
   - Should @../docs/ references work?
   - If so, what's the intended shared parent directory?
   - Or standardize all to @docs/ with local copies?

4. **Practice charters scope**
   - Should all practices have CHARTER.md, or is autonomy-specific sufficient?
   - What should charters contain?

5. **Field ordering rule for project.yaml**
   - Current order is neither alphabetical nor chronological
   - Should we enforce alphabetical order or keep implicit grouping?

---

## PART 2: HUMANAIOS-EMPIRICA INTEGRATION DESIGN

### Strategic Decisions (Ready for Approval)

#### **Decision 1: ACAT API as Public Mesh Service**
- **Choice:** Expose ACAT API (POST /api/v1/acat/assess) as callable mesh service, ultimately public
- **Rationale:** Enables foundation practices to use behavioral assessment as grounding signal. Public status allows ecosystem adoption.
- **Deployment:** Standalone API at api.humanaios.ai + proxy through empirica-mesh-support for internal auth
- **Impact:** ACAT becomes foundational infrastructure (like calibration layer)
- **Status:** ✅ Ready to implement (Phase 1)

#### **Decision 2: Hybrid Organizational Model**
- **Choice:** humanaios practice (open research) + HumanAIOS LLC (commercial/confidential)
- **Rationale:** Allows Carly to participate in foundation research + governance while protecting business interests
- **Implication:** humanaios practice is public research seat; HumanAIOS LLC handles confidential work, business ops, IP
- **Status:** ✅ Ready to implement (practice setup)

#### **Decision 3: ACAT as Calibration Signal Source**
- **Choice:** Use ACAT assessments to ground Empirica vector calibration + measure convergence/divergence
- **Rationale:** ACAT measures "how well AI describes itself" (12 dimensions); Empirica measures "how well AI predicts outcomes" (13 vectors). Complementary grounding signals.
- **Methodology:** Monthly convergence report surfaces agreements + divergences (learning opportunities)
- **Status:** ✅ Ready to implement (research phase)

### Integration Architecture Highlights

**Operator Integration (Phase 1):**
- Data flow: ACAT assessment → Empirica finding (payload schema defined)
- Auth model: API key per practice, rotated quarterly
- Versioning: Schema v5.4 frozen at integration, 6mo deprecation window

**Research Integration (Phase 2):**
- Dimensional mapping: humility↔uncertainty, truth↔signal, scheme↔coherence, autonomy↔do
- Cross-validation: Learning Index vs Empirica vector subset
- Feedback: Monthly convergence report (agreements, divergences, patterns)

**Organizational Integration:**
- Entity model: humanaios practice (open) + HumanAIOS LLC (separate)
- Governance: humanaios inherits foundation protocols; HumanAIOS LLC separate Zone 2
- Mesh participation: humanaios can collab/propose with foundation; routes through mesh-support

---

## PART 3: INTERDEPENDENCIES & RECOMMENDATIONS

### How Integration Planning Informs M2R4 Phase 2

**Key Finding:** The hybrid organizational model (humanaios practice + HumanAIOS LLC) creates new governance edges that M2R4 schema design must account for.

**Specific implications:**
1. **Practice schema:** humanaios needs to inherit foundation governance docs (@docs/ references). How should this be specified in project.yaml or CLAUDE.md Authority section?
2. **Entity model:** Should HumanAIOS LLC be registered as a separate entity in Empirica's entity_registry? If so, what entity_type?
3. **Authority zones:** HumanAIOS LLC is separate from humanaios practice governance. How should escalation rules reflect this?

**Recommendation:** M2R4 Phase 2 (Schema Design) should address these unknowns in conjunction with the 5 M2R4 unknowns above.

### Proposed Parallel Execution

**Track A: M2R4 Phase 2 Decisions**
- Resolve 5 M2 unknowns (governance centralization, Z3_PROTOCOL, path convention, charters, field ordering)
- Address 3 integration-informed questions (practice schema for humanaios, entity model for HumanAIOS LLC, authority zone alignment)
- Timeline: 1 week for Admiral decisions → Phase 2 design can proceed

**Track C: Operator Implementation (Phase 1)**
- Deploy ACAT API endpoint specs + mesh-support proxy
- Configure auth/secrets for foundation practices
- Set up humanaios practice in foundation mesh
- Timeline: 2-3 weeks (independent of M2R4 Phase 2)

**Both tracks unblock downstream work:**
- M2R4 Phase 2 → Phase 3-6 specifications (sync pipeline, verification)
- Phase 1 → Phase 2 (research convergence) → Phase 3 (full mesh integration)

---

## DECISION PROMPTS FOR ADMIRAL

### M2R4 Decisions (5)

**DM1: Governance Document Centralization + Document Control**
- [ ] Centralize to evaluator/docs (master) + @-include imports for other practices (document control: git-based versioning + automated sync via CI/CD)
- [ ] Move to shared foundation location (if so, where? + document control method?)
- [ ] Keep distributed with explicit sync (if so, sync mechanism? + how to prevent stale copies in humanaios?)
- [ ] Hybrid approach (specify: which docs centralized vs distributed, document control per category?)

**DM2: Z3_PROTOCOL Ownership**
- [ ] Local (clarify intended locations)
- [ ] Upstream (clarify import path)
- [ ] Hybrid (some practices local, some upstream)

**DM3: Path Reference Convention**
- [ ] Standardize @docs/ (all practices have local copies)
- [ ] Standardize @../docs/ (establish shared parent)
- [ ] Mixed (specify per-practice rules)

**DM4: Practice Charters**
- [ ] All practices should have CHARTER.md
- [ ] Autonomy-specific only
- [ ] Optional per-practice

**DM5: Field Ordering Rule**
- [ ] Enforce alphabetical (within sections)
- [ ] Keep implicit grouping (current approach)
- [ ] Custom rule (specify)

### Integration Design Approvals (3)

**IA1: ACAT API as Public Mesh Service**
- [ ] Approved — proceed with Phase 1 operator implementation
- [ ] Approved with modifications (specify)
- [ ] Hold for further investigation

**IA2: Hybrid Organizational Model (humanaios practice + HumanAIOS LLC)**
- [ ] Approved — proceed with practice setup
- [ ] Approved with modifications (specify)
- [ ] Hold for further investigation

**IA3: ACAT as Calibration Signal Source**
- [ ] Approved — proceed with dimensional mapping validation
- [ ] Approved with modifications (specify)
- [ ] Hold for further investigation

---

## EVIDENCE & ARTIFACTS

**M2 Audit Artifacts (Empirica IDs):**
- Finding: M2R2-R3 complete (483498b6...)
- Finding: project.yaml field ordering (88922013...)
- Finding: Governance distribution gap (c9055c84...)
- Finding: CLAUDE.md variants (be676589...)
- Finding: config.yaml consistency (3e628fec...)
- Unknown: Governance centralization (baee5ce6...)
- Unknown: Z3_PROTOCOL (01b68038...)
- Unknown: Path convention (3bc75675...)
- Decision: M2 audit priority (a56f9947...)

**Integration Planning Artifacts (Empirica IDs):**
- Finding: Hybrid model viable (617bb719...)
- Finding: ACAT as mesh service (7c26dff3...)
- Finding: Dimensional mapping (8d133919...)
- Finding: Rollout plan (ce95190d...)
- Decision: ACAT API public (ac49c621...)
- Decision: Hybrid org model (2477bfc9...)
- Decision: ACAT signal source (f9ceadb2...)
- Unknown: Dimensional mapping detail (76bb28fa...)
- Unknown: Convergence thresholds (41d4039b...)
- Unknown: M2R4 implications (18a941e4...)
- Assumption: API versioning (bdc43d00...)
- Assumption: P-ANON compatible (d0c1ae50...)

**Documentation:**
- M2_RANK4_SCHEMA_DISCOVERY_REPORT.md (639 lines, full discovery)
- SCHEMA_DISCOVERY_SUMMARY.yaml (188 lines, structured summary)
- OPERATOR_INTEGRATION_PHASE1_SPEC.md (implementation guide for mesh-support + empirica-autonomy)

---

## NEXT STEPS

1. **Admiral reviews** this escalation document
2. **Admiral provides decisions** on 8 prompts (5 M2 + 3 integration)
3. **Phase 1 operator implementation** proceeds in parallel (doesn't wait for M2R4 Phase 2 decisions)
4. **M2R4 Phase 2 design** incorporates both M2 unknowns + integration-informed questions
5. **Monthly sync** between humanaios practice + foundation (research integration feedback loop)

---

**Status:** READY FOR ADMIRAL REVIEW  
**Prepared by:** empirica-foundation-evaluator  
**Date:** 2026-07-23
