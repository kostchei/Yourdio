"""
Quick smoke-test for the Fish Speech 1.5 narration integration.

Run AFTER the server is up:
    conda activate fish-speech
    python narration/test_narration.py

Or with the fish-speech env directly:
    conda run -n fish-speech python narration/test_narration.py
"""

import sys
from pathlib import Path

# Make sure we can import from the repo root
sys.path.insert(0, str(Path(__file__).parent.parent))

from narration import NarrationClient

TEST_TEXT = (
    "Welcome to Yourdio. Sit back and let me narrate your story. "
    "Fish Speech version one point five is now powering this voice."
)

OUTPUT_PATH = Path(__file__).parent / "test_output.wav"


def main():
    client = NarrationClient()

    print("Checking server health ...")
    if not client.is_alive():
        print("\n[ERROR] Fish Speech server is not running.")
        print("  -> Double-click start_narration_server.bat first, then re-run this test.")
        sys.exit(1)

    print("Server is alive! Reading Mako reference audio files...\n")
    
    samurai_w = Path(__file__).parent.parent / "samples" / "Mako" / "Mako_Samurai_Jack_Reference.wav"
    conan_w = Path(__file__).parent.parent / "samples" / "Mako" / "Mako_Conan_Reference.wav"
    
    mako_references = []
    if samurai_w.exists() and conan_w.exists():
        mako_references = [
            {"audio": samurai_w.read_bytes(), "text": "Long ago in a distant land, I, Aku, the shape-shifting master of darkness, unleashed an unspeakable evil! But a foolish Samurai warrior wielding a magic sword stepped forth to oppose me."},
            {"audio": conan_w.read_bytes(), "text": "Between the time when the oceans drank Atlantis, and the rise of the sons of Aryas, there was an age undreamed of. And unto this, Conan, destined to wear the jeweled crown of Aquilonia upon a troubled brow."}
        ]

    print("Generating zero-shot cloning narration ...\n")
    out = client.speak(
        text=TEST_TEXT,
        output_path=str(OUTPUT_PATH),
        temperature=0.7,
        top_p=0.8,
        references_list=mako_references,
    )
    print(f"\n[OK] Mako-omage narration saved to: {out}")
    print("    Open the file to listen to the generated audio.")


if __name__ == "__main__":
    main()
