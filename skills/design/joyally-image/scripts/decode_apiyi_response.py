#!/usr/bin/env python3
"""Decode one streamed APIYI image response and classify availability errors."""

from __future__ import annotations

import base64
import binascii
import json
import os
from pathlib import Path
import sys
import tempfile
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from PIL import Image


AUTH_MARKERS = (
    "invalid_api_key",
    "incorrect api key",
    "invalid authentication",
    "unauthorized",
)
BILLING_MARKERS = (
    "insufficient_balance",
    "insufficient balance",
    "insufficient_quota",
    "billing hard limit",
    "credit balance",
    "余额不足",
)
MAX_IMAGE_BYTES = 64 * 1024 * 1024
DOWNLOAD_TIMEOUT_SECONDS = 60


def classify_error(error: object) -> tuple[int, str]:
    if isinstance(error, dict):
        message = str(error.get("message", error))
        code = str(error.get("code", ""))
    else:
        message = str(error)
        code = ""
    marker = f"{code} {message}".lower()
    if any(value in marker for value in AUTH_MARKERS):
        return 4, f"APIYI_UNAVAILABLE:invalid-key:{message}"
    if any(value in marker for value in BILLING_MARKERS):
        return 4, f"APIYI_UNAVAILABLE:insufficient-balance:{message}"
    return 2, f"API_ERROR:{message}"


def decode_response(raw: bytes, output_path: Path) -> tuple[int, list[str]]:
    if not raw.strip():
        return 1, ["ERROR: empty response (timeout)"]
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as error:
        return 3, [f"ERROR: invalid JSON response: {error}"]
    if not isinstance(data, dict):
        return 3, [f"ERROR: response root must be an object, got {type(data).__name__}"]
    if "error" in data:
        code, message = classify_error(data["error"])
        return code, [message]
    if not data.get("data"):
        return 2, ["SOFT_REJECT: empty data array (model declined silently)"]

    item = data["data"][0]
    if not isinstance(item, dict):
        return 3, [f"UNKNOWN_FORMAT:{type(item).__name__}"]
    if output_path.exists():
        return 3, [f"ERROR: output already exists: {output_path}"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{output_path.stem}.",
        suffix=output_path.suffix,
        dir=output_path.parent,
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    response_format = ""
    try:
        if item.get("b64_json"):
            encoded = item["b64_json"]
            if not isinstance(encoded, str):
                return 3, ["ERROR: b64_json must be a string"]
            if "," in encoded:
                encoded = encoded.split(",", 1)[1]
            try:
                temporary.write_bytes(base64.b64decode(encoded, validate=True))
            except (binascii.Error, ValueError) as error:
                return 3, [f"ERROR: invalid base64 image: {error}"]
            response_format = "b64_json"
        elif item.get("url"):
            image_url = item["url"]
            if not isinstance(image_url, str) or urlparse(image_url).scheme != "https":
                return 3, ["ERROR: image URL must use HTTPS"]
            try:
                request = Request(image_url, headers={"User-Agent": "joyally-image/1"})
                with urlopen(request, timeout=DOWNLOAD_TIMEOUT_SECONDS) as response:
                    if urlparse(response.geturl()).scheme != "https":
                        return 3, ["ERROR: redirected image URL must use HTTPS"]
                    declared = response.headers.get("Content-Length")
                    if declared and int(declared) > MAX_IMAGE_BYTES:
                        return 3, ["ERROR: image download exceeds 64 MiB limit"]
                    total = 0
                    with temporary.open("wb") as destination:
                        while chunk := response.read(1024 * 1024):
                            total += len(chunk)
                            if total > MAX_IMAGE_BYTES:
                                return 3, ["ERROR: image download exceeds 64 MiB limit"]
                            destination.write(chunk)
            except (OSError, URLError, ValueError) as error:
                return 3, [f"ERROR: image download failed: {error}"]
            response_format = "url"
        else:
            return 3, [f"UNKNOWN_FORMAT:{sorted(item)}"]
        if temporary.stat().st_size == 0:
            return 3, ["ERROR: decoded image is empty"]
        try:
            with Image.open(temporary) as candidate:
                candidate.verify()
            with Image.open(temporary) as candidate:
                candidate.load()
                if not candidate.format or candidate.width <= 0 or candidate.height <= 0:
                    return 3, ["ERROR: decoded image has invalid format or dimensions"]
        except OSError as error:
            return 3, [f"ERROR: decoded payload is not a valid image: {error}"]
        os.replace(temporary, output_path)
    finally:
        temporary.unlink(missing_ok=True)
    return 0, [
        f"SAVED:{output_path.stat().st_size}",
        f"RESPONSE_FORMAT:{response_format}",
    ]


def main() -> int:
    output = os.environ.get("OUTPUT_PATH")
    if not output:
        print("ERROR: OUTPUT_PATH is required")
        return 3
    code, messages = decode_response(sys.stdin.buffer.read(), Path(output))
    print("\n".join(messages))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
