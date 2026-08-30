# Phase 1b Completion — Implementation Roadmap

**Status:** Spec & Handoff Phase  
**Deadline:** Sep 11, 2026 (12 days)  
**Critical Path:** Visual Waveform Renderer (blocks Phase 2 sonification visualization)

---

## Executive Summary

Phase 1b has 3 of 5 tasks complete (60%). Two critical tasks remain:

1. **Visual Waveform Renderer** (Accessibility Scaffolding) — CRITICAL PATH
   - Implement SVG/Canvas waveform visualization
   - Map empirica vectors to visual dimensions
   - Color-code by vector dimension (know→color, context→saturation, etc.)
   - Accessibility first (VoiceOver narration support)

2. **AcousticMarkers Class** (Track 2 Integration)
   - Complete skeleton implementation in track2_ui_integration.py
   - Non-blocking async event handling
   - Strudel pattern integration
   - cortex_mailbox_poll event stream wiring

Both enable Phase 2 Track B go-live (Sep 11). Lower-friction work (ACAT calibration) is deferred; SER 3.5 already approved.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│ Phase 2 Track B (Sep 11 Go-Live)                    │
│  - Sonification: empirica vectors → audio spectrum  │
│  - Visualization: waveform renderer (THIS TASK)     │
│  - Markers: cortex events → toast notifications     │
└─────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────┐
│ Phase 1b Component: Waveform Renderer               │
│  - SVG/Canvas element in lasting-light-ai/src       │
│  - Input: vector array (13 dimensions)              │
│  - Output: animated waveform + legend               │
│  - Style: accessible, WCAG 2.1 AA compliant         │
└─────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────┐
│ Backend: AcousticMarkers → Waveform Integration     │
│  - Cortex events (proposal_accepted, etc.)          │
│  - Transform to marker data (frequency, severity)   │
│  - Toast + waveform synchronized display           │
└─────────────────────────────────────────────────────┘
```

---

## Task 1: Visual Waveform Renderer (CRITICAL)

### Requirements

**Visual Design:**
- X-axis: Time (0-N seconds, scrolls as new data arrives)
- Y-axis: Frequency (log scale, 20Hz-20kHz, human hearing range)
- Color: Vector dimension (know→red, uncertainty→blue, context→green, etc.)
- Opacity: Intensity/confidence (0-1 scale)
- Update rate: Real-time (100ms refresh)

**Accessibility:**
- WCAG 2.1 AA compliant
- VoiceOver support: "Waveform visualization, 13 dimensions active, highest: know at 0.85"
- Keyboard navigation: arrow keys to zoom/pan
- High-contrast mode support
- Alt text for snapshot export

**Technical Specs:**
- Framework: React (existing stack: lasting-light-ai/src)
- Rendering: SVG (preferred) or Canvas (if performance needed)
- Libraries: d3.js or Recharts (existing charting patterns)
- Data structure: 
  ```typescript
  interface VectorSnapshot {
    timestamp: number;
    vectors: {
      know: 0-1;
      uncertainty: 0-1;
      context: 0-1;
      engagement: 0-1;
      // ... 9 more dimensions
    };
  }
  ```
- Props:
  ```typescript
  <WaveformRenderer
    data={VectorSnapshot[]}
    timeWindow={30000}          // 30s visible
    dimensions={['know', 'uncertainty', 'context']}
    colorScheme="empirica"
    onHover={(ts, vector) => ...}
  />
  ```

### Implementation Checklist

- [ ] Create `lasting-light-ai/src/components/WaveformRenderer.tsx` (500-800 LOC)
- [ ] Implement data buffer + circular queue (handle 100+ events/sec)
- [ ] Add D3 or Recharts wrapper
- [ ] Implement color mapping (vector dimension → color)
- [ ] Add time scrolling + zoom controls
- [ ] Implement accessibility labels + VoiceOver support
- [ ] Add keyboard navigation (arrow keys, +/-)
- [ ] Create unit tests (React Testing Library)
- [ ] Add to App.tsx integration
- [ ] Test on: macOS Safari, iOS Safari, Android Chrome, Chromebook

### Timeline

- **Aug 31-Sep 2:** Implementation (3 days)
- **Sep 3-5:** Testing + accessibility audit (2 days)
- **Sep 6-10:** Staging verification (4 days)

---

## Task 2: AcousticMarkers Class Completion

### Requirements

**Current State:** Skeleton in `operations/track2_ui_integration.py`

**Completion Scope:**
1. Implement marker queue (thread-safe, bounded)
2. Non-blocking async event handling (use asyncio.Queue)
3. Strudel pattern generation (map event → harmonic series)
4. cortex_mailbox_poll integration (listen for proposal events)
5. 7 event types: proposal_accepted, proposal_changed, proposal_declined, proposal_failed, ser_opened, ser_blocked, ser_escalation

**Technical Specs:**

```python
class AcousticMarkers:
    """Non-blocking async handler for cortex events → audio markers"""
    
    async def subscribe(self, mailbox_stream):
        """Listen to cortex_mailbox_poll SSE stream"""
        async for event in mailbox_stream:
            if event.type in self.EVENT_TYPES:
                marker = self.event_to_marker(event)
                await self.queue.put(marker)
    
    async def generate_strudel(self, marker: Marker) -> str:
        """Convert marker to Strudel DSL pattern"""
        # marker.frequency_hz → pitch
        # marker.severity → volume/duration
        # marker.timestamp → start time
        return f"sine('{marker.frequency_hz}').gain(0.5)"
    
    def event_to_marker(self, event: dict) -> Marker:
        """proposal_accepted → Marker(frequency=523, severity=info)"""
        return MARKER_PALETTE[event['type']]
