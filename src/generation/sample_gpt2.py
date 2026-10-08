#!/usr/bin/env python3
"""GPT Image sampling with per-task provenance and persistent failure states."""

import argparse
import base64
import json
import os
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib.parse import urlsplit, urlunsplit

from tqdm import tqdm

try:
    from .tracking import (
        archive_stale,
        base_record,
        black_box_tokenizer_audit,
        load_prompts,
        save_bytes_atomic,
        sha256_text,
        successful_record,
        terminal_record,
        validate_existing,
        write_manifest,
        write_run_summary,
        write_tokenizer_audit,
    )
except ImportError:
    from tracking import (
        archive_stale,
        base_record,
        black_box_tokenizer_audit,
        load_prompts,
        save_bytes_atomic,
        sha256_text,
        successful_record,
        terminal_record,
        validate_existing,
        write_manifest,
        write_run_summary,
        write_tokenizer_audit,
    )


DEFAULT_API_URL = ""
DEFAULT_MODEL = "gpt-image-2"
DEFAULT_QUALITY = "low"
DEFAULT_SIZE = "1024x1024"
DEFAULT_CONCURRENCY = 64
DEFAULT_IMAGES = 4
DEFAULT_MAX_RETRIES = 5
DEFAULT_TIMEOUT = 300


def parse_args():
    parser = argparse.ArgumentParser(description="GPT Image sampling for TextBench v8")
    parser.add_argument("--prompt_file", type=str, required=True)
    parser.add_argument("--output_dir", type=str, required=True)
    parser.add_argument("--quality", type=str, default=DEFAULT_QUALITY, choices=["low", "medium", "high"])
    parser.add_argument("--size", type=str, default=DEFAULT_SIZE)
    parser.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY)
    parser.add_argument("--num_images", type=int, default=DEFAULT_IMAGES)
    parser.add_argument("--max_prompts", type=int, default=0)
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL)
    parser.add_argument("--model_revision", type=str, default=None)
    parser.add_argument("--api_url", type=str, default=os.environ.get("GPT_IMAGE_API_URL", DEFAULT_API_URL))
    parser.add_argument("--api_key_env", type=str, default="GPT_IMAGE_API_KEY")
    parser.add_argument("--max_retries", type=int, default=DEFAULT_MAX_RETRIES)
    parser.add_argument("--request_timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument(
        "--allow-insecure-http",
        action="store_true",
        help="Explicitly allow a non-local HTTP endpoint (Bearer credentials can be intercepted)",
    )
    parser.add_argument("--audit-only", action="store_true", help="Write black-box tokenizer/cache audit only")
    parser.add_argument("--regenerate-stale", action="store_true")
    return parser.parse_args()


def _is_safety_message(message: str) -> bool:
    lowered = message.lower()
    return any(term in lowered for term in ("safety", "content policy", "content_policy", "moderation", "blocked prompt"))


def safe_api_origin(url: str) -> str:
    parsed = urlsplit(url)
    hostname = parsed.hostname or ""
    if ":" in hostname:
        hostname = f"[{hostname}]"
    try:
        port = parsed.port
    except ValueError:
        port = None
    netloc = f"{hostname}:{port}" if port else hostname
    return urlunsplit((parsed.scheme, netloc, parsed.path, "", ""))


