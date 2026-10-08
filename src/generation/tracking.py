"""Generation provenance, cache validation, and tokenizer preflight helpers."""

from __future__ import annotations

import hashlib
import inspect
import json
import os
import re
import shutil
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "ultratext-generation-v8/1"
SIDECAR_SUFFIX = ".generation.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def sha256_json(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def sha256_file(path: str | os.PathLike[str]) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_prompts(path: str | os.PathLike[str]) -> list[dict[str, Any]]:
    prompts: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    with open(path, "r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc.msg}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number}: expected a JSON object")
            prompt_id = value.get("prompt_id")
            prompt = value.get("prompt")
            gt_regions = value.get("gt_regions")
            if not isinstance(prompt_id, str) or not prompt_id:
                raise ValueError(f"{path}:{line_number}: prompt_id must be a non-empty string")
            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", prompt_id) or prompt_id in (".", ".."):
                raise ValueError(f"{path}:{line_number}: prompt_id is not safe for use as a filename")
            if prompt_id in seen_ids:
                raise ValueError(f"{path}:{line_number}: duplicate prompt_id {prompt_id!r}")
            if not isinstance(prompt, str) or not prompt:
                raise ValueError(f"{path}:{line_number}: prompt must be a non-empty string")
            if not isinstance(gt_regions, list):
                raise ValueError(f"{path}:{line_number}: gt_regions must be a list")
            if any(not isinstance(region, dict) for region in gt_regions):
                raise ValueError(f"{path}:{line_number}: every gt_regions entry must be an object")
            seen_ids.add(prompt_id)
            prompts.append(value)
    return prompts


def model_artifact_fingerprint(model_path: str | os.PathLike[str]) -> dict[str, Any] | None:
    """Hash cheap config/index artifacts without reading checkpoint weight shards."""
    root = Path(model_path)
    if not root.is_dir():
        return None
    selected: list[Path] = []
    exact_names = {
        "config.json",
        "model_index.json",
        "scheduler_config.json",
        "tokenizer_config.json",
        "special_tokens_map.json",
        "generation_config.json",
    }
    for path in root.rglob("*.json"):
        if path.name in exact_names or path.name.endswith(".index.json"):
            selected.append(path)
    if not selected:
        return None
    files = [
        {"path": os.fspath(path.relative_to(root)), "sha256": sha256_file(path), "size_bytes": path.stat().st_size}
        for path in sorted(selected)
    ]
    return {
        "method": "config_and_index_files",
        "is_weights_hash": False,
        "file_count": len(files),
        "files": files,
        "sha256": sha256_json(files),
    }


def tokenizer_artifact_fingerprint(model_path: str | os.PathLike[str]) -> dict[str, Any] | None:
    """Hash known tokenizer assets when the model is available as a local directory."""
    root = Path(model_path)
    if not root.is_dir():
        return None
    names = {
        "tokenizer.json",
        "tokenizer.model",
        "tokenizer_config.json",
        "special_tokens_map.json",
        "added_tokens.json",
        "vocab.json",
        "vocab.txt",
        "merges.txt",
        "spiece.model",
        "sentencepiece.bpe.model",
    }
    selected = sorted(path for path in root.rglob("*") if path.is_file() and path.name in names)
    if not selected:
        return None
    files = [
        {"path": os.fspath(path.relative_to(root)), "sha256": sha256_file(path), "size_bytes": path.stat().st_size}
        for path in selected
    ]
    return {
        "method": "known_local_tokenizer_files",
        "file_count": len(files),
        "files": files,
        "sha256": sha256_json(files),
    }


def _atomic_path(path: str | os.PathLike[str]) -> tuple[int, str]:
    target = os.path.abspath(os.fspath(path))
    os.makedirs(os.path.dirname(target), exist_ok=True)
    return tempfile.mkstemp(prefix=f".{os.path.basename(target)}.", suffix=".tmp", dir=os.path.dirname(target))


def write_json_atomic(path: str | os.PathLike[str], value: Any) -> None:
    fd, temporary = _atomic_path(path)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def write_jsonl_atomic(path: str | os.PathLike[str], rows: Iterable[dict[str, Any]]) -> None:
    fd, temporary = _atomic_path(path)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            for row in rows:
                handle.write(canonical_json_bytes(row).decode("utf-8"))
                handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def read_json(path: str | os.PathLike[str]) -> dict[str, Any] | None:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            value = json.load(handle)
        return value if isinstance(value, dict) else None
    except (OSError, ValueError, TypeError):
        return None


