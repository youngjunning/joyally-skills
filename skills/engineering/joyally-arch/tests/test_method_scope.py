"""Static scope regression; does not prove real UI or Agent behavior."""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / 'SKILL.md').read_text()
METHOD = SKILL.split('### Minimum-complete path', 1)[1].split('### Complexity admission gate', 1)[0]


class MethodScopeTests(unittest.TestCase):
    def test_entire_method_is_non_front_end_only(self):
        self.assertIn('non-front-end only', METHOD)
        self.assertIn('this entire subsection applies only', METHOD)
        self.assertIn('Do not apply its change-surface/reuse-ladder/deliberate-ceiling method', METHOD)
        for area in ['front-end architecture', 'visual design', 'client-side interaction', 'motion', 'reviews']:
            self.assertIn(area, METHOD)

    def test_full_stack_front_end_is_not_reincluded(self):
        self.assertIn('scope this method to the non-front-end portion', METHOD)
        self.assertIn('the front-end portion stays excluded', METHOD)

    def test_experience_and_other_engineering_obligations_remain(self):
        for requirement in ['visual hierarchy', 'responsive behavior', 'interaction states', 'accessibility', 'motion']:
            self.assertIn(requirement, METHOD)
        self.assertIn('Do not remove or defer these requirements', METHOD)
        for obligation in ['security', 'trust-boundary validation', 'functional completeness', 'testing obligations']:
            self.assertIn(obligation, METHOD)
        self.assertIn('references/web-architecture-patterns.md', METHOD)

    def test_backend_method_still_exists(self):
        for clause in ['backend services', 'data pipelines', 'CLI tools', 'whole change surface',
                       'Choose the first path', 'known ceiling', 'measurable revisit trigger']:
            self.assertIn(clause, METHOD)

    def test_readme_and_behavior_case_state_the_exclusion(self):
        readme = (ROOT / 'README.md').read_text()
        cases = (ROOT / 'references/behavior-checks.md').read_text()
        self.assertIn('limited to non-front-end work', readme)
        self.assertIn('skip that method', readme)
        self.assertIn('Excludes the whole minimum-complete method', cases)
        self.assertIn('keeps safeguards', cases.lower())


if __name__ == '__main__':
    unittest.main()
