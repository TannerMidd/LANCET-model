# Experimental command-risk classifier

35.3M-parameter CodeT5 encoder; unsigned 8-bit ONNX weights and a byte-BPE
tokenizer. Local CPU inference only. Model input is Bash command text, not
instructions to execute. This program never runs its input.

Install the three packages in requirements.txt into a Python environment.
From this directory, pass one JSON object per line to:

```powershell
'{"command":"git status","shell":"bash"}' | python classify.py --model .
```

Outputs are `risky`, `not_flagged`, or `review` for unsupported/invalid inputs.
`not_flagged` is not a claim of safety. All results include `experimental: true`
and `executionAuthorized: false`. PowerShell and inputs beyond 512 tokens or
8,192 UTF-8 bytes require review; input is never silently truncated.

The recall95 threshold was fitted on a small, separate calibration partition.
Research results used previously inspected project tests with related variants;
the full project suite also contains fitting data. These results do not establish
production safety. Use independent evaluation before integration.

The classifier was initialized from Salesforce/codet5-small at revision
b1ee9570c289f21b5922b9c768a1ce12957bf968, then trained on project cases, authored
contrast pairs, and filtered source inspection examples. Upstream model:
https://huggingface.co/Salesforce/codet5-small/tree/b1ee9570c289f21b5922b9c768a1ce12957bf968
The source model card lists Apache-2.0; no blanket redistribution license is
asserted here for mixed training sources. This is a local research bundle.

Full protocol, results and limitations are in the project repository under
docs/research/command-risk-v5/. The trained weights, tokenizer and model metadata
are verified against export.json when loaded. No network request or model
download occurs during inference. Warm latency excludes process startup/loading.
