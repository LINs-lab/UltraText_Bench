"""The paused OCR entry point must remain safe to import without OCR deps."""

from __future__ import annotations

import importlib.util
import io
import sys
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src/evaluation/layer1_ocr.py"


class OcrPauseTests(unittest.TestCase):
    def test_default_run_stops_before_loading_diagnostic_dependencies(self) -> None:
        spec = importlib.util.spec_from_file_location("v8_layer1_ocr", SCRIPT)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        error = io.StringIO()
        with redirect_stderr(error):
            status = module.main(SimpleNamespace(enable_diagnostic=False))

        self.assertEqual(status, 2)
        self.assertIn("OCR is paused in v8", error.getvalue())


if __name__ == "__main__":
    unittest.main()
