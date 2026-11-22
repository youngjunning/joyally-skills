import importlib.util
from pathlib import Path
import tempfile
import unittest


spec = importlib.util.spec_from_file_location(
    'validate_repository',
    Path(__file__).resolve().parents[1] / 'scripts/validate.py',
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ValidateRepositoryTests(unittest.TestCase):
    def test_next_build_output_is_not_scanned_as_public_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'catalog.json').write_text('[]')
            (root / 'README.md').write_text('')
            (root / 'skills').mkdir()
            cache = root / 'skills/example/workbench/.next'
            cache.mkdir(parents=True)
            (cache / 'required-server-files.json').write_text(
                '{"workspace": "' + '/' + 'Users/example/private-checkout"}'
            )

            self.assertEqual(module.validate(root), [])

    def test_missing_workflow_command_path_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'catalog.json').write_text('[]')
            (root / 'README.md').write_text('')
            (root / 'skills').mkdir()
            workflows = root / '.github/workflows'
            workflows.mkdir(parents=True)
            workflow = workflows / 'validate.yml'
            workflow.write_text(
                'jobs:\n'
                '  validate:\n'
                '    steps:\n'
                '      - run: python3 -m unittest discover '
                "-s skills/productivity/moved-skill/scripts -p 'test_*.py'\n"
            )

            self.assertIn(
                'workflow command path does not exist: '
                '.github/workflows/validate.yml:4: '
                'skills/productivity/moved-skill/scripts',
                module.validate(root),
            )


if __name__ == '__main__':
    unittest.main()
