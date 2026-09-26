# Modifications to upstream models

**LANCET Nano v0.3.0 is a modified downstream model. It is not the unmodified Salesforce CodeT5-base model.**

- **`model/model-int8.onnx`:**
  - Architecture: the CodeT5-base encoder with masked mean pooling, layer normalization and a binary command-risk head, in place of the original encoder-decoder generation pipeline.
  - Starting point: the pinned upstream CodeT5-base weights. No earlier LANCET checkpoint was used.
  - Training data: fine-tuned with class-balanced sampling on project-authored pairs, a project-authored secrets family, LANCET's retired agent-authored evaluation suites, V5's inspection examples, and documentation-labelled commands from tldr-pages, botocore, the Azure CLI, GitHub CLI, kubectl and Docker CLI.
  - Training method: a training-only risk-type head was used and is not exported. Epoch 7 was selected on development data.
  - Export: the graph was exported to ONNX and dynamically quantized with unsigned 8-bit per-channel MatMul/Gather operations.
- **`model/tokenizer.json`:** the CodeT5 byte-BPE tokenizer, byte-identical to the v0.1.0 and v0.2.0 tokenizer file.
- **`model/model.json`:** v0.3.0-specific calibration (a positive-slope Platt fit on calibration data only), review/risky thresholds, input contracts, lineage and hashes.
- **`model/export.json`:** integrity metadata. The FP32 graph is not shipped.
- **`classify.py`, `model/classify.py`:** the MIT LANCET runtime, unchanged from v0.2.0.

The model's license is [Apache-2.0](MODEL-LICENSE.md). The runtime code remains [MIT](LICENSE.md). Training data is not included or relicensed. These notices claim neither independent validation nor upstream endorsement.
