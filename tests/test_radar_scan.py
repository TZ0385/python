from __future__ import annotations

from datetime import date

import pytest

from tools.radar_scan import (
    FORBIDDEN_CANDIDATE_KEYS,
    build_document,
    merge_candidates,
    parse_github_search,
    parse_hn_search,
    parse_pypi_updates,
)


def test_github_payload_maps_to_discovery_facts_only() -> None:
    payload = {
        "items": [
            {
                "html_url": "https://github.com/owner/repo",
                "stargazers_count": 42,
                "license": {"spdx_id": "MIT"},
                "description": "A tool that should never be copied",
            }
        ]
    }
    candidates = parse_github_search(payload, date(2026, 9, 12))
    assert candidates == [
        {
            "source": "github-search",
            "url": "https://github.com/owner/repo",
            "first_seen": "2026-09-12",
            "stars": 42,
            "license": "MIT",
        }
    ]


def test_pypi_feed_parses_latest_release() -> None:
    document = (
        '<?xml version="1.0"?><rss><channel>'
        "<item><link>https://pypi.org/project/thing/</link>"
        "<title>thing 2.1.0</title></item>"
        "<item><link>https://example.com/not-pypi</link>"
        "<title>skip 1.0</title></item>"
        "</channel></rss>"
    )
    candidates = parse_pypi_updates(document, date(2026, 9, 12))
    assert candidates == [
        {
            "source": "pypi-updates",
            "url": "https://pypi.org/project/thing",
            "first_seen": "2026-09-12",
            "latest_release": "2.1.0",
        }
    ]


def test_hn_payload_keeps_urls_and_points_only() -> None:
    payload = {
        "hits": [
            {"url": "https://github.com/owner/repo", "points": 7, "title": "show hn"},
            {"url": "javascript:void(0)", "points": 1},
        ]
    }
    candidates = parse_hn_search(payload, date(2026, 9, 12))
    assert candidates == [
        {
            "source": "hn-latest",
            "url": "https://github.com/owner/repo",
            "first_seen": "2026-09-12",
            "points": 7,
        }
    ]


def test_merge_drops_reviewed_urls_and_preserves_first_seen() -> None:
    reviewed = {"https://github.com/owner/reviewed"}
    fresh = [
        {
            "source": "github-search",
            "url": "https://github.com/owner/repo",
            "first_seen": "2026-09-12",
        },
        {
            "source": "github-search",
            "url": "https://github.com/owner/reviewed",
            "first_seen": "2026-09-12",
        },
    ]
    previous = [
        {
            "source": "github-search",
            "url": "https://github.com/owner/repo",
            "first_seen": "2026-08-01",
        }
    ]
    merged = merge_candidates(fresh, previous, reviewed, limit=10)
    assert len(merged) == 1
    assert merged[0]["first_seen"] == "2026-08-01"


def test_merge_enforces_per_source_limit() -> None:
    fresh = [
        {
            "source": "github-search",
            "url": f"https://github.com/owner/repo{i}",
            "first_seen": "2026-09-12",
        }
        for i in range(5)
    ]
    merged = merge_candidates(fresh, [], set(), limit=2)
    assert len(merged) == 2


def test_no_candidate_ever_carries_a_verdict_field() -> None:
    poisoned = [
        {
            "source": "github-search",
            "url": "https://github.com/owner/repo",
            "first_seen": "2026-09-12",
            "description": "generated text must never survive",
        }
    ]
    with pytest.raises(ValueError):
        merge_candidates(poisoned, [], set(), limit=10)


def test_document_carries_the_human_review_note() -> None:
    document = build_document([])
    assert FORBIDDEN_CANDIDATE_KEYS.isdisjoint(document)
    assert "human-authored" in document["note"]
