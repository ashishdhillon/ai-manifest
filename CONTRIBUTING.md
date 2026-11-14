# Contributing to ai-manifest

Thank you for your interest in contributing to `ai-manifest`! We welcome contributions to expand detection signatures, support new package formats, and improve AI-BOM standards compliance.

---

## Development Principles

1. **Zero External Runtime Dependencies:**
   All parsers, scanners, CycloneDX serializers, and HTML generators must use Python 3.9+ standard library modules exclusively (`json`, `html`, `re`, `argparse`, `pathlib`, `dataclasses`, `uuid`).

2. **Standard Library Testing:**
   All tests must use Python's built-in `unittest` framework and pass without network access.

3. **Deterministic Discovery:**
   Component detection must produce stable, sorted outputs across multiple runs.

---

## Local Setup

```bash
git clone https://github.com/ashishdhillon/ai-manifest.git
cd ai-manifest
pip install -e .
```

Run test suite:

```bash
python3 -m unittest discover -s tests -v
```

---

## Adding a New AI Component Signature

1. Open `src/ai_manifest/scanner.py`.
2. Add the regex pattern, canonical name, and `ComponentType` to `SIGNATURES`.
3. If applicable, add the package mapping to `KNOWN_AI_PACKAGES`.
4. Add a test case in `tests/test_package_scanner.py` verifying detection.

---

## Pull Request Guidelines

- Use conventional commit messages (`feat:`, `fix:`, `test:`, `docs:`).
- Keep changes focused on a dedicated feature branch.
- Verify all unit tests pass before opening a PR.
