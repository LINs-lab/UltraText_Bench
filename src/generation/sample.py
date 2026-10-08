import argparse

import torch
from diffusers import QwenImagePipeline

try:
    from .diffusion_common import run_diffusion_generation
except ImportError:
    from diffusion_common import run_diffusion_generation


def parse_args():
    parser = argparse.ArgumentParser(description="LongText-Bench sampling with Qwen-Image-2512")
    parser.add_argument("--model_path", type=str, required=True)
    parser.add_argument("--model_revision", type=str, default=None)
    parser.add_argument("--prompt_file", type=str, required=True)
    parser.add_argument("--output_dir", type=str, required=True)
    parser.add_argument("--max_prompts", type=int, default=0, help="Limit prompts (0 = all)")
    parser.add_argument("--num_images_per_prompt", type=int, default=4)
    parser.add_argument("--cfg_scale", type=float, default=4.0)
    parser.add_argument("--steps", type=int, default=50)
    parser.add_argument("--height", type=int, default=1024)
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--max_sequence_length",
        type=int,
        default=0,
        help="Explicit pipeline text limit (0 = loaded pipeline default)",
    )
    parser.add_argument("--audit-only", action="store_true", help="Audit tokenizer/cache without generating")
    parser.add_argument(
        "--regenerate-stale",
        action="store_true",
        help="Archive and regenerate PNGs whose provenance binding does not match",
    )
    return parser.parse_args()


def generation_config(args, revision):
    return {
        "steps": args.steps,
        "height": args.height,
        "width": args.width,
        "true_cfg_scale": args.cfg_scale,
        "negative_prompt": "",
        "max_sequence_length": args.max_sequence_length or None,
    }


def call_kwargs(args, prompt, generator: torch.Generator):
    return {
        "prompt": prompt,
        "negative_prompt": "",
        "true_cfg_scale": args.cfg_scale,
        "height": args.height,
        "width": args.width,
        "num_inference_steps": args.steps,
        "generator": generator,
    }


def main():
    run_diffusion_generation(
        args=parse_args(),
        pipeline_class=QwenImagePipeline,
        pipeline_name="QwenImagePipeline",
        generation_config_factory=generation_config,
        call_kwargs_factory=call_kwargs,
    )


if __name__ == "__main__":
    main()
