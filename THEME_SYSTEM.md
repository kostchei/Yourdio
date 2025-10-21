# Yourdio Theme System

## Overview

The Yourdio theme system externalizes all compositional decisions from code into **YAML configuration files**. This allows you to control musical style without editing Python code.

---

## Quick Start

### Method 1: Use Pre-Made Themes

```bash
# List available themes
python theme_loader.py

# Use a theme
python build_yourdio_retro.py --theme themes/ambient_myst.yaml --output ./output_myst
```

### Method 2: Analyze Reference Audio (No Musical Knowledge Required!)

```bash
# Analyze an audio file you like
python analyze_reference.py samples/your_favorite_track.mp3 themes/my_style.yaml

# Use the generated theme
python build_yourdio_retro.py --theme themes/my_style.yaml --output ./output_custom
```

### Method 3: Hand-Craft a Theme

1. Copy `theme_schema.yaml` to `themes/my_theme.yaml`
2. Edit parameters (see [Parameter Reference](#parameter-reference))
3. Generate music with your theme

---

## Workflow: From Audio Sample to Generated Music

### Step 1: Provide Reference Audio

You mentioned: **"I could provide samples but don't know how to set the dials"**

**Solution**: Use the `analyze_reference.py` tool!

```bash
# Analyze your reference track (any audio format)
python analyze_reference.py ~/Music/ambient_track.mp3 themes/my_ambient.yaml
```

**What it does:**
- Extracts **tempo** (BPM)
- Measures **brightness** (spectral centroid → dark vs bright timbres)
- Detects **mode** (major/minor/modal character)
- Calculates **energy** (calm vs intense)
- Estimates **complexity** (simple vs dense harmonies)

**Output**: A complete YAML theme file ready to use!

### Step 2: Review & Adjust (Optional)

The generated YAML is human-readable. You can tweak it manually:

```yaml
# themes/my_ambient.yaml
name: "My Custom Ambient"

tempo:
  base: 52  # ← Adjust if too fast/slow

ensemble_gm:
  harmonic_bed: 89  # ← Try different GM patch numbers (0-127)

dynamics:
  harmonic_bed:
    base_velocity: 45  # ← Make louder (increase) or quieter (decrease)
```

### Step 3: Generate Music

```bash
python build_yourdio_retro.py \
  --theme themes/my_ambient.yaml \
  --renderer gm \
  --output ./my_ambient_output
```

Done! You now have 6 hours of music in the style of your reference track.

---

## Pre-Made Themes

### `ambient_myst.yaml`
**Style**: Mysterious, crystalline, contemplative
**Inspired by**: Myst (1993)
**Characteristics**:
- Slow tempo (52 BPM)
- A aeolian mode (natural minor)
- Quartal harmony (stacked fourths)
- Rare, mysterious ambient events
- Crystalline GM patches (bells, pads)

### `doom_e1m1.yaml`
**Style**: Dark, industrial, aggressive
**Inspired by**: Doom (1993)
**Characteristics**:
- Medium tempo (64 BPM)
- E phrygian mode (dark, exotic)
- Dissonant clusters and power chords
- Frequent aggressive events
- Metallic/sawtooth timbres

### `secret_of_mana.yaml`
**Style**: Warm, organic, nostalgic
**Inspired by**: Secret of Mana (1993)
**Characteristics**:
- Gentle tempo (58 BPM)
- D dorian mode (bright minor)
- Tertian harmony (familiar triads)
- Choir and warm pad sounds
- Moderate event frequency

---

## Parameter Reference

### 🎵 **Modal Center** (Scale/Mode)
```yaml
modal_center: 'D_dorian'
```
**Options**:
- `D_dorian` - Bright minor, hopeful (like folk melodies)
- `A_aeolian` - Natural minor, melancholic
- `E_phrygian` - Dark, exotic, Spanish flavor

**Or define custom**:
```yaml
custom_scale: [62, 64, 65, 67, 69, 71, 72, 74]  # MIDI note numbers
```

---

### 🎹 **Harmony Rules** (Chord Construction)
```yaml
harmony_rules:
  type: 'quartal'
  intervals: [0, 3, 6]  # Scale degrees to stack
```

**Common Types**:
- **Quartal** `[0, 3, 6]` - Stacked fourths (open, ambiguous, modern)
- **Tertian** `[0, 2, 4]` - Triads (familiar, warm, traditional)
- **Quintal** `[0, 4, 8]` - Fifths (powerful, open, medieval)
- **Clusters** `[0, 1, 2]` - Adjacent notes (dissonant, tense, modern)

**Variation** (conditional alternate voicing):
```yaml
  variation: 'power_chords'
  variation_intervals: [0, 7]  # Perfect fifth
  variation_chance_mod: 3  # Triggers when (prime % 3 == 0)
```

---

### 🥁 **Rhythmic Language** (Timing Behavior)
```yaml
rhythmic_language:
  harmonic_bed:
    base_duration: 32  # Beats per chord
    prime_mod_factor: 8  # Adds variety: duration = base + (prime % factor)
```

**Controls pacing** for each layer:
- `harmonic_bed` - Chord change rate
- `melodic_texture` - Note durations (uses Fibonacci)
- `drones` - Drone length
- `ambient_events` - Event timing (chaos-driven)

---

### 🎺 **Ensemble** (Instrumentation)
```yaml
ensemble_gm:
  harmonic_bed: 89     # Pad 2 (warm)
  melodic_texture: 92  # Pad 5 (bowed)
  drones: 95           # Pad 8 (sweep)
  ambient_events: 99   # FX 4 (atmosphere)
```

**GM Patch Numbers** (0-127):
- **Pads**: 88-95 (New Age, Warm, Polysynth, Choir, Bowed, Metallic, Halo, Sweep)
- **FX**: 96-103 (Rain, Soundtrack, Crystal, Atmosphere, Brightness, Goblins, Echoes, Sci-Fi)
- **Leads**: 80-87 (Sawtooth, Square, etc.)
- **Full GM list**: [General MIDI Specification](https://www.midi.org/specifications-old/item/gm-level-1-sound-set)

---

### ⏱️ **Tempo**
```yaml
tempo:
  base: 58  # Base BPM
  variation_range: [52, 68]  # Min/max for intensity modulation
```

**Typical Ranges**:
- **Very Slow** (40-50 BPM) - Deep ambient, meditative
- **Slow** (50-60 BPM) - Standard ambient (Myst, Minecraft)
- **Medium** (60-70 BPM) - Gentle movement (Secret of Mana)
- **Moderate** (70-80 BPM) - Tense ambient (Doom)

---

### 🔊 **Dynamics** (Volume/Velocity)
```yaml
dynamics:
  harmonic_bed:
    base_velocity: 45  # MIDI velocity (0-127)
    prime_mod_range: 20  # Adds variation: velocity = base + (prime % range)
```

**Guidelines**:
- **Quiet** (30-50) - Subtle, background
- **Medium** (50-70) - Present but not dominant
- **Loud** (70-90) - Prominent, assertive
- **Very Loud** (90-127) - Aggressive (use sparingly in ambient)

---

### 📈 **Structural Arc** (6-Hour Journey)
```yaml
structural_arc:
  type: 'parabolic'  # Shape of intensity over 12 chapters
  min_intensity: 0.2  # Starting calm
  max_intensity: 0.8  # Peak intensity
  climax_chapter: 6  # Where the peak occurs (0-11)
```

**Arc Types**:
- **Parabolic** - Rises to middle, falls back down (∩ shape)
- **Slow Burn** - Gradually ascends (/ shape)
- **Descending** - Starts high, winds down (\ shape)
- **Flat** - Consistent intensity throughout (—)

---

### 🎼 **Motif** (Recurring Melody)
```yaml
motif:
  core_pattern: [0, 2, 5, 7]  # Scale degrees
  interval_minutes: 17  # Time between appearances
```

**Scale Degrees** are relative to your `modal_center`:
- In D dorian: `[0, 2, 5, 7]` = D, E, A, B
- In A aeolian: `[0, 2, 5, 7]` = A, B, E, F#

---

## Advanced: Reference Audio Analysis Details

### What Features Are Extracted

```python
# When you run:
python analyze_reference.py my_track.mp3 themes/output.yaml
```

**Extracted**:
1. **Tempo** - Beat tracking via librosa
2. **Brightness** - Spectral centroid (frequency content)
3. **Mode** - Chroma analysis (major/minor/modal detection)
4. **Energy** - RMS amplitude (loudness over time)
5. **Complexity** - Spectral flatness (harmonic vs noisy)

**Mapped to**:
- Tempo → `tempo.base`
- Brightness → `ensemble_gm` (bright/dark timbre choice)
- Mode → `modal_center`
- Energy → `dynamics` + `structural_arc`
- Complexity → `harmony_rules` (simple triads vs dissonant clusters)

### Tips for Best Results

**Good reference tracks**:
- At least 2-3 minutes long
- Representative of desired style
- Ambient/instrumental (vocals confuse the analyzer)
- Consistent mood throughout

**Examples**:
- ✅ Myst soundtrack ambient loops
- ✅ Minecraft - "Wet Hands" by C418
- ✅ Doom E1M1 ambient sections
- ❌ Pop songs with vocals
- ❌ Highly dynamic orchestral pieces

---

## Troubleshooting

### "My generated theme sounds too intense/calm"

**Edit the YAML**:
```yaml
dynamics:
  harmonic_bed:
    base_velocity: 35  # ← Lower this (was 45)

structural_arc:
  max_intensity: 0.6  # ← Reduce peak intensity (was 0.8)
```

### "I want slower/faster tempo"

```yaml
tempo:
  base: 45  # ← Decrease for slower (was 58)
```

### "Harmonies sound too dissonant/consonant"

```yaml
harmony_rules:
  intervals: [0, 2, 4]  # ← Change to tertian (was [0, 3, 6] quartal)
```

### "Wrong instrument sounds"

Browse [GM Patch List](https://www.midi.org/specifications-old/item/gm-level-1-sound-set) and update:

```yaml
ensemble_gm:
  harmonic_bed: 52  # ← Try Choir Aahs (was 89 Pad 2)
```

---

## Next Steps

1. **Try the pre-made themes first**:
   ```bash
   python build_yourdio_retro.py --theme themes/ambient_myst.yaml
   ```

2. **Analyze your favorite ambient track**:
   ```bash
   python analyze_reference.py ~/Music/favorite.mp3 themes/my_theme.yaml
   ```

3. **Iterate**: Adjust the generated YAML, re-render (takes ~2 minutes!)

4. **Share**: Contribute your themes to the community!

---

## Dependencies

For reference audio analysis, install:
```bash
pip install librosa numpy pyyaml
```

For MIDI generation (already required):
```bash
pip install midiutil numpy pyyaml
```
