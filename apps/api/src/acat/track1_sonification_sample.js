/**
 * Track 1: Ambient Sonification — Sample Implementation
 *
 * Maps empirica epistemic vectors to continuous ambient sound:
 * - know (0-1) → pitch (60-500 Hz, logarithmic)
 * - context (0-1) → harmonic density (voice count, overtone series)
 * - clarity (0-1) → attack/release speed (perception of confidence)
 *
 * Reference: Assessment (Aug 2, 2026) + sonification_feedback.md
 * Status: Sample implementation for team reference
 */

import { Pattern, scale, note, sound } from 'strudel'

/**
 * VECTOR MAPPINGS
 */

// Map 'know' vector (epistemic certainty) to frequency (logarithmic scale)
// Low know = low pitch (uncertainty), high know = high pitch (confidence)
// 60Hz = very uncertain, 500Hz = very confident
function knowToFreq(know) {
  // Logarithmic mapping: log scale preserves harmonic relationships
  // 60Hz (C2) ≈ MIDI 36, 500Hz ≈ MIDI 79
  const minFreq = 60   // C2 (very uncertain)
  const maxFreq = 500  // B4 (very confident)
  const logMin = Math.log(minFreq)
  const logMax = Math.log(maxFreq)
  const logFreq = logMin + (know * (logMax - logMin))
  return Math.exp(logFreq)
}

// Map 'context' vector to voice count (harmonic series density)
// Low context = single voice (minimal information)
// High context = up to 8 voices (rich harmonic field)
function contextToVoiceCount(context) {
  return Math.ceil(context * 8) || 1 // At least 1 voice
}

// Map 'clarity' vector to attack/release envelope (ms)
// Low clarity = slow attack, long decay (diffuse)
// High clarity = fast attack, short decay (sharp)
function clarityToEnvelope(clarity) {
  const attack = 50 + (1 - clarity) * 500  // 50-550ms
  const release = 100 + (1 - clarity) * 1900 // 100-2000ms
  return { attack, release }
}

/**
 * TRACK 1 AMBIENT PATTERN
 *
 * Generates a continuously evolving ambient texture from epistemic state.
 * Called at PREFLIGHT, CHECK, and POSTFLIGHT transitions to avoid
 * glitching from high-frequency updates.
 */
export class Track1Generator {
  constructor() {
    this.lastVectors = null
    this.currentPattern = null
  }

  /**
   * Generate ambient pattern from epistemic vectors
   * @param {Object} vectors - Empirica epistemic state (know, context, clarity, uncertainty, etc.)
   * @returns {Pattern} Strudel pattern ready to play()
   */
  render(vectors) {
    const {
      know = 0.5,
      context = 0.5,
      clarity = 0.5,
      uncertainty = 0.5,
      density = 0.5,
    } = vectors

    const baseFreq = knowToFreq(know)
    const voiceCount = contextToVoiceCount(density) // Use density for polyphony
    const { attack, release } = clarityToEnvelope(clarity)

    // Build harmonic series: fundamental + overtones
    // Overtone series creates the "richness" of the sound
    const harmonic = (n) => baseFreq * (n + 1) // n=0 is fundamental, n=1 is 2x, etc.

    // Each voice: frequency-shifted harmonic, filtered, modulated
    const voices = Array.from({ length: voiceCount }, (_, i) => {
      const freq = harmonic(i)

      // Pitch glide (portamento) for smooth frequency transitions
      // Glide time proportional to how much vectors changed
      const glideTime = 200 + (uncertainty * 400) // 200-600ms glide

      // Volume: higher harmonics are quieter (natural timbre)
      // Fundamental is loudest, overtones fade
      const gainFactor = 1 / (i + 1) ** 0.5

      // Polyphonic voice: note + filters + modulation
      return `${freq}
        .mul(${gainFactor})
        .glide(${glideTime})
        .vibrato(${5 + clarity * 5}, ${0.5 + clarity * 1})
        .lpf(${2000 + context * 3000})
        .reverb(${0.3 + context * 0.5}, 2)
        .adsr(${attack}, 100, 0.7, ${release})`
    })

    // Join all voices into polyphonic pattern
    const voicePattern = voices.join(', ')

    // Master pattern: continuously loop with slight variation
    // This allows real-time updates at CHECK gates without glitching
    const pattern = `[${voicePattern}]
      .legato(0.95)
      .room(${0.4 + context * 0.3})
      .gain(${0.6 - uncertainty * 0.2})`

    return pattern
  }

