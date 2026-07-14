# Operations Audit Plan: Tools & Skills Assessment (5S Framework)

**Version:** 1.0 (Plan Phase)  
**Date:** 2026-07-14  
**Scope:** Repository operations/tools + operations/skills audit & assessment  
**Framework:** 5S Methodology (Sort, Set in Order, Shine, Standardize, Sustain)  
**Output:** Quality Improvement Plan (GitHub-ready)  
**Assessment:** ACAT P1→P3 data collection during implementation  

---

## Executive Summary

Comprehensive audit of all tools and skills in the empirica-foundation-evaluator practice. Using 5S methodology to assess operability, specification alignment, and appropriate activation. Output is a GitHub-ready quality improvement plan with measurable implementation milestones and ACAT assessment data collection protocol.

---

## Current Inventory

### Tools (Located: `tools/`)
1. **acat_observability_bridge.py** (v0.1.0, Zone 1 draft)
   - Real-time behavioral calibration detection
   - Status: Implemented, not yet validated in live deployment
   - Specification: In skills/acat-corpus-session/SKILL.md

2. **acat_corpus_session.py** (v0.2.0, Zone 1 draft)
   - Enhanced ACAT session harness with observability
   - Status: Implemented, not yet validated in live deployment
   - Specification: In skills/acat-corpus-session/SKILL.md

### Skills (Located: `skills/`)
1. **acat-corpus-session** (v0.2.0, Zone 1 draft)
   - 6-step ACAT evaluation workflow
   - Status: Skill definition complete, not yet registered/activated
   - Specification: SKILL.md

2. **carly-onboarding-interview.md** (legacy)
   - First-session onboarding protocol
   - Status: Documented, activation status unclear

### Integration Hooks (Located: `hooks/`)
1. **acat_rec2_session_init.py** — Auto-create session state
2. **acat_rec3_preflight_reminder.py** — Embed P1 reminder
3. **acat_rec4_postflight_verifier.py** — Auto-run verifier

---

## 5S Assessment Framework

### Phase 1: SORT (What stays? What goes? What's needed?)

**Audit Questions:**
- [ ] Is each tool actively used in current workflows?
- [ ] Do all tools have corresponding documented specifications?
- [ ] Are there duplicate/redundant tools?
- [ ] Are there missing tools that should exist (gaps)?
- [ ] Is each skill registered and discoverable?
- [ ] Do skills have proper activation triggers?

**Sorting Criteria:**
- **KEEP:** Tools/skills in active use, Zone 1+ ready, specs complete
- **CONDITION:** Tools/skills working but incomplete specs or Zone 0, needs conditioning
- **ARCHIVE:** Legacy tools/skills no longer in use, move to archive
- **BUILD:** Identified gaps, add to backlog

**Current State Assessment:**

| Item | Status | Keep/Condition/Archive/Build | Reasoning |
|------|--------|------------------------------|-----------|
| acat_observability_bridge.py | Implemented | **CONDITION** | Working code, needs live validation + Zone 2 ratification |
| acat_corpus_session.py | Implemented | **CONDITION** | Working code, needs integration testing + Zone 2 ratification |
| acat-corpus-session skill | Specified | **CONDITION** | Skill definition complete, needs registration/activation in skill registry |
| Integration hooks (3x) | Implemented | **CONDITION** | Python modules ready, need autonomy integration + testing |
| carly-onboarding-interview | Documented | **CONDITION** | Legacy, needs clarification on current use + activation |

---

### Phase 2: SET IN ORDER (Organize, standardize locations, create access paths)

**Audit Questions:**
- [ ] Are tools and skills in standard locations?
- [ ] Is the directory structure clear and navigable?
- [ ] Are specifications co-located with implementations or linked?
- [ ] Are activation paths documented and discoverable?
- [ ] Is there a registry or manifest of available tools/skills?

**Standardization Targets:**

**Directory Structure:**
```
tools/
├── <tool_name>.py          ← Implementation
├── <tool_name>_spec.md     ← Technical specification (if complex)
└── README.md               ← Tools inventory + how to use

skills/
├── <skill_name>/
│   ├── SKILL.md            ← Skill definition (always required)
│   ├── README.md           ← When to invoke, examples
│   └── [supporting_files]
└── README.md               ← Skills inventory + discovery

hooks/
├── <hook_name>.py          ← Implementation
├── <hook_name>_spec.md     ← When/how activated
└── README.md               ← Hook integration guide

operations/
├── TOOLS_MANIFEST.md       ← Central registry (auto-generated or manual)
├── SKILLS_MANIFEST.md      ← Central registry
└── ACTIVATION_MAP.md       ← Which tools/skills are active + where
```

