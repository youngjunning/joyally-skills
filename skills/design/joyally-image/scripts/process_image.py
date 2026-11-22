#!/usr/bin/env python3
"""Deterministic local inspection, conversion, resize, and compression."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from PIL import Image, ImageColor, ImageOps


FORMATS = {
    ".jpeg": "JPEG",
    ".jpg": "JPEG",
    ".png": "PNG",
    ".webp": "WEBP",
}
RESAMPLING = {
    "nearest": Image.Resampling.NEAREST,
    "lanczos": Image.Resampling.LANCZOS,
}


class ProcessingError(Exception):
    """A deterministic processing request cannot be completed safely."""


def _format_for(path: Path) -> str:
    try:
        return FORMATS[path.suffix.lower()]
    except KeyError as error:
        raise ProcessingError(f"unsupported output extension: {path.suffix or '<none>'}") from error


def _has_transparency(image: Image.Image) -> bool:
    if "A" in image.getbands():
        return image.getchannel("A").getextrema()[0] < 255
    if image.mode == "P" and "transparency" in image.info:
        return True
    return False


def inspect_image(path: Path) -> dict[str, object]:
    with Image.open(path) as image:
        image.load()
        alpha = image.convert("RGBA").getchannel("A")
        transparent = sum(alpha.histogram()[:255])
        pixels = image.width * image.height
        try:
            exif_count = len(image.getexif())
        except Exception:
            exif_count = 0
        return {
            "path": str(path),
            "format": image.format,
            "width": image.width,
            "height": image.height,
            "mode": image.mode,
            "frames": getattr(image, "n_frames", 1),
            "file_size_bytes": path.stat().st_size,
            "has_alpha": _has_transparency(image),
            "transparent_pixel_ratio": round(transparent / pixels, 6) if pixels else 0,
            "alpha_bbox": alpha.getbbox(),
            "exif_tag_count": exif_count,
            "has_icc_profile": bool(image.info.get("icc_profile")),
            "metadata_keys": sorted(str(key) for key in image.info),
        }


def _metadata(image: Image.Image, strip: bool) -> dict[str, object]:
    if strip:
        return {}
    metadata: dict[str, object] = {}
    icc = image.info.get("icc_profile")
    if icc:
        metadata["icc_profile"] = icc
    try:
        exif = image.getexif()
        if exif:
            exif[274] = 1  # pixels are normalized through exif_transpose
            metadata["exif"] = exif.tobytes()
    except Exception:
        pass
    return metadata


def _flatten(image: Image.Image, background: str | None) -> Image.Image:
    if not _has_transparency(image):
        return image.convert("RGB")
    if not background:
        raise ProcessingError("JPEG cannot preserve alpha; pass --background explicitly")
    color = ImageColor.getcolor(background, "RGB")
    rgba = image.convert("RGBA")
    canvas = Image.new("RGBA", rgba.size, (*color, 255))
    return Image.alpha_composite(canvas, rgba).convert("RGB")


def _prepare_for_format(
    image: Image.Image,
    output_format: str,
    background: str | None,
) -> Image.Image:
    if output_format == "JPEG":
        return _flatten(image, background)
    if image.mode == "CMYK":
        return image.convert("RGB")
    return image


def _save_atomic(
    image: Image.Image,
    source: Path,
    output: Path,
    *,
    metadata: dict[str, object],
    quality: int,
    background: str | None,
    force: bool,
) -> dict[str, object]:
    source_resolved = source.resolve()
    output_resolved = output.resolve()
    if source_resolved == output_resolved:
        raise ProcessingError("input and output must be different files")
    if output.exists() and not force:
        raise ProcessingError(f"output already exists: {output}")

    output_format = _format_for(output)
    prepared = _prepare_for_format(image, output_format, background)
    expected_size = prepared.size
    save_options = metadata.copy()
    if output_format == "WEBP":
        save_options.update(quality=quality, method=6)
    elif output_format == "JPEG":
        save_options.update(quality=quality, optimize=True)
    elif output_format == "PNG":
        save_options.update(optimize=True, compress_level=9)

    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{output.stem}.",
        suffix=output.suffix,
        dir=output.parent,
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        prepared.save(temporary, format=output_format, **save_options)
        with Image.open(temporary) as candidate:
            candidate.verify()
        with Image.open(temporary) as candidate:
            candidate.load()
            if candidate.format != output_format:
                raise ProcessingError(
                    f"output format mismatch: expected {output_format}, got {candidate.format}"
                )
            if candidate.size != expected_size:
                raise ProcessingError(
                    f"output size mismatch: expected {expected_size}, got {candidate.size}"
                )
        os.replace(temporary, output)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    return inspect_image(output)


def _resize(
    image: Image.Image,
    *,
    width: int | None,
    height: int | None,
    fit: str,
    resample: str,
) -> Image.Image:
    if not width and not height:
        raise ProcessingError("resize requires --width, --height, or both")
    if (width is not None and width <= 0) or (height is not None and height <= 0):
        raise ProcessingError("resize dimensions must be positive")

    filter_ = RESAMPLING[resample]
    if width is None:
        width = max(1, round(image.width * height / image.height))
    if height is None:
        height = max(1, round(image.height * width / image.width))
    size = (width, height)
    if fit == "contain":
        return ImageOps.contain(image, size, method=filter_)
    if fit == "cover":
        return ImageOps.fit(image, size, method=filter_)
    return image.resize(size, resample=filter_)


def _common_output_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--quality", type=int, default=80)
    parser.add_argument("--strip-metadata", action="store_true")
    parser.add_argument("--background", help="explicit JPEG matte, for example '#ffffff'")
    parser.add_argument("--force", action="store_true", help="replace an existing output, never the input")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser("inspect")
    inspect_parser.add_argument("input", type=Path)

    for command in ("convert", "compress"):
        _common_output_arguments(subparsers.add_parser(command))

    resize_parser = subparsers.add_parser("resize")
    _common_output_arguments(resize_parser)
    resize_parser.add_argument("--width", type=int)
    resize_parser.add_argument("--height", type=int)
    resize_parser.add_argument("--fit", choices=("contain", "cover", "stretch"), default="contain")
    resize_parser.add_argument("--resample", choices=tuple(RESAMPLING), default="lanczos")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if not args.input.is_file():
            raise ProcessingError(f"input does not exist: {args.input}")
        if args.command == "inspect":
            report = inspect_image(args.input)
        else:
            if not 1 <= args.quality <= 100:
                raise ProcessingError("quality must be between 1 and 100")
            with Image.open(args.input) as source_image:
                source_image.load()
                if getattr(source_image, "n_frames", 1) != 1:
                    raise ProcessingError(
                        "animated or multi-frame input requires a type-specific workflow"
                    )
                metadata = _metadata(source_image, args.strip_metadata)
                image = ImageOps.exif_transpose(source_image)
                if args.command == "resize":
                    image = _resize(
                        image,
                        width=args.width,
                        height=args.height,
                        fit=args.fit,
                        resample=args.resample,
                    )
                report = _save_atomic(
                    image,
                    args.input,
                    args.output,
                    metadata=metadata,
                    quality=args.quality,
                    background=args.background,
                    force=args.force,
                )
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ProcessingError, ValueError) as error:
        print(f"ERROR: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
