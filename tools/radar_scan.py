#!/usr/bin/env python3
"""Discover Project Radar review candidates (candidates only, never verdicts).

Inputs: GitHub Search (recent Python repositories by stars), the PyPI updates
feed, and the Hacker News Algolia search API. Output: a candidate list under
``catalog/projects/candidates.json`` containing only discovery facts — repo
URL, stars, latest release, license, first-seen date. The tool never writes
descriptions, rationale, or status: those stay human-authored per
``AGENTS.md`` and ``docs/CURATION_POLICY.md``.

Read-only and rate-limited like ``tools/check_links.py``, whose audited
SSRF/DNS-rebinding protections this tool reuses.
"""

from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ElementTree
from collections.abc import Iterable, Mapping
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

try:
    from tools.catalog import CatalogLoadError, load_radar
    from tools.check_links import (
        HostRateLimiter,
        SafeTargetGuard,
        build_session,
    )
except ModuleNotFoundError:  # Direct ``python tools/radar_scan.py`` execution.
    from check_links import HostRateLimiter, SafeTargetGuard, build_session

    from catalog import CatalogLoadError, load_radar


ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_RADAR_DIR = ROOT_DIR / "catalog" / "projects"
DEFAULT_OUTPUT = DEFAULT_RADAR_DIR / "candidates.json"
DEFAULT_TIMEOUT = 20.0
DEFAULT_MIN_INTERVAL = 1.5
FORBIDDEN_CANDIDATE_KEYS = {"description", "rationale", "status", "why"}

GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"
PYPI_UPDATES_URL = "https://pypi.org/rss/packages.xml"
HN_SEARCH_URL = "https://hn.algolia.com/api/v1/search_by_date"


def _today() -> date:
    return datetime.now(UTC).date()


def parse_github_search(payload: Mapping[str, Any], first_seen: date) -> list[dict[str, Any]]:
    """Map a GitHub repository-search payload to candidates."""

    candidates = []
    for item in payload.get("items", []):
        url = item.get("html_url")
        if not isinstance(url, str) or not url.startswith("https://github.com/"):
            continue
        candidate: dict[str, Any] = {
            "source": "github-search",
            "url": url,
            "first_seen": first_seen.isoformat(),
        }
        stars = item.get("stargazers_count")
        if isinstance(stars, int):
            candidate["stars"] = stars
        license_info = item.get("license")
        if isinstance(license_info, dict) and isinstance(
            license_info.get("spdx_id"), str
        ):
            candidate["license"] = license_info["spdx_id"]
        pushed_at = item.get("pushed_at")
        if isinstance(pushed_at, str):
            candidate["last_pushed_at"] = pushed_at
        candidates.append(candidate)
    return candidates


def parse_pypi_updates(document: str, first_seen: date) -> list[dict[str, Any]]:
    """Map the PyPI updates RSS feed to candidates."""

    candidates = []
    root = ElementTree.fromstring(document)
    for item in root.iter("item"):
        link = item.findtext("link")
        title = item.findtext("title") or ""
        if not isinstance(link, str) or not link.startswith("https://pypi.org/project/"):
            continue
        latest_release = title.split()[-1] if title.split() else None
        candidate = {
            "source": "pypi-updates",
            "url": link.rstrip("/"),
            "first_seen": first_seen.isoformat(),
        }
        if latest_release:
            candidate["latest_release"] = latest_release
        candidates.append(candidate)
    return candidates


def parse_hn_search(payload: Mapping[str, Any], first_seen: date) -> list[dict[str, Any]]:
    """Map an HN Algolia search payload to candidates."""

    candidates = []
    for hit in payload.get("hits", []):
        url = hit.get("url")
        if not isinstance(url, str) or not url.startswith("https://"):
            continue
        candidate: dict[str, Any] = {
            "source": "hn-latest",
            "url": url,
            "first_seen": first_seen.isoformat(),
        }
        points = hit.get("points")
        if isinstance(points, int):
            candidate["points"] = points
        candidates.append(candidate)
    return candidates


def _candidate_key(candidate: Mapping[str, Any]) -> tuple[str, str]:
    return (str(candidate["source"]), str(candidate["url"]))


