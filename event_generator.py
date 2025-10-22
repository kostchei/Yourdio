#!/usr/bin/env python3
"""
Event-Based Soundscape Generator for Yourdio

Generate short, loopable musical moments for specific game events.

This module creates brief MIDI soundscapes (1-4 minutes) tailored for
interactive media events such as:
- Combat encounters
- Stealth sequences
- Tavern ambiance
- Victory fanfares
- Exploration moments
- Boss battles

Each event type applies specific modifications to the base theme to
create appropriate mood and intensity.

Author: Yourdio Contributors
License: MIT
"""

__version__ = "1.0.5"
__author__ = "Yourdio Contributors"
__license__ = "MIT"

from pathlib import Path
from typing import Optional
import argparse

from yourdio import RetroMIDIComposer
from theme_loader import ThemeLoader


class EventSoundscapeGenerator:
    """Generate short, event-specific musical soundscapes"""

    # Event-specific configurations
    EVENT_CONFIGS = {
        "carousing": {
            "duration_minutes": 2.0,  # Short, loopable
            "primes": [3, 5, 7, 11],  # Upbeat prime sequence
            "chaos_seed": 0.42,
            "description": "Lively tavern atmosphere",
        },
        "fight": {
            "duration_minutes": 1.5,
            "primes": [2, 3, 5, 7],  # Aggressive, driving
            "chaos_seed": 0.87,
            "description": "Intense combat music",
        },
        "stealth": {
            "duration_minutes": 3.0,
            "primes": [5, 7, 11, 13],  # Sparse, tense
            "chaos_seed": 0.23,
            "description": "Tense sneaking atmosphere",
        },
        "victory": {
            "duration_minutes": 1.0,
            "primes": [3, 5, 7],  # Triumphant, short
            "chaos_seed": 0.65,
            "description": "Victory fanfare",
        },
        "exploration": {
            "duration_minutes": 4.0,
            "primes": [7, 11, 13, 17],  # Wonder, curiosity
            "chaos_seed": 0.31,
            "description": "Atmospheric exploration",
        },
        "tension": {
            "duration_minutes": 2.5,
            "primes": [2, 5, 11],  # Dissonant, unsettling
            "chaos_seed": 0.91,
            "description": "Building tension/dread",
        },
        "rest": {
            "duration_minutes": 3.0,
            "primes": [11, 13, 17],  # Peaceful, restorative
            "chaos_seed": 0.15,
            "description": "Peaceful rest/campfire",
        },
        "death": {
            "duration_minutes": 0.5,
            "primes": [2, 3],  # Short, somber
            "chaos_seed": 0.73,
            "description": "Death/failure sting",
        },
    }

    @classmethod
    def generate_event(
        cls, event_type: str, theme_path: Optional[str] = None, output_path: Optional[Path] = None
    ) -> Path:
        """
        Generate a soundscape for a specific event

        Args:
            event_type: Type of event (carousing, fight, stealth, etc.)
            theme_path: Path to YAML theme file (None = use default)
            output_path: Where to save the MIDI file (None = auto-generate)

        Returns:
            Path to generated MIDI file
        """
        if event_type not in cls.EVENT_CONFIGS:
            available = ", ".join(cls.EVENT_CONFIGS.keys())
            raise ValueError(f"Unknown event type '{event_type}'. Available: {available}")

        config = cls.EVENT_CONFIGS[event_type]

        # Load theme
        theme = ThemeLoader.load(Path(theme_path) if theme_path else None)

        print(f"\nGenerating '{event_type}' soundscape...")
        print(f"  Description: {config['description']}")
        print(f"  Duration: {config['duration_minutes']} minutes")
        print(f"  Theme: {theme.get('name', 'Default')}")

        # Create composer
        composer = RetroMIDIComposer(theme)

        # Generate MIDI
        midi = composer.create_chapter_midi(
            chapter_id=0,
            duration_minutes=float(config["duration_minutes"]),  # type: ignore[arg-type]
            prime_sequence=list(config["primes"]),  # type: ignore[call-overload]
            chaos_seed=float(config["chaos_seed"]),  # type: ignore[arg-type]
        )

        # Determine output path
        if output_path is None:
            output_dir = Path("events_output")
            output_dir.mkdir(exist_ok=True)
            theme_name = theme.get("name", "default").lower().replace(" ", "_")
            output_path = output_dir / f"{event_type}_{theme_name}.mid"

        # Save
        composer.save_chapter(midi, str(output_path))
        print(f"  Saved: {output_path}")

        return output_path

    @classmethod
    def generate_event_set(
        cls,
        theme_path: Optional[str] = None,
        events: Optional[list] = None,
        output_dir: Optional[Path] = None,
    ):
        """
        Generate a complete set of event soundscapes

        Args:
            theme_path: Path to YAML theme file
            events: List of event types to generate (None = all)
            output_dir: Directory to save files
        """
        if events is None:
            events = list(cls.EVENT_CONFIGS.keys())

        if output_dir is None:
            output_dir = Path("events_output")

        output_dir.mkdir(exist_ok=True)

        # Load theme once
        theme = ThemeLoader.load(Path(theme_path) if theme_path else None)
        theme_name = theme.get("name", "Default")

        print(f"\n{'='*60}")
        print("YOURDIO EVENT SOUNDSCAPE GENERATOR")
        print(f"{'='*60}")
        print(f"Theme: {theme_name}")
        print(f"Generating {len(events)} event soundscapes")
        print(f"Output: {output_dir}")
        print(f"{'='*60}\n")

        generated_files = []

        for event_type in events:
            if event_type not in cls.EVENT_CONFIGS:
                print(f"Warning: Unknown event type '{event_type}', skipping...")
                continue

            theme_slug = theme_name.lower().replace(" ", "_")
            output_path = output_dir / f"{event_type}_{theme_slug}.mid"

            try:
                cls.generate_event(event_type, theme_path, output_path)
                generated_files.append(output_path)
            except Exception as e:
                print(f"  Error generating {event_type}: {e}")

        print(f"\n{'='*60}")
        print(f"Generated {len(generated_files)} event soundscapes")
        print(f"{'='*60}\n")

        return generated_files

    @classmethod
    def list_events(cls):
        """List all available event types"""
        print("\nAvailable Event Types:")
        print(f"{'='*60}")
        for event_type, config in cls.EVENT_CONFIGS.items():
            duration = config["duration_minutes"]
            desc = config["description"]
            print(f"  {event_type:15} - {desc:30} ({duration} min)")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate event-specific soundscapes for games/interactive media"
    )

    parser.add_argument(
        "--event", type=str, help="Generate single event (carousing, fight, stealth, etc.)"
    )
    parser.add_argument(
        "--theme",
        type=str,
        default=None,
        help="Path to YAML theme file (default: built-in default)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="events_output",
        help="Output directory (default: events_output)",
    )
    parser.add_argument("--all", action="store_true", help="Generate all event types")
    parser.add_argument("--list", action="store_true", help="List all available event types")
    parser.add_argument(
        "--events", type=str, nargs="+", help="Generate specific events (space-separated list)"
    )

    args = parser.parse_args()

    if args.list:
        EventSoundscapeGenerator.list_events()
    elif args.event:
        # Generate single event
        EventSoundscapeGenerator.generate_event(event_type=args.event, theme_path=args.theme)
    elif args.all:
        # Generate all events
        EventSoundscapeGenerator.generate_event_set(
            theme_path=args.theme, output_dir=Path(args.output)
        )
    elif args.events:
        # Generate specific list of events
        EventSoundscapeGenerator.generate_event_set(
            theme_path=args.theme, events=args.events, output_dir=Path(args.output)
        )
    else:
        parser.print_help()
