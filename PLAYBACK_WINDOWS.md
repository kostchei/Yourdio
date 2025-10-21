# Playing Yourdio Music on Windows with Python

## Overview

There are several ways to play Yourdio-generated music on Windows using Python, depending on whether you want to play MIDI files directly or rendered audio files.

---

## Option 1: Play Rendered Audio Files (Simplest)

### Using pygame (Recommended for beginners)

```python
# playback_audio.py
"""
Simple audio player for rendered WAV files
Works with GM/OPL3/chip-tune rendered output
"""

import pygame
from pathlib import Path
import time
import sys

class AudioPlayer:
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)

    def play_chapter(self, wav_path: Path):
        """Play a single WAV file"""
        print(f"Loading: {wav_path.name}")
        pygame.mixer.music.load(str(wav_path))

        print(f"Playing: {wav_path.name}")
        pygame.mixer.music.play()

        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            time.sleep(1)

    def play_album(self, audio_dir: Path, loop: bool = False):
        """Play all chapters in sequence"""
        wav_files = sorted(audio_dir.glob('chapter_*.wav'))

        if not wav_files:
            print(f"No audio files found in {audio_dir}")
            return

        print(f"Found {len(wav_files)} chapters")
        print("Press Ctrl+C to stop\n")

        try:
            while True:
                for wav_file in wav_files:
                    self.play_chapter(wav_file)

                if not loop:
                    break

                print("\n--- Looping album ---\n")

        except KeyboardInterrupt:
            print("\n\nStopped playback")
            pygame.mixer.music.stop()

    def play_with_controls(self, audio_dir: Path):
        """Play with pause/resume controls"""
        wav_files = sorted(audio_dir.glob('chapter_*.wav'))

        if not wav_files:
            print(f"No audio files found in {audio_dir}")
            return

        current_index = 0
        paused = False

        print("Controls:")
        print("  SPACE - Pause/Resume")
        print("  N - Next chapter")
        print("  P - Previous chapter")
        print("  Q - Quit")
        print()

        # Load first chapter
        pygame.mixer.music.load(str(wav_files[current_index]))
        pygame.mixer.music.play()
        print(f"Playing: {wav_files[current_index].name}")

        try:
            while True:
                # Check if current track finished
                if not pygame.mixer.music.get_busy() and not paused:
                    # Auto-advance to next chapter
                    current_index = (current_index + 1) % len(wav_files)
                    pygame.mixer.music.load(str(wav_files[current_index]))
                    pygame.mixer.music.play()
                    print(f"Playing: {wav_files[current_index].name}")

                # Simple keyboard input (Note: this blocks, see advanced example below)
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\n\nStopped playback")
            pygame.mixer.music.stop()


# Usage
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python playback_audio.py <audio_directory>")
        print("\nExample:")
        print("  python playback_audio.py yourdio_output/audio_gm")
        sys.exit(1)

    audio_dir = Path(sys.argv[1])
    player = AudioPlayer()

    # Play all chapters once
    player.play_album(audio_dir, loop=False)

    # Or loop forever:
    # player.play_album(audio_dir, loop=True)
```

**Install pygame:**
```bash
pip install pygame
```

**Run:**
```bash
python playback_audio.py yourdio_output/audio_gm
```

---

## Option 2: Play MIDI Files Directly (Real-time synthesis)

### Using pygame.midi + Windows MIDI Synthesizer

