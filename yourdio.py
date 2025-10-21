#!/usr/bin/env python3
"""
Yourdio: Retro Lo-Fi Algorithmic Composer
Generate 6-hour ambient music compositions using prime numbers and chaos theory
"""

import midiutil
from midiutil import MIDIFile
import numpy as np
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import sys

# Import theme loader
from theme_loader import ThemeLoader


class RetroMIDIComposer:
    """
    Generate MIDI files directly from symbolic composition
    Targets General MIDI or OPL3-style synthesis
    Consumes YAML theme configurations for style control
    """

    def __init__(self, theme_config: Dict, max_polyphony: Optional[int] = None):
        self.theme = theme_config

        # Extract tempo parameters
        tempo_config = theme_config.get('tempo', {})
        if isinstance(tempo_config, dict):
            self.tempo = tempo_config.get('base', 58)
            self.tempo_range = tempo_config.get('variation_range', [52, 68])
        else:
            # Legacy support: single tempo value
            self.tempo = tempo_config or 58
            self.tempo_range = [self.tempo - 6, self.tempo + 6]

        # Extract harmony parameters
        harmony = theme_config.get('harmony_rules', {
            'type': 'quartal',
            'intervals': [0, 3, 6]
        })
        self.harmony_type = harmony.get('type', 'quartal')
        self.harmony_intervals = harmony.get('intervals', [0, 3, 6])
        self.harmony_variation = harmony.get('variation')
        self.harmony_variation_intervals = harmony.get('variation_intervals', [0, 2, 4])
        self.harmony_variation_mod = harmony.get('variation_chance_mod', 3)

        # Extract modal center and scale
        self.modal_center = theme_config.get('modal_center', 'D_dorian')
        custom_scale = theme_config.get('custom_scale')
        self.scale = self._build_scale(self.modal_center, custom_scale)

        # Extract rhythmic language
        rhythmic = theme_config.get('rhythmic_language', {})
        self.rhythm_harmonic = rhythmic.get('harmonic_bed', {})
        self.rhythm_melodic = rhythmic.get('melodic_texture', {})
        self.rhythm_drones = rhythmic.get('drones', {})
        self.rhythm_events = rhythmic.get('ambient_events', {})

        # Extract dynamics
        dynamics = theme_config.get('dynamics', {})
        self.dynamics_harmonic = dynamics.get('harmonic_bed', {'base_velocity': 45, 'prime_mod_range': 20})
        self.dynamics_melodic = dynamics.get('melodic_texture', {'base_velocity': 55, 'prime_mod_range': 25})
        self.dynamics_drones = dynamics.get('drones', {'velocity': 50})
        self.dynamics_events = dynamics.get('ambient_events', {'base_velocity': 60, 'intensity_scaling': 30})

        # Extract motif parameters
        motif = theme_config.get('motif', {})
        self.motif_pattern = motif.get('core_pattern', [0, 2, 5, 7])
        self.motif_interval = motif.get('interval_minutes', 17)
        self.motif_register_mod = motif.get('register_shift_prime_mod', 2)
        self.motif_ornament_mod = motif.get('ornament_density_mod', 5)

        # Extract chaos parameters
        chaos = theme_config.get('chaos', {})
        self.logistic_r = chaos.get('logistic_r', 3.86)
        self.lorenz_sigma = chaos.get('lorenz_sigma', 10.0)
        self.lorenz_rho = chaos.get('lorenz_rho', 28.0)
        self.lorenz_beta = chaos.get('lorenz_beta', 8.0/3.0)

        # Polyphony (can be overridden per chapter for intensity)
        if max_polyphony is not None:
            self.max_polyphony = max_polyphony
        else:
            self.max_polyphony = 32  # Default

        self.active_notes = []  # Track (end_time, pitch, channel)

    def _build_scale(self, mode: str, custom_scale: Optional[List[int]] = None) -> List[int]:
        """Build MIDI note numbers for modal scale"""
        # Use custom scale if provided
        if custom_scale is not None:
            return custom_scale

        scales = {
            'D_dorian': [62, 64, 65, 67, 69, 71, 72, 74],  # D E F G A B C D
            'A_aeolian': [69, 71, 72, 74, 76, 77, 79, 81], # A B C D E F G A
            'E_phrygian': [64, 65, 67, 69, 71, 72, 74, 76] # E F G A B C D E
        }
        return scales.get(mode, scales['D_dorian'])

    def _fibonacci_sequence(self, n: int) -> List[int]:
        """Generate Fibonacci sequence for rhythm patterns"""
        if n <= 0:
            return []
        elif n == 1:
            return [1]
        seq = [1, 1]
        for i in range(2, n):
            seq.append(seq[-1] + seq[-2])
        return seq

    def _lorenz_step(self, x: float, y: float, z: float, dt: float = 0.01) -> Tuple[float, float, float]:
        """
        Single step of Lorenz attractor for smooth parameter modulation
        Uses parameters from theme configuration
        Returns new (x, y, z) coordinates
        """
        sigma = self.lorenz_sigma
        rho = self.lorenz_rho
        beta = self.lorenz_beta

        dx = sigma * (y - x) * dt
        dy = (x * (rho - z) - y) * dt
        dz = (x * y - beta * z) * dt
        return x + dx, y + dy, z + dz

    def _enforce_polyphony_limit(self, midi: MIDIFile, track: int,
                                  time: float, pitch: int,
                                  duration: float, velocity: int) -> bool:
        """
        Add note only if under polyphony limit (authentic hardware constraint)
        Returns True if note was added, False if dropped
        """
        # Remove notes that have ended
        self.active_notes = [(end_t, p, c) for end_t, p, c in self.active_notes
                            if end_t > time]

        if len(self.active_notes) < self.max_polyphony:
            midi.addNote(track, track, pitch, time, duration, velocity)
            self.active_notes.append((time + duration, pitch, track))
            return True
        else:
            # Voice stealing: remove oldest note
            if self.active_notes:
                self.active_notes.pop(0)
                midi.addNote(track, track, pitch, time, duration, velocity)
                self.active_notes.append((time + duration, pitch, track))
                return True
            return False

    def create_chapter_midi(
        self,
        chapter_id: int,
        duration_minutes: float,
        prime_sequence: List[int],
        chaos_seed: float
    ) -> MIDIFile:
        """
        Generate one chapter as MIDI file

        Args:
            chapter_id: Chapter number (0-11)
            duration_minutes: Length in minutes (typically 30)
            prime_sequence: List of primes for parameter modulation
            chaos_seed: Float [0,1] for logistic map seeding
        """
        # Create MIDI file: 1 file, 4 tracks, 480 ticks per quarter note
        midi = MIDIFile(numTracks=4, ticks_per_quarternote=480)

        # Track 0: Harmonic bed (pad)
        # Track 1: Melodic texture (lead)
        # Track 2: Drones (bass)
        # Track 3: Ambient elements (percussion/FX)

        for track in range(4):
            midi.addTempo(track, 0, self.tempo)
            midi.addProgramChange(track, track, 0, self._get_gm_patch(track))

        # Generate content with prime-modulated parameters
        self._generate_harmonic_bed(midi, 0, duration_minutes, prime_sequence)
        self._generate_melodic_texture(midi, 1, duration_minutes, prime_sequence)
        self._generate_drones(midi, 2, duration_minutes, prime_sequence)
        self._generate_ambient_events(midi, 3, duration_minutes, chaos_seed)

        return midi

    def _get_gm_patch(self, track: int) -> int:
        """Map tracks to General MIDI patches from theme configuration"""
        ensemble = self.theme.get('ensemble_gm', {})

        track_names = ['harmonic_bed', 'melodic_texture', 'drones', 'ambient_events']

        if track < len(track_names):
            track_name = track_names[track]
            return ensemble.get(track_name, 89)

        return 89  # Default fallback

    def _generate_harmonic_bed(
        self,
        midi: MIDIFile,
        track: int,
        duration: float,
        primes: List[int]
    ):
        """
        Generate slow-moving harmonic pads
        Uses theme's rhythmic_language and dynamics parameters
        """
        beats_per_minute = self.tempo
        beats_total = int(duration * beats_per_minute)

        # Get rhythm parameters from theme
        base_duration = self.rhythm_harmonic.get('base_duration', 32)
        prime_mod_factor = self.rhythm_harmonic.get('prime_mod_factor', 8)

        # Get dynamics parameters from theme
        base_velocity = self.dynamics_harmonic.get('base_velocity', 45)
        prime_mod_range = self.dynamics_harmonic.get('prime_mod_range', 20)

        current_beat = 0
        prime_idx = 0

        while current_beat < beats_total:
            # Use prime to determine chord duration variation
            prime = primes[prime_idx % len(primes)]
            chord_length = base_duration + (prime % prime_mod_factor)

            # Select chord voicing from scale
            root_idx = (prime_idx * 2) % len(self.scale)
            chord_notes = self._build_chord(root_idx, primes[prime_idx % len(primes)])

            # Calculate velocity from theme parameters
            velocity = base_velocity + (prime % prime_mod_range)

            for note in chord_notes:
                midi.addNote(
                    track=track,
                    channel=track,
                    pitch=note,
                    time=current_beat,
                    duration=chord_length * 0.95,  # Slight overlap
                    volume=velocity
                )

            current_beat += chord_length
            prime_idx += 1

    def _build_chord(self, root_idx: int, prime: int) -> List[int]:
        """Build chord from scale using theme's harmony_rules"""
        # Use variation if defined and prime matches condition
        if self.harmony_variation and prime % self.harmony_variation_mod == 0:
            intervals = self.harmony_variation_intervals
        else:
            intervals = self.harmony_intervals

        notes = []
        for interval in intervals:
            note_idx = (root_idx + interval) % len(self.scale)
            octave_shift = -12 if prime % 2 == 0 else 0
            notes.append(self.scale[note_idx] + octave_shift)

        return notes

    def _generate_melodic_texture(
        self,
        midi: MIDIFile,
        track: int,
        duration: float,
        primes: List[int]
    ):
        """
        Generate sparse melodic fragments
        Uses theme's motif and rhythmic_language parameters
        """
        beats_per_minute = self.tempo
        beats_total = int(duration * beats_per_minute)

        # Get parameters from theme
        motif_interval_beats = int(self.motif_interval * beats_per_minute)
        core_motif = self.motif_pattern
        base_velocity = self.dynamics_melodic.get('base_velocity', 55)
        prime_mod_range = self.dynamics_melodic.get('prime_mod_range', 25)

        # Get Fibonacci settings from rhythmic_language
        fib_length = self.rhythm_melodic.get('sequence_length', 8)
        fib_base_unit = self.rhythm_melodic.get('base_unit', 0.25)

        current_beat = 0
        motif_count = 0

        while current_beat < beats_total:
            prime = primes[motif_count % len(primes)]

            # Prime modulates register and ornament density (from theme)
            register_shift = 12 if prime % self.motif_register_mod == 0 else 0
            ornament_density = (prime % self.motif_ornament_mod) / float(self.motif_ornament_mod)

            # Use Fibonacci sequence for note durations
            fib_durations = self._fibonacci_sequence(fib_length)

            for i, degree in enumerate(core_motif):
                note_idx = degree % len(self.scale)
                pitch = self.scale[note_idx] + register_shift

                # Timing with slight prime-driven jitter
                note_time = current_beat + (i * 2) + ((prime % 3) * 0.1)

                # Fibonacci-based duration (scaled by base_unit from theme)
                duration_beats = (fib_durations[i % len(fib_durations)] * fib_base_unit) + 1.0
                velocity = base_velocity + (prime % prime_mod_range)

                self._enforce_polyphony_limit(midi, track, note_time, pitch,
                                             duration_beats, velocity)

                # Add ornament based on density
                if np.random.random() < ornament_density:
                    ornament_pitch = self.scale[(note_idx + 1) % len(self.scale)] + register_shift
                    ornament_duration = 0.5
                    self._enforce_polyphony_limit(midi, track, note_time + 0.5,
                                                 ornament_pitch, ornament_duration,
                                                 velocity - 10)

            current_beat += motif_interval_beats
            motif_count += 1

    def _generate_drones(
        self,
        midi: MIDIFile,
        track: int,
        duration: float,
        primes: List[int]
    ):
        """
        Generate sustained bass drones
        Very slow evolution with Lorenz attractor for smooth filter modulation
        """
        beats_per_minute = self.tempo
        beats_total = int(duration * beats_per_minute)

        # Each drone lasts for prime-determined duration
        prime_idx = 0
        current_beat = 0

        # Initialize Lorenz attractor state
        x, y, z = 0.1, 0.0, 0.0

        # Get parameters from theme
        duration_multiplier = self.rhythm_drones.get('duration_multiplier', 4)
        cc_event_interval = self.rhythm_drones.get('cc_event_interval', 4)
        drone_velocity = self.dynamics_drones.get('velocity', 50)

        while current_beat < beats_total:
            prime = primes[prime_idx % len(primes)]

            # Drone duration in beats (from theme)
            drone_length = prime * duration_multiplier

            # Root note (low register)
            root_note = self.scale[0] - 24  # Two octaves down

            # Use Lorenz attractor for smooth filter sweep
            num_cc_events = int(drone_length / cc_event_interval)
            for i in range(num_cc_events):
                x, y, z = self._lorenz_step(x, y, z)
                # Map x coordinate to MIDI CC brightness (30-100 range)
                brightness = int(65 + 35 * np.clip(x / 20.0, -1, 1))
                cc_time = current_beat + (i * cc_event_interval)
                if cc_time < beats_total:
                    midi.addControllerEvent(track, track, cc_time, 74, brightness)

            # Add the drone note
            actual_duration = min(drone_length, beats_total - current_beat)
            self._enforce_polyphony_limit(midi, track, current_beat, root_note,
                                         actual_duration, drone_velocity)

            current_beat += drone_length
            prime_idx += 1

    def _generate_ambient_events(
        self,
        midi: MIDIFile,
        track: int,
        duration: float,
        chaos_seed: float
    ):
        """
        Generate rare events using logistic map
        Uses theme's rhythmic_language and dynamics parameters
        """
        beats_per_minute = self.tempo
        beats_total = int(duration * beats_per_minute)

        # Get parameters from theme
        threshold = self.rhythm_events.get('threshold', 0.87)
        event_count = self.rhythm_events.get('event_count', 64)

        # Generate chaos sequence
        events = self._logistic_map_events(chaos_seed, n=event_count, threshold=threshold)

        for event in events:
            # Map event time to beat position
            event_beat = event['timestamp'] * beats_total
            intensity = event['intensity']

            # Choose event type based on intensity
            if intensity > 0.9:
                self._add_thunder_roll(midi, track, event_beat, intensity)
            elif intensity > 0.7:
                self._add_metallic_swell(midi, track, event_beat, intensity)
            else:
                self._add_shimmer(midi, track, event_beat, intensity)

    def _logistic_map_events(
        self,
        seed: float,
        n: int = 64,
        threshold: float = 0.87
    ) -> List[Dict]:
        """Generate chaos-driven events using theme's logistic_r parameter"""
        r = self.logistic_r  # From theme configuration
        x = seed
        events = []
        for i in range(n):
            x = r * x * (1 - x)
            if x > threshold:
                events.append({
                    'iteration': i,
                    'intensity': (x - threshold) / (1 - threshold),
                    'timestamp': i / n
                })
        return events

    def _add_thunder_roll(self, midi: MIDIFile, track: int, beat: float, intensity: float):
        """Low rumble using pitch bend and rapid notes"""
        base_pitch = 36  # Low C
        velocity = int(60 + intensity * 30)

        # Rapid tremolo
        for i in range(8):
            midi.addNote(track, track, base_pitch, beat + i * 0.125, 0.25, velocity)

        # Pitch bend down for rumble effect
        midi.addPitchWheelEvent(track, track, beat, -4096)
        midi.addPitchWheelEvent(track, track, beat + 1, 0)

    def _add_metallic_swell(self, midi: MIDIFile, track: int, beat: float, intensity: float):
        """High shimmer with crescendo"""
        base_pitch = 84  # High C
        num_notes = 12

        for i in range(num_notes):
            velocity = int(30 + (i / num_notes) * intensity * 60)
            pitch = base_pitch + (i % 5)
            midi.addNote(track, track, pitch, beat + i * 0.5, 2.0, velocity)

    def _add_shimmer(self, midi: MIDIFile, track: int, beat: float, intensity: float):
        """Subtle high texture"""
        base_pitch = 72
        velocity = int(35 + intensity * 20)

        for i in range(4):
            pitch = base_pitch + i * 2
            midi.addNote(track, track, pitch, beat + i * 0.25, 1.5, velocity)

    def save_chapter(self, midi: MIDIFile, output_path: str):
        """Write MIDI file to disk"""
        with open(output_path, 'wb') as f:
            midi.writeFile(f)


