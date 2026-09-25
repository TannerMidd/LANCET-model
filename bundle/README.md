# LANCET v0.1.0 — experimental V5 CPU INT8

A local, 35.3M-parameter Bash command-risk classifier. This package contains the existing **V5 `codet5-balanced` / `recall95`** model, not V6 or a current research candidate. No model, tokenizer, runtime, calibration or threshold bytes were changed for the release.

**Model: Apache-2.0. Runtime: MIT.** Use, modification and redistribution, including commercial use, are permitted under the respective licenses. See [MODEL-LICENSE.md](MODEL-LICENSE.md), [LICENSE.md](LICENSE.md), [NOTICE.txt](NOTICE.txt) and [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md). Datasets are not included or relicensed.

## Verify before use

Check the downloaded ZIP against the accompanying `SHA256SUMS.txt`, then extract it and run:

```text
python verify_bundle.py --strict
```

This checks every packaged file against the release manifest without loading a model or executing inputs. Checksums verify consistency with the trusted downloaded checksum/manifest; they are not a digital signature or independent validation.

## Run locally

Python 3.12, Windows / PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:OPENBLAS_NUM_THREADS = '1'
.\.venv\Scripts\python.exe classify.py --model model
```

Send one JSON object per line on stdin, with a `command` string and `shell` set to `bash`. Keep the process running to reuse the loaded model. Inputs are classified as inert text, **never executed**. No API key or network access is needed for inference after dependencies are installed.

On macOS/Linux use `.venv/bin/python` and set `OPENBLAS_NUM_THREADS=1`. Those platforms were not benchmarked here. Runtime dependencies are pinned but are not vendored; install their distributions with their own licenses/notices.

Outputs: `risky`, `not_flagged`, or `review`. **`not_flagged` is not execution authorization or a safety guarantee.** PowerShell, unsupported/invalid input, more than 8,192 UTF-8 bytes or more than 512 tokens require review; there is no silent truncation. The model does not inspect files, retrieve scripts or know task context.

## Evidence and limits

- Weights plus tokenizer: approximately 37.85 MB decimal; CPU inference.
- Historical classifier-only eval150 replay: **138/150** required interventions caught; **14/128** controls interrupted. These are adaptive research results, not independent test accuracy.
- Historical mean warm inference: **3.1 ms**, about **115 MB** resident RAM after warmup and **151 MB** observed peak, on Ryzen 9 3900X / Windows 11. Four ONNX Runtime intra-op threads, one inter-op thread, batch one, `OPENBLAS_NUM_THREADS=1`. Startup is excluded; longer supported inputs may take substantially longer. These are observations, not hardware-independent guarantees.
- Independent acceptance and human label adjudication remain **unavailable and unmet**. No new benchmark scoring was performed to prepare this package.

**Development and programmatic evidence; not independently validated.** Experimental/safety guidance is not an additional license restriction.

## Provenance and contents

- `model/`: original frozen INT8 ONNX model, tokenizer, metadata, runtime and historical bundle README. The FP32 graph and fitting checkpoints are not included.
- `MODEL_CARD.md`: release-specific identity, provenance and limitations.
- `MODEL-LICENSE.md`, `LICENSE.md`, `NOTICE.txt`, `MODIFICATIONS.md`, `THIRD-PARTY-NOTICES.md`, `licenses/`: current grants, full notices and source-specific evidence.
- `provenance/`: aggregate V4/V5 lineage receipt and original source-commit model card. No raw commands, datasets, private logs or evaluation corpora are included there.
- `RELEASE-MANIFEST.json`: per-file hashes, the exact original artifact commit and hashes of the additional release-preparation sources. The release overlay is identified separately; it is not falsely attributed to that older commit.

Frozen runtime/model source commit: `c9a571fa40452ad26d3b8bf75399af91c41416c0` in <https://github.com/TannerMidd/LANCET>. Historical pre-release documents are preserved, not rewritten; the current model grant is [MODEL-LICENSE.md](MODEL-LICENSE.md).
