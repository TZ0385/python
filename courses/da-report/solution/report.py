"""From analysis to report — reviewed solution."""

from __future__ import annotations

import json
from pathlib import Path

SCENARIO_DIR = Path(__file__).resolve().parent.parent / "scenario" / "analysis-pack"
OUT_DIR = Path(__file__).resolve().parent.parent / "out"


def load_inputs(directory):
    return json.loads((Path(directory) / "results.json").read_text(encoding="utf-8"))


def build_report(inputs):
    metrics = {
        "rows_total": inputs["rows_total"],
        "rows_clean": inputs["rows_clean"],
        "total_revenue": inputs["total_revenue"],
        "top_category": inputs["top_category"],
        "revenue_by_region": inputs["revenue_by_region"],
    }
    return {
        "title": f"Analysis report: {inputs['dataset']}",
        "metrics": metrics,
        "sections": [
            {"heading": "Data quality",
             "body": f"{inputs['rows_clean']} of {inputs['rows_total']} rows "
                     f"survived cleaning."},
            {"heading": "Findings",
             "body": f"Total revenue {inputs['total_revenue']:.2f}; top "
                     f"category {inputs['top_category']}; strongest region "
                     f"{max(inputs['revenue_by_region'], key=inputs['revenue_by_region'].get)}."},
            {"heading": "Appendix",
             "body": f"Period {inputs['first_date']} to {inputs['last_date']}. "
                     "Numbers verified against results.json; prose is not verified."},
        ],
    }


def render_markdown(report):
    lines = [f"# {report['title']}", ""]
    for section in report["sections"]:
        lines += [f"## {section['heading']}", "", section["body"], ""]
    lines += [
        "```json",
        json.dumps(report["metrics"], indent=2),
        "```",
        "",
    ]
    return "\n".join(lines)


def write_report(report, markdown, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out_dir / "report.md").write_text(markdown, encoding="utf-8")


def main(argv=None):
    inputs = load_inputs(SCENARIO_DIR)
    report = build_report(inputs)
    write_report(report, render_markdown(report), OUT_DIR)
    print(f"wrote report.md + report.json to {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
