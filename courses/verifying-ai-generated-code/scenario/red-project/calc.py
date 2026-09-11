"""Tiny arithmetic module used by the green scenario project."""


def add(left: float, right: float) -> float:
    return left + right


def slugify(value: str) -> str:
    return "-".join(part for part in value.lower().split() if part)
