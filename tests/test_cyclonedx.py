from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ai_manifest.cyclonedx import generate_cyclonedx_bom, format_cyclonedx_json
from ai_manifest.models import AIComponent, ComponentType, SystemManifest
from ai_manifest.cli import main


class TestCycloneDX(unittest.TestCase):
    def test_cyclonedx_structure(self):
        manifest = SystemManifest(
            project_name="ComplianceBot",
            components=[
                AIComponent(
                    name="OpenAI Model",
                    component_type=ComponentType.MODEL,
                    evidence="gpt-4o",
                    file_path="src/llm.py",
                    version_or_variant="gpt-4o-2024-05-13",
                ),
                AIComponent(
                    name="ChromaDB",
                    component_type=ComponentType.VECTOR_DB,
                    evidence="chromadb.Client",
                    file_path="src/db.py",
                    version_or_variant=">=0.4.0",
                ),
                AIComponent(
                    name="guardkit",
                    component_type=ComponentType.GUARDRAIL,
                    evidence="import guardkit",
                    file_path="src/safety.py",
                ),
            ],
            timestamp="2026-11-14T12:00:00Z",
        )

        bom = generate_cyclonedx_bom(manifest)

        # Standard CycloneDX top-level assertions
        self.assertEqual(bom["bomFormat"], "CycloneDX")
        self.assertEqual(bom["specVersion"], "1.6")
        self.assertTrue(bom["serialNumber"].startswith("urn:uuid:"))
        self.assertEqual(bom["metadata"]["component"]["name"], "ComplianceBot")
        self.assertEqual(len(bom["components"]), 3)

        # Model component specific assertions
        model_comp = next(c for c in bom["components"] if c["name"] == "OpenAI Model")
        self.assertEqual(model_comp["type"], "machine-learning-model")
        self.assertEqual(model_comp["version"], "gpt-4o-2024-05-13")
        self.assertIn("modelCard", model_comp)

        # Vector DB component assertions
        db_comp = next(c for c in bom["components"] if c["name"] == "ChromaDB")
        self.assertEqual(db_comp["type"], "data")

        # Serialized JSON
        json_str = format_cyclonedx_json(manifest)
        parsed = json.loads(json_str)
        self.assertEqual(parsed["specVersion"], "1.6")

    def test_cli_cyclonedx_export(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "agent.py").write_text("import chromadb\nmodel = 'claude-3-5-sonnet'", encoding="utf-8")
            out_file = root / "bom.cdx.json"

            ret = main(["scan", str(root), "--format", "cyclonedx", "-o", str(out_file)])
            self.assertEqual(ret, 0)
            self.assertTrue(out_file.exists())

            bom_data = json.loads(out_file.read_text(encoding="utf-8"))
            self.assertEqual(bom_data["bomFormat"], "CycloneDX")
            names = [c["name"] for c in bom_data["components"]]
            self.assertIn("ChromaDB", names)
            self.assertIn("Anthropic Claude Model", names)
