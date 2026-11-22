from __future__ import annotations

from hashlib import sha256
import importlib.util
import io
import json
import os
from pathlib import Path
import socket
import tempfile
import unittest
from unittest import mock

from PIL import Image, PngImagePlugin


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts" / "process_image.py"
SPEC = importlib.util.spec_from_file_location("joyally_process_image", SCRIPT)
assert SPEC and SPEC.loader
PROCESS_IMAGE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROCESS_IMAGE)


class LocalProcessingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.source = self.root / "source.png"
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("fixture", "local-only")
        Image.new("RGBA", (64, 32), (40, 120, 180, 128)).save(
            self.source,
            pnginfo=metadata,
        )
        self.source_hash = sha256(self.source.read_bytes()).hexdigest()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_main(self, argv: list[str]) -> tuple[int, dict[str, object] | str]:
        output = io.StringIO()
        with mock.patch("sys.stdout", output):
            code = PROCESS_IMAGE.main(argv)
        rendered = output.getvalue().strip()
        return code, json.loads(rendered) if code == 0 else rendered

    @mock.patch.object(
        socket.socket,
        "connect",
        side_effect=AssertionError("local processing attempted network access"),
    )
    def test_conversion_needs_no_key_or_network(self, _connect: mock.Mock) -> None:
        destination = self.root / "output.webp"
        with mock.patch.dict(os.environ, {}, clear=True):
            code, report = self.run_main(
                ["convert", str(self.source), str(destination), "--quality", "80"]
            )

        self.assertEqual(0, code, report)
        self.assertEqual("WEBP", report["format"])
        self.assertEqual([64, 32], [report["width"], report["height"]])
        self.assertTrue(report["has_alpha"])
        self.assertEqual(self.source_hash, sha256(self.source.read_bytes()).hexdigest())
        _connect.assert_not_called()

    @mock.patch.object(
        socket.socket,
        "connect",
        side_effect=AssertionError("resize attempted network access"),
    )
    def test_contain_resize_preserves_source_and_aspect_ratio(self, _connect: mock.Mock) -> None:
        destination = self.root / "small.png"
        code, report = self.run_main(
            [
                "resize",
                str(self.source),
                str(destination),
                "--width",
                "32",
                "--height",
                "32",
                "--fit",
                "contain",
            ]
        )

        self.assertEqual(0, code, report)
        self.assertEqual([32, 16], [report["width"], report["height"]])
        self.assertEqual(self.source_hash, sha256(self.source.read_bytes()).hexdigest())
        _connect.assert_not_called()

    def test_inspection_reports_metadata_and_transparency(self) -> None:
        code, report = self.run_main(["inspect", str(self.source)])
        self.assertEqual(0, code, report)
        self.assertEqual("PNG", report["format"])
        self.assertTrue(report["has_alpha"])
        self.assertEqual(1.0, report["transparent_pixel_ratio"])
        self.assertIn("fixture", report["metadata_keys"])

    def test_input_cannot_be_overwritten_even_with_force(self) -> None:
        code, error = self.run_main(
            ["convert", str(self.source), str(self.source), "--force"]
        )
        self.assertEqual(2, code)
        self.assertIn("input and output must be different", error)
        self.assertEqual(self.source_hash, sha256(self.source.read_bytes()).hexdigest())

    def test_transparent_input_requires_explicit_jpeg_background(self) -> None:
        destination = self.root / "output.jpg"
        code, error = self.run_main(["convert", str(self.source), str(destination)])
        self.assertEqual(2, code)
        self.assertIn("JPEG cannot preserve alpha", error)
        self.assertFalse(destination.exists())
        self.assertEqual(self.source_hash, sha256(self.source.read_bytes()).hexdigest())

    def test_existing_output_is_preserved_after_failure(self) -> None:
        destination = self.root / "existing.png"
        destination.write_bytes(b"existing-output")
        before = destination.read_bytes()
        code, error = self.run_main(["convert", str(self.source), str(destination)])
        self.assertEqual(2, code)
        self.assertIn("output already exists", error)
        self.assertEqual(before, destination.read_bytes())

    def test_animated_webp_requires_type_specific_workflow(self) -> None:
        animated = self.root / "animated.webp"
        destination = self.root / "flattened.png"
        frames = [
            Image.new("RGB", (8, 8), "red"),
            Image.new("RGB", (8, 8), "blue"),
        ]
        try:
            frames[0].save(
                animated,
                format="WEBP",
                save_all=True,
                append_images=frames[1:],
                duration=100,
                loop=0,
            )
        except OSError as error:
            self.skipTest(f"Pillow build cannot write animated WebP: {error}")

        code, message = self.run_main(["convert", str(animated), str(destination)])
        self.assertEqual(2, code)
        self.assertIn("animated or multi-frame input", message)
        self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
