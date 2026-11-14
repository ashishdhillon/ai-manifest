from __future__ import annotations

import re
from pathlib import Path
from typing import List
from .models import AIComponent, ComponentType, SystemManifest

SIGNATURES = [
    # Models & Providers
    (r"(?i)\b(?:gpt-4o?|gpt-3\.5-turbo|text-embedding-3)\b", "OpenAI Model", ComponentType.MODEL),
    (r"(?i)\b(?:claude-3|claude-3-5|claude-sonnet|claude-opus)\b", "Anthropic Claude Model", ComponentType.MODEL),
    (r"(?i)\b(?:gemini-1\.5|gemini-2\.0|gemini-pro|gemini-flash)\b", "Google Gemini Model", ComponentType.MODEL),
    (r"(?i)\b(?:llama-3|llama-3\.1|llama-2)\b", "Meta Llama Model", ComponentType.MODEL),
    (r"(?i)\b(?:mistral-large|mistral-small|mixtral)\b", "Mistral AI Model", ComponentType.MODEL),
    (r"(?i)\b(?:ollama(?:\.chat|\.generate)?|localhost:11434)\b", "Ollama Local Runtime", ComponentType.MODEL),
    (r"(?i)\bhuggingface_hub|HuggingFacePipeline\b", "Hugging Face Model Hub", ComponentType.MODEL),

    # Vector Databases
    (r"(?i)\b(?:chromadb|chroma\.Client)\b", "ChromaDB", ComponentType.VECTOR_DB),
    (r"(?i)\b(?:qdrant_client|QdrantClient)\b", "Qdrant", ComponentType.VECTOR_DB),
    (r"(?i)\b(?:pinecone\.init|PineconeClient|pinecone)\b", "Pinecone", ComponentType.VECTOR_DB),
    (r"(?i)\b(?:faiss\.Index|faiss\.read_index)\b", "FAISS", ComponentType.VECTOR_DB),
    (r"(?i)\b(?:weaviate\.Client|weaviate\.connect)\b", "Weaviate", ComponentType.VECTOR_DB),
    (r"(?i)\bpgvector\b", "pgvector", ComponentType.VECTOR_DB),

    # Safety Guardrails
    (r"(?i)\bguardkit\b", "guardkit", ComponentType.GUARDRAIL),
    (r"(?i)\brag[_-]poison[_-]bench\b", "rag-poison-bench", ComponentType.GUARDRAIL),
    (r"(?i)\bnemo_guardrails\b", "NeMo Guardrails", ComponentType.GUARDRAIL),
    (r"(?i)\bllama_guard\b", "Llama Guard", ComponentType.GUARDRAIL),

    # AI Frameworks
    (r"(?i)\blangchain\b", "LangChain", ComponentType.FRAMEWORK),
    (r"(?i)\bllama_index\b", "LlamaIndex", ComponentType.FRAMEWORK),
    (r"(?i)\blitellm\b", "LiteLLM", ComponentType.FRAMEWORK),
]


class ManifestScanner:
    """Scans project source files to discover AI models, vector stores, and guardrails."""

    def scan_project(self, root_dir: Path | str) -> SystemManifest:
        root = Path(root_dir)
        discovered: list[AIComponent] = []
        seen_keys: set[tuple[str, str]] = set()

        extensions = ("*.py", "*.json", "*.yaml", "*.yml", "*.toml", "*.txt", "*.md")
        files_to_scan: list[Path] = []
        for ext in extensions:
            files_to_scan.extend(root.rglob(ext))

        for file_path in files_to_scan:
            # Skip virtual environments and hidden directories
            parts = file_path.parts
            if any(p.startswith(".") or p in ("venv", ".venv", "env", "node_modules", "dist", "build") for p in parts):
                continue

            try:
                content = file_path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue

            for pattern, name, c_type in SIGNATURES:
                match = re.search(pattern, content)
                if match:
                    key = (name, c_type.value)
                    if key not in seen_keys:
                        seen_keys.add(key)
                        discovered.append(
                            AIComponent(
                                name=name,
                                component_type=c_type,
                                evidence=match.group(0),
                                file_path=str(file_path.relative_to(root) if file_path.is_relative_to(root) else file_path),
                            )
                        )

        return SystemManifest(
            project_name=root.name or "AI Project",
            components=discovered,
        )
