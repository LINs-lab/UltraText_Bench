# Release scope and provenance

This repository packages the supplied UltraText Bench v8 dataset and evaluator with the current author-visible preprint. Its structure follows the IDM code release: a project README, paper figures, runnable entry points, offline checks, and a `paper/` directory containing the paper PDF.

## Dataset and code

The English and Chinese JSONL files are byte-identical to the supplied v8 records:

```text
8e89a96aab4b9bae6a592caddf8262f4874eaa244f5c6b62e59af0b757c4c248  data/en_prompts.jsonl
73d432170a2e8eaba33729941e06862a9481a3e37045289e922575c61fa2bb58  data/zh_prompts.jsonl
```

They contain 432 prompts, 407,918 target characters, and 2,926 regions. The supplied audit snapshots and signoff are retained as historical dataset-processing records. Their named reviewer is Codex; they must not be represented as human image-rating annotations.

The judge rubric, score validation, score formula, rounding, and aggregation logic are unchanged from v8. Packaging changes require an explicit judge model ID and remove the internal default GPT Image gateway URL. The gateway adapter still uses its original request format. The supplied Ideogram runner is omitted because its `Ideogram4Pipeline` dependency is not included in the released environment. Historical paper-alignment notes and obsolete template code are also omitted.

## Paper and figures

The PDF includes the arXiv preparation and few-step citation update dated 2026-10-07. Its checksum is in [paper/README.md](../paper/README.md). The displayed L3 gallery is cropped from page 2 of the preceding preprint; the evaluation figure is rendered from the corresponding source figure. These display derivatives do not change the paper.

The preprint has 38 total pages, with the main-text conclusion on page 14 and references starting on page 15. It includes authors and affiliations. Human Alignment retains ten-person participation and qualitative observations; unverified numeric human-validation tables are absent.

The benchmark repository is [LINs-lab/UltraText_Bench](https://github.com/LINs-lab/UltraText_Bench). The paper is available as [arXiv:2610.09823](https://arxiv.org/abs/2610.09823).

## Reproduction boundaries

This package includes the complete benchmark input records and evaluation client. It does not bundle Q-Judger weights, generator checkpoints, or the complete generated-image and raw-response archives for all 24 model configurations. Selected image examples in the paper support qualitative inspection, not an estimate of error frequency.

The manuscript's GPT Image 2 analysis uses 1,723 valid images out of 1,728 planned images. Its recorded judge revision and weight-artifact hash are unavailable. Packaging the reported results does not complete that missing provenance. No numerical human-alignment results have been inferred or generated.

The offline tests exercise strict response parsing, complete references, coverage, context-overflow handling, image bindings, tokenizer bookkeeping, and the disabled-by-default OCR path. They do not run GPU generation or a live Q-Judger service and do not reproduce leaderboard scores. The generation dependency list is a starting environment for the shipped Diffusers runners, not a recovered environment lockfile for historical experiments.

## Leaderboard

`data/leaderboard.json` transcribes the 24 model rows and all 11 score columns from the manuscript table. The README presents overall scores and language-specific difficulty breakdowns. These are reported manuscript values, not a new evaluation run. Run `python scripts/render_leaderboard.py --check` to verify that the displayed tables match the JSON.
