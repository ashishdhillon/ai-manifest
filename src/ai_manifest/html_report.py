from __future__ import annotations

import html
from typing import Dict, List
from .models import ComponentType, SystemManifest


def generate_html_system_card(manifest: SystemManifest) -> str:
    """Generate an interactive, standalone HTML AI System Card & Architecture Manifest."""
    project_name = html.escape(manifest.project_name)
    timestamp = html.escape(manifest.timestamp or "UTC")

    # Group components by type
    grouped: Dict[ComponentType, List] = {t: [] for t in ComponentType}
    for c in manifest.components:
        grouped.setdefault(c.component_type, []).append(c)

    model_count = len(grouped.get(ComponentType.MODEL, []))
    vdb_count = len(grouped.get(ComponentType.VECTOR_DB, []))
    guard_count = len(grouped.get(ComponentType.GUARDRAIL, []))
    fw_count = len(grouped.get(ComponentType.FRAMEWORK, []))

    # Color themes for component types
    type_colors = {
        ComponentType.MODEL.value: ("#8b5cf6", "#8b5cf615"),       # Purple
        ComponentType.VECTOR_DB.value: ("#06b6d4", "#06b6d415"),   # Cyan
        ComponentType.GUARDRAIL.value: ("#10b981", "#10b98115"),   # Emerald
        ComponentType.FRAMEWORK.value: ("#f59e0b", "#f59e0b15"),   # Amber
        ComponentType.DATA_SOURCE.value: ("#3b82f6", "#3b82f615"), # Blue
    }

    # Render table rows
    table_rows = []
    for c in manifest.components:
        c_name = html.escape(c.name)
        c_type = html.escape(c.component_type.value)
        c_ver = html.escape(c.version_or_variant)
        c_ev = html.escape(c.evidence)
        c_file = html.escape(c.file_path)

        border_c, bg_c = type_colors.get(c.component_type.value, ("#6b7280", "#6b728015"))
        badge_html = f'<span class="type-badge" style="color: {border_c}; background-color: {bg_c}; border-color: {border_c}50;">{c_type.upper()}</span>'

        table_rows.append(f"""
        <tr>
            <td><strong>{c_name}</strong></td>
            <td>{badge_html}</td>
            <td><code>{c_ver}</code></td>
            <td><code class="evidence-pill">{c_ev}</code></td>
            <td><small class="text-muted">{c_file}</small></td>
        </tr>
        """)

    table_rows_joined = "\n".join(table_rows) if table_rows else "<tr><td colspan='5' style='text-align:center;'>No third-party AI components detected.</td></tr>"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI System Card & Component Manifest: {project_name}</title>
    <style>
        :root {{
            --bg: #0f172a;
            --surface: #1e293b;
            --surface-border: #334155;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background-color: var(--bg);
            color: var(--text-primary);
            font-family: var(--font-family);
            line-height: 1.5;
            padding: 2rem 1rem;
        }}
        .container {{
            max-width: 1050px;
            margin: 0 auto;
        }}
        .header {{
            background: var(--surface);
            border: 1px solid var(--surface-border);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1.5rem;
        }}
        .header-title h1 {{
            font-size: 1.6rem;
            font-weight: 700;
            color: var(--text-primary);
        }}
        .header-title p {{
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-top: 0.25rem;
        }}
        .assurance-badge {{
            display: inline-block;
            background: #10b98115;
            border: 1px solid #10b98140;
            color: #34d399;
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
        }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        .kpi-card {{
            background: var(--surface);
            border: 1px solid var(--surface-border);
            border-radius: 10px;
            padding: 1.25rem;
        }}
        .kpi-label {{
            font-size: 0.78rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .kpi-value {{
            font-size: 1.8rem;
            font-weight: 700;
            margin-top: 0.3rem;
        }}
        .section-title {{
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }}
        .table-card {{
            background: var(--surface);
            border: 1px solid var(--surface-border);
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 2rem;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.92rem;
        }}
        th, td {{
            padding: 0.85rem 1.2rem;
            text-align: left;
        }}
        th {{
            background: #192237;
            color: var(--text-secondary);
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-bottom: 1px solid var(--surface-border);
        }}
        tr:not(:last-child) td {{
            border-bottom: 1px solid var(--surface-border);
        }}
        .type-badge {{
            display: inline-block;
            padding: 0.2rem 0.55rem;
            border-radius: 4px;
            font-size: 0.72rem;
            font-weight: 700;
            border: 1px solid;
        }}
        .evidence-pill {{
            background: #0f172a;
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
            color: #cbd5e1;
            font-size: 0.82em;
        }}
        .text-muted {{ color: var(--text-secondary); }}
        code {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 0.85em; }}
        .footer {{
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.82rem;
            padding-top: 1.5rem;
            border-top: 1px solid var(--surface-border);
        }}
        @media print {{
            body {{ background: #ffffff; color: #000000; padding: 0; }}
            .header, .kpi-card, .table-card {{
                background: #ffffff; border-color: #e2e8f0; color: #000000; box-shadow: none;
            }}
            .header-title h1, .section-title {{ color: #000000; }}
            th {{ background: #f1f5f9; color: #334155; }}
            .evidence-pill {{ background: #f8fafc; border: 1px solid #e2e8f0; color: #334155; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="header-title">
                <h1>AI System Card & Component Manifest</h1>
                <p>Audited Application: <strong>{project_name}</strong> &bull; Generated: {timestamp}</p>
            </div>
            <div>
                <span class="assurance-badge">EU AI Act Art. 53 &bull; NIST AI RMF Map Aligned</span>
            </div>
        </header>

        <section class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Total Components</div>
                <div class="kpi-value">{len(manifest.components)}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Models & Runtimes</div>
                <div class="kpi-value" style="color: #8b5cf6;">{model_count}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Vector Stores</div>
                <div class="kpi-value" style="color: #06b6d4;">{vdb_count}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Safety Guardrails</div>
                <div class="kpi-value" style="color: #10b981;">{guard_count}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Frameworks & Agents</div>
                <div class="kpi-value" style="color: #f59e0b;">{fw_count}</div>
            </div>
        </section>

        <section>
            <h2 class="section-title">Component Supply Chain & Architecture Ledger</h2>
            <div class="table-card">
                <table>
                    <thead>
                        <tr>
                            <th>Component Name</th>
                            <th>Architecture Type</th>
                            <th>Version / Specifier</th>
                            <th>Signature Evidence</th>
                            <th>File Lineage</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows_joined}
                    </tbody>
                </table>
            </div>
        </section>

        <footer class="footer">
            <p>Generated by <strong>ai-manifest</strong> &bull; Zero-Dependency Automated AI System Card and AI-BOM Generator</p>
        </footer>
    </div>
</body>
</html>
"""
