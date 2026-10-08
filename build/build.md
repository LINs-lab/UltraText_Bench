# UltraText Bench v8 — Prompt 审计与交付验证报告

验证日期：2026-08-16
数据版本：code_v8（L1/L2/L3 三级，432 条 prompt）
验证结果：**432/432 全部通过；独立内容签核覆盖 432/432 条。**

## 最终源文件校验值

- `data/en_prompts.jsonl`: `8e89a96aab4b9bae6a592caddf8262f4874eaa244f5c6b62e59af0b757c4c248`
- `data/zh_prompts.jsonl`: `73d432170a2e8eaba33729941e06862a9481a3e37045289e922575c61fa2bb58`

## 验证标准

| # | 检查项 | 说明 |
|---|---|---|
| 1 | char_range | GT 字符总数符合 level × language 范围 |
| 2 | gt_embedded_once | 每个 GT region 文本在 prompt 中恰好出现一次 |
| 3 | stats | chars/words/regions 按 gt_regions 统一口径重算一致 |
| 4 | structure | 顶层/region 字段完整且 `region_0..n` 连续 |
| 5 | id_consistent | prompt_id、category、level、language 与文件一致 |
| 6 | content_scan | 固定 QA、质检串和机械区域脚手架无命中 |
| 7 | content_signoff | 独立签核绑定源、人工 metadata 与历史计划账本 |
| 8 | political_term_observed | 窄范围政治关键词观察信号，命中不阻断交付 |
| 9 | contact_pattern_observed | 中国手机号/常规邮箱模式观察信号，命中不等于 PII 且不阻断交付 |

## 字符范围定义

| Level | EN chars | ZH chars |
|---|---:|---:|
| L1 | 250–600 | 350–600 |
| L2 | 600–1200 | 550–900 |
| L3 | ≥1200 | ≥600 |

## 逐条验证清单

