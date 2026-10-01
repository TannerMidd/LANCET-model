# Modifications to upstream models

**LANCET Nano v0.4.3 is a modified downstream model. It is not the unmodified Salesforce CodeT5+ 220M model.**

- **`model/encoder-int8.onnx`:**
  - Architecture: the CodeT5+ 220M encoder only, in place of the original encoder-decoder generation pipeline. The decoder is not used.
  - Starting point: the pinned upstream CodeT5+ 220M weights. No earlier LANCET checkpoint was used.
  - Training data: fine-tuned with domain-weighted sampling on project-authored contrast pairs (including a new command-semantics curriculum for Bash, PowerShell and cmd), a project-authored secrets family, LANCET's released agent-authored evaluation suites, ShellRisk-Bench training-split rows, the Shell Safety v2 training split, and documentation-labelled commands from tldr-pages, botocore, the Azure CLI, GitHub CLI, kubectl and Docker CLI.
  - Training method: 10 epochs with cosine learning-rate decay to zero; the exported weights are the epoch-7 checkpoint of seed 19103, chosen on held-out development groups.
  - Export: the encoder was exported to ONNX and dynamically quantized with unsigned 8-bit per-channel MatMul/Gather operations.
- **`model/head.npz`:** the trained pooling projection, layer normalization and risk/ask heads, applied in NumPy after the encoder. Long commands are split into overlapping 512-token windows and every token is pooled exactly once (mean and maximum).
- **`model/vocab.json`, `model/merges.txt`:** the CodeT5 byte-BPE tokenizer vocabulary and merges, the same tokenization as the v0.1.0-v0.4.2 tokenizer file.
- **`model/model.json`:** the calibration (a positive-slope Platt fit on calibration data only), review and risky thresholds, input contracts, lineage and hashes.
- **`model/export.json`:** integrity metadata. The FP32 graph is not shipped.
- **`classify.py`, `model/classify.py`:** the MIT LANCET runtime, updated for the windowed format and for PowerShell and cmd input.

The model's license is [Apache-2.0](MODEL-LICENSE.md), with the upstream [BSD-3-Clause notice](licenses/CodeT5-BSD-3-Clause.txt) retained. The runtime code remains [MIT](LICENSE.md). Training data is not included or relicensed. No upstream endorsement is claimed.
