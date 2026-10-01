"""Verify release file hashes without loading a model or executing model inputs."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def verify_bundle(directory, strict=False):
    root = Path(directory).resolve()
    manifest = json.loads((root / "RELEASE-MANIFEST.json").read_text(encoding="utf-8"))
    if manifest.get("releaseSchemaVersion") != 2 or not isinstance(manifest.get("files"), dict):
        raise ValueError("Unsupported release manifest")
    if manifest.get("modelLicense") != "Apache-2.0" or manifest.get("runtimeLicense") != "MIT":
        raise ValueError("Unexpected release license declarations")
    if manifest["files"].get(manifest.get("modelFile", "model/model-int8.onnx")) != manifest.get("modelSha256"):
        raise ValueError("Inconsistent model fingerprint")
    if not manifest["files"]:
        raise ValueError("Empty release manifest")
    for name, expected in manifest["files"].items():
        posix = PurePosixPath(name)
        if (not name or "\\" in name or ":" in name or posix.is_absolute()
                or ".." in posix.parts or posix.as_posix() != name
                or name == "RELEASE-MANIFEST.json"):
            raise ValueError("Invalid manifest path")
        path = (root / name).resolve()
        if not path.is_relative_to(root):
            raise ValueError("Manifest path escapes bundle")
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise ValueError("Invalid SHA-256 fingerprint")
        if not path.is_file() or digest(path) != expected:
            raise ValueError("Missing or changed release file: " + name)
    extra = sorted(p.relative_to(root).as_posix() for p in root.rglob("*")
                   if p.is_file() and p.relative_to(root).as_posix()
                   not in {*manifest["files"], "RELEASE-MANIFEST.json"})
    if strict and extra:
        raise ValueError("Unlisted files in strict verification")
    return {"verifiedFiles": len(manifest["files"]), "modelSha256": manifest["modelSha256"],
            "unlistedFiles": len(extra), "inferencePerformed": False,
            "modelLicense": manifest["modelLicense"], "runtimeLicense": manifest["runtimeLicense"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--strict", action="store_true", help="Reject unlisted files, including environments/caches")
    args = parser.parse_args()
    print(json.dumps(verify_bundle(args.directory, args.strict), indent=2))


if __name__ == "__main__":
    main()
