#!/usr/bin/env python3
"""Quick script to generate a test MIDI file"""

from yourdio import RetroMIDIComposer
import yaml

# Simple dark ambient theme
theme = {
    'name': 'OGG Test Sample',
    'tempo': 80,
    'key': 'Dm',
    'time_signature': '4/4',
    'scales': ['D', 'natural_minor'],
    'chords': [
        {'root': 'D', 'type': 'minor'},
        {'root': 'F', 'type': 'major'},
        {'root': 'C', 'type': 'major'},
        {'root': 'G', 'type': 'minor'}
    ],
    'rhythm_patterns': {
        'bass': [1, 0, 0, 1, 0, 0, 1, 0],
        'pad': [1, 0, 1, 0, 1, 0, 1, 0]
    },
    'instruments': {
        'bass': {'channel': 1, 'program': 38},
        'pad': {'channel': 2, 'program': 91},
        'lead': {'channel': 3, 'program': 81}
    }
}

print("Generating test MIDI file...")
print(f"Theme: {theme['name']}")
print(f"Key: {theme['key']}, Tempo: {theme['tempo']} BPM")

# Generate 2-minute sample (short chapter)
composer = RetroMIDIComposer(theme)
midi = composer.create_chapter_midi(
    chapter_id=1,
    duration_minutes=2,
    prime_sequence=[2, 3, 5, 7, 11],
    chaos_seed=0.5
)

# Save to file
output_path = "test_sample.mid"
composer.save_chapter(midi, output_path)

print(f"\nMIDI file created: {output_path}")
print("You can play this in the MIDI Player tab of Yourdio GUI!")
