"""
Reference Audio Analyzer for Yourdio
Analyzes audio files to extract musical features and suggest theme parameters
Requires: librosa, numpy
Install: pip install librosa numpy
"""

import librosa
import numpy as np
from pathlib import Path
from typing import Dict
import yaml


class ReferenceAnalyzer:
    """Analyze reference audio to extract style parameters"""

    # Map spectral characteristics to GM patches
    TIMBRE_MAP = {
        "bright": {"harmonic_bed": 88, "melodic_texture": 11, "drones": 54, "ambient_events": 100},
        "warm": {"harmonic_bed": 89, "melodic_texture": 92, "drones": 95, "ambient_events": 99},
        "dark": {"harmonic_bed": 90, "melodic_texture": 81, "drones": 39, "ambient_events": 101},
        "metallic": {"harmonic_bed": 93, "melodic_texture": 82, "drones": 38, "ambient_events": 98},
    }

    @staticmethod
    def analyze(audio_path: str, output_theme_path: str = None) -> Dict:
        """
        Analyze reference audio and generate theme YAML

        Args:
            audio_path: Path to audio file (WAV, MP3, OGG, etc.)
            output_theme_path: Where to save generated theme YAML (optional)

        Returns:
            Dictionary with suggested theme parameters
        """
        print(f"Analyzing: {audio_path}")
        print("=" * 60)

        # Load audio
        y, sr = librosa.load(audio_path, duration=180)  # Analyze first 3 minutes
        print(f"✓ Loaded audio: {len(y)/sr:.1f}s @ {sr}Hz")

        # Extract features
        tempo_bpm = ReferenceAnalyzer._extract_tempo(y, sr)
        brightness = ReferenceAnalyzer._extract_brightness(y, sr)
        mode = ReferenceAnalyzer._extract_mode(y, sr)
        energy = ReferenceAnalyzer._extract_energy(y, sr)
        complexity = ReferenceAnalyzer._extract_complexity(y, sr)

        print("\nExtracted Features:")
        print(f"  Tempo: {tempo_bpm:.1f} BPM")
        print(f"  Brightness: {brightness:.2f} (0=dark, 1=bright)")
        print(f"  Mode: {mode}")
        print(f"  Energy: {energy:.2f} (0=calm, 1=intense)")
        print(f"  Complexity: {complexity:.2f} (0=simple, 1=complex)")

        # Generate theme
        theme = ReferenceAnalyzer._features_to_theme(
            tempo_bpm, brightness, mode, energy, complexity, audio_path
        )

        # Save if requested
        if output_theme_path:
            output_path = Path(output_theme_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                yaml.dump(theme, f, default_flow_style=False, sort_keys=False)
            print(f"\n✓ Saved theme: {output_path}")

        return theme

    @staticmethod
    def _extract_tempo(y: np.ndarray, sr: int) -> float:
        """Extract tempo in BPM"""
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        # Clamp to reasonable range for ambient (40-80 BPM)
        return np.clip(tempo, 40, 80)

    @staticmethod
    def _extract_brightness(y: np.ndarray, sr: int) -> float:
        """Extract spectral brightness (0=dark, 1=bright)"""
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        # Normalize to 0-1 (assuming centroid range 500-4000 Hz for ambient)
        brightness = (np.mean(spectral_centroid) - 500) / 3500
        return np.clip(brightness, 0, 1)

    @staticmethod
    def _extract_mode(y: np.ndarray, sr: int) -> str:
        """Infer modal center from chroma features"""
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)

        # Detect root note (most prominent pitch class)
        root_idx = np.argmax(chroma_mean)

        # Detect mode by analyzing interval patterns
        # (Simplified: check minor vs major third)
        minor_third = chroma_mean[(root_idx + 3) % 12]
        major_third = chroma_mean[(root_idx + 4) % 12]

        if minor_third > major_third:
            # Minor mode - choose between dorian/aeolian/phrygian
            second = chroma_mean[(root_idx + 2) % 12]
            if second > chroma_mean[(root_idx + 1) % 12]:
                mode_type = "dorian" if root_idx == 2 else "aeolian"
            else:
                mode_type = "phrygian"
        else:
            mode_type = "dorian"  # Default to dorian for ambiguous cases

        # Map to available modes
        mode_map = {"dorian": "D_dorian", "aeolian": "A_aeolian", "phrygian": "E_phrygian"}

        return mode_map.get(mode_type, "D_dorian")

    @staticmethod
    def _extract_energy(y: np.ndarray, sr: int) -> float:
        """Extract overall energy/intensity (0=calm, 1=intense)"""
        rms = librosa.feature.rms(y=y)[0]
        energy = np.mean(rms)
        # Normalize (typical ambient RMS: 0.01-0.2)
        return np.clip((energy - 0.01) / 0.19, 0, 1)

    @staticmethod
    def _extract_complexity(y: np.ndarray, sr: int) -> float:
        """Extract harmonic complexity (0=simple, 1=complex)"""
        spectral_flatness = librosa.feature.spectral_flatness(y=y)
        # Higher flatness = more noise-like = more complex textures
        complexity = np.mean(spectral_flatness)
        return np.clip(complexity * 10, 0, 1)

    @staticmethod
    def _features_to_theme(
        tempo: float, brightness: float, mode: str, energy: float, complexity: float, audio_path: str
    ) -> Dict:
        """Convert extracted features to theme parameters"""

        # Determine timbre aesthetic
        if brightness > 0.7:
            timbre_aesthetic = "bright"
        elif brightness < 0.3:
            timbre_aesthetic = "dark"
        elif complexity > 0.6:
            timbre_aesthetic = "metallic"
        else:
            timbre_aesthetic = "warm"

        # Determine harmony rules based on complexity
        if complexity > 0.6:
            harmony_type = "dissonant_clusters"
            intervals = [0, 1, 3]
        elif complexity > 0.4:
            harmony_type = "quartal"
            intervals = [0, 3, 6]
        else:
            harmony_type = "tertian"
            intervals = [0, 2, 4]

        # Determine dynamics based on energy
        base_velocity = int(40 + energy * 30)  # 40-70 range
        velocity_range = int(15 + energy * 20)  # 15-35 range

        # Determine structural arc
        if energy > 0.6:
            arc_type = "slow_burn"
            max_intensity = 0.9
        else:
            arc_type = "parabolic"
            max_intensity = 0.7 + energy * 0.2

        theme = {
            "name": f"Generated Theme from {Path(audio_path).stem}",
            "description": f"Auto-generated theme (tempo={tempo:.0f}, brightness={brightness:.2f}, energy={energy:.2f})",
            "modal_center": mode,
            "harmony_rules": {
                "type": harmony_type,
                "intervals": intervals,
                "variation": "tertian",
                "variation_intervals": [0, 2, 4],
                "variation_chance_mod": 3 + int(complexity * 4),
            },
            "rhythmic_language": {
                "harmonic_bed": {
                    "type": "prime_modulated",
                    "base_duration": int(32 - energy * 8),  # Faster when energetic
                    "prime_mod_factor": 8,
                },
                "melodic_texture": {"type": "fibonacci", "sequence_length": 8, "base_unit": 0.25},
                "drones": {
                    "type": "lorenz_attractor",
                    "duration_multiplier": int(5 - energy * 2),  # Shorter when energetic
                    "cc_event_interval": 4,
                },
                "ambient_events": {
                    "type": "logistic_map",
                    "threshold": 0.85 + complexity * 0.05,
                    "event_count": int(50 + energy * 40),
                },
            },
            "ensemble_gm": ReferenceAnalyzer.TIMBRE_MAP[timbre_aesthetic],
            "tempo": {"base": int(tempo), "variation_range": [int(tempo - 6), int(tempo + 6)]},
            "dynamics": {
                "harmonic_bed": {"base_velocity": base_velocity, "prime_mod_range": velocity_range},
                "melodic_texture": {
                    "base_velocity": base_velocity + 10,
                    "prime_mod_range": velocity_range + 5,
                },
                "drones": {"velocity": base_velocity + 5},
                "ambient_events": {
                    "base_velocity": base_velocity + 15,
                    "intensity_scaling": int(25 + energy * 15),
                },
            },
            "structural_arc": {
                "type": arc_type,
                "min_intensity": 0.15 + energy * 0.1,
                "max_intensity": max_intensity,
                "climax_chapter": 6,
            },
            "parameter_evolution": {
                "tempo": True,
                "polyphony": True,
                "velocity": True,
                "register": energy > 0.5,
            },
            "chaos": {
                "logistic_r": 3.84 + complexity * 0.08,
                "lorenz_sigma": 9.0 + complexity * 3.0,
                "lorenz_rho": 28.0,
                "lorenz_beta": 2.666,
            },
            "motif": {
                "core_pattern": [0, 2, 5, 7],
                "interval_minutes": int(15 + (1 - energy) * 10),  # Rare when calm
                "register_shift_prime_mod": 2,
                "ornament_density_mod": int(4 + complexity * 4),
            },
        }

        return theme


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python analyze_reference.py <audio_file> [output_theme.yaml]")
        print("\nExample:")
        print("  python analyze_reference.py samples/myst_track.mp3 themes/generated_myst.yaml")
        sys.exit(1)

    audio_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        theme = ReferenceAnalyzer.analyze(audio_file, output_file)

        if not output_file:
            print("\nGenerated Theme (preview):")
            print("=" * 60)
            print(yaml.dump(theme, default_flow_style=False, sort_keys=False))

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
