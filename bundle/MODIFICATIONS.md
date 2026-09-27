# Modifications to upstream models

**LANCET Nano v0.4.0 is a modified downstream model. It is not the unmodified Salesforce CodeT5+ 220M model.**

- **`model/model-int8.onnx`:**
  - Architecture: the CodeT5+ 220M encoder with masked mean pooling, layer normalization and a binary command-risk head, in place of the original encoder-decoder generation pipeline. The decoder is not used.
  - Starting point: the pinned upstream CodeT5+ 220M weights (stored in FP16 upstream; promoted to FP32 before fine-tuning). No earlier LANCET checkpoint was used.
  - Training data: fine-tuned with domain-weighted sampling on project-authored pairs, a project-authored secrets family, LANCET's released agent-authored evaluation suites, a project red-team corpus, V5's inspection examples, ShellRisk-Bench training-split rows, and documentation-labelled commands from tldr-pages, botocore, the Azure CLI, GitHub CLI, kubectl and Docker CLI.
  - Training method: a training-only risk-type head was used and is not exported. The weights are the average of the three best development epochs (3, 6 and 8).
  - Export: the graph was exported to ONNX and dynamically quantized with unsigned 8-bit per-channel MatMul/Gather operations.
- **`model/tokenizer.json`:** the CodeT5 byte-BPE tokenizer, byte-identical to the v0.1.0–v0.3.0 tokenizer file.
- **`model/model.json`:** v0.4.0-specific calibration (a positive-slope Platt fit on calibration data only), review/risky thresholds, input contracts, lineage and hashes.
- **`model/export.json`:** integrity metadata. The FP32 graph is not shipped.
- **`classify.py`, `model/classify.py`:** the MIT LANCET runtime, unchanged from v0.3.0.

The model's license is [Apache-2.0](MODEL-LICENSE.md), with the upstream [BSD-3-Clause notice](licenses/CodeT5-BSD-3-Clause.txt) retained. The runtime code remains [MIT](LICENSE.md). Training data is not included or relicensed. No upstream endorsement is claimed.
