# Third-party notices and LANCET Nano fitting provenance

## Included components

| Component | License / evidence | Notice retained |
|---|---|---|
| LANCET Nano model assets | Apache-2.0 | [Explicit model grant](MODEL-LICENSE.md), [full text](licenses/Apache-2.0.txt), [changes](MODIFICATIONS.md) |
| Salesforce CodeT5-small pretrained model/tokenizer | Apache-2.0 declaration at revision `b1ee9570c289f21b5922b9c768a1ce12957bf968` | [Original upstream card](licenses/codet5-small-upstream-model-card.md), [credits](NOTICE.txt) |
| Separate CodeT5 source-project attribution | BSD-3-Clause | [Complete Salesforce notice](licenses/CodeT5-BSD-3-Clause.txt) |
| LANCET runtime / project-authored tooling | MIT | [Tanner Middleton notice](licenses/pi-jev-guard-MIT.txt) |
| NumPy, Hugging Face tokenizers, ONNX Runtime CPU | Their own licenses | Pinned in `requirements.txt`; not vendored |

## Nano fitting sources: datasets not included

| Source | Fit rows | How it was used | Terms and preserved evidence |
|---|---:|---|---|
| LANCET project-authored contrast recipes | 10,342 | Risky/benign pairs | Project-authored |
| Kwai-Klear / SWE-smith trajectories | 2,154 | Benign commands (subset of V5's audited pool) | MIT; [declaration](licenses/SWE-smith-license-declaration.md), [MIT text](licenses/MIT.txt) |
| yoonholee / Terminal-Bench trajectories | 748 | Benign commands (subset of V5's audited pool) | Apache-2.0; [declaration](licenses/Terminal-Bench-license-declaration.md) |
| TellinaTool / NL2Bash `data/bash` | 152 | Benign commands (subset of V5's audited pool) | MIT; [dataset notice](licenses/NL2Bash-data-MIT.txt) |
| tldr-pages, rev `998e3f02b8924a7d5112fe6099993d3625fb404c` (`common`, `linux`, `osx` pages) | 5,852 | Example commands, placeholders filled; labels from the description wording | CC BY 4.0; [license notice](licenses/tldr-pages-LICENSE.md), <https://creativecommons.org/licenses/by/4.0/> |
| botocore 1.43.103 service models (wheel SHA-256 `6a6a561a…bd67c`) | 880 | Generated `aws <service> <operation> --required-param value` shapes; labels from operation verbs | Apache-2.0; [NOTICE](licenses/botocore-NOTICE.txt), [full text](licenses/Apache-2.0.txt) |

The development and calibration roles held a further 3,001 documentation rows from tools and services separate from fitting. They also held development and calibration rows from the same authored and inspection sources.

Every inspection command in Nano's fitting, development and calibration roles belongs to the 5,213-row V5 inspection pool. V5's provenance audit matched that pool to the pinned original ShellRisk-Bench training Parquet ([receipt](provenance/v5-lineage-audit.json)). The rows attributed to Atomic Red Team, GTFOBins or payload collections are not in Nano's fitting data.

**No hosted-model output was used.** Labels come from project authoring, source-inferred benign status or deterministic documentation rules. No language model, including TypeSafe's Jev, produced any label, teacher target, filter or selection signal for Nano.

## Remaining limits

The source declarations are permissive, but they do not independently establish every publisher's rights to all embedded third-party content. LANCET has not certified the chain of title for every underlying snippet, and has not audited every CodeT5 pretraining example. The technical provenance audit is not legal certification.

No raw datasets, source trajectories, private logs, evaluation corpora, fitting checkpoints or vendored dependency packages are included. The model license does **not** relicense any of those materials.
