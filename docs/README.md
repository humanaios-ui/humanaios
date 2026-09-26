# Observability & Governance Documentation

**Central hub for real-time mesh state visualization, epistemic music generation, and Admiral controls.**

---

## 🧠 Witness V2 + Epistemic DJ: Observability Control Room

### Quick Links
- **[Control Room Dashboard](ControlRoom.html)** — Main interface (open this first)
- **[Witness V2 Standalone](WitnessV2.html)** — Visual-only version (reference)
- **[Setup & Testing Guide](OBSERVABILITY_CONTROL_ROOM_SETUP.md)** — How to deploy and test

### What It Does
**Dual-sensory governance observability:**
- **Left (Visual):** 6D epistemic skull + decision queue + dispatch comet
- **Right (Audio):** Strudel generative music patterns + Admiral control panel + mesh metrics

### Architecture
```
Supabase mesh_state (PostgreSQL)
    ↓ (WebSocket realtime)
ControlRoom.html
    ├→ Witness V2 (canvas visualization)
    └→ Epistemic DJ (generative music)
        └→ mesh-to-music.js (mapping logic)
```

### How to Start
```bash
# Open the main dashboard
open docs/ControlRoom.html

# Expected: connects to Supabase within 2-3 seconds, shows live mesh state
```

---

## 🎧 Epistemic DJ: Generative Music from Governance

### The Mapping
| Epistemic Vector | Audio Parameter | Effect |
|---|---|---|
| **know** | Scale consonance | pentatonic (high) → diminished (low) |
| **do** | Drum pattern coherence | locked groove ↔ scattered |
| **clarity** | Melody filter | bright ↔ dark |
| **coherence** | Rhythmic stability | stable ↔ chaotic |
| **engagement** | Tempo | 60–140 BPM |
| **uncertainty** | Pattern degradation | adds probability/mutation |
| **state** (LI) | Reverb/room size | intimate ↔ cathedral |

### Mood Presets
- **Focus:** High clarity + coherence, locked patterns, stable
- **Energize:** High engagement + impact, driving rhythm, intense
- **Reflect:** Lower engagement, sparse, exploratory
- **Debug:** Low know + high uncertainty, chaotic searching
- **Celebrate:** All vectors high, triumphant presence
- **Auto:** Real-time mesh tracking (default)

### How to Use
1. Open ControlRoom.html
2. Select mood preset or drag vector sliders
3. Read generated Strudel code
4. Click "Open in Strudel.cc" to hear it
5. Modify pattern live in Strudel, paste back into Control Room

---

## 📊 Real-Time Mesh Metrics

**Displayed in Control Room (bottom-right):**
- **Pending Decisions** — Currently awaiting Admiral approval
- **High Severity** — Urgent decisions requiring attention
- **Ratified / Applied** — Completion ratio of governance pipeline
- **Mesh Health** — Overall coherence (Livelihood Index)
- **Field State** — Calibrated | Power | Force Dominant
- **Live Updates** — Pulsing indicator (⚫ = connected)

Updates from Supabase in real-time via WebSocket.

---

## 🔌 Under the Hood

### Files

| File | Purpose | Lines |
|------|---------|-------|
| **ControlRoom.html** | Main unified dashboard | 380 |
| **mesh-to-music.js** | Mapping class: mesh → vectors → Strudel | 238 |
| **WitnessV2.html** | Standalone Witness visualization | 550+ |

### Dependencies
- Supabase JS v2 (CDN-loaded)
- HTML5 Canvas (no external graphics libs)
- Strudel.cc (external, for playback)

### Data Schema (Supabase)
```sql
-- Core table
mesh_state (
  id UUID,
  pending_decisions_count INT,
  pending_high_severity INT,
  ratified_decisions_count INT,
  ratified_applied_count INT,
  repos_synced INT,
  total_repos INT,
  dimension_scores JSONB (6 epistemic dimensions),
  mean_li FLOAT (Livelihood Index)
)

-- Supporting tables
pending_decisions (...) -- decisions awaiting ratification
ratified_decisions (...) -- decisions already approved
m3_metrics (...) -- M3 Nervous System rank metrics
sync_log (...) -- GitHub webhook sync history
witness_snapshots (...) -- snapshot history for playback
```

---

## 🚀 Getting Started

### 1. Quick Test (2 minutes)
```bash
# Open dashboard
open docs/ControlRoom.html

# Expected: 
# - Status: "Connected"
# - Witness shows 6D skull
# - Strudel code visible
# - Metrics show: Pending=0, Ratified=10, Health=86%
```

### 2. Verify Real-Time Updates (5 minutes)
```bash
# In Supabase Dashboard → SQL Editor:
INSERT INTO pending_decisions (
  decision_id, title, status
) VALUES (
  'test_01', 'Test decision', 'PENDING'
);

# Watch Control Room:
# - Outer arc gap widens (queue pressure increases)
# - Metrics update: Pending=1
# - Strudel uncertainty increases
```

