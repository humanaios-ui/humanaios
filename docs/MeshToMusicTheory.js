/**
 * MeshToMusicTheory — Epistemic Vectors → Music Composition
 * Maps governance state to musically coherent, expressive patterns
 * using proper music theory: tonality, harmony, voicing, counterpoint
 */

class MeshToMusicTheory {
  constructor() {
    // Solfeggio frequencies (Hz) mapped to LI bands
    this.SOLFEGGIO = [55, 174, 285, 396, 417, 528, 594, 639, 741, 963];

    // Musical modes (scale degrees from root)
    this.MODES = {
      ionian: [0, 2, 4, 5, 7, 9, 11],        // Major
      dorian: [0, 2, 3, 5, 7, 9, 10],        // Minor with raised 6th
      phrygian: [0, 1, 3, 5, 7, 8, 10],      // Dark, Spanish
      lydian: [0, 2, 4, 6, 7, 9, 11],        // Major with raised 4th
      mixolydian: [0, 2, 4, 5, 7, 9, 10],    // Major with lowered 7th
      aeolian: [0, 2, 3, 5, 7, 8, 10],       // Natural minor
      locrian: [0, 1, 3, 5, 6, 8, 10],       // Diminished sound
      harmonic_minor: [0, 2, 3, 5, 7, 8, 11], // Minor with raised 7th
      melodic_minor: [0, 2, 3, 5, 7, 9, 11]   // Minor with raised 6th & 7th
    };

    // Harmonic functions (roman numeral analysis)
    this.HARMONIC_FUNCTIONS = {
      stable: [0, 4, 7],           // I chord (tonic)
      subdominant: [5, 9, 0],      // IV chord
      dominant: [7, 11, 2],        // V chord
      relative_minor: [9, 0, 4],   // vi chord
      diminished: [2, 5, 8]        // vii° chord
    };
  }

  /**
   * Select tonality based on epistemic clarity
   * High clarity → Major (consonant, resolved)
   * Low clarity → Minor/Phrygian (dark, searching)
   */
  selectTonality(know, clarity, coherence) {
    const confidence = (know + clarity) / 2;
    const stability = coherence;

    if (confidence > 0.85 && stability > 0.8) {
      return 'ionian';                      // Optimistic, clear
    }
    if (confidence > 0.75 && stability > 0.7) {
      return 'lydian';                      // Bright, aspirational
    }
    if (confidence > 0.65) {
      return 'mixolydian';                  // Blues-tinged, balanced
    }
    if (confidence > 0.5) {
      return 'dorian';                      // Neutral, introspective
    }
    if (confidence > 0.35) {
      return 'aeolian';                     // Minor, searching
    }
    if (confidence > 0.2) {
      return 'phrygian';                    // Very dark, chaotic
    }
    return 'locrian';                       // Extremely chaotic
  }

  /**
   * Generate harmonic progression based on coherence
   * Returns chord sequence as scale degrees
   */
  generateProgression(coherence, completion) {
    if (coherence > 0.85 && completion > 0.7) {
      // Very stable: classic I-IV-V-I
      return [0, 5, 7, 0];
    }
    if (coherence > 0.75) {
      // Stable: I-vi-IV-V
      return [0, 9, 5, 7];
    }
    if (coherence > 0.6) {
      // Balanced: I-IV-vi-V
      return [0, 5, 9, 7];
    }
    if (coherence > 0.45) {
      // Uncertain: I-vi-ii-V (chromatic movement)
      return [0, 9, 2, 7];
    }
    if (coherence > 0.3) {
      // Unstable: chromatic descent
      return [0, 11, 10, 9];
    }
    // Chaotic: random intervals
    return [0, 3, 7, 2];
  }

  /**
   * Generate melodic contour based on completion + uncertainty
   * Combines direction (ascending/descending) with intervallic shape
   */
  generateMelodic(completion, uncertainty, know, signal) {
    const confidence = (completion + know) / 2;
    const intervalRange = 3 + uncertainty * 9;  // 3-12 semitone leaps

    if (confidence > 0.8) {
      // Resolved: ascending arch (rising, then resolving to tonic)
      return { shape: 'arch_ascending', range: 8, stepSize: 2 };
    }
    if (confidence > 0.6) {
      // Progressing: gentle steps upward
      return { shape: 'ascending', range: 7, stepSize: 1.5 };
    }
    if (confidence > 0.4) {
      // Searching: wandering, small intervals
      return { shape: 'wandering', range: 5, stepSize: 1 };
    }
    if (confidence > 0.2) {
      // Descending: falling search
      return { shape: 'descending', range: 8, stepSize: 1.5 };
    }
    // Chaotic: angular, large leaps
    return { shape: 'angular', range: 12, stepSize: 3 };
  }

