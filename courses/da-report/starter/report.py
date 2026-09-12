"""From analysis to report — starter (deliberately unfinished).

Contract: see TASK.md. Read scenario/analysis-pack/results.json and
produce a structured report.json plus a rendered report.md in out/.
"""

from __future__ import annotations

import json
from pathlib import Path

SCENARIO_DIR = Path(__file__).resolve().parent.parent / "scenario" / "analysis-pack"
OUT_DIR = Path(__file__).resolve().parent.parent / "out"


def load_inputs(directory):
    """Load results.json into a dict."""
    raise NotImplementedError


def build_report(inputs):
    """Return {"title": str, "sections": [{"heading", "body"}, ...],
    "metrics": {...}} — metrics must carry the input numbers unchanged."""
    raise NotImplementedError


def render_markdown(report):
    """Render the report dict to Markdown. Required headings in order:
    '# <title>', '## Data quality', '## Findings', '## Appendix'."""
    raise NotImplementedError


def write_report(report, markdown, out_dir):
    """Write report.json (indent 2, trailing newline) and report.md."""
    raise NotImplementedError


def main(argv=None):
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
