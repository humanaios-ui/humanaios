---
title: Three New Practice Frameworks
subtitle: Practice Optimizer + Local Machine Optimizer + Educator Practice (16-Practice System)
date: 2026-08-14
version: 1.0-NEW-PRACTICES
status: Ready for ratification (adds 3 practices to 13-practice system)
---

# THREE NEW PRACTICE FRAMEWORKS

---

## PRACTICE 1: PRACTICE OPTIMIZER

**Mission:** Ensure all 13 existing practices are functioning optimally. Meta-level quality assurance.

### Definition

| Aspect | Description |
|--------|-------------|
| **Role** | Internal Quality Assurance + Practice Health Monitor |
| **Seat Type** | Specialist (like acat-x, collaborator-ops) |
| **Authority** | Audit + recommend (not veto). Make findings visible, let practices decide responses. |
| **Primary Client** | Operations Steward (mesh-support) + Evaluator + Night |
| **Function** | Continuous optimization of practice health, efficiency, and effectiveness |

### Core Functions

**Function 1: Practice Health Audits** (Ongoing)
- Weekly: Scan all 13 practices for health signals (SLA, goal completion, blocker accumulation)
- Monthly: Deep audit of 2-3 practices (rotate through all practices quarterly)
- Audit dimensions: Efficiency, capability maturity, team health, technical debt, risk exposure
- Output: Health scorecards per practice + recommendations

**Function 2: Cross-Practice Optimization** (Monthly)
- Identify patterns: "3 practices have the same bottleneck" → single solution?
- Share solutions: "Practice A solved problem X; practice B has same problem" → surface solution
- Standardize: Identify best practices in one practice → propose to others
- Output: Cross-practice pattern reports + solution transfers

**Function 3: Bottleneck Detection** (Weekly)
- Monitor: Are practices hitting constraints that cascade to other practices?
- Alert: Flag emerging bottlenecks BEFORE they become critical
- Collaborate: Work with Operations Steward to unblock
- Output: Bottleneck early warning system

**Function 4: Capability Assessment** (Quarterly)
- Assess: Does each practice have skills/tools/processes they need?
- Compare: Are capabilities distributed fairly or is one practice under-resourced?
- Recommend: What capability gaps need Resource Miner attention?
- Output: Quarterly capability gap reports

**Function 5: Practice Maturity Tracking** (Quarterly)
- Measure: Is each practice maturing (becoming more autonomous, effective, efficient)?
- Track: Maturity trajectory per practice
- Identify: Which practices need support, which are ready for expansion?
- Output: Maturity scorecard + growth recommendations

### Success Metrics

| Metric | Target | Why |
|--------|--------|-----|
| **Mean practice health score** | 0.85+ | Indicates healthy practices across board |
| **SLA compliance** | 95%+ practices meeting targets | Shows operational excellence |
| **Goal completion rate** | 60%+ per quarter | Shows execution capability |
| **Cross-practice solution transfers** | 2-4 per month | Shows knowledge sharing working |
| **Bottleneck resolution time** | <3 days from detection | Shows responsiveness |
| **Time-to-optimal** (new practice) | <8 weeks | Shows onboarding efficiency |

### Integration with Existing System

**Reports to:** Operations Steward (mesh-support) for operational issues, Evaluator for system patterns

**Receives data from:** All 13 practices (via audits), INDEX.yaml (trends), mesh communication logs (SLA data)

**Sends findings to:** Practices (recommendations), mesh-support (operational issues), evaluator (system patterns), Resource Miner (capability gaps)

**Doesn't overlap with:** Evaluator (Evaluator is observer/translator; Optimizer is actionable auditor). Evaluator sees system patterns across practices; Optimizer sees internal practice health.

### Resource Requirements

**Team:** 1 dedicated practice lead (part-time initially, full-time if scaled)
**Tools:** Audit framework, health tracking dashboard, maturity model
**Timeline:** Launch Sep 2026 (after practices stabilize with current system)

---

## PRACTICE 2: LOCAL MACHINE OPTIMIZER

**Mission:** Optimize Night's local machine while discovering how local OS architecture translates to system-level functions.

### Definition

