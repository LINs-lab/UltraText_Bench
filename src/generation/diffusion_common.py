"""Shared distributed runner for local Diffusers image generators."""

from __future__ import annotations

import os
from importlib import metadata as importlib_metadata
from typing import Any, Callable

import torch
import torch.distributed as dist
from tqdm import tqdm

try:
    from .tracking import (
        archive_stale,
        audit_pipeline_prompt,
        base_record,
        load_prompts,
        merge_rank_shards,
        model_artifact_fingerprint,
        require_explicit_pipeline_limit,
        save_image_atomic,
        successful_record,
        terminal_record,
        tokenizer_artifact_fingerprint,
        validate_existing,
        sha256_json,
        write_rank_shard,
        write_run_summary,
        write_tokenizer_audit,
    )
except ImportError:  # Allows direct execution of scripts in this directory.
    from tracking import (
        archive_stale,
        audit_pipeline_prompt,
        base_record,
        load_prompts,
        merge_rank_shards,
        model_artifact_fingerprint,
        require_explicit_pipeline_limit,
        save_image_atomic,
        successful_record,
        terminal_record,
        tokenizer_artifact_fingerprint,
        validate_existing,
        sha256_json,
        write_rank_shard,
        write_run_summary,
        write_tokenizer_audit,
    )


def package_version(name: str) -> str | None:
    try:
        return importlib_metadata.version(name)
    except importlib_metadata.PackageNotFoundError:
        return None


def init_runtime(require_cuda: bool) -> tuple[int, int, torch.device, bool]:
    distributed = "RANK" in os.environ and "WORLD_SIZE" in os.environ
    if distributed:
        dist.init_process_group(backend="nccl")
        rank = dist.get_rank()
        world_size = dist.get_world_size()
        local_rank = int(os.environ.get("LOCAL_RANK", rank))
    else:
        rank = 0
        world_size = 1
        local_rank = 0
    if torch.cuda.is_available():
        torch.cuda.set_device(local_rank)
        device = torch.device(f"cuda:{local_rank}")
    elif require_cuda:
        raise RuntimeError("CUDA is required for generation; use --audit-only for tokenizer preflight")
    else:
        device = torch.device("cpu")
    return rank, world_size, device, distributed


def _validate_args(args: Any) -> None:
    if args.max_prompts < 0:
        raise ValueError("--max_prompts must be non-negative")
    if args.num_images_per_prompt < 1:
        raise ValueError("--num_images_per_prompt must be at least 1")
    if args.steps < 1:
        raise ValueError("--steps must be at least 1")
    if args.height < 1 or args.width < 1:
        raise ValueError("--height and --width must be positive")
    if args.max_sequence_length < 0:
        raise ValueError("--max_sequence_length must be non-negative")


def _safety_failure(exc: Exception) -> bool:
    message = str(exc).lower()
    return any(term in message for term in ("safety", "content policy", "content_policy", "moderation", "blocked prompt"))


