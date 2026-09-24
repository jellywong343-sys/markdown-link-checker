import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from markdown_link_checker.cli import extract_links, inspect_file, summary

class LinkCheckerTests(unittest.TestCase):
    def test_extract_and_local_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "guide.md").write_text("guide", encoding="utf-8")
            doc = root / "README.md"
            doc.write_text("[Guide](guide.md)\n[Missing](missing.md)\n[Web](https://example.com)\n", encoding="utf-8")
            results = inspect_file(doc)
            self.assertEqual([item.status for item in results], ["ok", "broken", "unchecked"])

    def test_duplicate_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            doc = Path(tmp) / "README.md"
            doc.write_text("[One](a.md) and [Two](a.md)", encoding="utf-8")
            links = extract_links(doc)
            self.assertEqual(len(links), 2)
            results = inspect_file(doc)
            self.assertEqual(summary(results)["duplicate_urls"], ["a.md"])

if __name__ == "__main__":
    unittest.main()
