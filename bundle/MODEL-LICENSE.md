# LANCET Nano model license: Apache-2.0

Copyright (c) 2026 Tanner Middleton (LANCET-specific contributions).
Upstream rights and notices are retained. No ownership of upstream work is claimed.

LANCET Nano's fine-tuned model weights and associated model assets are distributed under the **Apache License, Version 2.0**. This includes LANCET's modifications to the upstream Salesforce CodeT5+ 220M model. The upstream model is released under the BSD-3-Clause license; its copyright notice, conditions and disclaimer are retained in [licenses/CodeT5-BSD-3-Clause.txt](licenses/CodeT5-BSD-3-Clause.txt) and continue to apply to the upstream portions.

## Covered assets

- `model/encoder-int8.onnx`
- `model/head.npz`
- `model/vocab.json` and `model/merges.txt`
- `model/model.json`
- `model/export.json`

This grant covers the LANCET Nano v0.4.3 release, whose ONNX encoder SHA-256 is `4e7d6a53d27a7321a2638a4bf446301e8e343c51000963331469e3ab20aae2a4`. It does not license other historical, shelved or unreleased research checkpoints. Earlier releases keep their own grants.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use these files except in compliance with the License. You may obtain a copy in [licenses/Apache-2.0.txt](licenses/Apache-2.0.txt) or at <https://www.apache.org/licenses/LICENSE-2.0>.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

Use, modification and redistribution, including commercial use, are permitted subject to the License and the retained BSD-3-Clause notice. [NOTICE.txt](NOTICE.txt) and [MODIFICATIONS.md](MODIFICATIONS.md) identify the upstream credits and LANCET's changes.

## Scope distinctions

- Runtime code (`classify.py`, `model/classify.py`, `verify_bundle.py`) remains **MIT**, not Apache-2.0. See [LICENSE.md](LICENSE.md).
- Third-party training data is **not** included or relicensed by this grant. See [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).
- The names of Salesforce and the CodeT5 contributors are not used to endorse or promote this model.
- Experimental-status and safety guidance are **not additional license restrictions**.
