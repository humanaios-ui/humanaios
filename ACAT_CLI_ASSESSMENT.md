# ACAT Shell Command Assessment
## Is a CLI Interface Beneficial and Constructive?

**Date:** 2026-07-06  
**Assessment:** ✅ **YES — Highly beneficial and constructive**

---

## Current State: ACAT HTTP API Only

### Existing Interface
ACAT currently provides HTTP API endpoints:
```
POST /api/v1/acat/intake/phase1          — Submit Phase 1 assessment
POST /api/v1/acat/intake/phase3          — Submit Phase 3 assessment
POST /api/v1/acat/assess                 — Run assessment
POST /api/v1/acat/human-score            — Submit human scoring
GET  /api/v1/acat/health                 — Health check
```

**Technology:** Python-based API (HTTP POST requests with JSON payloads)  
**Current users:** API clients (web services, internal tools)  
**Lack:** No shell/CLI wrapper for direct command-line usage

---

## Why a CLI Interface is Needed

### 1. Empirica-ACAT Integration (Immediate Need)

**Requested in Collab A to humanaios:**
```
acat-score \
  --session-id <empirica-session-id> \
  --ai-id <practice-name> \
  --behavior-transcript <path> \
  --rubric-version v1.0 \
  --output json
```

**Why this matters:**
- Empirica's POSTFLIGHT hook needs to invoke ACAT assessment atomically
- HTTP calls from within Python/shell hooks are cumbersome and fragile
- A CLI wrapper makes this operation simple, idiomatic, and scriptable

### 2. Operational Benefits

| Benefit | Impact | Use Case |
|---------|--------|----------|
| **Scriptability** | Enable automation | Batch assessment runs, testing, CI/CD integration |
| **Shell integration** | Direct POSTFLIGHT invocation | Hook into empirica's measurement pipeline |
| **Testing convenience** | No HTTP client setup needed | Manual testing, debugging, local development |
| **Operational visibility** | Exit codes, stdout/stderr | Monitor assessment success/failure, log output |
| **Version management** | Easy to pin CLI version | Reproducible assessment across sessions |

### 3. Constructive Alignment with Empirica Discipline

The Empirica-ACAT framework requires **observable linkage** at the session level:

```
Session execution
    ↓
Empirica POSTFLIGHT hook
    ↓
acat-score CLI invocation ← [This is where CLI shines]
    ↓
ACAT assessment payload
    ↓
Session record enriched with {phase, phase_score, rubric_alignment, observations}
```

A CLI wrapper makes this pipeline:
- **Observable:** Clear invocation, easy to audit in logs
- **Composable:** Shell scripts, orchestration tools, CI systems
- **Debuggable:** Test with `--verbose`, inspect `--output json`
- **Maintainable:** Single entry point, versioning strategy clear

---

## Recommended CLI Specification

### Interface Design

```bash
acat-score assess \
  --session-id <uuid> \
  --ai-id <practice-name> \
  --behavior-transcript <path-or-json> \
  --rubric-version <v1.0|v1.1> \
  [--phase <1|3|comprehensive>] \
  [--output <json|text>] \
  [--verbose]

# Output: JSON
{
  "phase": 3,
  "phase_score": 3.2,
  "confidence": 0.88,
  "rubric_alignment": {
    "clarity": "met",
    "independence": "met",
    ...
  },
  "observations": [...]
}
```

### Entry Points (Phased)

**Phase 1 (Week 2):** Core assess command
```bash
acat-score assess --session-id ... --ai-id ... --behavior-transcript ...
```

**Phase 2 (Future):** Batch operations
```bash
acat-score batch --input assessments.jsonl --output results.jsonl
```

**Phase 3 (Future):** Async with polling
```bash
acat-score assess --async --job-id <id>
acat-score status --job-id <id>
```

---

## Implementation Path

### Constructive Approach

**Why build a CLI wrapper (not just HTTP calls):**
1. **Single source of truth:** One interface, both CLI and API
2. **Easier maintenance:** Edit one place, both paths updated
3. **Better error handling:** CLI can normalize HTTP errors to exit codes
4. **Operational clarity:** Shell scripts are auditable; curl chains are not

### Architecture (Recommended)

