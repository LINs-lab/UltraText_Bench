#!/usr/bin/env python3
"""Build the static project page from the repository's reported results."""

import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site"
OUTPUT = ROOT / "_site"
METRICS = [
    ("composite", "Composite"),
    ("text_fidelity", "Fidelity"),
    ("text_clarity", "Clarity"),
    ("spatial_quality", "Spatial"),
    ("scene_quality", "Scene"),
]


def main():
    data = json.loads((ROOT / "data/leaderboard.json").read_text(encoding="utf-8"))
    models = data["models"]
    if len(models) != 24 or len({model["model"] for model in models}) != 24:
        raise ValueError("Update the page's benchmark counts before changing the 24-model release.")
    for model in models:
        if model["access"] not in {"open-weight", "api-only"}:
            raise ValueError("Unknown model access category")
        scores = [model[key] for key, _ in METRICS]
        scores += [model["levels"][level][language] for level in ("L1", "L2", "L3") for language in ("EN", "ZH")]
        if not all(isinstance(value, (int, float)) and 0 <= value <= 100 for value in scores):
            raise ValueError("Expected finite ratings between 0 and 100")
    citation = re.search(r"```bibtex\s*\n(.*?)\n```", (ROOT / "README.md").read_text(encoding="utf-8"), re.S)
    if not citation:
        raise ValueError("README must include the paper's BibTeX citation")

    headers = '<th scope="col">#</th><th scope="col" aria-sort="none"><button type="button" data-sort="model">Model</button></th>'
    for key, label in METRICS:
        order = "descending" if key == "composite" else "none"
        arrow = " ↓" if key == "composite" else ""
        headers += f'<th scope="col" aria-sort="{order}"><button type="button" data-sort="{key}">{label}{arrow}</button></th>'
    rows = []
    for rank, model in enumerate(sorted(models, key=lambda model: (-model["composite"], model["model"])), 1):
        access = "Open-weight" if model["access"] == "open-weight" else "API-only"
        cells = f'<td>{rank}</td><td><span class="model-name">{html.escape(model["model"])}</span><span class="access-label">{access}</span></td>'
        for key, _ in METRICS:
            style = ' class="composite-cell"' if key == "composite" else ""
            cells += f'<td{style}>{model[key]:.2f}</td>'
        rows.append(f"<tr>{cells}</tr>")
    lookup = {model["model"]: model for model in models}
    substitutions = {
        "TABLE_HEAD": headers,
        "TABLE_ROWS": "\n".join(rows),
        "LEADERBOARD_DATA": json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026"),
        "CITATION": html.escape(citation.group(1)),
        "Z_CLARITY": f'{lookup["Z-Image-Turbo"]["text_clarity"]:.2f}',
        "Z_FIDELITY": f'{lookup["Z-Image-Turbo"]["text_fidelity"]:.2f}',
        "Q_L1": f'{lookup["Qwen-Image-2512"]["levels"]["L1"]["EN"]:.2f}',
        "Q_L3": f'{lookup["Qwen-Image-2512"]["levels"]["L3"]["EN"]:.2f}',
    }
    template = (SOURCE / "index.html").read_text(encoding="utf-8")
    rendered = re.sub(r"__([A-Z_0-9]+)__", lambda match: substitutions[match.group(1)], template)
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    shutil.copytree(SOURCE, OUTPUT, ignore=shutil.ignore_patterns("*.md", ".DS_Store"))
    (OUTPUT / "index.html").write_text(rendered, encoding="utf-8")
    (OUTPUT / "data").mkdir()
    shutil.copy2(ROOT / "data/leaderboard.json", OUTPUT / "data/leaderboard.json")
    (OUTPUT / ".nojekyll").touch()
    total = sum(path.stat().st_size for path in OUTPUT.rglob("*") if path.is_file())
    print(f"Built {len(models)} model configurations into {OUTPUT} ({total / 1024 / 1024:.2f} MiB)")


if __name__ == "__main__":
    main()