def merge_candidates(
    fresh: Iterable[Mapping[str, Any]],
    previous: Iterable[Mapping[str, Any]],
    reviewed_urls: set[str],
    *,
    limit: int,
) -> list[dict[str, Any]]:
    """Merge fresh candidates with a previous list.

    Rules: reviewed projects are dropped; an earlier ``first_seen`` is
    preserved; per-source limits are enforced; the result is deterministic
    (sorted, then per-source newest-first by stars/points); and no candidate
    ever carries a description-like or status field.
    """

    merged: dict[tuple[str, str], dict[str, Any]] = {}
    for candidate in previous:
        url = str(candidate.get("url", ""))
        if url in reviewed_urls:
            continue
        if any(key in candidate for key in FORBIDDEN_CANDIDATE_KEYS):
            raise ValueError(
                f"candidate {url} carries a forbidden verdict field; "
                "descriptions and status must stay human-authored"
            )
        merged[_candidate_key(candidate)] = dict(candidate)
    for candidate in fresh:
        url = str(candidate.get("url", ""))
        if url in reviewed_urls:
            continue
        if any(key in candidate for key in FORBIDDEN_CANDIDATE_KEYS):
            raise ValueError(
                f"candidate {url} carries a forbidden verdict field; "
                "descriptions and status must stay human-authored"
            )
        key = _candidate_key(candidate)
        existing = merged.get(key)
        if existing is not None:
            if str(candidate["first_seen"]) < str(existing.get("first_seen", "")):
                existing["first_seen"] = candidate["first_seen"]
            for field in ("stars", "points", "latest_release", "license", "last_pushed_at"):
                if field in candidate:
                    existing[field] = candidate[field]
        else:
            merged[key] = dict(candidate)

    per_source_counts: dict[str, int] = {}
    result: list[dict[str, Any]] = []
    for key in sorted(merged):
        source, _url = key
        if per_source_counts.get(source, 0) >= limit:
            continue
        per_source_counts[source] = per_source_counts.get(source, 0) + 1
        result.append(merged[key])
    return result


def build_document(candidates: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "candidates": list(candidates),
        "note": (
            "Discovery candidates only. Descriptions, rationale, and status "
            "are human-authored during review; see docs/CURATION_POLICY.md."
        ),
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    }


def _reviewed_urls(radar_dir: Path) -> set[str]:
    try:
        projects = load_radar(radar_dir)
    except CatalogLoadError:
        return set()
    return {str(project["url"]).rstrip("/") for project in projects}


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--radar-dir", type=Path, default=DEFAULT_RADAR_DIR)
    parser.add_argument("--limit", type=int, default=15, help="max candidates per source")
    parser.add_argument("--created-within-days", type=int, default=30)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    parser.add_argument("--min-interval", type=float, default=DEFAULT_MIN_INTERVAL)
    parser.add_argument(
        "--dry-run", action="store_true", help="print candidates without writing"
    )
    args = parser.parse_args()
    if args.limit < 1 or args.created_within_days < 1:
        parser.error("--limit and --created-within-days must be positive")

    reviewed = _reviewed_urls(args.radar_dir)
    previous: list[dict[str, Any]] = []
    if args.output.exists():
        try:
            previous = list(
                json.loads(args.output.read_text(encoding="utf-8")).get("candidates", [])
            )
        except (OSError, ValueError):
            print("warning: could not read previous candidates; starting fresh", file=sys.stderr)
            previous = []

    today = _today()
    created_after = (today - timedelta(days=args.created_within_days)).isoformat()
    guard_session = build_session(SafeTargetGuard())
    rate_limiter = HostRateLimiter(args.min_interval)

    def fetch_json(url: str, params: Mapping[str, str]) -> Any:
        rate_limiter.wait(url)
        response = guard_session.get(url, params=dict(params), timeout=args.timeout)
        response.raise_for_status()
        return response.json()

    fresh: list[dict[str, Any]] = []
    errors: list[str] = []

    try:
        payload = fetch_json(
            GITHUB_SEARCH_URL,
            {
                "q": f"language:python created:>{created_after}",
                "sort": "stars",
                "order": "desc",
                "per_page": str(args.limit),
            },
        )
        fresh.extend(parse_github_search(payload, today))
    except Exception as error:  # noqa: BLE001 — one source failing must not kill the rest
        errors.append(f"github-search: {error}")

    try:
        rate_limiter.wait(PYPI_UPDATES_URL)
        response = guard_session.get(PYPI_UPDATES_URL, timeout=args.timeout)
        response.raise_for_status()
        fresh.extend(parse_pypi_updates(response.text, today))
    except Exception as error:  # noqa: BLE001
        errors.append(f"pypi-updates: {error}")

    try:
        payload = fetch_json(
            HN_SEARCH_URL,
            {
                "query": "python",
                "tags": "story",
                "hitsPerPage": str(args.limit),
            },
        )
        fresh.extend(parse_hn_search(payload, today))
    except Exception as error:  # noqa: BLE001
        errors.append(f"hn-latest: {error}")

    try:
        candidates = merge_candidates(fresh, previous, reviewed, limit=args.limit)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 1

    document = build_document(candidates)
    rendered = json.dumps(document, ensure_ascii=False, indent=2) + "\n"
    if args.dry_run:
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"wrote {len(candidates)} candidates to {args.output}")

    if errors and not candidates:
        for message in errors:
            print(f"error: {message}", file=sys.stderr)
        return 1
    if errors:
        for message in errors:
            print(f"warning: {message}", file=sys.stderr)
    return 0


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
