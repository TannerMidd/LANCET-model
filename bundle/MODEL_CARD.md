# LANCET Nano model card

## Identity and license

- **LANCET Nano**, v0.4.3. Internal research ID: `lancet-round-19 / A-19103`, seed 19103, epoch 7.
- Model license: **Apache-2.0**, with an [explicit scope](MODEL-LICENSE.md). Runtime: **MIT**, see the [notice](licenses/pi-jev-guard-MIT.txt).
- Base: Salesforce/codet5p-220m, revision `2b92f36e2782341a50551759fdba0dd15e821f99`. Its [upstream model card](licenses/codet5p-220m-upstream-model-card.md) declares BSD-3-Clause; the [Salesforce notice](licenses/CodeT5-BSD-3-Clause.txt) is retained.
- Architecture: CodeT5+ 220M encoder over overlapping 512-token windows (64-token overlap); mean and maximum pooling of every token exactly once across windows; a learned projection, layer normalization and a risk head. No generative decoder is used at inference.
- Parameters: **110,789,762**. CPU INT8 ONNX encoder, 110,550,587 bytes; the 4.7 MB head runs in NumPy.
- ONNX SHA-256: `4e7d6a53d27a7321a2638a4bf446301e8e343c51000963331469e3ab20aae2a4`.
- Tokenizer: the CodeT5 byte-BPE vocabulary and merges (`vocab.json`, `merges.txt`), the same tokenization as v0.1.0–v0.4.2.
- Shells: **Bash, PowerShell and cmd.**
- Calibration: positive-slope Platt fit on a held calibration role only, with scale `0.501046180687904` and bias `0.8579191016201142`. Bands use the risk logit; the calibrated score is reported alongside.
- Output bands:
  - `risky`: risk logit ≥ `7.71649796562147` (score ≥ `0.9912`)
  - `review`: risk logit ≥ `-3.4448594882714976` (score ≥ `0.2956`)
  - `not_flagged`: below the review threshold
- Threshold rule: the review threshold maximizes the Triage formula (risky commands caught × min(1, 10% / safe commands stopped)) on held-out development calibration data from three populations (in-house, operational and agent-style commands), counting each command family once. The risky threshold keeps each population at most 1% of safe commands blocked. Chosen on calibration data only.

## Fitting lineage

Pinned upstream CodeT5+ 220M → fine-tuning (this release). **No earlier LANCET checkpoint was used as an initializer or teacher.**

Training used domain-weighted, label-balanced sampling across fitting areas and a pair-margin loss on authored risky/safe twins, for 10 epochs (81,920 sampled units, 16 per step) with linear warm-up and cosine decay of the learning rate to zero. The exported weights are the epoch-7 checkpoint of the seed with the best development score among four.

Training used 55,827 labelled rows plus 11,384 down-weighted documentation and inspection rows:

