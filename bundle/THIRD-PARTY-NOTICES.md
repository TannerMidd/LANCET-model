# Third-party notices and V5 fitting provenance

## Included components

| Component | License/evidence | Notice retained |
|---|---|---|
| LANCET V5 model assets | Apache-2.0 | [Explicit model grant](MODEL-LICENSE.md), [full text](licenses/Apache-2.0.txt), [changes](MODIFICATIONS.md) |
| Salesforce CodeT5-small pretrained model/tokenizer | Apache-2.0 declaration at revision `b1ee9570c289f21b5922b9c768a1ce12957bf968` | [Original upstream card](licenses/codet5-small-upstream-model-card.md), [credits](NOTICE.txt) |
| Separate CodeT5 source-project attribution | BSD-3-Clause at revision `208acbd759fd8014374387b272647ef7ab4b85e3` | [Complete Salesforce notice/disclaimer](licenses/CodeT5-BSD-3-Clause.txt) |
| LANCET runtime/project-authored tooling | MIT | [Original Tanner Middleton notice](licenses/pi-jev-guard-MIT.txt) |
| NumPy, Hugging Face tokenizers, ONNX Runtime CPU | Separate dependency distributions and their own licenses | Versions are pinned in `requirements.txt`; packages are not vendored in the archive |

The inspected pinned CodeT5 model tree had no standalone NOTICE file. The inspected CodeT5 source tree at the stated license revision had no NOTICE/COPYING file. Available original cards, copyright notices, complete license texts and downstream-change notices are retained. No endorsement is claimed.

## Actual V4/V5 source lineage — datasets not included

The model lineage is pinned upstream CodeT5-small → V4 epoch 13 → V5 rehearsal epoch 8 → balanced threshold profile, with no further fitting. V4 did not inherit a V1/V2/V3 fine-tuned model. It used project cases and project-authored contrast recipes. V5 added the following source-inferred inspection negatives:

| External source | Eligible train | Development | Calibration | Declared terms and preserved evidence |
|---|---:|---:|---:|---|
| Kwai-Klear / SWE-smith trajectories | 2,806 | 417 | 422 | MIT; [pinned declaration](licenses/SWE-smith-license-declaration.md), [full MIT text](licenses/MIT.txt) |
| yoonholee / Terminal-Bench trajectories | 984 | 129 | 178 | Apache-2.0; [pinned declaration](licenses/Terminal-Bench-license-declaration.md), [full Apache text](licenses/Apache-2.0.txt) |
| TellinaTool / NL2Bash `data/bash` | 199 | 31 | 47 | MIT; [full original dataset notice](licenses/NL2Bash-data-MIT.txt), copyright (c) 2020 NL2Bash dataset |

NL2Bash revision `d6b9f5bdff45621d190134e31ab63b7bf7002190` [explicitly licenses `data/bash` separately under MIT](https://github.com/TellinaTool/nl2bash/blob/d6b9f5bdff45621d190134e31ab63b7bf7002190/README.md). Its root GPL code badge is not the license of those dataset files. NL2Bash parser/translation-model source code is not bundled.

Kontext Security / [ShellRisk-Bench](https://huggingface.co/datasets/kontext-security/ShellRisk-Bench/tree/437467862139b4e9cdd5322024ef3434a67c7ec8) supplies the original collection/normalization provenance. Its [pinned source document](https://github.com/kontext-security/shellrisk-bench/blob/616e89cb07e10df12b24d596b3034d8b19edb8cd/DATASETS.md) identifies these upstream revisions and makes clear that its code/documentation license does not relicense the data.

All 5,213 inspection train/development/calibration rows were matched locally to the pinned original training Parquet by exact contents, source, upstream ID and label. Counts describe eligible pools, not unique optimizer-sampled examples. The V4/V5 fitting pools contain no rows attributed to GTFOBins, InternalAllTheThings/payloads or Atomic Red Team. Their presence elsewhere in the broader ShellRisk collection must not be misreported as V5 fitting exposure. Source-inferred labels are not independent human adjudication.

## Remaining limits

The source declarations are permissive, but they do not independently establish every publisher's rights to all embedded third-party content. Terminal-Bench's card describes scraped public leaderboard trajectories; NL2Bash describes website/StackOverflow-derived examples; SWE-smith trajectories involve third-party repositories. LANCET has not certified chain of title for each underlying snippet or audited every CodeT5 pretraining example. The technical provenance audit is not legal certification.

No raw datasets, source trajectories, private logs, evaluation corpora, historical fitting checkpoints or vendored dependency packages are included in the model archive. The explicit model license does **not** relicense any of those materials or other research checkpoints.

Historical extraction/model README documents are retained as provenance. Their pre-release wording is distinguished from the current grant in [MODEL-LICENSE.md](MODEL-LICENSE.md); the frozen model and runtime files themselves are unchanged.
