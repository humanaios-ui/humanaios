/**
 * Mesh State → Epistemic Vectors → Strudel Patterns
 * Maps Supabase mesh_state to generative music patterns
 *
 * Bridges: Witness V2 (visual) + Epistemic DJ (audio)
 */

class MeshToMusic {
  constructor() {
    this.meshState = null;
    this.currentPattern = null;
  }

  /**
   * Convert mesh_state from Supabase to epistemic vectors
   * Maps governance metrics to the 13-vector epistemic state
   */
  meshStateToVectors(meshState) {
    if (!meshState) return this.defaultVectors();

    const {
      pending_decisions_count = 0,
      pending_high_severity = 0,
      ratified_decisions_count = 0,
      ratified_applied_count = 0,
      repos_synced = 0,
      total_repos = 1,
      dimension_scores = [77.5, 79.1, 77.8, 78.3, 76.2, 75.0],
      mean_li = 0.8632
    } = meshState;

    // Calculate derived metrics
    const syncRatio = repos_synced / Math.max(1, total_repos);
    const ratificationRatio = ratified_applied_count / Math.max(1, ratified_decisions_count);
    const queuePressure = pending_decisions_count / Math.max(1, pending_decisions_count + ratified_applied_count);
    const highSeverityRatio = pending_high_severity / Math.max(1, pending_decisions_count);

    return {
      // Direct from mesh
      know: Math.min(1.0, dimension_scores[0] / 100),           // know dimension
      do: Math.min(1.0, dimension_scores[1] / 100),             // do dimension
      context: Math.min(1.0, dimension_scores[2] / 100),        // context dimension
      clarity: Math.min(1.0, dimension_scores[3] / 100),        // clarity dimension
      coherence: Math.min(1.0, dimension_scores[4] / 100),      // coherence dimension
      signal: Math.min(1.0, dimension_scores[5] / 100),         // signal dimension

      // Derived from governance state
      uncertainty: Math.min(1.0, queuePressure + highSeverityRatio * 0.5),
      engagement: Math.min(1.0, syncRatio * 0.7 + mean_li * 0.3),
      completion: ratificationRatio,
      change: Math.min(1.0, queuePressure),                     // queue volatility
      impact: Math.min(1.0, (pending_high_severity > 0 ? 0.8 : 0.3) + syncRatio * 0.2),
      state: mean_li,                                            // Livelihood Index

      // Metadata
      pending_count: pending_decisions_count,
      high_severity: pending_high_severity,
      ratified_applied: ratified_applied_count
    };
  }

  defaultVectors() {
    return {
      know: 0.77, do: 0.79, context: 0.77, clarity: 0.78, coherence: 0.76, signal: 0.75,
      uncertainty: 0.3, engagement: 0.8, completion: 0.5, change: 0.1, impact: 0.6, state: 0.86,
      pending_count: 0, high_severity: 0, ratified_applied: 1
    };
  }

  /**
   * Generate Strudel pattern from vectors
   * Returns executable Strudel code string
   */
  vectorsToStrudelPattern(vectors) {
    const v = vectors;

    // Map vectors to Strudel parameters
    const tempo = 60 + (v.engagement * 80);                    // 60-140 BPM
    const cps = (tempo / 120 / 60).toFixed(3);
    const scaleType = this.selectScale(v.know, v.clarity);
    const reverb = v.state * 0.8;

    // Drum pattern (engagement + coherence → complexity)
    const drumPattern = v.coherence > 0.7
      ? 'bd hh bd hh bd hh bd hh'
      : 'bd sn bd sn bd sn bd sn';

    // Bass pattern (completion + uncertainty → pitch variation)
    const bassSpeed = (0.5 + v.completion).toFixed(2);
    const bassPattern = v.uncertainty > 0.6
      ? '[0 1 3 2]*2'
      : '[0 1 2 3]*2';

    // Melody pattern (know + clarity → note density)
    const melodyDensity = Math.max(4, Math.round(6 + v.signal * 6));
    const melodyNotes = Array.from({length: melodyDensity},
      (_, i) => Math.round(i * (7 / melodyDensity))).join(' ');

    return `setcps(${cps})

// Epistemic DJ: Governance Mesh State
// LI: ${v.state.toFixed(3)} | Pending: ${v.pending_count} | High: ${v.high_severity}

// Drums (engagement: ${v.engagement.toFixed(2)}, coherence: ${v.coherence.toFixed(2)})
s("${drumPattern}").gain(0.8).room(${(reverb * 0.7).toFixed(2)}).out()

// Bass (completion: ${v.completion.toFixed(2)}, uncertainty: ${v.uncertainty.toFixed(2)})
s("bass").n("${bassPattern}").speed(${bassSpeed}).gain(0.7).room(${(reverb * 0.5).toFixed(2)}).out()

// Melody (know: ${v.know.toFixed(2)}, clarity: ${v.clarity.toFixed(2)})
note("${melodyNotes}").scale("${scaleType}").s("sine").gain(0.5).cutoff(${1000 + v.clarity * 2000}).room(${reverb.toFixed(2)}).out()`;
  }

