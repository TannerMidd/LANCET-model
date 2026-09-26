# LANCET Nano model card

## Identity and license

- **LANCET Nano**, v0.2.0. Internal research ID: `doc-labels-1 / N2`, seed 8201.
- Model license: **Apache-2.0**, with an [explicit scope](MODEL-LICENSE.md). Runtime: **MIT**, see the [notice](licenses/pi-jev-guard-MIT.txt).
- Base: Salesforce/codet5-small, revision `b1ee9570c289f21b5922b9c768a1ce12957bf968`.
- Architecture: CodeT5 encoder, masked mean pooling, layer normalization and a binary classifier head. No generative decoder is used at inference.
- Parameters: **35,318,017**. CPU INT8 ONNX, 35,727,419 bytes.
- ONNX SHA-256: `183ae5051fffe8578267c524efb78ef82c2f668f1e575690923ced8c5f1827f5`.
- Calibration: positive-slope Platt fit on a held calibration role only, with scale `1.022610154824388` and bias `-0.6326081110722507`.
- Output bands:
  - `risky`: score ≥ `0.9609579634556733`
  - `review`: score ≥ `0.6294868088136047`
  - `not_flagged`: below the review threshold

## Fitting lineage

Pinned CodeT5-small → V4 → **V5** (released as v0.1.0) → fine-tuning with class-balanced sampling (this release). The selected epoch was 4, with the two best epochs averaged. Nano uses V5's tokenizer unchanged.

Nano was fine-tuned on 20,128 rows:

| Source | Rows | Label basis |
|---|---:|---|
| LANCET project-authored contrast recipes | 10,342 | Project-authored risky/benign pairs (not human-adjudicated) |
| SWE-smith, Terminal-Bench and NL2Bash commands (a subset of V5's audited inspection pool) | 3,054 | Source-inferred benign |
| tldr-pages example commands (CC BY 4.0, rev `998e3f02`) | 5,852 | **Wording of each example's human-written description**, by frozen rules (for example "Delete…", "Destroy…" → risky; "List…", "Show…" → benign; ambiguous wording is dropped) |
| AWS CLI command shapes from botocore service models (Apache-2.0, 1.43.103) | 880 | **The operation verb** (`Delete*`, `Terminate*`, `Revoke*`, secret reads → risky; `List*`, `Describe*`, `Get*` → benign) |

The documentation labels come from deterministic rules. **No language model, hosted API or human labeler produced any training label, teacher target or selection signal.** In particular, no output from Jev (TypeSafe) or any other hosted model was used in fitting, selection or calibration.

The rules are in the research repository (`research/doc_labels/sources.py`, `doc-rules-4`). They were tightened by reading random candidate samples before data roles were assigned. Their precision was estimated only by the developer (an AI agent) reading samples, at roughly 85–90% for risky labels. They are heuristic and not adjudicated.

Development and calibration rows came from tools and AWS services not used in fitting (unit-isolated roles). Any documentation unit resembling a registered evaluation case was removed completely before sampling. The datasets themselves are not distributed.

## Evidence

The development-selected model was scored once on a fresh, sealed 400-command diagnostic suite (211 risky, 189 benign, 85 tool families). The suite's labels were written by the developer (an AI agent) and screened against all fitting data:

| | LANCET Nano | V5 (v0.1.0) |
|---|---:|---:|
| Risky caught (`risky` or `review`) | **83.9%** (177/211) | 76.3% |
| Benign interrupted | **5.8%** (11/189) | 8.5% |
| AUROC | 0.935 | 0.902 |

For context, two other models were scored once on the same suite: hosted Jev caught 97.6% and interrupted 4.8%; the local Laya model caught 77.7% and interrupted 42.9%. Both had a fixed task context; Nano sees only the command.

Median warm CPU time was 2.7 ms per command on Ryzen 9 3900X / Windows 11 (four intra-op threads, batch one). This is an observation, not a hardware-independent guarantee.

**This is diagnostic evidence, not independent acceptance.** The suite is agent-authored and small. Independent acceptance and human label adjudication remain unavailable. Nano starts from V5, so it inherits V5's historical benchmark exposure. The gain over a V5 retrain without documentation labels was not statistically confirmed on development data.

## Intended use and limitations

Nano is a research component for **Bash command-risk review, not an execution authority**. Inputs are inert text. It has no access to filesystem state, fetched script contents or task context.

- PowerShell, invalid or unsupported input, more than 8,192 UTF-8 bytes or more than 512 tokens return `review`. Inputs are never silently truncated.
- **`not_flagged` does not guarantee safety.** Every result carries `experimental: true` and `executionAuthorized: false`. These warnings describe the evidence and impose no extra license restriction.

## Release scope

- The model and tokenizer bytes are those produced and scored by the research pipeline.
- The runtime `classify.py` was checked for exact parity against the research runtime on development rows.
- Runtime dependencies (NumPy, tokenizers, ONNX Runtime CPU) are installed separately and not bundled.
- No PyTorch, Transformers, network access or later model download is needed for inference.
