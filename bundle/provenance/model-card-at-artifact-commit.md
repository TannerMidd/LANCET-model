# LANCET — experimental Bash command-risk classifier

## Identity

- Selected artifact: V5 `codet5-balanced`, `recall95` operating profile, INT8 ONNX.
- Base: Salesforce/codet5-small, revision `b1ee9570c289f21b5922b9c768a1ce12957bf968`.
- Architecture: CodeT5 encoder, masked mean pooling, layer normalization, dropout and binary classification head. No generative decoder at inference.
- Parameters: 35,318,017.
- Calibration: positive-slope Platt fit on the calibration partition.
- Decision threshold: `0.576954030455576`.
- INT8 artifact SHA-256: `e8f2e75580a435eba9744b4a8f14dc851f7c71e579c344bde75dee047f7c07a3`.
- Input: Bash command text, no filesystem state or user intent.
- Outputs: `risky`, `not_flagged`, `review` for unsupported/invalid input.

## Training and selection

The selected encoder continued from the V4 CodeT5 checkpoint for 12 epochs; epoch 8 was selected using development results. V5 fitting used 462 project cases, 11,152 authored examples and 3,989 curated inspection negatives with weighted sampling. The balanced profile subsequently adjusted the operating threshold on calibration data without additional weight training. Full definitions, hashes and disclosure remain in [V5 research](docs/research/command-risk-v5/README.md) and the local run manifests.

## Intended scope and limitations

LANCET is a research component for command-risk review. It does not parse all shell behavior, retrieve scripts, inspect the filesystem, classify file edits, or authorize execution. PowerShell is unsupported. Oversized input is rejected for review instead of truncated. Scores are model outputs rather than guarantees of safety.

Repeated benchmark inspection and related command variants limit generalization claims. The combined 952-case result includes training/development/calibration overlap and shared local rules. Read the [expanded evaluation](docs/research/command-risk-eval150/README.md), including its new-case subset, alongside the [combined regression report](docs/research/command-risk-combined/README.md).

## Local deployment

Runtime: NumPy, tokenizers and ONNX Runtime CPU. Four intra-op / one inter-op threads, one command at a time. No PyTorch, Transformers, remote inference or model download is needed to run the selected INT8 artifact. `model/export.json` verifies model, tokenizer and metadata hashes on load. The deployment bundle omits FP32 ONNX despite retaining its historical export hash; the local research checkpoint directory contains that export.

Observed footprint: about 38 MB weights plus tokenizer; about 115 MB resident Python process after warmup, 151 MB observed peak. Mean warm time was 3.1 ms on the 278-command evaluation workload using Ryzen 9 3900X / Windows 11. Longer supported commands can take substantially longer; these measurements are not minimum system requirements.

## Provenance

Extraction preserves original bytes, calibration and thresholds. `EXTRACTION.json` records the source Git HEAD plus file hashes because the research was uncommitted in the source checkout. Its paths are evidence of origin, not runtime dependencies. See [LICENSE.md](LICENSE.md) for the separate treatment of source code, pretrained assets and mixed-source training data.

