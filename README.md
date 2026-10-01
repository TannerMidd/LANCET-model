<h1 align="center">LANCET Nano</h1>
<p align="center">A local classifier for shell command risk: Bash, PowerShell and cmd.</p>
<p align="center"><strong>v0.4.3 · 111M parameters · 115 MB · CPU INT8 ONNX · ~14 ms per command · offline</strong></p>

<p align="center">
  <a href="https://github.com/TannerMidd/LANCET-model/releases/tag/v0.4.3">Download v0.4.3</a> ·
  <a href="https://huggingface.co/spaces/fingerthief/lancet-nano">Try it in your browser</a> ·
  <a href="https://tannermidd.github.io/LANCET-model/">Website</a> ·
  <a href="bundle/MODEL_CARD.md">Model card</a> ·
  <a href="bundle/README.md">Usage</a> ·
  <a href="benchmarks/lancet-bench-1/">Benchmark data</a> ·
  <a href="LICENSE.md">Licenses</a>
</p>

**Model: Apache-2.0. Runtime: MIT.** You may use, modify and redistribute it, including commercially, under the respective terms. Training data is not included or relicensed.

<p align="center"><img src="docs/charts/triage.png" alt="Triage Score at shipped settings across 7,911 commands from three benchmarks: LANCET Nano v0.4.3 68.3, LANCET Nano v0.4.2 54.4, LANCET Nano v0.4.0 47.1, LANCET Nano v0.4.1 44.9, LANCET Nano v0.3.0 44.7, LANCET Nano v0.2.0 40.7, LANCET Nano v0.1.0 40.5, Jev 38.9, Kestrel 30.7, ModernBERT bash 23.2, bash-classify 14.3, Laya 13.3, bev-decider 13.3, sh-guard 10.9" width="100%"></p>

## What's new in v0.4.3

- **Triage Score 68.3** (v0.4.2: 54.4), the best of any guard tested on the new, harder benchmark. Every risky command asked about or blocked earns a point; the score shrinks when more than 10% of safe commands are stopped. Three benchmarks (7,911 commands), weighted by size.
- **PowerShell and cmd.** v0.4.2 answered `review` for every non-Bash command; v0.4.3 classifies all three shells.
- **Long commands read in full.** Commands longer than one 512-token window are split into overlapping windows and every token is used. Nothing is truncated.
- **Far fewer interruptions on look-alike safe commands.** On lancet-bench-2-next it catches the same 78.0% of risky commands as v0.4.2 while stopping 12.4% of safe ones instead of 20.0%.
- **ShellRisk-Bench test split:** 64.8% caught (v0.4.2: 60.1%), 3.0% of safe commands stopped (2.7%).
- **Neutral set:** 85.8% caught (91.0%), 5.6% stopped (7.0%).
- **A newly trained model** on a new command-semantics curriculum of risky/safe twins (21,544 rows), trained to convergence. Same size and CPU speed as v0.4.2.

<p align="center"><img src="docs/charts/v043-vs-v042.png" alt="LANCET Nano v0.4.3 vs v0.4.2: Triage Score on lancet-bench-2-next, ShellRisk-Bench and a neutral third-party set, plus caught, stopped and blocked rates" width="100%"></p>

## Why every score dropped: a harder benchmark

Until v0.4.2, the Triage Score used **lancet-bench-1** (793 Bash commands). It had become too easy to tell the best guards apart: Jev caught 96.8% of its risky commands and v0.4.2 92.4%. It was also narrow, with Bash only, short single-line commands, and a quarter of its cases about secrets.

From v0.4.3 the Triage Score uses **lancet-bench-2-next**, a new, much more comprehensive benchmark:

