# ai-manifest

[![CI](https://github.com/ashishdhillon/ai-manifest/actions/workflows/ci.yml/badge.svg)](https://github.com/ashishdhillon/ai-manifest/actions/workflows/ci.yml)
[![Live Demo](https://img.shields.io/badge/Live_Demo-Interactive_System_Card-8b5cf6?style=flat&logo=googlechrome&logoColor=white)](https://ashishdhillon.github.io/ai-manifest/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)](pyproject.toml)

Automated component inventory, AI Software Bill of Materials (AI-BOM), and system card generator for AI applications and agentic pipelines.

---

## Overview

Software supply chain governance and compliance under the **EU AI Act (Article 53)** and **NIST AI RMF (MAP function)** require organizations to document every third-party foundation model, vector store, guardrail, and orchestration framework their applications rely on.

`ai-manifest` inspects your codebase and package manifests (`requirements.txt`, `pyproject.toml`, `package.json`) to produce audit-ready inventories:

- **Models & Inference Runtimes:** OpenAI, Anthropic Claude, Google Gemini, Meta Llama, Mistral, DeepSeek, Cohere, Ollama, vLLM, SGLang, Hugging Face.
- **Vector Databases & Embeddings:** ChromaDB, Qdrant, Pinecone, FAISS, Weaviate, pgvector, LanceDB, Milvus, Voyage AI.
- **Safety Middleware & Governance:** `guardkit`, `rag-poison-bench`, `airmf-audit`, `dpdp-rag-audit`, NeMo Guardrails, Guardrails AI, Llama Guard.
- **Agentic & Orchestration Frameworks:** LangGraph, CrewAI, DSPy, AutoGen, Semantic Kernel, LangChain, LlamaIndex, LiteLLM.

---

## Key Features

- **Zero External Dependencies:** Built entirely with Python 3.9+ standard library (`json`, `html`, `re`, `argparse`, `pathlib`, `uuid`).
- **CycloneDX 1.6 AI-BOM Specification:** Export standardized machine-readable Software Bill of Materials for enterprise compliance and security pipelines (`--format cyclonedx`).
- **Interactive HTML System Card:** Generates executive-ready dark/light HTML system cards (`--format html -o system-card.html`) with KPI summary metrics and print stylesheets.
- **Dual Source Discovery:** Discovers declared dependencies across package manifests and scans source code files (`.py`, `.ts`, `.js`, `.json`, `.yaml`) for unpinned models or runtime endpoints.

---

## Installation

```bash
git clone https://github.com/ashishdhillon/ai-manifest.git
cd ai-manifest
pip install -e .
```

---

## Quickstart

### 1. Terminal Summary Table
```bash
ai-manifest scan /path/to/my-ai-repo
```

### 2. Export Standardized CycloneDX 1.6 AI-BOM
```bash
ai-manifest scan /path/to/my-ai-repo --format cyclonedx -o bom.cdx.json
```

### 3. Generate Interactive HTML System Card
```bash
ai-manifest scan /path/to/my-ai-repo --format html -o system-card.html
```

### 4. Generate GitHub-Flavored Markdown Architecture Card
```bash
ai-manifest scan /path/to/my-ai-repo --format markdown -o SYSTEM_CARD.md
```

---

## Sample Terminal Output

```
┌────────────────────────────────────────────────────────────┐
│                    AI SYSTEM MANIFEST                      │
├────────────────────────────────────────────────────────────┤
│ Project: legal-agent-app                     Components: 5 │
├──────────────────────────┬──────────────┬──────────────────┤
│ Component Name           │ Type         │ Found In         │
├──────────────────────────┼──────────────┼──────────────────┤
│ Anthropic Claude Model   │ model        │ src/llm.py       │
│ ChromaDB                 │ vector_db    │ requirements.txt │
│ LangGraph                │ framework    │ src/graph.py     │
│ dpdp-rag-audit           │ guardrail    │ requirements.txt │
│ guardkit                 │ guardrail    │ src/safety.py    │
└──────────────────────────┴──────────────┴──────────────────┘
```

---

## Python API

Integrate directly into your CI/CD compliance checks:

```python
from ai_manifest import ManifestScanner, format_cyclonedx, format_html

scanner = ManifestScanner()
manifest = scanner.scan_project("./src")

print(f"Discovered {len(manifest.components)} AI components in {manifest.project_name}:")
for comp in manifest.components:
    print(f" • [{comp.component_type.value.upper()}] {comp.name} ({comp.version_or_variant})")

# Export CycloneDX 1.6 AI-BOM string
cdx_json = format_cyclonedx(manifest)

# Export standalone HTML system card
html_card = format_html(manifest)
```

---

## Academic & Regulatory References

`ai-manifest` aligns its technical component reporting with peer-reviewed literature and international standards:
- **Mitchell et al. (ACM FAT\* 2019)**: *Model Cards for Model Reporting*
- **Raji et al. (ACM FAccT 2020)**: *Closing the AI Accountability Gap: Defining an End-to-End Framework for Internal Algorithmic Auditing*
- **CycloneDX 1.6 AI-BOM Specification**: OWASP Machine Learning and Artificial Intelligence Software Bill of Materials standard.
- **EU Artificial Intelligence Act (Regulation EU 2024/1689)**: Article 53 & Annex IV technical documentation mandates.
- **NIST AI Risk Management Framework (NIST AI 100-1)**: MAP Function component categorization.

For full BibTeX entries and citations, see [REFERENCES.md](REFERENCES.md).

---

## Running Tests

Run the zero-dependency test suite:

```bash
python3 -m unittest discover -s tests -v
```

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on adding new detection signatures and package parsers.

---

## License

MIT © [Ashish Dhillon](https://github.com/ashishdhillon)
