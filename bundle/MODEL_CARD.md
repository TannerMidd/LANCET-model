# LANCET V5 model card

## Identity and license

- Artifact: `codet5-balanced`, `recall95` operating profile, CPU INT8 ONNX.
- Model license: **Apache-2.0**, [explicit scope](MODEL-LICENSE.md). Runtime: **MIT**, [notice](licenses/pi-jev-guard-MIT.txt).
- Base: Salesforce/codet5-small, revision `b1ee9570c289f21b5922b9c768a1ce12957bf968`.
- Architecture: CodeT5 encoder, masked mean pooling, layer normalization, dropout and binary classifier head; no generative decoder at inference.
- Parameters: **35,318,017**.
- Calibration: positive-slope Platt fit on the calibration partition.
- Threshold: `0.576954030455576`.
- ONNX SHA-256: `e8f2e75580a435eba9744b4a8f14dc851f7c71e579c344bde75dee047f7c07a3`.

## Fitting lineage and selection

Pinned upstream CodeT5-small → V4 epoch 13 → V5 rehearsal epoch 8 of 12 → balanced threshold profile without further fitting. V4 did not inherit older mixed-source fine-tuned models. V5 used weighted sampling from 462 project cases, 11,152 authored examples and 3,989 curated inspection negatives. Epoch selection used development results; the later balanced operating profile changed the threshold on calibration data after prior benchmark inspection.

The 3,989 source inspection training rows comprise 2,806 SWE-smith, 984 Terminal-Bench and 199 NL2Bash examples. Their pinned dataset declarations are MIT/Apache-2.0; see [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md). All 5,213 inspection train/development/calibration rows were locally mapped to the original pinned training Parquet. These are eligible pool counts, not counts of unique optimizer-sampled examples. The aggregate receipt is [provenance/v5-lineage-audit.json](provenance/v5-lineage-audit.json).

The source labels and inspection curation are heuristic/source-derived, not independently adjudicated. The audit does not certify every dataset publisher's rights to underlying snippets or all CodeT5 pretraining provenance. Raw training data is not distributed or relicensed.

## Intended use and limitations

A research component for **Bash command-risk review**, not an execution authority. Inputs are inert text. No filesystem state, fetched script contents, file-edit analysis or user/task context is available. PowerShell, invalid/unsupported input, more than 8,192 UTF-8 bytes or more than 512 tokens require review; no silent truncation.

Outputs are `risky`, `not_flagged` and `review`, with `experimental: true` and `executionAuthorized: false`. `not_flagged` does not guarantee safety. These warnings describe intended use/evidence and impose no extra license restriction.

Repeated benchmark inspection, fitting overlap and related variants limit generalization claims. The V5 combined 952-case regression figure includes training/development/calibration overlap and shared local rules; it is not independent accuracy. Classifier-only eval150 recorded **138/150** required interventions caught and **14/128** controls interrupted. Removing local rules does not remove V5's historical benchmark exposure.

Historical mean warm latency was **3.1 ms** on Ryzen 9 3900X / Windows 11 for the 278-command workload; resident Python RAM was about **115 MB** after warmup, with **151 MB** observed peak. Measurements used CPU ONNX Runtime, four intra-op/one inter-op threads, batch one and `OPENBLAS_NUM_THREADS=1`. Startup is excluded; longer inputs can be substantially slower. Other platforms were not benchmarked here.

## Release scope

No model, runtime, tokenizer, calibration or threshold bytes changed during release preparation. Only licensing, notices, documentation, packaging and a hash verifier were added. No new fitting or protected scoring occurred. The original model card is retained as [historical source evidence](provenance/model-card-at-artifact-commit.md); its repository-relative research links describe the original repository, not additional packaged files.

Runtime dependencies are NumPy, Hugging Face tokenizers and ONNX Runtime CPU; they are installed separately, not bundled. Inference requires no PyTorch, Transformers, remote inference or subsequent model download. The portable runtime's original class name `PortableV4` is retained; this selected artifact is V5.

V6 and ongoing method research are not released or promoted in this package. Independent acceptance and human label adjudication remain **unavailable and unmet**.

**Development and programmatic evidence; not independently validated.**
