from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ai_manifest.package_parser import (
    parse_package_json,
    parse_pyproject_toml,
    parse_requirements_txt,
)
from ai_manifest.scanner import ManifestScanner
from ai_manifest.models import ComponentType


class TestPackageScanner(unittest.TestCase):
    def test_parse_requirements_txt(self):
        sample = """
        # Core RAG dependencies
        chromadb>=0.4.22
        openai~=1.12.0
        langchain-core==0.2.1
        guardkit
        # Development
        pytest>=7.0.0
        """
        deps = parse_requirements_txt(sample)
        dep_dict = dict(deps)
        self.assertIn("chromadb", dep_dict)
        self.assertEqual(dep_dict["chromadb"], ">=0.4.22")
        self.assertEqual(dep_dict["openai"], "~=1.12.0")
        self.assertEqual(dep_dict["guardkit"], "unpinned")

    def test_parse_pyproject_toml(self):
        sample = """
        [project]
        name = "agent-app"
        version = "0.1.0"
        dependencies = [
            "langgraph>=0.1.0",
            "dspy-ai==2.4.0",
            "qdrant-client>=1.7.0"
        ]
        """
        deps = parse_pyproject_toml(sample)
        dep_dict = dict(deps)
        self.assertIn("langgraph", dep_dict)
        self.assertEqual(dep_dict["langgraph"], ">=0.1.0")
        self.assertIn("dspy-ai", dep_dict)
        self.assertEqual(dep_dict["dspy-ai"], "==2.4.0")

    def test_parse_package_json(self):
        sample = """
        {
            "name": "ai-nextjs-app",
            "dependencies": {
                "@google/genai": "^0.1.1",
                "@pinecone-database/pinecone": "^2.0.0"
            },
            "devDependencies": {
                "typescript": "^5.0.0"
            }
        }
        """
        deps = parse_package_json(sample)
        dep_dict = dict(deps)
        self.assertIn("@google/genai", dep_dict)
        self.assertEqual(dep_dict["@google/genai"], "^0.1.1")
        self.assertIn("@pinecone-database/pinecone", dep_dict)

    def test_full_project_manifest_scan(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)

            # 1. requirements.txt
            (root / "requirements.txt").write_text("vllm>=0.4.0\nlancedb==0.5.0\ncrewai>=0.28.0\n", encoding="utf-8")

            # 2. Python agent source code
            agent_file = root / "agent.py"
            agent_file.write_text("from langgraph.graph import StateGraph\nimport deepseek_r1\n", encoding="utf-8")

            scanner = ManifestScanner()
            manifest = scanner.scan_project(root)

            names = {c.name for c in manifest.components}
            self.assertIn("vLLM Inference Engine", names)
            self.assertIn("LanceDB", names)
            self.assertIn("CrewAI", names)
            self.assertIn("LangGraph", names)
            self.assertIn("DeepSeek AI Model", names)

            # Check that version info was populated from requirements.txt
            vllm_comp = next(c for c in manifest.components if c.name == "vLLM Inference Engine")
            self.assertEqual(vllm_comp.version_or_variant, ">=0.4.0")