def sidecar_path(image_path: str | os.PathLike[str]) -> str:
    return f"{os.fspath(image_path)}{SIDECAR_SUFFIX}"


def save_image_atomic(image: Any, path: str | os.PathLike[str]) -> None:
    fd, temporary = _atomic_path(path)
    os.close(fd)
    try:
        image.save(temporary, format="PNG")
        with open(temporary, "rb") as handle:
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def save_bytes_atomic(value: bytes, path: str | os.PathLike[str]) -> None:
    fd, temporary = _atomic_path(path)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(value)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def base_record(
    *,
    prompt_id: Any,
    sample_index: int,
    prompt_text: str,
    gt_regions: list[dict[str, Any]],
    image_path: str,
    output_dir: str,
    model_identifier: str,
    model_revision: str | None,
    generation_config: dict[str, Any],
    model_artifact: dict[str, Any] | None,
    seed: int | None,
    tokenizer_audit: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "prompt_id": str(prompt_id),
        "sample_index": int(sample_index),
        "status": "planned",
        "action": "planned",
        "prompt_sha256": sha256_text(prompt_text),
        "gt_sha256": sha256_json(gt_regions),
        "image_path": os.path.relpath(image_path, output_dir),
        "image_sha256": None,
        "model_identifier": model_identifier,
        "model_revision": model_revision,
        "model_identity_sha256": sha256_json(
            {"model_identifier": model_identifier, "model_revision": model_revision}
        ),
        "model_artifact_fingerprint": model_artifact,
        "model_artifact_fingerprint_sha256": model_artifact.get("sha256") if model_artifact else None,
        "tokenizer_identifier": tokenizer_audit.get("tokenizer_identifier"),
        "tokenizer_revision": tokenizer_audit.get("tokenizer_revision"),
        "tokenizer_identity_sha256": tokenizer_audit.get("tokenizer_identity_sha256"),
        "tokenizer_artifact_fingerprint_sha256": tokenizer_audit.get(
            "tokenizer_artifact_fingerprint_sha256"
        ),
        "config_sha256": sha256_json(generation_config),
        "generation_config": generation_config,
        "seed": seed,
        "tokenizer_audit": tokenizer_audit,
        "updated_at": utc_now(),
    }


_BINDING_FIELDS = (
    "schema_version",
    "prompt_id",
    "sample_index",
    "prompt_sha256",
    "gt_sha256",
    "model_identifier",
    "model_revision",
    "model_identity_sha256",
    "model_artifact_fingerprint_sha256",
    "tokenizer_identifier",
    "tokenizer_revision",
    "tokenizer_identity_sha256",
    "tokenizer_artifact_fingerprint_sha256",
    "config_sha256",
    "seed",
)


