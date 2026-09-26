# LANCET Nano v0.2.0 (experimental, CPU INT8)

A local Bash command-risk classifier with 35.3M parameters. It classifies each command as `risky`, `review` or `not_flagged` in a few milliseconds on a CPU, with no network access.

**Model: Apache-2.0. Runtime: MIT.** Use, modification and redistribution, including commercial use, are permitted under the respective licenses. See [MODEL-LICENSE.md](MODEL-LICENSE.md), [LICENSE.md](LICENSE.md), [NOTICE.txt](NOTICE.txt) and [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md). Datasets are not included or relicensed.

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

- On a fresh, sealed 400-command diagnostic suite (one pass), Nano caught **83.9%** of risky commands and interrupted **5.8%** of benign ones. V5 caught 76.3% and interrupted 8.5%.
- The suite's labels were written by the developer (an AI agent), so this is not independent acceptance.
- Median warm time was 2.7 ms per command on Ryzen 9 3900X / Windows 11, with four ONNX Runtime threads.
- Training labels for the new data come from documentation wording and AWS operation verbs, applied by deterministic rules. No language model output was used.

See [MODEL_CARD.md](MODEL_CARD.md).

## Contents

- `model/`: INT8 ONNX model, tokenizer, `model.json` (calibration and thresholds), `export.json` (hashes), runtime.
- `MODEL_CARD.md`, licenses and notices, and `licenses/`.
- `provenance/`: the aggregate Nano training receipt and the inherited V5 lineage audit. These contain no commands or datasets.
- `RELEASE-MANIFEST.json`: per-file hashes.