  /**
   * Play pattern with cross-fade for smooth transitions
   * @param {Object} vectors - Current epistemic state
   * @param {number} fadeDurationMs - Crossfade duration (default 200ms)
   */
  async play(vectors, fadeDurationMs = 200) {
    const newPattern = this.render(vectors)

    if (this.currentPattern) {
      // Fade out old pattern
      await this.fadeOut(fadeDurationMs / 2)
      this.currentPattern.stop()
    }

    // Play new pattern with fade-in
    this.currentPattern = newPattern
    return this.fadeIn(fadeDurationMs / 2)
  }

  async fadeOut(durationMs) {
    if (!this.currentPattern) return
    const steps = 20
    const stepDuration = durationMs / steps
    for (let i = 0; i < steps; i++) {
      this.currentPattern.gain(1 - (i / steps) * 0.3)
      await new Promise((r) => setTimeout(r, stepDuration))
    }
  }

  async fadeIn(durationMs) {
    if (!this.currentPattern) return
    const steps = 20
    const stepDuration = durationMs / steps
    for (let i = 0; i < steps; i++) {
      this.currentPattern.gain(0.7 + (i / steps) * 0.3)
      await new Promise((r) => setTimeout(r, stepDuration))
    }
  }
}

/**
 * USAGE EXAMPLE
 *
 * Integrate with humanaios-ui and cortex_mailbox_poll:
 *
 * ```javascript
 * import { Track1Generator } from './track1_sonification_sample.js'
 *
 * const track1 = new Track1Generator()
 *
 * // On PREFLIGHT (open transaction)
 * await track1.play({
 *   know: 0.65,
 *   context: 0.69,
 *   clarity: 0.70,
 *   uncertainty: 0.32,
 *   density: 0.50
 * })
 *
 * // On CHECK (transition noetic→praxic)
 * await track1.play({
 *   know: 0.75,
 *   context: 0.77,
 *   clarity: 0.75,
 *   uncertainty: 0.20,
 *   density: 0.60
 * })
 *
 * // On POSTFLIGHT (close transaction)
 * await track1.play({
 *   know: 0.85,
 *   context: 0.80,
 *   clarity: 0.72,
 *   uncertainty: 0.10,
 *   density: 0.65
 * })
 * ```
 */

/**
 * VERIFICATION CHECKLIST (from assessment)
 *
 * ⚠️ Strudel v0.2.46+ syntax validation needed:
 *   - [ ] glide() — pitch portamento available?
 *   - [ ] .vibrato() — modulation depth/rate params?
 *   - [ ] .lpf() — low-pass filter available?
 *   - [ ] .adsr() — amplitude envelope available?
 *   - [ ] .reverb() — reverb params (dry/wet, decay)?
 *   - [ ] .legato() — note overlap factor?
 *   - [ ] .room() — convolution reverb space?
 *   - [ ] .gain() — volume envelope?
 *
 * ⚠️ Latency test (simulate 5+ findings/min):
 *   - [ ] Measure glitch rate on 60Hz base pattern
 *   - [ ] Test on macOS (Safari, Chrome)
 *   - [ ] Test on iOS Safari (critical latency risk)
 *   - [ ] Test on Android Chrome
 *   - [ ] Measure CPU load on 2-year-old MacBook
 *
 * ⚠️ Harmonic quantization:
 *   - [ ] Verify no beating artifacts from voice detuning
 *   - [ ] Test with explicit scale()/chord() quantizers if needed
 *   - [ ] Confirm harmonic series stays tuned across know updates
 *
 * ⚠️ Integration:
 *   - [ ] Wire into cortex_mailbox_poll event stream (Track 2 gestures)
 *   - [ ] Batch Track 1 updates at CHECK gates
 *   - [ ] Fire Track 2 immediately (brief transients)
 *   - [ ] Test cross-fade smoothness at high update cadence
 */
