# Ollama + Claude Code Integration Plan
## Constitutional Alignment & Framework Development Acceleration

**Constitutional Basis:** §V (Mesh Discipline), §VI (Multi-Practice Coordination), §I (Phase-Aware Completion)  
**Status:** NOETIC PLANNING (Determining scope & feasibility before praxic commitment)  
**Scope:** Optional development tool for Framework Week 1-4, coordinated across 4 practices

---

## I. CONSTITUTIONAL ALIGNMENT

### §V Mesh Discipline Application

**Pull when uncertain** ✓
- Each practice (humanaios, autonomy, outreach, mesh-support) pulls Ollama capability rather than guessing locally
- Clear adoption path rather than hidden local experimentation

**Push when convergent** ✓
- Framework evaluator proposes Ollama adoption as optional tool
- Typed proposal with decision gates (ECO if required)
- Each practice decides independently

**Don't free-ride** ✓
- Ollama is complementary, not replacement for SER 2 observable linkage
- Production uses empirica grounding; Ollama for dev/testing only
- Clear separation: local ≠ production calibration dataset

**Mesh discipline is structural** ✓
- Practices that adopt Ollama accelerate development
- Practices that skip it still integrate normally
- No penalty, but discovery signal: who invested in velocity

### §VI Sustained Multi-Practice Coordination

This spans 2+ practices (humanaios, autonomy, mesh-support minimum) and outlives one session.

**Governance:** Optional tool adoption (non-ECO-gated)
- Each practice votes independently on Week 1 adoption
- Coordinated via shared OLLAMA_ADOPTION_AGREEMENT.md
- No binding commitment; opt-in per practice

**Authorization:** Human confirmation on framework (user approval)
- Evaluator proposes integration
- User confirms: worth pursuing? (Yes/No/Conditional)
- If Yes: document as recommended practice

---

## II. PHASE-AWARE COMPLETION (§I)

### Current Phase: NOETIC (Planning)

**Completion Criteria:**
- [ ] Understand Ollama's capabilities + constraints
- [ ] Map practice-specific use cases (4 practices × Week 1-4 phases)
- [ ] Identify risk/blockers (model quality, integration friction, cost trade-offs)
- [ ] Define success metrics for adoption
- [ ] Document adoption agreement + governance

**Next Phase Gate:** User confirmation → Proceed to praxic (implementation)

---

## III. PRACTICE-SPECIFIC INTEGRATION

### Practice 1: humanaios (ACAT CLI Development)

**Current Workflow:**
- Weeks 1-2: Build acat-score CLI against Anthropic API
- Cost: API tokens per development iteration
- Iteration speed: Limited by API latency + costs

**With Ollama:**
- Local CLI development using Qwen2.5-coder (32K context, tool calling)
- Deploy agentic reasoning for CLI design iterations
- Validate JSON output schema against ACAT_CLI_ASSESSMENT.md §VII

**Use Cases:**
1. **CLI Design Phase (Week 1):** Prototype command structure, argument parsing
2. **Implementation Phase (Week 1-2):** Code generation + multi-turn refinement
3. **Testing Phase (Week 2):** Local validation before integration test

**Adoption Decision:**
- [ ] Worth 5-min setup investment? (Ollama install + model pull)
- [ ] Gain: 3-5x iteration speed + zero API costs
- [ ] Risk: Model quality (Qwen2.5-coder vs Claude) — acceptable for dev?

**Integration Point:** Optional local harness (Week 1 kickoff)

---

### Practice 2: autonomy (F-50 Firewall Rule Design)

**Current Workflow:**
- Week 1: Design F-50 rules + SER 2 state transitions
- Approach: Manual reasoning + validation in SER context
- Cost: High-touch design + integration test coupling

**With Ollama:**
- Agentic reasoning for rule exploration (multi-turn dialogue)
- Test state machine transitions locally before SER 2
- Validate routing logic against framework constraints

**Use Cases:**
1. **Rule Exploration (Week 1):** Generate candidate rules via Qwen reasoning
2. **State Machine Design (Week 1):** Prototype transitions (open → in_progress → closed)
3. **Validation (Week 1):** Test rules against F-50 constraints locally

**Adoption Decision:**
- [ ] Worth design acceleration for complex state machine?
- [ ] Gain: Rapid rule iteration, early error detection
- [ ] Risk: Local validation ≠ live SER 2 validation (still need integration test)

**Integration Point:** Optional design harness (Week 1 kickoff)

---

### Practice 3: outreach (Phase 3 Pilot Coordination)

**Current Workflow:**
- Weeks 1-6: Standby on pilot role
- Week 7-10: Sessions assessed via live framework
- No local development needed

**With Ollama:**
- Optional: Prototype assessment workflows locally (Weeks 1-6)
- Test observable linkage patterns before live sessions
- Validate data model assumptions

**Use Cases:**
1. **Optional:** Pre-staging test sessions (understand framework before Week 7)
2. **Risk reduction:** Identify integration issues before Weeks 7-10

