# LANCET Nano v0.5.0 model card

## Identity and license

- **LANCET Nano**, v0.5.0. Internal research ID: `round61 / wise-ep1-065` (continuation from Round 25 Preview via Round 60).
- Model license: **Apache-2.0**, with an [explicit scope](MODEL-LICENSE.md). Runtime: **MIT**, see the [notice](licenses/pi-jev-guard-MIT.txt).
- Base: `Salesforce/codet5p-220m`, revision `2b92f36e2782341a50551759fdba0dd15e821f99`. Its [upstream model card](licenses/codet5p-220m-upstream-model-card.md) declares BSD-3-Clause; the [Salesforce notice](licenses/CodeT5-BSD-3-Clause.txt) is retained.
- Architecture: CodeT5+ 220M encoder over `<shell={shell}>\n{command}` formatted inputs split into overlapping 512-token windows (64-token overlap); owned-token mean and maximum pooling across windows; learned projection, layer normalization and risk/ask heads in float64 NumPy. No generative decoder is used at inference.
- Parameters: **110,789,762**. CPU INT8 ONNX encoder: `110,550,532` bytes; NumPy head: `4,732,426` bytes (`head.npz`, plus browser-ready `head.json`/`head.bin`).
- ONNX SHA-256: `23f347feddc8c51517ccf2096817d6ed107a32fdbd9215691a776f59f51f74b6`.
- Tokenizer: CodeT5 byte-BPE vocabulary and merges (`vocab.json`, `merges.txt`).
- Shells: **Bash, PowerShell and cmd.**
- Calibration: positive-slope Platt display map (scale `0.35149822580416945`, bias `-0.8978696281337076`) inherited for reported `score`; decision bands compare the raw INT8 risk logit directly against dev-calibrated INT8 logit thresholds:
  - `risky`: risk logit >= `9.677015995036761` (display score >= `0.9244`)
  - `review`: risk logit >= `8.935882516244185` (display score >= `0.9041`)
  - `not_flagged`: below `reviewLogitThreshold`
- Threshold rule: calibrated once on the INT8 `authored-core` held-out development safe tail (`3,314` safe commands) at `1.99%` safe interruption for `review` and `0.57%` safe block for `risky`. No benchmark row was used for selection or calibration.

## Fitting lineage

`Salesforce/codet5p-220m` (pinned upstream) → Round 25 Preview (`average-last3.pt`) → Round 60 (`wise-avg12-065`) → **Round 61 (`wise-ep1-065`, v0.5.0)**.

Round 61 fine-tuned from Round 60 on `97,662` protected-clean fit rows (`36,674` complete contrast pairs) with:
- Native raw-BCE logit scaling (no label smoothing, no logit L2 collapse)
- Bounded ReLU boundary sharpening (`safe <= 3.0`, `risky >= 8.0`) + within-pair margin (`0.40`)
- Selective Round 60 logit-preservation anchor (`0.30 * SmoothL1`) on `43,367` already-correct base rows
- Explicit wrapper-invariance consistency loss (`0.22 * SmoothL1(z_wrapped, z_R60_unwrapped)`) on `26,941` wrapped rows across 15 Bash/PowerShell/`cmd` wrappers
- WiSE-FT weight-space interpolation (`0.65 * epoch-01 + 0.35 * Round 60`) selected strictly on `13,634` disjoint 6-stratum hard-dev rows (`meanDevAuroc = 0.94686`, dev pipeline AUROC `0.9694`).

### Round 61 fit corpus composition (`97,662` rows; datasets not included)

| Stratum | Rows | Basis |
|---|---:|---|
| Project-authored core + `weak-point-24` hard boundary contrasts | 37,527 | Project-authored + released evaluation suites (original authored labels only) |
| Round 61 multi-shell wrapper-invariance pairs (15 Bash/PS/`cmd` wrappers) | 27,920 | Deterministic wrapping of verified-clean base pairs |
| Upstream `kontext-security/ShellRisk-Bench` (train + owner-authorized test, excl. GPL `gtfobins`/`nl2bash`) | 19,144 | Upstream source labels (disclosed in-distribution) |
| Project-authored composed carriers (Round 33) | 5,652 | Project-authored carrier contrasts |
| Project-authored domain contrasts (Rounds 36, 60, 61) | 4,698 | Project-authored operational-damage vs. read-only pairs |
| Shell Safety v2 training split (MIT) | 1,398 | Dataset author's `allow` / `deny` labels |
| Explicit review / ask rows | 1,323 | Project-authored review track |

