from __future__ import annotations

import argparse
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from narration import NarrationClient


@dataclass(frozen=True)
class StyleProfile:
    temperature: float
    top_p: float
    repetition_penalty: float
    chunk_length: int
    max_new_tokens: int
    seed: Optional[int]


STYLE_PROFILES = {
    "neutral": StyleProfile(
        temperature=0.70,
        top_p=0.80,
        repetition_penalty=1.10,
        chunk_length=300,
        max_new_tokens=1024,
        seed=None,
    ),
    "old_japanese_evil_narrator": StyleProfile(
        temperature=0.55,
        top_p=0.70,
        repetition_penalty=1.20,
        chunk_length=260,
        max_new_tokens=1024,
        seed=7,
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate ExampleText narration in Mako-homage voice."
    )
    parser.add_argument(
        "--text-path",
        type=Path,
        default=ROOT / "narration" / "ExampleText.md",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=ROOT / "samples" / "generated_mako_homage",
    )
    parser.add_argument(
        "--output-name",
        default="ExampleText_mako_homage_old_japanese_evil.wav",
    )
    parser.add_argument(
        "--style-profile",
        choices=sorted(STYLE_PROFILES.keys()),
        default="old_japanese_evil_narrator",
    )
    parser.add_argument(
        "--direction",
        default="",
        help=(
            "Optional style direction keywords (not spoken), e.g. "
            "'old japanese evil narrator'."
        ),
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=700,
        help="Max characters per generation chunk.",
    )
    parser.add_argument(
        "--request-timeout",
        type=float,
        default=360.0,
        help="HTTP timeout in seconds per chunk request.",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=3,
        help="Retries per chunk when the API times out or errors.",
    )
    parser.add_argument(
        "--pause-ms",
        type=int,
        default=250,
        help="Silence inserted between chunks in the merged output.",
    )
    parser.add_argument(
        "--max-chunks",
        type=int,
        default=0,
        help="Limit number of chunks to generate (0 means all).",
    )
    parser.add_argument(
        "--spoken-prefix",
        default="",
        help="Optional spoken prefix prepended to each chunk (will be audible).",
    )
    return parser.parse_args()


def apply_direction(style: StyleProfile, direction: str) -> StyleProfile:
    direction_lower = direction.lower().strip()
    if not direction_lower:
        return style

    temperature = style.temperature
    top_p = style.top_p
    repetition_penalty = style.repetition_penalty
    chunk_length = style.chunk_length
    max_new_tokens = style.max_new_tokens
    seed = style.seed

    if "old" in direction_lower:
        temperature -= 0.05
        top_p -= 0.03
    if "evil" in direction_lower or "dark" in direction_lower or "sinister" in direction_lower:
        temperature -= 0.03
        repetition_penalty += 0.05
    if "japanese" in direction_lower:
        chunk_length = max(180, chunk_length - 20)
        if seed is None:
            seed = 7
    if "narrator" in direction_lower:
        repetition_penalty += 0.02

    temperature = min(max(temperature, 0.1), 1.0)
    top_p = min(max(top_p, 0.1), 1.0)
    repetition_penalty = min(max(repetition_penalty, 0.9), 2.0)

    return StyleProfile(
        temperature=temperature,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        chunk_length=chunk_length,
        max_new_tokens=max_new_tokens,
        seed=seed,
    )


def split_long_text(text: str, max_chars: int) -> list[str]:
    blocks = [b.strip() for b in re.split(r"\n(?=Part\s+\d+:)", text) if b.strip()]
    if not blocks:
        blocks = [text.strip()]

    chunks: list[str] = []
    for block in blocks:
        paras = [p.strip() for p in block.split("\n\n") if p.strip()]
        cur = ""
        for para in paras:
            candidate = para if not cur else f"{cur}\n\n{para}"
            if len(candidate) <= max_chars:
                cur = candidate
                continue
            if cur:
                chunks.append(cur)
            cur = ""
            if len(para) <= max_chars:
                cur = para
                continue

            sentences = re.split(r"(?<=[.!?])\s+", para)
            s_cur = ""
            for sent in sentences:
                sent = sent.strip()
                if not sent:
                    continue
                s_candidate = sent if not s_cur else f"{s_cur} {sent}"
                if len(s_candidate) <= max_chars:
                    s_cur = s_candidate
                else:
                    if s_cur:
                        chunks.append(s_cur)
                    s_cur = sent
                    while len(s_cur) > max_chars:
                        chunks.append(s_cur[:max_chars])
                        s_cur = s_cur[max_chars:]
            if s_cur:
                cur = s_cur
        if cur:
            chunks.append(cur)
    return chunks


def main() -> int:
    args = parse_args()
    style = apply_direction(STYLE_PROFILES[args.style_profile], args.direction)

    out_dir = args.out_dir
    chunks_dir = out_dir / "chunks"
    out_dir.mkdir(parents=True, exist_ok=True)
    chunks_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / args.output_name

    samurai = ROOT / "samples" / "Mako" / "Mako_Samurai_Jack_Reference.wav"
    conan = ROOT / "samples" / "Mako" / "Mako_Conan_Reference.wav"
    if not args.text_path.exists() or not samurai.exists() or not conan.exists():
        raise FileNotFoundError("Missing ExampleText or reference files.")

    text = args.text_path.read_text(encoding="utf-8", errors="replace").strip()
    if not text:
        raise RuntimeError("ExampleText.md is empty.")

    references = [
        {
            "audio": samurai.read_bytes(),
            "text": (
                "Long ago in a distant land, I, Aku, the shape-shifting master "
                "of darkness, unleashed an unspeakable evil."
            ),
        },
        {
            "audio": conan.read_bytes(),
            "text": (
                "Between the time when the oceans drank Atlantis and the rise of "
                "the sons of Aryas, there was an age undreamed of."
            ),
        },
    ]

    client = NarrationClient()
    if not client.is_alive():
        raise RuntimeError("Fish Speech API server is not running at 127.0.0.1:8080.")

    chunks = split_long_text(text, max_chars=args.max_chars)
    if args.max_chunks > 0:
        chunks = chunks[: args.max_chunks]
    if not chunks:
        raise RuntimeError("No chunks were produced from ExampleText.md.")

    print(f"Generating {len(chunks)} chunks with style profile: {args.style_profile}")
    if args.direction.strip():
        print(f"Direction: {args.direction.strip()}")
    print(
        "Params: "
        f"temp={style.temperature:.2f}, top_p={style.top_p:.2f}, "
        f"rep={style.repetition_penalty:.2f}, chunk_len={style.chunk_length}, "
        f"seed={style.seed}"
    )
    chunk_files: list[Path] = []
    for i, chunk in enumerate(chunks, start=1):
        chunk_path = chunks_dir / f"chunk_{i:03d}.wav"
        if chunk_path.exists() and chunk_path.stat().st_size > 4096:
            print(f"  [{i}/{len(chunks)}] reusing existing chunk")
            chunk_files.append(chunk_path)
            continue

        chunk_text = f"{args.spoken_prefix.strip()} {chunk}".strip() if args.spoken_prefix else chunk

        print(f"  [{i}/{len(chunks)}] generating")
        last_error: Optional[Exception] = None
        for attempt in range(1, args.max_retries + 1):
            try:
                client.speak(
                    text=chunk_text,
                    output_path=str(chunk_path),
                    temperature=style.temperature,
                    top_p=style.top_p,
                    repetition_penalty=style.repetition_penalty,
                    max_new_tokens=style.max_new_tokens,
                    chunk_length=style.chunk_length,
                    seed=style.seed,
                    references_list=references,
                    request_timeout=args.request_timeout,
                )
                last_error = None
                break
            except Exception as exc:
                last_error = exc
                print(f"    attempt {attempt}/{args.max_retries} failed: {exc}")
                time.sleep(4 * attempt)

        if last_error is not None:
            raise RuntimeError(f"Failed generating chunk {i}") from last_error

        chunk_files.append(chunk_path)

    merged: list[np.ndarray] = []
    sample_rate = None
    pause = None
    for i, chunk_file in enumerate(chunk_files):
        audio, sr = sf.read(str(chunk_file), dtype="float32")
        if audio.ndim == 2:
            audio = audio.mean(axis=1)
        if sample_rate is None:
            sample_rate = int(sr)
            pause = np.zeros(int(sample_rate * max(args.pause_ms, 0) / 1000), dtype=np.float32)
        elif int(sr) != sample_rate:
            raise RuntimeError(f"Sample rate mismatch in {chunk_file}: {sr} != {sample_rate}")
        merged.append(audio)
        if i < len(chunk_files) - 1 and len(pause) > 0:
            merged.append(pause)

    if sample_rate is None:
        raise RuntimeError("No chunk audio was produced.")

    final_audio = np.concatenate(merged) if merged else np.zeros(1, dtype=np.float32)
    sf.write(str(out_path), final_audio, sample_rate, subtype="PCM_16")
    print(f"Done: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