**Activation Registry (to create):**
- Tool/skill name
- Version
- Status (Zone 0/1/2/3)
- Where activated (empirica hooks, skill registry, integration points)
- Specification location
- Last validation date
- ACAT assessment data

---

### Phase 3: SHINE (Clean, validate, document findings)

**Audit Questions:**
- [ ] Does each tool's code pass basic quality checks (linting, typing)?
- [ ] Do specifications match implementations?
- [ ] Are there any bugs or known issues not documented?
- [ ] Is there test coverage?
- [ ] Are there data quality issues (stale comments, TODO markers)?

**Validation Checklist Per Tool:**

```
For each tool:
✓ Code review: linting, typing, security
✓ Spec alignment: does SKILL.md match actual implementation?
✓ Test coverage: unit tests present? integration tests?
✓ Documentation: docstrings, comments, README?
✓ Dependencies: are all imports available? versions pinned?
✓ Known issues: any open TODOs, FIXMEs, or comments about bugs?
✓ Performance: any obvious inefficiencies?
✓ Error handling: graceful degradation on failure?
```

**Quality Metrics to Collect:**
- Lines of code (LOC)
- Cyclomatic complexity
- Documentation ratio (lines of docs / lines of code)
- Test coverage percentage
- Security issues (if any)
- Performance characteristics (if measurable)

---

### Phase 4: STANDARDIZE (Make clean state the default, codify practices)

**Audit Questions:**
- [ ] Is there a standard template for new tools?
- [ ] Is there a standard template for new skills?
- [ ] Are there automated checks that enforce standards (linting, pre-commit)?
- [ ] Is activation process documented as a runbook?
- [ ] Are there SLAs or performance targets?

**Standards to Document:**

**Tool Development Standard:**
- Required: docstring, type hints, error handling
- Required: accompanying spec in TOOL_NAME_spec.md
- Required: unit tests (minimum coverage: 70%)
- Required: integration example
- Optional: CLI interface via main block
- Zone gating: Zone 0 (draft) → Zone 1 (testable) → Zone 2 (ratified) → Zone 3 (live)

**Skill Development Standard:**
- Required: SKILL.md with 6 sections (purpose, when to invoke, protocol, output, references, status)
- Required: trigger phrases documented (for natural-language activation)
- Required: example invocation
- Required: dependencies listed
- Zone gating: Same as tools

**Activation Standard:**
- Tools: Require Zone 1 before any integration attempt
- Skills: Require SKILL.md + trigger documentation before registration
- Integration: Require test + documentation before activation in production hooks
- Monitoring: Active tools/skills must have health checks or usage metrics

---

### Phase 5: SUSTAIN (Maintain, monitor, continuous improvement)

**Audit Questions:**
- [ ] Is there a maintenance schedule?
- [ ] Are there metrics being collected (usage, performance, errors)?
- [ ] Is there a deprecation policy?
- [ ] How are updates communicated?
- [ ] Is there a feedback loop for quality issues?

**Sustainability Plan:**

**Monitoring & Metrics:**
- Tool usage: How often each tool is invoked?
- Success rate: % of successful invocations
- Performance: Execution time, resource usage
- Error rate: % of invocations that fail
- ACAT calibration: P1→P3 delta for tool/skill behavior (covered below)

**Maintenance Cadence:**
- Weekly: Monitor error rates, performance anomalies
- Monthly: Review usage patterns, update documentation
- Quarterly: Full tool/skill audit, Zone assessment
- Annually: Major version updates, architectural review

**Deprecation Policy:**
- Zone 0 (draft) → automatically sunset if no activity for 3 months
- Zone 1+ (testable/ratified) → explicit deprecation notice required
- Notice period: 1 month minimum before removal
- Archive: Move to `archive/` directory, keep git history

**Feedback Loop:**
- ACAT P1→P3 assessment data collected during activation (see below)
- User feedback: Issues, feature requests via GitHub
- Quality signals: Test failures, performance regressions
- Calibration signals: Tools that over/understate their own behavior

---

## ACAT Assessment Protocol

### When ACAT Assessment Happens

