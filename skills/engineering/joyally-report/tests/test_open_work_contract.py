from pathlib import Path
import unittest


SKILL_DIR = Path(__file__).resolve().parents[1]
SKILL_TEXT = (SKILL_DIR / "SKILL.md").read_text()
CONTRACT_TEXT = (SKILL_DIR / "references/turn-report.md").read_text()


class OpenWorkContractTests(unittest.TestCase):
    def test_entrypoint_reconciles_conversation_before_verdict(self):
        self.assertIn("Before composing the verdict", SKILL_TEXT)
        self.assertIn("current conversation", SKILL_TEXT)
        self.assertIn("#current-conversation-open-work", SKILL_TEXT)

    def test_contract_separates_scope_state_and_next_action(self):
        self.assertIn("## Current-conversation open work", CONTRACT_TEXT)
        self.assertIn("latest correction", CONTRACT_TEXT)
        self.assertIn("Do not scan other sessions", CONTRACT_TEXT)
        self.assertIn("optional suggestions", CONTRACT_TEXT)
        self.assertIn("pending implementation / 待实现", CONTRACT_TEXT)
        self.assertIn("pending verification / 待验证", CONTRACT_TEXT)
        self.assertIn("completion or unblock condition", CONTRACT_TEXT)
        self.assertIn("No known required work remains", CONTRACT_TEXT)

    def test_interrupted_task_cannot_disappear_after_side_question(self):
        self.assertIn("A side question does not cancel", CONTRACT_TEXT)
        self.assertIn("deletion is still pending implementation", CONTRACT_TEXT)
        self.assertIn("Saving a note does not silently add a deployment task", CONTRACT_TEXT)


if __name__ == "__main__":
    unittest.main()
