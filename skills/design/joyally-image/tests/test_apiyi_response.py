from __future__ import annotations

import base64
import importlib.util
import json
import io
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from PIL import Image


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts" / "decode_apiyi_response.py"
SPEC = importlib.util.spec_from_file_location("joyally_apiyi_response", SCRIPT)
assert SPEC and SPEC.loader
APIYI_RESPONSE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(APIYI_RESPONSE)


class ApiyiResponseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.output = Path(self.temporary.name) / "candidate.png"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def payload(self, value: dict[str, object]) -> bytes:
        return json.dumps(value, ensure_ascii=False).encode()

    def png_bytes(self) -> bytes:
        buffer = io.BytesIO()
        Image.new("RGB", (2, 2), "navy").save(buffer, format="PNG")
        return buffer.getvalue()

    def test_invalid_key_uses_non_retryable_fallback_signal(self) -> None:
        code, messages = APIYI_RESPONSE.decode_response(
            self.payload({"error": {"code": "invalid_api_key", "message": "bad key"}}),
            self.output,
        )
        self.assertEqual(4, code)
        self.assertEqual(["APIYI_UNAVAILABLE:invalid-key:bad key"], messages)
        self.assertFalse(self.output.exists())

    def test_insufficient_balance_uses_non_retryable_fallback_signal(self) -> None:
        code, messages = APIYI_RESPONSE.decode_response(
            self.payload({"error": {"message": "账户余额不足"}}),
            self.output,
        )
        self.assertEqual(4, code)
        self.assertEqual(
            ["APIYI_UNAVAILABLE:insufficient-balance:账户余额不足"],
            messages,
        )
        self.assertFalse(self.output.exists())

    def test_rate_limit_is_not_mislabeled_as_balance_failure(self) -> None:
        code, messages = APIYI_RESPONSE.decode_response(
            self.payload({"error": {"code": "rate_limit", "message": "too many requests"}}),
            self.output,
        )
        self.assertEqual(2, code)
        self.assertEqual(["API_ERROR:too many requests"], messages)

    def test_success_decodes_without_external_request(self) -> None:
        image_bytes = self.png_bytes()
        code, messages = APIYI_RESPONSE.decode_response(
            self.payload(
                {"data": [{"b64_json": base64.b64encode(image_bytes).decode()}]}
            ),
            self.output,
        )
        self.assertEqual(0, code, messages)
        self.assertEqual(image_bytes, self.output.read_bytes())
        self.assertIn("RESPONSE_FORMAT:b64_json", messages)

    def test_invalid_image_bytes_never_report_success(self) -> None:
        code, messages = APIYI_RESPONSE.decode_response(
            self.payload(
                {"data": [{"b64_json": base64.b64encode(b"not-an-image").decode()}]}
            ),
            self.output,
        )
        self.assertEqual(3, code)
        self.assertIn("not a valid image", messages[0])
        self.assertFalse(self.output.exists())

    @mock.patch.object(APIYI_RESPONSE, "urlopen")
    def test_non_https_url_is_rejected_before_download(self, urlopen: mock.Mock) -> None:
        code, messages = APIYI_RESPONSE.decode_response(
            self.payload({"data": [{"url": "http://example.com/image.png"}]}),
            self.output,
        )
        self.assertEqual(3, code)
        self.assertEqual(["ERROR: image URL must use HTTPS"], messages)
        urlopen.assert_not_called()

    @mock.patch.object(APIYI_RESPONSE, "urlopen")
    def test_https_download_is_bounded_and_validated(self, urlopen: mock.Mock) -> None:
        image_bytes = self.png_bytes()

        class Response(io.BytesIO):
            headers = {"Content-Length": str(len(image_bytes))}

            def geturl(self) -> str:
                return "https://cdn.example.com/image.png"

            def __enter__(self) -> "Response":
                return self

            def __exit__(self, *_args: object) -> None:
                self.close()

        urlopen.return_value = Response(image_bytes)
        code, messages = APIYI_RESPONSE.decode_response(
            self.payload({"data": [{"url": "https://cdn.example.com/image.png"}]}),
            self.output,
        )
        self.assertEqual(0, code, messages)
        self.assertEqual(image_bytes, self.output.read_bytes())
        self.assertIn("RESPONSE_FORMAT:url", messages)
        self.assertEqual(
            APIYI_RESPONSE.DOWNLOAD_TIMEOUT_SECONDS,
            urlopen.call_args.kwargs["timeout"],
        )

    def test_success_never_overwrites_existing_candidate(self) -> None:
        self.output.write_bytes(b"accepted-candidate")
        code, messages = APIYI_RESPONSE.decode_response(
            self.payload(
                {"data": [{"b64_json": base64.b64encode(b"replacement").decode()}]}
            ),
            self.output,
        )
        self.assertEqual(3, code)
        self.assertIn("output already exists", messages[0])
        self.assertEqual(b"accepted-candidate", self.output.read_bytes())


if __name__ == "__main__":
    unittest.main()
