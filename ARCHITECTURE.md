# Yourdio Architecture

## Overview

Yourdio generates **6-hour algorithmic ambient compositions** or **short event soundscapes** using mathematical patterns and YAML-configured themes. The system produces tiny MIDI files (~70 KB for 6 hours) that render instantly.

---

## Core Concept: Retro Lo-Fi Symbolic Composition

**Why MIDI + General MIDI?**
- **Speed**: 6 hours renders in <10 seconds (vs. hours for audio)
- **Size**: 70 KB total (vs. ~6 GB for audio stems)
- **Determinism**: 100% reproducible, no DSP artifacts
- **Iteration**: Test full pipeline in seconds, not days
- **Aesthetic**: Authentic retro game music (Secret of Mana, Myst, Doom era)

---

## Mathematical Foundation

### 1. Prime Number Sequences
Prime numbers (2, 3, 5, 7, 11, 13, 17, ...) modulate parameters over time:
- Chord durations
- Velocity variations
- Harmony choices
- Register shifts

**Why primes?** They create organic, non-repeating patterns that feel natural rather than mechanical.

### 2. Fibonacci Rhythms
Fibonacci sequence (1, 1, 2, 3, 5, 8, 13, ...) generates note durations:
- Natural-feeling rhythm patterns
- Golden ratio proportions
- Scales from theme's `base_unit` parameter

### 3. Lorenz Attractor
3D chaotic system creates smooth, unpredictable parameter evolution:
- Filter sweeps on drone layer
- Continuous modulation without sudden jumps
- Configured via `chaos.lorenz_sigma`, `lorenz_rho`, `lorenz_beta`

**The equations:**
```
dx/dt = σ(y - x)
dy/dt = x(ρ - z) - y
dz/dt = xy - βz
```

### 4. Logistic Map
Simple chaos equation generates rare dramatic events:
```
x(n+1) = r × x(n) × (1 - x(n))
```

- Events only trigger when `x > threshold` (typically 0.85-0.92)
- Controlled via `chaos.logistic_r` (3.84-3.95 for chaos)
- Creates thunder rolls, metallic swells, shimmers

### 5. Intensity Arcs
Chapter-by-chapter intensity evolution over 6 hours:

- **Parabolic**: Rises to climax, then falls (classical story arc)
- **Slow Burn**: Linear ascending build (epic film score)
- **Descending**: Starts intense, gradually calms
- **Flat**: Constant intensity (meditation, ambience)

