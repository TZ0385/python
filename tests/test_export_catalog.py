from __future__ import annotations

import json
from pathlib import Path

from tools.export_catalog import build_export, build_radar_export, render, run

ROOT = Path(__file__).resolve().parents[1]


def test_export_has_stable_public_contract(valid_catalog: dict) -> None:
    export = build_export(valid_catalog)

    assert export["schema_version"] == 1
    assert export["catalog"] == {
        "reviewed_on": "2026-08-31",
        "status": "active",
    }
    assert export["paths"] == valid_catalog["catalog"]["paths"]
    assert export["resources"][0]["reviewed_on"] == "2026-08-31"


def test_checked_in_export_matches_catalog_sources() -> None:
    assert run(["--check"]) == 0
    assert run(["--check", "--target", "both"]) == 0


def test_catalog_schema_is_valid_json() -> None:
    schema = json.loads(
        (ROOT / "schema" / "catalog-v1.schema.json").read_text(encoding="utf-8")
    )

    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["properties"]["schema_version"]["const"] == 1


def test_render_export_is_deterministic(valid_catalog: dict) -> None:
    assert render(build_export(valid_catalog)) == render(build_export(valid_catalog))


def test_radar_export_lists_reviewed_projects_sorted() -> None:
    projects = [
        {"id": "zeta", "reviewed_on": "2026-09-02"},
        {"id": "alpha", "reviewed_on": "2026-09-02"},
    ]
    export = build_radar_export(projects)
    assert export["$schema"] == "./schema/radar-v1.schema.json"
    assert [p["id"] for p in export["projects"]] == ["alpha", "zeta"]


def test_radar_schema_declares_lifecycle_and_familiarity() -> None:
    schema = json.loads(
        (ROOT / "schema" / "radar-v1.schema.json").read_text(encoding="utf-8")
    )
    project = schema["properties"]["projects"]["items"]
    assert set(project["properties"]["status"]["enum"]) == {
        "new",
        "rising",
        "stable",
        "major-update",
        "experimental",
        "archived",
    }
    assert set(project["properties"]["ai_familiarity"]["enum"]) == {
        "low",
        "medium",
        "high",
    }
