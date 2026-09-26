# Observability Control Room — Integration Guide

**Date:** 2026-07-20  
**Phase:** Option A → Option C Architecture  
**Status:** Ready to test  

---

## What You Have

### **1. Mesh-to-Music Mapping** (`mesh-to-music.js`)
- Converts Supabase `mesh_state` → 13 epistemic vectors → Strudel patterns
- 5 mood presets: Focus, Energize, Reflect, Debug, Celebrate
- Real-time pattern generation based on governance metrics
- Crossfade interpolation for smooth transitions

### **2. Observability Control Room** (`ControlRoom.html`)
- **Left side (visual):** Witness V2 — 6D skull, decision queue, dispatch comet, data core
- **Right side (audio):** Epistemic DJ + Strudel REPL + mesh metrics
- **Shared layer:** Real-time Supabase subscriptions (mesh_state, pending_decisions, ratified_decisions)
- **Admiral controls:** 6 vector sliders for manual pattern tweaking
- **Mood system:** 5 presets + auto-generation from live mesh data

---

## Quick Start

### Step 1: Verify Dependencies

All files are in place:

```bash
# Verify files exist
ls -la docs/mesh-to-music.js           # ✅ mapping logic
ls -la docs/ControlRoom.html           # ✅ unified dashboard
ls -la docs/WitnessV2.html             # ✅ reference (already working)
```

### Step 2: Open the Control Room

```bash
# Option A: Local file (development)
open docs/ControlRoom.html

# Option B: Serve via HTTP (production)
cd docs && python3 -m http.server 8000
# Then: http://localhost:8000/ControlRoom.html
```

### Step 3: Verify Real-Time Connection

**Expected behavior on load:**

1. **Status indicator** (top-right): "Connecting..." → "Connected"
2. **Witness V2** (left side):
   - 6D skull appears with current mesh state
   - Outer arc shows decision queue pressure
   - Comet rotates based on dispatch cadence
   - Breath ring pulses at governance heartbeat
3. **Epistemic DJ** (right side):
   - Strudel code auto-generated from mesh state
   - Metrics display shows:
     - Pending decisions: 0 (or current count)
     - High severity: 0 (or current count)
     - Ratified/Applied: 10/1 (from REGISTERED.md bootstrap)
     - Mesh health: 86% (from mean_li = 0.8632)
     - Field state: "Calibrated"

---

## Features

### Visual: Witness V2 (Left Side)

**What it shows:**
- **6D Epistemic Skull:** vectors (know, do, context, clarity, coherence, signal) as radii
- **Outer Arc:** Decision queue fill (gap = pending decisions waiting)
- **Comet:** Rotating indicator of dispatch cadence
- **Breath Ring:** Pulsing discovery cycle at governance heartbeat frequency
- **Data Core:** Central activity glow (intensity = mesh engagement)

**Responsive to:** mesh_state updates from Supabase (real-time WebSocket)

### Audio: Epistemic DJ (Right Side)

**What it generates:**
- **Drums:** Engagement + Coherence → rhythm pattern (8-16 notes per bar)
- **Bass:** Completion + Uncertainty → pitch/speed modulation
- **Melody:** Know + Clarity → scale selection (pentatonic-major to diminished)
- **Reverb:** Livelihood Index → room size/immersion

**Mapping logic:**
- **High engagement + coherence** = locked groove (bd(8) hh(16))
- **High completion + low uncertainty** = resolved bass (bass:2 bass:3 bass:5)
- **High know/clarity** = pentatonic major (stable melodic sense)
- **Low know/clarity** = diminished (chaotic/exploratory)

### Controls: Epistemic DJ Interface (Right Side)

#### Mood Presets
```
[Focus] [Energize] [Reflect] [Debug] [Celebrate] [Auto]
```

Click any preset to lock in those epistemic vectors. Click **Auto** to return to real-time mesh state tracking.

**What each preset sounds like:**
- **Focus:** High clarity, low uncertainty, moderate engagement → clear, stable pattern
- **Energize:** High engagement, moderate uncertainty → driving, intense rhythm
- **Reflect:** Lower engagement, moderate uncertainty → sparse, exploratory pattern
- **Debug:** Low know, high uncertainty, high engagement → chaotic, searching pattern
- **Celebrate:** All vectors high → triumphant, fully present pattern

#### Vector Sliders (Manual Tweaking)
```
know:       [████░] 0.77
do:         [████░] 0.79
clarity:    [████░] 0.78
coherence:  [████░] 0.76
engagement: [████░] 0.80
uncertainty:[███░░] 0.30
```

- Drag any slider to manually override that vector
- **Strudel code regenerates in real-time**
- Remains locked until you click **"Regenerate from Mesh"**
- Admiral can experiment with "what if coherence was higher?"

