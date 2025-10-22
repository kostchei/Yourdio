# Yourdio

**Algorithmic retro lo-fi music generator for 6-hour ambient journeys and short event soundscapes**

Generate hours of music in seconds using mathematical patterns, prime numbers, and chaos theory. Produces tiny MIDI files with authentic 1994-era game audio aesthetics.

```bash
# Generate 6-hour epic orchestral composition
python yourdio.py --theme themes/conan_epic.yaml --output conan

# Generate 1.5-minute combat music
python event_generator.py --event fight --theme themes/combat_intense.yaml

# Play it
python playback_audio.py --dir conan
```

**Result**: 70 KB of MIDI files, 6 hours of music, generated in ~8 seconds.

---

## Features

- ⚡ **Instant Generation**: 6 hours in 8 seconds (vs. days of composition)
- 💾 **Tiny Files**: 70 KB for 6 hours (vs. gigabytes)
- 🎮 **Retro Aesthetic**: Authentic 1994 General MIDI sound
- 🎨 **Theme-Driven**: Control all musical parameters via YAML
- 🔢 **Mathematical**: Prime numbers, Fibonacci rhythms, Lorenz attractors
- 🎵 **9 Pre-Made Themes**: Epic, tavern, combat, stealth, victory, Myst, Doom, SoM
- 🎬 **Event Soundscapes**: Short loops for games (fight, carousing, stealth, etc.)
- 🔁 **Perfectly Reproducible**: Same seed = same music

---

## Quick Start

### Install

```bash
pip install midiutil numpy pyyaml pygame
```

### Generate Music

```bash
# 6-hour epic composition (Conan-inspired)
python yourdio.py --theme themes/conan_epic.yaml --output conan_output

# Short tavern music (2 minutes, loopable)
python event_generator.py --event carousing --theme themes/tavern_carousing.yaml

# All 8 event types at once
python event_generator.py --all --theme themes/combat_intense.yaml
```

### Play Music

```bash
# Play specific chapter
python playback_audio.py --chapter 0 --dir conan_output

# Play all 12 chapters (6 hours)
python playback_audio.py --dir conan_output

# Play single file
python playback_audio.py --file events_output/fight_intense_combat.mid
```

---

## Available Themes

### Long-Form (6-Hour Journeys)

- **`conan_epic.yaml`** - Epic orchestral, builds from 0.4 → 0.95 intensity (Basil Poledouris-inspired)
- **`ambient_myst.yaml`** - Crystalline, mysterious pads (Myst-inspired)
- **`doom_e1m1.yaml`** - Dark industrial, pounding rhythms (Doom-inspired)
- **`secret_of_mana.yaml`** - Warm organic, nostalgic (Secret of Mana-inspired)

### Event Soundscapes (Short Loops)

- **`tavern_carousing.yaml`** - Upbeat folk, 112 BPM, guitar/flute
- **`combat_intense.yaml`** - Aggressive metal, 140 BPM, dissonant
- **`stealth_tension.yaml`** - Sparse ambient, 48 BPM, very quiet
- **`victory_triumph.yaml`** - Triumphant brass, 120 BPM, loud

---

## How It Works

### Mathematical Foundation

1. **Prime Number Sequences** (2, 3, 5, 7, 11, 13...) modulate parameters over time
2. **Fibonacci Rhythms** (1, 1, 2, 3, 5, 8...) create natural note durations
3. **Lorenz Attractor** (3D chaos) provides smooth filter sweeps
4. **Logistic Map** (chaos equation) triggers rare dramatic events
5. **Intensity Arcs** shape the 6-hour journey

### Four-Layer Architecture

Each 30-minute chapter generates 4 MIDI tracks:
- **Track 0**: Harmonic bed (slow pad chords)
- **Track 1**: Melodic texture (sparse motifs)
- **Track 2**: Drones (deep bass with filter modulation)
- **Track 3**: Ambient events (rare percussion/FX hits)

### Theme System

All musical decisions controlled via YAML:

