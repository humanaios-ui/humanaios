import { exec } from 'child_process';
import { promisify } from 'util';
import { run, query } from './db.js';

const execAsync = promisify(exec);

const TARGET_PRACTICES = [
  { id: 'empirica-foundation.carly.humanaios', name: 'humanaios', role: 'Phase 1 Pilot Lead' },
  { id: 'empirica-foundation.carly.empirica-outreach', name: 'outreach', role: 'Audit Lead' },
  { id: 'empirica-foundation.carly.empirica-autonomy', name: 'autonomy', role: 'Calibration' },
  { id: 'empirica-foundation.carly.empirica-mesh-support', name: 'mesh-support', role: 'Governance' },
];

const MILESTONES = [
  { date: '2026-08-18', event: 'Target practices respond', status: 'pending' },
  { date: '2026-08-21', event: 'Audit deadline (outreach)', status: 'pending' },
  { date: '2026-08-22', event: 'Phase 2 gate decision', status: 'pending' },
];

export async function initTimeline() {
  for (const milestone of MILESTONES) {
    await run(
      `INSERT OR IGNORE INTO timeline (id, date, event, status) VALUES (?, ?, ?, ?)`,
      [`milestone_${milestone.event}`, milestone.date, milestone.event, milestone.status]
    );
  }
}

export async function pollMesh() {
  try {
    const { stdout } = await execAsync(
      'empirica mailbox poll --ai-id empirica-foundation-evaluator --output json'
    );

    const data = JSON.parse(stdout);

    if (data.proposals) {
      for (const proposal of data.proposals) {
        const target = TARGET_PRACTICES.find(p => p.id === proposal.target_claudes?.[0]);
        if (target) {
          await run(
            `INSERT OR REPLACE INTO proposals
             (id, source_claude, target_practice, title, type, status, created_at, updated_at)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
            [
              proposal.id,
              proposal.source_claude,
              target.name,
              proposal.title,
              proposal.type,
              proposal.status,
              new Date(proposal.created_at).toISOString(),
              new Date().toISOString()
            ]
          );
        }

        // Analytics Step 2: Track proposal as orchestration event
        await trackOrchestrationEvent(proposal);
      }
    }

    // Analytics Step 2: Poll and track SER state
    await pollSERState();

    // Analytics Step 2: Poll and track blocker status
    await pollBlockerStatus();

    return data;
  } catch (err) {
    console.error('Poll error:', err.message);
    return null;
  }
}

async function trackOrchestrationEvent(proposal) {
  try {
    const emittedAt = new Date(proposal.created_at);
    const receivedAt = new Date();
    const latencyMs = receivedAt - emittedAt;

    const eventId = `event_${proposal.id}_${Date.now()}`;

    await run(
      `INSERT OR REPLACE INTO orchestration_events
       (id, proposal_id, event_type, source_claude, target_claudes, status, action_category,
        emitted_at, received_at, latency_ms, proposal_title, eco_actor, created_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      [
        eventId,
        proposal.id,
        proposal.type || 'proposal_event',
        proposal.source_claude,
        JSON.stringify(proposal.target_claudes || []),
        proposal.status,
        proposal.action_category || 'OPERATIONAL',
        emittedAt.toISOString(),
        receivedAt.toISOString(),
        latencyMs,
        proposal.title,
        proposal.eco_actor,
        receivedAt.toISOString()
      ]
    );
  } catch (err) {
    console.error('Error tracking orchestration event:', err.message);
  }
}

async function pollSERState() {
  try {
    // Poll empirica mailbox for SER-related events
    const { stdout } = await execAsync(
      'empirica mailbox sers --output json 2>/dev/null || echo "{}"'
    );

    const sers = JSON.parse(stdout || '{}');

    if (sers && typeof sers === 'object') {
      for (const [serId, serData] of Object.entries(sers)) {
        if (!serData) continue;

        const id = `ser_${serId}_${Date.now()}`;

        await run(
          `INSERT OR REPLACE INTO ser_coordination
           (id, ser_id, ser_title, ser_state, participants, escalation_enabled,
            escalation_count, total_participants, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
          [
            id,
            serId,
            serData.title || serId,
            serData.state || 'unknown',
            JSON.stringify(serData.participants || []),
            serData.escalation_enabled ? 1 : 0,
            serData.escalation_count || 0,
            (serData.participants || []).length,
            new Date().toISOString(),
            new Date().toISOString()
          ]
        );
      }
    }
  } catch (err) {
    console.error('Error polling SER state:', err.message);
  }
}

async function pollBlockerStatus() {
  try {
    // Poll empirica findings/unknowns for blocker tracking
    const { stdout } = await execAsync(
      'empirica project-search --task "blocker" --type unknown --limit 5 --output json 2>/dev/null || echo "{}"'
    );

    const blockers = JSON.parse(stdout || '{}');

    if (blockers && blockers.docs) {
      for (const blocker of blockers.docs) {
        if (!blocker.id) continue;

        const blockerId = `blocker_${blocker.id}`;

        await run(
          `INSERT OR IGNORE INTO blocker_routing
           (id, blocker_id, blocker_title, description, blocker_type, priority,
            source_practice, affected_practices, status, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
          [
            `${blockerId}_${Date.now()}`,
            blockerId,
            blocker.title || 'Unknown Blocker',
            blocker.description || '',
            'dependency',
            'medium',
            'empirica-foundation-evaluator',
            JSON.stringify(['empirica-foundation-evaluator']),
            'open',
            new Date().toISOString()
          ]
        );
      }
    }
  } catch (err) {
    console.error('Error polling blocker status:', err.message);
  }
}

export async function getPracticeState() {
  const proposals = await query(`
    SELECT target_practice, type, status, COUNT(*) as count
    FROM proposals
    GROUP BY target_practice, status
  `);

  const state = {};
  for (const practice of TARGET_PRACTICES) {
    state[practice.name] = {
      id: practice.id,
      name: practice.name,
      role: practice.role,
      proposals: proposals.filter(p => p.target_practice === practice.name),
    };
  }

  return state;
}

export async function getTimeline() {
  return await query('SELECT * FROM timeline ORDER BY date');
}

export async function getAlerts() {
  const proposals = await query(`
    SELECT * FROM proposals WHERE status IN ('eco_review', 'failed') ORDER BY updated_at DESC
  `);

  const alerts = [];

  if (proposals.some(p => p.status === 'eco_review')) {
    alerts.push({
      level: 'high',
      message: `${proposals.filter(p => p.status === 'eco_review').length} proposals awaiting ECO decision`,
      type: 'blocker'
    });
  }

  const auditDeadline = new Date('2026-08-21');
  const now = new Date();
  const daysUntil = Math.ceil((auditDeadline - now) / (1000 * 60 * 60 * 24));

  if (daysUntil <= 4 && daysUntil > 0) {
    alerts.push({
      level: 'high',
      message: `Audit deadline in ${daysUntil} days (Aug 21)`,
      type: 'deadline'
    });
  }

  return alerts;
}