```
humanaios/operations/acat/
├── api/                    ← HTTP endpoints (existing)
├── cli/                    ← NEW: CLI wrapper
│   └── commands.py        ← Entry point (assess, batch, status)
├── core/                   ← Shared logic (existing)
│   └── assess.py          ← Core assessment function
└── __main__.py            ← CLI entry point

# Invocation path:
$ acat-score assess ... 
  ↓ (Python entry point)
  ↓ (argparse dispatch)
  ↓ (core.assess function)
  ↓ (same logic as HTTP /assess endpoint)
  ↓ (JSON output)
```

### Installation

Two approaches (pick one):

**Option A: Setuptools console_scripts (Recommended)**
```python
# setup.py or pyproject.toml
entry_points={
    'console_scripts': [
        'acat-score=acat.cli.commands:main',
    ]
}
```
Result: `acat-score assess ...` available system-wide after install

**Option B: Python -m**
```bash
python -m acat assess --session-id ...
```
Result: No installation needed, but longer invocation

---

## Benefits for Empirica-ACAT Integration

### Observable Linkage

With CLI wrapper, the POSTFLIGHT flow becomes:

```python
# empirica POSTFLIGHT hook
session_transcript = compile_session_log()  # standard empirica

# Invoke ACAT via simple CLI call
acat_result = subprocess.run([
    'acat-score', 'assess',
    '--session-id', session_id,
    '--ai-id', ai_id,
    '--behavior-transcript', '/tmp/session.log',
    '--output', 'json'
], capture_output=True, json=True)

# Parse result, enrich session record
acat_grounding = acat_result['payload']
session_record['acat_grounding'] = acat_grounding
session_record['convergence'] = {
    'delta': empirica_vectors - acat_phase_score,
    'confidence': acat_grounding['confidence']
}
```

**Advantages:**
- ✅ No HTTP client needed in empirica
- ✅ Exit codes signal success/failure
- ✅ Subprocess isolation (no connection pooling issues)
- ✅ Works offline (API server down, CLI still runs)
- ✅ Easy to version-pin and test

---

## Constructive Outcomes

### For humanaios (ACAT owner)
- Single source of truth (core logic, not duplicated)
- Operational tool for testing assessments
- Scriptable for batch operations
- Clear contract with consumers (CLI interface)

### For Empirica-ACAT framework
- Observable linkage: session → ACAT assessment → JSON grounding
- Operational clarity: shell scripts are auditable
- Composable: integrates with other CLI tools
- Testable: `acat-score assess < input.json` for unit tests

### For Foundation (long-term)
- CLI becomes the canonical integration point
- Other practices can adopt without HTTP infrastructure
- Measurement pipeline becomes distributed and resilient
- Audit trail: who ran what assessment when (shell history)

---

## Recommendation

### Build the CLI in Phase 1a (Parallel with SER 1)

**Timeline:** Same week as SER 1 creation (Week 1, Days 1-2)  
**Effort:** ~4 hours (Python argparse wrapper + entry point)  
**Blocker:** No — can start immediately, doesn't depend on cortex mesh  
**Return:** Unblocks Empirica-ACAT framework observable linkage

### Specification for humanaios

Create `acat-score` command:
```bash
acat-score assess \
  --session-id <uuid> \
  --ai-id <practice> \
  --behavior-transcript <path> \
  --rubric-version v1.0 \
  --output json
```

**Success Criteria:**
- ✅ Command callable from shell
- ✅ Returns JSON matching HTTP API response
- ✅ Exit code 0 on success, non-zero on failure
- ✅ Stderr carries error messages (no HTTPException leaks)
- ✅ Works offline (doesn't require API server)

---

## Conclusion

A CLI wrapper for ACAT is **both beneficial AND constructive** because:

1. **Necessary:** Empirica-ACAT observable linkage requires it
2. **Simple:** ~4 hours of argparse wrapper work
3. **Durable:** Single source of truth (core logic)
4. **Auditable:** Shell invocations are traceable
5. **Scalable:** Foundation practices can adopt without HTTP setup

**Recommendation:** Include ACAT CLI wrapper in the Collab A deliverable for humanaios (Phase 1a, Week 1, parallel with SER 1 creation).

---

**Status:** ✅ **Recommended for implementation**