```yaml
modal_center: 'D_dorian'          # Scale
tempo: {base: 72, variation_range: [68, 80]}
harmony_rules:
  intervals: [0, 2, 4]             # Chord voicing
ensemble_gm:
  harmonic_bed: 48    # Strings
  melodic_texture: 56   # Trumpet
structural_arc:
  type: 'slow_burn'     # Build continuously
  max_intensity: 0.95
```

---

## Usage Examples

### Example 1: Epic 6-Hour Build

```bash
python yourdio.py --theme themes/conan_epic.yaml --output conan_6hr
```

**What you get:**
- 12 chapters (chapter_00.mid → chapter_11.mid)
- Starts at intensity 0.4, tempo 72 BPM
- Builds to intensity 0.95, tempo 80 BPM
- Strings, trumpet, cello, timpani
- 70 KB total, 6 hours music

### Example 2: Tavern Fight Scene

```bash
# Bar brawl: fight event with tavern instruments
python event_generator.py --event fight --theme themes/tavern_carousing.yaml
```

**What you get:**
- 1.5 minutes, loopable
- Acoustic guitar, flute, bass, vibes
- But with fight rhythm patterns (fast, chaotic)
- ~3 KB file

### Example 3: Custom Theme from Audio

```bash
# Analyze your favorite track
python analyze_reference.py ~/Music/ambient_track.mp3 --output themes/my_style.yaml

# Generate 6 hours in that style
python yourdio.py --theme themes/my_style.yaml --output my_music
```

**What it extracts:**
- Tempo (BPM)
- Brightness → instrument selection
- Mode (major/minor)
- Energy → dynamics
- Complexity → harmony density

---

## Event Soundscapes

8 pre-configured event types for games/interactive media:

| Event | Duration | Description |
|-------|----------|-------------|
| **carousing** | 2.0 min | Lively tavern atmosphere |
| **fight** | 1.5 min | Intense combat music |
| **stealth** | 3.0 min | Tense sneaking atmosphere |
| **victory** | 1.0 min | Triumphant fanfare |
| **exploration** | 4.0 min | Atmospheric wandering |
| **tension** | 2.5 min | Building dread |
| **rest** | 3.0 min | Peaceful campfire |
| **death** | 0.5 min | Failure sting |

```bash
# List all events
python event_generator.py --list

# Generate specific events
python event_generator.py --events fight victory stealth

# Generate all 8 with one theme
python event_generator.py --all --theme themes/combat_intense.yaml
```

Mix and match: Any theme + any event = unique combination!

---

## Creating Custom Themes

### Option 1: Copy and Edit

```bash
cp theme_schema.yaml themes/my_theme.yaml
# Edit themes/my_theme.yaml
python yourdio.py --theme themes/my_theme.yaml
```

### Option 2: Analyze Reference Audio

```bash
pip install librosa  # Required for audio analysis
python analyze_reference.py favorite_song.mp3 --output themes/my_theme.yaml
```

### Option 3: Use Presets

Just pick one:
```bash
python yourdio.py --theme themes/doom_e1m1.yaml
```

---

## Documentation

- **[HOW_IT_WORKS.md](HOW_IT_WORKS.md)** - Detailed explanation of music generation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical deep dive, algorithms, code structure
- **[THEME_SYSTEM.md](THEME_SYSTEM.md)** - Complete parameter reference
- **[EVENT_SOUNDSCAPES.md](EVENT_SOUNDSCAPES.md)** - Event generator guide
- **[PLAYBACK_WINDOWS.md](PLAYBACK_WINDOWS.md)** - Playback options
- **[README_THEME_INTEGRATION.md](README_THEME_INTEGRATION.md)** - Theme system overview

---

## Command Reference

### Main Generator (`yourdio.py`)

```bash
python yourdio.py [OPTIONS]

Options:
  --theme PATH       Path to theme YAML file (default: built-in)
  --output DIR       Output directory (default: midi_output)
```

### Event Generator (`event_generator.py`)

```bash
python event_generator.py [OPTIONS]

Options:
  --event TYPE       Generate single event (carousing, fight, etc.)
  --events TYPE...   Generate multiple events (space-separated)
  --all              Generate all 8 event types
  --theme PATH       Path to theme YAML file
  --output DIR       Output directory (default: events_output)
  --list             List available event types
```

