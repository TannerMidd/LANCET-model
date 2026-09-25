# Modifications to the upstream model

**LANCET V5 is a modified downstream model, not unmodified Salesforce CodeT5-small.**

- `model/model-int8.onnx`: CodeT5-small encoder with masked mean pooling, layer normalization, dropout and a binary command-risk head instead of the original encoder-decoder generation pipeline. V4 selected epoch 13; V5 continued the V4 weights and selected epoch 8 of 12. The graph was exported to ONNX and dynamically quantized using unsigned 8-bit MatMul/Gather operations.
- `model/tokenizer.json`: the CodeT5-based byte-BPE tokenizer serialized for LANCET's portable tokenizers runtime.
- `model/model.json`: LANCET-specific fitting lineage, positive-slope Platt calibration, input contracts, operating profile and hashes. The `recall95` threshold is `0.576954030455576`; that profile changed the threshold without additional fitting.
- `model/export.json` and `model/checksums.json`: downstream export/integrity metadata. The historical FP32 export hash remains recorded, but that graph is not shipped in the CPU INT8 archive.
- `classify.py` and `model/classify.py`: the original MIT-licensed LANCET runtime. The retained class name `PortableV4` does not mean that this selected artifact is a V4 model.

**Release preparation makes no further changes to these frozen files, model decisions, calibration or thresholds.** It adds an explicit model license, attribution, source-specific license evidence, documentation, packaging and a file-hash verifier. Historical model/extraction documents remain byte-for-byte preserved and are clearly identified as historical.

The model's current license is [Apache-2.0](MODEL-LICENSE.md); runtime code remains [MIT](LICENSE.md). Training data is not included or relicensed. These notices do not claim independent validation or upstream endorsement.