**No hosted language-model output (including TypeSafe Jev) was used as a training label, teacher target, filter, or selection signal.** No private logs or protected benchmark commands entered fitting, development, selection, or calibration (`Guard.assert_clean` verified against `evals/protected-19.json` plus external neutral isolation against `upstream-ssv2-suite` and `upstream-rogue-suite`).

## Evidence (`lancet-bench-3`, counted pass `use 067`)

v0.5.0 was scored once across all `11,859` frozen Bench 3 inputs in a complete inert singleton CPU pass (4 ONNX Runtime threads, zero commands executed).

| Suite | Status for v0.5.0 | Score | Risky caught | Safe interrupted | AUROC |
|---|---|---:|---:|---:|---:|
| **Bench 3 Core** (`3,423` risky / `3,423` safe) | **Unseen** | **71.31** | `71.31%` (`2,441/3,423`) | **`9.93%`** (`340/3,423`) | `0.8965` |
| **ShellRisk test** (`193` risky / `4,001` safe) | **In-distribution** | **70.47** | `70.47%` (`136/193`) | **`1.10%`** (`44/4,001`) | `0.9825` |
| **Neutral pool** (`229` risky / `360` safe: SSV2 test + Rogue) | **Unseen** | **55.90** | `55.90%` (`128/229`) | **`4.17%`** (`15/360`) | `0.9017` |
| **Weighted Overall** | Continuation vs. R25 `59.17` | **68.51** | — | **`5.13%`** pooled | — |

- **Paired uncertainty vs. Round 25 Preview (`59.17`):** `+9.342` points, 95% CI **`[+0.512, +12.766]`**.
- **Comparison vs. previous release `v0.4.3` (`43.44` on Bench 3):** `+25.07` overall points; unseen Core `27.36 → 71.31` (`30.8% → 9.93%` safe interruption).
- **Neutral detail (unseen):** SSV2 `58.89` (`58.9%` catch / `3.58%` safe int, AUROC `0.9350`); Rogue `37.41` (`44.9%` catch / `12.0%` safe int, AUROC `0.7225`).
- **Diagnostic tracks:** Robustness expected-action **`94.12%`**, Context ask `5.88%`, Chains `43.48%` whole-input catch at `7.14%` safe control interruption.
- **Export parity:** Native PyTorch vs. FP32 ONNX max absolute logit diff `3.55e-06` (risk) and `4.60e-06` (ask); all 4 input-rejection fixtures passed.
- **Speed:** `69.95 ms` median (`77.31 ms` mean, `103.94 ms` p95) on CPU (4 ONNX Runtime intra-op threads, batch 1) across all `11,859` commands. Observations depend on hardware and command length.

## Intended use and limitations

LANCET Nano v0.5.0 is a fast local component for **command-risk triage and review, not a security sandbox or execution authority**. Inputs are inert text; the model has no access to filesystem state, remote script contents, environment variables, or task intent.

- **Unseen Neutral & multi-step chains:** Novel phrasing outside shell operational idioms (Neutral `55.9%` catch) and multi-step attack chains (`43.5%` whole-input catch) remain harder than single/composed operational commands.
- **Conservative hard-block band:** At the shipped thresholds, ~98% of flagged risky commands return `review` (`ask`) rather than automatic `risky` (`block`), minimizing false hard blocks (`7/7,784` pooled). Integrations wanting stricter automatic blocking can treat `review` and `risky` uniformly as gated actions or lower `riskyLogitThreshold` locally.
- **In-distribution ShellRisk disclosure:** Because ShellRisk train+test were fitted per owner policy, ShellRisk numbers reflect in-distribution retention rather than unseen generalization.
- **`not_flagged` does not guarantee safety.** Every result carries `experimental: true` and `executionAuthorized: false`. These notices impose no extra license restriction.
