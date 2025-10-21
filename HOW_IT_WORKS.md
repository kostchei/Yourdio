# How Yourdio Works

## The Big Idea

Yourdio generates hours of ambient music using **mathematical patterns** instead of pre-recorded samples or traditional composition. The result: tiny MIDI files that capture authentic 1994-era game music aesthetics.

---

## Why Retro Lo-Fi MIDI?

### The 1994 Game Audio Aesthetic

Think: **Doom**, **Master of Magic**, **Secret of Mana**, **Myst**

**Technical constraints of the era:**
- General MIDI synthesis (128 sounds)
- 18-32 simultaneous voices max
- 16-bit MIDI resolution
- Simple modulation (filter sweeps, pitch bends)

**Modern advantages:**
- ⚡ **Renders in seconds** (not hours)
- 💾 **70 KB for 6 hours** (not gigabytes)
- 🔁 **Perfect reproducibility**
- ✏️ **Instant iteration**
- 🎮 **Authentic retro sound**

---

## The Music Generation Process

### 1. Choose a Theme (Musical DNA)

Themes are YAML files that control EVERY musical decision:

```yaml
# Example: Epic orchestral theme
modal_center: 'D_dorian'          # Scale (bright minor)
tempo: {base: 72, variation_range: [68, 80]}
ensemble_gm:
  harmonic_bed: 48   # Strings
  melodic_texture: 56  # Trumpet
  drones: 42         # Cello
  ambient_events: 47   # Timpani

harmony_rules:
  intervals: [0, 2, 4]  # Major/minor triads

structural_arc:
  type: 'slow_burn'    # Build continuously
  min_intensity: 0.4
  max_intensity: 0.95
```

**Think of themes as "musical DNA"** - they define the personality, not the notes.

### 2. Mathematical Pattern Generation

The system uses math to create organic-feeling music:

#### Prime Numbers → Natural Variation
```
Primes: 2, 3, 5, 7, 11, 13, 17, 19, 23...
```
Used for:
- Chord duration: `32 + (prime % 8)` beats
- Velocity: `45 + (prime % 20)`
- Harmony choices: use variation when `prime % 3 == 0`

**Why?** Primes never repeat patterns, preventing mechanical repetition over 6 hours.

#### Fibonacci → Rhythmic Flow
```
Fibonacci: 1, 1, 2, 3, 5, 8, 13, 21...
```
Used for melodic note durations:
- Natural golden ratio proportions
- Feels organic, not gridded
- Scales by theme's `base_unit`

#### Lorenz Attractor → Smooth Evolution
```
3D chaotic butterfly system
x' = σ(y - x)
y' = x(ρ - z) - y
z' = xy - βz
```
Used for:
- Continuous filter sweeps on bass drones
- Smooth parameter changes without jumps
- Maps X coordinate to filter brightness (CC74)

#### Logistic Map → Rare Events
```
x_next = r × x × (1 - x)
```
Used for:
- Dramatic percussion hits
- Only triggers when x > threshold (0.85-0.92)
- Thunder rolls, metallic swells, shimmers

### 3. Four-Layer Construction

Each 30-minute chapter generates 4 parallel tracks:

**Track 0: Harmonic Bed** (Slow pad chords)
- Every ~30-40 beats
- Uses harmony_rules for voicing
- GM pad sounds (88-95)

**Track 1: Melodic Texture** (Sparse melodies)
- Recurring motif pattern
- Fibonacci rhythm durations
- GM lead sounds (brass, flute, synth)

**Track 2: Drones** (Deep bass sustain)
- Root note, 2 octaves down
- Lorenz attractor controls filter
- Very long durations (prime × 4 beats)

**Track 3: Ambient Events** (Rare hits)
- Logistic map chaos triggers
- Thunder rolls, swells, shimmers
- GM percussion/FX

### 4. Intensity Evolution

Over 12 chapters (6 hours), intensity evolves:

**Structural Arc Types:**

**Parabolic** (traditional story):
```
Intensity:  0.2 → 0.5 → 0.8 (climax) → 0.5 → 0.2
Chapters:    0    3    6              9    11
```

**Slow Burn** (epic build):
```
Intensity:  0.4 → 0.5 → 0.7 → 0.8 → 0.95
Chapters:    0    3    6    9    11
```

**Flat** (meditation):
```
Intensity:  0.5 → 0.5 → 0.5 → 0.5 → 0.5
Chapters:    0    3    6    9    11
```

Intensity controls:
- **Tempo**: Interpolate between min/max
- **Polyphony**: More voices = more complexity
- **Velocity**: Louder = more intense
- **Register**: Higher pitches for climax

---

## Examples

### Example 1: Conan Epic (Slow Burn)

**Theme**: `conan_epic.yaml`
- Mode: D Dorian (heroic bright minor)
- Tempo: 72 BPM → 80 BPM
- Arc: Slow burn (0.4 → 0.95)
- Instruments: Strings, trumpet, cello, timpani

