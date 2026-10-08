import argparse

import torch
from diffusers import ZImagePipeline

try:
    from .diffusion_common import run_diffusion_generation
except ImportError:
    from diffusion_common import run_diffusion_generation


def parse_args():
    parser = argparse.ArgumentParser(description="Z-Image-Turbo sampling for TextBench v8")
    parser.add_argument("--model_path", type=str, default="Tongyi-MAI/Z-Image-Turbo")
    parser.add_argument("--model_revision", type=str, default=None)
    parser.add_argument("--prompt_file", type=str, required=True)
    parser.add_argument("--output_dir", type=str, required=True)
    parser.add_argument("--num_images_per_prompt", type=int, default=4)
    parser.add_argument("--steps", type=int, default=8)
    parser.add_argument("--height", type=int, default=1024)
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--cfg_scale", type=float, default=4.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max_prompts", type=int, default=0)
    parser.add_argument("--max_sequence_length", type=int, default=0)
    parser.add_argument("--audit-only", action="store_true")
    parser.add_argument("--regenerate-stale", action="store_true")
    return parser.parse_args()


def generation_config(args, revision):
    return {
        "steps": args.steps,
        "height": args.height,
        "width": args.width,
        "guidance_scale": args.cfg_scale,
        "max_sequence_length": args.max_sequence_length or None,
    }


def call_kwargs(args, prompt, generator: torch.Generator):
    return {
        "prompt": prompt,
        "height": args.height,
        "width": args.width,
        "num_inference_steps": args.steps,
        "guidance_scale": args.cfg_scale,
        "generator": generator,
    }


def main():
    run_diffusion_generation(
        args=parse_args(),
        pipeline_class=ZImagePipeline,
        pipeline_name="ZImagePipeline",
        generation_config_factory=generation_config,
        call_kwargs_factory=call_kwargs,
    )


if __name__ == "__main__":
    main()
