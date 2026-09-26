"""LANCET Nano runtime: ONNX + byte-BPE Bash command-risk classifier. Does not import torch/transformers.

Reads JSON lines on stdin ({"command": "...", "shell": "bash"}) and prints one JSON result per line.
Commands are classified as inert text and are never executed.

Copyright (c) 2026 Tanner Middleton. MIT License (see licenses/pi-jev-guard-MIT.txt).
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer


class LancetNano:
    def __init__(self, directory, threads=4):
        self.directory = Path(directory)
        self.meta = json.loads((self.directory/"model.json").read_text(encoding="utf-8"))
        export = json.loads((self.directory/"export.json").read_text(encoding="utf-8"))
        if not export.get("validationComplete"):
            raise ValueError("Incomplete export")
        for name in ("model-int8.onnx", "tokenizer.json", "model.json"):
            if hashlib.sha256((self.directory/name).read_bytes()).hexdigest() != export["sha256"][name]:
                raise ValueError("Artifact hash mismatch: "+name)
        self.tokenizer = Tokenizer.from_file(str(self.directory/"tokenizer.json"))
        self.tokenizer.encode_special_tokens = True
        options = ort.SessionOptions()
        options.intra_op_num_threads = threads
        options.inter_op_num_threads = 1
        self.session = ort.InferenceSession(str(self.directory/"model-int8.onnx"), sess_options=options,
                                            providers=["CPUExecutionProvider"])

    def encode(self, command, shell="bash"):
        if shell != "bash":
            return None, "unsupported-shell"
        if not isinstance(command, str):
            return None, "command-not-string"
        if not command.strip():
            return None, "empty-command"
        if "\0" in command:
            return None, "nul-byte"
        try:
            size = len(command.encode("utf-8"))
        except UnicodeEncodeError:
            return None, "invalid-unicode"
        if size > self.meta["maxRawBytes"]:
            return None, "raw-input-too-long"
        ids = ([self.tokenizer.token_to_id("<s>")] + self.tokenizer.encode(command, add_special_tokens=False).ids
               + [self.tokenizer.token_to_id("</s>")])
        if len(ids) > self.meta["maxTokens"]:
            return None, "token-input-too-long"  # never silently truncate a possibly dangerous suffix
        return ids, None

    def score(self, command, shell="bash"):
        ids, reason = self.encode(command, shell)
        result = {"score": None, "classification": "review", "reason": reason,
                  "reviewThreshold": self.meta["reviewThreshold"], "riskyThreshold": self.meta["riskyThreshold"],
                  "experimental": True, "executionAuthorized": False}
        if ids is None:
            return result
        inputs = np.array([ids], dtype=np.int64)
        logit = float(self.session.run(None, {"ids": inputs, "mask": np.ones_like(inputs)})[0][0])
        if not np.isfinite(logit):
            return {**result, "reason": "nonfinite-model-output"}
        cal = self.meta["calibration"]
        score = float(1/(1+np.exp(-np.clip(logit*cal["scale"]+cal["bias"], -60, 60))))
        band = ("risky" if score >= self.meta["riskyThreshold"] else
                "review" if score >= self.meta["reviewThreshold"] else "not_flagged")
        return {**result, "score": score, "classification": band, "reason": "uncertainty-band" if band == "review" else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", type=Path, required=True, help="directory containing model-int8.onnx")
    parser.add_argument("--threads", type=int, default=4)
    args = parser.parse_args()
    predictor = LancetNano(args.model, args.threads)
    for line in sys.stdin:
        try:
            row = json.loads(line)
            result = predictor.score(row["command"], row.get("shell", "bash"))
        except (KeyError, TypeError, ValueError) as exc:
            result = {"score": None, "classification": "review", "reason": "invalid-input: "+str(exc),
                      "experimental": True, "executionAuthorized": False}
        print(json.dumps(result, ensure_ascii=False, allow_nan=False), flush=True)


if __name__ == "__main__":
    main()
