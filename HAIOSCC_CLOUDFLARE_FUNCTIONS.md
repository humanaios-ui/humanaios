# HAIOSCC Cloudflare Functions — Observation Post API

**Status:** Implementation specification for Days 5-6 (Week 1)

**Environment:** Cloudflare Pages Functions (serverless)

**Database:** Supabase project `ksinisdzgtnqzsymhfya`

---

## Architecture

Three Cloudflare Functions + 1 scheduled cron handle the observation post:

| Function | Endpoint | Method | Purpose |
|---|---|---|---|
| `state.ts` | `/api/state/*` | GET | Read operational state (dashboard hydration) |
| `metrics.ts` | `/api/metrics/update` | POST | Ingest SMAG/Copilot/Gate measurements |
| `escalations.ts` | `/api/escalation/verify` | POST, GET | Check SER escalation rules + notify |
| (cron) | — | — | 15-min auto-verification loop |

---

## 1. Setup: `wrangler.toml`

```toml
# Root of HAIOSCC repo

name = "haioscc"
main = "src/index.ts"
compatibility_date = "2026-01-01"
compatibility_flags = ["nodejs_compat"]

[[env]]
name = "production"
routes = [
  { pattern = "haioscc.pages.dev/*", zone_id = "..." }
]

[env.production.vars]
SUPABASE_URL = "https://ksinisdzgtnqzsymhfya.supabase.co"
ENVIRONMENT = "production"

[[env.production.r2_buckets]]
binding = "ARCHIVE_BUCKET"
bucket_name = "haioscc-archive"

[[triggers.crons]]
cron = "*/15 * * * *"

[[env.production.env]]
SUPABASE_SERVICE_ROLE_KEY = { secret = true }
GITHUB_TOKEN = { secret = true }
CF_API_TOKEN = { secret = true }
CF_ZONE_ID = { secret = true }
CF_ACCOUNT_ID = { secret = true }
```

---

## 2. Function: `state.ts`

Hydrates dashboard by reading current operational state.

```typescript
// src/functions/state.ts

import { Router, createCors } from "itty-router";
import { createClient } from "@supabase/supabase-js";

const router = Router();
const { preflight, corsify } = createCors();

interface Env {
  SUPABASE_URL: string;
  SUPABASE_SERVICE_ROLE_KEY: string;
}

async function getOperationalState(env: Env) {
  const supabase = createClient(
    env.SUPABASE_URL,
    env.SUPABASE_SERVICE_ROLE_KEY,
    {
      auth: { persistSession: false },
    }
  );

  // GET /api/state/operational
  const { data: opState, error: opError } = await supabase
    .from("operational_state")
    .select("*")
    .single();

  if (opError) throw opError;
  return opState;
}

async function getSERStatus(env: Env) {
  const supabase = createClient(
    env.SUPABASE_URL,
    env.SUPABASE_SERVICE_ROLE_KEY,
    {
      auth: { persistSession: false },
    }
  );

  // GET /api/state/ser - all SER 1-4 status
  const { data: sers, error } = await supabase
    .from("ser_status")
    .select("*")
    .order("ser_num");

  if (error) throw error;
  return sers;
}

async function getLayerMetrics(env: Env) {
  const supabase = createClient(
    env.SUPABASE_URL,
    env.SUPABASE_SERVICE_ROLE_KEY,
    {
      auth: { persistSession: false },
    }
  );

  // GET /api/state/layers - latest from each layer
  const [layer1, layer2, layer3, harmony] = await Promise.all([
    supabase
      .from("layer_1_metrics")
      .select("*")
      .order("measurement_date", { ascending: false })
      .limit(1)
      .single(),
    supabase
      .from("layer_2_copilot")
      .select("*")
      .order("measurement_date", { ascending: false })
      .limit(1)
      .single(),
    supabase
      .from("layer_3_gates")
      .select("*")
      .order("gate_num", { ascending: false })
      .limit(3),
    supabase
      .from("three_layer_harmony")
      .select("*")
      .order("measurement_date", { ascending: false })
      .limit(1)
      .single(),
  ]);

  return {
    layer1: layer1.data || null,
    layer2: layer2.data || null,
    layer3: layer3.data || null,
    harmony: harmony.data || null,
  };
}

async function getPendingEscalations(env: Env) {
  const supabase = createClient(
    env.SUPABASE_URL,
    env.SUPABASE_SERVICE_ROLE_KEY,
    {
      auth: { persistSession: false },
    }
  );

  // GET /api/state/escalations - alert the dashboard
  const { data: escalations, error } = await supabase
    .from("escalations")
    .select("*, ser:ser_status(name)")
    .eq("status", "pending")
    .lt("escalation_deadline", new Date().toISOString())
    .order("escalation_deadline");

  if (error) throw error;
  return escalations;
}

// Routes
router.get("/api/state/operational", async (_, env: Env) => {
  const data = await getOperationalState(env);
  return new Response(JSON.stringify(data), {
    headers: { "Content-Type": "application/json" },
  });
});

router.get("/api/state/ser", async (_, env: Env) => {
  const data = await getSERStatus(env);
  return new Response(JSON.stringify(data), {
    headers: { "Content-Type": "application/json" },
  });
});

router.get("/api/state/layers", async (_, env: Env) => {
  const data = await getLayerMetrics(env);
  return new Response(JSON.stringify(data), {
    headers: { "Content-Type": "application/json" },
  });
});

router.get("/api/state/escalations", async (_, env: Env) => {
  const data = await getPendingEscalations(env);
  return new Response(JSON.stringify(data), {
    headers: { "Content-Type": "application/json" },
  });
});

router.options("*", preflight);
router.all("*", corsify);

export default router;
```