- **3,204 commands built as 1,602 risky/safe twins.** Every risky command has a safe look-alike that differs only in the detail that decides the risk, such as reading a secret's expiry date instead of its value, or a real preview instead of one that changes things first.
- **289 scenarios in 40 areas:** AWS, Azure and GCP, Kubernetes, PostgreSQL, Redis, SQLite and other databases, Git, CI and publishing, containers, credentials, filesystems and backups, infrastructure as code, deceptive previews, encoded input, shell quoting, expansion, redirection, state and control flow, Python, JavaScript and data tools, messaging, remote execution, and macOS and Windows administration.
- **Every scenario must survive composition.** Each one is repeated inside a subshell, a function, a command substitution, a nested `bash -c`, a pipeline and a background job.
- **Three shells:** 3,066 Bash, 102 PowerShell and 36 cmd commands. Commands are longer and more realistic: 1,803 are multi-line; lancet-bench-1 had none.
- **Held out.** No LANCET release was trained, tuned or calibrated on it. Each guard is scored once at its shipped setting.

Because it is much harder, **every guard scores lower than before**, LANCET and comparators alike. v0.4.2 scored 82.7 under the previous Triage Score and 54.4 under the new one. The model did not change; the test did. Scores are only comparable on the same benchmark. lancet-bench-1 is retired and now part of LANCET's training data; its commands, labels and results stay [published](benchmarks/lancet-bench-1/).

## Where v0.4.3 gains and loses

<p align="center"><img src="docs/charts/v043-gains-losses.png" alt="v0.4.3 vs v0.4.2 on the same commands: Triage +13.9; lancet-bench-2-next catches unchanged with 122 fewer safe commands interrupted; ShellRisk catches up 4.7 points; the neutral set is the only Triage loss (-1.1 points)" width="100%"></p>

## Triage Score by release

<p align="center"><img src="docs/charts/history.png" alt="Triage Score by release on lancet-bench-2-next: v0.1.0 40.5, v0.2.0 40.7, v0.3.0 44.7, v0.4.0 47.1, v0.4.1 44.9, v0.4.2 54.4, v0.4.3 68.3" width="100%"></p>

Every LANCET Nano release scored the same way, at its shipped setting, on the same three benchmarks. The grey ticks mark each release's score on the retired lancet-bench-1.

## Triage Score across three benchmarks

<p align="center"><img src="docs/charts/triage-points.png" alt="Risky commands caught against safe commands stopped, combined across lancet-bench-2-next, ShellRisk-Bench and a neutral set, with each guard's Triage Score: LANCET Nano v0.4.3 68.3, LANCET Nano v0.4.2 54.4, LANCET Nano v0.4.0 47.1, LANCET Nano v0.4.1 44.9, LANCET Nano v0.3.0 44.7, LANCET Nano v0.2.0 40.7, LANCET Nano v0.1.0 40.5, Jev 38.9, Kestrel 30.7, ModernBERT bash 23.2, bash-classify 14.3, Laya 13.3, bev-decider 13.3, sh-guard 10.9" width="100%"></p>

Each guard is scored once at its shipped setting on three benchmarks (7,911 commands): lancet-bench-2-next (3,204), the ShellRisk-Bench test split (4,194) and a neutral set of outside-party commands (513). Every risky command asked about or blocked earns a point; the score shrinks in proportion when more than 10% of safe commands are stopped. The three are combined by size (58% / 20% / 21%). Risky caught and safe stopped are combined the same way.

