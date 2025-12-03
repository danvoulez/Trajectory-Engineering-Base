#!/usr/bin/env python3
"""
Configura repositório GitHub via API:
- Release v1.0.0
- Descrição, website, topics
- Issues iniciais
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "--quiet"])
    import requests

# Carrega credenciais
env_path = Path(".env")
if not env_path.exists():
    print("✗ Arquivo .env não encontrado")
    sys.exit(1)

env_vars = {}
with open(env_path) as f:
    for line in f:
        if "=" in line and not line.strip().startswith("#"):
            key, value = line.strip().split("=", 1)
            env_vars[key] = value

GITHUB_APP_ID = env_vars.get("GITHUB_APP_ID")
GITHUB_CLIENT_ID = env_vars.get("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = env_vars.get("GITHUB_CLIENT_SECRET")
GITHUB_APP_INSTALLATION_ID = env_vars.get("GITHUB_APP_INSTALLATION_ID")

REPO = "danvoulez/Trajectory-Engeneering-Base"
BASE_URL = "https://api.github.com"

def get_installation_token():
    """Obtém token de instalação do GitHub App"""
    # Para simplificar, vamos usar um token pessoal ou OAuth
    # GitHub App requer JWT signing, então vamos usar uma abordagem mais simples
    print("⚠ Usando GitHub CLI ou token pessoal (configure GITHUB_TOKEN)")
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("  Configure: export GITHUB_TOKEN=seu_token")
        return None
    return token

def api_request(method, endpoint, token, data=None):
    """Faz requisição à API do GitHub"""
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    if method == "GET":
        resp = requests.get(url, headers=headers)
    elif method == "PATCH":
        resp = requests.patch(url, headers=headers, json=data)
    elif method == "POST":
        resp = requests.post(url, headers=headers, json=data)
    elif method == "PUT":
        resp = requests.put(url, headers=headers, json=data)

    resp.raise_for_status()
    return resp.json() if resp.content else {}

def main():
    token = get_installation_token()
    if not token:
        print("\n📝 Para usar GitHub API, configure:")
        print("   export GITHUB_TOKEN=seu_token_pessoal")
        print("\n   Ou use GitHub CLI:")
        print("   gh auth login")
        print("   gh release create v1.0.0 --notes-file CHANGELOG.md")
        return

    print("Configurando repositório GitHub...\n")

    # 1. Atualizar descrição e topics
    print("1. Configurando descrição e topics...")
    repo_data = {
        "description": "Baseline for Trajectory Engineering: JSON✯Atomic schemas, OpenAPI, CLIs, examples",
        "topics": ["trajectory", "json-atomic", "diamond", "audit", "ai-training", "merkle", "blake3", "ed25519"]
    }
    try:
        api_request("PATCH", f"/repos/{REPO}", token, repo_data)
        print("   ✓ Descrição e topics atualizados")
    except Exception as e:
        print(f"   ⚠ Erro: {e}")

    # 2. Criar release v1.0.0
    print("\n2. Criando release v1.0.0...")
    changelog = Path("CHANGELOG.md").read_text()
    release_notes = changelog.split("## [1.0.0]")[1].split("##")[0].strip() if "## [1.0.0]" in changelog else changelog

    release_data = {
        "tag_name": "v1.0.0",
        "name": "Diamond Baseline v1.0.0",
        "body": release_notes,
        "draft": False,
        "prerelease": False
    }

    try:
        api_request("POST", f"/repos/{REPO}/releases", token, release_data)
        print("   ✓ Release v1.0.0 criada")
    except Exception as e:
        print(f"   ⚠ Erro: {e}")

    # 3. Criar issues iniciais
    print("\n3. Criando issues iniciais...")
    issues = [
        {
            "title": "Spec Freeze v1 (breaking só na v2)",
            "body": "Congelar especificações da v1. Mudanças breaking apenas na v2."
        },
        {
            "title": "AuditSet/EvalSuite v1 (chatlogs)",
            "body": "Criar AuditSet e EvalSuite v1 para chatlogs com seeds/hashes selados."
        },
        {
            "title": "Proto-CLIs (tcap/unote/spent/diamante; dry-run)",
            "body": "Implementar CLIs prototipais para tcap, unote, spent e diamante (modo dry-run)."
        }
    ]

    for issue in issues:
        try:
            api_request("POST", f"/repos/{REPO}/issues", token, issue)
            print(f"   ✓ Issue criada: {issue['title']}")
        except Exception as e:
            print(f"   ⚠ Erro ao criar issue '{issue['title']}': {e}")

    print("\n✓ Configuração concluída!")

if __name__ == "__main__":
    main()