---

## 3. Function: `metrics.ts`

Ingests measurements from empirica CLI + Copilot signals.

```typescript
// src/functions/metrics.ts

import { createClient } from "@supabase/supabase-js";

interface MetricsPayload {
  source: "empirica_cli" | "copilot_api" | "acat_api";
  measurement_date: string;
  layer_1?: {
    smag_raw: number;
    smag_adjusted: number;
    copilot_avg_confidence: number;
    trajectory_count: number;
  };
  layer_2?: {
    avg_confidence: number;
    bias_audit_status: string;
    criterion_4_bias_score: number;
    model_variance_r_raw: Record<string, number>;
    model_variance_r_adjusted?: Record<string, number>;
  };
  gate?: {
    gate_num: number;
    measured_outcome: string;
    gap_analysis?: string;
  };
}

export async function POST(request: Request, env: any) {
  const supabase = createClient(
    env.SUPABASE_URL,
    env.SUPABASE_SERVICE_ROLE_KEY,
    {
      auth: { persistSession: false },
    }
  );

  const payload: MetricsPayload = await request.json();

  try {
    if (payload.source === "empirica_cli" && payload.layer_1) {
      // Ingest Layer 1 metrics (Monday 9am snapshot)
      const { error } = await supabase.from("layer_1_metrics").insert({
        measurement_date: payload.measurement_date,
        smag_learning_density_raw: payload.layer_1.smag_raw,
        smag_learning_density_adjusted: payload.layer_1.smag_adjusted,
        copilot_confidence_avg: payload.layer_1.copilot_avg_confidence,
        trajectory_count: payload.layer_1.trajectory_count,
        on_track_for_gate:
          payload.layer_1.smag_adjusted >= 40, // Adjust per gate
      });

      if (error) throw error;

      // Create weekly snapshot entry
      const snapshotDate = new Date(payload.measurement_date);
      snapshotDate.setDate(snapshotDate.getDate() - snapshotDate.getDay()); // Mon
      await supabase
        .from("weekly_snapshots")
        .upsert(
          {
            snapshot_date: snapshotDate.toISOString().split("T")[0],
            snapshot_type: "monday_9am",
            layer_1_snapshot: {
              raw: payload.layer_1.smag_raw,
              adjusted: payload.layer_1.smag_adjusted,
            },
          },
          { onConflict: "snapshot_date,snapshot_type" }
        );
    } else if (payload.source === "copilot_api" && payload.layer_2) {
      // Ingest Layer 2 metrics
      const { error } = await supabase.from("layer_2_copilot").upsert(
        {
          measurement_date: payload.measurement_date,
          avg_confidence: payload.layer_2.avg_confidence,
          bias_audit_status: payload.layer_2.bias_audit_status,
          criterion_4_bias_score: payload.layer_2.criterion_4_bias_score,
          model_variance_r_raw: payload.layer_2.model_variance_r_raw,
          model_variance_r_adjusted:
            payload.layer_2.model_variance_r_adjusted || null,
        },
        { onConflict: "measurement_date" }
      );

      if (error) throw error;

      // Auto-escalate if confidence < 0.70 for 7+ days
      if (payload.layer_2.avg_confidence < 0.7) {
        const escalationDeadline = new Date();
        escalationDeadline.setDate(escalationDeadline.getDate() + 7);

        await supabase
          .from("escalations")
          .upsert(
            {
              ser_id: 4, // SER 4 = Copilot Intelligence Coordination
              trigger_rule: "copilot_confidence<0.70",
              triggered_at: new Date().toISOString(),
              escalation_deadline: escalationDeadline.toISOString(),
              escalation_target: "Admiral",
              status: "pending",
            },
            { onConflict: "ser_id,trigger_rule" }
          );
      }
    } else if (payload.gate) {
      // Ingest Gate outcome
      const { error } = await supabase
        .from("layer_3_gates")
        .update({
          measured_outcome: payload.gate.measured_outcome,
          gap_analysis: payload.gate.gap_analysis || null,
          status: "postflight_ready", // Ready for Admiral POSTFLIGHT
        })
        .eq("gate_num", payload.gate.gate_num);

      if (error) throw error;
    }

    return new Response(JSON.stringify({ ok: true }), { status: 200 });
  } catch (error: any) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
    });
  }
}
```