**What happens:**
1. Chapter 0 starts at intensity 0.4, tempo 72
2. Every chapter, intensity climbs linearly
3. By chapter 11: intensity 0.95, tempo 80
4. More voices, louder dynamics, higher register
5. Result: 6-hour epic build like film score

### Example 2: Tavern Carousing (Flat)

**Theme**: `tavern_carousing.yaml`
- Mode: D Dorian (cheerful)
- Tempo: 112 BPM (lively)
- Arc: Flat (0.6 → 0.7, constant merriment)
- Instruments: Acoustic guitar, flute, bass, vibes

**What happens:**
1. Fast tempo throughout (112 BPM)
2. Consistent intensity (no build)
3. Short chord durations (8 beats) = bouncy
4. Frequent motif (every 30 seconds)
5. Result: Upbeat tavern loop

### Example 3: Stealth Tension (Flat)

**Theme**: `stealth_tension.yaml`
- Mode: A Aeolian (dark minor)
- Tempo: 48 BPM (very slow)
- Arc: Flat (0.3 → 0.4, sustained tension)
- Instruments: Eerie pads, crystal FX, choir, bells

**What happens:**
1. Very slow tempo (48 BPM)
2. Sparse notes (long 64-beat durations)
3. Quiet velocities (25-40)
4. Rare events (threshold 0.92)
5. Result: Tense, sparse atmosphere

---

## Event Soundscapes

Short, loopable moments for specific situations:

```python
# event_generator.py defines:
'fight': {
    'duration_minutes': 1.5,      # Short loop
    'primes': [2, 3, 5, 7],       # Aggressive sequence
    'chaos_seed': 0.87,           # High chaos
}
```

**Mix themes × events** for variety:
- Fight event + Tavern theme = Bar brawl
- Stealth event + Victory theme = Sneaky satisfaction
- Victory event + Combat theme = Brutal triumph

---

## The Theme System

### Three Ways to Control Style

**1. Use Pre-Made Themes** (easiest)
```bash
python yourdio.py --theme themes/conan_epic.yaml
```

**2. Analyze Audio** (no music knowledge)
```bash
python analyze_reference.py favorite_song.mp3 --output themes/my_theme.yaml
python yourdio.py --theme themes/my_theme.yaml
```
Extracts: tempo, brightness, mode, energy, complexity

**3. Hand-Craft** (musicians)
```bash
cp theme_schema.yaml themes/custom.yaml
# Edit parameters
python yourdio.py --theme themes/custom.yaml
```

### Key Theme Parameters

| Parameter | Effect | Example Values |
|-----------|--------|----------------|
| `modal_center` | Scale/mood | D_dorian, A_aeolian, E_phrygian |
| `tempo.base` | Speed | 48 (slow) to 140 (fast) |
| `harmony_rules.intervals` | Chord sound | [0,3,6] open, [0,2,4] full, [0,1,3] tense |
| `ensemble_gm.*` | Instruments | 0-127 GM patch numbers |
| `structural_arc.type` | 6-hour shape | slow_burn, parabolic, flat |
| `motif.core_pattern` | Melody | [0,2,5,7] scale degrees |
| `chaos.logistic_r` | Unpredictability | 3.70 (calm) to 3.95 (chaotic) |

---

## Why It Sounds Good

### 1. Mathematical Patterns Create Naturalness
- Prime numbers → never repeats
- Fibonacci → golden ratio feels right
- Lorenz chaos → smooth unpredictability
- Not random = not jarring

### 2. Constraint Breeds Creativity
- Limited to GM sounds → focus on composition
- Polyphony limits → voice leading matters
- Retro aesthetic → clear decision boundaries

### 3. Intensity Arcs Provide Structure
- Not random ambient noise
- Intentional dramatic shape
- Gives listener journey/narrative

### 4. Layer Independence
- Each track has its own rhythm
- Tracks interact in complex ways
- Creates dense texture from simple rules

---

## Technical Details

**See ARCHITECTURE.md for:**
- Detailed algorithm explanations
- Code structure
- Mathematical equations
- Performance characteristics

**See THEME_SYSTEM.md for:**
- Complete parameter reference
- GM instrument list
- Harmony theory
- Customization guide

**See EVENT_SOUNDSCAPES.md for:**
- Event types and durations
- Theme/event combinations
- Usage examples

---

## The Magic Moment

When you run:
```bash
python yourdio.py --theme themes/conan_epic.yaml --output conan
```

In ~8 seconds you get:
- 12 MIDI files (chapter_00.mid → chapter_11.mid)
- 6 hours of music
- 70 KB total file size
- Plays on any MIDI player
- Authentic 1994 retro vibe
- Built with math, not samples

**That's the magic of algorithmic composition.**
