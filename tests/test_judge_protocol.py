"""Dependency-free protocol tests for the strict v8 VLM judge."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/eval_vlm_judge_api.py"
SPEC = importlib.util.spec_from_file_location("v8_eval_vlm_judge_api", SCRIPT)
assert SPEC and SPEC.loader
JUDGE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = JUDGE
SPEC.loader.exec_module(JUDGE)


def complete_scores() -> dict[str, int]:
    return {name: index * 10 for index, name in enumerate(JUDGE.RAW_DIMS, 1)}


class StrictOutputTests(unittest.TestCase):
    def test_exact_integer_schema_is_accepted(self) -> None:
        scores = complete_scores()
        self.assertEqual(JUDGE.parse_raw_scores(json.dumps(scores)), scores)

    def test_missing_extra_string_and_boolean_values_are_rejected(self) -> None:
        cases = []
        missing = complete_scores()
        missing.pop(JUDGE.RAW_DIMS[0])
        cases.append(missing)
        extra = {**complete_scores(), "explanation": 1}
        cases.append(extra)
        string_value = complete_scores()
        string_value[JUDGE.RAW_DIMS[0]] = "10"
        cases.append(string_value)
        boolean_value = complete_scores()
        boolean_value[JUDGE.RAW_DIMS[0]] = True
        cases.append(boolean_value)

        for value in cases:
            with self.subTest(value=value), self.assertRaises(JUDGE.JudgeResponseError):
                JUDGE.parse_raw_scores(json.dumps(value))

    def test_duplicate_keys_and_nonstandard_nan_are_rejected(self) -> None:
        fields = [f'"{name}":{index * 10}' for index, name in enumerate(JUDGE.RAW_DIMS, 1)]
        duplicate = "{" + ",".join([*fields, '"text_accuracy":10']) + "}"
        nan_value = "{" + ",".join(
            '"text_accuracy":NaN' if item.startswith('"text_accuracy"') else item
            for item in fields
        ) + "}"

        for text in (duplicate, nan_value):
            with self.subTest(text=text), self.assertRaises(JUDGE.JudgeResponseError):
                JUDGE.parse_raw_scores(text)

    def test_reference_preserves_every_region_and_field(self) -> None:
        regions = [
            {
                "id": f"region_{index}",
                "text": "x" * (250 + index),
                "position": "middle-center",
                "size": "small",
                "type": "body",
                "carrier": "document",
                "importance": "high",
            }
            for index in range(13)
        ]
        prompt = {
            "prompt_id": "TEST",
            "category": "article",
            "level": "L3",
            "language": "EN",
            "prompt": "generation instruction",
            "gt_regions": regions,
            "stats": {"total_chars": sum(len(row["text"]) for row in regions)},
        }
        reference = JUDGE.build_reference(prompt)
        self.assertNotIn("prompt", reference)
        self.assertEqual(reference["gt_regions"], regions)
        self.assertEqual(len(reference["gt_regions"]), 13)
        user_text = JUDGE.build_user_text(reference)
        self.assertIn("x" * 262, user_text)
        self.assertIn("BEGIN_UNTRUSTED_REFERENCE_JSON", user_text)

    def test_prompt_id_cannot_escape_sample_directory(self) -> None:
        prompt = {
            "prompt_id": "../outside",
            "category": "article",
            "level": "L1",
            "language": "EN",
            "prompt": "generation instruction",
            "gt_regions": [
                {
                    "id": "region_0",
                    "text": "required",
                    "position": "center",
                    "size": "small",
                    "type": "body",
                    "carrier": "document",
                    "importance": "high",
                }
            ],
        }
        with self.assertRaises(JUDGE.EvaluationError):
            JUDGE.validate_prompt_row(prompt, 1)

    def test_coverage_separates_generation_failures_from_quality(self) -> None:
        rows = [
            {
                "prompt_id": "P1",
                "status": "success",
                "found": True,
                "valid_artifact": True,
                "eligible_for_judge": True,
                "judge_attempted": True,
                "generation": {"status": "success"},
            },
            {
                "prompt_id": "P1",
                "status": "missing",
                "found": False,
                "valid_artifact": False,
                "eligible_for_judge": False,
                "judge_attempted": False,
                "generation": {"status": "safety_rejected"},
            },
            {
                "prompt_id": "P2",
                "status": "missing",
                "found": False,
                "valid_artifact": False,
                "eligible_for_judge": False,
                "judge_attempted": False,
                "generation": {"status": "failed"},
            },
            {
                "prompt_id": "P2",
                "status": "missing",
                "found": False,
                "valid_artifact": False,
                "eligible_for_judge": False,
                "judge_attempted": False,
                "generation": {"status": "planned"},
            },
        ]
        coverage = JUDGE.coverage_summary(rows, num_samples=2)
        self.assertEqual(coverage["planned_images"], 4)
        self.assertEqual(coverage["judge_success"], 1)
        self.assertEqual(coverage["generation_safety_rejected"], 1)
        self.assertEqual(coverage["generation_failed"], 1)
        self.assertEqual(coverage["missing_unknown"], 1)
        self.assertEqual(coverage["prompts_scored"], 1)
        self.assertEqual(coverage["prompts_complete"], 0)

    def test_resume_rejects_null_or_internally_inconsistent_scores(self) -> None:
        raw = complete_scores()
        reporting = JUDGE.aggregate_to_four_dims(raw)
        composite = JUDGE.compute_composite(reporting)
        valid = {
            "status": "success",
            "row_key": "P::1",
            "hashes": {"evaluation_key_sha256": "a" * 64},
            "scores": {"raw": raw, "reporting": reporting, "composite": composite},
            **raw,
            **reporting,
            "composite": composite,
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "resume.jsonl"
            path.write_text(json.dumps(valid) + "\n", encoding="utf-8")
            self.assertEqual(len(JUDGE.load_resume_rows([path])), 1)

            for corrupt in (
                {**valid, "scores": None},
                {**valid, "composite": composite + 1},
                {
                    **valid,
                    "scores": {**valid["scores"], "reporting": {**reporting, "text_clarity": 1.0}},
                },
            ):
                path.write_text(json.dumps(corrupt) + "\n", encoding="utf-8")
                self.assertEqual(JUDGE.load_resume_rows([path]), {})

    def test_unknown_image_tokens_still_detects_definite_text_overflow(self) -> None:
        args = Namespace(
            judge_tokenizer=None,
            model_name=None,
            judge_tokenizer_revision=None,
            judge_model_revision=None,
            judge_context_tokens=100,
            judge_image_token_reserve=-1,
            max_output_tokens=60,
            judge_safety_tokens=50,
            allow_tokenizer_download=False,
            trust_remote_code=False,
        )
        auditor = JUDGE.JudgeTokenizerAuditor(args)
        auditor.load_status = "loaded"

        class FakeTokenizer:
            def apply_chat_template(self, *args, **kwargs):
                return list(range(10))

        auditor.tokenizer = FakeTokenizer()
        result = auditor.audit("reference")
        self.assertIs(result["fits_context"], False)
        self.assertEqual(
            result["budget_check_basis"],
            "definite_overflow_text+output+safety_lower_bound",
        )


if __name__ == "__main__":
    unittest.main()
