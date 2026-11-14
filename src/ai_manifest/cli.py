from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from .exporter import (
    format_cyclonedx,
    format_html,
    format_json,
    format_markdown,
    format_table,
)
from .scanner import ManifestScanner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-manifest",
        description="Automated component inventory and system card generator for AI applications.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Scan directory for AI components and output manifest")
    scan_parser.add_argument("path", nargs="?", default=".", help="Root directory to scan (default: current directory)")
    scan_parser.add_argument("--format", choices=["table", "markdown", "json", "cyclonedx", "html"], default="table", help="Output format")
    scan_parser.add_argument("-o", "--output", help="Write manifest output to file")

    return parser


def handle_scan(args: argparse.Namespace) -> int:
    scanner = ManifestScanner()
    target_path = Path(args.path)

    if not target_path.exists():
        print(f"Error: Target path '{args.path}' does not exist.", file=sys.stderr)
        return 2

    manifest = scanner.scan_project(target_path)

    if args.format == "json":
        out = format_json(manifest)
    elif args.format == "cyclonedx":
        out = format_cyclonedx(manifest)
    elif args.format == "html":
        out = format_html(manifest)
    elif args.format == "markdown":
        out = format_markdown(manifest)
    else:
        out = format_table(manifest)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"Manifest written to {args.output}")
    else:
        print(out)

    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "scan":
        return handle_scan(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
