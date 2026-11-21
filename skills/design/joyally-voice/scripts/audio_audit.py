#!/usr/bin/env python3
"""Read-only audio metadata and loudness audit using ffprobe and ffmpeg."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, check=False)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def probe(path: Path) -> dict:
    result = run([
        "ffprobe", "-v", "error", "-show_streams", "-show_format",
        "-of", "json", str(path),
    ])
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "ffprobe failed")
    payload = json.loads(result.stdout)
    audio = next((item for item in payload.get("streams", []) if item.get("codec_type") == "audio"), {})
    fmt = payload.get("format", {})
    return {
        "codec": audio.get("codec_name"),
        "sample_rate_hz": int(audio["sample_rate"]) if audio.get("sample_rate") else None,
        "channels": audio.get("channels"),
        "channel_layout": audio.get("channel_layout"),
        "duration_seconds": float(fmt["duration"]) if fmt.get("duration") else None,
        "bit_rate": int(fmt["bit_rate"]) if fmt.get("bit_rate") else None,
    }


def loudness(path: Path) -> dict:
    result = run([
        "ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
        "-f", "null", "-",
    ])
    matches = re.findall(r"\{\s*\"input_i\".*?\}", result.stderr, re.S)
    if not matches:
        raise RuntimeError("ffmpeg did not return loudness measurements")
    values = json.loads(matches[-1])
    return {
        "integrated_lufs": float(values["input_i"]),
        "true_peak_dbtp": float(values["input_tp"]),
        "loudness_range_lu": float(values["input_lra"]),
        "threshold_lufs": float(values["input_thresh"]),
    }


def inspect(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(path)
    return {
        "path": str(path.resolve()),
        "bytes": path.stat().st_size,
        "sha256": digest(path),
        **probe(path),
        **loudness(path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()
    missing = [name for name in ("ffprobe", "ffmpeg") if not shutil.which(name)]
    if missing:
        parser.exit(2, f"Missing required command(s): {', '.join(missing)}\n")
    output, errors = [], []
    for path in args.files:
        try:
            output.append(inspect(path))
        except (FileNotFoundError, RuntimeError, ValueError, json.JSONDecodeError) as error:
            errors.append({"path": str(path), "error": str(error)})
    print(json.dumps({"audio": output, "errors": errors}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
