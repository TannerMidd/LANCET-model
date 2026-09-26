# LANCET Nano model card

## Identity and license

- **LANCET Nano**, v0.3.0. Internal research ID: `doc-labels-6 / B3`, seed 9201.
- Model license: **Apache-2.0**, with an [explicit scope](MODEL-LICENSE.md). Runtime: **MIT**, see the [notice](licenses/pi-jev-guard-MIT.txt).
- Base: Salesforce/codet5-base, revision `02cd2d31bb7c6d0e4d91156167b2de044989c733`. Its [upstream model card](licenses/codet5-base-upstream-model-card.md) declares Apache-2.0.
- Architecture: CodeT5-base encoder, masked mean pooling, layer normalization and a binary classifier head. No generative decoder is used at inference.
- Parameters: **109,609,345**. CPU INT8 ONNX, 110,560,712 bytes.
- ONNX SHA-256: `b635571b0c55fba5224a00e2c9132918db816b76c433e8c8dc75d151ef03de1c`.
- Tokenizer: byte-identical to v0.1.0's and v0.2.0's CodeT5 byte-BPE tokenizer.
- Calibration: positive-slope Platt fit on a held calibration role only, with scale `0.8416362250422593` and bias `-0.7429544835543572`.
- Output bands:
  - `risky`: score ≥ `0.8965157725433559`
  - `review`: score ≥ `0.7715354869912129`
  - `not_flagged`: below the review threshold

## Fitting lineage

Pinned upstream CodeT5-base → fine-tuning (this release). **No earlier LANCET checkpoint was used as an initializer or teacher.** This is the first clean-start Nano.

Training used class-balanced sampling, a training-only risk-type head that is not exported, and a pair-margin loss on authored pairs. Epoch 7 was selected on held-out development groups.

Training used 31,127 rows:

| Source | Rows | Label basis |
|---|---:|---|
| LANCET project-authored contrast recipes | 9,906 | Project-authored risky/benign pairs |
| LANCET secrets family (agent-authored reveal-vs-metadata pairs, 20 tools) | 5,328 | Project-authored pairs |
| LANCET's retired agent-authored evaluation suites (see below) | 4,358 | Their original authored labels |
| SWE-smith, Terminal-Bench and NL2Bash commands (V5's audited inspection pool) | 3,054 | Source-inferred benign |
| tldr-pages example commands (CC BY 4.0) | 6,126 | Description wording, by frozen rules |
| Azure CLI reference examples (MIT) | 1,118 | Command verb and description, by rules |
| AWS CLI command shapes from botocore models (Apache-2.0) | 927 | Operation verb; credential-returning operations (AWS `sensitive` output fields) are risky |
| GitHub CLI (MIT), Docker CLI (Apache-2.0), kubectl (Apache-2.0) examples | 310 | Command verb and description, by rules |

**About the retired evaluation suites:**
- The owner released LANCET's used, agent-authored evaluation suites for training: sealed-eval-1/2/3, the novel-V5 diagnostic and pool, eval150, matrix, study-validation, authored-holdout, and Devious v2.
- Only their commands and original authored `label`/`expect` fields were used, never any hosted-model outputs stored alongside them.
- They no longer count as held-out evidence for this model.

**About the documentation labels (`doc-rules-7`):**
- They come from deterministic rules in the research repository (`research/doc_labels/sources*.py`).
- They are heuristic, were reviewed only by the developer (an AI agent) on samples, and are not human-adjudicated.
- **No language model, hosted API or human labeler produced any training label, teacher target or selection signal.** No output from Jev (TypeSafe) or any other hosted model was used.

Development and calibration came from tools, services and families separate from fitting. The datasets themselves are not distributed.

## Evidence

The development-selected model was scored once on `lancet-bench-1`. The benchmark has 793 agent-authored commands (409 risky, 384 benign) across 37 areas, and was frozen and screened against all fitting data before this training data existed:

| | v0.3.0 | v0.2.0 | v0.1.0 | Jev (hosted) |
|---|---:|---:|---:|---:|
| Risky caught (`risky` or `review`) | **85.8%** (351/409) | 73.6% | 65.5% | 96.8% |
| Safe interrupted | **5.5%** (21/384) | 6.2% | 5.5% | 7.8% |
| AUROC | 0.962 | 0.896 | 0.860 | 0.982 |
| Risky secrets caught (112) | **66%** | 24% | 14% | 98% |

- **Against v0.2.0** (paired bootstrap by family, 95%): catch rate **+12.2 points [+6.4, +17.7]**; interruption −0.8 points [−3.2, +1.6].
- **Weaker areas:** v0.3.0 is weaker than v0.2.0 on network/remote execution (68% vs 91%, 22 risky cases) and infrastructure-as-code (83% vs 92%, 12 cases).
- **Jev comparison:** Jev saw a fixed task context; Nano sees only the command.

**ShellRisk upstream sets** (not agent-authored; never used for fitting or selection):

| | source-external caught (176) | safe interrupted (3,313) | AUROC | source-holdout caught (74) | safe interrupted (1,594) | AUROC |
|---|---:|---:|---:|---:|---:|---:|
| v0.3.0 | 48.9% | **6.3%** | 0.847 | 41.9% | **6.0%** | 0.805 |
| v0.2.0 | 48.3% | 9.7% | 0.852 | 45.9% | 9.3% | 0.860 |

**Release gate and exception.** Four checks against v0.2.0 were preregistered.

- **Passed:** benchmark catch-rate gain, benchmark interruption, and ShellRisk interruption.
- **Failed:** the ShellRisk catch-rate check required the 95% lower bound to be at least −5 points. The observed difference was +0.6 points [−6.5, +7.8].
- **Why it failed:** with 176 risky commands, even a model with an equal catch rate would usually fail that check. This design error is disclosed, and the rule was not changed after scoring.
- **Decision:** the owner approved release as a documented exception. See `provenance/release-gate.json`.
- **Caution:** the lower upstream AUROC and source-holdout catch rate are real cautions for commands resembling that distribution.

**Speed.** Median warm CPU time was 21.8 ms per command (p95 33.7 ms), against 6.4 ms for v0.2.0 in the same run. The machine was a busy Ryzen 9 3900X / Windows 11, with four intra-op threads and batch one. These are observations, not hardware-independent guarantees.

**This is diagnostic evidence, not independent acceptance.** The benchmark is agent-authored, and the same agent wrote much of the training data, so correlation is possible. The benchmark has also informed two development rounds. Independent acceptance and human label adjudication remain unavailable.

## Intended use and limitations

Nano is a research component for **Bash command-risk review, not an execution authority**. Inputs are inert text. It has no access to filesystem state, fetched script contents or task context.

- PowerShell, invalid or unsupported input, more than 8,192 UTF-8 bytes or more than 512 tokens return `review`. Inputs are never silently truncated.
- **`not_flagged` does not guarantee safety.** Every result carries `experimental: true` and `executionAuthorized: false`. These warnings describe the evidence and impose no extra license restriction.

## Release scope

- The model and tokenizer bytes are those produced and scored by the research pipeline.
- The runtime `classify.py` is unchanged from v0.2.0. It reads thresholds and calibration from `model.json`.
- Runtime dependencies (NumPy, tokenizers, ONNX Runtime CPU) are installed separately and not bundled.
- No PyTorch, Transformers, network access or later model download is needed for inference.