  /**
   * Convert melodic shape to actual note sequence
   */
  shapedMelody(contour, modeNotes, length) {
    const notes = [];
    let position = 0;

    switch (contour.shape) {
      case 'arch_ascending':
        // Ascend, then descend back to root
        for (let i = 0; i < length / 2; i++) {
          notes.push(modeNotes[(i * 2) % modeNotes.length]);
        }
        for (let i = length / 2; i < length; i++) {
          notes.push(modeNotes[(Math.max(0, (length - i) * 2)) % modeNotes.length]);
        }
        break;

      case 'ascending':
        // Gradual rise
        for (let i = 0; i < length; i++) {
          notes.push(modeNotes[(Math.floor(i * 0.5)) % modeNotes.length]);
        }
        break;

      case 'descending':
        // Gradual fall
        for (let i = 0; i < length; i++) {
          const idx = modeNotes.length - 1 - Math.floor(i * 0.5);
          notes.push(modeNotes[Math.max(0, idx) % modeNotes.length]);
        }
        break;

      case 'wandering':
        // Random walk with small steps
        notes.push(0);
        for (let i = 1; i < length; i++) {
          const direction = Math.random() > 0.5 ? 1 : -1;
          const step = Math.floor(Math.random() * 2) * direction;
          const nextNote = Math.max(0, Math.min(modeNotes.length - 1, notes[i - 1] + step));
          notes.push(nextNote);
        }
        break;

      case 'angular':
        // Large, unpredictable leaps
        notes.push(0);
        for (let i = 1; i < length; i++) {
          const leap = Math.floor(Math.random() * (modeNotes.length - 1));
          notes.push(leap);
        }
        break;

      default:
        // Default: scale degrees
        for (let i = 0; i < length; i++) {
          notes.push((i * 2) % modeNotes.length);
        }
    }

    return notes.map(n => modeNotes[n % modeNotes.length]);
  }

  /**
   * Generate rhythm based on epistemic state
   * Returns rhythmic pattern as Strudel notation
   */
  generateRhythm(engagement, coherence, do_vec) {
    const tempo = 60 + engagement * 80;     // 60-140 BPM
    const swing = (1 - coherence) * 0.3;    // 0-0.3 swing factor
    const precision = do_vec > 0.7 ? 'tight' : 'loose';

    const patterns = {
      tight_fast: '~ bd hh bd hh bd hh bd',     // Energetic, locked
      tight_slow: 'bd ~ bd ~ bd ~ bd ~',       // Deliberate, precise
      loose_fast: 'bd [hh hh] bd ~ hh bd hh',  // Swung, groovy
      loose_slow: 'bd ~ ~ bd ~ ~ bd ~'         // Sparse, breathing
    };

    const speed = engagement > 0.7 ? 'fast' : 'slow';
    const feel = precision === 'tight' ? 'tight' : 'loose';
    const key = `${feel}_${speed}`;

    return {
      pattern: patterns[key] || patterns.tight_fast,
      tempo: tempo.toFixed(0),
      swing: swing.toFixed(2)
    };
  }

  /**
   * Generate orchestration based on signal + engagement
   * Combines instrument choices with texture
   */
  generateOrchestration(signal, engagement, state) {
    // Orchestration: instrument selection based on state
    const instruments = {
      sparse: ['sine'],                                    // Single clear voice
      minimal: ['sine', 'square'],                         // Two voices
      balanced: ['sine', 'square', 'triangle'],            // Three-part texture
      dense: ['sine', 'square', 'triangle', 'sawtooth'],   // Four-part
      full: ['sine', 'square', 'triangle', 'sawtooth', 'bass'] // Rich texture
    };

    const textureDensity = signal > 0.8 ? 'full' : signal > 0.65 ? 'dense' : signal > 0.5 ? 'balanced' : 'minimal';
    const instrs = instruments[textureDensity];

    return {
      texture: textureDensity,
      instruments: instrs,
      reverb: (state * 0.8).toFixed(2),
      room_size: (0.2 + state * 0.6).toFixed(2)
    };
  }

