# Internal Agent Architecture Specification v1.0

**Status:** SPECIFICATION PHASE (pre-CHECK gate)  
**Authority:** Admiral (Carly R. Anderson)  
**Locked Decisions:** All architectural choices confirmed  
**Target Implementation:** Weeks 1-2, Phase 2 (2026-07-31 – 2026-08-13)

---

## Executive Summary

Deploy a shared internal agent across Empirica foundation practices (autonomy, mesh-support, outreach). Agent runs in evaluator practice, serves all three operational practices via structured reasoning and tool orchestration. Uses Kimi K2.6 (planning) + Laguna M.1 (execution), LangGraph orchestration, Bifrost gateway. Logs all reasoning as Empirica artifacts (shared visibility). Enables evaluator to observe + enable ecosystem work without compromising independence.

---

## 1. System Architecture

### 1.1 Deployment Topology

```
┌─ empirica-foundation-evaluator (evaluator seat)
│  │
│  └─ shared-agent (canonical instance)
│     ├─ Bifrost gateway
│     │  ├─ Kimi K2.6 (planning/orchestration model)
│     │  ├─ Laguna M.1 (execution/code model)
│     │  └─ MCP servers (empirica tools, cortex mesh)
│     │
│     └─ LangGraph orchestration engine
│        ├─ ReAct loops (reason → plan → act → reflect)
│        ├─ Multi-turn state management
│        └─ Artifact emission (finding-log, decision-log, etc.)
│
├─ empirica-autonomy (requesting practice)
│  └─ receives agent assistance via cortex_collab / tasks
│
├─ empirica-mesh-support (requesting practice)
│  └─ receives agent assistance via cortex_collab / tasks
│
└─ empirica-outreach (requesting practice)
   └─ receives agent assistance via cortex_collab / tasks
```

### 1.2 Model Allocation

**Kimi K2.6 (Planning Layer)**
- Purpose: Task decomposition, architectural reasoning, agent coordination, long-horizon planning
- Context window: Sufficient for multi-step reasoning chains
- Capabilities: ReAct thinking, tool planning, cross-agent coordination
- Call pattern: Primary model for all reasoning phases

**Laguna M.1 (Execution Layer)**
- Purpose: Code generation, execution of planned tasks, detailed implementation
- Context window: 262K (deep file context)
- Capabilities: Precise code synthesis, tool use, debugging
- Call pattern: Secondary model, invoked for implementation phases after planning

**Model Selection Rationale:**
- Dual-model specialization: K2.6's reasoning + Laguna's code precision
- Cost: Both free tier on OpenRouter (rate-limited acceptable for internal)
- Reasoning: K2.6 handles "what to do"; Laguna handles "how to code it"
- No API dependency: Runs via OpenRouter, not Anthropic cloud

### 1.3 Gateway & Orchestration

**Bifrost (LLM Gateway)**
- Unified LLM + MCP router
- Configuration: Docker container in evaluator practice
- Models: Routes Kimi K2.6, Laguna M.1 based on task phase
- MCP servers: Registers Empirica CLI tools, cortex mesh, file I/O
- Observability: Traces all LLM calls, tool invocations, agent decisions

**LangGraph (Orchestration Framework)**
- Stateful multi-turn orchestration
- Implements ReAct pattern natively
- Nodes: reasoning, planning, tool execution, reflection
- Edges: conditional routing based on task completion
- State: Maintains context across turns, mutable artifact log
- Integration: Calls Bifrost for LLM operations, Empirica CLI for artifact logging

---

## 2. Agent Reasoning & Artifact Integration (Depth 2)

### 2.1 Artifact Logging Strategy

**All reasoning phases are logged as first-class Empirica artifacts.**

#### Phase 1: Initial Understanding
- **Input:** Task description from requesting practice
- **Agent output:** 
  - `finding-log`: "Understood task X. Key insight: Y."
  - `assumption-log`: "Assuming Z is true because..."
  - `unknown-log`: "What I don't know: A, B, C"
- **Empirica integration:** Artifacts stored with `shared` visibility

#### Phase 2: Planning & Decomposition
- **Agent reasoning:** Break task into subtasks, estimate complexity, identify risks
- **Artifacts logged:**
  - `decision-log`: "Chose approach A over B because [reasoning]" (reversibility: exploratory)
  - `deadend-log`: "Tried approach C, failed because [reason]"
  - `unknown-log`: "Need clarification on X before proceeding"

