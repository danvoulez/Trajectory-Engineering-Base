#!/usr/bin/env python3
"""Calcula BLAKE3 hash (fallback para SHA256 se blake3 não estiver disponível)"""
import sys
from pathlib import Path

try:
    import blake3
    hasher = blake3.blake3()
except ImportError:
    import hashlib
    hasher = hashlib.sha256()  # Fallback

file_path = Path(sys.argv[1])
with open(file_path, 'rb') as f:
    while chunk := f.read(8192):
        hasher.update(chunk)

print(hasher.hexdigest())