| Guard | Triage Score | lancet-bench-2-next | ShellRisk test | Neutral set | Risky caught | Safe stopped | Parameters | Runs on |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| **LANCET Nano v0.4.3** | **68.3** | 63.1 | 64.8 | 85.8 | 77.0% | 9.0% | 111 M | CPU, local |
| LANCET Nano v0.4.2 | 54.4 | 39.0 | 60.1 | 91.0 | 77.1% | 13.7% | 110 M | CPU, local |
| LANCET Nano v0.4.0 | 47.1 | 41.1 | 60.6 | 50.8 | 55.7% | 10.5% | 110 M | CPU, local |
| LANCET Nano v0.4.1 | 44.9 | 38.1 | 70.5 | 39.3 | 67.9% | 14.6% | 110 M | CPU, local |
| LANCET Nano v0.3.0 | 44.7 | 44.3 | 46.6 | 43.6 | 55.3% | 11.6% | 110 M | CPU, local |
| LANCET Nano v0.2.0 | 40.7 | 39.3 | 47.7 | 37.9 | 55.2% | 13.6% | 35 M | CPU, local |
| LANCET Nano v0.1.0 | 40.5 | 34.9 | 45.6 | 51.0 | 58.4% | 14.1% | 35 M | CPU, local |
| Jev | 38.9 | 43.6 | 32.4 | 32.1 | 90.0% | 23.4% | undisclosed | hosted API |
| Kestrel | 30.7 | 12.7 | 100.0 | 14.0 | 68.1% | 37.1% | — | local |
| ModernBERT bash | 23.2 | 16.2 | 40.9 | 25.6 | 48.1% | 22.8% | 150 M | local |
| bash-classify | 14.3 | 13.5 | 16.8 | 14.0 | 92.9% | 65.8% | rules | local |
| Laya | 13.3 | 11.0 | 16.2 | 17.1 | 87.3% | 69.6% | 421 M | GPU, local |
| bev-decider | 13.3 | 10.8 | 18.7 | 14.8 | 94.4% | 75.3% | 0.4 B | GPU, local |
| sh-guard | 10.9 | 10.2 | 12.1 | 11.7 | 97.9% | 90.5% | rules | local |

Jev received task context; the others see only the command. Per-benchmark columns are each benchmark's own Triage Score (0-100). Guards that support only Bash answer the 138 PowerShell and cmd commands as "ask".

<p align="center"><img src="docs/charts/by-area.png" alt="Triage Score by area on lancet-bench-2-next for Nano v0.4.2, v0.4.3 and Jev" width="100%"></p>

