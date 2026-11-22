from pathlib import Path
import unittest


SKILL_DIR = Path(__file__).resolve().parents[1]
SKILL_TEXT = (SKILL_DIR / "SKILL.md").read_text()
CONTRACT_TEXT = (SKILL_DIR / "references/turn-report.md").read_text()
REPORT_TYPES_TEXT = (SKILL_DIR / "references/report-types.md").read_text()


class TurnReportContractTests(unittest.TestCase):
    def test_final_answer_separates_distillation_from_status(self):
        self.assertIn("before writing the final answer", SKILL_TEXT)
        self.assertIn("decision surface", SKILL_TEXT)
        self.assertIn("evidence surface", SKILL_TEXT)
        self.assertIn("distillation strip", SKILL_TEXT)
        self.assertIn("status strip", SKILL_TEXT)
        self.assertIn("Summary only: no divider.", CONTRACT_TEXT)
        self.assertIn("Summary + body + distillation + status: three dividers.", CONTRACT_TEXT)
        self.assertIn("claim → evidence → boundary", CONTRACT_TEXT)
        self.assertIn("[owner/repository](repository URL)", CONTRACT_TEXT)
        self.assertNotIn("⎇", CONTRACT_TEXT)
        self.assertIn("browsable remote homepage", CONTRACT_TEXT)
        self.assertIn("one concise, task-specific contribution", CONTRACT_TEXT)
        self.assertIn("蒸馏：无新增。\n\n---\n\n使用技能：", CONTRACT_TEXT)
        self.assertIn("do not copy those labels into the final answer", REPORT_TYPES_TEXT)
        self.assertNotIn("## 摘要", CONTRACT_TEXT)
        self.assertNotIn("## 收尾", CONTRACT_TEXT)


if __name__ == "__main__":
    unittest.main()
