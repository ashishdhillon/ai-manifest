# ai-manifest

[![CI](https://github.com/ashishdhillon/ai-manifest/actions/workflows/ci.yml/badge.svg)](https://github.com/ashishdhillon/ai-manifest/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)](pyproject.toml)

Automated component inventory and system card generator for AI applications and LLM pipelines.

---

## Overview

Software supply chain governance for AI requires knowing exactly which foundation models, vector databases, and safety guardrails your application relies on.

`ai-manifest` inspects your codebase and produces an audit-ready inventory manifest:
- **Models & Runtimes:** OpenAI, Anthropic, Google Gemini, Meta Llama, Mistral, Ollama, HuggingFace.
- **Vector Databases:** ChromaDB, Qdrant, Pinecone, FAISS, Weaviate, pgvector.
- **Safety Middleware:** `guardkit`, `rag-poison-bench`, NeMo Guardrails, Llama Guard.
- **Orchestration Frameworks:** LangChain, LlamaIndex, LiteLLM.

---

## Quickstart

```bash
git clone https://github.com/ashishdhillon/ai-manifest.git
cd ai-manifest
pip install -e .
```

Scan an AI repository:

```bash
# Terminal summary table
ai-manifest scan /path/to/my-ai-repo

# Generate an architecture documentation system card
ai-manifest scan /path/to/my-ai-repo --format markdown -o system-card.md

# Export machine-readable JSON inventory
ai-manifest scan /path/to/my-ai-repo --format json -o manifest.json
```

---

## Sample Output

```
┌────────────────────────────────────────────────────────────┐
│                    AI SYSTEM MANIFEST                      │
├────────────────────────────────────────────────────────────┤
│ Project: my-agent-app                        Components: 4 │
├──────────────────────────┬──────────────┬──────────────────┤
│ Component Name           │ Type         │ Found In         │
├──────────────────────────┼──────────────┼──────────────────┤
│ OpenAI Model             │ model        │ app.py           │
│ ChromaDB                 │ vector_db    │ db/client.py     │
│ guardkit                 │ guardrail    │ security.py      │
│ LangChain                │ framework    │ pipeline.py      │
└──────────────────────────┴──────────────┴──────────────────┘
```

---

## Python API

```python
from ai_manifest import ManifestScanner, format_markdown

scanner = ManifestScanner()
manifest = scanner.scan_project("./src")

print(f"Discovered {len(manifest.components)} AI components:")
for comp in manifest.components:
    print(f" • {comp.name} ({comp.component_type.value}) in {comp.file_path}")

doc = format_markdown(manifest)
```

---

## License

MIT © [Ashish Dhillon](https://github.com/ashishdhillon)