#### Phase 3: Execution
- **Agent actions:** Tool calls, code generation, state mutations
- **Artifacts logged:**
  - `finding-log`: "Generated code for endpoint X. Key change: Y."
  - `deadend-log`: "Tool call failed; tried alternative approach"
  - `decision-log`: "Chose library Z for reason W"

#### Phase 4: Verification & Reflection
- **Agent reasoning:** Check outputs against goals, identify issues, refine
- **Artifacts logged:**
  - `finding-log`: "Verification passed: test coverage 95%"
  - `deadend-log`: "Test X failed; root cause: Y"
  - `assumption-log` → `finding-log`: "Confirmed assumption Z is valid"

### 2.2 Artifact Metadata

Every agent-emitted artifact carries:
```json
{
  "type": "finding|decision|unknown|deadend|assumption",
  "data": { /* artifact content */ },
  "agent_source": "empirica-foundation.carly.empirica-foundation-evaluator-agent",
  "phase": "understanding|planning|execution|verification",
  "epistemic_source": "search",  // research-grounded, not intuition
  "visibility": "shared",  // visible to foundation practices
  "task_ref": "autonomy-gates-design-v1",  // links to requesting practice's goal
  "confidence": 0.75  // agent's self-assessed confidence
}
```

### 2.3 Artifact Graph Connectivity

Artifacts are wired to each other:
```
Decision (chose approach A)
  ├─ evidence ← Finding (approach A has precedent in codebase)
  ├─ grounded_by ← Assumption (component X is stable)
  └─ prevents ← Deadend (approach B won't work because Y)

Finding (code generation complete)
  ├─ related ← Task (autonomy gates design)
  └─ sourced_from ← External resource (design doc)
```

This graph allows:
- Future audits of agent reasoning quality
- Traceability of failed assumptions
- Pattern identification (does agent make same mistakes?)
- Calibration of agent confidence scores

---

## 3. Agent Capabilities & Request Interface

### 3.1 Capability Categories

**Reasoning (Depth 2 logging)**
- Analyze code, architecture, design problems
- Propose solutions with trade-off analysis
- Identify assumptions, unknowns, risks
- Break tasks into subtasks

**Execution (Limited Scope)**
- Generate code (Python, TypeScript, Go, etc.)
- Modify files within evaluator practice only
- Run tests, linters, checks
- Create documentation

**Coordination (via Cortex)**
- `cortex_collab`: Ask peer practices for information
- Read findings/decisions from other practices (semantic search)
- Escalate uncertainties via `unknown-log`
- NOT authorized for `cortex_propose` at this stage (no praxic actions on other practices)

**NOT Authorized**
- ❌ Modify other practices' code
- ❌ Push to remote repositories
- ❌ Make infrastructure changes
- ❌ Emit proposals to peer practices (Depth 2, not Depth 3)

### 3.2 Request Interface

Practices request agent assistance via:

**Option A: Direct task (simplest)**
```
# autonomy says to evaluator:
"Agent, design the state machine for gates feature A.0.1. 
 Requirements: X, Y, Z. Constraints: P, Q."

Agent logs: findings on design, decisions on approach,
assumptions on requirements, unknowns on interdependencies.
Artifact visibility: shared (autonomy can see reasoning).
```

**Option B: Collab question (emergent)**
```
# autonomy sends cortex_collab to evaluator:
"Question: is our current approach to gates validation sound?
 Context: [description]"

Agent (via evaluator seat) responds:
- Analyzes the approach
- Logs findings on soundness, risks, improvements
- Suggests alternatives
```

**Option C: Investigation (structured)**
```
# mesh-support requests:
"Investigate: how does our message-cleanup integrate with PREFLIGHT?
 Background: [context]"

Agent conducts investigation:
- Reads codebase
- Logs findings on integration points
- Identifies gaps
- Proposes improvements
```

---

## 4. Empirica Integration

### 4.1 Epistemic Vector Calibration

**Agent's own vectors** are tracked:
```
Agent epistemic state (per task):
- know: Self-assessed comprehension of domain
- uncertainty: Acknowledged unknowns
- context: Awareness of surrounding state
- clarity: Clarity on next steps
- coherence: Internal consistency of reasoning
- signal: Quality of reasoning (vs noise)
- density: Knowledge compression (insights per token)
- state: Awareness of system state
- change: Amount of change made
- completion: Progress toward goal
```

