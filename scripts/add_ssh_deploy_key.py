#!/usr/bin/env python3
"""
Adiciona chave SSH como Deploy Key usando GitHub App
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

try:
    import jwt
    import requests
except ImportError:
    print("Instalando dependências...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyJWT", "cryptography", "requests", "--quiet"])
    import jwt
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
GITHUB_APP_INSTALLATION_ID = env_vars.get("GITHUB_APP_INSTALLATION_ID")
PRIVATE_KEY_PATH = Path("minicontratos.2025-11-20.private-key.pem")

REPO_OWNER = "danvoulez"
REPO_NAME = "Trajectory-Engineering-Base"
BASE_URL = "https://api.github.com"

def load_private_key():
    """Carrega chave privada RSA"""
    if not PRIVATE_KEY_PATH.exists():
        print(f"✗ Chave privada não encontrada: {PRIVATE_KEY_PATH}")
        sys.exit(1)
    
    with open(PRIVATE_KEY_PATH, 'r') as f:
        return f.read()

def generate_jwt():
    """Gera JWT para autenticação do GitHub App"""
    private_key = load_private_key()
    
    now = int(time.time())
    payload = {
        'iat': now - 60,  # Issued at time (60 seconds ago to account for clock skew)
        'exp': now + 600,  # Expires in 10 minutes
        'iss': GITHUB_APP_ID  # GitHub App ID
    }
    
    token = jwt.encode(payload, private_key, algorithm='RS256')
    return token

def get_installation_token():
    """Obtém token de instalação do GitHub App"""
    jwt_token = generate_jwt()
    
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    url = f"{BASE_URL}/app/installations/{GITHUB_APP_INSTALLATION_ID}/access_tokens"
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    
    return response.json()['token']

def get_ssh_public_key():
    """Lê chave pública SSH"""
    ssh_key_path = Path.home() / ".ssh" / "id_ed25519_github.pub"
    
    if not ssh_key_path.exists():
        print(f"✗ Chave SSH não encontrada: {ssh_key_path}")
        print("  Execute: ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_github")
        sys.exit(1)
    
    return ssh_key_path.read_text().strip()

def add_deploy_key(token, title, key):
    """Adiciona deploy key ao repositório"""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    url = f"{BASE_URL}/repos/{REPO_OWNER}/{REPO_NAME}/keys"
    data = {
        'title': title,
        'key': key,
        'read_only': False  # Permite write access
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        return True, response.json()
    elif response.status_code == 422:
        # Pode ser que a chave já exista
        error = response.json()
        if 'key' in str(error) and 'already' in str(error).lower():
            return False, "Chave já existe"
        return False, error
    else:
        response.raise_for_status()
        return False, response.json()

def main():
    print("🔐 Adicionando chave SSH como Deploy Key via GitHub App...\n")
    
    # 1. Obter token
    print("1. Obtendo token de instalação...")
    try:
        token = get_installation_token()
        print("   ✓ Token obtido")
    except Exception as e:
        print(f"   ✗ Erro ao obter token: {e}")
        sys.exit(1)
    
    # 2. Ler chave SSH
    print("\n2. Lendo chave SSH...")
    try:
        ssh_key = get_ssh_public_key()
        print("   ✓ Chave SSH lida")
        print(f"   Fingerprint: {ssh_key.split()[1][:20]}...")
    except Exception as e:
        print(f"   ✗ Erro: {e}")
        sys.exit(1)
    
    # 3. Adicionar deploy key
    print("\n3. Adicionando deploy key...")
    title = f"Trajectory Engineering - {datetime.now().strftime('%Y-%m-%d')}"
    
    try:
        success, result = add_deploy_key(token, title, ssh_key)
        if success:
            print(f"   ✓ Deploy key adicionada: {result.get('title', title)}")
            print(f"   ID: {result.get('id')}")
        else:
            if isinstance(result, str) and "já existe" in result:
                print(f"   ⚠ {result}")
                print("   A chave já está configurada no repositório")
            else:
                print(f"   ✗ Erro: {result}")
                sys.exit(1)
    except Exception as e:
        print(f"   ✗ Erro ao adicionar deploy key: {e}")
        sys.exit(1)
    
    print("\n✅ Deploy key configurada com sucesso!")
    print("\n📝 Próximos passos:")
    print("   1. Configure SSH localmente:")
    print("      eval \"$(ssh-agent -s)\"")
    print("      ssh-add ~/.ssh/id_ed25519_github")
    print("")
    print("   2. Teste conexão:")
    print("      ssh -T git@github.com")
    print("")
    print("   3. Atualize remote para SSH:")
    print("      git remote set-url origin git@github.com:danvoulez/Trajectory-Engineering-Base.git")

if __name__ == "__main__":
    main()

