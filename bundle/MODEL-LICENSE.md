# LANCET V5 model license — Apache-2.0

Copyright (c) 2026 Tanner Middleton (LANCET-specific contributions).
Upstream rights and notices are retained; no ownership of upstream work is claimed.

LANCET V5's fine-tuned model weights and associated model assets are distributed under the **Apache License, Version 2.0**. This includes LANCET's modifications to the upstream Salesforce CodeT5-small model. The original upstream model card also declares Apache-2.0.

## Covered assets

- `model/model-int8.onnx`
- `model/tokenizer.json`
- `model/model.json`
- `model/export.json`
- `model/checksums.json`

This grant covers the V5 `codet5-balanced` / `recall95` release, whose ONNX SHA-256 is `e8f2e75580a435eba9744b4a8f14dc851f7c71e579c344bde75dee047f7c07a3`. It does not silently license other historical or unreleased research checkpoints.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use these files except in compliance with the License. You may obtain a copy in [licenses/Apache-2.0.txt](licenses/Apache-2.0.txt) or at <https://www.apache.org/licenses/LICENSE-2.0>.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

Use, modification and redistribution, including commercial use, are permitted subject to the License. Preserve applicable licenses and attribution/change notices. [NOTICE.txt](NOTICE.txt) and [MODIFICATIONS.md](MODIFICATIONS.md) identify upstream credits and LANCET's changes.

## Scope distinctions

- Runtime code, including `classify.py` and `model/classify.py`, remains **MIT**, not Apache-2.0. See [LICENSE.md](LICENSE.md).
- Third-party training data is **not** included or relicensed by this grant. Dataset license declarations do not certify rights in every underlying third-party snippet. See [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).
- Historical extraction/bundle documents describing an unlicensed local research snapshot are preserved unchanged for provenance. This is the current model-specific license grant; those historical descriptions do not add restrictions to it.
- Experimental-status and safety guidance are limitations of the evidence, **not additional license restrictions**. No endorsement, safety certification or independent validation is implied.
