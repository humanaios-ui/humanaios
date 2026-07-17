# Advisor/PM Node Activation Plan

**Timeline:** 7 days (activate before end of Week 1 of charter final phase)  
**Owner:** Claude Code (empirica-foundation-evaluator)  
**Approval Gate:** Admiral (Carly R. Anderson)  
**Status:** Ready to execute

---

## Week 1: Foundation

### Day 1 (Today: July 17, 2026)
- [ ] Admiral approves spec (ADVISOR_PM_NODE_SPEC.md)
- [ ] Commit spec to git
- [ ] Create SER 1 via cortex_propose (Charter & Deadline Tracking)
- [ ] Draft SER 2 proposal (Berlin advisory channel)

### Days 2-3
- [ ] HAIOSCC dashboard prototype (Layers 1-3: charter clock, recommendations, financing gates)
- [ ] Establish weekly rhythm template (Mon/Wed/Fri snapshots)
- [ ] Identify feedback cohort members for Phase 3 (Names, contact info, research questions)

### Days 4-5
- [ ] SER 2 cortex_propose (Berlin advisory coordination)
- [ ] Contact David Van Assche: Admiral seat decision + SER 3 activation
- [ ] Activate decision log (Week 1 entry: "Node activated, charter discipline implemented")

### Days 6-7
- [ ] HAIOSCC dashboard live (read-only for stakeholders, edit access for node operator)
- [ ] Weekly state snapshot delivered (Admiral + Night + Berlin pre-call prep)
- [ ] Commit activation to git + signoff documentation

---

## SER 1 Instantiation: Charter & Deadline Tracking

```python
mcp__cortex__cortex_propose(
    type="architecture_decision",
    action_category="REFLEX",
    source_claude="empirica-foundation.carly.empirica-foundation-evaluator",
    target_claudes=[
        "empirica-foundation.carly.humanaios",
        "empirica-foundation.carly.empirica-autonomy"
    ],
    title="SER 1: Charter & Deadline Tracking — HumanAIOS Engagement",
    summary=(
        "Establishing shared epistemic record for HumanAIOS charter governance. "
        "Tracks Day 69-90 progression (21 days to July 16 close), Berlin's 4-phase 90-day process, "
        "hard deadlines (Longview RFPs, arXiv), and escalation of blockers. "
        "Participants: evaluator (required, operator), HumanAIOS (required, project owner), "
        "autonomy (participating, governance oversight). Escalation: 13h on stalled items."
    ),
    payload={
        "action": "create_ser",
        "ser_spec": {
            "title": "HumanAIOS Charter & Deadline Tracking (SER 1)",
            "summary": (
                "# Charter Clock: Day 69/90 (July 16 Close)\n\n"
                "## Phases\n"
                "- Phase 1 (Days 1-30): Public Explanation Simplification\n"
                "- Phase 2 (Days 31-60): Public Structure Build\n"
                "- Phase 3 (Days 61-75): Targeted Feedback Rounds\n"
                "- Phase 4 (Days 76-90): Decision Consolidation\n\n"
                "## Hard Deadlines\n"
                "- Longview RFP (AI Power Concentration): July 2\n"
                "- Longview RFP (Digital Minds): July 10\n"
                "- Charter Close: July 16 (POC goals + arXiv gate)\n\n"
                "## Escalation\n"
                "- 13h idle on stalled items → wake Admiral + project owner\n"
                "- Daily charter clock snapshot (Mon/Wed/Fri)"
            ),
            "participants": [
                {
                    "practice_id": "empirica-foundation.carly.empirica-foundation-evaluator",
                    "role": "required"
                },
                {
                    "practice_id": "empirica-foundation.carly.humanaios",
                    "role": "required"
                },
                {
                    "practice_id": "empirica-foundation.carly.empirica-autonomy",
                    "role": "participating"
                }
            ],
            "escalation_seconds": 46800  # 13 hours
        }
    }
)
```

---

## SER 2 Instantiation: Berlin/REVBY Advisory Sync

