# Empirica Internal Agent — Phase 1 Infrastructure Setup

**Status:** Implementation Phase 1 (Bifrost Gateway + LangGraph)  
**Target Delivery:** Week 1 (July 31 - Aug 6, 2026)

## Overview

Deploy shared internal agent across Empirica foundation practices (autonomy, mesh-support, outreach). Agent runs in evaluator practice, orchestrated by Bifrost gateway and LangGraph engine. Uses Kimi K2.6 (planning) + Laguna M.1 (execution) models on OpenRouter.

## Setup Instructions

### Prerequisites

- Docker + Docker Compose installed
- Empirica CLI available (`empirica --version`)
- Python 3.8+ for LangGraph environment
- OpenRouter API key (set via environment variable, see below)

### Phase 1: Infrastructure Provisioning (Automated)

**Run the automated setup script:**

```bash
cd /Users/andersonfamily/practices/empirica-foundation-evaluator/agent

# Set OpenRouter API key (required for script to work)
export OPENROUTER_API_KEY="your-openrouter-api-key-here"

# Execute Phase 1 setup
./setup-phase1.sh
```

**What the script does:**

1. **P1.1: Provision Bifrost container**
   - Starts Docker container on port 8080
   - Creates data directory for persistence
   - Verifies container health

2. **P1.2: Configure OpenRouter credentials**
   - Exports API key from environment or script default
   - Tests connectivity to OpenRouter
   - Validates model availability

3. **P1.3: Register models with Bifrost**
   - Kimi K2.6: Planning/orchestration layer (262K context)
   - Laguna M.1: Execution/code generation layer (262K context)
   - Routing rules configured in `bifrost-config.yaml`

4. **P1.4: Register MCP servers**
   - Empirica CLI tools (finding-log, decision-log, etc.)
   - Cortex mesh communication (collab, propose)
   - File I/O for reading/writing in agent workspace

5. **P1.5: Deploy LangGraph orchestration**
   - Python virtual environment created
   - LangGraph + dependencies installed
   - ReAct loop template configured

6. **P1.6: Create agent identity**
   - Canonical 3-form: `empirica-foundation.carly.empirica-foundation-evaluator-agent`
   - Stored in `.agent-identity.json`
   - Registered for mesh communication

**Expected output:**

```
========================================
Phase 1 Setup: Internal Agent Infrastructure
========================================

[P1.1] Provisioning Bifrost container...
  ✓ Data directory ready
  ✓ OpenRouter API key loaded
  ✓ Bifrost container is running

[P1.2] Configuring OpenRouter credentials...
  ✓ Bifrost health check passed
  ✓ OpenRouter connectivity confirmed

[P1.3] Registering models with Bifrost...
  ✓ Kimi K2.6 (planning layer) configured
  ✓ Laguna M.1 (execution layer) configured

[P1.4] Registering MCP servers...
  ✓ Empirica CLI available
  ✓ MCP server configurations registered

[P1.5] Setting up LangGraph orchestration environment...
  ✓ Python virtual environment created
  ✓ LangGraph configuration created

[P1.6] Creating agent identity...
  ✓ Agent canonical 3-form: empirica-foundation.carly.empirica-foundation-evaluator-agent
  ✓ Agent identity stored

[VERIFY] Running verification tests...
  [Test 1] Bifrost gateway health... ✓ PASS
  [Test 2] Empirica CLI availability... ✓ PASS
  [Test 3] Model configuration... ✓ PASS

========================================
Phase 1 Setup COMPLETE
========================================
```

### Verification

After setup completes, verify components:

**1. Bifrost Gateway**
```bash
curl http://localhost:8080/health
# Should return: {"status":"ok"}
```

**2. Empirica CLI**
```bash
empirica --version
# Should return version info
```

**3. Model connectivity**
```bash
# Test via Bifrost (if curl is available)
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "moonshotai/kimi-k2.6", "messages": [{"role": "user", "content": "Hello"}]}'
```

**4. LangGraph environment**
```bash
source venv-agent/bin/activate
python -c "import langgraph; print(langgraph.__version__)"
```

## Configuration Files

### `docker-compose.yaml`
- Bifrost container orchestration
- Port mapping (8080)
- Volume mounting for persistence
- Health checks

### `bifrost-config.yaml`
- Model definitions (Kimi K2.6, Laguna M.1)
- OpenRouter provider configuration
- MCP server registration
- Rate limiting (free tier limits)
- Observability settings

### `setup-phase1.sh`
- Automated provisioning script
- Handles all 6 Phase 1 tasks
- Includes verification tests
- Generates setup log

## File Locations

| Component | Location | Purpose |
|---|---|---|
| Docker config | `agent/docker-compose.yaml` | Container orchestration |
| Bifrost config | `agent/bifrost-config.yaml` | Model + MCP routing |
| Setup script | `agent/setup-phase1.sh` | Automated provisioning |
| Runtime data | `.empirica/bifrost/data/` | Bifrost persistence (gitignored) |
| Python venv | `venv-agent/` | LangGraph environment |
| Agent config | `agent/langgraph_config.yaml` | LangGraph settings |
| Agent identity | `.agent-identity.json` | Mesh addressing |

## Troubleshooting

**Problem: Docker command not found**
```bash
# Ensure Docker is installed and running
docker --version
# Or use system Docker setup
```

**Problem: Bifrost health check fails**
```bash
# Check container logs
docker-compose logs -f bifrost

# Verify port 8080 is not in use
lsof -i :8080
```

**Problem: OpenRouter connectivity fails**
```bash
# Check API key is set
echo $OPENROUTER_API_KEY

# Test OpenRouter directly (outside Bifrost)
curl https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"
```

**Problem: Empirica CLI not found**
```bash
# Ensure empirica is installed and in PATH
which empirica

# If not in PATH, add to .bashrc or use full path
/usr/local/bin/empirica --version
```

## Next Steps

Once Phase 1 setup is complete:

1. **Phase 2 (Week 2):** Implement agent reasoning loop
   - ReAct loop in LangGraph
   - Artifact logging integration
   - Task decomposition (planning model)
   - Execution layer (code model)

2. **Phase 3 (Week 3+):** Production deployment
   - Request routing interface
   - Mesh communication (cortex_collab)
   - Multi-practice coordination
   - Monitoring + observability

## Support

- Bifrost docs: https://docs.getbifrost.ai
- LangGraph docs: https://langchain.com/langgraph
- OpenRouter models: https://openrouter.ai
- Empirica CLI: `empirica --help`

---

**Authority:** Admiral (Carly R. Anderson)  
**Status:** Phase 1 READY FOR EXECUTION  
**Last Updated:** 2026-07-30
