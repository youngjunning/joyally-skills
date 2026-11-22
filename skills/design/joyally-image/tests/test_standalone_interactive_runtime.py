from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
ENTRY = ROOT / "scripts/joyally-diagram.mjs"
EXAMPLE = ROOT / "examples/interactive-minimal.workflow.json"


class ResourceReferences(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag in {"script", "img", "iframe", "source", "video", "audio"}:
            if source := attributes.get("src"):
                self.references.append((tag, source))
        if tag == "link" and (href := attributes.get("href")):
            self.references.append((tag, href))
        if tag == "object" and (data := attributes.get("data")):
            self.references.append((tag, data))


class StandaloneInteractiveRuntimeTest(unittest.TestCase):
    def run_cli(self, *args: object) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            ["node", str(ENTRY), *map(str, args)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=45,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        return result

    def test_runtime_resources_are_available_without_companion_skills(self) -> None:
        result = self.run_cli("doctor")
        self.assertIn("Joyally Image diagrams are ready.", result.stdout)

    def test_example_validates_and_delivers_self_contained_html(self) -> None:
        validated = json.loads(
            self.run_cli("validate", "workflow", EXAMPLE, "--json").stdout
        )
        self.assertTrue(validated["ok"])

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "diagram.html"
            delivered = json.loads(
                self.run_cli(
                    "deliver", "workflow", EXAMPLE, output, "--json"
                ).stdout
            )
            self.assertTrue(delivered["ok"])

            checked = json.loads(self.run_cli("check", output, "--json").stdout)
            self.assertTrue(checked["ok"])

            html = output.read_text("utf-8")
            parser = ResourceReferences()
            parser.feed(html)
            self.assertEqual(parser.references, [])
            self.assertIsNone(
                re.search(r"url\(\s*['\"]?https?://", html, re.IGNORECASE)
            )
            self.assertIn('<meta name="generator" content="Joyally Image">', html)
            self.assertIn("<svg", html)

    def test_public_contract_and_provenance_are_self_contained(self) -> None:
        public_files = [
            ROOT / "SKILL.md",
            ROOT / "README.md",
            ROOT / "README.zh-CN.md",
            ROOT / "references/interactive-diagram.md",
            ROOT / "references/knowledge-map.md",
        ]
        for path in public_files:
            self.assertNotIn("Archify", path.read_text("utf-8"), path.as_posix())

        runtime = ROOT / "runtime/diagram"
        provenance = json.loads((runtime / "UPSTREAM.json").read_text("utf-8"))
        token_reference = (
            provenance["localModifications"]["assets/template.html"]
            .split("Source: ", 1)[1]
            .split(" diagram.", 1)[0]
        )
        resolved_token_reference = (runtime / token_reference).resolve()
        self.assertTrue(resolved_token_reference.is_relative_to(ROOT))
        self.assertTrue(resolved_token_reference.is_file())
        self.assertIn(
            "Joyally Image branding",
            provenance["localModifications"]["presentation"],
        )
        for name in [
            "LICENSE",
            "LICENSE-MIT",
            "NOTICE",
            "THIRD_PARTY_NOTICES.md",
            "UPSTREAM.json",
        ]:
            self.assertTrue((runtime / name).is_file(), name)
        for name in ["NOTICE", "THIRD_PARTY_NOTICES.md", "UPSTREAM.json"]:
            self.assertIn("archify", (runtime / name).read_text("utf-8").lower(), name)


if __name__ == "__main__":
    unittest.main()
