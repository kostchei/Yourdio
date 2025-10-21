#!/usr/bin/env python3
"""
Simple MIDI Playback for Yourdio
Plays MIDI files using pygame.midi
"""

import pygame
import pygame.midi
import time
from pathlib import Path


def play_midi(midi_path: str):
    """
    Play a MIDI file using pygame.midi

    Args:
        midi_path: Path to MIDI file
    """
    midi_path = Path(midi_path)

    if not midi_path.exists():
        print(f"Error: File not found: {midi_path}")
        return

    print(f"\nPlaying: {midi_path.name}")
    print("Press Ctrl+C to stop\n")

    # Initialize pygame and pygame.midi
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(str(midi_path))

    # Play the MIDI file
    pygame.mixer.music.play()

    # Wait for playback to finish or user interrupt
    try:
        while pygame.mixer.music.get_busy():
            time.sleep(1)
        print("\nPlayback finished!")
    except KeyboardInterrupt:
        print("\n\nPlayback stopped by user")
        pygame.mixer.music.stop()
    finally:
        pygame.quit()


def play_all_chapters(output_dir: str):
    """
    Play all chapters in sequence

    Args:
        output_dir: Directory containing chapter MIDI files
    """
    output_dir = Path(output_dir)

    if not output_dir.exists():
        print(f"Error: Directory not found: {output_dir}")
        return

    # Get all MIDI files sorted by name
    midi_files = sorted(output_dir.glob("chapter_*.mid"))

    if not midi_files:
        print(f"No chapter MIDI files found in: {output_dir}")
        return

    print(f"\n{'='*60}")
    print("YOURDIO MIDI PLAYER")
    print(f"{'='*60}")
    print(f"Found {len(midi_files)} chapters")
    print(f"Total duration: {len(midi_files) * 30} minutes ({len(midi_files) * 0.5:.1f} hours)")
    print(f"{'='*60}\n")

    # Initialize pygame
    pygame.init()
    pygame.mixer.init()

    try:
        for i, midi_file in enumerate(midi_files):
            print(f"\n[{i+1}/{len(midi_files)}] Playing: {midi_file.name}")
            print("Press Ctrl+C to skip to next chapter or stop\n")

            pygame.mixer.music.load(str(midi_file))
            pygame.mixer.music.play()

            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                time.sleep(1)

            print(f"Chapter {i} complete!")

    except KeyboardInterrupt:
        print("\n\nPlayback stopped by user")
        pygame.mixer.music.stop()
    finally:
        pygame.quit()
        print("\n{'='*60}")
        print("Playback session ended")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Play Yourdio MIDI files")
    parser.add_argument("--file", type=str, help="Play a single MIDI file")
    parser.add_argument(
        "--dir",
        type=str,
        default="conan_output",
        help="Play all chapters from directory (default: conan_output)",
    )
    parser.add_argument("--chapter", type=int, help="Play specific chapter number (0-11)")

    args = parser.parse_args()

    if args.file:
        # Play single file
        play_midi(args.file)
    elif args.chapter is not None:
        # Play specific chapter
        chapter_file = Path(args.dir) / f"chapter_{args.chapter:02d}.mid"
        play_midi(str(chapter_file))
    else:
        # Play all chapters
        play_all_chapters(args.dir)