| # | prompt_id | category | level | lang | chars | words | regions | char | embed | stats | struct | id | scan | content | political signal | contact signal | RESULT |
|---:|---|---|---|---|---:|---:|---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | `A1_L1_EN_001` | sign | L1 | EN | 423 | 68 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 2 | `A1_L1_EN_002` | sign | L1 | EN | 453 | 73 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 3 | `A1_L1_EN_003` | sign | L1 | EN | 363 | 57 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 4 | `A1_L2_EN_001` | sign | L2 | EN | 805 | 128 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 5 | `A1_L2_EN_002` | sign | L2 | EN | 837 | 132 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 6 | `A1_L2_EN_003` | sign | L2 | EN | 674 | 96 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 7 | `A1_L3_EN_001` | sign | L3 | EN | 1472 | 230 | 11 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 8 | `A1_L3_EN_002` | sign | L3 | EN | 1546 | 245 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 9 | `A1_L3_EN_003` | sign | L3 | EN | 1369 | 197 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 10 | `A3_L1_EN_001` | poster | L1 | EN | 389 | 64 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 11 | `A3_L1_EN_002` | poster | L1 | EN | 425 | 73 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 12 | `A3_L1_EN_003` | poster | L1 | EN | 438 | 67 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 13 | `A2_L1_EN_001` | label | L1 | EN | 384 | 63 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 14 | `A2_L1_EN_002` | label | L1 | EN | 397 | 63 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 15 | `A2_L1_EN_003` | label | L1 | EN | 455 | 80 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 16 | `A2_L2_EN_001` | label | L2 | EN | 940 | 142 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 17 | `A2_L2_EN_002` | label | L2 | EN | 869 | 137 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 18 | `A2_L2_EN_003` | label | L2 | EN | 713 | 116 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 19 | `A4_L1_EN_001` | billboard | L1 | EN | 349 | 57 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 20 | `A4_L1_EN_002` | billboard | L1 | EN | 468 | 75 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 21 | `A4_L1_EN_003` | billboard | L1 | EN | 393 | 59 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 22 | `A4_L2_EN_001` | billboard | L2 | EN | 1158 | 161 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 23 | `A4_L2_EN_002` | billboard | L2 | EN | 883 | 150 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 24 | `A4_L2_EN_003` | billboard | L2 | EN | 941 | 129 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 25 | `A4_L3_EN_001` | billboard | L3 | EN | 1641 | 247 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 26 | `A4_L3_EN_002` | billboard | L3 | EN | 1700 | 241 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 27 | `A4_L3_EN_003` | billboard | L3 | EN | 1515 | 253 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 28 | `B1_L1_EN_001` | article | L1 | EN | 566 | 103 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 29 | `B1_L1_EN_002` | article | L1 | EN | 588 | 110 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 30 | `B1_L1_EN_003` | article | L1 | EN | 518 | 88 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 31 | `B1_L2_EN_001` | article | L2 | EN | 1042 | 165 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 32 | `B1_L2_EN_002` | article | L2 | EN | 1095 | 156 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 33 | `B1_L2_EN_003` | article | L2 | EN | 1126 | 192 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 34 | `B1_L3_EN_001` | article | L3 | EN | 2032 | 319 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 35 | `B1_L3_EN_002` | article | L3 | EN | 2026 | 305 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 36 | `B1_L3_EN_003` | article | L3 | EN | 2238 | 353 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 37 | `B3_L1_EN_001` | letter | L1 | EN | 396 | 67 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 38 | `B3_L1_EN_002` | letter | L1 | EN | 430 | 77 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 39 | `B3_L1_EN_003` | letter | L1 | EN | 466 | 77 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 40 | `B3_L2_EN_001` | letter | L2 | EN | 1031 | 160 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 41 | `B3_L2_EN_002` | letter | L2 | EN | 689 | 131 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 42 | `B3_L2_EN_003` | letter | L2 | EN | 966 | 176 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 43 | `B3_L3_EN_001` | letter | L3 | EN | 1619 | 247 | 11 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 44 | `B3_L3_EN_002` | letter | L3 | EN | 1515 | 252 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 45 | `B3_L3_EN_003` | letter | L3 | EN | 1589 | 237 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 46 | `B2_L1_EN_001` | newspaper | L1 | EN | 526 | 81 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 47 | `B2_L1_EN_002` | newspaper | L1 | EN | 541 | 86 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 48 | `B2_L1_EN_003` | newspaper | L1 | EN | 556 | 88 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 49 | `B2_L2_EN_001` | newspaper | L2 | EN | 1085 | 172 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 50 | `B2_L2_EN_002` | newspaper | L2 | EN | 1066 | 159 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 51 | `B2_L2_EN_003` | newspaper | L2 | EN | 1114 | 164 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 52 | `B2_L3_EN_001` | newspaper | L3 | EN | 2013 | 302 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 53 | `B2_L3_EN_002` | newspaper | L3 | EN | 1826 | 268 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 54 | `B2_L3_EN_003` | newspaper | L3 | EN | 1870 | 264 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 55 | `B4_L1_EN_001` | resume | L1 | EN | 510 | 65 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 56 | `B4_L1_EN_002` | resume | L1 | EN | 534 | 68 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 57 | `B4_L1_EN_003` | resume | L1 | EN | 573 | 82 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 58 | `B4_L2_EN_001` | resume | L2 | EN | 1138 | 153 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 59 | `B4_L2_EN_002` | resume | L2 | EN | 1143 | 149 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 60 | `B4_L2_EN_003` | resume | L2 | EN | 1195 | 154 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 61 | `B4_L3_EN_001` | resume | L3 | EN | 2502 | 342 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 62 | `B4_L3_EN_002` | resume | L3 | EN | 2738 | 374 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 63 | `B4_L3_EN_003` | resume | L3 | EN | 2692 | 345 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 64 | `C1_L1_EN_001` | menu | L1 | EN | 553 | 98 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 65 | `C1_L1_EN_002` | menu | L1 | EN | 583 | 90 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 66 | `C1_L1_EN_003` | menu | L1 | EN | 543 | 89 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 67 | `C1_L2_EN_001` | menu | L2 | EN | 1187 | 178 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 68 | `C1_L2_EN_002` | menu | L2 | EN | 1038 | 157 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 69 | `C1_L2_EN_003` | menu | L2 | EN | 1126 | 174 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 70 | `C1_L3_EN_001` | menu | L3 | EN | 3021 | 473 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 71 | `C1_L3_EN_002` | menu | L3 | EN | 2890 | 466 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 72 | `C1_L3_EN_003` | menu | L3 | EN | 2766 | 454 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 73 | `C3_L1_EN_001` | invoice | L1 | EN | 570 | 87 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 74 | `C3_L1_EN_002` | invoice | L1 | EN | 452 | 64 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 75 | `C3_L1_EN_003` | invoice | L1 | EN | 435 | 68 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 76 | `C3_L2_EN_001` | invoice | L2 | EN | 961 | 155 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 77 | `C3_L2_EN_002` | invoice | L2 | EN | 1166 | 188 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 78 | `C3_L2_EN_003` | invoice | L2 | EN | 1118 | 181 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 79 | `C3_L3_EN_001` | invoice | L3 | EN | 2745 | 412 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 80 | `C3_L3_EN_002` | invoice | L3 | EN | 2787 | 446 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 81 | `C3_L3_EN_003` | invoice | L3 | EN | 2737 | 432 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 82 | `C2_L1_EN_001` | receipt | L1 | EN | 354 | 59 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 83 | `C2_L1_EN_002` | receipt | L1 | EN | 369 | 67 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 84 | `C2_L1_EN_003` | receipt | L1 | EN | 375 | 60 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 85 | `C2_L2_EN_001` | receipt | L2 | EN | 1056 | 194 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 86 | `C2_L2_EN_002` | receipt | L2 | EN | 814 | 142 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 87 | `C2_L2_EN_003` | receipt | L2 | EN | 940 | 163 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 88 | `C2_L3_EN_001` | receipt | L3 | EN | 1799 | 285 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 89 | `C2_L3_EN_002` | receipt | L3 | EN | 1844 | 302 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 90 | `C2_L3_EN_003` | receipt | L3 | EN | 1728 | 268 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 91 | `C4_L1_EN_001` | product_pkg | L1 | EN | 474 | 72 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 92 | `C4_L1_EN_002` | product_pkg | L1 | EN | 563 | 80 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 93 | `C4_L1_EN_003` | product_pkg | L1 | EN | 527 | 89 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 94 | `C4_L2_EN_001` | product_pkg | L2 | EN | 1064 | 159 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 95 | `C4_L2_EN_002` | product_pkg | L2 | EN | 1153 | 158 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 96 | `C4_L2_EN_003` | product_pkg | L2 | EN | 1115 | 171 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 97 | `C4_L3_EN_001` | product_pkg | L3 | EN | 2242 | 316 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 98 | `C4_L3_EN_002` | product_pkg | L3 | EN | 2226 | 373 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 99 | `C4_L3_EN_003` | product_pkg | L3 | EN | 2317 | 388 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 100 | `D1_L1_EN_001` | webpage | L1 | EN | 555 | 88 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 101 | `D1_L1_EN_002` | webpage | L1 | EN | 539 | 85 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 102 | `D1_L1_EN_003` | webpage | L1 | EN | 590 | 99 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 103 | `D1_L2_EN_001` | webpage | L2 | EN | 1173 | 167 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 104 | `D1_L2_EN_002` | webpage | L2 | EN | 1007 | 146 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 105 | `D1_L2_EN_003` | webpage | L2 | EN | 920 | 126 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 106 | `D1_L3_EN_001` | webpage | L3 | EN | 2292 | 302 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 107 | `D1_L3_EN_002` | webpage | L3 | EN | 2426 | 343 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 108 | `D1_L3_EN_003` | webpage | L3 | EN | 2403 | 340 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 109 | `D3_L1_EN_001` | social_media | L1 | EN | 493 | 77 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 110 | `D3_L1_EN_002` | social_media | L1 | EN | 529 | 80 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 111 | `D3_L1_EN_003` | social_media | L1 | EN | 544 | 79 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 112 | `D3_L2_EN_001` | social_media | L2 | EN | 1023 | 162 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 113 | `D3_L2_EN_002` | social_media | L2 | EN | 1084 | 155 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 114 | `D3_L2_EN_003` | social_media | L2 | EN | 1150 | 159 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 115 | `D3_L3_EN_001` | social_media | L3 | EN | 2002 | 320 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 116 | `D3_L3_EN_002` | social_media | L3 | EN | 2343 | 339 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 117 | `D3_L3_EN_003` | social_media | L3 | EN | 3505 | 573 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 118 | `D2_L1_EN_001` | slide | L1 | EN | 538 | 74 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 119 | `D2_L1_EN_002` | slide | L1 | EN | 475 | 73 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 120 | `D2_L1_EN_003` | slide | L1 | EN | 553 | 76 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 121 | `D2_L2_EN_001` | slide | L2 | EN | 1049 | 161 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 122 | `D2_L2_EN_002` | slide | L2 | EN | 1145 | 157 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 123 | `D2_L2_EN_003` | slide | L2 | EN | 896 | 152 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 124 | `D2_L3_EN_001` | slide | L3 | EN | 2854 | 413 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 125 | `D2_L3_EN_002` | slide | L3 | EN | 4088 | 598 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 126 | `D2_L3_EN_003` | slide | L3 | EN | 3288 | 536 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 127 | `E1_L1_EN_001` | schedule | L1 | EN | 550 | 82 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 128 | `E1_L1_EN_002` | schedule | L1 | EN | 575 | 112 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 129 | `E1_L1_EN_003` | schedule | L1 | EN | 499 | 74 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 130 | `E1_L2_EN_001` | schedule | L2 | EN | 1048 | 187 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 131 | `E1_L2_EN_002` | schedule | L2 | EN | 1060 | 202 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 132 | `E1_L2_EN_003` | schedule | L2 | EN | 1078 | 177 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 133 | `E1_L3_EN_001` | schedule | L3 | EN | 2829 | 460 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 134 | `E1_L3_EN_002` | schedule | L3 | EN | 2909 | 479 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 135 | `E1_L3_EN_003` | schedule | L3 | EN | 3096 | 513 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 136 | `D4_L1_EN_001` | dashboard | L1 | EN | 574 | 106 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 137 | `D4_L1_EN_002` | dashboard | L1 | EN | 560 | 100 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 138 | `D4_L1_EN_003` | dashboard | L1 | EN | 592 | 99 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 139 | `D4_L2_EN_001` | dashboard | L2 | EN | 1108 | 183 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 140 | `D4_L2_EN_002` | dashboard | L2 | EN | 1088 | 194 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 141 | `D4_L2_EN_003` | dashboard | L2 | EN | 1000 | 194 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 142 | `D4_L3_EN_001` | dashboard | L3 | EN | 2808 | 476 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 143 | `D4_L3_EN_002` | dashboard | L3 | EN | 2691 | 422 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 144 | `D4_L3_EN_003` | dashboard | L3 | EN | 2597 | 425 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 145 | `E3_L1_EN_001` | certificate | L1 | EN | 538 | 69 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 146 | `E3_L1_EN_002` | certificate | L1 | EN | 466 | 62 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 147 | `E3_L1_EN_003` | certificate | L1 | EN | 398 | 57 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 148 | `E3_L2_EN_001` | certificate | L2 | EN | 1064 | 151 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 149 | `E3_L2_EN_002` | certificate | L2 | EN | 1094 | 155 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 150 | `E3_L2_EN_003` | certificate | L2 | EN | 1115 | 181 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 151 | `E3_L3_EN_001` | certificate | L3 | EN | 1537 | 216 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 152 | `E3_L3_EN_002` | certificate | L3 | EN | 1955 | 259 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 153 | `E3_L3_EN_003` | certificate | L3 | EN | 1754 | 284 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 154 | `E2_L1_EN_001` | form | L1 | EN | 545 | 81 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 155 | `E2_L1_EN_002` | form | L1 | EN | 402 | 60 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 156 | `E2_L1_EN_003` | form | L1 | EN | 438 | 70 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 157 | `E2_L2_EN_001` | form | L2 | EN | 1194 | 177 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 158 | `E2_L2_EN_002` | form | L2 | EN | 1177 | 159 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 159 | `E2_L2_EN_003` | form | L2 | EN | 883 | 126 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 160 | `E2_L3_EN_001` | form | L3 | EN | 2304 | 362 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 161 | `E2_L3_EN_002` | form | L3 | EN | 2525 | 381 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 162 | `E2_L3_EN_003` | form | L3 | EN | 3130 | 422 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 163 | `E4_L1_EN_001` | code | L1 | EN | 557 | 80 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 164 | `E4_L1_EN_002` | code | L1 | EN | 502 | 82 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 165 | `E4_L1_EN_003` | code | L1 | EN | 576 | 97 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 166 | `E4_L2_EN_001` | code | L2 | EN | 1186 | 164 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 167 | `E4_L2_EN_002` | code | L2 | EN | 1183 | 131 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 168 | `E4_L2_EN_003` | code | L2 | EN | 1143 | 145 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 169 | `E4_L3_EN_001` | code | L3 | EN | 4219 | 437 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 170 | `E4_L3_EN_002` | code | L3 | EN | 3437 | 390 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 171 | `E4_L3_EN_003` | code | L3 | EN | 5230 | 641 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 172 | `F1_L1_EN_001` | caption | L1 | EN | 502 | 69 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 173 | `F1_L1_EN_002` | caption | L1 | EN | 467 | 78 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 174 | `F1_L1_EN_003` | caption | L1 | EN | 457 | 65 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 175 | `F1_L2_EN_001` | caption | L2 | EN | 863 | 139 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 176 | `F1_L2_EN_002` | caption | L2 | EN | 978 | 166 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 177 | `F1_L2_EN_003` | caption | L2 | EN | 1010 | 145 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 178 | `F1_L3_EN_001` | caption | L3 | EN | 1907 | 320 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 179 | `F1_L3_EN_002` | caption | L3 | EN | 1902 | 335 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 180 | `F1_L3_EN_003` | caption | L3 | EN | 1860 | 276 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 181 | `F2_L1_EN_001` | dialogue | L1 | EN | 419 | 93 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 182 | `F2_L1_EN_002` | dialogue | L1 | EN | 431 | 86 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 183 | `F2_L1_EN_003` | dialogue | L1 | EN | 572 | 106 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 184 | `F2_L2_EN_001` | dialogue | L2 | EN | 925 | 196 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 185 | `F2_L2_EN_002` | dialogue | L2 | EN | 1055 | 185 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 186 | `F2_L2_EN_003` | dialogue | L2 | EN | 1078 | 193 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 187 | `F2_L3_EN_001` | dialogue | L3 | EN | 2064 | 376 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 188 | `F2_L3_EN_002` | dialogue | L3 | EN | 2744 | 453 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 189 | `F2_L3_EN_003` | dialogue | L3 | EN | 2683 | 445 | 11 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 190 | `F3_L1_EN_001` | comic_panel | L1 | EN | 380 | 70 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 191 | `F3_L1_EN_002` | comic_panel | L1 | EN | 498 | 89 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 192 | `F3_L1_EN_003` | comic_panel | L1 | EN | 278 | 49 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 193 | `F3_L2_EN_001` | comic_panel | L2 | EN | 967 | 176 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 194 | `F3_L2_EN_002` | comic_panel | L2 | EN | 1160 | 188 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 195 | `F3_L2_EN_003` | comic_panel | L2 | EN | 921 | 168 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 196 | `F3_L3_EN_001` | comic_panel | L3 | EN | 2563 | 443 | 11 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 197 | `F3_L3_EN_002` | comic_panel | L3 | EN | 2146 | 379 | 12 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 198 | `F3_L3_EN_003` | comic_panel | L3 | EN | 2703 | 467 | 11 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 199 | `F4_L1_EN_001` | infographic | L1 | EN | 576 | 93 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 200 | `F4_L1_EN_002` | infographic | L1 | EN | 590 | 104 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 201 | `F4_L1_EN_003` | infographic | L1 | EN | 576 | 86 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 202 | `F4_L2_EN_001` | infographic | L2 | EN | 1118 | 197 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 203 | `F4_L2_EN_002` | infographic | L2 | EN | 883 | 168 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 204 | `F4_L2_EN_003` | infographic | L2 | EN | 1106 | 166 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 205 | `F4_L3_EN_001` | infographic | L3 | EN | 2790 | 422 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 206 | `F4_L3_EN_002` | infographic | L3 | EN | 3626 | 541 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 207 | `F4_L3_EN_003` | infographic | L3 | EN | 3622 | 553 | 11 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 208 | `A3_L2_EN_001` | poster | L2 | EN | 772 | 123 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 209 | `A3_L2_EN_002` | poster | L2 | EN | 977 | 153 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 210 | `A3_L2_EN_003` | poster | L2 | EN | 759 | 109 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 211 | `A2_L3_EN_001` | label | L3 | EN | 1724 | 279 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 212 | `A2_L3_EN_002` | label | L3 | EN | 1370 | 238 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 213 | `A2_L3_EN_003` | label | L3 | EN | 1808 | 287 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 214 | `A3_L3_EN_001` | poster | L3 | EN | 1704 | 252 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 215 | `A3_L3_EN_002` | poster | L3 | EN | 1646 | 239 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 216 | `A3_L3_EN_003` | poster | L3 | EN | 1752 | 263 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 217 | `A1_L1_ZH_001` | sign | L1 | ZH | 362 | 52 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 218 | `A1_L1_ZH_002` | sign | L1 | ZH | 375 | 46 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 219 | `A1_L1_ZH_003` | sign | L1 | ZH | 365 | 57 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 220 | `A1_L2_ZH_001` | sign | L2 | ZH | 564 | 67 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 221 | `A1_L2_ZH_002` | sign | L2 | ZH | 575 | 82 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 222 | `A1_L2_ZH_003` | sign | L2 | ZH | 612 | 84 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 223 | `A1_L3_ZH_001` | sign | L3 | ZH | 628 | 102 | 12 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 224 | `A1_L3_ZH_002` | sign | L3 | ZH | 623 | 88 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 225 | `A1_L3_ZH_003` | sign | L3 | ZH | 639 | 100 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 226 | `A2_L1_ZH_001` | label | L1 | ZH | 362 | 52 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 227 | `A2_L1_ZH_002` | label | L1 | ZH | 359 | 49 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 228 | `A2_L1_ZH_003` | label | L1 | ZH | 383 | 49 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 229 | `A2_L2_ZH_001` | label | L2 | ZH | 557 | 84 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 230 | `A2_L2_ZH_002` | label | L2 | ZH | 576 | 89 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 231 | `A2_L2_ZH_003` | label | L2 | ZH | 554 | 84 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 232 | `A2_L3_ZH_001` | label | L3 | ZH | 606 | 95 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 233 | `A2_L3_ZH_002` | label | L3 | ZH | 672 | 85 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 234 | `A2_L3_ZH_003` | label | L3 | ZH | 676 | 81 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 235 | `A3_L1_ZH_001` | poster | L1 | ZH | 351 | 45 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 236 | `A3_L1_ZH_002` | poster | L1 | ZH | 418 | 56 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 237 | `A3_L1_ZH_003` | poster | L1 | ZH | 351 | 46 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 238 | `A3_L2_ZH_001` | poster | L2 | ZH | 652 | 85 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 239 | `A3_L2_ZH_002` | poster | L2 | ZH | 682 | 90 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 240 | `A3_L2_ZH_003` | poster | L2 | ZH | 713 | 89 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 241 | `A3_L3_ZH_001` | poster | L3 | ZH | 770 | 122 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 242 | `A3_L3_ZH_002` | poster | L3 | ZH | 606 | 79 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 243 | `A3_L3_ZH_003` | poster | L3 | ZH | 620 | 97 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 244 | `A4_L1_ZH_001` | billboard | L1 | ZH | 373 | 49 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 245 | `A4_L1_ZH_002` | billboard | L1 | ZH | 373 | 53 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 246 | `A4_L1_ZH_003` | billboard | L1 | ZH | 350 | 38 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 247 | `A4_L2_ZH_001` | billboard | L2 | ZH | 552 | 58 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 248 | `A4_L2_ZH_002` | billboard | L2 | ZH | 621 | 66 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 249 | `A4_L2_ZH_003` | billboard | L2 | ZH | 653 | 89 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 250 | `A4_L3_ZH_001` | billboard | L3 | ZH | 665 | 108 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 251 | `A4_L3_ZH_002` | billboard | L3 | ZH | 670 | 88 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 252 | `A4_L3_ZH_003` | billboard | L3 | ZH | 625 | 109 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 253 | `B1_L1_ZH_001` | article | L1 | ZH | 364 | 35 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 254 | `B1_L1_ZH_002` | article | L1 | ZH | 387 | 42 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 255 | `B1_L1_ZH_003` | article | L1 | ZH | 364 | 38 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 256 | `B1_L2_ZH_001` | article | L2 | ZH | 598 | 46 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 257 | `B1_L2_ZH_002` | article | L2 | ZH | 613 | 49 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 258 | `B1_L2_ZH_003` | article | L2 | ZH | 561 | 36 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 259 | `B1_L3_ZH_001` | article | L3 | ZH | 617 | 58 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 260 | `B1_L3_ZH_002` | article | L3 | ZH | 664 | 67 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 261 | `B1_L3_ZH_003` | article | L3 | ZH | 621 | 67 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 262 | `B2_L1_ZH_001` | newspaper | L1 | ZH | 395 | 50 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 263 | `B2_L1_ZH_002` | newspaper | L1 | ZH | 369 | 40 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 264 | `B2_L1_ZH_003` | newspaper | L1 | ZH | 362 | 42 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 265 | `B2_L2_ZH_001` | newspaper | L2 | ZH | 696 | 76 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 266 | `B2_L2_ZH_002` | newspaper | L2 | ZH | 632 | 63 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 267 | `B2_L2_ZH_003` | newspaper | L2 | ZH | 578 | 68 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 268 | `B2_L3_ZH_001` | newspaper | L3 | ZH | 627 | 72 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 269 | `B2_L3_ZH_002` | newspaper | L3 | ZH | 618 | 71 | 11 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 270 | `B2_L3_ZH_003` | newspaper | L3 | ZH | 604 | 71 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 271 | `B3_L1_ZH_001` | letter | L1 | ZH | 371 | 40 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 272 | `B3_L1_ZH_002` | letter | L1 | ZH | 381 | 37 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 273 | `B3_L1_ZH_003` | letter | L1 | ZH | 351 | 36 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 274 | `B3_L2_ZH_001` | letter | L2 | ZH | 577 | 58 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 275 | `B3_L2_ZH_002` | letter | L2 | ZH | 615 | 62 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 276 | `B3_L2_ZH_003` | letter | L2 | ZH | 566 | 67 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 277 | `B3_L3_ZH_001` | letter | L3 | ZH | 703 | 68 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 278 | `B3_L3_ZH_002` | letter | L3 | ZH | 629 | 59 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 279 | `B3_L3_ZH_003` | letter | L3 | ZH | 621 | 69 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 280 | `B4_L1_ZH_001` | resume | L1 | ZH | 471 | 70 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 281 | `B4_L1_ZH_002` | resume | L1 | ZH | 438 | 53 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 282 | `B4_L1_ZH_003` | resume | L1 | ZH | 408 | 56 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 283 | `B4_L2_ZH_001` | resume | L2 | ZH | 715 | 86 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 284 | `B4_L2_ZH_002` | resume | L2 | ZH | 671 | 95 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 285 | `B4_L2_ZH_003` | resume | L2 | ZH | 672 | 93 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 286 | `B4_L3_ZH_001` | resume | L3 | ZH | 980 | 121 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 287 | `B4_L3_ZH_002` | resume | L3 | ZH | 844 | 105 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 288 | `B4_L3_ZH_003` | resume | L3 | ZH | 793 | 83 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 289 | `C2_L1_ZH_001` | receipt | L1 | ZH | 377 | 77 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 290 | `C2_L1_ZH_002` | receipt | L1 | ZH | 378 | 83 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 291 | `C2_L1_ZH_003` | receipt | L1 | ZH | 351 | 70 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 292 | `C2_L2_ZH_001` | receipt | L2 | ZH | 630 | 112 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 293 | `C2_L2_ZH_002` | receipt | L2 | ZH | 583 | 109 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 294 | `C2_L2_ZH_003` | receipt | L2 | ZH | 653 | 117 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 295 | `C2_L3_ZH_001` | receipt | L3 | ZH | 696 | 133 | 10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 296 | `C2_L3_ZH_002` | receipt | L3 | ZH | 648 | 134 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 297 | `C2_L3_ZH_003` | receipt | L3 | ZH | 697 | 121 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 298 | `C3_L1_ZH_001` | invoice | L1 | ZH | 493 | 94 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 299 | `C3_L1_ZH_002` | invoice | L1 | ZH | 484 | 94 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 300 | `C3_L1_ZH_003` | invoice | L1 | ZH | 555 | 103 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 301 | `C3_L2_ZH_001` | invoice | L2 | ZH | 828 | 162 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 302 | `C3_L2_ZH_002` | invoice | L2 | ZH | 795 | 130 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 303 | `C3_L2_ZH_003` | invoice | L2 | ZH | 777 | 124 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 304 | `C3_L3_ZH_001` | invoice | L3 | ZH | 1045 | 194 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 305 | `C3_L3_ZH_002` | invoice | L3 | ZH | 815 | 164 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 306 | `C3_L3_ZH_003` | invoice | L3 | ZH | 1000 | 164 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 307 | `C1_L1_ZH_001` | menu | L1 | ZH | 351 | 57 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 308 | `C1_L1_ZH_002` | menu | L1 | ZH | 392 | 71 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 309 | `C1_L1_ZH_003` | menu | L1 | ZH | 373 | 71 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 310 | `C1_L2_ZH_001` | menu | L2 | ZH | 593 | 84 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 311 | `C1_L2_ZH_002` | menu | L2 | ZH | 558 | 102 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 312 | `C1_L2_ZH_003` | menu | L2 | ZH | 563 | 84 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 313 | `C1_L3_ZH_001` | menu | L3 | ZH | 734 | 101 | 9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 314 | `C1_L3_ZH_002` | menu | L3 | ZH | 611 | 106 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 315 | `C1_L3_ZH_003` | menu | L3 | ZH | 790 | 134 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 316 | `E1_L1_ZH_001` | schedule | L1 | ZH | 548 | 125 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 317 | `E1_L1_ZH_002` | schedule | L1 | ZH | 449 | 93 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 318 | `E1_L1_ZH_003` | schedule | L1 | ZH | 364 | 76 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 319 | `E1_L2_ZH_001` | schedule | L2 | ZH | 679 | 117 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 320 | `E1_L2_ZH_002` | schedule | L2 | ZH | 715 | 121 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 321 | `E1_L2_ZH_003` | schedule | L2 | ZH | 597 | 103 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 322 | `E1_L3_ZH_001` | schedule | L3 | ZH | 1068 | 199 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 323 | `E1_L3_ZH_002` | schedule | L3 | ZH | 727 | 149 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 324 | `E1_L3_ZH_003` | schedule | L3 | ZH | 781 | 152 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 325 | `D4_L1_ZH_001` | dashboard | L1 | ZH | 406 | 83 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 326 | `D4_L1_ZH_002` | dashboard | L1 | ZH | 394 | 78 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 327 | `D4_L1_ZH_003` | dashboard | L1 | ZH | 363 | 81 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 328 | `D4_L2_ZH_001` | dashboard | L2 | ZH | 625 | 123 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 329 | `D4_L2_ZH_002` | dashboard | L2 | ZH | 615 | 120 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 330 | `D4_L2_ZH_003` | dashboard | L2 | ZH | 559 | 105 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 331 | `D4_L3_ZH_001` | dashboard | L3 | ZH | 771 | 159 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 332 | `D4_L3_ZH_002` | dashboard | L3 | ZH | 936 | 194 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 333 | `D4_L3_ZH_003` | dashboard | L3 | ZH | 780 | 145 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 334 | `D1_L1_ZH_001` | webpage | L1 | ZH | 361 | 61 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 335 | `D1_L1_ZH_002` | webpage | L1 | ZH | 476 | 77 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 336 | `D1_L1_ZH_003` | webpage | L1 | ZH | 392 | 57 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 337 | `D1_L2_ZH_001` | webpage | L2 | ZH | 569 | 77 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 338 | `D1_L2_ZH_002` | webpage | L2 | ZH | 567 | 80 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 339 | `D1_L2_ZH_003` | webpage | L2 | ZH | 570 | 78 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 340 | `D1_L3_ZH_001` | webpage | L3 | ZH | 644 | 88 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 341 | `D1_L3_ZH_002` | webpage | L3 | ZH | 721 | 109 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 342 | `D1_L3_ZH_003` | webpage | L3 | ZH | 838 | 133 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 343 | `D2_L1_ZH_001` | slide | L1 | ZH | 380 | 59 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 344 | `D2_L1_ZH_002` | slide | L1 | ZH | 361 | 59 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 345 | `D2_L1_ZH_003` | slide | L1 | ZH | 412 | 63 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 346 | `D2_L2_ZH_001` | slide | L2 | ZH | 572 | 87 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 347 | `D2_L2_ZH_002` | slide | L2 | ZH | 632 | 94 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 348 | `D2_L2_ZH_003` | slide | L2 | ZH | 586 | 87 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 349 | `D2_L3_ZH_001` | slide | L3 | ZH | 828 | 122 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 350 | `D2_L3_ZH_002` | slide | L3 | ZH | 857 | 128 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 351 | `D2_L3_ZH_003` | slide | L3 | ZH | 831 | 120 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 352 | `D3_L1_ZH_001` | social_media | L1 | ZH | 364 | 39 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 353 | `D3_L1_ZH_002` | social_media | L1 | ZH | 351 | 56 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 354 | `D3_L1_ZH_003` | social_media | L1 | ZH | 417 | 46 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 355 | `D3_L2_ZH_001` | social_media | L2 | ZH | 583 | 101 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 356 | `D3_L2_ZH_002` | social_media | L2 | ZH | 551 | 70 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 357 | `D3_L2_ZH_003` | social_media | L2 | ZH | 582 | 80 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 358 | `D3_L3_ZH_001` | social_media | L3 | ZH | 637 | 99 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 359 | `D3_L3_ZH_002` | social_media | L3 | ZH | 601 | 71 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 360 | `D3_L3_ZH_003` | social_media | L3 | ZH | 608 | 84 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 361 | `C4_L1_ZH_001` | product_pkg | L1 | ZH | 358 | 62 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 362 | `C4_L1_ZH_002` | product_pkg | L1 | ZH | 356 | 48 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 363 | `C4_L1_ZH_003` | product_pkg | L1 | ZH | 366 | 61 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 364 | `C4_L2_ZH_001` | product_pkg | L2 | ZH | 559 | 79 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 365 | `C4_L2_ZH_002` | product_pkg | L2 | ZH | 589 | 92 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 366 | `C4_L2_ZH_003` | product_pkg | L2 | ZH | 694 | 131 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 367 | `C4_L3_ZH_001` | product_pkg | L3 | ZH | 620 | 96 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 368 | `C4_L3_ZH_002` | product_pkg | L3 | ZH | 643 | 91 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 369 | `C4_L3_ZH_003` | product_pkg | L3 | ZH | 628 | 108 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 370 | `E2_L1_ZH_001` | form | L1 | ZH | 363 | 55 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 371 | `E2_L1_ZH_002` | form | L1 | ZH | 439 | 77 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 372 | `E2_L1_ZH_003` | form | L1 | ZH | 426 | 82 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 373 | `E2_L2_ZH_001` | form | L2 | ZH | 674 | 114 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 374 | `E2_L2_ZH_002` | form | L2 | ZH | 618 | 103 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 375 | `E2_L2_ZH_003` | form | L2 | ZH | 632 | 93 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 376 | `E2_L3_ZH_001` | form | L3 | ZH | 993 | 206 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 377 | `E2_L3_ZH_002` | form | L3 | ZH | 1036 | 179 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 378 | `E2_L3_ZH_003` | form | L3 | ZH | 1079 | 210 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 379 | `E3_L1_ZH_001` | certificate | L1 | ZH | 434 | 67 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 380 | `E3_L1_ZH_002` | certificate | L1 | ZH | 468 | 69 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 381 | `E3_L1_ZH_003` | certificate | L1 | ZH | 381 | 61 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 382 | `E3_L2_ZH_001` | certificate | L2 | ZH | 586 | 99 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 383 | `E3_L2_ZH_002` | certificate | L2 | ZH | 633 | 94 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 384 | `E3_L2_ZH_003` | certificate | L2 | ZH | 557 | 87 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 385 | `E3_L3_ZH_001` | certificate | L3 | ZH | 977 | 147 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 386 | `E3_L3_ZH_002` | certificate | L3 | ZH | 969 | 136 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 387 | `E3_L3_ZH_003` | certificate | L3 | ZH | 904 | 129 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 388 | `E4_L1_ZH_001` | code | L1 | ZH | 396 | 48 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 389 | `E4_L1_ZH_002` | code | L1 | ZH | 511 | 88 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 390 | `E4_L1_ZH_003` | code | L1 | ZH | 430 | 58 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 391 | `E4_L2_ZH_001` | code | L2 | ZH | 807 | 112 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 392 | `E4_L2_ZH_002` | code | L2 | ZH | 892 | 117 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 393 | `E4_L2_ZH_003` | code | L2 | ZH | 856 | 105 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 394 | `E4_L3_ZH_001` | code | L3 | ZH | 959 | 132 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 395 | `E4_L3_ZH_002` | code | L3 | ZH | 725 | 91 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 396 | `E4_L3_ZH_003` | code | L3 | ZH | 776 | 140 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 397 | `F1_L1_ZH_001` | caption | L1 | ZH | 532 | 98 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 398 | `F1_L1_ZH_002` | caption | L1 | ZH | 417 | 50 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 399 | `F1_L1_ZH_003` | caption | L1 | ZH | 368 | 61 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 400 | `F1_L2_ZH_001` | caption | L2 | ZH | 591 | 75 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 401 | `F1_L2_ZH_002` | caption | L2 | ZH | 602 | 129 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 402 | `F1_L2_ZH_003` | caption | L2 | ZH | 596 | 82 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 403 | `F1_L3_ZH_001` | caption | L3 | ZH | 676 | 106 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 404 | `F1_L3_ZH_002` | caption | L3 | ZH | 618 | 125 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 405 | `F1_L3_ZH_003` | caption | L3 | ZH | 649 | 88 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 406 | `F2_L1_ZH_001` | dialogue | L1 | ZH | 350 | 60 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 407 | `F2_L1_ZH_002` | dialogue | L1 | ZH | 360 | 57 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 408 | `F2_L1_ZH_003` | dialogue | L1 | ZH | 392 | 46 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 409 | `F2_L2_ZH_001` | dialogue | L2 | ZH | 655 | 105 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 410 | `F2_L2_ZH_002` | dialogue | L2 | ZH | 582 | 77 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 411 | `F2_L2_ZH_003` | dialogue | L2 | ZH | 587 | 83 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 412 | `F2_L3_ZH_001` | dialogue | L3 | ZH | 616 | 96 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 413 | `F2_L3_ZH_002` | dialogue | L3 | ZH | 631 | 106 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 414 | `F2_L3_ZH_003` | dialogue | L3 | ZH | 621 | 114 | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 415 | `F3_L1_ZH_001` | comic_panel | L1 | ZH | 369 | 54 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 416 | `F3_L1_ZH_002` | comic_panel | L1 | ZH | 356 | 56 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 417 | `F3_L1_ZH_003` | comic_panel | L1 | ZH | 366 | 56 | 5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 418 | `F3_L2_ZH_001` | comic_panel | L2 | ZH | 633 | 96 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 419 | `F3_L2_ZH_002` | comic_panel | L2 | ZH | 594 | 88 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 420 | `F3_L2_ZH_003` | comic_panel | L2 | ZH | 652 | 85 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 421 | `F3_L3_ZH_001` | comic_panel | L3 | ZH | 692 | 91 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 422 | `F3_L3_ZH_002` | comic_panel | L3 | ZH | 607 | 89 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 423 | `F3_L3_ZH_003` | comic_panel | L3 | ZH | 623 | 74 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 424 | `F4_L1_ZH_001` | infographic | L1 | ZH | 353 | 60 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 425 | `F4_L1_ZH_002` | infographic | L1 | ZH | 386 | 50 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 426 | `F4_L1_ZH_003` | infographic | L1 | ZH | 361 | 64 | 4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 427 | `F4_L2_ZH_001` | infographic | L2 | ZH | 569 | 90 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 428 | `F4_L2_ZH_002` | infographic | L2 | ZH | 567 | 108 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 429 | `F4_L2_ZH_003` | infographic | L2 | ZH | 650 | 96 | 6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 430 | `F4_L3_ZH_001` | infographic | L3 | ZH | 839 | 112 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 431 | `F4_L3_ZH_002` | infographic | L3 | ZH | 941 | 104 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |
| 432 | `F4_L3_ZH_003` | infographic | L3 | ZH | 934 | 170 | 8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CLEAR | CLEAR | PASS |

## 硬门禁汇总

| 检查项 | 通过数 | 通过率 |
|---|---:|---:|
| 字符范围 | 432/432 | 100.0% |
| GT 单次嵌入 | 432/432 | 100.0% |
| stats 一致 | 432/432 | 100.0% |
| 结构完整 | 432/432 | 100.0% |
| ID/类别一致 | 432/432 | 100.0% |
| 固定内容扫描 | 432/432 | 100.0% |
| 独立内容签核 | 432/432 | 100.0% |
| **综合** | **432/432** | **100.0%** |

## 非阻断观察

| 观察信号 | 命中数 | 命中率 |
|---|---:|---:|
| 窄范围政治关键词 | 0/432 | 0.0% |
| 中国手机号/常规邮箱模式 | 0/432 | 0.0% |

观察信号只用于必要时的人工复核；`CLEAR` 不声明“无政治内容”或“无隐私风险”，`OBSERVED` 也不等于违规。

## 交付确认

所有结构门禁及独立内容签核均通过；报告、audit_rows、prompts_map、build 由同一输入快照在内存生成并经反向校验。

内容签核人：Codex independent content review
内容签核时间：2026-08-16T14:39:03Z
自动化门禁：code_v8/scripts/rebuild_audit_snapshots.py