---

## 4. Function: `escalations.ts`

Automatic escalation verification + notification.

```typescript
// src/functions/escalations.ts

import { createClient } from "@supabase/supabase-js";

export async function GET(request: Request, env: any) {
  const supabase = createClient(
    env.SUPABASE_URL,
    env.SUPABASE_SERVICE_ROLE_KEY,
    {
      auth: { persistSession: false },
    }
  );

  // Cron job: verify all escalation deadlines (runs every 15 min)
  const now = new Date();

  // Find escalations that have passed deadline and are still pending
  const { data: overdue, error } = await supabase
    .from("escalations")
    .select("*")
    .eq("status", "pending")
    .lt("escalation_deadline", now.toISOString());

  if (error) throw error;

  // Mark as overdue
  if (overdue && overdue.length > 0) {
    await supabase
      .from("escalations")
      .update({ status: "overdue" })
      .in(
        "id",
        overdue.map((e) => e.id)
      );

    // TODO: Send notifications (Slack, email) for overdue escalations
    // Placeholder: log to system
    console.log(`⚠️ ${overdue.length} escalations OVERDUE`);
  }

  // Update SER escalation_deadline on ser_status for dashboard
  const { data: sers, error: serError } = await supabase
    .from("ser_status")
    .select("id, escalation_rule_days");

  if (serError) throw serError;

  for (const ser of sers || []) {
    const deadline = new Date();
    deadline.setDate(
      deadline.getDate() + (ser.escalation_rule_days || 14)
    );

    await supabase
      .from("ser_status")
      .update({ escalation_deadline: deadline.toISOString() })
      .eq("id", ser.id);
  }

  return new Response(
    JSON.stringify({ checked: overdue?.length || 0, ok: true }),
    { status: 200 }
  );
}
```

---

## 5. Cron Trigger: `wrangler.toml`

```toml
[[triggers.crons]]
cron = "*/15 * * * *"  # Every 15 minutes
```

When triggered, POST to `/api/escalation/verify` to run the verification loop.

---

## 6. Integration with Empirica CLI

**Monday 9am snapshot (SER 1):**

```bash
# At 9am Monday, Admiral runs:
empirica finding-log \
  --finding "SER 1 Monday Snapshot (Jul 21): SMAG 28% raw, 22% Copilot-adjusted. Copilot confidence 0.72 (target 0.75). Gate 1 POSTFLIGHT logged, learning incorporated. Three-layer harmony: GOOD." \
  --impact 0.8 \
  --visibility shared \
  --source claude \
  --epistem_provenance "search"
```

