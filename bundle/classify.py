"""ONNX + byte-BPE classifier runtime. Does not import torch/transformers."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer


class PortableV4:
    def __init__(self,directory,int8=True):
        self.directory=Path(directory)
        self.meta=json.loads((self.directory/"model.json").read_text(encoding="utf-8"))
        self.export=json.loads((self.directory/"export.json").read_text(encoding="utf-8"))
        filename="model-int8.onnx" if int8 else "model.onnx"
        for name in (filename,"tokenizer.json","model.json"):
            actual=hashlib.sha256((self.directory/name).read_bytes()).hexdigest()
            if actual!=self.export["sha256"][name]:
                raise ValueError("Artifact hash mismatch: "+name)
        self.tokenizer=Tokenizer.from_file(str(self.directory/"tokenizer.json"))
        self.tokenizer.encode_special_tokens=True
        options=ort.SessionOptions()
        options.intra_op_num_threads=4
        options.inter_op_num_threads=1
        self.session=ort.InferenceSession(str(self.directory/filename),sess_options=options,providers=["CPUExecutionProvider"])

    def encode(self,command,shell="bash"):
        if shell!="bash":
            return None,"unsupported-shell"
        if not isinstance(command,str):
            return None,"command-not-string"
        if not command.strip():
            return None,"empty-command"
        if "\0" in command:
            return None,"nul-byte"
        if len(command.encode("utf-8"))>self.meta["maxRawBytes"]:
            return None,"raw-input-too-long"
        ids=self.tokenizer.encode(command,add_special_tokens=False).ids
        bos,eos=self.tokenizer.token_to_id("<s>"),self.tokenizer.token_to_id("</s>")
        prefix=[bos,self.tokenizer.token_to_id("<encoder-only>"),eos] if self.meta["kind"]=="unixcoder" else [bos]
        ids=prefix+ids+[eos]
        if len(ids)>self.meta["maxTokens"]:
            return None,"token-input-too-long"
        return ids,None

    def score(self,command,shell="bash"):
        ids,reason=self.encode(command,shell)
        result={"score":None,"threshold":self.meta["threshold"],"classification":"review","reason":reason,
                "experimental":True,"executionAuthorized":False}
        if ids is None:
            return result
        inputs=np.array([ids],dtype=np.int64)
        logit=float(self.session.run(None,{"ids":inputs,"mask":np.ones_like(inputs)})[0][0])
        cal=self.meta["calibration"]
        score=float(1/(1+np.exp(-np.clip(logit*cal["scale"]+cal["bias"],-60,60))))
        return {**result,"score":score,"classification":"risky" if score>=self.meta["threshold"] else "not_flagged"}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model",type=Path,required=True)
    parser.add_argument("--fp32",action="store_true")
    args=parser.parse_args()
    predictor=PortableV4(args.model,not args.fp32)
    for line in sys.stdin:
        try:
            row=json.loads(line)
            result=predictor.score(row["command"],row.get("shell","bash"))
        except (KeyError,TypeError,ValueError) as exc:
            result={"score":None,"classification":"review","reason":"invalid-input: "+str(exc),
                    "experimental":True,"executionAuthorized":False}
        print(json.dumps(result,ensure_ascii=False,allow_nan=False),flush=True)


if __name__=="__main__":
    main()