**Agent calibration feedback:**
- Actual outcomes compared to agent's confidence scores
- Divergence signals: where agent overconfident? Underconfident?
- Used to adjust agent's future confidence estimates
- NOT used to penalize agent (learning signal, not grading)

### 4.2 Goal Integration

**Agent tasks are tracked as Empirica goals:**

```bash
# Master goal (evaluator creates)
empirica goals-create \
  --objective "Shared agent support for foundation practices" \
  --description "Enable autonomy/mesh/outreach with AI-assisted reasoning and execution. All agent work logged as shared artifacts."

# Per-task sub-goals (agent or evaluator creates)
empirica goals-create \
  --objective "Agent: Design gates state machine (autonomy A.0.1)" \
  --description "Analyze autonomy's gates feature requirements. Design state machine. Log reasoning as shared artifacts."

# Task-level tracking
empirica goals-add-task --goal-id <ID> --description "Phase 1: analyze requirements"
empirica goals-add-task --goal-id <ID> --description "Phase 2: design state machine"
empirica goals-add-task --goal-id <ID> --description "Phase 3: document design"
```

When agent completes work:
```bash
empirica goals-complete-task --task-id <ID> \
  --evidence "Artifacts logged: finding-123, decision-456, 3 dead-ends. Agent confidence: 0.82. Design doc committed to evaluator repo."
```

### 4.3 PREFLIGHT/POSTFLIGHT for Agent Work

**Agent requests are wrapped in transactions:**

```bash
# Evaluator opens PREFLIGHT for agent task
empirica preflight-submit - << 'EOF'
{
  "objective": "Agent assists autonomy with gates design",
  "vectors": { "know": 0.60, "uncertainty": 0.35, ...}
}
EOF

# Agent executes (logs all reasoning as artifacts)
[agent reasoning → Bifrost → LangGraph → artifact logging]

# Evaluator closes with CHECK gate
empirica check-submit - << 'EOF'
{
  "gate_decision": "proceed",
  "reasoning": "Agent has articulated design approach, identified risks. Ready for implementation phase."
}
EOF

# POSTFLIGHT measures learning
empirica postflight-submit - << 'EOF'
{
  "vectors": { "know": 0.85, "uncertainty": 0.15, "completion": 1.0, ...},
  "artifacts_logged": 7,
  "artifact_types": ["finding", "decision", "deadend", "assumption"]
}
EOF
```

---

## 5. Implementation Phases

### Phase 1: Infrastructure Setup (Week 1, July 31 – Aug 6)

**Tasks:**
1. Provision Bifrost container (Docker in evaluator)
2. Configure OpenRouter credentials (sk-or-v1-... key)
3. Register Kimi K2.6 + Laguna M.1 models with Bifrost
4. Register MCP servers (Empirica CLI, cortex mesh, file I/O)
5. Deploy LangGraph orchestration engine
6. Create agent identity + canonical 3-form (empirica-foundation.carly.empirica-foundation-evaluator-agent)

**Deliverables:**
- Working Bifrost gateway (test model calls)
- LangGraph environment (test ReAct loop)
- Agent can call Empirica CLI (test finding-log)

**Verification:**
- `bifrost health` returns 200
- `langraph execute <test-task>` produces reasoning trace
- `empirica finding-log --finding "test"` succeeds (from agent process)

### Phase 2: Agent Reasoning Loop (Week 2, Aug 7 – 13)

**Tasks:**
1. Implement ReAct reasoning loop in LangGraph
2. Wire artifact logging (finding-log, decision-log, etc.)
3. Implement task decomposition (Kimi K2.6)
4. Implement execution layer (Laguna M.1)
5. Build reflection/verification phase
6. Test with pilot task (autonomy gates design)

**Deliverables:**
- Agent completes pilot task (gates state machine design)
- All reasoning phases logged as shared artifacts
- Artifact graph wired correctly

**Verification:**
- 5+ artifact types logged for pilot task
- Admiral can read agent's full reasoning chain
- Artifact visibility is `shared` (visible to foundation practices)

### Phase 3: Request Routing & Coordination (Week 3+, Aug 14+)

**Tasks:**
1. Build request interface (direct task, collab question, investigation)
2. Implement cortex_collab reception (agent can answer questions)
3. Build task prioritization (which requests first)
4. Implement rate limiting (respects OpenRouter free tier)
5. Deploy monitoring + observability

