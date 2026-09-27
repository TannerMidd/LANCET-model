# LANCET Nano v0.4.0 (experimental, CPU INT8)

A local Bash command-risk classifier with 109.6M parameters (a CodeT5+ encoder). It classifies each command as `risky`, `review` or `not_flagged` on a CPU in about 14 ms, with no network access.

**Model: Apache-2.0. Runtime: MIT.** Use, modification and redistribution, including commercial use, are permitted under the respective licenses. See [MODEL-LICENSE.md](MODEL-LICENSE.md), [LICENSE.md](LICENSE.md), [NOTICE.txt](NOTICE.txt) and [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md). Datasets are not included or relicensed.

## What changed from v0.3.0

- **New base encoder:** Salesforce CodeT5+ 220M's encoder (BSD-3-Clause), trained from the pinned upstream weights. Same size and speed as v0.3.0.
- **New training data:**
  - Attack-technique commands from ShellRisk-Bench's training split (Atomic Red Team and InternalAllTheThings), with more SWE-smith and Terminal-Bench everyday commands as safe examples.
  - A project red-team corpus of commands that earlier LANCET versions missed, with matching safe look-alikes.
  - More project-authored evaluation cases released for training.
- **Results:**

| Catch rate at ≤10% interruption | v0.4.0 | v0.3.0 |
|---|---:|---:|
| lancet-bench-1 (793 commands) | 92.2% | 93.4% |
| ShellRisk-Bench test split (4,194 commands) | **91.2%** | 59.1% |
| Neutral third-party set (66 commands) | **52.4%** | 40.5% |

At the shipped thresholds, v0.4.0 catches **89.0%** of risky `lancet-bench-1` commands (v0.3.0: 85.8%) and interrupts 6.2% of safe ones (5.5%). On the ShellRisk-Bench test split it catches **60.6%** of risky commands (46.6%) and interrupts **2.3%** of safe ones (6.1%).

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

| lancet-bench-1 (793 commands) | v0.4.0 | v0.3.0 | v0.2.0 | v0.1.0 | Jev (hosted) |
|---|---:|---:|---:|---:|---:|
| Risky caught | **89.0%** | 85.8% | 73.6% | 65.5% | 96.8% |
| Safe interrupted | 6.2% | 5.5% | 6.2% | 5.5% | 7.8% |
| Risky secrets caught | **72%** | 66% | 24% | 14% | 98% |
| AUROC | **0.974** | 0.962 | 0.896 | 0.860 | 0.982 |

- **Speed:** median warm time was 13.9 ms per command (p95 19.2 ms) against 13.6 ms for v0.3.0, in the same run on a Ryzen 9 3900X / Windows 11 with four ONNX Runtime threads.
- **Labels:** no language-model output was used as a label, teacher target or selection signal.

Details are in [MODEL_CARD.md](MODEL_CARD.md).

## Contents

- `model/`: INT8 ONNX model, tokenizer, `model.json` (calibration and thresholds), `export.json` (hashes), runtime.
- `MODEL_CARD.md`, licenses and notices, and `licenses/`.
- `provenance/`: the aggregate training receipt and the V5 inspection-pool lineage audit. These contain no commands or datasets.
- `RELEASE-MANIFEST.json`: per-file hashes.
