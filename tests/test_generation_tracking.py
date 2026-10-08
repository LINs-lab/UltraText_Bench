"""Dependency-free provenance tests for generated image cache binding."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src/generation/tracking.py"
SPEC = importlib.util.spec_from_file_location("v8_generation_tracking", SCRIPT)
assert SPEC and SPEC.loader
TRACKING = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = TRACKING
SPEC.loader.exec_module(TRACKING)


class GenerationBindingTests(unittest.TestCase):
    def expected(self, directory: Path, *, gt_text: str = "complete GT") -> dict:
        image_path = directory / "A1_L1_EN_001_1.png"
        return TRACKING.base_record(
            prompt_id="A1_L1_EN_001",
            sample_index=1,
            prompt_text="full generation prompt",
            gt_regions=[{"id": "region_0", "text": gt_text}],
            image_path=str(image_path),
            output_dir=str(directory),
            model_identifier="model/name",
            model_revision="revision-1",
            generation_config={"steps": 20},
            model_artifact={"sha256": "a" * 64},
            seed=43,
            tokenizer_audit={"status": "checked", "input_truncated": False},
        )

    def test_matching_sidecar_and_image_are_reused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            image_path = directory / "A1_L1_EN_001_1.png"
            image_path.write_bytes(b"not-a-real-png-but-hashable")
            expected = self.expected(directory)
            TRACKING.successful_record(str(image_path), expected)

            status, record = TRACKING.validate_existing(str(image_path), expected)

            self.assertEqual(status, "valid")
            self.assertEqual(record["action"], "skipped_verified")
            self.assertEqual(record["image_sha256"], TRACKING.sha256_file(image_path))

    def test_changed_gt_and_changed_image_are_stale(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            image_path = directory / "A1_L1_EN_001_1.png"
            image_path.write_bytes(b"original")
            original = self.expected(directory)
            TRACKING.successful_record(str(image_path), original)

            changed_gt = self.expected(directory, gt_text="new complete GT")
            status, record = TRACKING.validate_existing(str(image_path), changed_gt)
            self.assertEqual(status, "stale")
            self.assertIn("gt_sha256_mismatch", record["stale_reasons"])

            image_path.write_bytes(b"changed")
            status, record = TRACKING.validate_existing(str(image_path), original)
            self.assertEqual(status, "stale")
            self.assertIn("image_sha256_mismatch", record["stale_reasons"])

    def test_black_box_audit_is_explicitly_unknown(self) -> None:
        audit = TRACKING.black_box_tokenizer_audit("prompt")
        self.assertEqual(audit["status"], "unknown")
        self.assertEqual(audit["method"], "black_box_api")
        self.assertIsNone(audit["input_truncated"])
        self.assertIsNone(audit["raw_tokens"])

    def test_local_artifact_fingerprints_are_self_describing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            (directory / "config.json").write_text('{"model":"one"}', encoding="utf-8")
            (directory / "tokenizer.json").write_text('{"tokenizer":"one"}', encoding="utf-8")

            model = TRACKING.model_artifact_fingerprint(directory)
            tokenizer = TRACKING.tokenizer_artifact_fingerprint(directory)
            self.assertIsNotNone(model)
            self.assertIsNotNone(tokenizer)
            assert model is not None and tokenizer is not None
            self.assertEqual(model["sha256"], TRACKING.sha256_json(model["files"]))
            self.assertEqual(tokenizer["sha256"], TRACKING.sha256_json(tokenizer["files"]))

            old_hash = tokenizer["sha256"]
            (directory / "tokenizer.json").write_text('{"tokenizer":"two"}', encoding="utf-8")
            changed = TRACKING.tokenizer_artifact_fingerprint(directory)
            self.assertIsNotNone(changed)
            assert changed is not None
            self.assertNotEqual(old_hash, changed["sha256"])

    def test_pipeline_limit_uses_generation_call_and_rejects_unsupported_override(self) -> None:
        class Tokenizer:
            model_max_length = 20

            def __call__(self, text: str, **kwargs: object) -> dict:
                ids = list(range(12))
                if kwargs.get("truncation"):
                    ids = ids[: int(kwargs["max_length"])]
                return {"input_ids": ids}

        class SupportedPipeline:
            tokenizer = Tokenizer()

            def __call__(self, prompt: str, max_sequence_length: int = 7) -> None:
                return None

            def encode_prompt(self, prompt: str, max_sequence_length: int = 9) -> None:
                return None

        class UnsupportedPipeline:
            def __call__(self, prompt: str, **kwargs: object) -> None:
                return None

        pipeline = SupportedPipeline()
        TRACKING.require_explicit_pipeline_limit(pipeline, 5, "supported")
        audit = TRACKING.audit_pipeline_prompt(pipeline, "prompt")
        self.assertEqual(audit["max_tokens"], 7)
        self.assertEqual(audit["effective_tokens"], 7)
        self.assertTrue(audit["input_truncated"])
        with self.assertRaises(ValueError):
            TRACKING.require_explicit_pipeline_limit(UnsupportedPipeline(), 5, "unsupported")


if __name__ == "__main__":
    unittest.main()