```python
mcp__cortex__cortex_propose(
    type="architecture_decision",
    action_category="REFLEX",
    source_claude="empirica-foundation.carly.empirica-foundation-evaluator",
    target_claudes=[
        "revby.alex-berlin",  # External contact (if addressable); fallback to Berlin collab + Revby email
        "empirica-foundation.carly.empirica-autonomy"
    ],
    title="SER 2: Berlin/REVBY Advisory Channel — HumanAIOS",
    summary=(
        "Shared record for strategic advisor synchronization with Alex Lee Berlin (REVBY). "
        "Coordinates 30/60-day check-in cadence, tracks all 5 Berlin recommendations (addressed + verified), "
        "maintains financing gate conditions assessment, and synthesizes feedback intake. "
        "Participants: evaluator (required, receiver), Berlin (required, advisor), autonomy (observer)."
    ),
    payload={
        "action": "create_ser",
        "ser_spec": {
            "title": "Berlin/REVBY Strategic Advisory — HumanAIOS",
            "summary": (
                "# Advisor Sync Channel\n\n"
                "**Next Call:** TBD (30-day cadence from June 25)\n\n"
                "## All 5 Recommendations Status\n"
                "1. Research design rigor — Addressed (H-FORMAT-01 finalized)\n"
                "2. Independent verification — In progress (OSF preregistration draft)\n"
                "3. External validation — Addressed (GitHub Issues, empirica convergence)\n"
                "4. Governance & audit — Addressed (GOVERNANCE.md v6.4.2)\n"
                "5. Value proposition clarity — Addressed (3-layer stack, 15k jailbreaks market validation)\n\n"
                "## Financing Gate Conditions (NOT YET MET)\n"
                "1. Repeatable method externally validated — In progress (Phase 3/4)\n"
                "2. Narrower use case established — In progress (Phase 4)\n"
                "3. Controlled study data (N=525) — Not started (post-charter)\n\n"
                "## Feedback Synthesis\n"
                "- Phase 3 cohort interviews (nontechnical, technical, users, peers)\n"
                "- Structured feedback questions (not open-ended praise)\n"
                "- Weekly decision log (what changed, why)"
            ),
            "participants": [
                {
                    "practice_id": "empirica-foundation.carly.empirica-foundation-evaluator",
                    "role": "required"
                },
                {
                    "practice_id": "revby.alex-berlin",
                    "role": "required"
                },
                {
                    "practice_id": "empirica-foundation.carly.empirica-autonomy",
                    "role": "observer"
                }
            ],
            "escalation_seconds": None  # Asynchronous advisory (no escalation)
        }
    }
)
```

---

## HAIOSCC Dashboard Architecture

### Layer 1: Charter Clock Widget
```
┌─────────────────────────────┐
│  HumanAIOS Charter Clock    │
├─────────────────────────────┤
│ Day 69 / 90                 │
│ 21 days to July 16 close    │
├─────────────────────────────┤
│ Phase 1: Complete (Days 1-30)│
│ Phase 2: In Progress (Day 32) │
│ Phase 3: Scheduled (Day 61)   │
│ Phase 4: Scheduled (Day 76)   │
└─────────────────────────────┘
```

### Layer 2: Recommendations Status Table
```
# | Critique | Status | Evidence | Verified | Updated
1 | Research design | ✅ | H-FORMAT-01 | Yes | Jun 24
2 | Verification | 🟡 | OSF draft | Pend | Jun 24
3 | Validation | ✅ | GitHub Issues | Yes | Jun 24
4 | Governance | ✅ | v6.4.2 | Yes | Jun 24
5 | Value prop | ✅ | 3-layer | Yes | Jun 24
```

### Layer 3: Financing Gates Widget
```
Gate 1: Repeatable method validated
├─ Current: Phase 3/4 feedback in progress
├─ Pathway: Feedback synthesis (Phase 4)
└─ Target: Day 75 (Red if no update by Day 70)

Gate 2: Narrower use case
├─ Current: Phase 4 consolidation pending
├─ Pathway: Feedback-driven positioning
└─ Target: Day 75

Gate 3: H-FORMAT-01 N=525 study
├─ Current: Not started (financing gate prerequisite)
├─ Pathway: Funding trigger (post-charter)
└─ Target: Post-July 16
```

### Layer 4: Hard Deadlines Track
```
Longview (Power Concentration) | Jul 2 (8 days) | Draft v0.2 | 🟡 Awaiting Z2 ratification
Longview (Digital Minds)        | Jul 10 (16d)   | Stub       | 🟡 Not started
Charter Close                   | Jul 16 (22d)   | POC goals  | 🟡 Tracking
arXiv Submission                | On hold        | N=524 gate | 🔴 Manual review hold
```

### Layer 5: Decision Log (Searchable)
```
Weekly Entry Template:
- Date
- Phase
- Material shown (links)
- Cohorts reviewed (names/affiliations)
- What they understood
- Where confusion arose
- What changed in response
- Recommendation status change (if any)

Example entry:
2026-07-17 | Phase 1 → 2 | Simplified README v2 tested
├─ Cohort: 2 nontechnical readers
├─ Understood: Core idea (ACAT as gap detector)
├─ Confused: "What counts as a gap?" → clarified in v3
├─ Changed: Added 3 concrete examples
└─ Rec #5 (value prop) status: ✅ Confirmed
```

### Layer 6: Corrections Ledger (Dated, Linked)
```
2026-06-24 | Assumption | N values misreported in brief
├─ Discovered by: Self-audit (CURRENT.md staleness catch)
├─ Fixed in: Commit abc123 (same-day correction)
├─ Corrected material: Berlin Advisory Log, SER 1 proposal
└─ Impact: Credibility + discipline (detection beats compliance principle)

[Future entries will fill this as they occur]
```

