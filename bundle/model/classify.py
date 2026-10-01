"""LANCET Nano runtime: windowed ONNX + NumPy command-risk classifier for Bash, PowerShell and cmd.

Does not import torch/transformers. Reads JSON lines on stdin ({"command": "...", "shell": "bash"}) and prints one
JSON result per line. Commands are classified as inert text and are never executed.

Inference (format `semantic-windowed-1`): byte-level BPE ids are split into 512-token windows (510 payload tokens,
64-token overlap, framed by <s> ... </s>); the INT8 ONNX encoder runs one window at a time; NumPy takes the mean and
the maximum of every payload token exactly once across all windows, then applies the projection, LayerNorm and the
risk head. Long inputs are covered completely: nothing is truncated. Bands compare the risk logit with the shipped
logit thresholds; `score` is the calibrated probability reported alongside.

Copyright (c) 2026 Tanner Middleton. MIT License (see licenses/pi-jev-guard-MIT.txt).
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np
import onnxruntime as ort
from tokenizers import ByteLevelBPETokenizer

SHELLS = ("bash", "powershell", "cmd")
FILES = ("encoder-int8.onnx", "head.npz", "vocab.json", "merges.txt", "model.json")


def windows(payload, size=512, overlap=64, bos=1, eos=2):
    """Overlapping windows; `owned` marks each payload token exactly once."""
    capacity = size - 2
    if not payload or not 0 <= overlap < capacity:
        raise ValueError("Empty input or invalid window contract")
    result, start, previous_end = [], 0, 0
    while start < len(payload):
        end = min(len(payload), start + capacity)
        owned = [int(start + i >= previous_end) for i in range(end - start)]
        result.append(([bos, *payload[start:end], eos], [0, *owned, 0]))
        if end == len(payload):
            break
        previous_end, start = end, end - overlap
    if sum(sum(mask) for _, mask in result) != len(payload):
        raise ValueError("Every token must be pooled exactly once")
    return result


class LancetNano:
    def __init__(self, directory, threads=4):
        self.directory = Path(directory)
        export = json.loads((self.directory/"export.json").read_text(encoding="utf-8"))
        if not export.get("validationComplete"):
            raise ValueError("Incomplete export")
        for name in FILES:
            if hashlib.sha256((self.directory/name).read_bytes()).hexdigest() != export["sha256"][name]:
                raise ValueError("Artifact hash mismatch: "+name)
        self.meta = json.loads((self.directory/"model.json").read_text(encoding="utf-8"))
        if self.meta.get("format") != "semantic-windowed-1":
            raise ValueError("Unsupported model format: "+str(self.meta.get("format")))
        self.tokenizer = ByteLevelBPETokenizer(str(self.directory/"vocab.json"), str(self.directory/"merges.txt"))
        head = np.load(self.directory/"head.npz")
        self.projection = head["projection"].astype(np.float64)
        self.norm_weight, self.norm_bias = head["norm_weight"].astype(np.float64), head["norm_bias"].astype(np.float64)
        self.norm_eps = float(head["norm_eps"])
        self.head_weight, self.head_bias = head["head_weight"].astype(np.float64), head["head_bias"].astype(np.float64)
        contract = self.meta["input"]
        self.window_tokens, self.overlap, self.max_bytes = contract["windowTokens"], contract["overlapTokens"], contract["maxUtf8Bytes"]
        options = ort.SessionOptions()
        options.intra_op_num_threads = threads
        options.inter_op_num_threads = 1
        options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        self.session = ort.InferenceSession(str(self.directory/"encoder-int8.onnx"), sess_options=options,
                                            providers=["CPUExecutionProvider"])

    def reject(self, command, shell):
        if shell not in SHELLS:
            return "unsupported-shell"
        if not isinstance(command, str):
            return "command-not-string"
        if not command.strip():
            return "empty-command"
        if "\0" in command:
            return "nul-byte"
        try:
            size = len(command.encode("utf-8"))
        except UnicodeEncodeError:
            return "invalid-unicode"
        if size > self.max_bytes:
            return "raw-input-too-long"
        return None

    def logits(self, command):
        """[risk, ask] logits; the ask logit is a diagnostic and never sets the band."""
        ids = self.tokenizer.encode(command).ids
        total = np.zeros(self.projection.shape[0])
        maximum = np.full(self.projection.shape[0], -np.inf)
        count = 0
        for window_ids, owned in windows(ids, self.window_tokens, self.overlap):
            x = np.asarray([window_ids], dtype=np.int64)
            hidden = self.session.run(None, {"input_ids": x, "attention_mask": np.ones_like(x)})[0][0].astype(np.float64)
            mask = np.asarray(owned, dtype=bool)
            total += hidden[mask].sum(0)
            maximum = np.maximum(maximum, hidden[mask].max(0))
            count += int(mask.sum())
        z = self.projection @ np.concatenate([total/count, maximum])
        z = (z - z.mean())/math.sqrt(z.var() + self.norm_eps)*self.norm_weight + self.norm_bias
        out = self.head_weight @ z + self.head_bias
        if not np.isfinite(out).all():
            raise FloatingPointError("nonfinite-model-output")
        return out

    def score(self, command, shell="bash"):
        result = {"score": None, "classification": "review", "reason": self.reject(command, shell),
                  "reviewThreshold": self.meta["reviewThreshold"], "riskyThreshold": self.meta["riskyThreshold"],
                  "experimental": True, "executionAuthorized": False}
        if result["reason"]:
            return result
        try:
            risk, _ = self.logits(command)
        except FloatingPointError:
            return {**result, "reason": "nonfinite-model-output"}
        cal = self.meta["calibration"]
        z = cal["scale"]*risk + cal["bias"]
        score = 1/(1 + math.exp(-z)) if z >= 0 else math.exp(z)/(1 + math.exp(z))
        band = ("risky" if risk >= self.meta["riskyLogitThreshold"] else
                "review" if risk >= self.meta["reviewLogitThreshold"] else "not_flagged")
        return {**result, "score": score, "classification": band, "riskLogit": float(risk),
                "reason": "uncertainty-band" if band == "review" else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", type=Path, required=True, help="directory containing encoder-int8.onnx")
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
