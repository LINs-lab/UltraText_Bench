#!/usr/bin/env python3
"""Render the README leaderboard from the reported manuscript scores."""

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- LEADERBOARD:START -->"
END = "<!-- LEADERBOARD:END -->"
DIMENSIONS = (
    ("composite", "Composite"),
    ("text_fidelity", "Fidelity"),
    ("text_clarity", "Clarity"),
    ("spatial_quality", "Spatial"),
    ("scene_quality", "Scene"),
)
LEVELS = [(level, language) for level in ("L1", "L2", "L3") for language in ("EN", "ZH")]
GROUPS = (("open-weight", "Open-weight models"), ("api-only", "API-only models"))


def score(value):
    if type(value) not in (int, float) or not math.isfinite(value) or not 0 <= value <= 100:
        raise ValueError(f"Invalid 0–100 rating: {value!r}")
    return value


def table(rows, headers, values):
    maximum = [max(column) for column in zip(*(values(row) for row in rows))]
    lines = ["| Model | " + " | ".join(headers) + " |", "| --- | " + " | ".join(["---:"] * len(headers)) + " |"]
    for row in rows:
        name = row["model"].replace("|", "\\|")
        cells = [f"**{value:.2f}**" if value == best else f"{value:.2f}" for value, best in zip(values(row), maximum)]
        lines.append("| " + name + " | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def render(data):
    models = data["models"]
    names = [row["model"] for row in models]
    if not models or len(set(names)) != len(names) or any(not name.strip() or "\n" in name for name in names):
        raise ValueError("Model names must be nonempty and unique")
    for row in models:
        if row["access"] not in dict(GROUPS):
            raise ValueError(f"Unknown model group: {row['access']}")
        for key, _ in DIMENSIONS:
            score(row[key])
        for level, language in LEVELS:
            score(row["levels"][level][language])

    groups = [(title, sorted((row for row in models if row["access"] == key), key=lambda row: -row["composite"])) for key, title in GROUPS]
    if any(not rows for _, rows in groups):
        raise ValueError("Both reported model groups must be present")
    lines = [
        f"Reported results for **{len(models)} model configurations**, transcribed from the paper. Ratings range from 0 to 100; higher is better. Overall scores average EN/ZH prompt-macro means equally. Each group is ordered by Composite; bold marks the best value in that group.",
        "Composite weights are 60/30/5/5 for Fidelity/Clarity/Spatial/Scene. Missing or failed evaluations affect coverage, not quality means. Low/High labels denote API quality settings. See the [machine-readable scores](data/leaderboard.json) and [paper](paper/UltraText_Bench.pdf) for the reported values and their scope.",
    ]
    for title, rows in groups:
        lines += ["### " + title, table(rows, [label for _, label in DIMENSIONS], lambda row: [row[key] for key, _ in DIMENSIONS])]
    lines += ["<details>\n<summary>Composites by difficulty level and language</summary>", "L1/L2/L3 denote Hard/Very Hard/Extreme. These columns report language-specific prompt-macro composites."]
    for title, rows in groups:
        lines += ["#### " + title, table(rows, [f"{level} {language}" for level, language in LEVELS], lambda row: [row["levels"][level][language] for level, language in LEVELS])]
    lines.append("</details>")
    return "\n\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check without rewriting README.md")
    args = parser.parse_args()
    data = json.loads((ROOT / "data/leaderboard.json").read_text())
    path = ROOT / "README.md"
    current = path.read_text()
    if current.count(START) != 1 or current.count(END) != 1:
        raise SystemExit("README must contain exactly one leaderboard marker pair")
    prefix, rest = current.split(START)
    _, suffix = rest.split(END)
    expected = prefix + START + "\n\n" + render(data) + "\n\n" + END + suffix
    if args.check:
        if current != expected:
            raise SystemExit("Leaderboard is stale; run python scripts/render_leaderboard.py")
        print(f"PASS: README matches {len(data['models'])} reported model rows")
    else:
        path.write_text(expected)
        print(f"Rendered {len(data['models'])} reported model rows")


if __name__ == "__main__":
    main()