```python
# playback_midi.py
"""
Play MIDI files using Windows built-in MIDI synthesizer
No audio rendering required - plays immediately
"""

import pygame.midi
import mido
from pathlib import Path
import time
import sys

class MIDIPlayer:
    def __init__(self):
        pygame.midi.init()

        # List available MIDI output devices
        print("Available MIDI devices:")
        for i in range(pygame.midi.get_count()):
            info = pygame.midi.get_device_info(i)
            if info[3]:  # Is output device
                print(f"  [{i}] {info[1].decode()}")

        # Use default output device (usually Microsoft GS Wavetable Synth)
        default_output = pygame.midi.get_default_output_id()
        print(f"\nUsing device: {pygame.midi.get_device_info(default_output)[1].decode()}")

        self.midi_out = pygame.midi.Output(default_output)
        self.midi_out.set_instrument(0)  # Piano by default

    def play_midi_file(self, midi_path: Path):
        """Play a MIDI file in real-time"""
        print(f"Playing: {midi_path.name}")

        midi_file = mido.MidiFile(midi_path)

        try:
            for message in midi_file.play():
                if message.type == 'note_on':
                    self.midi_out.note_on(message.note, message.velocity, message.channel)
                elif message.type == 'note_off':
                    self.midi_out.note_off(message.note, message.velocity, message.channel)
                elif message.type == 'program_change':
                    self.midi_out.set_instrument(message.program, message.channel)
                elif message.type == 'control_change':
                    self.midi_out.write_short(0xB0 | message.channel, message.control, message.value)
                elif message.type == 'pitchwheel':
                    # Convert pitch wheel value to MIDI format
                    value = message.pitch + 8192
                    lsb = value & 0x7F
                    msb = (value >> 7) & 0x7F
                    self.midi_out.write_short(0xE0 | message.channel, lsb, msb)

        except KeyboardInterrupt:
            print("\nStopped playback")
        finally:
            # Send all notes off
            for channel in range(16):
                self.midi_out.write_short(0xB0 | channel, 123, 0)  # All notes off

    def play_album(self, midi_dir: Path, loop: bool = False):
        """Play all MIDI chapters in sequence"""
        midi_files = sorted(midi_dir.glob('chapter_*.mid'))

        if not midi_files:
            print(f"No MIDI files found in {midi_dir}")
            return

        print(f"Found {len(midi_files)} chapters")
        print("Press Ctrl+C to stop\n")

        try:
            while True:
                for midi_file in midi_files:
                    self.play_midi_file(midi_file)

                if not loop:
                    break

                print("\n--- Looping album ---\n")

        except KeyboardInterrupt:
            print("\n\nStopped playback")

    def cleanup(self):
        """Clean up MIDI resources"""
        del self.midi_out
        pygame.midi.quit()


# Usage
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python playback_midi.py <midi_directory>")
        print("\nExample:")
        print("  python playback_midi.py yourdio_output/midi")
        sys.exit(1)

    midi_dir = Path(sys.argv[1])
    player = MIDIPlayer()

    try:
        player.play_album(midi_dir, loop=False)
    finally:
        player.cleanup()
```

**Install dependencies:**
```bash
pip install pygame mido
```

**Run:**
```bash
python playback_midi.py yourdio_output/midi
```

---

## Option 3: Advanced Player with GUI (Best User Experience)

