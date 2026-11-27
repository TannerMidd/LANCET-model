# Modifications to upstream models

**LANCET Nano v0.5.0 is a modified downstream model. It is not the unmodified Salesforce CodeT5+ 220M model.**

- **`model/encoder-int8.onnx`:**
  - Architecture: the CodeT5+ 220M encoder only, in place of the original encoder-decoder generation pipeline. The decoder is not used.
  - Lineage: pinned upstream `Salesforce/codet5p-220m` → Round 25 Preview → Round 60 (`wise-avg12-065`) → Round 61 (`wise-ep1-065`).
  - Training data: `97,662` protected-clean rows (`36,674` contrast pairs) covering project-authored command-semantics and domain contrasts, `27,920` multi-shell wrapper-invariance pairs across 15 Bash/PowerShell/`cmd` wrappers, non-GPL `ShellRisk-Bench` rows (train+test, excluding `gtfobins`/`nl2bash`), and `Shell Safety v2` train rows.
  - Training method: native raw-BCE scaling with bounded ReLU margins (`safe <= 3.0`, `risky >= 8.0`), selective parent logit-preservation anchoring, unwrapped-to-wrapped consistency loss, and WiSE-FT weight-space interpolation (`0.65 * epoch-01 + 0.35 * Round 60`) selected on 6-stratum held-out dev.
  - Export: exported to ONNX and dynamically quantized with unsigned 8-bit per-channel MatMul/Gather operations (native vs. FP32 parity max diff `3.55e-06`).
- **`model/head.npz` (and browser copies `model/head.json`, `model/head.bin`):** trained pooling projection, layer normalization and risk/ask heads applied in float64 NumPy after the encoder. Long commands are prefixed with `<shell={shell}>\n`, split into overlapping 512-token windows, and every token is pooled exactly once (mean and maximum).
- **`model/vocab.json`, `model/merges.txt`:** CodeT5 byte-BPE tokenizer vocabulary and merges.
- **`model/model.json`:** display calibration, INT8 dev-matched review and risky thresholds, `semantic-windowed-3` input contract, lineage and hashes.
- **`model/export.json`:** integrity metadata. The FP32 graph is not shipped.
- **`classify.py`, `model/classify.py`:** the MIT LANCET runtime updated for `semantic-windowed-3` shell-tagged windowed inference across Bash, PowerShell, and `cmd`.

The model's license is [Apache-2.0](MODEL-LICENSE.md), with the upstream [BSD-3-Clause notice](licenses/CodeT5-BSD-3-Clause.txt) retained. The runtime code remains [MIT](LICENSE.md). Training data is not included or relicensed. No upstream endorsement is claimed.