### Audio Analyzer (`analyze_reference.py`)

```bash
python analyze_reference.py INPUT [OPTIONS]

Arguments:
  INPUT              Path to audio file (MP3, WAV, etc.)

Options:
  --output PATH      Output YAML file path
```

### Playback (`playback_audio.py`)

```bash
python playback_audio.py [OPTIONS]

Options:
  --file PATH        Play single MIDI file
  --dir PATH         Play all chapters from directory
  --chapter N        Play specific chapter (0-11)
```

---

## File Sizes & Performance

**6-Hour Composition:**
- File size: ~70 KB (12 MIDI files)
- Generation time: ~8 seconds
- Memory usage: <100 MB

**Single 2-Minute Event:**
- File size: ~3 KB
- Generation time: <1 second

**All 8 Events:**
- Total size: ~30 KB
- Generation time: ~5 seconds

---

## Why MIDI?

**Advantages:**
- ⚡ Renders in seconds, not hours
- 💾 Microscopic file sizes
- 🔁 100% reproducible
- ✏️ Instant iteration cycles
- 🎮 Authentic retro game aesthetic

**Trade-off:**
- Less sonic detail than full audio production
- Limited to General MIDI sound set
- Best for retro/lo-fi aesthetics

**Perfect for:**
- Retro game soundtracks
- Rapid prototyping
- Ambient background music
- Algorithmic composition experiments
- Learning music theory/composition

---

## Inspirations

**Musical:**
- Basil Poledouris (Conan the Barbarian)
- Robyn Miller (Myst)
- Bobby Prince (Doom)
- Hiroki Kikuta (Secret of Mana)
- Brian Eno (Ambient series)

**Technical:**
- Procedural generation (No Man's Sky, Minecraft)
- Algorithmic composition (Brian Eno's Bloom)
- Retro game audio (SNES, DOS era)
- Mathematical music (Xenakis, Hiller)

---

## Technical Stack

- **Python 3.13+**
- **MIDIUtil** - MIDI file generation
- **NumPy** - Mathematical operations
- **PyYAML** - Theme configuration
- **Pygame** - Audio playback
- **Librosa** (optional) - Audio analysis

---

## Project Structure

```
Yourdio/
├── yourdio.py                 # Main 6-hour generator
├── event_generator.py         # Short event soundscapes
├── theme_loader.py            # YAML validation/loading
├── analyze_reference.py       # Audio → theme conversion
├── playback_audio.py          # MIDI player
├── theme_schema.yaml          # Parameter template
├── themes/                    # Theme library
│   ├── conan_epic.yaml
│   ├── tavern_carousing.yaml
│   ├── combat_intense.yaml
│   ├── stealth_tension.yaml
│   ├── victory_triumph.yaml
│   ├── ambient_myst.yaml
│   ├── doom_e1m1.yaml
│   └── secret_of_mana.yaml
├── README.md                  # This file
├── HOW_IT_WORKS.md           # User-friendly explanation
├── ARCHITECTURE.md           # Technical deep dive
├── THEME_SYSTEM.md           # Parameter reference
├── EVENT_SOUNDSCAPES.md      # Event guide
└── PLAYBACK_WINDOWS.md       # Playback options
```

---

## License

MIT License - See LICENSE file for details.

---

## Contributing

Themes are the easiest way to contribute:
1. Create a new theme YAML file
2. Test it: `python yourdio.py --theme themes/your_theme.yaml`
3. Share it!

---

## Author

Built with mathematical composition principles and a love for retro game music.

---

## Quick Links

- **[Getting Started](#quick-start)** - Install and first run
- **[Themes](#available-themes)** - Browse pre-made themes
- **[Events](#event-soundscapes)** - Game event music
- **[Custom Themes](#creating-custom-themes)** - Make your own
- **[How It Works](HOW_IT_WORKS.md)** - Understand the magic
- **[Full Docs](#documentation)** - Complete reference