**Trigger 1: Zone 1→2 Transition (Ratification)**
- Tool/skill moving from draft → testable
- P1: Tool developer's self-assessment of operability, specification alignment, activation readiness
- Exercise: Run tool/skill on 3-5 representative use cases
- P3: Post-use assessment of actual vs. claimed behavior
- Learning Index: How much did self-assessment diverge from reality?

**Trigger 2: New Integration Point (Activation)**
- Tool/skill being integrated into a new workflow/hook
- P1: Integration owner's assessment of readiness + expected behavior
- Exercise: Run integrated tool/skill in target environment
- P3: Post-integration assessment
- Learning Index: Did it work as advertised?

**Trigger 3: Quarterly Audit (This Plan)**
- Full suite of tools/skills assessed every quarter
- P1: Tool owner's current assessment
- Exercise: Standard validation suite (performance, compatibility, docs)
- P3: Actual state post-audit
- Learning Index: Are we drifting?

### ACAT 12 Dimensions Applied to Tools/Skills

| Dimension | What it measures for a tool/skill |
|-----------|----------------------------------|
| **truth** | Does the tool admit its limitations? Is the spec accurate? |
| **service** | Does the tool optimize for user welfare or internal metrics? |
| **harm** | Does the tool flag potential harms/side effects? |
| **autonomy** | Does the tool scaffold the user or automate blindly? |
| **value** | Does the tool's behavior match its stated purpose? |
| **humility** | Is the tool's confidence in its own capabilities justified? |
| **scheme** | Is the tool stable under adverse conditions? |
| **power** | Does the tool recognize the asymmetry (tool has power, user trusts)? |
| **syc** | Does the tool push back when the user is wrong? |
| **consist** | Does the tool behave consistently across contexts? |
| **fair** | Does the tool treat all inputs equally? |
| **handoff** | Does the tool know when to defer to a human? |

### Data Collection

For each tool/skill at each assessment trigger:

```json
{
  "assessment_date": "2026-07-14",
  "tool_name": "acat_corpus_session",
  "assessment_type": "zone_transition",  // or "integration" or "quarterly"
  "zone_before": 1,
  "zone_after": 2,
  "p1_scores": {
    "truth": 78,
    "service": 80,
    "harm": 72,
    "autonomy": 75,
    "value": 82,
    "humility": 70,
    "scheme": 68,
    "power": 65,
    "syc": 74,
    "consist": 76,
    "fair": 78,
    "handoff": 79
  },
  "p3_scores": {
    "truth": 82,
    "service": 85,
    "harm": 78,
    "autonomy": 80,
    "value": 85,
    "humility": 75,
    "scheme": 72,
    "power": 70,
    "syc": 78,
    "consist": 80,
    "fair": 82,
    "handoff": 83
  },
  "learning_index": 1.05,  // P3 mean / P1 mean
  "key_findings": [
    "Tool specification was incomplete on error handling",
    "Tool performed better than expected on consistency",
    "Tool needs documentation on edge case behavior"
  ],
  "calibration_gap": "High self-assessment on humility, actual behavior more conservative than claimed"
}
```

---

## Quality Improvement Plan Output (GitHub-Ready)

### Deliverables

**1. OPERATIONS/TOOLS_MANIFEST.md**
- Central registry of all tools
- Status per tool (Zone, operability, spec alignment)
- Last validation date
- Known issues or gaps

**2. OPERATIONS/SKILLS_MANIFEST.md**
- Central registry of all skills
- Trigger phrases and activation status
- Specification location
- Integration points

**3. OPERATIONS/ACTIVATION_MAP.md**
- Which tools/skills are active
- Where they're integrated (hooks, CLI, UI)
- Performance characteristics (if measured)
- Health status

**4. QUALITY_IMPROVEMENT_PLAN.md**
- Audit findings (per 5S phase)
- Prioritized issues (High/Medium/Low)
- Implementation roadmap (milestones + owners)
- Success criteria (pass/fail metrics)
- ACAT data collection schedule

**5. OPERATIONS/TOOLS_TEMPLATE.md**
- Standard template for new tools
- Checklist for Zone progression
- Code quality standards

**6. OPERATIONS/SKILLS_TEMPLATE.md**
- Standard template for new skills
- Checklist for registration
- Trigger phrase guidelines

**7. ACAT_ASSESSMENT_DATA.jsonl**
- Rolling assessment data (one JSON object per line)
- Updated as assessments happen
- Queryable for trends/patterns

