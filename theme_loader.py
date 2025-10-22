"""
Theme Loader for Yourdio

Loads and validates YAML theme configuration files for the RetroMIDIComposer.

This module handles:
- Loading YAML theme files from disk
- Merging partial themes with default values
- Validating theme structure
- Providing default theme configurations

Author: Yourdio Contributors
License: MIT
"""

__version__ = "1.0.5"
__author__ = "Yourdio Contributors"
__license__ = "MIT"

import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class ThemeLoader:
    """Load and validate YAML theme files"""

    # Default theme if none specified
    DEFAULT_THEME = {
        "name": "Default",
        "modal_center": "D_dorian",
        "harmony_rules": {
            "type": "quartal",
            "intervals": [0, 3, 6],
        },
        "rhythmic_language": {
            "harmonic_bed": {"type": "prime_modulated", "base_duration": 32, "prime_mod_factor": 8},
            "melodic_texture": {"type": "fibonacci", "sequence_length": 8, "base_unit": 0.25},
            "drones": {
                "type": "lorenz_attractor",
                "duration_multiplier": 4,
                "cc_event_interval": 4,
            },
            "ambient_events": {"type": "logistic_map", "threshold": 0.87, "event_count": 64},
        },
        "ensemble_gm": {
            "harmonic_bed": 89,
            "melodic_texture": 92,
            "drones": 95,
            "ambient_events": 99,
        },
        "tempo": {"base": 58, "variation_range": [52, 68]},
        "dynamics": {
            "harmonic_bed": {"base_velocity": 45, "prime_mod_range": 20},
            "melodic_texture": {"base_velocity": 55, "prime_mod_range": 25},
            "drones": {"velocity": 50},
            "ambient_events": {"base_velocity": 60, "intensity_scaling": 30},
        },
        "structural_arc": {
            "type": "parabolic",
            "min_intensity": 0.2,
            "max_intensity": 0.8,
            "climax_chapter": 6,
        },
        "parameter_evolution": {
            "tempo": True,
            "polyphony": True,
            "velocity": True,
            "register": True,
        },
        "chaos": {
            "logistic_r": 3.86,
            "lorenz_sigma": 10.0,
            "lorenz_rho": 28.0,
            "lorenz_beta": 8.0 / 3.0,
        },
        "motif": {
            "core_pattern": [0, 2, 5, 7],
            "interval_minutes": 17,
            "register_shift_prime_mod": 2,
            "ornament_density_mod": 5,
        },
    }

    @classmethod
    def load(cls, theme_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        Load theme from YAML file

        Args:
            theme_path: Path to YAML theme file (None = use default)

        Returns:
            Theme dictionary with all parameters
        """
        if theme_path is None:
            print("Using default theme")
            return cls.DEFAULT_THEME.copy()

        theme_path = Path(theme_path)

        if not theme_path.exists():
            raise FileNotFoundError(f"Theme file not found: {theme_path}")

        print(f"Loading theme: {theme_path}")

        with open(theme_path, "r") as f:
            theme = yaml.safe_load(f)

        # Merge with defaults (for any missing fields)
        theme = cls._merge_with_defaults(theme)

        # Validate
        cls._validate(theme)

        print(f"  OK Loaded: {theme.get('name', 'Unnamed Theme')}")
        if "description" in theme:
            print(f"  {theme['description']}")

        return theme

    @classmethod
    def _merge_with_defaults(cls, theme: Dict) -> Dict:
        """Merge loaded theme with defaults for missing fields"""
        merged = cls.DEFAULT_THEME.copy()

        # Deep merge for nested dicts
        for key, value in theme.items():
            if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
                merged[key] = {**merged[key], **value}  # type: ignore[dict-item]
            else:
                merged[key] = value

        return merged

    @classmethod
    def _validate(cls, theme: Dict) -> None:
        """Validate theme has required structure"""
        required_sections = [
            "modal_center",
            "harmony_rules",
            "rhythmic_language",
            "ensemble_gm",
            "tempo",
        ]

        for section in required_sections:
            if section not in theme:
                raise ValueError(f"Theme missing required section: {section}")

        # Validate modal_center
        valid_modes = ["D_dorian", "A_aeolian", "E_phrygian"]
        if theme["modal_center"] not in valid_modes and "custom_scale" not in theme:
            raise ValueError(
                f"Invalid modal_center: {theme['modal_center']}. "
                f"Must be one of {valid_modes} or provide custom_scale"
            )

        # Validate harmony_rules
        if "intervals" not in theme["harmony_rules"]:
            raise ValueError("harmony_rules must specify 'intervals'")

        # Validate ensemble_gm patch numbers (0-127)
        for track, patch in theme["ensemble_gm"].items():
            if not (0 <= patch <= 127):
                raise ValueError(f"Invalid GM patch {patch} for {track}. Must be 0-127")

        print("  OK Theme validation passed")

    @classmethod
    def list_available_themes(cls, themes_dir: Path = Path("themes")) -> list:
        """List all available theme files"""
        if not themes_dir.exists():
            return []

        return sorted(themes_dir.glob("*.yaml"))


# Convenience function
def load_theme(theme_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load a theme file

    Args:
        theme_path: Path to YAML file, or None for default

    Returns:
        Theme dictionary

    Example:
        theme = load_theme('themes/ambient_myst.yaml')
        composer = RetroMIDIComposer(theme)
    """
    return ThemeLoader.load(Path(theme_path) if theme_path else None)


if __name__ == "__main__":
    # Test theme loading
    print("=" * 60)
    print("TESTING THEME LOADER")
    print("=" * 60)

    # List available themes
    themes = ThemeLoader.list_available_themes()
    print(f"\nFound {len(themes)} themes:")
    for theme_file in themes:
        print(f"  - {theme_file.name}")

    # Load each theme
    print("\nValidating themes:")
    for theme_file in themes:
        try:
            theme = ThemeLoader.load(theme_file)
            print(f"  OK {theme_file.name}: OK")
        except Exception as e:
            print(f"  FAIL {theme_file.name}: {e}")

    # Load default
    print("\nLoading default theme:")
    default = ThemeLoader.load(None)
    print(f"  OK {default['name']}")
