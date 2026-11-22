from pathlib import Path
import re
import subprocess
import unittest


SKILL_DIR = Path(__file__).resolve().parents[1]
SKILL_TEXT = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
GENERATION_TEXT = (SKILL_DIR / "references" / "generation.md").read_text(encoding="utf-8")
DECODER_TEXT = (SKILL_DIR / "scripts" / "decode_apiyi_response.py").read_text(encoding="utf-8")
INVITATION_LINK = "https://api.apiyi.com/register/?aff_code=ijv5"


class RoutingContractTests(unittest.TestCase):
    def test_local_only_route_precedes_credentials_and_forbids_external_requests(self) -> None:
        local_route = SKILL_TEXT.index("**Local-only:**")
        credential_rule = SKILL_TEXT.index("`APIYI_API_KEY`")
        self.assertLess(local_route, credential_rule)
        self.assertIn("Do not read `APIYI_API_KEY`", SKILL_TEXT)
        self.assertIn("send any external image request", SKILL_TEXT)

    def test_generative_route_keeps_apiyi_model_and_host_fallback(self) -> None:
        self.assertIn("`gpt-image-2.6-sunburst`", SKILL_TEXT)
        self.assertIn("host-native image generation or editing tool", SKILL_TEXT)
        self.assertIn("never GPT Image 2.6", SKILL_TEXT)

    def test_missing_key_and_balance_fallback_include_invitation_link(self) -> None:
        self.assertIn("A missing key is non-blocking", SKILL_TEXT)
        self.assertIn("insufficient-balance", DECODER_TEXT)
        self.assertIn(INVITATION_LINK, SKILL_TEXT)
        self.assertIn(INVITATION_LINK, GENERATION_TEXT)
        balance_rule = SKILL_TEXT.split("A confirmed invalid-key or insufficient-balance", 1)[1]
        balance_rule = balance_rule.split("\n7.", 1)[0]
        self.assertIn(INVITATION_LINK, balance_rule)

    def test_generation_reference_no_longer_exits_task_for_missing_key(self) -> None:
        environment_section = GENERATION_TEXT.split("## Model Setup", 1)[0]
        self.assertNotIn("exit 1", environment_section)
        self.assertIn("return 4", environment_section)
        self.assertIn('${APIYI_API_KEY:-}', GENERATION_TEXT)
        self.assertIn("check_apiyi_key || return $?", GENERATION_TEXT)

    def test_missing_key_contract_runs_under_nounset(self) -> None:
        match = re.search(
            r"```bash\n(check_apiyi_key\(\) \{.*?\n\})\n```",
            GENERATION_TEXT,
            re.DOTALL,
        )
        self.assertIsNotNone(match)
        result = subprocess.run(
            [
                "bash",
                "-u",
                "-c",
                f"{match.group(1)}\nunset APIYI_API_KEY\ncheck_apiyi_key",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(4, result.returncode)
        self.assertIn("APIYI_UNAVAILABLE:missing-key", result.stdout)

    def test_type_specific_apiyi_routes_preserve_fallback_signal(self) -> None:
        references = SKILL_DIR / "references"
        for path in references.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            if "GEN_LOG=$(gen_image_apiyi" not in text:
                continue
            with self.subTest(reference=path.name):
                self.assertIn("APIYI_FALLBACK_REQUIRED", text)

    def test_edit_route_checks_key_and_streams_response_validation(self) -> None:
        text = (SKILL_DIR / "references" / "image-edit.md").read_text(encoding="utf-8")
        key_check = text.index("if check_apiyi_key; then")
        request = text.index('curl -s --max-time 300 "https://api.apiyi.com/v1/images/edits"')
        self.assertLess(key_check, request)
        self.assertIn("scripts/decode_apiyi_response.py", text)
        self.assertIn("APIYI_FALLBACK_REQUIRED", text)

    def test_dynamic_wallpaper_parallel_status_preserves_fallback(self) -> None:
        text = (SKILL_DIR / "references" / "dynamic-wallpaper.md").read_text(
            encoding="utf-8"
        )
        match = re.search(
            r"```bash\n(wait_generation_pair\(\) \{.*?\n\})\n\nOUT_DIR=",
            text,
            re.DOTALL,
        )
        self.assertIsNotNone(match)
        function = match.group(1)

        for light, dark, expected in ((4, 4, 4), (4, 0, 4), (0, 4, 4), (1, 0, 1)):
            with self.subTest(light=light, dark=dark):
                script = (
                    f"{function}\n"
                    f"(exit {light}) & light_pid=$!\n"
                    f"(exit {dark}) & dark_pid=$!\n"
                    'wait_generation_pair "$light_pid" "$dark_pid"'
                )
                result = subprocess.run(
                    ["bash", "-u", "-c", script],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(expected, result.returncode, result.stderr)

    def test_mixed_route_preserves_original_and_rejects_false_success(self) -> None:
        self.assertIn("Preserve the original", SKILL_TEXT)
        self.assertIn("Never invent an output or claim success", SKILL_TEXT)


if __name__ == "__main__":
    unittest.main()
