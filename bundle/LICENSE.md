# LANCET licenses

LANCET has separate licenses for model assets and code. This is **not a blanket license for third-party training data**.

| Component | License | Governing notice |
|---|---|---|
| LANCET Nano weights, tokenizer and model metadata | **Apache-2.0** | [Model license and exact asset scope](MODEL-LICENSE.md); [full license](licenses/Apache-2.0.txt) |
| Upstream Salesforce CodeT5+ 220M model | **BSD-3-Clause** | [Original Salesforce notice](licenses/CodeT5-BSD-3-Clause.txt); [upstream model card](licenses/codet5p-220m-upstream-model-card.md) |
| LANCET runtime and project-authored code | **MIT** | [Full notice](licenses/pi-jev-guard-MIT.txt), copyright (c) 2026 Tanner Middleton |
| Runtime dependencies | Their own licenses | Installed separately; not bundled |
| Third-party datasets and unreleased research checkpoints | **No license grant here** | [Source-specific provenance](THIRD-PARTY-NOTICES.md) |

The model and runtime licenses permit use, modification and redistribution, including commercial use, subject to their terms. Preserve the applicable notices. The experimental and safety warnings are not additional license restrictions.

## Attribution and provenance

The base model is Salesforce/codet5p-220m at revision `2b92f36e2782341a50551759fdba0dd15e821f99`; its [original model card](licenses/codet5p-220m-upstream-model-card.md) declares BSD-3-Clause. The tokenizer file is byte-identical to the CodeT5 tokenizer shipped with earlier LANCET releases ([card](licenses/codet5-small-upstream-model-card.md)).

Nano v0.4.1 (the v0.4.0 weights with a new review threshold) is trained from that upstream base, not from an earlier LANCET checkpoint. It uses commands from **tldr-pages** (CC BY 4.0), AWS CLI command shapes from **botocore** (Apache-2.0), reference examples from the **Azure CLI** and **GitHub CLI** (MIT) and **kubectl** and **Docker CLI** (Apache-2.0), and rows from the **ShellRisk-Bench** training split. It also uses project-authored material. Credits and changes are in [NOTICE.txt](NOTICE.txt), [MODIFICATIONS.md](MODIFICATIONS.md) and [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).

The earlier extraction-wide statement is retained unchanged in [licenses/history/LANCET-extraction-provenance.md](licenses/history/LANCET-extraction-provenance.md). Its future-release wording describes a pre-release snapshot, not a restriction on this grant.
