# Yourdio Theme System - Complete Integration

## Summary

The Yourdio theme system allows complete control over musical style through YAML configuration files. All compositional decisions are externalized from code - no Python editing required.

---

## What's Been Built

### Core Files
1. **`yourdio.py`** - Main composition generator (reads themes)
2. **`theme_loader.py`** - YAML loader with validation
3. **`analyze_reference.py`** - Audio analysis to auto-generate themes
4. **`event_generator.py`** - Short event soundscapes (NEW!)
5. **`playback_audio.py`** - MIDI playback

### Theme Files
- **`theme_schema.yaml`** - Parameter reference template
- **`themes/conan_epic.yaml`** - Epic orchestral (Poledouris-inspired)
- **`themes/tavern_carousing.yaml`** - Lively tavern atmosphere
- **`themes/combat_intense.yaml`** - Fast, aggressive battle music
- **`themes/stealth_tension.yaml`** - Sparse, tense sneaking
- **`themes/victory_triumph.yaml`** - Triumphant fanfare
- **`themes/ambient_myst.yaml`** - Crystalline, mysterious
- **`themes/doom_e1m1.yaml`** - Dark, industrial
- **`themes/secret_of_mana.yaml`** - Warm, organic

### Documentation
- **`THEME_SYSTEM.md`** - Theme parameter reference
- **`EVENT_SOUNDSCAPES.md`** - Event generator guide
- **`PLAYBACK_WINDOWS.md`** - Playback options

---

## How It Works

### Theme-Driven Architecture

Themes control ALL musical parameters:
- **Modal Center**: Scale/mode (D_dorian, A_aeolian, E_phrygian, or custom scales)
- **Harmony**: Chord voicings (quartal, tertian, dissonant clusters, power chords)
- **Tempo**: Base BPM and variation range
- **Instrumentation**: General MIDI patch numbers (0-127)
- **Dynamics**: Velocity ranges per layer
- **Rhythm**: Duration multipliers and timing behavior
- **Structure**: Intensity arc type (parabolic, slow_burn, descending, flat)
- **Motif**: Recurring melodic pattern
- **Chaos**: Logistic map and Lorenz attractor parameters

### The Composition Engine

The system generates music using mathematical patterns:

1. **Prime Number Sequences** - Modulate parameters organically over time
2. **Fibonacci Rhythms** - Create natural-feeling note durations
3. **Lorenz Attractor** - Smooth filter sweeps and parameter evolution
4. **Logistic Map** - Generate rare, dramatic events at specific chaos thresholds
5. **Intensity Arcs** - Control dynamic build over 12 chapters (6 hours)

Four layers are generated per chapter:
- **Harmonic Bed** (Track 0): Slow-moving pad chords
- **Melodic Texture** (Track 1): Sparse melodic fragments with motifs
- **Drones** (Track 2): Deep sustained bass with filter modulation
- **Ambient Events** (Track 3): Rare dramatic punctuations

---

## Three Usage Modes

### Mode 1: Pre-Made Themes (Easiest)
```bash
# 6-hour epic composition
python yourdio.py --theme themes/conan_epic.yaml --output conan_output

# Tavern atmosphere
python yourdio.py --theme themes/tavern_carousing.yaml --output tavern_output
```

### Mode 2: Analyze Reference Audio (No Music Knowledge Required!)
```bash
# Analyze a song you like
python analyze_reference.py ~/Music/favorite_song.mp3 --output themes/my_theme.yaml

# Generate music with that style
python yourdio.py --theme themes/my_theme.yaml --output my_music
```

**What the analyzer extracts:**
- Tempo (BPM)
- Brightness (spectral centroid → instrument choice)
- Mode (major/minor/modal via chroma analysis)
- Energy (RMS amplitude → dynamics)
- Complexity (spectral flatness → harmony density)

### Mode 3: Hand-Craft Themes (For Musicians)
```bash
# Copy template
cp theme_schema.yaml themes/my_custom.yaml

# Edit parameters (see THEME_SYSTEM.md for details)
# Generate
python yourdio.py --theme themes/my_custom.yaml --output custom_output
```

---

## Event Soundscapes (NEW!)

Generate short, loopable music for specific game events:

```bash
# List available events
python event_generator.py --list

# Generate single event
python event_generator.py --event fight --theme themes/combat_intense.yaml

# Generate multiple events
python event_generator.py --events carousing fight stealth

# Generate ALL 8 event types
python event_generator.py --all --theme themes/tavern_carousing.yaml
```

