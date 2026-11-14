from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple


def parse_requirements_txt(content: str) -> List[Tuple[str, str]]:
    """Parse requirements.txt content into (package_name, version_spec) tuples."""
    results: List[Tuple[str, str]] = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        # Split on whitespace/hash comment
        line = line.split("#")[0].strip()
        # Match package name and optional version
        m = re.match(r"^([a-zA-Z0-9_\-\.]+)(?:\s*([><=~!^]=?\s*[a-zA-Z0-9_\.\*\+\-]+))?", line)
        if m:
            pkg_name = m.group(1).lower().replace("_", "-")
            version = m.group(2).strip() if m.group(2) else "unpinned"
            results.append((pkg_name, version))
    return results


def parse_package_json(content: str) -> List[Tuple[str, str]]:
    """Parse package.json content for JavaScript/TypeScript AI applications."""
    results: List[Tuple[str, str]] = []
    try:
        data = json.loads(content)
        deps: Dict[str, str] = {}
        if isinstance(data.get("dependencies"), dict):
            deps.update(data["dependencies"])
        if isinstance(data.get("devDependencies"), dict):
            deps.update(data["devDependencies"])

        for pkg, ver in deps.items():
            results.append((pkg.lower(), str(ver).strip()))
    except Exception:
        pass
    return results


def parse_pyproject_toml(content: str) -> List[Tuple[str, str]]:
    """Extract declared dependencies from pyproject.toml without external TOML libraries."""
    results: List[Tuple[str, str]] = []
    # Match strings inside dependencies = [ ... ]
    dep_blocks = re.findall(r"dependencies\s*=\s*\[(.*?)\]", content, re.DOTALL)
    for block in dep_blocks:
        items = re.findall(r'["\']([^"\']+)["\']', block)
        for item in items:
            m = re.match(r"^([a-zA-Z0-9_\-\.]+)(?:\s*([><=~!^]=?\s*[a-zA-Z0-9_\.\*\+\-]+))?", item.strip())
            if m:
                pkg_name = m.group(1).lower().replace("_", "-")
                version = m.group(2).strip() if m.group(2) else "unpinned"
                results.append((pkg_name, version))
    return results


def parse_manifest_file(file_path: Path) -> List[Tuple[str, str]]:
    """Detect manifest type by filename and parse declared dependencies."""
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []

    fname = file_path.name.lower()
    if fname in ("requirements.txt", "requirements-dev.txt", "deps.txt") or fname.endswith(".req.txt"):
        return parse_requirements_txt(content)
    elif fname == "package.json":
        return parse_package_json(content)
    elif fname == "pyproject.toml":
        return parse_pyproject_toml(content)

    return []
