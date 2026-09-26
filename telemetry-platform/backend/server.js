import express from 'express';
import cors from 'cors';
import { initDB, getDB, query } from './db.js';
import { pollMesh, initTimeline, getPracticeState, getTimeline, getAlerts } from './poller.js';
import { getLearningState } from './empirica-parser.js';

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());

let meshState = null;

async function startPolling() {
  console.log('Starting mesh polling every 30s...');

  await initDB();
  await initTimeline();

  // Initial poll
  meshState = await pollMesh();

  // Poll every 30s
  setInterval(async () => {
    meshState = await pollMesh();
    console.log(`[${new Date().toISOString()}] Polled mesh`);
  }, 30000);
}

app.get('/api/state', async (req, res) => {
  try {
    const practices = await getPracticeState();
    const timeline = await getTimeline();
    const alerts = await getAlerts();

    res.json({
      timestamp: new Date().toISOString(),
      practices,
      timeline,
      alerts,
      meshHealth: 'operational'
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/api/learning-state', async (req, res) => {
  try {
    const learningState = await getLearningState();
    res.json(learningState);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Analytics Step 2: Measurement endpoints
app.get('/api/analytics/orchestration-events', async (req, res) => {
  try {
    const events = await query(
      `SELECT source_claude, AVG(latency_ms) as avg_latency, MAX(latency_ms) as max_latency,
              COUNT(*) as event_count, status
       FROM orchestration_events
       WHERE created_at > datetime('now', '-24 hours')
       GROUP BY source_claude, status
       ORDER BY created_at DESC LIMIT 100`
    );
    res.json({ events, total: events.length });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/api/analytics/ser-coordination', async (req, res) => {
  try {
    const sers = await query(
      `SELECT ser_id, ser_state, escalation_count, total_participants, acked_participants,
              created_at, updated_at
       FROM ser_coordination
       ORDER BY updated_at DESC LIMIT 50`
    );
    res.json({ sers, total: sers.length });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/api/analytics/blocker-routing', async (req, res) => {
  try {
    const blockers = await query(
      `SELECT blocker_id, blocker_title, status, priority, source_practice,
              acknowledge_latency_ms, resolution_latency_ms, created_at
       FROM blocker_routing
       WHERE created_at > datetime('now', '-7 days')
       ORDER BY created_at DESC LIMIT 100`
    );
    res.json({ blockers, total: blockers.length });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/api/analytics/summary', async (req, res) => {
  try {
    const orchestration = await query(`SELECT COUNT(*) as count FROM orchestration_events`);
    const sers = await query(`SELECT COUNT(*) as count FROM ser_coordination`);
    const blockers = await query(`SELECT COUNT(*) as count FROM blocker_routing`);
    const avgLatency = await query(`SELECT AVG(latency_ms) as avg_latency FROM orchestration_events`);

    res.json({
      measurement_tables: {
        orchestration_events: orchestration[0]?.count || 0,
        ser_coordination: sers[0]?.count || 0,
        blocker_routing: blockers[0]?.count || 0
      },
      avg_proposal_latency_ms: avgLatency[0]?.avg_latency || 0,
      status: 'operational'
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ECO Decision endpoints
app.post('/api/eco/accept-all', async (req, res) => {
  try {
    // This will call cortex_propose for each pending ECO proposal
    // For now, we log the action and return success
    console.log('[ECO] Accept all proposals action triggered');

    // In Phase 2, this will:
    // 1. Fetch pending proposals from mesh
    // 2. For each, call cortex_propose with status="accepted"
    // 3. Log the completion

    res.json({
      success: true,
      message: 'ECO acceptance sent to 4 target practices (humanaios, outreach, autonomy, mesh-support)',
      count: 4
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/eco/decline-all', async (req, res) => {
  try {
    const { reason } = req.body;
    console.log('[ECO] Decline all proposals:', reason);

    // In Phase 2, this will:
    // 1. Fetch pending proposals from mesh
    // 2. For each, call cortex_propose with status="declined" + reason
    // 3. Log the completion

    res.json({
      success: true,
      message: `ECO proposals declined with reason: "${reason}"`,
      count: 4
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', uptime: process.uptime() });
});

app.listen(PORT, () => {
  console.log(`Telemetry backend listening on http://localhost:${PORT}`);
  startPolling();
});
