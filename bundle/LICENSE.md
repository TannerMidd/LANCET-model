# LANCET licenses

LANCET has separate licenses for model assets and code. This is **not a blanket license for third-party training data**.

| Component | License | Governing notice |
|---|---|---|
| LANCET Nano weights, tokenizer and model metadata | **Apache-2.0** | [Model license and exact asset scope](MODEL-LICENSE.md); [full license](licenses/Apache-2.0.txt) |
| LANCET runtime and project-authored code | **MIT** | [Full notice](licenses/pi-jev-guard-MIT.txt), copyright (c) 2026 Tanner Middleton |
| Separate CodeT5 source-project attribution | **BSD-3-Clause** | [Original Salesforce notice](licenses/CodeT5-BSD-3-Clause.txt); does not replace the model's Apache-2.0 declaration |
| Runtime dependencies | Their own licenses | Installed separately; not bundled |
| Third-party datasets and unreleased research checkpoints | **No license grant here** | [Source-specific provenance and limits](THIRD-PARTY-NOTICES.md) |

The model and runtime licenses permit use, modification and redistribution, including commercial use, subject to their terms. Preserve the applicable notices. The experimental and safety warnings are not additional license restrictions.

## Attribution and provenance

The base model is Salesforce/codet5-small at revision `b1ee9570c289f21b5922b9c768a1ce12957bf968`; its [original model card](licenses/codet5-small-upstream-model-card.md) declares Apache-2.0.

Nano continues LANCET V5 (v0.1.0). It adds training on commands from **tldr-pages** (CC BY 4.0) and on AWS CLI command shapes from **botocore** service models (Apache-2.0). Credits and changes are in [NOTICE.txt](NOTICE.txt), [MODIFICATIONS.md](MODIFICATIONS.md) and [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).

The earlier extraction-wide statement is retained unchanged in [licenses/history/LANCET-extraction-provenance.md](licenses/history/LANCET-extraction-provenance.md). Its future-release wording describes a pre-release snapshot, not a restriction on this grant.
