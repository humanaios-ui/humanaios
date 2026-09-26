# Practice Specification Template — Adoption Guidance Script

**Author:** empirica-foundation-evaluator  
**Version:** 1.0  
**Date:** 2026-08-14  
**Status:** Guidance for Phase 1 Adoption (Aug 12-25)  
**Audience:** All foundation practices (autonomy, humanaios, outreach, website, empirica-mesh-support)

---

## Overview: What is a Practice Specification?

A **Practice Specification** is a formal governance document that defines:
- **What your practice does** — mission, scope, domains owned
- **Who you serve** — internal/external contacts and engagement types
- **How you work with others** — interfaces, contracts, SLAs, consumption patterns
- **What you measure** — behavioral assessment scope, regulatory context
- **When you deliver** — phase timeline, success criteria, critical unknowns
- **Who decides** — authority boundaries, escalation paths

**Why it matters:**
- **Clarity:** Every contact, every practitioner knows who owns what decisions
- **Scalability:** Governance rules are explicit, not tribal knowledge
- **Auditability:** When questions arise, the spec is the source of truth
- **Mesh coordination:** Practices understand dependencies and SLAs with each other

---

## Structure: What Goes in Each Section

### 1. **Practice Metadata** (5 min to fill)
```yaml
practice:
  ai_id: empirica-<name>              # canonical AI id (kept from project name)
  human_name: "..."                   # human-readable practice name
  mission: "..."                      # one-sentence mission (why does this practice exist?)
  canonical_seat: "empirica-foundation.carly.<name>"  # full 3-form mesh address
  org_id: "empirica-foundation"       # your org
  tenant: "carly"                     # your tenant
```

**Quick questions to answer:**
- What is your practice called? (e.g., "autonomy", "humanaios")
- Why does it exist? (mission — keep to 1-2 sentences)
- Who/what do you serve? (list 2-3 contact types or engagement areas)

**Common mistakes:**
- ❌ Mission too long or too vague ("we do lots of things")
- ✓ Mission is specific ("Coordinate behavioral calibration measurement across foundation practices")

---

### 2. **Serves** — Contacts & Engagement Types (10 min)
```yaml
serves:
  contacts:
    - type: organization
      id: empirica-foundation
      relationship: internal-platform
  engagement_types:
    - behavioral-assessment
    - research-publication
    - mesh-coordination
    - infrastructure-support
```

**What to fill in:**
- **contacts:** Who do you interact with? (internal org, external stakeholders, other practices)
- **engagement_types:** What kinds of work? (behavioral assessment, infrastructure, comms, etc.)

**Guiding questions:**
- Do you serve internal practices only, or also external stakeholders?
- What are 3-4 types of work you do for these contacts?

---

### 3. **Owns** — Domains & Scope (15 min)
```yaml
owns:
  domains:
    - "Domain 1: what this practice owns"
    - "Domain 2: what this practice owns"
    - "Domain 3: ..."
  
  out_of_scope:
    - "What someone else owns (mention who)"
    - "What is explicitly NOT this practice's responsibility"
```

**Critical:** Be explicit about what you DON'T own. This prevents "everyone's responsible" confusion.

**Example (from outreach):**
```
domains:
  - "Stakeholder communication & feedback collection"
  - "Publication roadmap & regulatory timeline coordination"
  
out_of_scope:
  - "Core ACAT instrument development (humanaios owns)"
  - "Practice specification adoption (mesh-support owns)"
```

**Red flag:** If your "owns" section is vague (e.g., "support practices") or your "out_of_scope" is empty, spend time here.

---

### 4. **Presents** — Interfaces & Contracts (20-30 min)
This is the meat of the spec. For each interface (interface = a thing you offer), define:

```yaml
presents:
  interfaces:
    - name: "behavioral_assessment"
      capability: ["what you do", "list of concrete capabilities"]
      contracts:
        - name: "contract_name"
          input: "what caller provides (field, field, field)"
          output: "what you return (field, field, field)"
          sla_response: "how fast you acknowledge (4 hours, 2 hours, 30 min)"
          sla_resolution: "how fast you finish (same day, 2 business days)"
          rationale: "WHY these SLAs? (mesh cadence? technical constraint? upstream dependency?)"
```

**For each contract, ask:**
- **Input:** What does the caller need to provide? (be specific: "stakeholder_name, contact_method, timeline")
- **Output:** What do they get back? (be specific: "engagement_status, scheduled_date, feedback_summary")
- **SLA response:** How fast do you acknowledge receipt? (4 hours? 30 min? same business day?)
- **SLA resolution:** How fast do you finish the work? (same day? 2 weeks?)
- **Rationale:** Why these numbers? (tied to mesh sync cadence? upstream dependency? physical constraint?)

