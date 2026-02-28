from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np
import soundfile as sf


ROOT = Path(__file__).resolve().parent.parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Stitch chunk WAV files into one omnibus WAV file."
    )
    parser.add_argument(
        "--chunks-dir",
        type=Path,
        default=ROOT / "samples" / "generated_mako_homage" / "chunks",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT
        / "samples"
        / "generated_mako_homage"
        / "ExampleText_mako_homage_old_japanese_evil_omnibus.wav",
    )
    parser.add_argument(
        "--pause-ms",
        type=int,
        default=250,
        help="Silence between chunks in milliseconds.",
    )
    return parser.parse_args()


def _chunk_sort_key(path: Path) -> tuple[int, str]:
    match = re.search(r"(\d+)", path.stem)
    if match:
        return (int(match.group(1)), path.name)
    return (10**9, path.name)


def main() -> int:
    args = parse_args()
    chunks_dir = args.chunks_dir
    output = args.output

    if not chunks_dir.exists():
        raise FileNotFoundError(f"Chunks directory not found: {chunks_dir}")

    chunk_files = sorted(chunks_dir.glob("*.wav"), key=_chunk_sort_key)
    if not chunk_files:
        raise RuntimeError(f"No chunk WAV files found in: {chunks_dir}")

    merged: list[np.ndarray] = []
    sample_rate: int | None = None
    pause = None

    for i, chunk_file in enumerate(chunk_files):
        audio, sr = sf.read(str(chunk_file), dtype="float32")
        if audio.ndim == 2:
            audio = audio.mean(axis=1)
        if sample_rate is None:
            sample_rate = int(sr)
            pause = np.zeros(
                int(sample_rate * max(args.pause_ms, 0) / 1000), dtype=np.float32
            )
        elif int(sr) != sample_rate:
            raise RuntimeError(
                f"Sample rate mismatch in {chunk_file}: {sr} != {sample_rate}"
            )
        merged.append(audio)
        if i < len(chunk_files) - 1 and len(pause) > 0:
            merged.append(pause)

    if sample_rate is None:
        raise RuntimeError("No audio found to stitch.")

    output.parent.mkdir(parents=True, exist_ok=True)
    omnibus = np.concatenate(merged) if merged else np.zeros(1, dtype=np.float32)
    sf.write(str(output), omnibus, sample_rate, subtype="PCM_16")

    print(f"Stitched {len(chunk_files)} chunks")
    print(f"Output: {output}")
    print(f"Sample rate: {sample_rate} Hz")
    print(f"Duration: {len(omnibus) / sample_rate:.2f} sec")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
