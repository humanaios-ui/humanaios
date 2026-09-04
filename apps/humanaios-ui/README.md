# HumanAIOS UI — Phase 1b Integration

Real-time waveform visualization + acoustic marker sonification for epistemic state monitoring.

## What This Is

The Phase 1b UI implements **live visualization of AI epistemic state** via:

1. **Waveform Renderer** — Real-time frequency × time plot
   - Horizontal axis: rolling 30-second window (time)
   - Vertical axis: 60–500 Hz (frequency, log scale)
   - Color dimension: epistemic vector components (know, context, clarity, uncertainty)
   - Performance target: <16ms render cycle

2. **Marker Consumer** — SSE client for acoustic events
   - Connects to `/api/v1/sonify/markers/stream` (Server-Sent Events)
   - Consumes 9 marker types: proposal (accepted/changed/declined/failed), SER (opened/blocked/escalation), CHECK gate, POSTFLIGHT
   - Haptic feedback (W3C Vibration API) for urgent events
   - Audio playback (Web Audio API) with frequency-severity mapping

3. **Integration** — React + Vite + TypeScript
   - Connection status display (connected/disconnected + queue size)
   - Real-time marker visualization overlaid on waveform
   - Event panel showing latest marker details
   - Accessibility: WCAG AA (color + haptic + ARIA live regions)

## Architecture

```
App.tsx (orchestration)
├─ WaveformRenderer.tsx (SVG canvas, time/freq axes, color mapping)
└─ MarkerConsumer.ts (SSE client, event queue, audio/haptic dispatch)
```

### Data Flow

```
Backend SSE stream (/api/v1/sonify/markers/stream)
    ↓
MarkerConsumer.connect() — EventSource listener
    ↓
handleMarkerEvent() — parse, queue, dispatch
    ↓
App.tsx subscribers — setMarkers(), setLastEvent()
    ↓
WaveformRenderer — render markers on canvas
    ↓
Audio/haptic playback (browser Audio API + Vibration API)
```

## Getting Started

### Install

```bash
npm install
```

### Development

```bash
npm run dev
```

Opens at `http://localhost:5173` (Vite default).

### Build

```bash
npm run build
```

Produces `dist/` for deployment.

### Environment

Set `REACT_APP_API_URL` to point to your backend (default: `/api/v1`):

```bash
REACT_APP_API_URL=https://api.humanaios.local npm run dev
```

## API Contract

The UI expects a backend SSE endpoint at `/api/v1/sonify/markers/stream`:

### Server-Sent Events

**Endpoint:** `GET /api/v1/sonify/markers/stream`

**Response:** Streaming JSON events (newline-delimited)

**Event Schema:**
```json
{
  "marker_type": "proposal_accepted" | "proposal_changed" | "proposal_declined" | "proposal_failed" | "ser_opened" | "ser_blocked" | "ser_escalation" | "check_gate_passed" | "postflight_closed",
  "source_id": "prop_xxx" | "ser_yyy" | "transaction_zzz",
  "timestamp": "2026-09-04T18:54:16Z",
  "frequency_hz": 523-1174,
  "severity": "info" | "warning" | "urgent",
  "icon": "✓" | "⚠" | "🔴" | "📊" | etc.,
  "description": "Proposal accepted: Phase 1b completion confirmation",
  "metadata": { "proposal_id": "prop_...", "target_claudes": [...], ... }
}
```

**Latency Target:** <200ms from event emission to visual marker rendered

**Bandwidth:** ~5 events/minute peak (transitions, proposals, SER state changes)

## Performance

Measured targets (Phase 1b):

- **Render latency:** <16ms (60 FPS, SVG canvas)
- **Event latency:** <200ms (SSE dispatch → marker visible)
- **Memory:** <50MB (last 100 markers in state)
- **CPU:** <10% (idle), <30% (active, high event rate)

## Accessibility

WCAG AA compliance:

- **Color:** All vector types distinguished by color + legend text (not color-only)
- **Haptic:** Urgent markers trigger vibration patterns (W3C API)
- **Audio:** Frequency mapping (523–1174 Hz) scaled linearly with severity
- **ARIA:** Live region updates for connection status + event log
- **Keyboard:** All interactive elements keyboard-accessible (future: detail panel)

## Testing

```bash
npm run test
```

Runs Vitest suite (placeholder — add integration tests as Phase 2 work).

## Phase 2 Roadmap

- [ ] Detail panel — click marker to show full event metadata
- [ ] Time sync — align waveform render with backend clock
- [ ] Multi-vector playback — simultaneous audio streams for multiple dimensions
- [ ] Replay mode — scrub through historical event log
- [ ] Export — download waveform snapshot + event log as JSON/CSV

## Known Limitations

1. **Simulation mode** — WaveformRenderer currently generates synthetic data. Phase 2 will integrate live epistemic state API.
2. **Audio context** — May not work in private/incognito mode (browser security).
3. **Mobile haptics** — Vibration API support varies by device (iOS has limited support).
4. **SSE fallback** — No automatic HTTP/2 fallback; browser must support EventSource.

## Deployment

### Local

```bash
npm run build
npm run preview
```

### Docker (production)

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

### Reverse Proxy

Set `REACT_APP_API_URL` environment variable before build to bake in API URL:

```nginx
location /humanaios-ui/ {
  proxy_pass http://ui-container/;
}

location /api/v1/ {
  proxy_pass http://backend-api/v1/;
}
```

## Maintenance

- **Dependencies:** React 18, Vite 6, TypeScript 7 (as of Sep 2026)
- **Browser support:** Modern browsers with ES2020 + EventSource + Web Audio API
- **Node:** 18+

## References

- **Phase 1b Spec:** `../../docs/PHASE_1B_DELIVERABLES.md`
- **Backend SSE Router:** `../../src/Track2/track2_ui_integration.py`
- **Acoustic Markers:** `../../src/Track2/AcousticMarkers.py`
- **ACAT Integration:** `../../docs/ACAT_COMPOSITION_FEEDBACK_LOOP.md`

---

**Status:** Phase 1b UI implementation ready (Sep 11, 2026 deadline).  
**Last updated:** 2026-09-04  
**Maintainer:** empirica-foundation.carly.humanaios
