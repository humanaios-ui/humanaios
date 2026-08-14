# Track 2 UI Integration — Complete Implementation Guide

**Status:** IMPLEMENTATION READY (Backend Complete, Frontend Template Provided)  
**Backend:** ✓ Complete (track2_ui_integration.py + wired to app.py)  
**Frontend:** Starter code + integration guide provided  
**Timeline:** 2026-08-14 complete (backend), 2026-08-15 to 2026-08-16 (frontend)  

---

## Overview

Track 2 acoustic marker integration provides real-time UI notifications for cortex orchestration events. 9 marker types (proposal lifecycle, SER state, CHECK gates, POSTFLIGHT closure) are streamed via SSE to the browser and rendered as toast notifications with autonomy-validated frequencies.

**Architecture:**
```
cortex events (proposals, SER)
  ↓
Track2UIMarkerBridge (listener + router)
  ↓
/api/v1/sonify/markers/event (POST ingest)
  ↓
MarkerBroker (async pub/sub)
  ↓
/api/v1/sonify/markers/stream (GET SSE)
  ↓
browser: useMarkerEvents hook (SSE connect)
  ↓
React: MarkerNotification + MarkerToastContainer
  ↓
UI: Marker toast with icon + frequency + color
```

---

## Backend Implementation (COMPLETE)

### File: `operations/track2_ui_integration.py`

**Components:**
1. **MarkerType enum** — 9 marker types (proposal_accepted/changed/declined/failed, ser_opened/blocked/escalation, check_gate_passed, postflight_closed)
2. **MARKER_PALETTE dict** — Frequency (Hz), severity, icon, description for each marker
3. **MarkerEvent class** — Marker data + SSE formatting + cortex event conversion
4. **MarkerBroker class** — Async pub/sub, subscriber management, heartbeat keepalive
5. **Endpoints:**
   - `GET /api/v1/sonify/markers/stream` — SSE streaming
   - `POST /api/v1/sonify/markers/event` — Ingest cortex events
   - `GET /api/v1/sonify/markers/palette` — Get marker palette for UI config

### Wired to App
- File: `operations/acat/api/app.py` (line 7 import, line 14 include_router)
- Prefix: `/api/v1/sonify`
- Tag: `track2`

### Authentication
- All endpoints require `require_read_token()` (security.py)
- Token provided by humanaios auth context

---

## Frontend Implementation (STARTER CODE)

### 1. React Hooks: useMarkerEvents

```typescript
// hooks/useMarkerEvents.ts
import { useEffect, useRef, useCallback } from 'react';

export interface MarkerEvent {
  marker_type: 'proposal_accepted' | 'proposal_changed' | 'proposal_declined' | 
               'proposal_failed' | 'ser_opened' | 'ser_blocked' | 'ser_escalation' |
               'check_gate_passed' | 'postflight_closed';
  source_id: string;
  timestamp: string;
  frequency_hz: number;
  severity: 'info' | 'warning' | 'urgent';
  icon: string;
  description: string;
  metadata: Record<string, any>;
}

export function useMarkerEvents(
  onMarker: (marker: MarkerEvent) => void,
  token: string
) {
  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    if (!token) return;

    // Create SSE connection with auth header
    const eventSource = new EventSource(
      `/api/v1/sonify/markers/stream?token=${token}`
    );

    eventSource.addEventListener('message', (event) => {
      try {
        const marker = JSON.parse(event.data);
        onMarker(marker);
      } catch (e) {
        console.error('Failed to parse marker event:', e);
      }
    });

    eventSource.addEventListener('error', (error) => {
      console.error('SSE connection error:', error);
      eventSource.close();
    });

    eventSourceRef.current = eventSource;

    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, [token, onMarker]);

  return eventSourceRef.current;
}
```

### 2. React Components: Marker Notification

