"""
Narration health and error monitor.

This script is designed to run outside interactive prompts:
1) one-shot check for CI / quick verification
2) watch mode for continuous monitoring
"""

from __future__ import annotations

import argparse
import json
import logging
from logging.handlers import RotatingFileHandler
import sys
import time
import traceback
import wave
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Import from repo root when executed as a script.
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from narration import NarrationClient


@dataclass
class CheckResult:
    name: str
    ok: bool
    message: str
    duration_sec: float
    details: dict[str, Any]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Monitor Fish Speech narration health.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument(
        "--text-path",
        type=Path,
        default=REPO_ROOT / "narration" / "ExampleText.md",
    )
    parser.add_argument(
        "--samurai-ref",
        type=Path,
        default=REPO_ROOT / "samples" / "Mako" / "Mako_Samurai_Jack_Reference.wav",
    )
    parser.add_argument(
        "--conan-ref",
        type=Path,
        default=REPO_ROOT / "samples" / "Mako" / "Mako_Conan_Reference.wav",
    )
    parser.add_argument(
        "--log-dir",
        type=Path,
        default=REPO_ROOT / "narration" / "monitor_logs",
    )
    parser.add_argument(
        "--smoke-test",
        action="store_true",
        help="Run a short TTS synthesis smoke test and validate output WAV.",
    )
    parser.add_argument(
        "--smoke-text",
        default="Narration smoke test. Checking zero shot voice cloning pipeline.",
    )
    parser.add_argument(
        "--smoke-out",
        type=Path,
        default=REPO_ROOT / "narration" / "monitor_smoke.wav",
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Run checks repeatedly on a fixed interval.",
    )
    parser.add_argument("--interval-sec", type=int, default=30)
    return parser.parse_args()


def setup_logger(log_dir: Path) -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("narration_monitor")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        log_dir / "monitor.log",
        maxBytes=1_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def timed_check(name: str, fn) -> CheckResult:
    start = time.perf_counter()
    try:
        message, details = fn()
        duration = time.perf_counter() - start
        return CheckResult(name=name, ok=True, message=message, duration_sec=duration, details=details)
    except Exception as exc:
        duration = time.perf_counter() - start
        return CheckResult(
            name=name,
            ok=False,
            message=f"{type(exc).__name__}: {exc}",
            duration_sec=duration,
            details={"traceback": traceback.format_exc()},
        )


def check_server(client: NarrationClient) -> tuple[str, dict[str, Any]]:
    alive = client.is_alive(timeout=3.0)
    if not alive:
        raise RuntimeError(f"Fish Speech API is not reachable at {client.base_url}")
    return "server reachable", {"base_url": client.base_url}


def _validate_wav(path: Path) -> dict[str, Any]:
    with wave.open(str(path), "rb") as wav_file:
        channels = wav_file.getnchannels()
        frame_rate = wav_file.getframerate()
        frames = wav_file.getnframes()
        duration = frames / frame_rate if frame_rate > 0 else 0
        if frames <= 0:
            raise RuntimeError("WAV has zero frames")
        return {
            "channels": channels,
            "sample_rate": frame_rate,
            "frames": frames,
            "duration_sec": round(duration, 3),
        }


def check_text_file(text_path: Path) -> tuple[str, dict[str, Any]]:
    if not text_path.exists():
        raise FileNotFoundError(f"Missing text file: {text_path}")
    text = text_path.read_text(encoding="utf-8", errors="replace").strip()
    if not text:
        raise RuntimeError(f"Text file is empty: {text_path}")
    return "text file present", {"path": str(text_path), "chars": len(text), "lines": text.count("\n") + 1}


def check_reference_file(path: Path, label: str) -> tuple[str, dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing {label} reference: {path}")
    size = path.stat().st_size
    if size <= 1024:
        raise RuntimeError(f"{label} reference looks too small ({size} bytes)")
    wav_info = _validate_wav(path)
    return f"{label} reference valid", {"path": str(path), "size_bytes": size, **wav_info}


def check_smoke_synthesis(
    client: NarrationClient,
    smoke_text: str,
    smoke_out: Path,
    samurai_ref: Path,
    conan_ref: Path,
) -> tuple[str, dict[str, Any]]:
    references = [
        {
            "audio": samurai_ref.read_bytes(),
            "text": (
                "Long ago in a distant land, I, Aku, the shape-shifting master of darkness, "
                "unleashed an unspeakable evil."
            ),
        },
        {
            "audio": conan_ref.read_bytes(),
            "text": (
                "Between the time when the oceans drank Atlantis and the rise of the sons of Aryas, "
                "there was an age undreamed of."
            ),
        },
    ]
    out = client.speak(
        text=smoke_text,
        output_path=str(smoke_out),
        temperature=0.7,
        top_p=0.8,
        max_new_tokens=768,
        references_list=references,
    )
    if not out.exists():
        raise RuntimeError(f"Smoke output file was not created: {out}")
    size = out.stat().st_size
    if size <= 4096:
        raise RuntimeError(f"Smoke output size too small: {size} bytes")
    wav_info = _validate_wav(out)
    return "smoke synthesis ok", {"path": str(out), "size_bytes": size, **wav_info}


def run_once(args: argparse.Namespace, logger: logging.Logger) -> int:
    client = NarrationClient(host=args.host, port=args.port)
    checks = [
        timed_check("server", lambda: check_server(client)),
        timed_check("example_text", lambda: check_text_file(args.text_path)),
        timed_check("samurai_reference", lambda: check_reference_file(args.samurai_ref, "samurai")),
        timed_check("conan_reference", lambda: check_reference_file(args.conan_ref, "conan")),
    ]

    if args.smoke_test:
        checks.append(
            timed_check(
                "smoke_synthesis",
                lambda: check_smoke_synthesis(
                    client=client,
                    smoke_text=args.smoke_text,
                    smoke_out=args.smoke_out,
                    samurai_ref=args.samurai_ref,
                    conan_ref=args.conan_ref,
                ),
            )
        )

    all_ok = all(c.ok for c in checks)
    summary = {
        "timestamp_utc": utc_now_iso(),
        "ok": all_ok,
        "checks": [asdict(c) for c in checks],
    }

    args.log_dir.mkdir(parents=True, exist_ok=True)
    status_path = args.log_dir / "latest_status.json"
    status_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    for check in checks:
        level = logging.INFO if check.ok else logging.ERROR
        logger.log(level, "[%s] %s (%.2fs)", check.name, check.message, check.duration_sec)

    if all_ok:
        logger.info("monitor cycle: OK")
        return 0

    logger.error("monitor cycle: FAILED")
    return 1


def main() -> int:
    args = parse_args()
    logger = setup_logger(args.log_dir)
    logger.info("starting narration monitor")
    logger.info("mode=%s interval=%ss smoke_test=%s", "watch" if args.watch else "once", args.interval_sec, args.smoke_test)

    if not args.watch:
        return run_once(args, logger)

    # Watch mode: keep running and logging.
    while True:
        run_once(args, logger)
        time.sleep(max(args.interval_sec, 1))


if __name__ == "__main__":
    raise SystemExit(main())
