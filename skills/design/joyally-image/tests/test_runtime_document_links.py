from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
REFERENCE_DIR = ROOT / "runtime/diagram/references"


class RuntimeDocumentLinksTest(unittest.TestCase):
    def test_migrated_references_resolve_inside_standalone_skill(self) -> None:
        for name in (
            "authoring-contract.md",
            "delivery-contract.md",
            "repository-authoring.md",
        ):
            document = REFERENCE_DIR / name
            text = re.sub(r"```.*?```", "", document.read_text("utf-8"), flags=re.S)
            for href in re.findall(r"\]\(([^\s)]+)\)", text):
                link = urlsplit(href)
                if link.scheme or link.netloc or not link.path:
                    continue
                with self.subTest(document=name, href=href):
                    target = (document.parent / unquote(link.path)).resolve()
                    self.assertTrue(target.is_relative_to(ROOT), href)
                    self.assertTrue(target.is_file(), href)
                    if link.fragment:
                        headings = re.findall(
                            r"^#{1,6}\s+(.+)$", target.read_text("utf-8"), re.M
                        )
                        anchors = {
                            re.sub(r"[^\w -]", "", heading.lower()).replace(" ", "-")
                            for heading in headings
                        }
                        self.assertIn(unquote(link.fragment), anchors, href)


if __name__ == "__main__":
    unittest.main()