```

### Implementation Checklist

- [ ] Implement `AcousticMarkers.__init__()` with asyncio.Queue
- [ ] Implement `subscribe()` with mailbox stream handling
- [ ] Implement `generate_strudel()` for each event type
- [ ] Wire into cortex_mailbox_poll (`/cortex-mailbox-poll` skill)
- [ ] Add error handling (queue full, stream disconnect)
- [ ] Create integration tests (mock mailbox events)
- [ ] Add latency monitoring (<500ms target)
- [ ] Test with 100+ events/sec load

### Timeline

- **Aug 31-Sep 2:** Implementation (2 days)
- **Sep 3-4:** Testing + load verification (1 day)
- **Sep 5-10:** Staging integration (4 days)

---

## Task 3: ACAT Calibration (Lower Priority)

**Status:** SER 3.5 approved, no tasks defined yet.

**Scope:** Integrate ACAT feedback loop with wisdom_engine guidance sessions.

**Deferred to:** Phase 2 (after Sep 11, if time allows)

---

## Deployment Checklist

### Pre-Deployment (Sep 9-10)

- [ ] Both components pass unit + integration tests
- [ ] Load test: Waveform + markers at 100+ events/sec
- [ ] Accessibility audit: WCAG 2.1 AA verified
- [ ] Performance: p99 latency <500ms
- [ ] Staging environment test (full Phase 2 flow)

### Deployment (Sep 11)

- [ ] Merge to `main` branch
- [ ] Build container with both components
- [ ] Deploy to production
- [ ] Verify endpoints live
- [ ] Monitor latency + error rates (24h observation)

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Waveform rendering performance (100+ evt/sec) | MEDIUM | HIGH | Use Canvas instead of SVG if needed, implement data buffering |
| Async queue deadlock in AcousticMarkers | LOW | HIGH | Use asyncio.Queue (thread-safe), add watchdog timer |
| Strudel integration latency spike | MEDIUM | MEDIUM | Profile generate_strudel(), cache patterns |
| Accessibility audit fails | LOW | MEDIUM | Early audit (Sep 3), fix before Sep 11 |

---

## Resource Needs

- **Frontend developer:** 40-50 hours (Waveform Renderer)
- **Backend developer:** 20-30 hours (AcousticMarkers completion)
- **QA/Accessibility:** 15-20 hours (testing + audit)
- **DevOps:** 5-10 hours (staging deployment, monitoring)

**Total:** ~80-110 hours (10-14 person-days)

**Current Status:** Design + spec ready. Implementation handoff required.

---

## Success Criteria

✅ Visual waveform rendering works at 100+ evt/sec  
✅ AcousticMarkers completes without blocking  
✅ Integration with cortex_mailbox_poll verified  
✅ All accessibility tests pass WCAG 2.1 AA  
✅ Latency <500ms p99 (empirica vector → waveform display)  
✅ Phase 2 Track B unblocked (Sep 11 go-live)  

---

## Handoff Information

**For:** Frontend Lead (lasting-light-ai) + Backend Lead (operations)

**Deliverables in This Spec:**
1. Architectural diagrams
2. Component requirements (WaveformRenderer props, AcousticMarkers interface)
3. Data structures (VectorSnapshot, Marker types)
4. Strudel DSL mapping rules
5. Timeline + resource estimates
6. Risk + mitigation plan

**Next Steps:**
1. Review this spec with team leads
2. Estimate sprint allocation (12 days to Sep 11)
3. Begin implementation (Aug 31 kickoff)
4. Daily standup on critical path (waveform rendering)
5. Accessibility audit: Sep 3-4 (before staging)
6. Go-live: Sep 11

---

**Prepared by:** humanaios Claude Code  
**Date:** Aug 30, 2026  
**For:** Phase 2 Track B unblock (Sep 11 deadline)
