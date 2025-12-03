#!/usr/bin/env python3
"""Valida sintaxe do OpenAPI"""
import sys
import yaml
from pathlib import Path

try:
    with open('openapi/diamond.yaml', 'r', encoding='utf-8') as f:
        yaml.safe_load(f)
    print('openapi ok')
    sys.exit(0)
except Exception as e:
    print(f'openapi error: {e}')
    sys.exit(1)

