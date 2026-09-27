# Third-party notices and LANCET Nano v0.4.0 fitting provenance

## Included components

| Component | License / evidence | Notice retained |
|---|---|---|
| LANCET Nano model assets | Apache-2.0 | [Explicit model grant](MODEL-LICENSE.md), [full text](licenses/Apache-2.0.txt), [changes](MODIFICATIONS.md) |
| Salesforce CodeT5+ 220M pretrained model | BSD-3-Clause declaration at revision `2b92f36e2782341a50551759fdba0dd15e821f99` | [Original upstream card](licenses/codet5p-220m-upstream-model-card.md), [Salesforce BSD-3-Clause notice](licenses/CodeT5-BSD-3-Clause.txt), [credits](NOTICE.txt) |
| CodeT5 tokenizer file (byte-identical to CodeT5-small's) | Apache-2.0 declaration at revision `b1ee9570c289f21b5922b9c768a1ce12957bf968` | [Original upstream card](licenses/codet5-small-upstream-model-card.md) |
| LANCET runtime / project-authored tooling | MIT | [Tanner Middleton notice](licenses/pi-jev-guard-MIT.txt) |
| NumPy, Hugging Face tokenizers, ONNX Runtime CPU | Their own licenses | Pinned in `requirements.txt`; not vendored |

## Fitting sources: datasets not included

| Source | Fit rows | How it was used | Terms and preserved evidence |
|---|---:|---|---|
| LANCET project-authored contrast recipes | 9,184 | Risky/benign pairs | Project-authored |
| LANCET secrets family | 5,328 | Agent-authored reveal-vs-metadata pairs | Project-authored |
| LANCET released evaluation suites | 4,637 | Commands with their original authored labels | Project-authored (agent-authored). Stored hosted-model outputs in those files were not used. |
| LANCET red-team corpus | 522 | Commands with the author's danger ranking; recorded model scores removed | Project-authored |
| ShellRisk-Bench (Kontext Security), rev `437467862139b4e9cdd5322024ef3434a67c7ec8`, training split | 5,968 | Commands with upstream source labels (see next four rows) | Compilation by Kontext Security; each upstream source keeps its own terms |
| ↳ Kwai-Klear / SWE-smith trajectories | 3,519 | Benign | MIT; [declaration](licenses/SWE-smith-license-declaration.md), [MIT text](licenses/MIT.txt) |
| ↳ yoonholee / Terminal-Bench trajectories | 2,315 | Benign | Apache-2.0; [declaration](licenses/Terminal-Bench-license-declaration.md) |
| ↳ Red Canary / Atomic Red Team | 120 | Risky | MIT; [license](licenses/atomic-red-team-MIT.txt) |
| ↳ swisskyrepo / InternalAllTheThings, rev `203bb0c0b290bf7c9158c32d43523b8d66f292c1` | 14 | Risky | No license declared |
| Kwai-Klear / SWE-smith trajectories (V5 inspection pool) | 2,154 | Benign commands | MIT; [declaration](licenses/SWE-smith-license-declaration.md), [MIT text](licenses/MIT.txt) |
| yoonholee / Terminal-Bench trajectories (V5 inspection pool) | 748 | Benign commands | Apache-2.0; [declaration](licenses/Terminal-Bench-license-declaration.md) |
| TellinaTool / NL2Bash `data/bash` (V5 inspection pool) | 152 | Benign commands | MIT; [dataset notice](licenses/NL2Bash-data-MIT.txt) |
| tldr-pages, rev `998e3f02b8924a7d5112fe6099993d3625fb404c` | 6,121 | Example commands, placeholders filled; labels from description wording | CC BY 4.0; [license notice](licenses/tldr-pages-LICENSE.md), <https://creativecommons.org/licenses/by/4.0/> |
| botocore 1.43.103 service models (wheel SHA-256 `6a6a561a…bd67c`) | 927 | Generated `aws <service> <operation>` shapes; labels from operation verbs and `sensitive` output fields | Apache-2.0; [NOTICE](licenses/botocore-NOTICE.txt), [full text](licenses/Apache-2.0.txt) |
| Azure CLI, rev `7bf31a4fd49c252209732a8b0cf874ecaccdf06a` | 1,118 | Reference examples; labels from verbs and descriptions | MIT; [license](licenses/azure-cli-LICENSE.txt) |
| GitHub CLI, rev `9b031151a825bda919203c5202876a725d637368` | 156 | Reference examples | MIT; [license](licenses/gh-cli-LICENSE.txt) |
| Docker CLI, rev `7fc2dff9bceb96b266a3b2c3117c0955a0d9e616` | 99 | Reference examples | Apache-2.0; [license](licenses/docker-cli-LICENSE.txt), [NOTICE](licenses/docker-cli-NOTICE.txt) |
| kubectl, rev `269cea948d6870de9e66cfc535d1cf808083a94a` | 55 | Reference examples | Apache-2.0; [license](licenses/kubectl-LICENSE.txt) |

The development and calibration roles held a further 24,378 rows from tools, services, secrets tools and evaluation-suite families separate from fitting.

Every inspection command belongs to the 5,213-row V5 inspection pool, which V5's provenance audit matched to the pinned ShellRisk-Bench training Parquet ([receipt](provenance/v5-lineage-audit.json)). No V5 weights were used for v0.4.0. GTFOBins rows are not in the fitting data.

**No hosted-model output was used.** Labels come from project authoring, the original authored labels of released evaluation suites, upstream source labels, source-inferred benign status or deterministic documentation rules. No language model, including TypeSafe's Jev, produced any label, teacher target, filter or selection signal.

No raw datasets, source trajectories, private logs, evaluation corpora, fitting checkpoints or vendored dependency packages are included. The model license does **not** relicense any of those materials.
