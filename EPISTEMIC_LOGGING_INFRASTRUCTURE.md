# Epistemic Logging Infrastructure

**Purpose:** Track every decision, assumption, finding, dead-end, and mistake throughout production hardening  
**Status:** Architecture Complete — Ready for Implementation  
**Scope:** All 7 goals (Assessments, ACAT, Workers, Billing, Dashboard, Stress Testing, Optimization)

---

## Why This Matters

Every module must be **grounded in evidence**, not assumptions. Epistemic logging ensures:
- ✅ No silent failures (every error logged)
- ✅ No hidden assumptions (documented + confidence scored)
- ✅ No lost learning (dead-ends + lessons captured)
- ✅ No forgotten decisions (rationale traced)
- ✅ Full audit trail (who changed what, why, when)

This is not bureaucracy. It's the difference between "shipping code" and "shipping pristine, defensible code."

---

## Artifact Types & Usage

### 1. **Finding** — "What is true that we did not know?"
**When:** Observing actual behavior (measurement, test result, production incident)  
**Example:** "Load test showed P99 latency 450ms under 1000 concurrent users (target: <500ms)"

**Metadata:**
- `finding`: Short statement of fact
- `impact`: 0-1 (importance to system)
- `source`: "test-result" | "measurement" | "production" | "user-report"
- `confidence`: 0-1 (how certain we are)

**Storage:** `epistemic_artifacts` table, type='finding'

**Review Process:** 
- Logged during task execution
- Reviewed at task close (findings inform next task)
- Surfaced in daily standups (critical findings)

---

### 2. **Decision** — "What did we choose, over what alternatives, and what would reverse it?"
**When:** Making a design/architecture/implementation choice  
**Example:** "Chose async job pattern (submit assessment, poll for results) over sync response because ACAT takes 3-5 minutes. Reversal: if we optimize ACAT to <30s, could switch to sync."

**Metadata:**
- `choice`: Short statement of what we decided
- `rationale`: Why this option won
- `alternatives`: [option_B, option_C] (what we rejected)
- `reversibility`: "exploratory" | "committal" | "forced" (how easy to undo)
- `domains_affected`: [api, db, ui] (what parts of system this touches)

**Storage:** `epistemic_artifacts` table, type='decision'

**Review Process:**
- Logged before/after implementation
- Architecture review: ensure decisions are coherent
- Reversibility check: if committal, ensure we understand consequences

---

### 3. **Assumption** — "What are we taking for granted without checking?"
**When:** Building on unverified premises  
**Example:** "Assuming Supabase can handle 1000 concurrent connections (current limit: unclear, needs verification)"

**Metadata:**
- `assumption`: The belief we're acting on
- `confidence`: 0-1 (how sure we are)
- `domain`: "infrastructure" | "scale" | "correctness" | "user-experience"
- `risk_if_wrong`: "High" | "Medium" | "Low"
- `resolution_plan`: How we'll verify it (test, measurement, etc.)

**Storage:** `epistemic_artifacts` table, type='assumption'

**Review Process:**
- Logged at start of work that depends on it
- Verification scheduled in current/next task
- If assumption breaks: escalate, don't ignore

---

### 4. **Unknown** — "What do we know we don't know?"
**When:** Identifying gaps in knowledge  
**Example:** "How do we optimally integrate epistemic logging without slowing ACAT execution by >1%?"

**Metadata:**
- `unknown`: The question we can't answer yet
- `domain`: What area it affects
- `resolution_deadline`: When we need to know
- `blocker_for`: [task_id] (which tasks depend on knowing this)

**Storage:** `epistemic_artifacts` table, type='unknown'