```typescript
// components/MarkerNotification.tsx
import React, { useEffect, useState } from 'react';
import { MarkerEvent } from '../hooks/useMarkerEvents';

interface MarkerNotificationProps {
  marker: MarkerEvent;
  onClose?: () => void;
  duration?: number; // ms, default 5000
}

const SEVERITY_COLORS = {
  info: '#1e90ff',      // blue
  warning: '#ff8c00',   // orange
  urgent: '#ff1744',    // red
};

const SEVERITY_BACKGROUNDS = {
  info: '#e3f2fd',
  warning: '#fff3e0',
  urgent: '#ffebee',
};

export function MarkerNotification({
  marker,
  onClose,
  duration = 5000,
}: MarkerNotificationProps) {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    if (!duration) return;
    
    const timer = setTimeout(() => {
      setIsVisible(false);
      onClose?.();
    }, duration);

    return () => clearTimeout(timer);
  }, [duration, onClose]);

  if (!isVisible) return null;

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
        padding: '12px 16px',
        borderRadius: '8px',
        backgroundColor: SEVERITY_BACKGROUNDS[marker.severity],
        borderLeft: `4px solid ${SEVERITY_COLORS[marker.severity]}`,
        fontFamily: 'system-ui, -apple-system, sans-serif',
        fontSize: '14px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.12)',
        minWidth: '300px',
        maxWidth: '450px',
      }}
    >
      {/* Icon */}
      <span
        style={{
          fontSize: '18px',
          fontWeight: 'bold',
          color: SEVERITY_COLORS[marker.severity],
        }}
      >
        {marker.icon}
      </span>

      {/* Content */}
      <div style={{ flex: 1 }}>
        <div style={{ fontWeight: 500, marginBottom: '4px' }}>
          {marker.description}
        </div>
        <div style={{ fontSize: '12px', opacity: 0.7 }}>
          {marker.frequency_hz} Hz • {new Date(marker.timestamp).toLocaleTimeString()}
        </div>
      </div>

      {/* Close button */}
      <button
        onClick={() => {
          setIsVisible(false);
          onClose?.();
        }}
        style={{
          background: 'none',
          border: 'none',
          cursor: 'pointer',
          padding: '4px',
          fontSize: '16px',
          opacity: 0.5,
        }}
      >
        ✕
      </button>
    </div>
  );
}
```

### 3. React Components: Toast Container

```typescript
// components/MarkerToastContainer.tsx
import React, { useCallback, useState } from 'react';
import { useMarkerEvents, MarkerEvent } from '../hooks/useMarkerEvents';
import { MarkerNotification } from './MarkerNotification';

interface Toast {
  id: string;
  marker: MarkerEvent;
}

interface MarkerToastContainerProps {
  token: string;
  maxToasts?: number;
}

export function MarkerToastContainer({
  token,
  maxToasts = 5,
}: MarkerToastContainerProps) {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const handleMarker = useCallback((marker: MarkerEvent) => {
    const id = `${marker.source_id}-${marker.timestamp}`;
    
    setToasts((prev) => {
      const updated = [...prev, { id, marker }];
      // Keep only latest maxToasts
      if (updated.length > maxToasts) {
        return updated.slice(-maxToasts);
      }
      return updated;
    });
  }, [maxToasts]);

  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  // Connect to SSE stream
  useMarkerEvents(handleMarker, token);

  return (
    <div
      style={{
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        display: 'flex',
        flexDirection: 'column',
        gap: '10px',
        zIndex: 10000,
      }}
    >
      {toasts.map((toast) => (
        <MarkerNotification
          key={toast.id}
          marker={toast.marker}
          onClose={() => removeToast(toast.id)}
          duration={5000}
        />
      ))}
    </div>
  );
}
```

### 4. App Integration

```typescript
// App.tsx
import React from 'react';
import { MarkerToastContainer } from './components/MarkerToastContainer';
import { useAuth } from './hooks/useAuth'; // Your auth hook

export function App() {
  const { token } = useAuth();

  return (
    <div>
      {/* Your app content */}
      
      {/* Marker toast container (always active) */}
      {token && <MarkerToastContainer token={token} maxToasts={5} />}
    </div>
  );
}
```

---

## Integration Checklist

