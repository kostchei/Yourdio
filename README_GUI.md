# Yourdio GUI - Retro Lo-Fi Music Generator

A classic Winamp-inspired GUI for generating algorithmic ambient music compositions.

## Features

### Theme Generator Tab
- Generate 6-hour ambient compositions (12 chapters × 30 minutes)
- Adjust musical parameters with sliders and knobs:
  - **Tempo**: Base BPM and variation range
  - **Scale/Mode**: D Dorian, A Aeolian, E Phrygian
  - **Harmony**: Chord construction rules
  - **Dynamics**: Velocity settings for each layer
  - **Chaos Parameters**: Logistic and Lorenz attractor settings
  - **Structural Arc**: Control the dramatic journey (parabolic, slow burn, etc.)
- Load/Save themes as YAML files
- Real-time parameter editing

### Event Soundscapes Tab
- Generate short, loopable event music (1-4 minutes each)
- 8 event types:
  - **Carousing**: Lively tavern atmosphere (2 min)
  - **Fight**: Intense combat music (1.5 min)
  - **Stealth**: Tense sneaking atmosphere (3 min)
  - **Victory**: Triumphant fanfare (1 min)
  - **Exploration**: Atmospheric wandering (4 min)
  - **Tension**: Building dread (2.5 min)
  - **Rest**: Peaceful campfire (3 min)
  - **Death**: Failure sting (0.5 min)
- Select multiple events to generate
- Uses current theme settings

## Installation

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the GUI
```bash
python yourdio_gui.py
```

### Build Windows Executable
```bash
python build_exe.py
```

The executable will be created in the `dist/` folder as `Yourdio.exe`.

## Usage

### Creating a 6-Hour Theme

1. Switch to the **THEME GENERATOR** tab
2. Adjust parameters using sliders and input fields
3. Click **Load YAML** to use an existing theme (optional)
4. Click **Save YAML** to save your current settings
5. Choose an output directory
6. Click **▶ GENERATE 12 CHAPTERS** to create the composition
7. Wait for generation to complete (status shown in footer)

### Generating Event Soundscapes

1. Switch to the **EVENT SOUNDSCAPES** tab
2. Check the events you want to generate
3. Use **Select All** or **Select None** for convenience
4. Load a different theme YAML if desired (or use current settings)
5. Choose an output directory
6. Click **▶ GENERATE EVENTS** to create selected soundscapes

## Theme Files

Themes are stored as YAML files. See `theme_schema.yaml` for the complete parameter reference.

Example themes can be found in the `themes/` directory.

## Output Format

All output is in MIDI format (.mid files), compatible with:
- General MIDI synthesizers
- DAWs (Ableton, FL Studio, Logic, etc.)
- Hardware synthesizers
- OPL3 renderers for authentic retro sound

## Retro Design

The UI is inspired by classic Winamp visualization plugins with:
- Dark color scheme (black/green LCD aesthetic)
- Monospace Courier font
- ASCII art borders
- Retro-styled controls and buttons
- Real-time status logging

## Technical Details

- Built with tkinter for lightweight, native Windows GUI
- Non-blocking generation (runs in background threads)
- Scrollable parameter panels for compact display
- Automatic theme validation
- Progress feedback in status console

## License

MIT License - Feel free to use and modify!

## Credits

Yourdio - Algorithmic composition engine using prime numbers and chaos theory
GUI - Classic retro design inspired by Winamp visualizers