  /**
   * Generate chord voicing that respects voice-leading rules
   */
  voiceChord(degree, mode) {
    const intervals = this.MODES[mode];
    const root = intervals[degree % intervals.length];

    // Voice as triad (root, third, fifth) or seventh chord
    const third = intervals[(degree + 2) % intervals.length];
    const fifth = intervals[(degree + 4) % intervals.length];
    const seventh = intervals[(degree + 6) % intervals.length];

    return {
      root,
      third,
      fifth,
      seventh,
      chord: [root, third, fifth]  // Triadic voicing
    };
  }

  /**
   * Master composition engine
   * Returns complete Strudel composition from mesh state
   */
  compose(vectors) {
    const v = vectors;

    // 1. Select tonality
    const tonality = this.selectTonality(v.know, v.clarity, v.coherence);
    const modeNotes = this.MODES[tonality];

    // 2. Generate harmonic progression
    const progression = this.generateProgression(v.coherence, v.completion);

    // 3. Generate melodic contour
    const contour = this.generateMelodic(v.completion, v.uncertainty, v.know, v.signal);
    const melodyLength = Math.max(4, Math.round(8 + v.signal * 8));
    const melody = this.shapedMelody(contour, modeNotes, melodyLength);

    // 4. Generate rhythm
    const rhythm = this.generateRhythm(v.engagement, v.coherence, v.do);

    // 5. Generate orchestration
    const orchestration = this.generateOrchestration(v.signal, v.engagement, v.state);

    // 6. Build Strudel code
    const cps = (parseInt(rhythm.tempo) / 120 / 60).toFixed(3);
    const melodyStr = melody.join(' ');
    const progStr = progression.join(' ');

    return `setcps(${cps})  // Tempo: ${rhythm.tempo} BPM | Tonality: ${tonality} | Coherence: ${v.coherence.toFixed(2)}

// ━━━ HARMONIC FOUNDATION ━━━
// Progression: ${progression.map(d => ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii°'][d]).join(' → ')}
stack(
  s("bd").gain(0.8).room(${orchestration.room_size}),
  note("${progStr}").scale("${tonality}").s("square").gain(0.4).cutoff(1000).room(${orchestration.room_size})
).out()

// ━━━ MELODIC LINE ━━━
// Shape: ${contour.shape} | Clarity: ${v.clarity.toFixed(2)} | Completion: ${v.completion.toFixed(2)}
note("${melodyStr}").scale("${tonality}").s("sine").gain(0.5).cutoff(${2000 + v.clarity * 2000}).room(${orchestration.room_size}).out()

// ━━━ MESH STATE SIGNATURE ━━━
// LI: ${v.state.toFixed(3)} | Know: ${v.know.toFixed(2)} | Coherence: ${v.coherence.toFixed(2)} | Uncertainty: ${v.uncertainty.toFixed(2)}`;
  }

  /**
   * Explain the mapping for learning
   */
  explain(vectors) {
    const v = vectors;
    const tonality = this.selectTonality(v.know, v.clarity, v.coherence);
    const contour = this.generateMelodic(v.completion, v.uncertainty, v.know, v.signal);
    const rhythm = this.generateRhythm(v.engagement, v.coherence, v.do);

    return {
      tonality: {
        choice: tonality,
        reason: `Selected based on know(${v.know.toFixed(2)}) + clarity(${v.clarity.toFixed(2)}) + coherence(${v.coherence.toFixed(2)})`
      },
      melody: {
        shape: contour.shape,
        reason: `Based on completion(${v.completion.toFixed(2)}) and uncertainty(${v.uncertainty.toFixed(2)})`
      },
      rhythm: {
        tempo: `${rhythm.tempo} BPM`,
        reason: `Engagement: ${v.engagement.toFixed(2)} (60-140 BPM range)`
      },
      state: {
        li: v.state.toFixed(3),
        field: v.state >= 0.97 ? 'Calibrated' : v.state >= 0.8 ? 'Power' : 'Force Dominant'
      }
    };
  }
}

// Export for use in ControlRoom
if (typeof module !== 'undefined' && module.exports) {
  module.exports = MeshToMusicTheory;
}