| Source | Rows | Label basis |
|---|---:|---|
| LANCET command-semantics curriculum (Bash, PowerShell, cmd; risky/safe twins, long scripts) | 21,544 | Project-authored |
| LANCET project-authored contrast recipes | 9,184 | Project-authored risky/benign pairs |
| LANCET secrets family (reveal-vs-metadata pairs) | 7,728 | Project-authored pairs |
| ShellRisk-Bench training split: SWE-smith and Terminal-Bench commands | 5,818 | Upstream source label (benign) |
| LANCET's released agent-authored evaluation suites | 5,047 | Their original authored labels |
| Shell Safety v2 training split (MIT) | 2,475 | Dataset author's `allow` / `deny` labels |
| LANCET semantic contrast sets (agent-style, `exec`-style and shell-escape commands with safe look-alikes) | 1,878 | Project-authored pairs |
| LANCET retired benchmark lancet-bench-1 | 788 | Original authored labels |
| LANCET shell-escape atlas | 638 | Project-authored pairs |
| LANCET earlier draft benchmark (never scored) | 512 | Original authored labels |
| ShellRisk-Bench training split: Atomic Red Team (MIT) and InternalAllTheThings (no license declared) | 133 | Upstream source label (risky) |
| LANCET agent-workflow commands | 82 | Project-authored labels |
| tldr-pages example commands (CC BY 4.0), down-weighted | 6,093 | Description wording, by frozen rules |
| SWE-smith, Terminal-Bench and NL2Bash commands (V5's audited inspection pool), down-weighted | 2,956 | Source-inferred benign |
| Azure CLI reference examples (MIT), down-weighted | 1,118 | Command verb and description, by rules |
| AWS CLI command shapes from botocore models (Apache-2.0), down-weighted | 917 | Operation verb; credential-returning operations are risky |
| GitHub CLI (MIT), Docker CLI (Apache-2.0), kubectl (Apache-2.0) examples, down-weighted | 300 | Command verb and description, by rules |

Only commands and original labels were used from the evaluation suites, never any hosted-model outputs stored alongside them. **No language model, hosted API or human labeler produced any training label, teacher target or selection signal.** No output from Jev (TypeSafe) or any other hosted model was used.

Development, calibration and confirmation (36,931 rows) came from tools, services and families separate from fitting. The datasets themselves are not distributed.

## Evidence

v0.4.3 was scored once on each benchmark at its shipped thresholds. None of the three was used for training, development, selection or calibration.

The **Triage Score** gives each risky command asked about or blocked one point, scales the result down in proportion when more than 10% of safe commands are stopped, and combines the three benchmarks weighted by size (lancet-bench-2-next 58%, ShellRisk-Bench test 20%, neutral set 21%).

| | v0.4.3 | v0.4.2 |
|---|---:|---:|
| **Triage Score** | **68.3** | 54.4 |
| lancet-bench-2-next (1,602 risky / 1,602 safe): caught / stopped | 78.0% / **12.4%** | 78.0% / 20.0% |
| ShellRisk-Bench test (193 risky / 4,001 safe): caught / stopped | **64.8%** / 3.0% | 60.1% / **2.7%** |
| Neutral set (212 risky / 301 safe): caught / stopped | 85.8% / **5.6%** | **91.0%** / 7.0% |
| Risky blocked outright, lancet-bench-2-next / ShellRisk | 50.0% / 36.3% | 17.7% / 6.2% |

Ranking quality (AUROC) is 0.869 on lancet-bench-2-next, 0.951 on the ShellRisk-Bench test split and 0.961 on the neutral set; catch at ≤10% interruption 76.0%, 83.9% and 92.0%.

**lancet-bench-2-next** has 3,204 commands built as 1,602 risky/safe twins from 289 scenarios in 40 areas, each also repeated inside a subshell, function, command substitution, nested shell, pipeline and background job; 3,066 are Bash, 102 PowerShell and 36 cmd. It replaced lancet-bench-1 (793 Bash commands), on which the strongest guards were near the ceiling. Triage Scores on the two benchmarks are not comparable: v0.4.2 scored 82.7 on the previous one and 54.4 on this one with the same weights. lancet-bench-1 was retired and used as training data for v0.4.3, so it is no longer reported.

The neutral set is 66 commands from the Rogue Security coding-agent benchmark plus 447 from the Shell Safety v2 test split; v0.4.3's training used the Shell Safety v2 training split, never its test split.

**Comparators** (each at its own shipped setting): Jev (hosted) Triage Score 38.9; on lancet-bench-2-next it catches 95.1% and stops 21.8%, with a fixed task context. Nano sees only the command. Earlier releases and other guards are compared in the [full table](https://github.com/TannerMidd/LANCET-model#triage-score-across-three-benchmarks).

**Speed.** The same as v0.4.2 when measured side by side (median within 1%): about 14 ms per command on a Ryzen 9 3900X / Windows 11, with four intra-op threads and batch one. Commands longer than one window take one encoder pass per window. These are observations, not hardware-independent guarantees.

## Intended use and limitations

Nano is a research component for **command-risk review, not an execution authority**. Inputs are inert text. It has no access to filesystem state, fetched script contents or task context.

- Other shells, invalid or unsupported input, or more than 8,192 UTF-8 bytes return `review`. Inputs are never silently truncated.
- PowerShell and cmd coverage is newer and smaller than Bash coverage (102 and 36 benchmark commands).
- **`not_flagged` does not guarantee safety.** Every result carries `experimental: true` and `executionAuthorized: false`. These warnings impose no extra license restriction.

## Release scope

- The model, head and tokenizer bytes are those produced and scored by the research pipeline.
- The runtime `classify.py` is new in v0.4.3 for the windowed format. It reads thresholds and calibration from `model.json` and checks every model file's hash before loading.
- Runtime dependencies (NumPy, tokenizers, ONNX Runtime CPU) are installed separately and not bundled.
- No PyTorch, Transformers, network access or later model download is needed for inference.
