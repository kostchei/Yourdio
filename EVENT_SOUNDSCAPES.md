# Event Soundscapes for Yourdio

Generate short, loopable musical moments for specific game events like combat, carousing, stealth, etc.

## Quick Start

### Generate a Single Event

```bash
# Generate a carousing (tavern) soundscape
python event_generator.py --event carousing --theme themes/tavern_carousing.yaml

# Generate combat music
python event_generator.py --event fight --theme themes/combat_intense.yaml

# Generate stealth music
python event_generator.py --event stealth --theme themes/stealth_tension.yaml
```

### Generate Multiple Events

```bash
# Generate specific events
python event_generator.py --events carousing fight victory

# Generate all 8 event types
python event_generator.py --all --theme themes/tavern_carousing.yaml
```

### List Available Events

```bash
python event_generator.py --list
```

## Available Event Types

| Event | Duration | Description |
|-------|----------|-------------|
| **carousing** | 2.0 min | Lively tavern atmosphere - ale, laughter, merriment |
| **fight** | 1.5 min | Intense combat music - fast, aggressive, adrenaline |
| **stealth** | 3.0 min | Tense sneaking atmosphere - sparse, quiet, suspenseful |
| **victory** | 1.0 min | Victory fanfare - triumphant, celebratory |
| **exploration** | 4.0 min | Atmospheric exploration - wonder, curiosity |
| **tension** | 2.5 min | Building tension/dread - unsettling, ominous |
| **rest** | 3.0 min | Peaceful rest/campfire - restorative, calm |
| **death** | 0.5 min | Death/failure sting - short, somber |

## Specialized Themes

### Tavern/Carousing Theme
**File**: `themes/tavern_carousing.yaml`

Perfect for tavern scenes, celebrations, and lively social gatherings.

**Musical Characteristics**:
- **Tempo**: 112 BPM (lively, danceable)
- **Mode**: D Dorian (bright, cheerful)
- **Harmony**: Simple folk triads
- **Instruments**:
  - Acoustic Guitar (strumming)
  - Flute (cheerful melody)
  - Acoustic Bass (walking bass)
  - Vibraphone (percussive accents)
- **Mood**: Energetic, jovial, rustic

**Usage**:
```bash
python event_generator.py --event carousing --theme themes/tavern_carousing.yaml
```

### Combat Theme
**File**: `themes/combat_intense.yaml`

Aggressive, fast-paced battle music for fights and action sequences.

**Musical Characteristics**:
- **Tempo**: 140 BPM (very fast, intense)
- **Mode**: E Phrygian (dark, exotic, menacing)
- **Harmony**: Dissonant clusters, tritones, power chords
- **Instruments**:
  - Overdriven Guitar (aggressive rhythm)
  - Trumpet (urgent brass stabs)
  - Synth Bass (driving low end)
  - Timpani (battle percussion)
- **Dynamics**: Very loud (85-100 velocity)
- **Mood**: Aggressive, chaotic, adrenaline-pumping

**Usage**:
```bash
python event_generator.py --event fight --theme themes/combat_intense.yaml
```

### Stealth/Tension Theme
**File**: `themes/stealth_tension.yaml`

Sparse, tense atmosphere for sneaking and suspenseful moments.

**Musical Characteristics**:
- **Tempo**: 48 BPM (very slow, creeping)
- **Mode**: A Aeolian (natural minor - dark)
- **Harmony**: Sparse quartal voicings, single notes
- **Instruments**:
  - Pad (sweep) - eerie background
  - Crystal FX - delicate high notes
  - Choir Pad - dark sustain
  - Tubular Bells - distant metallic sounds
- **Dynamics**: Very quiet (25-40 velocity)
- **Mood**: Tense, sparse, every sound matters

**Usage**:
```bash
python event_generator.py --event stealth --theme themes/stealth_tension.yaml
```

### Victory Theme
**File**: `themes/victory_triumph.yaml`

Triumphant fanfare for victories and quest completions.

