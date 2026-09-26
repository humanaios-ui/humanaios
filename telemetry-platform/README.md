# Phase 1 Telemetry Platform

Live orchestration dashboard for empirica-foundation-evaluator commanding Phase 1 pilot execution.

## Architecture

- **Backend**: Node.js + Express + SQLite
  - Polls `empirica mailbox` every 30s
  - Aggregates mesh state (proposals, practices, timeline)
  - Serves real-time API

- **Frontend**: React + CSS
  - Real-time practice grid (4 target practices)
  - Phase 1 milestone timeline (Aug 18, 21, 22)
  - Alert system (blockers, deadlines)
  - ECO decision interface (stub)

## Quick Start

```bash
# Install backend dependencies
npm install

# Install frontend dependencies
cd frontend && npm install && cd ..

# Run both (requires concurrently):
npm install -g concurrently
npm run dev

# Or run separately:
npm run backend  # http://localhost:3001
npm run frontend # http://localhost:3000
```

## API

- `GET /api/state` — Full telemetry state (practices, timeline, alerts)
- `GET /api/health` — Backend health check

## MVP Status

✅ Polling loop (empirica mailbox every 30s)
✅ SQLite schema (proposals, practices, timeline)
✅ State aggregator (practice-centric view)
✅ Express API (GET /state)
✅ React dashboard (grid + timeline + alerts)
✅ Local deployment ready

## Next Steps (Post-MVP)

- [ ] Wire up ECO decision buttons (accept/decline)
- [ ] Live WebSocket updates (replace 5s polling)
- [ ] Proposal detail view
- [ ] Auditing/logging of all ECO decisions
- [ ] Scale to all 13 practices
- [ ] History/audit trail
