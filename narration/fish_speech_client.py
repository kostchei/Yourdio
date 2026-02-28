"""
Yourdio – Fish Speech 1.5 Narration Client
==========================================
Wraps the Fish Speech local API server so the rest of Yourdio can generate
narration audio with a single function call.

Usage
-----
    from narration.fish_speech_client import NarrationClient

    client = NarrationClient()           # connects to running API server
    audio_path = client.speak(
        text="Welcome to Yourdio!",
        output_path="output/intro.wav",
    )

The API server must be running first — use `start_server.bat` (or call
`NarrationClient.ensure_server()` programmatically).
"""

import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

import ormsgpack
import requests

# ── absolute paths ──────────────────────────────────────────────────────────────
_HERE = Path(__file__).parent
_REPO_ROOT = _HERE.parent
_FISH_DIR = _REPO_ROOT / "fish-speech"
_CHECKPOINTS = _FISH_DIR / "checkpoints" / "fish-speech-1.5"

# ── defaults ─────────────────────────────────────────────────────────────────────
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8080
DEFAULT_FORMAT = "wav"


class NarrationClient:
    """
    Thin Python wrapper around the Fish Speech 1.5 HTTP API.

    Parameters
    ----------
    host : str
        Host where the Fish Speech API server is running.
    port : int
        Port of the API server.
    api_key : str | None
        Optional bearer token if the server was started with --api-key.
    """

    def __init__(
        self,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        api_key: Optional[str] = None,
    ):
        self.base_url = f"http://{host}:{port}"
        self.tts_url = f"{self.base_url}/v1/tts"
        self.api_key = api_key
        self._headers = {
            "content-type": "application/msgpack",
        }
        if api_key:
            self._headers["authorization"] = f"Bearer {api_key}"

    # ── health ───────────────────────────────────────────────────────────────────

    def is_alive(self, timeout: float = 2.0) -> bool:
        """Return True if the Fish Speech API server is reachable."""
        try:
            r = requests.get(f"{self.base_url}/docs", timeout=timeout)
            return r.status_code < 500
        except requests.exceptions.ConnectionError:
            return False

    def wait_until_ready(self, max_wait: float = 60.0, poll: float = 1.0) -> bool:
        """Block until the server responds or *max_wait* seconds elapse."""
        deadline = time.time() + max_wait
        while time.time() < deadline:
            if self.is_alive():
                return True
            time.sleep(poll)
        return False

    # ── TTS ──────────────────────────────────────────────────────────────────────

    def speak(
        self,
        text: str,
        output_path: str = "narration.wav",
        fmt: str = DEFAULT_FORMAT,
        temperature: float = 0.7,
        top_p: float = 0.8,
        repetition_penalty: float = 1.1,
        max_new_tokens: int = 1024,
        chunk_length: int = 300,
        seed: Optional[int] = None,
        reference_audio: Optional[bytes] = None,
        reference_text: Optional[str] = None,
    ) -> Path:
        """
        Synthesise *text* and save the result to *output_path*.

        Parameters
        ----------
        text             : Text to synthesise.
        output_path      : Where to write the generated audio file.
        fmt              : Audio format – ``"wav"``, ``"mp3"``, or ``"flac"``.
        temperature      : Sampling temperature (lower = more stable voice).
        top_p            : Nucleus sampling probability.
        repetition_penalty : Penalises repeated tokens (keeps narration flowing).
        max_new_tokens   : Maximum codec tokens to generate.
        chunk_length     : Chunk length for streaming synthesis.
        seed             : Fixed seed for deterministic output (``None`` = random).
        reference_audio  : Raw bytes of a reference WAV for zero-shot voice cloning.
        reference_text   : Transcript of the reference audio.

        Returns
        -------
        Path
            Absolute path to the saved audio file.
        """
        if not self.is_alive():
            raise RuntimeError(
                "Fish Speech API server is not running. "
                "Start it first with start_server.bat or NarrationClient.launch_server()."
            )

        # Build request payload
        references = []
        if reference_audio is not None:
            references.append(
                {"audio": reference_audio, "text": reference_text or ""}
            )

        payload = {
            "text": text,
            "references": references,
            "reference_id": None,
            "format": fmt,
            "max_new_tokens": max_new_tokens,
            "chunk_length": chunk_length,
            "top_p": top_p,
            "repetition_penalty": repetition_penalty,
            "temperature": temperature,
            "streaming": False,
            "use_memory_cache": "off",
            "seed": seed,
        }

        packed = ormsgpack.packb(payload, option=ormsgpack.OPT_SERIALIZE_NUMPY)
        response = requests.post(
            self.tts_url,
            params={"format": "msgpack"},
            data=packed,
            headers=self._headers,
            timeout=120,
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"Fish Speech API returned {response.status_code}: {response.text}"
            )

        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(response.content)
        print(f"[NarrationClient] Saved {len(response.content):,} bytes → {out}")
        return out

    # ── server lifecycle ─────────────────────────────────────────────────────────

    @classmethod
    def launch_server(
        cls,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        device: str = "cuda",
        half: bool = True,
    ) -> subprocess.Popen:
        """
        Launch the Fish Speech API server as a background process.

        Returns the ``subprocess.Popen`` handle so the caller can manage its
        lifecycle (e.g. call ``.terminate()`` on shutdown).
        """
        python = cls._conda_python()
        api_script = str(_FISH_DIR / "tools" / "api_server.py")
        llama_ckpt = str(_CHECKPOINTS / "model.pth")
        decoder_ckpt = str(_CHECKPOINTS / "firefly-gan-vq-fsq-8x1024-21hz-generator.pth")

        cmd = [
            python,
            api_script,
            "--listen", f"{host}:{port}",
            "--llama-checkpoint-path", llama_ckpt,
            "--decoder-checkpoint-path", decoder_ckpt,
            "--device", device,
        ]
        if half:
            cmd.append("--half")

        print(f"[NarrationClient] Launching Fish Speech server:\n  {' '.join(cmd)}")
        proc = subprocess.Popen(
            cmd,
            cwd=str(_FISH_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        return proc

    @staticmethod
    def _conda_python() -> str:
        """Return path to python in the fish-speech conda environment."""
        conda_root = Path(
            os.environ.get("CONDA_PREFIX_1", sys.executable).split("envs")[0]
        )
        candidates = [
            conda_root / "envs" / "fish-speech" / "python.exe",
            Path(sys.executable).parent.parent / "envs" / "fish-speech" / "python.exe",
        ]
        for c in candidates:
            if c.exists():
                return str(c)
        # Fall back to whatever python is on PATH inside the env
        return "python"
