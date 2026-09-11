from __future__ import annotations

from datetime import date
from typing import Any

import pytest

from tools.catalog import (
    CatalogLoadError,
    load_radar,
    validate_radar,
)


def make_project(**overrides: Any) -> dict[str, Any]:
    project: dict[str, Any] = {
        "id": "sample-project",
        "repo": "owner/sample-project",
        "url": "https://github.com/owner/sample-project",
        "category": "code-quality",
        "status": "rising",
        "first_seen": date(2026, 9, 2),
        "reviewed_on": date(2026, 9, 2),
        "license": "MIT",
        "evidence": {
            "last_release": "1.0.0",
            "release_cadence": "monthly",
            "maintenance": "active team",
        },
        "ai_familiarity": "medium",
        "alternatives": ["sample-other"],
        "rationale_en": "Does one thing well with evidence.",
        "rationale_zh": "专注做好一件事，有证据支撑。",
        "when_not_to_use_en": "When you need the ecosystem of sample-other.",
        "when_not_to_use_zh": "需要 sample-other 生态时。",
        "risk_en": "Fast-moving API.",
        "risk_zh": "API 变化较快。",
    }
    project.update(overrides)
    return project


def test_valid_project_passes() -> None:
    assert validate_radar([make_project()], today=date(2026, 9, 12)) == []


@pytest.mark.parametrize(
    "field,value,code",
    [
        ("status", "trending", "invalid-enum"),
        ("category", "misc", "invalid-enum"),
        ("ai_familiarity", "unknown", "invalid-enum"),
        ("repo", "not-a-repo", "invalid-repo"),
        ("url", "http://insecure.example/repo", "https-required"),
        ("id", "Bad_ID", "invalid-id"),
        ("rationale_zh", "", "invalid-text"),
    ],
)
def test_invalid_fields_are_reported(field: str, value: Any, code: str) -> None:
    issues = validate_radar(
        [make_project(**{field: value})], today=date(2026, 9, 12)
    )
    assert any(issue.code == code for issue in issues), issues


def test_unknown_fields_are_rejected() -> None:
    issues = validate_radar(
        [make_project(extra="nope")], today=date(2026, 9, 12)
    )
    assert any(issue.code == "unknown-field" for issue in issues)


def test_review_date_cannot_predate_first_seen() -> None:
    issues = validate_radar(
        [make_project(first_seen=date(2026, 9, 10))],
        today=date(2026, 9, 12),
    )
    assert any(issue.code == "date-parity" for issue in issues)


def test_stale_review_is_reported() -> None:
    issues = validate_radar(
        [make_project()],
        today=date(2027, 9, 12),
        max_review_age_days=366,
    )
    assert any(issue.code == "stale-review" for issue in issues)


def test_duplicate_ids_are_reported() -> None:
    issues = validate_radar(
        [make_project(), make_project()], today=date(2026, 9, 12)
    )
    assert any(issue.code == "duplicate-id" for issue in issues)


def test_evidence_requires_all_three_fields() -> None:
    evidence = {"last_release": "1.0.0", "release_cadence": "monthly"}
    issues = validate_radar(
        [make_project(evidence=evidence)], today=date(2026, 9, 12)
    )
    assert any(
        issue.code == "missing-field" and issue.location.endswith("evidence")
        for issue in issues
    )


def test_committed_radar_sources_validate_and_ids_match_filenames(
    tmp_path: Any,
) -> None:
    import shutil
    from pathlib import Path

    source = Path(__file__).resolve().parents[1] / "catalog" / "projects"
    target = tmp_path / "projects"
    shutil.copytree(source, target)
    projects = load_radar(target)
    assert len(projects) >= 7
    issues = validate_radar(projects, today=date(2026, 9, 12))
    assert issues == []


def test_loader_rejects_id_filename_mismatch(tmp_path: Any) -> None:
    (tmp_path / "wrong-name.yml").write_text(
        "id: something-else\n", encoding="utf-8"
    )
    with pytest.raises(CatalogLoadError):
        load_radar(tmp_path)
