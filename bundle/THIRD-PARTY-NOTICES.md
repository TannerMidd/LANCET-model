# Third-party notices and LANCET Nano v0.3.0 fitting provenance

## Included components

| Component | License / evidence | Notice retained |
|---|---|---|
| LANCET Nano model assets | Apache-2.0 | [Explicit model grant](MODEL-LICENSE.md), [full text](licenses/Apache-2.0.txt), [changes](MODIFICATIONS.md) |
| Salesforce CodeT5-base pretrained model | Apache-2.0 declaration at revision `02cd2d31bb7c6d0e4d91156167b2de044989c733` | [Original upstream card](licenses/codet5-base-upstream-model-card.md), [credits](NOTICE.txt) |
| CodeT5 tokenizer file (byte-identical to CodeT5-small's) | Apache-2.0 declaration at revision `b1ee9570c289f21b5922b9c768a1ce12957bf968` | [Original upstream card](licenses/codet5-small-upstream-model-card.md) |
| Separate CodeT5 source-project attribution | BSD-3-Clause | [Complete Salesforce notice](licenses/CodeT5-BSD-3-Clause.txt) |
| LANCET runtime / project-authored tooling | MIT | [Tanner Middleton notice](licenses/pi-jev-guard-MIT.txt) |
| NumPy, Hugging Face tokenizers, ONNX Runtime CPU | Their own licenses | Pinned in `requirements.txt`; not vendored |

## Fitting sources: datasets not included

| Source | Fit rows | How it was used | Terms and preserved evidence |
|---|---:|---|---|
| LANCET project-authored contrast recipes | 9,906 | Risky/benign pairs | Project-authored |
| LANCET secrets family | 5,328 | Agent-authored reveal-vs-metadata pairs | Project-authored |
| LANCET retired evaluation suites | 4,358 | Commands with their original authored labels | Project-authored (agent-authored). Stored hosted-model outputs in those files were not used. |
| Kwai-Klear / SWE-smith trajectories | 2,154 | Benign commands (subset of V5's audited pool) | MIT; [declaration](licenses/SWE-smith-license-declaration.md), [MIT text](licenses/MIT.txt) |
| yoonholee / Terminal-Bench trajectories | 748 | Benign commands (subset of V5's audited pool) | Apache-2.0; [declaration](licenses/Terminal-Bench-license-declaration.md) |
| TellinaTool / NL2Bash `data/bash` | 152 | Benign commands (subset of V5's audited pool) | MIT; [dataset notice](licenses/NL2Bash-data-MIT.txt) |
| tldr-pages, rev `998e3f02b8924a7d5112fe6099993d3625fb404c` | 6,126 | Example commands, placeholders filled; labels from description wording | CC BY 4.0; [license notice](licenses/tldr-pages-LICENSE.md), <https://creativecommons.org/licenses/by/4.0/> |
| botocore 1.43.103 service models (wheel SHA-256 `6a6a561a…bd67c`) | 927 | Generated `aws <service> <operation>` shapes; labels from operation verbs and `sensitive` output fields | Apache-2.0; [NOTICE](licenses/botocore-NOTICE.txt), [full text](licenses/Apache-2.0.txt) |
| Azure CLI, rev `7bf31a4fd49c252209732a8b0cf874ecaccdf06a` | 1,118 | Reference examples; labels from verbs and descriptions | MIT; [license](licenses/azure-cli-LICENSE.txt) |
| GitHub CLI, rev `9b031151a825bda919203c5202876a725d637368` | 156 | Reference examples | MIT; [license](licenses/gh-cli-LICENSE.txt) |
| Docker CLI, rev `7fc2dff9bceb96b266a3b2c3117c0955a0d9e616` | 99 | Reference examples | Apache-2.0; [license](licenses/docker-cli-LICENSE.txt), [NOTICE](licenses/docker-cli-NOTICE.txt) |
| kubectl, rev `269cea948d6870de9e66cfc535d1cf808083a94a` | 55 | Reference examples | Apache-2.0; [license](licenses/kubectl-LICENSE.txt) |

The development and calibration roles held a further 21,652 rows from tools, services, secrets tools and evaluation-suite families separate from fitting.

Every inspection command belongs to the 5,213-row V5 inspection pool. V5's provenance audit matched that pool to the pinned original ShellRisk-Bench training Parquet ([receipt](provenance/v5-lineage-audit.json)). No V5 weights were used for v0.3.0. Rows attributed to Atomic Red Team, GTFOBins or payload collections are not in the fitting data.

**No hosted-model output was used.** Labels come from project authoring, the original authored labels of retired evaluation suites, source-inferred benign status or deterministic documentation rules. No language model, including TypeSafe's Jev, produced any label, teacher target, filter or selection signal.

## Remaining limits

The source declarations are permissive, but they do not independently establish every publisher's rights to all embedded third-party content. LANCET has not certified the chain of title for every underlying snippet, and has not audited every CodeT5 pretraining example. The technical provenance audit is not legal certification.

No raw datasets, source trajectories, private logs, evaluation corpora, fitting checkpoints or vendored dependency packages are included. The model license does **not** relicense any of those materials.
