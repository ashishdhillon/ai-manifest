from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from .models import AIComponent, ComponentType, SystemManifest
from .package_parser import parse_manifest_file

SIGNATURES = [
    # Models & Providers
    (r"(?i)\b(?:gpt-4o(?:-mini)?|gpt-4-turbo|gpt-3\.5-turbo|text-embedding-3(?:-small|-large)?|o1(?:-preview|-mini)?|o3-mini)\b", "OpenAI Model", ComponentType.MODEL),
    (r"(?i)\b(?:claude-3(?:-5)?-(?:sonnet|opus|haiku)|claude-2\.1)\b", "Anthropic Claude Model", ComponentType.MODEL),
    (r"(?i)\b(?:gemini-1\.5-(?:pro|flash)|gemini-2\.0-(?:flash|pro)|gemini-pro)\b", "Google Gemini Model", ComponentType.MODEL),
    (r"(?i)\b(?:llama-3(?:\.[123])?|llama-2|meta-llama)\b", "Meta Llama Model", ComponentType.MODEL),
    (r"(?i)\b(?:mistral-large|mistral-small|mixtral|codestral)\b", "Mistral AI Model", ComponentType.MODEL),
    (r"(?i)\b(?:deepseek[_-](?:v2|v3|r1|coder)|deepseek)\b", "DeepSeek AI Model", ComponentType.MODEL),
    (r"(?i)\b(?:command-r(?:-plus)?|embed-english-v3\.0|embed-multilingual)\b", "Cohere Model", ComponentType.MODEL),
    (r"(?i)\b(?:ollama(?:\.chat|\.generate)?|localhost:11434)\b", "Ollama Local Runtime", ComponentType.MODEL),
    (r"(?i)\b(?:vllm(?:\.entrypoints)?|AsyncLLMEngine|EngineArgs)\b", "vLLM Inference Engine", ComponentType.MODEL),
    (r"(?i)\bsglang\b", "SGLang Runtime", ComponentType.MODEL),
    (r"(?i)\bhuggingface_hub|HuggingFacePipeline|AutoModelForCausalLM\b", "Hugging Face Model Hub", ComponentType.MODEL),

    # Vector Databases & Embeddings
    (r"(?i)\b(?:chromadb|chroma\.Client|chroma_client)\b", "ChromaDB", ComponentType.VECTOR_DB),
    (r"(?i)\b(?:qdrant_client|QdrantClient)\b", "Qdrant", ComponentType.VECTOR_DB),
    (r"(?i)\b(?:pinecone\.init|PineconeClient|pinecone)\b", "Pinecone", ComponentType.VECTOR_DB),
    (r"(?i)\b(?:faiss\.Index|faiss\.read_index|IndexFlatL2)\b", "FAISS", ComponentType.VECTOR_DB),
    (r"(?i)\b(?:weaviate\.Client|weaviate\.connect)\b", "Weaviate", ComponentType.VECTOR_DB),
    (r"(?i)\b(?:pgvector|PGVector|vector_extension)\b", "pgvector", ComponentType.VECTOR_DB),
    (r"(?i)\b(?:lancedb|connect_lancedb)\b", "LanceDB", ComponentType.VECTOR_DB),
    (r"(?i)\b(?:pymilvus|MilvusClient)\b", "Milvus", ComponentType.VECTOR_DB),
    (r"(?i)\b(?:voyageai|voyage-large-2)\b", "Voyage AI", ComponentType.VECTOR_DB),

    # Safety Guardrails & Governance
    (r"(?i)\bguardkit\b", "guardkit", ComponentType.GUARDRAIL),
    (r"(?i)\brag[_-]poison[_-]bench\b", "rag-poison-bench", ComponentType.GUARDRAIL),
    (r"(?i)\bairmf[_-]audit\b", "airmf-audit", ComponentType.GUARDRAIL),
    (r"(?i)\bdpdp[_-]rag[_-]audit\b", "dpdp-rag-audit", ComponentType.GUARDRAIL),
    (r"(?i)\b(?:guardrails-ai|guardrails_ai)\b", "Guardrails AI", ComponentType.GUARDRAIL),
    (r"(?i)\bnemo_guardrails\b", "NeMo Guardrails", ComponentType.GUARDRAIL),
    (r"(?i)\bllama_guard\b", "Llama Guard", ComponentType.GUARDRAIL),

    # AI Frameworks & Orchestrators
    (r"(?i)\blanggraph\b", "LangGraph", ComponentType.FRAMEWORK),
    (r"(?i)\blangchain(?:_core|_community)?\b", "LangChain", ComponentType.FRAMEWORK),
    (r"(?i)\bllama_index(?:_core)?\b", "LlamaIndex", ComponentType.FRAMEWORK),
    (r"(?i)\blitellm\b", "LiteLLM", ComponentType.FRAMEWORK),
    (r"(?i)\bdspy(?:\.Predict|\.ChainOfThought)?\b", "DSPy", ComponentType.FRAMEWORK),
    (r"(?i)\bcrewai\b", "CrewAI", ComponentType.FRAMEWORK),
    (r"(?i)\bsemantic_kernel\b", "Semantic Kernel", ComponentType.FRAMEWORK),
    (r"(?i)\bautogen\b", "AutoGen", ComponentType.FRAMEWORK),
]

