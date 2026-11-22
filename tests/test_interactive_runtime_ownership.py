from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
IMAGE = ROOT / "skills/design/joyally-image"
DESIGN = ROOT / "skills/design/joyally-design"
EXAMPLE = IMAGE / "examples/interactive-minimal.workflow.json"


class InteractiveRuntimeOwnershipTest(unittest.TestCase):
    def run_command(self, *args: object) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            list(map(str, args)),
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=45,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        return result

    def test_runtime_belongs_to_image_and_design_only_forwards(self) -> None:
        self.assertTrue((IMAGE / "runtime/diagram/bin/archify.mjs").is_file())
        self.assertTrue((IMAGE / "scripts/joyally-diagram.mjs").is_file())
        self.assertTrue((IMAGE / "examples/interactive-minimal.workflow.json").is_file())
        self.assertFalse((DESIGN / "runtime/diagram").exists())
        self.assertTrue((DESIGN / "scripts/joyally-diagram.mjs").is_file())
        self.assertTrue((DESIGN / "scripts/joyally-archify.mjs").is_file())
        engine = (DESIGN / "scripts/design-engine.mjs").read_text("utf-8")
        self.assertIn("diagram: 'joyally-diagram.mjs'", engine)
        self.assertNotIn("Archify 后端", (DESIGN / "SKILL.md").read_text("utf-8"))

    def test_old_design_engine_command_forwards_to_image(self) -> None:
        result = self.run_command(
            "node",
            DESIGN / "scripts/design-engine.mjs",
            "diagram",
            "validate",
            "workflow",
            EXAMPLE,
            "--json",
        )
        self.assertTrue(json.loads(result.stdout)["ok"])
        self.assertIn("deprecated", result.stderr.lower())
        self.assertIn("joyally-image", result.stderr)

    def test_old_design_wrapper_filename_forwards_to_image(self) -> None:
        result = self.run_command(
            "node",
            DESIGN / "scripts/joyally-archify.mjs",
            "validate",
            "workflow",
            EXAMPLE,
            "--json",
        )
        self.assertTrue(json.loads(result.stdout)["ok"])
        self.assertIn("deprecated", result.stderr.lower())

    def test_repository_visual_contract_matches_bundled_snapshot(self) -> None:
        snapshot = IMAGE / "runtime/diagram/assets/joyally-diagram.tokens.json"
        self.assertTrue(snapshot.is_file())
        result = self.run_command(
            "python3", DESIGN / "scripts/validate-diagram-theme.py"
        )
        self.assertIn("bundled snapshot", result.stdout)


if __name__ == "__main__":
    unittest.main()
