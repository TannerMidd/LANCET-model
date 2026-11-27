# Third-party notices and LANCET Nano v0.5.0 fitting provenance

## Included components

| Component | License / evidence | Notice retained |
|---|---|---|
| LANCET Nano model assets | Apache-2.0 | [Explicit model grant](MODEL-LICENSE.md), [full text](licenses/Apache-2.0.txt), [changes](MODIFICATIONS.md) |
| Salesforce CodeT5+ 220M pretrained model | BSD-3-Clause declaration at revision `2b92f36e2782341a50551759fdba0dd15e821f99` | [Original upstream card](licenses/codet5p-220m-upstream-model-card.md), [Salesforce BSD-3-Clause notice](licenses/CodeT5-BSD-3-Clause.txt), [credits](NOTICE.txt) |
| CodeT5 tokenizer vocabulary and merges | Apache-2.0 declaration at revision `b1ee9570c289f21b5922b9c768a1ce12957bf968` | [Original upstream card](licenses/codet5-small-upstream-model-card.md) |
| LANCET runtime / project-authored tooling | MIT | [Tanner Middleton notice](licenses/pi-jev-guard-MIT.txt) |
| NumPy, Hugging Face tokenizers, ONNX Runtime CPU | Their own licenses | Pinned in `requirements.txt`; not vendored |

## Fitting sources: datasets not included

| Source | Fit rows | How it was used | Terms and preserved evidence |
|---|---:|---|---|
| LANCET authored core, `weak-point-24` boundary pool & released suites | 37,527 | Project-authored risky/safe contrasts and original authored labels | Project-authored (stored hosted-model outputs never used) |
| LANCET Round 61 multi-shell wrapper-invariance corpus | 27,920 | Paired contrasts wrapped across 15 Bash/PowerShell/`cmd` carriers | Project-authored |
| LANCET Round 33 composed carriers & Rounds 36/60/61 domain contrasts | 10,350 | Project-authored carrier and operational-damage contrasts | Project-authored |
| LANCET explicit review / ask track | 1,323 | Review-head supervision | Project-authored |
| ShellRisk-Bench (Kontext Security), rev `437467862139b4e9cdd5322024ef3434a67c7ec8`, train + owner-authorized test (excl. GPL `gtfobins` & `nl2bash`) | 19,144 | Upstream source labels (disclosed in-distribution for v0.5.0) | Compilation by Kontext Security; SWE-smith ([MIT](licenses/SWE-smith-license-declaration.md)), Terminal-Bench ([Apache-2.0](licenses/Terminal-Bench-license-declaration.md)), Atomic Red Team ([MIT](licenses/atomic-red-team-MIT.txt)), InternalAllTheThings (no license declared) |
| tomngdev / Shell Safety v2, rev `3258db497dae218f23d1d648ef2eb7cb6ab5e70c`, training split | 1,398 | Dataset author's `allow` / `deny` labels (`test` split stayed strictly unseen) | MIT; [declaration](licenses/shell-safety-v2-license-declaration.md), [MIT text](licenses/MIT.txt) |

The disjoint development set held a further `13,634` rows across six strata (`authored-core`, `weak-hard`, `composed-carriers`, `wrapper61`, `domain60`, `shell-safety`). **Bench 3 core (`6,846` commands)** and the **Neutral pool (`589` commands: Shell Safety v2 test + Rogue)** were never used for training, development, selection, or calibration (`Guard.assert_clean` verified against `evals/protected-19.json`).

**No hosted-model output was used.** No language model, including TypeSafe's Jev, produced any training label, teacher target, filter, or selection signal.

No raw datasets, source trajectories, private logs, evaluation corpora, fitting checkpoints or vendored dependency packages are included. The model license does **not** relicense any of those materials.
