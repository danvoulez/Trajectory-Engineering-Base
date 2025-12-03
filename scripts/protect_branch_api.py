#!/usr/bin/env python3
"""
Configura branch protection via GitHub API
"""

import os
import sys
import subprocess
from pathlib import Path

try:
    import jwt
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyJWT", "cryptography", "requests", "--quiet"])
    import jwt
    import requests

# Carrega credenciais
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

REPO_OWNER = "danvoulez"
REPO_NAME = "Trajectory-Engineering-Base"
BASE_URL = "https://api.github.com"

def load_private_key():
    with open(PRIVATE_KEY_PATH, 'r') as f:
        return f.read()

def generate_jwt():
    import time
    private_key = load_private_key()
    now = int(time.time())
    payload = {
        'iat': now - 60,
        'exp': now + 600,
        'iss': GITHUB_APP_ID
    }
    return jwt.encode(payload, private_key, algorithm='RS256')

def get_installation_token():
    jwt_token = generate_jwt()
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = f"{BASE_URL}/app/installations/{GITHUB_APP_INSTALLATION_ID}/access_tokens"
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    return response.json()['token']

def protect_branch(token):
    """Configura branch protection"""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github+json'
    }

    url = f"{BASE_URL}/repos/{REPO_OWNER}/{REPO_NAME}/branches/main/protection"

    data = {
        "required_status_checks": {
            "strict": True,
            "contexts": ["check"]
        },
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": True,
            "required_approving_review_count": 1,
            "require_code_owner_reviews": True
        },
        "restrictions": None,
        "required_linear_history": True,
        "allow_force_pushes": False,
        "allow_deletions": False
    }

    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 200:
        return True, response.json()
    else:
        return False, response.json()

def main():
    print("🔒 Configurando branch protection via GitHub App...\n")

    try:
        token = get_installation_token()
        print("✓ Token obtido")

        success, result = protect_branch(token)
        if success:
            print("✓ Branch protection configurada com sucesso!")
            print(f"\nConfigurações:")
            print(f"  - Require PR: ✓")
            print(f"  - Require 1 approval: ✓")
            print(f"  - Require Code Owners: ✓")
            print(f"  - Require status check 'check': ✓")
            print(f"  - Require linear history: ✓")
            print(f"  - Block force pushes: ✓")
            print(f"  - Block deletions: ✓")
        else:
            print(f"✗ Erro: {result}")
            sys.exit(1)
    except Exception as e:
        print(f"✗ Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
