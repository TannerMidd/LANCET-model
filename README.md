<h1 align="center">LANCET</h1>
<p align="center">A small, local classifier for Bash command risk.</p>
<p align="center"><strong>35.3M parameters · CPU INT8 ONNX · Offline inference</strong></p>

<p align="center">
  <a href="https://github.com/TannerMidd/LANCET-model/releases/tag/v0.1.0">Download v0.1.0</a> ·
  <a href="bundle/MODEL_CARD.md">Model card</a> ·
  <a href="bundle/README.md">Usage</a> ·
  <a href="LICENSE.md">Licenses</a>
</p>

**Model: Apache-2.0. Runtime: MIT.** Use, modify and redistribute—including commercially—under the respective terms. Training data is not included or relicensed.

## Quick start

Download the [release ZIP](https://github.com/TannerMidd/LANCET-model/releases/download/v0.1.0/lancet-v0.1.0-v5-cpu-int8.zip) and [checksum](https://github.com/TannerMidd/LANCET-model/releases/download/v0.1.0/SHA256SUMS.txt), verify the checksum, and extract. Inside the extracted directory, using Python 3.12 on Windows / PowerShell:

```powershell
python verify_bundle.py --strict
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:OPENBLAS_NUM_THREADS = '1'
.\.venv\Scripts\python.exe classify.py --model model
```

Send JSONL on stdin with a `command` string and `shell` set to `bash`. Outputs are `risky`, `not_flagged`, or `review`. Inputs are inert text—**never executed**. No API key or network connection is needed after installation. [Full instructions and platform notes](bundle/README.md).

Cloning instead? Install Git LFS, run `git lfs pull`, and use the unchanged files inside `bundle/`. ZIP downloads do not require Git LFS.

## Boundaries

- **Bash only.** No filesystem inspection, fetched scripts or task context.
- PowerShell, invalid/unsupported inputs, more than 8,192 UTF-8 bytes or more than 512 tokens require review. No silent truncation.
- **`not_flagged` is not execution authorization or a safety guarantee.** Historical evaluations are adaptive, not independent accuracy.
- Independent acceptance and human label adjudication remain unavailable and unmet.

**Development and programmatic evidence; not independently validated.**

## Credits and release scope

Built on Salesforce CodeT5-small by **Yue Wang, Weishi Wang, Shafiq Joty and Steven C. H. Hoi**. Runtime and LANCET contributions: **Tanner Middleton**. [Full credits](bundle/NOTICE.txt) · [Source-specific notices](bundle/THIRD-PARTY-NOTICES.md) · [Model changes](bundle/MODIFICATIONS.md).

This is the **V5 `codet5-balanced` / `recall95`** model-only distribution. The model, tokenizer, runtime, calibration and threshold are unchanged. The ZIP was verified by 79 passing project tests, a reproducible build, CPU startup and matching downloaded hashes. The bundle manifest records its original artifact commit and release overlay at build time; that overlay is now included here.

This repository has a new, standalone history. It does not mirror the private research repository or distribute datasets, evaluation corpora, private logs, fitting checkpoints or V6 research candidates. Source license declarations do not independently certify every upstream snippet's chain of title.
