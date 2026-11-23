"""Exercise the writing skill's public identity and relocated checker entrypoints."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('link_writing', ROOT / 'scripts/link-skills.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class WritingDistributionTests(unittest.TestCase):
    def setUp(self):
        catalog = json.loads((ROOT / 'catalog.json').read_text())
        entries = [item for item in catalog if item['name'] == 'joyally-writing']
        self.assertEqual(len(entries), 1)
        self.entry = entries[0]
        self.source = ROOT / self.entry['path']
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dest = Path(self.tmp.name) / 'skills'

    def test_catalog_install_exposes_the_same_skill_identity(self):
        installer.install([(self.entry['name'], self.source)], self.dest)
        installed = self.dest / self.entry['name']
        self.assertEqual(installed.resolve(), self.source.resolve())
        self.assertEqual(self.source.name, self.entry['name'])
        frontmatter = (installed / 'SKILL.md').read_text().split('---', 2)[1]
        declared_name = next(line.split(':', 1)[1].strip()
                             for line in frontmatter.splitlines() if line.startswith('name:'))
        self.assertEqual(declared_name, installed.name)
        self.assertEqual(installer.install([(self.entry['name'], self.source)], self.dest),
                         [(self.entry['name'], 'unchanged')])

    def test_relocated_book_checkers_run_from_a_standalone_copy(self):
        copied = self.dest / self.entry['name']
        shutil.copytree(self.source, copied)
        checkers = sorted((copied / 'scripts').glob('check_*.py'))
        self.assertEqual(len(checkers), 4)
        for checker in checkers:
            with self.subTest(checker=checker.name):
                result = subprocess.run([sys.executable, str(checker), '--help'],
                                        cwd=self.tmp.name, capture_output=True, text=True,
                                        timeout=15)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('usage:', result.stdout.lower())


if __name__ == '__main__':
    unittest.main()
