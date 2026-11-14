from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ai_manifest.html_report import generate_html_system_card
from ai_manifest.models import AIComponent, ComponentType, SystemManifest
from ai_manifest.cli import main


class TestHTMLReport(unittest.TestCase):
    def test_html_system_card_content(self):
        manifest = SystemManifest(
            project_name="LegalRagBot",
            components=[
                AIComponent(
                    name="Google Gemini Model",
                    component_type=ComponentType.MODEL,
                    evidence="gemini-1.5-pro",
                    file_path="src/llm.py",
                    version_or_variant="gemini-1.5-pro-preview",
                ),
                AIComponent(
                    name="Qdrant",
                    component_type=ComponentType.VECTOR_DB,
                    evidence="QdrantClient",
                    file_path="src/db.py",
                    version_or_variant=">=1.7.0",
                ),
                AIComponent(
                    name="dpdp-rag-audit",
                    component_type=ComponentType.GUARDRAIL,
                    evidence="import dpdp_rag_audit",
                    file_path="src/privacy.py",
                ),
            ],
            timestamp="2026-11-14T12:00:00Z",
        )

        html_out = generate_html_system_card(manifest)
        self.assertIn("<!DOCTYPE html>", html_out)
        self.assertIn("AI System Card & Component Manifest", html_out)
        self.assertIn("LegalRagBot", html_out)
        self.assertIn("Google Gemini Model", html_out)
        self.assertIn("Qdrant", html_out)
        self.assertIn("dpdp-rag-audit", html_out)
        self.assertIn("EU AI Act Art. 53", html_out)

    def test_cli_html_export(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "main.py").write_text("import chromadb\nimport dspy\n", encoding="utf-8")
            out_file = root / "system-card.html"

            ret = main(["scan", str(root), "--format", "html", "-o", str(out_file)])
            self.assertEqual(ret, 0)
            self.assertTrue(out_file.exists())

            content = out_file.read_text(encoding="utf-8")
            self.assertIn("<!DOCTYPE html>", content)
            self.assertIn("ChromaDB", content)
            self.assertIn("DSPy", content)
