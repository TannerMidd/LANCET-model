# LANCET Nano v0.3.0 (experimental, CPU INT8)

A local Bash command-risk classifier with 109.6M parameters (a CodeT5-base encoder). It classifies each command as `risky`, `review` or `not_flagged` on a CPU in tens of milliseconds, with no network access.

**Model: Apache-2.0. Runtime: MIT.** Use, modification and redistribution, including commercial use, are permitted under the respective licenses. See [MODEL-LICENSE.md](MODEL-LICENSE.md), [LICENSE.md](LICENSE.md), [NOTICE.txt](NOTICE.txt) and [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md). Datasets are not included or relicensed.

## What changed from v0.2.0

- **Larger encoder:** CodeT5-base (109.6M parameters, 111 MB INT8) instead of CodeT5-small (35.3M, 36 MB). It was trained from the pinned upstream weights, not from any earlier LANCET checkpoint.
- **More training data:**
  - Azure CLI, GitHub CLI, kubectl and Docker CLI reference examples.
  - A secret-reveal labelling rule for documented commands that print or mint secrets.
  - A project-authored secrets family.
  - LANCET's earlier, now-retired agent-authored evaluation suites.
- **Results on the new 793-command release benchmark (`lancet-bench-1`):**
  - catches **85.8%** of risky commands (v0.2.0: 73.6%)
  - interrupts **5.5%** of safe ones (v0.2.0: 6.2%)
  - catches **66%** of risky secrets commands (v0.2.0: 24%)
- **Cost:** it is about 3× larger and about 3.4× slower than v0.2.0 on the same CPU.

**Released by owner exception.** One preregistered release check failed. It required the lower 95% bound of the ShellRisk upstream catch-rate difference to be no worse than −5 points; the observed difference was +0.6 points with an interval of −6.5 to +7.8. That check was too strict for a 176-command set, which is disclosed as a design error. The owner approved release as a documented exception. See [MODEL_CARD.md](MODEL_CARD.md).

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

## Evidence and limits

| lancet-bench-1 (793 commands, one counted pass each) | v0.3.0 | v0.2.0 | v0.1.0 | Jev (hosted) |
|---|---:|---:|---:|---:|
| Risky caught | **85.8%** | 73.6% | 65.5% | 96.8% |
| Safe interrupted | **5.5%** | 6.2% | 5.5% | 7.8% |
| Risky secrets caught | **66%** | 24% | 14% | 98% |

- **Agent-authored benchmark:** the developer (an AI agent) wrote the benchmark and its labels, so this is not independent acceptance. The benchmark has informed two development rounds.
- **ShellRisk upstream sets** (not agent-authored, never trained on):
  - source-external: v0.3.0 caught about the same share of risky commands as v0.2.0 (48.9% vs 48.3%) and interrupted fewer safe ones (6.3% vs 9.7%).
  - source-holdout: v0.3.0 caught fewer (41.9% vs 45.9%), and its ranking quality (AUROC) is lower on both sets.
- **Speed:** median warm time was 21.8 ms per command against 6.4 ms for v0.2.0, in the same run on a busy Ryzen 9 3900X / Windows 11 with four ONNX Runtime threads.
- **Labels:** no language-model output was used as a label, teacher target or selection signal.

## Contents

- `model/`: INT8 ONNX model, tokenizer, `model.json` (calibration and thresholds), `export.json` (hashes), runtime.
- `MODEL_CARD.md`, licenses and notices, and `licenses/`.
- `provenance/`: the aggregate training receipt, the release-gate result with its exception, and the V5 inspection-pool lineage audit. These contain no commands or datasets.
- `RELEASE-MANIFEST.json`: per-file hashes.
