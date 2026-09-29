# LANCET Nano v0.4.2 (experimental, CPU INT8)

A local Bash command-risk classifier with 109.6M parameters (a CodeT5+ encoder). It classifies each command as `risky`, `review` or `not_flagged` on a CPU in about 14 ms, with no network access.

**Model: Apache-2.0. Runtime: MIT.** Use, modification and redistribution, including commercial use, are permitted under the respective licenses. See [MODEL-LICENSE.md](MODEL-LICENSE.md), [LICENSE.md](LICENSE.md), [NOTICE.txt](NOTICE.txt) and [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md). Datasets are not included or relicensed.

## What changed from v0.4.1

- **A newly trained model.** v0.4.2 is fine-tuned again from the pinned upstream CodeT5+ 220M base, on a larger and more balanced mix (43,418 rows). New in the mix: the Shell Safety v2 training split (MIT) and project-authored contrast sets of agent-style, `exec`-style and shell-escape commands with safe look-alikes.
- **Far fewer interruptions on everyday commands.** On the 513-command neutral set, v0.4.2 stops 7.0% of safe commands (v0.4.1: 16.9%) while catching 91.0% of risky ones (v0.4.1: 66.5%).
- **More asking, less outright blocking.** v0.4.2 answers `review` for more of the risky commands it catches and `risky` for fewer.
- **Results** (Triage Score: risky commands asked about or blocked earn a point; scaled down when more than 10% of safe commands are stopped; three benchmarks weighted by size):

| At the shipped thresholds | v0.4.2 | v0.4.1 |
|---|---:|---:|
| **Triage Score** | **82.7** | 69.7 |
| lancet-bench-1: risky caught / safe stopped | **92.4%** / 9.9% | 91.7% / 9.4% |
| ShellRisk-Bench test: risky caught / safe stopped | 60.1% / **2.7%** | **70.5%** / 3.1% |
| Neutral set (513 commands): risky caught / safe stopped | **91.0%** / **7.0%** | 66.5% / 16.9% |
| Risky commands blocked outright (lancet-bench-1) | 32.5% | 67.0% |

## Verify before use

Check the downloaded ZIP against `SHA256SUMS.txt`, extract it, and run:

```text
python verify_bundle.py --strict
```

This checks every packaged file against the release manifest. It does not load the model or execute any input. Checksums confirm consistency with the downloaded manifest; they are not a digital signature.

## Run locally

With Python 3.12 on Windows / PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:OPENBLAS_NUM_THREADS = '1'
'{"command": "kubectl delete namespace prod", "shell": "bash"}' | .\.venv\Scripts\python.exe classify.py --model model
```

On macOS or Linux, use `.venv/bin/python` and set `OPENBLAS_NUM_THREADS=1`. Those platforms were not benchmarked.

- **Input:** one JSON object per line on stdin, with a `command` string and `shell` set to `bash`.
- **Speed:** keep the process running to reuse the loaded model.
- **Safety of input:** commands are classified as inert text and are **never executed**.

Each output line includes:
- `classification`: `risky`, `review` or `not_flagged`
- `score`: the calibrated score
- both thresholds
- `experimental: true` and `executionAuthorized: false`

**`not_flagged` is not execution authorization or a safety guarantee.** Other shells, invalid input, more than 8,192 UTF-8 bytes or more than 512 tokens return `review`. Inputs are never silently truncated.

## Evidence

| lancet-bench-1 (793 commands) | v0.4.2 | v0.4.1 | v0.4.0 | v0.3.0 | v0.2.0 | Jev (hosted) |
|---|---:|---:|---:|---:|---:|---:|
| Risky caught | **92.4%** | 91.7% | 89.0% | 85.8% | 73.6% | 96.8% |
| Safe interrupted | 9.9% | 9.4% | 6.2% | 5.5% | 6.2% | 7.8% |
| Risky secrets caught | **78%** | 77% | 72% | 66% | 24% | 98% |
| AUROC | 0.963 | **0.974** | **0.974** | 0.962 | 0.896 | 0.982 |

- **Triage Score across all three benchmarks:** v0.4.2 82.7, v0.4.1 69.7, Jev (hosted) 58.6.
- **Speed:** same architecture and size as v0.4.0 and v0.4.1: median warm time about 14 ms per command on a Ryzen 9 3900X / Windows 11 with four ONNX Runtime threads.
- **Labels:** no language-model output was used as a label, teacher target or selection signal.

Details are in [MODEL_CARD.md](MODEL_CARD.md).

## Contents

- `model/`: INT8 ONNX model, tokenizer, `model.json` (calibration and thresholds), `export.json` (hashes), runtime.
- `MODEL_CARD.md`, licenses and notices, and `licenses/`.
- `provenance/`: the aggregate training receipt and the V5 inspection-pool lineage audit. These contain no commands or datasets.
- `RELEASE-MANIFEST.json`: per-file hashes.