KNOWN_AI_PACKAGES: Dict[str, Tuple[str, ComponentType]] = {
    # Models & Runtimes
    "openai": ("OpenAI Model", ComponentType.MODEL),
    "@azure/openai": ("OpenAI Model", ComponentType.MODEL),
    "anthropic": ("Anthropic Claude Model", ComponentType.MODEL),
    "@anthropic-ai/sdk": ("Anthropic Claude Model", ComponentType.MODEL),
    "google-genai": ("Google Gemini Model", ComponentType.MODEL),
    "google-generativeai": ("Google Gemini Model", ComponentType.MODEL),
    "@google/genai": ("Google Gemini Model", ComponentType.MODEL),
    "cohere": ("Cohere Model", ComponentType.MODEL),
    "deepseek": ("DeepSeek AI Model", ComponentType.MODEL),
    "transformers": ("Hugging Face Model Hub", ComponentType.MODEL),
    "huggingface-hub": ("Hugging Face Model Hub", ComponentType.MODEL),
    "ollama": ("Ollama Local Runtime", ComponentType.MODEL),
    "vllm": ("vLLM Inference Engine", ComponentType.MODEL),
    "sglang": ("SGLang Runtime", ComponentType.MODEL),

    # Vector DBs
    "chromadb": ("ChromaDB", ComponentType.VECTOR_DB),
    "qdrant-client": ("Qdrant", ComponentType.VECTOR_DB),
    "@qdrant/js-client-rest": ("Qdrant", ComponentType.VECTOR_DB),
    "pinecone": ("Pinecone", ComponentType.VECTOR_DB),
    "pinecone-client": ("Pinecone", ComponentType.VECTOR_DB),
    "@pinecone-database/pinecone": ("Pinecone", ComponentType.VECTOR_DB),
    "faiss-cpu": ("FAISS", ComponentType.VECTOR_DB),
    "faiss-gpu": ("FAISS", ComponentType.VECTOR_DB),
    "weaviate-client": ("Weaviate", ComponentType.VECTOR_DB),
    "pgvector": ("pgvector", ComponentType.VECTOR_DB),
    "lancedb": ("LanceDB", ComponentType.VECTOR_DB),
    "vectordb": ("LanceDB", ComponentType.VECTOR_DB),
    "pymilvus": ("Milvus", ComponentType.VECTOR_DB),
    "voyageai": ("Voyage AI", ComponentType.VECTOR_DB),

    # Guardrails
    "guardkit": ("guardkit", ComponentType.GUARDRAIL),
    "rag-poison-bench": ("rag-poison-bench", ComponentType.GUARDRAIL),
    "airmf-audit": ("airmf-audit", ComponentType.GUARDRAIL),
    "dpdp-rag-audit": ("dpdp-rag-audit", ComponentType.GUARDRAIL),
    "guardrails-ai": ("Guardrails AI", ComponentType.GUARDRAIL),
    "nemoguardrails": ("NeMo Guardrails", ComponentType.GUARDRAIL),

    # Frameworks
    "langchain": ("LangChain", ComponentType.FRAMEWORK),
    "langchain-core": ("LangChain", ComponentType.FRAMEWORK),
    "langgraph": ("LangGraph", ComponentType.FRAMEWORK),
    "@langchain/core": ("LangChain", ComponentType.FRAMEWORK),
    "llama-index": ("LlamaIndex", ComponentType.FRAMEWORK),
    "llama-index-core": ("LlamaIndex", ComponentType.FRAMEWORK),
    "litellm": ("LiteLLM", ComponentType.FRAMEWORK),
    "dspy": ("DSPy", ComponentType.FRAMEWORK),
    "dspy-ai": ("DSPy", ComponentType.FRAMEWORK),
    "crewai": ("CrewAI", ComponentType.FRAMEWORK),
    "semantic-kernel": ("Semantic Kernel", ComponentType.FRAMEWORK),
    "pyautogen": ("AutoGen", ComponentType.FRAMEWORK),
    "autogen": ("AutoGen", ComponentType.FRAMEWORK),
}


