# LANCET licenses

LANCET has separate licenses for model assets and code. This is **not a blanket license for third-party training data**.

| Component | License | Governing notice |
|---|---|---|
| Released V5 weights, tokenizer and model metadata | **Apache-2.0** | [Model license and exact asset scope](MODEL-LICENSE.md); [full license](licenses/Apache-2.0.txt) |
| LANCET runtime and project-authored code, including release tooling | **MIT** | [Full retained notice](licenses/pi-jev-guard-MIT.txt), copyright (c) 2026 Tanner Middleton; upstream exceptions remain under their own notices |
| Separate CodeT5 source-project attribution | **BSD-3-Clause** | [Original Salesforce notice](licenses/CodeT5-BSD-3-Clause.txt); not substituted for the model's Apache-2.0 declaration |
| Runtime dependencies | Their own licenses | Installed separately; dependency distributions are not bundled |
| Third-party datasets and unreleased research checkpoints | **No license grant here** | [Source-specific provenance and limits](THIRD-PARTY-NOTICES.md) |

The model and runtime licenses permit use, modification and redistribution, including commercial use, subject to their respective terms. Preserve applicable notices and disclose modifications as required. The experimental/safety warnings are not additional license restrictions.

## Attribution and provenance

The base model is Salesforce/codet5-small at revision `b1ee9570c289f21b5922b9c768a1ce12957bf968`. Its [original model card](licenses/codet5-small-upstream-model-card.md) declares Apache-2.0. Credits and downstream changes are in [NOTICE.txt](NOTICE.txt), [MODIFICATIONS.md](MODIFICATIONS.md) and [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).

The verified V4/V5 fitting lineage contains project/authored examples and filtered SWE-smith, Terminal-Bench and NL2Bash inspection examples. Those three external sources declare MIT/Apache-2.0; the broader ShellRisk collection also contains other sources that were **not in these fitting pools**. The technical audit is not a guarantee of every upstream publisher's rights in underlying snippets or trajectories.

Original notices and frozen artifacts are unchanged. The earlier extraction-wide statement is retained in [licenses/history/LANCET-extraction-provenance.md](licenses/history/LANCET-extraction-provenance.md); its future-release wording describes the pre-release snapshot, not a restriction on the current explicit V5 model license.