def validate_existing(image_path: str, expected: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    """Return missing, valid, or stale plus a manifest-ready record."""
    record = dict(expected)
    if not os.path.exists(image_path):
        return "missing", record

    observed_hash = sha256_file(image_path)
    observed = read_json(sidecar_path(image_path))
    reasons: list[str] = []
    if observed is None:
        reasons.append("missing_or_invalid_sidecar")
    else:
        if observed.get("status") != "success":
            reasons.append("sidecar_status_not_success")
        for field in _BINDING_FIELDS:
            if observed.get(field) != expected.get(field):
                reasons.append(f"{field}_mismatch")
        if observed.get("image_sha256") != observed_hash:
            reasons.append("image_sha256_mismatch")

    if not reasons:
        record.update(observed or {})
        record.update(
            status="success",
            action="skipped_verified",
            image_sha256=observed_hash,
            updated_at=utc_now(),
        )
        return "valid", record

    record.update(
        status="stale",
        action="stale_not_reused",
        image_sha256=observed_hash,
        stale_reasons=sorted(set(reasons)),
        observed_binding={field: observed.get(field) for field in _BINDING_FIELDS} if observed else None,
        updated_at=utc_now(),
    )
    return "stale", record


def archive_stale(image_path: str, output_dir: str) -> list[str]:
    """Move an explicitly regenerated stale artifact into a provenance archive."""
    image = Path(image_path)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    archive_dir = Path(output_dir) / ".stale"
    archive_dir.mkdir(parents=True, exist_ok=True)
    archived: list[str] = []
    for source in (image, Path(sidecar_path(image_path))):
        if not source.exists():
            continue
        destination = archive_dir / f"{source.name}.{stamp}"
        shutil.move(os.fspath(source), os.fspath(destination))
        archived.append(os.path.relpath(destination, output_dir))
    return archived


def persist_record(image_path: str, record: dict[str, Any]) -> dict[str, Any]:
    record = dict(record)
    record["updated_at"] = utc_now()
    write_json_atomic(sidecar_path(image_path), record)
    return record


def successful_record(image_path: str, expected: dict[str, Any], action: str = "generated") -> dict[str, Any]:
    record = dict(expected)
    record.update(
        status="success",
        action=action,
        image_sha256=sha256_file(image_path),
        updated_at=utc_now(),
    )
    return persist_record(image_path, record)


def terminal_record(
    image_path: str,
    expected: dict[str, Any],
    status: str,
    action: str,
    **details: Any,
) -> dict[str, Any]:
    record = dict(expected)
    record.update(status=status, action=action, image_sha256=None, **details)
    return persist_record(image_path, record)


def _extract_ids(value: Any) -> Any:
    if isinstance(value, dict):
        return value.get("input_ids")
    return getattr(value, "input_ids", None)


def _token_count(value: Any) -> int | None:
    if value is None:
        return None
    shape = getattr(value, "shape", None)
    if shape is not None and len(shape) >= 1:
        return int(shape[-1])
    if isinstance(value, (list, tuple)):
        if not value:
            return 0
        first = value[0]
        if isinstance(first, (list, tuple)):
            return len(first)
        return len(value)
    return None


def _reasonable_limit(value: Any) -> int | None:
    return int(value) if isinstance(value, int) and 0 < value < 1_000_000 else None


def require_explicit_pipeline_limit(pipe: Any, requested: int, pipeline_name: str) -> None:
    if not requested:
        return
    try:
        parameters = inspect.signature(pipe.__call__).parameters
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValueError(
            f"Cannot verify max_sequence_length support for {pipeline_name}; refusing an audit/generation mismatch"
        ) from exc
    if "max_sequence_length" not in parameters:
        raise ValueError(
            f"{pipeline_name} does not explicitly expose max_sequence_length; "
            "refusing an audit/generation limit mismatch"
        )


def _pipeline_limit(pipe: Any, override: int | None) -> tuple[int | None, str | None]:
    if override and override > 0:
        return override, "cli_override"
    # The public call default is authoritative because this is the path used for generation.
    for method_name in ("__call__", "encode_prompt"):
        try:
            parameter = inspect.signature(getattr(pipe, method_name)).parameters.get("max_sequence_length")
        except (AttributeError, TypeError, ValueError):
            parameter = None
        limit = _reasonable_limit(parameter.default) if parameter is not None else None
        if limit:
            return limit, f"{method_name}_signature_default"
    return None, None


def _audit_tokenizer(
    tokenizer: Any,
    prompt: str,
    limit: int | None,
    name: str,
    fallback_revision: str | None,
) -> dict[str, Any]:
    tokenizer_limit = _reasonable_limit(getattr(tokenizer, "model_max_length", None))
    effective_limit = limit or tokenizer_limit
    limit_source = "pipeline" if limit else ("tokenizer.model_max_length" if tokenizer_limit else None)
    init_kwargs = getattr(tokenizer, "init_kwargs", None)
    init_kwargs = init_kwargs if isinstance(init_kwargs, dict) else {}
    tokenizer_identifier = getattr(tokenizer, "name_or_path", None) or init_kwargs.get("name_or_path")
    tokenizer_revision = init_kwargs.get("revision") or init_kwargs.get("_commit_hash") or fallback_revision
    revision_source = "tokenizer" if init_kwargs.get("revision") or init_kwargs.get("_commit_hash") else "model_revision_fallback"
    result: dict[str, Any] = {
        "name": name,
        "class": tokenizer.__class__.__name__,
        "tokenizer_identifier": tokenizer_identifier or tokenizer.__class__.__name__,
        "tokenizer_revision": tokenizer_revision,
        "tokenizer_revision_source": revision_source if tokenizer_revision else "unknown",
        "raw_tokens": None,
        "effective_tokens": None,
        "max_tokens": effective_limit,
        "max_tokens_source": limit_source,
        "truncated": None,
        "input_truncated": None,
    }
    try:
        raw = tokenizer(
            prompt,
            add_special_tokens=True,
            padding=False,
            truncation=False,
            return_attention_mask=False,
        )
        raw_count = _token_count(_extract_ids(raw))
        result["raw_tokens"] = raw_count
        if effective_limit is None:
            result["effective_tokens"] = raw_count
            result["truncated"] = None
            result["input_truncated"] = None
        else:
            encoded = tokenizer(
                prompt,
                add_special_tokens=True,
                padding=False,
                truncation=True,
                max_length=effective_limit,
                return_attention_mask=False,
            )
            effective_count = _token_count(_extract_ids(encoded))
            result["effective_tokens"] = effective_count
            result["truncated"] = bool(raw_count is not None and raw_count > effective_limit)
            result["input_truncated"] = result["truncated"]
    except Exception as exc:  # Tokenizer implementations expose different call signatures.
        result["error_type"] = type(exc).__name__
    return result


def audit_pipeline_prompt(
    pipe: Any,
    prompt: str,
    max_sequence_length: int | None = None,
    model_revision: str | None = None,
) -> dict[str, Any]:
    limit, limit_source = _pipeline_limit(pipe, max_sequence_length)
    audits: list[dict[str, Any]] = []
    for name in ("tokenizer", "tokenizer_2", "tokenizer_3"):
        tokenizer = getattr(pipe, name, None)
        if tokenizer is not None:
            item = _audit_tokenizer(tokenizer, prompt, limit, name, model_revision)
            if item.get("max_tokens_source") == "pipeline":
                item["max_tokens_source"] = limit_source
            audits.append(item)

    usable = [item for item in audits if item.get("raw_tokens") is not None]
    if not usable:
        identities = [
            {
                "name": item["name"],
                "identifier": item["tokenizer_identifier"],
                "revision": item["tokenizer_revision"],
                "class": item["class"],
            }
            for item in audits
        ]
        return {
            "status": "unknown",
            "method": "pipeline_tokenizer_preflight",
            "confidence": "unknown",
            "raw_tokens": None,
            "effective_tokens": None,
            "max_tokens": limit,
            "truncated": None,
            "input_truncated": None,
            "tokenizer_identifier": audits[0].get("tokenizer_identifier") if audits else None,
            "tokenizer_revision": audits[0].get("tokenizer_revision") if audits else None,
            "tokenizer_identity_sha256": sha256_json(identities) if identities else None,
            "raw_characters": len(prompt),
            "raw_utf8_bytes": len(prompt.encode("utf-8")),
            "tokenizers": audits,
        }

    primary = usable[0]
    identities = [
        {
            "name": item["name"],
            "identifier": item["tokenizer_identifier"],
            "revision": item["tokenizer_revision"],
            "class": item["class"],
        }
        for item in audits
    ]
    known_flags = [item["truncated"] for item in usable if item.get("truncated") is not None]
    return {
        "status": "checked",
        "method": "pipeline_tokenizer_preflight",
        "confidence": "medium",
        "raw_tokens": primary.get("raw_tokens"),
        "effective_tokens": primary.get("effective_tokens"),
        "max_tokens": primary.get("max_tokens"),
        "truncated": any(known_flags) if known_flags else None,
        "input_truncated": any(known_flags) if known_flags else None,
        "tokenizer_identifier": primary.get("tokenizer_identifier"),
        "tokenizer_revision": primary.get("tokenizer_revision"),
        "tokenizer_identity_sha256": sha256_json(identities),
        "raw_characters": len(prompt),
        "raw_utf8_bytes": len(prompt.encode("utf-8")),
        "tokenizers": audits,
        "note": "Uses the loaded pipeline tokenizer and encode limit; pipeline templates may add tokens.",
    }


def black_box_tokenizer_audit(prompt: str) -> dict[str, Any]:
    return {
        "status": "unknown",
        "method": "black_box_api",
        "confidence": "unknown",
        "raw_tokens": None,
        "effective_tokens": None,
        "max_tokens": None,
        "truncated": None,
        "input_truncated": None,
        "tokenizer_identifier": None,
        "tokenizer_revision": None,
        "tokenizer_identity_sha256": None,
        "raw_characters": len(prompt),
        "raw_utf8_bytes": len(prompt.encode("utf-8")),
        "note": "Provider tokenizer and effective input limit are not observable.",
    }


def manifest_sort_key(record: dict[str, Any]) -> tuple[str, int]:
    return str(record.get("prompt_id", "")), int(record.get("sample_index", 0))


def write_manifest(output_dir: str, records: Iterable[dict[str, Any]]) -> str:
    path = os.path.join(output_dir, "generation_manifest.jsonl")
    write_jsonl_atomic(path, sorted(records, key=manifest_sort_key))
    return path


def write_tokenizer_audit(output_dir: str, rows: Iterable[dict[str, Any]]) -> str:
    path = os.path.join(output_dir, "tokenizer_audit.jsonl")
    write_jsonl_atomic(path, sorted(rows, key=lambda row: str(row.get("prompt_id", ""))))
    return path


def write_rank_shard(output_dir: str, rank: int, records: Iterable[dict[str, Any]]) -> str:
    path = os.path.join(output_dir, f".generation_manifest.rank{rank}.jsonl")
    write_jsonl_atomic(path, records)
    return path


def read_jsonl(path: str | os.PathLike[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number}: expected a JSON object")
            rows.append(value)
    return rows


def merge_rank_shards(output_dir: str, world_size: int) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    shard_paths = [os.path.join(output_dir, f".generation_manifest.rank{rank}.jsonl") for rank in range(world_size)]
    for path in shard_paths:
        records.extend(read_jsonl(path))
    write_manifest(output_dir, records)
    for path in shard_paths:
        os.unlink(path)
    return sorted(records, key=manifest_sort_key)


def status_counts(records: Iterable[dict[str, Any]]) -> dict[str, int]:
    return dict(sorted(Counter(str(record.get("status", "unknown")) for record in records).items()))


def write_run_summary(
    output_dir: str,
    *,
    generation_config: dict[str, Any],
    prompt_file: str,
    prompt_count: int,
    sample_count: int,
    records: list[dict[str, Any]],
) -> str:
    summary = {
        "schema_version": SCHEMA_VERSION,
        "created_at": utc_now(),
        "prompt_file": os.path.abspath(prompt_file),
        "prompt_file_sha256": sha256_file(prompt_file),
        "prompt_count": prompt_count,
        "planned_samples": sample_count,
        "status_counts": status_counts(records),
        "model_identifier": generation_config.get("model_identifier"),
        "model_revision": generation_config.get("model_revision"),
        "model_identity_sha256": sha256_json(
            {
                "model_identifier": generation_config.get("model_identifier"),
                "model_revision": generation_config.get("model_revision"),
            }
        ),
        "model_artifact_fingerprint": generation_config.get("model_artifact_fingerprint"),
        "model_artifact_fingerprint_sha256": (
            generation_config.get("model_artifact_fingerprint") or {}
        ).get("sha256"),
        "tokenizer_artifact_fingerprint": generation_config.get("tokenizer_artifact_fingerprint"),
        "tokenizer_artifact_fingerprint_sha256": (
            generation_config.get("tokenizer_artifact_fingerprint") or {}
        ).get("sha256"),
        "tokenizer_identities": sorted(
            {
                (
                    record.get("tokenizer_identifier"),
                    record.get("tokenizer_revision"),
                    record.get("tokenizer_identity_sha256"),
                )
                for record in records
            },
            key=lambda identity: tuple("" if part is None else str(part) for part in identity),
        ),
        "config_sha256": sha256_json(generation_config),
        "generation_config": generation_config,
        "manifest": "generation_manifest.jsonl",
        "tokenizer_audit": "tokenizer_audit.jsonl",
    }
    path = os.path.join(output_dir, "generation_run.json")
    write_json_atomic(path, summary)
    return path
