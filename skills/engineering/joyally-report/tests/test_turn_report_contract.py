from pathlib import Path
import unittest


SKILL_DIR = Path(__file__).resolve().parents[1]
SKILL_TEXT = (SKILL_DIR / "SKILL.md").read_text()
CONTRACT_TEXT = (SKILL_DIR / "references/turn-report.md").read_text()


class TurnReportContractTests(unittest.TestCase):
    def test_dividers_are_the_only_region_markers(self):
        self.assertIn("without a summary heading", SKILL_TEXT)
        self.assertIn("without a closing heading", SKILL_TEXT)
        self.assertIn("The two dividers are the only region markers", CONTRACT_TEXT)
        self.assertNotIn("## 摘要", CONTRACT_TEXT)
        self.assertNotIn("## 收尾", CONTRACT_TEXT)


if __name__ == "__main__":
    unittest.main()