This triggers:
1. Empirica creates finding + trajectory
2. Cortex emits `finding_event` (observable event)
3. HAIOSCC listener (in extension or webhook) receives it
4. POST to `/api/metrics/update` with Layer 1 data
5. Dashboard hydrates new metrics

**Gate N POSTFLIGHT (immediately after gate closes):**

```bash
empirica finding-log \
  --finding "Gate 1 POSTFLIGHT: [Predicted/Measured/Gap/Learning/Action]" \
  --enabled-by "gate-1-postflight" \
  --informs "phase-1-planning" \
  --trajectory-type "gate_learning_→_next_gate_design" \
  --impact 0.9 \
  --cross-session \
  --visibility shared
```

This triggers:
1. HAIOSCC listener receives `gate_postflight` event
2. POST to `/api/metrics/update` with Layer 3 gate data
3. Dashboard updates "Gate N: POSTFLIGHT logged ✅"

---

## 7. Dashboard Tab Changes (UI Layer)

### Current Tabs (Zone-3 Operations)
- Zone 3 Queue
- Finance Pipeline
- Collaborators
- Verification Log

### New Tabs (Observation Post)
- **SER Status** (SER 1, 2, 3, 4 with escalation timers)
- **Three-Layer Metrics** (SMAG, Copilot, Gates side-by-side)
- **Weekly Rhythm** (Mon/Wed/Fri snapshots)
- **Gate POSTFLIGHT Log** (all gate decisions)
- **Corrections Ledger** (invalidated assumptions)
- **Escalations** (pending, overdue)

### SER Status Tab Example
```
SER 1: Research Execution
├─ Status: in_progress
├─ Participants: David Van Assche (required), DeMarius Lawson (participating)
├─ Last verified: 2 hours ago ✅
├─ Escalation deadline: Aug 5, 2026 (21 days from trigger)
├─ Last ack: David (Aug 1), DeMarius (Aug 3)
└─ Evidence: Gate 1 POSTFLIGHT logged, Phase 1 mobilization on track

SER 2: Collaborator Coordination
├─ Status: open
├─ Participants: David Van Assche (required), SER 2 lead (participating)
├─ Last verified: 4 days ago
├─ Escalation deadline: Aug 15, 2026 (14 days)
├─ Last ack: (none yet — David needs to ack)
└─ Alert: 🟡 Overdue ack — escalation pending
```

---

## 8. Implementation Timeline

| Day | Task | Responsible |
|---|---|---|
| **5 (Jul 22)** | Apply schema to Supabase | Supabase → confirm 16 tables created |
| **5** | Deploy Cloudflare Functions (state.ts, metrics.ts, escalations.ts) | Engineering |
| **5** | Connect HAIOSCC UI to `/api/state/*` endpoints | UI Engineering |
| **5** | Add new tabs (SER Status, Three-Layer Metrics, Escalations) | UI Engineering |
| **6 (Jul 23)** | Wire empirica CLI → HAIOSCC listener (via cortex event hook or webhook) | Engineering + Cortex integration |
| **6** | Test end-to-end: Monday snapshot → /api/metrics/update → dashboard | QA |
| **6** | Prepare Admiral handover doc + test run | Admiral + Support |
| **Aug 1** | Gate 1 closes → Admiral creates POSTFLIGHT → triggers dashboard update | Admiral |

---

## 9. Deployment Checklist

- [ ] Supabase schema applied (16 tables)
- [ ] RLS enabled (service role only)
- [ ] Seed data inserted (SER 1-4, integrations)
- [ ] Cloudflare Functions deployed + env vars set
- [ ] HAIOSCC UI updated with new tabs
- [ ] Empirica CLI integration wired (listener active)
- [ ] Cron job running (15-min loop)
- [ ] End-to-end test complete (snapshot → dashboard)
- [ ] Admiral briefing complete + acknowledged

---

**Status:** Ready for implementation (Days 5-6, Week 1)

**Next Stage:** Integration testing + Admiral activation (Aug 1)