**Worked example:**
```yaml
- name: "investigatation_request"
  input: "research_question, scope, urgency_level, deadline"
  output: "investigation_findings, confidence_score, data_sources"
  sla_response: "2 hours"
  sla_resolution: "3 business days"
  rationale: "Mesh syncs daily; urgent questions need fast triage. Investigations typically take 2-3 days given upstream dependencies on autonomy phase status."
```

**Mesh-support will ask:** Are these SLAs realistic? Do you have dependencies you can't meet them without?

---

### 5. **Consumes** — What You Need from Others (15 min)
```yaml
consumes:
  from:
    - empirica-autonomy:
        - "data or service A"
        - "data or service B"
      when_to_call:
        - "Call autonomy when..."
        - "Call autonomy when..."
      when_to_decline:
        - "Decline: send to them directly if..."
    
    - empirica-mesh-support:
        - "service A"
      when_to_call:
        - "Call when..."
      when_to_decline:
        - "..."
```

**For each practice you consume from:**
- **What do you need?** (concrete: "validated behavioral findings", not "support")
- **When do you ask them?** (specific scenarios)
- **When do you route the caller directly to them?** (practices should know "I'll call mesh-support" vs "go ask them yourself")

**Why this matters:** Mesh-support uses this to understand the coordination graph. If every practice calls every other practice, the mesh gets bottlenecked.

---

### 6. **Behavioral Assessment** — How You Measure (15 min)
```yaml
behavioral_assessment:
  work_type: "code"                   # type of work (code, research, comms, design, ops, etc.)
  calibration_model: "shared_reference_standard_v1"  # which model?
  measurement_uncertainty: "published_per_round"     # how transparent?
  substrate_tracking: true            # do you track which LLM / tool version?
  grader_version_tracked: true        # do you track grader version over time?
  quarterly_rounds: true              # measurement cadence
  measurement_frequency: "quarterly_rounds"
  baseline_grader_version: "Claude Haiku 4.5"  # for what grader?
  
  assessment_scope:
    - "What you measure: (Dimension A)"
    - "What you measure: (Dimension B)"
  
  measurement_anchor:
    - "How you ground it in reality (ground truth, mechanical verification, external validation, etc.)"
```

**Questions to answer:**
- What type of work does your practice do? (affects measurement model)
- What dimensions are you measured on? (e.g., "code correctness", "response time", "clarity of output")
- How do you know if you're doing it right? (what is ground truth?)

---

### 7. **Regulatory Context** (10-15 min)
If your practice intersects with regulatory requirements, document them:

```yaml
regulatory_context:
  frameworks:
    - name: "EU AI Act"
      scope: "binding, enforcement Aug 2026+"
      relevance: "how does this affect your practice?"
    - name: "prEN 18229-1"
      scope: "Logging, Transparency, Human Oversight"
      relevance: "..."
  
  integrated_approach: "How do you satisfy all frameworks at once?"
  publication_gates: 
    - "deadline 1"
    - "deadline 2"
```

**If you don't have regulatory constraints:** you can skip this or mark it "not applicable".

---

### 8. **Dependencies** — Practices You Depend On (10 min)
```yaml
dependencies:
  - practice: "empirica-autonomy"
    reason: "their Phase 1 baseline gates our publication timeline"
    constraint: "we cannot ship before they complete"
  - practice: "humanaios"
    reason: "their behavioral findings inform our assessment scope"
    constraint: "we need their latest corpus state quarterly"
```

**For each dependency:**
- **Which practice?** (name it exactly)
- **Why do you depend on them?** (specific, not generic)
- **What's the constraint?** (hard gate? soft coordination? data input?)

**Mesh-support uses this to:** detect circular dependencies, understand critical path items, schedule syncs.

---

### 9. **Phase Timeline** — Your Adoption Phases (15 min)
```yaml
phase_timeline:
  phase_1_specification:
    start: "2026-08-12"
    end: "2026-08-25"
    activity: "Complete practice specification template"
    success_criteria:
      - "practice-spec reviewed and approved by mesh-support (30-min interview)"
      - "All critical unknowns addressed or escalated"
      - "Interface contracts reviewed for SLA feasibility"
      - "Dependencies confirmed with upstream practices"
  
  phase_2_review:
    start: "2026-08-26"
    end: "2026-09-20"
    activity: "Refinement with mesh-support + Admiral feedback"
    success_criteria:
      - "All feedback from Phase 1 interview addressed"
      - "Any escalations resolved"
  
  phase_3_ratification:
    start: "2026-09-21"
    end: "2026-09-30"
    activity: "Admiral ratification + publication"
    success_criteria:
      - "Admiral approves practice-spec as conformant"
      - "Spec published in System Specification Charter"
```

**All practices follow the same timeline:**
- **Phase 1 (Aug 12-25):** You draft, mesh-support reviews in 30-min interview
- **Phase 2 (Aug 26-Sep 20):** Roundtrip feedback, refinement
- **Phase 3 (Sep 21-30):** Admiral ratification, publication

---