**Musical Characteristics**:
- **Tempo**: 120 BPM (energetic)
- **Mode**: D Dorian (bright, heroic)
- **Harmony**: Full 7th chords, rich voicings
- **Instruments**:
  - String Ensemble (rich foundation)
  - Trumpet (heroic fanfare)
  - Trombone (brass bass)
  - Timpani (celebratory drums)
- **Dynamics**: Loud (80-95 velocity)
- **Mood**: Triumphant, celebratory, bold

**Usage**:
```bash
python event_generator.py --event victory --theme themes/victory_triumph.yaml
```

## Playing Event Soundscapes

```bash
# Play a specific event
python playback_audio.py --file events_output/fight_intense_combat.mid

# Play tavern music
python playback_audio.py --file events_output/carousing_tavern_carousing.mid

# Play stealth music
python playback_audio.py --file events_output/stealth_stealth_&_tension.mid
```

## Creating Custom Event Themes

You can mix and match themes with events! The event type controls:
- Duration
- Prime number sequence (affects variation pattern)
- Chaos seed (affects randomization)

The theme controls all musical parameters:
- Tempo, mode, harmony, rhythm
- Instrumentation
- Dynamics
- Intensity arc

**Example**: Generate a fight scene with the tavern theme (bar brawl!):
```bash
python event_generator.py --event fight --theme themes/tavern_carousing.yaml
# Creates: fight_tavern_carousing.mid (1.5 min of upbeat brawling music)
```

**Example**: Generate exploration with the combat theme (tense exploration):
```bash
python event_generator.py --event exploration --theme themes/combat_intense.yaml
# Creates: exploration_intense_combat.mid (4 min of aggressive wandering)
```

## Event Generator Options

```bash
# Generate single event
python event_generator.py --event <type> --theme <theme.yaml>

# Generate multiple specific events
python event_generator.py --events fight victory carousing --theme <theme.yaml>

# Generate all 8 event types
python event_generator.py --all --theme <theme.yaml>

# Custom output directory
python event_generator.py --all --output my_events/

# List available events
python event_generator.py --list
```

## File Sizes

Event soundscapes are tiny MIDI files:
- **fight** (1.5 min): ~2-3 KB
- **carousing** (2.0 min): ~3-4 KB
- **stealth** (3.0 min): ~2 KB (sparse)
- **victory** (1.0 min): ~2 KB

**Total for all 8 events**: < 30 KB

Perfect for games, interactive media, or streaming applications!

## Integration Examples

### Game Loop Integration

```python
from event_generator import EventSoundscapeGenerator

# Generate combat music when battle starts
combat_file = EventSoundscapeGenerator.generate_event(
    'fight',
    theme_path='themes/combat_intense.yaml'
)

# Play the file
play_midi(combat_file)
```

### Generate Event Set for a Game

```bash
# Generate complete event set with a specific theme
python event_generator.py --all --theme themes/tavern_carousing.yaml --output game_assets/audio/

# This creates 8 loopable MIDI files ready to use:
# - carousing_tavern_carousing.mid
# - fight_tavern_carousing.mid
# - stealth_tavern_carousing.mid
# - victory_tavern_carousing.mid
# - exploration_tavern_carousing.mid
# - tension_tavern_carousing.mid
# - rest_tavern_carousing.mid
# - death_tavern_carousing.mid
```

## Tips

1. **Looping**: These events are designed to loop seamlessly. Set your MIDI player to loop mode for continuous playback.

2. **Mixing Themes**: Try unexpected combinations!
   - Stealth event + Victory theme = Sneaky triumph
   - Fight event + Rest theme = Lazy sparring
   - Victory event + Stealth theme = Quiet satisfaction

3. **Layering**: Generate the same event with multiple themes and layer them for richness.

4. **Customization**: Edit the YAML themes to fine-tune the exact sound you want. All parameters are documented in `theme_schema.yaml`.

5. **Short Durations**: Event soundscapes are intentionally short (0.5-4 minutes) for looping. For longer pieces, use the main `yourdio.py` generator.
