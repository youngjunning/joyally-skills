from pathlib import Path
import unittest


SKILL_TEXT = (Path(__file__).resolve().parents[1] / "SKILL.md").read_text()


class StyleSovereigntyTests(unittest.TestCase):
    def test_capability_provenance_does_not_select_visual_style(self):
        self.assertIn("Capability provenance never determines visual style.", SKILL_TEXT)
        self.assertIn("carries over only its functional contract", SKILL_TEXT)
        self.assertIn("Resolve appearance from the Joyally Qingshan Lake default", SKILL_TEXT)
        self.assertIn("never import the source project's palette", SKILL_TEXT)


if __name__ == "__main__":
    unittest.main()
