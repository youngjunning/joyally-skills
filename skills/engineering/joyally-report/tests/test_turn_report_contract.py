from pathlib import Path
import unittest


SKILL_DIR = Path(__file__).resolve().parents[1]
SKILL_TEXT = (SKILL_DIR / "SKILL.md").read_text()
CONTRACT_TEXT = (SKILL_DIR / "references/turn-report.md").read_text()


class TurnReportContractTests(unittest.TestCase):
    def test_distillation_and_status_are_separate_regions(self):
        self.assertIn("four-region contract", SKILL_TEXT)
        self.assertIn("Distillation strip", CONTRACT_TEXT)
        self.assertIn("Status strip", CONTRACT_TEXT)
        self.assertIn(
            "Summary + body + distillation + status: three dividers.",
            CONTRACT_TEXT,
        )
        self.assertIn("蒸馏：无新增。\n\n---\n\n使用技能：", CONTRACT_TEXT)

    def test_status_receipts_keep_the_host_git_format(self):
        self.assertIn("[owner/repository](repository URL)", CONTRACT_TEXT)
        self.assertNotIn("![Git]", CONTRACT_TEXT)
        self.assertIn("one concise, task-specific contribution", CONTRACT_TEXT)
        self.assertNotIn("> Report", CONTRACT_TEXT)


if __name__ == "__main__":
    unittest.main()
