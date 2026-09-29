# LANCET Nano model card

## Identity and license

- **LANCET Nano**, v0.4.2. Internal research ID: `doc-labels-15e / R2`, seed 15603.
- Model license: **Apache-2.0**, with an [explicit scope](MODEL-LICENSE.md). Runtime: **MIT**, see the [notice](licenses/pi-jev-guard-MIT.txt).
- Base: Salesforce/codet5p-220m, revision `2b92f36e2782341a50551759fdba0dd15e821f99`. Its [upstream model card](licenses/codet5p-220m-upstream-model-card.md) declares BSD-3-Clause; the [Salesforce notice](licenses/CodeT5-BSD-3-Clause.txt) is retained.
- Architecture: CodeT5+ 220M encoder, masked mean pooling, layer normalization and a binary classifier head. No generative decoder is used at inference.
- Parameters: **109,614,728**. CPU INT8 ONNX, 110,560,681 bytes.
- ONNX SHA-256: `1b6249c369ad390682d034fb9ee872dcecaa0c3418eb89218b6fa6111594a547`.
- Tokenizer: byte-identical to the CodeT5 byte-BPE tokenizer shipped with v0.1.0–v0.4.1 (CodeT5+ uses the same vocabulary and merges).
- Calibration: positive-slope Platt fit on a held calibration role only, with scale `0.664356045455189` and bias `0.6933066505190515`.
- Output bands:
  - `risky`: score ≥ `0.9600226519174887`
  - `review`: score ≥ `0.5272825855548885`
  - `not_flagged`: below the review threshold
- Threshold rule: the lowest thresholds at which each of three held-out development populations (in-house, operational and agent-style commands) has at most 8% of its safe commands asked about and at most 1% blocked, counted both by rows and by command families. Small adversarial stress areas (secrets, red-team) are reported but do not set them. Chosen on calibration data only, before any benchmark scoring.

## Fitting lineage

Pinned upstream CodeT5+ 220M → fine-tuning (this release). **No earlier LANCET checkpoint was used as an initializer or teacher.**

Training used domain-weighted, label-balanced sampling across fitting areas, a training-only risk-type head that is not exported, and a pair-margin loss on authored pairs. The exported weights are the average of the three best epochs (11, 12 and 14), chosen on held-out development groups.

Training used 43,418 rows:

| Source | Rows | Label basis |
|---|---:|---|
| LANCET project-authored contrast recipes | 9,184 | Project-authored risky/benign pairs |
| tldr-pages example commands (CC BY 4.0) | 6,093 | Description wording, by frozen rules |
| ShellRisk-Bench training split: SWE-smith and Terminal-Bench commands | 5,818 | Upstream source label (benign) |
| LANCET secrets family (agent-authored reveal-vs-metadata pairs, 20 tools) | 5,328 | Project-authored pairs |
| LANCET's released agent-authored evaluation suites | 4,459 | Their original authored labels |
| LANCET semantic contrast sets (agent-style, `exec`-style and shell-escape commands with safe look-alikes) | 3,354 | Project-authored pairs |
| SWE-smith, Terminal-Bench and NL2Bash commands (V5's audited inspection pool) | 2,956 | Source-inferred benign |
| Shell Safety v2 training split (MIT) | 2,475 | Dataset author's `allow` / `deny` labels |
| LANCET red-team corpus and safe look-alikes | 1,149 | Project author's danger ranking (4–5 risky, 1–2 benign) |
| Azure CLI reference examples (MIT) | 1,118 | Command verb and description, by rules |
| AWS CLI command shapes from botocore models (Apache-2.0) | 917 | Operation verb; credential-returning operations are risky |
| GitHub CLI (MIT), Docker CLI (Apache-2.0), kubectl (Apache-2.0) examples | 300 | Command verb and description, by rules |
| LANCET agent-workflow commands | 134 | Project-authored labels |
| ShellRisk-Bench training split: Atomic Red Team (MIT) and InternalAllTheThings (no license declared) | 133 | Upstream source label (risky) |

Only commands and original labels were used from the evaluation suites, never any hosted-model outputs stored alongside them. Recorded model scores in the red-team corpus were removed before training. **No language model, hosted API or human labeler produced any training label, teacher target or selection signal.** No output from Jev (TypeSafe) or any other hosted model was used.

Development and calibration (30,370 rows) came from tools, services and families separate from fitting. The datasets themselves are not distributed.

## Evidence

v0.4.2 was scored once on each benchmark at its shipped thresholds. The **Triage Score** gives each risky command asked about or blocked one point, scales the result down in proportion when more than 10% of safe commands are stopped, and combines the three benchmarks weighted by size (lancet-bench-1 41%, ShellRisk-Bench test 29%, neutral set 30%).

| | v0.4.2 | v0.4.1 |
|---|---:|---:|
| **Triage Score** | **82.7** | 69.7 |
| lancet-bench-1 (409 risky / 384 safe): caught / stopped | **92.4%** (378) / 9.9% (38) | 91.7% (375) / 9.4% (36) |
| ShellRisk-Bench test (193 risky / 4,001 safe): caught / stopped | 60.1% (116) / **2.7%** (109) | **70.5%** (136) / 3.1% (126) |
| Neutral set (212 risky / 301 safe): caught / stopped | **91.0%** (193) / **7.0%** (21) | 66.5% (141) / 16.9% (51) |
| lancet-bench-1 risky secrets caught (112) | **78%** | 77% |
| Risky blocked outright, lancet-bench-1 / ShellRisk | 32.5% / 6.2% | 67.0% / 23.8% |

Ranking quality (AUROC) is 0.963 on lancet-bench-1, 0.897 on the ShellRisk-Bench test split and 0.953 on the neutral set; catch at ≤10% interruption 92.4%, 82.9% and 91.0%.

The neutral set is 66 commands from the Rogue Security coding-agent benchmark plus 447 from the Shell Safety v2 test split; v0.4.2's training used the Shell Safety v2 training split, never its test split.

**Comparators** (each at its own shipped setting): Jev (hosted) Triage Score 58.6; on lancet-bench-1 it catches 96.8% and stops 7.8%, AUROC 0.982, with a fixed task context. Nano sees only the command.

**Speed.** Same architecture and size as v0.4.0 and v0.4.1: median warm CPU time about 14 ms per command on a Ryzen 9 3900X / Windows 11, with four intra-op threads and batch one. These are observations, not hardware-independent guarantees.

## Intended use and limitations

Nano is a research component for **Bash command-risk review, not an execution authority**. Inputs are inert text. It has no access to filesystem state, fetched script contents or task context.

- PowerShell, invalid or unsupported input, more than 8,192 UTF-8 bytes or more than 512 tokens return `review`. Inputs are never silently truncated.
- **`not_flagged` does not guarantee safety.** Every result carries `experimental: true` and `executionAuthorized: false`. These warnings impose no extra license restriction.

## Release scope

- The model and tokenizer bytes are those produced and scored by the research pipeline.
- The runtime `classify.py` is unchanged from v0.3.0–v0.4.1. It reads thresholds and calibration from `model.json`.
- Runtime dependencies (NumPy, tokenizers, ONNX Runtime CPU) are installed separately and not bundled.
- No PyTorch, Transformers, network access or later model download is needed for inference.
