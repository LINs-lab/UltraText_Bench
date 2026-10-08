"""公共评测指标 — BoW / NED / char_similarity / Hungarian / LCS"""
import numpy as np


def bow_match(ocr_text, gt_texts, lang='en'):
    """词袋匹配: Recall + Precision + F1"""
    gt_full = ' '.join(gt_texts) if isinstance(gt_texts, list) else gt_texts
    if lang == 'zh':
        ocr_c = list(ocr_text.replace(' ', ''))
        gt_c = list(gt_full.replace(' ', ''))
    else:
        ocr_c = list(ocr_text.lower().replace(' ', ''))
        gt_c = list(gt_full.lower().replace(' ', ''))

    gt_cc = {}
    for c in gt_c:
        gt_cc[c] = gt_cc.get(c, 0) + 1
    ocr_cc = {}
    for c in ocr_c:
        ocr_cc[c] = ocr_cc.get(c, 0) + 1
    matched = sum(min(gt_cc.get(c, 0), ocr_cc.get(c, 0)) for c in set(ocr_c))
    char_r = matched / max(len(gt_c), 1)
    char_p = matched / max(len(ocr_c), 1)
    char_f1 = 2 * char_r * char_p / max(char_r + char_p, 1e-8)

    if lang == 'zh':
        gt_w = list(gt_full.replace(' ', ''))
        ocr_w = list(ocr_text.replace(' ', ''))
    else:
        gt_w = gt_full.lower().split()
        ocr_w = ocr_text.lower().split()
    gwc = {}
    for w in gt_w:
        gwc[w] = gwc.get(w, 0) + 1
    owc = {}
    for w in ocr_w:
        owc[w] = owc.get(w, 0) + 1
    mw = sum(min(gwc.get(w, 0), owc.get(w, 0)) for w in set(ocr_w))
    word_r = mw / max(len(gt_w), 1)

    return {
        'char_recall': round(char_r, 4),
        'char_precision': round(char_p, 4),
        'char_f1': round(char_f1, 4),
        'word_recall': round(word_r, 4),
    }


def ned(s1, s2):
    """归一化编辑距离 (1 - edit_dist/max_len)"""
    s1, s2 = s1.lower().strip(), s2.lower().strip()
    if len(s1) + len(s2) > 3000:
        return None
    m, n = len(s1), len(s2)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, n + 1):
            tmp = dp[j]
            dp[j] = prev if s1[i-1] == s2[j-1] else 1 + min(dp[j], dp[j-1], prev)
            prev = tmp
    return round(1 - dp[n] / max(m, n, 1), 4)


def char_similarity(s1, s2):
    """字符级相似度"""
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    s1, s2 = s1.lower(), s2.lower()
    c1 = {}
    for c in s1:
        c1[c] = c1.get(c, 0) + 1
    c2 = {}
    for c in s2:
        c2[c] = c2.get(c, 0) + 1
    inter = sum(min(c1.get(c, 0), c2.get(c, 0)) for c in set(c1) | set(c2))
    return inter / max(len(s1), len(s2))


def hungarian_match(ocr_blocks, gt_regions):
    """匈牙利匹配: 对齐OCR块到GT区域"""
    from scipy.optimize import linear_sum_assignment
    nb, ng = len(ocr_blocks), len(gt_regions)
    if nb == 0 or ng == 0:
        return [], ng, nb
    cost = np.zeros((nb, ng))
    for i, b in enumerate(ocr_blocks):
        bt = b.get('text', '') if isinstance(b, dict) else str(b)
        for j, g in enumerate(gt_regions):
            cost[i, j] = 1 - char_similarity(bt, g['text'])
    ri, ci = linear_sum_assignment(cost)
    pairs = [(int(i), int(j), round(1 - cost[i, j], 4)) for i, j in zip(ri, ci) if cost[i, j] < 0.9]
    return pairs, ng - len(pairs), nb - len(pairs)


def lcs_length(seq1, seq2):
    """基于文本相似度的LCS长度"""
    m, n = len(seq1), len(seq2)
    if m * n > 10000:
        return min(m, n) // 2
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if char_similarity(seq1[i-1], seq2[j-1]) > 0.5:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
