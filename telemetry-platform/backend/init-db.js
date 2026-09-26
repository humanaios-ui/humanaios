/**
 * Database initialization script for Analytics Step 2 telemetry platform
 * Creates three measurement tables and indexes
 */

import sqlite3 from 'sqlite3';

const DB_PATH = './telemetry.db';

export async function initAnalyticsDB() {
  return new Promise((resolve, reject) => {
    const db = new sqlite3.Database(DB_PATH);

    db.serialize(() => {
      // Create Phase 1 tables (compatibility)
      db.run(`CREATE TABLE IF NOT EXISTS practices (
        id TEXT PRIMARY KEY,
        name TEXT,
        role TEXT,
        status TEXT,
        health TEXT,
        know REAL,
        do REAL,
        context REAL,
        completion REAL,
        impact REAL,
        last_updated DATETIME
      )`);

      db.run(`CREATE TABLE IF NOT EXISTS proposals (
        id TEXT PRIMARY KEY,
        source_claude TEXT,
        target_practice TEXT,
        title TEXT,
        type TEXT,
        status TEXT,
        created_at DATETIME,
        updated_at DATETIME
      )`);

      db.run(`CREATE TABLE IF NOT EXISTS timeline (
        id TEXT PRIMARY KEY,
        date TEXT,
        event TEXT,
        status TEXT
      )`);

      // Create Phase 2 Analytics tables
      db.run(`CREATE TABLE IF NOT EXISTS orchestration_events (
        id TEXT PRIMARY KEY,
        proposal_id TEXT NOT NULL,
        event_type TEXT NOT NULL,
        source_claude TEXT NOT NULL,
        target_claudes TEXT NOT NULL,
        status TEXT NOT NULL,
        action_category TEXT,
        emitted_at DATETIME NOT NULL,
        received_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        latency_ms INTEGER,
        proposal_title TEXT,
        payload_summary TEXT,
        eco_actor TEXT,
        change_kind TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        created_by TEXT,
        cortex_project_id TEXT
      )`);

      db.run(`CREATE INDEX IF NOT EXISTS idx_orchestration_events_proposal_id
        ON orchestration_events(proposal_id)`);
      db.run(`CREATE INDEX IF NOT EXISTS idx_orchestration_events_status
        ON orchestration_events(status)`);
      db.run(`CREATE INDEX IF NOT EXISTS idx_orchestration_events_latency
        ON orchestration_events(latency_ms)`);

      db.run(`CREATE TABLE IF NOT EXISTS ser_coordination (
        id TEXT PRIMARY KEY,
        ser_id TEXT NOT NULL UNIQUE,
        ser_title TEXT,
        ser_state TEXT NOT NULL,
        participants TEXT NOT NULL,
        escalation_enabled BOOLEAN DEFAULT 1,
        escalation_interval_seconds INTEGER DEFAULT 600,
        last_escalation_at DATETIME,
        escalation_count INTEGER DEFAULT 0,
        idle_for_seconds INTEGER,
        last_transition_at DATETIME,
        last_transition_actor TEXT,
        transition_history TEXT,
        total_participants INTEGER,
        acked_participants INTEGER,
        required_participants_acked BOOLEAN,
        visibility TEXT DEFAULT 'private',
        project_ids TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        created_by TEXT,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )`);

      db.run(`CREATE INDEX IF NOT EXISTS idx_ser_coordination_ser_id
        ON ser_coordination(ser_id)`);
      db.run(`CREATE INDEX IF NOT EXISTS idx_ser_coordination_state
        ON ser_coordination(ser_state)`);
      db.run(`CREATE INDEX IF NOT EXISTS idx_ser_coordination_escalation_enabled
        ON ser_coordination(escalation_enabled) WHERE escalation_enabled = 1`);

      db.run(`CREATE TABLE IF NOT EXISTS blocker_routing (
        id TEXT PRIMARY KEY,
        blocker_id TEXT NOT NULL UNIQUE,
        blocker_title TEXT NOT NULL,
        description TEXT,
        blocker_type TEXT NOT NULL,
        priority TEXT NOT NULL DEFAULT 'medium',
        category TEXT,
        source_practice TEXT NOT NULL,
        affected_practices TEXT NOT NULL,
        assigned_to TEXT,
        escalated_to TEXT,
        status TEXT NOT NULL DEFAULT 'open',
        status_changed_at DATETIME,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        acknowledged_at DATETIME,
        resolution_started_at DATETIME,
        resolved_at DATETIME,
        acknowledge_latency_ms INTEGER,
        resolution_latency_ms INTEGER,
        related_ser_id TEXT,
        related_proposal_id TEXT,
        resolution_notes TEXT,
        practices_labor_hours REAL
      )`, (err) => {
        if (err) {
          reject(err);
        } else {
          // Create indexes for blocker table
          db.run(`CREATE INDEX IF NOT EXISTS idx_blocker_routing_blocker_id
            ON blocker_routing(blocker_id)`);
          db.run(`CREATE INDEX IF NOT EXISTS idx_blocker_routing_status
            ON blocker_routing(status)`);
          db.run(`CREATE INDEX IF NOT EXISTS idx_blocker_routing_priority
            ON blocker_routing(priority)`);
          db.run(`CREATE INDEX IF NOT EXISTS idx_blocker_routing_open_unacked
            ON blocker_routing(status, acknowledged_at)
            WHERE status = 'open' AND acknowledged_at IS NULL`, (err) => {
              if (err) reject(err);
              else {
                console.log('✅ Database initialized with all tables');
                resolve();
                db.close();
              }
            }
          );
        }
      });
    });
  });
}

// Run initialization if called directly
if (process.argv[1] === new URL(import.meta.url).pathname) {
  initAnalyticsDB()
    .then(() => {
      console.log('✅ Analytics telemetry database initialized');
      process.exit(0);
    })
    .catch((err) => {
      console.error('❌ Failed to initialize database:', err);
      process.exit(1);
    });
}