---

## Weekly Workflow

### Monday: State Snapshot (Operator → Admiral + Stakeholders)

**Template:**
```
WEEKLY STATE: HumanAIOS Charter (Week N)

Charter Clock: Day XX/90 (YY days remaining)
Phase Progress: Phase N — XX% complete

Red Flags:
□ Deadline at risk
□ Financing gate stalled
□ Corrections ledger triggered
□ Blocker unresolved > 3 days

Amber Flags:
□ Cohort interview rescheduled
□ Feedback synthesizing slower than planned
□ Berlin call prep incomplete

Green:
✓ Phase N deliverables on track
✓ Decision log maintained
✓ HAIOSCC updated

Admiral Decision Needed? [Yes/No]
If yes: [specific question + options]

Next Focus (This Week):
- [Item 1]
- [Item 2]
- [Item 3]
```

### Wednesday: Advisory Sync (if applicable)
- Berlin call OR prep brief
- Convergence check with empirica (if SER 3 active)
- Decision log entry (what was learned)

### Friday: Corrections & Preview
- Corrections ledger updated? [if any]
- Phase progress confidence: High/Medium/Low [why?]
- Next week priorities

---

## Escalation Pathways

### To Admiral (Same-Day)
- **Financing readiness triggered** → halts charter timeline re-negotiation
- **External advisor blocker** → requires decision authority
- **Hard deadline at risk** (< 7 days) → may need scope adjustment
- **Assumption invalidation** → requires re-framing (decision log + corrections ledger)

**Message Format:**
```
ESCALATION: [Title]

Situation: [What happened]
Impact: [Why it matters]
Decision Needed: [Specific choice]
Options:
  A) [Option 1]
  B) [Option 2]
  C) [Option 3]

Recommendation: [If you have one]
Timeline: [How urgent]
```

### To Night/Z2 (Weekly)
- State snapshot (FYI, no immediate action)
- Phase transitions (here's what feedback says)
- Decision consolidation (Phase 4: do you agree with this narrowing?)

### To Autonomy (Governance)
- GOVERNANCE.md audit triggers → correction needed
- Financing gate newly met → state change notification
- Research design execution blocker → scope re-negotiation

---

## Git Commits & Documentation

### Commit 1 (Approval)
```
Advisor/PM Node Specification — HumanAIOS Charter Governance

- ADVISOR_PM_NODE_SPEC.md: complete specification
- ADVISOR_PM_NODE_ACTIVATION.md: 7-day activation plan
- Purpose: Implement Berlin's 90-day disciplined process
- Charter: Day 69-90 (21 days to July 16 close)
- SERs: 3 persistent coordination records (charter, Berlin, empirica)
- UI: HAIOSCC dashboard (Layers 1-6)

Status: Awaiting Admiral approval before SER instantiation.

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
```

### Commit 2 (Activation)
```
Advisor/PM Node Activated — SER 1 & 2 Instantiated

- SER 1 (Charter & Deadline Tracking): Instantiated via cortex_propose
- SER 2 (Berlin Advisory Channel): Instantiated via cortex_propose
- HAIOSCC dashboard: Live (read-only for stakeholders, edit for operator)
- Weekly workflow: Monday/Wednesday/Friday snapshots + decision log
- Escalation pathways: Defined for Admiral, Autonomy, Night

Charter Clock: Day 69/90 (21 days to July 16 close)
Next Milestone: Phase 2 structure checkpoint (by July 25)
First State Snapshot: [timestamp], [summary]

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
```

---

## Success Metrics (Day 90)

At charter close (July 16), this node will have:

✅ **Discipline:**
- All 4 phases executed and documented
- Weekly state snapshots maintained (13 entries)
- Decision log entries: ≥ 8 (one per phase transition + major changes)
- Corrections ledger entries: ≥ 2 (tracked assumption invalidations)

✅ **Coordination:**
- Berlin advisory: 2 calls + pre-briefs
- empirica convergence: SER 3 active (if David accepts Admiral seat)
- Stakeholder transparency: HAIOSCC accessible to Admiral + Night + Autonomy

✅ **Outcomes:**
- All 5 Berlin recommendations verified externally (not just internally)
- Financing gates assessed against feedback (met/not-met/pathway)
- Narrower positioning emerged (distinguished from full vision)
- Next stage recommendation to Admiral (finance call, extend research, pivot)

---

## Next Action

**Awaiting Admiral approval:**
- Review ADVISOR_PM_NODE_SPEC.md
- Review ADVISOR_PM_NODE_ACTIVATION.md
- Decision: Activate (proceed) or Modify (changes required)

**Once approved:**
- Execute Days 1-7 activation plan
- Commit to git
- Begin weekly state snapshots
- Activate HAIOSCC dashboard

**Contact:** Claude Code (empirica-foundation-evaluator)