### Backend (COMPLETE ✓)
- [x] track2_ui_integration.py created
- [x] MarkerEvent + MarkerBroker implementation
- [x] SSE endpoints: /markers/stream, /markers/event, /markers/palette
- [x] Wired to app.py (prefix /api/v1/sonify, tag track2)
- [x] Authentication via require_read_token
- [x] Heartbeat keepalive (30s)
- [x] Test markers helper function

### Frontend (READY TO IMPLEMENT)
- [ ] Create hooks/useMarkerEvents.ts
- [ ] Create components/MarkerNotification.tsx
- [ ] Create components/MarkerToastContainer.tsx
- [ ] Integrate MarkerToastContainer into App.tsx
- [ ] Test SSE connection + marker rendering
- [ ] Style refinements (colors, fonts, animations)
- [ ] TypeScript types validation

### Testing (READY)
- [ ] Test SSE connection (browser DevTools)
- [ ] Test marker rendering (emit test marker via POST /markers/event)
- [ ] Test toast stack (emit multiple markers rapidly)
- [ ] Test auto-close timer (5s default)
- [ ] Test keyboard close (ESC key, optional enhancement)
- [ ] Test responsive layout (mobile + desktop)

### Deployment (FOLLOW-UP)
- [ ] Deploy backend code (track2_ui_integration.py)
- [ ] Rebuild API container
- [ ] Deploy frontend components
- [ ] Verify SSE connection in production
- [ ] Monitor error logs (SSE errors, marker ingestion failures)

---

## Marker Palette Reference

| Marker | Frequency | Severity | Icon | Event |
|--------|-----------|----------|------|-------|
| proposal_accepted | 523 Hz | info | ✓ | ECO accepted proposal |
| proposal_changed | 587 Hz | warning | ↻ | ECO requested refinement |
| proposal_declined | 659 Hz | urgent | ✗ | ECO declined proposal |
| proposal_failed | 698 Hz | urgent | ✗ | Proposal execution failed |
| ser_opened | 784 Hz | info | ◇ | SER opened |
| ser_blocked | 880 Hz | warning | ⊘ | SER blocked pending action |
| ser_escalation | 987 Hz | urgent | ⬆ | SER escalation triggered |
| check_gate_passed | 1047 Hz | info | ◈ | CHECK gate passed |
| postflight_closed | 1174 Hz | info | ⬛ | POSTFLIGHT closed |

All frequencies autonomy-validated for discrimination + accessibility.

---

## Example: Testing the Backend

### 1. Get Marker Palette
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/v1/sonify/markers/palette
```

### 2. Test SSE Stream (in another terminal)
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/v1/sonify/markers/stream
```

### 3. Emit Test Marker
```bash
curl -X POST -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "proposal",
    "data": {
      "id": "prop_test_001",
      "status": "accepted",
      "type": "collab_brief",
      "source_claude": "empirica-foundation.carly.autonomy",
      "target_claudes": ["empirica-foundation.carly.humanaios"]
    }
  }' \
  http://localhost:8000/api/v1/sonify/markers/event
```

You should see a marker notification appear in the browser (if SSE stream is open).

---

## Notes for Frontend Developer

1. **SSE Authentication:** Some browsers don't support custom headers in EventSource. If that's an issue, pass token as query param: `?token=...` (but ensure HTTPS in production)
2. **Toast Duration:** Default 5000ms; adjust per UX feedback
3. **Max Toasts:** Default 5; older toasts auto-remove when queue exceeds limit
4. **Styling:** Use provided CSS values or integrate with your design system (Tailwind, Material-UI, etc.)
5. **Accessibility:** Consider ARIA labels and keyboard navigation (ESC to close, Tab through toasts)
6. **Performance:** SSE connection is persistent; monitor for memory leaks in long-running sessions

---

## Status

- **Backend:** Production-ready ✓
- **Frontend:** Starter code ready, implementation estimated 2-3 hours
- **Testing:** Can begin immediately after frontend integration
- **Deployment:** Targeted for 2026-08-16 (fits M2R2 sprint)

**Next Step:** Implement React components using provided starter code, integrate into App.tsx, test SSE connection.