| Aspect | Description |
|--------|-------------|
| **Role** | Infrastructure Optimization + System Architecture Discovery |
| **Seat Type** | Specialist (unique to this system) |
| **Authority** | Full OS-level access (with Night approval) to optimize local machine. Report findings on OS ↔ system parallels. |
| **Primary Client** | Night (direct) + Platform Custodian (humanaios) + mesh-support (infrastructure) |
| **Function** | Keep local infrastructure optimal while bridging local ↔ distributed architecture |

### Core Functions

**Function 1: Local Machine Optimization** (Continuous)
- Monitor: CPU, memory, disk, network performance
- Optimize: Resource allocation, cleanup, performance tuning
- Alert: If performance degrading, proactively fix
- Report: Weekly performance report + optimization changes made
- Output: Well-tuned local machine (Night's setup)

**Function 2: OS-to-System Architecture Discovery** (Ongoing Research)
- Investigate: How do OS concepts translate to system architecture?
  - Example: OS processes ↔ 13 practices (bounded contexts, communication)
  - Example: OS memory hierarchy ↔ system data layers (working memory, warm state, cold archive)
  - Example: OS scheduling ↔ Cortex mesh message routing (queue management, priority)
  - Example: OS buffer management ↔ resource buffering strategy (prevent bottleneck cascade)
- Document: Parallels discovered, lessons for system design
- Recommend: Apply OS principles to system architecture
- Output: "OS-to-System Architecture Discovery" quarterly research

**Function 3: Performance Monitoring & Bottleneck Detection** (Weekly)
- Track: Where is local performance bottleneck? (CPU? Memory? Disk? Network?)
- Compare: Is local bottleneck mirrored in system? (Theory of Constraints at both levels?)
- Alert: If bottleneck emerging, fix before it cascades
- Output: Performance dashboards + alerts

**Function 4: Security & Compliance** (Ongoing)
- Monitor: Is local machine secure? Patches updated? Data encrypted?
- Audit: Are practices' security requirements being met locally?
- Report: Security posture assessment
- Output: Security compliance report

**Function 5: Capacity Planning** (Quarterly)
- Assess: Is current machine adequate for current workload?
- Forecast: What machine capabilities needed in 6-12 months (more practices, more users, more data)?
- Recommend: When to upgrade hardware, storage, bandwidth
- Output: Capacity planning roadmap

### Success Metrics

| Metric | Target | Why |
|--------|--------|-----|
| **System uptime** | 99.9%+ | Local machine reliability |
| **Performance degradation** | <5% per quarter | Indicates good optimization |
| **OS-to-system parallels discovered** | 4-8 per quarter | Shows learning/bridging capability |
| **Optimization changes implemented** | 2-4 per month | Shows proactive improvement |
| **Security compliance** | 100% | No vulnerabilities or patches outstanding |
| **Architecture insights applied to system** | 1-2 per quarter | Shows practical value |

### Integration with Existing System

**Reports to:** Night (direct daily), Platform Custodian (architecture insights), mesh-support (infrastructure recommendations)

**Receives data from:** Local machine OS telemetry, system performance metrics (for comparison)

**Sends findings to:** Architecture team (OS parallels), mesh-support (infrastructure upgrades), Resource Miner (capacity planning costs)

**Doesn't overlap with:** Platform Custodian (Custodian owns HumanAIOS architecture; Optimizer owns local infrastructure + discovery)

### Resource Requirements

**Team:** 1 dedicated engineer (can be part-time initially)
**Tools:** OS monitoring tools, performance dashboards, architecture documentation
**Access:** Full local machine OS-level access (carefully scoped for security)
**Timeline:** Launch Sep 2026 (after security review)

### Security & Privacy Considerations

- **Scope:** Local machine only (Night's workstation), not 13-practice infrastructure
- **Access control:** Practice lead needs OS-level access (must be trusted, security-cleared)
- **Data handling:** Any data from local machine analysis must be encrypted, with audit trail
- **Governance:** Operations Steward must approve any OS-level changes before implementation

---

## PRACTICE 3: EDUCATOR PRACTICE

**Mission:** Recursive learning, epistemic management, question-generation, and knowledge organization using Johari Window framework.

### Definition

| Aspect | Description |
|--------|-------------|
| **Role** | Epistemic Manager + Learning Architect + Question Generator |
| **Seat Type** | Specialist (knowledge/learning focus) |
| **Authority** | Define learning curriculum, identify knowledge gaps, ask questions. Recommendations, not directives. |
| **Primary Client** | All practices + Evaluator + Night |
| **Function** | Manage what we know/don't know + ensure recursive learning drives improvement |

### Core Functions

**Function 1: Johari Window Organization** (Ongoing)
- **Known-Knowns:** What do we know we know? (Documented in findings, decisions, sources)
- **Known-Unknowns:** What do we know we don't know? (Logged in unknown-log, assumption-log)
- **Unknown-Knowns:** What do we know but haven't articulated? (Implicit knowledge, tacit expertise)
- **Unknown-Unknowns:** What don't we know we don't know? (Blindspots, black swans)

**Organize:**
- Sort all artifacts (findings, decisions, unknowns, assumptions) into Johari quadrants
- Make visible: Which quadrants are over/under-represented?
- Target: Expand known-knowns, shrink unknown-unknowns, articulate unknown-knowns
- Output: Quarterly Johari Window assessment

**Function 2: Recursive Learning Loops** (Continuous)
- Monitor: Are we learning from past decisions? Are predictions improving?
- Track: Decision feedback loops (predicted impact vs. actual) → calibration
- Identify: Patterns we keep discovering → should have been known earlier
- Recommend: How to turn feedback into learning (not just data)
- Output: Learning velocity metrics + recommendations

**Function 3: Question Generation** (Weekly)
- Ask: What are we NOT asking that we SHOULD be asking?
- Identify: Blindspots (unknown-unknowns) from patterns in known-knowns
- Propose: Research questions, investigation areas, hypothesis testing
- Challenge: Devil's advocate role — what assumptions are we making?
- Output: Weekly "Unasked Questions" report

**Function 4: Knowledge Curriculum Design** (Quarterly)
- Assess: What knowledge does each practice need to develop?
- Design: Learning roadmap (what to learn, in what order, by when)
- Identify: Knowledge gaps blocking progress
- Recommend: How to fill gaps (research, training, hiring, partnerships)
- Output: Quarterly knowledge curriculum + progress tracking

**Function 5: Cross-Practice Learning** (Monthly)
- Share: What did Practice A learn that Practice B should know?
- Document: Cross-practice insights, lessons, best practices
- Transfer: Ensure learning spreads, not hoarded
- Measure: Learning transfer rate (how many practices adopt learning from others?)
- Output: Cross-practice learning summaries

### Success Metrics

| Metric | Target | Why |
|--------|--------|-----|
| **Known-Knowns growth** | +20% per quarter | Expanding documented knowledge |
| **Unknown-Unknowns reduction** | -10% per quarter | Shrinking blindspots |
| **Decision prediction accuracy** | 85%+ (via feedback loops) | Learning from outcomes |
| **Questions generated per week** | 5-10 high-quality questions | Active epistemic challenge |
| **Learning transfer rate** | 60%+ (practices adopt cross-practice learning) | Knowledge flowing across system |
| **Recursive learning cycles** | 4+ per quarter | Active improvement loops |

### Integration with Existing System

**Reports to:** Evaluator (epistemic patterns), all practices (learning recommendations), Night (strategic knowledge gaps)

**Receives data from:** All artifact logs (findings, decisions, unknowns, assumptions), feedback loops (post-decision validation), decision archive (SEMANTIC_BRIDGE.yaml)

**Sends findings to:** Practices (learning recommendations), Resource Miner (knowledge gap → hiring/partnership), Strategic Lead (strategic learning priorities)

**Doesn't overlap with:** Evaluator (Evaluator translates patterns; Educator organizes knowledge). Evaluator is external observer; Educator is internal knowledge architect.

### Resource Requirements

**Team:** 1 dedicated practice lead (learning/epistemology background)
**Tools:** Johari Window dashboard, knowledge mapping tools, learning tracking system
**Timeline:** Launch Aug 2026 (can start immediately, lightweight)

### Johari Window Implementation

```
JOHARI WINDOW QUADRANTS:

                  Known to Self        Not Known to Self
Known to Others   _______________      _______________
                  | KNOWN-KNOWNS |    | BLIND SPOTS |
                  | (Open Area)   |    | (Unknown-   |
                  |               |    |  Unknowns)  |
                  |_______________|    |_____________|

Not Known to      _______________      _______________
Others            | HIDDEN AREA   |    | UNKNOWN-    |
                  | (Unknown-     |    | UNKNOWNS    |
                  |  Knowns)      |    | (Truly      |
                  |               |    |  Unknown)   |
                  |_______________|    |_____________|

TARGET: Expand Known-Knowns, Shrink Blind Spots & Unknown-Unknowns
MECHANISM: Find unknown-knowns → articulate → expand known-knowns
MEASUREMENT: Quarterly assessment of quadrant sizes + trends
```

---

## SYSTEM INTEGRATION: 13 + 3 = 16 PRACTICES

### Updated Practice Roster

**Empirica-Foundation Core (9):** autonomy, mesh-support, outreach, opportunity-aggregator, foundation-evaluator, **practice-optimizer**, **local-machine-optimizer**, **educator**, acat-x

**HumanAIOS Ecosystem (3):** humanaios, humanaios-internal, website

**Cross-Org Collaborators (4):** collaborator-ops, flta-app-empirica, grok-crossref, grok-crossref

### Updated Hierarchy

```
STRATEGIC LAYER (Night's direct reports):
├─ Strategic Lead (autonomy) → execution
├─ Operations Steward (mesh-support) → coordination
├─ Resource Weaver (outreach) → partnerships
├─ Platform Custodian (humanaios) → core platform
├─ Epistemic Observer (evaluator) → system patterns
├─ Resource Miner (opportunity-aggregator) → resource transactions

META/SPECIALIST LAYER (supporting strategic execution):
├─ Practice Optimizer → practice health + optimization
├─ Local Machine Optimizer → infrastructure + OS discovery
├─ Educator → knowledge + learning
├─ Research Lead (acat-x) → research + evaluation
└─ [Others: collaborator-ops, flta-app, grok-crossref, website, humanaios-internal]
```

### How Three New Practices Interact

**Practice Optimizer ↔ Evaluator:**
- Evaluator: "I see pattern X across practices"
- Optimizer: "Here's which practices have it, here's how to fix it"

**Educator ↔ Evaluator:**
- Evaluator: "System produced insight Y"
- Educator: "Let's articulate this as known-known + spread to other practices"

**Local Machine Optimizer ↔ Platform Custodian:**
- Local: "Found OS principle Z that applies to system"
- Custodian: "Let's apply to HumanAIOS architecture"

**All three ↔ Resource Miner:**
- Optimizer: "Practice gap X requires hiring"
- Educator: "Knowledge gap Y requires training/partnership"
- LocalOpt: "Capacity planning: need hardware upgrade in 6 months"
- Miner: "Allocating resources to fill gaps"

---

## IMPLEMENTATION TIMELINE

**Phase 1 (Aug 21 - Sep 4): Launch Educator**
- Start lightweight (1 person, part-time)
- Begin Johari Window organization of existing artifacts
- Generate first "Unasked Questions" report
- Cost: Low (minimal resources)

**Phase 2 (Sep 11 - Oct 2): Launch Practice Optimizer**
- Hire/assign practice lead
- Begin weekly practice health audits
- Start bottleneck detection
- Cost: Medium (dedicated resource)

**Phase 3 (Oct 9 - Nov 1): Launch Local Machine Optimizer**
- After security review + approval
- Begin local machine optimization
- Start OS-to-system discovery research
- Cost: Medium (infrastructure access + security overhead)

**By Nov 30:** All three practices operational, feeding insights into system.

---

## RESOURCE REQUIREMENTS SUMMARY

| Practice | Team | Cost | Launch |
|----------|------|------|--------|
| **Educator** | 1 part-time lead | Low | Aug 21 |
| **Practice Optimizer** | 1 dedicated lead | Medium | Sep 11 |
| **Local Machine Optimizer** | 1 engineer (part-time) | Medium | Oct 9 |
| **TOTAL** | 2-3 people | Medium-High | Phased |

**Question for Night:** Can Resource Miner allocate $50K-$100K for staffing these three practices (Aug-Dec 2026)?

---

## STATUS: 16-PRACTICE SYSTEM READY FOR RATIFICATION

**13 existing practices + 3 new practices = 16-practice Empirica-Foundation + HumanAIOS + Educator system**

All frameworks complete. Ready for ratification + implementation by 2026-08-21.

Next session: Execute implementation roadmap, activate Phase 1 (Educator), begin Phase 2 prep (Practice Optimizer), complete Phase 3 prep (Local Machine Optimizer).
