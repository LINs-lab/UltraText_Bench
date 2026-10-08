"""Regression tests for v8 prompt audit hard gates and observation signals."""

from __future__ import annotations

import copy
import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/rebuild_audit_snapshots.py"
SPEC = importlib.util.spec_from_file_location("v8_rebuild_audit_snapshots", SCRIPT)
assert SPEC and SPEC.loader
AUDIT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = AUDIT
SPEC.loader.exec_module(AUDIT)


def valid_row(prompt_text: str = "Neutral sample text") -> dict:
    gt_text = "x" * 250
    return {
        "prompt_id": "A1_L1_EN_001",
        "category": "sign",
        "level": "L1",
        "language": "EN",
        "prompt": f"{prompt_text}\n{gt_text}",
        "gt_regions": [
            {
                "id": "region_0",
                "text": gt_text,
                "position": "top-center",
                "size": "large",
                "type": "title",
                "carrier": "sign",
                "importance": "high",
            }
        ],
        "stats": {
            "total_chars": 250,
            "total_words": 1,
            "total_regions": 1,
        },
    }


class ObservationSignalTests(unittest.TestCase):
    def test_clear_text_has_no_observations(self) -> None:
        self.assertEqual(
            AUDIT.observation_signals("ordinary fictional scene"),
            {
                "political_term_observed": False,
                "contact_pattern_observed": False,
            },
        )

    def test_patterns_are_reported_as_observations(self) -> None:
        signals = AUDIT.observation_signals(
            "Joe Biden and contact@example.org are rendered as sample text"
        )
        self.assertTrue(signals["political_term_observed"])
        self.assertTrue(signals["contact_pattern_observed"])

    def test_observations_do_not_fail_source_validation(self) -> None:
        row = valid_row("Joe Biden contact@example.org")
        checks = AUDIT.validate_source_row(row, "test-row")
        self.assertTrue(checks["political_term_observed"])
        self.assertTrue(checks["contact_pattern_observed"])
        self.assertTrue(all(checks[name] for name in AUDIT.SOURCE_HARD_CHECK_NAMES))
        self.assertTrue(
            set(AUDIT.DELIVERY_HARD_CHECK_NAMES).isdisjoint(AUDIT.OBSERVATION_NAMES)
        )

        source = AUDIT.SourceSnapshot({}, {}, (row,), {row["prompt_id"]: row})
        signoff = AUDIT.Signoff(
            b"{}",
            "0" * 64,
            "test reviewer",
            "2026-07-18T00:00:00Z",
            frozenset({row["prompt_id"]}),
            {},
        )
        rendered = AUDIT.render_build(source, {row["prompt_id"]: checks}, signoff)
        text = rendered.decode("utf-8")
        self.assertIn("| OBSERVED | OBSERVED | PASS |", text)
        self.assertIn("窄范围政治关键词 | 1/1 | 100.0%", text)

    def test_content_scaffold_remains_a_hard_failure(self) -> None:
        row = valid_row("Text region 1")
        with self.assertRaisesRegex(AUDIT.AuditError, "content_scan"):
            AUDIT.validate_source_row(row, "test-row")

    def test_structural_failure_remains_a_hard_failure(self) -> None:
        row = copy.deepcopy(valid_row())
        row["gt_regions"][0]["id"] = "region_9"
        with self.assertRaisesRegex(AUDIT.AuditError, "must be region_0"):
            AUDIT.validate_source_row(row, "test-row")


if __name__ == "__main__":
    unittest.main()
