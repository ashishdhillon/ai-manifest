import unittest
import tempfile
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ai_manifest.scanner import ManifestScanner
from ai_manifest.exporter import format_table, format_markdown, format_json
from ai_manifest.models import ComponentType


class TestAIManifest(unittest.TestCase):
    def test_scanner_discovery(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            # Create sample files
            f1 = tmp_path / "app.py"
            f1.write_text("import chromadb\nmodel = 'gpt-4o'\nimport guardkit", encoding="utf-8")

            f2 = tmp_path / "config.json"
            f2.write_text('{"embed_db": "qdrant_client", "framework": "langchain"}', encoding="utf-8")

            scanner = ManifestScanner()
            manifest = scanner.scan_project(tmp_path)

            names = [c.name for c in manifest.components]
            self.assertIn("OpenAI Model", names)
            self.assertIn("ChromaDB", names)
            self.assertIn("guardkit", names)
            self.assertIn("Qdrant", names)
            self.assertIn("LangChain", names)

    def test_exporters(self):
        scanner = ManifestScanner()
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            f = tmp_path / "main.py"
            f.write_text("from llama_index import VectorStoreIndex", encoding="utf-8")

            manifest = scanner.scan_project(tmp_path)
            tbl = format_table(manifest)
            self.assertIn("AI SYSTEM MANIFEST", tbl)

            md = format_markdown(manifest)
            self.assertIn("# AI System Inventory", md)

            js = format_json(manifest)
            self.assertIn('"project_name":', js)


if __name__ == "__main__":
    unittest.main()
