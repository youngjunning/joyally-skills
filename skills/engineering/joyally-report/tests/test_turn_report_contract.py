from pathlib import Path
import unittest


SKILL_DIR = Path(__file__).resolve().parents[1]
SKILL_TEXT = (SKILL_DIR / "SKILL.md").read_text()
CONTRACT_TEXT = (SKILL_DIR / "references/turn-report.md").read_text()
REPORT_TYPES_TEXT = (SKILL_DIR / "references/report-types.md").read_text()


class TurnReportContractTests(unittest.TestCase):
    def test_final_answer_combines_distillation_and_skills_but_not_git(self):
        self.assertIn("before writing the final answer", SKILL_TEXT)
        self.assertIn("decision surface", SKILL_TEXT)
        self.assertIn("evidence surface", SKILL_TEXT)
        self.assertIn("combined closing strip", SKILL_TEXT)
        self.assertIn("Git strip", SKILL_TEXT)
        self.assertIn("Summary only: no divider.", CONTRACT_TEXT)
        self.assertIn("Summary + body + combined closing + Git: three dividers.", CONTRACT_TEXT)
        self.assertIn("Do not insert a divider between distillation and Skills", CONTRACT_TEXT)
        self.assertIn("claim → evidence → boundary", CONTRACT_TEXT)
        self.assertIn("[owner/repository](repository URL)", CONTRACT_TEXT)
        self.assertIn("browsable remote homepage", CONTRACT_TEXT)
        self.assertIn("one concise, task-specific contribution", CONTRACT_TEXT)
        self.assertIn("**蒸馏：** 无新增。\n\n**技能：**", CONTRACT_TEXT)
        self.assertNotIn("**蒸馏：** 无新增。\n\n---\n\n**技能：**", CONTRACT_TEXT)
        self.assertIn("完成提交推送）。\n\n---\n\n[owner/repository]", CONTRACT_TEXT)
        self.assertIn("do not copy those labels into the final answer", REPORT_TYPES_TEXT)
        self.assertNotIn("## 摘要", CONTRACT_TEXT)
        self.assertNotIn("## 收尾", CONTRACT_TEXT)


if __name__ == "__main__":
    unittest.main()