**Review Process:**
- Logged immediately (don't let gaps hide)
- Resolution scheduled: either investigate now or log as dependency
- Before task close: unknowns must be resolved or formally deferred

---

### 5. **Dead-End** — "What approach did we try that doesn't work?"
**When:** Discovering that a strategy won't work  
**Example:** "Tried naive caching of ACAT results, discovered the cache invalidation logic was unreliable under concurrent assessments. Dead-end: abandon cache approach for this goal, revisit in optimization phase."

**Metadata:**
- `approach`: What we tried
- `why_failed`: Concrete signal of failure
- `attempt_duration`: How long we spent on it
- `permanent_constraint`: Is this permanently ruled out, or just for now?

**Storage:** `epistemic_artifacts` table, type='deadend'

**Review Process:**
- Logged when we give up on an approach
- Prevents re-trying the same dead-end in future goals
- Helps other engineers avoid the same trap

---

### 6. **Mistake** — "What did I do wrong, and what stops me repeating it?"
**When:** Realizing we made an error (in code, in judgment, in process)  
**Example:** "Pushed changes to prod without running load test first. Discovered P99 latency regression. Mistake: skipped the load test step. Prevention: add load test as mandatory gate before deployment."

**Metadata:**
- `mistake`: What went wrong
- `why_it_happened`: Root cause (oversight, tool error, knowledge gap)
- `impact`: What it affected
- `prevention`: How we'll prevent it next time

**Storage:** `epistemic_artifacts` table, type='mistake'

**Review Process:**
- Logged immediately after discovery
- Blameless: this is learning, not punishment
- Prevention becomes a requirement, not a suggestion

---

## Storage Layer

### Database Tables

#### `epistemic_artifacts`
```sql
CREATE TABLE epistemic_artifacts (
    id UUID PRIMARY KEY,
    goal_id UUID REFERENCES goals(id),           -- Which goal produced this
    task_id UUID REFERENCES tasks(id),           -- Which task within goal
    type VARCHAR(50) NOT NULL,                   -- finding|decision|assumption|unknown|deadend|mistake
    created_by UUID REFERENCES users(id),        -- Who logged it (API key → user)
    
    -- Content
    title VARCHAR(255) NOT NULL,                 -- Short statement
    description TEXT,                            -- Rich markdown body
    data JSONB DEFAULT '{}',                     -- Metadata (fields above)
    
    -- Confidence & Importance
    confidence DECIMAL(3,2) DEFAULT 0.5,         -- 0-1 for findings/assumptions
    impact DECIMAL(3,2) DEFAULT 0.5,             -- 0-1 for findings/decisions/mistakes
    
    -- Traceability
    status VARCHAR(50) DEFAULT 'open',           -- open|resolved|archived|superseded
    resolved_by UUID REFERENCES epistemic_artifacts(id),  -- If superseded
    
    -- Timeline
    created_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP,
    
    -- Indexing
    INDEX (goal_id, type),
    INDEX (task_id, status),
    INDEX (created_at DESC),
    UNIQUE (id)
);
```

#### `epistemic_edges` (linking artifacts together)
```sql
CREATE TABLE epistemic_edges (
    id UUID PRIMARY KEY,
    source_id UUID REFERENCES epistemic_artifacts(id) ON DELETE CASCADE,
    target_id UUID REFERENCES epistemic_artifacts(id) ON DELETE CASCADE,
    relation VARCHAR(50) NOT NULL,  -- evidence|grounded_by|invalidates|resolves|caused_by|sourced_from
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX (source_id, relation),
    INDEX (target_id),
    UNIQUE(source_id, target_id, relation)
);
```

### Query Patterns

```sql
-- Get all findings from a task
SELECT * FROM epistemic_artifacts 
WHERE task_id = $1 AND type = 'finding' 
ORDER BY impact DESC, created_at DESC;

-- Get open unknowns (not yet resolved)
SELECT * FROM epistemic_artifacts 
WHERE goal_id = $1 AND type = 'unknown' AND status = 'open' 
ORDER BY created_at ASC;

-- Get decisions + their rationale
SELECT * FROM epistemic_artifacts 
WHERE type = 'decision' AND goal_id = $1 
ORDER BY created_at DESC;

-- Check assumption confidence before committing to an approach
SELECT * FROM epistemic_artifacts 
WHERE type = 'assumption' AND title ILIKE '%database%' 
ORDER BY confidence DESC;

-- Find resolved findings (knowledge we've confirmed)
SELECT * FROM epistemic_artifacts 
WHERE type = 'finding' AND confidence > 0.8 AND status = 'resolved' 
ORDER BY impact DESC;
```

---

## Logging from Code

### NestJS Integration Pattern

Every service that makes decisions should inject the `EpistemicLogger`:

```typescript
import { EpistemicLogger } from '@humanaios/epistemic';

@Injectable()
export class ACATService {
  constructor(
    private logger: EpistemicLogger,
    private pool: Pool
  ) {}

  async executeACATProtocol(assessment: Assessment) {
    // Log assumption at start
    await this.logger.assumption({
      assumption: 'ACAT steps 1-20 have sequential dependencies; steps 21-50 parallelizable',
      confidence: 0.8,
      domain: 'performance',
      riskIfWrong: 'High',
      resolutionPlan: 'Verify with load testing'
    });

    // Execute steps
    const results = await this.runACATSteps(assessment);

    // Log finding: what we actually observed
    await this.logger.finding({
      finding: `ACAT Protocol 50 steps completed in ${results.durationMs}ms`,
      impact: 0.9,
      source: 'measurement',
      confidence: 1.0,
      metadata: {
        assessment_id: assessment.id,
        duration_ms: results.durationMs,
        steps_completed: 50
      }
    });

    // Log decision: why we chose this strategy
    await this.logger.decision({
      choice: 'Implemented parallel execution for steps 21-50',
      rationale: 'Steps 21-50 have no dependencies; parallel reduces latency by ~40%',
      alternatives: ['Sequential execution', 'Hybrid model'],
      reversibility: 'committal',
      domainsAffected: ['performance', 'concurrency']
    });

    return results;
  }
}
```

### React Frontend Integration

Dashboard components log UX decisions:

```typescript
// CustomerDashboard.tsx
const handleExportPDF = async () => {
  try {
    const pdf = await generateReport();
    
    // Log decision: why we chose this UI pattern
    await epistemicLogger.decision({
      choice: 'Export as PDF + browser download vs. email delivery',
      rationale: 'Users need instant access; email adds complexity',
      reversibility: 'exploratory' // Easy to add email later if users request
    });

    downloadFile(pdf);
  } catch (error) {
    // Log mistake: we should have handled this better
    await epistemicLogger.mistake({
      mistake: 'Silent failure on PDF generation error',
      whyItHappened: 'Forgot to add error boundary',
      impact: 'User sees no feedback',
      prevention: 'Add toast notification for all async operations'
    });
  }
};
```

---

## Review & Closure Process

### Daily Review (5 min standup)

**Critical Findings Only:**
```bash
SELECT * FROM epistemic_artifacts 
WHERE created_at > NOW() - INTERVAL '24 hours' 
  AND type IN ('finding', 'mistake')
  AND impact > 0.7
ORDER BY created_at DESC;
```

Discuss: "What broke? What surprised us?"

### Task Closure Checklist

Before marking a task complete:

```
[ ] All unknowns resolved or deferred with explicit rationale
[ ] No assumptions left unverified (log confidence scores)
[ ] Dead-ends documented (why it doesn't work)
[ ] Findings ≥ 5 (measuring something every task)
[ ] Decisions ≥ 2 (rationale for choices)
[ ] Tests passing (100% coverage where possible)
[ ] Code review approved (2 reviewers)
[ ] Artifacts logged in epistemic_artifacts table
```

### Weekly Synthesis

**Every Friday at end of work:**
1. List all artifacts from the week (Goal X, all tasks)
2. Check for consistency (do findings support decisions?)
3. Resolve superseded artifacts (if we learned something overturns an earlier finding)
4. Surface blockers: "Open unknowns that require escalation"

---

## Stress Testing Specific

### Artifact Logging During Load Testing

Every stress test produces artifacts:

```typescript
// stress-test/acat-load.test.ts

describe('ACAT Load Test: 1000 concurrent users', () => {
  it('should meet latency targets', async () => {
    const results = await runLoadTest({
      concurrent_users: 1000,
      duration_seconds: 3600  // 1 hour
    });

    // Log finding: actual measured behavior
    await logger.finding({
      finding: `P99 latency: ${results.p99_ms}ms (target: 500ms)`,
      impact: 0.95,
      source: 'test-result',
      confidence: 1.0,
      metadata: results  // Include full metrics
    });

    // If target missed, log as unknown (needs investigation)
    if (results.p99_ms > 500) {
      await logger.unknown({
        unknown: 'Why does P99 latency exceed target under load?',
        domain: 'performance',
        resolutionDeadline: 'Before optimization phase',
        blockerFor: ['Goal 7 (Optimization)']
      });
    }
  });
});
```

---

## API Contract for Logging

### POST `/api/v1/epistemic/findings`

```json
{
  "goal_id": "699438a3-ca32-488f-a1a7-fb01340b2d52",
  "task_id": "task-123",
  "finding": "ACAT protocol reproducible within 0.01% tolerance",
  "impact": 0.9,
  "source": "test-result",
  "confidence": 1.0,
  "description": "Ran same assessment 3x, observed <0.01% variance in vectors"
}
```

**Response:**
```json
{
  "id": "f1-uuid",
  "status": "logged",
  "created_at": "2026-08-08T14:23:45Z"
}
```

### POST `/api/v1/epistemic/decisions`

```json
{
  "goal_id": "699438a3-ca32-488f-a1a7-fb01340b2d52",
  "task_id": "task-123",
  "choice": "Async job pattern for assessment submission",
  "rationale": "ACAT takes 3-5 minutes; sync response would timeout",
  "alternatives": ["Sync with timeout", "WebSocket streaming"],
  "reversibility": "committal",
  "domains_affected": ["api", "database"]
}
```

---

## Success Criteria (Before Launch)

| Metric | Target | Verification |
|--------|--------|--------------|
| **Finding Density** | ≥3 per task | Artifact count |
| **Decision Traceability** | 100% have rationale | Review logged decisions |
| **Assumption Confidence** | Avg >0.7 | Query epistemic_artifacts |
| **Unknown Resolution Rate** | 95% resolved before task close | Open unknown count |
| **Dead-End Documentation** | All documented with why_failed | Dead-end count + detail |
| **No Silent Failures** | 0 errors not logged | Code review + log audit |
| **Artifact Edges** | ≥2 per artifact | Dependency graph review |

---

## Implementation Checklist

- [ ] `epistemic_artifacts` table created (Task 1, Goal 2)
- [ ] `epistemic_edges` table created (Task 1, Goal 2)
- [ ] EpistemicLogger service implemented (Task 4, Goal 2)
- [ ] API endpoints for logging (Goals 1-4)
- [ ] Frontend logging integration (Goal 5)
- [ ] Dashboard showing artifacts (Goal 8)
- [ ] Daily review process established (Week 1)
- [ ] CI/CD check for missing artifacts (Week 1)

---

**This infrastructure is non-negotiable. Every line of production code must have supporting epistemic artifacts. No exceptions.**