def _tokenizer_rows(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for record in records:
        prompt_id = str(record["prompt_id"])
        if prompt_id not in rows:
            rows[prompt_id] = {
                "prompt_id": prompt_id,
                "prompt_sha256": record["prompt_sha256"],
                **record["tokenizer_audit"],
            }
    return list(rows.values())


def run_diffusion_generation(
    *,
    args: Any,
    pipeline_class: Any,
    pipeline_name: str,
    generation_config_factory: Callable[[Any, str | None], dict[str, Any]],
    call_kwargs_factory: Callable[[Any, str, torch.Generator], dict[str, Any]],
) -> None:
    _validate_args(args)
    rank, world_size, device, distributed = init_runtime(require_cuda=not args.audit_only)

    prompts = load_prompts(args.prompt_file)
    if args.max_prompts > 0:
        prompts = prompts[: args.max_prompts]

    per_rank = (len(prompts) + world_size - 1) // world_size
    local_prompts = prompts[rank * per_rank : min((rank + 1) * per_rank, len(prompts))]
    os.makedirs(args.output_dir, exist_ok=True)

    if rank == 0:
        print(f"Total prompts: {len(prompts)}, world_size: {world_size}, per_rank: ~{per_rank}")
        print(f"Loading {pipeline_name} from {args.model_path} ...")

    load_kwargs: dict[str, Any] = {"torch_dtype": torch.bfloat16}
    if args.model_revision:
        load_kwargs["revision"] = args.model_revision
    pipe = pipeline_class.from_pretrained(args.model_path, **load_kwargs)
    if not args.audit_only:
        pipe = pipe.to(device)
    require_explicit_pipeline_limit(pipe, args.max_sequence_length, pipeline_name)

    resolved_revision = args.model_revision
    if resolved_revision is None:
        config = getattr(pipe, "config", None)
        resolved_revision = getattr(config, "_commit_hash", None)
        if resolved_revision is None and hasattr(config, "get"):
            resolved_revision = config.get("_commit_hash")

    generation_config = generation_config_factory(args, resolved_revision)
    tokenizer_artifact = tokenizer_artifact_fingerprint(args.model_path)
    generation_config.update(
        model_identifier=args.model_path,
        model_revision=resolved_revision,
        pipeline=pipeline_name,
        torch_dtype="bfloat16",
        diffusers_version=package_version("diffusers"),
        torch_version=getattr(torch, "__version__", None),
        model_artifact_fingerprint=model_artifact_fingerprint(args.model_path),
        tokenizer_artifact_fingerprint=tokenizer_artifact,
    )
    config_sha256 = sha256_json(generation_config)
    if distributed:
        config_hashes: list[str | None] = [None] * world_size
        dist.all_gather_object(config_hashes, config_sha256)
        if len(set(config_hashes)) != 1:
            raise RuntimeError(f"Generation config differs across ranks: {config_hashes}")

    if rank == 0:
        mode = "tokenizer audit" if args.audit_only else "generation"
        print(f"Model loaded. Starting {mode} ...")

    records: list[dict[str, Any]] = []
    for metadata in tqdm(local_prompts, desc=f"Rank {rank}", disable=(rank != 0)):
        prompt_text = metadata["prompt"]
        prompt_id = metadata["prompt_id"]
        audit = audit_pipeline_prompt(
            pipe,
            prompt_text,
            args.max_sequence_length or None,
            model_revision=resolved_revision,
        )
        audit["tokenizer_artifact_fingerprint"] = tokenizer_artifact
        audit["tokenizer_artifact_fingerprint_sha256"] = (
            tokenizer_artifact.get("sha256") if tokenizer_artifact else None
        )

        for sample_index in range(1, args.num_images_per_prompt + 1):
            image_path = os.path.join(args.output_dir, f"{prompt_id}_{sample_index}.png")
            seed = args.seed + sample_index
            expected = base_record(
                prompt_id=prompt_id,
                sample_index=sample_index,
                prompt_text=prompt_text,
                gt_regions=metadata["gt_regions"],
                image_path=image_path,
                output_dir=args.output_dir,
                model_identifier=args.model_path,
                model_revision=resolved_revision,
                generation_config=generation_config,
                model_artifact=generation_config["model_artifact_fingerprint"],
                seed=seed,
                tokenizer_audit=audit,
            )
            cache_status, record = validate_existing(image_path, expected)
            if cache_status == "valid":
                records.append(record)
                continue
            if cache_status == "stale" and not args.regenerate_stale:
                records.append(record)
                continue
            if args.audit_only:
                if cache_status == "stale":
                    records.append(record)
                else:
                    record.update(status="audit_only", action="tokenizer_audit_only")
                    records.append(record)
                continue

            archived: list[str] = []
            if cache_status == "stale":
                archived = archive_stale(image_path, args.output_dir)
            generator = torch.Generator(device=device).manual_seed(seed)
            try:
                call_kwargs = call_kwargs_factory(args, prompt_text, generator)
                if args.max_sequence_length:
                    call_kwargs["max_sequence_length"] = args.max_sequence_length
                result = pipe(**call_kwargs)
                save_image_atomic(result.images[0], image_path)
                record = successful_record(image_path, expected)
                if archived:
                    record["archived_stale_artifacts"] = archived
                    record = successful_record(image_path, record, action="regenerated_stale")
            except Exception as exc:  # Preserve a per-task failure and continue the run.
                status = "safety_rejected" if _safety_failure(exc) else "failed"
                record = terminal_record(
                    image_path,
                    expected,
                    status,
                    "generation_failed",
                    error_type=type(exc).__name__,
                    error_message=str(exc)[:500],
                    archived_stale_artifacts=archived or None,
                )
            records.append(record)

    write_rank_shard(args.output_dir, rank, records)
    if distributed:
        dist.barrier()
    if rank == 0:
        merged = merge_rank_shards(args.output_dir, world_size)
        write_tokenizer_audit(args.output_dir, _tokenizer_rows(merged))
        write_run_summary(
            args.output_dir,
            generation_config=generation_config,
            prompt_file=args.prompt_file,
            prompt_count=len(prompts),
            sample_count=len(prompts) * args.num_images_per_prompt,
            records=merged,
        )
        counts: dict[str, int] = {}
        for record in merged:
            counts[record["status"]] = counts.get(record["status"], 0) + 1
        print(f"Done. Status counts: {dict(sorted(counts.items()))}")
        print(f"Manifest: {os.path.join(args.output_dir, 'generation_manifest.jsonl')}")
    if distributed:
        dist.barrier()
        dist.destroy_process_group()
