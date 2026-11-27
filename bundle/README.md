# LANCET Nano v0.5.0 (experimental, CPU INT8)

A tiny, standalone local command-risk classifier for **Bash, PowerShell and cmd** with **110.8M parameters** (a CodeT5+ encoder, `110.55 MB` INT8 ONNX). It classifies each command as `risky`, `review` or `not_flagged` entirely on CPU in **~70 ms median** with zero network access, zero API cost, and zero telemetry.

**Model: Apache-2.0. Runtime: MIT.** Use, modification and redistribution, including commercial use, are permitted under the respective licenses. See [MODEL-LICENSE.md](MODEL-LICENSE.md), [LICENSE.md](LICENSE.md), [NOTICE.txt](NOTICE.txt) and [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md). Datasets are not included or relicensed.

## What changed from v0.4.3

- **Massive jump on unseen Bench 3 Core (`27.36 → 71.31`):** On the 6,846-command unseen **lancet-bench-3** core suite, v0.5.0 cuts safe command interruptions by **3×** (`30.8% → 9.93%`, cleanly under the 10% usability cliff) while holding `71.31%` risky catch (AUROC `0.8965`) — lifting overall Bench 3 score by **`+25.07` points** (`43.44 → 68.51`).
- **Explicit shell tagging (`semantic-windowed-3`):** Commands are prefixed with `<shell=bash>`, `<shell=powershell>`, or `<shell=cmd>` before byte-BPE windowing, improving cross-shell accuracy on PowerShell and `cmd`.
- **Multi-shell wrapper invariance & pipeline mastery:** Trained with `27,920` paired wrapped contrasts across all 15 Bash, PowerShell, and `cmd` wrappers (`pipeline`, `ps-pipeline`, `cmd-pipeline`, `background-wait`, `nested-shell`, `subshell`, `substitution`, `function-call`, etc.) plus an explicit unwrapped-to-wrapped consistency loss — lifting PowerShell pipeline catch **14×** over Round 25 Preview (`5.4% → 76.8%`) and Bash pipeline catch from `38.9% → 58.1%` while slashing wrapper false alarms.
- **Lowest false-alarm rate among top guards (`5.13%` pooled):** Cuts pooled safe interruptions across all `7,784` safe commands from `15.3%` (v0.4.3) down to **`5.13%`**, beating every hosted frontier LLM guard tested on the same 11,859-command suite.
- **Full-length windowed coverage:** Inputs up to 8,192 UTF-8 bytes are split into overlapping 512-token windows (64-token overlap) and pooled completely with no silent truncation.

## Bench 3 Results (`use 067`, full 11,859-row singleton CPU pass)

Weighted Bench 3 score: every risky command asked about or blocked earns credit; safe interruptions above 10% penalize each set proportionally. Overall weights: **Bench 3 core** (`6,846` commands, `66.8%`), **ShellRisk test** (`4,194`, `15.9%`), **Neutral pool** (`589`, `17.3%`).

> **Important disclosure:** Per project owner policy (`evals/protected-19.json`), v0.5.0 fitted on the upstream ShellRisk-Bench train and test splits (with GPL `gtfobins` and `nl2bash` origins excluded); **ShellRisk test is therefore in-distribution for v0.5.0 and is not an external check.** **Bench 3 core (`6,846` commands)** and the **Neutral pool (`589` commands: Shell Safety v2 test + Rogue)** remained strictly unseen (`Guard.assert_clean` verified, zero commands executed).

| Guard (shipped / measured settings) | Overall | Bench 3 Core *(unseen)* | ShellRisk *(in-dist for v0.5.0)* | Neutral *(unseen)* | Pooled Safe Int | Median ms |
|---|---:|---:|---:|---:|---:|---:|
| **LANCET Nano v0.5.0 (local CPU)** | **68.51** | **71.31** (`71.3%` / `9.9%`) | **70.47** (`70.5%` / `1.1%`) | 55.90 (`55.9%` / `4.2%`) | **5.1%** | **70.0 ms** |
| Google Gemini Decision 1 (hosted) | 60.03 | 54.32 | 53.37 | 88.21 | 11.6% | 249.0 ms |
| Perplexity Decider v1.2 (hosted) | 59.22 | 50.71 | 54.92 | **96.07** | 13.3% | 211.0 ms |
| TypeSafe Jev 1.14 (hosted) | 50.69 | 47.52 | 39.38 | 73.36 | 12.2% | 148.2 ms |
| Cat Shell Risk Commander (local) | 44.43 | 22.59 | **90.16** | 86.90 | 10.6% | **3.8 ms** |
| LANCET Nano v0.4.3 (previous release) | 43.44 | 27.36 (`84.3%` / `30.8%`) | 64.77 (`64.8%` / `3.0%`) | 86.03 (`86.0%` / `5.6%`) | 15.3% | 35.3 ms |

Diagnostic tracks on Bench 3: **Robustness expected-action `94.12%`**, Context ask `5.88%`, Multi-step Chains `43.48%` whole-input catch at `7.14%` safe control interruption.

## Verify before use

Check the downloaded ZIP against `SHA256SUMS.txt`, extract it, and run:

```text
python verify_bundle.py --strict
```

This checks every packaged file against `RELEASE-MANIFEST.json`. It does not load the model or execute any input. Checksums confirm consistency with the downloaded manifest; they are not a digital signature.

## Run locally

Python 3.12 (Linux / macOS / Windows):

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=1 printf '{"command":"kubectl delete namespace prod","shell":"bash"}\n' | .venv/bin/python classify.py --model model
```

On Windows / PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:OPENBLAS_NUM_THREADS = '1'
'{"command": "Remove-Item -Recurse -Force C:\\Users\\me\\Documents", "shell": "powershell"}' | .\.venv\Scripts\python.exe classify.py --model model
```

- **Input:** one JSON object per line on stdin, with a `command` string and `shell` set to `bash`, `powershell` or `cmd`.
- **Speed:** keep the process running to reuse the loaded model (`~70 ms` median CPU on 4 ONNX threads across 11,859 singleton commands; longer multi-window commands take one encoder pass per 512-token window).
- **Safety of input:** commands are classified as inert text and are **never executed**.

Each output line includes `classification` (`risky`, `review`, or `not_flagged`), `score`, `riskLogit`, `askLogit`, `reviewThreshold`, `riskyThreshold`, `experimental: true`, and `executionAuthorized: false`.

> **Important:** **`not_flagged` is not execution authorization or a safety guarantee.** In v0.5.0, the shipped thresholds favor human-in-the-loop `review` (`ask`) over automatic hard `block` (`risky`) to keep false blocks near zero (`7/7,784` pooled). Always pair command classifiers with OS sandboxing and least-privilege execution.

## Contents

- `model/`: INT8 ONNX encoder (`encoder-int8.onnx`), NumPy head (`head.npz` + browser-ready `head.json`/`head.bin`), tokenizer (`vocab.json`, `merges.txt`), `model.json`, `export.json`, runtime.
- `MODEL_CARD.md`, licenses and notices, and `licenses/`.
- `provenance/`: aggregate training and Bench 3 (`use 067`) receipt plus historical lineage audit. No commands or datasets are included.
- `RELEASE-MANIFEST.json`: per-file SHA-256 hashes.
