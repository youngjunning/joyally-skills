from pathlib import Path
import json
import unittest


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT.parent / "joyally-design"


class InteractiveRuntimeOwnershipTest(unittest.TestCase):
    def test_runtime_and_public_entrypoint_belong_to_joyally_image(self):
        self.assertTrue((ROOT / "runtime/diagram/bin/archify.mjs").is_file())
        self.assertTrue((ROOT / "scripts/joyally-diagram.mjs").is_file())
        self.assertTrue((ROOT / "examples/interactive-minimal.workflow.json").is_file())
        self.assertFalse((DESIGN / "runtime/diagram").exists())
        self.assertFalse((DESIGN / "scripts/joyally-diagram.mjs").exists())
        self.assertFalse((DESIGN / "scripts/joyally-archify.mjs").exists())

    def test_reader_facing_image_docs_hide_upstream_implementation_name(self):
        public_files = [
            ROOT / "SKILL.md",
            ROOT / "README.md",
            ROOT / "README.zh-CN.md",
            ROOT / "references/interactive-diagram.md",
            ROOT / "references/knowledge-map.md",
        ]
        for path in public_files:
            self.assertNotIn("Archify", path.read_text("utf-8"), path.as_posix())

    def test_design_no_longer_exposes_a_diagram_backend(self):
        engine = (DESIGN / "scripts/design-engine.mjs").read_text("utf-8")
        self.assertNotIn("diagram: 'joyally-diagram.mjs'", engine)
        self.assertNotIn("Archify 后端", (DESIGN / "SKILL.md").read_text("utf-8"))

    def test_provenance_points_to_the_visual_contract_and_keeps_attribution(self):
        runtime = ROOT / "runtime/diagram"
        provenance = json.loads((runtime / "UPSTREAM.json").read_text("utf-8"))
        token_reference = provenance["localModifications"]["assets/template.html"].split("Source: ", 1)[1].split(" diagram.", 1)[0]
        self.assertTrue((runtime / token_reference).resolve().is_file())
        self.assertIn("Joyally Image branding", provenance["localModifications"]["presentation"])
        for name in ["LICENSE", "LICENSE-MIT", "NOTICE", "THIRD_PARTY_NOTICES.md", "UPSTREAM.json"]:
            self.assertTrue((runtime / name).is_file(), name)
        for name in ["NOTICE", "THIRD_PARTY_NOTICES.md", "UPSTREAM.json"]:
            self.assertIn("archify", (runtime / name).read_text("utf-8").lower(), name)


if __name__ == "__main__":
    unittest.main()