**Available events:**
- **carousing** (2 min) - Tavern atmosphere
- **fight** (1.5 min) - Combat music
- **stealth** (3 min) - Tense sneaking
- **victory** (1 min) - Triumphant fanfare
- **exploration** (4 min) - Atmospheric wandering
- **tension** (2.5 min) - Building dread
- **rest** (3 min) - Peaceful campfire
- **death** (0.5 min) - Failure sting

See `EVENT_SOUNDSCAPES.md` for details.

---

## Playback

```bash
# Play a single MIDI file
python playback_audio.py --file path/to/file.mid

# Play specific chapter
python playback_audio.py --chapter 0 --dir conan_output

# Play all 12 chapters (6 hours!)
python playback_audio.py --dir conan_output
```

---

## Key Theme Parameters

| Parameter | Controls | Examples |
|-----------|----------|----------|
| `modal_center` | Scale/mode | `D_dorian`, `A_aeolian`, `E_phrygian` |
| `harmony_rules.intervals` | Chord voicing | `[0,3,6]` quartal, `[0,2,4]` tertian |
| `ensemble_gm.harmonic_bed` | Pad instrument | 88=Pad 1, 89=Pad 2, 95=Pad 8 |
| `tempo.base` | Speed (BPM) | 48-140 |
| `structural_arc.type` | 6-hour shape | `slow_burn`, `parabolic`, `flat` |
| `dynamics.base_velocity` | Loudness | 25-100 |
| `motif.core_pattern` | Melody | `[0,2,5,7]` scale degrees |
| `chaos.logistic_r` | Unpredictability | 3.70-3.95 |

See `THEME_SYSTEM.md` for complete parameter reference.

---

## Quick Examples

### Example 1: Epic 6-Hour Journey
```bash
python yourdio.py --theme themes/conan_epic.yaml --output conan_6hr
# Generates 12 chapters building from intensity 0.4 to 0.95
# Tempo increases from 68 to 79 BPM
# Features brass, strings, timpani
```

### Example 2: Tavern Combat Music
```bash
# Generate 1.5-minute fight music with tavern instruments (bar brawl!)
python event_generator.py --event fight --theme themes/tavern_carousing.yaml
```

### Example 3: Custom Theme from Your Favorite Track
```bash
# Analyze a reference track
python analyze_reference.py ~/Music/ambient_track.mp3 --output themes/my_vibe.yaml

# Generate 6 hours of music in that style
python yourdio.py --theme themes/my_vibe.yaml --output my_ambient
```

---

## Dependencies

### Basic (MIDI generation):
```bash
pip install midiutil numpy pyyaml pygame
```

### Optional (audio analysis):
```bash
pip install librosa
```

---

## File Sizes

**Why MIDI?** Extremely compact:
- 6-hour composition: ~70 KB (12 MIDI files)
- Single 2-minute event: ~3 KB
- All 8 event types: ~30 KB total

Renders instantly (<10 seconds for 6 hours) vs. hours for audio rendering.

---

## Architecture Notes

### How Themes Are Applied

1. **Theme Loading**: `ThemeLoader.load()` reads YAML, validates, merges with defaults
2. **Composer Init**: `RetroMIDIComposer(theme)` extracts all parameters
3. **Chapter Generation**: Each 30-minute chapter uses theme parameters + prime sequences
4. **Intensity Evolution**: `calculate_chapter_intensity()` uses theme's `structural_arc`
5. **Parameter Evolution**: Tempo, polyphony, velocity can evolve with intensity

### Layer Generation

Each layer reads specific theme sections:
- `_generate_harmonic_bed()` → `rhythmic_language.harmonic_bed`, `dynamics.harmonic_bed`
- `_generate_melodic_texture()` → `motif`, `rhythmic_language.melodic_texture`
- `_generate_drones()` → `rhythmic_language.drones`, `chaos.lorenz_*`
- `_generate_ambient_events()` → `rhythmic_language.ambient_events`, `chaos.logistic_r`

---

## Success Criteria

✅ All compositional parameters externalized to YAML
✅ 9 complete themes created (Conan, tavern, combat, stealth, victory, Myst, Doom, SoM, default)
✅ Event generator for short soundscapes
✅ Audio analysis → automatic theme generation
✅ MIDI playback system
✅ Complete documentation
✅ Sub-10-second generation for 6 hours

**The system is production-ready!**