Detail by area on lancet-bench-2-next. More charts are on the [website](https://tannermidd.github.io/LANCET-model/).

## Quick start

Download the [release ZIP](https://github.com/TannerMidd/LANCET-model/releases/download/v0.4.3/lancet-v0.4.3-nano-cpu-int8.zip) and its [checksum](https://github.com/TannerMidd/LANCET-model/releases/download/v0.4.3/SHA256SUMS.txt). Verify the checksum and extract the ZIP. Then, inside the extracted directory (Python 3.12, Windows / PowerShell), run:

```powershell
python verify_bundle.py --strict
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:OPENBLAS_NUM_THREADS = '1'
'{"command": "kubectl delete namespace prod", "shell": "bash"}' | .\.venv\Scripts\python.exe classify.py --model model
'{"command": "Remove-Item -Recurse -Force C:\\Users\\me\\Documents", "shell": "powershell"}' | .\.venv\Scripts\python.exe classify.py --model model
```

Send JSON lines with a `command` string and `shell` set to `bash`, `powershell` or `cmd`. Each input is classified as `risky`, `review` or `not_flagged`. Inputs are inert text and are **never executed**. No API key or network connection is needed after installation. See the [full instructions](bundle/README.md).

If you clone the repository instead of downloading the ZIP, install Git LFS, run `git lfs pull`, and use `bundle/`.

## How it was trained

LANCET Nano v0.4.3 is the Salesforce **CodeT5+ 220M** encoder, fine-tuned from its pinned upstream weights, with a small pooling head that reads long commands as overlapping windows. It does not start from an earlier LANCET checkpoint.

Training labels come from **project authoring, documentation and source datasets, not model opinions**:
- LANCET's new command-semantics curriculum: project-authored risky/safe twins for Bash, PowerShell and cmd, including long multi-line scripts
- the wording of human-written example descriptions in [tldr-pages](https://github.com/tldr-pages/tldr) (CC BY 4.0)
- AWS operation verbs and the `sensitive` output-field markings in [botocore](https://github.com/boto/botocore) service models (Apache-2.0), so commands that print credentials are risky
- reference examples from the Azure CLI, GitHub CLI (MIT), kubectl and Docker CLI (Apache-2.0)
- attack-technique and everyday developer commands from the [ShellRisk-Bench](https://huggingface.co/datasets/kontext-security/ShellRisk-Bench) training split, with its upstream labels
- the [Shell Safety v2](https://huggingface.co/datasets/tomngdev/shell-safety-v2) training split (MIT), with its author's allow/deny labels
- LANCET's project-authored risky/safe pairs, contrast sets of agent-style, `exec`-style and shell-escape commands, a secrets family, its earlier evaluation suites and the retired lancet-bench-1 (original labels)

No language model, hosted API or human labeler produced any training label. See the [model card](bundle/MODEL_CARD.md) and [source notices](bundle/THIRD-PARTY-NOTICES.md).

## Boundaries

- **Bash, PowerShell and cmd.** PowerShell and cmd coverage is newer and smaller than Bash coverage. Nano does not inspect the filesystem, fetched scripts or task context.
- Other shells, invalid input or more than 8,192 UTF-8 bytes return `review`. Inputs are never silently truncated.
- **`not_flagged` is not execution authorization or a safety guarantee.**
- Its weakest areas on lancet-bench-2-next are credentials, Windows administration, macOS administration and deceptive previews (see the chart above).

## Benchmark data

- [**lancet-bench-1**](benchmarks/lancet-bench-1/): 793 Bash commands (409 risky, 384 benign) across 37 tool areas, with labels, rationales and results for 14 command guards. It was LANCET's release benchmark until 2026-09-29, when it was retired in favour of lancet-bench-2-next. It is free to use (MIT). The commands are test data; do not run them.
- **lancet-bench-2-next** is kept private so it stays a fair, unseen test for future releases. Its design and per-area results are summarized above.

## Versions

- **v0.4.3 — LANCET Nano, CodeT5+ 220M, windowed** (current, pre-release): newly trained; Bash, PowerShell and cmd; Triage Score 68.3.
- [v0.4.2 — LANCET Nano, CodeT5+ 220M](https://github.com/TannerMidd/LANCET-model/releases/tag/v0.4.2): Triage Score 54.4 (82.7 on the retired lancet-bench-1).
- [v0.4.1 — LANCET Nano, CodeT5+ 220M](https://github.com/TannerMidd/LANCET-model/releases/tag/v0.4.1): v0.4.0 with a lower review threshold.
- [v0.4.0 — LANCET Nano, CodeT5+ 220M](https://github.com/TannerMidd/LANCET-model/releases/tag/v0.4.0): the same weights with the stricter v0.4.0 thresholds.
- [v0.3.0 — LANCET Nano, CodeT5-base](https://github.com/TannerMidd/LANCET-model/releases/tag/v0.3.0): still available unchanged.
- [v0.2.0 — LANCET Nano, CodeT5-small](https://github.com/TannerMidd/LANCET-model/releases/tag/v0.2.0): smaller (36 MB) and faster (~3–6 ms).
- [v0.1.0 — LANCET Nano v0.1.0 (formerly V5)](https://github.com/TannerMidd/LANCET-model/releases/tag/v0.1.0).

## Credits

LANCET is built on Salesforce CodeT5+ by **Yue Wang, Hung Le, Akhilesh Deepak Gotmare, Nghi D. Q. Bui, Junnan Li and Steven C. H. Hoi**. Training commands come from the **tldr-pages** team and contributors, AWS **botocore**, the Azure CLI, GitHub CLI, kubectl and Docker CLI projects, **ShellRisk-Bench** by Kontext Security (with **Atomic Red Team** by Red Canary and **InternalAllTheThings**), **Shell Safety v2** by tomngdev, plus the datasets credited in the notices. Runtime and LANCET contributions: **Tanner Middleton**.

See the [full credits](bundle/NOTICE.txt), [source notices](bundle/THIRD-PARTY-NOTICES.md) and [model changes](bundle/MODIFICATIONS.md).
