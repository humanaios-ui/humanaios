# Track 1 Strudel Verification Guide

**Timeline:** 2-3 hours  
**Target:** Strudel v0.2.46+ syntax validation + latency + CPU profiling  
**Platform:** macOS, Chrome browser, speakers required

---

## Setup: Local Dev Server

### Option A: Python Built-in Server (Simplest)

```bash
cd /Users/andersonfamily/practices/humanaios/apps/api/src/acat

# Start HTTP server on localhost:8000
python3 -m http.server 8000

# Output:
# Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

### Option B: Node.js HTTP Server

```bash
cd /Users/andersonfamily/practices/humanaios/apps/api/src/acat

# Using http-server (if installed)
npx http-server -p 8000

# Or use Express/simple-server equivalent
```

---

## Running the Test Harness

1. **Start dev server** (from Option A or B above)

2. **Open in Chrome:**
   ```
   http://localhost:8000/track1_test_harness.html
   ```

3. **Open Chrome DevTools:**
   - Press `Cmd+Option+I` (macOS)
   - Go to **Performance** tab for CPU profiling
   - Go to **Console** to see Strudel load confirmation

4. **Run Verification:**
   - Enable **speakers** (or headphones)
   - Click **PREFLIGHT** button
     - Should see: "✓ Strudel v0.2.46+ loaded"
     - Strudel methods should be checked ✓
   - Adjust vector sliders to test different states
   - Click **CHECK** and **POSTFLIGHT** to simulate transaction flow

---

## What to Verify

### ✅ Strudel Syntax Validation

Checkboxes on the right panel should show:
- ✓ glide() syntax
- ✓ .vibrato()
- ✓ .lpf() (low-pass)
- ✓ .adsr() envelope
- ✓ .reverb()

If any are unchecked, **Strudel v0.2.46+ is missing that method** → findings needed.

### ✅ Latency Measurement

**Expected:** < 10ms pattern generation time

- **Good:** 0-5ms (green)
- **Warn:** 5-10ms (yellow)
- **Alert:** > 10ms (red) → investigate

### ✅ CPU Load

**Expected:** 5-20% sustained on modern macOS

- **Good:** < 30% (green)
- **Warn:** 30-50% (yellow)
- **Alert:** > 50% (red) → voice reduction needed

### ✅ Audio Quality

**Listen for:**
- ✓ Smooth pitch transitions when adjusting "Know" slider
- ✓ Rich harmonic content when "Context" slider is high (more voices)
- ✓ Sharp attacks when "Clarity" slider is high
- ⚠️ No beating/warbling artifacts in harmonic series
- ⚠️ No audio glitches or clicks when changing vectors

---

## Simulation: Cortex Event Cadence (5+ findings/min)

The test harness simulates PREFLIGHT → CHECK → POSTFLIGHT transaction flow.

For latency testing at **5+ findings/min cadence:**

1. **Open Chrome DevTools Performance tab**
2. **Start recording** (Cmd+Shift+E)
3. Click PREFLIGHT → wait 1s → click CHECK → wait 1s → click POSTFLIGHT
4. **Stop recording**
5. Look for:
   - CPU spikes > 50%?
   - Frame drops?
   - Long tasks?

### Simulate High-Frequency Events

Edit the test harness to fire CHECK/POSTFLIGHT automatically at 5/min:

```javascript
// In track1_test_harness.html, after PREFLIGHT:
setInterval(async () => {
  await verifier.play(verifier.getVectors(), 'CHECK')
}, 12000) // 12s = 5 per minute

setInterval(async () => {
  await verifier.play(verifier.getVectors(), 'POSTFLIGHT')
}, 24000) // Alternate
```

Monitor CPU in DevTools while running.

---

## Deliverables: Report Results

After verification, deliver findings for each claim:

| Claim | Status | Evidence |
|---|---|---|
| Strudel v0.2.46+ CDN loads | ✓/✗ | Console shows "Strudel loaded", checkboxes visible |
| glide() callable | ✓/✗ | Checkbox marked after PREFLIGHT |
| .vibrato() available | ✓/✗ | Checkbox marked after PREFLIGHT |
| .lpf() available | ✓/✗ | Checkbox marked after PREFLIGHT |
| .adsr() available | ✓/✗ | Checkbox marked after PREFLIGHT |
| .reverb() available | ✓/✗ | Checkbox marked after PREFLIGHT |
| Latency < 10ms | ✓/✗ | DevTools Performance: capture pattern gen time |
| CPU < 30% sustained | ✓/✗ | DevTools Performance: CPU flame chart |
| No audio glitches | ✓/✗ | Listen for clicks/warbling across 10min playback |
| Harmonic coherence OK | ✓/✗ | No beating artifacts in overlapping voices |

---

## If Issues Found

### Strudel Method Missing

- Check Strudel CDN URL: `https://cdn.jsdelivr.net/npm/strudel@0.2.46/dist/strudel.min.js`
- Verify v0.2.46 is the correct version (may need to check Strudel docs for method names)
- **Finding:** "Method `[X]` not available in Strudel v0.2.46; use alternative `[Y]` or downgrade/upgrade version"

### Latency High (> 10ms)

- Check browser background processes (close other tabs)
- Profile with DevTools: identify bottleneck (pattern gen, audio buffer, etc.)
- **Finding:** "Pattern generation latency [X]ms on macOS Chrome; [reason]. Optimization: [approach]"

### CPU High (> 50%)

- Reduce voice count (set density < 0.5)
- Disable reverb (test with lpf+vibrato only)
- Test on 2-year-old MacBook if available
- **Finding:** "Polyphony [N] voices + reverb = [CPU]% on macOS Chrome. Recommendation: reduce to [N-2] voices or use master reverb vs per-voice"

### Audio Glitches

- Test different browser (Safari)
- Increase buffer size (if option available in Strudel)
- **Finding:** "Audio glitches detected on macOS Chrome at [CPU load]% when [event cadence]. Cause: [diagnosis]. Solution: [mitigation]"

---

## Success Criteria

✅ **Go-live ready** if:
- All 5 Strudel methods verified ✓
- Latency < 10ms
- CPU < 30% sustained
- No audio glitches
- Harmonic series coherent (no beating)

⚠️ **Blocked** if:
- Any method missing (needs Strudel workaround or version change)
- Latency > 20ms (needs optimization)
- CPU > 50% sustained (needs architecture change — off-load to Web Worker?)
- Persistent audio glitches (critical blocker)

---

## Next After Verification

Once Strudel syntax is verified:
1. **Proceed to accessibility scaffolding** (visual waveform renderer)
2. **Complete track2_ui_integration.py** (AcousticMarkers class)
3. **Integration test** at expected 5+ findings/min with visual + audio

---

**Estimated time to verdict:** 1.5-2 hours for thorough testing + profiling
