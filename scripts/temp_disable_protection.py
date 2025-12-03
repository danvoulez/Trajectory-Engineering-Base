#!/usr/bin/env python3
"""Temporariamente desabilita status check obrigatório para permitir primeiro push do workflow"""
import sys
from pathlib import Path
import subprocess

try:
    import jwt
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyJWT", "cryptography", "requests", "--quiet"])
    import jwt
    import requests

env_path = Path(".env")
env_vars = {}
with open(env_path) as f:
    for line in f:
        if "=" in line and not line.strip().startswith("#"):
            key, value = line.strip().split("=", 1)
            env_vars[key] = value

GITHUB_APP_ID = env_vars.get("GITHUB_APP_ID")
GITHUB_APP_INSTALLATION_ID = env_vars.get("GITHUB_APP_INSTALLATION_ID")
PRIVATE_KEY_PATH = Path("minicontratos.2025-11-20.private-key.pem")

def load_private_key():
    with open(PRIVATE_KEY_PATH, 'r') as f:
        return f.read()

def generate_jwt():
    import time
    private_key = load_private_key()
    now = int(time.time())
    payload = {'iat': now - 60, 'exp': now + 600, 'iss': GITHUB_APP_ID}
    return jwt.encode(payload, private_key, algorithm='RS256')

def get_installation_token():
    jwt_token = generate_jwt()
    headers = {'Authorization': f'Bearer {jwt_token}', 'Accept': 'application/vnd.github.v3+json'}
    url = f"https://api.github.com/app/installations/{GITHUB_APP_INSTALLATION_ID}/access_tokens"
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    return response.json()['token']

# Desabilita status check obrigatório temporariamente
token = get_installation_token()
headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github+json'}
url = "https://api.github.com/repos/danvoulez/Trajectory-Engineering-Base/branches/main/protection"

# Lê proteção atual
resp = requests.get(url, headers=headers)
current = resp.json()

# Remove status checks obrigatórios temporariamente
data = current.copy()
data['required_status_checks'] = None

resp = requests.put(url, headers=headers, json=data)
if resp.status_code == 200:
    print("✓ Status check temporariamente desabilitado")
    print("  Faça o push e depois reative com: python3 scripts/protect_branch_api.py")
else:
    print(f"✗ Erro: {resp.json()}")