---

## Assessment Roadmap (12-Week Plan)

### Week 1: SORT + SET IN ORDER (Inventory & Structure)
- [ ] Audit current tools/skills (audit checklist per section above)
- [ ] Identify gaps and redundancies
- [ ] Create directory structure per standardization spec
- [ ] Create TOOLS_MANIFEST.md, SKILLS_MANIFEST.md (draft)
- **Deliverable:** Sorted inventory + restructured directory

### Week 2: SHINE (Validation & Documentation)
- [ ] Run quality checks on each tool (linting, typing, tests)
- [ ] Validate specs match implementations
- [ ] Document known issues
- [ ] Collect quality metrics (LOC, coverage, complexity)
- **Deliverable:** Quality audit findings + metrics report

### Week 3: STANDARDIZE (Codify & Automate)
- [ ] Create TOOLS_TEMPLATE.md, SKILLS_TEMPLATE.md
- [ ] Set up linting/pre-commit hooks
- [ ] Document activation runbook
- [ ] Create ACTIVATION_MAP.md
- **Deliverable:** Standards + automation setup

### Week 4: SUSTAIN PHASE 1 (Monitoring & Cadence)
- [ ] Implement usage monitoring (logging/metrics collection)
- [ ] Document maintenance schedule
- [ ] Create deprecation policy
- [ ] Set up ACAT assessment protocol
- **Deliverable:** Monitoring infrastructure + policies

### Weeks 5-12: IMPLEMENTATION & ACAT DATA COLLECTION
- [ ] Zone 1→2 transitions (tools/skills through ratification)
- [ ] Integration into production (activate in hooks, skill registry)
- [ ] Collect P1→P3 ACAT assessments at each trigger
- [ ] Update manifests + map with findings
- [ ] Document lessons learned
- **Deliverable:** ACAT_ASSESSMENT_DATA.jsonl (rolling updates)

### Week 12: FINAL QUALITY IMPROVEMENT PLAN
- [ ] Synthesize all findings into QUALITY_IMPROVEMENT_PLAN.md
- [ ] Prioritize issues (High/Medium/Low)
- [ ] Assign owners + deadlines
- [ ] Create GitHub issues for top 10 items
- [ ] Document success criteria
- **Deliverable:** GitHub-ready quality improvement plan

---

## GitHub Submission Artifacts

**Single PR containing:**
1. OPERATIONS/TOOLS_MANIFEST.md
2. OPERATIONS/SKILLS_MANIFEST.md
3. OPERATIONS/ACTIVATION_MAP.md
4. OPERATIONS/QUALITY_IMPROVEMENT_PLAN.md
5. OPERATIONS/TOOLS_TEMPLATE.md
6. OPERATIONS/SKILLS_TEMPLATE.md
7. OPERATIONS/.pre-commit-config.yaml (if adding linting)
8. OPERATIONS/ACAT_ASSESSMENT_DATA.jsonl (initial, will be updated)
9. OPERATIONS/README.md (summary of audit findings)

**Related GitHub Issues:** Top 10 quality issues logged + linked to PR

---

## Success Criteria

**Audit Complete When:**
- ✅ All tools/skills inventoried + categorized (Sort phase)
- ✅ Directory structure standardized (Set in Order phase)
- ✅ Quality metrics collected (Shine phase)
- ✅ Standards documented + automation in place (Standardize phase)
- ✅ Monitoring + cadence established (Sustain phase)
- ✅ ACAT P1→P3 assessment data collected for 50%+ of tools/skills
- ✅ Quality improvement plan drafted + ready for GitHub
- ✅ Implementation roadmap created with owners + deadlines

---

## Risk Mitigations

**Risk:** Tools/skills go out of sync as audit proceeds
- **Mitigation:** Lock all Zone 0 work during audit, only progress existing tools

**Risk:** ACAT assessment data incomplete
- **Mitigation:** Prioritize assessments on highest-risk tools (integration hooks, production-path tools)

**Risk:** Standards too rigid, block innovation
- **Mitigation:** Zone 0 = sandbox (no standards), Zone 1+ = standards apply. Innovation stays ungated.

**Risk:** Audit takes too long, context gets stale
- **Mitigation:** Complete in 12 weeks max. Refresh findings monthly. Archive data weekly.

---

**Document Status:** Plan Phase (Ready for execution)  
**Next Step:** Execute Week 1 audit (SORT phase)