**Adoption Decision:**
- [ ] Worth early familiarization investment?
- [ ] Gain: Lower Week 7 surprises, faster ramp
- [ ] Risk: Minimal (opt-in, no critical path impact)

**Integration Point:** Optional (not on critical path)

---

### Practice 4: mesh-support (Escalation Logic Testing)

**Current Workflow:**
- Week 1: Configure escalation monitoring + data provenance tracking
- Approach: Live SER 2 testing + manual validation
- Risk: Logic errors surface during production SER 2 transitions

**With Ollama:**
- Test state machine transitions locally (4h escalation timer, escalation rules)
- Validate data provenance tracking logic before deployment
- Catch state-transition bugs before they affect live SER 2

**Use Cases:**
1. **Escalation Testing (Week 1):** Simulate timeout scenarios locally
2. **State Validation (Week 1):** Test state transitions (OPEN → IN_PROGRESS → BLOCKED → CLOSED)
3. **Data Provenance (Week 1):** Validate tracking logic pre-deployment

**Adoption Decision:**
- [ ] Worth pre-validating escalation logic locally?
- [ ] Gain: Early error detection, production stability
- [ ] Risk: Must still validate in live SER 2 context (not a replacement)

**Integration Point:** Optional infrastructure harness (Week 1 kickoff)

---

## IV. WEEK 1-4 TIMELINE

### Week 1: Setup + Parallel Development

**Monday (Day 1):**
- [ ] Confirm user approval: Ollama integration worth pursuing?
- [ ] Create OLLAMA_ADOPTION_AGREEMENT.md (voluntary, non-binding)
- [ ] Document optional setup for each practice

**Tuesday-Friday (Days 2-5):**
- humanaios: Ollama setup (if opted-in) → CLI design phase
- autonomy: Ollama setup (if opted-in) → F-50 rule prototyping
- mesh-support: Ollama setup (if opted-in) → Escalation logic testing
- outreach: Standby (opt-in for early familiarization only)

**Sync Point (Friday EOD):**
- Report: adoption rate + velocity gain estimates
- Any blockers surfaced?

### Week 2: Parallel Development + Integration

**humanaios:**
- CLI development continues locally (Ollama)
- Target: acat-score CLI deliverable (per EMPIRICA_ACAT_INTEGRATION_PLAN.md)
- Integration checkpoint: Does local Ollama development support on-time delivery?

**autonomy:**
- F-50 rules locally validated (Ollama) → ready for SER 2 integration
- Target: F-50 design finalized by Week 2 EOW
- Integration checkpoint: Are local rules production-ready?

**mesh-support + outreach:**
- Standby (or optional early staging)

### Week 3: Integration Readiness

**All practices:**
- Transition from local Ollama dev → SER 2 live integration
- Ollama remains available as optional reference/verification tool
- Production validation: observable linkage + F-50 firewall live (SER 2, not Ollama)

### Week 4: SER 2 Validation

**All practices:**
- SER 2 phase 1c validation: all deliverables tested
- No further Ollama development (optional for future iterations)

---

## V. GOVERNANCE GATES

### Gate 1: User Authorization (NOW)
**Question:** Is Ollama integration worth investigating for Week 1-4?
**Options:**
- ✅ Yes, proceed with planning
- ⚠️ Conditional (limit scope to specific practices)
- ❌ No, skip Ollama — stick with production-only empirica

**Result:** Informs whether we document adoption agreement

### Gate 2: Practice Adoption (Week 1, Day 1)
**Question:** Does each practice opt-in to Ollama?
- humanaios: Yes/No (impacts CLI delivery timeline?)
- autonomy: Yes/No (impacts F-50 rule readiness?)
- mesh-support: Yes/No (impacts escalation pre-validation?)
- outreach: Yes/No (impacts pilot preparation?)

**Result:** Determines which practices use local development harness

### Gate 3: Integration Checkpoint (Week 2, EOW)
**Question:** Is Ollama helping or hurting framework delivery?
- Metrics: Lines of code/iteration, bugs caught early, integration friction
- Decision: Continue optional adoption? Deprecate for specific practice? Recommend for future?

**Result:** Informs whether Ollama becomes recommended best practice

---

## VI. RISK ASSESSMENT

### Risk 1: Model Quality (Qwen2.5-coder vs Claude)
**Scenario:** Local Ollama development produces code that doesn't integrate well
**Mitigation:** 
- Ollama is dev-time only; production validation still required
- Each practice validates outputs before SER 2 integration
- Fallback: skip Ollama, use API-based development (slower but higher quality)

**Probability:** LOW (Qwen2.5-coder is production-grade for coding)
**Impact:** MEDIUM (dev rework if validation fails)

