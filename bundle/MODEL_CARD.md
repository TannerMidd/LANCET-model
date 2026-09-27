# LANCET Nano model card

## Identity and license

- **LANCET Nano**, v0.4.1. Internal research ID: `doc-labels-9b / H1`, seed 9601 (the v0.4.0 weights), with a new review threshold.
- Model license: **Apache-2.0**, with an [explicit scope](MODEL-LICENSE.md). Runtime: **MIT**, see the [notice](licenses/pi-jev-guard-MIT.txt).
- Base: Salesforce/codet5p-220m, revision `2b92f36e2782341a50551759fdba0dd15e821f99`. Its [upstream model card](licenses/codet5p-220m-upstream-model-card.md) declares BSD-3-Clause; the [Salesforce notice](licenses/CodeT5-BSD-3-Clause.txt) is retained.
- Architecture: CodeT5+ 220M encoder, masked mean pooling, layer normalization and a binary classifier head. No generative decoder is used at inference.
- Parameters: **109,614,728**. CPU INT8 ONNX, 110,560,709 bytes.
- ONNX SHA-256: `f412c91867f769aa2b7b0bd5625b460efeb2018fcc5bddd4b39f09dfd2dc4f32`.
- Tokenizer: byte-identical to the CodeT5 byte-BPE tokenizer shipped with v0.1.0–v0.3.0 (CodeT5+ uses the same vocabulary and merges).
- Calibration: positive-slope Platt fit on a held calibration role only, with scale `0.8128674983663715` and bias `-0.8842568794525207`.
- Output bands:
  - `risky`: score ≥ `0.8795421382252008` (unchanged from v0.4.0)
  - `review`: score ≥ `0.3032267395410385` (v0.4.0: `0.8188976760554079`)
- Review threshold rule: the lowest threshold at which no realistic area of the held-out calibration data has more than 8% of its safe commands flagged (v0.4.0: 5%). Small agent-authored adversarial areas (secrets, red-team) are reported but do not set it. Chosen on calibration data only, before any benchmark scoring.
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

v0.4.1 was scored once on each benchmark at its shipped thresholds. The **Triage Score** gives each risky command asked about or blocked one point, scales the result down in proportion when more than 10% of safe commands are stopped, and combines the three benchmarks weighted by size (lancet-bench-1 51%, ShellRisk-Bench test 36%, neutral set 13%).

| | v0.4.1 | v0.4.0 |
|---|---:|---:|
| **Triage Score** | **75.3** | 73.2 |
| lancet-bench-1 (409 risky / 384 safe): caught / stopped | **91.7%** (375) / 9.4% (36) | 89.0% (364) / 6.2% (24) |
| ShellRisk-Bench test (193 risky / 4,001 safe): caught / stopped | **70.5%** (136) / 3.1% (126) | 60.6% (117) / 2.3% (92) |
| Neutral set (42 risky / 24 safe): caught / stopped | 59.5% (25) / 25.0% (6) | 57.1% (24) / 12.5% (3) |
| lancet-bench-1 risky secrets caught (112) | **77%** | 72% |
| Risky blocked outright, lancet-bench-1 / ShellRisk | 67.0% / 23.8% | 67.0% / 23.8% |

The model weights are unchanged, so ranking quality is identical to v0.4.0: AUROC 0.974 on lancet-bench-1, 0.952 on the ShellRisk-Bench test split and 0.746 on the neutral set; catch at ≤10% interruption 92.2%, 91.2% and 52.4%.

On LANCET's separate ShellRisk source-external slice (176 risky, 3,313 safe), v0.4.1 catches 71.0% at 3.4% stopped (v0.4.0: 60.2% at 2.5%).

**Comparators on lancet-bench-1** (each at its own shipped setting): Jev (hosted) 96.8% caught / 7.8% stopped, AUROC 0.982, with a fixed task context; Nano sees only the command. Jev's Triage Score is 63.5.

**Speed.** Unchanged from v0.4.0: median warm CPU time 13.9 ms per command (p95 19.2 ms) on a Ryzen 9 3900X / Windows 11, with four intra-op threads and batch one. These are observations, not hardware-independent guarantees.

## Intended use and limitations

Nano is a research component for **Bash command-risk review, not an execution authority**. Inputs are inert text. It has no access to filesystem state, fetched script contents or task context.

- PowerShell, invalid or unsupported input, more than 8,192 UTF-8 bytes or more than 512 tokens return `review`. Inputs are never silently truncated.
- **`not_flagged` does not guarantee safety.** Every result carries `experimental: true` and `executionAuthorized: false`. These warnings impose no extra license restriction.

## Release scope

- The model and tokenizer bytes are those produced and scored by the research pipeline.
- The runtime `classify.py` is unchanged from v0.3.0 and v0.4.0. It reads thresholds and calibration from `model.json`.
- Runtime dependencies (NumPy, tokenizers, ONNX Runtime CPU) are installed separately and not bundled.
- No PyTorch, Transformers, network access or later model download is needed for inference.