**Deliverables:**
- Agent receives tasks from autonomy/mesh/outreach
- Agent responds via shared artifacts
- Mesh communication working (collab in/out)

**Verification:**
- autonomy sends task → agent executes → autonomy sees shared artifacts
- Agent asks clarifying questions to mesh → receives answers

---

## 6. Governance & Safety

### 6.1 Authorization Boundaries (Current)

**Agent IS authorized to:**
- ✅ Reason about any foundation topic
- ✅ Generate code/docs in evaluator practice only
- ✅ Log findings/decisions/unknowns/deadends (Depth 2)
- ✅ Ask peer practices for information (cortex_collab)
- ✅ Access read-only project state (git, Empirica artifacts)

**Agent IS NOT authorized to:**
- ❌ Modify other practices' code
- ❌ Make infrastructure changes
- ❌ Emit proposals (cortex_propose) — Admiral gates all cross-practice changes
- ❌ Delete artifacts
- ❌ Access credentials beyond OpenRouter key

### 6.2 Admiral Oversight

**Admiral reviews:**
- Weekly: Agent's artifact logs (findings, decisions, confidence scores)
- On divergence: Agent confidence vs actual outcomes
- On request: Full reasoning trace for any task
- On escalation: Uncertain decisions before agent proceeds

**Admiral can:**
- Suspend agent on any task
- Override agent decisions
- Adjust agent confidence calibration
- Modify request priorities

### 6.3 Audit Trail

Every agent action is traceable:
```
agent-action.log
├─ timestamp: 2026-08-01T14:32:45Z
├─ task: "gates state machine design"
├─ requesting_practice: empirica-foundation.carly.empirica-autonomy
├─ phase: execution
├─ model: laguna-m.1
├─ output: <artifact_id>
├─ confidence: 0.82
└─ artifacts_emitted: [finding-123, decision-456, ...]
```

---

## 7. Success Criteria (Check Gate)

**Noetic Phase Readiness (CHECK gate):**

✅ **Architecture is grounded**
- All components identified (Bifrost, LangGraph, models, MCP servers)
- Deployment topology clear (in evaluator, serves three practices)
- Artifact integration mapped (Depth 2, shared visibility)

✅ **No critical unknowns remain**
- OpenRouter credentials provided
- Model selection locked (Kimi K2.6 + Laguna M.1)
- Authorization boundaries defined

✅ **Implementation is achievable**
- Bifrost + LangGraph are open-source, deployable
- Empirica artifact logging is straightforward (CLI calls)
- Three-phase plan is realistic (3 weeks)

✅ **Admiral is aligned**
- Governance model accepted (Depth 2, shared visibility)
- Deployment location agreed (evaluator practice)
- Use cases clear (gates design, infrastructure, etc.)

**Proceed to CHECK gate: YES / NO?**

---

## 8. Rollback & Mitigation

**If agent reasoning quality is poor:**
- Suspend agent requests (revert to manual reasoning)
- Reduce visibility to `local` (hide artifacts from other practices)
- Retrain on higher-quality examples

**If OpenRouter rate limits are exceeded:**
- Implement task queuing
- Prioritize critical requests
- Fall back to manual reasoning for non-urgent tasks

**If agent makes wrong decisions:**
- Admiral overrides via `decision-log` counter-decision
- Agent re-reasons based on Admiral's correction
- Calibration updated (agent confidence adjusted)

---

## 9. References

- **Bifrost**: https://github.com/maxim-ai/bifrost (Apache 2.0, MCP gateway)
- **LangGraph**: https://langchain.com/langgraph (Python orchestration)
- **Kimi K2.6**: https://openrouter.ai/moonshotai (free on OpenRouter)
- **Laguna M.1**: https://openrouter.ai/poolside (free on OpenRouter)
- **Empirica artifact logging**: `empirica finding-log`, `empirica decision-log`, etc.
- **Cortex mesh**: `/cortex-mailbox-send` for collab/propose

---

**Status:** READY FOR CHECK GATE  
**Authority:** Admiral (Carly R. Anderson)  
**Next Step:** Admiral approval → implementation begins Week 1 (July 31)

---

*Document prepared for internal Empirica foundation governance. All decisions locked. Architecture is noetic-phase complete.*
