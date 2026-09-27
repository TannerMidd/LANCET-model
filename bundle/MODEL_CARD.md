# LANCET Nano model card

## Identity and license

- **LANCET Nano**, v0.4.0. Internal research ID: `doc-labels-9b / H1`, seed 9601.
- Model license: **Apache-2.0**, with an [explicit scope](MODEL-LICENSE.md). Runtime: **MIT**, see the [notice](licenses/pi-jev-guard-MIT.txt).
- Base: Salesforce/codet5p-220m, revision `2b92f36e2782341a50551759fdba0dd15e821f99`. Its [upstream model card](licenses/codet5p-220m-upstream-model-card.md) declares BSD-3-Clause; the [Salesforce notice](licenses/CodeT5-BSD-3-Clause.txt) is retained.
- Architecture: CodeT5+ 220M encoder, masked mean pooling, layer normalization and a binary classifier head. No generative decoder is used at inference.
- Parameters: **109,614,728**. CPU INT8 ONNX, 110,560,709 bytes.
- ONNX SHA-256: `f412c91867f769aa2b7b0bd5625b460efeb2018fcc5bddd4b39f09dfd2dc4f32`.
- Tokenizer: byte-identical to the CodeT5 byte-BPE tokenizer shipped with v0.1.0–v0.3.0 (CodeT5+ uses the same vocabulary and merges).
- Calibration: positive-slope Platt fit on a held calibration role only, with scale `0.8128674983663715` and bias `-0.8842568794525207`.
- Output bands:
  - `risky`: score ≥ `0.8795421382252008`
  - `review`: score ≥ `0.8188976760554079`
  - `not_flagged`: below the review threshold

## Fitting lineage

Pinned upstream CodeT5+ 220M → fine-tuning (this release). **No earlier LANCET checkpoint was used as an initializer or teacher.**

Training used domain-weighted, label-balanced sampling, a training-only risk-type head that is not exported, and a pair-margin loss on authored pairs. The exported weights are the average of the three best epochs (3, 6 and 8), chosen on held-out development groups.

Training used 37,169 rows:

| Source | Rows | Label basis |
|---|---:|---|
| LANCET project-authored contrast recipes | 9,184 | Project-authored risky/benign pairs |
| tldr-pages example commands (CC BY 4.0) | 6,121 | Description wording, by frozen rules |
| ShellRisk-Bench training split: SWE-smith and Terminal-Bench commands | 5,834 | Upstream source label (benign) |
| LANCET secrets family (agent-authored reveal-vs-metadata pairs, 20 tools) | 5,328 | Project-authored pairs |
| LANCET's released agent-authored evaluation suites | 4,637 | Their original authored labels |
| SWE-smith, Terminal-Bench and NL2Bash commands (V5's audited inspection pool) | 3,054 | Source-inferred benign |
| Azure CLI reference examples (MIT) | 1,118 | Command verb and description, by rules |
| AWS CLI command shapes from botocore models (Apache-2.0) | 927 | Operation verb; credential-returning operations are risky |
| LANCET red-team corpus and safe look-alikes | 522 | Project author's danger ranking (4–5 risky, 1–2 benign) |
| GitHub CLI (MIT), Docker CLI (Apache-2.0), kubectl (Apache-2.0) examples | 310 | Command verb and description, by rules |
| ShellRisk-Bench training split: Atomic Red Team (MIT) and InternalAllTheThings (no license declared) | 134 | Upstream source label (risky) |

Only commands and original labels were used from the evaluation suites, never any hosted-model outputs stored alongside them. Recorded model scores in the red-team corpus were removed before training. **No language model, hosted API or human labeler produced any training label, teacher target or selection signal.** No output from Jev (TypeSafe) or any other hosted model was used.

Development and calibration came from tools, services and families separate from fitting. The datasets themselves are not distributed.

## Evidence

The development-selected model was scored once on `lancet-bench-1` (793 commands: 409 risky, 384 benign, 37 areas):

| | v0.4.0 | v0.3.0 | v0.2.0 | v0.1.0 | Jev (hosted) |
|---|---:|---:|---:|---:|---:|
| Risky caught (`risky` or `review`) | **89.0%** (364/409) | 85.8% | 73.6% | 65.5% | 96.8% |
| Safe interrupted | 6.2% (24/384) | 5.5% | 6.2% | 5.5% | 7.8% |
| AUROC | **0.974** | 0.962 | 0.896 | 0.860 | 0.982 |
| Risky secrets caught (112) | **72%** | 66% | 24% | 14% | 98% |
| Catch at ≤10% interruption | 92.2% | 93.4% | 79.5% | 73.1% | 97.3% |

**Against v0.3.0** (paired bootstrap by family, 95%): catch rate **+3.2 points [+0.5, +5.9]**; interruption +0.8 points [−1.6, +3.4]. Jev saw a fixed task context; Nano sees only the command.

**ShellRisk-Bench** (upstream labels; no test rows were used in training):

| | Test split: caught (193) | interrupted (4,001) | AUROC | Catch at ≤10% |
|---|---:|---:|---:|---:|
| v0.4.0 | **60.6%** | **2.3%** | **0.952** | **91.2%** |
| v0.3.0 | 46.6% | 6.1% | 0.827 | 59.1% |

On LANCET's separate ShellRisk source-external slice (176 risky, 3,313 safe), v0.4.0 caught 60.2% at 2.5% interrupted (v0.3.0: 48.9% at 6.3%); paired difference +11.4 catch points [+4.1, +18.7] and −3.8 interruption points.

**Neutral third-party set** (rogue-security coding-agent-security-benchmark, 66 Bash commands after overlap screening: 42 risky, 24 safe): v0.4.0 caught 52.4% at 12.5% interrupted, AUROC 0.746 (v0.3.0: 50.0% at 20.8%, 0.701). Catch at ≤10% interruption: 52.4% (v0.3.0: 40.5%).

**Speed.** Median warm CPU time was 13.9 ms per command (p95 19.2 ms), against 13.6 ms for v0.3.0 in the same run. The machine was a Ryzen 9 3900X / Windows 11, with four intra-op threads and batch one. These are observations, not hardware-independent guarantees.

## Intended use and limitations

Nano is a research component for **Bash command-risk review, not an execution authority**. Inputs are inert text. It has no access to filesystem state, fetched script contents or task context.

- PowerShell, invalid or unsupported input, more than 8,192 UTF-8 bytes or more than 512 tokens return `review`. Inputs are never silently truncated.
- **`not_flagged` does not guarantee safety.** Every result carries `experimental: true` and `executionAuthorized: false`. These warnings impose no extra license restriction.

## Release scope

- The model and tokenizer bytes are those produced and scored by the research pipeline.
- The runtime `classify.py` is unchanged from v0.3.0. It reads thresholds and calibration from `model.json`.
- Runtime dependencies (NumPy, tokenizers, ONNX Runtime CPU) are installed separately and not bundled.
- No PyTorch, Transformers, network access or later model download is needed for inference.
