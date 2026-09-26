# LANCET Nano model license: Apache-2.0

Copyright (c) 2026 Tanner Middleton (LANCET-specific contributions).
Upstream rights and notices are retained. No ownership of upstream work is claimed.

LANCET Nano's fine-tuned model weights and associated model assets are distributed under the **Apache License, Version 2.0**. This includes LANCET's modifications to the upstream Salesforce CodeT5-base model. The original upstream model card also declares Apache-2.0.

## Covered assets

- `model/model-int8.onnx`
- `model/tokenizer.json`
- `model/model.json`
- `model/export.json`

This grant covers the LANCET Nano v0.3.0 release, whose ONNX SHA-256 is `b635571b0c55fba5224a00e2c9132918db816b76c433e8c8dc75d151ef03de1c`. It does not license other historical, shelved or unreleased research checkpoints. Earlier releases keep their own grants.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use these files except in compliance with the License. You may obtain a copy in [licenses/Apache-2.0.txt](licenses/Apache-2.0.txt) or at <https://www.apache.org/licenses/LICENSE-2.0>.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

Use, modification and redistribution, including commercial use, are permitted subject to the License. Preserve applicable licenses and attribution and change notices. [NOTICE.txt](NOTICE.txt) and [MODIFICATIONS.md](MODIFICATIONS.md) identify the upstream credits and LANCET's changes.

## Scope distinctions

- Runtime code (`classify.py`, `model/classify.py`, `verify_bundle.py`) remains **MIT**, not Apache-2.0. See [LICENSE.md](LICENSE.md).
- Third-party training data is **not** included or relicensed by this grant. See [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).
- Experimental-status and safety guidance describe the limits of the evidence. They are **not additional license restrictions**. No endorsement, safety certification or independent validation is implied.