Intensity (0.0-1.0) modulates:
- Tempo (within theme's `variation_range`)
- Polyphony (voice count)
- Velocity (loudness)
- Register (pitch range)

---

## Four-Layer Architecture

Each chapter generates 4 parallel MIDI tracks:

### Track 0: Harmonic Bed (Pads)
**Purpose**: Slow-moving harmonic foundation

**Generation**:
1. Select root note from scale (rotates via prime index)
2. Build chord using `harmony_rules.intervals`
3. Duration = `base_duration + (prime % prime_mod_factor)`
4. Velocity = `base_velocity + (prime % prime_mod_range)`
5. Add notes to MIDI with slight overlap

**Theme Parameters**:
- `rhythmic_language.harmonic_bed`
- `dynamics.harmonic_bed`
- `harmony_rules`
- `ensemble_gm.harmonic_bed` (instrument)

### Track 1: Melodic Texture (Lead)
**Purpose**: Sparse melodic fragments with recurring motif

**Generation**:
1. Wait `motif_interval` beats
2. Play `motif.core_pattern` notes from scale
3. Use Fibonacci sequence for note durations
4. Prime numbers modulate register shifts
5. Add ornaments based on density

**Theme Parameters**:
- `motif.core_pattern` (melodic shape)
- `motif.interval_minutes` (how often)
- `rhythmic_language.melodic_texture`
- `dynamics.melodic_texture`
- `ensemble_gm.melodic_texture`

### Track 2: Drones (Bass)
**Purpose**: Deep sustained bass with filter modulation

**Generation**:
1. Play root note two octaves down
2. Hold for `prime × duration_multiplier` beats
3. Use Lorenz attractor for continuous CC74 (filter brightness)
4. Update filter every `cc_event_interval` beats

**Theme Parameters**:
- `rhythmic_language.drones.duration_multiplier`
- `rhythmic_language.drones.cc_event_interval`
- `dynamics.drones.velocity`
- `chaos.lorenz_*`
- `ensemble_gm.drones`

### Track 3: Ambient Events (Percussion/FX)
**Purpose**: Rare dramatic punctuations

**Generation**:
1. Run logistic map with `chaos_seed`
2. When `x > threshold`, trigger event
3. Choose event type based on intensity:
   - High (>0.9): Thunder roll (rapid tremolo + pitch bend)
   - Medium (>0.7): Metallic swell (ascending shimmer)
   - Low: Shimmer (gentle high notes)

**Theme Parameters**:
- `rhythmic_language.ambient_events.threshold`
- `rhythmic_language.ambient_events.event_count`
- `dynamics.ambient_events`
- `chaos.logistic_r`
- `ensemble_gm.ambient_events`

---

## Composition Pipeline

### Full 6-Hour Composition (`yourdio.py`)

```
1. Load Theme
   └─> ThemeLoader.load(theme_path)
   └─> Validate parameters
   └─> Merge with defaults

2. For each chapter (0-11):
   ├─> Calculate intensity (structural_arc)
   ├─> Evolve parameters (tempo, polyphony)
   ├─> Select prime subsequence
   ├─> Generate chaos seed
   └─> Create chapter MIDI:
       ├─> Track 0: Harmonic bed (pad chords)
       ├─> Track 1: Melodic texture (motifs)
       ├─> Track 2: Drones (bass sustain)
       └─> Track 3: Ambient events (rare hits)

3. Save MIDI files
   └─> chapter_00.mid through chapter_11.mid
```

**Output**: 12 files × 30 minutes = 6 hours total

### Event Soundscapes (`event_generator.py`)

```
1. Load Theme (same as above)

2. Get event config:
   ├─> Duration (0.5-4 minutes)
   ├─> Prime sequence (event-specific)
   └─> Chaos seed (event-specific)

3. Generate single-chapter MIDI
   └─> Same 4-layer structure
   └─> Shorter duration
   └─> Event-specific parameters

4. Save MIDI file
   └─> event_theme.mid
```

**Output**: 1 loopable file per event

---

## Theme System

### Theme Structure

All themes follow this schema:

```yaml
name: "Theme Name"
description: "Brief description"

modal_center: 'D_dorian'  # or A_aeolian, E_phrygian, custom_scale

harmony_rules:
  type: 'quartal'  # or tertian, dissonant_clusters, power_chords
  intervals: [0, 3, 6]
  variation: 'power_chords'  # optional
  variation_intervals: [0, 4]
  variation_mod: 3

rhythmic_language:
  harmonic_bed: {base_duration: 32, prime_mod_factor: 8}
  melodic_texture: {sequence_length: 8, base_unit: 0.25}
  drones: {duration_multiplier: 4, cc_event_interval: 4}
  ambient_events: {threshold: 0.87, event_count: 64}

ensemble_gm:
  harmonic_bed: 89     # GM patch 0-127
  melodic_texture: 92
  drones: 95
  ambient_events: 99

tempo:
  base: 58
  variation_range: [52, 68]

dynamics:
  harmonic_bed: {base_velocity: 45, prime_mod_range: 20}
  melodic_texture: {base_velocity: 55, prime_mod_range: 25}
  drones: {velocity: 50}
  ambient_events: {base_velocity: 60, intensity_scaling: 30}

structural_arc:
  type: 'parabolic'  # or slow_burn, descending, flat
  min_intensity: 0.2
  max_intensity: 0.8
  climax_chapter: 6

parameter_evolution:
  tempo: true
  polyphony: true
  velocity: true
  register: true

chaos:
  logistic_r: 3.86
  lorenz_sigma: 10.0
  lorenz_rho: 28.0
  lorenz_beta: 2.667

motif:
  core_pattern: [0, 2, 5, 7]
  interval_minutes: 17
  register_shift_prime_mod: 2
  ornament_density_mod: 5
```

### Theme Categories

**Long-Form (6-hour journeys)**:
- `conan_epic.yaml` - Epic orchestral build
- `ambient_myst.yaml` - Crystalline mystery
- `doom_e1m1.yaml` - Dark industrial
- `secret_of_mana.yaml` - Warm organic

**Event-Specific (short loops)**:
- `tavern_carousing.yaml` - Upbeat, folk
- `combat_intense.yaml` - Fast, aggressive
- `stealth_tension.yaml` - Sparse, quiet
- `victory_triumph.yaml` - Triumphant, loud

---

## Polyphony Limiting

Authentic hardware constraints (e.g., OPL3 = 18 voices, GM = 32 voices):

```
1. Track active notes with end times
2. Before adding note:
   ├─> Remove notes that have ended
   ├─> If count < max_polyphony: Add note
   └─> Else: Voice steal (remove oldest)
```

This recreates authentic 1994-era voice limitations for retro feel.

---

## Audio Analysis (`analyze_reference.py`)

Automatically generate themes from audio files using `librosa`:

**Extracted Features**:
1. **Tempo**: Beat detection → `tempo.base`
2. **Brightness**: Spectral centroid → instrument choices
3. **Mode**: Chroma analysis → `modal_center`
4. **Energy**: RMS amplitude → dynamics
5. **Complexity**: Spectral flatness → harmony density

**Mapping**:
```
Brightness → GM patch selection
  High (>8000 Hz) → Bell/crystal sounds
  Low (<4000 Hz) → Warm pads/strings

Energy → Velocity
  High → base_velocity 60-80
  Low → base_velocity 30-50

Complexity → Harmony
  Complex → Dense tertian chords
  Simple → Sparse quartal/single notes
```

---

## File Organization

```
Yourdio/
├── yourdio.py              # Main 6-hour generator
├── event_generator.py      # Short event soundscapes
├── theme_loader.py         # YAML validation/loading
├── analyze_reference.py    # Audio → theme conversion
├── playback_audio.py       # MIDI player
├── theme_schema.yaml       # Parameter reference
├── themes/
│   ├── conan_epic.yaml
│   ├── tavern_carousing.yaml
│   ├── combat_intense.yaml
│   ├── stealth_tension.yaml
│   ├── victory_triumph.yaml
│   ├── ambient_myst.yaml
│   ├── doom_e1m1.yaml
│   └── secret_of_mana.yaml
└── docs/
    ├── ARCHITECTURE.md     # This file
    ├── README_THEME_INTEGRATION.md
    ├── THEME_SYSTEM.md
    ├── EVENT_SOUNDSCAPES.md
    └── PLAYBACK_WINDOWS.md
```

---

## Design Philosophy

### Constraints as Features

**1994 Lo-Fi Aesthetic:**
- General MIDI only (no custom samples)
- 18-32 voice polyphony limits
- 16-bit quantized MIDI timing
- Simple reverb/modulation (CC events)

These limitations force creative solutions and create authentic retro feel.

### Deterministic Chaos

Mathematical chaos (Lorenz, logistic map) provides:
- Organic unpredictability
- Smooth evolution (not random jumps)
- Reproducible results (same seed = same output)
- Natural-sounding variation

### Prime-Driven Variation

Prime numbers prevent:
- Mechanical repetition
- Obvious patterns
- Loop fatigue
- Predictable evolution

Result: 6 hours that never feels repetitive.

### Theme-Driven Composition

Separate "what to play" (code) from "how it sounds" (themes):
- Non-musicians can use analysis or presets
- Musicians can hand-craft parameters
- Same code, infinite musical styles
- Share themes like software configs

---

## Performance Characteristics

**Generation Speed:**
- 6-hour composition: ~8 seconds
- Single 2-minute event: <1 second
- All 8 events: ~5 seconds

**File Sizes:**
- 6 hours (12 chapters): ~70 KB
- 2-minute event: ~3 KB
- Theme file: ~2 KB

**Memory Usage:**
- Peak: <100 MB RAM
- No audio buffers needed
- Minimal state tracking

---

## Extension Points

### Adding New Modes/Scales
Edit `RetroMIDIComposer._build_scale()` to add:
```python
scales = {
    'C_lydian': [60, 62, 64, 66, 67, 69, 71, 72],  # C D E F# G A B C
    # ...
}
```

Or use `custom_scale` in theme YAML.

### Adding New Event Types
Edit `EventSoundscapeGenerator.EVENT_CONFIGS`:
```python
'boss_fight': {
    'duration_minutes': 3.0,
    'primes': [2, 3, 5, 7, 11],
    'chaos_seed': 0.95,
    'description': 'Epic boss battle'
}
```

### Adding New Instruments
Just change GM patch numbers in themes (0-127):
- 0-7: Piano
- 8-15: Chromatic Percussion
- 16-23: Organ
- 24-31: Guitar
- 32-39: Bass
- 40-47: Strings
- 48-55: Ensemble
- 56-63: Brass
- 64-71: Reed
- 72-79: Pipe
- 80-87: Synth Lead
- 88-95: Synth Pad
- 96-103: Synth FX
- 104-111: Ethnic
- 112-119: Percussive
- 120-127: Sound FX

---

## Comparison to Traditional DAW Workflow

| Aspect | Yourdio | Traditional DAW |
|--------|---------|-----------------|
| 6-hour composition time | ~10 seconds | Days to weeks |
| File size | 70 KB | 5-10 GB |
| Iteration speed | Instant | Minutes to hours |
| Reproducibility | Perfect | Difficult |
| Style control | YAML themes | Manual mixing |
| Learning curve | Copy/paste/edit | Steep |
| Retro aesthetic | Authentic | Requires careful sampling |

**Trade-off**: Less sonic detail/realism, but massively faster iteration and perfect for retro game audio.

---

## Recommended Reading

**Mathematical Background:**
- Chaos theory and strange attractors
- Fibonacci in music composition
- Prime number distribution
- Modal harmony systems

**Musical Concepts:**
- General MIDI specification
- Voice leading in quartal harmony
- Retro game music composition
- Ambient music theory (Eno, Roach)

**Technical References:**
- MIDI specification 1.0
- MIDIUtil Python library docs
- NumPy for mathematical operations
- PyYAML for configuration
