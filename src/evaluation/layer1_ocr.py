"""Deprecated PaddleOCR diagnostic; excluded from v8 ranking and composite scores.

python src/evaluation/layer1_ocr.py \
    --enable-diagnostic \
    --sample_dir results/qwen_image_v2_50s_en \
    --gt_file data/en_prompts.jsonl \
    --output_dir results/qwen_image_v2_50s_en/layer1 \
    --lang en

The explicit flag prevents this legacy metric from being run or interpreted
as part of the official VLM-only protocol by accident.
"""
import os, sys, glob, json, argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


def init_ocr():
    from paddleocr import PaddleOCR
    return PaddleOCR(use_doc_orientation_classify=False,
                     use_doc_unwarping=False, use_textline_orientation=False)


def run_ocr(ocr, image_path):
    blocks = []
    for r in ocr.predict(image_path):
        for text, score in zip(r['rec_texts'], r['rec_scores']):
            if score > 0.5:
                blocks.append(text)
    full_text = ' '.join(blocks)
    return full_text, blocks


def region_matched_scores(ocr_blocks, gt_regions):
    import numpy as np
    from src.evaluation.metrics import hungarian_match, ned

    if not ocr_blocks or not gt_regions:
        return {'region_matched_ned': 0.0, 'region_recall': 0.0}

    pairs, unmatched_gt, unmatched_ocr = hungarian_match(ocr_blocks, gt_regions)
    total_gt = len(gt_regions)

    neds = []
    for ocr_idx, gt_idx, sim in pairs:
        ocr_text = ocr_blocks[ocr_idx]
        gt_text = gt_regions[gt_idx]['text']
        n = ned(ocr_text, gt_text)
        if n is not None:
            neds.append(n)

    avg_ned = np.mean(neds) if neds else 0.0
    region_recall = len(pairs) / max(total_gt, 1)

    return {
        'region_matched_ned': round(avg_ned, 4),
        'region_recall': round(region_recall, 4),
    }


def main(args):
    if not getattr(args, 'enable_diagnostic', False):
        print(
            "OCR is paused in v8 and is not a ranking metric. "
            "Pass --enable-diagnostic only for optional debugging.",
            file=sys.stderr,
        )
        return 2

    import numpy as np
    from tqdm import tqdm
    from src.evaluation.metrics import bow_match, ned

    print("WARNING: OCR diagnostic only; results do not enter the v8 ranking.")
    with open(args.gt_file) as f:
        gt_map = {json.loads(l)["prompt_id"]: json.loads(l) for l in f}

    sample_dir = os.path.abspath(args.sample_dir)
    images = sorted(glob.glob(f'{sample_dir}/*.png'))

    data = []
    for img in images:
        basename = os.path.basename(img).rsplit(".", 1)[0]
        pid = basename.rsplit("_", 1)[0]
        if pid in gt_map:
            data.append({'image': img, 'prompt_id': pid, 'gt': gt_map[pid]})

    ocr = init_ocr()
    print(f"OCR diagnostic: {len(data)} images, {len(gt_map)} prompts")

    results = []
    for item in tqdm(data, desc="OCR"):
        gt_texts = [r['text'] for r in item['gt']['gt_regions']]
        try:
            ocr_text, ocr_blocks = run_ocr(ocr, item['image'])
            scores = bow_match(ocr_text, gt_texts, args.lang)
            gt_full = ' '.join(gt_texts)
            scores['ned'] = ned(ocr_text, gt_full)
            region_scores = region_matched_scores(ocr_blocks, item['gt']['gt_regions'])
            scores.update(region_scores)
        except Exception:
            scores = {'char_recall': 0, 'char_precision': 0, 'char_f1': 0,
                      'word_recall': 0, 'ned': 0, 'region_matched_ned': 0, 'region_recall': 0}

        results.append({
            'image': os.path.basename(item['image']),
            'prompt_id': item['prompt_id'],
            'category': item['gt'].get('category', ''),
            'level': item['gt'].get('level', ''),
            **scores
        })

    os.makedirs(args.output_dir, exist_ok=True)
    with open(os.path.join(args.output_dir, 'results.jsonl'), "w") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"\n=== Non-ranking OCR diagnostic ({len(results)} images) ===")
    for k in ['char_recall', 'char_precision', 'char_f1', 'word_recall',
              'ned', 'region_matched_ned', 'region_recall']:
        vals = [r[k] for r in results if r.get(k) is not None]
        if vals:
            print(f"  {k}: {np.mean(vals):.4f}")
    return 0


if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description="Deprecated optional OCR diagnostic; not a v8 ranking metric."
    )
    p.add_argument(
        "--enable-diagnostic",
        action="store_true",
        help="explicitly opt in to the deprecated non-ranking OCR diagnostic",
    )
    p.add_argument("--sample_dir", required=True)
    p.add_argument("--gt_file", required=True)
    p.add_argument("--output_dir", required=True)
    p.add_argument("--lang", default='en', choices=['en', 'zh'])
    raise SystemExit(main(p.parse_args()))
