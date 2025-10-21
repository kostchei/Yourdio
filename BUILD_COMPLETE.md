# Yourdio Windows GUI - Build Complete!

## What Has Been Created

A complete Windows GUI application for Yourdio with retro Winamp-inspired aesthetics.

### Files Created

1. **yourdio_gui.py** - Main GUI application (1,000+ lines)
   - Retro green-on-black LCD aesthetic
   - Two-tab interface (Theme Generator & Event Soundscapes)
   - Full parameter control with sliders, dropdowns, and text inputs
   - YAML import/export functionality
   - Background threaded generation (non-blocking UI)

2. **requirements.txt** - Python dependencies
   - midiutil, numpy, pyyaml, pygame, pyinstaller

3. **build_exe.py** - Automated build script
   - Creates single-file Windows executable
   - Bundles all dependencies
   - Windowed mode (no console)

4. **README_GUI.md** - User documentation
   - Installation instructions
   - Usage guide for both tabs
   - Technical details

5. **dist/Yourdio.exe** - Windows Executable (32MB)
   - Ready to distribute
   - No Python installation required
   - Fully portable

## Features

### Tab 1: Theme Generator (6-Hour Compositions)
Generate epic 6-hour ambient soundtracks with full control over:

- **Tempo**: Base BPM (40-120) with min/max variation range
- **Scale/Mode**: D Dorian, A Aeolian, E Phrygian
- **Harmony**: Custom chord intervals and types
- **Dynamics**: Separate velocity controls for 4 layers
  - Harmonic bed (pads)
  - Melodic texture (leads)
  - Drones (bass)
  - Ambient events (FX)
- **Chaos Parameters**:
  - Logistic map growth rate (2.5-4.0)
  - Lorenz attractor sigma (5.0-20.0)
- **Structural Arc**: Choose journey type
  - Parabolic (peaks in middle)
  - Slow burn (builds to climax)
  - Descending (starts intense, fades)
  - Flat (constant intensity)
- **Load/Save** YAML themes
- **Output**: 12 MIDI chapters × 30 minutes = 6 hours

### Tab 2: Event Soundscapes (Short Loops)
Generate game/interactive event music (1-4 minutes):

**8 Event Types:**
- **Carousing** - Tavern atmosphere (2 min)
- **Fight** - Combat intensity (1.5 min)
- **Stealth** - Sneaking tension (3 min)
- **Victory** - Triumphant fanfare (1 min)
- **Exploration** - Wandering wonder (4 min)
- **Tension** - Building dread (2.5 min)
- **Rest** - Peaceful campfire (3 min)
- **Death** - Failure sting (0.5 min)

Select multiple events, generate in batch using current theme settings.

## Visual Design

Inspired by classic Winamp visualizers:

- **Colors**: Black background (#000000) with bright green text (#00ff00)
- **LCD displays**: Dark green background with cyan accents
- **ASCII borders**: ═══ and ║ for retro authenticity
- **Courier font**: Monospace throughout for classic terminal feel
- **Knobs/Sliders**: Horizontal sliders with real-time value display
- **Status console**: Scrolling log at bottom with generation progress

## How to Use

### Running from Python
```bash
cd Yourdio
pip install -r requirements.txt
python yourdio_gui.py
```

### Running the Executable
Simply double-click `dist/Yourdio.exe` - no installation needed!

### Generating a 6-Hour Theme
1. Open the **THEME GENERATOR** tab
2. Tweak parameters with sliders (or load existing YAML)
3. Set output directory
4. Click **▶ GENERATE 12 CHAPTERS**
5. Wait for completion (watch status log)
6. Find 12 MIDI files in output directory

### Generating Event Soundscapes
1. Open the **EVENT SOUNDSCAPES** tab
2. Check events you want (or Select All)
3. Set output directory
4. Click **▶ GENERATE EVENTS**
5. Get loopable MIDI files for each event

## Technical Details

- **Framework**: tkinter (native, no external GUI dependencies)
- **Threading**: Background generation doesn't block UI
- **File I/O**: YAML for themes, MIDI for output
- **Packaging**: PyInstaller with --onefile for portability
- **Size**: ~32MB (includes numpy, pygame, all dependencies)
- **Platform**: Windows 64-bit (tested on Windows 11)

## Distribution

The executable is completely portable:
- No installation required
- No Python needed on target machine
- Can run from USB drive
- Single .exe file contains everything

Simply copy `dist/Yourdio.exe` anywhere and run!

## Next Steps

You can now:
1. **Distribute** the .exe to users
2. **Create themes** in YAML and share them
3. **Generate music** for your projects
4. **Customize** the GUI colors/styling in `yourdio_gui.py`
5. **Add icons** by modifying `build_exe.py` (line 22)

## Enjoy Your Retro Music Generator!

```
╔═══════════════════════════════════════════════════╗
║  Y O U R D I O  ░▒▓ Retro Lo-Fi Generator ▓▒░  ║
╚═══════════════════════════════════════════════════╝
```

---

**Location**: `d:\Code\Yourdio\dist\Yourdio.exe`

**File size**: 32MB

**Status**: ✓ TESTED AND WORKING