#### Strudel REPL
```javascript
// Epistemic DJ: Governance State Pattern
// Generated from mesh state: pending=0, high=0, applied=1

setcps(0.65)  // Tempo: 120 BPM

// Drums (engagement: 0.80, coherence: 0.76)
d0 > sound("bd(4) hh(12)")

// Bass (completion: 0.50, uncertainty: 0.30)
d1 > sound("bass:1 bass:4").speed(1.00)

// Melody (know: 0.77, clarity: 0.78)
d2 > sound("square:8").scale("major")

// Effects
d0 > rev(0.69)
d1 > rev(0.35)
d2 > rev(0.69)
```

- **Copy Strudel Code:** Copies to clipboard, paste into https://strudel.cc
- **Regenerate from Mesh:** Abandon manual edits, return to auto-generation
- **Open in Strudel.cc:** Opens new browser tab with pattern pre-loaded

### Mesh Metrics (Right Side, Bottom)

```
Pending Decisions     0
High Severity         0
Ratified / Applied    100%
Mesh Health           86%
Field State           Calibrated
Live Updates          ⚫ Supabase (pulsing)
```

These update in real-time as mesh_state changes in Supabase.

---

## How It Works (Architecture)

### Data Flow

```
Supabase Database (PostgreSQL)
    ↓ (WebSocket subscription)
  mesh_state table (realtime)
    ↓
ControlRoom.html
    ├→ Witness V2 (left canvas)
    │    └→ drawWitness() uses: know, do, context, clarity, coherence, signal
    │
    └→ Epistemic DJ (right panel)
         ├→ MeshToMusic.meshStateToVectors()
         ├→ MeshToMusic.vectorsToStrudelPattern()
         └→ Strudel code displayed + stats updated
```

### Real-Time Updates

**Subscriptions active:**
1. `mesh_state` — Overall governance health (realtime enabled)
2. `pending_decisions` — Queue of awaiting decisions (realtime)
3. `ratified_decisions` — Ratified but not yet applied (realtime)

**Latency:**
- Supabase → browser: ~50-100ms (WebSocket)
- mesh_state change → visual/audio update: <500ms

### Manual Tweaking

When Admiral adjusts vector sliders:
1. Sliders lock manual mode (ignore mesh_state until reset)
2. MeshToMusic.vectorsToStrudelPattern() called with manual values
3. Strudel code regenerates
4. No changes to Supabase (purely local visualization)
5. Click "Regenerate from Mesh" to return to auto mode

---

## Testing Checklist

### Test 1: Verify Real-Time Connection

```bash
# Terminal 1: Open Control Room
open docs/ControlRoom.html

# Terminal 2: Check Supabase realtime
# (Witness top-right should show: "Connected")

# Terminal 3: Monitor Supabase activity
# Check logs for postgres_changes events
```

**Expected:** Connection status changes from "Connecting..." to "Connected" within 2-3 seconds.

### Test 2: Trigger Visual Update

```bash
# Add a pending decision to Supabase (manual insert)
# In Supabase Dashboard → SQL Editor:

INSERT INTO pending_decisions (
  decision_id, title, decision_type, scope, status
) VALUES (
  'test_decision_001',
  'Test: Admiral approval needed',
  'finding_registration',
  'Test scope',
  'PENDING'
);

# Witness should update:
# - Outer arc's gap widens (more queue pressure)
# - Comet rotates faster (higher urgency)
# - Strudel bass changes (uncertainty increases)
```

**Expected:** Visual and audio updates within <500ms.

### Test 3: Manual Vector Tweaking

```
1. Drag "engagement" slider all the way right (1.0)
2. Observe:
   - Witness rhythm becomes locked (bd(8) hh(16))
   - Strudel tempo increases (~140 BPM)
   - Breath ring breathes faster
3. Drag "uncertainty" slider left (0.1)
4. Observe:
   - Strudel scale becomes pentatonic major
   - Bass pattern resolves to "bass:2 bass:3 bass:5"
5. Click "Regenerate from Mesh" to return to real state
```

**Expected:** All changes immediate, reversible.

### Test 4: Mood Preset Activation

```
1. Click [Celebrate] preset
2. Observe:
   - All vectors jump to high (0.90+)
   - Witness becomes intensely present (high colors, intense pulsing)
   - Strudel code becomes triumphant (highest tempo, pentatonic major)
3. Adjust a single slider (e.g., engagement down to 0.5)
4. Observe:
   - Preset button deactivates (no longer highlighted)
   - Manual tweaking mode active
5. Click [Auto] to return to mesh-driven updates
```