### 10. **Critical Unknowns** — What You're Still Figuring Out (10 min)
```yaml
critical_unknowns:
  - "Unknown A (what specifically is still unclear?)"
  - "Unknown B (where is the uncertainty?)"
  - "Unknown C (what decision is blocking this?)"
```

**Be honest.** The spec is a starting point, not a final declaration. If you're unsure:
- About dependencies, say so.
- About SLAs, say so.
- About scope boundaries, say so.

Mesh-support will help you resolve these in the Phase 1 interview.

---

### 11. **Regulatory Deadlines & Next Actions** (5-10 min)
If your practice has hard deadlines, list them:
```yaml
regulatory_deadlines:
  - "Deadline A (specific date, enforcement body)"
  - "Deadline B (..."

next_actions:
  - "By tomorrow: ..."
  - "By next week: ..."
  - "By Phase 1 end (Aug 25): ..."
```

---

## The Interview Process (30 min with mesh-support)

**When:** 2026-08-12 to 2026-08-25 (you pick a slot)  
**Who:** You + mesh-support  
**Format:** Async video or call (30 min)  
**Preparation:** Write down your practice-spec.yaml BEFORE the interview

### Interview Agenda (30 min)

1. **Scope clarity (5 min)** — "walk me through what your practice does in 60 seconds"
2. **Interface contracts (10 min)** — "are these SLAs realistic? any dependencies you can't meet without?"
3. **Critical unknowns (5 min)** — "let's triage what needs resolving vs what can wait"
4. **Phase timeline (5 min)** — "do your Phase 1/2/3 plans align with mesh coordination?"
5. **Escalations (5 min)** — "what needs Admiral sign-off?"

**mesh-support will provide written feedback:** within 48 hours, you'll get comments on:
- Scope clarity (is there ambiguity?)
- Dependency conflicts (circular? missing?)
- SLA feasibility (realistic given mesh cadence?)
- Regulatory alignment (any compliance gaps?)
- Phase timeline (do the dates work?)

### After the Interview (Phase 2)

You iterate on feedback (Aug 26-Sep 20), then Admiral ratifies (Sep 21-30).

---

## Worked Example: Practice Specification for Evaluator Seat

See `EVALUATOR_PRACTICE_SPEC.yaml` in this directory. It shows a complete, filled-in practice spec for the evaluator seat.

**Read it to see:**
- How mission statements are worded
- How scope domains are structured (what to include, what to exclude)
- How interface contracts specify input/output/SLAs/rationale
- How critical unknowns are phrased
- How regulatory context is integrated
- How dependencies are listed

Use it as a **template for what to aim for**, not as a copy-paste model. Your practice's spec will be different.

---

## Quick Checklist Before You Submit

- [ ] **Metadata complete?** (ai_id, mission, contacts, engagement types)
- [ ] **Scope clear?** (domains + explicit out-of-scope sections)
- [ ] **Interfaces concrete?** (input/output specific, not vague; SLAs with rationale)
- [ ] **Consumption patterns documented?** (which practices you call, when to route callers elsewhere)
- [ ] **Behavioral assessment scope stated?** (how do you measure success?)
- [ ] **Dependencies listed?** (which practices do you depend on? what's the constraint?)
- [ ] **Phase timeline reasonable?** (dates achievable?)
- [ ] **Critical unknowns logged?** (honest about what you're still figuring out?)
- [ ] **Regulatory context included (if applicable)?**

---

## FAQ

**Q: Do I have to fill in every section?**  
A: Yes, but if a section doesn't apply (e.g., regulatory context for a non-regulatory practice), mark it "not applicable" and briefly explain why.

**Q: What if I don't know my SLAs?**  
A: Make a best guess based on your mesh cadence (typically 4 hours for acknowledge, 1-2 business days for resolution). mesh-support will help you refine in the interview.

**Q: What if I'm uncertain about dependencies?**  
A: List them as critical unknowns. The Phase 1 interview is where you resolve uncertainty.

**Q: Can I change my spec after ratification?**  
A: Yes, but only with Admiral approval. The spec is your commitment to the foundation. Changes go through a minor-version update (v1.1, v1.2) and re-ratification.

**Q: What if my practice is new/small?**  
A: The spec still applies. Even small practices benefit from clarity. Keep your scope focused and honest about what you don't yet do.

---

## Next Steps

1. **Read the worked example** (`EVALUATOR_PRACTICE_SPEC.yaml`)
2. **Draft your practice-spec.yaml** (use the sections above as a guide)
3. **Schedule interview with mesh-support** (send them your draft + a 30-min time slot from Aug 12-25)
4. **Iterate on feedback** (Phase 2, Aug 26-Sep 20)
5. **Admiral ratification** (Phase 3, Sep 21-30)

---

**Questions?** Post in the governance adoption coordination channel (mesh-support is monitoring).

**Document Owner:** empirica-foundation-evaluator  
**Last Updated:** 2026-08-14  
**Next Review:** 2026-08-25 (Phase 1 completion)