class ManifestScanner:
    """Scans project source files and package manifests to discover AI models, vector stores, and guardrails."""

    def scan_project(self, root_dir: Path | str) -> SystemManifest:
        root = Path(root_dir)
        discovered: list[AIComponent] = []
        seen_keys: set[tuple[str, str]] = set()

        # Step 1: Scan package manifests (requirements.txt, package.json, pyproject.toml)
        manifest_files = [
            root / "requirements.txt",
            root / "requirements-dev.txt",
            root / "pyproject.toml",
            root / "package.json",
        ]
        # Also check subdirectories for manifests
        for mf in ("requirements.txt", "package.json", "pyproject.toml"):
            for found in root.rglob(mf):
                if not any(p.startswith(".") or p in ("venv", ".venv", "env", "node_modules", "dist", "build") for p in found.parts):
                    if found not in manifest_files:
                        manifest_files.append(found)

        package_version_map: Dict[str, Tuple[str, str]] = {}
        for mf in manifest_files:
            if mf.is_file():
                entries = parse_manifest_file(mf)
                for pkg_name, ver in entries:
                    if pkg_name in KNOWN_AI_PACKAGES:
                        canon_name, c_type = KNOWN_AI_PACKAGES[pkg_name]
                        package_version_map[canon_name] = (ver, str(mf.relative_to(root) if mf.is_relative_to(root) else mf))
                        key = (canon_name, c_type.value)
                        if key not in seen_keys:
                            seen_keys.add(key)
                            discovered.append(
                                AIComponent(
                                    name=canon_name,
                                    component_type=c_type,
                                    evidence=f"manifest dependency '{pkg_name}' ({ver})",
                                    file_path=str(mf.relative_to(root) if mf.is_relative_to(root) else mf),
                                    version_or_variant=ver,
                                )
                            )

        # Step 2: Scan source files for signatures
        extensions = ("*.py", "*.json", "*.yaml", "*.yml", "*.toml", "*.txt", "*.md", "*.ts", "*.js")
        files_to_scan: list[Path] = []
        for ext in extensions:
            files_to_scan.extend(root.rglob(ext))

        for file_path in files_to_scan:
            parts = file_path.parts
            if any(p.startswith(".") or p in ("venv", ".venv", "env", "node_modules", "dist", "build") for p in parts):
                continue
            if file_path.name in ("package.json", "pyproject.toml", "requirements.txt"):
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
                        version_val = package_version_map.get(name, ("detected-in-code", ""))[0]
                        discovered.append(
                            AIComponent(
                                name=name,
                                component_type=c_type,
                                evidence=match.group(0),
                                file_path=str(file_path.relative_to(root) if file_path.is_relative_to(root) else file_path),
                                version_or_variant=version_val,
                            )
                        )

        # Sort components deterministically by type and name
        discovered.sort(key=lambda c: (c.component_type.value, c.name))

        return SystemManifest(
            project_name=root.name or "AI Project",
            components=discovered,
        )
