from pathlib import Path
import unittest


SKILL_DIR = Path(__file__).resolve().parents[1]
SKILL_TEXT = (SKILL_DIR / "SKILL.md").read_text()
CONTRACT_TEXT = (SKILL_DIR / "references/turn-report.md").read_text()
REPORT_TYPES_TEXT = (SKILL_DIR / "references/report-types.md").read_text()


class TurnReportContractTests(unittest.TestCase):
    def test_final_answer_uses_a_decision_to_handoff_gradient(self):
        self.assertIn("before writing the final answer", SKILL_TEXT)
        self.assertIn("decision surface", SKILL_TEXT)
        self.assertIn("evidence surface", SKILL_TEXT)
        self.assertIn("handoff strip", SKILL_TEXT)
        self.assertIn("Decision only: no divider.", CONTRACT_TEXT)
        self.assertIn("Decision + evidence + handoff: two dividers.", CONTRACT_TEXT)
        self.assertIn("claim → evidence → boundary", CONTRACT_TEXT)
        self.assertIn("![Git](https://api.iconify.design/logos/git-icon.svg?width=16&height=16) [owner/repository](repository URL)", CONTRACT_TEXT)
        self.assertNotIn("⎇", CONTRACT_TEXT)
        self.assertIn("browsable remote homepage", CONTRACT_TEXT)
        self.assertIn("one concise, task-specific contribution", CONTRACT_TEXT)
        self.assertIn("joyally-report（整理交付结论与证据）", CONTRACT_TEXT)
        self.assertNotIn("Skills：joyally-report、joy-git。", CONTRACT_TEXT)
        self.assertIn("do not copy those labels into the final answer", REPORT_TYPES_TEXT)
        self.assertNotIn("## 摘要", CONTRACT_TEXT)
        self.assertNotIn("## 收尾", CONTRACT_TEXT)


if __name__ == "__main__":
    unittest.main()