### Risk 2: Setup Friction
**Scenario:** Installing Ollama + pulling models takes time; doesn't pay off
**Mitigation:**
- Voluntary adoption (don't force practices)
- Document setup: 5 min for install, 2 min for model pull
- Early checkpoint (Week 1 Day 2) to surface friction

**Probability:** MEDIUM (environmental setup varies)
**Impact:** LOW (opt-in means practices bail early if friction too high)

### Risk 3: False Confidence
**Scenario:** Code passes local Ollama validation, fails in SER 2 production
**Mitigation:**
- Clear messaging: Ollama is optional dev tool, NOT production validator
- Every practice must validate outputs in actual SER 2 context
- Framework documentation emphasizes: local ≠ production

**Probability:** LOW (if discipline enforced)
**Impact:** HIGH (could delay Week 3 integration if not caught)

### Risk 4: Cost-Benefit Mismatch
**Scenario:** Setup overhead > velocity gain
**Mitigation:**
- Early feedback loop (Week 2 checkpoint)
- Deprecate if metrics show friction > benefit
- No sunk-cost: optional tool, easy to abandon

**Probability:** MEDIUM (depends on practice experience)
**Impact:** LOW (fallback is to skip Ollama entirely)

---

## VII. SUCCESS CRITERIA

### Noetic Phase (Planning — NOW)
- ✅ User confirms: worth pursuing
- ✅ Plan documents practice-specific use cases
- ✅ Risks + mitigations identified
- ✅ Governance gates defined

**Completion:** User approval + plan documented

### Praxic Phase (Implementation — Week 1-4)

**Adoption Metrics:**
- [ ] ≥2/4 practices opt-in to Ollama (feasibility signal)
- [ ] Setup time < 10 min per practice (friction threshold)
- [ ] No blockers surfaced Week 1 Day 2

**Development Metrics:**
- [ ] humanaios: CLI delivered on time (Week 2)
- [ ] autonomy: F-50 rules production-ready (Week 2)
- [ ] mesh-support: Escalation logic validated pre-SER 2
- [ ] No integration rework in Week 3 due to Ollama-dev drift

**Framework Metrics:**
- [ ] SER 2 Phase 1b integration succeeds (Week 3)
- [ ] Observable linkage live by Week 3 EOW
- [ ] F-50 firewall enforcement validated by Week 4

**Adoption Decision (Week 2):**
- Continue: Ollama became recommended practice
- Conditional: Recommended only for specific practices
- Deprecate: Frictionful; revert to API-only development

---

## VIII. IMPLEMENTATION APPROACH

### If User Approves: Create Adoption Agreement
**Step 1:** Document in OLLAMA_ADOPTION_AGREEMENT.md
- Voluntary, non-binding framework for Week 1-4
- Each practice commits independently
- Clear opt-out clause (no penalty)

**Step 2:** Create Practice-Specific Guides
- humanaios: OLLAMA_SETUP_CLI_DEVELOPER.md
- autonomy: OLLAMA_SETUP_INFRASTRUCTURE_DESIGNER.md
- mesh-support: OLLAMA_SETUP_ESCALATION_TESTER.md
- outreach: OLLAMA_SETUP_OPTIONAL_STAGING.md

**Step 3:** Integrate into SER 2 Week 1 Kickoff
- Optional: Practices install Ollama during Week 1 setup
- Not on critical path: skip if any friction detected
- Checkpoint: report adoption metrics Friday EOD

### Governance & Escalation
- **Non-blocking:** Ollama adoption is optional
- **Early feedback:** Week 1 Day 2 checkpoint surfaces issues
- **Weekly sync:** Week 2 checkpoint validates integration benefit
- **No sunk cost:** Easy to abandon if metrics show friction > benefit

---

## IX. CONSTITUTIONAL DISCIPLINE

### §V Mesh Discipline: Pull When Uncertain
**Applied:** Each practice pulls Ollama capability (via documented guide) rather than guessing locally
- Clear adoption path
- Voluntary (no free-ride)
- Shared learnings (Week 2 checkpoint)

### §VI Multi-Practice Coordination
**Applied:** Ollama adoption coordinated across 4 practices without ECO gate
- Voluntary agreement (non-binding)
- Independent decisions per practice
- Shared evaluation (Week 2 metrics)

### §I Phase-Aware Completion
**Applied:** Noetic phase = planning (understand before committing)
- User approval gate before praxic phase
- Success criteria defined per phase
- Integration checkpoint before proceeding to Week 3

---

## DECISION POINT

**Question for User:** Is investigating Ollama integration worth the planning effort?

**Option A: YES, PROCEED**
→ Create adoption agreement + practice guides
→ Practices opt-in Week 1 (voluntary)
→ Checkpoint Week 2 (metrics + integration benefit)
→ Recommend or deprecate based on data

**Option B: CONDITIONAL**
→ Limit to specific practices (e.g., humanaios + autonomy only)
→ Skip if setup friction signals early

**Option C: NO, SKIP**
→ Stick with empirica-only development (API-based)
→ No Ollama integration planning

**Recommendation:** Option A (YES)
- **Why:** Low-risk investigation (voluntary, opt-in, Week 2 checkpoint gates continuation)
- **Benefit:** Potential 3-5x dev velocity for humanaios + autonomy
- **Cost:** ~4 hours planning (now) + ~1 hour per practice setup (Week 1)
- **Fallback:** Abandon Week 2 if metrics show friction > benefit

---

**Status:** NOETIC PLANNING COMPLETE
**Next Action:** User confirmation → Praxic implementation (Week 1)