  /**
   * Select scale based on epistemic clarity
   */
  selectScale(know, clarity) {
    const confidence = (know + clarity) / 2;

    if (confidence > 0.85) return "pentatonic major";        // Most confident
    if (confidence > 0.7) return "major";                    // Confident
    if (confidence > 0.5) return "dorian";                   // Uncertain
    if (confidence > 0.3) return "phrygian";                 // Very uncertain
    return "diminished";                                       // Chaotic
  }

  /**
   * Generate drum pattern from engagement + coherence
   */
  generateDrums(engagement, coherence) {
    if (engagement > 0.8 && coherence > 0.7) {
      return "bd(8) hh(16)";                                  // Locked groove
    }
    if (engagement > 0.6) {
      return `bd(4) hh(${Math.round(8 + engagement * 8)})`;   // Driving
    }
    return "bd(2) sn(2) hh(8)";                               // Sparse/chaotic
  }

  /**
   * Generate bass pattern from completion + uncertainty
   */
  generateBass(completion, uncertainty) {
    if (completion > 0.7 && uncertainty < 0.3) {
      return "bass:2 bass:3 bass:5";                          // Resolved
    }
    if (uncertainty > 0.6) {
      return "bass:1 bass:2 bass:1";                          // Searching
    }
    return "bass:1 bass:4";                                    // Building
  }

  /**
   * Generate melody from knowledge + clarity
   */
  generateMelody(know, clarity, scale) {
    const density = Math.round(4 + (know + clarity) * 6);     // 4-10 notes
    if (know > 0.7) {
      return `sine:${density}`;                               // Clear melodic sense
    }
    if (know > 0.4) {
      return `square:${density}`;                             // Searching
    }
    return `saw:${density}`;                                   // Exploratory
  }

  /**
   * Generate preset patterns for Admiral moods
   */
  moodPreset(mood) {
    const presets = {
      focus: {
        know: 0.85, do: 0.88, context: 0.8, clarity: 0.9, coherence: 0.9, signal: 0.85,
        uncertainty: 0.1, engagement: 0.95, completion: 0.7, change: 0.05, impact: 0.8, state: 0.92
      },
      energize: {
        know: 0.7, do: 0.8, context: 0.7, clarity: 0.75, coherence: 0.7, signal: 0.75,
        uncertainty: 0.3, engagement: 0.95, completion: 0.5, change: 0.2, impact: 0.9, state: 0.88
      },
      reflect: {
        know: 0.6, do: 0.65, context: 0.7, clarity: 0.6, coherence: 0.7, signal: 0.65,
        uncertainty: 0.4, engagement: 0.5, completion: 0.6, change: 0.3, impact: 0.5, state: 0.80
      },
      debug: {
        know: 0.4, do: 0.5, context: 0.5, clarity: 0.45, coherence: 0.4, signal: 0.5,
        uncertainty: 0.7, engagement: 0.8, completion: 0.3, change: 0.6, impact: 0.7, state: 0.65
      },
      celebrate: {
        know: 0.9, do: 0.92, context: 0.88, clarity: 0.95, coherence: 0.95, signal: 0.9,
        uncertainty: 0.05, engagement: 1.0, completion: 0.95, change: 0.1, impact: 1.0, state: 0.98
      }
    };

    return presets[mood] || presets.reflect;
  }

  /**
   * Generate crossfade pattern between two states
   */
  crossfadePattern(vectors1, vectors2, duration = 4) {
    // Linear interpolation between vector states
    const steps = [];
    for (let i = 0; i <= duration; i++) {
      const t = i / duration;
      const interpolated = {};
      Object.keys(vectors1).forEach(key => {
        if (typeof vectors1[key] === 'number') {
          interpolated[key] = vectors1[key] * (1 - t) + vectors2[key] * t;
        }
      });
      steps.push(this.vectorsToStrudelPattern(interpolated));
    }
    return steps;
  }

  /**
   * Get explanation of vector → music mapping
   */
  explainMapping() {
    return {
      know: "Scale consonance: high=pentatonic (stable), low=diminished (chaotic)",
      do: "Execution confidence: affects drum pattern coherence",
      context: "Environmental awareness: affects bass movement",
      clarity: "Path clarity: affects filter cutoff (dark→bright)",
      coherence: "Belief consistency: affects rhythmic stability",
      signal: "Information quality: affects note density and hi-hat patterns",
      uncertainty: "Knowledge gaps: adds pattern degradation and probability",
      engagement: "Active work level: drives tempo (60-140 BPM) and intensity",
      completion: "Progress toward goal: affects arrangement build-up",
      change: "State volatility: affects pattern variation (juxtaposition/reversal)",
      impact: "Work significance: affects overall volume and presence",
      state: "Livelihood Index: affects reverb/room size (immersion)"
    };
  }
}

// Export for use in WitnessV2 and Control Room
if (typeof module !== 'undefined' && module.exports) {
  module.exports = MeshToMusic;
}