def calculate_chapter_intensity(chapter: int, total_chapters: int = 12, arc_config: Dict = None) -> float:
    """
    Calculate intensity for chapter to create dramatic arc
    Uses theme's structural_arc configuration

    Args:
        chapter: Chapter number (0-11)
        total_chapters: Total number of chapters
        arc_config: Theme's structural_arc configuration

    Returns:
        Intensity value (typically 0.0-1.0)
    """
    if arc_config is None:
        arc_config = {'type': 'parabolic', 'min_intensity': 0.2, 'max_intensity': 0.8}

    arc_type = arc_config.get('type', 'parabolic')
    min_val = arc_config.get('min_intensity', 0.2)
    max_val = arc_config.get('max_intensity', 0.8)
    climax_chapter = arc_config.get('climax_chapter', total_chapters // 2)

    normalized = chapter / (total_chapters - 1)

    if arc_type == 'parabolic':
        # Peak at climax_chapter
        climax_normalized = climax_chapter / (total_chapters - 1)
        arc = 1 - abs(normalized - climax_normalized) * 2
    elif arc_type == 'slow_burn':
        # Linear ascending
        arc = normalized
    elif arc_type == 'descending':
        # Linear descending
        arc = 1 - normalized
    elif arc_type == 'flat':
        # Constant intensity
        arc = 0.5
    else:
        # Default to parabolic
        arc = 1 - abs(normalized - 0.5) * 2

    # Scale to intensity range
    intensity = min_val + (max_val - min_val) * np.clip(arc, 0, 1)
    return intensity


def generate_full_composition(theme_path: Optional[str] = None, output_dir: Path = None):
    """
    Generate all 12 chapters with intensity curve

    Args:
        theme_path: Path to YAML theme file (None = use default)
        output_dir: Directory to save MIDI files
    """
    # Load theme from YAML file
    theme = ThemeLoader.load(Path(theme_path) if theme_path else None)

    print(f"\n{'='*60}")
    print(f"YOURDIO - Retro Lo-Fi Algorithmic Composer")
    print(f"{'='*60}")
    print(f"Theme: {theme.get('name', 'Default')}")
    if 'description' in theme:
        print(f"  {theme['description']}")
    print(f"{'='*60}\n")

    # Prime sequence for all chapters
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]

    if output_dir is None:
        output_dir = Path('midi_output')
    output_dir.mkdir(exist_ok=True)

    # Get structural arc from theme
    arc_config = theme.get('structural_arc', {})

    for chapter in range(12):
        print(f"Generating Chapter {chapter}...", end=' ')

        # Calculate intensity for this chapter
        intensity = calculate_chapter_intensity(chapter, total_chapters=12, arc_config=arc_config)

        # Adjust tempo based on intensity if parameter_evolution enabled
        param_evolution = theme.get('parameter_evolution', {})
        current_theme = theme.copy()

        if param_evolution.get('tempo', True):
            tempo_config = theme['tempo']
            tempo_min, tempo_max = tempo_config['variation_range']
            current_tempo = int(tempo_min + intensity * (tempo_max - tempo_min))
            current_theme['tempo'] = {**tempo_config, 'base': current_tempo}

        # Adjust polyphony based on intensity if enabled
        if param_evolution.get('polyphony', True):
            max_poly = int(18 + intensity * 14)  # 18-32 voices
        else:
            max_poly = None  # Use theme default

        composer = RetroMIDIComposer(current_theme, max_polyphony=max_poly)

        # Each chapter gets its own prime subsequence
        chapter_primes = primes[chapter:chapter+8]
        chaos_seed = (primes[chapter] % 97) / 97.0

        midi = composer.create_chapter_midi(
            chapter_id=chapter,
            duration_minutes=30,
            prime_sequence=chapter_primes,
            chaos_seed=chaos_seed
        )

        output_path = output_dir / f'chapter_{chapter:02d}.mid'
        composer.save_chapter(midi, str(output_path))

        actual_tempo = current_theme['tempo']['base']
        print(f"Done! (intensity: {intensity:.2f}, tempo: {actual_tempo} BPM)")
        print(f"  -> {output_path}")

    print(f"\n{'='*60}")
    print(f"Generation complete! 12 chapters saved to: {output_dir}")
    print(f"Total duration: 6 hours")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Yourdio: Retro Lo-Fi Algorithmic Composer')
    parser.add_argument('--theme', type=str, default=None,
                       help='Path to YAML theme file (default: built-in default theme)')
    parser.add_argument('--output', type=str, default='midi_output',
                       help='Output directory for MIDI files (default: midi_output)')

    args = parser.parse_args()

    generate_full_composition(
        theme_path=args.theme,
        output_dir=Path(args.output)
    )
