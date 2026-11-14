# Changelog

All notable changes to `ai-manifest` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.2.0] - 2026-11-14

### Added
- **Package Manifest Dependency Extraction**:
  - Automatically parses package manifests across Python and JavaScript ecosystems (`requirements.txt`, `pyproject.toml`, `package.json`).
  - Extracts declared package versions and specifiers (e.g. `chromadb>=0.4.22`, `@google/genai^0.1.1`) to enrich component lineage data.
- **CycloneDX 1.6 AI-BOM Specification**:
  - Full support for exporting standardized AI Software Bill of Materials via `--format cyclonedx`.
  - Serializes machine learning models (`machine-learning-model`), vector data sources (`data`), guardrails (`library`), and frameworks (`framework`) with `modelCard` parameters and Package URLs (`purl`).
- **Interactive HTML System Card & Architecture Dashboard**:
  - Standalone, dark/light responsive HTML system card generation (`--format html -o system-card.html`).
  - Executive KPI summary cards, color-coded architecture badges, signature evidence pills, and print stylesheet.
  - Aligned with EU AI Act Article 53 technical documentation and NIST AI RMF MAP function requirements.
- **Expanded Agentic & Inference Catalog**:
  - Added detection signatures for LangGraph, DSPy, CrewAI, AutoGen, Semantic Kernel, vLLM, SGLang, DeepSeek, LanceDB, Milvus, and Voyage AI.
- **Comprehensive Academic & Regulatory References**:
  - Added `REFERENCES.md` with BibTeX citations and links to foundational AI governance literature.

---

## [0.1.0] - 2026-11-14

### Added
- Initial release of automated AI component inventory scanner.
- Regex heuristics for OpenAI, Claude, Gemini, Llama, ChromaDB, Qdrant, Pinecone, FAISS, and LangChain.
- ASCII table, Markdown, and raw JSON export formats.
- Pure Python 3.9+ standard library implementation with zero external runtime dependencies.
