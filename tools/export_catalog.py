#!/usr/bin/env python3
"""Build the deterministic JSON exports (catalog, radar) consumed by flypython.com."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping, Sequence
from datetime import date, datetime
from pathlib import Path
from typing import Any

try:
    from tools.catalog import (
        CatalogLoadError,
        load_catalog,
        load_radar,
        validate_catalog,
        validate_radar,
    )
except ModuleNotFoundError:  # Direct ``python tools/export_catalog.py`` execution.
    from catalog import (
        CatalogLoadError,
        load_catalog,
        load_radar,
        validate_catalog,
        validate_radar,
    )


ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CATALOG = ROOT_DIR / "catalog"
DEFAULT_CATALOG_OUTPUT = ROOT_DIR / "catalog.json"
DEFAULT_RADAR_DIR = ROOT_DIR / "catalog" / "projects"
DEFAULT_RADAR_OUTPUT = ROOT_DIR / "radar.json"
TARGETS = ("catalog", "radar", "both")


def _json_ready(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Mapping):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    return value


def build_export(data: Mapping[str, Any]) -> dict[str, Any]:
    metadata = data["catalog"]
    return {
        "$schema": "./schema/catalog-v1.schema.json",
        "schema_version": 1,
        "catalog": {
            "reviewed_on": _json_ready(metadata["reviewed_on"]),
            "status": metadata["status"],
        },
        "paths": _json_ready(metadata["paths"]),
        "resources": _json_ready(data["resources"]),
    }


def build_radar_export(projects: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    ordered = sorted(projects, key=lambda project: str(project.get("id", "")))
    return {
        "$schema": "./schema/radar-v1.schema.json",
        "schema_version": 1,
        "projects": _json_ready(list(ordered)),
    }


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--output", type=Path, default=DEFAULT_CATALOG_OUTPUT)
    parser.add_argument(
        "--radar-dir", type=Path, default=DEFAULT_RADAR_DIR,
        help="directory of per-project Radar YAML files",
    )
    parser.add_argument("--radar-output", type=Path, default=DEFAULT_RADAR_OUTPUT)
    parser.add_argument(
        "--target",
        choices=TARGETS,
        default="catalog",
        help="which export to write or check (default: catalog)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail when a checked-in JSON export is missing or out of date",
    )
    parser.add_argument(
        "--stdout", action="store_true", help="write the export to standard output"
    )
    return parser


def _load_and_validate_catalog(catalog_path: Path) -> str | None:
    try:
        data = load_catalog(catalog_path)
    except CatalogLoadError as exc:
        print(str(exc), file=sys.stderr)
        return None
    issues = validate_catalog(data)
    if issues:
        for issue in issues:
            print(f"{issue.location}: {issue.code}: {issue.message}", file=sys.stderr)
        return None
    return render(build_export(data))


def _load_and_validate_radar(radar_dir: Path) -> str | None:
    try:
        projects = load_radar(radar_dir)
    except CatalogLoadError as exc:
        print(str(exc), file=sys.stderr)
        return None
    issues = validate_radar(projects)
    if issues:
        for issue in issues:
            print(f"{issue.location}: {issue.code}: {issue.message}", file=sys.stderr)
        return None
    return render(build_radar_export(projects))


def _write_or_check(rendered: str, output: Path, *, check: bool, label: str) -> bool:
    if check:
        try:
            current = output.read_text(encoding="utf-8")
        except OSError:
            print(f"{label} export is missing: {output}", file=sys.stderr)
            return False
        if current != rendered:
            print(
                f"{label} export is out of date: run {Path(__file__).name}",
                file=sys.stderr,
            )
            return False
        print(f"{label} export current: {output}")
        return True

    output.write_text(rendered, encoding="utf-8")
    print(f"wrote {label} export to {output}")
    return True


def run(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    want_catalog = args.target in ("catalog", "both")
    want_radar = args.target in ("radar", "both")

    rendered_catalog = _load_and_validate_catalog(args.catalog) if want_catalog else None
    rendered_radar = _load_and_validate_radar(args.radar_dir) if want_radar else None
    if (want_catalog and rendered_catalog is None) or (
        want_radar and rendered_radar is None
    ):
        return 1
    catalog_text = rendered_catalog or ""
    radar_text = rendered_radar or ""

    if args.stdout:
        if want_catalog and want_radar:
            print("--stdout supports one target; use --target catalog or radar", file=sys.stderr)
            return 2
        print(rendered_catalog if want_catalog else rendered_radar, end="")
        return 0

    ok = True
    if want_catalog:
        ok = _write_or_check(
            catalog_text, args.output, check=args.check, label="catalog"
        ) and ok
    if want_radar:
        ok = _write_or_check(
            radar_text, args.radar_output, check=args.check, label="radar"
        ) and ok
    return 0 if ok else 1


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
