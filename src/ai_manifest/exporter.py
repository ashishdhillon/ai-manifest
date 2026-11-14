from __future__ import annotations

import json
from .models import SystemManifest


def format_table(manifest: SystemManifest) -> str:
    lines = [
        "┌────────────────────────────────────────────────────────────┐",
        "│                    AI SYSTEM MANIFEST                      │",
        "├────────────────────────────────────────────────────────────┤",
        f"│ Project: {manifest.project_name:<35} Components: {len(manifest.components):<4} │",
        "├──────────────────────────┬──────────────┬──────────────────┤",
        "│ Component Name           │ Type         │ Found In         │",
        "├──────────────────────────┼──────────────┼──────────────────┤",
    ]
    if not manifest.components:
        lines.append("│ No third-party AI models or vector stores discovered.      │")
    else:
        for c in manifest.components:
            f_name = c.file_path[-16:] if len(c.file_path) > 16 else c.file_path
            lines.append(f"│ {c.name:<24} │ {c.component_type.value:<12} │ {f_name:<16} │")
    lines.append("└──────────────────────────┴──────────────┴──────────────────┘")
    return "\n".join(lines)


def format_markdown(manifest: SystemManifest) -> str:
    lines = [
        f"# AI System Inventory & Architecture Manifest: {manifest.project_name}",
        "",
        f"- **Generated At (UTC):** `{manifest.timestamp}`",
        f"- **Total Discovered Components:** `{len(manifest.components)}`",
        "",
        "## Component Ledger",
        "",
        "| Component Name | Type | Detected Signature | File Location |",
        "| :--- | :--- | :--- | :--- |",
    ]
    for c in manifest.components:
        lines.append(f"| **{c.name}** | `{c.component_type.value}` | `{c.evidence}` | `{c.file_path}` |")
    return "\n".join(lines)


def format_json(manifest: SystemManifest) -> str:
    return json.dumps(manifest.to_dict(), indent=2)


def format_cyclonedx(manifest: SystemManifest) -> str:
    from .cyclonedx import format_cyclonedx_json
    return format_cyclonedx_json(manifest)


def format_html(manifest: SystemManifest) -> str:
    from .html_report import generate_html_system_card
    return generate_html_system_card(manifest)