**Expected:** Presets lock epistemic state; manual tweaking breaks the lock; [Auto] resets.

### Test 5: Copy & Paste Strudel Code

```
1. Click "Copy Strudel Code"
2. Browse to https://strudel.cc
3. Paste code into left editor
4. Click "▶️ Play"
5. Hear the governance state as music!
```

**Expected:** Code executes without syntax errors.

---

## Troubleshooting

### Connection Status Shows "Disconnected"

**Symptoms:** "Disconnected" label, no visual animation

**Diagnostics:**
```bash
# Check Supabase project status
curl -s https://ksinisdzgtnqzsymhfya.supabase.co/rest/v1/

# Check browser console for errors
# (F12 → Console tab)
```

**Fix:**
1. Verify Supabase project is active (Dashboard → Settings)
2. Verify `SUPABASE_ANON_KEY` in ControlRoom.html is correct (hardcoded in file)
3. Refresh browser
4. Check for CORS errors (Supabase → Settings → API → CORS allowed origins)

### Witness V2 Not Rendering

**Symptoms:** Black canvas, no skull/comet visible

**Diagnostics:**
```bash
# Check browser console for JavaScript errors
# (F12 → Console)
# Look for: "Cannot read property 'getContext' of null"
```

**Fix:**
1. Verify canvas exists: `document.getElementById('witness-canvas')` in console
2. Refresh page (canvas resize race condition)
3. Check that `mesh-to-music.js` loaded (check Network tab in DevTools)

### Strudel Code Not Updating

**Symptoms:** Strudel textarea stays blank or doesn't update

**Diagnostics:**
```bash
# In browser console, manually test:
> meshToMusic = new MeshToMusic()
> meshToMusic.vectorsToStrudelPattern({know: 0.77, ...})
# Should output Strudel code string
```

**Fix:**
1. Verify `mesh-to-music.js` is in same directory as `ControlRoom.html`
2. Check browser console for parse errors
3. Manually trigger regeneration: click "Regenerate from Mesh" button

### Real-Time Metrics Not Updating

**Symptoms:** Pending/High Severity counts stay at 0

**Diagnostics:**
```bash
# Check Supabase table directly:
# Dashboard → SQL Editor:
SELECT COUNT(*) FROM pending_decisions WHERE status = 'PENDING';
```

**Fix:**
1. Add test pending decision (see Test 2 above)
2. Verify WebSocket subscription is active (browser DevTools → Network → WS)
3. Check that `mesh_state` table exists and has data (Dashboard → Tables)

---

## Next: Phase 2 Enhancements

### Enhancement 1: Persistent Presets
Save Admiral's favorite vector combinations as custom presets (localStorage)

### Enhancement 2: Governance Timeline
Add time-series view showing mesh state history (6D vectors over past 24h)

### Enhancement 3: Governor Integration
Wire Admiral alerts to Slack when high-severity decisions appear in queue

### Enhancement 4: Export Patterns
Render Strudel patterns as audio files (.wav/.mp3) for offline listening

### Enhancement 5: Multi-Session Orchestration
Connect multiple Admirals' Control Rooms to the same mesh (shared WebSocket, collaborative tweaking)

---

## Files Summary

| File | Purpose |
|------|---------|
| `docs/mesh-to-music.js` | MeshToMusic class: mesh_state → vectors → Strudel patterns |
| `docs/ControlRoom.html` | Main dashboard: Witness V2 + Epistemic DJ + Strudel REPL |
| `docs/WitnessV2.html` | Standalone Witness visualization (reference) |
| `supabase/schema.sql` | Underlying database (mesh_state, pending_decisions, etc.) |
| `scripts/credential-sync.sh` | Manage workspace credentials (for Supabase access) |

---

## Credentials Used

**Hardcoded in ControlRoom.html:**
```javascript
SUPABASE_URL = 'https://ksinisdzgtnqzsymhfya.supabase.co';
SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...';  // (truncated)
```

These are **read-only** anon keys — only SELECT on public tables. Full credentials stored in workspace vault (`~/.empirica/workspace/secrets/`).

---

## What's Next

### Ready to test?
```bash
open docs/ControlRoom.html
# Should connect within 2-3 seconds, show live mesh state
```

### Want to enrich the data?
Insert remaining 45 findings from REGISTERED.md (see WITNESS_BOOTSTRAP_STATUS.md for SQL)

### Want to integrate with Admiral's workflow?
Set up Slack alerts, webhooks, or GitHub integration (see GitHub webhook section in WITNESS_BOOTSTRAP_STATUS.md)

---

**Status:** ✅ Control Room ready for testing  
**Next Action:** Open in browser, verify real-time connection  
**Support:** See troubleshooting above, or check Supabase logs for connection issues
