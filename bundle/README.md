# LANCET Nano v0.4.3 (experimental, CPU INT8)

A local command-risk classifier for **Bash, PowerShell and cmd** with 110.8M parameters (a CodeT5+ encoder). It classifies each command as `risky`, `review` or `not_flagged` on a CPU in about 14 ms, with no network access.

**Model: Apache-2.0. Runtime: MIT.** Use, modification and redistribution, including commercial use, are permitted under the respective licenses. See [MODEL-LICENSE.md](MODEL-LICENSE.md), [LICENSE.md](LICENSE.md), [NOTICE.txt](NOTICE.txt) and [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md). Datasets are not included or relicensed.

## What changed from v0.4.2

- **A newly trained model on a new curriculum.** v0.4.3 is fine-tuned again from the pinned upstream CodeT5+ 220M base. New in the mix: a project-authored command-semantics curriculum (21,544 rows) of risky/safe twins for Bash, PowerShell and cmd, including long multi-line scripts. Training now runs to convergence (cosine decay to zero).
- **PowerShell and cmd.** v0.4.2 answered `review` for every non-Bash command. v0.4.3 classifies them.
- **Long commands are read in full.** Inputs longer than one 512-token window are split into overlapping windows and every token is used. Nothing is truncated; the old 512-token limit is gone (the 8,192-byte limit remains).
- **Far fewer interruptions on look-alike safe commands.** On lancet-bench-2-next, v0.4.3 catches the same 78.0% of risky commands as v0.4.2 while stopping 12.4% of safe ones instead of 20.0%. On ShellRisk-Bench it catches more (64.8% vs 60.1%) at about the same interruption rate.
- **More decisive.** v0.4.3 blocks outright half of the risky commands it sees on lancet-bench-2-next (v0.4.2: 17.7%) and asks about fewer.

## A harder benchmark

Earlier releases were scored on lancet-bench-1 (793 Bash commands). The strongest guards were close to its ceiling: Jev caught 96.8% and v0.4.2 92.4%. From v0.4.3 the Triage Score uses **lancet-bench-2-next**, a much more comprehensive benchmark that no model was trained, tuned or calibrated on:

- **3,204 commands, built as 1,602 risky/safe twins.** Each risky command has a safe look-alike that differs only in the detail that decides the risk (reading a secret's expiry date versus reading its value, a dry run versus the real thing).
- **289 scenarios across 40 areas:** AWS, Azure and GCP, Kubernetes, databases, Git, CI and publishing, containers, credentials, filesystems, deceptive previews, encoded input, quoting, expansion, redirection, control flow, macOS and Windows administration, and more.
- **Each scenario survives composition:** it is repeated inside a subshell, a function, a command substitution, a nested `bash -c`, a pipeline and a background job.
- **Three shells:** 3,066 Bash, 102 PowerShell and 36 cmd commands. Commands are longer and more realistic: 1,803 are multi-line, against none in lancet-bench-1.

Because the benchmark is much harder, **every guard's Triage Score is lower than before.** v0.4.2 scored 82.7 under the previous Triage Score; on the same commands under the new one it scores 54.4. The model did not change; the test did. Scores are only comparable within the same benchmark.

## Results

Triage Score: every risky command asked about or blocked earns a point; the score shrinks in proportion when more than 10% of safe commands are stopped. Overall = lancet-bench-2-next 58%, ShellRisk-Bench test 20%, neutral set 21% (weighted by size).

| At the shipped thresholds | v0.4.3 | v0.4.2 | Jev (hosted) |
|---|---:|---:|---:|
| **Triage Score** | **68.3** | 54.4 | 38.9 |
| lancet-bench-2-next (3,204): risky caught / safe stopped | 78.0% / **12.4%** | 78.0% / 20.0% | **95.1%** / 21.8% |
| ShellRisk-Bench test (4,194): risky caught / safe stopped | 64.8% / 3.0% | 60.1% / **2.7%** | **67.9%** / 20.9% |
| Neutral set (513): risky caught / safe stopped | 85.8% / **5.6%** | 91.0% / 7.0% | **97.2%** / 30.2% |
| Risky blocked outright (lancet-bench-2-next) | 50.0% | 17.7% | 62.0% |

Every earlier release and the other command guards scored on the same benchmarks are in the [full comparison table](https://github.com/TannerMidd/LANCET-model#triage-score-across-three-benchmarks).

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
'{"command": "Remove-Item -Recurse -Force C:\\Users\\me\\Documents", "shell": "powershell"}' | .\.venv\Scripts\python.exe classify.py --model model
```

On macOS or Linux, use `.venv/bin/python` and set `OPENBLAS_NUM_THREADS=1`. Those platforms were not benchmarked.

- **Input:** one JSON object per line on stdin, with a `command` string and `shell` set to `bash`, `powershell` or `cmd`.
- **Speed:** keep the process running to reuse the loaded model. Long commands take longer: one encoder pass per 512-token window.
- **Safety of input:** commands are classified as inert text and are **never executed**.

Each output line includes:
- `classification`: `risky`, `review` or `not_flagged`
- `score`: the calibrated score, and `riskLogit`
- both thresholds
- `experimental: true` and `executionAuthorized: false`

**`not_flagged` is not execution authorization or a safety guarantee.** Other shells, invalid input or more than 8,192 UTF-8 bytes return `review`. Inputs are never silently truncated.

## Evidence

- **Speed:** the same as v0.4.2 when measured side by side (median within 1%): about 14 ms per command on a Ryzen 9 3900X / Windows 11 with four ONNX Runtime threads. Commands longer than one 512-token window take one encoder pass per window.
- **Labels:** no language-model output was used as a label, teacher target or selection signal.
- **Held out:** lancet-bench-2-next, the ShellRisk-Bench test split and the neutral set were never used for training, development, selection or calibration.

Details are in [MODEL_CARD.md](MODEL_CARD.md).

## Contents

- `model/`: INT8 ONNX encoder, NumPy head (`head.npz`), tokenizer vocabulary and merges, `model.json` (calibration and thresholds), `export.json` (hashes), runtime.
- `MODEL_CARD.md`, licenses and notices, and `licenses/`.
- `provenance/`: the aggregate training receipt and the V5 inspection-pool lineage audit. These contain no commands or datasets.
- `RELEASE-MANIFEST.json`: per-file hashes.
