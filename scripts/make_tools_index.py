#!/usr/bin/env python3
import json, hashlib, sys, os

files = ["tools/verify_tbac.py","tools/generate_tbac.py"]

def b3(path):
    return hashlib.blake2s(open(path,"rb").read()).hexdigest()

idx = {
  "version": "tbac-tools-v1",
  "repo": "danvoulez/Trajectory-Engineering-Base",
  "files": [{"path": f, "b3": b3(f)} for f in files],
  "signature": None
}

open("tools-index.json","w").write(json.dumps(idx, indent=2))
print("WROTE tools-index.json")