```python
# playback_gui.py
"""
GUI player for Yourdio with play/pause/skip controls
Works with both MIDI and WAV files
"""

import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
import pygame
import threading

class YourdioPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Yourdio Player")
        self.root.geometry("600x400")

        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)

        self.playlist = []
        self.current_index = 0
        self.is_playing = False
        self.is_paused = False

        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Current track label
        self.track_label = ttk.Label(main_frame, text="No track loaded",
                                     font=("Arial", 12, "bold"))
        self.track_label.grid(row=0, column=0, columnspan=4, pady=10)

        # Progress label
        self.progress_label = ttk.Label(main_frame, text="--:-- / --:--")
        self.progress_label.grid(row=1, column=0, columnspan=4, pady=5)

        # Playlist
        playlist_frame = ttk.LabelFrame(main_frame, text="Playlist", padding="5")
        playlist_frame.grid(row=2, column=0, columnspan=4, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.playlist_box = tk.Listbox(playlist_frame, height=10)
        self.playlist_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(playlist_frame, orient=tk.VERTICAL, command=self.playlist_box.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.playlist_box.config(yscrollcommand=scrollbar.set)

        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)

        ttk.Button(button_frame, text="Load Folder", command=self.load_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="⏮ Previous", command=self.previous_track).pack(side=tk.LEFT, padx=5)
        self.play_pause_btn = ttk.Button(button_frame, text="▶ Play", command=self.toggle_play_pause)
        self.play_pause_btn.pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="⏹ Stop", command=self.stop).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Next ⏭", command=self.next_track).pack(side=tk.LEFT, padx=5)

        # Volume control
        volume_frame = ttk.Frame(main_frame)
        volume_frame.grid(row=4, column=0, columnspan=4, pady=5)

        ttk.Label(volume_frame, text="Volume:").pack(side=tk.LEFT, padx=5)
        self.volume_slider = ttk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                       command=self.change_volume, length=200)
        self.volume_slider.set(70)
        self.volume_slider.pack(side=tk.LEFT, padx=5)

        # Loop checkbox
        self.loop_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(main_frame, text="Loop Playlist", variable=self.loop_var).grid(row=5, column=0, columnspan=4)

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

    def load_folder(self):
        """Load all audio files from a folder"""
        folder = filedialog.askdirectory(title="Select Yourdio Output Folder")
        if not folder:
            return

        folder_path = Path(folder)

        # Look for WAV files
        audio_files = sorted(folder_path.glob('*.wav'))

        if not audio_files:
            # Try subdirectories
            audio_files = sorted(folder_path.glob('audio_*/*.wav'))

        if not audio_files:
            tk.messagebox.showwarning("No Files", "No WAV files found in selected folder")
            return

        self.playlist = audio_files
        self.playlist_box.delete(0, tk.END)

        for audio_file in audio_files:
            self.playlist_box.insert(tk.END, audio_file.name)

        self.current_index = 0
        self.track_label.config(text=f"Loaded {len(audio_files)} tracks")

    def toggle_play_pause(self):
        """Play or pause current track"""
        if not self.playlist:
            tk.messagebox.showwarning("No Playlist", "Please load a folder first")
            return

        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.play_pause_btn.config(text="⏸ Pause")
        elif self.is_playing:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.play_pause_btn.config(text="▶ Play")
        else:
            self.play_track(self.current_index)

    def play_track(self, index):
        """Play track at given index"""
        if not self.playlist or index >= len(self.playlist):
            return

        self.current_index = index
        track = self.playlist[index]

        pygame.mixer.music.load(str(track))
        pygame.mixer.music.play()

        self.is_playing = True
        self.is_paused = False
        self.play_pause_btn.config(text="⏸ Pause")

        self.track_label.config(text=f"Playing: {track.name}")
        self.playlist_box.selection_clear(0, tk.END)
        self.playlist_box.selection_set(index)
        self.playlist_box.see(index)

        # Start monitoring thread
        threading.Thread(target=self.monitor_playback, daemon=True).start()

    def monitor_playback(self):
        """Monitor playback and auto-advance to next track"""
        while self.is_playing and pygame.mixer.music.get_busy():
            pygame.time.wait(100)

        if self.is_playing and not self.is_paused:
            # Track finished, play next
            self.root.after(100, self.next_track)

    def next_track(self):
        """Play next track"""
        if not self.playlist:
            return

        self.current_index += 1

        if self.current_index >= len(self.playlist):
            if self.loop_var.get():
                self.current_index = 0
            else:
                self.stop()
                return

        self.play_track(self.current_index)

    def previous_track(self):
        """Play previous track"""
        if not self.playlist:
            return

        self.current_index = max(0, self.current_index - 1)
        self.play_track(self.current_index)

    def stop(self):
        """Stop playback"""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.play_pause_btn.config(text="▶ Play")
        self.track_label.config(text="Stopped")

    def change_volume(self, value):
        """Change playback volume"""
        volume = float(value) / 100
        pygame.mixer.music.set_volume(volume)


# Main
if __name__ == '__main__':
    root = tk.Tk()
    app = YourdioPlayer(root)
    root.mainloop()
```

**Run:**
```bash
python playback_gui.py
```

Then click "Load Folder" and select your `yourdio_output/audio_gm` directory.

---

## Option 4: Stream Infinite Mode (Real-Time Generation + Playback)