### 3. Full Testing (15 minutes)
See **OBSERVABILITY_CONTROL_ROOM_SETUP.md** → Testing Checklist (5 comprehensive tests)

---

## 🎛️ Admiral Controls

### Vector Sliders (Manual Tweaking)
Drag any epistemic vector slider to lock in manual values:
```
know:       [────░] ← drag for scale choice
do:         [─────░] ← drag for drum coherence
clarity:    [────░] ← drag for melody brightness
coherence:  [────░] ← drag for rhythmic stability
engagement: [─────░] ← drag for tempo
uncertainty:[───░░] ← drag for pattern mutation
```

Manual mode persists until you click **"Regenerate from Mesh"**.

### Mood Presets
Pre-defined epistemic states for common Admiral contexts:
```
[Focus] [Energize] [Reflect] [Debug] [Celebrate] [Auto]
```

Click any preset to instantly adopt its epistemic state. Click **[Auto]** to return to real-time mesh tracking.

### Strudel Integration
1. **Copy Strudel Code** — copies textarea to clipboard
2. **Regenerate from Mesh** — abandon manual edits, return to auto-generation
3. **Open in Strudel.cc** — new browser tab with pattern pre-loaded and ready to play

---

## 📈 Mesh Health Interpretation

| Field State | LI Range | Meaning | Musical Feel |
|---|---|---|---|
| **Calibrated** | 0.97–1.0 | Optimal, homeostatic | Triumphant, present |
| **Power** | 0.80–0.97 | Healthy, engaged | Driving, coherent |
| **Force Dominant** | 0.0–0.80 | Chaotic, divergent | Searching, exploratory |

Color changes in Witness reflect field state (green for Calibrated, amber for Power, red for Force).

---

## 🔧 Troubleshooting

### Control Room Won't Connect
```bash
# Check browser console (F12 → Console)
# Look for: connection errors, CORS issues

# Verify Supabase project is active
curl -s https://ksinisdzgtnqzsymhfya.supabase.co/rest/v1/

# Verify anon key is correct in ControlRoom.html (hardcoded)
```

### Witness Canvas Blank
```bash
# Refresh browser (race condition on first load)
# Check: document.getElementById('witness-canvas') in console
# Verify: mesh-to-music.js loaded (DevTools → Network)
```

### Strudel Code Not Updating
```bash
# Verify mesh-to-music.js in same directory as ControlRoom.html
# In console: new MeshToMusic().vectorsToStrudelPattern({...})
# Should return Strudel code string
```

### Metrics Show Old Values
```bash
# Verify WebSocket connection active (DevTools → Network → WS)
# Manually insert a test pending decision
# Should see metrics update within <500ms
```

See **OBSERVABILITY_CONTROL_ROOM_SETUP.md** → Troubleshooting for full diagnostic guide.

---

## 📚 Full Documentation Index

| Document | Purpose |
|---|---|
| **OBSERVABILITY_CONTROL_ROOM_SETUP.md** | Complete setup, architecture, testing checklist |
| **EMPIRICA_MASTER_CREDENTIALS.md** | Workspace credential management |
| **WITNESS_BOOTSTRAP_STATUS.md** | Real-time governance data ingestion status |
| **WitnessV2.html** | Standalone visualization (reference implementation) |

---

## 🎯 Next Steps

- [ ] **Test:** Open ControlRoom.html, verify connection
- [ ] **Explore:** Drag vector sliders, watch Witness & Strudel change
- [ ] **Play:** Click "Open in Strudel.cc", hear your mesh state
- [ ] **Integrate:** Wire to Admiral's daily governance workflow
- [ ] **Extend:** Add Slack alerts, GitHub integrations, timeline views

---

## 💡 Key Concepts

### Why Dual-Sensory?
Visual (Witness) + Audio (Epistemic DJ) engage different parts of the brain:
- **Visual:** Rapid comprehension of state, spatial relationships
- **Audio:** Intuitive feel for dynamics, emotional resonance, pattern recognition

Together they provide **holistic governance awareness** in real-time.

### Why Strudel?
Strudel.cc is a live-coding music environment (Tidal Cycles derivative) that:
- Runs entirely in browser (no server needed)
- Supports real-time pattern modification
- Makes epistemic state audible and modifiable
- Integrates with Web Audio API

### Why Epistemic Vectors?
The 13 epistemic vectors (know, do, context, etc.) encode the *quality* of governance state:
- Not just metrics (count of decisions), but **epistemic coherence**
- Maps to sensory perceptions (sound, color, motion)
- Admiral develops intuitive pattern recognition over time

---

## ✅ Status

- **Control Room:** Ready to test
- **Witness V2:** Live with real governance data (10 findings bootstrapped)
- **Epistemic DJ:** Generating patterns from mesh state
- **Real-time syncing:** Active via Supabase WebSocket
- **Admiral controls:** Fully functional (presets + manual tweaking)

**Open ControlRoom.html to start using it now.**

---

**Questions?** Check the troubleshooting section above, or review OBSERVABILITY_CONTROL_ROOM_SETUP.md for comprehensive guides.
