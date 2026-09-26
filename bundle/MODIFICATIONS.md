# Modifications to upstream models

**LANCET Nano is a modified downstream model. It is neither unmodified Salesforce CodeT5-small nor LANCET V5.**

- **`model/model-int8.onnx`:**
  - Architecture: the CodeT5-small encoder with masked mean pooling, layer normalization and a binary command-risk head, in place of the original encoder-decoder generation pipeline.
  - Starting point: LANCET V5 weights, previously released as v0.1.0. From there, Nano was fine-tuned with class-balanced sampling on project-authored pairs, V5's inspection examples, and documentation-labelled commands from tldr-pages and botocore.
  - Training: a training-only risk-type head was used and is not exported. Epoch 4 was selected on development data, and the two best epochs were averaged.
  - Export: the graph was exported to ONNX and dynamically quantized with unsigned 8-bit per-channel MatMul/Gather operations.
- **`model/tokenizer.json`:** the CodeT5-based byte-BPE tokenizer, byte-identical to V5's.
- **`model/model.json`:** Nano-specific calibration (a positive-slope Platt fit on calibration data only), review/risky thresholds, input contracts, lineage and hashes.
- **`model/export.json`:** integrity metadata. The FP32 graph is not shipped.
- **`classify.py`, `model/classify.py`:** the MIT LANCET runtime, updated for Nano's three output bands (`risky`, `review`, `not_flagged`). Its encoding and scoring match the research runtime used for evaluation.

The model's license is [Apache-2.0](MODEL-LICENSE.md). The runtime code remains [MIT](LICENSE.md). Training data is not included or relicensed. These notices claim neither independent validation nor upstream endorsement.
