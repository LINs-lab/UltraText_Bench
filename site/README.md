# Project page

The bilingual static site is published at <https://lins-lab.github.io/UltraText_Bench/>. Add `?lang=zh` to open the Chinese version directly.

Build and preview with Python 3.9 or later (no third-party dependencies):

```bash
python3 scripts/build_project_page.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory _site
```

The build reads the reported scores from `data/leaderboard.json` and the BibTeX entry from the root README. `_site/` is generated output. Static table rows remain readable without JavaScript; JavaScript provides filtering, sorting, language switching, image enlargement, and citation copying.

The `Project page` GitHub Actions workflow deploys changes on `main`. In repository Settings → Pages, select **GitHub Actions** as the build source. Only the generated `_site/` directory is published.