def validate_api_url(url: str, allow_insecure_http: bool) -> None:
    parsed = urlsplit(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise SystemExit("--api_url must be a valid HTTP(S) URL")
    if parsed.username or parsed.password:
        raise SystemExit("Do not embed credentials in --api_url; use the API key environment variable")
    local = parsed.hostname in ("localhost", "127.0.0.1", "::1")
    if parsed.scheme != "https" and not local and not allow_insecure_http:
        raise SystemExit("Refusing to send a Bearer credential over HTTP; use HTTPS or --allow-insecure-http")


def call_api(prompt: str, args, api_key: str) -> dict:
    payload = json.dumps(
        {
            "model": args.model,
            "method": "/images/generations",
            "prompt": prompt,
            "quality": args.quality,
            "size": args.size,
            "background": "opaque",
        },
        ensure_ascii=False,
    ).encode("utf-8")
    request = Request(
        args.api_url,
        data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    with urlopen(request, timeout=args.request_timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def generate_one(task: dict, args, api_key: str) -> dict:
    expected = task["expected"]
    image_path = task["image_path"]
    archived: list[str] = []
    if task["cache_status"] == "stale":
        archived = archive_stale(image_path, args.output_dir)

    last_error_type = None
    last_error_message = None
    for attempt in range(1, args.max_retries + 1):
        if attempt > 1:
            time.sleep(5 * (2 ** (attempt - 2)) + random.uniform(0, 10))
        try:
            data = call_api(task["prompt_text"], args, api_key)
            if "error" in data:
                error = data.get("error") or {}
                message = str(error.get("message", "provider error"))
                if _is_safety_message(message):
                    return terminal_record(
                        image_path,
                        expected,
                        "safety_rejected",
                        "provider_safety_rejected",
                        attempts=attempt,
                        provider_error=message[:500],
                        archived_stale_artifacts=archived or None,
                    )
                last_error_type = str(error.get("type") or "provider_error")
                last_error_message = message[:500]
                continue
            if data.get("code") or data.get("type") == "upstream_error":
                last_error_type = str(data.get("type") or data.get("code") or "upstream_error")
                last_error_message = str(data.get("message", "upstream error"))[:500]
                continue
            images = data.get("data", [])
            if not images or not images[0].get("b64_json"):
                last_error_type = "missing_image_data"
                last_error_message = "Provider returned no b64_json image."
                continue

            image_bytes = base64.b64decode(images[0]["b64_json"], validate=True)
            save_bytes_atomic(image_bytes, image_path)
            record = successful_record(image_path, expected, action="regenerated_stale" if archived else "generated")
            if archived:
                record["archived_stale_artifacts"] = archived
                record = successful_record(image_path, record, action="regenerated_stale")
            record["attempts"] = attempt
            return successful_record(image_path, record, action=record["action"])
        except HTTPError as exc:
            last_error_type = f"http_{exc.code}"
            try:
                response_body = exc.read(16_384).decode("utf-8", errors="replace")
                response_value = json.loads(response_body)
                response_error = response_value.get("error", response_value)
                last_error_message = str(
                    response_error.get("message", response_body)
                    if isinstance(response_error, dict)
                    else response_error
                )[:500]
            except (OSError, ValueError, TypeError):
                last_error_message = str(exc.reason)[:500]
            if exc.code in (400, 403) and _is_safety_message(last_error_message):
                return terminal_record(
                    image_path,
                    expected,
                    "safety_rejected",
                    "provider_safety_rejected",
                    attempts=attempt,
                    provider_error=last_error_message,
                    archived_stale_artifacts=archived or None,
                )
        except (URLError, TimeoutError, OSError, ValueError, TypeError) as exc:
            last_error_type = type(exc).__name__
            last_error_message = str(exc)[:500]
        except Exception as exc:  # Preserve an unexpected task-level failure instead of aborting the run.
            last_error_type = type(exc).__name__
            last_error_message = str(exc)[:500]

    return terminal_record(
        image_path,
        expected,
        "failed",
        "max_retries_exhausted",
        attempts=args.max_retries,
        error_type=last_error_type,
        error_message=last_error_message,
        archived_stale_artifacts=archived or None,
    )


def main():
    args = parse_args()
    if args.max_retries < 1:
        raise SystemExit("--max_retries must be at least 1")
    if args.request_timeout < 1:
        raise SystemExit("--request_timeout must be at least 1")
    if args.concurrency < 1:
        raise SystemExit("--concurrency must be at least 1")
    if args.num_images < 1:
        raise SystemExit("--num_images must be at least 1")
    if args.max_prompts < 0:
        raise SystemExit("--max_prompts must be non-negative")
    if not args.api_url:
        raise SystemExit("Set --api_url or GPT_IMAGE_API_URL to your compatible gateway endpoint")
    validate_api_url(args.api_url, args.allow_insecure_http)
    os.makedirs(args.output_dir, exist_ok=True)

    prompts = load_prompts(args.prompt_file)
    if args.max_prompts > 0:
        prompts = prompts[: args.max_prompts]

    generation_config = {
        "model_identifier": args.model,
        "model_revision": args.model_revision,
        "pipeline": "GPTImageAPI",
        "quality": args.quality,
        "size": args.size,
        "background": "opaque",
        "api_url": safe_api_origin(args.api_url),
        "api_endpoint_sha256": sha256_text(args.api_url),
        "tokenizer": "black_box_unknown",
        "seed_supported": False,
    }
    tasks: list[dict] = []
    records: list[dict] = []
    audit_rows: list[dict] = []
    for metadata in prompts:
        prompt_text = metadata["prompt"]
        prompt_id = metadata["prompt_id"]
        audit = black_box_tokenizer_audit(prompt_text)
        audit_rows.append({"prompt_id": str(prompt_id), "prompt_sha256": None, **audit})
        for sample_index in range(1, args.num_images + 1):
            image_path = os.path.join(args.output_dir, f"{prompt_id}_{sample_index}.png")
            expected = base_record(
                prompt_id=prompt_id,
                sample_index=sample_index,
                prompt_text=prompt_text,
                gt_regions=metadata["gt_regions"],
                image_path=image_path,
                output_dir=args.output_dir,
                model_identifier=args.model,
                model_revision=args.model_revision,
                generation_config=generation_config,
                model_artifact=None,
                seed=None,
                tokenizer_audit=audit,
            )
            audit_rows[-1]["prompt_sha256"] = expected["prompt_sha256"]
            cache_status, record = validate_existing(image_path, expected)
            if cache_status == "valid":
                records.append(record)
            elif cache_status == "stale" and not args.regenerate_stale:
                records.append(record)
            elif args.audit_only:
                if cache_status == "stale":
                    records.append(record)
                else:
                    record.update(status="audit_only", action="tokenizer_audit_only")
                    records.append(record)
            else:
                tasks.append(
                    {
                        "prompt_text": prompt_text,
                        "image_path": image_path,
                        "expected": expected,
                        "cache_status": cache_status,
                    }
                )

    print(f"Prompts: {len(prompts)}, Planned: {len(prompts) * args.num_images}, Pending: {len(tasks)}")
    print(f"Quality: {args.quality}, Size: {args.size}, Concurrency: {args.concurrency}")

    if tasks:
        validate_api_url(args.api_url, args.allow_insecure_http)
        api_key = os.environ.get(args.api_key_env)
        if not api_key:
            raise SystemExit(f"Missing API key: set environment variable {args.api_key_env}")
        with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
            futures = [executor.submit(generate_one, task, args, api_key) for task in tasks]
            for future in tqdm(as_completed(futures), total=len(futures), desc="Generating"):
                records.append(future.result())

    write_manifest(args.output_dir, records)
    write_tokenizer_audit(args.output_dir, audit_rows)
    write_run_summary(
        args.output_dir,
        generation_config=generation_config,
        prompt_file=args.prompt_file,
        prompt_count=len(prompts),
        sample_count=len(prompts) * args.num_images,
        records=records,
    )
    counts: dict[str, int] = {}
    for record in records:
        counts[record["status"]] = counts.get(record["status"], 0) + 1
    print(f"Done. Status counts: {dict(sorted(counts.items()))}")
    print(f"Manifest: {os.path.join(args.output_dir, 'generation_manifest.jsonl')}")


if __name__ == "__main__":
    main()
