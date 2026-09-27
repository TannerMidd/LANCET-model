# LANCET Nano v0.4.1 (experimental, CPU INT8)

A local Bash command-risk classifier with 109.6M parameters (a CodeT5+ encoder). It classifies each command as `risky`, `review` or `not_flagged` on a CPU in about 14 ms, with no network access.

**Model: Apache-2.0. Runtime: MIT.** Use, modification and redistribution, including commercial use, are permitted under the respective licenses. See [MODEL-LICENSE.md](MODEL-LICENSE.md), [LICENSE.md](LICENSE.md), [NOTICE.txt](NOTICE.txt) and [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md). Datasets are not included or relicensed.

## What changed from v0.4.0

- **Same model, new review threshold.** The weights, calibration curve and `risky` threshold are unchanged from v0.4.0. The `review` threshold moves from `0.819` to `0.303`, so Nano asks about more borderline commands. It never blocks more.
- **How it was set:** each realistic area of the held-out calibration data may now have up to 8% of its safe commands asked about (v0.4.0 allowed 5%). This keeps a margin under the 10% line that the Triage Score treats as usable.
- **Results** (Triage Score: risky commands asked about or blocked earn a point; scaled down when more than 10% of safe commands are stopped; three benchmarks weighted by size):

| At the shipped thresholds | v0.4.1 | v0.4.0 |
|---|---:|---:|
| **Triage Score** | **75.3** | 73.2 |
| lancet-bench-1: risky caught / safe stopped | **91.7%** / 9.4% | 89.0% / 6.2% |
| ShellRisk-Bench test: risky caught / safe stopped | **70.5%** / 3.1% | 60.6% / 2.3% |
| Neutral set: risky caught / safe stopped | 59.5% / 25.0% | 57.1% / 12.5% |
| Risky commands blocked outright (lancet-bench-1) | 67.0% | 67.0% |

**Expect more `review` results than with v0.4.0:** about 1 in 11 safe commands on the release benchmark, against 1 in 16.

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

| lancet-bench-1 (793 commands) | v0.4.1 | v0.4.0 | v0.3.0 | v0.2.0 | Jev (hosted) |
|---|---:|---:|---:|---:|---:|
| Risky caught | **91.7%** | 89.0% | 85.8% | 73.6% | 96.8% |
| Safe interrupted | 9.4% | 6.2% | 5.5% | 6.2% | 7.8% |
| Risky secrets caught | **77%** | 72% | 66% | 24% | 98% |
| AUROC | **0.974** | **0.974** | 0.962 | 0.896 | 0.982 |

- **Speed:** unchanged from v0.4.0: median warm time 13.9 ms per command (p95 19.2 ms) on a Ryzen 9 3900X / Windows 11 with four ONNX Runtime threads.
- **Labels:** no language-model output was used as a label, teacher target or selection signal.

Details are in [MODEL_CARD.md](MODEL_CARD.md).

## Contents

- `model/`: INT8 ONNX model, tokenizer, `model.json` (calibration and thresholds), `export.json` (hashes), runtime.
- `MODEL_CARD.md`, licenses and notices, and `licenses/`.
- `provenance/`: the aggregate training receipt and the V5 inspection-pool lineage audit. These contain no commands or datasets.
- `RELEASE-MANIFEST.json`: per-file hashes.