```python
# playback_streaming.py
"""
Generate and play Yourdio music in real-time
Never stops - infinite ambient music!
"""

from pathlib import Path
import pygame
import tempfile
import subprocess
from theme_loader import ThemeLoader
from macrocompositor.midi_generator import RetroMIDIComposer, calculate_chapter_intensity

class StreamingPlayer:
    def __init__(self, theme_path: Path = None):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)

        # Load theme
        self.theme = ThemeLoader.load(theme_path)
        print(f"Theme: {self.theme['name']}")

        # Create temp directory for streaming
        self.temp_dir = Path(tempfile.mkdtemp(prefix='yourdio_stream_'))
        print(f"Streaming to: {self.temp_dir}")

        self.primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37,
                      41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

    def generate_chapter(self, chapter_num: int) -> Path:
        """Generate a single chapter on-the-fly"""
        print(f"Generating chapter {chapter_num}...")

        # Calculate intensity
        arc_config = self.theme.get('structural_arc', {})
        intensity = calculate_chapter_intensity(chapter_num % 12, arc_config=arc_config)

        # Adjust theme for intensity
        current_theme = self.theme.copy()
        param_evolution = self.theme.get('parameter_evolution', {})

        if param_evolution.get('tempo', True):
            tempo_config = self.theme['tempo']
            tempo_min, tempo_max = tempo_config['variation_range']
            current_tempo = int(tempo_min + intensity * (tempo_max - tempo_min))
            current_theme['tempo'] = {**tempo_config, 'base': current_tempo}

        # Create composer
        composer = RetroMIDIComposer(current_theme)

        # Generate MIDI (short chapters for streaming)
        chapter_primes = self.primes[chapter_num % len(self.primes):(chapter_num % len(self.primes))+8]
        chaos_seed = (self.primes[chapter_num % len(self.primes)] % 97) / 97.0

        midi = composer.create_chapter_midi(
            chapter_id=chapter_num,
            duration_minutes=5,  # Short chapters for responsive streaming
            prime_sequence=chapter_primes,
            chaos_seed=chaos_seed
        )

        # Save MIDI
        midi_path = self.temp_dir / f'chapter_{chapter_num % 3}.mid'  # Rotate 3 files
        composer.save_chapter(midi, str(midi_path))

        # Render to WAV using FluidSynth
        wav_path = midi_path.with_suffix('.wav')
        subprocess.run([
            'fluidsynth',
            '-ni', '-g', '0.8', '-R', '0', '-C', '0',
            '-r', '44100',
            '-F', str(wav_path),
            'path/to/soundfont.sf2',  # Update this path!
            str(midi_path)
        ], capture_output=True)

        print(f"  Generated: {wav_path.name}")
        return wav_path

    def stream_infinite(self):
        """Generate and play chapters infinitely"""
        print("Starting infinite streaming...")
        print("Press Ctrl+C to stop\n")

        chapter_num = 0

        try:
            while True:
                # Generate next chapter
                wav_path = self.generate_chapter(chapter_num)

                # Play it
                print(f"Playing chapter {chapter_num}...")
                pygame.mixer.music.load(str(wav_path))
                pygame.mixer.music.play()

                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)

                chapter_num += 1

        except KeyboardInterrupt:
            print("\n\nStopping stream...")
            pygame.mixer.music.stop()
        finally:
            # Cleanup temp files
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)


# Usage
if __name__ == '__main__':
    import sys

    theme_path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    player = StreamingPlayer(theme_path)
    player.stream_infinite()
```

**Run:**
```bash
python playback_streaming.py themes/ambient_myst.yaml
```

---

## Quick Reference

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **pygame (WAV)** | Simple, reliable | Requires pre-rendered audio | Most users |
| **pygame.midi** | Instant playback, no rendering | Windows MIDI synth quality | Quick testing |
| **GUI Player** | Best UX, visual controls | More complex code | End users |
| **Streaming** | Infinite music, low storage | Requires FluidSynth | Installations |

---

## Installation Summary

```bash
# For WAV playback (Option 1, 3)
pip install pygame

# For MIDI playback (Option 2)
pip install pygame mido

# For streaming (Option 4)
pip install pygame pyyaml
# Also install FluidSynth: https://github.com/FluidSynth/fluidsynth/releases
```

---

## Troubleshooting

### "No module named 'pygame'"
```bash
pip install pygame
```

### "No audio devices found"
Make sure Windows audio is not muted and speakers/headphones are connected.

### MIDI sounds bad
Windows GS Wavetable Synth is basic. For better quality:
1. Use Option 1 (pre-rendered WAV with FluidSynth)
2. Or install a better soundfont and use virtual MIDI devices

### GUI not showing
Make sure tkinter is installed (comes with Python on Windows by default).

---

## Recommended: Simple Playback Script

For most users, this is the easiest:

```python
# play.py
import pygame
from pathlib import Path
import sys

pygame.mixer.init()

if len(sys.argv) < 2:
    print("Usage: python play.py <audio_directory>")
    sys.exit(1)

audio_dir = Path(sys.argv[1])
wav_files = sorted(audio_dir.glob('chapter_*.wav'))

if not wav_files:
    wav_files = sorted(audio_dir.glob('audio_*/*.wav'))

print(f"Playing {len(wav_files)} chapters...")
print("Press Ctrl+C to stop\n")

try:
    for wav in wav_files:
        print(f"Playing: {wav.name}")
        pygame.mixer.music.load(str(wav))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
except KeyboardInterrupt:
    print("\nStopped")
```

**Run:**
```bash
python play.py yourdio_output/audio_gm
```

Done! 🎵
